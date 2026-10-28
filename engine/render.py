"""Mesin konten Ghostrip: render Reels (mp4), Story & Feed (jpg) dari file JSON harian.

Pakai:  python3 engine/render.py konten/2026-10-29.json
Hasil:  media/2026-10-29/<slot>.mp4 / .jpg  + media/2026-10-29/manifest.json
"""
import json, math, os, random, subprocess, sys, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "fonts", "Outfit.ttf")
FPS = 30
NAVY, NAVY2 = (11, 22, 38), (22, 44, 78)
MINT, MINT_D = (125, 232, 200), (64, 190, 160)
WHITE, SOFT = (255, 255, 255), (198, 222, 236)
RED, CARD = (255, 110, 110), (24, 40, 66)
WA = "0815-1704-7930"

_fc = {}
def font(size, weight="Bold"):
    k = (size, weight)
    if k not in _fc:
        f = ImageFont.truetype(FONT, size)
        f.set_variation_by_name(weight)
        _fc[k] = f
    return _fc[k]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(t): t = clamp(t); return 1 - (1 - t) ** 3
def ease_back(t):
    t = clamp(t); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

# ---------------------------------------------------------------- background
_bg = {}
def background(W, H):
    if (W, H) not in _bg:
        y = np.linspace(0, 1, H)[:, None, None]
        top, bot = np.array(NAVY), np.array(NAVY2)
        arr = (top * (1 - y) + bot * y).repeat(W, axis=1).astype(np.uint8)
        im = Image.fromarray(arr, "RGB")
        glow = Image.new("L", (W, H), 0)
        ImageDraw.Draw(glow).ellipse((W * .1, H * .25, W * .9, H * .75), fill=60)
        glow = glow.filter(ImageFilter.GaussianBlur(160))
        im = Image.composite(Image.new("RGB", (W, H), MINT_D), im, glow)
        _bg[(W, H)] = im
    return _bg[(W, H)].copy()

random.seed(7)
PARTICLES = [(random.random(), random.random(), random.uniform(3, 7), random.uniform(.2, .6)) for _ in range(26)]
def particles(d, W, H, t):
    for px, py, r, sp in PARTICLES:
        x = px * W + math.sin(t * sp * 2 + px * 9) * 18
        y = (py * H - t * sp * 60) % H
        d.ellipse((x - r, y - r, x + r, y + r), fill=(60, 110, 120))

# ---------------------------------------------------------------- ghost mascot
_gc = {}
def ghost_img(size, expr="happy", blink=False):
    k = (size, expr, blink)
    if k in _gc: return _gc[k]
    S = 3; w = size * S; h = int(size * 1.18) * S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, w, w), fill=MINT)
    d.rectangle((0, w // 2, w, h - w // 7), fill=MINT)
    n = 4; bw = w / n
    for i in range(n):
        d.ellipse((i * bw, h - w // 4, (i + 1) * bw, h), fill=MINT)
    # shade
    d.ellipse((w * .08, w * .06, w * .38, w * .3), fill=(190, 250, 232))
    ex, ey, er = w * .32, w * .45, w * .075
    eyes = [(ex, ey), (w - ex, ey)]
    dark = (12, 24, 40)
    for i, (x, y) in enumerate(eyes):
        if blink or (expr == "wink" and i == 1):
            d.rounded_rectangle((x - er, y - er * .2, x + er, y + er * .25), radius=int(er * .2), fill=dark)
        elif expr == "shocked":
            d.ellipse((x - er * 1.15, y - er * 1.3, x + er * 1.15, y + er * 1.3), fill=dark)
            d.ellipse((x - er * .4, y - er * .9, x + er * .15, y - er * .3), fill=WHITE)
        else:
            d.ellipse((x - er, y - er * 1.2, x + er, y + er * 1.2), fill=dark)
            d.ellipse((x - er * .35, y - er * .8, x + er * .15, y - er * .25), fill=WHITE)
    mx, my = w / 2, w * .66
    if expr == "shocked":
        d.ellipse((mx - w * .07, my - w * .05, mx + w * .07, my + w * .09), fill=dark)
    elif expr == "sad":
        d.arc((mx - w * .1, my, mx + w * .1, my + w * .14), 200, 340, fill=dark, width=int(w * .025))
    else:
        d.chord((mx - w * .1, my - w * .06, mx + w * .1, my + w * .1), 0, 180, fill=dark)
        d.ellipse((mx - w * .05, my + w * .015, mx + w * .05, my + w * .085), fill=(255, 140, 150))
    for x in (w * .2, w * .8):
        d.ellipse((x - w * .06, my - w * .04, x + w * .06, my + w * .02), fill=(255, 170, 180, 150))
    im = im.resize((size, int(size * 1.18)), Image.LANCZOS)
    _gc[k] = im
    return im

def draw_ghost(canvas, cx, cy, size, t, expr="happy", appear=0.0, scale=1.0):
    p = ease_back((t - appear) / .45)
    if p <= 0: return
    blink = (t % 3.1) < .12 and expr not in ("shocked",)
    s = max(8, int(size * p * scale))
    g = ghost_img(s, expr, blink)
    bob = math.sin(t * 2.4) * size * .04
    tilt = math.sin(t * 1.7) * 4
    g2 = g.rotate(tilt, resample=Image.BICUBIC, expand=True)
    # shadow
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((cx - s * .35, cy + s * .62, cx + s * .35, cy + s * .72), fill=(0, 0, 0, 70))
    canvas.alpha_composite(sh) if canvas.mode == "RGBA" else None
    canvas.paste(g2, (int(cx - g2.width / 2), int(cy - g2.height / 2 + bob)), g2)

# ---------------------------------------------------------------- text helpers
def tokens(text):
    """(kata, sorot, nempel) - nempel=True kalau tidak ada spasi sebelum kata (mis. koma setelah *sorotan*)."""
    out = []; prev = ""
    for part in re.split(r"(\*[^*]+\*)", text):
        if not part: continue
        hl = part.startswith("*")
        body = part.strip("*") if hl else part
        glue_first = bool(out) and not body[:1].isspace() and not prev[-1:].isspace()
        prev = body
        for j, w in enumerate(body.split()):
            out.append((w, hl, glue_first and j == 0))
    return out

def layout(text, f, maxw):
    lines, cur, curw = [], [], 0
    sp = f.getlength(" ")
    for w, hl, glue in tokens(text):
        ww = f.getlength(w)
        gap = 0 if (glue or not cur) else sp
        if cur and not glue and curw + gap + ww > maxw:
            lines.append(cur); cur, curw, gap = [], 0, 0
        cur.append((w, hl, ww, gap)); curw += gap + ww
    if cur: lines.append(cur)
    return lines

def draw_rich(d, text, cx, y, f, maxw, t=99, start=0, stagger=.05, color=WHITE, hl=MINT, lh=1.18, align="center"):
    """Teks dengan kata *sorotan*, muncul kata per kata. Return tinggi blok."""
    lines = layout(text, f, maxw); size = f.size
    i = 0
    for li, line in enumerate(lines):
        lw = sum(x[2] + x[3] for x in line)
        x = cx - lw / 2 if align == "center" else cx
        yy = y + li * size * lh
        pos = []
        for w, ishl, ww, gap in line:
            x += gap
            pos.append((w, ishl, ww, x, ease_out((t - start - i * stagger) / .25)))
            x += ww; i += 1
        # kotak sorotan: satu kotak per deretan kata sorot yang berurutan
        k = 0
        while k < len(pos):
            if pos[k][1]:
                j = k
                while j + 1 < len(pos) and pos[j + 1][1]: j += 1
                p = pos[k][4]
                if p > 0:
                    pad = size * .12; off = (1 - p) * 30
                    fillc = tuple(int(v * p + NAVY[c] * (1 - p)) for c, v in enumerate((30, 70, 80)))
                    d.rounded_rectangle((pos[k][3] - pad, yy + off + size * .14, pos[j][3] + pos[j][2] + pad, yy + off + size * 1.14),
                                        radius=int(size * .24), fill=fillc)
                k = j + 1
            else:
                k += 1
        for w, ishl, ww, xx, p in pos:
            if p > 0:
                off = (1 - p) * 30
                c = hl if ishl else color
                c = tuple(int(c[q] * p + NAVY[q] * (1 - p)) for q in range(3))
                d.text((xx, yy + off), w, font=f, fill=c)
    return len(lines) * size * lh

def nwords(text): return len(tokens(text))

def icon_check(d, x, y, r, ok=True):
    d.ellipse((x - r, y - r, x + r, y + r), fill=MINT if ok else RED)
    k = (12, 24, 40); w = max(3, int(r * .28))
    if ok:
        d.line([(x - r * .45, y), (x - r * .1, y + r * .38), (x + r * .5, y - r * .38)], fill=k, width=w, joint="curve")
    else:
        d.line([(x - r * .38, y - r * .38), (x + r * .38, y + r * .38)], fill=k, width=w)
        d.line([(x - r * .38, y + r * .38), (x + r * .38, y - r * .38)], fill=k, width=w)

def truck(d, x, y, s, c=SOFT):
    d.rounded_rectangle((x, y, x + s * 1.3, y + s * .7), radius=int(s * .08), fill=c)
    d.rounded_rectangle((x + s * 1.35, y + s * .2, x + s * 1.8, y + s * .7), radius=int(s * .1), fill=c)
    d.rectangle((x + s * 1.48, y + s * .28, x + s * 1.7, y + s * .45), fill=NAVY)
    for wx in (x + s * .3, x + s * 1.0, x + s * 1.58):
        d.ellipse((wx - s * .14, y + s * .62, wx + s * .14, y + s * .9), fill=(12, 24, 40))
        d.ellipse((wx - s * .06, y + s * .70, wx + s * .06, y + s * .82), fill=c)

def brand_bar(d, W, H, f=None):
    f = f or font(34, "SemiBold")
    txt = f"@ghostrip.app  ·  Coba gratis 7 hari  ·  WA {WA}"
    d.rounded_rectangle((40, H - 110, W - 40, H - 40), radius=35, fill=(18, 34, 58))
    d.text((W / 2, H - 75), txt, font=f, fill=MINT, anchor="mm")

# ---------------------------------------------------------------- scenes
# Setiap scene: draw(canvas, d, sc, t, W, H) dan events(sc) -> waktu SFX
def sc_hook(c, d, sc, t, W, H):
    f = font(sc.get("size", 92), "ExtraBold")
    top = H * .2
    hgt = draw_rich(d, sc["text"], W / 2, top, f, W - 140, t, .15, .06)
    if sc.get("sub"):
        draw_rich(d, sc["sub"], W / 2, top + hgt + 40, font(48, "Medium"), W - 180, t,
                  .3 + nwords(sc["text"]) * .06, .04, color=SOFT)
    draw_ghost(c, W / 2, H * .68, int(W * .36), t, sc.get("ghost", "shocked"), .05)

def ev_hook(sc): return [0.05] + [0.15 + i * .06 for i in range(0, nwords(sc["text"]), 3)]

def sc_text(c, d, sc, t, W, H):
    f = font(sc.get("size", 80), "ExtraBold")
    top = H * .24
    hgt = draw_rich(d, sc["text"], W / 2, top, f, W - 140, t, .1, .05)
    if sc.get("sub"):
        draw_rich(d, sc["sub"], W / 2, top + hgt + 40, font(50, "Medium"), W - 180, t,
                  .25 + nwords(sc["text"]) * .05, .035, color=SOFT)
    if sc.get("truck"):
        x = (t * 260) % (W + 500) - 400
        truck(d, x, H * .64, 140, (120, 160, 190))
    draw_ghost(c, W * .74, H * .74, int(W * .26), t, sc.get("ghost", "happy"), .2)

def ev_text(sc): return [0.1, 0.2 + nwords(sc["text"]) * .05]

def sc_list(c, d, sc, t, W, H):
    top = H * .14 if H > 1500 else H * .1
    hgt = draw_rich(d, sc["title"], W / 2, top, font(sc.get("size", 74), "ExtraBold"), W - 140, t, .05, .04)
    y = top + hgt + 60
    ok = sc.get("mark", "check") == "check"
    fi = font(sc.get("item_size", 52 if H > 1500 else 46), "SemiBold")
    for i, item in enumerate(sc["items"]):
        a = .5 + i * sc.get("gap", .55)
        p = ease_out((t - a) / .35)
        lines = layout(item, fi, W - 300)
        rh = max(130 if H > 1500 else 120, len(lines) * fi.size * 1.2 + 60)
        if p > 0:
            x0 = 70 - (1 - p) * 300
            d.rounded_rectangle((x0, y, x0 + W - 140, y + rh), radius=36, fill=CARD)
            mk = sc["marks"][i] if "marks" in sc else ok
            icon_check(d, x0 + 70, y + rh / 2, 30 * ease_back((t - a - .1) / .35) + .01, mk)
            draw_rich(d, item, x0 + 130, y + (rh - len(lines) * fi.size * 1.2) / 2, fi, W - 300, align="left")
        y += rh + 26
    if sc.get("ghost"):
        gy = max(y + 150, H * .84) if H > 1500 else y + (H - 130 - y) / 2 + 10
        if gy < H - 140:
            draw_ghost(c, W * .5, gy, int(W * (.2 if H > 1500 else .17)), t, sc["ghost"], .3)

def ev_list(sc): return [0.05] + [.5 + i * sc.get("gap", .55) for i in range(len(sc["items"]))]

def sc_chat(c, d, sc, t, W, H):
    top = H * .12
    if sc.get("title"):
        top += draw_rich(d, sc["title"], W / 2, top, font(64, "ExtraBold"), W - 140, t, .05, .04) + 30
    px0, px1 = 70, W - 70
    fb = font(48, "Medium"); fn = font(34, "SemiBold")
    hh = 150
    for m in sc["messages"]:
        hh += len(layout(m["text"], fb, W * .58)) * fb.size * 1.22 + 90 + 24
    top = max(top, H * .46 - hh / 2)
    d.rounded_rectangle((px0, top, px1, top + hh + 30), radius=50, fill=(14, 28, 48))
    d.rounded_rectangle((px0, top, px1, top + 110), radius=50, fill=(20, 40, 66))
    d.rectangle((px0, top + 60, px1, top + 110), fill=(20, 40, 66))
    d.text((px0 + 50, top + 55), sc.get("group", "Grup Armada"), font=font(40, "SemiBold"), fill=WHITE, anchor="lm")
    y = top + 150
    for i, m in enumerate(sc["messages"]):
        a = .4 + i * sc.get("gap", 1.0)
        p = ease_back((t - a) / .35)
        lines = layout(m["text"], fb, W * .58)
        bw = max(sum(x[2] + x[3] for x in ln) for ln in lines) + 60
        bw = max(bw, fn.getlength(m["from"]) + 60)
        bh = len(lines) * fb.size * 1.22 + 90
        me = m.get("me", False)
        if p > 0:
            x = px1 - 40 - bw if me else px0 + 40
            sh = (1 - clamp(p)) * 40
            d.rounded_rectangle((x, y + sh, x + bw, y + bh + sh), radius=32,
                                fill=(38, 110, 96) if me else (34, 54, 84))
            d.text((x + 30, y + 22 + sh), m["from"], font=fn, fill=MINT if not me else (200, 255, 236))
            draw_rich(d, m["text"], x + 30, y + 66 + sh, fb, W * .58, align="left")
        y += bh + 24
    if sc.get("ghost"):
        draw_ghost(c, W * .78, H * .86, int(W * .22), t, sc["ghost"], .2)

def ev_chat(sc): return [.4 + i * sc.get("gap", 1.0) for i in range(len(sc["messages"]))]

def _rupiah_digits(s): return int(re.sub(r"\D", "", s) or 0)
def _fmt(n): return "Rp " + f"{n:,}".replace(",", ".")

def sc_calc(c, d, sc, t, W, H):
    top = H * .1
    top += draw_rich(d, sc.get("title", "Hitung trip pakai *Ghostrip*"), W / 2, top, font(66, "ExtraBold"), W - 140, t, .05, .04) + 40
    x0, x1 = 90, W - 90
    y1 = top + 50 + 80 + 140 + 82 * len(sc["rows"]) + 20 + 180 + (60 if sc.get("note") else 0) + 30
    p0 = ease_out((t - .15) / .4)
    d.rounded_rectangle((x0, top + (1 - p0) * 200, x1, y1 + (1 - p0) * 200), radius=56, fill=(240, 252, 248))
    oy = (1 - p0) * 200; y = top + 50 + oy
    d.text((x0 + 50, y), "Ghostrip", font=font(44, "ExtraBold"), fill=(20, 120, 100)); y += 80
    d.rounded_rectangle((x0 + 40, y, x1 - 40, y + 100), radius=28, fill=(220, 246, 238))
    d.text((x0 + 70, y + 50), sc.get("route", "Palembang → Jambi"), font=font(42, "SemiBold"), fill=(12, 24, 40), anchor="lm")
    y += 140
    fr, fv = font(42, "Medium"), font(42, "Bold")
    for i, (k, v) in enumerate(sc["rows"]):
        a = .6 + i * .35
        p = ease_out((t - a) / .3)
        if p > 0:
            col = tuple(int(12 + (1 - p) * 220) for _ in range(3))
            d.text((x0 + 60, y), k, font=fr, fill=(70, 90, 110) if p >= 1 else col)
            d.text((x1 - 60, y), v, font=fv, fill=(12, 24, 40) if p >= 1 else col, anchor="ra")
            d.line((x0 + 60, y + 62, x1 - 60, y + 62), fill=(214, 230, 226), width=2)
        y += 82
    a = .6 + len(sc["rows"]) * .35 + .2
    p = ease_out((t - a) / 1.0)
    if p > 0:
        y += 20
        d.rounded_rectangle((x0 + 40, y, x1 - 40, y + 150), radius=36, fill=(20, 120, 100))
        d.text((x0 + 80, y + 75), "Harga trip", font=font(40, "SemiBold"), fill=(210, 255, 240), anchor="lm")
        tot = _rupiah_digits(sc["total"])
        val = _fmt(int(tot * p) // 1000 * 1000) if p < 1 else sc["total"]
        d.text((x1 - 80, y + 75), val, font=font(54, "ExtraBold"), fill=WHITE, anchor="rm")
        y += 180
    if sc.get("note"):
        pn = ease_back((t - a - 1.1) / .4)
        if pn > 0:
            fnn = font(38, "Bold"); tw = fnn.getlength(sc["note"]) + 90
            d.rounded_rectangle((W / 2 - tw / 2, y, W / 2 + tw / 2, y + 80), radius=40, fill=(22, 21, 19))
            d.text((W / 2, y + 40), sc["note"], font=fnn, fill=MINT, anchor="mm")
    draw_ghost(c, W * .5, max(y1 + 230, H * .84), int(W * .2), t, sc.get("ghost", "wink"), 1.2)

def ev_calc(sc):
    n = len(sc["rows"]); return [.15] + [.6 + i * .35 for i in range(n)] + [.6 + n * .35 + .2, .6 + n * .35 + 1.3]

def sc_cta(c, d, sc, t, W, H):
    s = 1 + math.sin(t * 5) * .015
    draw_ghost(c, W / 2, H * .3, int(W * .34), t, "happy", .0, s)
    d.text((W / 2, H * .47), "Ghostrip", font=font(110, "ExtraBold"), fill=MINT, anchor="mm")
    hgt = draw_rich(d, sc.get("text", "Coba *GRATIS 7 hari*"), W / 2, H * .53, font(70, "ExtraBold"), W - 160, t, .3, .06)
    y = H * .53 + hgt + 40
    p = ease_back((t - .9) / .4)
    if p > 0:
        f = font(48, "Bold"); txt = sc.get("button", f"Chat WA {WA}")
        tw = f.getlength(txt) + 120; pulse = 1 + math.sin(t * 6) * .03 * (t > 1.3)
        bw, bh = tw * p * pulse, 120 * p * pulse
        d.rounded_rectangle((W / 2 - bw / 2, y, W / 2 + bw / 2, y + bh), radius=int(bh / 2), fill=MINT)
        if p > .8: d.text((W / 2, y + bh / 2), txt, font=f, fill=(12, 24, 40), anchor="mm")
    if sc.get("sub"):
        draw_rich(d, sc["sub"], W / 2, y + 170, font(42, "Medium"), W - 200, t, 1.3, .03, color=SOFT)

def ev_cta(sc): return [0.0, .3, .9]

def sc_question(c, d, sc, t, W, H):
    d.rounded_rectangle((70, H * .16, W - 70, H * .2 + 60), radius=40, fill=(20, 40, 66))
    d.text((W / 2, H * .18 + 30), sc.get("label", "PERTANYAAN HARI INI"), font=font(38, "Bold"), fill=MINT, anchor="mm")
    hgt = draw_rich(d, sc["text"], W / 2, H * .27, font(78, "ExtraBold"), W - 160, t, .1, .04)
    y = H * .27 + hgt + 50; fo = font(46, "SemiBold")
    for i, o in enumerate(sc.get("options", [])):
        p = ease_out((t - .6 - i * .3) / .3)
        if p > 0:
            d.rounded_rectangle((110, y, W - 110, y + 120), radius=60, fill=(240, 252, 248) if i == 0 else (32, 56, 88))
            d.text((W / 2, y + 60), o, font=fo, fill=(12, 24, 40) if i == 0 else WHITE, anchor="mm")
        y += 145
    if sc.get("sub"):
        draw_rich(d, sc["sub"], W / 2, y + 30, font(40, "Medium"), W - 200, color=SOFT)
    draw_ghost(c, W * .5, H * .83, int(W * .22), t, sc.get("ghost", "happy"), .2)

def ev_question(sc): return [.1] + [.6 + i * .3 for i in range(len(sc.get("options", [])))]

SCENES = {"hook": (sc_hook, ev_hook), "text": (sc_text, ev_text), "list": (sc_list, ev_list),
          "chat": (sc_chat, ev_chat), "calc": (sc_calc, ev_calc), "cta": (sc_cta, ev_cta),
          "question": (sc_question, ev_question)}

def frame(sc, t, W, H, fade_in=True, static=False):
    im = background(W, H).convert("RGBA")
    d = ImageDraw.Draw(im)
    particles(d, W, H, t)
    SCENES[sc["type"]][0](im, d, sc, t, W, H)
    if static and sc["type"] != "cta":
        brand_bar(d, W, H)
    out = im.convert("RGB")
    if fade_in and t < .18:
        out = Image.blend(background(W, H), out, clamp(t / .18))
    return out

# ---------------------------------------------------------------- audio
SR = 44100
def _env(n, a=.005, r=.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / r)

def music(dur, seed=0):
    rng = np.random.default_rng(seed)
    n = int(dur * SR); out = np.zeros(n)
    bpm = 104; beat = 60 / bpm
    prog = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
    if seed % 2: prog = [prog[2], prog[3], prog[0], prog[1]]
    b = 0
    while b * beat < dur:
        st = int(b * beat * SR); chord = prog[(b // 4) % 4]
        k = np.arange(int(.18 * SR)); kick = np.sin(2 * np.pi * (55 + 90 * np.exp(-k / 900)) * k / SR) * _env(len(k), .002, .08)
        e = min(n, st + len(k)); out[st:e] += .55 * kick[:e - st]
        hs = int((b + .5) * beat * SR)
        if hs < n:
            h = rng.standard_normal(int(.05 * SR)) * _env(int(.05 * SR), .001, .012); e = min(n, hs + len(h)); out[hs:e] += .12 * h[:e - hs]
        for j in range(2):
            ps = int((b + j * .5) * beat * SR)
            f = chord[(b * 2 + j) % 3] * 2
            m = int(.28 * SR); tt = np.arange(m) / SR
            pl = (np.sin(2 * np.pi * f * tt) + .3 * np.sin(4 * np.pi * f * tt)) * _env(m, .003, .12)
            e = min(n, ps + m)
            if ps < n: out[ps:e] += .16 * pl[:e - ps]
        if b % 4 == 0:
            m = int(4 * beat * SR); tt = np.arange(m) / SR
            pad = sum(np.sin(2 * np.pi * f * tt + .3) for f in chord) / 3 * np.minimum(1, tt / .4) * np.exp(-tt / 3)
            bass = np.sin(2 * np.pi * chord[0] / 2 * tt) * np.exp(-tt / 1.5)
            e = min(n, st + m); out[st:e] += .1 * pad[:e - st] + .25 * bass[:e - st]
        b += 1
    fade = np.ones(n); fl = int(.8 * SR); fade[-fl:] = np.linspace(1, 0, fl)
    return out * fade * .5

def sfx_pop(n=None):
    m = int(.09 * SR); tt = np.arange(m) / SR
    return np.sin(2 * np.pi * (500 + 900 * tt / .09) * tt) * _env(m, .002, .03) * .35

def sfx_whoosh():
    m = int(.35 * SR); rng = np.random.default_rng(3)
    w = rng.standard_normal(m); w = np.convolve(w, np.ones(30) / 30, "same")
    return w * np.sin(np.linspace(0, np.pi, m)) * .5

def write_wav(path, x):
    import wave
    x = np.clip(x, -1, 1); pcm = (x * 32000).astype(np.int16)
    st = np.stack([pcm, pcm], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())

# ---------------------------------------------------------------- outputs
def render_reel(post, out_mp4, seed=0):
    W, H = 1080, 1920
    scenes = post["scenes"]
    total = sum(s.get("dur", 3.0) for s in scenes)
    audio = music(total, seed)
    t0 = 0
    for i, s in enumerate(scenes):
        if i:
            w = sfx_whoosh(); a = int(t0 * SR); e = min(len(audio), a + len(w)); audio[a:e] += w[:e - a] * .5
        for et in SCENES[s["type"]][1](s):
            p = sfx_pop(); a = int((t0 + et) * SR)
            if a < len(audio): e = min(len(audio), a + len(p)); audio[a:e] += p[:e - a]
        t0 += s.get("dur", 3.0)
    wav = out_mp4 + ".wav"; write_wav(wav, audio)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_mp4]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    cover = None
    for s in scenes:
        dur = s.get("dur", 3.0)
        for fi in range(int(round(dur * FPS))):
            fr = frame(s, fi / FPS, W, H)
            pr.stdin.write(fr.tobytes())
    pr.stdin.close(); pr.wait(); os.remove(wav)
    # cover = scene pertama, keadaan akhir
    cov = frame(scenes[0], scenes[0].get("dur", 3.0) - .05, W, H)
    cov.save(out_mp4.replace(".mp4", "-cover.jpg"), quality=90)
    return total

def render_static(scene, out_jpg, W, H):
    frame(scene, 30.0, W, H, fade_in=False, static=True).save(out_jpg, quality=92)

def main(spec_path):
    spec = json.load(open(spec_path))
    day = spec["date"]; outdir = os.path.join(ROOT, "media", day); os.makedirs(outdir, exist_ok=True)
    manifest = []
    for i, post in enumerate(spec["posts"]):
        slot, kind = post["slot"], post["kind"]
        if kind == "reel":
            path = os.path.join(outdir, f"{slot}.mp4")
            dur = render_reel(post, path, seed=hash(day + slot) % 1000)
            files = {"media": path, "cover": path.replace(".mp4", "-cover.jpg"), "dur": dur}
        elif kind == "story":
            path = os.path.join(outdir, f"{slot}.jpg"); render_static(post["scene"], path, 1080, 1920)
            files = {"media": path}
        elif kind == "feed":
            path = os.path.join(outdir, f"{slot}.jpg"); render_static(post["scene"], path, 1080, 1350)
            files = {"media": path}
        else:
            raise ValueError(kind)
        manifest.append({"slot": slot, "kind": kind, **{k: (os.path.relpath(v, ROOT) if isinstance(v, str) else v) for k, v in files.items()}})
        print("OK", slot, files)
    json.dump(manifest, open(os.path.join(outdir, "manifest.json"), "w"), indent=1)

if __name__ == "__main__":
    main(sys.argv[1])
