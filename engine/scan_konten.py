"""SCAN WAJIB setelah konten dibuat & dirender, sebelum upload ke Metricool.

Pakai: python3 engine/scan_konten.py konten/YYYY-MM-DD.json
Cek tiap post di manifest media/<tanggal>/:
- Aspek & resolusi: reel/story 1080x1920 (9:16), feed/carousel 1080x1350 (4:5)
- Reel: durasi 15-45 dtk, ada audio, voiceover lengkap & kualitas (cek_konten.check)
- Carousel 2-10 slide; file tidak kosong; ukuran video < 100 MB
- Caption (reel/feed/carousel): ada CTA (DEMO / WA 0815-1704-7930 / gratis 7 hari), #ghostrip,
  panjang <= 2200, hashtag <= 30, tanpa nama terlarang; reel butuh tiktok_title <= 90
- Teks layar & caption: tanpa nama terlarang, tanpa emoji di teks layar
Keluar kode 0 = SEMUA AMAN (WAJIB langsung upload ke Metricool tanpa menunggu persetujuan), 1 = ada masalah (perbaiki, render & scan ulang).
Status "AMAN - SUARA MENYUSUL" = upload sekarang, catat di SUSULAN-SUARA.md.
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cek_konten import check

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZE = {"reel": (1080, 1920), "story": (1080, 1920), "feed": (1080, 1350), "carousel": (1080, 1350)}
BANNED = ["gunung inti gemilang", "lermi", "trans anugrah"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")

def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration",
                                   "-of", "json", path])
    return json.loads(out)

def texts(obj):
    if isinstance(obj, str): yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k not in ("caption", "tiktok_title", "voice_id", "slot", "kind", "time", "topic"): yield from texts(v)
    elif isinstance(obj, list):
        for v in obj: yield from texts(v)

def scan(spec_path):
    spec = json.load(open(spec_path)); day = spec["date"]
    man = {m["slot"]: m for m in json.load(open(os.path.join(ROOT, "media", day, "manifest.json")))}
    report, ok_all = [], True
    for post in spec["posts"]:
        slot, kind = post["slot"], post["kind"]; issues = []; info = {}
        m = man.get(slot)
        if not m: issues.append("belum dirender (tidak ada di manifest)")
        else:
            files = m["media"] if isinstance(m["media"], list) else [m["media"]]
            if kind == "carousel" and not 2 <= len(files) <= 10: issues.append(f"jumlah slide {len(files)} (harus 2-10)")
            for f in files:
                p = os.path.join(ROOT, f)
                if not os.path.exists(p) or os.path.getsize(p) == 0: issues.append(f"file kosong/hilang: {f}"); continue
                pr = probe(p); v = [s for s in pr["streams"] if s["codec_type"] == "video"]
                wh = (v[0]["width"], v[0]["height"]) if v else None
                if wh != SIZE[kind]: issues.append(f"aspek/resolusi {wh} != {SIZE[kind]} ({f})")
                info.setdefault("ukuran", f"{wh[0]}x{wh[1]}" if wh else "?")
                if kind == "reel":
                    dur = float(pr["format"]["duration"]); info["durasi"] = round(dur, 1)
                    if not 15 <= dur <= 45: issues.append(f"durasi {dur:.1f} dtk (harus 15-45)")
                    if not any(s["codec_type"] == "audio" for s in pr["streams"]): issues.append("tidak ada audio")
                    if os.path.getsize(p) > 100e6: issues.append("video > 100 MB")
                    n = sum(1 for s in post.get("scenes", []) if s.get("say"))
                    q = check(p, post.get("voice_id"), n or None)
                    info["suara"] = q.get("voiceover"); info["kualitas"] = q.get("status")
                    if q.get("status") != "AMAN": issues += [f"kualitas: {x}" for x in q.get("masalah", [])] or ["kualitas audio PERLU DICEK"]
        layar = " ".join(texts(post.get("scenes") or post.get("scene") or post.get("slides")))
        if EMOJI.search(layar): issues.append("ada emoji di teks layar")
        if kind != "story":
            cap = post.get("caption", "")
            if not cap: issues.append("caption kosong")
            else:
                low = cap.lower()
                if "#ghostrip" not in low: issues.append("caption tanpa #ghostrip")
                if not ("demo" in low or "0815-1704-7930" in cap): issues.append("caption tanpa CTA (DEMO/WA)")
                if len(cap) > 2200: issues.append(f"caption {len(cap)} karakter (> 2200)")
                if cap.count("#") > 30: issues.append("hashtag > 30")
            if kind == "reel":
                tt = post.get("tiktok_title", "")
                if not tt or len(tt) > 90: issues.append(f"tiktok_title kosong/terlalu panjang ({len(tt)})")
        allt = (layar + " " + post.get("caption", "")).lower()
        for b in BANNED:
            if b in allt: issues.append(f"nama terlarang: {b}")
        # Suara belum lengkap karena kuota TTS = boleh dijadwalkan dulu (dicatat di SUSULAN-SUARA.md), bukan penghalang upload.
        suara = [x for x in issues if "voiceover" in x]; lain = [x for x in issues if x not in suara]
        ok = not lain; ok_all &= ok
        status = "PERBAIKI" if lain else ("AMAN - SUARA MENYUSUL" if suara else "AMAN")
        report.append({"slot": slot, "jenis": kind, "jam": post.get("time"), **info, "status": status, "masalah": issues})
    print(json.dumps({"tanggal": day, "semua_aman": ok_all, "hasil": report}, ensure_ascii=False, indent=1))
    return ok_all

if __name__ == "__main__":
    sys.exit(0 if scan(sys.argv[1]) else 1)
