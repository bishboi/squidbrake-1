"""Re-voice the lead's lines with an ElevenLabs voice (speech-to-speech), keeping the generated lip-sync and timing.
Step 1 (align): ElevenLabs Scribe gives word times + speaker labels for each clip; speaker turns are matched in order to the
script's lines, which also rewrites tr_<scene>.json (line start/end) so subtitles and trims use true timings.
Step 2 (convert): each of the lead's turns is converted to the target voice -> vs_<scene>_<k>.mp3/.json, spliced in by skit.py.
Usage: python3 voice_swap.py <clips_dir> <voice_id>   (key is injected by the network proxy; STUB=1 skips the conversion)"""
import os, sys, json, subprocess, requests
import beats_skit as B
D, VOICE = sys.argv[1], sys.argv[2]; CM_VOICE = os.environ.get("CM_VOICE", "XrExE9yKIg1WjnnlVkGX")   # stock female voice for the invented CM
VOICES = {"कबीर": VOICE, "मुख्यमंत्री": CM_VOICE}; KEY = os.environ.get("ELEVENLABS_API_KEY", "proxy-injected"); H = {"xi-api-key": KEY}
dur = lambda p: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

def scribe(sid):
    cache = f"{D}/scribe_{sid}.json"
    if os.path.exists(cache): return json.load(open(cache))
    wav = f"{D}/_a.wav"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{D}/clip_{sid}.mp4", "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", headers=H, timeout=300, files={"file": open(wav, "rb")},
                      data={"model_id": "scribe_v1", "diarize": "true", "timestamps_granularity": "word", "language_code": "hin"})
    r.raise_for_status(); words = [w for w in r.json()["words"] if w.get("type") == "word"]; json.dump(words, open(cache, "w"), ensure_ascii=False); return words

def turns(words, clean=False):
    out = []
    for w in words:
        if out and out[-1]["spk"] == w["speaker_id"]: out[-1]["end"] = w["end"]; out[-1]["n"] += 1
        else: out.append(dict(spk=w["speaker_id"], start=w["start"], end=w["end"], n=1))
    if clean:   # drop one-word diarization glitches, then re-merge
        keep = [t for t in out if not (t["n"] <= 1 and t["end"] - t["start"] < 0.5)]; out = []
        for t in keep:
            if out and out[-1]["spk"] == t["spk"]: out[-1]["end"] = t["end"]; out[-1]["n"] += t["n"]
            else: out.append(dict(t))
    return out

for s in B.SCENES:
    if not s["lines"]: continue
    sid = s["id"]; groups = []                       # consecutive lines by the same speaker form one group
    for i, (who, text) in enumerate(s["lines"]):
        if groups and groups[-1]["who"] == who: groups[-1]["idx"].append(i)
        else: groups.append(dict(who=who, idx=[i]))
    words = scribe(sid); T = None
    for clean in (False, True):                      # exact match, else drop trailing ad-lib turns
        c = turns(words, clean)
        if len(c) == len(groups) or (len(c) > len(groups) and c[len(groups) - 1]["end"] < words[-1]["start"] + 0.01 and True):
            T = c[:len(groups)]; break
    if T is None and len(turns(words)) < len(groups):  # diarizer merged different speakers: split at the biggest pauses
        gaps = sorted(range(1, len(words)), key=lambda i: words[i]["start"] - words[i - 1]["end"], reverse=True)[:len(groups) - 1]; cut = [0] + sorted(gaps) + [len(words)]
        T = [dict(spk=str(k), start=words[a]["start"], end=words[b - 1]["end"], n=b - a) for k, (a, b) in enumerate(zip(cut, cut[1:]))]
    if T is None: print(f"ALIGN FAIL {sid}: script has {len(groups)} turns, audio has {len(turns(words))}", flush=True); continue
    total = dur(f"{D}/clip_{sid}.mp4"); tr = [None] * len(s["lines"])
    for g, t in zip(groups, T):
        n = sum(len(s["lines"][i][1]) for i in g["idx"]); c = t["start"]
        for i in g["idx"]:
            d = (t["end"] - t["start"]) * len(s["lines"][i][1]) / n; tr[i] = {"start": c, "end": c + d, "text": ""}; c += d
    json.dump(tr, open(f"{D}/tr_{sid}.json", "w"), ensure_ascii=False)
    for k, (g, t) in enumerate(zip(groups, T)):
        out = f"{D}/vs_{sid}_{k}.mp3"
        if g["who"] not in VOICES or os.path.exists(out): continue
        a = max(t["start"] - 0.12, (T[k - 1]["end"] + 0.03) if k else 0.0); b = min(t["end"] + 0.30, (T[k + 1]["start"] - 0.03) if k + 1 < len(T) else total)
        wav = f"{D}/_seg.wav"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{D}/clip_{sid}.mp4", "-ss", f"{a:.2f}", "-t", f"{b - a:.2f}", "-vn", "-ac", "1", "-ar", "44100", wav], check=True)
        if os.environ.get("STUB"): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, out], check=True)
        else:
            r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{VOICES[g['who']]}?output_format=mp3_44100_128", headers=H, timeout=300, files={"audio": open(wav, "rb")},
                data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "true",
                      "voice_settings": json.dumps({"stability": 0.5, "similarity_boost": 0.85, "style": 0.0, "use_speaker_boost": True})})
            if r.status_code != 200: sys.exit(f"{sid}[{k}] {r.status_code} {r.text[:300]}")
            open(out, "wb").write(r.content)
        json.dump({"start": a, "end": b}, open(f"{D}/vs_{sid}_{k}.json", "w")); print("swapped", sid, k, f"{a:.1f}-{b:.1f}", flush=True)
