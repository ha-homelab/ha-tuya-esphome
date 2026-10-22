# SWP1-PW2-V5 / TYWE3S: ověřený převod přes sériové rozhraní

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Jeden kus SWP1-PW2-V5 byl převeden 2026-10-18 poté, co běžný Tuya-Convert selhal s identitou PSK `02`. Kabelová sonda zjistila ESP8266EX, krystal 26 MHz a flash 2 MiB. Ověřená záloha továrního firmwaru poskytla mapu GPIO před konečným zápisem. Majitel následně potvrdil normální provoz zásuvky u knihovny.

Důkazy platí pro tento kus, nikoli každý výrobek s podobným krytem. Starý spálený spínač použitý pro porovnání hardwaru byl jiný přístroj; jeho identita Home Assistant a konfigurace LocalTuya zůstaly zachovány.

## Ověřený hardware

- Relé: **GPIO13, aktivní v H**, obnova `ALWAYS_OFF`.
- Fyzické tlačítko: **GPIO3 / RXD0, aktivní v L**, pull-up a potlačení zákmitů 30 ms.
- Indikátor relé: **GPIO14, aktivní v L**, sleduje požadovaný stav relé.
- Indikátor připojení: **GPIO0, aktivní v L**.
- Sériové logování: vypnuto; před zkouškou tlačítka odpojte UART programátoru, protože vstup sdílí RXD0.

Hardwarový JSON tovární aplikace určil tyto funkce; následné pozorování tlačítka, relé a indikátorů je potvrdilo. Nebylo třeba postupně zkoušet výstupy GPIO ani nahrávat neutrální diagnostický firmware. Profil nenastavuje elektrická měření. LED ani stav API nejsou zpětnou vazbou kontaktů relé.

## Nízkonapěťové zapojení

**Před otevřením nebo jakýmkoli připojováním zařízení úplně odpojte od sítě. Po celou dobu programování musí zůstat odpojené.** Použijte stabilizované napájení 3,3 V a ověřenou logiku UART 3,3 V. Převodník úrovní upravuje signály; neposkytuje stabilizované napájení.

![Funkční sériové zapojení: externí napájení 3,3 V, adaptér UART 5 V, převodník úrovní a TYWE3S](images/swp1-serial-wiring.svg)

Obrázek znázorňuje elektrické spoje, **nikoli fyzické polohy plošek**. Piny určete podle [datasheetu Tuya TYWE3S](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv) a porovnejte orientaci s deskou. Funkci testovací plošky nosné desky neodvozujte z její polohy. Dokumentované jmenovité napájení je 3,3 V.

Pro zde použitý adaptér s logikou 5 V:

1. **5V adaptéru → reference HV** převodníku.
2. Externí stabilizované **3.3V → VCC modulu a LV převodníku**.
3. GND adaptéru, GND převodníku, záporný pól zdroje a GND modulu mají společnou zem.
4. **TX adaptéru → HV1**, odpovídající **LV1 → RXD0 modulu**.
5. **TXD0 modulu → LV2**, odpovídající **HV2 → RX adaptéru**.
6. Výstup 3V3 adaptéru nechte odpojený. Nikdy nespojujte dva napájecí výstupy paralelně.

Převodník musí podporovat rychlost a směr UART. Tento řetězec po opravě zapojení fungoval při 115200 baud; tím nejsou ověřeny všechny levné moduly HV/LV. U skutečného adaptéru UART 3,3 V lze po ověření výstupní úrovně převodník vynechat.

Adaptér bez zatížení ukazoval 3,3 V, ale připojené zařízení dostávalo jen **1,9 V**. Na TX navíc bylo **5,1 V**. Jde o dva odlišné problémy: externí zdroj vyřešil VCC, převodník úrovně UART. Měřte VCC na zatíženém modulu a signály vůči stejné zemi. Viz [návod ESPHome k fyzickému připojení](https://esphome.io/guides/physical_device_connection/).

## Režim download, záloha a firmware

Při vypnutém napájení spojte **GPIO0 s GND**. Obnovte nízké napětí, poté **krátce spojte RST s GND a RST uvolněte**. EN držte v H; RST nedržte v L. GPIO0 může během zápisu zůstat uzemněný, ale před normálním startem propojku odstraňte. Čitelná zpráva ROM `boot mode:(1,0)` zde potvrdila režim download. Viz [dokumentace zaváděcích režimů Espressif](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html).

Sériový port smí používat pouze jeden program. Před esptool ukončete Miniterm. Správné překřížení TX/RX vyřešilo poslední chybu komunikace; rozsvícená LED nebyla důkazem funkčního sériového spojení.

Před zápisem obsluha přečetla **všech 2,097,152 bajtů** tovární flash a pomocí esptool ověřila zálohu proti zařízení. Zálohy, surové sériové logy, sestavené obrazy a přihlašovací údaje uchovávejte mimo veřejný Git: tovární dump může obsahovat tajné údaje pro zřízení zařízení. [Přehled příkazů esptool](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html) popisuje identifikaci, `read-flash`, `verify-flash` a `write-flash`. Velikost čtení určete podle skutečně zjištěné flash, nikoli označení krytu.

Sestavte [samostatný profil](../examples/swp1-pw2-v5.yaml) v novém soukromém adresáři. Příkazy spusťte z kořene repozitáře; kopírujte pouze tento profil, nikoli obecný základ nebo balíček XS-SSA01:

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

Pomocný program si vyžádá přihlašovací údaje Wi-Fi, vygeneruje odlišné klíče a odmítne přepsat existující tajné údaje. Příkazy pouze kompilují, nezapisují flash. Viz [poznámky k šifrovanému zřízení](security-profile.md). Tento kus používal **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz**. Instalovaný obraz měl **429,600 bajtů**, zapsaných na `0x0` při 115200 baud; esptool potvrdil hash zápisu. Další sestavení mohou mít jinou velikost: počet bajtů je pozorování, nikoli podmínka instalace.

## Normální start a převzetí

Vypněte napájení, odstraňte spoj GPIO0–GND a oba signální vodiče UART, poté obnovte pouze externí 3,3 V. Šifrované nativní API se připojilo, příkazy ON/OFF fungovaly a softwarový restart ze stavu ON obnovil OFF. Majitel potvrdil dva stisky tlačítka s cvaknutím relé a odpovídajícím indikátorem.

Poté byly odstraněny dočasné vodiče i externí napájení a před běžnou instalací uzavřen kryt. Majitel potvrdil provoz instalované zásuvky. **Nebyl proveden řízený síťový vypínací/zapínací test ze stavu ON, měření napětí kontaktů ani přechodových jevů při startu.** Samotné cvaknutí na stole by spínání zátěže nedokazovalo.

Home Assistant získal jedno relé a diagnostiku připojení, signálu, verze a restartu. Instalovaná role byla přejmenována v HA bez nového flashování; původní hostname firmwaru zůstává platný. Úplné soukromé zdroje byly uloženy do adresáře ESPHome v HA i ESPHome Dashboard. Relé bylo jednou přidáno do oddílu Living Room na druhé stránce dashboardu. Budoucí nasazení repozitáře musí zachovat tyto identity registru nebo je výslovně migrovat.

## Pokud krok selže

- **Žádná sériová odpověď:** ověřte zatížené VCC, společnou zem, TX adaptéru → RX modulu, TX modulu → RX adaptéru a nepřítomnost jiného terminálu na portu.
- **Nečitelné bajty:** zachyťte nový reset při 74880 baud pro log ROM; pro vlastní přenos použijte zvolenou rychlost esptool.
- **Stále režim download:** odstraňte propojku GPIO0–zem a restartujte.
- **Stavová LED svítí při resetu:** GPIO0 řídí i tuto LED; může to vysvětlovat uzemněná zaváděcí propojka. Není to test resetu.
- **Tlačítko s programátorem nefunguje:** odpojte UART; GPIO3 je sdílený.
- **API funguje, zátěž ne:** hlášený stav relé nediagnostikuje kontakty, napájení cívky ani síťové zapojení. Neměřte na odkryté desce pod síťovým napětím.
