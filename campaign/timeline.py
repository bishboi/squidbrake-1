"""Shared timing: processes narration clips and lays beats / shots / captions on the timeline."""
import os, re, subprocess, wave
from beats import BEATS
LEAD, GAP, XF, TAIL, TEMPO = 1.2, 0.3, 0.6, 6.0, 1.10

def _dur(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()

def build(A):
    T = os.path.join(A, "_render"); os.makedirs(T, exist_ok=True); t = LEAD; shots = []; caps = []
    for b in BEATS:
        o = f"{T}/vo_{b['id']}.wav"
        if not os.path.exists(o):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{A}/vo_{b['id']}.wav", "-af",
                "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
                "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
                "silenceremove=stop_periods=-1:stop_duration=0.45:stop_threshold=-42dB:stop_silence=0.4,"
                f"atempo={TEMPO},loudnorm=I=-17:TP=-2:LRA=9,aresample=48000", "-ac", "1", o], check=True)
        b["d"] = _dur(o); b["t0"] = t; span = b["d"] + GAP + (TAIL if b.get("end") else 0); n = len(b["shots"])
        for i, (sid, still, motion) in enumerate(b["shots"]):
            shots.append(dict(id=sid, still=still, motion=motion, t0=t + span * i / n, t1=t + span * (i + 1) / n))
        parts = [p.strip(" —") for p in re.split(r"\.\.\.|(?<=[।?])|—", b.get("cap", b["vo"])) if p.strip(" —")]
        merged = []
        for p in parts:  # merge tiny fragments so captions don't flicker
            if merged and len(merged[-1]) + len(p) < 34: merged[-1] += (" " if merged[-1].endswith(("।", "?")) else " … ") + p
            else: merged.append(p)
        tot = sum(len(m) for m in merged); c = t
        if not b.get("end"):
            for m in merged:
                d = b["d"] * len(m) / tot; caps.append(dict(text=m, t0=c, t1=c + d)); c += d
        b["t1"] = t + span; t += span
    shots[0]["t0"] = 0.0
    for s in shots:  # footage needed per shot, including cross-fade overlap
        s["a"] = max(0.0, s["t0"] - XF / 2); s["b"] = min(t, s["t1"] + XF / 2); s["need"] = s["b"] - s["a"]
    return shots, caps, t
