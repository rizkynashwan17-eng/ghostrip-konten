# Susulan suara (dikerjakan tugas harian 15.40 WIB, langkah A)

Rizky sudah mengizinkan: lengkapi suara TANPA bertanya. Sejak 29 Okt 2026 mode posting manual: setelah suara jadi, render ulang lalu perbarui halaman lewat `engine/posting.py` (bukan Metricool). Hapus baris dari tabel setelah berhasil diganti. Posting yang jamnya sudah lewat: hapus barisnya (tidak bisa diganti).

Request suara yang belum lengkap: (tidak ada). Nataru reel1-v2, Zero ODOL + vokal, salah hitung + vokal sudah bersuara dan sudah dipakai di halaman Posting (dicek Rizky 29 Okt).
Urutan pengerjaan TTS otomatis menurut kunci `"jadwal"` di request (tayang terdekat dulu), jadi kalau kuota habis yang paling dekat jadwalnya sudah aman duluan. 

Konten yang harus diperbarui di halaman Posting (setelah suara jadi dan lolos inspeksi: render ulang, lalu `posting.py tambah` / `manual` dengan id sama):
| konten | jadwal WIB | file baru | file konten JSON |
|---|---|---|---|
| Kelas jalan & MST (reel1-v2) — suara dibuat ulang: sebelumnya ada "Say curiously" (bahasa Inggris) + suara pecah. Kuota TTS habis 30 Okt dini hari; buat ulang setelah reset, INSPEKSI WAJIB (dengar.json lolos), render `python3 engine/render.py konten/2026-10-30-v2.json`, `python3 engine/posting.py tambah konten/2026-10-30-v2.json`, lalu ubah jam post id 2026-10-30-1130-reel1-v2 tetap 19:30 & kosongkan catatan | 2026-10-30 19:30 | media/2026-10-30/reel1-v2.mp4 | konten/2026-10-30-v2.json |
