# SWP1-PW2-V5 / TYWE3S: konversi serial yang terverifikasi

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Satu unit SWP1-PW2-V5 dikonversi pada 2026-10-18 setelah Tuya-Convert biasa gagal dengan identitas PSK `02`. Pemeriksaan berkabel menemukan ESP8266EX, kristal 26 MHz, dan flash 2 MiB. Cadangan pabrik yang terverifikasi menyediakan pemetaan GPIO sebelum firmware final ditulis. Pemilik kemudian mengonfirmasi operasi normal sebagai stopkontak rak buku.

Bukti ini berlaku untuk unit tersebut, bukan setiap produk dengan casing serupa. Sakelar lama yang terbakar, yang dipakai sebagai pembanding perangkat keras, adalah perangkat berbeda; identitas Home Assistant dan konfigurasi LocalTuya-nya dipertahankan.

## Perangkat keras terkonfirmasi

- Relai: **GPIO13, aktif tinggi**, pemulihan `ALWAYS_OFF`.
- Tombol fisik: **GPIO3 / RXD0, aktif rendah**, pull-up dan debounce 30 ms.
- Indikator relai: **GPIO14, aktif rendah**, mengikuti status relai yang diperintahkan.
- Indikator koneksi: **GPIO0, aktif rendah**.
- Log serial: dinonaktifkan; lepaskan kabel UART programmer sebelum menguji tombol karena masukan berbagi RXD0.

JSON perangkat keras aplikasi pabrik mengidentifikasi penetapan ini; pengamatan tombol, relai, dan indikator sesudahnya cocok. Pemindaian keluaran GPIO maupun firmware diagnostik netral tidak diperlukan. Profil tidak mengatur pengukuran listrik. LED atau status API bukan umpan balik kontak relai.

## Pengawatan tegangan rendah

**Putuskan sepenuhnya dari listrik PLN sebelum membuka atau menyambungkan apa pun. Biarkan tetap terputus selama seluruh pemrograman.** Gunakan catu 3,3 V teregulasi dan logika UART 3,3 V yang sudah diverifikasi. Pengubah level menyesuaikan sinyal; bukan penyedia daya teregulasi untuk perangkat.

![Pengawatan serial fungsional: catu eksternal 3,3 V, adaptor UART 5 V, pengubah level, dan TYWE3S](images/swp1-serial-wiring.svg)

Gambar menunjukkan sambungan listrik, **bukan posisi fisik pad solder**. Identifikasi pin dengan [datasheet Tuya TYWE3S](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv) dan cocokkan orientasi gambar dengan papan. Jangan menebak fungsi pad uji papan pembawa dari posisinya. Catu nominal terdokumentasi adalah 3,3 V.

Untuk adaptor berlogika 5 V yang digunakan di sini:

1. **5V adaptor → referensi HV** pengubah level.
2. Catu eksternal teregulasi **3.3V → VCC modul dan LV pengubah**.
3. GND adaptor, GND pengubah, negatif catu, dan GND modul berbagi ground yang sama.
4. **TX adaptor → HV1**, pasangan **LV1 → RXD0 modul**.
5. **TXD0 modul → LV2**, pasangan **HV2 → RX adaptor**.
6. Biarkan keluaran 3V3 adaptor tidak tersambung. Jangan pernah memparalelkan dua keluaran catu daya.

Gunakan pengubah yang sesuai dengan kecepatan dan arah UART. Rangkaian ini bekerja pada 115200 baud setelah pengawatan dibetulkan; hal itu tidak menjamin setiap papan HV/LV murah. Adaptor UART 3,3 V asli dapat digunakan tanpa pengubah setelah level keluarannya diverifikasi.

Adaptor terbaca 3,3 V tanpa beban, tetapi perangkat yang tersambung hanya mendapat **1,9 V**. TX juga menghasilkan **5,1 V**. Ini masalah terpisah: catu eksternal memperbaiki VCC, pengubah menyesuaikan level UART. Ukur VCC pada modul berbeban dan sinyal terhadap ground yang sama. Lihat [panduan sambungan fisik ESPHome](https://esphome.io/guides/physical_device_connection/).

## Mode unduh, cadangan, dan firmware

Saat daya mati, tahan **GPIO0 terhubung ke GND**. Pulihkan tegangan rendah, lalu **hubungkan RST sebentar ke GND dan lepaskan RST**. Pertahankan EN tinggi; jangan menahan RST rendah. GPIO0 boleh tetap ke ground saat penulisan, tetapi lepaskan jumper sebelum boot normal. Pesan ROM terbaca `boot mode:(1,0)` mengonfirmasi mode unduh. Lihat [dokumentasi mode boot Espressif](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html).

Hanya satu program boleh menggunakan port serial. Tutup Miniterm sebelum esptool. Menyilangkan TX/RX dengan benar mengatasi kegagalan komunikasi terakhir; LED menyala tidak membuktikan koneksi serial bekerja.

Sebelum menulis, operator membaca **seluruh 2,097,152 byte** flash pabrik dan memverifikasi cadangan terhadap perangkat dengan esptool. Simpan cadangan, log serial mentah, image hasil build, dan kredensial di luar Git publik: dump pabrik dapat berisi rahasia provisioning. [Referensi perintah esptool](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html) menjelaskan identifikasi, `read-flash`, `verify-flash`, dan `write-flash`. Pilih ukuran baca berdasarkan hasil deteksi flash sebenarnya, bukan nama casing.

Bangun [profil mandiri](../examples/swp1-pw2-v5.yaml) dalam direktori privat baru. Jalankan perintah berikut dari akar repositori; salin hanya profil ini, bukan basis umum atau paket XS-SSA01:

```sh
SWP_REPO="$PWD"
SWP_BUILD_DIR="$HOME/.local/share/esphome/swp1-private"
umask 077
mkdir -p "$SWP_BUILD_DIR"
cp "$SWP_REPO/examples/swp1-pw2-v5.yaml" "$SWP_BUILD_DIR/"
python3.12 -m venv "$SWP_BUILD_DIR/.venv"
"$SWP_BUILD_DIR/.venv/bin/python" -m pip install 'esphome==2026.9.1'
"$SWP_BUILD_DIR/.venv/bin/python" "$SWP_REPO/scripts/create-secrets.py" \
  "$SWP_BUILD_DIR/secrets.yaml"
"$SWP_BUILD_DIR/.venv/bin/python" -m esphome compile \
  "$SWP_BUILD_DIR/swp1-pw2-v5.yaml"
```

Program pembantu meminta kredensial Wi-Fi, menghasilkan kunci berbeda, dan menolak menimpa rahasia yang sudah ada. Perintah ini mengompilasi tanpa menulis flash. Lihat [catatan provisioning terenkripsi](security-profile.md). Unit ini memakai **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz**. Image terpasang berukuran **429,600 byte**, ditulis ke `0x0` pada 115200 baud; esptool mengonfirmasi hash hasil penulisan. Ukuran build lain dapat berbeda: jumlah byte ini pengamatan, bukan syarat pemasangan.

## Boot normal dan penerimaan

Matikan daya, lepaskan GPIO0–GND serta kedua kabel sinyal UART, lalu pulihkan hanya 3,3 V eksternal. API native terenkripsi tersambung; ON/OFF bekerja dan restart perangkat lunak dari ON memulihkan OFF. Pemilik mengonfirmasi dua penekanan tombol dengan klik relai dan indikator yang mengikuti.

Setelah itu semua kabel sementara dan catu eksternal dilepas, lalu casing ditutup sebelum pemasangan normal. Pemilik mengonfirmasi stopkontak terpasang bekerja. **Uji pemutusan/pemulihan listrik PLN terkendali dari ON, pengukuran tegangan kontak, dan pengukuran transien boot tidak dilakukan.** Klik di meja saja tidak membuktikan pengalihan beban.

Home Assistant menerima satu relai serta diagnostik koneksi, sinyal, versi, dan restart. Peran terpasang diganti namanya di HA tanpa flash ulang; hostname firmware awal tetap valid. Sumber privat lengkap disimpan di direktori ESPHome HA dan ESPHome Dashboard. Relai ditambahkan sekali ke bagian Living Room halaman dashboard kedua. Deployment repositori berikutnya harus mempertahankan identitas registri itu atau memigrasikannya secara eksplisit.

## Jika suatu langkah gagal

- **Tidak ada respons serial:** periksa VCC berbeban, ground bersama, TX adaptor → RX modul, TX modul → RX adaptor, serta tidak ada terminal lain yang memakai port.
- **Byte tidak terbaca:** tangkap reset baru pada 74880 baud untuk log ROM; gunakan baud esptool terpilih untuk transfer sebenarnya.
- **Masih mode unduh:** lepaskan jumper GPIO0–ground dan restart.
- **LED status menyala saat reset:** GPIO0 juga menggerakkan LED itu; jumper boot ke ground dapat menjelaskannya. Jangan jadikan ini tes reset.
- **Tombol gagal saat programmer terhubung:** lepaskan UART; GPIO3 dipakai bersama.
- **API bekerja tetapi beban tidak:** status relai yang dilaporkan tidak mendiagnosis kontak, catu koil, atau kabel PLN. Jangan menyentuh papan terbuka bertegangan PLN dengan probe.
