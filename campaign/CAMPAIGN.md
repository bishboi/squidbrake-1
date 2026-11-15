# Let Delhi Breathe — NSUI Delhi clean-air campaign

**Slogans:** Let Delhi Breathe · Pollution पर Solution · दिल्ली को साँस लेने दो · **Tags:** #LetDelhiBreathe #PollutionParSolution · **Question we keep asking:** ज़िम्मेदार कौन?

## 1. The idea in one line

Clean air is not a favour from any government — it is a right. Every winter Delhi gets a blame game instead of a plan.
The campaign makes one demand that nobody can pass on to someone else: **one accountable authority, one public plan, one deadline.**

**Tone:** grief first, anger second, hope last. We speak as sons, daughters and students — not as a party attacking a party.
The villain is the *pointing finger*, not a named person. This keeps the campaign credible and shareable beyond our own supporters.

## 2. Who we are talking to

| Audience | What they feel | What we ask of them |
|---|---|---|
| Students (DU, JNU, Jamia, IP, Ambedkar) | Anger, helplessness | Join the march, sign the charter, make content |
| Parents of young children | Fear, guilt | Share the film, send a child's letter |
| Elderly and their families | Being forgotten | Tell their story on camera |
| Outdoor workers (rickshaw, vendors, traffic police, delivery riders) | No choice | Receive masks and health check-ups, speak at events |
| Media and the undecided public | Fatigue ("every year the same story") | Cover the charter and the deadline, not just the smog |

## 3. The film — "Let Delhi Breathe" (3 min 29 sec)

File: `campaign/let-delhi-breathe.mp4` · full narration: section 8 · shot list: `campaign/beats.py`
Every shot is generated video (not slides), with Hindi narration, captions, an original score and ambient sound.

| Chapter | What we see | Feeling |
|---|---|---|
| याद है वो दिल्ली? | Kites over Old Delhi, a boat on a clean Yamuna | Nostalgia |
| आज | City under smog; **AQI 1000+**; **13 of the world's 20 most polluted cities are in India** | Shock |
| आरव, 7 साल | Schoolboy with an inhaler, then on a nebuliser | Heartbreak |
| शांति देवी | Grandmother on oxygen | Tenderness |
| बेज़ुबान | Street dog, cow at burning garbage, birds on wires | Compassion |
| **यमुना** | River under toxic foam, women offering Chhath prayers standing in it | Grief |
| **इलाज के नाम पर** | Chemical sprayed to hide the foam; water sprayed around AQI monitors — "हवा साफ़ नहीं होती, बस आँकड़े साफ़ हो जाते हैं" | Anger |
| **स्विट्ज़रलैंड** | A jet climbing out of the smog; a faceless official breathing Alpine air | Bitter irony |
| **10 साल AAP, अब BJP** | Secretariat in smog, empty chairs; convoy of sealed SUVs, tea beside an air purifier, a departure gate — all shown faceless | Cold anger |
| ज़िम्मेदार कौन? | Microphones, pointing fingers; later a direct question to the Chief Minister and the Environment Minister | Anger |
| आवाज़ें जो दब गईं | Mothers and students protesting, abandoned placards | Defeat |
| बच्चों की विरासत | Father and daughter fading into smog, girl behind a window, a child's eyes | The emotional peak |
| Pollution पर Solution | Students marching into sunrise, end card "Let Delhi Breathe" | Resolve |

Cut-downs to make from the same shots: a 30-second reel (child's question + end card), a 20-second Yamuna reel,
a 15-second "आँकड़े साफ़, हवा नहीं" reel, and vertical single-chapter stories.

### Claims in the film and what backs them — check before release

| Line in the film | Basis | Status |
|---|---|---|
| AQI above 1000 in parts of Delhi | Private real-time monitors (IQAir) showed 1000+ readings in November 2024 | Solid, but say "private monitors": the official CPCB index stops at 500, which the film states |
| 13 of the 20 most polluted cities are in India; Delhi the most polluted capital | IQAir World Air Quality Report 2024 (shown on screen) | Solid; update if a newer edition changes the count |
| Chemical sprayed on the Yamuna to suppress foam | Delhi Jal Board has sprayed anti-foaming agents before Chhath, widely reported | Solid |
| Water sprayed around AQI monitoring stations | News videos and opposition allegations; the government has called it routine dust control | **Contested** — keep the clips and dates ready |
| AAP governed Delhi for ten years, BJP governs now | AAP governments 2015–2025; BJP government since February 2025 | Solid |
| Sealed cars, air purifiers, children who can study abroad | A general statement about the privilege of those in power; no named person is shown or accused | Keep it general — do not attach it to a named politician or their family without a published source |
| Those responsible were in Switzerland while the city choked | Supplied by the campaign team | **Not verified by the film-maker — confirm who, when and a source before publishing** |

## 3b. Second film — "दिल्ली 2126" (2 min 8 sec)

File: `campaign/delhi-2126.mp4` · script: `campaign/beats2126.py`

A letter from Aarvi, a twelve-year-old living in Delhi a hundred years from now, read in a child's voice. Shots from the
first film morph across a century into their future versions (corner labels show "2026 → 2126"): the kite rooftop turns to
dust, India Gate is half buried, the foaming Yamuna dries into a black channel, the pigeons vanish from the wires.
Her world has breathing classes instead of playgrounds, glass domes for the rich and air-ration queues for everyone else,
and a single tree in a museum. Today's protest footage appears as a history-book archive, with our own placard in a
museum case. She asks: "आपको सब पता था… फिर आपने कुछ किया क्यों नहीं?" Then the turn — "ये चिट्ठी अभी लिखी नहीं गई है" — the
ruined skyline heals into a green city, India Gate is shown split between the two futures, and the film closes on the
campaign end card.

It is clearly labelled as fiction on screen ("काल्पनिक भविष्य | AI-निर्मित") and makes no factual claims, so it needs no
sourcing. Best used as the second release, a week after the first film, and as the opener at campus screenings.
Build: `FILM=beats2126 python3 gen_assets.py <dir> vo stills videos`, then `FILM=beats2126 python3 render.py <dir> <music.mp3> delhi-2126.mp4`.

## 3c. Comedy skit — "Pollution का Solution — एक खोज" (2 min 35 sec)

File: `campaign/pollution-ka-solution-skit.mp4` · script: `campaign/beats_skit.py` · cast and T-shirt references: `campaign/brand/`

A reel-style satire with speaking characters, comedy music, stings and audience laughter. Three students in the campaign
T-shirt — the lead (from supplied photos), Meera (sarcastic) and Bunty (comic relief) — go looking for a solution.
At the first bungalow the gatekeeper says the minister is "घर पर" — his village home, where he left before Diwali because the
doctor said Delhi's air is harmful ("और हमारे लिए? विटामिन है?"). At the second, the deadpan guard says the minister is in a
meeting — in Switzerland, "studying what clean air looks like". So they go straight to the Chief Minister, who tells them
"AQI तो एक temperature है… किसी भी instrument से नाप लो" and, when corrected, "तो AC चला लो!" Outside, Bunty suggests going to the PM;
the lead replies that he is away in winter, and that to get an answer from him you go not to his house but to Jantar Mantar —
all three slap their foreheads: "फिर से नहीं…!" They walk on — "जिन्हें AQI का
मतलब नहीं पता, उनसे solution क्या मिलेगा? शुरुआत हम ख़ुद करेंगे… और सवाल पूछना बिल्कुल नहीं छोड़ेंगे" — carrying cartons of masks,
which they hand out to rickshaw pullers and street workers. Bunty then tries to put one on a street cow: "इनको मास्क कैसे
पहनाऊँ?" — "गाय और कुत्तों के लिए मास्क नहीं बनते… इनके लिए तो हवा ही साफ़ करनी पड़ेगी।" The last line to camera: "AQI temperature नहीं होता। पर हाँ — जनता का पारा ज़रूर चढ़ रहा है।"

Nameplates name real office-holders: Bhupender Yadav (Minister of Environment, Forest and Climate Change) on the first
gate, J. P. Nadda (Minister of Health and Family Welfare) on the second, and Rekha Gupta on the Chief Minister's desk. The
two ministers are never shown, and the Chief Minister is played by an invented face that is not modelled on any real
person or photo. The film opens on a card saying it is fictional satire with AI-made visuals and voices, and carries a
"काल्पनिक व्यंग्य | AI-निर्मित" label throughout. Because real people are named, have the jokes attached to them
(leaving Delhi before Diwali on a doctor's advice, the Switzerland trip, the AC line) checked by your legal team
before release, and follow the Election Commission's rules on labelling synthetic content.
Build: `python3 skit_gen.py <dir>` (stills, dialogue clips, transcripts), then `python3 skit.py <dir> <sfx_dir> pollution-ka-solution-skit.mp4`.

## 4. On-ground ideas

1. **साँस सत्याग्रह (launch day).** A completely silent march from Mandi House to Jantar Mantar. No slogans for the first
   kilometre — only masks and the sound of an amplified heartbeat. Silence is the image TV cameras do not get from a normal protest.
2. **"Blame Relay" nukkad natak.** Four actors in white kurtas pass a relay baton labelled *ज़िम्मेदारी* around in a circle
   while a child in the middle coughs. Performed at metro stations and college gates; 4 minutes, easy to film.
3. **ख़ाली झूले (Empty Swings).** A row of children's swings installed at Connaught Place, each carrying a school bag and an
   inhaler. A board reads: "ये बच्चे आज बाहर नहीं खेल सकते।"
4. **Delhi's Report Card.** A giant school report card for "Clean Air", subject by subject (public transport, dust, waste
   burning, stubble support, data transparency), graded by students, delivered publicly to every responsible office — Centre,
   Delhi government, MCD, and the air-quality commission. Everyone gets the same card: nobody can point elsewhere.
5. **Oxygen Class.** Professors take one lecture outdoors on the college lawn with the whole class masked, an AQI display
   beside the blackboard. One campus a day for two weeks.
6. **नेता जी के नाम चिट्ठी.** School children and grandparents write postcards. Target 1,00,000 postcards, displayed as a wall
   before being delivered.
7. **बेज़ुबान दस्ता.** Student volunteers with vets run water, feeding and first-aid points for street animals and birds on
   severe-AQI days. Shows that we act, not only demand.
8. **Mask and health camps for outdoor workers.** N95 masks and free lung-function tests for rickshaw pullers, vendors,
   sanitation workers and traffic police, with volunteer doctors.
9. **Campus AQI boards.** A low-cost sensor and live display at every college gate, run by the NSUI unit; daily reading posted online.
10. **यमुना आरती, मास्क पहनकर.** An evening aarti on the Yamuna bank with every participant masked and jars of the river's water on display — one image that joins the air and the river.
11. **"आँकड़े नहीं, हवा साफ़ करो" watch.** Student teams photograph and geotag any sprinkling staged around AQI monitoring stations and publish it daily.
12. **21-day countdown.** A public clock at the campaign site counting the days since the charter was submitted without a written reply.

## 5. Digital ideas

- **#ZimmedarKaun chain:** people post a selfie pointing at the camera, with the line "मैं पूछ रहा/रही हूँ" — turning the
  politicians' pointing finger back on them.
- **"मेरी साँस, मेरी कहानी":** 30-second testimonies (asthmatic child's mother, a 70-year-old, a delivery rider). One a day.
- **Then/Now:** people post their own childhood sky photo next to today's from the same spot.
- **AQI filter:** an Instagram filter that puts today's live AQI of your area on your face mask.
- **Missed-call and WhatsApp petition** for the charter, with a daily signature counter.
- **Daily "Excuse of the Day" card:** quoting, with source and date, that day's official statement shifting responsibility — no editorialising needed.

## 6. Charter of demands (the "one plan, one deadline" charter)

1. **One accountable body** — a joint Centre–Delhi–neighbouring-states clean-air task force with a named head, public targets and a quarterly public report.
2. **A year-round plan, not a November emergency** — published sector-wise targets for vehicles, dust, industry, waste and biomass burning.
3. **Public transport first** — more electric buses, last-mile links, and **concessional metro passes for students**.
4. **Support farmers instead of blaming them** — machines and payment for stubble management before the harvest, not fines after it.
5. **Zero open waste burning and enforced dust control** at every construction site, with a public complaint dashboard.
6. **Protect the most exposed** — air purifiers in government schools and hospitals, free masks and annual lung check-ups for outdoor workers.
7. **Honest data** — real-time, ward-level AQI and source data, no sprinkling or cleaning drives staged around monitoring stations, and an independent audit of the monitors.
8. **A living Yamuna** — a dated plan to stop untreated sewage and industrial discharge entering the river, with monthly public water-quality reports; treat the cause, not the foam.
9. **Care for the voiceless** — shelter, water and veterinary support for street animals on severe-AQI days.

## 7. Six-week rollout

| Week | Phase | Main actions |
|---|---|---|
| 1 | **Feel** | Film release, testimonies, Then/Now posts |
| 2 | **Ask** | #ZimmedarKaun chain, Blame Relay street plays, Report Card deliveries |
| 3 | **Show up** | साँस सत्याग्रह silent march, Empty Swings, charter submitted, countdown clock starts |
| 4 | **Serve** | Mask and health camps, बेज़ुबान दस्ता, campus AQI boards |
| 5 | **Pressure** | Postcard wall, Oxygen Classes, daily Excuse-of-the-Day cards |
| 6 | **Deadline** | Day-21 public hearing: read out the replies received (or not), announce next steps |

**How we measure it:** charter signatures, postcards collected, colleges with AQI boards, workers screened,
film completion rate, and — the only one that finally matters — a written, dated reply to the charter.

## 8. Narration (Hindi voice-over, as recorded)

> याद है वो दिल्ली? जब आसमान नीला था... और यमुना के पानी में चाँद दिखता था।
> आज... उसी शहर में साँस लेना... एक सज़ा है।
> दिल्ली के कई इलाक़ों में AQI... एक हज़ार के पार जा चुका है। जबकि सरकारी पैमाना... पाँच सौ पर ही ख़त्म हो जाता है।
> दुनिया के बीस सबसे प्रदूषित शहरों में... तेरह भारत के हैं। और दिल्ली... दुनिया की सबसे प्रदूषित राजधानी।
>
> ये आरव है। सात साल का। इसके बस्ते में किताबों के साथ... एक इनहेलर भी रहता है।
> इसने खेल के मैदान से पहले... अस्पताल का रास्ता पहचान लिया है।
> शांति देवी ने इस शहर को बनते देखा है। आज चार कदम चलती हैं... तो साँस उखड़ जाती है।
> और वो बेज़ुबान... सड़क का कुत्ता... गाय... परिंदे... जिनके लिए न कोई मास्क है... न कोई आवाज़।
>
> और यमुना? जिसे हम माँ कहते हैं... वो ज़हरीले झाग में दम तोड़ रही है।
> उसी झाग में खड़े होकर... हमारी माँएँ सूरज को अर्घ्य देती हैं।
> और इलाज? झाग छिपाने के लिए... नदी में और केमिकल छिड़क दिया जाता है। गंदगी वहीं रहती है... बस कैमरे को दिखनी बंद हो जाती है।
> हवा का भी यही इलाज है। AQI नापने वाली मशीनों के आसपास... पानी का छिड़काव। हवा साफ़ नहीं होती... बस आँकड़े साफ़ हो जाते हैं।
>
> और जिन पर ज़िम्मेदारी थी? जब शहर घुट रहा था... वो स्विट्ज़रलैंड की साफ़ हवा में थे।
> दस साल... आम आदमी पार्टी की सरकार रही। अब भाजपा की सरकार है। सरकारें बदलीं... हवा नहीं बदली।
> बंद शीशों वाली महँगी गाड़ियाँ... बंगलों में एयर प्यूरीफ़ायर... हाथ में गरम चाय। जिनके बच्चे विदेश की साफ़ हवा में पढ़ सकते हैं... उन्हें आपके बच्चे की खाँसी सुनाई नहीं देती।
> पूछो... ज़िम्मेदार कौन? तो एक सरकार... दूसरी सरकार पर उँगली उठा देती है।
> लोग सड़कों पर उतरे। माँओं ने तख़्तियाँ उठाईं। छात्रों ने आवाज़ उठाई। पर हर साल... वही वादे... वही धुआँ।
>
> ज़रा सोचिए... हम अपने बच्चों के लिए क्या छोड़कर जा रहे हैं? एक ज़हरीली हवा... एक मरी हुई नदी... और खिड़की के पीछे क़ैद बचपन।
> एक दिन आपका बच्चा पूछेगा... जब हवा ज़हर बन रही थी... तब आप क्या कर रहे थे?
>
> मुख्यमंत्री रेखा गुप्ता जी... पर्यावरण मंत्री जी... दिल्ली आपसे जवाब माँग रही है।
> अब बहाने नहीं... समाधान चाहिए। Pollution पर... Solution.
> साँस लेना कोई एहसान नहीं... हमारा हक़ है। सवाल पूछिए। जवाब माँगिए। NSUI के साथ आइए।
> **दिल्ली को... साँस लेने दो।**

## 9. Production notes

- Every shot is AI-generated and the film carries an on-screen "सांकेतिक दृश्य | AI-निर्मित" label. Aarav and Shanti Devi are
  representative characters, not real people. The film names the AAP and BJP governments and addresses the Chief Minister by name, but no real person's face or likeness is generated: officials are shown faceless, and the NSUI leader should appear through real footage or an official photo.
- Campaign posters and the NSUI emblem in `campaign/brand/` were restored from the T-shirt mock-up; the emblem is a redraw, so swap in the official files when you have them.
- Narration: `openai/gpt-audio` · stills: `google/gemini-3.1-flash-image` · video shots: `google/gemini-omni-1.2-flash` (image-to-video, 1080p)
  · score: `google/lyria-3-pro-preview`, all through OpenRouter.
- Rebuild: `OPENROUTER_API_KEY=… python3 gen_assets.py <assets_dir> vo stills videos`, then
  `python3 render.py <assets_dir> <music.mp3> let-delhi-breathe.mp4`. Change the narrator with `VO_VOICE=<voice>`.
- Before public release: have a Hindi speaker listen once end to end, confirm the two flagged claims in section 3,
  replace the generated score if you need a licensed track for broadcast, and add the official NSUI logo on the end card.
