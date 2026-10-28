# Panduan konten harian Ghostrip (dibaca oleh tugas terjadwal)

Tujuan: setiap hari otomatis membuat & menjadwalkan konten Ghostrip di Metricool.
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


## Variasi format & alur (WAJIB, permintaan Rizky 28 Okt)
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
| slot | jenis | jam | Metricool |
|---|---|---|---|
| story | foto 1080×1920 | 07:30 | instagram STORY |
| reel1 | video 18–25 dtk | 11:30 | instagram REEL + tiktok |
| feed | foto 1080×1350 (atau carousel) | 17:00 | instagram POST |
| reel2 | video 18–25 dtk | 19:30 | instagram REEL + tiktok |
Facebook Page belum terhubung; kalau `getBrandSettings` menunjukkan facebookData, tambahkan facebook.
Reel1 & reel2 = dua topik BERBEDA. Story boleh polling/pertanyaan yang nyambung ke reel hari itu. Feed = ringkasan fakta yang bisa disimpan (compare, list, atau carousel 3–5 slide).


## Sistem stok konten (H-2) — dijalankan tugas harian 15.40 WIB (ATURAN PATEN & WAJIB dari Rizky)
Setiap kali membuat, mengisi suara, atau mengganti konten WAJIB diakhiri laporan update untuk Rizky: tanggal & jam tayang, topik, status suara (✅/⏳), dan masalah bila ada. Tugas ini tidak boleh dilewati/dimatikan kecuali Rizky memintanya.
Urutan setiap hari:
A. SUSULAN SUARA dulu (kuota Gemini baru saja reset): kerjakan semua baris di `SUSULAN-SUARA.md` (lihat isi file itu).
B. CEK STOK: `getScheduledPosts` dari besok s.d. hari+5. Hari dianggap "terisi" kalau slot Reels 11:30 & 19:30 (atau Reels manual Rizky di malam hari) sudah ada.
   - Kalau hari pertama yang BELUM terisi masih > 2 hari lagi (stok aman ≥ H-2): JANGAN buat konten. Akhiri dengan 1 baris "Stok aman sampai <tanggal>." (hemat usage).
   - Kalau hari kosong pertama ≤ hari+2: buat konten untuk SEMUA hari kosong sampai hari+4 (biasanya 2–3 hari sekaligus), hanya slot yang kosong.
C. Suara: kirim semua request sekaligus. Yang tidak kebagian kuota → Reels tetap dijadwalkan tanpa suara + dicatat di `SUSULAN-SUARA.md` (diproses besok di langkah A, masih sebelum jam tayang karena stok ≥ 2 hari).
D. Bersih-bersih repo: hapus folder `media/<tanggal>` dan `voice/out/<tanggal>-*` yang tanggalnya ≥ 10 hari lalu (Metricool sudah menyimpan salinan media sendiri).

## Langkah membuat konten (dipakai di langkah B)
1. Clone/pull repo. Baca `RIWAYAT.md` (hindari topik 30 hari terakhir).
2. Pilih 2 topik reel + 1 topik feed, RISET dulu (lihat di atas), catat sumbernya.
3. Tulis `konten/YYYY-MM-DD.json` (contoh lengkap: `konten/2026-10-28-v2.json`).
4. SUARA (Gemini TTS lewat GitHub Actions): `python3 engine/render.py --voice-requests konten/YYYY-MM-DD.json` → commit & push (file `voice/requests/*.json`) → tunggu sampai `voice/out/<voice_id>/done.json` muncul di origin/main (cek `git fetch` tiap 15 dtk, maks 12 menit) → `git pull`. Kalau gagal/`error.txt` (kuota harian habis), lanjutkan TANPA suara; video tetap dibuat dengan musik + teks, LALU setelah dijadwalkan tambahkan baris ke tabel `SUSULAN-SUARA.md` (konten, jadwal WIB, uuid Metricool, file mp4, file konten JSON) supaya tugas susulan jam 15.15 WIB melengkapi suaranya dan mengganti video di Metricool tanpa perlu izin Rizky.
   Teks `say` ditulis seperti orang bicara: angka & singkatan yang sulit dibaca tulis dengan huruf di `say` ("dua ribu dua puluh tujuh", "sepuluh ton"). Opsional `"tone"`: penasaran/kaget/santai/menjelaskan/kecewa/senang/mengajak/tegas.
5. `python3 engine/render.py konten/YYYY-MM-DD.json`, lalu CEK VISUAL: ambil 4–5 frame tiap reel (`ffmpeg -ss <detik> -i <mp4> -frames:v 1 x.jpg`) + gambar story/feed dan lihat dengan Read. Pastikan teks tidak keluar kartu/terpotong, kartu tidak menimpa karakter atau bar dialog. Perbaiki JSON (teks lebih pendek, hapus `illus`, dll) lalu render ulang.
6. Tambah baris ke `RIWAYAT.md`, commit & push ke `main`.
7. URL media = `https://raw.githubusercontent.com/rizkynashwan17-eng/ghostrip-konten/<SHA-commit>/<path>`.
8. Jadwalkan dengan `createScheduledPost` (blogId `7702870`, timezone Asia/Jakarta, autoPublish true, draft false), hanya slot yang masih kosong (cek `getScheduledPosts` dulu; konten manual Rizky dihitung mengisi slot sejenis).
   - Reels: instagramData {type REEL, showReelOnFeed true, isAiGenerated true}, tiktokData {title ≤ 90 karakter, privacyOption PUBLIC_TO_EVERYONE, isAigc true, commercialContentOwnBrand true}.
   - Story: instagramData {type STORY, isAiGenerated true}, tanpa text.
   - Feed/carousel: instagramData {type POST, isAiGenerated true}.
9. Verifikasi dengan `getScheduledPosts`.

## Format JSON (engine v2)
Setiap scene reel (dan `scene` story/feed, `slides` carousel) memakai kunci berikut (semua opsional kecuali yang jelas dibutuhkan):
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
