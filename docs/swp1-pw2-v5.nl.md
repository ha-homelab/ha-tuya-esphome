# SWP1-PW2-V5 / TYWE3S: geverifieerde seriële conversie

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Eén SWP1-PW2-V5-exemplaar is op 2026-10-18 geconverteerd nadat gewone Tuya-Convert mislukte met PSK-identiteit `02`. Een bekabelde controle identificeerde ESP8266EX, een kristal van 26 MHz en 2 MiB flash. Een geverifieerde fabrieksback-up leverde de GPIO-indeling vóór het schrijven van de definitieve firmware. De eigenaar bevestigde daarna normaal gebruik als stopcontact bij de boekenkast.

Dit bewijs geldt voor dit exemplaar, niet voor elk product met een vergelijkbare behuizing. De oude doorgebrande schakelaar waarmee de hardware werd vergeleken, was een ander apparaat; diens Home Assistant-identiteit en LocalTuya-configuratie bleven behouden.

## Bevestigde hardware

- Relais: **GPIO13, actief hoog**, herstelmodus `ALWAYS_OFF`.
- Fysieke knop: **GPIO3 / RXD0, actief laag**, pull-up en 30 ms ontdendering.
- Relaisindicator: **GPIO14, actief laag**, volgt de aangestuurde relaisstatus.
- Verbindingsindicator: **GPIO0, actief laag**.
- Seriële logging: uitgeschakeld; koppel de UART-draden van de programmer los vóór de knoptest, want de ingang deelt RXD0.

De hardware-JSON van de fabrieksapplicatie gaf deze toewijzingen; latere waarnemingen van knop, relais en indicatoren kwamen ermee overeen. Een GPIO-uitgangsscan of neutrale diagnostische firmware was niet nodig. Het profiel configureert geen elektrische metingen. Een led of API-status geeft geen terugkoppeling van de relaiscontacten.

## Laagspanningsbedrading

**Koppel het apparaat volledig los van de netspanning voordat u het opent of iets aansluit. Houd het tijdens het hele programmeren losgekoppeld.** Gebruik een gestabiliseerde 3,3 V-voeding en gecontroleerde 3,3 V-UART-logica. Een niveauomzetter past signalen aan; hij levert geen gestabiliseerde voeding.

![Functionele seriële bedrading: externe 3,3 V-voeding, 5 V-UART-adapter, niveauomzetter en TYWE3S](images/swp1-serial-wiring.svg)

De tekening toont elektrische verbindingen, **geen fysieke soldeerpuntposities**. Identificeer modulepinnen met het [Tuya TYWE3S-datablad](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv) en vergelijk de oriëntatie met de print. Leid de functie van een testpunt op de draagprint niet af uit zijn positie. De gedocumenteerde nominale voeding is 3,3 V.

Voor de hier gebruikte adapter met 5 V-logica:

1. Adapter **5V → HV-referentie** van de niveauomzetter.
2. Externe gestabiliseerde **3.3V → VCC van de module en LV van de omzetter**.
3. Adapter-GND, omzetter-GND, voedingsmin en module-GND delen één massa.
4. Adapter **TX → HV1**, bijbehorende **LV1 → RXD0 van de module**.
5. Module **TXD0 → LV2**, bijbehorende **HV2 → RX van de adapter**.
6. Laat de 3V3-uitgang van de adapter los. Schakel nooit twee voedingsuitgangen parallel.

Gebruik een omzetter geschikt voor UART-snelheid en -richting. Deze keten werkte na bedradingscorrectie op 115200 baud; dat kwalificeert niet elke goedkope HV/LV-print. Een echte 3,3 V-UART-adapter kan zonder omzetter, nadat het uitgangsniveau is gecontroleerd.

De adapter mat onbelast 3,3 V, maar aangesloten kreeg het apparaat slechts **1,9 V**. TX leverde bovendien **5,1 V**. Dit zijn verschillende problemen: externe voeding corrigeerde VCC, de omzetter paste UART-niveaus aan. Meet VCC onder belasting bij de module en signalen ten opzichte van dezelfde massa. Zie de [ESPHome-handleiding voor fysieke verbindingen](https://esphome.io/guides/physical_device_connection/).

## Downloadmodus, back-up en firmware

Houd bij uitgeschakelde voeding **GPIO0 aan GND**. Schakel de laagspanning in en **verbind RST kort met GND en laat RST weer los**. Houd EN hoog; houd RST niet laag. GPIO0 mag tijdens het flashen aan massa blijven, maar verwijder de brug vóór normaal opstarten. De leesbare ROM-melding `boot mode:(1,0)` bevestigde hier downloadmodus. Zie de [Espressif-documentatie over opstartmodi](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html).

Slechts één programma mag de seriële poort gebruiken. Sluit Miniterm vóór esptool. Correct kruisen van TX/RX loste de laatste communicatiefout op; een brandende led bewees geen werkende seriële verbinding.

Vóór schrijven las de operator **alle 2,097,152 bytes** fabrieksflash en verifieerde de back-up met esptool tegen het apparaat. Bewaar back-ups, ruwe seriële logs, gebouwde images en inloggegevens buiten openbaar Git: een fabrieksdump kan provisioninggeheimen bevatten. De [esptool-commandoreferentie](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html) beschrijft identificatie, `read-flash`, `verify-flash` en `write-flash`. Bepaal de leesgrootte uit de werkelijke flashdetectie, niet de behuizingsnaam.

Bouw het [zelfstandige profiel](../examples/swp1-pw2-v5.yaml) in een nieuwe privédirectory. Voer deze opdrachten uit vanuit de repositoryroot; kopieer alleen dit profiel, niet de algemene basis of een XS-SSA01-pakket:

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

Het hulpprogramma vraagt wifi-inloggegevens, genereert afzonderlijke sleutels en weigert bestaande geheimen te overschrijven. Deze opdrachten compileren zonder flashen. Zie de [notities over versleutelde provisioning](security-profile.md). Dit exemplaar gebruikte **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz**. Het geïnstalleerde image was **429,600 bytes**, geschreven op `0x0` met 115200 baud; esptool bevestigde de geschreven hash. Nieuwe builds kunnen een andere grootte hebben: dit aantal is een waarneming, geen installatievereiste.

## Normaal opstarten en acceptatie

Schakel uit, verwijder GPIO0–GND en beide UART-signaaldraden, en herstel uitsluitend externe 3,3 V. De versleutelde native API maakte verbinding; ON/OFF-opdrachten werkten en een zachte herstart vanuit ON bracht het relais terug naar OFF. De eigenaar bevestigde twee knopdrukken met relaisklikken en een volgende indicator.

Daarna werden alle tijdelijke draden en externe voeding verwijderd en werd de behuizing gesloten vóór normale installatie. De eigenaar bevestigde dat het geïnstalleerde stopcontact werkte. **Een gecontroleerde netspanningscyclus vanuit ON, contactspanningsmetingen en metingen van opstarttransiënten zijn niet uitgevoerd.** Alleen werkbankklikken zouden het schakelen van een belasting niet bewijzen.

Home Assistant kreeg één relais plus diagnose voor verbinding, signaal, versie en herstart. De geïnstalleerde functie werd in HA hernoemd zonder opnieuw te flashen; de oorspronkelijke firmwarehostnaam blijft geldig. De volledige privébron werd opgeslagen in zowel de HA-ESPHome-map als ESPHome Dashboard. Het relais werd één keer toegevoegd aan Living Room op de tweede dashboardpagina. Toekomstige repositorydeployments moeten die registeridentiteiten behouden of expliciet migreren.

## Als een stap mislukt

- **Geen serieel antwoord:** controleer belaste VCC, gemeenschappelijke massa, adapter-TX → module-RX, module-TX → adapter-RX en of geen terminal de poort bezet.
- **Onleesbare bytes:** leg een nieuwe reset vast op 74880 baud voor de ROM-log; gebruik de gekozen esptool-baudrate voor de overdracht zelf.
- **Nog in downloadmodus:** verwijder de GPIO0–massabrug en herstart.
- **Statusled aan tijdens reset:** GPIO0 stuurt ook die led; de geaarde opstartbrug kan dit verklaren. Gebruik dit niet als resettest.
- **Knop werkt niet met programmer:** koppel UART los; GPIO3 wordt gedeeld.
- **API werkt, belasting niet:** gerapporteerde relaisstatus diagnosticeert geen contacten, spoelvoeding of netbedrading. Meet niet aan een blootliggende print onder netspanning.
