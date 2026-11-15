"""Generate voice-over (gpt-audio), images (Gemini image) and score (Lyria) through OpenRouter.
Usage: OPENROUTER_API_KEY=... python3 gen_assets.py <outdir> [vo|img|music ...]"""
import os, sys, json, base64, subprocess, requests
from concurrent.futures import ThreadPoolExecutor
from beats import BEATS, STYLE, WARM
K = os.environ["OPENROUTER_API_KEY"]; OUT = sys.argv[1]; WHAT = sys.argv[2:] or ["vo", "img", "music"]
URL = "https://openrouter.ai/api/v1/chat/completions"; H = {"Authorization": "Bearer " + K}
VOICE = os.environ.get("VO_VOICE", "onyx")
SYS = ("तुम एक अनुभवी हिंदी डॉक्यूमेंट्री वॉइस-ओवर आर्टिस्ट हो। You are the narrator of an emotional Hindi documentary film about "
       "air pollution in Delhi. Read the user's line EXACTLY as written — do not add, drop, translate or answer anything. "
       "Voice: deep, warm, grave, intimate; slow measured pace; real pain and restraint, like a film trailer narrator. "
       "Treat every '...' as a long dramatic pause. Natural Hindustani pronunciation. Tone for this line: {tone}")
os.makedirs(OUT, exist_ok=True)

def stream_audio(body):
    r = requests.post(URL, headers=H, json=body, stream=True, timeout=900); aud = b""; txt = ""
    for line in r.iter_lines():
        if not line.startswith(b"data: "): continue
        d = line[6:]
        if d == b"[DONE]": break
        j = json.loads(d)
        if "error" in j: raise RuntimeError(j["error"])
        for c in j.get("choices", []):
            a = c.get("delta", {}).get("audio") or {}
            if a.get("data"): aud += base64.b64decode(a["data"])
            if a.get("transcript"): txt += a["transcript"]
    return aud, txt

def tone(b):
    i = b["id"][0]
    return {"a": "wistful, nostalgic, then heavy", "b": "tender and heartbroken", "c": "tender and heartbroken",
            "d": "soft, aching compassion", "e": "quiet respect and sorrow", "f": "controlled anger, bitter irony",
            "g": "weary, defeated", "h": "intimate, pleading, the emotional peak",
            "i": "rising, resolute, powerful, a call to action"}[i]

def vo(b):
    p = f"{OUT}/vo_{b['id']}.wav"
    if os.path.exists(p): return
    for attempt in range(4):
        try:
            aud, txt = stream_audio({"model": "openai/gpt-audio", "modalities": ["text", "audio"], "stream": True,
                "audio": {"voice": VOICE, "format": "pcm16"},
                "messages": [{"role": "system", "content": SYS.format(tone=tone(b))}, {"role": "user", "content": b["vo"]}]})
            if len(aud) < 24000: raise RuntimeError("short")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "-", p], input=aud, check=True)
            json.dump({"said": txt, "want": b["vo"]}, open(p + ".json", "w"), ensure_ascii=False)
            print("vo", b["id"], round(len(aud) / 48000, 1), "OK" if txt.strip() == b["vo"].strip() else "DIFF: " + txt, flush=True); return
        except Exception as e: print("retry vo", b["id"], e, flush=True)

def img(args):
    b, n, prompt = args; p = f"{OUT}/img_{b['id']}_{n}.png"
    if os.path.exists(p): return
    for attempt in range(4):
        try:
            j = requests.post(URL, headers=H, timeout=400, json={"model": "google/gemini-3.1-flash-image", "modalities": ["image", "text"],
                "image_config": {"aspect_ratio": "16:9", "image_size": "2K"},
                "messages": [{"role": "user", "content": prompt + (WARM if b.get("warm") else STYLE)}]}).json()
            u = j["choices"][0]["message"]["images"][0]["image_url"]["url"]
            open(p, "wb").write(base64.b64decode(u.split(",", 1)[1])); print("img", p, flush=True); return
        except Exception as e: print("retry img", b["id"], n, str(e)[:200], flush=True)

jobs = []
with ThreadPoolExecutor(10) as ex:
    if "vo" in WHAT: jobs += [ex.submit(vo, b) for b in BEATS]
    if "img" in WHAT: jobs += [ex.submit(img, (b, n, p)) for b in BEATS for n, p in enumerate(b["imgs"])]
    for j in jobs: j.result()
