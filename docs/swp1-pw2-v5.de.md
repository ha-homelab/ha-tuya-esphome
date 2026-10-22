# SWP1-PW2-V5 / TYWE3S: verifizierte Umrüstung über die serielle Schnittstelle

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Ein SWP1-PW2-V5-Exemplar wurde am 2026-10-18 umgerüstet, nachdem das übliche Tuya-Convert mit PSK-Identität `02` gescheitert war. Eine kabelgebundene Untersuchung identifizierte einen ESP8266EX, einen 26-MHz-Quarz und 2 MiB Flash. Ein verifiziertes Werksbackup lieferte die GPIO-Belegung vor dem Schreiben der endgültigen Firmware. Der Eigentümer bestätigte anschließend den normalen Betrieb als Steckdose am Bücherregal.

Diese Nachweise gelten für dieses Exemplar, nicht für jedes Produkt mit ähnlichem Gehäuse. Der alte, durchgebrannte Schalter, der als Hardwarevergleich diente, war ein anderes Gerät: Seine Home-Assistant-Identität und LocalTuya-Konfiguration blieben erhalten.

## Bestätigte Hardware

- Relais: **GPIO13, aktiv high**, Wiederherstellung mit `ALWAYS_OFF`.
- Physischer Taster: **GPIO3 / RXD0, aktiv low**, Pull-up und 30 ms Entprellung.
- Relaisanzeige: **GPIO14, aktiv low**, folgt dem angeforderten Relaiszustand.
- Verbindungsanzeige: **GPIO0, aktiv low**.
- Serielles Logging: deaktiviert; vor dem Tastentest die UART-Leitungen des Programmieradapters trennen, da der Eingang RXD0 mitbenutzt.

Die Hardware-JSON der Werksanwendung enthielt diese Zuordnungen; spätere Beobachtungen von Taster, Relais und Anzeigen bestätigten sie. Weder ein Durchschalten der GPIO-Ausgänge noch eine neutrale Diagnosefirmware war nötig. Das Profil konfiguriert keine elektrische Leistungsmessung. LED- oder API-Zustand sind keine Rückmeldung der Relaiskontakte.

## Niederspannungsverdrahtung

**Vor dem Öffnen oder Anschließen irgendwelcher Leitungen das Gerät vollständig vom Stromnetz trennen. Während der gesamten Programmierung getrennt lassen.** Eine geregelte 3,3-V-Quelle und nachweislich 3,3-V-UART-Logik verwenden. Ein Pegelwandler ändert Signalpegel; er liefert dem Zielgerät keine geregelte Versorgung.

![Funktionale serielle Verdrahtung: externe 3,3-V-Versorgung, 5-V-UART-Adapter, Pegelwandler und TYWE3S](images/swp1-serial-wiring.svg)

Die Zeichnung zeigt elektrische Verbindungen, **keine physischen Padpositionen**. Modulanschlüsse anhand des [Tuya-TYWE3S-Datenblatts](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv) bestimmen und die Zeichnungsausrichtung mit der Platine vergleichen. Die Funktion eines Testpads auf der Trägerplatine nicht aus seiner Position ableiten. Die dokumentierte Nennversorgung beträgt 3,3 V.

Für den hier verwendeten Adapter mit 5-V-Logik:

1. Adapter **5V → HV**-Referenz des Pegelwandlers.
2. Externe geregelte **3.3V → Modul-VCC und Wandler-LV**.
3. Adapter-GND, Wandler-GND, Versorgungsminus und Modul-GND an eine gemeinsame Masse anschließen.
4. Adapter **TX → HV1**, zugehöriges **LV1 → Modul-RXD0**.
5. Modul **TXD0 → LV2**, zugehöriges **HV2 → Adapter-RX**.
6. Den 3V3-Ausgang des Adapters unbeschaltet lassen. Zwei Versorgungsausgänge nicht parallel schalten.

Einen für UART-Geschwindigkeit und Signalrichtung geeigneten Pegelwandler verwenden. Diese konkrete Kette funktionierte nach Korrektur der Verdrahtung mit 115200 Baud; das qualifiziert nicht jede preiswerte HV/LV-Platine. Bei einem echten 3,3-V-UART-Adapter kann der Wandler nach Prüfung des Ausgangspegels entfallen.

Der Adapter zeigte unbelastet zunächst 3,3 V, am angeschlossenen Zielgerät kamen aber nur **1,9 V** an. Sein TX-Signal erreichte außerdem **5,1 V**. Das sind getrennte Probleme: Eine externe Versorgung behob die Stromversorgung, der Wandler passte die UART-Pegel an. VCC am belasteten Modul und die Signalpegel gegen dieselbe Masse messen. Siehe [ESPHome-Hinweise zum physischen Anschluss](https://esphome.io/guides/physical_device_connection/).

## Downloadmodus, Backup und Firmware

Bei ausgeschalteter Versorgung **GPIO0 mit GND verbinden**. Die Niederspannungsversorgung wieder einschalten, dann **RST kurz mit GND verbinden und RST wieder freigeben**. EN high halten; RST nicht dauerhaft low halten. GPIO0 darf beim Flashen an Masse bleiben, die Brücke muss aber vor dem normalen Start entfernt werden. Die lesbare ROM-Meldung `boot mode:(1,0)` bestätigte hier den Downloadmodus. Siehe [Espressifs Dokumentation der Bootmodi](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html).

Nur ein Programm darf den seriellen Port besitzen. Miniterm vor esptool beenden. Die korrekte Kreuzung von TX/RX behob den letzten Kommunikationsfehler; eine leuchtende LED hatte keine funktionierende serielle Verbindung nachgewiesen.

Vor dem Schreiben las der Bediener **alle 2,097,152 Bytes** des Werks-Flashs aus und verifizierte das Backup mit esptool gegen das Gerät. Backups, rohe serielle Logs, kompilierte Images und Zugangsdaten außerhalb öffentlicher Git-Repositories aufbewahren: Ein Werksdump kann Provisionierungsgeheimnisse enthalten. Die [esptool-Befehlsreferenz](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html) beschreibt Identifikation, `read-flash`, `verify-flash` und `write-flash`. Die Lesegröße anhand der tatsächlichen Flash-Abfrage wählen, nicht anhand des Gehäusenamens.

Das [eigenständige Profil](../examples/swp1-pw2-v5.yaml) in einem neuen privaten Verzeichnis bauen. Diese Befehle im Repository-Stamm ausführen; nur dieses Profil kopieren, nicht die generische Basis oder ein XS-SSA01-Paket:

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

Der Secrets-Helfer fragt WLAN-Zugangsdaten ab, erzeugt unterschiedliche Schlüssel und verweigert das Überschreiben vorhandener Secrets. Diese Befehle kompilieren, ohne zu flashen. Zum Umgang mit Zugangsdaten siehe [verschlüsselte Provisionierung](security-profile.md). Dieses Exemplar verwendete **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz**. Das installierte Image war **429,600 Bytes** groß und wurde mit 115200 Baud an Adresse `0x0` geschrieben; esptool bestätigte den geschriebenen Hash. Neue Builds können anders groß sein; diese Bytezahl ist eine Beobachtung, keine Installationsanforderung.

## Normaler Start und Abnahme

Ausschalten, GPIO0–GND und beide UART-Signalleitungen entfernen, dann ausschließlich externe 3,3 V anlegen. Die verschlüsselte native API verband sich; ON/OFF funktionierte, und ein Software-Neustart aus ON stellte das Relais auf OFF zurück. Der Eigentümer bestätigte zwei Tastendrücke mit Relaisklicken und entsprechend folgender Anzeige.

Danach wurden alle provisorischen Leitungen und die externe Versorgung entfernt und das Gehäuse vor dem normalen Einbau geschlossen. Der Eigentümer meldete funktionierenden Betrieb an der eingebauten Steckdose. **Ein kontrollierter Netz-Aus-/Einschalttest aus ON sowie Messungen der Kontaktspannung und der Einschalttransienten wurden nicht durchgeführt.** Relaisklicken auf der Werkbank allein hätte kein Lastschalten bewiesen.

Home Assistant erhielt ein Relais sowie Diagnosewerte für Verbindung, Signal, Version und Neustart. Die installierte Rolle wurde in HA ohne erneutes Flashen umbenannt; der ursprüngliche Firmware-Hostname bleibt gültig. Der vollständige private Quellstand wurde sowohl im ESPHome-Verzeichnis von HA als auch im ESPHome Dashboard gespeichert. Das Relais wurde genau einmal im Bereich Living Room der zweiten Dashboard-Seite ergänzt. Eine spätere Quellbereitstellung muss diese Registry-Identitäten erhalten oder ausdrücklich migrieren.

## Wenn ein Schritt fehlschlägt

- **Keine serielle Antwort:** VCC unter Last, gemeinsame Masse, Adapter-TX → Modul-RX, Modul-TX → Adapter-RX und einen von Terminals freigegebenen Port prüfen.
- **Unlesbare Bytes:** Einen frischen Reset mit 74880 Baud für das ROM-Log erfassen; für die eigentliche Übertragung die gewählte esptool-Baudrate verwenden.
- **Weiter im Downloadmodus:** GPIO0-Massebrücke entfernen und neu starten.
- **Status-LED leuchtet beim Reset weiter:** GPIO0 steuert hier auch diese LED; die geerdete Bootbrücke kann dies erklären. Nicht als Resettest verwenden.
- **Taster funktioniert mit angeschlossenem Programmieradapter nicht:** UART trennen; GPIO3 wird gemeinsam benutzt.
- **API funktioniert, die Last aber nicht:** Ein gemeldeter Relaiszustand diagnostiziert weder Kontakte noch Spulenversorgung oder Netzverdrahtung. Keine offene, unter Netzspannung stehende Platine prüfen.
