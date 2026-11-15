# -*- coding: utf-8 -*-
"""Script for the comedy skit "Pollution का Solution — एक खोज". Fictional satire: the ministers are unnamed and never shown; the Chief Minister is an invented character, not modelled on any real person.
Each scene: id, dur (seconds), refs (cast sheets used for the first frame), still (first-frame prompt),
action (what happens, with the spoken lines), lines [(speaker, text)], optional chyron / sfx at the end of the scene."""
TAGLINE = "काल्पनिक व्यंग्य  |  AI-निर्मित"
BEATS = []
CAST = {  # reference sheets generated once, then passed to every still
 "cast": ("Character reference sheet, photorealistic, plain light grey studio background, full-body front view of three Indian college students standing side by side, evenly lit. All three wear the same white polo T-shirt from the first reference image with the 'Pollution Par Solution' poster from the second reference image printed large on the chest, and blue jeans. LEFT: KABIR, 22, tall and lean, short neat black beard, short black hair, calm confident look. MIDDLE: MEERA, 21, medium height, long black hair in a high ponytail, round black-framed glasses, sharp witty expression. RIGHT: BUNTY, 20, short and chubby, curly messy hair, clean-shaven round face, goofy grin, a pollution mask pulled down under his chin. No other text."),
 "guard1": ("Photorealistic portrait, plain light grey studio background: RAMLAL, a 58-year-old Indian bungalow gatekeeper, thin, grey bushy moustache, weathered kind-but-sly face, faded khaki security uniform with a khaki peaked cap, holding a small glass of chai. Waist-up, front view. No text."),
 "guard2": ("Photorealistic portrait, plain light grey studio background: a 30-year-old Indian VIP security guard, muscular, clean-shaven with slick gelled hair, dark aviator sunglasses, tight grey safari suit, a curly earpiece wire, arms crossed, deadpan face. Waist-up, front view. No text."),
}
LOOK = ("Photorealistic cinematic film still from a comedy drama, 35mm lens, smoggy hazy Delhi daylight with a warm-grey palette. "
        "The students are exactly the three from the first reference image — KABIR (the lead: the tall man with short dark side-swept hair and a neat short beard, exactly as in the first reference image and in the photos of the last reference image), MEERA (high ponytail, round black glasses), "
        "BUNTY (short, chubby, curly hair, mask under his chin) — same faces, same white polo T-shirts (poster print on the chest, small NSUI wordmark, tipped collar, no portrait photo on the shirt), blue jeans. "
        "No captions, no subtitles, no extra text. ")
VOICES = ("Voices — KABIR: calm, warm young male voice. MEERA: sharp, sarcastic young female voice. BUNTY: high-pitched, excitable, funny young male voice. "
          "RAMLAL: raspy, lazy old man's voice. GUARD: flat, robotic deadpan male voice. CM: cheerful, over-confident middle-aged woman's voice. ")
RULES = ("Comedy scene, realistic, clear spoken Hindi dialogue with accurate lip-sync, good comic timing. One continuous shot, no cuts. "
         "Only the lines given are spoken, exactly as written, in Hindi. Natural ambient sound only, no music, no laughter track, no subtitles or text on screen. ")

SCENES = [
 dict(id="c1", dur=10, refs=["cast"], chyron="Pollution का Solution — एक खोज",
  still="Medium shot from the front: the three students walk side by side toward the camera down a Delhi street drowned in thick smog, traffic and blurred headlights behind. KABIR walks in the centre slightly ahead as the leader, BUNTY on one side holds up his phone and stares at it in horror, MEERA on the other side waves smoke from her face.",
  action="The three walk toward the camera coughing. BUNTY stares at his phone and exclaims: \"AQI एक हज़ार! भाई, ये हवा है या तंदूर का धुआँ?\" KABIR, calm and determined, says: \"बस! आज मंत्री जी से solution लेकर ही लौटेंगे।\" MEERA nods.",
  lines=[("बंटी", "AQI एक हज़ार! भाई, ये हवा है या तंदूर का धुआँ?"), ("कबीर", "बस! आज मंत्री जी से solution लेकर ही लौटेंगे।")]),
 dict(id="g1a", dur=10, refs=["cast", "guard1"], chyron="मंत्री नंबर 1 का बंगला",
  still="Outside the tall ornate black iron gate of a grand white government bungalow. The three students stand on the left facing the gate, KABIR in front. On the right the gatekeeper RAMLAL from the second reference image stands in the half-open small side gate holding his glass of chai, looking at them. Medium wide shot, all four clearly visible.",
  action="KABIR says politely: \"नमस्ते अंकल! मंत्री जी से मिलना है। प्रदूषण का solution चाहिए।\" RAMLAL takes a slow sip of chai, nods and replies: \"मंत्री जी? हाँ हाँ... घर पर ही हैं।\" The three students smile with relief and look at each other.",
  lines=[("कबीर", "नमस्ते अंकल! मंत्री जी से मिलना है। प्रदूषण का solution चाहिए।"), ("रामलाल", "मंत्री जी? हाँ हाँ... घर पर ही हैं।")]),
 dict(id="g1b", dur=10, refs=["cast", "guard1"], sfx="boom+laugh",
  still="Same bungalow gate, closer two-shot over the shoulder: MEERA on the left in profile with KABIR and BUNTY just behind her, facing RAMLAL the gatekeeper from the second reference image on the right, who leans lazily on the black iron gate holding his chai glass, a sly half-smile under his grey moustache.",
  action="MEERA says impatiently: \"तो बुला दीजिए ना!\" RAMLAL scratches his head, grins slyly and says: \"अरे... घर पर हैं मतलब — गाँव वाले घर पर। दिवाली से पहले ही निकल गए थे।\" The students' smiles drop; they stare at him, stunned.",
  lines=[("मीरा", "तो बुला दीजिए ना!"), ("रामलाल", "अरे... घर पर हैं मतलब — गाँव वाले घर पर। दिवाली से पहले ही निकल गए थे।")]),
 dict(id="g1c", dur=12, refs=["cast", "guard1"], sfx="laugh",
  still="Same bungalow gate, medium shot: BUNTY in the middle leaning forward toward RAMLAL the gatekeeper from the second reference image, who bends close as if sharing a secret, one hand beside his mouth; MEERA stands beside them with arms crossed and a flat unimpressed face, KABIR beside her watching. Wardrobe: only the three students wear the white polo T-shirt with the poster print; RAMLAL wears his faded khaki security uniform and khaki peaked cap exactly as in the second reference image.",
  action="BUNTY asks, confused: \"दिवाली से पहले? क्यों?\" RAMLAL leans in and says in a loud whisper: \"डॉक्टर ने बोला है — दिल्ली की हवा सेहत के लिए हानिकारक है।\" MEERA, staying where she is with arms crossed, turns her head slowly, looks straight into the camera and says dryly: \"और हमारे लिए? विटामिन है?\"",
  lines=[("बंटी", "दिवाली से पहले? क्यों?"), ("रामलाल", "डॉक्टर ने बोला है — दिल्ली की हवा सेहत के लिए हानिकारक है।"), ("मीरा", "और हमारे लिए? विटामिन है?")]),
 dict(id="t2", dur=5, refs=["cast"], chyron="मंत्री नंबर 2 की तलाश में...", sfx="whoosh",
  still="The three students squeezed together on the back seat of a green-and-yellow Delhi auto rickshaw driving through thick smog, seen from the front through the open side; BUNTY in the middle squashed and coughing, MEERA holding her dupatta-free hand over her nose, KABIR pointing ahead.",
  action="The auto rickshaw bounces along the smoggy road, the three sway together, BUNTY coughs and fans the air, KABIR points ahead. Nobody speaks. Auto engine and horn sounds.", lines=[]),
 dict(id="g2a", dur=10, refs=["cast", "guard2"], chyron="मंत्री नंबर 2 का बंगला", sfx="scratch",
  still="Outside the sleek modern steel gate of a luxurious glass-and-stone ministerial bungalow with trimmed hedges. The three students stand on the left, KABIR in front; on the right the security guard from the second reference image stands rigid with arms crossed, sunglasses on, blocking the gate. Medium wide shot, all four clearly visible.",
  action="KABIR asks: \"भाई साहब, मंत्री जी हैं?\" The GUARD answers without moving: \"सर मीटिंग में हैं।\" MEERA asks suspiciously: \"कहाँ?\" The GUARD pauses and says flatly: \"स्विट्ज़रलैंड।\" The three students freeze with open mouths.",
  lines=[("कबीर", "भाई साहब, मंत्री जी हैं?"), ("गार्ड", "सर मीटिंग में हैं।"), ("मीरा", "कहाँ?"), ("गार्ड", "स्विट्ज़रलैंड।")]),
 dict(id="g2b", dur=12, refs=["cast", "guard2"], sfx="boom+laugh",
  still="Same modern steel gate, closer shot: BUNTY in front with wide shocked eyes and both hands on his head, facing the security guard from the second reference image who stands expressionless in sunglasses with arms crossed; MEERA and KABIR behind BUNTY exchanging a look.",
  action="BUNTY shouts in disbelief: \"स्विट्ज़रलैंड?! वहाँ कौन सा प्रदूषण है?\" The GUARD, completely deadpan, replies: \"वही तो स्टडी करने गए हैं... कि साफ़ हवा दिखती कैसी है।\" MEERA slowly face-palms, KABIR shakes his head.",
  lines=[("बंटी", "स्विट्ज़रलैंड?! वहाँ कौन सा प्रदूषण है?"), ("गार्ड", "वही तो स्टडी करने गए हैं... कि साफ़ हवा दिखती कैसी है।")]),
 dict(id="p1", dur=10, refs=["cast"],
  still="The three students sit dejected in a row on a roadside kerb in thick evening smog, traffic blurred behind; BUNTY chin in hands, MEERA cleaning her glasses, KABIR looking into the distance. Medium shot from the front, low angle.",
  action="BUNTY sighs: \"अब कहाँ जाएँ? एक गाँव में... एक स्विट्ज़रलैंड में।\" KABIR stands up, dusts his hands and says firmly: \"अब सीधा मुख्यमंत्री जी के पास चलते हैं।\" MEERA puts her glasses back on and gets up.",
  lines=[("बंटी", "अब कहाँ जाएँ? एक गाँव में... एक स्विट्ज़रलैंड में।"), ("कबीर", "अब सीधा मुख्यमंत्री जी के पास चलते हैं।")]),
 dict(id="cm1", dur=12, refs=["cast", "cm"], chyron="मुख्यमंत्री कार्यालय",
  still="Inside a grand wood-panelled chief minister's office. Behind a huge polished desk sits the CM — the woman from the second reference image, same face, grey-streaked bob hair, gold-rimmed glasses, magenta silk saree — smiling confidently with a cup of tea, a large air purifier glowing green beside the desk. The three students stand in front of the desk facing her, KABIR in the middle and slightly ahead. Medium wide shot with the camera at the end of the desk, so that the CM (left) and the students (right) face each other across the frame and the students' faces and the fronts of their T-shirts are clearly visible in three-quarter view. No flags, no emblems, no party symbols.",
  action="KABIR says respectfully but firmly: \"मैडम, दिल्ली का AQI एक हज़ार के पार है। हमें solution चाहिए।\" The CM waves her hand, smiling with total confidence, and replies: \"अरे बेटा, घबराओ मत! AQI तो एक temperature है... किसी भी instrument से नाप लो।\" The three students freeze and blink at her.",
  lines=[("कबीर", "मैडम, दिल्ली का AQI एक हज़ार के पार है। हमें solution चाहिए।"), ("मुख्यमंत्री", "अरे बेटा, घबराओ मत! AQI तो एक temperature है... किसी भी instrument से नाप लो।")], sfx="scratch"),
 dict(id="cm2", dur=12, refs=["cast", "cm"], sfx="boom+laugh",
  still="Same chief minister's office, closer shot across the desk: BUNTY on the left with his jaw dropped, MEERA in the middle adjusting her glasses with a pained look, KABIR on the right staring in disbelief; in the foreground right, seen three-quarter from the front, the CM from the second reference image in her magenta saree leaning back in her chair, smiling, pointing at the air conditioner remote on the desk.",
  action="BUNTY blurts out: \"Temperature?!\" MEERA says slowly, as if explaining to a child: \"मैडम... AQI हवा की quality होती है।\" The CM shrugs cheerfully, picks up the AC remote and says: \"अच्छा? तो... AC चला लो!\" KABIR closes his eyes and sighs.",
  lines=[("बंटी", "Temperature?!"), ("मीरा", "मैडम... AQI हवा की quality होती है।"), ("मुख्यमंत्री", "अच्छा? तो... AC चला लो!")]),
 dict(id="d2", dur=11, refs=["cast"], music="hope",
  still="The three students stride out of a grand government building gate toward the camera, determined: KABIR in front and in the centre carrying a broom over his shoulder, MEERA holding a small tree sapling in a pot, BUNTY carrying a stack of pollution masks and garbage sacks. Golden evening light cutting through the haze, low angle hero shot.",
  action="They walk toward the camera with determination. KABIR says: \"जिन्हें AQI का मतलब नहीं पता... उनसे solution क्या मिलेगा? शुरुआत हम ख़ुद करेंगे।\" MEERA adds sharply: \"और सवाल पूछना... बिल्कुल नहीं छोड़ेंगे।\" BUNTY raises a fist.",
  lines=[("कबीर", "जिन्हें AQI का मतलब नहीं पता... उनसे solution क्या मिलेगा? शुरुआत हम ख़ुद करेंगे।"), ("मीरा", "और सवाल पूछना... बिल्कुल नहीं छोड़ेंगे।")]),
 dict(id="m1", dur=8, refs=["cast"], chyron="Pollution पर Solution — शुरुआत हम से",
  still="Wide shot on the bank of the Yamuna in Delhi at golden hour: dozens of young student volunteers in the same white polo T-shirts cleaning the riverbank, filling sacks with plastic waste and planting saplings; in the foreground KABIR sweeping, MEERA planting a sapling, BUNTY struggling comically with a huge garbage sack. Haze, sunlight, hopeful mood.",
  action="The volunteers work with energy, KABIR sweeps, MEERA presses soil around the sapling, BUNTY heaves the huge sack onto his shoulder and wobbles, others cheer. Nobody speaks; cheerful crowd sounds.", lines=[]),
 dict(id="e1", dur=10, refs=["cast"], sfx="laugh",
  still="Medium close-up of KABIR in the centre looking straight into the camera with a confident smile, MEERA on his left and BUNTY on his right leaning into the frame, the riverbank clean-up and volunteers in white T-shirts blurred behind them at golden hour.",
  action="KABIR looks into the camera and says with a calm smile: \"और मैडम... AQI temperature नहीं होता। पर हाँ — जनता का पारा ज़रूर चढ़ रहा है।\" BUNTY grins and adds: \"नाप लेना!\" MEERA laughs.",
  lines=[("कबीर", "और मैडम... AQI temperature नहीं होता। पर हाँ — जनता का पारा ज़रूर चढ़ रहा है।"), ("बंटी", "नाप लेना!")]),
]
