"""Closing call to action, spoken in the lead's own cloned voice (ElevenLabs text-to-speech).
Usage: python3 outro_vo.py <clips_dir> <voice_id>  ->  <clips_dir>/outro.mp3 + outro.json (subtitle lines)"""
import os, sys, json, subprocess, requests
D, VOICE = sys.argv[1], sys.argv[2]
LINES = ["दोस्तों, ये लड़ाई सिर्फ़ हमारी नहीं, आपकी भी है।",
         "हमारे साथ जुड़िए। अपने मोहल्ले में लोगों को मास्क बाँटिए, उन्हें जागरूक कीजिए।",
         "साँस लेना हमारा हक़ है। पॉल्यूशन पर सॉल्यूशन। एन एस यू आई के साथ आइए।"]
SUBS = ["दोस्तों... ये लड़ाई सिर्फ़ हमारी नहीं, आपकी भी है।", "हमारे साथ जुड़िए। अपने मोहल्ले में लोगों को मास्क बाँटिए, उन्हें जागरूक कीजिए।",
        "साँस लेना हमारा हक़ है। Pollution पर Solution... NSUI के साथ आइए।"]
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128", headers={"xi-api-key": os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")}, timeout=200,
    json={"text": " ".join(LINES), "model_id": os.environ.get("TTS_MODEL", "eleven_multilingual_v2"),
          "voice_settings": {"stability": 0.42, "similarity_boost": 0.85, "style": 0.35, "use_speaker_boost": True}})
r.raise_for_status(); open(f"{D}/outro.mp3", "wb").write(r.content)
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{D}/outro.mp3"], capture_output=True, text=True).stdout)
n = sum(len(x) for x in SUBS); c = 0.0; subs = []
for x in SUBS: dd = d * len(x) / n; subs.append({"text": x, "start": c, "end": c + dd}); c += dd
json.dump({"duration": d, "subs": subs}, open(f"{D}/outro.json", "w"), ensure_ascii=False); print("outro", round(d, 1), "s")
