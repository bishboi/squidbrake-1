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
TMP = R.TMP; os.makedirs(TMP, exist_ok=True); run, probe = R.run, R.probe
OUTRO = json.load(open(f"{D}/outro.json")) if os.path.exists(f"{D}/outro.json") else None
TAIL = max(5.5, OUTRO["duration"] + 2.6) if OUTRO else 5.5; INTRO = 3.4; t = INTRO; caps = []; shots = []; segs = []; cues = []; hope_at = None
for s in B.SCENES:
    clip = f"{D}/clip_{s['id']}.mp4"; tr = json.load(open(f"{D}/tr_{s['id']}.json")) if os.path.exists(f"{D}/tr_{s['id']}.json") else []
    d = float(probe(clip, "format=duration")); end = min(d - 0.05, max(x["end"] for x in tr) + 1.7) if tr and s["lines"] else d - 0.05
    if s.get("cut"): end = min(end, s["cut"])
    if s.get("tight") and tr: end = min(end, max(x["end"] for x in tr) + 0.4)   # stop right after the last scripted line (clip may run on)
    last = s is B.SCENES[-1]; seg = f"{TMP}/sk_{s['id']}.mp4"
    run("-i", clip, "-t", f"{end:.2f}", "-vf", f"scale={R.W}:{R.H}:flags=lanczos,fps={R.FPS},setsar=1" + (f",tpad=stop_mode=clone:stop_duration={TAIL}" if last else "") + ",format=yuv420p",
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", seg)
    swaps = [(json.load(open(p)), p[:-5] + ".mp3") for p in sorted(__import__("glob").glob(f"{D}/vs_{s['id']}_*.json"))]   # lead lines re-voiced by voice_swap.py
    tail = "loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,afade=t=in:d=0.05,afade=t=out:st=%.2f:d=0.15" % (end - 0.15)
    if swaps:
        # 1) normalise the scene with the re-voiced lines muted, 2) lay the converted lines on top at an exact level relative to the other voices
        gate = "+".join([f"between(t,{w['start']:.2f},{w['end']:.2f})" for w, _ in swaps] + [f"between(t,{a:.2f},{b:.2f})" for a, b in s.get("mute", [])]); bg = f"{TMP}/sk_{s['id']}_bg.wav"
        run("-i", clip, "-t", f"{end:.2f}", "-vn", "-af", f"volume=enable='{gate}':volume=0,{tail}", "-ac", "2", bg)
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
        run("-i", clip, "-t", f"{end:.2f}", "-vn", "-af", ("volume=0.12," if s.get("silent") else "") + tail, "-ac", "2", f"{TMP}/sk_{s['id']}.wav")
    names = [n for n, _ in s["lines"]]
    for i, x in enumerate(tr):   # subtitle text from the script when the line count matches, else what was actually said
        text = (f"{names[i]} :  {s['lines'][i][1]}" if len(tr) == len(s["lines"]) else x["text"]).replace("...", "…")
        caps.append(dict(text=text, t0=t + x["start"], t1=t + min(x["end"] + 0.3, end)))
    if s.get("chyron"): shots.append(dict(tag=s["chyron"], t0=t, t1=t + min(end, 4.0)))
    punch = t + (max(x["end"] for x in tr) if tr else end) + 0.1
    for k in (s.get("sfx") or "").split("+"):
        if k == "whoosh": cues.append(("whoosh", max(0, t - 0.4), 0.9))
        elif k == "boom": cues.append(("boom", punch, 1.0))
        elif k == "scratch": cues.append(("scratch", punch - 0.1, 0.8))
        elif k == "laugh": cues.append(("laugh", punch + (0.35 if "boom" in s["sfx"] else 0.1), 0.75))
    if s.get("music") == "hope": hope_at = t
    segs.append((s["id"], t, end)); t += end
run("-f", "lavfi", "-i", f"color=c=black:s={R.W}x{R.H}:r={R.FPS}:d={INTRO}", "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", f"{TMP}/sk_intro.mp4")
asegs = list(segs)
if OUTRO:   # closing call to action in the lead's voice, over the end card
    o0 = t + 1.3; run("-i", f"{D}/outro.mp3", "-af", "loudnorm=I=-13:TP=-1.5:LRA=7,aresample=48000,afade=t=in:d=0.05", "-ac", "2", f"{TMP}/sk_outro.wav")
    asegs.append(("outro", o0, OUTRO["duration"])); caps += [dict(text=x["text"], t0=o0 + x["start"], t1=o0 + x["end"]) for x in OUTRO["subs"]]
total = t + TAIL; open(f"{TMP}/sk.txt", "w").write(f"file '{TMP}/sk_intro.mp4'\n" + "".join(f"file '{TMP}/sk_{i}.mp4'\n" for i, _, _ in segs))
run("-f", "concat", "-safe", "0", "-i", f"{TMP}/sk.txt", "-c", "copy", f"{TMP}/sk_base.mp4")
R.BEATS[:] = [dict(id="end", end=True, t0=t + 0.3, d=0.0)]; titles = R.make_titles(total)
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
