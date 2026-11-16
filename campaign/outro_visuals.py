"""Animated outro for the skit: three shots from the film itself behind the call to action, the NSUI emblem, the two campaign posters,
and keyword chips that appear exactly when the lead says them (word times come from outro.json)."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))

def make(D, TMP, R, t, o):
    """t = start of the outro on the film timeline. Returns (video_path, length, titles, voice_start)"""
    run, probe, W, H, F = R.run, R.probe, R.W, R.H, R.F
    VO0 = 0.8; L = VO0 + o["speech"][1] + 2.2; o0 = t + VO0; XF = 0.4
    e1d = float(probe(f"{D}/clip_e1.mp4", "format=duration"))
    pieces = [("m1", 0.4, 4.8, 0.0), ("bjp", 1.0, 4.8, 0.0), ("e1", max(0.0, e1d - 5.2), 5.0, max(0.0, L - (4.8 + 4.8 + 5.0 - 2 * XF)))]
    files = []
    for i, (cid, ss, dur, pad) in enumerate(pieces):
        f = f"{TMP}/sk_outro_p{i}.mp4"; vf = f"scale={W}:{H}:flags=lanczos,fps={R.FPS},setsar=1" + (f",tpad=stop_mode=clone:stop_duration={pad:.2f}" if pad else "") + ",format=yuv420p"
        run("-ss", f"{ss:.2f}", "-t", f"{dur:.2f}", "-i", f"{D}/clip_{cid}.mp4", "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", f); files.append(f)
    off1 = pieces[0][2] - XF; off2 = off1 + pieces[1][2] - XF; vid = f"{TMP}/sk_outro_v.mp4"
    run("-i", files[0], "-i", files[1], "-i", files[2], "-filter_complex", f"[0:v][1:v]xfade=transition=fade:duration={XF}:offset={off1:.2f}[a];[a][2:v]xfade=transition=fade:duration={XF}:offset={off2:.2f}[v]",
        "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", vid)
    # ---- overlays ----
    wt = {}
    for text, a, b in o["words"]:
        for key, names in (("join", ("जुड़िए", "जुड़िए।")), ("mask", ("mask", "मास्क")), ("aware", ("जागरूक",)), ("breath", ("सांस", "साँस")), ("poll", ("pollution", "पॉल्यूशन")), ("nsui", ("NSUI", "एन"))):
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
    po = poster("let-delhi-breathe", 760); T.append(dict(layer=shadowed(po, (230, 150)), t0=lock + 0.15, t1=end_t, fi=0.8, fo=0.5)); cx = 1390
    T.append(dict(layer=shift(R.text_layer([("साँस लेना", F(R.SER, 112), WH), ("हमारा हक़ है", F(R.SER, 112), GR)], 150), cx - W // 2), t0=lock + 0.3, t1=end_t, fi=0.7, fo=0.5))
    pl = R.text_layer([("Pollution पर Solution", F(R.BIG, 66), WH)], 500); ImageDraw.Draw(pl).rounded_rectangle([cx - 300, 600, cx + 300, 610], 5, fill=SAFF); T.append(dict(layer=shift(pl, cx - W // 2), t0=g("poll", 9.3) - 0.1, t1=end_t, fi=0.5, fo=0.5))
    em2, emm2 = emblem(190); fin = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fin.paste(em2, (cx - 95, 626), emm2)
    ht = R.text_layer([("#LetDelhiBreathe     #PollutionParSolution", F(R.CAP, 42), WH)], 828); fin = Image.alpha_composite(fin, shift(ht, cx - W // 2 - 0)); T.append(dict(layer=fin, t0=g("nsui", 10.8) - 0.1, t1=end_t, fi=0.6, fo=0.5))
    return vid, L, T, o0
