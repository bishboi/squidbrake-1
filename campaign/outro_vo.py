"""Closing call to action, spoken in the lead's own cloned voice (ElevenLabs text-to-speech, v3 — it won a blind ranking against v2 variants).
Usage: python3 outro_vo.py <clips_dir> <voice_id>  ->  <clips_dir>/outro.mp3 + outro.json (duration, speech span, subtitle lines, word times)"""
import os, sys, json, subprocess, requests
D, VOICE = sys.argv[1], sys.argv[2]; H = {"xi-api-key": os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")}
TEXT = ("दोस्तों, ये लड़ाई सिर्फ़ हमारी नहीं, आपकी भी है. हमारे साथ जुड़िए. अपने मोहल्ले में लोगों को मास्क बाँटिए, उन्हें जागरूक कीजिए. "
        "साँस लेना हमारा हक़ है. पॉल्यूशन पर सॉल्यूशन. एन एस यू आई के साथ आइए.")
SUBS = ["दोस्तों, ये लड़ाई सिर्फ़ हमारी नहीं, आपकी भी है।", "हमारे साथ जुड़िए। अपने मोहल्ले में लोगों को मास्क बाँटिए, उन्हें जागरूक कीजिए।",
        "साँस लेना हमारा हक़ है। Pollution पर Solution। NSUI के साथ आइए।"]
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128", headers=H, timeout=200,
    json={"text": TEXT, "model_id": "eleven_v3", "voice_settings": {"stability": 0.5, "similarity_boost": 0.85, "style": 0.3, "use_speaker_boost": True}})
r.raise_for_status(); open(f"{D}/outro.mp3", "wb").write(r.content)
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{D}/outro.mp3"], capture_output=True, text=True).stdout)
s = requests.post("https://api.elevenlabs.io/v1/speech-to-text", headers=H, timeout=200, files={"file": open(f"{D}/outro.mp3", "rb")}, data={"model_id": "scribe_v1", "timestamps_granularity": "word", "language_code": "hin"}).json()
words = [[w["text"], w["start"], w["end"]] for w in s["words"] if w.get("type") == "word" and w["text"].strip()]
a, b = words[0][1], words[-1][2]; n = sum(len(x) for x in SUBS); c = a; subs = []
for x in SUBS: dd = (b - a) * len(x) / n; subs.append({"text": x, "start": c, "end": c + dd}); c += dd
json.dump({"duration": d, "speech": [a, b], "subs": subs, "words": words}, open(f"{D}/outro.json", "w"), ensure_ascii=False); print("outro", round(d, 1), "s, speech", round(a, 1), "-", round(b, 1)); print([(w[0], round(w[1], 1)) for w in words])
