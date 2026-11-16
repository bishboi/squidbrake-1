"""Re-voice scripted lines into cloned/stock ElevenLabs voices (speech-to-speech), keeping the generated lip-sync and timing.
For each clip: ElevenLabs Scribe gives word times; the words are matched in order against the script lines (fuzzy, ad-libs ignored), which gives
each line its true start/end -> tr_<scene>.json (used for subtitles and trims). Each line spoken by someone in VOICES is converted, cut so it
never overlaps a neighbouring word, and saved as vs_<scene>_<line>.mp3/.json (spliced in by skit.py).
Usage: python3 voice_swap.py <clips_dir> <lead_voice_id>      (key is injected by the network proxy)"""
import os, sys, json, re, unicodedata, subprocess, difflib, requests
import beats_skit as B
D, LEAD_VOICE = sys.argv[1], sys.argv[2]; CM_VOICE = os.environ.get("CM_VOICE", "ThT5KcBeYPX3keUQqHPh"); CM_PITCH = float(os.environ.get("CM_PITCH", "-1.5"))   # a deeper, warmer female voice for the invented Chief Minister
VOICES = {"कबीर": LEAD_VOICE, "मुख्यमंत्री": CM_VOICE}; H = {"xi-api-key": os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")}
dur = lambda p: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
ALIAS = {"पॉल्यूशन": "pollution", "स्विट्जरलैंड": "switzerland", "मैडम": "madam", "अंकल": "uncle"}
def norm(t):
    x = "".join(c for c in unicodedata.normalize("NFC", t).replace("\u093c", "").replace("\u0901", "\u0902").lower() if unicodedata.category(c)[0] not in "PSZC"); return ALIAS.get(x, x)
def toks(t): return [x for x in (norm(w) for w in t.split()) if x]

def scribe(sid):
    cache = f"{D}/scribe_{sid}.json"
    if os.path.exists(cache): return json.load(open(cache))
    wav = f"{D}/_a.wav"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{D}/clip_{sid}.mp4", "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", headers=H, timeout=300, files={"file": open(wav, "rb")}, data={"model_id": "scribe_v1", "timestamps_granularity": "word", "language_code": "hin"})
    r.raise_for_status(); words = [w for w in r.json()["words"] if w.get("type") == "word" and norm(w["text"])]; json.dump(words, open(cache, "w"), ensure_ascii=False); return words

def align(lines, words):
    """global alignment of script tokens to Scribe words; returns {line: (first_word_idx, last_word_idx)}"""
    S = [(i, t) for i, (_, txt) in enumerate(lines) for t in toks(txt)]; W = [norm(w["text"]) for w in words]; n, m = len(S), len(W)
    sim = lambda a, b: difflib.SequenceMatcher(None, a, b).ratio()
    sc = [[0.0] * (m + 1) for _ in range(n + 1)]; bk = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1): sc[i][0] = sc[i - 1][0] - 0.4; bk[i][0] = "u"
    for j in range(1, m + 1): sc[0][j] = sc[0][j - 1] - 0.1; bk[0][j] = "l"
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = sim(S[i - 1][1], W[j - 1]); opts = [(sc[i - 1][j - 1] + (s * 2 if s >= 0.6 else -1.0), "d"), (sc[i - 1][j] - 0.4, "u"), (sc[i][j - 1] - 0.1, "l")]
            sc[i][j], bk[i][j] = max(opts)
    i, j, hit = n, m, {}
    while i > 0 or j > 0:
        b = bk[i][j]
        if b == "d":
            if sim(S[i - 1][1], W[j - 1]) >= 0.6: lo, hi = hit.get(S[i - 1][0], (j - 1, j - 1)); hit[S[i - 1][0]] = (min(lo, j - 1), max(hi, j - 1))
            i, j = i - 1, j - 1
        elif b == "u": i -= 1
        else: j -= 1
    return hit

def deepen(path):
    """lower the pitch by CM_PITCH semitones (duration unchanged) and add a little warmth"""
    f = 2 ** (CM_PITCH / 12); tmp = path + ".d.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-af", f"asetrate=44100*{f:.4f},aresample=44100,atempo={1 / f:.4f},equalizer=f=180:width_type=o:width=1.5:g=3", "-b:a", "128k", tmp], check=True); os.replace(tmp, path)

def clean(path, t0):
    """trim the converted line to its words (+ a short tail) and turn down breaths / stray sounds in the pauses; returns the new start time"""
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", headers=H, timeout=200, files={"file": open(path, "rb")}, data={"model_id": "scribe_v1", "timestamps_granularity": "word", "language_code": "hin"})
    if r.status_code != 200: return t0
    w = [x for x in r.json().get("words", []) if x.get("type") == "word" and norm(x["text"])]
    if not w: return t0
    head = max(0.0, w[0]["start"] - 0.06); stop = w[-1]["end"] + 0.14; af = []
    for a, b in zip(w, w[1:]):
        if b["start"] - a["end"] > 0.28: af.append(f"volume=enable='between(t,{a['end'] + 0.07 - head:.2f},{b['start'] - 0.07 - head:.2f})':volume=0.06")
    af += ["afade=t=in:d=0.02", f"afade=t=out:st={max(0.0, stop - head - 0.1):.2f}:d=0.1"]
    tmp = path + ".tmp.mp3"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{head:.2f}", "-t", f"{stop - head:.2f}", "-i", path, "-af", ",".join(af), "-b:a", "128k", tmp], check=True)
    os.replace(tmp, path); return t0 + head

for s in B.SCENES:
    if not s["lines"]: continue
    sid = s["id"]; words = scribe(sid); hit = align(s["lines"], words); total = dur(f"{D}/clip_{sid}.mp4"); tr = []
    for i, (who, txt) in enumerate(s["lines"]):
        need = len(toks(txt))
        if i not in hit: print(f"NO MATCH {sid}[{i}] {who}", flush=True); tr.append({"start": (tr[-1]["end"] + 0.2) if tr else 0.0, "end": (tr[-1]["end"] + 1.5) if tr else 1.5, "text": ""}); continue
        a, b = hit[i]; tr.append({"start": words[a]["start"], "end": words[b]["end"], "text": ""})
        out = f"{D}/vs_{sid}_{i}.mp3"
        if who not in VOICES or os.path.exists(out): continue
        t0 = max(words[a]["start"] - 0.12, (words[a - 1]["end"] + 0.02) if a > 0 else 0.0)
        t1 = min(words[b]["end"] + 0.45, (words[b + 1]["start"] - 0.03) if b + 1 < len(words) else total)
        wav = f"{D}/_seg.wav"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{D}/clip_{sid}.mp4", "-ss", f"{t0:.2f}", "-t", f"{t1 - t0:.2f}", "-vn", "-ac", "1", "-ar", "44100", wav], check=True)
        iso = requests.post("https://api.elevenlabs.io/v1/audio-isolation", headers=H, timeout=300, files={"audio": open(wav, "rb")})   # strip street noise / ambience from the source first
        if iso.status_code == 200:
            open(f"{D}/_iso.mp3", "wb").write(iso.content); subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{D}/_iso.mp3", "-ac", "1", "-ar", "44100", wav], check=True)
        r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{VOICES[who]}?output_format=mp3_44100_128", headers=H, timeout=300, files={"audio": open(wav, "rb")},
            data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "true", "voice_settings": json.dumps({"stability": 0.5, "similarity_boost": 0.85, "style": 0.0, "use_speaker_boost": True})})
        if r.status_code != 200: sys.exit(f"{sid}[{i}] {r.status_code} {r.text[:300]}")
        open(out, "wb").write(r.content); t0 = clean(out, t0)
        if who == "मुख्यमंत्री": deepen(out)
        json.dump({"start": t0, "end": t1}, open(f"{D}/vs_{sid}_{i}.json", "w")); print("swapped", sid, i, who, f"{t0:.1f}-{t1:.1f}", flush=True)
    json.dump(tr, open(f"{D}/tr_{sid}.json", "w"), ensure_ascii=False)
    lastb = max((hit[i][1] for i in hit), default=None)   # first word after the last scripted line = start of any ad-lib; the scene is cut before it
    json.dump({"next_start": (words[lastb + 1]["start"] if lastb is not None and lastb + 1 < len(words) else None)}, open(f"{D}/nxt_{sid}.json", "w"))
