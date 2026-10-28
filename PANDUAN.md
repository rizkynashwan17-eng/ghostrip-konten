# Panduan konten harian Ghostrip (dibaca oleh tugas terjadwal)

Tujuan: setiap hari otomatis membuat & menjadwalkan 4 konten Ghostrip di Metricool.
Tidak ada orang yang mengecek sebelum tayang, jadi patuhi semua aturan di bawah.

## Produk & audiens
- Ghostrip = aplikasi hitung harga trip truk + quotation PDF untuk perusahaan trucking/ekspedisi kecil-menengah di Indonesia.
- Langganan Rp149 rb/bulan, **coba gratis 7 hari**, daftar lewat **WA 0815-1704-7930**. Instagram @ghostrip.app, TikTok @ghostrip.id.
- Penonton: pemilik usaha truk (±70% yang menghitung harga) dan admin (±30%).
- ATURAN WAJIB: keputusan harga selalu di tangan **bos**. Sopir/admin boleh menghitung, bos yang approve. Jangan pernah menggambarkan aplikasi "menggantikan bos".
- Fitur yang boleh disebut: hitung harga trip (jarak, solar, tol, uang jalan, markup, jenis truk), riwayat hitungan, quotation PDF dengan kop, TTD & cap, PPN/PPh, pengaturan per akun, bisa dipakai beberapa akun. JANGAN mengarang fitur lain (mis. GPS tracking, AI, integrasi akuntansi).
- Nama perusahaan/orang di konten harus FIKTIF (contoh: PT Maju Jaya Logistik, PT Makmur Semakmurnya, Ibu Gadis). DILARANG: "PT Gunung Inti Gemilang", "Ibu Lermi", "Trans Anugrah", atau nama perusahaan asli lain.
- Angka biaya harus masuk akal (solar ±Rp6.800/liter, CDD ±4–5 km/liter, fuso ±3 km/liter) dan total harus benar secara hitungan.
- Bahasa Indonesia santai-sopan ("bos", "customer", "trip"). Tanpa klaim berlebihan ("pasti untung", "nomor 1").

## Jadwal (WIB, Asia/Jakarta)
| slot | jenis | jam | platform Metricool |
|---|---|---|---|
| story | foto 1080×1920 | 07:30 | instagram STORY |
| reel1 | video ±15–20 dtk | 11:30 | instagram REEL + tiktok |
| feed | foto 1080×1350 | 17:00 | instagram POST |
| reel2 | video ±15–20 dtk | 19:30 | instagram REEL + tiktok |
Facebook Page belum terhubung di Metricool; kalau `getBrandSettings` menunjukkan facebookData, tambahkan facebook (REEL/STORY/POST sesuai slot).

## Langkah harian
1. `git clone` repo ini (atau `git pull`). Baca `RIWAYAT.md` agar topik/hook tidak berulang dalam 14 hari terakhir.
2. Tulis `konten/YYYY-MM-DD.json` (tanggal hari ini WIB) mengikuti contoh `konten/2026-10-29.json`. Pilih 2 sudut berbeda untuk reel1 & reel2 dari "Bank ide" di bawah.
3. `python3 engine/render.py konten/YYYY-MM-DD.json` lalu cek beberapa frame (ffmpeg -ss … -frames:v 1) dan gambar story/feed: teks tidak terpotong/menumpuk, tidak ada kotak kosong (emoji tidak bisa tampil di gambar; emoji hanya boleh di caption).
4. Tambah baris ke `RIWAYAT.md`, commit & push ke `main`.
5. URL media = `https://raw.githubusercontent.com/rizkynashwan17-eng/ghostrip-konten/<SHA-commit>/<path>` (pakai SHA, bukan `main`).
6. Jadwalkan 4 posting dengan `createScheduledPost` (blogId `7702870`, timezone Asia/Jakarta, autoPublish true, draft false). Lewati slot yang jamnya sudah lewat.
   - Reels: media=[mp4], instagramData {type REEL, showReelOnFeed true, isAiGenerated true}, tiktokData {title ≤ 90 karakter, privacyOption PUBLIC_TO_EVERYONE, isAigc true, commercialContentOwnBrand true}, providers instagram+tiktok, text = caption.
   - Story: media=[jpg], instagramData {type STORY, isAiGenerated true}, text kosong.
   - Feed: media=[jpg], instagramData {type POST, isAiGenerated true}, text = caption.
7. Cek dengan `getScheduledPosts` bahwa 4 posting ada. Kalau ada yang gagal, coba sekali lagi; kalau tetap gagal, laporkan di ringkasan akhir.

## Format JSON & jenis scene
- Scene video: `hook` (teks besar + hantu kaget/sedih), `chat` (gelembung WA; me=true = bubble kanan), `calc` (kartu hitungan Ghostrip, rows + total + note), `list` (daftar dengan ✓ atau ✗, mark "check"/"x"), `text` (teks + sub, `truck: true` untuk truk lewat), `question` (pertanyaan + pilihan), `cta` (penutup, wajib di akhir setiap reel).
- `*kata*` = disorot mint. Ekspresi hantu: happy, shocked, sad, wink.
- Durasi tiap scene 3–6 dtk, total reel 14–20 dtk, 4–5 scene. Teks per scene maksimal ±12 kata.
- Story memakai 1 scene (`question`, `list`, atau `text`), feed memakai 1 scene (`list` paling cocok, size 60–66, item_size 40–44).
- Caption: 3–6 baris, ada ajakan "Coba gratis 7 hari, chat WA 0815-1704-7930", 6–10 hashtag (#ghostrip selalu ada).

## Bank ide (putar bergantian, boleh variasi baru yang sejenis)
- Customer nanya harga, bos lambat jawab → customer lari.
- Biaya yang sering kelupaan (solar naik, tol pulang, makan/inap sopir, bongkar muat, retribusi).
- Bikin quotation masih ketik ulang di Word → Ghostrip PDF langsung dengan kop, TTD & cap.
- Admin salah ketik angka di quotation → malu ke customer.
- Harga solar naik, tarif lama masih dipakai → untung hilang.
- Sopir di lapangan bisa hitung, bos tinggal approve dari HP.
- Beda harga CDD vs fuso vs wingbox: kenapa harus dihitung per jenis truk.
- Markup asal-asalan vs markup pasti.
- Riwayat hitungan: customer minta harga rute yang sama, tinggal buka riwayat.
- PPN/PPh di quotation sering salah hitung.
- Tips bisnis truk umum (negosiasi harga, rute balik/muatan pulang, catat biaya per trip) dengan Ghostrip sebagai penutup.
- Testimoni fiktif TIDAK boleh. Klaim jumlah pengguna TIDAK boleh.
