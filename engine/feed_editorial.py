"""Feed Ghostrip gaya EDITORIAL (PATEN 4 Nov 2026, permintaan Rizky).

Gaya: kartu sosial editorial (judul besar tebal, satu frasa miring bergaris sapuan,
kapsul miring, gelembung chat, panah coretan, panel bersudut bulat, logo Ghostrip.id
di kanan bawah). Warna latar BERGANTI antar-post supaya feed tidak monoton, tapi
selalu dari palet brand (navy, teal, mint, krem, oranye) dan font Outfit.

Pakai: python3 engine/feed_editorial.py konten/<file>.json
Post feed yang punya scene.layout dirender di sini (render.py melewatinya).

Markup judul: *frasa* = miring + garis sapuan; ~frasa~ = warna aksen.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "file://" + os.path.join(ROOT, "fonts", "Outfit.ttf")
ICON = "file://" + os.path.join(ROOT, "assets", "icon.png")
GHOST = "file://" + os.path.join(ROOT, "assets", "ghost_wave.png")

# Palet brand — warna latar bergiliran. Jangan tambah warna di luar brand.
# PATEN 4 Nov (revisi Rizky): feed harus kohesif seperti referensi — satu warna utama (teal),
# selingan navy & krem, aksen mint konsisten, oranye hanya sentuhan kecil.
PALET = {
    "navy":   dict(bg="#071a22", fg="#ffffff", sub="#b9d3d6", ac="#ff9d5c", sw="#7ff0d6", panel="#0f3b46", p1="#7ff0d6", p2="#ff9d5c", pf="#ffffff", line="#ffffff", ink="#0d1b24", note="#8fb0b5", dot=".id", dotc="#7ff0d6"),
    "teal":   dict(bg="#1d5a63", fg="#ffffff", sub="#c6e2e2", ac="#ff9d5c", sw="#7ff0d6", panel="#0f3b46", p1="#7ff0d6", p2="#ff9d5c", pf="#ffffff", line="#ffffff", ink="#0d1b24", note="#9cc3c4", dot=".id", dotc="#7ff0d6"),
    "mint":   dict(bg="#7ff0d6", fg="#0d1b24", sub="#1d4a4f", ac="#071a22", sw="#ff9d5c", panel="#071a22", p1="#071a22", p2="#ff9d5c", pf="#ffffff", line="#0d1b24", ink="#0d1b24", note="#1d4a4f", dot=".id", dotc="#0f3b46"),
    "krem":   dict(bg="#f2ead9", fg="#0d1b24", sub="#4d5f63", ac="#e2733a", sw="#2fb8a0", panel="#0f3b46", p1="#7ff0d6", p2="#ff9d5c", pf="#071a22", line="#0d1b24", ink="#0d1b24", note="#5d6d70", dot=".id", dotc="#2fb8a0"),
    "oranye": dict(bg="#ff9d5c", fg="#0d1b24", sub="#4a2a14", ac="#ffffff", sw="#071a22", panel="#071a22", p1="#071a22", p2="#ffffff", pf="#f2ead9", line="#0d1b24", ink="#0d1b24", note="#4a2a14", dot=".id", dotc="#ffffff"),
}
URUTAN = ["teal", "navy", "teal", "navy", "navy", "teal", "navy"]  # Sen..Min. TEAL = warna utama, navy selingan (krem TIDAK dipakai untuk feed, Rizky 7 Nov), aksen selalu mint. Latar mint/oranye penuh TIDAK dipakai.


def judul(t, pal):
    t = html.escape(t)
    t = re.sub(r"\*(.+?)\*", lambda m: f'<span class="it">{m.group(1)}<svg viewBox="0 0 300 34" preserveAspectRatio="none"><path d="M4 22 C 70 6, 170 4, 296 14 C 220 14, 130 18, 40 30" fill="none" stroke="{pal["sw"]}" stroke-width="9" stroke-linecap="round"/></svg></span>', t)
    t = re.sub(r"~(.+?)~", r'<span class="ac">\1</span>', t)
    return t.replace("\\n", "<br>").replace("\n", "<br>")


def e(t): return html.escape(str(t))


ARROW = '<svg class="arrow" style="{pos}" viewBox="0 0 200 170"><path d="M20 20 C 120 10, 170 60, 120 100 C 90 125, 60 95, 95 80 C 140 62, 175 110, 170 150" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round"/><path d="M150 135 L170 152 L182 128" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def pills(items, pal, x0=0):
    kinds = ["", "p1", "", "pf", "p2", "", "p1"]
    rots = [-6, 4, -3, 5, -4, 3, -5]
    offs = [10, 60, 0, 70, 20, 50, 0]
    out = []
    for i, it in enumerate(items):
        k = kinds[i % 7]
        out.append(f'<div class="p {k}" style="margin-left:{offs[i%7]+x0}px;transform:rotate({rots[i%7]}deg)"><small>{i+1:02d}</small>{e(it)}</div>')
    return '<div class="pills">' + "".join(out) + "</div>"


def doc_card(d):
    rows = "".join(f'<div class="row">{e(r)} <span class="ok">✓</span></div>' for r in d.get("rows", []))
    return f'''<div class="panel"><div class="doc"><div class="h">{e(d.get("judul","QUOTATION"))}</div>
<div class="n">{e(d.get("sub",""))}</div><div class="ln" style="width:80%"></div>{rows}
<div class="tot"><span>Total</span><span>Rp ••.•••.•••</span></div></div>
<div class="stamp">TTD<br>&amp; CAP</div><div class="sim">SIMULASI</div></div>'''


def chat(msgs):
    out = []
    for m in msgs:
        side = "r" if m.get("dari") == "kanan" else "l"
        who = f'<i>{e(m["nama"])}</i>' if m.get("nama") else ""
        out.append(f'<div class="b {side}">{who}{e(m["teks"])}</div>')
    return '<div class="chat">' + "".join(out) + "</div>"


def rows_card(items, judul_kartu=""):
    r = "".join(f'<div class="rw"><b>{i+1:02d}</b><span>{e(t)}</span></div>' for i, t in enumerate(items))
    h = f'<div class="rh">{e(judul_kartu)}</div>' if judul_kartu else ""
    return f'<div class="rows">{h}{r}</div>'


def body(sc, pal):
    L = sc["layout"]
    if L == "checklist":  # panel dokumen kiri + kapsul miring kanan
        return f'<div class="grid2">{doc_card(sc.get("doc", {}))}{pills(sc["items"], pal)}</div>' + ARROW.format(pos="right:90px;top:-150px", c=pal["ac"] if pal["bg"] in ("#071a22", "#0f3b46") else pal["p2"])
    if L == "alur":  # kartu langkah bernomor + pdf miring
        return f'<div class="grid2 alur">{rows_card(sc["items"], sc.get("kartu",""))}<div class="side">{doc_card(sc.get("doc", {}))}</div></div>'
    if L == "chat":  # gelembung chat + kapsul opsional
        extra = pills(sc["items"], pal) if sc.get("items") else ""
        return f'<div class="stack">{chat(sc["chat"])}{extra}</div>'
    if L == "file":  # tumpukan kapsul nama file
        return f'<div class="files">' + "".join(
            f'<div class="fchip {"last" if i==len(sc["items"])-1 else ""}" style="transform:rotate({[-4,3,-2,4,-3,2][i%6]}deg);margin-left:{[0,90,30,120,50,10][i%6]}px"><em class="fi"></em>{e(t)}</div>'
            for i, t in enumerate(sc["items"])) + "</div>"
    raise ValueError(L)


CSS = """
@font-face{font-family:Outfit;src:url(%(font)s);font-weight:100 900}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;background:%(bg)s;font-family:Outfit;color:%(fg)s;overflow:hidden;position:relative}
.page{position:absolute;inset:0;padding:84px 80px 62px;display:flex;flex-direction:column}
.eyebrow{display:flex;gap:14px;align-items:center}
.tag{font-weight:700;font-size:22px;letter-spacing:.14em;color:%(tagc)s}
.pill-s{background:%(p1)s;color:%(p1fg)s;font-weight:800;font-size:20px;letter-spacing:.08em;padding:9px 20px;border-radius:999px;transform:rotate(-3deg)}
h1{margin-top:40px;font-weight:700;font-size:%(tsize)spx;line-height:1.02;letter-spacing:-.02em}
h1 .it{font-style:italic;position:relative;display:inline-block}
h1 .it svg{position:absolute;left:-6px;bottom:-14px;width:108%%;height:32px}
h1 .ac{color:%(ac)s}
.sub{margin-top:28px;font-size:30px;line-height:1.35;color:%(sub)s;max-width:720px}
.body{flex:1;position:relative;margin-top:40px;min-height:0}
.grid2{display:flex;gap:30px;align-items:center;height:100%%}
.panel{position:relative;flex:0 0 450px;height:460px;border-radius:44px;background:%(panel)s;overflow:hidden}
.panel::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 30%% 20%%,rgba(127,240,214,.22),transparent 60%%)}
.doc{position:absolute;left:56px;top:40px;width:320px;height:370px;background:#f2ead9;border-radius:22px;transform:rotate(-5deg);box-shadow:0 30px 60px rgba(0,0,0,.35);padding:32px 28px;color:#0d1b24}
.doc .h{font-weight:800;font-size:25px;letter-spacing:.06em}
.doc .n{font-size:15px;color:#6b7a7f;margin-top:4px}
.doc .ln{height:12px;border-radius:6px;background:#d9cfba;margin-top:16px}
.doc .row{display:flex;justify-content:space-between;align-items:center;margin-top:15px;font-size:17px;font-weight:600}
.doc .ok{width:26px;height:26px;border-radius:50%%;background:#2fb8a0;display:grid;place-items:center;color:#fff;font-size:16px;font-weight:800}
.doc .tot{margin-top:20px;padding-top:14px;border-top:2px dashed #c9bea6;display:flex;justify-content:space-between;font-weight:800;font-size:19px}
.stamp{position:absolute;right:26px;bottom:24px;width:100px;height:100px;border:4px solid #ff9d5c;border-radius:50%%;color:#ff9d5c;display:grid;place-items:center;text-align:center;font-weight:800;font-size:15px;letter-spacing:.06em;transform:rotate(-14deg);line-height:1.1;background:rgba(242,234,217,.0)}
.sim{position:absolute;right:24px;top:22px;background:rgba(7,26,34,.8);color:#7ff0d6;font-size:15px;font-weight:700;letter-spacing:.1em;padding:6px 14px;border-radius:999px}
.pills{display:flex;flex-direction:column;gap:22px;flex:1}
.p{align-self:flex-start;font-weight:600;font-size:%(psize)spx;padding:14px 30px;border-radius:999px;border:3px solid %(line)s;white-space:nowrap;color:%(fg)s}
.p.p1{background:%(p1)s;border-color:%(p1)s;color:%(p1fg)s}
.p.p2{background:%(p2)s;border-color:%(p2)s;color:%(p2fg)s}
.p.pf{background:%(pf)s;border-color:%(pf)s;color:%(pffg)s}
.p small{font-size:21px;font-weight:800;opacity:.6;margin-right:10px;vertical-align:4px}
.arrow{position:absolute;width:170px;height:150px}
.rows{flex:1;background:%(panel)s;border-radius:40px;padding:38px 40px;color:#fff;box-shadow:0 24px 50px rgba(0,0,0,.18)}
.rh{font-size:20px;font-weight:800;letter-spacing:.12em;color:#7ff0d6;margin-bottom:18px}
.rw{display:flex;gap:20px;align-items:baseline;padding:15px 0;border-bottom:1px solid rgba(255,255,255,.14);font-size:31px;font-weight:600;line-height:1.2}
.rw:last-child{border-bottom:0}
.rw b{color:#ff9d5c;font-size:24px;min-width:38px}
.alur .side{flex:0 0 330px;position:relative;height:460px}
.alur .panel{flex:none;width:330px;height:460px;background:transparent}
.alur .panel::before{display:none}
.alur .doc{left:0;top:30px;width:310px;transform:rotate(6deg)}
.alur .sim{right:0;top:0}
.alur .stamp{right:6px;bottom:20px}
.stack{display:flex;flex-direction:column;gap:30px;height:100%%;justify-content:center}
.chat{display:flex;flex-direction:column;gap:18px}
.b{max-width:86%%;font-size:37px;line-height:1.3;padding:20px 28px;border-radius:30px;font-weight:500}
.b i{display:block;font-style:normal;font-size:18px;font-weight:800;letter-spacing:.1em;opacity:.7;margin-bottom:4px;text-transform:uppercase}
.b.l{align-self:flex-start;background:%(bl)s;color:%(blfg)s;border-bottom-left-radius:8px}
.b.r{align-self:flex-end;background:%(br)s;color:%(brfg)s;border-bottom-right-radius:8px}
.stack .pills{flex-direction:row;flex-wrap:wrap;gap:16px 14px;flex:none}
.stack .p{font-size:31px;padding:13px 26px}
.files{display:flex;flex-direction:column;gap:32px;padding-top:24px}
.fchip{align-self:flex-start;font-size:48px;font-weight:600;padding:26px 42px;border-radius:28px;background:%(pf)s;color:%(pffg)s;box-shadow:0 14px 30px rgba(0,0,0,.12)}
.fi{display:inline-block;position:relative;width:26px;height:34px;border-radius:4px 10px 4px 4px;border:3.5px solid currentColor;margin-right:18px;vertical-align:-4px;opacity:.8}.fi:before,.fi:after{content:'';position:absolute;left:4px;right:4px;height:3px;background:currentColor;border-radius:2px}.fi:before{top:12px}.fi:after{top:19px;right:9px}
.fchip.last{background:%(p2)s;color:%(p2fg)s;font-weight:800}
.ghost{position:absolute;right:20px;bottom:24px;width:190px;transform:rotate(8deg)}
.foot{display:flex;justify-content:space-between;align-items:flex-end;margin-top:30px}
.note{font-size:21px;line-height:1.4;color:%(note)s;max-width:520px}
.logo{display:flex;align-items:center;gap:12px}
.logo img{width:52px;height:52px;border-radius:14px}
.logo b{font-size:34px;font-weight:700;letter-spacing:-.01em;color:%(fg)s}
.logo b span{color:%(dotc)s}
"""


def kontras(c):
    c = c.lstrip("#"); r, g, b = (int(c[i:i+2], 16) for i in (0, 2, 4))
    return "#0d1b24" if (0.299*r + 0.587*g + 0.114*b) > 150 else "#ffffff"


def page(sc, warna):
    pal = dict(PALET[warna])
    gelap = warna in ("navy", "teal")
    v = dict(pal, font=FONT, tsize=sc.get("title_size", 104), psize=sc.get("pill_size", 36),
             tagc=("#7ff0d6" if gelap else pal["fg"]),
             p1fg=kontras(pal["p1"]), p2fg=kontras(pal["p2"]), pffg=kontras(pal["pf"]),
             bl=("#ffffff" if gelap else "#071a22"), blfg=("#0d1b24" if gelap else "#ffffff"),
             br=("#7ff0d6" if warna != "mint" else "#ff9d5c"), brfg="#0d1b24")
    if warna == "oranye": v.update(bl="#071a22", blfg="#ffffff", br="#f2ead9", brfg="#0d1b24")
    if warna == "krem": v.update(br="#7ff0d6")
    pillk = f'<span class="pill-s">{e(sc["pill"])}</span>' if sc.get("pill") else ""
    sub = f'<p class="sub">{e(sc["sub"])}</p>' if sc.get("sub") else ""
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS % v}</style></head><body>
<div class="page"><div class="eyebrow"><span class="tag">{e(sc.get("kicker",""))}</span>{pillk}</div>
<h1>{judul(sc["title"], pal)}</h1>{sub}<div class="body">{body(sc, pal)}</div>
<div class="foot"><p class="note">{e(sc.get("note","")).replace(chr(10),"<br>")}</p>
<div class="logo"><img src="{ICON}"><b>Ghostrip<span>.id</span></b></div></div></div></body></html>'''


def render(sc, warna, out_jpg):
    from playwright.sync_api import sync_playwright
    tmp = out_jpg + ".html"; open(tmp, "w").write(page(sc, warna))
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto("file://" + tmp); pg.wait_for_timeout(400)
        # jaga-jaga: konten tidak boleh meluber ke footer
        over = pg.evaluate("()=>{const b=document.querySelector('.body');return b.scrollHeight>b.clientHeight+4}")
        pg.screenshot(path=out_jpg, type="jpeg", quality=93); b.close()
    os.remove(tmp)
    if over: print("PERINGATAN: isi meluber di", out_jpg)
    return not over


def main(spec_path):
    import datetime
    spec = json.load(open(spec_path)); day = spec["date"]
    outdir = os.path.join(ROOT, "media", day); os.makedirs(outdir, exist_ok=True)
    mpath = os.path.join(outdir, "manifest.json")
    manifest = json.load(open(mpath)) if os.path.exists(mpath) else []
    for post in spec["posts"]:
        if post["kind"] != "feed" or "layout" not in post.get("scene", {}): continue
        sc = post["scene"]
        warna = sc.get("warna") or URUTAN[datetime.date.fromisoformat(day).weekday()]
        path = os.path.join(outdir, f'{post["slot"]}-ed.jpg')
        ok = render(sc, warna, path)
        manifest = [m for m in manifest if m["slot"] != post["slot"]] + [{"slot": post["slot"], "kind": "feed", "media": os.path.relpath(path, ROOT), "gaya": "editorial", "warna": warna}]
        print("OK" if ok else "CEK", post["slot"], warna, os.path.relpath(path, ROOT))
    json.dump(manifest, open(mpath, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
