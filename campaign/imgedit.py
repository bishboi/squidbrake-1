"""Image generation with reference images (Gemini image via OpenRouter).
Usage: OPENROUTER_API_KEY=... python3 imgedit.py <out.png> <aspect> "<prompt>" <ref1> [<ref2> ...]"""
import os, sys, io, base64, requests
from PIL import Image
def edit(out, aspect, prompt, refs, size="2K"):
    content = [{"type": "text", "text": prompt}]
    for r in refs:
        im = Image.open(r).convert("RGB"); im.thumbnail((2048, 2048)); b = io.BytesIO(); im.save(b, "PNG")
        content.append({"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()}})
    for attempt in range(4):
        try:
            j = requests.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]}, timeout=400,
                json={"model": os.environ.get("IMG_MODEL", "google/gemini-3-pro-image"), "modalities": ["image", "text"],
                      "image_config": {"aspect_ratio": aspect, "image_size": size}, "messages": [{"role": "user", "content": content}]}).json()
            u = j["choices"][0]["message"]["images"][0]["image_url"]["url"]; open(out, "wb").write(base64.b64decode(u.split(",", 1)[1])); print("wrote", out, flush=True); return True
        except Exception as e: print("retry", out, str(e)[:300], flush=True)
    return False
if __name__ == "__main__": edit(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
