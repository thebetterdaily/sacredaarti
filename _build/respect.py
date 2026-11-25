# -*- coding: utf-8 -*-
"""Respectful forms of address for the website's English prose.

Bare names ("Shiva", "Hanuman") become the forms used at home and in the mandir
("Shivji", "Hanumanji", "Durga Mata"). Titles and fixed names are left alone:
a name is skipped when a capitalised word sits right before it (Lord Shiva,
Shri Hanuman, Jai Ganesh) or right after it (Hanuman Chalisa, Ganesh Chaturthi),
or when it is followed by aarti/puja/bhajan ("the Hanuman aarti").
"""
import re

# deity key in content -> label shown on chips, meta lines and breadcrumbs
LABEL = {
    'Ganesha': 'Ganeshji', 'Hanuman': 'Hanumanji', 'Shiva': 'Shivji', 'Durga': 'Durga Mata',
    'Vishnu': 'Bhagwan Vishnu', 'Krishna': 'Shri Krishna', 'Ram': 'Shri Ram', 'Lakshmi': 'Lakshmi Mata',
    'Saraswati': 'Saraswati Mata', 'Shani': 'Shani Dev', 'Satyanarayan': 'Satyanarayan Bhagwan',
    'Surya': 'Surya Dev', 'SaiBaba': 'Sai Baba', 'Ganga': 'Ganga Maiya', 'KhatuShyam': 'Khatu Shyamji',
    'Santoshi': 'Santoshi Mata', 'Brihaspati': 'Brihaspati Dev', 'Tulsi': 'Tulsi Mata', 'Navagraha': 'Navagraha',
    'Universal': 'Universal', 'Katha': 'Katha',
}

PROSE = {
    'Ganesha': 'Ganeshji', 'Ganesh': 'Ganeshji', 'Ganapati': 'Ganeshji', 'Shiva': 'Shivji', 'Shiv': 'Shivji',
    'Hanuman': 'Hanumanji', 'Durga': 'Durga Mata', 'Lakshmi': 'Lakshmi Mata', 'Laxmi': 'Lakshmi Mata',
    'Parvati': 'Parvati Mata', 'Saraswati': 'Saraswati Mata', 'Kali': 'Kali Mata', 'Sita': 'Sita Mata',
    'Krishna': 'Shri Krishna', 'Rama': 'Shri Ram', 'Ram': 'Shri Ram', 'Vishnu': 'Bhagwan Vishnu',
    'Shani': 'Shani Dev', 'Surya': 'Surya Dev', 'Radha': 'Radha Rani', 'Ganga': 'Ganga Maiya',
}
_RX = re.compile(r"(?P<pre>\b[A-Za-z]+\s)?\b(?P<n>" + '|'.join(sorted(PROSE, key=len, reverse=True)) + r")\b(?P<post>'s|\s+\S+)?")
_SKIP_AFTER = re.compile(r"\s+(aarti|aartis|puja|bhajan|bhajans|temple|temples|mantra|ji|jī)\b", re.I)

_TITLED = re.compile(r"\b(?:Lord|Goddess|Mother|Mata)\s+(Ganesha|Ganesh|Shiva|Hanuman|Vishnu|Krishna|Rama|Ram|Durga|Lakshmi|Parvati|Saraswati|Kali|Sita)\b(?!\s+[A-Z])")

def respect(text):
    if not text: return text
    text = _TITLED.sub(lambda m: PROSE[m.group(1)], text)
    def sub(m):
        pre, n, post = m.group('pre') or '', m.group('n'), m.group('post') or ''
        w = pre.strip()
        if w and w[0].isupper() and w not in ('The', 'In', 'On', 'To', 'For', 'With', 'And', 'O', 'Of'): return m.group(0)
        p = post.strip()
        if p and p[0].isupper() and post != "'s": return m.group(0)
        if post and _SKIP_AFTER.match(post): return m.group(0)
        rep = PROSE[n]
        if w.lower() == 'the' and n == 'Ganga': pre = ''          # "the Ganga" -> "Ganga Maiya"
        if pre and rep.startswith(('Shri', 'Bhagwan')) and w.lower() == 'the': pre = ''
        return pre + rep + post
    return _RX.sub(sub, text)

if __name__ == '__main__':
    for s in ['Sung to Shiva as Mahadev, the Hanuman Chalisa is read by Hanuman devotees.',
              'Lord Shiva and Goddess Durga; Jai Ganesh Deva; the standard Hanuman aarti; on Ganga Dussehra',
              "Krishna and Radha beside him; the Ganga in Haridwar; Hanuman's devotion to Rama and Sita",
              'O Shiva, you wear the moon', 'Kije Hanuman Lala; Jagdambe Kali; poet Ram Sundar; Guru Vishnu']:
        print(respect(s))
