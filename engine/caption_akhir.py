"""Penutup caption BAKU Ghostrip (PATEN Rizky, 4 Nov 2026).

SEMUA caption (reel, feed, carousel; IG/TikTok/FB) harus ditutup dengan blok di bawah ini,
persis seperti tertulis. Isi caption = hook/isi singkat + (bila perlu) catatan fiksi/simulasi,
LALU blok baku. Jangan menulis CTA, nomor WA, atau hashtag lain di badan caption.

Pakai:  python3 engine/caption_akhir.py konten/<file>.json [...]   → pasang/rapikan caption di file itu
Fungsi: pasang(caption) -> caption dengan penutup baku (aman dipanggil berulang)
"""
import json, re, sys

PENUTUP = (
    "🚛 Mau urusan logistik lebih praktis?\n\n"
    "Coba Ghostrip gratis selama 7 hari!\n\n"
    "📲 WhatsApp: 0815-1704-7930\n"
    "🌐 ghostrip.id\n\n"
    "#Ghostrip #LogistikIndonesia #Transportasi #BisnisLogistik #AplikasiLogistik"
)
_CTA = re.compile(r"coba gratis|0815-?1704-?7930|komen demo|chat wa|wa 0815", re.I)


def badan(caption):
    """Caption tanpa penutup baku, tanpa CTA/hashtag lama."""
    c = (caption or "").replace(PENUTUP, "").strip()
    out = []
    for para in re.split(r"\n\s*\n", c):
        lines = [l for l in para.split("\n") if not l.strip().startswith("#")]
        keep = []
        for l in lines:
            if _CTA.search(l):
                # buang hanya kalimat CTA; kalimat lain di baris yang sama tetap
                sents = [s for s in re.split(r"(?<=[.!?])\s+", l) if not _CTA.search(s)]
                l = " ".join(sents)
            if l.strip(): keep.append(l.rstrip())
        if keep: out.append("\n".join(keep))
    return "\n\n".join(out).strip()


def pasang(caption):
    b = badan(caption)
    return (b + "\n\n" if b else "") + PENUTUP


def main(paths):
    for p in paths:
        d = json.load(open(p)); n = 0
        for post in d.get("posts", []):
            if post.get("kind") == "story" or "caption" not in post: continue
            post["caption"] = pasang(post["caption"]); n += 1
        json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
        print(p, n, "caption")


if __name__ == "__main__":
    main(sys.argv[1:])
