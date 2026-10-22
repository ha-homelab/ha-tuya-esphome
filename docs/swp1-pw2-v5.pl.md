# SWP1-PW2-V5 / TYWE3S: zweryfikowana konwersja szeregowa

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Jeden egzemplarz SWP1-PW2-V5 przekonwertowano 2026-10-18 po nieudanej standardowej próbie Tuya-Convert z tożsamością PSK `02`. Odczyt przewodowy wykrył ESP8266EX, kwarc 26 MHz i pamięć flash 2 MiB. Zweryfikowana kopia fabryczna dostarczyła mapę GPIO przed końcowym zapisem. Właściciel potwierdził później normalną pracę jako gniazdko przy regale.

Dowody dotyczą tego egzemplarza, nie każdego produktu o podobnej obudowie. Stary przepalony przełącznik użyty do porównania sprzętu był innym urządzeniem; jego tożsamość Home Assistant i konfigurację LocalTuya zachowano.

## Potwierdzony sprzęt

- Przekaźnik: **GPIO13, aktywny stan wysoki**, przywracanie `ALWAYS_OFF`.
- Przycisk fizyczny: **GPIO3 / RXD0, aktywny stan niski**, pull-up i eliminacja drgań 30 ms.
- Wskaźnik przekaźnika: **GPIO14, aktywny stan niski**, odpowiada zadanemu stanowi przekaźnika.
- Wskaźnik połączenia: **GPIO0, aktywny stan niski**.
- Logowanie szeregowe: wyłączone; przed testem przycisku odłącz przewody UART programatora, ponieważ wejście współdzieli RXD0.

Sprzętowy JSON aplikacji fabrycznej określił te przypisania; późniejsze obserwacje przycisku, przekaźnika i wskaźników je potwierdziły. Skanowanie wyjść GPIO ani neutralny firmware diagnostyczny nie były potrzebne. Profil nie konfiguruje pomiarów elektrycznych. LED lub stan API nie są informacją zwrotną ze styków przekaźnika.

## Połączenia niskonapięciowe

**Całkowicie odłącz urządzenie od sieci elektrycznej przed otwarciem lub podłączaniem czegokolwiek. Musi pozostać odłączone przez cały czas programowania.** Użyj stabilizowanego zasilania 3,3 V i sprawdzonej logiki UART 3,3 V. Konwerter poziomów dostosowuje sygnały; nie zapewnia stabilizowanego zasilania urządzenia.

![Funkcjonalne połączenia szeregowe: zewnętrzne zasilanie 3,3 V, adapter UART 5 V, konwerter poziomów i TYWE3S](images/swp1-serial-wiring.svg)

Rysunek pokazuje połączenia elektryczne, **nie fizyczne położenie pól lutowniczych**. Zidentyfikuj piny według [dokumentacji Tuya TYWE3S](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv), porównując orientację z płytką. Nie wnioskuj o funkcji punktu testowego na płytce bazowej z jego położenia. Udokumentowane nominalne zasilanie wynosi 3,3 V.

Dla użytego tu adaptera z logiką 5 V:

1. **5V adaptera → odniesienie HV** konwertera.
2. Zewnętrzne stabilizowane **3.3V → VCC modułu i LV konwertera**.
3. GND adaptera, GND konwertera, minus zasilacza i GND modułu mają wspólną masę.
4. **TX adaptera → HV1**, odpowiadające **LV1 → RXD0 modułu**.
5. **TXD0 modułu → LV2**, odpowiadające **HV2 → RX adaptera**.
6. Pozostaw wyjście 3V3 adaptera odłączone. Nigdy nie łącz równolegle dwóch wyjść zasilania.

Konwerter musi obsługiwać prędkość i kierunek UART. Ten zestaw działał przy 115200 baud po poprawieniu przewodów; nie oznacza to kwalifikacji każdej taniej płytki HV/LV. Prawdziwy adapter UART 3,3 V może pracować bez konwertera po sprawdzeniu poziomu wyjściowego.

Adapter bez obciążenia dawał 3,3 V, ale podłączone urządzenie otrzymywało tylko **1,9 V**. Ponadto TX miał **5,1 V**. To odrębne problemy: zewnętrzny zasilacz naprawił VCC, konwerter dostosował poziomy UART. Mierz VCC na obciążonym module, a sygnały względem tej samej masy. Zobacz [przewodnik ESPHome po połączeniach fizycznych](https://esphome.io/guides/physical_device_connection/).

## Tryb pobierania, kopia zapasowa i firmware

Przy wyłączonym zasilaniu połącz **GPIO0 z GND**. Przywróć niskie napięcie, następnie **na chwilę połącz RST z GND i zwolnij RST**. Utrzymuj EN w stanie wysokim; nie trzymaj RST w niskim. GPIO0 może być uziemiony podczas zapisu, lecz usuń mostek przed normalnym startem. Czytelny komunikat ROM `boot mode:(1,0)` potwierdził tryb pobierania. Zobacz [dokumentację trybów startowych Espressif](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html).

Port szeregowy może zajmować tylko jeden program. Zamknij Miniterm przed esptool. Prawidłowe skrzyżowanie TX/RX rozwiązało ostatni problem komunikacyjny; świecąca LED nie dowodziła działającego połączenia szeregowego.

Przed zapisem operator odczytał **wszystkie 2,097,152 bajty** fabrycznej flash i zweryfikował kopię z urządzeniem przez esptool. Kopie, surowe logi szeregowe, zbudowane obrazy i dane uwierzytelniające przechowuj poza publicznym Git: fabryczny zrzut może zawierać tajne dane provisioningu. [Dokumentacja poleceń esptool](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html) opisuje identyfikację, `read-flash`, `verify-flash` i `write-flash`. Rozmiar odczytu wybierz na podstawie rzeczywistej identyfikacji flash, nie nazwy obudowy.

Zbuduj [samodzielny profil](../examples/swp1-pw2-v5.yaml) w nowym prywatnym katalogu. Polecenia uruchom z katalogu głównego repozytorium; kopiuj tylko ten profil, nie ogólną bazę ani pakiet XS-SSA01:

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

Narzędzie poprosi o dane Wi-Fi, wygeneruje odrębne klucze i odmówi nadpisania istniejących sekretów. Polecenia kompilują bez zapisu flash. Zobacz [uwagi o szyfrowanym provisioningu](security-profile.md). Ten egzemplarz używał **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz**. Zainstalowany obraz miał **429,600 bajtów**, zapisanych pod `0x0` przy 115200 baud; esptool potwierdził hash zapisu. Kolejne kompilacje mogą mieć inny rozmiar: liczba bajtów jest obserwacją, nie wymaganiem instalacyjnym.

## Normalny start i odbiór

Wyłącz zasilanie, usuń GPIO0–GND i oba przewody sygnałowe UART, następnie przywróć tylko zewnętrzne 3,3 V. Szyfrowane natywne API połączyło się, ON/OFF działało, a programowy restart z ON przywracał OFF. Właściciel potwierdził dwa naciśnięcia przycisku z kliknięciami przekaźnika i odpowiednim wskaźnikiem.

Następnie usunięto wszystkie tymczasowe przewody oraz zewnętrzne zasilanie i zamknięto obudowę przed normalną instalacją. Właściciel potwierdził działanie zainstalowanego gniazdka. **Nie wykonano kontrolowanego cyklu odłączenia/przywrócenia sieci ze stanu ON, pomiarów napięcia styków ani stanów przejściowych przy starcie.** Same kliknięcia na stole nie dowodziłyby przełączania obciążenia.

Home Assistant otrzymał jeden przekaźnik i diagnostykę połączenia, sygnału, wersji i restartu. Rolę instalacji zmieniono nazwą w HA bez ponownego flashowania; oryginalna nazwa hosta firmware pozostaje ważna. Pełne prywatne źródła zapisano w katalogu ESPHome w HA i w ESPHome Dashboard. Przekaźnik dodano raz do sekcji Living Room drugiej strony pulpitu. Przyszłe wdrożenia repozytorium muszą zachować te tożsamości rejestru albo jawnie je zmigrować.

## Jeśli krok się nie powiedzie

- **Brak odpowiedzi szeregowej:** sprawdź VCC pod obciążeniem, wspólną masę, TX adaptera → RX modułu, TX modułu → RX adaptera i czy inny terminal nie zajmuje portu.
- **Nieczytelne bajty:** przechwyć świeży reset przy 74880 baud dla logu ROM; do właściwego transferu użyj wybranej prędkości esptool.
- **Nadal tryb pobierania:** usuń mostek GPIO0–masa i uruchom ponownie.
- **LED stanu świeci podczas resetu:** GPIO0 steruje również tą LED; uziemiony mostek startowy może to wyjaśniać. Nie traktuj tego jako testu resetu.
- **Przycisk nie działa z programatorem:** odłącz UART; GPIO3 jest współdzielony.
- **API działa, obciążenie nie:** zgłaszany stan nie diagnozuje styków, zasilania cewki ani przewodów sieciowych. Nie wykonuj pomiarów na odsłoniętej płytce pod napięciem sieciowym.
