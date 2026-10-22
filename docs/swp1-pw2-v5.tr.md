# SWP1-PW2-V5 / TYWE3S: doğrulanmış seri dönüşüm

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Bir SWP1-PW2-V5 örneği, normal Tuya-Convert işlemi PSK kimliği `02` ile başarısız olduktan sonra 2026-10-18 tarihinde dönüştürüldü. Kablolu sorgulama ESP8266EX, 26 MHz kristal ve 2 MiB flash belirledi. Doğrulanmış fabrika yedeği, son firmware yazılmadan önce GPIO eşlemesini sağladı. Sahibi daha sonra kitaplık prizi olarak normal çalışmasını doğruladı.

Bu kanıtlar yalnızca bu örneğe aittir; benzer kasalı her ürüne genellenemez. Donanım karşılaştırmasında kullanılan eski yanmış anahtar farklı bir cihazdı; onun Home Assistant kimliği ve LocalTuya yapılandırması korundu.

## Doğrulanan donanım

- Röle: **GPIO13, yüksek etkin**, geri yükleme `ALWAYS_OFF`.
- Fiziksel düğme: **GPIO3 / RXD0, düşük etkin**, pull-up ve 30 ms sıçrama giderme.
- Röle göstergesi: **GPIO14, düşük etkin**, komut verilen röle durumunu izler.
- Bağlantı göstergesi: **GPIO0, düşük etkin**.
- Seri günlük: kapalı; giriş RXD0'ı paylaştığından düğme testinden önce programlayıcının UART kablolarını çıkarın.

Fabrika uygulamasının donanım JSON'u bu atamaları belirledi; sonraki düğme, röle ve gösterge gözlemleri bunlarla uyumluydu. GPIO çıkış taraması veya tarafsız tanılama firmware'i gerekmedi. Profil elektriksel ölçüm yapılandırmaz. LED veya API durumu röle kontaklarından geri bildirim değildir.

## Düşük gerilim bağlantıları

**Kapağı açmadan veya herhangi bir bağlantı yapmadan önce cihazı şebekeden tamamen ayırın. Programlama boyunca şebekeden ayrılmış halde tutun.** Regüle 3,3 V kaynak ve doğrulanmış 3,3 V UART mantığı kullanın. Seviye dönüştürücü sinyalleri uyarlar; cihaza regüle güç sağlamaz.

![İşlevsel seri bağlantılar: harici 3,3 V güç, 5 V UART adaptörü, seviye dönüştürücü ve TYWE3S](images/swp1-serial-wiring.svg)

Çizim elektriksel bağlantıları gösterir, **fiziksel lehim pedi konumlarını değil**. Modül pinlerini [Tuya TYWE3S veri sayfasıyla](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv) belirleyin ve yönünü kartla karşılaştırın. Taşıyıcı kartın test pedinin işlevini konumundan çıkarmayın. Belgelenmiş nominal besleme 3,3 V'tur.

Burada kullanılan 5 V mantıklı adaptör için:

1. Adaptör **5V → dönüştürücü HV referansı**.
2. Harici regüle **3.3V → modül VCC ve dönüştürücü LV**.
3. Adaptör GND, dönüştürücü GND, kaynak eksi ucu ve modül GND ortak toprağa bağlanır.
4. Adaptör **TX → HV1**, karşılık gelen **LV1 → modül RXD0**.
5. Modül **TXD0 → LV2**, karşılık gelen **HV2 → adaptör RX**.
6. Adaptörün 3V3 çıkışını bağlamayın. İki güç çıkışını asla paralellemeyin.

UART hızına ve yönüne uygun dönüştürücü kullanın. Bu zincir kablolar düzeltildikten sonra 115200 baud ile çalıştı; bu, her ucuz HV/LV kartını onaylamaz. Gerçek 3,3 V UART adaptörü, çıkış seviyesi doğrulandıktan sonra dönüştürücüsüz kullanılabilir.

Adaptör yüksüzken 3,3 V ölçülüyordu, ancak bağlı cihaz yalnızca **1,9 V** alıyordu. TX ayrıca **5,1 V** sürüyordu. Bunlar ayrı sorunlardır: harici kaynak VCC'yi, dönüştürücü UART seviyelerini düzeltti. Yük altındaki modülde VCC'yi ve aynı toprağa göre sinyalleri ölçün. [ESPHome fiziksel bağlantı kılavuzuna](https://esphome.io/guides/physical_device_connection/) bakın.

## İndirme modu, yedek ve firmware

Güç kapalıyken **GPIO0'ı GND'ye bağlayın**. Düşük gerilimi geri verip **RST'yi kısa süre GND'ye bağlayın, ardından RST'yi bırakın**. EN yüksek kalmalı; RST'yi düşük tutmayın. GPIO0 yazma sırasında toprakta kalabilir, ancak normal açılıştan önce köprüyü çıkarın. Okunabilir ROM mesajı `boot mode:(1,0)` indirme modunu doğruladı. [Espressif açılış modu belgelerine](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html) bakın.

Seri portu yalnızca bir program kullanabilir. Esptool'dan önce Miniterm'i kapatın. TX/RX'in doğru çaprazlanması son iletişim hatasını giderdi; yanan LED çalışan seri bağlantı kanıtı değildi.

Yazmadan önce operatör fabrika flash'ının **2,097,152 baytının tamamını** okudu ve esptool ile yedeği cihazla karşılaştırarak doğruladı. Yedekleri, ham seri günlüklerini, derlenmiş görüntüleri ve kimlik bilgilerini herkese açık Git dışında tutun: fabrika dökümü kurulum sırları içerebilir. [Esptool komut başvurusu](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html) tanımlama, `read-flash`, `verify-flash` ve `write-flash` işlemlerini açıklar. Okuma boyutunu kasa adına değil, gerçek flash tespitine göre seçin.

[Bağımsız profili](../examples/swp1-pw2-v5.yaml) yeni özel bir dizinde derleyin. Komutları depo kökünden çalıştırın; yalnızca bu profili kopyalayın, genel tabanı veya XS-SSA01 paketini değil:

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

Yardımcı Wi-Fi kimlik bilgilerini sorar, ayrı anahtarlar üretir ve mevcut sırların üzerine yazmayı reddeder. Komutlar flash yazmadan derler. [Şifreli kurulum notlarına](security-profile.md) bakın. Bu örnek **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz** kullanıyordu. Kurulan görüntü **429,600 bayttı**, `0x0` adresine 115200 baud ile yazıldı; esptool yazılan hash'i doğruladı. Yeniden derlemelerin boyutu değişebilir: bu sayı gözlemdir, kurulum şartı değildir.

## Normal açılış ve kabul

Gücü kapatın, GPIO0–GND ve iki UART sinyal kablosunu çıkarın; yalnızca harici 3,3 V'u geri verin. Şifreli yerel API bağlandı; ON/OFF çalıştı ve ON durumundan yazılımsal yeniden başlatma OFF durumunu geri getirdi. Sahibi röle tıklaması ve eşlik eden göstergeyle iki düğme basışını doğruladı.

Ardından tüm geçici kablolar ve harici güç çıkarıldı; normal kurulumdan önce kasa kapatıldı. Sahibi kurulu prizin çalıştığını doğruladı. **ON durumundan kontrollü şebeke kesme/açma testi, kontak gerilimi ölçümleri veya açılış geçicilerinin ölçümü yapılmadı.** Tek başına tezgâhtaki tıklamalar yük anahtarlamasını kanıtlamazdı.

Home Assistant'a bir röle ile bağlantı, sinyal, sürüm ve yeniden başlatma tanılamaları geldi. Kurulu işlev HA'da yeniden flash yazmadan yeniden adlandırıldı; firmware'in ilk ana bilgisayar adı geçerlidir. Tam özel kaynaklar hem HA ESPHome dizinine hem ESPHome Dashboard'a kaydedildi. Röle ikinci dashboard sayfasının Living Room bölümüne bir kez eklendi. Gelecekteki depo dağıtımları bu kayıt kimliklerini korumalı veya açıkça taşımalıdır.

## Bir adım başarısız olursa

- **Seri yanıt yok:** yüklü VCC, ortak toprak, adaptör TX → modül RX, modül TX → adaptör RX ve portu başka terminalin kullanmadığını kontrol edin.
- **Okunamayan baytlar:** ROM günlüğü için yeni reseti 74880 baud ile yakalayın; gerçek aktarımda seçilen esptool hızını kullanın.
- **Hâlâ indirme modunda:** GPIO0–toprak köprüsünü çıkarıp yeniden başlatın.
- **Reset sırasında durum LED'i yanıyor:** GPIO0 bu LED'i de sürer; topraklı açılış köprüsü bunu açıklayabilir. Reset testi olarak kullanmayın.
- **Programlayıcı bağlıyken düğme çalışmıyor:** UART'ı ayırın; GPIO3 ortaktır.
- **API çalışıyor, yük çalışmıyor:** bildirilen röle durumu kontakları, bobin gücünü veya şebeke kablolarını teşhis etmez. Şebekeye bağlı açık kart üzerinde ölçüm yapmayın.
