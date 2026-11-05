"""Feed FOTO-MOCKUP (PATEN 5 Nov 2026): foto kiriman Rizky + layar aplikasi Ghostrip, susunan brand tetap.

Pakai: python3 engine/foto_feed.py konten/<tanggal>-....json   (render semua post yang scene-nya punya "foto")
Output: media/<tanggal>/<slot>.jpg (1080x1350) + manifest.json (gaya "mockup-foto").

scene (di post kind "feed", slot "feed-foto", jam 12:00):
  foto   : "foto/<tanggal>-<nama>.jpg"  (foto asli kiriman Rizky, disimpan di repo)
  mode   : "ganti-layar"  -> foto SUDAH memuat tablet/HP/laptop; layar lama diganti layar Ghostrip (perspektif + cahaya mengikuti foto)
           "overlay"      -> foto polos; perangkat digambar di atasnya (engine/feed_mockup.py: device hp|tablet|laptop, screen, rot, x, y, cy, scale)
  quad   : (ganti-layar) 4 sudut layar di foto, piksel foto ASLI, urutan kiri-atas, kanan-atas, kanan-bawah, kiri-bawah
  aspek  : (ganti-layar) lebar/tinggi layar di foto; >=1 lanskap (judul + 2 kartu), <1 potret (1 tangkapan layar)
  layar  : {"judul":"Hitung trip","url":"ghostrip.id/hitung","kartu":["hasil","home"]}  (nama file di remotion/public/iklan3d/*.png)
  title, sub : judul tebal & sub-judul (judul pakai \\n untuk baris baru)
Isi layar = tangkapan layar ASLI dengan data FIKTIF; label DATA SIMULASI otomatis.
"""
import json, os, sys, html
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "remotion/public/iklan3d")
FONT = "file://" + os.path.join(ROOT, "fonts/Outfit.ttf")


def layar_web(aspek, L):
    """Tampilan DESKTOP: jendela browser berisi website ghostrip.id (assets/web/ghostrip-id-1440.png, tangkapan layar penuh 1440 px).
    L["web"] = {"scroll": px dari atas halaman, "menubar": true/false (laptop), "notch": true/false, "url": "ghostrip.id"}"""
    Wd = L["web"]; W = 1440; H = int(round(W / aspek))
    mb = 30 if Wd.get("menubar") else 0; tb = 64
    site = "file://" + os.path.join(ROOT, "assets/web/ghostrip-id-1440.png"); url = html.escape(Wd.get("url", "ghostrip.id"))
    notch = f'<div style="position:absolute;left:50%;top:0;margin-left:-82px;width:164px;height:{mb}px;background:#000;border-radius:0 0 14px 14px"></div>' if Wd.get("notch") else ""
    css = f"""@font-face{{font-family:Outfit;src:url({FONT});font-weight:100 900}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:{W}px;height:{H}px;background:#f3f1ee;font-family:Outfit;position:relative;overflow:hidden}}
.mb{{position:absolute;left:0;right:0;top:0;height:{mb}px;background:#0b0d0f}}
.tb{{position:absolute;left:0;right:0;top:{mb}px;height:{tb}px;background:#eceae6;border-bottom:1px solid #d9d5ce;display:flex;align-items:center;justify-content:center}}
.url{{width:520px;height:38px;border-radius:12px;background:#fbfaf8;color:#4a5559;font-size:21px;display:flex;align-items:center;justify-content:center}}
.dots{{position:absolute;left:28px;top:22px;display:flex;gap:11px}}.dots i{{width:20px;height:20px;border-radius:50%;background:#c9c4bc}}
.vw{{position:absolute;left:0;right:0;top:{mb + tb}px;bottom:0;overflow:hidden;background:#eef8f5}}.vw img{{width:{W}px;display:block;margin-top:-{int(Wd.get("scroll", 0))}px}}"""
    return (f'<!doctype html><html><head><meta charset=utf-8><style>{css}</style></head><body>'
            f'<div class="mb"></div>{notch}<div class="tb"><div class="dots"><i></i><i></i><i></i></div><div class="url">{url}</div></div>'
            f'<div class="vw"><img src="{site}"></div></body></html>'), W, H


def layar_html(aspek, L):
    if L.get("web"):
        return layar_web(aspek, L)
    W = 1200; H = int(round(W / aspek))
    shot = lambda n: "file://" + os.path.join(IMG, n + ".png")
    kartu = L.get("kartu", ["hasil", "home"]); judul = html.escape(L.get("judul", "Hitung trip")); url = html.escape(L.get("url", "ghostrip.id"))
    css = f"""@font-face{{font-family:Outfit;src:url({FONT});font-weight:100 900}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:{W}px;height:{H}px;background:#f3f1ee;font-family:Outfit;position:relative;overflow:hidden}}
.bar{{position:absolute;left:0;right:0;top:0;height:78px;display:flex;align-items:center;justify-content:center;border-bottom:1px solid #e1ddd7;background:#f7f5f2}}
.url{{width:420px;height:40px;border-radius:12px;background:#e9e6e1;color:#6b7479;font-size:21px;display:flex;align-items:center;justify-content:center}}
.dots{{position:absolute;left:34px;top:26px;display:flex;gap:14px}}.dots i{{width:24px;height:24px;border-radius:7px;border:3px solid #b9b4ad}}
h1{{position:absolute;left:64px;top:112px;font-size:92px;font-weight:700;color:#0f2530;letter-spacing:-.03em}}
.sub{{position:absolute;right:64px;top:150px;font-size:24px;color:#7a8387}}
.card{{position:absolute;overflow:hidden;border-radius:40px;box-shadow:0 10px 30px rgba(15,37,48,.18)}}.card img{{width:100%;display:block}}"""
    if aspek >= 1:
        ch = H - 250 - 70; cw = 520
        body = f'<div class="card" style="left:64px;top:250px;width:{cw}px;height:{ch}px"><img src="{shot(kartu[0])}"></div>'
        body += f'<div class="card" style="left:616px;top:250px;width:{cw}px;height:{ch}px"><img src="{shot(kartu[-1])}"></div>'
        top = f'<div class="bar"><div class="dots"><i></i><i></i></div><div class="url">{url}</div></div><h1>{judul}</h1><div class="sub">Contoh data simulasi</div>'
    else:  # potret: satu tangkapan layar penuh
        body = f'<div class="card" style="left:0;top:0;width:{W}px;height:{H}px;border-radius:0;box-shadow:none"><img src="{shot(kartu[0])}"></div>'; top = ""
    return f"<!doctype html><html><head><meta charset=utf-8><style>{css}</style></head><body>{top}{body}</body></html>", W, H


def render_layar(aspek, L, out):
    from playwright.sync_api import sync_playwright
    src, W, H = layar_html(aspek, L); tmp = out + ".html"; open(tmp, "w").write(src)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"]); pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + tmp); pg.wait_for_timeout(600); pg.screenshot(path=out); b.close()
    os.remove(tmp)


def ganti_layar(foto, quad, aspek, L, out):
    import cv2
    ori = cv2.imread(foto); oh, ow = ori.shape[:2]
    s = max(1080 / ow, 1350 / oh)                      # cover-crop ke 1080x1350
    big = cv2.resize(ori, (int(round(ow * s)), int(round(oh * s))), interpolation=cv2.INTER_LANCZOS4)
    ox, oy = (big.shape[1] - 1080) // 2, (big.shape[0] - 1350) // 2
    big = big[oy:oy + 1350, ox:ox + 1080]
    Q = (np.array(quad, np.float32) * s) - np.array([ox, oy], np.float32)
    tmp = out + ".layar.png"; render_layar(aspek, L, tmp); scr = cv2.imread(tmp); os.remove(tmp)
    h, w = scr.shape[:2]
    M = cv2.getPerspectiveTransform(np.array([(0, 0), (w, 0), (w, h), (0, h)], np.float32), Q)
    warp = cv2.warpPerspective(scr, M, (1080, 1350), flags=cv2.INTER_CUBIC)
    r = int(L.get("radius", 60)); mk = np.zeros((h, w), np.uint8)
    cv2.rectangle(mk, (r, 0), (w - r, h), 255, -1); cv2.rectangle(mk, (0, r), (w, h - r), 255, -1)
    for cx, cy in [(r, r), (w - r, r), (r, h - r), (w - r, h - r)]: cv2.circle(mk, (cx, cy), r, 255, -1)
    mask = cv2.GaussianBlur(cv2.warpPerspective(mk, M, (1080, 1350), flags=cv2.INTER_LINEAR), (0, 0), 1.2).astype(np.float32) / 255
    # pencahayaan layar lama: fit kuadrat per kanal dari piksel terang tak jenuh -> warna & gradasi cahaya ikut foto
    hsv = cv2.cvtColor(big, cv2.COLOR_BGR2HSV)
    cand = (mask > 0.98) & (hsv[..., 2] > 165) & (hsv[..., 1] < 60)
    ys, xs = np.nonzero(cand)
    if L.get("cahaya") == "tetap" or len(xs) < 2000:  # layar emisif/gelap: cahaya tetap (BGR), tanpa fit dari layar lama
        light = np.full((1350, 1080, 3), 1, np.float32) * np.array(L.get("cahaya_bgr", [240, 236, 232]), np.float32)
    else:
        if len(xs) > 20000:
            i = np.random.default_rng(1).choice(len(xs), 20000, replace=False); ys, xs = ys[i], xs[i]
        sc = np.array([1, 1e3, 1e3, 1e6, 1e6, 1e6])
        X = np.stack([np.ones_like(xs), xs, ys, xs * xs, xs * ys, ys * ys], 1).astype(np.float64) / sc
        yy, xx = np.mgrid[0:1350, 0:1080]
        Xa = np.stack([np.ones(yy.size), xx.ravel(), yy.ravel(), xx.ravel() ** 2, (xx * yy).ravel(), yy.ravel() ** 2], 1) / sc
        light = np.zeros((1350, 1080, 3), np.float32)
        for c in range(3):
            co, *_ = np.linalg.lstsq(X, big[ys, xs, c].astype(np.float64), rcond=None)
            light[..., c] = np.clip((Xa @ co).reshape(1350, 1080), 0, 255)
    lit = np.clip(cv2.GaussianBlur(warp, (0, 0), 0.9).astype(np.float32) / 255 * light * 1.03, 0, 255)
    k = float(L.get("pantulan", 0))  # kilau/pantulan dari layar lama (0..0.3), supaya terasa satu foto
    if k:
        g = cv2.GaussianBlur(cv2.cvtColor(big, cv2.COLOR_BGR2GRAY), (0, 0), 18).astype(np.float32)
        lit = np.clip(lit + k * g[..., None], 0, 255)
    res = big.astype(np.float32) * (1 - mask[..., None]) + lit * mask[..., None]
    res += np.random.default_rng(3).normal(0, 2.2, res.shape).astype(np.float32)
    cv2.imwrite(out, np.clip(res, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])


def buat(sc, out):
    import feed_mockup
    foto = sc["foto"] if os.path.isabs(sc["foto"]) else os.path.join(ROOT, sc["foto"])
    if sc.get("mode", "ganti-layar") == "ganti-layar":
        bg = out + ".latar.jpg"
        ganti_layar(foto, sc["quad"], sc.get("aspek", 1.13), sc.get("layar", {}), bg)
        spec = {"device": "none", "bg": bg}
    else:
        bg = None; spec = {k: sc[k] for k in ("device", "screen", "rot", "x", "y", "cy", "scale", "file_name") if k in sc}; spec["bg"] = foto
    spec.update(title=sc["title"], sub=sc.get("sub", ""), simulasi=True)
    feed_mockup.render(spec, out)
    if bg: os.remove(bg)


def main(spec_path):
    spec = json.load(open(spec_path)); day = spec["date"]; outdir = os.path.join(ROOT, "media", day); os.makedirs(outdir, exist_ok=True)
    mpath = os.path.join(outdir, "manifest.json"); manifest = json.load(open(mpath)) if os.path.exists(mpath) else []
    for post in spec["posts"]:
        if post["kind"] != "feed" or "foto" not in post.get("scene", {}): continue
        path = os.path.join(outdir, f"{post['slot']}.jpg"); buat(post["scene"], path)
        manifest = [m for m in manifest if m["slot"] != post["slot"]] + [{"slot": post["slot"], "kind": "feed", "media": os.path.relpath(path, ROOT), "gaya": "mockup-foto"}]
        print("OK", post["slot"], os.path.relpath(path, ROOT))
    json.dump(manifest, open(mpath, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
