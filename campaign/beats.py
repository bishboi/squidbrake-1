# -*- coding: utf-8 -*-
"""Script for the film "Let Delhi Breathe" (v2, generated video shots).
Each beat: vo = Hindi narration (read verbatim), cap = caption text if it differs from vo,
title = (big, small, source) on-screen card, shots = list of (still_id, still_prompt, motion_prompt).
"""
STYLE = (" Photorealistic cinematic documentary film still, 35mm lens, shallow depth of field, "
         "muted desaturated grey-teal palette with sickly orange smog haze, soft film grain, somber, emotional. "
         "Ordinary Indian people, Delhi. No readable text, no captions, no watermark, no logos, no flags.")
WARM = (" Photorealistic cinematic film still, 35mm lens, warm golden sunlight, clear blue sky, rich natural colours. "
        "No readable text, no captions, no watermark, no logos.")
MOTION = " Photorealistic, natural slow cinematic motion, documentary realism, no text or captions appearing. Ambient natural sound only, no speech, no music."

BEATS = [
 dict(id="a1", vo="याद है वो दिल्ली? जब आसमान नीला था... और यमुना के पानी में चाँद दिखता था।", shots=[
  ("kites", "Children flying colourful kites on an Old Delhi rooftop in winter morning sunlight, clear deep blue sky, domes and old houses in the distance, joyful." + WARM,
   "The children laugh and tug their kite strings, kites dance in the blue sky, the camera slowly cranes upward."),
  ("yam_clean", "The Yamuna river decades ago at dawn, clean blue rippling water, a boatman rowing a small wooden boat, white birds flying low, old ghats and trees on the bank, the moon still faintly visible in the sky." + WARM,
   "The boatman rows gently, ripples spread on the clean water, birds glide past, slow drift forward.")]),
 dict(id="a2", vo="आज... उसी शहर में साँस लेना... एक सज़ा है।", shots=[
  ("smog_aerial", None, "Slow aerial drone flight forward over the city as thick smog drifts between the buildings, the dull sun barely glowing.")]),
 dict(id="a3", title=("AQI 1000+", "सरकारी पैमाना 500 पर ख़त्म", None),
  vo="दिल्ली के कई इलाक़ों में ए क्यू आई... एक हज़ार के पार जा चुका है। जबकि सरकारी पैमाना... पाँच सौ पर ही ख़त्म हो जाता है।",
  cap="दिल्ली के कई इलाक़ों में AQI... एक हज़ार के पार जा चुका है। जबकि सरकारी पैमाना... पाँच सौ पर ही ख़त्म हो जाता है।", shots=[
  ("indiagate", None, "The old man in a shawl walks slowly away toward India Gate with his cane through thick drifting winter smog, distant headlights pass, slow dolly forward.")]),
 dict(id="a4", title=("20 में से 13", "दुनिया के सबसे प्रदूषित शहर भारत में", "स्रोत : IQAir World Air Quality Report 2024"),
  vo="दुनिया के बीस सबसे प्रदूषित शहरों में... तेरह भारत के हैं। और दिल्ली... दुनिया की सबसे प्रदूषित राजधानी।", shots=[
  ("highway", "Wide telephoto shot of a north Indian city at dusk drowned in smog: an endless traffic jam on a flyover, red tail lights, factory and power plant chimneys releasing smoke on the horizon, a blood-orange sun." + STYLE,
   "Traffic crawls forward, smoke rises from the chimneys, smog rolls across the frame, slow push in.")]),
 dict(id="b1", vo="ये आरव है। सात साल का। इसके बस्ते में किताबों के साथ... एक इनहेलर भी रहता है।", shots=[
  ("boy", None, "The schoolboy looks at the camera, slowly lifts the inhaler toward his masked face, traffic and people pass behind him in the haze, gentle handheld camera.")]),
 dict(id="b2", vo="इसने खेल के मैदान से पहले... अस्पताल का रास्ता पहचान लिया है।", shots=[
  ("hospital", None, "Mist flows from the nebulizer mask, the sleeping boy's chest rises and falls, his mother's thumb gently strokes his hand, very slow push in.")]),
 dict(id="c1", vo="शांति देवी ने इस शहर को बनते देखा है। आज चार कदम चलती हैं... तो साँस उखड़ जाती है।", shots=[
  ("dadi", None, "The grandmother looks into the camera, breathes heavily, pulls her shawl closer and lowers her eyes, people pass blurred behind her."),
  ("oxygen", None, "The elderly woman breathes slowly through the oxygen tube and turns her head toward the grey window, dust floating in the light, slow push in.")]),
 dict(id="d1", vo="और वो बेज़ुबान... सड़क का कुत्ता... गाय... परिंदे... जिनके लिए न कोई मास्क है... न कोई आवाज़।", shots=[
  ("dog", None, "The street dog lifts its head weakly, blinks its watery eyes and lowers its chin back on its paws while blurred headlights pass behind."),
  ("cow", None, "Smoke curls up from the burning garbage, the cow chews slowly and turns its head, vehicles move through the haze behind."),
  ("pigeons", None, "The pigeons sit hunched on the wires in the smog, one shakes its feathers and flies away, slow tilt up to the blank grey sky.")]),
 dict(id="y1", vo="और यमुना? जिसे हम माँ कहते हैं... वो ज़हरीले झाग में दम तोड़ रही है।", shots=[
  ("yam_foam", "Aerial drone shot of the Yamuna river in Delhi near a barrage, the dark polluted water completely covered with thick white toxic foam like floating snow, grey smog, a bridge and hazy city skyline behind." + STYLE,
   "Slow drone flight low over the river as the thick white toxic foam drifts and swirls on the dark water.")]),
 dict(id="y2", vo="उसी झाग में खड़े होकर... हमारी माँएँ सूरज को अर्घ्य देती हैं।", shots=[
  ("yam_chhath", "Indian women devotees in bright sarees standing waist-deep in a river covered in thick white toxic foam at hazy sunrise, seen from behind, holding woven baskets of fruit and raising folded hands toward a dull orange sun, Chhath Puja on the polluted Yamuna." + STYLE,
   "The women raise their offerings toward the dull rising sun while the white foam drifts around their waists, slow push in.")]),
 dict(id="y3", vo="और इलाज? झाग छिपाने के लिए... नदी में और केमिकल छिड़क दिया जाता है। गंदगी वहीं रहती है... बस कैमरे को दिखनी बंद हो जाती है।", shots=[
  ("yam_spray", "Two workers standing on a small motor boat on a foam-covered polluted river in Delhi, spraying liquid chemical from hoses onto the thick white foam, plastic drums on the boat, smog, bridge behind." + STYLE,
   "The workers sweep their hoses side to side spraying chemical onto the foam, the foam slowly dissolves near the boat, the boat drifts forward."),
  ("yam_dark", "Close low-angle shot of black polluted river water with oily film, plastic waste and remnants of dissolving white foam at the muddy bank of the Yamuna, a drain pipe pouring dark sewage into the river." + STYLE,
   "Dark sewage pours from the pipe into the river, the oily water ripples and the last foam breaks apart, slow push in.")]),
 dict(id="m1", vo="हवा का भी यही इलाज है। ए क्यू आई नापने वाली मशीनों के आसपास... पानी का छिड़काव। हवा साफ़ नहीं होती... बस आँकड़े साफ़ हो जाते हैं।",
  cap="हवा का भी यही इलाज है। AQI नापने वाली मशीनों के आसपास... पानी का छिड़काव। हवा साफ़ नहीं होती... बस आँकड़े साफ़ हो जाते हैं।", shots=[
  ("aqi_spray", "A water tanker truck with a large anti-smog mist cannon spraying a huge cloud of water mist right next to a small white air quality monitoring station cabin with sensor inlets and an antenna on its roof, beside a busy smoggy Delhi road." + STYLE,
   "The mist cannon keeps spraying a wide cloud of water around the white monitoring cabin while smoggy traffic passes, slow pan from the truck to the cabin."),
  ("aqi_close", "Close-up of the metal sensor inlets on the roof of a white air quality monitoring station, fine water mist and droplets falling all around them, thick brown smog and blurred traffic in the background." + STYLE,
   "Water mist falls and droplets run down the sensor inlets while the smog hangs heavy behind, slow push in.")]),
 dict(id="s1", vo="और जिन पर ज़िम्मेदारी थी? जब शहर घुट रहा था... वो स्विट्ज़रलैंड की साफ़ हवा में थे।", shots=[
  ("plane", "A passenger jet climbing steeply out of a thick flat brown layer of smog covering a city into a perfectly clear blue sky above, seen from the side, sunlight on its wings." + WARM,
   "The jet climbs out of the brown smog layer into the clear blue sky, the city vanishes below in haze."),
  ("swiss", "Seen strictly from behind: an anonymous Indian official in a white kurta-pyjama, dark sleeveless jacket and a woollen overcoat standing on a luxury hotel terrace, arms relaxed on the railing, facing snow-covered Swiss Alps and a blue lake under a crystal-clear blue sky, a cup of tea on the railing, face not visible." + WARM,
   "The man seen from behind takes a long deep breath of the clean mountain air and stretches his arms contentedly, steam rises from the tea cup, slow push in.")]),
 dict(id="p1", title=("10 साल AAP  |  अब BJP", "सरकारें बदलीं, हवा नहीं", None),
  vo="दस साल... आम आदमी पार्टी की सरकार रही। अब भाजपा की सरकार है। सरकारें बदलीं... हवा नहीं बदली।", shots=[
  ("sachivalaya", "x", "Thick smog drifts across the government secretariat tower, official cars roll through the gate, the dull sun glows behind the building, slow tilt up."),
  ("chairs", None, "Slow dolly along the row of empty official chairs, dust floating in the dim light, smog pressing against the tall windows.")]),
 dict(id="p2", vo="बंद शीशों वाली महँगी गाड़ियाँ... बंगलों में एयर प्यूरीफ़ायर... हाथ में गरम चाय। जिनके बच्चे विदेश की साफ़ हवा में पढ़ सकते हैं... उन्हें आपके बच्चे की खाँसी सुनाई नहीं देती।", shots=[
  ("convoy", "x", "The convoy of black luxury SUVs with tinted windows speeds past, the masked people at the bus stop cough and turn their faces from the dust, smog swirling behind the cars."),
  ("tea", "x", "Locked-off close-up: the hands gently stir and tilt the steaming cup of tea on its saucer at chest level, steam curls upward, the air purifier's green light glows steadily and brown smog drifts outside the window. The camera does not move and no head or face ever enters the frame."),
  ("airport", "x", "The teenager walks away toward the departure gate pulling the suitcase, the hand in the white kurta sleeve waves goodbye, an aircraft taxis outside the glass.")]),
 dict(id="f1", title=("ज़िम्मेदार कौन?", None, None),
  vo="पूछो... ज़िम्मेदार कौन? तो एक सरकार... दूसरी सरकार पर उँगली उठा देती है।", shots=[
  ("mics", None, "Reporters jostle and push microphones forward, camera flashes pop, the man in the white kurta keeps jabbing his pointing finger away to the side, his face never in frame."),
  ("circle", None, "Seen from directly above, the men in white kurtas keep pointing and gesturing at one another in turn, the camera slowly rotates overhead.")]),
 dict(id="g1", vo="लोग सड़कों पर उतरे। माँओं ने तख़्तियाँ उठाईं। छात्रों ने आवाज़ उठाई। पर हर साल... वही वादे... वही धुआँ।", shots=[
  ("mothers", None, "The masked mothers hold their children close and lift their campaign placards, the crowd behind them moves, handheld documentary camera."),
  ("placards", None, "Smog drifts over the empty wet road, an abandoned cardboard placard flutters in the wind, distant street lights glow, slow push in.")]),
 dict(id="h1", vo="ज़रा सोचिए... हम अपने बच्चों के लिए क्या छोड़कर जा रहे हैं? एक ज़हरीली हवा... एक मरी हुई नदी... और खिड़की के पीछे क़ैद बचपन।", shots=[
  ("father", None, "The father and his small daughter walk hand in hand away from the camera down the road and slowly fade into the thick smog."),
  ("window", None, "The little girl's breath fogs the window pane, her small hand slides slowly down the glass as she stares at the grey smog outside.")]),
 dict(id="h2", vo="एक दिन आपका बच्चा पूछेगा... जब हवा ज़हर बन रही थी... तब आप क्या कर रहे थे?", shots=[
  ("eyes", None, "The child stares straight into the camera, blinks slowly, and a single tear rolls down onto the mask, extremely slow push in.")]),
 dict(id="p3", vo="मुख्यमंत्री रेखा गुप्ता जी... पर्यावरण मंत्री जी... दिल्ली आपसे जवाब माँग रही है।", shots=[
  ("students", None, "The students shout slogans and pump their fists in rhythm holding their campaign placards high, candle flames flicker, smog drifts through the street lights.")]),
 dict(id="i1", title=("Pollution पर Solution", None, None),
  vo="अब बहाने नहीं... समाधान चाहिए। पॉल्यूशन पर... सोल्यूशन।", cap="अब बहाने नहीं... समाधान चाहिए।", shots=[
  ("march", None, "The students walk forward toward the camera with determination holding their campaign placards high, sunlight breaking through the haze behind them, camera tracking backward at low angle.")]),
 dict(id="i2", vo="साँस लेना कोई एहसान नहीं... हमारा हक़ है। सवाल पूछिए। जवाब माँगिए। एन एस यू आई के साथ आइए।",
  cap="साँस लेना कोई एहसान नहीं... हमारा हक़ है। सवाल पूछिए। जवाब माँगिए। NSUI के साथ आइए।", shots=[
  ("crowd", None, "The huge crowd of students raises and waves their hands together, golden sunlight sweeps across them, slow aerial rise.")]),
 dict(id="i3", end=True, vo="दिल्ली को... साँस लेने दो।", shots=[
  ("rooftop", None, "The child on the rooftop spreads her arms wider and takes a deep breath as the kite soars in the clear blue sky, camera slowly rises behind her.")]),
]
# stills reused from the first cut: v2 shot id -> v1 image file
REUSE = dict(kites="a1_0", smog_aerial="a2_0", indiagate="a3_0", boy="b1_0", hospital="b2_0", dadi="c1_0", oxygen="c2_0", dog="d1_0",
             cow="d2_0", pigeons="d2_1", mics="f1_0", circle="f2_0", mothers="g1_0", students="g1_1", placards="g2_0", father="h1_0",
             window="h3_0", eyes="h4_0", march="i1_0", crowd="i2_0", rooftop="i3_0")
