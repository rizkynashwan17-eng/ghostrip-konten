# Susulan suara (dikerjakan tugas otomatis tiap hari 15.15 WIB, setelah kuota Gemini TTS reset)

Rizky sudah mengizinkan: lengkapi suara TANPA bertanya. Sejak 29 Okt 2026 mode posting manual: setelah suara jadi, render ulang lalu perbarui halaman lewat `engine/posting.py` (bukan Metricool). Hapus baris dari tabel setelah berhasil diganti. Posting yang jamnya sudah lewat: hapus barisnya (tidak bisa diganti).

Request suara yang belum lengkap: (tidak ada). 29 Okt 15.45 WIB: Nataru reel1-v2, Zero ODOL + vokal, salah hitung + vokal SUDAH bersuara & diganti di Metricool.
Urutan pengerjaan TTS otomatis menurut kunci `"jadwal"` di request (tayang terdekat dulu), jadi kalau kuota habis yang paling dekat jadwalnya sudah aman duluan. (Reels KIR 29 Okt SUDAH bersuara & diganti di Metricool 28 Okt sore — lewati.)

Posting Metricool yang harus diganti medianya (cari id terbaru via getScheduledPosts, cocokkan uuid; isi lain JANGAN diubah, salin dari getScheduledPosts):
| konten | jadwal WIB | uuid | file baru | file konten JSON |
|---|---|---|---|---|
| Kelas jalan & MST (reel1-v2) — suara dibuat ulang: sebelumnya ada "Say curiously" (bahasa Inggris) + suara pecah. Kuota TTS habis 30 Okt dini hari; buat ulang setelah reset, INSPEKSI WAJIB (dengar.json lolos), render `python3 engine/render.py konten/2026-10-30-v2.json`, `python3 engine/posting.py tambah konten/2026-10-30-v2.json`, lalu ubah jam post id 2026-10-30-1130-reel1-v2 tetap 19:30 & kosongkan catatan | 2026-10-30 19:30 | - | media/2026-10-30/reel1-v2.mp4 | konten/2026-10-30-v2.json |
