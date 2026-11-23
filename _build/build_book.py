# -*- coding: utf-8 -*-
"""Typeset the KDP paperback interior (6 x 9 in, black ink) with Chromium."""
import os, re, html, io, base64, json, datetime
from PIL import Image, ImageOps, ImageEnhance
import qrcode, qrcode.image.svg
from pypdf import PdfReader
from playwright.sync_api import sync_playwright
import content, guide

E = html.escape
ALL = {a['slug']: a for a in content.build()}
OUTDIR = 'book'; os.makedirs(f'{OUTDIR}/img', exist_ok=True)
YEAR = datetime.date.today().year
AUTHOR = os.environ.get('SA_AUTHOR', 'The Better Daily')

PARTS = [
 ('One', 'Aartis', 'आरती', 'ganesha',
  "Fifteen aartis, beginning with Ganesha, who is always worshipped first. The refrain that is repeated after each stanza is printed after every stanza, exactly where it is sung.",
  ['jai-ganesh-deva','sukhkarta-dukhharta','om-jai-jagdish-hare','om-jai-lakshmi-mata','om-jai-shiv-omkara','jai-ambe-gauri','ambe-tu-hai-jagdambe-kali',
   'aarti-kije-hanuman-lala-ki','aarti-kunj-bihari-ki','jai-saraswati-mata','jai-lakshmi-ramana','jai-kashyap-nandan','jai-jai-shri-shanidev','aarti-shri-sai-guruvar-ki','om-jai-gange-mata']),
 ('Two', 'Chalisas', 'चालीसा', 'hanuman',
  "A chalisa is a hymn of forty verses (chaupais), opened and closed by couplets (dohas). There is no refrain: read straight through.",
  ['hanuman-chalisa','shiv-chalisa','durga-chalisa','shani-chalisa']),
 ('Three', 'Stutis and Mantras', 'स्तुति एवं मन्त्र', 'ram',
  "Hymns of praise and Sanskrit mantras that are often recited alongside the aarti, at festivals or as a daily practice.",
  ['shri-ramchandra-kripalu','sundar-kand-key-verses','ya-devi-sarvabhuteshu','sarva-mangala-mangalye','maha-mrityunjaya-mantra','gayatri-mantra',
   'shantakaram-bhujagashayanam','gajananam-bhutaganadi','manojavam-marutatulyavegam','krishnaya-vasudevaya']),
 ('Four', 'Prayers for Every Day', 'नित्य प्रार्थना', 'saraswati',
  "Short verses for the moments of an ordinary day: waking, lighting the lamp, eating, studying. They are ideal first prayers for children.",
  ['karagre-vasate-lakshmi','shubham-karoti','brahmarpanam','ya-kundendu-saraswati-vandana','guru-brahma','vakratunda-mahakaya','asato-ma-sadgamaya','om-purnamadah']),
 ('Five', 'Closing the Puja', 'पूजा समापन', 'shivparivar',
  "Recited after the aarti, while the flame still burns and before the prasad is shared.",
  ['karpur-gauram','tvameva-mata','kshama-prarthana','sarve-bhavantu-sukhinah','shanti-path']),
 ('Six', 'Vrat Katha', 'व्रत कथा', 'karvachauth',
  "A vrat katha is the story told on the day of a fast. This is the story of Karva Chauth.",
  ['karva-chauth-vrat-katha']),
]
ORDER = [s for p in PARTS for s in p[5]]
assert set(ORDER) == set(ALL), set(ALL) ^ set(ORDER)
SHORT = {k for k in ALL if ALL[k]['kind'] in ('shloka','mantra') and len(ALL[k]['stanzas']) == 1}

# ---------- images ----------
def prep_image(name, big=False):
    """Greyscale JPEG at 300 dpi for its printed size (Gemini line art from book/art/)."""
    if not name: return None
    art = f'{OUTDIR}/art/{name}.png'
    src = art if os.path.exists(art) else f'img_orig/{name}.png'
    if not os.path.exists(src): return None
    out = f'{OUTDIR}/img/{name}_{"L" if big else "S"}.jpg'
    im = Image.open(src).convert('L')
    if src.startswith('img_orig'):
        im = ImageOps.autocontrast(im, cutoff=1)
    im.thumbnail((1000, 1150) if big else (420, 520), Image.LANCZOS)
    im.save(out, 'JPEG', quality=80, optimize=True, dpi=(300, 300))
    return os.path.abspath(out)

def qr_svg(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=0)
    s = img.to_string(encoding='unicode')
    return re.sub(r'^<\?xml[^>]*>', '', s)

# ---------- html pieces ----------
def mark(token):  # invisible locator used to read back page numbers
    return f'<span class="mk">§{token}§</span>'

def stanza(a, s):
    lab = f'<div class="lab">{E(s["label"])}</div>' if s.get('label') else ''
    hi, tr = s['hi'], s.get('tr') or ''
    if a['kind'] == 'chalisa':   # interleave: each Devanagari line followed by its transliteration
        rows = ''.join(f'<div class="il"><div class="h">{E(x)}</div><div class="t">{E(y)}</div></div>' for x, y in zip(hi.split('\n'), tr.split('\n')))
        return f'<div class="st chal">{lab}{rows}<div class="m">{E(s["mean"])}</div></div>'
    if a['kind'] == 'stuti':   # one half-line of a chaupai per printed line
        hi = re.sub(r'। (?=\S)', '।\n', hi); tr = re.sub(r' \| (?=\S)', ' |\n', tr)
    h = E(hi).replace('\n', '<br>')
    t = f'<div class="t">{E(tr).replace(chr(10), "<br>")}</div>' if tr else ''
    r = ''
    if a.get('refrain') and s.get('refrain'):
        r = f'<div class="r"><span class="rh">॥ {E(a["refrain"])} ॥</span> <span class="rt">{E(a["refrain_tr"])}</span></div>'
    return f'<div class="st">{lab}<div class="h">{h}</div>{t}<div class="m">{E(s["mean"])}</div>{r}</div>'

def entry(slug, num):
    a = ALL[slug]
    short = slug in SHORT
    img = prep_image(a['img']) if not short and a['kind'] != 'katha' else None
    pic = f'<img class="pic" src="file://{img}">' if img else ''
    qr = '' if short else f'<div class="qr">{qr_svg("https://sacredaarti.com/aarti/"+slug+"/")}<span>Read &amp; share<br>on your phone</span></div>'
    use = []
    if a['days'] and a['days'][0] not in ('Daily',): use.append(', '.join(d for d in a['days'] if d not in ('Daily','Daily Puja')))
    if a['fest']: use.append(', '.join(f for f in a['fest'][:3] if f not in a['days']))
    use = ' · '.join(u for u in use if u)
    refnote = f'<p class="rnote">After each stanza sing: <span class="deva">॥ {E(a["refrain"])} ॥</span></p>' if a.get('refrain') else ''
    cls = 'entry short' if short else ('entry katha' if a['kind'] == 'katha' else 'entry')
    body = '\n'.join(stanza(a, s) for s in a['stanzas'])
    return f'''<section class="{cls}" id="{slug}">{mark(slug)}
<header class="eh">{pic}<div class="et"><div class="kicker">{num:02d} · {E(content_label(a))}</div>
<h2>{E(a['title'])}</h2><div class="hi">{a['hi']}</div>{f'<div class="use">{E(use)}</div>' if use and not short else ''}</div>{qr}</header>
<p class="about">{E(a['about'])}</p>{refnote}
<div class="body">{body}</div></section>'''

def content_label(a):
    d = {'SaiBaba':'Sai Baba','Universal':'Universal prayer','Katha':'Katha'}.get(a['deity'], a['deity'])
    k = {'aarti':'Aarti','chalisa':'Chalisa','stuti':'Stuti','mantra':'Mantra','shloka':'Shloka','katha':'Vrat Katha'}[a['kind']]
    return f'{d} · {k}' if a['deity'] not in ('Universal','Katha') else k

def part_divider(p, i):
    num, en, hi, img, intro, slugs = p
    im = prep_image(img, big=True)
    return f'''<section class="part">{mark('part'+num)}<div class="pn">Part {num}</div><h1>{E(en)}</h1><div class="phi">{hi}</div>
{f'<img class="pimg" src="file://{im}">' if im else ''}<p class="pintro">{E(intro)}</p></section>'''

def pg(token, pages):
    return str(pages.get(token, '000'))

def toc(pages):
    rows = []
    for p in PARTS:
        rows.append(f'<tr class="tp"><td>Part {p[0]} · {E(p[1])} <span class="deva">{p[2]}</span></td><td>{pg("part"+p[0], pages)}</td></tr>')
        for s in p[5]:
            a = ALL[s]
            rows.append(f'<tr><td>{E(a["title"])} <span class="deva">{a["hi"]}</span></td><td>{pg(s, pages)}</td></tr>')
    front = [('How to use this book','howto'),('Reading the Roman text','pron'),('Aarti at home','home'),('Which aarti, which day','finder')]
    back = [('About the texts','sources'),('Index','index')]
    f = ''.join(f'<tr><td>{E(t)}</td><td>{pg(k, pages)}</td></tr>' for t,k in front)
    b = ''.join(f'<tr><td>{E(t)}</td><td>{pg(k, pages)}</td></tr>' for t,k in back)
    return f'<section class="toc">{mark("toc")}<h1 class="fh">Contents</h1><table>{f}{"".join(rows)}{b}</table></section>'

def ref(slug, pages):
    return f'{E(ALL[slug]["title"])} <span class="pg">{pg(slug, pages)}</span>'

def front_matter(pages):
    howto = ''
    for h, items in guide.HOW_TO:
        tag = 'ol' if h == 'The usual order' else 'ul'
        howto += f'<h3>{E(h)}</h3><{tag}>' + ''.join(f'<li>{E(x)}</li>' for x in items) + f'</{tag}>'
    pron = ''.join(f'<tr><td>{E(k)}</td><td>{E(v)}</td></tr>' for k, v in guide.PRONUNCIATION)
    wk = ''.join(f'<tr><td>{d}</td><td>{E(w)}</td><td>{"<br>".join(ref(s, pages) for s in sl)}</td></tr>' for d, w, sl in guide.WEEKDAYS)
    fe = ''.join(f'<tr><td>{E(f)}</td><td>{"<br>".join(ref(s, pages) for s in sl)}</td></tr>' for f, n, sl in guide.FESTIVALS)
    ch = ''.join(f'<tr><td>{E(w)}</td><td>{ref(s, pages)}</td></tr>' for w, s in guide.CHILDREN)
    return f'''
<section class="half"><div class="ht">Sacred Aarti Sangrah</div><div class="hh">पवित्र आरती संग्रह</div></section>
<section class="blank"></section>
<section class="title"><div class="om">ॐ</div><h1>Sacred Aarti<br>Sangrah</h1><div class="thi">पवित्र आरती संग्रह</div>
<p class="tsub">Complete Hindu Aartis, Chalisas and Daily Prayers<br>in Devanagari, with Easy Transliteration<br>and English Meaning</p>
<p class="tann">Annotated edition</p><div class="tpub">{E(AUTHOR)}<br><span>sacredaarti.com</span></div></section>
<section class="copy"><p><b>Sacred Aarti Sangrah (Annotated)</b><br>पवित्र आरती संग्रह</p>
<p>Copyright © {YEAR} The Better Daily, LLC. All rights reserved.</p>
<p>The traditional devotional texts in this book are in the public domain and may be freely sung, shared and taught. The selection and arrangement, transliterations, English meanings, introductions, notes and guides are original to this edition.</p>
<p>The texts follow the standard published versions in common use in North India. Where families commonly sing a different word or an extra stanza, this is noted in the introduction to the aarti. Devotional practice varies by family and region; follow the custom of your home and temple.</p>
<p>The deity illustrations in this book were created with the help of AI image tools as artistic representations for devotional use.</p>
<p>ISBN 979-8-14-512899-4 (paperback)</p>
<p>First edition, {YEAR}.<br>Published by The Better Daily, LLC.<br>sacredaarti.com</p></section>
<section class="present"><div class="om">ॐ</div><p class="pr1">This book is presented to</p><div class="line"></div><p class="pr1">with blessings, on the occasion of</p><div class="line"></div><p class="pr1">from</p><div class="line"></div><p class="pr1">date</p><div class="line short"></div>
<p class="prq">सर्वे भवन्तु सुखिनः<br><span>May all be happy.</span></p></section>
<section class="blank"></section>
{toc(pages)}
<section class="fm">{mark('howto')}<h1 class="fh">How to use this book</h1>
<p>Every hymn in this book is printed in three layers, so that you can sing it even if you do not read Hindi, and understand it even if you do.</p>
<div class="demo">{stanza(ALL['om-jai-jagdish-hare'], ALL['om-jai-jagdish-hare']['stanzas'][1])}</div>
<ol><li><b>Devanagari</b>, the original text, in large type.</li>
<li><b>Transliteration</b> in Roman letters, written to be sung. Long vowels carry a line (ā ī ū); see the next page for the full key.</li>
<li><b>Meaning</b>: a plain English rendering of each stanza, written for this edition.</li>
<li><b>The refrain</b> (टेक), printed after each stanza where it is repeated in singing.</li></ol>
<p>Each aarti begins with a short note on its origin and on when it is sung. The QR code beside it opens the same text on sacredaarti.com, so you can read along on a phone or share it with family.</p></section>
<section class="fm">{mark('pron')}<h1 class="fh">Reading the Roman text</h1>
<p>The transliteration follows how these hymns are actually sung in Hindi, so the silent 'a' at the end of most words is dropped (Rām, not Rāma). Sanskrit verses are written out in full, as they are chanted.</p>
<table class="kt">{pron}</table></section>
<section class="fm">{mark('home')}<h1 class="fh">Aarti at home</h1>{howto}</section>
<section class="fm">{mark('finder')}<h1 class="fh">Which aarti, which day</h1>
<h3>By day of the week</h3><table class="ft">{wk}</table>
<h3>By festival</h3><table class="ft">{fe}</table>
<h3>For children</h3><table class="ft">{ch}</table></section>'''

def back_matter(pages):
    idx = sorted(ORDER, key=lambda s: ALL[s]['title'].lower().replace('shri ', '').replace('om ', ''))
    rows = ''.join(f'<tr><td>{E(ALL[s]["title"])}</td><td class="deva">{ALL[s]["hi"]}</td><td>{pg(s, pages)}</td></tr>' for s in idx)
    return f'''<section class="fm">{mark('sources')}<h1 class="fh">About the texts</h1>
<p>Devotional texts travel by mouth and by memory, so most aartis exist in several slightly different versions. This edition follows the standard texts as published in widely used North Indian collections, and keeps the wording and order of stanzas most families sing. Common variants are mentioned in the notes.</p>
<p>The Hanuman Chalisa, Shri Ramchandra Kripalu and the Sundar Kand verses are by Goswami Tulsidas (16th century). Om Jai Jagdish Hare is by Pandit Shardha Ram Phillauri (around 1870). Sukhkarta Dukhharta is by Samarth Ramdas (17th century). The Sanskrit verses come from the Vedas, the Upanishads, the Bhagavad Gita, the Devi Mahatmya and the Ramaraksha Stotra, as noted with each. Many of the other aartis carry a poet's name in their last stanza (Shivanand Swami, Saidas, Ayodhyadas, Devidas, Ram Sundar), but little else is known about their authors.</p>
<p>The English meanings aim to convey the sense of each stanza simply, not word by word. For deeper study of the Ramcharitmanas and the Chalisa, the Gita Press editions with commentary are recommended.</p>
<p>Corrections and suggestions are welcome through sacredaarti.com, where the full collection can also be read online.</p></section>
<section class="fm index">{mark('index')}<h1 class="fh">Index</h1><table>{rows}</table></section>
<section class="end"><div class="om">ॐ</div><p>ॐ शान्तिः शान्तिः शान्तिः</p></section>'''

CSS = open('book_style.css').read()

def build_html(pages):
    parts = []
    n = 0
    for p in PARTS:
        parts.append(part_divider(p, 0))
        for s in p[5]:
            n += 1; parts.append(entry(s, n))
    doc = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
{front_matter(pages)}<div class="mainmatter">{"".join(parts)}</div>{back_matter(pages)}</body></html>'''
    return doc

def render(doc, path):
    open(f'{OUTDIR}/interior.html', 'w').write(doc)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg_ = b.new_page()
        pg_.goto('file://' + os.path.abspath(f'{OUTDIR}/interior.html')); pg_.wait_for_timeout(800)
        pg_.pdf(path=path, prefer_css_page_size=True, print_background=True)
        b.close()

def read_pages(path):
    r = PdfReader(path); pages = {}
    for i, page in enumerate(r.pages):
        for t in re.findall(r'§([\w\-]+)§', page.extract_text() or ''):
            pages.setdefault(t, i + 1)
    return pages, len(r.pages)

if __name__ == '__main__':
    pdf = f'{OUTDIR}/Sacred_Aarti_Sangrah_interior.pdf'
    render(build_html({}), pdf)
    pages, n = read_pages(pdf)
    render(build_html(pages), pdf)
    pages2, n2 = read_pages(pdf)
    assert pages == pages2, 'page numbers shifted between passes'
    missing = [s for s in ORDER if s not in pages]
    print('pages:', n2, 'missing markers:', missing)
    json.dump(pages, open(f'{OUTDIR}/pagemap.json', 'w'), indent=1)
