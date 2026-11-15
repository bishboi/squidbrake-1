"""Assemble the film from generated assets.
Usage: python3 render.py <assets_dir> <music.mp3> <out.mp4>"""
import os, sys, re, subprocess, wave, math
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from beats import BEATS
A, MUSIC, OUT = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__)); TMP = os.path.join(A, "_render"); os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1920, 1080, 25
LEAD, GAP, XF, TAIL, TEMPO = 1.2, 0.3, 0.7, 5.0, 1.12
F = lambda n, s: ImageFont.truetype(f"{HERE}/fonts/{n}.ttf", s)
CAP, BIG, SER, LAT = "NotoSansDevanagari-Medium", "NotoSansDevanagari-ExtraBold", "NotoSerifDevanagari-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
beats = [b for b in BEATS if not b.get("skip")]

def dur(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()

def prep_vo():
    for b in beats:
        o = f"{TMP}/vo_{b['id']}.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{A}/vo_{b['id']}.wav", "-af",
            "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
            "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
            "silenceremove=stop_periods=-1:stop_duration=0.45:stop_threshold=-42dB:stop_silence=0.4,"
            f"atempo={TEMPO},loudnorm=I=-17:TP=-2:LRA=9,aresample=48000", "-ac", "1", o], check=True)
        b["d"] = dur(o)

def timeline():
    t = LEAD; shots = []; caps = []
    for b in beats:
        b["t0"] = t; span = b["d"] + GAP + (TAIL if b.get("end") else 0); n = len(b["imgs"])
        for i in range(n):
            shots.append(dict(img=f"{A}/img_{b['id']}_{i}.png", t0=t + span * i / n, t1=t + span * (i + 1) / n, k=len(shots)))
        text = b.get("cap", b["vo"])
        parts = [p.strip(" —") for p in re.split(r"\.\.\.|(?<=[।?])|—", text) if p.strip(" —")]
        merged = []
        for p in parts:  # merge tiny fragments so captions don't flicker
            if merged and len(merged[-1]) + len(p) < 34: merged[-1] += " … " + p if not merged[-1].endswith(("।", "?")) else " " + p
            else: merged.append(p)
        tot = sum(len(m) for m in merged); c = t
        if not b.get("end"):
            for m in merged:
                d = b["d"] * len(m) / tot; caps.append(dict(text=m, t0=c, t1=c + d)); c += d
        b["t1"] = t + span; t += span
    shots[0]["t0"] = 0
    return shots, caps, t

def runs(text, font):
    """split into Devanagari / other runs — the Devanagari fonts carry no Latin glyphs or digits"""
    lat = ImageFont.truetype(LAT, int(font.size * 0.86)); out = []
    for ch in text:
        f = font if ("\u0900" <= ch <= "\u097f" or ch == " ") else lat
        if out and out[-1][1] is f: out[-1][0] += ch
        else: out.append([ch, f])
    return out

def mlen(d, text, font): return sum(d.textlength(t, font=f) for t, f in runs(text, font))

def mtext(d, cx, y, text, font, fill):
    x = cx - mlen(d, text, font) / 2; base = y + font.getmetrics()[0]
    for t, f in runs(text, font): d.text((x, base), t, font=f, fill=fill, anchor="ls"); x += d.textlength(t, font=f)

def text_layer(lines, y=None, shadow=True):
    """lines: [(text, font, fill)] centred; returns RGBA layer"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    hs = [int(f.size * 1.45) for t, f, _ in lines]; yy = y if y is not None else (H - sum(hs)) // 2
    if shadow:
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh); y2 = yy
        for (t, f, _), h in zip(lines, hs): mtext(ds, W // 2, y2, t, f, (0, 0, 0, 235)); y2 += h
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(7))); im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(3)))
        d = ImageDraw.Draw(im)
    for (t, f, c), h in zip(lines, hs): mtext(d, W // 2, yy, t, f, c); yy += h
    return im

def wrap(text, font, maxw):
    d = ImageDraw.Draw(Image.new("L", (8, 8))); out = []; cur = ""
    for w in text.split():
        if mlen(d, (cur + " " + w).strip(), font) > maxw and cur: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return out + [cur]

def static_overlay():
    """letterbox bars + vignette + disclaimer tag, one RGBA image"""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = Image.new("L", (W // 8, H // 8)); p = px.load()
    for y in range(H // 8):
        for x in range(W // 8):
            r = math.hypot((x - W / 16) / (W / 16), (y - H / 16) / (H / 16)); p[x, y] = int(min(1, max(0, r - 0.55) / 0.85) * 190)
    ov.putalpha(px.resize((W, H), Image.BICUBIC)); d = ImageDraw.Draw(ov)
    d.rectangle([0, 0, W, 64], fill=(0, 0, 0, 255)); d.rectangle([0, H - 64, W, H], fill=(0, 0, 0, 255))
    mtext(d, W - 230, 16, "सांकेतिक दृश्य  |  AI-निर्मित चित्र", F(CAP, 22), (255, 255, 255, 130))
    return ov

def fade(t, t0, t1, fi=0.35, fo=0.35):
    if t < t0 or t > t1: return 0.0
    return max(0.0, min(1.0, (t - t0) / fi, (t1 - t) / fo))

def with_alpha(layer, a):
    if a >= 0.999: return layer
    l = layer.copy(); l.putalpha(l.getchannel("A").point(lambda v: int(v * a))); return l

def shot_frame(s, src, t):
    """Ken Burns: slow push/pull with drift, eased"""
    span = s["t1"] - s["t0"] + XF; u = min(1, max(0, (t - s["t0"] + XF / 2) / span)); u = u * u * (3 - 2 * u) * 0.5 + u * 0.5
    k = s["k"]; z0, z1 = (1.0, 1.13) if k % 2 == 0 else (1.13, 1.0); z = z0 + (z1 - z0) * u
    dx = (0.5 - u) * 0.035 * (1 if k % 3 else -1); dy = (u - 0.5) * 0.02 * (1 if k % 4 < 2 else -1)
    sw, sh = src.size; cw, ch = sw / z, sh / z; cx, cy = sw * (0.5 + dx), sh * (0.5 + dy)
    x0 = min(max(0, cx - cw / 2), sw - cw); y0 = min(max(0, cy - ch / 2), sh - ch)
    return src.transform((W, H), Image.AFFINE, (cw / W, 0, x0, 0, ch / H, y0), Image.BICUBIC)

def render_chunk(args):
    ci, f0, f1, shots, caps, total, titles = args
    ov = static_overlay(); cache = {}; capl = {}; out = f"{TMP}/chunk{ci}.mp4"
    def src(s):
        if s["k"] not in cache:
            for k in [k for k in cache if k < s["k"] - 1]: del cache[k]
            cache[s["k"]] = Image.open(s["img"]).convert("RGB").resize((2496, 1404), Image.LANCZOS).crop((0, 0, 2496, 1404))
        return cache[s["k"]]
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-maxrate", "9M", "-bufsize", "18M", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        t = fi / FPS; cur = [s for s in shots if s["t0"] - XF / 2 <= t < s["t1"] + XF / 2]
        fr = shot_frame(cur[0], src(cur[0]), t)
        if len(cur) > 1:
            a = (t - (cur[1]["t0"] - XF / 2)) / XF; fr = Image.blend(fr, shot_frame(cur[1], src(cur[1]), t), max(0, min(1, a)))
        fr = fr.convert("RGBA"); fr.alpha_composite(ov)
        for tl in titles:
            a = fade(t, tl["t0"], tl["t1"], tl.get("fi", 0.6), tl.get("fo", 0.6))
            if a > 0: fr.alpha_composite(with_alpha(tl["layer"], a))
        for i, c in enumerate(caps):
            a = fade(t, c["t0"] - 0.1, c["t1"] + 0.1, 0.25, 0.25)
            if a > 0:
                if i not in capl:
                    f = F(CAP, 50); ls = wrap(c["text"], f, 1500); capl[i] = text_layer([(l, f, (255, 255, 255, 255)) for l in ls], y=H - 100 - 72 * len(ls))
                fr.alpha_composite(with_alpha(capl[i], a))
        g = min(1, t / 2.0, (total - t) / 2.5)  # global fade from / to black
        fr = fr.convert("RGB")
        if g < 1: fr = Image.blend(Image.new("RGB", (W, H)), fr, max(0, g))
        ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait(); return out

def make_titles(total):
    bt = {b["id"]: b for b in beats}; T = []
    red, wh = (255, 82, 64, 255), (255, 255, 255, 255)
    for b in beats:
        if b.get("title"):
            a, sub = b["title"]; lines = [(a, F(BIG, 150), wh)] + ([(sub, F(BIG, 64), red)] if sub else [])
            T.append(dict(layer=text_layer(lines, y=250 if sub else 300), t0=b["t0"] + b["d"] * 0.30, t1=b["t1"] - 0.2))
    e = bt["i3"]; dark = Image.new("RGBA", (W, H), (0, 0, 0, 150))
    T.append(dict(layer=dark, t0=e["t0"] + 0.2, t1=total + 1, fi=1.5))
    T.append(dict(layer=text_layer([("हक़ है साँस", F(SER, 210), wh), ("लेकर रहेंगे", F(BIG, 96), red)], y=235), t0=e["t0"] + 0.3, t1=total + 1, fi=1.0))
    T.append(dict(layer=text_layer([("#HaqHaiSaans   #SaansSatyagraha", F(CAP, 50), wh),
                                    ("NSUI  |  दिल्ली की हर साँस के लिए", F(BIG, 54), wh)], y=730), t0=e["t0"] + e["d"] + 0.8, t1=total + 1, fi=1.0))
    return T

if __name__ == "__main__":
    prep_vo(); shots, caps, total = timeline(); titles = make_titles(total); nf = int(total * FPS)
    print(f"duration {total:.1f}s, {len(shots)} shots, {len(caps)} captions", flush=True)
    if os.environ.get("PREVIEW"):   # dump a few stills for checking
        for tt in map(float, os.environ["PREVIEW"].split(",")):
            fn = int(tt * FPS); o = render_chunk((f"p{tt}", fn, fn + 1, shots, caps, total, titles))
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", o, "-frames:v", "1", f"{TMP}/prev_{tt}.jpg"])
        sys.exit()
    N = os.cpu_count(); edges = [nf * i // N for i in range(N + 1)]
    if os.environ.get("REUSE_VIDEO"): chunks = [f"{TMP}/chunk{i}.mp4" for i in range(N)]
    else:
      with Pool(N) as p: chunks = p.map(render_chunk, [(i, edges[i], edges[i + 1], shots, caps, total, titles) for i in range(N)])
    open(f"{TMP}/list.txt", "w").write("".join(f"file '{c}'\n" for c in chunks))
    # audio: narration placed on the timeline, score slowed to fit and ducked under the voice
    ins = []; fl = []
    for i, b in enumerate(beats):
        ins += ["-i", f"{TMP}/vo_{b['id']}.wav"]; fl.append(f"[{i}:a]adelay={int(b['t0'] * 1000)}:all=1[v{i}]")
    n = len(beats); mt = max(0.5, min(1.0, 177.3 / (total + 0.5)))
    fl.append("".join(f"[v{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,aecho=0.8:0.6:55:0.12,volume=4.5dB,apad=whole_dur={total:.2f},asplit=2[vo][sc]")
    fl.append(f"[{n}:a]atempo={mt:.4f},aresample=48000,volume=1.04,afade=t=in:d=3,afade=t=out:st={total - 4:.2f}:d=4[m]")
    fl.append("[m][sc]sidechaincompress=threshold=0.05:ratio=5:attack=120:release=900[md]")
    fl.append(f"[vo][md]amix=inputs=2:normalize=0,alimiter=limit=0.95,atrim=0:{total:.2f}[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-i", MUSIC, "-filter_complex", ";".join(fl), "-map", "[a]", "-c:a", "aac", "-b:a", "192k", f"{TMP}/audio.m4a"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{TMP}/list.txt", "-i", f"{TMP}/audio.m4a",
                    "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", "-shortest", OUT], check=True)
    print("wrote", OUT)
