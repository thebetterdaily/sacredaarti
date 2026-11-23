# -*- coding: utf-8 -*-
"""Additions for the website (Nov 2026): popular aartis, chalisas and mantras not in the first edition of the book.
Texts checked against widely published versions (Gita Press style, BhaktiBharat, Drik Panchang). Meanings are original."""
from content_aartis import S

def P(hi, en, label=None):
    return S(hi, en, label=label, refrain=False)

MORE = [
# ---------------- aartis ----------------
dict(slug='om-jai-shri-shyam-hare', title='Om Jai Shri Shyam Hare (Khatu Shyam Aarti)', hi='ॐ जय श्री श्याम हरे', deity='KhatuShyam', kind='aarti', lang='hi',
 img='khatushyam', pop=15, days=['Ekadashi','Sunday'], fest=['Phalgun Mela','Ekadashi','Dev Uthani Ekadashi'],
 about="The aarti of Baba Khatu Shyam, worshipped at Khatu in Rajasthan as Krishna in the form of Barbarika, the grandson of Bhima who offered his head before the Mahabharata war. It is sung at the Khatu Shyam temple and at Shyam bhajan evenings across North India, especially on Ekadashi.",
 refrain='ॐ जय श्री श्याम हरे, बाबा जय श्री श्याम हरे',
 stanzas=[
 S("""ॐ जय श्री श्याम हरे, बाबा जय श्री श्याम हरे।
खाटू धाम विराजत, अनुपम रूप धरे॥""","Victory to Shri Shyam, O Baba Shyam, who sits in his home at Khatu in a form beyond compare.", refrain=False),
 S("""रतन जड़ित सिंहासन, सिर पर चंवर ढुरे।
तन केसरिया बागो, कुण्डल श्रवण पड़े॥""","He sits on a jewelled throne with a whisk waved over his head; he wears a saffron robe, with earrings in his ears."),
 S("""गल पुष्पों की माला, सिर पर मुकुट धरे।
खेवत धूप अग्नि पर, दीपक ज्योति जले॥""","A garland of flowers hangs at his neck and a crown sits on his head; incense smoulders on the coals and the lamp burns bright."),
 S("""मोदक खीर चूरमा, सुवरण थाल भरे।
सेवक भोग लगावत, सेवा नित्य करे॥""","Golden plates are filled with modak, kheer and churma; his servants offer them to him and serve him every day."),
 S("""झांझ कटोरा और घड़ियावल, शंख मृदंग घुरे।
भक्त आरती गावे, जय-जयकार करे॥""","Cymbals, bells and gongs ring out with the conch and the drum, as devotees sing the aarti and cry out his victory."),
 S("""जो ध्यावे फल पावे, सब दुःख से उबरे।
सेवक जन निज मुख से, श्री श्याम-श्याम उचरे॥""","Whoever meditates on him receives the fruit and is freed from every sorrow; his devotees keep the name 'Shyam, Shyam' on their lips."),
 S("""श्री श्याम बिहारी जी की आरती, जो कोई नर गावे।
कहत भक्त-जन, मनवांछित फल पावे॥""","Whoever sings this aarti of Shri Shyam Bihari, say the devotees, receives what the heart desires."),
 S("""जय श्री श्याम हरे, बाबा जी श्री श्याम हरे।
निज भक्तों के तुमने, पूरण काज करे॥""","Victory to Shri Shyam, O revered Baba: you have fulfilled every task of your devotees."),
 ]),

dict(slug='jai-santoshi-mata', title='Jai Santoshi Mata', hi='जय सन्तोषी माता', deity='Santoshi', kind='aarti', lang='hi',
 img='santoshi', pop=17, days=['Friday'], fest=['Santoshi Mata Vrat (Fridays)'],
 about="The aarti of Santoshi Mata, the goddess of contentment, sung at the end of the Friday fast kept in her honour. Jaggery and roasted chana are her offering, and sour food is avoided on the day of the fast.",
 refrain='जय सन्तोषी माता, मैया जय सन्तोषी माता',
 stanzas=[
 S("""जय सन्तोषी माता, मैया जय सन्तोषी माता।
अपने सेवक जन को, सुख सम्पति दाता॥""","Victory to Santoshi Mata, O Mother, who gives happiness and prosperity to those who serve her.", refrain=False),
 S("""सुन्दर चीर सुनहरी, माँ धारण कीन्हो।
हीरा पन्ना दमके, तन श्रृंगार लीन्हो॥""","The Mother wears a beautiful golden sari; diamonds and emeralds sparkle on her adorned form."),
 S("""गेरू लाल छटा छवि, बदन कमल सोहे।
मंद हँसत करुणामयी, त्रिभुवन जन मोहे॥""","Her face glows like a lotus with a red-ochre radiance; her gentle, compassionate smile enchants the three worlds."),
 S("""स्वर्ण सिंहासन बैठी, चंवर ढुरें प्यारे।
धूप, दीप, मधु, मेवा, भोग धरें न्यारे॥""","She sits on a golden throne as whisks are lovingly waved; incense, lamps, honey and dry fruits are set before her."),
 S("""गुड़ अरु चना परमप्रिय, तामें संतोष कियो।
संतोषी कहलाई, भक्तन वैभव दियो॥""","Jaggery and chana are dearest to her, and she was content with them; so she is called Santoshi, and she gives abundance to her devotees."),
 S("""शुक्रवार प्रिय मानत, आज दिवस सोही।
भक्त मंडली छाई, कथा सुनत मोही॥""","Friday is her favourite day, and today is that day; her devotees have gathered and are absorbed in hearing her story."),
 S("""मंदिर जगमग ज्योति, मंगल ध्वनि छाई।
विनय करें हम सेवक, चरनन सिर नाई॥""","The temple glitters with light and auspicious sounds fill the air; we, your servants, bow our heads at your feet and pray."),
 S("""भक्ति भावमय पूजा, अंगीकृत कीजै।
जो मन बसे हमारे, इच्छा फल दीजै॥""","Accept this worship offered with devotion, and grant the wish that lives in our hearts."),
 S("""दुखी, दरिद्री, रोगी, संकटमुक्त किए।
बहु धनधान्य भरे घर, सुख सौभाग्य दिए॥""","You have freed the sorrowful, the poor and the sick from their troubles, filled homes with wealth and grain, and given joy and good fortune."),
 S("""ध्यान धर्यो जिस जन ने, मनवांछित फल पायो।
पूजा कथा श्रवण कर, घर आनंद आयो॥""","Whoever meditated on you received what the heart desired; by worshipping and hearing your story, joy came into the home."),
 S("""शरण गहे की लज्जा, राखियो जगदंबे।
संकट तू ही निवारे, दयामयी अंबे॥""","O Mother of the world, protect the honour of those who take refuge in you; you alone remove our troubles, O compassionate Amba."),
 S("""संतोषी माँ की आरती, जो कोई नर गावे।
ऋद्धि-सिद्धि सुख संपत्ति, जी भरकर पावे॥""","Whoever sings this aarti of Santoshi Ma receives prosperity, success, happiness and wealth in full measure."),
 ]),

dict(slug='om-jai-brihaspati-deva', title='Om Jai Brihaspati Deva', hi='ॐ जय बृहस्पति देवा', deity='Brihaspati', kind='aarti', lang='hi',
 img='brihaspati', pop=19, days=['Thursday'], fest=['Brihaspativar Vrat (Thursdays)'],
 about="The aarti of Brihaspati Dev, the guru of the gods and the lord of Thursday (Guruvar). It closes the Thursday fast, when yellow clothes are worn and bananas, gram dal and yellow sweets are offered. The last line carries the poet's name, Jethanand.",
 refrain='ॐ जय बृहस्पति देवा, स्वामी जय बृहस्पति देवा',
 stanzas=[
 S("""ॐ जय बृहस्पति देवा, स्वामी जय बृहस्पति देवा।
छिन छिन भोग लगाऊँ, कदली फल मेवा॥""","Victory to Lord Brihaspati, O Master; every moment I offer you bananas and dry fruits.", refrain=False),
 S("""तुम पूरण परमात्मा, तुम अन्तर्यामी।
जगतपिता जगदीश्वर, तुम सबके स्वामी॥""","You are the complete Supreme Self who knows every heart; father and lord of the world, you are master of all."),
 S("""चरणामृत निज निर्मल, सब पातक हर्ता।
सकल मनोरथ दायक, कृपा करो भर्ता॥""","The pure water that has washed your feet takes away every sin; O sustainer, giver of all wishes, be gracious to us."),
 S("""तन, मन, धन अर्पण कर, जो जन शरण पड़े।
प्रभु प्रकट तब होकर, आकर द्वार खड़े॥""","When someone offers body, mind and wealth and takes refuge in you, the Lord appears and comes to stand at their door."),
 S("""दीनदयाल दयानिधि, भक्तन हितकारी।
पाप दोष सब हर्ता, भव बंधन हारी॥""","Kind to the humble and an ocean of mercy, you are the well-wisher of devotees; you remove all sins and faults and free us from worldly bondage."),
 S("""सकल मनोरथ दायक, सब संशय हारो।
विषय विकार मिटाओ, संतन सुखकारी॥""","Giver of every wish, take away all our doubts; wipe out the disorders of the senses, O bringer of joy to the saints."),
 S("""जो कोई आरती तेरी, प्रेम सहित गावे।
जेठानन्द आनन्दकर, सो निश्चय पावे॥""","Whoever sings your aarti with love, says Jethanand, will surely attain joy."),
 ]),

dict(slug='aarti-shri-ramayan-ji-ki', title='Aarti Shri Ramayan Ji Ki', hi='आरती श्री रामायण जी की', deity='Ram', kind='aarti', lang='hi',
 img='ram', pop=None, days=['Daily'], fest=['Ramayan Path','Ram Navami','Diwali'],
 about="The aarti of the Ramayan itself, sung at the end of a Ramcharitmanas or Sundar Kand recitation. It is in Tulsidas's Awadhi and names the sages, gods and poets who have sung Rama's story.",
 refrain='आरती श्री रामायण जी की। कीरति कलित ललित सिय पी की',
 stanzas=[
 S("""आरती श्री रामायण जी की।
कीरति कलित ललित सिय पी की॥""","Aarti to the holy Ramayan, the graceful and lovely glory of Sita's beloved.", refrain=False),
 S("""गावत ब्रह्मादिक मुनि नारद।
बालमीक बिग्यान बिसारद॥
सुक सनकादि सेष अरु सारद।
बरनि पवनसुत कीरति नीकी॥""","Brahma and the gods, the sage Narada and Valmiki, master of wisdom, sing it; Shuka, Sanaka and his brothers, Shesha and Sharada sing it, and Hanuman, son of the Wind, describes its beautiful glory."),
 S("""गावत बेद पुरान अष्टदस।
छओं सास्त्र सब ग्रंथन को रस॥
मुनि जन धन संतन को सरबस।
सार अंस संमत सबही की॥""","The Vedas and the eighteen Puranas sing it; it is the essence of the six schools and of every scripture. It is the wealth of sages and the everything of saints, the core that all agree on."),
 S("""गावत संतत संभु भवानी।
अरु घटसंभव मुनि बिग्यानी॥
ब्यास आदि कबिबर्ज बखानी।
कागभुसुंडि गरुड़ के ही की॥""","Shiva and Bhavani sing it without end, as does the wise sage Agastya; Vyasa and the great poets have told it, and it is dear to the hearts of Kakbhushundi and Garuda."),
 S("""कलिमल हरनि बिषय रस फीकी।
सुभग सिंगार मुक्ति जुबती की॥
दलन रोग भव मूरि अमी की।
तात मात सब बिधि तुलसी की॥""","It washes away the stains of the dark age and makes the pleasures of the senses taste dull; it is the lovely adornment of liberation. It is the nectar-root that destroys the disease of worldly life, and in every way it is father and mother to Tulsi."),
 ]),

dict(slug='jai-jai-tulsi-mata', title='Jai Jai Tulsi Mata', hi='जय जय तुलसी माता', deity='Tulsi', kind='aarti', lang='hi',
 img='tulsi', pop=None, days=['Daily'], fest=['Tulsi Vivah','Kartik month','Dev Uthani Ekadashi'],
 about="The aarti of Tulsi, the holy basil, worshipped as a goddess and as the beloved of Vishnu. Many homes light a lamp at the tulsi plant every evening, and the aarti is sung especially through the month of Kartik and at Tulsi Vivah.",
 refrain='जय जय तुलसी माता, मैया जय तुलसी माता',
 stanzas=[
 S("""जय जय तुलसी माता, मैया जय तुलसी माता।
सब जग की सुख दाता, वर दाता॥""","Victory to Mother Tulsi, who gives happiness and blessings to the whole world.", refrain=False),
 S("""सब योगों के ऊपर, सब रोगों के ऊपर।
रज से रक्षा करके, भव त्राता॥""","You are above every discipline and greater than every illness; you protect us from impurity and carry us across worldly life."),
 S("""बटु पुत्री हे श्यामा, सुर बल्ली हे ग्राम्या।
विष्णु प्रिये जो तुमको सेवे, सो नर तर जाता॥""","O dark-leaved one, divine creeper who lives among the homes of the village: beloved of Vishnu, whoever serves you is carried across."),
 S("""हरि के शीश विराजत, त्रिभुवन से हो वन्दित।
पतित जनो की तारिणी, विख्याता॥""","You rest on the head of Hari and are honoured by the three worlds; you are famed as the saviour of the fallen."),
 S("""लेकर जन्म विजन में, आई दिव्य भवन में।
मानव लोक तुम्ही से, सुख संपति पाता॥""","Born in the wild, you came to live in sacred homes; through you the human world receives happiness and prosperity."),
 S("""हरि को तुम अति प्यारी, श्यामवरण तुम्हारी।
प्रेम अजब है उनका, तुमसे कैसा नाता॥""","You are most dear to Hari, and your colour is his dark hue; how wondrous is his love, and how deep his bond with you."),
 ]),

# ---------------- chalisas and stutis ----------------
dict(slug='ganesh-chalisa', title='Shri Ganesh Chalisa', hi='श्री गणेश चालीसा', deity='Ganesha', kind='chalisa', lang='hi',
 img='ganesha', pop=18, days=['Wednesday'], fest=['Ganesh Chaturthi','Sankashti Chaturthi','Wednesday'],
 about="Forty verses on Ganesha in Awadhi, telling of his birth to Parvati, how Shani's glance took his head and Vishnu brought an elephant's head in its place, and how he won the race around the world by circling his parents. It is recited on Wednesdays, on Sankashti Chaturthi and before any new undertaking.",
 stanzas=[
 P("""जय गणपति सदगुण सदन, कविवर बदन कृपाल।
विघ्न हरण मंगल करण, जय जय गिरिजालाल॥""","Victory to Ganapati, home of every virtue, eloquent of speech and kind; remover of obstacles and maker of good fortune, victory to the darling of Girija.","Doha"),
 P("""जय जय जय गणपति गणराजू। मंगल भरण करण शुभ काजू॥
जय गजबदन सदन सुखदाता। विश्व विनायक बुद्धि विधाता॥
वक्र तुण्ड शुचि शुण्ड सुहावन। तिलक त्रिपुण्ड भाल मन भावन॥
राजत मणि मुक्तन उर माला। स्वर्ण मुकुट शिर नयन विशाला॥""","Victory to Ganapati, king of the ganas, who fills life with blessings and makes every task auspicious. Victory to the elephant-faced giver of joy, Vinayaka of the world and creator of wisdom. His curved trunk is lovely, and the three-line tilak on his brow delights the mind. A garland of gems and pearls shines on his chest, a golden crown on his head, and his eyes are wide.","Chaupai 1–4"),
 P("""पुस्तक पाणि कुठार त्रिशूलं। मोदक भोग सुगन्धित फूलं॥
सुन्दर पीताम्बर तन साजित। चरण पादुका मुनि मन राजित॥
धनि शिव सुवन षडानन भ्राता। गौरी ललन विश्व-विख्याता॥
ऋद्धि-सिद्धि तव चंवर सुधारे। मूषक वाहन सोहत द्वारे॥""","In his hands are a book, an axe and a trident; he is offered modak and fragrant flowers. A beautiful yellow cloth adorns his body, and his sandalled feet shine in the minds of sages. Blessed son of Shiva and brother of six-faced Kartikeya, darling of Gauri, famous through the world: Riddhi and Siddhi wave whisks over him, and his mouse mount waits at the door.","Chaupai 5–8"),
 P("""कहौं जन्म शुभ कथा तुम्हारी। अति शुचि पावन मंगलकारी॥
एक समय गिरिराज कुमारी। पुत्र हेतु तप कीन्हा भारी॥
भयो यज्ञ जब पूर्ण अनूपा। तब पहुँच्यो तुम धरि द्विज रूपा॥
अतिथि जानि कै गौरी सुखारी। बहुविधि सेवा करी तुम्हारी॥""","I tell the auspicious story of your birth, most pure, holy and blessed. Once the daughter of the mountain king performed great austerities for a son. When her matchless sacrifice was complete, you came in the form of a Brahmin. Knowing you to be a guest, Gauri joyfully served you in many ways.","Chaupai 9–12"),
 P("""अति प्रसन्न ह्वै तुम वर दीन्हा। मातु पुत्र हित जो तप कीन्हा॥
मिलहि पुत्र तुहि, बुद्धि विशाला। बिना गर्भ धारण यहि काला॥
गणनायक गुण ज्ञान निधाना। पूजित प्रथम रूप भगवाना॥
अस कहि अन्तर्धान रूप ह्वै। पलना पर बालक स्वरूप ह्वै॥""","Well pleased, you granted the boon for which the Mother had done penance: 'You shall have a son of great wisdom, at this very time, without bearing him in the womb: leader of the ganas, treasury of virtue and knowledge, the form of God worshipped first.' Saying this you vanished, and appeared as a child in the cradle.","Chaupai 13–16"),
 P("""बनि शिशु रुदन जबहिं तुम ठाना। लखि मुख सुख नहिं गौरि समाना॥
सकल मगन, सुखमंगल गावहिं। नभ ते सुरन, सुमन वर्षावहिं॥
शम्भु, उमा, बहु दान लुटावहिं। सुर मुनिजन, सुत देखन आवहिं॥
लखि अति आनन्द मंगल साजा। देखन भी आये शनि राजा॥""","When, as an infant, you began to cry, Gauri's joy at seeing your face knew no bounds. Everyone rejoiced and sang songs of blessing, and the gods showered flowers from the sky. Shambhu and Uma gave gifts freely, and gods and sages came to see the child. Seeing the great joy and celebration, King Shani too came to look.","Chaupai 17–20"),
 P("""निज अवगुण गुनि शनि मन माहीं। बालक, देखन चाहत नाहीं॥
गिरिजा कछु मन भेद बढ़ायो। उत्सव मोर, न शनि तुहि भायो॥
कहन लगे शनि, मन सकुचाई। का करिहौ, शिशु मोहि दिखाई॥
नहिं विश्वास, उमा उर भयऊ। शनि सों बालक देखन कहयऊ॥""","Mindful of the harm in his own gaze, Shani did not want to look at the child. Girija was hurt and said, 'Does my celebration not please you, Shani?' Shani, uneasy, replied, 'What will you gain by showing me the child?' Uma did not believe him and asked Shani to look at the baby.","Chaupai 21–24"),
 P("""पड़तहिं शनि दृग कोण प्रकाशा। बालक सिर उड़ि गयो अकाशा॥
गिरिजा गिरीं विकल ह्वै धरणी। सो दुःख दशा गयो नहिं वरणी॥
हाहाकार मच्यो कैलाशा। शनि कीन्हों लखि सुत को नाशा॥
तुरत गरुड़ चढ़ि विष्णु सिधायो। काटि चक्र सो गज सिर लाये॥""","As soon as the light of Shani's glance fell on him, the child's head flew off into the sky. Girija fell to the ground in anguish, a grief that cannot be described. A cry of sorrow rose in Kailash, for Shani's look had destroyed the son. At once Vishnu set out on Garuda, and with his discus brought back an elephant's head.","Chaupai 25–28"),
 P("""बालक के धड़ ऊपर धारयो। प्राण मन्त्र पढ़ि शंकर डारयो॥
नाम गणेश शम्भु तब कीन्हे। प्रथम पूज्य बुद्धि निधि, वर दीन्हे॥
बुद्धि परीक्षा जब शिव कीन्हा। पृथ्वी कर प्रदक्षिणा लीन्हा॥
चले षडानन, भरमि भुलाई। रचे बैठ तुम बुद्धि उपाई॥""","He set it on the child's body, and Shankar recited the mantra of life over him. Shambhu then named him Ganesha and blessed him as the first to be worshipped and the treasury of wisdom. When Shiva tested their wisdom by asking his sons to circle the earth, six-faced Kartikeya rushed off in confusion, while you sat and thought of a wiser way.","Chaupai 29–32"),
 P("""चरण मातु-पितु के धर लीन्हें। तिनके सात प्रदक्षिण कीन्हें॥
धनि गणेश कहि शिव हिय हरषे। नभ ते सुरन सुमन बहु बरसे॥
तुम्हरी महिमा बुद्धि बड़ाई। शेष सहसमुख सके न गाई॥
मैं मतिहीन मलीन दुखारी। करहुँ कौन विधि विनय तुम्हारी॥""","You held your mother's and father's feet and walked around them seven times. 'Blessed is Ganesha,' said Shiva with a glad heart, and the gods showered flowers from the sky. Even thousand-mouthed Shesha cannot sing the greatness of your wisdom; how can I, dull, impure and troubled, praise you?","Chaupai 33–36"),
 P("""भजत रामसुन्दर प्रभुदासा। जग प्रयाग, ककरा, दुर्वासा॥
अब प्रभु दया दीन पर कीजै। अपनी शक्ति भक्ति कुछ दीजै॥""","Your servant Ramsundar sings your praise, as do Prayag, Kakra and Durvasa. Now, Lord, be kind to this humble one and grant me some of your strength and devotion.","Chaupai 37–40"),
 P("""श्री गणेश यह चालीसा, पाठ करै कर ध्यान।
नित नव मंगल गृह बसै, लहे जगत सन्मान॥
सम्बन्ध अपने सहस्र दश, ऋषि पंचमी दिनेश।
पूरण चालीसा भयो, मंगल मूर्ति गणेश॥""","Whoever recites this Chalisa of Shri Ganesha with attention will find new blessings in the home every day and be honoured by the world. Completed in the year one thousand and ten of its era, on Rishi Panchami: the Chalisa of Ganesha, form of all that is auspicious, is complete.","Doha"),
 ]),

dict(slug='lakshmi-chalisa', title='Shri Lakshmi Chalisa', hi='श्री लक्ष्मी चालीसा', deity='Lakshmi', kind='chalisa', lang='hi',
 img='lakshmi', pop=16, days=['Friday'], fest=['Diwali','Dhanteras','Sharad Purnima','Friday'],
 about="Forty verses to Lakshmi, goddess of wealth and good fortune, recalling her rising from the churning of the ocean and her life beside Vishnu in every avatar, as Sita with Rama and Rukmini with Krishna. It is recited on Fridays and during the Diwali season. The closing doha carries the poet's name, Ramdas.",
 stanzas=[
 P("""मातु लक्ष्मी करि कृपा, करो हृदय में वास।
मनोकामना सिद्ध करि, पुरवहु मेरी आस॥""","Mother Lakshmi, be gracious and dwell in my heart; fulfil my wishes and complete my hopes.","Doha"),
 P("""यही मोर अरदास, हाथ जोड़ विनती करूँ।
सब विधि करौ सुवास, जय जननि जगदंबिका॥""","This is my plea, made with folded hands: make your home with us in every way, victory to you, Mother of the world.","Soratha"),
 P("""सिन्धु सुता मैं सुमिरौं तोही। ज्ञान बुद्धि विद्या दो मोही॥
तुम समान नहिं कोई उपकारी। सब विधि पुरवहु आस हमारी॥
जय जय जगत जननि जगदम्बा। सबकी तुम ही हो अवलम्बा॥
तुम ही हो सब घट घट वासी। विनती यही हमारी खासी॥""","Daughter of the ocean, I remember you: give me knowledge, understanding and learning. No one is as generous as you; fulfil our hopes in every way. Victory to the Mother of the world, the support of all, who lives in every heart: this is our special prayer.","Chaupai 1–4"),
 P("""जगजननी जय सिन्धु कुमारी। दीनन की तुम हो हितकारी॥
विनवौं नित्य तुमहिं महारानी। कृपा करौ जग जननि भवानी॥
केहि विधि स्तुति करौं तिहारी। सुधि लीजै अपराध बिसारी॥
कृपा दृष्टि चितवो मम ओरी। जगजननी विनती सुन मोरी॥""","Victory to the Mother of the world, daughter of the ocean, friend of the poor. Every day I pray to you, great queen: be kind, Mother Bhavani. How can I praise you? Forget my faults and remember me. Turn your gracious eyes towards me, Mother, and hear my prayer.","Chaupai 5–8"),
 P("""ज्ञान बुद्धि जय सुख की दाता। संकट हरो हमारी माता॥
क्षीरसिन्धु जब विष्णु मथायो। चौदह रत्न सिन्धु में पायो॥
चौदह रत्न में तुम सुखरासी। सेवा कियो प्रभु बनि दासी॥
जब जब जन्म जहाँ प्रभु लीन्हा। रूप बदल तहँ सेवा कीन्हा॥""","Giver of knowledge, wisdom and happiness, take away our troubles, Mother. When Vishnu had the ocean of milk churned, fourteen jewels came out of it; among them you were the treasure of joy, and you served the Lord as his own. Wherever the Lord took birth, you changed your form and served him there.","Chaupai 9–12"),
 P("""स्वयं विष्णु जब नर तनु धारा। लीन्हेउ अवधपुरी अवतारा॥
तब तुम प्रगट जनकपुर माहीं। सेवा कियो हृदय पुलकाहीं॥
अपनायो तोहि अन्तर्यामी। विश्व विदित त्रिभुवन की स्वामी॥
तुम सम प्रबल शक्ति नहिं आनी। कहँ लौं महिमा कहौं बखानी॥""","When Vishnu himself took a human body and was born in Ayodhya, you appeared in Janakpur and served him with a thrilled heart. The knower of hearts took you as his own, and you became the famed queen of the three worlds. There is no power as great as yours; how far can I tell your glory?","Chaupai 13–16"),
 P("""मन क्रम वचन करै सेवकाई। मन इच्छित वांछित फल पाई॥
तजि छल कपट और चतुराई। पूजहिं विविध भाँति मन लाई॥
और हाल मैं कहौं बुझाई। जो यह पाठ करै मन लाई॥
ताको कोई कष्ट न होई। मन इच्छित पावै फल सोई॥""","Whoever serves you in thought, deed and word receives the fruit the heart desires. Leaving deceit and cleverness, they worship you in many ways with full attention. And I will tell you more: whoever recites this with the mind fixed on it suffers no hardship and gains what the heart wants.","Chaupai 17–20"),
 P("""त्राहि त्राहि जय दुःख निवारिणि। त्रिविध ताप भव बंधन हारिणि॥
जो चालीसा पढ़ै पढ़ावै। ध्यान लगाकर सुनै सुनावै॥
ताकौ कोई न रोग सतावै। पुत्र आदि धन सम्पत्ति पावै॥
पुत्रहीन अरु संपति हीना। अन्ध बधिर कोढ़ी अति दीना॥""","Save us, save us, remover of sorrow, who breaks the three kinds of suffering and the bonds of worldly life. Whoever reads this Chalisa or has it read, listens to it or recites it with attention, is troubled by no illness and gains children, wealth and property, even those without children or means, the blind, the deaf, the sick and the very poor.","Chaupai 21–24"),
 P("""विप्र बोलाय कै पाठ करावै। शंका दिल में कभी न लावै॥
पाठ करावै दिन चालीसा। ता पर कृपा करैं गौरीसा॥
सुख सम्पत्ति बहुत सी पावै। कमी नहीं काहू की आवै॥
बारह मास करै जो पूजा। तेहि सम धन्य और नहिं दूजा॥""","If they call a priest to recite it, never letting doubt into their hearts, and have it read for forty days, the Lord of Gauri blesses them. They gain much happiness and wealth and lack nothing. No one is as blessed as the one who worships you all twelve months of the year.","Chaupai 25–28"),
 P("""प्रतिदिन पाठ करै मन माहीं। उन सम कोउ जग में कहुँ नाहीं॥
बहुविधि क्या मैं करौं बड़ाई। लेय परीक्षा ध्यान लगाई॥
करि विश्वास करै व्रत नेमा। होय सिद्ध उपजै उर प्रेमा॥
जय जय जय लक्ष्मी भवानी। सब में व्यापित हो गुण खानी॥""","There is no one in the world like the one who recites it in their heart every day. Why should I praise it in so many ways? Try it with attention and see. Whoever keeps the fast and its rules with faith succeeds, and love wells up in the heart. Victory to Lakshmi Bhavani, mine of virtue, present in all.","Chaupai 29–32"),
 P("""तुम्हरो तेज प्रबल जग माहीं। तुम सम कोउ दयालु कहुँ नाहीं॥
मोहि अनाथ की सुधि अब लीजै। संकट काटि भक्ति मोहि दीजै॥
भूल चूक करि क्षमा हमारी। दर्शन दीजै दशा निहारी॥
बिन दर्शन व्याकुल अधिकारी। तुमहि अछत दुःख सहते भारी॥""","Your radiance is mighty in the world, and no one is as kind as you. Remember me now, helpless as I am: cut away my troubles and give me devotion. Forgive our mistakes and, seeing our state, show yourself to us. Without the sight of you your devotee is restless and suffers greatly, though you are here.","Chaupai 33–36"),
 P("""नहिं मोहिं ज्ञान बुद्धि है तन में। सब जानत हो अपने मन में॥
रूप चतुर्भुज करके धारण। कष्ट मोर अब करहु निवारण॥
केहि प्रकार मैं करौं बड़ाई। ज्ञान बुद्धि मोहि नहिं अधिकाई॥""","I have no knowledge or wisdom of my own; you know everything in your heart. Take your four-armed form and remove my troubles now. How can I praise you, when I have so little knowledge or understanding?","Chaupai 37–40"),
 P("""त्राहि त्राहि दुख हारिणी, हरो वेगि सब त्रास।
जयति जयति जय लक्ष्मी, करो शत्रु को नाश॥
रामदास धरि ध्यान नित, विनय करत कर जोर।
मातु लक्ष्मी दास पर, करहु दया की कोर॥""","Save us, remover of sorrow, and quickly take away all fear; victory, victory to Lakshmi, destroy what stands against us. Ramdas meditates on you daily and prays with folded hands: Mother Lakshmi, cast a glance of mercy on your servant.","Doha"),
 ]),

dict(slug='sankat-mochan-hanuman-ashtak', title='Sankat Mochan Hanuman Ashtak', hi='संकटमोचन हनुमानाष्टक', deity='Hanuman', kind='stuti', lang='hi',
 img='hanuman', pop=14, days=['Tuesday','Saturday'], fest=['Hanuman Jayanti','Tuesday','Saturday'],
 about="Eight verses by Goswami Tulsidas recalling the times Hanuman rescued others from danger: freeing the sun, finding Sita, bringing the Sanjivani herb, and rescuing Rama and Lakshmana from Ahiravana. Each verse ends with the line that gives the hymn its name, 'who does not know your name, Sankat Mochan, the remover of troubles?' It is recited after the Hanuman Chalisa on Tuesdays and Saturdays.",
 refrain='को नहिं जानत है जग में कपि संकटमोचन नाम तिहारो',
 stanzas=[
 S("""बाल समय रबि भक्षि लियो तब, तीनहुँ लोक भयो अँधियारो।
ताहि सों त्रास भयो जग को, यह संकट काहु सों जात न टारो॥
देवन आनि करी बिनती तब, छाँड़ि दियो रबि कष्ट निवारो।""","As a child you swallowed the sun, and darkness fell on the three worlds. The whole world was terrified, and no one could end the crisis. When the gods came and pleaded with you, you released the sun and ended their distress.","1"),
 S("""बालि की त्रास कपीस बसै गिरि, जात महाप्रभु पंथ निहारो।
चौंकि महामुनि साप दियो तब, चाहिय कौन बिचार बिचारो॥
कै द्विज रूप लिवाय महाप्रभु, सो तुम दास के सोक निवारो।""","Fearing Bali, Sugriva lived on the mountain, watching the road for the Lord. Startled, he wondered what to do. Taking the form of a Brahmin, you brought the Lord to him, and so ended your servant's grief.","2"),
 S("""अंगद के संग लेन गए सिय, खोज कपीस यह बैन उचारो।
जीवत ना बचिहौ हम सो जु, बिना सुधि लाये इहाँ पगु धारो॥
हेरि थके तट सिन्धु सबै तब, लाय सिया-सुधि प्रान उबारो।""","You went with Angada to search for Sita, and Sugriva declared: 'Whoever returns without news of her will not stay alive.' When everyone had searched until they were exhausted on the seashore, you brought news of Sita and saved their lives.","3"),
 S("""रावन त्रास दई सिय को सब, राक्षसि सों कहि सोक निवारो।
ताहि समय हनुमान महाप्रभु, जाय महा रजनीचर मारो॥
चाहत सीय असोक सों आगि सु, दै प्रभु मुद्रिका सोक निवारो।""","Ravana tormented Sita and ordered the demonesses to break her spirit. At that time, great Hanuman, you went and slew mighty demons. When Sita longed for fire from the Ashoka tree, you gave her the Lord's ring and ended her grief.","4"),
 S("""बान लग्यो उर लछिमन के तब, प्रान तजे सुत रावन मारो।
लै गृह बैद्य सुषेन समेत, तबै गिरि द्रोन सु बीर उपारो॥
आनि सजीवन हाथ दई तब, लछिमन के तुम प्रान उबारो।""","When Ravana's son struck Lakshmana in the chest with an arrow and his life was ebbing, you brought the physician Sushena with his house, and the hero uprooted the Drona mountain. You brought the Sanjivani herb, placed it in their hands, and saved Lakshmana's life.","5"),
 S("""रावन युद्ध अजान कियो तब, नाग कि फाँस सबै सिर डारो।
श्रीरघुनाथ समेत सबै दल, मोह भयो यह संकट भारो॥
आनि खगेस तबै हनुमान जु, बंधन काटि सुत्रास निवारो।""","When Ravana fought by trickery and cast the serpent noose over everyone, Rama and the whole army fell senseless in this grave crisis. Then you brought Garuda, king of birds, who cut the bonds and ended the terror.","6"),
 S("""बंधु समेत जबै अहिरावन, लै रघुनाथ पताल सिधारो।
देबिहिं पूजि भली बिधि सों बलि, देउ सबै मिलि मंत्र बिचारो॥
जाय सहाय भयो तब ही, अहिरावन सैन्य समेत सँहारो।""","When Ahiravana carried Rama and his brother away to the underworld, and planned with his followers to offer them as a sacrifice to the goddess, you went to their aid and destroyed Ahiravana with his army.","7"),
 S("""काज किये बड़ देवन के तुम, बीर महाप्रभु देखि बिचारो।
कौन सो संकट मोर गरीब को, जो तुमसे नहिं जात है टारो॥
बेगि हरो हनुमान महाप्रभु, जो कछु संकट होय हमारो।""","You have done great deeds even for the gods; consider this, great hero. What trouble of mine, poor as I am, is there that you cannot remove? Quickly take away, great Hanuman, whatever trouble we have.","8"),
 S("""लाल देह लाली लसे, अरु धरि लाल लँगूर।
बज्र देह दानव दलन, जय जय जय कपि सूर॥""","Your red body glows with a red radiance, and your tail too is red. Thunderbolt-bodied destroyer of demons, victory, victory, victory to the heroic monkey.","Doha", refrain=False),
 ]),

# ---------------- mantras and shlokas ----------------
dict(slug='shiv-panchakshar-stotram', title='Shiv Panchakshar Stotram (Om Namah Shivaya)', hi='शिव पञ्चाक्षर स्तोत्रम्', deity='Shiva', kind='mantra', lang='sa',
 img='shiva', pop=None, days=['Monday'], fest=['Mahashivratri','Shravan Mondays','Pradosh'],
 about="A Sanskrit hymn attributed to Adi Shankaracharya, built on the five syllables of the mantra 'Na-ma-shi-vā-ya'. Each verse praises Shiva and ends on one of the five syllables, so reciting it is a way of chanting Om Namah Shivaya with its meaning.",
 stanzas=[
 P("""नागेन्द्रहाराय त्रिलोचनाय भस्माङ्गरागाय महेश्वराय।
नित्याय शुद्धाय दिगम्बराय तस्मै नकाराय नमः शिवाय॥""","Salutations to Shiva, the syllable 'Na': who wears the king of serpents as a garland, three-eyed, his body smeared with ash; the great lord, eternal, pure, clothed only by the directions."),
 P("""मन्दाकिनीसलिलचन्दनचर्चिताय नन्दीश्वरप्रमथनाथमहेश्वराय।
मन्दारपुष्पबहुपुष्पसुपूजिताय तस्मै मकाराय नमः शिवाय॥""","Salutations to Shiva, the syllable 'Ma': anointed with the water of the Ganga and with sandal paste, lord of Nandi and of the ganas, worshipped with mandara and many other flowers."),
 P("""शिवाय गौरीवदनाब्जवृन्दसूर्याय दक्षाध्वरनाशकाय।
श्रीनीलकण्ठाय वृषध्वजाय तस्मै शिकाराय नमः शिवाय॥""","Salutations to Shiva, the syllable 'Shi': the auspicious one, the sun that opens the lotus of Gauri's face, destroyer of Daksha's sacrifice, the blue-throated one whose banner bears the bull."),
 P("""वसिष्ठकुम्भोद्भवगौतमार्यमुनीन्द्रदेवार्चितशेखराय।
चन्द्रार्कवैश्वानरलोचनाय तस्मै वकाराय नमः शिवाय॥""","Salutations to Shiva, the syllable 'Va': whose head is worshipped by Vasishtha, Agastya, Gautama and the great sages and gods, and whose three eyes are the moon, the sun and fire."),
 P("""यक्षस्वरूपाय जटाधराय पिनाकहस्ताय सनातनाय।
दिव्याय देवाय दिगम्बराय तस्मै यकाराय नमः शिवाय॥""","Salutations to Shiva, the syllable 'Ya': who took the form of a yaksha, who wears matted hair and holds the Pinaka bow; the eternal, the divine, the god clothed by the directions."),
 P("""पञ्चाक्षरमिदं पुण्यं यः पठेच्छिवसन्निधौ।
शिवलोकमवाप्नोति शिवेन सह मोदते॥""","Whoever recites this holy hymn of five syllables in the presence of Shiva attains Shiva's realm and rejoices with Shiva.","Phalashruti"),
 ]),

dict(slug='hare-krishna-mahamantra', title='Hare Krishna Mahamantra', hi='हरे कृष्ण महामन्त्र', deity='Krishna', kind='mantra', lang='sa',
 img='krishna', pop=None, days=['Daily','Ekadashi'], fest=['Janmashtami','Ekadashi','Kirtan'],
 about="The sixteen-word mantra of the names of Hari, Krishna and Rama, found in the Kali-Santarana Upanishad and made famous worldwide by Chaitanya Mahaprabhu and later ISKCON. It is chanted on a japa mala (traditionally 108 times per round) and sung in kirtan. The Upanishad gives the 'Hare Rama' half first; kirtan usually begins with 'Hare Krishna'.",
 stanzas=[
 P("""हरे कृष्ण हरे कृष्ण कृष्ण कृष्ण हरे हरे।
हरे राम हरे राम राम राम हरे हरे॥""","O Hari (Radha, the divine energy), O Krishna, O Rama: the mantra simply calls the names of God with love, asking to be engaged in his service."),
 ]),

dict(slug='mangal-bhavan-amangal-hari', title='Mangal Bhavan Amangal Hari', hi='मंगल भवन अमंगल हारी', deity='Ram', kind='shloka', lang='hi',
 img='ram', pop=None, days=['Daily'], fest=['Ram Navami','Ramayan Path','Diwali'],
 about="A chaupai from the Bal Kand of Tulsidas's Ramcharitmanas, one of the most widely sung lines of the Ramayan and the opening of many Ram bhajans. It asks the child Rama, who plays in Dasharatha's courtyard, to have mercy.",
 stanzas=[
 P("""मंगल भवन अमंगल हारी।
द्रवउ सो दसरथ अजिर बिहारी॥""","May he who is the home of all that is auspicious and the remover of all that is inauspicious, the child who plays in Dasharatha's courtyard, melt with compassion for me.","Bal Kand"),
 ]),

dict(slug='achyutam-keshavam', title='Achyutam Keshavam', hi='अच्युतं केशवं', deity='Vishnu', kind='shloka', lang='sa',
 img='vishnu', pop=None, days=['Daily','Thursday'], fest=['Ekadashi','Janmashtami','Ram Navami'],
 about="The first verse of the Achyutashtakam, attributed to Adi Shankaracharya: a string of the names of Vishnu, Krishna and Rama. It is the basis of the much-loved bhajan 'Achyutam Keshavam Krishna Damodaram'.",
 stanzas=[
 P("""अच्युतं केशवं रामनारायणं कृष्णदामोदरं वासुदेवं हरिम्।
श्रीधरं माधवं गोपिकावल्लभं जानकीनायकं रामचन्द्रं भजे॥""","I worship Achyuta the unfailing, Keshava, Rama and Narayana, Krishna and Damodara, Vasudeva and Hari; Shridhara, Madhava, the beloved of the gopis, and Ramachandra, the lord of Janaki."),
 ]),

dict(slug='navagraha-mantra', title='Navagraha Mantra', hi='नवग्रह मन्त्र', deity='Navagraha', kind='shloka', lang='sa',
 img='navagraha', pop=None, days=['Saturday','Daily'], fest=['Graha Shanti','New beginnings'],
 about="A single Sanskrit verse that prays to the Trinity and the nine planets (navagraha) together, asking that all of them bring peace. It is recited daily by many and at the start of havans, griha pravesh and other ceremonies.",
 stanzas=[
 P("""ब्रह्मा मुरारिस्त्रिपुरान्तकारी भानुः शशी भूमिसुतो बुधश्च।
गुरुश्च शुक्रः शनिराहुकेतवः सर्वे ग्रहाः शान्तिकरा भवन्तु॥""","May Brahma, Vishnu the slayer of Mura, and Shiva the destroyer of the three cities, and the Sun, the Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu and Ketu: may all the planets bring peace."),
 ]),

dict(slug='yena-baddho-bali-raja', title='Yena Baddho Bali Raja (Rakhi Mantra)', hi='येन बद्धो बली राजा', deity='Universal', kind='shloka', lang='sa',
 img=None, pop=None, days=[], fest=['Raksha Bandhan'],
 about="The mantra recited while tying the rakhi or a sacred thread (raksha sutra) on the wrist. It recalls the thread with which King Bali, the mighty lord of the demons, was bound, and asks the thread to hold firm in protection.",
 stanzas=[
 P("""येन बद्धो बली राजा दानवेन्द्रो महाबलः।
तेन त्वामपि बध्नामि रक्षे मा चल मा चल॥""","With the thread that bound the mighty King Bali, lord of the demons, I tie this on you too. O protecting thread, do not waver, do not waver."),
 ]),
]

EXTRA_WEEKDAYS = {'Thursday': ['om-jai-brihaspati-deva'], 'Friday': ['jai-santoshi-mata', 'lakshmi-chalisa'], 'Wednesday': ['ganesh-chalisa'],
                  'Tuesday': ['sankat-mochan-hanuman-ashtak'], 'Monday': ['shiv-panchakshar-stotram']}
EXTRA_FESTIVALS = {'Diwali': ['lakshmi-chalisa'], 'Ganesh Chaturthi': ['ganesh-chalisa'], 'Mahashivratri and Shravan': ['shiv-panchakshar-stotram'],
                   'Janmashtami': ['hare-krishna-mahamantra', 'achyutam-keshavam'], 'Ram Navami and Hanuman Jayanti': ['aarti-shri-ramayan-ji-ki', 'sankat-mochan-hanuman-ashtak']}
NEW_FESTIVALS = [("Ekadashi and Khatu Shyam", "The eleventh day of each lunar fortnight, sacred to Vishnu and to Baba Khatu Shyam.", ['om-jai-shri-shyam-hare', 'achyutam-keshavam', 'hare-krishna-mahamantra']),
                 ("Tulsi Vivah and Kartik", "The wedding of Tulsi and Shaligram (Vishnu) at the end of Kartik month.", ['jai-jai-tulsi-mata']),
                 ("Raksha Bandhan", "Sisters tie a rakhi on their brothers' wrists.", ['yena-baddho-bali-raja'])]
