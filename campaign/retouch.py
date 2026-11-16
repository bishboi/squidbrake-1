"""Gentle, natural portrait retouch for the whole film: smooth only skin-toned areas (luma) and add a very soft glow.
GRAPH(in_label, out_label) -> ffmpeg filter_complex fragment."""
import os
STRENGTH = float(os.environ.get("RETOUCH", "1.0"))
def graph(i="[0:v]", o="[rt]"):
    s = STRENGTH
    return (f"{i}format=yuv420p,split=3[o][s][k];"
            f"[s]bilateral=sigmaS=5:sigmaR=0.075[sm];"
            f"[k]format=rgba,colorkey=color=0xB47A5C:similarity=0.30:blend=0.15,alphaextract,negate,gblur=sigma=2.5,lut=y=val*{0.8 * s:.2f},format=yuv420p[mk];"
            f"[o][sm][mk]maskedmerge=planes=1[sk];"
            f"[sk]split[g1][g2];[g2]gblur=sigma=22[gb];[g1][gb]blend=c0_mode=screen:c0_opacity={0.13 * s:.3f}:c1_expr=A:c2_expr=A,eq=gamma=1.02{o}")
