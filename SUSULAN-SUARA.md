# Susulan suara (dikerjakan tugas otomatis tiap hari 15.15 WIB, setelah kuota Gemini TTS reset)

Rizky sudah mengizinkan: lengkapi suara & ganti video di Metricool TANPA bertanya. Hapus baris dari tabel setelah berhasil diganti. Posting yang jamnya sudah lewat: hapus barisnya (tidak bisa diganti).

Request suara yang belum lengkap: `2026-10-31-reel1-v2`, `manual-odol`, `manual-salah-hitung`.
Urutan pengerjaan TTS otomatis menurut kunci `"jadwal"` di request (tayang terdekat dulu), jadi kalau kuota habis yang paling dekat jadwalnya sudah aman duluan. (Reels KIR 29 Okt SUDAH bersuara & diganti di Metricool 28 Okt sore — lewati.)

Posting Metricool yang harus diganti medianya (cari id terbaru via getScheduledPosts, cocokkan uuid; isi lain JANGAN diubah, salin dari getScheduledPosts):
| konten | jadwal WIB | uuid | file baru | file konten JSON |
|---|---|---|---|---|
| Reels Nataru | 31 Okt 11:30 | 4183418540628529089 | media/2026-10-31/reel1-v2.mp4 | konten/2026-10-31-v2.json |
| Reels Zero ODOL (video Rizky + vokal) | 31 Okt 19:00 | 2577346606753599253 | media/manual/reels-zero-odol-vo.mp4 | (video manual, pakai mix_manual.py) |
| Reels salah hitung / nombok (video manual + vokal) | 1 Nov 19:00 | -6088459601878496524 | media/2026-11-01/reel-salah-hitung-vo.mp4 | (video manual, pakai mix_manual.py) |

Vokal ODOL: `python3 engine/mix_manual.py media/manual/reels-zero-odol.mp4 manual-odol media/manual/reels-zero-odol-vo.mp4 "0.2,3.6,8.1,12.6,17.6,20.6" "3.5,8.0,12.5,17.0,20.5,24.5"`

Vokal salah hitung: `python3 engine/mix_manual.py media/2026-11-01/reel-salah-hitung.mp4 manual-salah-hitung media/2026-11-01/reel-salah-hitung-vo.mp4 "0.2,3.5,6.9,10.9,13.6,19.0" "3.3,6.7,10.7,13.3,18.7,22.3"`
