"""Devanagari -> readable Roman transliteration.

Scheme ("light IAST"): long vowels marked (ā ī ū), sh/ch/chh, no retroflex dots.
Hindi/Awadhi/Marathi mode applies schwa deletion; Sanskrit mode keeps every 'a'.
"""
import re

V_IND = {'अ':'a','आ':'ā','इ':'i','ई':'ī','उ':'u','ऊ':'ū','ऋ':'ri','ए':'e','ऐ':'ai','ओ':'o','औ':'au','ऑ':'o','ॐ':'om'}
V_SIGN = {'ा':'ā','ि':'i','ी':'ī','ु':'u','ू':'ū','ृ':'ri','े':'e','ै':'ai','ो':'o','ौ':'au','ॉ':'o'}
CONS = {'क':'k','ख':'kh','ग':'g','घ':'gh','ङ':'n','च':'ch','छ':'chh','ज':'j','झ':'jh','ञ':'n',
        'ट':'t','ठ':'th','ड':'d','ढ':'dh','ण':'n','त':'t','थ':'th','द':'d','ध':'dh','न':'n',
        'प':'p','फ':'ph','ब':'b','भ':'bh','म':'m','य':'y','र':'r','ल':'l','ळ':'l','व':'v',
        'श':'sh','ष':'sh','स':'s','ह':'h','क़':'q','ख़':'kh','ग़':'gh','ज़':'z','ड़':'d','ढ़':'dh','फ़':'f'}
NUKTA='़'; VIRAMA='्'; ANUS='ं'; CANDRA='ँ'; VISARGA='ः'; AVAGRAHA='ऽ'
NASAL_BY_NEXT = {'k':'n','g':'n','c':'n','j':'n','t':'n','d':'n','n':'n','p':'m','b':'m','m':'m'}

def _syllables(word):
    """Return list of units: ('C', roman, has_inherent_a_bool, cluster_flag) or ('V', roman) or ('N', nasal marker)."""
    units=[]; i=0; w=word
    while i < len(w):
        ch=w[i]
        if i+1 < len(w) and w[i+1]==NUKTA and ch+NUKTA in CONS:
            ch=ch+NUKTA; i+=1
        if ch in CONS:
            rom=CONS[ch]; j=i+1
            if j < len(w) and w[j]==VIRAMA:
                units.append(['C',rom,False,ch]); i=j+1; continue
            if j < len(w) and w[j] in V_SIGN:
                units.append(['C',rom,False,ch]); units.append(['v',V_SIGN[w[j]]]); i=j+1; continue
            units.append(['C',rom,True,ch]); i=j; continue
        if ch in V_IND: units.append(['V',V_IND[ch]]); i+=1; continue
        if ch in (ANUS,CANDRA): units.append(['N',ch]); i+=1; continue
        if ch==VISARGA: units.append(['H']); i+=1; continue
        if ch==AVAGRAHA: units.append(['A']); i+=1; continue
        units.append(['X',ch]); i+=1
    return units

def _is_vowelish(u): return u[0] in ('V','v') or (u[0]=='C' and u[2])

def translit_word(word, sanskrit=False, mode='hi'):
    u=_syllables(word)
    if not u: return word
    if not sanskrit:
        # word-final schwa deletion (keep after clusters like 'tr','ny', and in 1-akshara words)
        cons_idx=[k for k,x in enumerate(u) if x[0]=='C']
        last=len(u)-1
        akshara = sum(1 for x in u if _is_vowelish(x))
        if u[last][0]=='C' and u[last][2] and akshara>1:
            prev_is_cons = last>0 and u[last-1][0]=='C' and not u[last-1][2]
            keep = prev_is_cons and (u[last][1] in ('r','y','v','m','n'))
            if not keep: u[last][2]=False
        # medial schwa deletion, right-to-left: V C [a] C V  -> delete
        k=len(u)-2
        while k>0:
            x=u[k]
            if x[0]=='C' and x[2]:
                before = u[k-1]
                after = u[k+1] if k+1 < len(u) else None
                after2 = u[k+2] if k+2 < len(u) else None
                prev_vowel = _is_vowelish(before) or before[0]=='N'
                # preceding unit must be a vowel-bearing syllable whose consonant is single
                single_before = before[0]=='C' and before[2] and not (k-2>=0 and u[k-2][0]=='C' and not u[k-2][2])
                if before[0] in ('v','V'):
                    # vowel sign belongs to consonant before it; check that consonant is single
                    single_before = not (k-3>=0 and u[k-3][0]=='C' and not u[k-3][2])
                next_cv = after is not None and after[0]=='C' and (after[2] or (after2 is not None and after2[0]=='v'))
                if after is not None and after[0]=='C' and after[1]=='h' and after2 is not None and after2[0]=='v' and after2[1] in ('i','ī'):
                    next_cv=False
                if after is not None and after[0]=='C' and after[2] and k+2==len(u)-1 and u[-1][0]=='N':
                    next_cv=False
                if mode=='mr': next_cv=False
                if prev_vowel and single_before and next_cv:
                    x[2]=False; k-=2; continue
            k-=1
    out=[]
    for idx,x in enumerate(u):
        t=x[0]
        if t=='C': out.append(x[1]+('a' if x[2] else ''))
        elif t in ('V','v'): out.append(x[1])
        elif t=='N':
            nxt=next((y for y in u[idx+1:] if y[0]=='C'),None)
            if x[1]==ANUS and nxt is not None and idx+1<len(u) and u[idx+1][0]=='C':
                out.append(NASAL_BY_NEXT.get(nxt[1][0],'n'))
            elif x[1]==ANUS and idx==len(u)-1 and (sanskrit or (idx>0 and u[idx-1][0]=='C' and u[idx-1][2])): out.append('m')
            else: out.append('n')
        elif t=='H': out.append('' if (not sanskrit and idx<len(u)-1) else 'h')
        elif t=='A': out.append("'")
        else: out.append(x[1])
    s=''.join(out)
    s=s.replace('jny','gy').replace('jn','gy') if 'ज्ञ' in word else s
    return s

WORD_OVERRIDES = {
 'जय':'jai','जै':'jai','मैं':'main','हैं':'hain','में':'mein','नहीं':'nahīn','नहिं':'nahin','यह':'yah','वह':'vah',
 'ॐ':'om','श्री':'shrī','श्रीगुरु':'shrī guru','कहाँ':'kahān','जहाँ':'jahān','तहँ':'tahan','महँ':'mahan',
 'आरती':'ārtī','कीजै':'kījai','कीजे':'kīje','लला':'lalā','गणेश':'ganesh','देवा':'devā',
 'हनुमान':'hanumān','राम':'rām','सीता':'sītā','लखन':'lakhan','शिव':'shiv','माता':'mātā','मैया':'maiyā',
 'स्वामी':'swāmī','स्वामि':'swāmi','ज्ञान':'gyān','अर्द्धांगी':'arddhāngī','अर्धांगी':'ardhāngī',
 'सुनहु':'sunahu','करहु':'karahu','हरहु':'harahu','बसहु':'basahu','देहु':'dehu','राखहु':'rākhahu',
 'कृष्ण':'krishna','विष्णु':'vishnu','लक्ष्मी':'lakshmī','दुर्गा':'durgā','दुर्गे':'durge','ब्रह्मा':'brahmā',
 'आस':'ās','तुम':'tum','तुझको':'tujhko','सब':'sab','अब':'ab','जब':'jab','तब':'tab','कब':'kab',
 'पवनसुत':'pavansut','रघुबर':'raghubar','रघुपति':'raghupati','रघुनाथ':'raghunāth','रघुबीर':'raghubīr',
 'महादेवा':'mahādevā','सिन्दूर':'sindūr','लड्डुअन':'laddu-an','पारब्रह्म':'pārbrahm','परमात्मा':'parmātmā',
 'सम्पत्ति':'sampatti','सम्पति':'sampati','अन्तर्यामी':'antaryāmī','पालनकर्ता':'pālankartā',
 'दुखहर्ता':'dukhhartā','सुखकर्ता':'sukhkartā','दुःखहर्ता':'duhkhhartā','दुःख':'duhkh','दुख':'dukh',
 'हरषि':'harashi','बरन':'baran','सरन':'saran','सरना':'saranā','करना':'karnā','परसा':'parsā',
 'अंजनि':'anjani','अंजना':'anjanā','संकट':'sankat','मंगल':'mangal','मूरति':'mūrati','सन्त':'sant','संत':'sant',
 'सन्तन':'santan','संतन':'santan','भक्तन':'bhaktan','गावे':'gāve','गावै':'gāvai','पावे':'pāve','पावै':'pāvai',
 'कहत':'kahat','शिवानन्द':'shivānand','शिवानंद':'shivānand','मनवांछित':'manvānchhit','गौरी':'gaurī',
 'जगदीश':'jagdīsh','जगदम्बे':'jagdambe','अम्बे':'ambe','श्यामा':'shyāmā','निशदिन':'nishdin','निशिदिन':'nishidin',
 'चन्द्रवदन':'chandravadan','रक्ताम्बर':'raktāmbar','कलेवर':'kalevar','कोटिक':'kotik','सम':'sam',
 'शुंभ':'shumbh','निशुंभ':'nishumbh','शुम्भ':'shumbh','निशुम्भ':'nishumbh','महिषासुर':'mahishāsur',
 'चण्ड':'chand','मुण्ड':'mund','मधु':'madhu','कैटभ':'kaitabh','भैरों':'bhairon','डमरू':'damrū','मृदंगा':'mridangā',
 'केहरि':'kehari','खड्ग':'khadg','खप्पर':'khappar','कंचन':'kanchan','अगर':'agar','कपूर':'kapūr','बाती':'bātī',
 'गिरिधर':'giridhar','मुरारी':'murārī','कुंजबिहारी':'kunjbihārī','नंदलाला':'nandlālā','बनमाली':'banmālī',
 'बनवारी':'banvārī','वृंदावन':'vrindāvan','मुरचंग':'murchang','मिरदंग':'mirdang','ग्वालिन':'gvālin',
 'सोंड':'sond','वक्रतुंड':'vakratund','शेंदुराची':'shendurāchī','पीतांबर':'pītāmbar','लंबोदर':'lambodar',
 'कुमति':'kumati','सुमति':'sumati','निवार':'nivār','संगी':'sangī','बजरंगी':'bajrangī','केसरीनंदन':'kesarīnandan',
 'चालीसा':'chālīsā','गोसाईं':'gosāīn','नाईं':'nāīn','साईं':'sāīn','साईंदास':'sāīndās','सत्यनारायण':'satyanārāyan',
 'नारायण':'nārāyan','रमणा':'ramanā','शनिदेव':'shanidev','शनि':'shani','शनिश्चर':'shanishchar',
 'त्रिभुवन':'tribhuvan','तत्त्वज्ञान':'tattvagyān','अज्ञान':'agyān','सर्वभूतेषु':'sarvabhūteshu',
 'पंचामृत':'panchāmrit','उद्धार':'uddhār','संहार':'sanhār','अंग':'ang','अंगे':'ange','संगे':'sange','संगा':'sangā',
 'विश्वनाथ':'vishvanāth','ब्रह्मचारी':'brahmachārī','कैलासा':'kailāsā','मृगछाला':'mrigchhālā','मुण्डन':'mundan',
 'त्रिगुणस्वामी':'trigunswāmī','प्रणवाक्षर':'pranavākshar','अविवेका':'avivekā','सदाशिव':'sadāshiv',
 'त्रिपुरारी':'tripurārī','कंसारी':'kansārī','गरूड़ासन':'garūdāsan','हंसासन':'hansāsan','वृषवाहन':'vrishvāhan',
 'पञ्चानन':'panchānan','चतुरानन':'chaturānan','एकानन':'ekānan','दसभुज':'dasbhuj','चतुर्भुज':'chaturbhuj',
 'कमण्डलु':'kamandalu','त्रिशूलधारी':'trishūldhārī','जगपालन':'jagpālan','सनकादिक':'sankādik',
 'गरुड़ादिक':'garudādik','भूतादिक':'bhūtādik','श्वेताम्बर':'shvetāmbar','पीताम्बर':'pītāmbar','बाघम्बर':'bāghambar',
 'अक्षमाला':'akshamālā','वनमाला':'vanmālā','मुण्डमाला':'mundamālā','शिवलहरी':'shivlaharī',
 'ऋद्धि':'riddhi','सिद्धि':'siddhi','निरंजनी':'niranjanī','क्षीरोदधि':'kshīrodadhi','चतुर्दश':'chaturdash',
 'जीवन':'jīvan','भवनिधि':'bhavnidhi','प्रकाशिनी':'prakāshinī','निवासिनी':'nivāsinī','महालक्ष्मीजी':'mahālakshmījī',
 'सरस्वती':'saraswatī','सदगुण':'sadgun','विख्याता':'vikhyātā','पद्मासिनि':'padmāsini','चन्द्रवदनि':'chandravadani',
 'मंथरा':'mantharā','रावण':'rāvan','ज्ञानचक्षु':'gyānchakshu','निस्तार':'nistār','प्रदायिनि':'pradāyini',
 'अग्नि':'agni','चन्द्र':'chandra','चंद्र':'chandra','मंत्र':'mantra','मन्त्र':'mantra','पुत्र':'putra','सूर्य':'sūrya',
 'धर्म':'dharm','कर्म':'karm','यज्ञ':'yagya','वस्त्र':'vastra','नेत्र':'netra','मित्र':'mitra','शस्त्र':'shastra',
 'सहस्र':'sahasra','अस्त्र':'astra','चरित्र':'charitra','दशरथ':'dasharath','दायकु':'dāyaku','भरतहि':'bharatahi','पवनतनय':'pavantanay','प्राणपति':'prānpati','नागफनी':'nāgphanī','उदधि':'udadhi','त्रयोदशी':'trayodashī','दीनदयाल':'dīndayāl','विपति':'vipati','हृदयँ':'hridayan','गुननिधि':'gunanidhi','श्रीरघुबीर':'Shrī Raghubīr','श्रीपति':'Shrīpati','श्रीबनवारी':'Shrī Banvārī','दुःख':'dukh','दुःखहारी':'dukhhārī','स्वीकार':'swīkār','दयामय':'dayāmay','सियाराम':'Siyārām','सियारामजी':'Siyārāmjī','हनुमानजी':'Hanumānjī','जनम':'janam','करनी':'karnī','हरनी':'harnī','कमलनयन':'kamalnayan',
}

PROPER = {'ganesh','rām','sītā','lakhan','hanumān','shiv','shankar','pārvatī','mahādevā','mahādev','gaurī',
  'krishna','vishnu','lakshmī','durgā','ambe','brahmā','hari','raghubar','raghupati','raghunāth','raghubīr','raghurāī',
  'jānakī','anjani','anjanā','kesarī','tulsīdās','lankā','sugrīv','bibhīshan','nārad','sārad','kuber','sāīn',
  'satyanārāyan','nārāyan','shani','sūrya','saraswatī','kailāsā','kāshī','nandī','gangā','gange','rādhikā',
  'vrindāvan','giridhar','murārī','jagdīsh','shivānand','shirdī','ayodhyādās','devīdās','rāvan','mantharā',
  'sagar','vibhīshan','rāmchandra','shanidev','jagdambe','jagdamb','jagdambā','durge','girijā','tulsī','bhavānī','jānkī','jānakī','kashyap','aditi','prahlād','hanumat','hanumant','kunjbihārī','vishvanāth','kārtik','jamvant','satyadevā','ambā','lakshman','kaikeī','kaikeihun','draupadī','pāndav','kaurav','ravi','bibhīshan','raghunandan','govind','gaurisut','shambhu','ganrāū','sugrīvahin','sāīndās','bharat','shārad','jamvant','pavan','raghunandan','dasharath','kaushalyā','mahishāsur'}

TOKEN_RE = re.compile(r"[ऀ-ॣॱ-ॿ‌‍]+|[^ऀ-ॣॱ-ॿ]+")

def translit_line(line, sanskrit=False, overrides=None, mode='hi'):
    ov = dict(WORD_OVERRIDES); ov.update(overrides or {})
    out=[]
    for tok in TOKEN_RE.findall(line):
        if re.match("[ऀ-ॣॱ-ॿ]", tok):
            if not sanskrit and tok in ov: r=ov[tok]
            elif sanskrit and tok in (overrides or {}): r=overrides[tok]
            elif tok=='ॐ': r='om'
            else: r=translit_word(tok, sanskrit, mode)
            out.append(r)
        else:
            t=tok.replace('॥','||').replace('।','|').replace('॰','.')
            out.append(t)
    s=''.join(out)
    s=s.replace('||','\u2016')
    s=re.sub(r"\s*\|\s*"," | ",s); s=re.sub(r"\s*\u2016\s*"," || ",s)
    s=s.replace('\u2016','||').strip()
    # capitalise proper names and first letter
    def cap(m):
        w=m.group(0); return w[0].upper()+w[1:] if w.lower() in PROPER else w
    s=re.sub(r"[a-zāīūA-Z'\-]+",cap,s)
    s=s.strip()
    s=re.sub(r"(\| )([a-zāīū])",lambda m:m.group(1)+m.group(2).upper(),s)
    m=re.search(r"[A-Za-zāīūĀĪŪ]",s)
    return s[:m.start()]+s[m.start()].upper()+s[m.start()+1:] if m and m.start()<=1 else s

def translit(text, sanskrit=False, overrides=None, mode='hi'):
    return '\n'.join(translit_line(l, sanskrit, overrides, mode) for l in text.split('\n'))

if __name__=='__main__':
    tests = ["जय हनुमान ज्ञान गुन सागर। जय कपीस तिहुँ लोक उजागर॥",
      "ॐ जय जगदीश हरे, स्वामी जय जगदीश हरे।","भक्त जनों के संकट, दास जनों के संकट, क्षण में दूर करे॥",
      "बरनउँ रघुबर बिमल जसु, जो दायकु फल चारि॥","सुख सम्पति घर आवे, कष्ट मिटे तन का॥",
      "मात पिता तुम मेरे, शरण गहूँ किसकी।","अन्धन को आँख देत, कोढ़िन को काया।","पान चढ़े फूल चढ़े, और चढ़े मेवा।",
      "गले में बैजंती माला, बजावै मुरली मधुर बाला।","कनकमय मोर मुकुट बिलसै, देवता दरसन को तरसैं।",
      "धड़कन समझना पहचानना कमलनयन","लंका सो कोट समुद्र-सी खाई। जात पवनसुत बार न लाई॥"]
    for t in tests: print(translit(t))
    print(translit("वक्रतुण्ड महाकाय सूर्यकोटि समप्रभ। निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा॥",True))
    print(translit("ॐ भूर्भुवः स्वः तत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि धियो यो नः प्रचोदयात्॥",True))
    print(translit("वन्देऽहं करुणाकरं रघुवरं भूपालचूडामणिम्॥",True))

# --- additions for the 2026 website content ---
WORD_OVERRIDES.update({'श्रृंगार': 'shringār', 'करुणामयी': 'karunāmayī', 'दयामयी': 'dayāmayī', 'परमप्रिय': 'parampriy',
    'गणपति': 'ganpati', 'गजबदन': 'gajbadan', 'जननि': 'janani', 'जगजननी': 'jagjananī', 'श्यामवरण': 'shyāmvaran',
    'भावमय': 'bhāvmay', 'केसरिया': 'kesariyā', 'घड़ियावल': 'ghadiyāval', 'बृहस्पति': 'Brihaspati', 'सन्तोषी': 'Santoshī',
    'संतोषी': 'Santoshī', 'खाटू': 'Khātū', 'श्याम': 'Shyām', 'श्याम-श्याम': 'Shyām-Shyām', 'रामसुन्दर': 'Rāmsundar'})
PROPER |= {'girijā', 'umā', 'dasrath', 'ahirāvan', 'lachhiman', 'angad', 'sushen', 'prayāg', 'durvāsā', 'janakpur', 'avadhpurī', 'rāmāyan'}
