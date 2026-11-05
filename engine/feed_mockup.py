"""Feed Ghostrip gaya MOCKUP FOTO (perangkat di atas foto latar), contoh dari Rizky 5 Nov 2026.

Susunan brand tetap: logo Ghostrip.id kiri atas, judul tebal putih kiri bawah, sub-judul di bawahnya,
gradasi gelap di bawah supaya teks terbaca. Perangkat: hp | tablet | laptop, isi layar = tangkapan
layar ASLI aplikasi dengan data fiktif (remotion/public/iklan3d/*.png).

Pakai: python3 engine/feed_mockup.py <spec.json> <out.jpg>
spec: {"device":"hp|tablet|laptop","bg":"path foto latar","screen":"path png","title":"...","sub":"...",
       "rot":-10,"x":0,"y":0,"scale":1,"crop_top":0}
"""
import json, os, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = lambda p: "file://" + (p if p.startswith("/") else os.path.join(ROOT, p))
FONT = U("fonts/Outfit.ttf"); ICON = U("assets/icon.png")

CSS = """
@font-face{font-family:Outfit;src:url(%(font)s);font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;position:relative;font-family:Outfit;background:#071a22}
.bg{position:absolute;inset:0;background:url(%(bg)s) center/cover}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,13,19,.35) 0%%,rgba(4,13,19,0) 22%%,rgba(4,13,19,0) 55%%,rgba(4,13,19,.88) 100%%)}
.logo{position:absolute;left:78px;top:84px;display:flex;align-items:center;gap:18px}
.logo img{width:88px;height:88px;border-radius:24px;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.logo b{color:#fff;font-size:38px;font-weight:700;text-shadow:0 2px 12px rgba(0,0,0,.4)}
.txt{position:absolute;left:108px;right:110px;bottom:108px;color:#fff}
.txt h1{font-size:58px;line-height:1.12;font-weight:700;letter-spacing:-.01em;text-shadow:0 4px 24px rgba(0,0,0,.35)}
.txt p{margin-top:16px;font-size:25px;line-height:1.38;color:rgba(255,255,255,.88);font-weight:400}
.sim{position:absolute;right:78px;top:104px;background:rgba(7,26,34,.7);color:#7ff0d6;font-size:16px;font-weight:700;letter-spacing:.12em;padding:8px 16px;border-radius:999px}
.dev{position:absolute;left:50%%;top:%(cy)spx;transform:translate(-50%%,-50%%) translate(%(x)spx,%(y)spx) rotate(%(rot)sdeg) scale(%(scale)s);filter:drop-shadow(0 40px 50px rgba(0,0,0,.55)) drop-shadow(0 8px 14px rgba(0,0,0,.35))}
/* HP */
.hp{width:400px;height:850px;border-radius:66px;background:linear-gradient(145deg,#3b4a52,#11181c 40%%,#2a363c);padding:13px}
.hp .scr{width:100%%;height:100%%;border-radius:54px;overflow:hidden;background:#000;position:relative}
.hp .notch{position:absolute;left:50%%;top:12px;transform:translateX(-50%%);width:120px;height:34px;border-radius:20px;background:#000;z-index:2}
/* TABLET */
.tab{width:660px;height:880px;border-radius:46px;background:linear-gradient(145deg,#3b4a52,#0f1619 45%%,#283338);padding:24px}
.tab .scr{width:100%%;height:100%%;border-radius:24px;overflow:hidden;background:#fff}
/* LAPTOP */
.lap{width:900px}
.lap .lid{width:900px;height:580px;border-radius:26px 26px 8px 8px;background:#0d1419;padding:22px 22px 30px;border:2px solid #39464d}
.lap .scr{width:100%%;height:100%%;border-radius:6px;overflow:hidden;background:#3a4246;position:relative}
.lap .base{width:1040px;height:30px;margin-left:-70px;border-radius:4px 4px 26px 26px;background:linear-gradient(180deg,#c9d1d4,#8a959a 60%%,#5c666b)}
.lap .base:after{content:"";display:block;width:160px;height:10px;margin:0 auto;border-radius:0 0 12px 12px;background:#77838a}
.scr img{width:100%%;height:100%%;object-fit:cover;object-position:top;display:block}
.pdfbar{height:40px;background:#22292d;color:#cfd8dc;font-size:15px;display:flex;align-items:center;padding:0 18px;gap:14px}
.pdfbar i{font-style:normal;opacity:.6}
.pdfpage{position:absolute;left:50%%;top:56px;transform:translateX(-50%%);width:400px;box-shadow:0 8px 24px rgba(0,0,0,.4)}
.pdfpage img{width:100%%;height:auto}
"""


def device(spec):
    d, s = spec["device"], U(spec["screen"])
    if d == "hp":
        return f'<div class="hp"><div class="scr"><div class="notch"></div><img src="{s}"></div></div>'
    if d == "tablet":
        return f'<div class="tab"><div class="scr"><img src="{s}"></div></div>'
    if d == "laptop":
        name = html.escape(spec.get("file_name", "Surat_Penawaran.pdf"))
        return (f'<div class="lap"><div class="lid"><div class="scr"><div class="pdfbar"><b>{name}</b><i>1 / 1</i><i>100%</i></div>'
                f'<div class="pdfpage"><img src="{s}"></div></div></div><div class="base"></div></div>')
    raise ValueError(d)


def page(spec):
    v = dict(font=FONT, bg=U(spec["bg"]), cy=spec.get("cy", 600), x=spec.get("x", 0), y=spec.get("y", 0),
             rot=spec.get("rot", 0), scale=spec.get("scale", 1))
    sim = '<div class="sim">DATA SIMULASI</div>' if spec.get("simulasi", True) else ""
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS % v}</style></head><body>
<div class="bg"></div><div class="dev">{device(spec)}</div><div class="shade"></div>
<div class="logo"><img src="{ICON}"><b>Ghostrip.id</b></div>{sim}
<div class="txt"><h1>{html.escape(spec["title"]).replace(chr(10), "<br>")}</h1><p>{html.escape(spec.get("sub", ""))}</p></div>
</body></html>'''


def render(spec, out):
    from playwright.sync_api import sync_playwright
    tmp = out + ".html"; open(tmp, "w").write(page(spec))
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto("file://" + os.path.abspath(tmp)); pg.wait_for_timeout(500)
        pg.screenshot(path=out, type="jpeg", quality=93); b.close()
    os.remove(tmp)


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
