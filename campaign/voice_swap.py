"""Re-voice the lead's lines with an ElevenLabs voice (speech-to-speech), keeping the generated lip-sync and timing.
Usage: python3 voice_swap.py <clips_dir> <voice_id>      (key is injected by the network proxy; STUB=1 skips the API)
Writes <clips_dir>/vs_<scene>_<line>.mp3 + vs_<scene>_<line>.json (start/end); skit.py splices them in automatically."""
import os, sys, json, subprocess, requests
import beats_skit as B
D, VOICE = sys.argv[1], sys.argv[2]; LEAD = "कबीर"; PAD = (0.05, 0.15)
KEY = os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")
for s in B.SCENES:
    tj = f"{D}/tr_{s['id']}.json"
    if not os.path.exists(tj): continue
    tr = json.load(open(tj))
    for i, (who, _) in enumerate(s["lines"]):
        out = f"{D}/vs_{s['id']}_{i}.mp3"
        if who != LEAD or i >= len(tr) or os.path.exists(out): continue
        a = max(0.0, tr[i]["start"] - PAD[0]); b = tr[i]["end"] + PAD[1]; wav = f"{D}/_seg.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{D}/clip_{s['id']}.mp4", "-ss", f"{a:.2f}", "-t", f"{b - a:.2f}", "-vn", "-ac", "1", "-ar", "44100", wav], check=True)
        if os.environ.get("STUB"): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, out], check=True)
        else:
            r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{VOICE}?output_format=mp3_44100_128", headers={"xi-api-key": KEY}, timeout=300,
                files={"audio": open(wav, "rb")}, data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "true",
                "voice_settings": json.dumps({"stability": 0.5, "similarity_boost": 0.85, "style": 0.0, "use_speaker_boost": True})})
            if r.status_code != 200: sys.exit(f"{s['id']}[{i}] {r.status_code} {r.text[:300]}")
            open(out, "wb").write(r.content)
        json.dump({"start": a, "end": b}, open(f"{D}/vs_{s['id']}_{i}.json", "w")); print("swapped", s["id"], i, round(b - a, 1), flush=True)
