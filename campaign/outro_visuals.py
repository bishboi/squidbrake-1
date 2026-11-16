"""Animated outro for the skit: three shots from the film itself behind the call to action, the NSUI emblem, the two campaign posters,
and keyword chips that appear exactly when the lead says them (word times come from outro.json)."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))

def make(D, TMP, R, t, o):
    """t = start of the outro on the film timeline. Returns (video_path, length, titles, voice_start)"""
    run, probe, W, H, F = R.run, R.probe, R.W, R.H, R.F
    VO0 = 0.8; L = VO0 + o["speech"][1] + 3.2; o0 = t + VO0; XF = 0.4
    custom = getattr(__import__("importlib").import_module(os.environ.get("SKIT", "beats_skit")), "OUTRO_PLAN", None)
    e1d = float(probe(f"{D}/clip_e1.mp4", "format=duration")) if not custom else 0.0
    plan = custom or [("m1", 0.4, 4.6), ("bjp", 1.0, 4.6), ("d2", 0.6, 4.6), ("m2", 0.8, 4.6), ("e1", max(0.0, e1d - 5.2), 5.0)]
    skip = set(filter(None, os.environ.get("SKIP", "").split(","))); alt = iter([("rl", 0.5, 4.6), ("c1", 2.0, 4.6), ("g1a", 0.5, 4.6)])
    plan = [p if p[0] not in skip else next(alt) for p in plan]   # background shots follow the cut
    pad = max(0.0, L - (sum(p[2] for p in plan) - XF * (len(plan) - 1)))
    files = []
    for i, (cid, ss, dur) in enumerate(plan):
        f = f"{TMP}/sk_outro_p{i}.mp4"; vf = f"scale={W}:{H}:flags=lanczos,fps={R.FPS},setsar=1" + (f",tpad=stop_mode=clone:stop_duration={pad:.2f}" if i == len(plan) - 1 and pad else "") + ",format=yuv420p"
        run("-ss", f"{ss:.2f}", "-t", f"{dur:.2f}", "-i", f"{D}/clip_{cid}.mp4", "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", f); files.append(f)
    fl = []; prev = "[0:v]"; acc = plan[0][2]
    for i in range(1, len(plan)):
        fl.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={acc - XF:.2f}[x{i}]"); prev = f"[x{i}]"; acc += plan[i][2] - XF
    vid = f"{TMP}/sk_outro_v.mp4"
    run(*[a for p in files for a in ("-i", p)], "-filter_complex", ";".join(fl), "-map", prev, "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", vid)
    # ---- overlays ----
    wt = {}
    for text, a, b in o["words"]:
        for key, names in (("join", ("जुड़िए", "जुड़िए।")), ("mask", ("mask", "मास्क")), ("aware", ("जागरूक",)), ("breath", ("सांस", "साँस")), ("poll", ("pollution", "पॉल्यूशन")), ("help", ("helpline", "हेल्पलाइन")), ("miss", ("missed",)), ("nsui", ("NSUI", "एन"))):
            if key not in wt and text.strip(" ,।.").lower() in [n.lower() for n in names]: wt[key] = a
    g = lambda k, d: o0 + wt.get(k, d)
    NAVY, SAFF, WH, GR = (11, 38, 102, 228), R.SAFFRON, R.WHITE, R.GREEN
    def shadowed(img, pos, radius=26):
        L_ = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius, fill=255)
        ImageDraw.Draw(sh).rounded_rectangle([pos[0], pos[1] + 12, pos[0] + img.width, pos[1] + img.height + 12], radius, fill=(0, 0, 0, 190)); L_ = Image.alpha_composite(L_, sh.filter(ImageFilter.GaussianBlur(20))); L_.paste(img, pos, m); return L_
    def poster(name, h): im = Image.open(f"{HERE}/brand/{name}.png").convert("RGB"); return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    def emblem(size):
        em = Image.open(f"{HERE}/brand/nsui-emblem.png").convert("RGB").resize((size, size), Image.LANCZOS); m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).ellipse([1, 1, size - 2, size - 2], fill=255); return em, m
    def chip(text, y):
        L_ = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L_); f = F(R.BIG, 72); w = int(R.mlen(d, text, f)) + 96
        d.rounded_rectangle([110, y, 110 + w, y + 118], 18, fill=NAVY); d.rounded_rectangle([110, y, 124, y + 118], 7, fill=SAFF); R.mtext(d, 110 + 14 + (w - 14) // 2, y + 14, text, f, WH); return L_
    def shift(layer, dx): n = Image.new("RGBA", (W, H), (0, 0, 0, 0)); n.paste(layer, (dx, 0), layer); return n
    T = []; lock = g("breath", 7.3) - 0.25; end_t = t + L + 1
    em, emm = emblem(118); badge = Image.new("RGBA", (W, H), (0, 0, 0, 0)); badge.paste(em, (70, 84), emm); T.append(dict(layer=badge, t0=t + 0.5, t1=lock + 0.3, fi=0.6, fo=0.4))
    T.append(dict(layer=shadowed(poster("pollution-par-solution", 640), (1230, 215)), t0=g("join", 3.1) - 0.3, t1=lock + 0.3, fi=0.7, fo=0.4))
    for key, text, y, dflt in (("join", "जुड़िए", 300, 3.1), ("mask", "मास्क बाँटिए", 440, 5.1), ("aware", "जागरूक कीजिए", 580, 6.1)):
        T.append(dict(layer=chip(text, y), t0=g(key, dflt) - 0.05, t1=lock + 0.3, fi=0.35, fo=0.4))
    T.append(dict(layer=Image.new("RGBA", (W, H), (0, 0, 0, 175)), t0=lock, t1=end_t, fi=0.8, fo=0.5))
    po = poster("let-delhi-breathe", 640); T.append(dict(layer=shadowed(po, (250, 165)), t0=lock + 0.15, t1=end_t, fi=0.8, fo=0.5)); cx = 1390
    T.append(dict(layer=shift(R.text_layer([("साँस लेना", F(R.SER, 96), WH), ("हमारा हक़ है", F(R.SER, 96), GR)], 95), cx - W // 2), t0=lock + 0.3, t1=end_t, fi=0.7, fo=0.5))
    pl = R.text_layer([("Pollution पर Solution", F(R.BIG, 58), WH)], 392); ImageDraw.Draw(pl).rounded_rectangle([cx - 280, 484, cx + 280, 493], 5, fill=SAFF); T.append(dict(layer=shift(pl, cx - W // 2), t0=g("poll", 9.3) - 0.1, t1=end_t, fi=0.5, fo=0.5))
    # helpline block: emblem + number pill, shown while the helpline is announced and kept to the end
    hl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(hl); em2, emm2 = emblem(150); hl.paste(em2, (930, 532), emm2)
    d.rounded_rectangle([1110, 520, 1860, 690], 24, fill=NAVY); d.rounded_rectangle([1110, 520, 1126, 690], 8, fill=SAFF)
    R.mtext(d, 1493, 530, "पॉल्यूशन हेल्पलाइन", F(R.BIG, 38), (255, 255, 255, 235)); R.mtext(d, 1493, 578, "8875833833", F(R.BIG, 92), WH)
    T.append(dict(layer=hl, t0=g("help", 13.2) - 0.1, t1=end_t, fi=0.6, fo=0.5))
    how = R.text_layer([("मिस्ड कॉल दें   |   WhatsApp करें", F(R.CAP, 44), WH)], 706); T.append(dict(layer=shift(how, cx - W // 2 + 85), t0=g("miss", 14.3) - 0.2, t1=end_t, fi=0.5, fo=0.5))
    ht = R.text_layer([("#LetDelhiBreathe     #PollutionParSolution", F(R.CAP, 38), WH)], 790); T.append(dict(layer=shift(ht, cx - W // 2), t0=g("nsui", 21.9) - 0.1, t1=end_t, fi=0.6, fo=0.5))
    return vid, L, T, o0
