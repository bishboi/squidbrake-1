# -*- coding: utf-8 -*-
"""Script for the comedy skit "Pollution का Solution — एक खोज". Fictional satire: the ministers are unnamed and never shown.
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
        "The students are exactly the three from the first reference image — KABIR (tall, short beard), MEERA (high ponytail, round black glasses), "
        "BUNTY (short, chubby, curly hair, mask under his chin) — same faces, same white polo T-shirts with the poster print, blue jeans. "
        "No captions, no subtitles, no extra text. ")
VOICES = ("Voices — KABIR: calm, warm young male voice. MEERA: sharp, sarcastic young female voice. BUNTY: high-pitched, excitable, funny young male voice. "
          "RAMLAL: raspy, lazy old man's voice. GUARD: flat, robotic deadpan male voice. ")
RULES = ("Comedy scene, realistic, clear spoken Hindi dialogue with accurate lip-sync, good comic timing. One continuous shot, no cuts. "
         "Only the lines given are spoken, exactly as written, in Hindi. Natural ambient sound only, no music, no laughter track, no subtitles or text on screen. ")

SCENES = [
 dict(id="c1", dur=10, refs=["cast"], chyron="Pollution का Solution — एक खोज",
  still="Medium shot from the front: the three students walk side by side toward the camera down a Delhi street drowned in thick smog, traffic and blurred headlights behind. BUNTY holds up his phone and stares at it in horror, MEERA waves smoke from her face, KABIR looks ahead.",
  action="The three walk toward the camera coughing. BUNTY stares at his phone and exclaims: \"AQI एक हज़ार! भाई, ये हवा है या तंदूर का धुआँ?\" MEERA, annoyed and determined, says: \"बस! आज मंत्री जी से solution लेकर ही लौटेंगे।\" KABIR nods.",
  lines=[("बंटी", "AQI एक हज़ार! भाई, ये हवा है या तंदूर का धुआँ?"), ("मीरा", "बस! आज मंत्री जी से solution लेकर ही लौटेंगे।")]),
 dict(id="g1a", dur=10, refs=["cast", "guard1"], chyron="मंत्री नंबर 1 का बंगला",
  still="Outside the tall ornate black iron gate of a grand white government bungalow. The three students stand on the left facing the gate, KABIR in front. On the right the gatekeeper RAMLAL from the second reference image stands in the half-open small side gate holding his glass of chai, looking at them. Medium wide shot, all four clearly visible.",
  action="KABIR says politely: \"नमस्ते अंकल! मंत्री जी से मिलना है। प्रदूषण का solution चाहिए।\" RAMLAL takes a slow sip of chai, nods and replies: \"मंत्री जी? हाँ हाँ... घर पर ही हैं।\" The three students smile with relief and look at each other.",
  lines=[("कबीर", "नमस्ते अंकल! मंत्री जी से मिलना है। प्रदूषण का solution चाहिए।"), ("रामलाल", "मंत्री जी? हाँ हाँ... घर पर ही हैं।")]),
 dict(id="g1b", dur=10, refs=["cast", "guard1"], sfx="boom+laugh",
  still="Same bungalow gate, closer two-shot over the shoulder: MEERA on the left in profile with KABIR and BUNTY just behind her, facing RAMLAL the gatekeeper from the second reference image on the right, who leans lazily on the black iron gate holding his chai glass, a sly half-smile under his grey moustache.",
  action="MEERA says impatiently: \"तो बुला दीजिए ना!\" RAMLAL scratches his head, grins slyly and says: \"अरे... घर पर हैं मतलब — गाँव वाले घर पर। दिवाली से पहले ही निकल गए थे।\" The students' smiles drop; they stare at him, stunned.",
  lines=[("मीरा", "तो बुला दीजिए ना!"), ("रामलाल", "अरे... घर पर हैं मतलब — गाँव वाले घर पर। दिवाली से पहले ही निकल गए थे।")]),
 dict(id="g1c", dur=12, refs=["cast", "guard1"], sfx="laugh",
  still="Same bungalow gate, medium shot: BUNTY in the middle leaning forward toward RAMLAL the gatekeeper from the second reference image, who bends close as if sharing a secret, one hand beside his mouth; MEERA stands beside them with arms crossed and a flat unimpressed face, KABIR behind.",
  action="BUNTY asks, confused: \"दिवाली से पहले? क्यों?\" RAMLAL leans in and says in a loud whisper: \"डॉक्टर ने बोला है — दिल्ली की हवा सेहत के लिए हानिकारक है।\" MEERA turns her head slowly, looks straight into the camera and says dryly: \"और हमारे लिए? विटामिन है?\"",
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
  action="BUNTY sighs: \"अब कहाँ जाएँ? एक गाँव में... एक स्विट्ज़रलैंड में।\" KABIR stands up, dusts his hands and says firmly: \"एक दरवाज़ा अभी बचा है। चलो।\" MEERA puts her glasses back on and gets up.",
  lines=[("बंटी", "अब कहाँ जाएँ? एक गाँव में... एक स्विट्ज़रलैंड में।"), ("कबीर", "एक दरवाज़ा अभी बचा है। चलो।")]),
 dict(id="d1", dur=6, refs=["cast"], chyron="आख़िरी दरवाज़ा : नेता प्रतिपक्ष का दफ़्तर — यहाँ गेट खुला मिला", music="hope",
  still="Seen from behind: the three students walk through a simple wide-open gate into the courtyard of a modest office building glowing with warm welcoming light, a young staff member at the door greeting them with folded hands, no guards, no barriers, evening haze.",
  action="The three students walk in through the open gate, the staff member smiles and gestures them inside with folded hands, warm light spills out. Nobody speaks.", lines=[]),
 dict(id="d2", dur=10, refs=["cast"],
  still="The three students stride out of the same office gate toward the camera, energised and smiling: KABIR in front carrying a broom over his shoulder, MEERA holding a small tree sapling in a pot, BUNTY carrying a stack of pollution masks and garbage sacks. Golden evening light cutting through the haze, low angle hero shot.",
  action="They walk toward the camera with determination. KABIR says: \"जवाब मिल गया। जब तक सरकार नहीं जागती... शुरुआत हम ख़ुद करेंगे।\" MEERA adds sharply: \"और सवाल पूछना... बिल्कुल नहीं छोड़ेंगे।\" BUNTY raises a fist.",
  lines=[("कबीर", "जवाब मिल गया। जब तक सरकार नहीं जागती... शुरुआत हम ख़ुद करेंगे।"), ("मीरा", "और सवाल पूछना... बिल्कुल नहीं छोड़ेंगे।")]),
 dict(id="m1", dur=8, refs=["cast"], chyron="Pollution पर Solution — शुरुआत हम से",
  still="Wide shot on the bank of the Yamuna in Delhi at golden hour: dozens of young student volunteers in the same white polo T-shirts cleaning the riverbank, filling sacks with plastic waste and planting saplings; in the foreground KABIR sweeping, MEERA planting a sapling, BUNTY struggling comically with a huge garbage sack. Haze, sunlight, hopeful mood.",
  action="The volunteers work with energy, KABIR sweeps, MEERA presses soil around the sapling, BUNTY heaves the huge sack onto his shoulder and wobbles, others cheer. Nobody speaks; cheerful crowd sounds.", lines=[]),
 dict(id="e1", dur=9, refs=["cast"], sfx="laugh",
  still="Close-up of MEERA looking straight into the camera with a sly smile, the riverbank clean-up and volunteers in white T-shirts blurred behind her at golden hour; BUNTY's curly head just entering the frame from the right edge.",
  action="MEERA looks into the camera and says sweetly but sarcastically: \"और मंत्री जी... स्विट्ज़रलैंड से लौटें, तो बताइएगा ज़रूर — साफ़ हवा दिखती कैसी है।\" BUNTY pops fully into the frame grinning and adds: \"फोटो भी भेजना!\" MEERA rolls her eyes and smiles.",
  lines=[("मीरा", "और मंत्री जी... स्विट्ज़रलैंड से लौटें, तो बताइएगा ज़रूर — साफ़ हवा दिखती कैसी है।"), ("बंटी", "फोटो भी भेजना!")]),
]
