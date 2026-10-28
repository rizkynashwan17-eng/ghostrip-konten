# Susulan suara (dikerjakan tugas otomatis tiap hari 15.15 WIB, setelah kuota Gemini TTS reset)

Rizky sudah mengizinkan: lengkapi suara & ganti video di Metricool TANPA bertanya. Hapus baris dari tabel setelah berhasil diganti. Posting yang jamnya sudah lewat: hapus barisnya (tidak bisa diganti).

Request suara yang belum lengkap: `2026-10-30-reel1-v2`, `2026-10-31-reel1-v2`, `manual-odol`. (Reels KIR 29 Okt SUDAH bersuara & diganti di Metricool 28 Okt sore — lewati.)

Posting Metricool yang harus diganti medianya (cari id terbaru via getScheduledPosts, cocokkan uuid; isi lain JANGAN diubah, salin dari getScheduledPosts):
| konten | jadwal WIB | uuid | file baru | file konten JSON |
|---|---|---|---|---|
| Reels kelas jalan | 30 Okt 11:30 | -8436520620524353127 | media/2026-10-30/reel1-v2.mp4 | konten/2026-10-30-v2.json |
| Reels Nataru | 31 Okt 11:30 | 4183418540628529089 | media/2026-10-31/reel1-v2.mp4 | konten/2026-10-31-v2.json |
| Reels Zero ODOL (video Rizky + vokal) | 31 Okt 19:00 | 2577346606753599253 | media/manual/reels-zero-odol-vo.mp4 | (video manual, pakai mix_manual.py) |

Vokal ODOL: `python3 engine/mix_manual.py media/manual/reels-zero-odol.mp4 manual-odol media/manual/reels-zero-odol-vo.mp4 "0.2,3.6,8.1,12.6,17.6,20.6" "3.5,8.0,12.5,17.0,20.5,24.5"`
