"""Generate the skit's stills, dialogue clips and transcripts. Usage: OPENROUTER_API_KEY=... python3 skit_gen.py <dir>"""
import os, sys, io, json, time, base64, subprocess, requests
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from imgedit import edit
B = __import__("importlib").import_module(os.environ.get("SKIT", "beats_skit"))
D = sys.argv[1]; API = "https://openrouter.ai/api/v1"; H = {"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]}
os.environ.setdefault("IMG_MODEL", "google/gemini-3-pro-image")

def clip(s):
    still = f"{D}/still_{s['id']}.png"; out = f"{D}/clip_{s['id']}.mp4"
    if not os.path.exists(still): edit(still, "16:9", ("" if s.get("nolook") else B.LOOK) + s["still"], [f"{D}/{r}.png" for r in s["refs"]] + ([f"{D}/hero.png"] if os.path.exists(f"{D}/hero.png") else []))
    if os.environ.get("STILLS_ONLY"): return
    if not os.path.exists(out):
        im = Image.open(still).convert("RGB").resize((1920, 1080), Image.LANCZOS); b = io.BytesIO(); im.save(b, "JPEG", quality=92)
        body = {"model": os.environ.get("VIDEO_MODEL", "google/gemini-omni-1.2-flash"), "prompt": B.RULES + (B.VOICES if s["lines"] else "") + s["action"], "duration": min(s["dur"], int(os.environ.get("MAX_DUR", 99))), "resolution": os.environ.get("VIDEO_RES", "1080p"),
                "aspect_ratio": "16:9", "generate_audio": True, "frame_images": [{"type": "image_url", "frame_type": "first_frame",
                "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()}}]}
        for attempt in range(int(os.environ.get("TRIES", 3))):
            try:
                j = requests.post(API + "/videos", headers=H, json=body, timeout=180).json()
                if "id" not in j: raise RuntimeError(str(j)[:300])
                for _ in range(120):
                    time.sleep(8); st = requests.get(f"{API}/videos/{j['id']}", headers=H, timeout=60).json()
                    if st.get("status") in ("completed", "failed", "cancelled", "expired"): break
                if st.get("status") != "completed": raise RuntimeError(str(st)[:300])
                r = requests.get(f"{API}/videos/{j['id']}/content?index=0", headers=H, timeout=300); r.raise_for_status(); open(out, "wb").write(r.content); break
            except Exception as e: print("retry clip", s["id"], attempt + 1, str(e)[:80], flush=True)
    tj = f"{D}/tr_{s['id']}.json"
    if os.path.exists(out) and not os.path.exists(tj):   # what was actually said, with timings, for subtitles and checking
        wav = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", out, "-ac", "1", "-ar", "16000", "-f", "wav", "-"], capture_output=True).stdout
        for attempt in range(3):
            try:
                j = requests.post(API + "/chat/completions", headers=H, timeout=200, json={"model": "google/gemini-3.8-flash", "messages": [{"role": "user", "content": [
                    {"type": "text", "text": "Transcribe every spoken line in this audio (Hindi in Devanagari; keep English words in Latin). Return ONLY a JSON array of objects {\"start\": seconds, \"end\": seconds, \"text\": ...}, one per spoken line. If there is no speech return []."},
                    {"type": "input_audio", "input_audio": {"data": base64.b64encode(wav).decode(), "format": "wav"}}]}]}).json()
                t = j["choices"][0]["message"]["content"]; tr = json.loads(t[t.find("["):t.rfind("]") + 1]); json.dump(tr, open(tj, "w"), ensure_ascii=False); break
            except Exception as e: print("retry transcript", s["id"], str(e)[:200], flush=True)
    if os.path.exists(tj):
        tr = json.load(open(tj)); print(s["id"], "OK" if len(tr) == len(s["lines"]) else f"MISMATCH want {len(s['lines'])}", [(round(x["start"], 1), round(x["end"], 1), x["text"]) for x in tr], flush=True)

ONLY = os.environ.get("ONLY")
with ThreadPoolExecutor(6) as ex: list(ex.map(clip, [s for s in B.SCENES if not ONLY or s["id"] in ONLY.split(",")]))
