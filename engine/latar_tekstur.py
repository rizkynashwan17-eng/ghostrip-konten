"""Latar foto prosedural untuk feed mockup (tanpa foto stok): denim, kayu, karton, beton.

Pakai: python3 engine/latar_tekstur.py <denim|kayu|karton|beton> out.jpg [seed]
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1350


def noise(h, w, scale, rng):
    """Noise halus multi-oktaf (value noise diperbesar)."""
    out = np.zeros((h, w))
    amp, tot = 1.0, 0
    for s in scale:
        small = rng.random((max(2, h // s), max(2, w // s)))
        im = Image.fromarray((small * 255).astype("uint8")).resize((w, h), Image.BICUBIC)
        out += amp * (np.asarray(im) / 255.0); tot += amp; amp *= 0.5
    return out / tot


def vignette(a, k=0.55):
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2.2) / (H / 2)) ** 2)
    return a * (1 - k * np.clip(d - 0.35, 0, 1.2)[..., None])


def light(a, cx=0.25, cy=0.15, k=0.35):
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt((x / W - cx) ** 2 + (y / H - cy) ** 2)
    return a * (1 + k * np.clip(0.8 - d, 0, 1)[..., None])


def denim(rng):
    y, x = np.mgrid[0:H, 0:W].astype(float)
    # anyaman twill diagonal halus + benang putih (weft) yang tampak acak
    tw = 0.5 + 0.5 * np.sin((x + y * 0.55) * 2 * np.pi / 5.2)
    tw2 = 0.5 + 0.5 * np.sin((x - y * 1.7) * 2 * np.pi / 3.1)
    slub = noise(H, W, (400, 90, 22), rng)
    fine = rng.random((H, W))
    v = 0.48 * tw + 0.12 * tw2 + 0.25 * slub + 0.15 * fine
    fade = noise(H, W, (700, 250), rng)  # pudar khas jeans
    v = v * 0.7 + fade * 0.45
    deep = np.array([12, 26, 58]); mid = np.array([38, 66, 112]); hi = np.array([92, 120, 160])
    v = np.clip(v, 0, 1)[..., None]
    a = np.where(v < 0.55, deep + (mid - deep) * (v / 0.55), mid + (hi - mid) * ((v - 0.55) / 0.45))
    a = light(vignette(a, 0.7), k=0.25)
    im = Image.fromarray(np.clip(a, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.6))
    d = ImageDraw.Draw(im, "RGBA")
    # jahitan oranye ganda: kelim kiri & lengkung saku kanan bawah
    def stitch(pts, gap=0):
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            n = int(np.hypot(x1 - x0, y1 - y0) / 14)
            for j in range(n):
                if j % 2: continue
                t0, t1 = j / n, (j + 0.75) / n
                d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0 + gap), (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1 + gap)], fill=(214, 150, 70, 235), width=4)
    for off in (0, 16):
        stitch([(930 + off, -10), (900 + off, 1360)])
        stitch([(-10, 300 + off), (1090, 345 + off)])
    # garis kelim (lipatan) gelap
    d.line([(916, -10), (886, 1360)], fill=(5, 12, 30, 120), width=10)
    d.line([(-10, 284), (1090, 329)], fill=(5, 12, 30, 110), width=9)
    # paku keling tembaga (jauh dari logo kiri atas & teks bawah)
    for (cx, cy) in [(980, 346)]:
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(70, 45, 25, 255))
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(150, 98, 52, 255))
        d.ellipse([cx - 9, cy - 13, cx + 3, cy - 3], fill=(230, 180, 120, 200))
    return im


def kayu(rng):
    y, x = np.mgrid[0:H, 0:W].astype(float)
    warp = noise(H, W, (900, 300), rng) * 18 + y * 0.004 * 0
    rings = np.sin((x + warp) * 2 * np.pi / 23.0) * 0.5 + np.sin((x * 1.7 + warp * 2) * 2 * np.pi / 61.0) * 0.5
    streak = np.asarray(Image.fromarray((rng.random((8, W)) * 255).astype("uint8")).resize((W, H), Image.BICUBIC)) / 255.0
    grain = rng.random((H, W))
    v = np.clip(0.5 + 0.18 * rings + 0.22 * (streak - 0.5) + 0.08 * (grain - 0.5), 0, 1)[..., None]
    dark = np.array([46, 28, 18]); light_c = np.array([120, 78, 48])
    a = dark + (light_c - dark) * v
    # sambungan papan
    for bx in (360, 720):
        a[:, bx - 2:bx + 2] *= 0.45
    a = light(vignette(a, 0.6), k=0.35)
    return Image.fromarray(np.clip(a, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.5))


def karton(rng):
    y, x = np.mgrid[0:H, 0:W].astype(float)
    fib = noise(H, W, (200, 40, 6), rng)
    flute = 0.5 + 0.5 * np.sin(y * 2 * np.pi / 18)
    v = np.clip(0.55 + 0.25 * (fib - 0.5) * 2 + 0.05 * flute + 0.1 * (rng.random((H, W)) - 0.5), 0, 1)[..., None]
    a = np.array([120, 84, 50]) + (np.array([196, 150, 102]) - np.array([120, 84, 50])) * v
    a = light(vignette(a, 0.6), k=0.3)
    im = Image.fromarray(np.clip(a, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.4))
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([0, 980, W, 1050], fill=(206, 190, 160, 150))  # lakban
    return im


def beton(rng):
    v = noise(H, W, (600, 150, 30, 6), rng)
    v = np.clip(0.5 + (v - 0.5) * 1.6 + 0.08 * (rng.random((H, W)) - 0.5), 0, 1)[..., None]
    a = np.array([40, 52, 56]) + (np.array([120, 132, 134]) - np.array([40, 52, 56])) * v
    a = light(vignette(a, 0.75), k=0.3)
    return Image.fromarray(np.clip(a, 0, 255).astype("uint8"))


if __name__ == "__main__":
    kind, out = sys.argv[1], sys.argv[2]
    rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 7)
    {"denim": denim, "kayu": kayu, "karton": karton, "beton": beton}[kind](rng).save(out, quality=94)
    print(out)
