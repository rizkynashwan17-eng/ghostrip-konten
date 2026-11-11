"""Gaya Reels per tanggal (PATEN Rizky 5 Nov 2026): SELANG-SELING mulai Minggu 8 Nov 2026.

8, 10, 12 Nov ... (selisih hari genap dari 8 Nov) = "bedah"  -> BEDAH TEKNIKAL (remotion/src/Bedah.tsx), tema "teknikal"
9, 11, 13 Nov ... (selisih ganjil)                   = "whatif" -> gaya lama pilot reel1-whatif, ikut tema harian
Mulai 13 Nov 2026 (PATEN 11 Nov 2026, REVISI): 1 Reels per hari dari naskah, SELANG-SELING A/B:
13 Nov = A "cerita" (naskah 13 Nov), 14 Nov = B "produk" (naskah 13 Nov), 15 Nov = A (naskah 14 Nov), 16 Nov = B (naskah 14 Nov), dst.
36 naskah -> 36 hari (13 Nov s.d. 18 Des 2026). Pakai `naskah_untuk(tanggal)` untuk tahu tanggal naskah & jenisnya.
Pakai: python3 engine/gaya_reels.py [tanggal_awal] [jumlah_hari]  -> cetak jadwal gaya
"""
import datetime as dt, sys

AWAL = dt.date(2026, 11, 8)
NASKAH = dt.date(2026, 11, 13)  # PATEN 11 Nov 2026: format naskah A (cerita) + B (produk), lihat PANDUAN.md


def gaya(tanggal):
    d = dt.date.fromisoformat(tanggal) if isinstance(tanggal, str) else tanggal
    if d >= NASKAH:
        return "cerita" if (d - NASKAH).days % 2 == 0 else "produk"  # A jam 11:30 / B jam 19:30, selang-seling harian
    if d < AWAL:
        return "whatif"
    return "bedah" if (d - AWAL).days % 2 == 0 else "whatif"


def naskah_untuk(tanggal):
    """(tanggal_naskah, 'A'|'B') untuk hari tayang `tanggal`; None bila naskah habis (setelah 18 Des 2026) atau sebelum 13 Nov."""
    d = dt.date.fromisoformat(tanggal) if isinstance(tanggal, str) else tanggal
    n = (d - NASKAH).days
    if n < 0 or n >= 36:
        return None
    return (NASKAH + dt.timedelta(days=n // 2)).isoformat(), "AB"[n % 2]


if __name__ == "__main__":
    a = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today()
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 14
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    for i in range(n):
        d = a + dt.timedelta(days=i)
        print(d.isoformat(), hari[d.weekday()], gaya(d), naskah_untuk(d) or '')
