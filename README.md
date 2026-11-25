# YAMOTO DECEPTION LAB

Aplikasi desktop Windows yang berjalan secara lokal untuk membantu pencatatan eksperimen dan pengukuran fitur visual maupun sinyal audio. Proyek ini masih berada dalam tahap uji coba (beta).

> **Penting — aplikasi ini bukan alat pendeteksi kebohongan.** YAMOTO DECEPTION LAB tidak dapat menentukan apakah seseorang berkata jujur atau berbohong. Gerakan wajah, tatapan, bentuk geometri wajah, suara, kegugupan, maupun perilaku seseorang bukan bukti kebohongan. Hasil aplikasi hanya berupa pengukuran teknis untuk keperluan observasi dan penelitian.

## 1. Informasi versi dan status

| Informasi | Keterangan |
|---|---|
| Nama aplikasi | YAMOTO DECEPTION LAB |
| Versi installer | 0.2.0 |
| Platform paket | Windows 64-bit (x64) |
| Format installer | NSIS (.exe) |
| Status | Beta / uji coba terbatas |
| Penyimpanan | Lokal di komputer pengguna (SQLite) |
| Koneksi server | Tidak diperlukan untuk pemrosesan fitur media |
| Pengujian otomatis | Build, instalasi, startup smoke test, pemeriksaan engine, uninstall, dan checksum berhasil di Windows CI 64-bit |
| Pengujian Windows 11 fisik | Belum dilakukan |

**Catatan versi:** nomor versi installer mengikuti konfigurasi paket desktop. Versi internal engine dapat berbeda.

## 2. Sebelum memasang aplikasi

### Persyaratan

- Komputer atau laptop dengan Windows 10/11 64-bit (x64).
- Ruang penyimpanan kosong yang cukup. Disarankan menyediakan sekitar 1 GB untuk unduhan, ekstraksi, dan instalasi.
- Izin untuk memasang aplikasi di Windows.
- Kamera hanya diperlukan jika ingin mencoba fitur Camera Preview.
- File gambar, video, atau audio WAV diperlukan untuk mencoba fitur analisis media.

Pengguna biasa **tidak perlu memasang Node.js, Python, Rust, Git, atau perangkat pengembangan lainnya**. Komponen engine disertakan di dalam paket installer.

### Penting untuk pengguna yang menerima file dari teman

Repository GitHub proyek ini bersifat privat. Tautan GitHub Actions hanya dapat dibuka oleh akun yang memiliki akses ke repository. Jika kamu tidak memiliki akses, minta pengembang membagikan file ZIP installer melalui media berbagi file yang tepercaya.

Pastikan file ZIP diterima secara utuh dan checksum di dalamnya ikut disertakan. Jangan menjalankan installer yang sumbernya tidak jelas.

## 3. Cara mengunduh installer

1. Masuk ke akun GitHub yang memiliki akses ke repository.
2. Buka [Windows build workflow run #25](https://github.com/suryowedossusilo-netizen/YAMOTO-DECEPTION-LAB-/actions/runs/45602451522).
3. Pada halaman hasil workflow, gulir ke bagian **Artifacts**.
4. Pilih dan unduh artifact bernama **yamoto-deception-lab-windows-x64**.
5. Hasil unduhan berupa file ZIP. Ekstrak ZIP tersebut ke folder yang mudah ditemukan, misalnya folder Downloads.
6. Di dalam folder hasil ekstraksi akan terdapat:
   - `YAMOTO DECEPTION LAB_0.2.0_x64-setup.exe` — file installer aplikasi.
   - `YAMOTO DECEPTION LAB_0.2.0_x64-setup.exe.sha256` — file checksum untuk memeriksa integritas installer.

Artifact GitHub Actions memiliki masa penyimpanan terbatas sesuai konfigurasi workflow. Jika artifact tersebut sudah kedaluwarsa, pengembang perlu menyediakan build terbaru.

## 4. Periksa keamanan file dengan SHA-256

Langkah ini disarankan sebelum memasang aplikasi. Tujuannya memastikan file installer yang diterima sama dengan file yang checksum-nya disediakan.

1. Buka folder hasil ekstraksi ZIP.
2. Klik kanan area kosong di folder tersebut, lalu pilih **Open in Terminal** atau buka PowerShell dan arahkan ke folder itu.
3. Jalankan perintah berikut:

```powershell
$installer = ".\YAMOTO DECEPTION LAB_0.2.0_x64-setup.exe"
$checksumFile = "$installer.sha256"
$expected = ((Get-Content $checksumFile -Raw).Trim() -split '\s+')[0]
$actual = (Get-FileHash $installer -Algorithm SHA256).Hash

if ($actual -ne $expected) {
    throw "SHA-256 tidak cocok. Jangan jalankan installer."
}

Write-Host "SHA-256 cocok. File installer lolos pemeriksaan integritas."
```

Jika muncul pesan **SHA-256 cocok**, file lolos pemeriksaan integritas terhadap checksum yang disertakan. Jika checksum tidak cocok, file checksum tidak ditemukan, atau perintah menghasilkan error, **jangan jalankan installer**. Unduh ulang atau minta pengembang mengirimkan ulang paketnya.

Pemeriksaan checksum memastikan file tidak berubah dari file yang menjadi acuan checksum; pemeriksaan ini bukan sertifikasi bahwa aplikasi bebas dari seluruh risiko keamanan.

## 5. Cara memasang aplikasi

1. Pastikan file installer sudah lolos pemeriksaan SHA-256.
2. Klik dua kali `YAMOTO DECEPTION LAB_0.2.0_x64-setup.exe`.
3. Jika Windows menampilkan jendela konfirmasi, periksa kembali nama dan sumber file sebelum melanjutkan.
4. Ikuti instruksi yang muncul pada installer.
5. Tunggu hingga proses instalasi selesai.
6. Buka **YAMOTO DECEPTION LAB** melalui Start Menu atau shortcut desktop jika tersedia.
7. Tunggu beberapa saat sampai halaman utama tampil dan status workspace diperbarui.

### Jika Windows menampilkan peringatan keamanan

Build beta dapat memunculkan peringatan Windows SmartScreen atau peringatan aplikasi yang tidak dikenal, misalnya karena installer belum memiliki tanda tangan digital dari penerbit tepercaya. Jangan mengabaikan peringatan hanya karena aplikasi berasal dari teman. Pastikan sumber file, nama file, dan checksum sudah diverifikasi. Jika masih ragu, hentikan instalasi dan hubungi pengembang.

## 6. Panduan menggunakan aplikasi

Tampilan aplikasi memiliki empat menu utama: **Overview**, **Live Analysis**, **Dataset**, dan **Experiment Lab**.

### A. Overview

Halaman ini merupakan ringkasan kondisi aplikasi.

Yang dapat diperiksa:
- **Engine:** menunjukkan apakah engine lokal berhasil terhubung.
- **Datasets:** jumlah dataset yang telah dibuat.
- **Experiments:** jumlah eksperimen yang telah dibuat.
- **Media Features:** menunjukkan status kesiapan dependensi fitur media.

Ketika aplikasi baru pertama kali dipasang, jumlah dataset dan eksperimen dapat bernilai nol. Itu normal. Jika Engine menunjukkan OFFLINE atau Media Features menunjukkan CHECK DEPENDENCIES, catat pesan yang tampil dan laporkan kepada pengembang.

Tombol **Open live preview** akan membawa pengguna ke menu Live Analysis.

### B. Live Analysis — Camera Preview

Fitur ini digunakan untuk menguji apakah aplikasi dapat meminta izin dan menampilkan kamera.

Langkah pengujian:
1. Buka menu **Live Analysis**.
2. Pada bagian **Camera preview**, tekan **Start camera**.
3. Jika Windows menampilkan permintaan izin kamera, pilih izinkan hanya jika kamu memang ingin menguji fitur tersebut.
4. Pastikan gambar dari kamera tampil pada area preview.
5. Tekan **Stop camera** untuk menghentikan kamera.

Hal yang perlu diketahui:
- Camera Preview hanya menampilkan gambar kamera secara langsung.
- Preview ini tidak melakukan perekaman.
- Preview kamera tidak otomatis dianalisis.
- Kamera akan dihentikan ketika pengguna menekan Stop camera atau aplikasi ditutup.

Jika kamera tidak tampil, periksa apakah kamera sedang digunakan aplikasi lain, apakah izin kamera Windows/browser untuk aplikasi desktop sudah tersedia, dan apakah perangkat kamera terdeteksi oleh Windows.

### C. Live Analysis — Facial Geometry (gambar)

Fitur ini menggunakan MediaPipe Face Mesh untuk mengambil titik-titik landmark wajah dan menghitung beberapa rasio geometri dari **satu gambar**.

Format yang diterima:
- PNG
- JPG/JPEG
- WEBP

Batas pemrosesan:
- Ukuran file maksimal 15 MB.
- Dimensi gambar maksimal 20 megapiksel.
- Pemrosesan dibatasi untuk satu wajah.

Langkah pengujian:
1. Siapkan gambar wajah milik sendiri atau gambar peserta yang telah memberikan persetujuan.
2. Gunakan gambar yang jelas, tidak terlalu gelap, wajah tidak tertutup, dan menghadap kamera.
3. Buka menu **Live Analysis**.
4. Cari bagian **Facial geometry (MediaPipe)**.
5. Pilih file gambar melalui tombol pemilihan file.
6. Tunggu sampai proses selesai.
7. Periksa bagian **Feature extraction result**.

Hasil dapat memuat informasi seperti:
- `face_detected`: apakah wajah terdeteksi.
- `landmarks_count`: jumlah titik landmark yang diperoleh.
- `frame_width` dan `frame_height`: ukuran gambar.
- `face_box_normalized`: perkiraan kotak area wajah dalam koordinat ternormalisasi.
- `left_eye_openness_geometry` dan `right_eye_openness_geometry`: rasio geometri area mata.
- `mouth_openness_geometry`: rasio geometri area mulut.

Jika wajah tidak terdeteksi, aplikasi dapat mengembalikan `face_detected: false`. Hal itu tidak berarti ada sesuatu yang salah dengan orang dalam gambar. Kualitas foto, sudut wajah, pencahayaan, resolusi, dan bagian wajah yang tertutup dapat memengaruhi hasil.

### D. Live Analysis — Video Facial Geometry

Fitur ini mengambil sampel frame dari video dan mengukur geometri wajah pada frame yang terpilih.

Format video yang didukung oleh pemroses:
- MP4
- MOV
- AVI

Batas pemrosesan:
- Ukuran file maksimal 15 MB.
- Durasi maksimal 5 menit.
- Pengambilan sampel kira-kira satu frame per detik.
- Maksimal sekitar 301 sampel frame.
- Pemrosesan dibatasi untuk satu wajah pada setiap frame.

Langkah pengujian:
1. Siapkan video pendek dengan wajah terlihat cukup jelas.
2. Pastikan orang yang direkam sudah memberikan persetujuan.
3. Buka **Live Analysis**.
4. Cari bagian **Video facial geometry**.
5. Pilih file video.
6. Tunggu proses selesai. Video yang lebih panjang atau perangkat yang lebih lambat dapat membutuhkan waktu lebih lama.
7. Periksa hasil pada bagian **Feature extraction result**.

Hasil dapat memuat:
- `duration_seconds`: durasi video yang diproses.
- `sampled_frames`: jumlah frame yang diperiksa.
- `face_detected_frames`: jumlah frame yang mendeteksi wajah.
- `face_detection_fraction`: proporsi frame yang mendeteksi wajah.
- `samples`: pengukuran tiap sampel beserta waktu dalam video.

Video diproses melalui file sementara agar dapat dibaca oleh pemroses video. File sementara tersebut dihapus setelah proses selesai. Jika proses gagal atau aplikasi tertutup secara tidak normal, laporkan kondisi tersebut kepada pengembang.

### E. Live Analysis — Audio Signal Measurements

Fitur audio mengukur karakteristik sinyal dasar dari file WAV. Fitur ini bukan pengenal ucapan dan tidak memahami isi percakapan.

Format yang diterima:
- WAV (`.wav`)

Batas pemrosesan:
- Ukuran file maksimal 15 MB.
- Durasi maksimal 10 menit.
- Sample rate antara 8.000 Hz sampai 192.000 Hz.

Langkah pengujian:
1. Siapkan file WAV yang boleh digunakan untuk pengujian.
2. Buka menu **Live Analysis**.
3. Cari bagian **Audio signal measurements**.
4. Pilih file WAV.
5. Tunggu sampai proses selesai.
6. Periksa hasil pengukuran.

Hasil dapat memuat:
- `duration_seconds`: durasi audio.
- `sample_rate_hz`: frekuensi sampling audio.
- `rms_amplitude` dan `rms_dbfs`: ukuran amplitudo rata-rata sinyal.
- `peak_amplitude`: amplitudo puncak.
- `zero_crossing_rate`: tingkat perubahan tanda sampel sinyal.
- `spectral_centroid_hz_first_window`: titik pusat spektral dari bagian awal sinyal yang dianalisis.

Hasil dipengaruhi oleh mikrofon, tingkat volume, kebisingan ruangan, format rekaman, codec, dan kualitas audio. Angka-angka tersebut tidak menunjukkan apakah pembicara jujur atau berbohong.

### F. Dataset

Menu **Dataset** digunakan untuk membuat dan melihat daftar dataset penelitian.

Cara membuat dataset:
1. Buka menu **Dataset**.
2. Isi kolom **Name** dengan nama dataset.
3. Isi **Description / research notes** dengan penjelasan singkat, misalnya tujuan pengumpulan data atau keterangan sumber data.
4. Tekan **Save locally**.
5. Periksa apakah dataset muncul pada bagian **Saved records**.

Data dataset disimpan pada database lokal di komputer pengguna. Buat nama dataset yang tidak memuat informasi pribadi peserta.

### G. Experiment Lab

Menu **Experiment Lab** digunakan untuk membuat dan melihat catatan eksperimen.

Cara membuat eksperimen:
1. Buka menu **Experiment Lab**.
2. Isi **Name** dengan nama eksperimen.
3. Isi **Description / research notes** dengan tujuan atau catatan eksperimen.
4. Tekan **Save locally**.
5. Pastikan catatan muncul pada bagian **Saved records**.

Status model saat ini tetap **NOT TRAINED**. Menu ini merupakan pencatatan eksperimen, bukan fitur untuk melatih model pendeteksi kebohongan.

## 7. Batasan file dan hal yang perlu diperhatikan

| Fitur | Format | Batas utama |
|---|---|---|
| Gambar wajah | PNG, JPG/JPEG, WEBP | 15 MB; 20 megapiksel |
| Video wajah | MP4, MOV, AVI | 15 MB; maksimal 5 menit |
| Audio | WAV | 15 MB; maksimal 10 menit; 8–192 kHz |
| Camera Preview | Kamera yang dikenali Windows | Preview langsung, bukan rekaman |

Jika file ditolak, periksa format, ukuran, durasi, dan kualitas file. Jangan mengganti ekstensi file secara manual untuk menyamarkan format yang sebenarnya tidak didukung.

## 8. Privasi dan penggunaan yang bertanggung jawab

Sebelum menguji gambar, video, atau audio orang lain:
- Minta persetujuan yang jelas dari orang yang bersangkutan.
- Jelaskan tujuan pengujian dan jenis data yang akan diproses.
- Gunakan data milik sendiri atau data uji yang memang diizinkan.
- Hindari mengunggah atau memproses rekaman pribadi, rahasia, atau sensitif tanpa izin.
- Gunakan ID samaran, bukan nama lengkap, nomor telepon, alamat, atau identitas pribadi.
- Jangan menyebarkan hasil analisis seseorang tanpa persetujuannya.

Pemrosesan fitur media dilakukan secara lokal. Engine tidak menyimpan byte gambar dan audio mentah sebagai arsip; data video ditempatkan sementara untuk proses decoding dan kemudian dihapus. Catatan observasi dan fitur hasil ekstraksi disimpan di database SQLite lokal. Karena data hasil tersimpan di perangkat, lindungi akun Windows dan perangkat yang digunakan.

Jangan gunakan aplikasi ini untuk menilai kejujuran seseorang, mengambil keputusan tentang pekerjaan, pendidikan, hubungan, kesehatan, hukum, atau keputusan penting lainnya. Jangan memperlakukan hasil pengukuran sebagai bukti ilmiah tentang emosi, kepribadian, niat, atau kebohongan.

Baca juga [SECURITY.md](SECURITY.md) dan [docs/AI-MODEL-LIMITATIONS.md](docs/AI-MODEL-LIMITATIONS.md).

## 9. Checklist pengujian untuk teman-teman

Silakan uji sesuai kemampuan perangkat. Tidak perlu memaksakan semua fitur jika tidak memiliki perangkat atau file yang sesuai.

- [ ] Installer dapat dibuka.
- [ ] Instalasi selesai tanpa error.
- [ ] Aplikasi dapat dijalankan setelah instalasi.
- [ ] Halaman Overview tampil.
- [ ] Status Engine menunjukkan CONNECTED.
- [ ] Status Media Features menunjukkan READY.
- [ ] Camera Preview dapat dimulai dan dihentikan (jika memiliki kamera).
- [ ] Gambar PNG/JPG/WEBP berhasil diproses.
- [ ] Video MP4/MOV/AVI berhasil diproses.
- [ ] Audio WAV berhasil diproses.
- [ ] Dataset dapat dibuat dan muncul pada Saved records.
- [ ] Experiment dapat dibuat dan muncul pada Saved records.
- [ ] Tombol refresh dapat memperbarui informasi.
- [ ] Aplikasi dapat ditutup dan dibuka kembali.
- [ ] Aplikasi dapat di-uninstall.

**Jangan menganggap semua fitur pasti berhasil hanya karena installer berhasil dipasang.** Tujuan uji coba ini justru untuk menemukan masalah yang mungkin belum terlihat pada pengujian otomatis.

## 10. Cara melaporkan bug atau kendala

Jika menemukan masalah, kirim laporan kepada pengembang dengan format berikut. Sertakan screenshot pesan error jika memungkinkan, tetapi pastikan screenshot tidak menampilkan data pribadi atau media peserta.

```text
LAPORAN UJI COBA YAMOTO DECEPTION LAB

1. Versi aplikasi:
2. Versi Windows (contoh: Windows 11 64-bit):
3. Spesifikasi perangkat (prosesor dan RAM):
4. Fitur yang sedang diuji:
5. Langkah sebelum masalah terjadi:
6. Hasil yang diharapkan:
7. Hasil yang sebenarnya:
8. Pesan error (jika ada):
9. Apakah masalah bisa diulangi?:
10. Screenshot (jika ada):
```

Untuk masalah pemrosesan media, tambahkan informasi berikut tanpa mengirimkan isi rekaman pribadi:
- Jenis file dan ekstensi.
- Ukuran file.
- Durasi video/audio.
- Resolusi gambar/video jika diketahui.
- Apakah file yang sama dapat dibuka di aplikasi lain.

Jangan mengirimkan file rekaman wajah atau suara orang lain kepada pengembang kecuali orang tersebut sudah memberi izin secara jelas.

## 11. Jika ingin menghapus aplikasi

1. Tutup YAMOTO DECEPTION LAB.
2. Buka **Windows Settings → Apps → Installed apps**.
3. Cari **YAMOTO DECEPTION LAB**.
4. Pilih menu aplikasi, lalu pilih **Uninstall**.
5. Ikuti proses sampai selesai.

**Perhatian:** uninstall aplikasi belum tentu menghapus database dan catatan penelitian yang tersimpan terpisah di profil pengguna Windows. Jika ingin menyimpan catatan, lakukan pencadangan terlebih dahulu. Jika ingin menghapus data, pastikan data tersebut memang sudah tidak diperlukan dan penghapusannya sesuai dengan persetujuan serta kebijakan retensi penelitian. Jangan menghapus folder sistem atau folder lain secara sembarangan.

## 12. Status fitur dan validasi

Fitur yang tersedia saat ini:
- Antarmuka desktop React/TypeScript dengan Tauri 2.
- Engine Python lokal dan database SQLite.
- Pembuatan serta pencatatan dataset dan eksperimen.
- Preview kamera tanpa perekaman.
- Ekstraksi geometri wajah dari satu gambar.
- Ekstraksi geometri wajah dari sampel frame video.
- Pengukuran sinyal audio WAV.

Belum tersedia atau belum tervalidasi:
- Model AI pendeteksi kebohongan.
- Skor kejujuran atau label benar/bohong.
- Pengenalan emosi, kepribadian, atau niat.
- Validasi ilmiah untuk menyimpulkan kebohongan.
- Pengujian end-to-end pada perangkat fisik Windows 11 x64.

Pengujian otomatis installer telah mencakup build pada runner Windows 64-bit, pemasangan diam-diam, pemeriksaan startup aplikasi, pemeriksaan kesehatan engine, uninstall, dan pembuatan checksum. Pengujian tersebut **bukan** pengganti pengujian langsung pada berbagai perangkat Windows milik pengguna.

## 13. Informasi untuk pengembang

Persyaratan pengembangan: Node.js 20+, Python 3.11+, Rust stable, dan prasyarat Tauri untuk Windows.

```powershell
npm install
python -m pip install -r engine/requirements.txt pytest
npm run dev
```

Build frontend: `npm run build`.

Jalankan pengujian engine: `python -m pytest tests -q`.

Lihat [BUILD-STATUS.md](BUILD-STATUS.md) untuk status implementasi dan pengujian.
