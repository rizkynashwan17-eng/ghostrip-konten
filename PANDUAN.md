# Panduan konten harian Ghostrip (dibaca oleh tugas terjadwal)

Tujuan: setiap hari otomatis membuat konten Ghostrip dan memasukkannya ke halaman Posting Ghostrip (Rizky memposting manual).

## STRATEGI KONTEN — ATURAN PATEN Rizky (30 Okt 2026), MENGGANTIKAN semua aturan tema/topik/cara pikir lama
Baca dan ikuti `STRATEGI-KONTEN.md` (teks asli dari Rizky) sebelum menulis konten apa pun — KECUALI arahan gaya grafik/visual di dalamnya (mis. bagian 5B, AI-generated visuals): itu TIDAK berlaku; gaya grafik video selalu mengikuti bagian GAYA VIDEO di bawah (sama persis dengan pilot). Ringkasan wajib:
- Tema per HARI (tanggal tayang, WIB). Dua Reels hari itu sama-sama mengikuti tema hari itu, dengan sudut/topik berbeda:
  - Senin: REALITA DUNIA LOGISTIK → hook → situasi nyata → masalah → pelajaran → soft selling (wajib, nyambung dengan masalah).
  - Selasa: CINEMATIC LOGISTICS STORYTELLING → TANPA selling: tidak menyebut Ghostrip di narasi, tanpa demo, tanpa CTA, caption juga tanpa CTA. Setelah cerita selesai: end card logo Ghostrip saja (adegan `logo`).
  - Rabu: TIPS ADMINISTRASI & WORKFLOW → hook → masalah → tips → kaitkan manfaat Ghostrip → soft selling wajib di akhir.
  - Kamis: GHOSTRIP FEATURE SHOWCASE → masalah → demonstrasi fitur yang BENAR-BENAR ada (hitung trip, riwayat, quotation PDF, TTD & cap, kop perusahaan, kirim ke WhatsApp) → manfaat → CTA relevan.
  - Jumat: CINEMATIC STORYTELLING kedua (aturan sama dengan Selasa; tema, konflik, tokoh & visual BERBEDA dari Selasa).
  - Sabtu: HUMOR/relatable ATAU EDUKASI logistik → soft selling wajib di akhir, tidak merusak humor/edukasi.
  - Minggu: FLEKSIBEL (tutorial, FAQ, polling, eksperimen cerita, tren relevan, edukasi, recap); soft selling opsional.
- Cerita (Selasa/Jumat): hook 1–3 dtk → setup → konflik → eskalasi → klimaks → ending → logo. Fiksi jangan diklaim nyata; nonfiksi wajib diverifikasi. Realisme logistik: istilah & kendaraan masuk akal, jangan mengarang prosedur teknis, jangan menampilkan berkendara berbahaya sebagai teladan.
- Soft selling: nyambung dengan masalah yang dibahas, natural, tidak menyebut Ghostrip berkali-kali, CTA tidak sama di setiap video, tanpa klaim hasil yang tidak terbukti ("pasti untung", "bebas kesalahan", hemat X% tanpa bukti).
- KERAHASIAAN INDUSTRI (wajib): DILARANG tarif aktual per rute sebagai patokan, rincian biaya operasional aktual, MARGIN/UNTUNG transporter, kontrak/penawaran pelanggan, tarif vendor, data customer. Boleh: proses kalkulasi secara umum, kategori biaya tanpa angka komersial, angka FIKTIF berlabel "simulasi".
- Copywriting: bahasa Indonesia natural, hook relevan, kalimat jelas, detail konkret; tanpa clickbait yang tidak sesuai isi.
- Checklist sebelum masuk halaman: 12 poin di bagian 11 `STRATEGI-KONTEN.md` (tema hari, tujuan, hook, akurasi, kerahasiaan, soft selling, bebas promosi untuk cerita, logo hanya di akhir, visual/audio/subtitle, caption per platform, klaim terverifikasi).
- Feed (17.00) & Reels (19.30) mengikuti tema hari yang sama (mis. Selasa: feed teaser cerita tanpa CTA di gambar; Rabu: feed checklist tips). STORY DIHENTIKAN sejak 6 Nov 2026 (PATEN 5 Nov).
- Pilot `konten/2026-11-02-whatif.json` HANYA referensi gaya visual. JANGAN dimasukkan ke halaman apa adanya (ada adegan untung→rugi dan biaya per rute yang dilarang aturan kerahasiaan).

## GAYA VIDEO — ATURAN PATEN Rizky (30 Okt 2026): SEMUA VIDEO BARU WAJIB REMOTION, gaya grafik SAMA PERSIS (ketiplek) dengan pilot
Referensi visual tunggal: `media/2026-11-02/reel1-whatif.mp4` (pilot jembatan timbang). WARNA BRAND IDENTITY WAJIB TETAP SAMA (Rizky, 30 Okt 2026): navy gelap/teal untuk latar, mint #7ff0d6 (positif/aksen), oranye #ff9d5c (kata kunci & aksen), krem untuk kartu kertas, merah hanya untuk peringatan; font Outfit; logo & hantu mint Ghostrip. Palet ada di `remotion/src/theme.ts` — jangan diubah. Jangan memakai gaya lain, AI-generated visuals, atau arahan visual dari STRATEGI-KONTEN.md. Isi/tema boleh beda, tampilan harus sama.
- Semua video baru (Reels) dibuat dengan Remotion (`remotion/` + `engine/whatif.py`), art style & grafik SAMA dengan pilot "jembatan timbang": malam sinematik navy-teal dengan cahaya cakrawala oranye, kamera push-in, butiran film & vinyet, kartu kertas krem, peta navy dengan garis rute bercahaya + penanda, kotak penghitung, teks besar per frasa (Outfit tebal, kata kunci oranye), label jam berjalan, tokoh flat Sopir topi oranye & Bos kumis, hantu Ghostrip mint. `engine/render.py` TIDAK dipakai lagi untuk video (story & feed masih boleh).
- SATU narator (Gemini TTS, satu request per video). 1 kalimat = 1 adegan.
- TOKOH & FORMAT BEBAS (Rizky, 30 Okt 2026): tidak harus Sopir bertanya/mengadu ke Bos. Boleh siapa saja yang relevan dengan dunia logistik — admin, dispatcher, customer, mekanik, vendor, keluarga sopir, pemilik armada, sales — dan format apa saja (cerita, POV, monolog, kilas balik, perbandingan, investigasi kecil). Tokoh tersedia di `Person` (parts.tsx): sopir, bos, admin, dispatcher, customer, mekanik; boleh menambah tokoh baru dengan gaya & palet yang sama.
- STORYLINE WAJIB BERISI: tiap adegan harus memajukan cerita atau memberi informasi/insight baru; tidak boleh adegan kosong, kalimat basa-basi, atau mengulang poin. Ada hook kuat, konflik/masalah yang jelas, dan penutup yang memuaskan (pelajaran, twist, atau keputusan). Sebelum render, baca ulang naskah: kalau ada kalimat yang bisa dihapus tanpa mengurangi cerita, hapus.
- Kartu judul adegan pertama: field `seri` (mis. "REALITA LOGISTIK", "CERITA", "TIPS ADMIN", "FITUR GHOSTRIP", "POV", "GIMANA KALAU…") + `judul` + `part`.
- Penutup: hari dengan soft selling → adegan `cta` (tagline & ajakan disesuaikan, tidak sama tiap video); Selasa/Jumat → adegan `logo` (end card logo saja, tanpa ajakan).
- Jenis adegan tersedia (remotion/src/scenes.tsx): jalan, dokumen, timbangan, stat, aturan, karakter, peta, struk, angka, cta, logo. Boleh menambah jenis adegan baru di scenes.tsx asalkan memakai komponen & palet yang sama (parts.tsx: NightSky, Lamp, Bokeh, Paper, Truck, Person, Camera, Grain) supaya gaya tetap konsisten.
- Durasi: alat, bukan target; umumnya 25–60 dtk (scan Remotion: 15–90 dtk).
- File: `konten/YYYY-MM-DD-whatif.json`, field tambahan `tema` = realita | cerita | tips | fitur | humor | edukasi | bebas.
- Langkah: (1) `python3 engine/whatif.py suara konten/X-whatif.json` → push → tunggu `voice/out/<id>/done.json` (+ `dengar.json`); (2) `python3 engine/whatif.py render konten/X-whatif.json`; (3) cek visual 4–5 frame; (4) inspeksi; (5) `python3 engine/posting.py tambah konten/X-whatif.json`, push. `--tanpa-suara` hanya untuk pratinjau, tidak boleh masuk halaman.
- Inspeksi untuk video Remotion lebih ringan (permintaan Rizky): wajib ada narasi, tidak ada suara pecah/klik, dan pemeriksa dengar lolos — kalau pemeriksa dengar hanya terkendala kuota (`belum_dicek`), boleh masuk halaman asalkan `cek_konten` lainnya AMAN; ditambah cek visual singkat. Aturan tema & kerahasiaan tetap dicek (`scan_konten.py` sudah memeriksanya).

## GAYA REELS SELANG-SELING — ATURAN PATEN Rizky (5 Nov 2026): GAYA LAMA dan GAYA BEDAH TEKNIKAL berganti SETIAP HARI mulai Minggu 8 Nov 2026
- Penentu tunggal: `python3 engine/gaya_reels.py <tanggal> <jumlah hari>`. 8, 10, 12 Nov … (selisih hari GENAP dari 8 Nov) = **bedah**; 9, 11, 13 Nov … (GANJIL) = **whatif** (gaya lama pilot reel1-whatif). Contoh: Minggu 8 bedah, Senin 9 lama, Selasa 10 bedah, Rabu 11 lama, Kamis 12 bedah, dst. `scan_konten.py` MENOLAK Reels yang gayanya tidak sesuai tanggal.
- Hari gaya LAMA: ikut tema harian (STRATEGI KONTEN) seperti biasa. Hari gaya BEDAH: Reels bertema **teknikal** (field `"tema": "teknikal"`, `"gaya": "bedah"`) — seputar teknis dunia trucking & logistik (rem, ban, beban & sumbu/JBI, ODOL, kopling & transmisi, sistem angin, kelistrikan, BBM & konsumsi solar, perawatan, muatan & pengikatan, kontainer, jembatan timbang, dokumen teknis kendaraan, dll.); tema harian hari itu TIDAK berlaku untuk Reels (feed tetap ikut tema hari). Reels cerita Selasa/Jumat hanya dibuat bila hari itu gaya lama.
- GAYA BEDAH WAJIB DETAIL (permintaan Rizky): penjelasan mekanisme langkah demi langkah (apa komponennya → bagaimana bekerja → apa yang terjadi saat gagal → kenapa → cara mencegah), dan ANIMASI PENJELASAN DETAIL: potongan (cutaway) komponen 3D yang benar-benar bergerak (aliran udara/oli/panas, tekanan, gaya, putaran), angka teknis yang terverifikasi, label penunjuk pada bagian yang dibahas. Minimal 5 sudut/ilustrasi 3D berbeda per video, minimal 2 kartu sumber kredibel (KNKT, Kemenhub, pabrikan, jurnal, media otomotif tepercaya) dengan tanggal; angka/klaim tanpa sumber DILARANG. Durasi ±45–60 dtk, 1 kalimat = 1 adegan, ditutup adegan `logo`.
- TAMPILAN KHAS GHOSTRIP (wajib BEDA JAUH dari video referensi supaya aman hak cipta; jangan meniru judul, subtitle, letak logo, warna, atau tata letak referensi): latar blueprint gelap navy-teal bergrid; LOGO MELAYANG di TENGAH ATAS (`logo_float.png` hantu tanpa kotak + "Ghostrip.id"); judul bab bernomor (bulatan oranye + topik mint + judul putih di tengah, kata kunci mint bergaris oranye, tanpa huruf miring); subtitle TANPA kotak (kata muncul bertahap, kata yang diucapkan mint); label chip navy berbingkai mint dengan titik penanda; kartu sumber navy dengan tanda kutip mint; kata besar gaya STEMPEL oranye; tulisan "Ilustrasi" kecil di kanan bawah. Warna brand (theme.ts) dan font Outfit.
- Mesin: `remotion/src/Bedah.tsx` (komposisi "Bedah", 3D three.js lewat @remotion/three). Adegan yang ada: `jalan` (truk di jalan menurun; opsi laju, goyang, zoom, gigi, panahMesin, trukX), `rem` (tromol dibelah; tekan, panas0/panas1, putar), `angin` (tabung angin + gauge bar0/bar1). Untuk topik lain BUAT komponen adegan 3D baru di Bedah.tsx dengan gaya yang sama (primitif three.js, bahan matte, cahaya lembut, latar blueprint) dan daftarkan di `Scene3D`; cek still per adegan (`npx remotion still src/index.ts Bedah out.png --frame=N --props=public/run/props.json --gl=swangle`) sebelum render penuh.
- Alur: file `konten/<tanggal>-bedah.json` (post reel `engine` remotion, `gaya` bedah, `tema` teknikal, `scenes` dengan kicker/judul/label/kutipan/boom), `python3 engine/whatif.py suara <file>` → push → tunggu workflow suara → `python3 engine/whatif.py render <file>` (3D: ±40 menit di server 2 core, jalankan di latar) → inspeksi → `posting.py tambah`.
- Pilot pertama: `konten/2026-11-08-bedah.json` (rem blong di turunan panjang). Reels gaya lama yang sudah bersuara dipindah supaya cocok dengan selang-seling: "PP dua kali lipat?" → Minggu 15 Nov, "surat jalan yang tertukar" (cerita) → Jumat 13 Nov.

## GAYA FEED — ATURAN PATEN Rizky (4 Nov 2026): SEMUA FEED 17.00 memakai gaya EDITORIAL
- Mesin: `engine/feed_editorial.py` (render.py melewati feed yang punya `scene.layout`). Contoh acuan: feed 4 Nov `media/2026-11-04/feed-tips.jpg` (disukai Rizky).
- Gaya (dari referensi Pinterest Rizky): judul besar tebal Outfit, satu frasa *miring + garis sapuan*, ~aksen~ warna, kapsul miring bernomor, gelembung chat, panah coretan tangan, panel bersudut bulat (kartu quotation krem berlabel SIMULASI sebagai pengganti foto), catatan kecil kiri bawah, logo **Ghostrip.id** (ikon + ".id") kanan bawah.
- WARNA (revisi Rizky 4 Nov): feed harus KOHESIF seperti referensi, BUKAN tiap post beda warna. Warna utama = TEAL brand (#1d5a63, paling sering), selingan NAVY (#071a22) dan KREM (#f2ead9), aksen SELALU mint #7ff0d6 (kapsul, garis sapuan, chat), oranye #ff9d5c hanya sentuhan kecil (angka, 1 kapsul, panah). Latar mint penuh / oranye penuh TIDAK dipakai. Pola default per hari: Sen teal, Sel navy, Rab teal, Kam krem, Jum navy, Sab teal, Min krem (feed 4 Nov navy tetap karena acuan).
- Layout: `checklist` (panel dokumen + kapsul), `alur` (kartu langkah bernomor + PDF), `chat` (gelembung + kapsul opsional), `file` (tumpukan kapsul nama file + maskot). Boleh tambah layout baru asal gaya sama.
- Format scene: `{"layout","warna","kicker","pill","title","title_size","sub","items","chat":[{"dari":"kiri|kanan","nama","teks"}],"doc":{"judul","sub","rows"},"kartu","note"}`. Tanpa emoji di layar. Feed cerita (Sel/Jum): tanpa ajakan/CTA di gambar.
- Setelah render: lihat gambarnya (tidak ada teks bertumpuk/meluber; mesin memberi PERINGATAN bila meluber) + `scan_konten.py`.

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

## Riset fakta (tetap berlaku)
- Setiap fakta/angka/aturan harus dicek dengan WebSearch/WebFetch ke sumber yang jelas (situs pemerintah: Kemenhub, BPJT, JDIH/peraturan.bpk.go.id; media: Kompas, Detik, Bisnis.com, Kontan, CNBC, Antara; produsen truk resmi).
- Tulis sumbernya di kartu FAKTA (`"source": "Kemenhub, 2025"` atau nama media + bulan/tahun) dan di akhir caption ("Sumber: …").
- Kalau fakta tidak bisa dipastikan dari sumber, JANGAN dipakai. Pilih fakta lain. Lebih baik sederhana tapi benar.
- Jangan mengarang angka statistik, kutipan pejabat, atau tanggal aturan.


(Aturan lama "Arah konten", "Bank topik" dan "Variasi format, alur & latar lokasi" DIHAPUS 30 Okt 2026 — diganti STRATEGI KONTEN di atas.)

## Produk & aturan merek
- Ghostrip = aplikasi hitung harga trip truk + quotation PDF (kop, TTD, cap, PPN/PPh), riwayat hitungan, pengaturan solar/markup/jenis truk per akun.
- Langganan Rp149 rb/bln, **coba gratis 7 hari**, **komen DEMO** atau WA **0815-1704-7930**. IG @ghostrip.app, TikTok @ghostrip.id.
- Keputusan harga SELALU di tangan **bos**. Sopir/admin boleh menghitung, bos yang approve.
- Jangan mengarang fitur lain (GPS, AI, akuntansi, dll). Tanpa testimoni fiktif, tanpa klaim jumlah pengguna, tanpa "pasti untung".
- Nama perusahaan/orang harus FIKTIF (PT Maju Jaya Logistik, PT Makmur Semakmurnya, Ibu Gadis, Budi Santoso). DILARANG: "PT Gunung Inti Gemilang", "Ibu Lermi", "Trans Anugrah".

## Jadwal standar (WIB, Asia/Jakarta) — ATURAN PATEN Rizky (5 Nov 2026): mulai 6 Nov 2026 SATU HARI = 1 FEED (17:00) + 1 REELS (19:30), TANPA STORY. Tambahan: KARTU KOSONG "Feed manual" jam 12:00 untuk gambar buatan Rizky sendiri (lihat bagian FEED MANUAL RIZKY). (1 Nov: 1 Reels/hari.)
| slot | jenis | jam | platform di halaman |
|---|---|---|---|
| feed-manual | kartu KOSONG, gambar dibuat & diunggah Rizky sendiri (bukan buatan Claude) | 12:00 | IG post (+FB) |
| feed | gambar editorial 1080×1350 (atau carousel) | 17:00 | IG post (+FB) |
| reel | video Remotion gaya pilot reel1-whatif (tema hari itu) | 19:30 | IG reel + TikTok + FB |
- WAJIB: 1 Reels per hari (bukan 2), dibuat dengan Remotion; gaya SELANG-SELING mulai 8 Nov 2026 (gaya lama pilot `media/2026-11-02/reel1-whatif.mp4` ↔ gaya BEDAH TEKNIKAL, lihat bagian GAYA REELS SELANG-SELING), plus 1 feed gaya editorial. TIDAK ADA story (dihentikan 6 Nov 2026): jangan membuat, merender, atau memasukkan story ke halaman (`posting.py`, `render.py`, `scan_konten.py` sudah melewatinya).
- Facebook Page diposting manual oleh Rizky lewat Meta Business Suite (halaman selalu menampilkannya).
- Feed = ringkasan/checklist yang bisa disimpan, gaya editorial, sesuai tema hari dan nyambung ke Reels hari itu.
- Stok cadangan Reels yang sudah ditulis tapi belum masuk halaman: cek `konten/*.json` dan `SUSULAN-SUARA.md` sebelum membuat Reels baru untuk suatu tanggal (jangan dobel). Saat ini: 6 Nov (cerita: rem yang tidak boleh ditawar), 9 Nov (realita: tiga permintaan harga jam empat sore).

## FEED MANUAL RIZKY — ATURAN PATEN Rizky (5 Nov 2026): feed mockup 12:00 DIBUAT RIZKY SENDIRI; Claude hanya menyediakan kartu & caption
- Rizky membuat gambar feed (mockup foto/perangkat) sendiri. Claude TIDAK membuatnya otomatis dan tugas harian tidak boleh membuatnya. (Mesin `engine/foto_feed.py`, `feed_mockup.py`, `latar_tekstur.py` hanya arsip/uji, tidak dipakai di alur harian.)
- Tempat di jadwal: kartu kosong `feed-manual` jam 12:00 per hari (`python3 engine/posting.py slot-manual <tanggal> [<tanggal> ...]`), mengikuti stok hari ini s.d. hari+2 (tugas harian menambahkannya bila belum ada). Di halaman Posting kartu itu punya tombol "Unggah gambar" (gambar tersimpan di HP Rizky, lalu Bagikan/Simpan/Sudah seperti kartu lain).
- Caption: Rizky mengirim gambarnya ke Claude di chat dengan kata "caption". Claude melihat gambar, menulis caption (hook + isi singkat, caption selalu beda dari sebelumnya, tanpa nama asli/harga/data sensitif, + penutup baku), menyimpan gambar ke `foto/manual/<tanggal>.jpg`, lalu `python3 engine/posting.py isi-manual <id> --media foto/manual/<tanggal>.jpg --caption-file cap.txt`, commit & push. Caption TIDAK dibuat sebelum gambarnya diterima.
- Tugas harian hanya memastikan kartu kosongnya ada; tidak mengisi dan tidak melaporkannya sebagai kekurangan stok.

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
Catatan 30 Okt 2026: Reels dibuat dengan Remotion (lihat GAYA VIDEO); tema mengikuti STRATEGI KONTEN per hari. Langkah engine/render.py di bawah hanya untuk feed/carousel (story sudah dihentikan).
1. Clone/pull repo. Baca `RIWAYAT.md` (hindari topik 30 hari terakhir).
2. Pilih 2 topik reel + 1 topik feed, RISET dulu (lihat di atas), catat sumbernya.
3. Tulis `konten/YYYY-MM-DD.json` (contoh lengkap: `konten/2026-10-28-v2.json`).
4. SUARA (Gemini TTS lewat GitHub Actions): `python3 engine/render.py --voice-requests konten/YYYY-MM-DD.json` → commit & push (file `voice/requests/*.json`) → tunggu sampai `voice/out/<voice_id>/done.json` muncul di origin/main (cek `git fetch` tiap 15 dtk, maks 12 menit) → `git pull`. Kalau gagal/`error.txt` (kuota harian habis), lanjutkan TANPA suara; video tetap dibuat dengan musik + teks, LALU tambahkan baris ke tabel `SUSULAN-SUARA.md` (konten, jadwal WIB, file mp4, file konten JSON) supaya tugas harian berikutnya melengkapi suaranya dan memperbarui halaman tanpa perlu izin Rizky.
   Teks `say` ditulis seperti orang bicara: angka & singkatan yang sulit dibaca tulis dengan huruf di `say` ("dua ribu dua puluh tujuh", "sepuluh ton"). Opsional `"tone"`: penasaran/kaget/santai/menjelaskan/kecewa/senang/mengajak/tegas.
5. `python3 engine/render.py konten/YYYY-MM-DD.json`, lalu CEK VISUAL: ambil 4–5 frame tiap reel (`ffmpeg -ss <detik> -i <mp4> -frames:v 1 x.jpg`) + gambar story/feed dan lihat dengan Read. Pastikan teks tidak keluar kartu/terpotong, kartu tidak menimpa karakter atau bar dialog. Perbaiki JSON (teks lebih pendek, hapus `illus`, dll) lalu render ulang.
5b. SCAN WAJIB (ATURAN PATEN Rizky, 28 Okt 2026): `python3 engine/scan_konten.py konten/YYYY-MM-DD.json`. Mengecek aspek & resolusi (reel/story 1080x1920 9:16, feed/carousel 1080x1350 4:5), durasi reel 15–45 dtk, audio, voiceover & kualitas suara, jumlah slide, caption (CTA, #ghostrip, panjang, hashtag), tiktok_title ≤ 90, emoji di layar, nama terlarang. Kalau ada "PERBAIKI" → perbaiki JSON, render & scan ulang sampai `semua_aman: true`. Cantumkan hasil scan di laporan.
6. Tambah baris ke `RIWAYAT.md`, commit & push ke `main`.
7. URL media = `https://raw.githubusercontent.com/rizkynashwan17-eng/ghostrip-konten/<SHA-commit>/<path>`.
8. MASUK HALAMAN (WAJIB, tanpa menunggu persetujuan Rizky): begitu scan dan inspeksi AMAN, jalankan `python3 engine/posting.py tambah konten/YYYY-MM-DD-v2.json` (hanya slot yang masih kosong; cek `posting.py daftar` dulu; konten manual Rizky dihitung mengisi slot sejenis). Reels → platform IG + TikTok, story/feed/carousel → IG. Caption dan `tiktok_title` (≤ 90 karakter) diambil dari JSON konten.
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

## Caption — PENUTUP BAKU (ATURAN PATEN Rizky, 4 Nov 2026) berlaku untuk SEMUA caption (reel, feed, carousel; IG, TikTok, FB; semua tema termasuk cerita)
Struktur: isi singkat (hook/pertanyaan + 1–3 baris isi, catatan "Cerita fiksi. Nama tokoh rekaan." / "Angka dan data: simulasi" bila perlu), lalu penutup baku PERSIS ini (sumber tunggal: `engine/caption_akhir.py`):

```
🚛 Mau urusan logistik lebih praktis?

Coba Ghostrip gratis selama 7 hari!

📲 WhatsApp: 0815-1704-7930
🌐 ghostrip.id

#Ghostrip #LogistikIndonesia #Transportasi #BisnisLogistik #AplikasiLogistik
```
- Jangan menulis CTA, nomor WA, atau hashtag lain di badan caption (hashtag hanya 5 dari penutup baku).
- Pasang/rapikan otomatis: `python3 engine/caption_akhir.py konten/<file>.json`. `engine/posting.py tambah` juga memasangnya sendiri; `scan_konten.py` menolak caption yang tidak berakhir dengan penutup baku.
- Cerita (Selasa/Jumat): badan caption tetap tanpa promosi/CTA (narasi video tanpa Ghostrip); hanya penutup baku yang menutup caption (permintaan Rizky 4 Nov).
- Emoji hanya di caption, bukan di gambar. Sumber fakta ("Sumber: …") boleh di badan bila ada.
