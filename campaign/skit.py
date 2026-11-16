"""Assemble the comedy skit: dialogue clips cut on the last spoken line, subtitles from the transcripts, chyrons,
comedy / hope music beds ducked under the dialogue, and reel-style stings (boom, scratch, whoosh, laughter).
Usage: FILM=beats_skit python3 skit.py <clips_dir> <sfx_dir> <out.mp4>"""
import os, sys, json, subprocess
D, SFX, OUT = sys.argv[1:4]
os.environ["FILM"] = "beats_skit"; sys.argv = [sys.argv[0], D, "-", OUT]
import render as R                      # text, overlay and compositing helpers
import beats_skit as B
def lufs(path, ss=None, t=None):
    cmd = ["ffmpeg", "-hide_banner", "-nostats"] + (["-ss", f"{ss:.2f}", "-t", f"{t:.2f}"] if ss is not None else []) + ["-i", path, "-vn", "-af", "ebur128", "-f", "null", "-"]
    m = __import__("re").findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(cmd, capture_output=True, text=True).stderr); return float(m[-1]) if m else -30.0
def iso_audio(sid):
    """the scene's own audio with street noise, hiss and stray laughter removed (ElevenLabs voice isolator); falls back to the raw clip audio"""
    out = f"{D}/iso_{sid}.wav"
    if os.path.exists(out): return out
    raw = f"{D}/_raw_{sid}.wav"; run("-i", f"{D}/clip_{sid}.mp4", "-vn", "-ac", "1", "-ar", "44100", raw)
    import requests
    r = requests.post("https://api.elevenlabs.io/v1/audio-isolation", headers={"xi-api-key": os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")}, timeout=300, files={"audio": open(raw, "rb")})
    if r.status_code != 200: print("isolation failed for", sid, r.status_code, flush=True); return f"{D}/clip_{sid}.mp4"
    open(f"{D}/_iso_{sid}.mp3", "wb").write(r.content); run("-i", f"{D}/_iso_{sid}.mp3", "-ac", "1", "-ar", "44100", out); return out
TMP = R.TMP; os.makedirs(TMP, exist_ok=True); run, probe = R.run, R.probe
OUTRO = json.load(open(f"{D}/outro.json")) if os.path.exists(f"{D}/outro.json") else None
TAIL = (0.8 + OUTRO["speech"][1] + 3.2) if OUTRO else 5.5; INTRO = 3.4; XFD = 0.3; t = INTRO - XFD; caps = []; shots = []; segs = []; cues = []; hope_at = None
for s in B.SCENES:
    clip = f"{D}/clip_{s['id']}.mp4"; tr = json.load(open(f"{D}/tr_{s['id']}.json")) if os.path.exists(f"{D}/tr_{s['id']}.json") else []
    d = float(probe(clip, "format=duration")); end = min(d - 0.05, max(x["end"] for x in tr) + 1.7) if tr and s["lines"] else d - 0.05
    nxt = json.load(open(f"{D}/nxt_{s['id']}.json"))["next_start"] if os.path.exists(f"{D}/nxt_{s['id']}.json") else None
    if tr and s["lines"] and nxt: end = min(end, max(max(x["end"] for x in tr) + 0.12, nxt - 0.04))   # never cut into an unscripted word
    if s.get("cut"): end = min(end, s["cut"])
    if s.get("tight") and tr: end = min(end, max(x["end"] for x in tr) + 0.5)   # stop right after the last scripted line (clip may run on)
    aud = iso_audio(s["id"]) if not s.get("silent") else clip
    last = s is B.SCENES[-1]; seg = f"{TMP}/sk_{s['id']}.mp4"
    run("-i", clip, "-t", f"{end:.2f}", "-vf", f"scale={R.W}:{R.H}:flags=lanczos,fps={R.FPS},setsar=1" + (f",tpad=stop_mode=clone:stop_duration={TAIL}" if (last and not OUTRO) else "") + ",format=yuv420p",
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", seg)
    swaps = [(json.load(open(p)), p[:-5] + ".mp3") for p in sorted(__import__("glob").glob(f"{D}/vs_{s['id']}_*.json"))]   # lead lines re-voiced by voice_swap.py
    tail = "loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,afade=t=in:d=0.12,afade=t=out:st=%.2f:d=%.2f" % (end - XFD, XFD)
    if swaps:
        # 1) normalise the scene with the re-voiced lines muted, 2) lay the converted lines on top at an exact level relative to the other voices
        gate = "+".join([f"between(t,{w['start']:.2f},{w['end']:.2f})" for w, _ in swaps] + [f"between(t,{a:.2f},{b:.2f})" for a, b in s.get("mute", [])]); bg = f"{TMP}/sk_{s['id']}_bg.wav"
        g0 = lufs(aud, 0.0, end); gain0 = max(-12.0, min(14.0, -15.0 - g0))   # level set from the ORIGINAL scene, so the ambience left after muting the lead line is not boosted
        run("-i", aud, "-t", f"{end:.2f}", "-vn", "-af", f"volume=enable='{gate}':volume=0,volume={gain0:.1f}dB,aresample=48000,afade=t=in:d=0.12,afade=t=out:st={end - XFD:.2f}:d={XFD}", "-ac", "2", bg)
        ins = []; fl = []; outs = []
        for j, (w, mp3) in enumerate(swaps):
            who = s["lines"][int(mp3.rsplit("_", 1)[1][:-4])][0]
            oth = [lufs(bg, x["start"], x["end"] - x["start"]) for (n, _), x in zip(s["lines"], tr) if n != who and x["end"] - x["start"] > 0.8] if tr else []
            ref = (max(oth) + 5.0) if oth else (-12.0 if who == "कबीर" else -14.0)    # lead: 5 dB above the loudest other voice in the scene
            gain = max(-6.0, min(20.0, ref - lufs(mp3))); ins += ["-i", mp3]
            fl.append(f"[{j + 1}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain:.1f}dB,adelay={int(w['start'] * 1000)}:all=1[v{j}]"); outs.append(f"[v{j}]")
        fl.append("[0:a]" + "".join(outs) + f"amix=inputs={len(swaps) + 1}:normalize=0:duration=first,alimiter=limit=0.97:level=0[o]")
        run("-i", bg, *ins, "-filter_complex", ";".join(fl), "-map", "[o]", "-ac", "2", f"{TMP}/sk_{s['id']}.wav")
    else:
        run("-i", aud, "-t", f"{end:.2f}", "-vn", "-af", ("volume=0.12," if s.get("silent") else "") + tail, "-ac", "2", f"{TMP}/sk_{s['id']}.wav")
    names = [n for n, _ in s["lines"]]
    for i, x in enumerate(tr):   # subtitle text from the script when the line count matches, else what was actually said
        text = (f"{names[i]} :  {s['lines'][i][1]}" if len(tr) == len(s["lines"]) else x["text"]).replace("...", "…")
        caps.append(dict(text=text, t0=t + x["start"], t1=t + min(x["end"] + 0.3, end)))
    if s.get("chyron"): shots.append(dict(tag=s["chyron"], t0=t, t1=t + min(end, 4.0)))
    punch = t + (max(x["end"] for x in tr) if tr else end) + 0.1
    for k in (s.get("sfx") or "").split("+"):
        if k == "whoosh": cues.append(("whoosh", max(0, t - 0.4), 0.45))
        elif k == "boom": cues.append(("boom", punch, 0.42))
        elif k == "scratch": cues.append(("scratch", punch - 0.1, 0.4))
        elif k == "laugh": cues.append(("laugh", punch + (0.35 if "boom" in s["sfx"] else 0.1), 0.75))
    if s.get("music") == "hope": hope_at = t
    segs.append((s["id"], t, end)); t += end - (0 if (last and not OUTRO) else XFD)
run("-f", "lavfi", "-i", f"color=c=black:s={R.W}x{R.H}:r={R.FPS}:d={INTRO}", "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", f"{TMP}/sk_intro.mp4")
asegs = list(segs)
outro_titles = []
if OUTRO:   # closing call to action in the lead's voice, over an animated outro built from the film's own footage and the campaign logos
    import outro_visuals
    ovid, OL, outro_titles, o0 = outro_visuals.make(D, TMP, R, t, OUTRO)
    run("-i", f"{D}/outro.mp3", "-af", "highpass=f=70,acompressor=threshold=0.1:ratio=3:attack=15:release=150:makeup=2,loudnorm=I=-13:TP=-1.5:LRA=7,aresample=48000,afade=t=in:d=0.05", "-ac", "2", f"{TMP}/sk_outro.wav")
    asegs.append(("outro", o0, OUTRO["duration"])); caps += [dict(text=x["text"], t0=o0 + x["start"], t1=o0 + x["end"]) for x in OUTRO["subs"]]
total = t + TAIL
vin = [f"{TMP}/sk_intro.mp4"] + [f"{TMP}/sk_{i}.mp4" for i, _, _ in segs] + ([ovid] if OUTRO else []); starts = [0.0] + [t0 for _, t0, _ in segs] + ([t] if OUTRO else []); fl = []; prev = "[0:v]"
for i in range(1, len(vin)):
    fl.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XFD}:offset={starts[i]:.3f}[x{i}]"); prev = f"[x{i}]"
run(*[a for p in vin for a in ("-i", p)], "-filter_complex", ";".join(fl), "-map", prev, "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", f"{TMP}/sk_base.mp4")
R.BEATS[:] = [dict(id="end", end=True, t0=t + 0.3, d=0.0)]; titles = outro_titles if OUTRO else R.make_titles(total)
# opening disclaimer: the skit names real office-holders, so say plainly that it is fiction
from PIL import Image
box = Image.new("RGBA", (R.W, R.H), (0, 0, 0, 215)); tl = R.text_layer([("यह एक काल्पनिक व्यंग्य है", R.F(R.BIG, 84), R.WHITE),
    ("पात्र, घटनाएँ और संवाद काल्पनिक हैं  |  सभी दृश्य और आवाज़ें AI-निर्मित हैं", R.F(R.CAP, 40), R.WHITE)], 420)
box.alpha_composite(tl); titles.insert(0, dict(layer=box, t0=0.0, t1=INTRO, fi=0.01, fo=0.3))
R.composite(f"{TMP}/sk_base.mp4", f"{TMP}/sk_video.mp4", caps, titles, total, shots=shots)
# ---- audio ----
ins = []; fl = []; n = 0; dia = []
for sid, t0, end in asegs:
    ins += ["-i", f"{TMP}/sk_{sid}.wav"]; fl.append(f"[{n}:a]adelay={int(t0 * 1000)}:all=1[d{n}]"); dia.append(f"[d{n}]"); n += 1
fl.append("".join(dia) + f"amix=inputs={len(dia)}:normalize=0,apad=whole_dur={total:.2f},asplit=2[dia][sc]")
ins += ["-stream_loop", "-1", "-i", f"{SFX}/comedy.mp3", "-i", f"{SFX}/hope.mp3"]; c, h = n, n + 1; n += 2
fl.append(f"[{c}:a]atrim=0:{hope_at:.2f},aresample=48000,volume=0.55,afade=t=in:d=1,afade=t=out:st={hope_at - 1.2:.2f}:d=1.2[c]")
fl.append(f"[{h}:a]aresample=48000,volume=0.8,afade=t=in:d=0.8,afade=t=out:st={total - hope_at - 3:.2f}:d=3,adelay={int(hope_at * 1000)}:all=1[h]")
fl.append(f"[c][h]amix=inputs=2:normalize=0,apad=whole_dur={total:.2f}[mus];[mus][sc]sidechaincompress=threshold=0.04:ratio=6:attack=60:release=500[md]")
fx = []
for k, at, vol in cues:
    ins += ["-i", f"{SFX}/{k}.wav"]; fl.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={int(at * 1000)}:all=1[x{n}]"); fx.append(f"[x{n}]"); n += 1
fl.append("[dia][md]" + "".join(fx) + f"amix=inputs={2 + len(fx)}:normalize=0,alimiter=limit=0.89:level=0,atrim=0:{total:.2f}[a]")
run(*ins, "-filter_complex", ";".join(fl), "-map", "[a]", "-c:a", "aac", "-b:a", "192k", f"{TMP}/sk_audio.m4a")
run("-i", f"{TMP}/sk_video.mp4", "-i", f"{TMP}/sk_audio.m4a", "-c", "copy", "-movflags", "+faststart", "-shortest", OUT)
print(f"wrote {OUT}  {total:.1f}s", [(k, round(a, 1)) for k, a, _ in cues])

# ---- optional 9:16 version (PORTRAIT=<out.mp4>): same footage and audio, relaid for phones; no shots are regenerated ----
if os.environ.get("PORTRAIT"):
    from PIL import ImageDraw
    PW, PH, VY, VH = 1080, 1920, 520, 608; OFF = INTRO   # the intro card is dropped
    R.static_overlay = lambda: Image.new("RGBA", (R.W, R.H), (0, 0, 0, 0))   # no letterbox bars / corner tag inside the picture
    nocap = f"{TMP}/sk_nocap.mp4"; R.composite(f"{TMP}/sk_base.mp4", nocap, [], [x for x in titles if x.get("layer") is not box], total)
    plate = Image.new("RGBA", (PW, PH), (0, 0, 0, 0)); d = ImageDraw.Draw(plate); NAVY = (11, 38, 102, 235)
    em = Image.open(f"{R.HERE}/brand/nsui-emblem.png").convert("RGB").resize((170, 170), Image.LANCZOS); m = Image.new("L", (170, 170), 0); ImageDraw.Draw(m).ellipse([1, 1, 168, 168], fill=255); plate.paste(em, (70, 250), m)
    f1 = R.F(R.BIG, 66); f2 = R.F(R.CAP, 40); x0 = 270
    R.mtext(d, x0 + R.mlen(d, "Pollution पर Solution", f1) / 2, 252, "Pollution पर Solution", f1, R.WHITE); d.rounded_rectangle([x0, 348, x0 + 420, 356], 4, fill=R.SAFFRON)
    R.mtext(d, x0 + R.mlen(d, "दिल्ली को साँस लेने दो  |  NSUI", f2) / 2, 368, "दिल्ली को साँस लेने दो  |  NSUI", f2, (255, 255, 255, 235))
    f3 = R.F(R.CAP, 24); R.mtext(d, PW - 60 - R.mlen(d, "काल्पनिक व्यंग्य  |  AI-निर्मित", f3) / 2, VY + VH + 10, "काल्पनिक व्यंग्य  |  AI-निर्मित", f3, (255, 255, 255, 150))
    d.rounded_rectangle([70, 1430, PW - 70, 1570], 26, fill=NAVY); d.rounded_rectangle([70, 1430, 86, 1570], 8, fill=R.SAFFRON)
    R.mtext(d, PW // 2 + 8, 1436, "पॉल्यूशन हेल्पलाइन  :  मिस्ड कॉल दें  |  WhatsApp करें", R.F(R.CAP, 32), (255, 255, 255, 235)); R.mtext(d, PW // 2 + 8, 1476, "8875833833", R.F(R.BIG, 70), R.WHITE)
    plate.save(f"{TMP}/pt_plate.png")
    def cap_layer(text):
        f = R.F(R.CAP, 54); ls = R.wrap(text, f, 940); L = Image.new("RGBA", (PW, PH), (0, 0, 0, 0)); dd = ImageDraw.Draw(L); h = 78 * len(ls); y = 1180 + max(0, (228 - h) // 2)
        dd.rounded_rectangle([50, y - 14, PW - 50, y + h + 14], 22, fill=(0, 0, 0, 150))
        for i, l in enumerate(ls): R.mtext(dd, PW // 2, y + 78 * i, l, f, R.WHITE)
        return L
    def tag_layer(text):
        f = R.F(R.BIG, 38); L = Image.new("RGBA", (PW, PH), (0, 0, 0, 0)); dd = ImageDraw.Draw(L); w = int(R.mlen(dd, text, f)) + 44
        dd.rounded_rectangle([60, VY - 68, 60 + w, VY - 10], 10, fill=(0, 0, 0, 170)); dd.rectangle([60, VY - 68, 68, VY - 10], fill=R.SAFFRON); R.mtext(dd, 60 + w // 2 + 4, VY - 64, text, f, R.WHITE); return L
    capl = {}; tagl = {}; n = int((total - OFF) * R.FPS)
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", f"{OFF}", "-i", nocap, "-i", f"{TMP}/pt_plate.png", "-filter_complex",
        f"[0:v]split[a][b];[a]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,gblur=sigma=9,eq=brightness=-0.22:saturation=0.8,scale={PW}:{PH}[bg];[b]scale={PW}:{VH}:flags=lanczos[fg];[bg][fg]overlay=0:{VY}[v];[v][1:v]overlay=0:0,format=rgb24[o]",
        "-map", "[o]", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{PW}x{PH}", "-r", str(R.FPS), "-i", "-", "-ss", f"{OFF}", "-i", f"{TMP}/sk_audio.m4a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "6M", "-bufsize", "12M", "-pix_fmt", "yuv420p", "-af", "afade=t=in:d=0.3", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", os.environ["PORTRAIT"]], stdin=subprocess.PIPE)
    last = None
    for fi in range(n):
        raw = dec.stdout.read(PW * PH * 3)
        if len(raw) < PW * PH * 3: raw = last
        last = raw; tt = fi / R.FPS + OFF; fr = Image.frombuffer("RGB", (PW, PH), raw).copy()
        for s_ in shots:
            a = R.fade(tt, s_["t0"] + 0.15, s_["t1"] - 0.15, 0.3, 0.3)
            if a > 0:
                if s_["tag"] not in tagl: tagl[s_["tag"]] = tag_layer(s_["tag"])
                R.paste(fr, tagl[s_["tag"]], a)
        for i, c in enumerate(caps):
            a = R.fade(tt, c["t0"] - 0.1, c["t1"] + 0.1, 0.2, 0.2)
            if a > 0:
                if i not in capl: capl[i] = cap_layer(c["text"])
                R.paste(fr, capl[i], a)
        g = min(1.0, (total - tt) / 1.0)
        if g < 1: fr = Image.blend(Image.new("RGB", (PW, PH)), fr, max(0, g))
        enc.stdin.write(fr.tobytes())
    dec.kill(); enc.stdin.close(); enc.wait(); print("wrote", os.environ["PORTRAIT"])
