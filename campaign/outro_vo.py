"""Closing call to action, spoken in the lead's own cloned voice (ElevenLabs text-to-speech, v3 — it won a blind ranking against v2 variants).
Usage: python3 outro_vo.py <clips_dir> <voice_id>  ->  <clips_dir>/outro.mp3 + outro.json (duration, speech span, subtitle lines, word times)"""
import os, sys, json, subprocess, requests
D, VOICE = sys.argv[1], sys.argv[2]; H = {"xi-api-key": os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")}
TEXT = ("दोस्तों, ये लड़ाई सिर्फ़ हमारी नहीं, आपकी भी है. हमारे साथ जुड़िए. अपने मोहल्ले में लोगों को मास्क बाँटिए, उन्हें जागरूक कीजिए. "
        "साँस लेना हमारा हक़ है. पॉल्यूशन पर सॉल्यूशन. अपना समर्थन या सवाल भेजने के लिए, हमारी पॉल्यूशन हेल्पलाइन पर मिस्ड कॉल दीजिए, या व्हाट्सएप कीजिए. "
        "नंबर है, eight, eight, seven, five, eight, three, three, eight, three, three. एन एस यू आई के साथ आइए.")
SUBS = ["दोस्तों, ये लड़ाई सिर्फ़ हमारी नहीं, आपकी भी है।", "हमारे साथ जुड़िए। अपने मोहल्ले में लोगों को मास्क बाँटिए, उन्हें जागरूक कीजिए।",
        "साँस लेना हमारा हक़ है। Pollution पर Solution।", "समर्थन या सवाल के लिए हमारी Pollution हेल्पलाइन पर मिस्ड कॉल दीजिए या WhatsApp कीजिए।",
        "नंबर : 8875833833   |   NSUI के साथ आइए।"]
ANCHORS = ["दोस्तों", "हमारे", "सांस", "अपना", "नंबर"]   # first word of each subtitle line (as the recogniser spells it)
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128", headers=H, timeout=200,
    json={"text": TEXT, "model_id": "eleven_v3", "voice_settings": {"stability": 0.5, "similarity_boost": 0.85, "style": 0.3, "use_speaker_boost": True}})
r.raise_for_status(); open(f"{D}/outro.mp3", "wb").write(r.content)
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{D}/outro.mp3"], capture_output=True, text=True).stdout)
s = requests.post("https://api.elevenlabs.io/v1/speech-to-text", headers=H, timeout=200, files={"file": open(f"{D}/outro.mp3", "rb")}, data={"model_id": "scribe_v1", "timestamps_granularity": "word", "language_code": "hin"}).json()
words = [[w["text"], w["start"], w["end"]] for w in s["words"] if w.get("type") == "word" and w["text"].strip()]
a, b = words[0][1], words[-1][2]; norm = lambda t: t.strip(" ,।.").replace("साँस", "सांस")
starts = []
for k in ANCHORS:   # start of each subtitle line = first occurrence of its anchor word after the previous line's start
    i = next((i for i, w in enumerate(words) if norm(w[0]) == k and (not starts or w[1] > starts[-1] + 0.5)), None)
    starts.append(words[i][1] if i is not None else None)
if None in starts:   # fall back to proportional timing
    n = sum(len(x) for x in SUBS); c = a; starts = []
    for x in SUBS: starts.append(c); c += (b - a) * len(x) / n
subs = [{"text": t, "start": s0, "end": (starts[i + 1] - 0.05 if i + 1 < len(starts) else b)} for i, (t, s0) in enumerate(zip(SUBS, starts))]
json.dump({"duration": d, "speech": [a, b], "subs": subs, "words": words}, open(f"{D}/outro.json", "w"), ensure_ascii=False); print("outro", round(d, 1), "s, speech", round(a, 1), "-", round(b, 1)); print([(w[0], round(w[1], 1)) for w in words])
