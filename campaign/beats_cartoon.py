# -*- coding: utf-8 -*-
"""Cartoon satire "ज़िम्मेदारी का तकिया" — two invented party caricatures throw a pillow marked ज़िम्मेदारी at each other over Delhi's
air while a citizen coughs in the middle (SKIT=beats_cartoon). The characters are generic cartoon figures, not likenesses of real people."""
TAGLINE = "राजनीतिक व्यंग्य  |  AI-निर्मित कार्टून"
BEATS = []
CAST = {}
LOOK = ("Bright, clean 2D editorial cartoon illustration in a modern Indian animated-explainer style: bold outlines, flat colours with soft shading, expressive faces. "
        "The three characters are exactly those of the first reference image (the cartoon character sheet): "
        "NETA-B, a stout cartoon politician with a black moustache, saffron kurta and saffron scarf with a lotus badge; "
        "NETA-A, a slim cartoon politician, clean-shaven, in a white kurta with a blue-and-yellow sash and a broom badge; "
        "NAGRIK, an ordinary middle-aged Delhi citizen in a checked shirt with a white mask pulled under his chin, tired eyes, holding an inhaler. "
        "They are invented generic caricatures and must not resemble any real person. Setting: a Delhi street drowned in grey-brown cartoon smog with India Gate faint in the background. "
        "No captions, subtitles, name labels or character names anywhere; the only lettering allowed is the word on the pillow. ")
VOICES = ("Voices — NETA-B: loud, pompous, booming middle-aged male voice. NETA-A: sharp, nasal, indignant male voice. NAGRIK: tired, hoarse, ordinary man's voice, coughing between words. ")
RULES = ("Animated 2D cartoon scene with lively, slightly exaggerated cartoon motion and clear spoken Hindi dialogue with matching mouth movement. One continuous shot, no cuts. "
         "Only the lines given are spoken, exactly as written, in Hindi. Cartoon ambience only, no music, no laughter track, no subtitles or new text on screen; the word on the pillow stays unchanged. ")
PILLOW = "a big plump white pillow with the single Hindi word \"ज़िम्मेदारी\" printed on it in large bold red Devanagari letters, spelled exactly ज़ि-म्मे-दा-री as in the pillow of the second reference image"
OUTRO_PLAN = [("k1", 0.5, 4.6), ("k2", 1.0, 4.6), ("k3", 1.0, 4.6), ("k4", 1.0, 4.6), ("k5", 1.0, 5.0)]
SCENES = [
 dict(id="k1", dur=10, refs=["toon"], chyron="ज़िम्मेदारी का तकिया",
  still=f"Wide shot: NAGRIK stands in the centre of the smoggy street coughing, one hand on his chest; NETA-B stands on the left and NETA-A on the right, each behind a small podium, both looking away innocently and whistling. On the ground in front of NAGRIK lies {PILLOW}.",
  action="NAGRIK coughs, points at the pillow on the ground and asks the two politicians: \"नेता जी! दिल्ली की हवा ज़हर हो गई है। इसकी ज़िम्मेदारी कौन लेगा?\" Both politicians look at the pillow, then quickly look away.",
  lines=[("नागरिक", "नेता जी! दिल्ली की हवा ज़हर हो गई है। इसकी ज़िम्मेदारी कौन लेगा?")]),
 dict(id="k2", dur=10, refs=["toon", "still_k1"], sfx="whoosh", music="hope",
  still=f"Medium shot: NETA-B on the left has picked up {PILLOW} and holds it high over his head with both hands, about to throw it to the right, mouth open mid-shout; NAGRIK stands in the middle ducking; NETA-A on the right raises his palms in alarm.",
  action="NETA-B shouts: \"पंजाब में पराली जल रही है! वहाँ सरकार इनकी है। ये लो... ज़िम्मेदारी तुम्हारी!\" and hurls the pillow over NAGRIK's head toward NETA-A on the right.",
  lines=[("भाजपा नेता", "पंजाब में पराली जल रही है! वहाँ सरकार इनकी है। ये लो... ज़िम्मेदारी तुम्हारी!")]),
 dict(id="k3", dur=10, refs=["toon", "still_k1"], sfx="whoosh",
  still=f"Medium shot: NETA-A on the right has caught {PILLOW} against his chest and is winding up to throw it back to the left, face indignant; NAGRIK stands in the middle coughing with his head turned toward him; NETA-B on the left folds his arms smugly.",
  action="NETA-A shouts back: \"अरे वाह! दिल्ली में सरकार आपकी, केंद्र में सरकार आपकी! ये लो... ज़िम्मेदारी आपकी!\" and flings the pillow back over NAGRIK's head toward NETA-B on the left.",
  lines=[("आप नेता", "अरे वाह! दिल्ली में सरकार आपकी, केंद्र में सरकार आपकी! ये लो... ज़िम्मेदारी आपकी!")]),
 dict(id="k4", dur=9, refs=["toon", "still_k1"], sfx="laugh",
  still=f"Wide shot: {PILLOW} is flying through the air in an arc above NAGRIK's head, with cartoon speed lines; NETA-B on the left and NETA-A on the right both have their arms stretched out, having just thrown and about to catch; NAGRIK in the middle looks up dizzy, coughing, smog thickening around him.",
  action="The pillow flies back and forth over NAGRIK's head several times like a game of catch. NETA-B shouts: \"तुम्हारी!\" NETA-A shouts: \"नहीं, तुम्हारी!\" NAGRIK, turning his head left and right and coughing, cries: \"अरे, कोई तो पकड़ लो!\"",
  lines=[("भाजपा नेता", "तुम्हारी!"), ("आप नेता", "नहीं, तुम्हारी!"), ("नागरिक", "अरे, कोई तो पकड़ लो!")]),
 dict(id="k5", dur=10, refs=["toon", "still_k1"],
  still=f"Medium close shot: NAGRIK in the foreground looks straight at the viewer with tired eyes, inhaler in hand, white feathers floating down around him; behind him, smaller but clearly drawn, the same NETA-B (stout, black moustache, saffron kurta, black hair) and the same NETA-A (slim, clean-shaven, black hair, white kurta with blue-and-yellow sash) from the character sheet — both young-to-middle-aged with black hair, no beards, no white hair — are still tossing {PILLOW} between them.",
  action="NAGRIK looks at the viewer and says wearily: \"इनका तकिया इधर से उधर घूमता रहा... और दिल्ली की साँस, बीच में घुटती रही।\" Feathers drift down; behind him the two keep tossing the pillow.",
  lines=[("नागरिक", "इनका तकिया इधर से उधर घूमता रहा... और दिल्ली की साँस, बीच में घुटती रही।")]),
]
