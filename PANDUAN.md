# Panduan konten harian Ghostrip (dibaca oleh tugas terjadwal)

Tujuan: setiap hari otomatis membuat konten Ghostrip dan memasukkannya ke halaman Posting Ghostrip (Rizky memposting manual).

## FORMAT REELS BARU: "GIMANA KALAU…" (Remotion) — ATURAN PATEN Rizky (30 Okt 2026)
Mulai stok berikutnya (konten yang dibuat setelah stok lama habis), SEMUA Reels baru dibuat dengan Remotion gaya "Gimana kalau…" (referensi: video "what if" animasi sinematik yang dikirim Rizky). Story & feed tetap pakai `engine/render.py`.
- Struktur: judul seri "GIMANA KALAU… <SKENARIO> · PART n" + label jam & lokasi di adegan pertama; SATU narator (bukan dialog); ganti adegan cepat (1 kalimat = 1 adegan, ±2–4 dtk); kamera push-in; selingan infografis (peta rute + penghitung, kartu aturan kertas, struk biaya, layar angka); teks besar per frasa di tengah bawah dengan kata kunci oranye; label jam berjalan; penutup CTA hantu Ghostrip.
- Warna brand: malam navy-teal, cahaya cakrawala & kata kunci oranye #ff9d5c, positif mint #7ff0d6, peringatan merah. Font Outfit. Tokoh: Sopir topi oranye, Bos kumis, hantu Ghostrip (tanpa topi).
- Isi: skenario nyata dunia trucking (jembatan timbang/ODOL, solar naik di tengah trip, salah rute jalan kelas III, ban pecah di tol, macet Nataru, trip pulang kosong, dll.) yang berujung ke biaya/untung-rugi, lalu "padahal bisa dihitung sebelum berangkat". Variasi PATEN tetap: skenario & lokasi berganti; rotasi tipe adegan; jangan ulang skenario dalam 14 hari. Angka biaya pakai rumus Ghostrip & tandai "*ilustrasi"; fakta aturan wajib sumber (cek web); keputusan harga di tangan bos.
- File: `konten/YYYY-MM-DD-whatif.json` (contoh: `konten/2026-11-02-whatif.json`; format & jenis adegan di docstring `engine/whatif.py` dan `remotion/src/scenes.tsx`: jalan, dokumen, timbangan, stat, aturan, karakter, peta, struk, angka, cta). Durasi target 25–40 dtk (scan: 15–45).
- Langkah: (1) `python3 engine/whatif.py suara konten/X-whatif.json` → push (SATU request TTS per video, hemat kuota) → tunggu workflow `voice.yml` sampai `voice/out/<id>/done.json` + `dengar.json` lolos; (2) `python3 engine/whatif.py render konten/X-whatif.json` (pertama kali otomatis `npm install` di `remotion/`; Chromium bawaan dipakai); (3) cek visual beberapa frame (teks tidak menimpa, tidak terpotong); (4) INSPEKSI WAJIB di bawah; (5) `python3 engine/posting.py tambah konten/X-whatif.json`, push.
- `--tanpa-suara` hanya untuk pratinjau; video tanpa narasi DILARANG masuk halaman posting.

## INSPEKSI WAJIB SETELAH MEMBUAT KONTEN — ATURAN PATEN Rizky (29 Okt 2026)
Setiap konten yang baru dibuat atau suaranya diganti WAJIB langsung dicek sebelum masuk halaman posting. Tidak boleh ada yang lolos tanpa inspeksi.
1. Suara: `engine/tts_gemini.py` (satu model per video, tolak suara pecah/terpotong/kepanjangan, normalisasi -3 dBFS) lalu `engine/dengar_gemini.py` (Gemini mendengarkan tiap baris, transkrip dicocokkan dengan naskah, deteksi kresek/distorsi/bahasa salah; baris gagal otomatis dibuat ulang). Keduanya jalan otomatis di workflow `voice.yml`. Tunggu sampai `voice/out/<id>/dengar.json` ada dengan `"lolos": true`.
2. Video: `python3 engine/cek_konten.py <mp4> <voice_id> <jumlah_dialog>` → harus status AMAN (voiceover lengkap, tidak ada sampel pecah, tidak kresek, intonasi hidup, pemeriksa dengar lolos, model seragam).
3. Konten: `python3 engine/scan_konten.py konten/YYYY-MM-DD.json` → semua_aman true.
4. Baru setelah ketiganya AMAN: `python3 engine/posting.py tambah ...`, push. Kalau tidak AMAN: perbaiki/buat ulang; kalau sampai tugas selesai masih gagal, JANGAN dimasukkan ke halaman — catat di SUSULAN-SUARA.md dan laporkan ke Rizky beserta alasannya.
5. Laporan harian menyebut hasil inspeksi tiap konten (✅ lolos semua / ⚠️ alasan).

## MODE POSTING MANUAL — ATURAN PATEN sejak 29 Okt 2026 (Metricool TIDAK dipakai lagi, semua langkah di bawah memakai halaman Posting)
Rizky memilih posting manual (Instagram sempat terputus dari Metricool, kuota Metricool terbatas). Metricool tidak dipakai lagi: jangan memanggil tool Metricool sama sekali (createScheduledPost, updateScheduledPost, getScheduledPosts), kecuali Rizky sendiri memintanya. Semua posting lama di Metricool sudah draft.
- Halaman: `index.html` (GitHub Pages, https://rizkynashwan17-eng.github.io/ghostrip-konten/) membaca `posting/jadwal.json`. Rizky membuka halaman, ketuk Bagikan → IG/TikTok/Meta Business Suite (Facebook Page, diposting manual oleh Rizky lewat Meta Business Suite) (caption tersalin otomatis), lalu centang Sudah. Pengingat kalender di HP Rizky: 07.30, 11.30, 17.00, 19.30 setiap hari.
- Perintah halaman (`engine/posting.py`): `daftar` (cek stok/slot), `tambah konten/YYYY-MM-DD-v2.json` (otomatis memakai `media/<tanggal>/manifest.json`, versi `-vo.mp4` dipakai kalau ada; id sama = diganti, dipakai juga untuk susulan suara), `manual ...` (video manual Rizky, lihat docstring), `catatan <id> "teks"`, `bersihkan 10`. Media yang masih tercantum di `posting/jadwal.json` jangan dihapus.
- Wajib commit & push `posting/jadwal.json` + semua media yang dirujuk (halaman mengambil media dari repo). Setelah push, cek `https://raw.githubusercontent.com/rizkynashwan17-eng/ghostrip-konten/main/posting/jadwal.json` berisi konten baru.
- Laporan harian ke Rizky tetap wajib; sebut konten baru yang masuk halaman (tanggal · jam · jenis · topik · status suara).
- Label AI & aturan merek tetap berlaku (caption tanpa nama asli terlarang, dll.).

Tidak ada orang yang mengecek sebelum tayang, jadi patuhi semua aturan di bawah.

## Arah konten (WAJIB)
Konten = CAMPURAN format (lihat "Variasi format & alur"): cerita/sketsa, fakta & aturan detail, kuis, mitos vs fakta, hitung-hitungan biaya, tips, demo. Penonton harus terhibur atau belajar sesuatu yang konkret, lalu di akhir dikaitkan ke harga trip dan ditutup CTA Ghostrip. Bukan iklan keras.
Catatan: 28–31 Okt semuanya format FAKTA → konten berikutnya utamakan CERITA, KUIS, MITOS, HITUNG.

### Riset fakta (WAJIB sebelum menulis)
- Setiap fakta/angka/aturan harus dicek dengan WebSearch/WebFetch ke sumber yang jelas (situs pemerintah: Kemenhub, BPJT, JDIH/peraturan.bpk.go.id; media: Kompas, Detik, Bisnis.com, Kontan, CNBC, Antara; produsen truk resmi).
- Tulis sumbernya di kartu FAKTA (`"source": "Kemenhub, 2025"` atau nama media + bulan/tahun) dan di akhir caption ("Sumber: …").
- Kalau fakta tidak bisa dipastikan dari sumber, JANGAN dipakai. Pilih fakta lain. Lebih baik sederhana tapi benar.
- Jangan mengarang angka statistik, kutipan pejabat, atau tanggal aturan.

### Bank topik (putar, jangan ulang dalam 30 hari; boleh topik baru sejenis)
- Arti istilah: CDD/CDE, fuso, tronton, wingbox, trailer 20ft/40ft, GVW/JBB/JBI, gandar/sumbu, MST.
- Aturan: Zero ODOL 2027, kelas jalan & MST, uji KIR berkala, golongan tol per jumlah gandar, pembatasan truk saat libur panjang/mudik, jam operasional truk di kota besar, batas kecepatan truk di tol, larangan lajur kanan.
- Teknis: kenapa truk pakai solar, kenapa roda belakang ganda, blind spot truk, kenapa truk jalan pelan di tanjakan, konsumsi solar per jenis truk, ban & tekanan angin, rem angin.
- Bisnis: komponen biaya trip (solar, tol, uang jalan, makan/inap sopir, bongkar muat, retribusi), muatan balik (backhaul), cara menentukan markup, PPN/PPh di quotation, kenapa harga trip harus dihitung ulang saat solar naik.
- Sejarah/fun fact: asal nama merek/istilah truk, truk terpanjang/terberat di Indonesia (jika ada sumber).


## Variasi format, alur & latar lokasi — ATURAN PATEN & WAJIB (Rizky, 28 Okt 2026)
Konten TIDAK boleh fun fact terus dan alur TIDAK boleh monoton. Putar format berikut:
| kode | format | contoh alur scene |
|---|---|---|
| CERITA | sketsa/drama pendek Bos–Sopir–Admin–Customer dengan konflik & twist, pelajaran di akhir | adegan jalan (`type: road`) → chat customer → linimasa H1/H2/H3 (`items` + `tag`) → Bos kaget (`char2` dua karakter) → solusi → cta |
| FAKTA | tahukah kamu / arti istilah / aturan | kicker → fact → compare/list → stat → cta |
| KUIS | tebak-tebakan, jawaban muncul belakangan | pertanyaan + `mark: "quiz"`, `answer`, `reveal` (detik) → penjelasan fact → cta |
| MITOS | mitos vs fakta | compare kiri "MITOS" (illus warn) vs kanan "FAKTA" → fact + sumber → cta |
| HITUNG | studi kasus angka/biaya trip (fiktif tapi masuk akal) | chat/rute → list biaya → stat total → "kalau lupa X, rugi Y" → cta |
| TIPS | cara/langkah praktis untuk bos ekspedisi | judul angka ("3 cara…") → items num → stat → cta |
| DEMO | fitur Ghostrip dipakai di situasi nyata (tanpa mengarang fitur) | masalah → hantu datang → langkah pakai app → hasil → cta |

Aturan rotasi:
- Dalam satu hari, reel1 dan reel2 HARUS format berbeda. Dalam 3 hari berturut-turut, maksimal 2 reel FAKTA; minimal 1 CERITA per 2 hari.
- Scene pembuka bergantian: pertanyaan, pernyataan mengejutkan/angka besar (`stat`), adegan cerita (road/chat), kuis. Jangan selalu `kicker` + judul.
- Urutan blok berbeda tiap reel (jangan selalu fact → list → stat). Panjang 4–6 scene, durasi scene bervariasi.
- LATAR LOKASI (permintaan Rizky): jangan di meja terus. Setiap reel minimal 2 scene memakai `set` lokasi, dan scene meja kantor (karakter tanpa `set`) maksimal 2 per reel. Pilihan `set`: `jalan` (truk melaju, pohon), `malam` (bulan, bintang, lampu jalan), `tol` (gerbang tol, palang terbuka, truk masuk), `timbangan` (gantry WIM), `spbu` (kanopi SOLAR, dispenser), `gudang` (pintu rolling, tumpukan muatan, truk mundur), `pool` (parkiran armada). Atur `truck`: box/wing/tank/over/empty, `drive`: true/false, `gantry`: teks papan. Karakter di lokasi otomatis berdiri di kiri bawah (atau `:right`). Jangan pakai set yang sama 2 scene berturut-turut kecuali bagian cerita.
- Ganti suasana warna `tint`: teal (default), orange, blue, purple, red (masalah/rugi) — maksimal 2 reel berurutan dengan tint sama.
- Karakter bergantian memimpin: kadang Sopir, kadang Admin/Customer, kadang Hantu sebagai narator; pakai `char2` untuk adegan dua orang.
- Story: putar polling, kuis, teaser, "tebak angka", behind-the-scene. Feed: putar tabel/simpan ini, carousel cerita, mitos vs fakta, checklist.
- Catat format di kolom RIWAYAT (mis. "CERITA: trip molor 3 hari"), dan cek riwayat sebelum memilih.
- Format CERITA/HITUNG/DEMO boleh tanpa sumber berita, tapi angka harus masuk akal dan nama orang/perusahaan fiktif; fakta aturan tetap wajib bersumber.

## Produk & aturan merek
- Ghostrip = aplikasi hitung harga trip truk + quotation PDF (kop, TTD, cap, PPN/PPh), riwayat hitungan, pengaturan solar/markup/jenis truk per akun.
- Langganan Rp149 rb/bln, **coba gratis 7 hari**, **komen DEMO** atau WA **0815-1704-7930**. IG @ghostrip.app, TikTok @ghostrip.id.
- Keputusan harga SELALU di tangan **bos**. Sopir/admin boleh menghitung, bos yang approve.
- Jangan mengarang fitur lain (GPS, AI, akuntansi, dll). Tanpa testimoni fiktif, tanpa klaim jumlah pengguna, tanpa "pasti untung".
- Nama perusahaan/orang harus FIKTIF (PT Maju Jaya Logistik, PT Makmur Semakmurnya, Ibu Gadis, Budi Santoso). DILARANG: "PT Gunung Inti Gemilang", "Ibu Lermi", "Trans Anugrah".

## Jadwal standar (WIB, Asia/Jakarta)
| slot | jenis | jam | platform di halaman |
|---|---|---|---|
| story | foto 1080×1920 | 07:30 | IG story |
| reel1 | video 18–25 dtk | 11:30 | IG reel + TikTok |
| feed | foto 1080×1350 (atau carousel) | 17:00 | IG post |
| reel2 | video 18–25 dtk | 19:30 | IG reel + TikTok |
Facebook Page diposting manual oleh Rizky lewat Meta Business Suite (halaman selalu menampilkannya).
Reel1 & reel2 = dua topik BERBEDA. Story boleh polling/pertanyaan yang nyambung ke reel hari itu. Feed = ringkasan fakta yang bisa disimpan (compare, list, atau carousel 3–5 slide).


## Sistem stok konten (H-2) — dijalankan tugas harian 15.40 WIB (ATURAN PATEN & WAJIB dari Rizky)
Setiap kali membuat, mengisi suara, atau mengganti konten WAJIB diakhiri laporan update untuk Rizky: tanggal & jam tayang, topik, status suara (✅/⏳), dan masalah bila ada. Tugas ini tidak boleh dilewati/dimatikan kecuali Rizky memintanya.
Urutan setiap hari:
A. SUSULAN SUARA dulu (kuota Gemini baru saja reset): kerjakan semua baris di `SUSULAN-SUARA.md` (lihat isi file itu).
   A0. CEK OTOMATIS REELS TANPA SUARA (tidak perlu disuruh): lihat semua Reels di `posting/jadwal.json` (hari ini s.d. +7; `python3 engine/posting.py daftar`). Cari sumbernya di repo (manifest `media/<tanggal>/`, `konten/*.json`, `media/manual/`). Kalau belum bersuara (tidak ada `voice/out/<id>/done.json`, atau video manual yang audionya hanya musik) → tulis voiceover Claude: buat `voice/requests/<id>.json` (kalimat pendek sesuai durasi scene, isi `"jadwal": "YYYY-MM-DDTHH:MM"`), tambah baris + perintah mix ke `SUSULAN-SUARA.md`, push. Video manual pakai `engine/mix_manual.py` dengan jendela waktu per scene.
   PRIORITAS KUOTA: `engine/tts_gemini.py` mengerjakan request urut `jadwal` terdekat dulu. Kalau kuota habis, Reels yang paling dekat tayang diselesaikan lebih dulu; sisanya menunggu reset (±14:00 WIB) selama jamnya belum lewat.
B. CEK STOK: `python3 engine/posting.py daftar` dari besok s.d. hari+5. Hari dianggap "terisi" kalau slot Reels 11:30 & 19:30 (atau Reels manual Rizky di malam hari) sudah ada.
   - Kalau hari pertama yang BELUM terisi masih > 2 hari lagi (stok aman ≥ H-2): JANGAN buat konten. Akhiri dengan 1 baris "Stok aman sampai <tanggal>." (hemat usage).
   - Kalau hari kosong pertama ≤ hari+2: buat konten untuk SEMUA hari kosong sampai hari+4 (biasanya 2–3 hari sekaligus), hanya slot yang kosong.
C. Suara: kirim semua request sekaligus. Yang tidak kebagian kuota → Reels tetap masuk halaman tanpa suara + dicatat di `SUSULAN-SUARA.md` (diproses besok di langkah A, masih sebelum jam tayang karena stok ≥ 2 hari), dengan catatan ⚠️ di halaman bila belum layak diposting.
C2. MASUK HALAMAN: konten yang sudah AMAN (lihat "INSPEKSI WAJIB") langsung dimasukkan ke halaman dengan `posting.py tambah` / `manual`, push, tanpa menunggu disuruh. Yang tidak aman jangan dimasukkan; laporkan alasannya.
D. Bersih-bersih repo: `python3 engine/posting.py bersihkan 10`, hapus folder `media/<tanggal>` dan `voice/out/<tanggal>-*` yang tanggalnya ≥ 10 hari lalu, kecuali media yang masih ada di `posting/jadwal.json`.

## Langkah membuat konten (dipakai di langkah B)
1. Clone/pull repo. Baca `RIWAYAT.md` (hindari topik 30 hari terakhir).
2. Pilih 2 topik reel + 1 topik feed, RISET dulu (lihat di atas), catat sumbernya.
3. Tulis `konten/YYYY-MM-DD.json` (contoh lengkap: `konten/2026-10-28-v2.json`).
4. SUARA (Gemini TTS lewat GitHub Actions): `python3 engine/render.py --voice-requests konten/YYYY-MM-DD.json` → commit & push (file `voice/requests/*.json`) → tunggu sampai `voice/out/<voice_id>/done.json` muncul di origin/main (cek `git fetch` tiap 15 dtk, maks 12 menit) → `git pull`. Kalau gagal/`error.txt` (kuota harian habis), lanjutkan TANPA suara; video tetap dibuat dengan musik + teks, LALU tambahkan baris ke tabel `SUSULAN-SUARA.md` (konten, jadwal WIB, file mp4, file konten JSON) supaya tugas harian berikutnya melengkapi suaranya dan memperbarui halaman tanpa perlu izin Rizky.
   Teks `say` ditulis seperti orang bicara: angka & singkatan yang sulit dibaca tulis dengan huruf di `say` ("dua ribu dua puluh tujuh", "sepuluh ton"). Opsional `"tone"`: penasaran/kaget/santai/menjelaskan/kecewa/senang/mengajak/tegas.
5. `python3 engine/render.py konten/YYYY-MM-DD.json`, lalu CEK VISUAL: ambil 4–5 frame tiap reel (`ffmpeg -ss <detik> -i <mp4> -frames:v 1 x.jpg`) + gambar story/feed dan lihat dengan Read. Pastikan teks tidak keluar kartu/terpotong, kartu tidak menimpa karakter atau bar dialog. Perbaiki JSON (teks lebih pendek, hapus `illus`, dll) lalu render ulang.
5b. SCAN WAJIB (ATURAN PATEN Rizky, 28 Okt 2026): `python3 engine/scan_konten.py konten/YYYY-MM-DD.json`. Mengecek aspek & resolusi (reel/story 1080x1920 9:16, feed/carousel 1080x1350 4:5), durasi reel 15–45 dtk, audio, voiceover & kualitas suara, jumlah slide, caption (CTA, #ghostrip, panjang, hashtag), tiktok_title ≤ 90, emoji di layar, nama terlarang. Kalau ada "PERBAIKI" → perbaiki JSON, render & scan ulang sampai `semua_aman: true`. Cantumkan hasil scan di laporan.
6. Tambah baris ke `RIWAYAT.md`, commit & push ke `main`.
7. URL media = `https://raw.githubusercontent.com/rizkynashwan17-eng/ghostrip-konten/<SHA-commit>/<path>`.
8. MASUK HALAMAN (WAJIB, tanpa menunggu persetujuan Rizky): begitu scan dan inspeksi AMAN, jalankan `python3 engine/posting.py tambah konten/YYYY-MM-DD-v2.json` (hanya slot yang masih kosong; cek `posting.py daftar` dulu; konten manual Rizky dihitung mengisi slot sejenis). Reels → platform IG + TikTok, story/feed/carousel → IG. Story tanpa caption. Caption dan `tiktok_title` (≤ 90 karakter) diambil dari JSON konten.
9. Commit & push `posting/jadwal.json` + semua media yang dirujuk, lalu verifikasi `https://raw.githubusercontent.com/rizkynashwan17-eng/ghostrip-konten/main/posting/jadwal.json` berisi konten baru.

## Format JSON (engine v2)
Setiap scene reel (dan `scene` story/feed, `slides` carousel) memakai kunci berikut (semua opsional kecuali yang jelas dibutuhkan):
- `set`: latar lokasi (jalan/malam/tol/timbangan/spbu/gudang/pool), judul & kartu tetap di atas, lokasi di bawah.
- `dur` detik (3.5–5.5). `type`: kosong (biasa), `"road"` (truk jalan di jalan raya, + `gantry` teks papan, `truck` = box/over/tank/wing), `"calendar"` (+ `calendar` {top, date}), `"cta"` (penutup, WAJIB di akhir setiap reel).
- `kicker` pil mint kecil di atas judul (mis. "TAHUKAH KAMU?", "FUN FACT", "ATURAN BARU").
- `title` judul besar; `*kata*` = sorotan mint. Maks ±8 kata.
- `badge` {text, color: red/orange/mint} pil miring di bawah judul (mis. "2 bulan lagi DILARANG").
- `fact` {n, head, body, source} kartu FAKTA. body maks ±25 kata.
- `compare` {left:{illus,label,sub,color,dual}, right:{…}} dua sisi dengan panah. illus: truck_box, truck_over, truck_tank, truck_wing, truck_empty, two_trucks, atau ikon fuel/clock/scale/toll/doc/money/warn. `dual: true` = roda belakang ganda.
- `stat` {label, value, color: red/mint/orange, size} kartu putih angka besar.
- `items` daftar kartu (+ `mark`: check/x/num, `gap`).
- `chat` {name, lines[]} kotak chat putih.
- `illus` satu ilustrasi tengah (nama sama dengan di atas).
- `char` karakter: `bos:neutral|happy|sad|shocked|think` (+ `:up` tangan naik, `:left`/`:right`), `sopir:<mood>`, atau `ghost`. Bos/sopir otomatis duduk di balik meja.
- `say` {who: BOS/SOPIR/HANTU/ADMIN/CUSTOMER, text} bar dialog bawah. Maks ±12 kata. Setiap scene reel sebaiknya punya `say`.
- `glow` (default true), `sparkles`, `tint`: teal/orange/blue/purple/red (warna suasana).
- `char2`: karakter kedua (mis. `"char": "bos:shocked:right", "char2": "sopir:happy:left"`).
- `items` boleh berisi objek `{"text": "...", "tag": "H1"}` (label oranye, cocok untuk linimasa cerita).
- Kuis: `"mark": "quiz", "answer": <index 0-based>, "reveal": <detik>` → pilihan A/B/C, jawaban benar menyala setelah `reveal`.
Jangan menumpuk terlalu banyak di satu scene: maksimal 2 blok (mis. fact + stat, atau title + compare) + karakter.
Untuk story/feed: footer @ghostrip.app otomatis; tidak ada bar dialog.

## Caption
3–7 baris: hook pertanyaan, penjelasan fakta singkat, kaitan ke harga trip/Ghostrip, CTA "Coba gratis 7 hari, komen DEMO atau WA 0815-1704-7930", "Sumber: …", 6–10 hashtag (#ghostrip selalu ada, + #funfact/#tahukahkamu bila cocok). Emoji hanya di caption, bukan di gambar.
