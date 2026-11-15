# -*- coding: utf-8 -*-
"""Script for the film "दिल्ली 2126" — a letter from a child living in Delhi a hundred years from now.
Speculative fiction. Shots are (shot_id, motion_prompt, options):
  first = still used as the first frame (default: shot_id), last = still used as the last frame (a morph across a century),
  tag = corner label, reuse = clip id taken from the first film."""
TAGLINE = "काल्पनिक भविष्य  |  AI-निर्मित"
VOICE = "nova"
VO_SYS = ("You are voicing a twelve-year-old girl named Aarvi who lives in Delhi in the year 2126 and is reading aloud a letter "
          "to the people of the past. Read the user's line EXACTLY as written, in Hindi — do not add, drop, translate or answer "
          "anything. Voice: young, soft, sincere and intimate, quietly sad, never theatrical; unhurried natural pace. Treat '...' "
          "as a short pause. Natural Hindustani pronunciation. Tone for this line: {tone}")
TONE = {"o": "soft, matter-of-fact sadness, a child describing her normal", "q": "hurt, direct, a quiet question",
        "r": "hope slowly returning, then a gentle, firm appeal"}
FUT = (" Photorealistic cinematic science-fiction film still set in Delhi in the year 2126, 35mm lens, dense orange-brown toxic dust "
       "haze, decayed and half-abandoned, grounded and believable, soft film grain. No readable text, no captions, no watermark, no logos.")
SAME = "This is the same place and the same camera framing as the reference photo, one hundred years later. "
MOTION = " Photorealistic, natural slow cinematic motion, no text or captions appearing. Ambient natural sound only, no speech, no music."
MORPH = "A slow time-lapse of one hundred years passing in a locked-off shot, the scene gradually transforming from the first frame into the last frame: "

# still_id -> (prompt, [reference stills from the first film])
STILLS = {
 "f_skyline": (SAME + "The Delhi cityscape seen from the air: crumbling towers wrapped in orange-brown dust, giant air-filter stacks, no trees, a blood-red sun barely visible." + FUT, ["smog_aerial"]),
 "f_girl": ("Portrait of a twelve-year-old Indian girl in worn patched clothes, a heavy scratched respirator mask hanging at her neck and dust goggles pushed up on her forehead, standing in a dim corridor of a decayed housing block, orange dust light through a sealed window, looking straight into the camera with calm tired eyes." + FUT, []),
 "f_roof": (SAME + "The Old Delhi rooftop is abandoned and crumbling, covered in orange dust, no children, a single torn faded kite tangled on a rusted wire, the sky a thick brown-orange wall of smog, the domes in the distance barely visible." + FUT, ["kites"]),
 "f_indiagate": (SAME + "India Gate stands cracked and half buried in drifts of orange dust, the road gone, a few small figures in full respirator suits walking past with oxygen tanks, rusted lamp posts." + FUT, ["indiagate"]),
 "f_yamuna": (SAME + "The Yamuna river has completely dried up into a cracked black tar-like channel with a thin stream of dark sludge, the barrage rusted and broken, orange dust sky." + FUT, ["yam_foam"]),
 "f_playground": (SAME + "The playground is buried in orange dust, the swings rusted and broken, dead tree stumps, a faded hazard sign on a fence, brown-orange sky." + FUT, ["playground"]),
 "f_class": ("A windowless underground school classroom, rows of Indian children at old desks each wearing a small oxygen mask connected by tubes to cylinders beside their chairs, a teacher holding up an oxygen cylinder valve to demonstrate, cold flickering tube light." + FUT, []),
 "f_domes": ("Enormous gleaming glass domes with lush green gardens and clean blue light inside rising above a vast dark slum of ordinary people living outside in thick orange toxic dust, seen from the slum, stark contrast between inside and outside." + FUT, []),
 "f_queue": ("A long queue of poor Indian families in respirator masks holding empty oxygen cylinders, waiting at a caged air-ration booth with a glowing meter, a mother holding a small child, orange dust swirling." + FUT, []),
 "f_tree": ("Inside a dim museum hall, a single small living green tree preserved inside a tall sealed glass case under a spotlight, a group of Indian schoolchildren in respirator masks pressing their hands on the glass and staring at it in wonder." + FUT, []),
 "f_wires": (SAME + "The electric wires hang empty and broken, not a single bird anywhere, the buildings decayed, the sky a solid orange-brown dust wall." + FUT, ["pigeons"]),
 "f_museum": ("A museum display case in a dim hall holding an old, faded, creased cardboard protest placard from a century ago showing the campaign poster from the reference image, reproduced accurately, lit by a small spotlight; a girl's hand in a worn glove touching the glass; dust in the air." + FUT, ["BRAND:let-delhi-breathe"]),
 "f_eyes": (SAME + "The same extreme close-up of a child's large dark eyes looking into the camera, but now above a heavy scratched industrial respirator mask, dust on the skin, orange light, a tear forming." + FUT, ["eyes"]),
 "g_skyline": (SAME + "The Delhi cityscape seen from the air under a brilliant clear blue sky, rooftops covered in gardens and solar panels, wide green tree-lined avenues, a clean blue river in the distance, birds flying, bright hopeful sunlight. Photorealistic cinematic film still, 35mm lens. No readable text, no logos.", ["smog_aerial"]),
 "split": ("One single wide photograph of India Gate split exactly down the middle: the left half is a dystopian future, cracked monument in thick orange toxic dust with figures in respirators; the right half is a hopeful future, the same monument under a clear blue sky with green trees, children running and kites flying. Seamless vertical divide through the centre of the arch. Photorealistic cinematic film still. No readable text, no logos.", ["indiagate"]),
}

BEATS = [
 dict(id="o1", title=("दिल्ली, 2126", "सौ साल बाद की एक चिट्ठी", None),
  vo="ये चिट्ठी... सौ साल बाद की दिल्ली से है। मेरा नाम आरवी है। मैं बारह साल की हूँ... और मैंने आज तक... आसमान नहीं देखा।", shots=[
  ("f_skyline", "Slow aerial drift forward over the ruined dust-choked city, orange haze rolling between crumbling towers, the red sun pulsing dimly.", dict(tag="2126")),
  ("f_girl", "The girl looks steadily into the camera, blinks slowly, dust drifting through the light behind her, very slow push in.", dict(tag="2126"))]),
 dict(id="o2", vo="दादी कहती थीं... कभी यहाँ आसमान नीला होता था। बच्चे छतों पर पतंग उड़ाते थे। मुझे लगता था... वो कहानियाँ सुनाती हैं।", shots=[
  ("kites", None, dict(reuse="kites", tag="2026")),
  ("m_roof", MORPH + "the blue sky turns brown and orange, the children and kites fade away, the rooftop crumbles and gathers dust.", dict(first="kites", last="f_roof", tag="2026 → 2126"))]),
 dict(id="o3", vo="इंडिया गेट अब धूल में आधा दबा है। वहाँ जाने के लिए... ऑक्सीजन का परमिट लगता है।", shots=[
  ("m_gate", MORPH + "the grey smog thickens into orange dust, dunes of dust rise and bury the road, the monument cracks, the old man fades and suited figures appear.", dict(first="indiagate", last="f_indiagate", tag="2026 → 2126"))]),
 dict(id="o4", vo="यमुना... अब नदी नहीं है। किताबों में लिखा है कि लोग उसे माँ कहते थे। अब वो... एक काली, सूखी लकीर है।", shots=[
  ("m_yamuna", MORPH + "the foam-covered river shrinks and dries into a cracked black channel, the barrage rusts and breaks, the sky turns orange.", dict(first="yam_foam", last="f_yamuna", tag="2026 → 2126"))]),
 dict(id="o5", vo="हमारे स्कूल में खेल का मैदान नहीं है। खिड़कियाँ नहीं हैं। साँस की क्लास है... जहाँ सिखाते हैं कि सिलेंडर कैसे बदलते हैं।", shots=[
  ("m_play", MORPH + "dust slowly buries the playground, the swings rust and break, the trees die into stumps, the sky turns orange.", dict(first="playground", last="f_playground", tag="2026 → 2126")),
  ("f_class", "The children breathe slowly through their masks, the teacher turns the cylinder valve to demonstrate, the tube light flickers, slow dolly along the desks.", dict(tag="2126"))]),
 dict(id="o6", vo="हवा अब ख़रीदी जाती है। अमीरों के लिए... काँच के गुंबद हैं। और हम सबके लिए... राशन की लाइन। रोज़... दो घंटे की साफ़ हवा।", shots=[
  ("f_domes", "Slow tilt up from the dark dusty slum to the huge glowing green glass domes above, orange dust blowing across the foreground.", dict(tag="2126")),
  ("f_queue", "The queue shuffles forward one step, people adjust their masks and cylinders, the meter on the booth blinks, dust swirls, the mother pulls her child closer.", dict(tag="2126"))]),
 dict(id="o7", vo="यहाँ कोई परिंदा नहीं है। कोई कुत्ता नहीं... कोई गाय नहीं। मैंने पेड़... सिर्फ़ म्यूज़ियम में देखा है।", shots=[
  ("m_wires", MORPH + "the pigeons vanish one by one, the wires sag and snap, the buildings decay and the sky turns to solid orange dust.", dict(first="pigeons", last="f_wires", tag="2026 → 2126")),
  ("f_tree", "The children lean closer and press their palms on the glass, the little tree's leaves tremble in the recycled air, slow push in.", dict(tag="2126"))]),
 dict(id="o8", vo="इतिहास की किताब में... आपके ज़माने की तस्वीरें हैं। लोग तख़्तियाँ लेकर खड़े हैं। माँएँ... छात्र। और नीचे लिखा है — किसी ने नहीं सुना।", shots=[
  ("mothers", None, dict(reuse="mothers", tag="2026", archive=True)),
  ("students", None, dict(reuse="students", tag="2026", archive=True)),
  ("f_museum", "The gloved hand slowly slides down the glass in front of the old placard, dust floats through the spotlight, very slow push in.", dict(tag="2126"))]),
 dict(id="q1", vo="मैं आपसे बस एक सवाल पूछना चाहती हूँ। आपको सब पता था। ज़हरीली हवा भी... मरती हुई नदी भी... बीमार बच्चे भी। फिर आपने... कुछ किया क्यों नहीं?", shots=[
  ("f_eyes", "The child stares straight into the camera above the respirator, blinks slowly, a single tear rolls down through the dust, extremely slow push in.", dict(tag="2126"))]),
 dict(id="r1", title=("ये भविष्य अभी लिखा नहीं गया", None, None),
  vo="लेकिन ये चिट्ठी... अभी लिखी नहीं गई है। ये दिल्ली... अभी बनी नहीं है। मेरा आसमान... आज भी आपके हाथ में है।", shots=[
  ("m_back", "A slow time-lapse transforming the first frame into the last frame: the orange dust clears, the ruins become living green rooftops, trees grow along the avenues, the sky turns brilliant blue and birds return.", dict(first="f_skyline", last="g_skyline", tag="2126 → ?"))]),
 dict(id="r2", vo="दो दिल्ली हैं। एक... जो आपके चुप रहने से बनेगी। दूसरी... जो आज आवाज़ उठाने से।", shots=[
  ("split", "On the left half orange dust blows past the suited figures, on the right half children run and kites dance in the blue sky, the dividing line stays fixed in the centre, slow push in.", dict())]),
 dict(id="r3", end=True, vo="दिल्ली को साँस लेने दो। ताकि एक दिन... मैं आसमान देख सकूँ।", shots=[
  ("march", None, dict(reuse="march", tag="2026")),
  ("rooftop", None, dict(reuse="rooftop"))]),
]
