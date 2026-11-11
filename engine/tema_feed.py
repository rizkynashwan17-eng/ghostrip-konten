"""Tema FEED per tanggal (PATEN Rizky, 7 Nov 2026): feed TIDAK PERNAH bercerita dan TIDAK menjadi teaser Reels/cerita.
Tema feed digilir TIAP HARI antara 3 tema, mulai 10 Nov 2026 dari "logistik":
  logistik -> trucking -> fitur -> logistik -> ...
  - logistik : seputar dunia logistik (kontainer, pelabuhan, dokumen kirim, rantai pasok, istilah & proses; edukasi terverifikasi)
  - trucking : seputar dunia trucking (armada, KIR/STNK, tol, ODOL, biaya & operasional umum, kehidupan admin/sopir sebagai tips/humor/realita, BUKAN cerita fiksi)
  - fitur    : seputar fitur aplikasi Ghostrip yang benar-benar ada (hitung trip, penawaran PDF, invoice, cek muatan, data truk, tim, news)
Reels memakai tema harian sendiri (STRATEGI-KONTEN.md); feed TIDAK mengikutinya.
Pakai: python3 engine/tema_feed.py [tanggal_awal] [jumlah_hari]
"""
import datetime as dt, sys

AWAL = dt.date(2026, 11, 11)  # digeser 1 hari (11 Nov 2026): feed digeser ke hari berikutnya
URUT = ["logistik", "trucking", "fitur"]


def tema(tanggal):
    d = dt.date.fromisoformat(tanggal) if isinstance(tanggal, str) else tanggal
    if d < AWAL:
        return None  # sebelum aturan ini: tidak diperiksa
    return URUT[(d - AWAL).days % 3]


if __name__ == "__main__":
    a = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today()
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    for i in range(n):
        d = a + dt.timedelta(days=i)
        print(d.isoformat(), hari[d.weekday()], tema(d))
