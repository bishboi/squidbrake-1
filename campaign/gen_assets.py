"""Generate narration (gpt-audio), stills (Gemini image) and video shots (Gemini Omni) through OpenRouter.
Usage: OPENROUTER_API_KEY=... python3 gen_assets.py <assets_dir> vo|stills|videos ..."""
import os, sys, io, json, time, math, base64, subprocess, requests
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from timeline import M
BEATS, MOTION = M.BEATS, M.MOTION
K = os.environ["OPENROUTER_API_KEY"]; OUT = sys.argv[1]; WHAT = sys.argv[2:]
API = "https://openrouter.ai/api/v1"; H = {"Authorization": "Bearer " + K}
VOICE = os.environ.get("VO_VOICE", getattr(M, "VOICE", "onyx")); VMODEL = os.environ.get("VIDEO_MODEL", "google/gemini-omni-1.2-flash")
SYS0 = ("You are the narrator of an emotional Hindi documentary film about pollution in Delhi. Read the user's line EXACTLY as "
       "written, in Hindi — do not add, drop, translate or answer anything. Voice: deep, warm, grave and intimate, like a film "
       "trailer narrator; measured pace, not slow; real feeling and restraint. Treat '...' as a short dramatic pause. "
       "Natural Hindustani pronunciation. Tone for this line: {tone}")
TONE0 = {"a": "wistful, then heavy and factual", "b": "tender and heartbroken", "c": "tender and heartbroken", "d": "soft, aching compassion",
        "y": "grief turning to quiet anger", "m": "bitter, ironic", "p": "cold, controlled anger, direct", "s": "cold, bitter irony", "f": "controlled anger",
        "g": "weary, defeated", "h": "intimate, pleading, the emotional peak", "i": "rising, resolute, powerful, a call to action"}
SYS = getattr(M, "VO_SYS", SYS0); TONE = getattr(M, "TONE", TONE0)
os.makedirs(OUT, exist_ok=True)

def vo(b):
    p = f"{OUT}/vo_{b['id']}.wav"
    if os.path.exists(p): return
    for attempt in range(4):
        try:
            r = requests.post(API + "/chat/completions", headers=H, stream=True, timeout=600, json={"model": "openai/gpt-audio",
                "modalities": ["text", "audio"], "stream": True, "audio": {"voice": VOICE, "format": "pcm16"},
                "messages": [{"role": "system", "content": SYS.format(tone=TONE[b["id"][0]])}, {"role": "user", "content": b["vo"]}]})
            aud = b""; txt = ""
            for line in r.iter_lines():
                if not line.startswith(b"data: ") or line[6:] == b"[DONE]": continue
                j = json.loads(line[6:])
                if "error" in j: raise RuntimeError(j["error"])
                for c in j.get("choices", []):
                    a = c.get("delta", {}).get("audio") or {}
                    if a.get("data"): aud += base64.b64decode(a["data"])
                    txt += a.get("transcript") or ""
            if len(aud) < 24000: raise RuntimeError("short")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "-", p], input=aud, check=True)
            print("vo", b["id"], round(len(aud) / 48000, 1), "|", txt, flush=True); return
        except Exception as e: print("retry vo", b["id"], e, flush=True)

def still(s):
    sid, prompt, _ = s; p = f"{OUT}/still_{sid}.png"
    if os.path.exists(p) or not prompt or prompt == "x": return
    for attempt in range(4):
        try:
            j = requests.post(API + "/chat/completions", headers=H, timeout=400, json={"model": "google/gemini-3.1-flash-image",
                "modalities": ["image", "text"], "image_config": {"aspect_ratio": "16:9", "image_size": "2K"},
                "messages": [{"role": "user", "content": prompt}]}).json()
            u = j["choices"][0]["message"]["images"][0]["image_url"]["url"]
            open(p, "wb").write(base64.b64decode(u.split(",", 1)[1])); print("still", sid, flush=True); return
        except Exception as e: print("retry still", sid, str(e)[:200], flush=True)

def video(s):
    p = f"{OUT}/clip_{s['id']}.mp4"
    if os.path.exists(p) or s.get("reuse"): return
    def frame(sid, kind):
        im = Image.open(f"{OUT}/still_{sid}.png").convert("RGB").resize((1920, 1080), Image.LANCZOS); buf = io.BytesIO(); im.save(buf, "JPEG", quality=92)
        return {"type": "image_url", "frame_type": kind, "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()}}
    frames = [frame(s["first"], "first_frame")] + ([frame(s["last"], "last_frame")] if s.get("last") else [])
    body = {"model": VMODEL, "prompt": s["motion"] + MOTION, "duration": int(min(15, max(4, math.ceil(s["need"] + 0.3)))), "resolution": "1080p",
            "aspect_ratio": "16:9", "generate_audio": True, "frame_images": frames}
    for attempt in range(3):
        try:
            j = requests.post(API + "/videos", headers=H, json=body, timeout=180).json()
            if "id" not in j: raise RuntimeError(str(j)[:300])
            for _ in range(120):
                time.sleep(8); st = requests.get(f"{API}/videos/{j['id']}", headers=H, timeout=60).json()
                if st.get("status") in ("completed", "failed", "cancelled", "expired"): break
            if st.get("status") != "completed": raise RuntimeError(str(st)[:300])
            r = requests.get(f"{API}/videos/{j['id']}/content?index=0", headers=H, timeout=300); r.raise_for_status()
            open(p, "wb").write(r.content); print("clip", s["id"], body["duration"], "s", flush=True); return
        except Exception as e: print("retry clip", s["id"], str(e)[:300], flush=True)

with ThreadPoolExecutor(8) as ex:
    if "vo" in WHAT: list(ex.map(vo, BEATS))
    if "stills" in WHAT and hasattr(M, "STILLS"):   # stills made from reference images
        from imgedit import edit
        here = os.path.dirname(os.path.abspath(__file__)); os.environ.setdefault("IMG_MODEL", "google/gemini-3.1-flash-image")
        ref = lambda r: f"{here}/brand/{r[6:]}.png" if r.startswith("BRAND:") else f"{OUT}/still_{r}.png"
        list(ex.map(lambda kv: os.path.exists(f"{OUT}/still_{kv[0]}.png") or edit(f"{OUT}/still_{kv[0]}.png", "16:9", kv[1][0], [ref(r) for r in kv[1][1]]), M.STILLS.items()))
    elif "stills" in WHAT: list(ex.map(still, [s for b in BEATS for s in b["shots"]]))
    if "videos" in WHAT:
        from timeline import build
        shots, caps, total = build(OUT); print(f"film {total:.1f}s, footage {sum(s['need'] for s in shots):.0f}s", flush=True)
        list(ex.map(video, shots))
