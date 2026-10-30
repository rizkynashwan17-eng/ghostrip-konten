# Susulan suara (dikerjakan tugas harian 15.40 WIB, langkah A)

Rizky sudah mengizinkan: lengkapi suara TANPA bertanya. Sejak 29 Okt 2026 mode posting manual: setelah suara jadi, render ulang lalu perbarui halaman lewat `engine/posting.py` (bukan Metricool). Hapus baris dari tabel setelah berhasil diganti. Posting yang jamnya sudah lewat: hapus barisnya (tidak bisa diganti).

Request suara yang belum lengkap: 5 video Remotion (lihat tabel). ATURAN 30 Okt: mulai 1 Nov hanya 1 Reels per hari jam 19.30 — dua Reels cadangan dipindah ke 6 & 9 Nov. Reel lama 'salah hitung' 1 Nov dihapus dari halaman (bukan Remotion). Kuota TTS harian habis 30 Okt 16.14 WIB: run otomatis yang antre ikut membuat ulang suara MST sehingga kuota terpakai, lalu hasilnya gagal di-push (konflik). Workflow sudah diperbaiki (checkout `ref: main`). Nataru reel1-v2, Zero ODOL + vokal, salah hitung + vokal sudah bersuara dan sudah dipakai di halaman Posting (dicek Rizky 29 Okt).
Urutan pengerjaan TTS otomatis menurut kunci `"jadwal"` di request (tayang terdekat dulu), jadi kalau kuota habis yang paling dekat jadwalnya sudah aman duluan. 

Konten yang harus diperbarui di halaman Posting (setelah suara jadi dan lolos inspeksi: render ulang, lalu `posting.py tambah` / `manual` dengan id sama):
| konten | jadwal WIB | file baru | file konten JSON |
|---|---|---|---|
| Edukasi: perjalanan satu order (Remotion, voice 2026-11-01-reel1-alur) | 2026-11-01 19:30 | media/2026-11-01/reel1-alur.mp4 | konten/2026-11-01-edukasi.json |
| Realita: tiga permintaan harga jam 4 sore (Remotion, voice 2026-11-02-reel1-realita) — DIPINDAH ke Senin | 2026-11-09 19:30 | media/2026-11-09/reel1-realita.mp4 | konten/2026-11-09-realita.json |
| Realita: truk sampai, gudang tutup (Remotion, voice 2026-11-02-reel2-realita) | 2026-11-02 19:30 | media/2026-11-02/reel2-realita.mp4 | konten/2026-11-02-realita.json |
| Cerita: surat jalan yang tertukar (Remotion, voice 2026-11-03-reel1-cerita) | 2026-11-03 19:30 | media/2026-11-03/reel1-cerita.mp4 | konten/2026-11-03-cerita.json |
| Cerita: rem yang tidak boleh ditawar (Remotion, voice 2026-11-03-reel2-cerita) — DIPINDAH ke Jumat | 2026-11-06 19:30 | media/2026-11-06/reel2-cerita.mp4 | konten/2026-11-06-cerita.json |

Cara (31 Okt, setelah kuota reset ±14.00 WIB): naikkan "rev" di kelima `voice/requests/<id>.json` dalam SATU commit, push, tunggu `voice/out/<id>/done.json` (+ dengar.json). Lalu `python3 engine/whatif.py render <file konten>` (render semua post di file), cek 4–5 frame, `python3 engine/cek_konten.py media/<tgl>/<slot>.mp4 <voice_id> 1`, `python3 engine/scan_konten.py <file konten>`, lalu `python3 engine/posting.py tambah <file konten>` dan push. Story & feed 1–3 Nov sudah di halaman.
Catatan: kalau pemeriksa dengar Gemini kena kuota, transkrip bisa dicek dengan ElevenLabs Scribe (dipakai 30 Okt untuk MST baris 4).
