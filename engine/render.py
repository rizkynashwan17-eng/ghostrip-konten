"""Mesin konten Ghostrip v2 - gaya mengikuti video manual Rizky.

Gaya: latar navy-teal gelap, karakter Bos (kumis, kemeja biru) di balik meja, Sopir (topi oranye),
hantu Ghostrip 3D (assets/ghost_wave.png), bar dialog bawah dengan label BOS/SOPIR/HANTU,
kartu FAKTA + sumber, truk flat oranye-teal, penutup ikon app + pil "GRATIS 7 HARI".

Pakai:  python3 engine/render.py konten/2026-11-01.json
Hasil:  media/<tanggal>/<slot>.mp4 / .jpg (+ -N.jpg untuk carousel) + manifest.json
Format JSON: lihat PANDUAN.md.
"""
import json, math, os, random, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "fonts", "Outfit.ttf")
FPS = 30
WA = "0815-1704-7930"

BG_TOP, BG_BOT = (15, 34, 42), (16, 24, 32)
GLOW = (32, 86, 84)
MINT, MINT_D = (110, 224, 198), (60, 192, 166)
ORANGE, ORANGE_L = (247, 154, 91), (255, 192, 143)
YELLOW, RED, PINK = (242, 201, 76), (226, 84, 84), (240, 127, 127)
WHITE, INK, SOFT, MUTED = (255, 255, 255), (16, 24, 32), (196, 214, 222), (110, 128, 140)
CARD, CARD2 = (20, 34, 44), (28, 44, 56)
DESK, DESK2 = (78, 104, 116), (36, 50, 60)
SKIN, SKIN2, HAIR = (248, 214, 181), (238, 182, 140), (58, 42, 34)
SHIRT, SHIRT2 = (141, 181, 217), (120, 160, 198)
LABEL_COL = {"BOS": ORANGE, "SOPIR": YELLOW, "HANTU": MINT, "ADMIN": (150, 190, 240), "CUSTOMER": (190, 170, 240)}

_fc = {}
def font(size, weight="Bold"):
    k = (int(size), weight)
    if k not in _fc:
        f = ImageFont.truetype(FONT, int(size)); f.set_variation_by_name(weight); _fc[k] = f
    return _fc[k]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(t): t = clamp(t); return 1 - (1 - t) ** 3
def ease_back(t):
    t = clamp(t); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def mix(c1, c2, p): return tuple(int(c1[i] * p + c2[i] * (1 - p)) for i in range(3))

# ------------------------------------------------------------------ background
_bg = {}
def background(W, H, glow=True, desk=False):
    k = (W, H, glow, desk)
    if k in _bg: return _bg[k].copy()
    y = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(BG_TOP) * (1 - y) + np.array(BG_BOT) * y).repeat(W, 1)
    if glow:
        yy, xx = np.mgrid[0:H, 0:W]
        d = np.sqrt(((xx - W / 2) / (W * .62)) ** 2 + ((yy - H * .42) / (H * .36)) ** 2)
        g = np.clip(1 - d, 0, 1)[:, :, None] ** 1.6
        arr = arr * (1 - g * .55) + np.array(GLOW) * g * .55
    im = Image.fromarray(arr.astype(np.uint8), "RGB")
    if desk:
        d = ImageDraw.Draw(im); top = int(H * .792)
        d.rectangle((0, top + 54, W, H), fill=DESK2)
        grad = np.linspace(0, 1, H - top - 54)[:, None, None]
        band = (np.array(DESK2) * (1 - grad) + np.array((22, 32, 40)) * grad).repeat(W, 1).astype(np.uint8)
        im.paste(Image.fromarray(band, "RGB"), (0, top + 54))
        d.rounded_rectangle((0, top, W, top + 56), radius=10, fill=DESK)
    _bg[k] = im
    return im.copy()

def sparkles(d, W, H, t, n=5):
    rnd = random.Random(11)
    for i in range(n):
        x, y = rnd.uniform(.06, .94) * W, rnd.uniform(.18, .72) * H
        s = (8 + rnd.random() * 10) * (0.7 + 0.3 * math.sin(t * 2.4 + i))
        d.polygon([(x, y - s * 2.2), (x + s * .5, y - s * .5), (x + s * 2.2, y), (x + s * .5, y + s * .5),
                   (x, y + s * 2.2), (x - s * .5, y + s * .5), (x - s * 2.2, y), (x - s * .5, y - s * .5)], fill=(214, 245, 238))

# ------------------------------------------------------------------ text
def tokens(text):
    out = []; prev = ""
    for part in re.split(r"(\*[^*]+\*)", text):
        if not part: continue
        hl = part.startswith("*"); body = part.strip("*") if hl else part
        glue = bool(out) and not body[:1].isspace() and not prev[-1:].isspace(); prev = body
        for j, w in enumerate(body.split()): out.append((w, hl, glue and j == 0))
    return out

def layout(text, f, maxw):
    lines, cur, curw = [], [], 0; sp = f.getlength(" ")
    for w, hl, glue in tokens(text):
        ww = f.getlength(w); gap = 0 if (glue or not cur) else sp
        if cur and not glue and curw + gap + ww > maxw: lines.append(cur); cur, curw, gap = [], 0, 0
        cur.append((w, hl, ww, gap)); curw += gap + ww
    if cur: lines.append(cur)
    return lines

def rich(d, text, cx, y, f, maxw, color=WHITE, hl=MINT, lh=1.2, align="center", p=1.0):
    """Teks dengan *sorotan* berwarna. Return tinggi."""
    lines = layout(text, f, maxw); size = f.size
    for li, line in enumerate(lines):
        lw = sum(a[2] + a[3] for a in line)
        x = cx - lw / 2 if align == "center" else cx
        yy = y + li * size * lh + (1 - p) * 24
        for w, ishl, ww, gap in line:
            x += gap
            d.text((x, yy), w, font=f, fill=mix(hl if ishl else color, BG_TOP, p))
            x += ww
    return len(lines) * size * lh

def text_h(text, f, maxw, lh=1.2): return len(layout(text, f, maxw)) * f.size * lh
def nwords(t): return len(tokens(t))

def pill(d, cx, cy, text, f, bg, fg, padx=34, h=None, anchor="mm"):
    tw = f.getlength(text); h = h or f.size * 1.75
    x0 = cx - tw / 2 - padx if anchor == "mm" else cx
    d.rounded_rectangle((x0, cy - h / 2, x0 + tw + padx * 2, cy + h / 2), radius=int(h / 2), fill=bg)
    d.text((x0 + padx + tw / 2, cy), text, font=f, fill=fg, anchor="mm")
    return tw + padx * 2

def shadow_card(im, box, radius, fill, shadow=60, outline=None, width=3):
    x0, y0, x1, y1 = [int(v) for v in box]
    sh = Image.new("L", im.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 16, x1, y1 + 22), radius=radius, fill=shadow)
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    im.paste(Image.new("RGB", im.size, (5, 10, 14)), (0, 0), sh)
    ImageDraw.Draw(im).rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=fill, outline=outline, width=width if outline else 0)

def rotated_paste(im, layer, cx, cy, angle):
    l2 = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    im.paste(l2, (int(cx - l2.width / 2), int(cy - l2.height / 2)), l2)

# ------------------------------------------------------------------ characters
_cc = {}
def person(kind="bos", mood="neutral", arms=False, size=300):
    """Gambar Bos/Sopir (setengah badan) RGBA, lebar ~1.6*size. Cache."""
    k = (kind, mood, arms, size)
    if k in _cc: return _cc[k]
    S = 2; s = size * S; W = int(s * 1.9); H = int(s * 1.55)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = W / 2; hr = s * .42; hy = s * .5
    sopir = kind == "sopir"
    skin = (205, 150, 108) if sopir else SKIN; skin2 = (180, 124, 86) if sopir else SKIN2
    shirt = (44, 62, 87) if sopir else SHIRT; shirt2 = (34, 50, 72) if sopir else SHIRT2
    # body
    bt = hy + hr * .82
    d.rounded_rectangle((cx - s * .62, bt, cx + s * .62, H + s * .3), radius=int(s * .32), fill=shirt)
    if sopir:
        d.polygon([(cx - s * .3, bt + 4), (cx + s * .3, bt + 4), (cx + s * .22, bt + s * .16), (cx - s * .22, bt + s * .16)], fill=(236, 236, 236))
    else:
        d.polygon([(cx - s * .2, bt + 2), (cx, bt + s * .22), (cx + s * .2, bt + 2)], fill=(236, 244, 250))
        d.polygon([(cx - s * .12, bt + 2), (cx, bt + s * .14), (cx + s * .12, bt + 2)], fill=shirt2)
    if arms:
        for sgn in (-1, 1):
            sx = cx + sgn * s * .5; ex = cx + sgn * s * .82
            d.line([(sx, bt + s * .25), (ex, bt - s * .25), (ex, hy - s * .1)], fill=shirt, width=int(s * .2), joint="curve")
            d.ellipse((ex - s * .13, hy - s * .3, ex + s * .13, hy - s * .04), fill=skin)
    # neck & head
    d.rectangle((cx - s * .12, hy + hr * .5, cx + s * .12, bt + s * .05), fill=skin2)
    for sgn in (-1, 1):
        ex = cx + sgn * hr * .98
        d.ellipse((ex - s * .07, hy - s * .02, ex + s * .07, hy + s * .14), fill=skin2)
    head = Image.new("RGBA", (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(head)
    hd.ellipse((cx - hr, hy - hr, cx + hr, hy + hr * 1.05), fill=skin)
    # shading gradient bottom
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).ellipse((cx - hr * 1.1, hy + hr * .25, cx + hr * 1.1, hy + hr * 1.6), fill=70)
    sh = sh.filter(ImageFilter.GaussianBlur(s * .06))
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).ellipse((cx - hr, hy - hr, cx + hr, hy + hr * 1.05), fill=255)
    sh = Image.fromarray(np.minimum(np.asarray(sh), np.asarray(mask)))
    head.paste(Image.new("RGBA", (W, H), skin2 + (255,)), (0, 0), sh)
    im.alpha_composite(head); d = ImageDraw.Draw(im)
    # hair / cap
    if sopir:
        d.chord((cx - hr * 1.02, hy - hr * 1.08, cx + hr * 1.02, hy + hr * .55), 180, 360, fill=ORANGE)
        d.rounded_rectangle((cx - hr * .2, hy - hr * .38, cx + hr * 1.3, hy - hr * .18), radius=int(s * .05), fill=(222, 128, 68))
        d.ellipse((cx - s * .04, hy - hr * 1.0, cx + s * .04, hy - hr * .92), fill=(222, 128, 68))
    else:
        d.chord((cx - hr * 1.05, hy - hr * 1.1, cx + hr * 1.05, hy + hr * .35), 180, 360, fill=HAIR)
        d.ellipse((cx - hr * .95, hy - hr * .55, cx - hr * .55, hy - hr * .05), fill=HAIR)
        d.ellipse((cx + hr * .55, hy - hr * .55, cx + hr * .95, hy - hr * .05), fill=HAIR)
        d.chord((cx - hr * .7, hy - hr * .55, cx + hr * .3, hy - hr * .05), 0, 180, fill=skin)
    # face
    ink = (40, 28, 24); ey = hy + hr * .12; ex = hr * .38; w = max(3, int(s * .028))
    if mood == "happy":
        for sg in (-1, 1): d.arc((cx + sg * ex - s * .07, ey - s * .05, cx + sg * ex + s * .07, ey + s * .06), 200, 340, fill=ink, width=w)
    elif mood in ("sad", "tired"):
        for sg in (-1, 1):
            d.arc((cx + sg * ex - s * .07, ey - s * .06, cx + sg * ex + s * .07, ey + s * .05), 20, 160, fill=ink, width=w)
            d.line([(cx + sg * ex - s * .09 * sg, ey - s * .14), (cx + sg * ex + s * .07 * sg, ey - s * .1)], fill=ink, width=w)
    elif mood == "shocked":
        for sg in (-1, 1):
            d.ellipse((cx + sg * ex - s * .045, ey - s * .06, cx + sg * ex + s * .045, ey + s * .05), fill=ink)
            d.arc((cx + sg * ex - s * .08, ey - s * .2, cx + sg * ex + s * .08, ey - s * .08), 200, 340, fill=ink, width=w)
    else:  # neutral / think
        for sg in (-1, 1): d.ellipse((cx + sg * ex - s * .04, ey - s * .05, cx + sg * ex + s * .04, ey + s * .04), fill=ink)
        if mood == "think":
            d.line([(cx - ex - s * .08, ey - s * .13), (cx - ex + s * .06, ey - s * .16)], fill=ink, width=w)
    for sg in (-1, 1):
        d.ellipse((cx + sg * hr * .58 - s * .08, hy + hr * .32, cx + sg * hr * .58 + s * .08, hy + hr * .48), fill=(244, 150, 150, 150))
    my = hy + hr * .5
    # mustache
    for sg in (-1, 1):
        d.ellipse((cx + (sg * s * .13) - s * .14, my - s * .045, cx + (sg * s * .13) + s * .14, my + s * .05), fill=HAIR)
    mo = my + s * .1
    if mood == "happy":
        d.chord((cx - s * .1, mo - s * .06, cx + s * .1, mo + s * .08), 0, 180, fill=(120, 40, 40))
    elif mood in ("sad", "tired"):
        d.arc((cx - s * .08, mo, cx + s * .08, mo + s * .1), 200, 340, fill=ink, width=w)
    elif mood == "shocked":
        d.ellipse((cx - s * .05, mo - s * .03, cx + s * .05, mo + s * .08), fill=(120, 40, 40))
    else:
        d.line([(cx - s * .05, mo + s * .02), (cx + s * .05, mo + s * .02)], fill=ink, width=w)
    im = im.resize((W // S, H // S), Image.LANCZOS)
    _cc[k] = im
    return im

_ghost = None
def ghost_sprite(h):
    global _ghost
    if _ghost is None: _ghost = Image.open(os.path.join(ROOT, "assets", "ghost_wave.png")).convert("RGBA")
    k = ("g", int(h))
    if k not in _cc:
        _cc[k] = _ghost.resize((int(_ghost.width * h / _ghost.height), int(h)), Image.LANCZOS)
    return _cc[k]

def draw_ghost(im, cx, cy, h, t, appear=0.0):
    p = ease_back((t - appear) / .5)
    if p <= 0: return
    g = ghost_sprite(max(10, h * p))
    # glow
    gl = Image.new("L", im.size, 0)
    ImageDraw.Draw(gl).ellipse((cx - h * .7, cy - h * .6, cx + h * .7, cy + h * .6), fill=90)
    gl = gl.filter(ImageFilter.GaussianBlur(h * .3))
    im.paste(Image.new("RGB", im.size, (60, 160, 150)), (0, 0), gl)
    bob = math.sin(t * 2.2) * h * .05
    rotated_paste(im, g, cx, cy + bob, math.sin(t * 1.6) * 4)

def draw_char(im, spec, t, W, H, desk_top):
    """spec: 'bos:happy', 'bos:shocked:up', 'sopir:sad', 'ghost'."""
    if not spec: return
    parts = spec.split(":"); kind = parts[0]
    if kind == "ghost":
        draw_ghost(im, W * .76, H * .5, 300, t, .1); return
    mood = parts[1] if len(parts) > 1 else "neutral"; arms = "up" in parts
    pos = "left" if "left" in parts else ("right" if "right" in parts else "center")
    size = 300
    p = ease_out((t - .05) / .45)
    img = person(kind, mood, arms, size)
    cx = {"center": W / 2, "left": W * .26, "right": W * .74}[pos]
    bounce = math.sin(t * 3) * 4 if mood == "happy" else 0
    y = desk_top - img.height + size * .38 + (1 - p) * 160 + bounce
    im.paste(img, (int(cx - img.width / 2), int(y)), img)

# ------------------------------------------------------------------ illustrations
BOX1, BOX2, TAPE = (247, 168, 104), (255, 196, 146), (108, 195, 168)
def box(d, x, y, w, h, tape=True):
    if w < 14 or h < 14: return
    d.rounded_rectangle((x, y, x + w, y + h), radius=int(min(w, h) * .12), fill=BOX1)
    d.rounded_rectangle((x + 4, y + 4, x + w - 4, y + h * .45), radius=int(min(w, h) * .1), fill=BOX2)
    if tape: d.rectangle((x + w * .42, y, x + w * .58, y + h), fill=TAPE)

def truck(d, x, y, s, load="box", flip=False, dual=False):
    """Truk flat (x,y = kiri-bawah roda), s = lebar dasar."""
    if s < 40: return
    cab_w = s * .32; bed_w = s * .72
    bx = x; cx0 = x + bed_w - s * .02
    if flip: cx0, bx = x, x + cab_w - s * .02
    by = y - s * .14
    d.rounded_rectangle((x, by - s * .07, x + bed_w + cab_w, by + s * .02), radius=int(s * .03), fill=MINT_D)
    d.rounded_rectangle((cx0, by - s * .36, cx0 + cab_w, by), radius=int(s * .07), fill=(26, 38, 50))
    wx = cx0 + cab_w * (.2 if not flip else .1)
    d.rounded_rectangle((wx, by - s * .3, wx + cab_w * .6, by - s * .18), radius=int(s * .025), fill=(190, 240, 230))
    for wi, wxx in enumerate((x + s * .17, x + bed_w * .78, cx0 + cab_w * .62 if not flip else cx0 + cab_w * .4)):
        r = s * .075
        if dual and wi < 2:
            d.ellipse((wxx - r + r * .9, by - r * .2, wxx + r + r * .9, by + r * 1.8), fill=(12, 18, 26))
        d.ellipse((wxx - r, by - r * .2, wxx + r, by + r * 1.8), fill=(22, 30, 40))
        d.ellipse((wxx - r * .4, by + r * .4, wxx + r * .4, by + r * 1.2), fill=(190, 240, 230))
    if load == "box":
        box(d, bx + s * .04, by - s * .44, bed_w * .86, s * .37)
    elif load == "over":
        for i in range(4):
            box(d, bx + s * .04 + (i % 2) * s * .02, by - s * .4 - i * s * .32, bed_w * .82, s * .3)
        d.line([(bx + s * .02, by - s * 1.4), (bx + s * .02, by - s * .07)], fill=(170, 110, 60), width=max(2, int(s * .012)))
        d.line([(bx + bed_w * .88, by - s * 1.4), (bx + bed_w * .88, by - s * .07)], fill=(170, 110, 60), width=max(2, int(s * .012)))
    elif load == "tank":
        d.rounded_rectangle((bx + s * .02, by - s * .4, bx + bed_w * .95, by - s * .06), radius=int(s * .17), fill=(200, 214, 222))
        d.rectangle((bx + s * .02, by - s * .26, bx + bed_w * .95, by - s * .2), fill=ORANGE)
    elif load == "wing":
        d.rounded_rectangle((bx + s * .02, by - s * .5, bx + bed_w * .95, by - s * .06), radius=int(s * .04), fill=(220, 232, 238))
        d.line([(bx + s * .02, by - s * .28), (bx + bed_w * .95, by - s * .28)], fill=(170, 190, 200), width=max(2, int(s * .01)))

def road(d, W, y, t, speed=260, h=320):
    d.rectangle((0, y, W, y + h), fill=(34, 49, 59))
    d.rectangle((0, y - 14, W, y), fill=(60, 80, 92))
    off = (t * speed) % 240
    for i in range(-1, W // 240 + 2):
        x = i * 240 - off
        d.rounded_rectangle((x, y + h * .58, x + 130, y + h * .58 + 16), radius=8, fill=(232, 207, 115))

def gantry(d, W, y, text, t):
    d.rectangle((120, y, 146, y + 410), fill=(92, 115, 128)); d.rectangle((W - 146, y, W - 120, y + 410), fill=(92, 115, 128))
    d.rounded_rectangle((100, y - 70, W - 100, y), radius=14, fill=(47, 70, 84))
    d.text((W / 2, y - 35), text, font=font(40, "Bold"), fill=(242, 205, 104), anchor="mm")
    on = (t % 1.0) < .6
    d.ellipse((W / 2 - 13, y + 10, W / 2 + 13, y + 36), fill=MINT if on else (40, 70, 70))

def trees(d, W, y):
    for x in (90, W - 90, W * .3):
        d.rectangle((x - 5, y - 120, x + 5, y), fill=(52, 76, 88)); d.ellipse((x - 46, y - 190, x + 46, y - 100), fill=(44, 66, 78))

def icon(d, kind, cx, cy, s, col=None):
    if s < 20: return
    col = col or MINT
    if kind == "fuel":
        d.rounded_rectangle((cx - s * .35, cy - s * .5, cx + s * .2, cy + s * .5), radius=int(s * .08), fill=ORANGE)
        d.rounded_rectangle((cx - s * .25, cy - s * .38, cx + s * .1, cy - s * .1), radius=int(s * .04), fill=(255, 230, 205))
        d.line([(cx + s * .2, cy - s * .2), (cx + s * .38, cy - s * .05), (cx + s * .38, cy + s * .35)], fill=ORANGE, width=int(s * .07))
    elif kind == "clock":
        d.ellipse((cx - s * .5, cy - s * .5, cx + s * .5, cy + s * .5), fill=(236, 242, 246))
        d.line([(cx, cy), (cx, cy - s * .32)], fill=INK, width=int(s * .07)); d.line([(cx, cy), (cx + s * .22, cy + s * .1)], fill=INK, width=int(s * .07))
    elif kind == "scale":
        d.rounded_rectangle((cx - s * .5, cy + s * .2, cx + s * .5, cy + s * .42), radius=int(s * .08), fill=(92, 115, 128))
        d.rounded_rectangle((cx - s * .3, cy - s * .35, cx + s * .3, cy + s * .2), radius=int(s * .1), fill=(236, 242, 246))
        d.text((cx, cy - s * .08), "kg", font=font(s * .28, "Bold"), fill=INK, anchor="mm")
    elif kind == "toll":
        d.rectangle((cx - s * .5, cy - s * .1, cx + s * .5, cy + s * .5), fill=(47, 70, 84))
        d.rectangle((cx - s * .5, cy - s * .2, cx + s * .5, cy - s * .1), fill=ORANGE)
        d.line([(cx - s * .3, cy + s * .1), (cx + s * .55, cy + s * .1)], fill=RED, width=int(s * .08))
    elif kind == "doc":
        d.rounded_rectangle((cx - s * .36, cy - s * .48, cx + s * .36, cy + s * .48), radius=int(s * .06), fill=(236, 242, 246))
        for i in range(4): d.line([(cx - s * .22, cy - s * .25 + i * s * .16), (cx + s * .22, cy - s * .25 + i * s * .16)], fill=MUTED, width=int(s * .05))
    elif kind == "money":
        d.rounded_rectangle((cx - s * .55, cy - s * .32, cx + s * .55, cy + s * .32), radius=int(s * .08), fill=(120, 200, 150))
        d.ellipse((cx - s * .16, cy - s * .16, cx + s * .16, cy + s * .16), fill=(90, 170, 120))
    elif kind == "warn":
        d.polygon([(cx, cy - s * .5), (cx + s * .55, cy + s * .45), (cx - s * .55, cy + s * .45)], fill=YELLOW)
        d.text((cx, cy + s * .08), "!", font=font(s * .6, "ExtraBold"), fill=INK, anchor="mm")

def draw_illus(im, d, name, t, W, cy, s=1.0):
    """Preset ilustrasi di tengah (cy = pusat vertikal)."""
    p = ease_back((t - .15) / .5)
    if p <= 0: return
    sc = s * p
    if name in ("truck", "truck_box", "truck_over", "truck_tank", "truck_wing", "truck_empty"):
        load = {"truck": "box", "truck_box": "box", "truck_over": "over", "truck_tank": "tank", "truck_wing": "wing", "truck_empty": "none"}[name]
        sz = 380 * sc; drive = math.sin(t * 6) * 3
        truck(d, W / 2 - sz * .52, cy + sz * .3 + drive, sz, load)
    elif name == "two_trucks":
        sz = 240 * sc
        truck(d, W / 2 - sz * .9, cy + sz * .1, sz, "box"); truck(d, W / 2 - sz * .3, cy + sz * .5, sz, "box")
    elif name in ("fuel", "clock", "scale", "toll", "doc", "money", "warn"):
        icon(d, name, W / 2, cy, 220 * sc)

# ------------------------------------------------------------------ scene parts
def draw_title(d, sc, t, W, y):
    h = 0
    if sc.get("kicker"):
        k = sc["kicker"]; f = font(34, "Bold")
        p = ease_out(t / .3)
        if p > 0: pill(d, W / 2, y + 28, k, f, MINT, INK)
        h += 82
    if sc.get("title"):
        f = font(sc.get("title_size", 66), "ExtraBold")
        h += rich(d, sc["title"], W / 2, y + h, f, W - 150, p=ease_out((t - .05) / .35)) + 16
    if sc.get("badge"):
        b = sc["badge"]; col = {"red": RED, "orange": ORANGE, "mint": MINT}.get(b.get("color", "red"), RED)
        p = ease_back((t - .35) / .4)
        if p > 0:
            f = font(46, "ExtraBold"); tw = f.getlength(b["text"]) + 80; hh = 96
            lay = Image.new("RGBA", (int(tw + 20), hh + 20), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
            ld.rounded_rectangle((10, 10, tw + 10, hh + 10), radius=hh // 2, fill=col)
            ld.text((tw / 2 + 10, hh / 2 + 10), b["text"], font=f, fill=WHITE if col == RED else INK, anchor="mm")
            lay = lay.resize((max(1, int(lay.width * p)), max(1, int(lay.height * p))))
            d._image.paste(lay, (int(W / 2 - lay.width / 2), int(y + h + 10)), lay)
        h += 130
    return h

def fact_card(im, d, f, t, W, y, start=.2):
    """{"n":1,"head":"Zero ODOL","body":"...","source":"Kontan, Okt 2025"}"""
    p = ease_out((t - start) / .4)
    if p <= 0: return 0
    x0, x1 = 70, W - 70
    fb = font(f.get("body_size", 44), "Medium"); bw = x1 - x0 - 80
    bh = text_h(f["body"], fb, bw, 1.32)
    h = 120 + bh + (60 if f.get("source") else 20)
    yy = y + (1 - p) * 40
    shadow_card(im, (x0, yy, x1, yy + h), 40, CARD, outline=(70, 160, 145), width=3)
    d = ImageDraw.Draw(im)
    label = f.get("label") or (f"FAKTA {f['n']}" if f.get("n") else "FAKTA")
    w = pill(d, x0 + 30, yy + 4, label, font(32, "Bold"), MINT, INK, padx=26, h=60, anchor="lm")
    d.text((x0 + 30 + w + 24, yy + 4), f.get("head", ""), font=font(44, "Bold"), fill=WHITE, anchor="lm")
    rich(d, f["body"], x0 + 40, yy + 70, fb, bw, color=SOFT, hl=MINT, lh=1.32, align="left")
    if f.get("source"):
        d.text((x1 - 30, yy + h - 30), "Sumber: " + f["source"], font=font(28, "Medium"), fill=MUTED, anchor="rm")
    return h

def stat_card(im, d, s, t, W, y, start=.4):
    """{"label":"Solar, operasional, tarif truk","value":"ikut naik ×2","color":"red"}"""
    p = ease_back((t - start) / .45)
    if p <= 0: return 0
    col = {"red": RED, "mint": (30, 160, 130), "orange": (220, 120, 50), "ink": INK}.get(s.get("color", "red"), RED)
    h = 200 if s.get("label") else 150
    x0, x1 = 140, W - 140; yy = y + (1 - min(p, 1)) * 30
    shadow_card(im, (x0, yy, x1, yy + h), 40, WHITE)
    d = ImageDraw.Draw(im)
    if s.get("label"): d.text((W / 2, yy + 52), s["label"], font=font(40, "SemiBold"), fill=(80, 100, 112), anchor="mm")
    d.text((W / 2, yy + (128 if s.get("label") else 75)), s["value"], font=font(s.get("size", 86), "ExtraBold"), fill=col, anchor="mm")
    return h

def compare(im, d, c, t, W, y):
    """{"left":{"illus":"truck_over","label":"Dulu: 1 trip","color":"red"},"right":{...}}"""
    for i, side in enumerate(("left", "right")):
        s = c[side]; p = ease_back((t - .3 - i * .5) / .45)
        if p <= 0: continue
        cx = W * (.27 if i == 0 else .73)
        col = {"red": PINK, "mint": MINT, "orange": ORANGE, "white": WHITE}.get(s.get("color", "white"), WHITE)
        ill = s.get("illus", "truck")
        sz = 330 * p
        if ill in ("truck", "truck_box", "truck_over", "truck_tank", "truck_wing", "truck_empty"):
            load = {"truck": "box", "truck_box": "box", "truck_over": "over", "truck_tank": "tank", "truck_wing": "wing", "truck_empty": "none"}[ill]
            truck(d, cx - sz * .5, y + 340, sz, load, dual=s.get("dual", False))
        elif ill == "two_trucks":
            truck(d, cx - sz * .62, y + 250, sz * .75, "box"); truck(d, cx - sz * .3, y + 340, sz * .75, "box")
        else:
            icon(d, ill, cx, y + 230, 170 * p)
        d.text((cx, y + 410), s["label"], font=font(50, "ExtraBold"), fill=col, anchor="mm")
        if s.get("sub"): d.text((cx, y + 470), s["sub"], font=font(36, "Medium"), fill=SOFT, anchor="mm")
    if t > .6: d.text((W / 2, y + 250), "→", font=font(70, "Bold"), fill=MINT, anchor="mm")
    return 500

def calendar_card(im, d, c, t, W, y):
    p = ease_back((t - .1) / .45)
    if p <= 0: return 0
    w, h = 560, 270
    lay = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle((30, 30, w + 30, h + 30), radius=30, fill=WHITE)
    ld.rounded_rectangle((30, 30, w + 30, 120), radius=30, fill=RED); ld.rectangle((30, 90, w + 30, 120), fill=RED)
    ld.text((w / 2 + 30, 75), c.get("top", "MULAI BERLAKU"), font=font(34, "Bold"), fill=WHITE, anchor="mm")
    ld.text((w / 2 + 30, 200), c["date"], font=font(70, "ExtraBold"), fill=INK, anchor="mm")
    lay = lay.resize((max(1, int(lay.width * p)), max(1, int(lay.height * p))))
    rotated_paste(im, lay, W / 2, y + h / 2 + 20, 3)
    return h + 60

def list_cards(im, d, items, t, W, y, mark="check", gap=.55, start=.4):
    f = font(46, "SemiBold"); hh = 0
    for i, it in enumerate(items):
        p = ease_out((t - start - i * gap) / .35)
        lines = layout(it if isinstance(it, str) else it["text"], f, W - 330)
        rh = max(124, len(lines) * f.size * 1.22 + 64)
        if p > 0:
            x0 = 70 - (1 - p) * 200
            ImageDraw.Draw(im).rounded_rectangle((x0, y + hh, x0 + W - 140, y + hh + rh), radius=36, fill=CARD2)
            d = ImageDraw.Draw(im); cy = y + hh + rh / 2; r = 34
            m = it.get("mark", mark) if isinstance(it, dict) else mark
            if m == "num":
                d.ellipse((x0 + 56 - r, cy - r, x0 + 56 + r, cy + r), fill=MINT)
                d.text((x0 + 56, cy), str(i + 1), font=font(38, "ExtraBold"), fill=INK, anchor="mm")
            else:
                d.ellipse((x0 + 56 - r, cy - r, x0 + 56 + r, cy + r), fill=MINT if m == "check" else RED)
                k = INK; w = 8
                if m == "check": d.line([(x0 + 40, cy), (x0 + 52, cy + 12), (x0 + 74, cy - 12)], fill=k, width=w, joint="curve")
                else:
                    d.line([(x0 + 44, cy - 12), (x0 + 68, cy + 12)], fill=WHITE, width=w); d.line([(x0 + 44, cy + 12), (x0 + 68, cy - 12)], fill=WHITE, width=w)
            rich(d, it if isinstance(it, str) else it["text"], x0 + 120, cy - len(lines) * f.size * 1.22 / 2, f, W - 330, align="left", lh=1.22)
        hh += rh + 24
    return hh

def chat_box(im, d, c, t, W, y):
    """{"name":"Customer","lines":["Pak, minta harga Fuso ya:", "1. ..."]}"""
    p = ease_out((t - .1) / .4)
    if p <= 0: return 0
    x0, x1 = 120, W - 120; f = font(40, "Medium")
    bh = sum(text_h(l, f, x1 - x0 - 120, 1.3) for l in c["lines"]) + 60
    h = 110 + bh + 40; yy = y + (1 - p) * 40
    shadow_card(im, (x0, yy, x1, yy + h), 36, (36, 54, 68))
    d = ImageDraw.Draw(im)
    d.ellipse((x0 + 30, yy + 32, x0 + 72, yy + 74), fill=(110, 128, 140))
    d.text((x0 + 90, yy + 53), c.get("name", "Customer"), font=font(36, "SemiBold"), fill=WHITE, anchor="lm")
    d.rounded_rectangle((x0 + 30, yy + 100, x1 - 30, yy + 100 + bh), radius=24, fill=WHITE)
    ly = yy + 130
    for i, l in enumerate(c["lines"]):
        pl = clamp((t - .5 - i * .4) / .3)
        if pl > 0: ly += rich(d, l, x0 + 60, ly, f, x1 - x0 - 120, color=mix(INK, WHITE, pl), hl=(30, 150, 125), align="left", lh=1.3)
    return h

def say_bar(im, d, s, t, W, H, start=.25):
    if not s: return
    p = ease_out((t - start) / .3)
    if p <= 0: return
    who = s.get("who", "BOS").upper(); col = LABEL_COL.get(who, ORANGE)
    f = font(44, "Bold"); txt = "“" + s["text"] + "”"
    lines = layout(txt, f, W - 180); th = len(lines) * f.size * 1.25
    y1 = H - 210; y0 = y1 - th - 100
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle((50, y0, W - 50, y1), radius=44, fill=(12, 18, 24, int(235 * p)))
    im.paste(lay, (0, 0), lay); d = ImageDraw.Draw(im)
    pill(d, 90, y0 + 42, who, font(32, "ExtraBold"), col, INK, padx=26, h=56, anchor="lm")
    rich(d, txt, W / 2, y0 + 80, f, W - 180, color=mix(WHITE, (12, 18, 24), p), lh=1.25)

def cta(im, d, sc, t, W, H):
    _icon = _cc.get("icon")
    if _icon is None:
        ic = Image.open(os.path.join(ROOT, "assets", "icon.png")).convert("RGBA").resize((420, 420), Image.LANCZOS)
        m = Image.new("L", ic.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 419, 419), radius=96, fill=255)
        ic.putalpha(m); _cc["icon"] = _icon = ic
    p = ease_back(t / .5)
    if p > 0:
        ic = _icon.resize((max(1, int(420 * p)), max(1, int(420 * p))), Image.LANCZOS)
        y = H * .2 + math.sin(t * 2) * 6
        im.paste(ic, (int(W / 2 - ic.width / 2), int(y + (420 - ic.height) / 2)), ic)
    d = ImageDraw.Draw(im)
    pt = ease_out((t - .3) / .35)
    if pt > 0:
        d.text((W / 2, H * .2 + 530), "Ghostrip", font=font(150, "ExtraBold"), fill=mix(WHITE, BG_TOP, pt), anchor="mm")
        d.text((W / 2, H * .2 + 640), sc.get("tagline", "Harga trip & quotation dalam 30 detik"), font=font(44, "Medium"), fill=mix(MINT, BG_TOP, pt), anchor="mm")
    pb = ease_back((t - .7) / .45)
    if pb > 0:
        f = font(76, "ExtraBold"); txt = sc.get("button", "GRATIS 7 HARI"); tw = f.getlength(txt) + 160
        lay = Image.new("RGBA", (int(tw + 40), 170), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle((20, 25, tw + 20, 145), radius=60, fill=ORANGE)
        ld.text((tw / 2 + 20, 85), txt, font=f, fill=INK, anchor="mm")
        s = pb * (1 + math.sin(t * 5) * .02 * (t > 1.4))
        lay = lay.resize((max(1, int(lay.width * s)), max(1, int(lay.height * s))))
        rotated_paste(im, lay, W / 2, H * .2 + 790, 2.5)
    pw = ease_back((t - 1.0) / .45)
    if pw > 0:
        d = ImageDraw.Draw(im); y = H * .2 + 930
        f = font(54, "Bold"); parts = [("Komen ", INK), ("DEMO", (30, 150, 125)), (" untuk coba", INK)]
        tw = sum(f.getlength(a) for a, _ in parts); bw = (tw + 130) * pw
        d.rounded_rectangle((W / 2 - bw / 2, y - 52 * pw, W / 2 + bw / 2, y + 52 * pw), radius=int(52 * pw), fill=WHITE)
        if pw > .8:
            x = W / 2 - tw / 2
            for a, c in parts: d.text((x, y), a, font=f, fill=c, anchor="lm"); x += f.getlength(a)
        if sc.get("sub"):
            d.text((W / 2, y + 110), sc["sub"], font=font(38, "Medium"), fill=SOFT, anchor="mm")

# ------------------------------------------------------------------ scene
def frame(sc, t, W, H, static=False):
    typ = sc.get("type", "explain")
    has_person = bool(sc.get("char")) and not sc["char"].startswith("ghost")
    road_scene = typ == "road"
    im = background(W, H, glow=sc.get("glow", True), desk=has_person and not road_scene)
    d = ImageDraw.Draw(im)
    desk_top = H * .792
    if typ == "cta":
        cta(im, d, sc, t, W, H)
        if sc.get("char", "").startswith("ghost"): draw_ghost(im, W * .84, H * .14, 200, t, .9)
        say_bar(im, ImageDraw.Draw(im), sc.get("say"), t, W, H, .4)
        return im
    if sc.get("sparkles"): sparkles(d, W, H, t)
    if road_scene:
        trees(d, W, H * .64); road(d, W, int(H * .64), t, sc.get("speed", 260))
        if sc.get("gantry"): gantry(d, W, int(H * .44), sc["gantry"], t)
        ld = sc.get("truck", "box"); sz = 380
        x = W / 2 - sz * .52 + (sc.get("drive", 0) and ((t * 120) % (W + 600) - W / 2 - 300))
        truck(d, x, H * .64 + 70 + math.sin(t * 7) * 3, sz, ld)
    top = H * (.11 if H > 1500 else .07)
    y = top + draw_title(d, sc, t, W, top) + 30
    d = ImageDraw.Draw(im)
    if typ == "calendar":
        y += calendar_card(im, d, sc["calendar"], t, W, y) + 30
    if sc.get("chat"): y += chat_box(im, ImageDraw.Draw(im), sc["chat"], t, W, y) + 30
    if sc.get("fact"): y += fact_card(im, ImageDraw.Draw(im), sc["fact"], t, W, y, .25 if sc.get("title") else .1) + 40
    if sc.get("compare"): y += compare(im, ImageDraw.Draw(im), sc["compare"], t, W, y) + 20
    if sc.get("items"): y += list_cards(im, ImageDraw.Draw(im), sc["items"], t, W, y, sc.get("mark", "check"), sc.get("gap", .55)) + 20
    if sc.get("stat"): y += stat_card(im, ImageDraw.Draw(im), sc["stat"], t, W, y, .6 if (sc.get("compare") or sc.get("fact")) else .3) + 30
    if sc.get("illus") and not road_scene:
        limit = desk_top - 60 if has_person else H - 260
        cy = y + (limit - y) / 2 if not has_person else y + 200
        draw_illus(im, ImageDraw.Draw(im), sc["illus"], t, W, min(cy, limit - 120))
    d = ImageDraw.Draw(im)
    if sc.get("char"):
        if sc["char"].startswith("ghost"): draw_ghost(im, W * .8, (y + 120) if H > 1500 else H * .7, 260 if H > 1500 else 210, t, .3)
        else: draw_char(im, sc["char"], t, W, H, desk_top if not road_scene else H * .9)
    if static:
        d = ImageDraw.Draw(im)
        f = font(32, "SemiBold"); txt = f"@ghostrip.app  ·  Coba gratis 7 hari  ·  WA {WA}"
        d.rounded_rectangle((40, H - 100, W - 40, H - 36), radius=32, fill=(10, 16, 22))
        d.text((W / 2, H - 68), txt, font=f, fill=MINT, anchor="mm")
    else:
        say_bar(im, ImageDraw.Draw(im), sc.get("say"), t, W, H)
    return im

def scene_events(sc):
    ev = [0.05]
    if sc.get("badge"): ev.append(.35)
    if sc.get("fact"): ev.append(.25)
    if sc.get("items"): ev += [.4 + i * sc.get("gap", .55) for i in range(len(sc["items"]))]
    if sc.get("stat"): ev.append(.6)
    if sc.get("compare"): ev += [.3, .8]
    if sc.get("type") == "cta": ev += [.7, 1.0]
    return ev

# ------------------------------------------------------------------ audio
SR = 44100
def _env(n, a=.005, r=.2):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / r)

def music(dur, seed=0):
    rng = np.random.default_rng(seed); n = int(dur * SR); out = np.zeros(n)
    bpm = 96; beat = 60 / bpm
    progs = [[[220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7], [164.8, 207.7, 246.9]],
             [[261.6, 329.6, 392.0], [196.0, 246.9, 293.7], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6]]]
    prog = progs[seed % 2]; b = 0
    while b * beat < dur:
        st = int(b * beat * SR); chord = prog[(b // 4) % 4]
        k = np.arange(int(.2 * SR)); kick = np.sin(2 * np.pi * (50 + 80 * np.exp(-k / 900)) * k / SR) * _env(len(k), .002, .09)
        e = min(n, st + len(k)); out[st:e] += .45 * kick[:e - st]
        if b % 2 == 1:
            sn = rng.standard_normal(int(.12 * SR)) * _env(int(.12 * SR), .001, .04); e = min(n, st + len(sn)); out[st:e] += .1 * sn[:e - st]
        for j in range(2):
            ps = int((b + j * .5) * beat * SR)
            if ps >= n: continue
            f = chord[(b * 2 + j) % 3] * 2; m = int(.3 * SR); tt = np.arange(m) / SR
            pl = (np.sin(2 * np.pi * f * tt) + .25 * np.sin(6 * np.pi * f * tt)) * _env(m, .004, .14)
            e = min(n, ps + m); out[ps:e] += .13 * pl[:e - ps]
        if b % 4 == 0:
            m = int(4 * beat * SR); tt = np.arange(m) / SR
            pad = sum(np.sin(2 * np.pi * f * tt + .3) for f in chord) / 3 * np.minimum(1, tt / .5) * np.exp(-tt / 3)
            bass = np.sin(2 * np.pi * chord[0] / 2 * tt) * np.exp(-tt / 1.6)
            e = min(n, st + m); out[st:e] += .09 * pad[:e - st] + .22 * bass[:e - st]
        b += 1
    fl = int(.8 * SR); out[-fl:] *= np.linspace(1, 0, fl)
    return out * .5

def sfx_pop():
    m = int(.09 * SR); tt = np.arange(m) / SR
    return np.sin(2 * np.pi * (520 + 900 * tt / .09) * tt) * _env(m, .002, .03) * .3

def sfx_whoosh():
    m = int(.35 * SR); w = np.random.default_rng(3).standard_normal(m); w = np.convolve(w, np.ones(30) / 30, "same")
    return w * np.sin(np.linspace(0, np.pi, m)) * .45

def write_wav(path, x):
    import wave
    pcm = (np.clip(x, -1, 1) * 32000).astype(np.int16); st = np.stack([pcm, pcm], 1)
    with wave.open(path, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())

# ------------------------------------------------------------------ output
def load_voice(post):
    """Suara Gemini TTS (voice/out/<voice_id>/NN.wav) -> list array 44.1 kHz per baris `say`, atau None."""
    vid = post.get("voice_id")
    if not vid: return None
    d = os.path.join(ROOT, "voice", "out", vid)
    if not os.path.exists(os.path.join(d, "done.json")): return None
    import wave
    out = []
    for fn in sorted(f for f in os.listdir(d) if f.endswith(".wav")):
        with wave.open(os.path.join(d, fn)) as w:
            sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
        n2 = int(len(x) * SR / sr); x = np.interp(np.linspace(0, len(x) - 1, n2), np.arange(len(x)), x)
        # buang hening di awal/akhir
        nz = np.where(np.abs(x) > .01)[0]
        if len(nz): x = x[max(0, nz[0] - 800): nz[-1] + 1600]
        out.append(x * (0.9 / max(.05, np.abs(x).max())))
    return out

def voice_requests(post):
    """Baris dialog untuk request TTS (urutan = scene yang punya `say`)."""
    mood_tone = {"shocked": "kaget", "think": "penasaran", "happy": "senang", "sad": "kecewa", "neutral": "santai"}
    out = []
    for s in post["scenes"]:
        if not s.get("say"): continue
        who = s["say"].get("who", "BOS").upper(); tone = s["say"].get("tone")
        if not tone:
            mood = (s.get("char") or "").split(":")[1] if ":" in (s.get("char") or "") else ""
            tone = "mengajak" if s.get("type") == "cta" else ("menjelaskan" if who == "HANTU" else mood_tone.get(mood, "santai"))
            if s["say"]["text"].strip().endswith("?"): tone = "penasaran"
        out.append({"who": who, "tone": tone, "text": s["say"]["text"].replace("&", "dan")})
    return out

def render_reel(post, out_mp4, seed=0):
    W, H = 1080, 1920; scenes = [dict(s) for s in post["scenes"]]
    voices = load_voice(post); vi = 0; vstarts = []
    if voices:
        for s in scenes:
            if s.get("say") and vi < len(voices):
                need = .35 + len(voices[vi]) / SR + .5
                s["dur"] = max(s.get("dur", 3.5), need); vstarts.append((s, voices[vi])); vi += 1
    total = sum(s.get("dur", 3.5) for s in scenes)
    audio = music(total, seed) * (.45 if voices else 1.0); t0 = 0
    for i, s in enumerate(scenes):
        if i:
            w = sfx_whoosh(); a = int(t0 * SR); e = min(len(audio), a + len(w)); audio[a:e] += w[:e - a]
        for et in scene_events(s):
            p = sfx_pop() * (.6 if voices else 1); a = int((t0 + et) * SR)
            if a < len(audio): e = min(len(audio), a + len(p)); audio[a:e] += p[:e - a]
        for ss, v in vstarts:
            if ss is s:
                a = int((t0 + .35) * SR); e = min(len(audio), a + len(v)); audio[a:e] += v[:e - a] * .95
        t0 += s.get("dur", 3.5)
    wav = out_mp4 + ".wav"; write_wav(wav, audio)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_mp4]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE); prev = None
    for s in scenes:
        dur = s.get("dur", 3.5); nf = int(round(dur * FPS))
        for fi in range(nf):
            fr = frame(s, fi / FPS, W, H)
            if prev is not None and fi < 6: fr = Image.blend(prev, fr, (fi + 1) / 7)
            pr.stdin.write(fr.tobytes())
        prev = fr
    pr.stdin.close(); pr.wait(); os.remove(wav)
    frame(scenes[0], scenes[0].get("dur", 3.5) - .05, W, H).save(out_mp4.replace(".mp4", "-cover.jpg"), quality=90)
    return total

def render_static(sc, out, W, H):
    frame(sc, 30.0, W, H, static=sc.get("type") != "cta").save(out, quality=92)

def main(spec_path):
    spec = json.load(open(spec_path)); day = spec["date"]
    outdir = os.path.join(ROOT, "media", day); os.makedirs(outdir, exist_ok=True)
    mpath = os.path.join(outdir, "manifest.json")
    manifest = json.load(open(mpath)) if os.path.exists(mpath) else []
    rel = lambda v: os.path.relpath(v, ROOT) if isinstance(v, str) else ([os.path.relpath(x, ROOT) for x in v] if isinstance(v, list) else v)
    for post in spec["posts"]:
        slot, kind = post["slot"], post["kind"]
        if kind == "reel":
            path = os.path.join(outdir, f"{slot}.mp4"); dur = render_reel(post, path, seed=sum(map(ord, day + slot)))
            files = {"media": path, "cover": path.replace(".mp4", "-cover.jpg"), "dur": dur}
        elif kind == "story":
            path = os.path.join(outdir, f"{slot}.jpg"); render_static(post["scene"], path, 1080, 1920); files = {"media": path}
        elif kind == "feed":
            path = os.path.join(outdir, f"{slot}.jpg"); render_static(post["scene"], path, 1080, 1350); files = {"media": path}
        elif kind == "carousel":
            paths = []
            for j, sc in enumerate(post["slides"], 1):
                pth = os.path.join(outdir, f"{slot}-{j}.jpg"); render_static(sc, pth, 1080, 1350); paths.append(pth)
            files = {"media": paths}
        else:
            raise ValueError(kind)
        manifest = [m for m in manifest if m["slot"] != slot] + [{"slot": slot, "kind": kind, **{k: rel(v) for k, v in files.items()}}]
        print("OK", slot, rel(files["media"]))
    json.dump(manifest, open(mpath, "w"), indent=1)

def make_requests(spec_path):
    """Tulis voice/requests/<date>-<slot>.json untuk setiap reel + set voice_id di JSON konten."""
    spec = json.load(open(spec_path)); os.makedirs(os.path.join(ROOT, "voice", "requests"), exist_ok=True)
    for post in spec["posts"]:
        if post["kind"] != "reel": continue
        vid = post.get("voice_id") or f"{spec['date']}-{post['slot']}"; post["voice_id"] = vid
        json.dump({"id": vid, "lines": voice_requests(post)}, open(os.path.join(ROOT, "voice", "requests", vid + ".json"), "w"), ensure_ascii=False, indent=1)
        print("request", vid)
    json.dump(spec, open(spec_path, "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    if sys.argv[1] == "--voice-requests": make_requests(sys.argv[2])
    else: main(sys.argv[1])
