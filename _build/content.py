from content_aartis import AARTIS
from content_chalisa import CHALISAS
from content_prayers import PRAYERS, KATHAS
from translit import translit
ALL = AARTIS + CHALISAS + PRAYERS + KATHAS
from content_more import MORE
OV = {}
def build(more=False):
    items = ALL + MORE if more else ALL
    for a in items:
        sk = a['lang']=='sa'
        mode = 'mr' if a['lang']=='mr' else 'hi'
        for s in a['stanzas']:
            ssk = sk or bool(s.get('label') and 'Sanskrit' in s['label'])
            s['tr'] = '' if a['kind']=='katha' else translit(s['hi'], ssk, OV, mode)
        a['refrain_tr'] = translit(a['refrain'], False, OV, 'mr' if a['lang']=='mr' else 'hi') if a.get('refrain') else None
    return items
