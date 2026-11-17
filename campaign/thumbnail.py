"""Compose YouTube thumbnails (1280x720): background image + brush-stroke headline banners + emblem + call-out strip.
Usage: python3 thumbnail.py <background.png> <out.jpg> <red|toon>"""
import sys, random, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); W, H = 1280, 720
BF = lambda s: ImageFont.truetype(f"{HERE}/fonts/Baloo2-ExtraBold.ttf", s); LAT = lambda s: ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", s)
M = ImageDraw.Draw(Image.new("L", (8, 8)))
def runs(text, font):
    lat = LAT(int(font.size * 0.84)); out = []
    for ch in text:
        f = font if "ऀ" <= ch <= "ॿ" else lat
        if out and out[-1][1] is f: out[-1][0] += ch
        else: out.append([ch, f])
    return out
def tlen(text, font): return sum(M.textlength(t, font=f) for t, f in runs(text, font))
def fit(text, size, maxw):
    while tlen(text, BF(size)) > maxw and size > 20: size -= 2
    return BF(size)
def draw_text(layer, cx, cy, text, font, fill, stroke=0, sfill=(0, 0, 0, 255)):
    d = ImageDraw.Draw(layer); x = cx - tlen(text, font) / 2; base = cy + font.size * 0.30
    for t, f in runs(text, font): d.text((x, base), t, font=f, fill=fill, anchor="ls", stroke_width=stroke, stroke_fill=sfill); x += d.textlength(t, font=f)
def brush(box, color):
    x0, y0, x1, y1 = box; L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); pts = []; n = 26
    for i in range(n + 1): pts.append((x0 + (x1 - x0) * i / n + random.uniform(-4, 4), y0 + random.uniform(-7, 5)))
    for i in range(6): pts.append((x1 + random.uniform(4, 26), y0 + (y1 - y0) * i / 5 + random.uniform(-3, 3)))
    for i in range(n + 1): pts.append((x1 - (x1 - x0) * i / n + random.uniform(-4, 4), y1 + random.uniform(-5, 7)))
    for i in range(6): pts.append((x0 - random.uniform(4, 26), y1 - (y1 - y0) * i / 5 + random.uniform(-3, 3)))
    d.polygon(pts, fill=color)
    for k in range(10):
        yy = random.uniform(y0 + 4, y1 - 4); d.line([(x0 - random.uniform(20, 60), yy), (x0 + 10, yy)], fill=color, width=random.randint(2, 5))
        yy = random.uniform(y0 + 4, y1 - 4); d.line([(x1 - 10, yy), (x1 + random.uniform(20, 60), yy)], fill=color, width=random.randint(2, 5))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), (0, 0, W, H), L.getchannel("A").filter(ImageFilter.GaussianBlur(6))); return Image.alpha_composite(sh, L)
def banner(im, box, color, text, size, fill, rot=0, stroke=0, sfill=(0, 0, 0, 255)):
    L = brush(box, color); draw_text(L, (box[0] + box[2]) / 2, (box[1] + box[3]) / 2, text, fit(text, size, box[2] - box[0] - 40), fill, stroke, sfill)
    im.alpha_composite(L.rotate(rot, resample=Image.BICUBIC, center=((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)))
def emblem(im, xy=(21, 17)):
    em = Image.open(f"{HERE}/brand/nsui-emblem.png").convert("RGB").resize((150, 150), Image.LANCZOS); m = Image.new("L", (150, 150), 0); ImageDraw.Draw(m).ellipse([1, 1, 148, 148], fill=255)
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse([xy[0] - 7, xy[1] - 7, xy[0] + 157, xy[1] + 157], fill=(255, 255, 255, 255)); im.alpha_composite(ring); im.paste(em, xy, m)
def callout(im, box, text, rot=-1.0):
    L = brush(box, (255, 214, 0, 255)); dd = ImageDraw.Draw(L); x0, y0, x1, y1 = box; cy = (y0 + y1) // 2
    dd.rounded_rectangle([x0 + 22, cy - 29, x0 + 106, cy + 29], 14, fill=(226, 22, 22, 255)); dd.polygon([(x0 + 54, cy - 15), (x0 + 54, cy + 15), (x0 + 82, cy)], fill=(255, 255, 255, 255))
    draw_text(L, (x0 + 126 + x1 - 10) / 2, cy, text, fit(text, 50, x1 - x0 - 150), (190, 16, 16, 255)); im.alpha_composite(L.rotate(rot, resample=Image.BICUBIC, center=((x0 + x1) / 2, cy)))
def tag(im, box, text):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L); dd.rounded_rectangle(list(box), 16, fill=(11, 38, 102, 240)); dd.rounded_rectangle([box[0], box[1], box[0] + 14, box[3]], 7, fill=(255, 153, 51, 255))
    draw_text(L, (box[0] + box[2]) / 2 + 6, (box[1] + box[3]) / 2, text, fit(text, 44, box[2] - box[0] - 40), (255, 255, 255, 255)); im.alpha_composite(L)
def veil(im, depth, strength, tint=(40, 15, 0)):
    g = Image.new("L", (1, H))
    for y in range(H): g.putpixel((0, y), int(max(0, 1 - y / depth) * strength))
    v = Image.new("RGBA", (W, H), tint + (255,)); v.putalpha(g.resize((W, H))); im.alpha_composite(v)

if __name__ == "__main__":
    bg, out, kind = sys.argv[1:4]; random.seed(11); src = Image.open(bg).convert("RGB").resize((W, H), Image.LANCZOS)
    WH, YL, RD, BK, NV = (255, 255, 255, 255), (255, 214, 0, 255), (214, 24, 28, 255), (12, 12, 16, 255), (13, 35, 110, 255)
    if kind == "red":
        im = src.convert("RGBA"); veil(im, 320, 110)
        banner(im, (215, 16, 1065, 124), RD, "लाल बत्ती पर 4 काम !", 98, WH, rot=1.0, stroke=3, sfill=(90, 0, 0, 255))
        banner(im, (250, 140, 1040, 226), BK, "सरकार तो सुनती नहीं...", 68, YL, rot=-1.0)
        banner(im, (440, 240, 1080, 318), WH, "पर ये आप कर सकते हैं", 62, NV, rot=0.8)
        emblem(im); tag(im, (760, 520, 1250, 584), "Red light ON, गाड़ी OFF"); callout(im, (560, 604, 1250, 700), "एक बार ये वीडियो ज़रूर देखें !")
    else:
        shift = 150; im = Image.new("RGBA", (W, H), (176, 170, 160, 255)); top = src.crop((0, 0, W, 6)).resize((W, shift)); im.paste(top, (0, 0)); im.paste(src.crop((0, 0, W, H - shift)), (0, shift)); veil(im, 260, 120, (30, 30, 34))
        banner(im, (205, 14, 1075, 110), RD, "ज़िम्मेदारी किसकी ?", 90, WH, rot=1.0, stroke=3, sfill=(90, 0, 0, 255))
        banner(im, (300, 122, 980, 196), BK, "BJP बोली AAP, AAP बोली BJP", 56, YL, rot=-0.8)
        emblem(im); tag(im, (24, 628, 474, 692), "दिल्ली की साँस बीच में घुटी"); callout(im, (830, 616, 1262, 700), "ज़रूर देखें !")
    im.convert("RGB").save(out, quality=93); print("wrote", out)
