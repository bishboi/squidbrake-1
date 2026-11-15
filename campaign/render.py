"""Assemble the film: generated video shots + captions + title cards + narration, score and ambience.
Usage: python3 render.py <assets_dir> <music.mp3> <out.mp4>      (PREVIEW=t1,t2 dumps stills instead)"""
import os, sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from beats import BEATS
from timeline import build, XF
A, MUSIC, OUT = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__)); TMP = os.path.join(A, "_render")
W, H, FPS = 1920, 1080, 25
INTER = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
F = lambda n, s: ImageFont.truetype(f"{HERE}/fonts/{n}.ttf", s)
CAP, BIG, SER = "NotoSansDevanagari-Medium", "NotoSansDevanagari-ExtraBold", "NotoSerifDevanagari-Bold"
WHITE, RED, GREEN, SAFFRON = (255, 255, 255, 255), (255, 82, 64, 255), (60, 190, 90, 255), (255, 153, 51, 255)
run = lambda *a, **k: subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True, **k)
probe = lambda p, e: subprocess.run(["ffprobe", "-v", "error", "-show_entries", e, "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()

# ---------- text ----------
def runs(text, font):
    """split into Devanagari / other runs — the Devanagari fonts carry no Latin glyphs or digits"""
    lat = ImageFont.truetype(INTER % ("SemiBold" if "Medium" in font.path else "ExtraBold"), int(font.size * 0.9)); out = []
    for ch in text:
        f = font if ("ऀ" <= ch <= "ॿ" or ch == " ") else lat
        if out and out[-1][1] is f: out[-1][0] += ch
        else: out.append([ch, f])
    return out
def mlen(d, text, font): return sum(d.textlength(t, font=f) for t, f in runs(text, font))
def mtext(d, cx, y, text, font, fill):
    x = cx - mlen(d, text, font) / 2; base = y + font.getmetrics()[0]
    for t, f in runs(text, font): d.text((x, base), t, font=f, fill=fill, anchor="ls"); x += d.textlength(t, font=f)
def text_layer(lines, y):
    """lines: [(text, font, fill)] centred with a soft shadow; returns a full-frame RGBA layer"""
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh); yy = y
    for t, f, _ in lines: mtext(ds, W // 2, yy, t, f, (0, 0, 0, 240)); yy += int(f.size * 1.45)
    im = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)), sh.filter(ImageFilter.GaussianBlur(3))); d = ImageDraw.Draw(im); yy = y
    for t, f, c in lines: mtext(d, W // 2, yy, t, f, c); yy += int(f.size * 1.45)
    return im
def wrap(text, font, maxw):
    d = ImageDraw.Draw(Image.new("L", (8, 8))); out = []; cur = ""
    for w in text.split():
        if mlen(d, (cur + " " + w).strip(), font) > maxw and cur: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return out + [cur]
def static_overlay():
    """letterbox bars + vignette + disclaimer tag"""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = Image.new("L", (W // 8, H // 8)); p = px.load()
    for y in range(H // 8):
        for x in range(W // 8):
            r = math.hypot((x - W / 16) / (W / 16), (y - H / 16) / (H / 16)); p[x, y] = int(min(1, max(0, r - 0.6) / 0.85) * 170)
    ov.putalpha(px.resize((W, H), Image.BICUBIC)); d = ImageDraw.Draw(ov)
    d.rectangle([0, 0, W, 60], fill=(0, 0, 0, 255)); d.rectangle([0, H - 60, W, H], fill=(0, 0, 0, 255))
    mtext(d, W - 230, 14, "सांकेतिक दृश्य  |  AI-निर्मित", F(CAP, 22), (255, 255, 255, 130)); return ov
def fade(t, t0, t1, fi=0.35, fo=0.35):
    return 0.0 if t < t0 or t > t1 else max(0.0, min(1.0, (t - t0) / fi, (t1 - t) / fo))
def paste(fr, layer, a):
    """paste the non-empty part of an RGBA layer at opacity a"""
    if "box" not in layer.info: layer.info["box"] = layer.getbbox(); layer.info["crop"] = layer.crop(layer.info["box"])
    c = layer.info["crop"]; m = c.getchannel("A") if a >= 0.999 else c.getchannel("A").point(lambda v: int(v * a))
    fr.paste(c, layer.info["box"][:2], m)

def make_titles(total):
    T = []
    for b in BEATS:
        if b.get("title"):
            big, small, src = b["title"]; lines = [(big, F(BIG, 150), WHITE)]
            if small: lines.append((small, F(BIG, 62), RED))
            if src: lines.append((src, F(CAP, 30), (255, 255, 255, 215)))
            T.append(dict(layer=text_layer(lines, 240 if small else 300), t0=b["t0"] + b["d"] * 0.25, t1=b["t1"] - 0.15, fi=0.6, fo=0.5))
    e = [b for b in BEATS if b.get("end")][0]; t0 = e["t0"] + e["d"] * 0.4
    T.append(dict(layer=Image.new("RGBA", (W, H), (0, 0, 0, 185)), t0=t0, t1=total + 1, fi=1.5, fo=0.5, full=True))
    # end card: campaign poster on the left, slogan and NSUI emblem on the right
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ph = 800; po = Image.open(f"{HERE}/brand/let-delhi-breathe.png").convert("RGB")
    po = po.resize((int(po.width * ph / po.height), ph), Image.LANCZOS); mask = Image.new("L", po.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, po.width - 1, ph - 1], 28, fill=255); px = 250; py = (H - ph) // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([px, py + 14, px + po.width, py + ph + 14], 28, fill=(0, 0, 0, 200))
    card = Image.alpha_composite(card, sh.filter(ImageFilter.GaussianBlur(22))); card.paste(po, (px, py), mask)
    T.append(dict(layer=card, t0=t0 + 0.3, t1=total + 1, fi=1.0, fo=0.5))
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cx = px + po.width + (W - px - po.width) // 2 - 40
    tl = text_layer([("दिल्ली को", F(SER, 120), WHITE), ("साँस लेने दो", F(SER, 120), GREEN), ("Pollution पर Solution", F(BIG, 60), WHITE)], 190)
    txt.paste(tl, (cx - W // 2, 0), tl); ImageDraw.Draw(txt).rounded_rectangle([cx - 230, 560, cx + 230, 570], 5, fill=SAFFRON)
    em = Image.open(f"{HERE}/brand/nsui-emblem.png").convert("RGB").resize((230, 230), Image.LANCZOS); cm = Image.new("L", (230, 230), 0)
    ImageDraw.Draw(cm).ellipse([2, 2, 227, 227], fill=255); txt.paste(em, (cx - 115, 710), cm)
    T.append(dict(layer=txt, t0=t0 + 1.2, t1=total + 1, fi=1.0, fo=0.5))
    return T

# ---------- video ----------
def segments(shots):
    """one normalised 1080p/25fps segment per shot, cut (or gently slowed) to the footage it must cover"""
    for i, s in enumerate(shots):
        s["seg"] = f"{TMP}/seg_{i:02d}.mp4"; clip = f"{A}/clip_{s['id']}.mp4"; need = s["need"] + 0.08
        if os.path.exists(clip):
            d = float(probe(clip, "format=duration")); slow = max(1.0, need / (d - 0.1))
            run("-i", clip, "-vf", f"setpts={slow:.4f}*PTS,scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1,format=yuv420p", "-t", f"{need:.3f}", "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", s["seg"])
            s["amb"] = clip if probe(clip, "stream=codec_type").count("audio") else None
        else:  # no generated clip: slow push-in on the still
            n = int(need * FPS) + 1; print("still fallback:", s["id"], flush=True); s["amb"] = None
            run("-loop", "1", "-i", f"{A}/still_{s['id']}.png", "-vf", f"scale=3840:2160,zoompan=z='1+0.10*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},format=yuv420p",
                "-t", f"{need:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", s["seg"])

def base_video(shots, out):
    ins = []; fl = []; prev = "[0:v]"
    for s in shots: ins += ["-i", s["seg"]]
    for i in range(1, len(shots)):
        fl.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={shots[i]['a']:.3f}[x{i}]"); prev = f"[x{i}]"
    run(*ins, "-filter_complex", ";".join(fl), "-map", prev, "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", out)

def composite(base, out, caps, titles, total, only=None):
    ov = static_overlay(); capl = {}; black = Image.new("RGB", (W, H)); nf = int(total * FPS)
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = None if only else subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-maxrate", "3200k", "-bufsize", "6400k", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for fi in range(nf):
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3: raw = last
        last = raw; t = fi / FPS
        if only is not None and fi not in only: continue
        fr = Image.frombuffer("RGB", (W, H), raw).copy(); fr.paste(ov, (0, 0), ov)
        for tl in titles:
            a = fade(t, tl["t0"], tl["t1"], tl["fi"], tl["fo"])
            if a > 0: paste(fr, tl["layer"], a)
        for i, c in enumerate(caps):
            a = fade(t, c["t0"] - 0.1, c["t1"] + 0.1, 0.25, 0.25)
            if a > 0:
                if i not in capl:
                    f = F(CAP, 50); ls = wrap(c["text"], f, 1500); capl[i] = text_layer([(l, f, WHITE) for l in ls], H - 96 - 72 * len(ls))
                paste(fr, capl[i], a)
        g = min(1, t / 2.0, (total - t) / 2.5)
        if g < 1: fr = Image.blend(black, fr, max(0, g))
        if only is not None: fr.save(f"{TMP}/prev_{fi / FPS:.1f}.jpg", quality=88)
        else: enc.stdin.write(fr.tobytes())
    dec.kill()
    if enc: enc.stdin.close(); enc.wait()

# ---------- audio ----------
def audio(shots, total, out):
    ins = []; fl = []; n = 0; vo = []; amb = []
    for b in BEATS:
        ins += ["-i", f"{TMP}/vo_{b['id']}.wav"]; fl.append(f"[{n}:a]adelay={int(b['t0'] * 1000)}:all=1[v{n}]"); vo.append(f"[v{n}]"); n += 1
    for s in shots:
        if s.get("amb"):
            ins += ["-i", s["amb"]]; d = s["need"]
            fl.append(f"[{n}:a]atrim=0:{d:.2f},aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.5,afade=t=out:st={max(0, d - 0.6):.2f}:d=0.6,"
                      f"adelay={int(s['a'] * 1000)}:all=1[e{n}]"); amb.append(f"[e{n}]"); n += 1
    mt = max(0.5, min(1.0, float(probe(MUSIC, "format=duration")) / (total + 0.5)))
    fl.append("".join(vo) + f"amix=inputs={len(vo)}:normalize=0,aecho=0.8:0.6:55:0.12,volume=4.5dB,apad=whole_dur={total:.2f},asplit=2[vo][sc]")
    fl.append(f"[{n}:a]atempo={mt:.4f},aresample=48000,volume=1.0,afade=t=in:d=3,afade=t=out:st={total - 4:.2f}:d=4[m]")
    fl.append("[m][sc]sidechaincompress=threshold=0.05:ratio=5:attack=120:release=900[md]"); mix = "[vo][md]"; k = 2
    if amb: fl.append("".join(amb) + f"amix=inputs={len(amb)}:normalize=0,highpass=f=80,volume=0.16[am]"); mix += "[am]"; k = 3
    fl.append(f"{mix}amix=inputs={k}:normalize=0,alimiter=limit=0.89,atrim=0:{total:.2f}[a]")
    run(*ins, "-i", MUSIC, "-filter_complex", ";".join(fl), "-map", "[a]", "-c:a", "aac", "-b:a", "192k", out)

if __name__ == "__main__":
    shots, caps, total = build(A); titles = make_titles(total); print(f"duration {total:.1f}s, {len(shots)} shots, {len(caps)} captions", flush=True)
    base = f"{TMP}/base.mp4"
    if not os.environ.get("REUSE_BASE"): segments(shots); base_video(shots, base)
    else:
        for s in shots: c = f"{A}/clip_{s['id']}.mp4"; s["amb"] = c if os.path.exists(c) and "audio" in probe(c, "stream=codec_type") else None
    if os.environ.get("PREVIEW"):
        composite(base, None, caps, titles, total, only={int(float(x) * FPS) for x in os.environ["PREVIEW"].split(",")}); sys.exit()
    composite(base, f"{TMP}/video.mp4", caps, titles, total); audio(shots, total, f"{TMP}/audio.m4a")
    run("-i", f"{TMP}/video.mp4", "-i", f"{TMP}/audio.m4a", "-c", "copy", "-movflags", "+faststart", "-shortest", OUT); print("wrote", OUT)
