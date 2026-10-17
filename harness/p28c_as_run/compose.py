"""Page preview: background image + the four Deneb renders at their page positions + footer, 1357 x 1920."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
D = os.path.expanduser("~/w/vc"); state = dict(a.split("=") for a in sys.argv[1:])
W, H = 1357, 1920
def lerp(a, b, t): return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
hx = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
bg = Image.new("RGB", (W, H)); px = ImageDraw.Draw(bg)
for y in range(H):
    c = lerp(hx("#120933"), hx("#1E0F4A"), y / 1080) if y < 1080 else lerp(hx("#1E0F4A"), hx("#FFF3DC"), (y - 1080) / 70) if y < 1150 else hx("#FFF3DC")
    px.line([(0, y), (W, y)], fill=c)
bg.save(f"{D}/P28C_Background.png")
page = bg.convert("RGBA")
for vid, (x, y) in {"V1": (0, 0), "V2": (0, 390), "V3": (60, 1160), "V4": (60, 1612)}.items():
    im = Image.open(f"{D}/out/{vid}_{state.get(vid, 'idle')}.png").convert("RGBA"); page.alpha_composite(im, (x, y))
d = ImageDraw.Draw(page); f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
for i, line in enumerate(["105 people, self-reported · 62 men, 41 women, 2 another or not stated · 75 aged 25–44 · about two-thirds in Europe · up to 3 fears per life stage",
                          "Counts are people unless marked picks · Data: Microsoft Fabric Community Halloween survey 2026, provided dataset, unmodified"]):
    w = d.textlength(line, font=f); d.text(((W - w) / 2, 1862 + i * 21), line, fill=(0x5A, 0x54, 0x70), font=f)
    assert w <= 1237, (w, line)
page.convert("RGB").save(f"{D}/page_{'_'.join(state.values()) or 'idle'}.png"); print("ok", [round(d.textlength(l, font=f)) for l in ["x"]])
