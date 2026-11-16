# -*- coding: utf-8 -*-
"""Awareness film "लाल बत्ती पर चार काम" — at the red light in front of the BJP headquarters the students hand out masks and
give drivers four simple things every citizen can do. Same cast, look and tools as the skit (SKIT=beats_redlight)."""
from beats_skit import LOOK, VOICES, RULES
TAGLINE = "जागरूकता संदेश  |  AI-निर्मित"
BEATS = []
LOC = ("The location is exactly the junction of the last reference image: a busy Delhi red-light crossing in hazy golden evening light, traffic stopped at a glowing red signal, "
       "and across the road the Bharatiya Janata Party national headquarters — a large modern cream-and-saffron office building with a big lotus emblem and Devanagari lettering on its facade, clearly visible. ")
MASK = " MASKS: every student wears a white pollution mask over nose and mouth for the whole shot. "
SHIRT = " Every student wears exactly the white polo of the T-shirt reference image: bold NSUI wordmark on the left chest and the full-colour lungs poster (never plain text only). "
KEEP = " The camera is locked off; the building, its lettering and the red signal stay unchanged. The students keep their masks on and speak through them. Exactly the lines given are spoken, nothing else."
OUTRO_PLAN = [("r1", 0.5, 4.6), ("r2", 1.0, 4.6), ("r3", 1.0, 4.6), ("r5", 1.0, 4.6), ("r6", 1.5, 5.0)]
SCENES = [
 dict(id="r1", dur=12, refs=["cast", "tshirt", "loc"], chyron="लाल बत्ती पर चार काम",
  still=LOC + "In the foreground, between the stopped cars, scooters and a green-and-yellow auto-rickshaw, KABIR stands in the centre facing the camera, holding a few white masks, with MEERA on his left and BUNTY on his right carrying an open carton of masks. Medium shot, all three clearly visible." + MASK + SHIRT,
  action="KABIR looks into the camera and says warmly and clearly: \"दोस्तों, साफ़ हवा की लड़ाई सिर्फ़ सरकार की नहीं, हमारी भी है। लाल बत्ती पर बस चार छोटे काम कीजिए।\" MEERA and BUNTY nod and hold up masks." + KEEP,
  lines=[("कबीर", "दोस्तों, साफ़ हवा की लड़ाई सिर्फ़ सरकार की नहीं, हमारी भी है। लाल बत्ती पर बस चार छोटे काम कीजिए।")]),
 dict(id="r2", dur=11, refs=["cast", "tshirt", "loc"], chyron="1.  लाल बत्ती पर इंजन बंद करें", hold=True, music="hope",
  still=LOC + "In the foreground KABIR leans slightly toward a middle-aged man sitting on a scooter stopped at the signal, exhaust smoke curling from the scooter; KABIR holds out a white mask to him and points at the scooter's ignition key. MEERA and BUNTY hand masks to other drivers behind. Medium shot, KABIR's face and T-shirt clearly visible." + MASK + SHIRT,
  action="KABIR hands the mask to the scooter rider and says kindly: \"भैया, लाल बत्ती पर इंजन बंद कर दीजिए। Red light on, गाड़ी off!\" The rider smiles, turns the key and switches the scooter off; the exhaust smoke stops. He gives a thumbs up." + KEEP,
  lines=[("कबीर", "भैया, लाल बत्ती पर इंजन बंद कर दीजिए। Red light on, गाड़ी off!")]),
 dict(id="r3", dur=11, refs=["cast", "tshirt", "loc"], chyron="2.  Metro, बस या carpool अपनाएँ", hold=True,
  still=LOC + "In the foreground MEERA (ponytail, round black glasses) stands at the open driver's window of a large white SUV in which a man in office clothes sits completely alone, the other seats empty; she offers him a white mask. A red city bus and a metro pillar are visible in the traffic behind. KABIR and BUNTY hand out masks in the background. Medium shot, MEERA's face clearly visible." + MASK + SHIRT,
  action="MEERA hands the mask through the window, glances at the empty seats and says, friendly but pointed: \"सर, अकेले इतनी बड़ी गाड़ी? हफ़्ते में कुछ दिन metro, बस या carpool अपनाइए।\" The driver looks at the empty seats, laughs sheepishly and nods." + KEEP,
  lines=[("मीरा", "सर, अकेले इतनी बड़ी गाड़ी? हफ़्ते में कुछ दिन metro, बस या carpool अपनाइए।")]),
 dict(id="r4", dur=11, refs=["cast", "tshirt", "loc"], chyron="3.  PUC जाँच और सर्विस समय पर", hold=True,
  still=LOC + "In the foreground BUNTY (chubby, curly hair) stands beside an old auto-rickshaw whose exhaust pipe is pouring thick dark smoke; he waves the smoke away with one hand and holds out a white mask to the driver with the other. MEERA and KABIR hand out masks in the background. Medium shot, BUNTY clearly visible." + MASK + SHIRT,
  action="BUNTY fans the dark smoke away, hands the mask to the auto driver and says cheerfully: \"भैया, गाड़ी धुआँ बहुत छोड़ रही है! PUC जाँच और सर्विस समय पर करवा लीजिए।\" The driver nods and folds his hands in thanks." + KEEP,
  lines=[("बंटी", "भैया, गाड़ी धुआँ बहुत छोड़ रही है! PUC जाँच और सर्विस समय पर करवा लीजिए।")]),
 dict(id="r5", dur=11, refs=["cast", "tshirt", "loc"], chyron="4.  कचरा न जलाएँ, मास्क पहनें", hold=True,
  still=LOC + "In the foreground KABIR hands a white mask to a mother sitting behind her husband on a motorcycle with a small child between them, the child already wearing a small mask; on the roadside footpath behind them a small heap of garbage smoulders with a thin line of smoke. MEERA and BUNTY hand out masks in the background. Medium shot, KABIR's face and T-shirt clearly visible." + MASK + SHIRT,
  action="KABIR gives the mask to the mother, gestures toward the smouldering garbage and says: \"और कचरा या पत्ते कभी मत जलाइए। बाहर निकलें, तो मास्क ज़रूर पहनिए।\" The mother puts the mask on and the child waves." + KEEP,
  lines=[("कबीर", "और कचरा या पत्ते कभी मत जलाइए। बाहर निकलें, तो मास्क ज़रूर पहनिए।")]),
 dict(id="r6", dur=10, refs=["cast", "tshirt", "loc"],
  still=LOC + "In the foreground the three students stand close together facing the camera, KABIR in the centre, MEERA on his left, BUNTY on his right; they have just pulled their masks down under their chins for a moment to speak, smiling confidently; behind them drivers wearing white masks sit in the stopped traffic, engines off. Medium close shot, golden light." + SHIRT,
  action="KABIR says to the camera with a confident smile: \"छोटे-छोटे कदम... और दिल्ली फिर से साँस लेगी।\" Then all three raise a fist together and say in unison: \"Pollution पर Solution!\" The camera is locked off; the building and signal stay unchanged. Exactly these lines are spoken.",
  lines=[("कबीर", "छोटे-छोटे कदम... और दिल्ली फिर से साँस लेगी।"), ("तीनों", "Pollution पर Solution!")]),
]
