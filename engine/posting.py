"""Kelola daftar konten untuk halaman "Posting Ghostrip" (posting manual oleh Rizky).

Halaman: index.html di root repo (GitHub Pages) membaca posting/jadwal.json.

Pakai:
  python3 engine/posting.py tambah konten/2026-11-02-v2.json
      → masukkan semua post dari file konten (pakai media/<tanggal>/manifest.json)
  python3 engine/posting.py manual --tanggal 2026-11-03 --jam 19:30 --jenis reel \
      --media media/manual/x.mp4 --judul "Promo fitur" --caption-file cap.txt [--tiktok "judul"] [--platform ig,tiktok]
  python3 engine/posting.py catatan <id> "teks"       → isi/ubah catatan sebuah post
  python3 engine/posting.py platform <id> ig          → ubah platform (mis. TikTok sudah tayang)
  python3 engine/posting.py bersihkan [hari=10]        → buang post yang lebih tua dari N hari
  python3 engine/posting.py daftar                     → tampilkan isi jadwal
Jenis: story | reel | feed | carousel. Default platform: reel → ig,tiktok,fb; lainnya → ig,fb (halaman juga selalu menampilkan Facebook Page).
"""
import argparse, datetime as dt, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "posting", "jadwal.json")
WIB = dt.timezone(dt.timedelta(hours=7))


def load():
    if os.path.exists(PATH):
        return json.load(open(PATH))
    return {"diperbarui": None, "posts": []}


def save(d):
    d["posts"].sort(key=lambda p: (p["tanggal"], p["jam"]))
    d["diperbarui"] = dt.datetime.now(WIB).isoformat(timespec="minutes")
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    json.dump(d, open(PATH, "w"), ensure_ascii=False, indent=1)
    print(f"jadwal.json: {len(d['posts'])} post")


def strip(t):
    return re.sub(r"\*", "", t or "").strip()


def upsert(d, post):
    for i, p in enumerate(d["posts"]):
        if p["id"] == post["id"]:
            post.setdefault("catatan", p.get("catatan", ""))
            d["posts"][i] = post
            return "diganti"
    d["posts"].append(post)
    return "ditambah"


def check_media(paths):
    for m in paths:
        if not os.path.exists(os.path.join(ROOT, m)):
            sys.exit(f"media tidak ada: {m}")


def judul_of(p):
    if p.get("topic"):
        return strip(p["topic"])
    sc = p.get("scene") or (p.get("slides") or [{}])[0] or (p.get("scenes") or [{}])[0]
    return strip(sc.get("title") or sc.get("text") or p.get("slot"))


def tambah(args):
    k = json.load(open(args.file))
    date = k["date"]
    man_path = os.path.join(ROOT, "media", date, "manifest.json")
    man = {m["slot"]: m for m in json.load(open(man_path))} if os.path.exists(man_path) else {}
    d = load()
    for p in k["posts"]:
        if not p.get("time"):
            print(f"lewati {p['slot']}: tanpa jam"); continue
        m = man.get(p["slot"])
        if not m:
            sys.exit(f"{p['slot']}: belum ada di {man_path} (render dulu)")
        media = m["media"] if isinstance(m["media"], list) else [m["media"]]
        # pakai versi bersuara (-vo) kalau ada
        media = [x.replace(".mp4", "-vo.mp4") if x.endswith(".mp4") and os.path.exists(os.path.join(ROOT, x.replace(".mp4", "-vo.mp4"))) else x for x in media]
        check_media(media)
        kind = p["kind"]
        post = {
            "id": f"{date}-{p['time'].replace(':', '')}-{p['slot']}",
            "tanggal": date, "jam": p["time"], "jenis": kind,
            "platform": ["ig", "tiktok", "fb"] if kind == "reel" else ["ig", "fb"],
            "judul": judul_of(p), "media": media, "cover": m.get("cover"),
            "caption": p.get("caption", ""), "tiktok_title": p.get("tiktok_title", ""),
            "catatan": "",
        }
        print(post["id"], upsert(d, post))
    save(d)


def manual(args):
    media = args.media.split(",")
    check_media(media)
    cap = open(args.caption_file).read().strip() if args.caption_file else (args.caption or "")
    plat = args.platform.split(",") if args.platform else (["ig", "tiktok", "fb"] if args.jenis == "reel" else ["ig", "fb"])
    slug = re.sub(r"[^a-z0-9]+", "-", args.judul.lower()).strip("-")[:30]
    post = {"id": f"{args.tanggal}-{args.jam.replace(':', '')}-{slug}", "tanggal": args.tanggal, "jam": args.jam,
            "jenis": args.jenis, "platform": plat, "judul": args.judul, "media": media, "cover": args.cover,
            "caption": cap, "tiktok_title": args.tiktok or "", "catatan": args.catatan or ""}
    d = load(); print(post["id"], upsert(d, post)); save(d)


def find(d, pid):
    for p in d["posts"]:
        if p["id"] == pid:
            return p
    sys.exit(f"id tidak ditemukan: {pid}")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("tambah"); a.add_argument("file")
    b = sp.add_parser("manual")
    for f in ["--tanggal", "--jam", "--jenis", "--media", "--judul"]:
        b.add_argument(f, required=True)
    for f in ["--caption", "--caption-file", "--tiktok", "--platform", "--cover", "--catatan"]:
        b.add_argument(f)
    c = sp.add_parser("catatan"); c.add_argument("id"); c.add_argument("teks")
    e = sp.add_parser("platform"); e.add_argument("id"); e.add_argument("platform")
    f = sp.add_parser("bersihkan"); f.add_argument("hari", nargs="?", type=int, default=10)
    sp.add_parser("daftar")
    args = ap.parse_args()
    if args.cmd == "tambah": tambah(args)
    elif args.cmd == "manual": manual(args)
    elif args.cmd == "catatan":
        d = load(); find(d, args.id)["catatan"] = args.teks; save(d)
    elif args.cmd == "platform":
        d = load(); find(d, args.id)["platform"] = args.platform.split(","); save(d)
    elif args.cmd == "bersihkan":
        d = load(); batas = (dt.datetime.now(WIB) - dt.timedelta(days=args.hari)).date().isoformat()
        d["posts"] = [p for p in d["posts"] if p["tanggal"] >= batas]; save(d)
    else:
        for p in load()["posts"]:
            print(p["tanggal"], p["jam"], p["jenis"], ",".join(p["platform"]), p["judul"], "|", p.get("catatan", ""))


if __name__ == "__main__":
    main()
