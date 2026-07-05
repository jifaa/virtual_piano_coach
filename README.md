# Virtual Piano Coach

Aplikasi Virtual Piano Coach adalah asisten latihan piano berbasis desktop yang dirancang untuk membantu Anda berlatih bermain piano dengan lebih interaktif. Aplikasi ini menggabungkan teknologi computer vision melalui MediaPipe untuk mendeteksi posisi dan postur tangan Anda, serta koneksi MIDI untuk mengenali nada yang sedang Anda mainkan secara real-time.

Dengan aplikasi ini, Anda bisa melihat hamparan (overlay) tuts piano secara virtual di atas tampilan kamera Anda. Aplikasi ini juga mampu memberikan umpan balik terkait postur tangan Anda saat bermain.

## Fitur Utama

- **Mode Latihan Fleksibel**: Anda bisa memilih untuk bermain bebas tanpa panduan (Free Play Mode) atau berlatih mengikuti lagu menggunakan file MIDI (Guided Practice Mode), di mana aplikasi akan menunggu Anda menekan nada yang tepat sebelum melanjutkan.
- **Pelacakan Tangan (Computer Vision)**: Aplikasi ini melacak pergerakan tangan dan jari Anda. Selain menampilkan overlay piano di layar, aplikasi juga akan melabeli jari mana yang digunakan dan memberikan umpan balik jika postur tangan Anda kurang tepat (misalnya terlalu kaku atau tertekuk).
- **Integrasi Keyboard MIDI**: Mendukung berbagai macam keyboard MIDI seperti Roland E-X10, Yamaha, atau Casio. Nada yang Anda tekan akan langsung terdeteksi di layar.
- **Antarmuka Pengguna Modern**: Dilengkapi dengan mode gelap yang nyaman di mata, navigasi sidebar yang simpel, dan menggunakan bahasa Indonesia agar mudah dipahami.

## Kebutuhan Perangkat

Untuk menggunakan aplikasi ini, Anda memerlukan beberapa perangkat keras berikut:
1. **Kamera Web (Webcam)**: Bisa menggunakan kamera bawaan laptop atau kamera eksternal, yang penting posisinya bisa menyorot area keyboard piano Anda dengan jelas.
2. **Keyboard MIDI**: Keyboard atau piano elektronik yang memiliki port USB MIDI.
3. **Kabel USB**: Digunakan untuk menyambungkan keyboard MIDI ke komputer Anda.
4. **Komputer atau Laptop**: Membutuhkan komputer yang cukup mampu untuk menjalankan pemrosesan kamera dan pelacakan tangan secara real-time.

## Cara Instalasi

Pastikan Anda sudah menginstal Python (disarankan versi 3.8 atau yang lebih baru) di komputer Anda.

1. Buka terminal atau command prompt, lalu arahkan ke folder proyek ini.
2. Instal semua pustaka yang dibutuhkan dengan menjalankan perintah berikut:
   `pip install -r requirements.txt`
3. Setelah instalasi selesai, jalankan aplikasi menggunakan perintah:
   `python main.py`

## Panduan Penggunaan Lengkap

Berikut adalah langkah-langkah untuk mulai menggunakan Virtual Piano Coach:

### 1. Persiapan Perangkat
Pertama, sambungkan keyboard MIDI Anda ke komputer menggunakan kabel USB dan nyalakan keyboard tersebut. Selanjutnya, posisikan kamera Anda sedemikian rupa sehingga seluruh bagian tuts keyboard piano dapat terlihat dengan jelas di layar. 

### 2. Pengaturan Awal (Setup)
Saat aplikasi terbuka, masuk ke menu Setup. Di sini, Anda perlu mengatur beberapa hal:
- Pilih perangkat kamera yang mengarah ke piano Anda.
- Pilih perangkat input MIDI yang sesuai dengan nama keyboard Anda.
- Tentukan ukuran keyboard yang Anda gunakan (misalnya 61 atau 88 tuts).
- Jika Anda ingin berlatih dengan lagu tertentu, Anda bisa memasukkan file MIDI panduannya di halaman ini.

### 3. Proses Kalibrasi
Agar overlay virtual piano bisa pas dengan bentuk keyboard asli Anda di kamera, Anda harus melakukan kalibrasi:
- Masuk ke menu Kalibrasi.
- Klik tombol untuk memulai pratinjau (preview) kamera.
- Anda akan diminta untuk mengklik empat sudut keyboard piano Anda pada layar secara berurutan: sudut kiri atas, sudut kanan atas, sudut kanan bawah, dan terakhir sudut kiri bawah.
- Setelah keempat titik tersebut pas, simpan kalibrasi Anda.

### 4. Mulai Berlatih
Sekarang Anda sudah siap untuk berlatih! 
- Masuk ke menu Practice dan tekan tombol untuk memulai latihan.
- Saat Anda menekan tuts pada keyboard asli, Anda akan melihat indikator visual pada layar kamera.
- Jika Anda menggunakan mode panduan (guided mode), aplikasi akan menampilkan nada apa yang harus ditekan dan akan menunggu Anda menekan tuts yang benar sebelum lagu dilanjutkan.

## Panduan Indikator Warna

Saat Anda berlatih, aplikasi menggunakan beberapa warna untuk membantu visualisasi:
- **Hijau**: Menandakan tuts sedang Anda tekan.
- **Merah**: Menandakan Anda menekan tuts yang salah (muncul pada mode panduan).
- **Biru (Isian)**: Menandakan target tuts yang harus ditekan oleh tangan kiri.
- **Kuning**: Menandakan target tuts yang harus ditekan oleh tangan kanan.
- **Garis Tepi Biru/Abu**: Menandakan tuts sedang tidak ditekan (idle).

## Tips Tambahan

Agar pengalaman berlatih Anda maksimal, pastikan ruangan tempat Anda bermain memiliki pencahayaan yang cukup terang dan merata. Kamera yang gelap akan kesulitan melacak pergerakan tangan Anda. Jangan lupa untuk menempatkan posisi kamera agar seluruh tuts terlihat tanpa terpotong. 

Apabila Anda menggeser posisi kamera atau piano, Anda wajib melakukan kalibrasi ulang agar hamparan visual piano kembali presisi. Saat bermain, pastikan juga tangan atau lengan baju Anda tidak terlalu menutupi area tuts sehingga kamera tetap bisa melihat tuts dengan jelas.

## Penyelesaian Masalah

Jika Anda mengalami kendala saat menggunakan aplikasi, coba beberapa langkah berikut:
- **Kamera tidak muncul**: Pastikan kamera tidak sedang digunakan oleh aplikasi lain (seperti Zoom atau Google Meet). Coba cabut dan colok kembali kamera Anda, lalu muat ulang aplikasi.
- **Keyboard MIDI tidak terdeteksi**: Periksa kembali sambungan kabel USB Anda. Pastikan keyboard sudah dalam keadaan menyala sebelum aplikasi dibuka. Jika masih tidak terbaca, cobalah pindah ke port USB yang berbeda.
- **Hamparan piano (overlay) miring atau tidak pas**: Ini biasanya terjadi karena kalibrasi kurang akurat. Silakan kembali ke menu kalibrasi dan ulangi proses klik pada keempat sudut keyboard dengan lebih teliti.
- **Tangan tidak terdeteksi oleh sistem**: Pastikan pencahayaan cukup terang. Coba angkat tangan Anda sedikit di atas keyboard agar terlihat utuh oleh kamera, dan hindari menggunakan lengan baju panjang yang terlalu longgar menutupi punggung tangan.
