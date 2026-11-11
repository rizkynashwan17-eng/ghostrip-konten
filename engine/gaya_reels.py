"""Gaya Reels per tanggal (PATEN Rizky 5 Nov 2026): SELANG-SELING mulai Minggu 8 Nov 2026.

8, 10, 12 Nov ... (selisih hari genap dari 8 Nov) = "bedah"  -> BEDAH TEKNIKAL (remotion/src/Bedah.tsx), tema "teknikal"
9, 11, 13 Nov ... (selisih ganjil)                   = "whatif" -> gaya lama pilot reel1-whatif, ikut tema harian
Mulai 13 Nov 2026 selang-seling DIHENTIKAN: tiap hari 2 Reels dari naskah (gaya "cerita" dan "produk").
Pakai: python3 engine/gaya_reels.py [tanggal_awal] [jumlah_hari]  -> cetak jadwal gaya
"""
import datetime as dt, sys

AWAL = dt.date(2026, 11, 8)
NASKAH = dt.date(2026, 11, 13)  # PATEN 11 Nov 2026: format naskah A (cerita) + B (produk), lihat PANDUAN.md


def gaya(tanggal):
    d = dt.date.fromisoformat(tanggal) if isinstance(tanggal, str) else tanggal
    if d >= NASKAH:
        return "naskah"  # 2 Reels per hari: A "cerita" jam 11:30 + B "produk" jam 19:30
    if d < AWAL:
        return "whatif"
    return "bedah" if (d - AWAL).days % 2 == 0 else "whatif"


if __name__ == "__main__":
    a = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today()
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 14
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    for i in range(n):
        d = a + dt.timedelta(days=i)
        print(d.isoformat(), hari[d.weekday()], gaya(d))
