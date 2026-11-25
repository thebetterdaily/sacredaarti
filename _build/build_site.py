# -*- coding: utf-8 -*-
"""Build sacredaarti.com as a static site into ./site"""
import os, json, shutil, html, datetime
from PIL import Image
import content, guide
from respect import respect, LABEL as RLABEL

OUT = 'site'; DOMAIN = 'https://sacredaarti.com'
CONTACT = os.environ.get('SA_CONTACT', '')   # contact address shown in the footer, set at build time
BOOK_PB = 'https://www.amazon.com/dp/B0HSVK621V'      # paperback, ISBN 9798145128994
BOOK_KINDLE = 'https://www.amazon.com/dp/B0HQ29WYX9'  # Kindle edition
BOOK_KINDLE_IN = 'https://www.amazon.in/dp/B0HQ29WYX9'
TODAY = datetime.date.today().isoformat()
VER = datetime.datetime.now().strftime('%Y%m%d%H%M')
E = html.escape
ALL = content.build(more=True)
import content_more
for _d, _w, _sl in guide.WEEKDAYS: _sl.extend(x for x in content_more.EXTRA_WEEKDAYS.get(_d, []) if x not in _sl)
for _f, _n, _sl in guide.FESTIVALS: _sl.extend(x for x in content_more.EXTRA_FESTIVALS.get(_f, []) if x not in _sl)
guide.FESTIVALS.extend(content_more.NEW_FESTIVALS)
BY = {a['slug']: a for a in ALL}
KIND_LABEL = {'aarti':'Aarti','chalisa':'Chalisa','stuti':'Stuti','mantra':'Mantra','shloka':'Shloka','katha':'Vrat Katha'}
KIND_GROUP = {'aarti':'aarti','chalisa':'chalisa','stuti':'aarti','mantra':'mantra','shloka':'mantra','katha':'katha'}
DEITY_LABEL = RLABEL
def dl(d): return DEITY_LABEL.get(d, d)

ORDER = sorted(ALL, key=lambda a: (a['pop'] or 999, ['aarti','chalisa','stuti','mantra','shloka','katha'].index(a['kind']), a['deity'], a['title']))

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Hanken+Grotesk:wght@400;500;600;700&family=Tiro+Devanagari+Hindi:ital@0;1&display=swap" rel="stylesheet">'

NAV = [('aartis','Aartis','आरती','/#collection'),('chalisa','Chalisa','चालीसा','/?k=chalisa#collection'),('prayers','Mantras','मंत्र','/?k=mantra#collection'),('guide','Puja guide','विधि','/guide'),('book','The book','पुस्तक','/book')]

INSTALL = """<div class="modal" id="install" role="dialog" aria-modal="true" aria-labelledby="install-t"><div class="box">
<button class="x" data-act="close" aria-label="Close">×</button><h3 id="install-t">Keep Sacred Aarti on your phone</h3>
<p class="sub">Free, no app store, and it opens even without internet once added.</p>
<div class="tabs"><button class="chip" data-tab="ios">iPhone</button><button class="chip" data-tab="ipad">iPad</button><button class="chip" data-tab="android">Android</button></div>
<div class="panel" id="p-ios"><ol class="steps"><li>Open sacredaarti.com in <b>Safari</b>.</li><li>Tap the <b>•••</b> button next to the address bar, then tap <b>Share</b> (on older iPhones, tap the <b>Share</b> button ↑ directly).</li>
<li>Scroll down the list and tap <b>Add to Home Screen</b>.</li><li>Keep <b>Open as Web App</b> on and tap <b>Add</b>. The ॐ icon appears with your other apps.</li></ol></div>
<div class="panel" id="p-ipad"><ol class="steps"><li>Open sacredaarti.com in <b>Safari</b>.</li><li>Tap the <b>Share</b> button ↑ at the top right, next to the address bar (if you don't see it, tap <b>•••</b> first).</li>
<li>Scroll down the list and tap <b>Add to Home Screen</b>. Not there? Tap <b>Edit Actions</b> at the bottom and add it.</li><li>Keep <b>Open as Web App</b> on and tap <b>Add</b>.</li></ol></div>
<div class="panel" id="p-android"><button class="pill dark go-install">Install Sacred Aarti now</button><ol class="steps"><li>Open sacredaarti.com in <b>Chrome</b>.</li>
<li>Tap the <b>⋮ menu</b> at the top right.</li><li>Tap <b>Add to Home screen</b> or <b>Install app</b>.</li><li>Tap <b>Install</b>. The ॐ icon appears with your other apps.</li></ol></div></div>"""

def page(title, desc, body, canon, active=None, jsonld=None, og_img=None):
    nav = ''.join(f'<a{" class=on aria-current=page" if active==k else ""} href="{u}">{en}<span class="deva">{hi}</span></a>' for k,en,hi,u in NAV)
    dock = ''.join(f'<a class="{"on" if (active==k or (k=="aartis" and active in ("chalisa","prayers"))) else ""}" href="{u}">{lab}</a>' for k,u,lab in [('aartis','/','Aartis'),('guide','/guide','Guide'),('book','/book','Book')])
    lds = jsonld if isinstance(jsonld, list) else ([jsonld] if jsonld else [])
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    og = og_img or '/img/og.jpg'
    contact = f' · <a href="mailto:{CONTACT}">Contact</a>' if CONTACT else ''
    return f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{DOMAIN}{canon}">
<meta property="og:site_name" content="Sacred Aarti"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}{canon}"><meta property="og:image" content="{DOMAIN}{og}"><meta name="twitter:card" content="summary_large_image">
<meta name="google-site-verification" content="DI1rDFRSuoA8SmptQQa6LwXnj1DVT81m-D4trpJaRhc">
<meta name="theme-color" content="#170B05">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Sacred Aarti"><meta name="apple-mobile-web-app-status-bar-style" content="black">
<link rel="manifest" href="/manifest.json"><link rel="icon" href="/icon-192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script>try{{if(localStorage.getItem('sa-mode')==='paper')document.documentElement.setAttribute('data-theme','paper')}}catch(e){{}}</script>
{FONTS}<link rel="stylesheet" href="/assets/style.css?v={VER}">{ld}
</head><body>
<header class="top"><div class="top-in"><a class="brand" href="/" aria-label="Sacred Aarti home"><span class="om">ॐ</span><span class="bt"><b>Sacred Aarti</b><span class="deva">पवित्र आरती संग्रह</span></span></a>
<nav class="nav" aria-label="Sections">{nav}</nav>
<div class="tact"><a class="ib" href="/#search" aria-label="Search"><svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="7" cy="7" r="5"/><path d="M11 11l4 4"/></svg></a><button class="ib" data-act="theme" aria-label="Switch between day and diya mode" title="Day / diya mode"><svg width="17" height="17" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 1.5a6.5 6.5 0 0 1 0 13z" fill="currentColor"/></svg></button><button class="pill dark sm" data-act="install">Add to phone</button></div></div></header>
<header class="mbar"><a class="logo" href="/"><span class="om">ॐ</span>Sacred Aarti</a><button class="install" data-act="install">Add to phone</button></header>
<main>{body}</main>
<nav class="dock" aria-label="Menu"><a href="/#search" aria-label="Search"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="7" cy="7" r="5"/><path d="M11 11l4 4"/></svg></a>{dock}<button data-act="theme" aria-label="Toggle evening mode"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 1.5a6.5 6.5 0 0 1 0 13z" fill="currentColor"/></svg></button></nav>
<footer class="foot"><div><div class="om">ॐ</div>Sacred Aarti · पवित्र आरती संग्रह<br>© {datetime.date.today().year} The Better Daily, LLC{contact}</div>
<div style="max-width:420px">Texts follow the standard published versions; English meanings are our own. Deity images are artistic representations made with AI tools for devotional use.</div></footer>
{INSTALL}
<script src="/assets/app.js?v={VER}" defer></script></body></html>'''

def has_colour(n): return bool(n) and os.path.exists(f'img_orig/{n}.png')
def has_any(n): return bool(n) and (has_colour(n) or os.path.exists(f'art_clean/{n}.png'))
def img_url(a):
    return f'/img/{a["img"]}.webp' if has_any(a.get('img')) else None
def thumb_url(n): return f'/img/t/{n}.webp'

def row(a, i):
    im = img_url(a) or ''
    search = ' '.join([a['title'], a['hi'], dl(a['deity']), a['deity'], a['kind'], ' '.join(a['fest']), a['slug'].replace('-',' ')]).lower()
    tn = f'<img class="tn" src="{thumb_url(a["img"])}" alt="" width="58" height="58" loading="lazy">' if im else '<span class="tn om">ॐ</span>'
    return f'''<li class="row" data-kind="{KIND_GROUP[a['kind']]}" data-deity="{a['deity']}" data-img="{im}" data-search="{E(search)}">
<span class="num">{i:02d}</span><a href="/aarti/{a['slug']}" style="display:contents">{tn}<div><h3>{E(a['title'])}</h3><div class="hi">{a['hi']}</div></div>
<div class="meta"><b>{dl(a['deity'])}</b>{KIND_LABEL[a['kind']]} · {E(a['fest'][0]) if a['fest'] else ''}</div><span class="go">→</span></a></li>'''

def tlink(slug, label):
    a = BY[slug]
    return f'<a href="/aarti/{slug}">{label}<img class="thumb" src="{thumb_url(a["img"])}" alt="" loading="lazy"></a>'

def home():
    deities = []
    for a in ORDER:
        if a['deity'] not in deities: deities.append(a['deity'])
    PRI = ['Ganesha','Shiva','Hanuman','Durga','Lakshmi','Vishnu','Krishna','Ram','Saraswati','Shani','Surya','Satyanarayan','SaiBaba','KhatuShyam','Santoshi','Brihaspati','Ganga','Tulsi','Navagraha','Universal','Katha']
    deities.sort(key=lambda d: PRI.index(d) if d in PRI else 50)
    chips = ''.join(f'<button class="chip" data-deity="{d}">{dl(d)}</button>' for d in deities)
    rows = '\n'.join(row(a, i+1) for i,a in enumerate(ORDER))
    wmap = {}
    for d,(name,who,slugs) in zip([0,1,2,3,4,5,6], guide.WEEKDAYS):
        wmap[d] = [name, respect(who), BY[slugs[0]]['title'], f'/aarti/{slugs[0]}']
    badge = '''<a class="badge" href="/book" aria-label="The Sacred Aarti book"><svg viewBox="0 0 120 120"><defs><path id="c" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs>
<text font-size="10" font-family="Hanken Grotesk" font-weight="600" fill="currentColor"><textPath href="#c" textLength="286" lengthAdjust="spacing">THE BOOK · AARTI SANGRAH · IN PRINT · </textPath></text></svg><span class="arr">→</span></a>'''
    n_aarti = len([a for a in ALL if a['kind']=='aarti'])
    prologue = (f'Light the lamp and begin with {tlink("jai-ganesh-deva","Ganeshji")}, who is always worshipped first. '
                f'Then sing to the deity of the day: {tlink("om-jai-shiv-omkara","Shivji")} on Monday, {tlink("hanuman-chalisa","Hanumanji")} on Tuesday, '
                f'{tlink("om-jai-lakshmi-mata","Lakshmi Mata")} on Friday, {tlink("jai-jai-shri-shanidev","Shani Dev")} on Saturday. '
                f'Close with {tlink("om-jai-jagdish-hare","Om Jai Jagdish Hare")}, offer the flame to everyone, and share the prasad.')
    body = f'''<div class="wrap">
<section class="hero"><div class="reveal">
<p class="eyebrow"><b>ॐ</b> &nbsp;Sacred Aarti · आरती संग्रह</p>
<h1 class="hero-t">Every aarti,<br><span class="it">word for word.</span></h1>
<p class="hero-hi">सम्पूर्ण आरती, चालीसा एवं मन्त्र</p>
<p class="lede">{n_aarti} complete aartis, {len([a for a in ALL if a['kind']=='chalisa'])} chalisas and daily prayers in Devanagari, easy transliteration and English meaning, so every generation can sing along.</p>
<form class="hsearch" action="/" role="search" onsubmit="return false"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="7" cy="7" r="5"/><path d="M11 11l4 4"/></svg><input id="hq" type="search" placeholder="Find an aarti: Hanumanji, Lakshmi Mata, जय…" aria-label="Find an aarti" autocomplete="off"></form>
<div class="ctas"><a class="pill dark" href="#collection">Browse all {len(ALL)} →</a><a class="pill line" href="/guide">How to do aarti at home</a></div>
<p class="today" id="today" data-map='{E(json.dumps(wmap))}'></p>
</div><div class="stage"><canvas id="diya" aria-hidden="true"></canvas><p class="cap">Move your cursor or finger through the diya</p>{badge}</div></section>



<section class="sec" id="collection"><div class="sec-h reveal"><span class="big" aria-hidden="true">01</span><h2>The collection</h2><p>Standard texts checked line by line, with the refrain marked the way it is sung.</p></div>
<div class="tools"><button class="chip on" data-kind="all">All</button><button class="chip" data-kind="aarti">Aartis</button><button class="chip" data-kind="chalisa">Chalisa</button><button class="chip" data-kind="mantra">Mantras &amp; shlokas</button><button class="chip" data-kind="katha">Katha</button>
<label class="search"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="7" cy="7" r="5"/><path d="M11 11l4 4"/></svg><input id="q" type="search" placeholder="Search: Shivji, Diwali, जय…" aria-label="Search"></label></div>
<div class="deity-row"><button class="chip on" data-deity="all">Every deity</button>{chips}</div>
<ol class="list" id="list">{rows}</ol><p class="empty" id="empty" style="display:none">Nothing found. Try another word.</p>
<div class="peek" id="peek"><img alt=""></div></section>

<section class="prologue reveal"><p class="tag">( The evening aarti )</p><p>{prologue}</p></section>

<section class="sec" id="phone"><div class="sec-h reveal"><span class="big" aria-hidden="true">02</span><h2>Keep it on your phone</h2><p>Add Sacred Aarti to your home screen like an app. It is free and opens even without internet.</p></div>
<div class="keep"><div><h3>iPhone</h3><ol class="steps"><li>Open sacredaarti.com in <b>Safari</b>.</li><li>Tap <b>•••</b> next to the address bar, then <b>Share</b>.</li><li>Scroll down, tap <b>Add to Home Screen</b>.</li><li>Keep <b>Open as Web App</b> on, tap <b>Add</b>.</li></ol></div>
<div><h3>iPad</h3><ol class="steps"><li>Open sacredaarti.com in <b>Safari</b>.</li><li>Tap <b>Share</b> ↑ at the top right (or <b>•••</b>, then Share).</li><li>Scroll down, tap <b>Add to Home Screen</b>. Missing? Tap <b>Edit Actions</b> and add it.</li><li>Tap <b>Add</b>.</li></ol></div>
<div><h3>Android</h3><ol class="steps"><li>Open sacredaarti.com in <b>Chrome</b>.</li><li>Tap the <b>⋮ menu</b> at the top right.</li><li>Tap <b>Add to Home screen</b> or <b>Install app</b>.</li><li>Tap <b>Install</b>.</li></ol></div>
<p class="why">Once added, every aarti is saved on your phone, so it still opens in the temple or on a plane with no signal. <a class="pill line" style="margin-left:8px;padding:7px 14px" href="#" data-act="install">Show me how</a></p></div></section>

<section class="band reveal"><div><p class="eyebrow" style="color:inherit;opacity:.7">03 · The book · now on Amazon</p><h2>Sacred Aarti Sangrah,<br>in print and on Kindle.</h2>
<p>The whole collection as a keepsake for the puja shelf: Devanagari, transliteration and meaning together, a home puja guide and daily prayers for children.</p>
<div class="ctas" style="margin-top:6px"><a class="pill" href="{BOOK_PB}" data-in="{BOOK_KINDLE_IN}" data-in-label="Kindle on Amazon.in →" rel="noopener" target="_blank">Paperback on Amazon →</a><a class="pill ghost" href="{BOOK_KINDLE}" data-in-hide rel="noopener" target="_blank">Kindle edition</a></div><a class="more" href="/book">About the book →</a></div>
<div style="display:grid;grid-template-columns:120px 1fr;gap:22px;align-items:center"><img src="/img/book-cover.jpg" alt="Sacred Aarti Sangrah book cover" width="120" height="180" loading="lazy" style="border-radius:8px;box-shadow:0 10px 30px rgba(0,0,0,.35)"><ul><li><span>01</span>&nbsp; {len(ALL)} aartis, chalisas and prayers</li><li><span>02</span>&nbsp; Pronunciation guide for new readers</li><li><span>03</span>&nbsp; Weekday and festival finder</li><li><span>04</span>&nbsp; Prayers for children</li></ul></div></section>
</div>'''
    ld = [{"@context":"https://schema.org","@type":"WebSite","name":"Sacred Aarti","alternateName":["SacredAarti","sacredaarti.com","पवित्र आरती संग्रह"],"url":DOMAIN+"/","inLanguage":["en","hi"],
           "publisher":{"@type":"Organization","name":"The Better Daily, LLC"}},
          {"@context":"https://schema.org","@type":"ItemList","name":"Hindu aartis, chalisas and mantras","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{DOMAIN}/aarti/{a['slug']}","name":a['title']} for i,a in enumerate(ORDER)]}]
    return page('Sacred Aarti | Aarti Lyrics in Hindi & English with Meaning, Chalisa & Mantras',
        'Sacred Aarti (sacredaarti.com): complete Hindu aarti lyrics in Hindi with easy English transliteration and meaning. Om Jai Jagdish Hare, Jai Ganesh Deva, Lakshmi aarti, Hanuman Chalisa, Shiv Chalisa, Gayatri Mantra and more. आरती संग्रह',
        body, '/', 'aartis', ld)

def stanza_html(a, s):
    lab = f'<p class="lab">{E(s["label"])}</p>' if s.get('label') else ''
    h = E(s['hi']).replace('\n','<br>')
    t = E(s['tr']).replace('\n','<br>') if s.get('tr') else ''
    r = ''
    if a.get('refrain') and s.get('refrain'):
        r = f'<p class="r"><span class="rh">॥ {E(a["refrain"])} ॥</span><span class="rt">{E(a["refrain_tr"])}</span></p>'
    tt = f'<p class="t">{t}</p>' if t else ''
    return f'<div class="st">{lab}<p class="h">{h}</p>{tt}<p class="m">{E(respect(s["mean"]))}</p>{r}</div>'

def seo_name(a):
    t = a['title']
    if a['kind'] == 'aarti' and 'aarti' not in t.lower(): t += ' Aarti'
    return t

def related(a):
    pool = [x for x in ORDER if x['slug'] != a['slug'] and (x['deity'] == a['deity'] or set(x['days']) & set(a['days']) - {'Daily','Daily Puja'})]
    pool += [BY[s] for s in ('om-jai-jagdish-hare','hanuman-chalisa','jai-ganesh-deva') if s != a['slug'] and BY[s] not in pool]
    items = ''.join(f'<li><a href="/aarti/{x["slug"]}">' + (f'<img src="{thumb_url(x["img"])}" alt="" width="28" height="28" loading="lazy">' if img_url(x) else '') + f'{E(x["title"])}</a></li>' for x in pool[:6])
    return f'<section class="related"><h2>Also sung with this</h2><ul>{items}</ul></section>'

def detail(a, i, prev, nxt):
    im = img_url(a)
    cls = 'dimg' if has_colour(a.get('img')) else 'dimg line'
    pic = f'<div class="{cls}"><img src="{im}" alt="{E(dl(a["deity"]))}, devotional illustration for {E(a["title"])}" width="560" height="700"></div>' if im else '<div class="dimg om">ॐ</div>'
    facts = f'<div><b>{dl(a["deity"])}</b>Deity</div><div><b>{KIND_LABEL[a["kind"]]}</b>Form</div>'
    if a['days']: facts += f'<div><b>{", ".join(a["days"][:2])}</b>Day</div>'
    if a['fest']: facts += f'<div><b>{E(", ".join(a["fest"][:2]))}</b>Occasion</div>'
    layers = '' if a['kind']=='katha' else '<button class="chip on" data-act="layer" data-l="h">हिंदी</button><button class="chip on" data-act="layer" data-l="t">Roman</button><button class="chip on" data-act="layer" data-l="m">Meaning</button>'
    stz = '\n'.join(stanza_html(a,s) for s in a['stanzas'])
    note = f'<p class="note">The refrain <span class="deva">॥ {E(a["refrain"])} ॥</span> is sung after every stanza, as marked.</p>' if a.get('refrain') else ''
    pn = f'<nav class="pn"><a href="/aarti/{prev["slug"]}">← Previous<b>{E(prev["title"])}</b></a><a href="/aarti/{nxt["slug"]}">Next →<b>{E(nxt["title"])}</b></a></nav>'
    body = f'''<div class="wrap {'katha' if a['kind']=='katha' else ''}">
<p class="crumbs"><a href="/">Sacred Aarti</a> / <a href="/#collection">{dl(a['deity'])}</a> / {KIND_LABEL[a['kind']]}</p>
<header class="dhead"><div><p class="no">{i:02d} · {KIND_LABEL[a['kind']].upper()}</p><h1>{E(a['title'])}</h1><p class="hi">{a['hi']}</p>
<div class="facts">{facts}</div></div>{pic}</header>
<p class="about">{E(respect(a['about']))}</p>
<div class="ctrl">{layers}<span class="sp"></span><button class="chip" data-act="smaller" aria-label="Smaller text">A−</button><button class="chip" data-act="bigger" aria-label="Larger text">A+</button><button class="chip" data-act="theme" data-lbl="cap">Day mode</button></div>
<article class="verses">{stz}</article>{note}{related(a)}{pn}</div>'''
    name = seo_name(a)
    desc = f"{name} lyrics ({a['hi']}) in Hindi with English transliteration and meaning of every stanza. {respect(a['about'])}"
    lyr = '\n\n'.join(s['hi'] for s in a['stanzas'])
    ld = [{"@context":"https://schema.org","@type":"MusicComposition","name":name,"alternateName":a['hi'],"inLanguage":"hi",
           "url":f"{DOMAIN}/aarti/{a['slug']}","about":dl(a['deity']),"genre":"Hindu devotional","description":respect(a['about']),
           "lyrics":{"@type":"CreativeWork","text":lyr[:4800],"inLanguage":"hi"},
           "image":DOMAIN+im if im else None,
           "publisher":{"@type":"Organization","name":"The Better Daily, LLC"}},
          {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Sacred Aarti","item":DOMAIN+"/"},
            {"@type":"ListItem","position":2,"name":name,"item":f"{DOMAIN}/aarti/{a['slug']}"}]}]
    if not im: ld[0].pop('image')
    title = f"{name} Lyrics in Hindi & English with Meaning | {a['hi']}"
    act = 'chalisa' if a['kind']=='chalisa' else ('prayers' if KIND_GROUP[a['kind']]=='mantra' else 'aartis')
    return page(title, desc[:290], body, f"/aarti/{a['slug']}", act, ld, im)

def link(slug): a=BY[slug]; return f'<a href="/aarti/{slug}">{E(a["title"])}</a>'

def guide_page():
    howto = ''
    for h, items in guide.HOW_TO:
        tag = 'ol' if h=='The usual order' else 'ul'
        howto += f'<h3>{E(h)}</h3><{tag}>' + ''.join(f'<li>{E(respect(x))}</li>' for x in items) + f'</{tag}>'
    for name, slug in [('Shubham Karoti','shubham-karoti'),('Vakratunda Mahakaya','vakratunda-mahakaya'),('Jai Ganesh Deva','jai-ganesh-deva'),
                       ('Om Jai Jagdish Hare','om-jai-jagdish-hare'),('Karpur Gauram','karpur-gauram'),('Kshama Prarthana','kshama-prarthana'),('Sarve Bhavantu Sukhinah','sarve-bhavantu-sukhinah')]:
        howto = howto.replace(name, f'<a href="/aarti/{slug}">{name}</a>', 1)
    wk = ''.join(f'<tr><td>{d}</td><td>{E(respect(w))}</td><td>{", ".join(link(s) for s in sl)}</td></tr>' for d,w,sl in guide.WEEKDAYS)
    fe = ''.join(f'<tr><td>{E(f)}</td><td>{E(respect(n))}<br>{", ".join(link(s) for s in sl)}</td></tr>' for f,n,sl in guide.FESTIVALS)
    ch = ''.join(f'<tr><td>{E(w)}</td><td>{link(s)}</td></tr>' for w,s in guide.CHILDREN)
    pr = ''.join(f'<tr><td>{E(k)}</td><td>{E(v)}</td></tr>' for k,v in guide.PRONUNCIATION)
    body = f'''<div class="wrap"><section class="sec"><div class="sec-h"><span class="big" aria-hidden="true">01</span><h2>Aarti at home</h2><p>A simple, traditional way to do the evening aarti, and which aarti to sing on which day.</p></div>
<div class="split"><div class="prose">{howto}</div><div>
<h3 style="font-size:22px;letter-spacing:-.02em;margin:28px 0 6px">By weekday</h3><table class="tbl"><tr><th>Day</th><th>Devoted to</th><th>Sing</th></tr>{wk}</table></div></div>
<div class="sec-h" style="margin-top:30px"><span class="big" aria-hidden="true">02</span><h2>Festival finder</h2></div><table class="tbl">{fe}</table>
<div class="split"><div><div class="sec-h"><span class="big" aria-hidden="true">03</span><h2 style="font-size:34px">For children</h2></div><table class="tbl">{ch}</table></div>
<div><div class="sec-h"><span class="big" aria-hidden="true">04</span><h2 style="font-size:34px">Reading the Roman text</h2></div><table class="tbl">{pr}</table></div></div></section></div>'''
    return page('How to Do Aarti at Home: Order, Weekday & Festival Guide | Sacred Aarti',
                'A simple guide to performing aarti at home: what you need, the traditional order, how to wave the lamp, which aarti to sing on each weekday and festival, and daily prayers for children.',
                body, '/guide', 'guide')

def book_page():
    buy = (f'<a class="pill dark" href="{BOOK_PB}" rel="noopener" target="_blank">Paperback on Amazon →</a>'
           f'<a class="pill line" href="{BOOK_KINDLE}" data-in="{BOOK_KINDLE_IN}" data-in-label="Kindle on Amazon.in →" rel="noopener" target="_blank">Kindle edition →</a>')
    body = f'''<div class="wrap"><section class="hero" style="min-height:auto;padding:60px 0 20px"><div>
<p class="eyebrow"><b>ॐ</b> &nbsp;The book · now on Amazon</p><h1 class="hero-t">Sacred Aarti<br><span class="it">Sangrah.</span></h1>
<p class="hero-hi">पवित्र आरती संग्रह</p><p class="lede">The complete collection in one book for the puja shelf, made for families who sing in Hindi but read most comfortably in English.</p>
<div class="ctas">{buy}</div>
<div class="formats"><div><b>Paperback</b>131 pages, 6 × 9 in, large clear type for reading while holding the thali. Printed by Amazon in the US, UK, Europe, Canada, Australia and Japan.</div>
<div><b>Kindle</b>The same book on any phone, tablet or Kindle, with the Devanagari font built in. In India it is on <a href="{BOOK_KINDLE_IN}" rel="noopener" target="_blank">Amazon.in</a>.</div></div>
<p class="small"><a href="/#collection">Or read every aarti free online →</a></p></div>
<div class="prose"><img src="/img/book-cover.jpg" alt="Sacred Aarti Sangrah book cover" style="width:220px;border-radius:10px;box-shadow:0 14px 36px rgba(0,0,0,.18);margin-bottom:10px"><h3>What makes it different</h3><ul>
<li>Standard, complete texts, with the refrain marked exactly where it is sung.</li>
<li>Three layers for every stanza: Devanagari, a pronunciation-friendly Roman transliteration, and a plain-English meaning.</li>
<li>A short note on the origin of each aarti: who wrote it, and when and why it is sung.</li>
<li>A home puja guide, a weekday and festival finder, and a section of daily prayers for children.</li>
<li>Large, clear type laid out to be read while holding the aarti thali.</li></ul></div></section></div>'''
    name = 'Sacred Aarti Sangrah (Annotated): Complete Hindu Aartis, Chalisas and Daily Prayers in Hindi with Easy Transliteration and English Meaning'
    ld = {"@context":"https://schema.org","@type":"Book","name":name,"alternateName":"पवित्र आरती संग्रह","inLanguage":["hi","en"],
          "author":{"@type":"Organization","name":"The Better Daily LLC"},"publisher":{"@type":"Organization","name":"The Better Daily, LLC"},
          "image":DOMAIN+"/img/book-cover.jpg","url":DOMAIN+"/book",
          "workExample":[{"@type":"Book","bookFormat":"https://schema.org/Paperback","isbn":"9798145128994","numberOfPages":131,"url":BOOK_PB},
                         {"@type":"Book","bookFormat":"https://schema.org/EBook","url":BOOK_KINDLE}]}
    return page('Sacred Aarti Sangrah Book: Paperback & Kindle | Hindu Aartis with Transliteration & Meaning',
                'Sacred Aarti Sangrah, now on Amazon in paperback and Kindle: complete Hindu aartis, chalisas and daily prayers in Devanagari with English transliteration and meaning, a home puja guide and prayers for children.', body, '/book', 'book', ld)

def write(path, s):
    p = os.path.join(OUT, path.lstrip('/'))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)

def images():
    from PIL import ImageDraw, ImageFont, ImageOps
    os.makedirs(f'{OUT}/img/t', exist_ok=True)
    names = {os.path.splitext(f)[0] for f in os.listdir('img_orig')} | {os.path.splitext(f)[0] for f in os.listdir('art_clean')}
    for n in names:
        if os.path.exists(f'img_orig/{n}.png'):
            im = Image.open(f'img_orig/{n}.png').convert('RGB')
        else:   # line art only: print it in maroon ink on warm paper
            g = Image.open(f'art_clean/{n}.png').convert('L')
            im = ImageOps.colorize(g, black=(92,30,0), white=(247,231,204))
        big = im.copy(); big.thumbnail((760, 950)); big.save(f'{OUT}/img/{n}.webp', 'WEBP', quality=80, method=6)
        t = ImageOps.fit(im, (128, 128), Image.LANCZOS, centering=(0.5, 0.32)); t.save(f'{OUT}/img/t/{n}.webp', 'WEBP', quality=78, method=6)
    og = Image.new('RGB', (1200, 630), (252,245,234)); d = ImageDraw.Draw(og)
    fb = ImageFont.truetype('fonts/EBGaramond-SemiBold.ttf', 92)
    fi = ImageFont.truetype('fonts/EBGaramond-Italic.ttf', 92)
    fh = ImageFont.truetype('fonts/TiroDevanagariHindi-Regular.ttf', 44)
    d.text((70, 120), 'Every aarti,', font=fb, fill=(59,23,8)); d.text((70, 225), 'word for word.', font=fi, fill=(226,98,11))
    d.text((72, 370), 'सम्पूर्ण आरती, चालीसा एवं मन्त्र', font=fh, fill=(184,50,26))
    d.text((72, 530), 'sacredaarti.com', font=ImageFont.truetype('fonts/DMSans-SemiBold.ttf', 32), fill=(59,23,8))
    g = Image.open('img_orig/ganesha.png').convert('RGB'); g = ImageOps.fit(g, (400, 500), Image.LANCZOS, centering=(.5,.4))
    m = Image.new('L', g.size, 0); ImageDraw.Draw(m).rounded_rectangle((0,0,g.size[0]-1,g.size[1]-1), 28, fill=255)
    og.paste(g, (740, 65), m)
    og.save(f'{OUT}/img/og.jpg', quality=86)

def icons():
    from PIL import ImageDraw, ImageFont
    for n, sz in (('icon-512.png', 512), ('icon-192.png', 192), ('apple-touch-icon.png', 180)):
        im = Image.new('RGB', (sz, sz), (92,30,0)); d = ImageDraw.Draw(im)
        f = ImageFont.truetype('fonts/TiroDevanagariHindi-Regular.ttf', int(sz*.58))
        bb = d.textbbox((0,0), 'ॐ', font=f); w, h = bb[2]-bb[0], bb[3]-bb[1]
        d.text(((sz-w)/2-bb[0], (sz-h)/2-bb[1]), 'ॐ', font=f, fill=(242,168,29))
        im.save(f'{OUT}/{n}')

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(f'{OUT}/assets')
    shutil.copy('site_src/style.css', f'{OUT}/assets/style.css'); shutil.copy('site_src/app.js', f'{OUT}/assets/app.js')
    images(); icons(); shutil.copy('site_src/book-cover.jpg', f'{OUT}/img/book-cover.jpg')
    write('/index.html', home())
    for i, a in enumerate(ORDER):
        write(f'/aarti/{a["slug"]}.html', detail(a, i+1, ORDER[i-1], ORDER[(i+1) % len(ORDER)]))
    write('/guide.html', guide_page()); write('/book.html', book_page())
    write('/404.html', page('Page not found | Sacred Aarti', 'Page not found', '<div class="wrap"><section class="sec"><h2 class="hero-t" style="font-size:56px">Not found.</h2><p class="lede" style="margin-top:16px"><a class="pill dark" href="/">Back to all aartis →</a></p></section></div>', '/404.html'))
    urls = ['/', '/guide', '/book'] + [f'/aarti/{a["slug"]}' for a in ORDER]
    imgs = {f'/aarti/{a["slug"]}': img_url(a) for a in ORDER}
    sm = ''.join(f'<url><loc>{DOMAIN}{u}</loc><lastmod>{TODAY}</lastmod>' + (f'<image:image><image:loc>{DOMAIN}{imgs[u]}</image:loc></image:image>' if imgs.get(u) else '') + '</url>' for u in urls)
    write('/sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">{sm}</urlset>')
    write('/robots.txt', f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    write('/CNAME', 'sacredaarti.com\n')
    write('/manifest.json', json.dumps({"name":"Sacred Aarti · पवित्र आरती संग्रह","short_name":"Sacred Aarti",
        "description":"Complete Hindu aartis, chalisas and mantras in Hindi with English transliteration and meaning","start_url":"/","scope":"/",
        "display":"standalone","background_color":"#170B05","theme_color":"#170B05","lang":"en","categories":["lifestyle","education","books"],
        "icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}],
        "shortcuts":[{"name":"Hanuman Chalisa","url":"/aarti/hanuman-chalisa"},{"name":"Om Jai Jagdish Hare","url":"/aarti/om-jai-jagdish-hare"}]}, ensure_ascii=False, indent=1))
    core = ['/', '/guide', '/book', '/assets/style.css?v='+VER, '/assets/app.js?v='+VER, '/manifest.json', '/icon-192.png'] + [f'/aarti/{a["slug"]}' for a in ORDER]
    write('/sw.js', f'''// Sacred Aarti service worker: network-first for pages, cached copy when offline.
const CACHE='sacred-aarti-{VER}';
const CORE={json.dumps(core)};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).catch(()=>{{}}));self.skipWaiting();}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));}});
self.addEventListener('fetch',e=>{{const r=e.request;if(r.method!=='GET')return;
  if(r.mode==='navigate'){{e.respondWith(fetch(r).then(res=>{{const c=res.clone();caches.open(CACHE).then(x=>x.put(r,c));return res;}}).catch(()=>caches.match(r).then(m=>m||caches.match('/'))));return;}}
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{{if(res.ok&&new URL(r.url).origin===location.origin){{const c=res.clone();caches.open(CACHE).then(x=>x.put(r,c));}}return res;}})));}});
''')
    print('pages:', len(urls), 'entries:', len(ORDER))

if __name__ == '__main__':
    main()
