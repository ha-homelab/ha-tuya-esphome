# SWP1-PW2-V5 / TYWE3S: conversione seriale verificata

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Un esemplare SWP1-PW2-V5 è stato convertito il 2026-10-18 dopo che Tuya-Convert ordinario aveva fallito con identità PSK `02`. Una verifica cablata ha identificato ESP8266EX, quarzo da 26 MHz e flash da 2 MiB. Un backup di fabbrica verificato ha fornito la mappa GPIO prima della scrittura del firmware definitivo. Il proprietario ha poi confermato il normale funzionamento come presa della libreria.

Queste prove riguardano quell'esemplare, non ogni prodotto con involucro simile. Il vecchio interruttore bruciato usato come riferimento hardware era un altro dispositivo: la sua identità Home Assistant e la configurazione LocalTuya sono state conservate.

## Hardware confermato

- Relè: **GPIO13, attivo alto**, ripristino `ALWAYS_OFF`.
- Pulsante fisico: **GPIO3 / RXD0, attivo basso**, pull-up e antirimbalzo di 30 ms.
- Indicatore relè: **GPIO14, attivo basso**, segue lo stato comandato del relè.
- Indicatore di connessione: **GPIO0, attivo basso**.
- Log seriale: disabilitato; scollegare i fili UART del programmatore prima di provare il pulsante, perché l'ingresso condivide RXD0.

Il JSON hardware dell'applicazione di fabbrica identificava queste assegnazioni; le successive osservazioni di pulsante, relè e indicatori le hanno confermate. Non è servita una scansione delle uscite GPIO né un firmware diagnostico neutro. Il profilo non configura misure elettriche. Un LED o lo stato API non sono un riscontro dei contatti del relè.

## Cablaggio a bassa tensione

**Scollegare completamente il dispositivo dalla rete elettrica prima di aprirlo o collegare qualsiasi cosa. Lasciarlo scollegato per tutta la programmazione.** Usare una sorgente regolata da 3,3 V e logica UART verificata a 3,3 V. Un traslatore adatta i livelli dei segnali; non fornisce alimentazione regolata al dispositivo.

![Cablaggio seriale funzionale: alimentazione esterna 3,3 V, adattatore UART 5 V, traslatore di livello e TYWE3S](images/swp1-serial-wiring.svg)

Il disegno mostra collegamenti elettrici, **non posizioni fisiche delle piazzole**. Individuare i pin usando il [datasheet Tuya TYWE3S](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv), verificando l'orientamento del disegno rispetto alla scheda. Non dedurre la funzione di una piazzola di test sulla scheda portante dalla posizione. L'alimentazione nominale documentata è 3,3 V.

Per l'adattatore con logica a 5 V usato qui:

1. **5V dell'adattatore → riferimento HV** del traslatore.
2. Sorgente esterna regolata **3.3V → VCC del modulo e LV del traslatore**.
3. GND di adattatore e traslatore, negativo della sorgente e GND del modulo condividono un'unica massa.
4. **TX dell'adattatore → HV1**, con il corrispondente **LV1 → RXD0 del modulo**.
5. **TXD0 del modulo → LV2**, con il corrispondente **HV2 → RX dell'adattatore**.
6. Lasciare scollegata l'uscita 3V3 dell'adattatore. Non mettere in parallelo due uscite di alimentazione.

Usare un traslatore adatto a velocità e direzione UART. Questa specifica catena ha funzionato a 115200 baud dopo la correzione del cablaggio; ciò non qualifica ogni scheda HV/LV economica. Un autentico adattatore UART da 3,3 V può omettere il traslatore dopo la verifica del livello di uscita.

L'adattatore inizialmente misurava 3,3 V a vuoto, ma il dispositivo collegato riceveva solo **1,9 V**. Inoltre portava TX a **5,1 V**. Sono problemi distinti: una sorgente esterna ha risolto l'alimentazione, il traslatore ha adattato i livelli UART. Misurare VCC sul modulo sotto carico e i segnali rispetto alla stessa massa. Vedere la [guida ESPHome ai collegamenti fisici](https://esphome.io/guides/physical_device_connection/).

## Modalità download, backup e firmware

A dispositivo spento, mantenere **GPIO0 collegato a GND**. Ripristinare la bassa tensione, quindi **collegare brevemente RST a GND e rilasciare RST**. Mantenere EN alto; non tenere RST basso. GPIO0 può restare a massa durante la scrittura, ma togliere il ponticello prima dell'avvio normale. Il messaggio ROM leggibile `boot mode:(1,0)` ha confermato qui la modalità download. Vedere la [documentazione Espressif sui modi di avvio](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html).

Un solo programma può possedere la porta seriale. Chiudere Miniterm prima di esptool. Il corretto incrocio TX/RX ha risolto l'ultimo errore di comunicazione; un LED acceso non dimostrava un collegamento seriale funzionante.

Prima di scrivere, l'operatore ha letto **tutti i 2,097,152 byte** della flash di fabbrica e ha verificato il backup rispetto al dispositivo con esptool. Conservare backup, log seriali grezzi, immagini compilate e credenziali fuori da Git pubblico: un dump di fabbrica può contenere segreti di provisioning. Il [riferimento dei comandi esptool](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html) descrive identificazione, `read-flash`, `verify-flash` e `write-flash`. Scegliere la dimensione di lettura dalla reale identificazione della flash, non dal nome dell'involucro.

Compilare il [profilo autonomo](../examples/swp1-pw2-v5.yaml) in una nuova directory privata. Eseguire questi comandi dalla radice del repository; copiare solo questo profilo, non la base generica o un pacchetto XS-SSA01:

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

L'assistente chiede le credenziali Wi-Fi, genera chiavi distinte e rifiuta di sovrascrivere segreti esistenti. Questi comandi compilano senza scrivere la flash. Per le credenziali vedere le [note sul provisioning cifrato](security-profile.md). Questo esemplare usava **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz**. L'immagine installata era di **429,600 byte**, scritti a `0x0` a 115200 baud; esptool ha confermato l'hash scritto. Altre compilazioni possono cambiare dimensione: questo numero è un'osservazione, non un requisito d'installazione.

## Avvio normale e accettazione

Spegnere, rimuovere GPIO0–GND ed entrambi i fili di segnale UART, quindi ripristinare solo i 3,3 V esterni. L'API nativa cifrata si è collegata; i comandi ON/OFF funzionavano e un riavvio software da ON riportava il relè a OFF. Il proprietario ha confermato due pressioni con scatti del relè e indicatore corrispondente.

Successivamente sono stati rimossi tutti i cablaggi temporanei e l'alimentazione esterna, e l'involucro è stato chiuso prima dell'installazione normale. Il proprietario ha confermato il funzionamento della presa installata. **Non sono stati eseguiti un test controllato di interruzione/ripristino della rete da ON, misure della tensione ai contatti o dei transitori di avvio.** Gli scatti sul banco da soli non avrebbero dimostrato la commutazione del carico.

Home Assistant ha ricevuto un relè e diagnostica di connessione, segnale, versione e riavvio. Il ruolo installato è stato rinominato in HA senza riflashare: l'hostname originale del firmware resta valido. Il sorgente privato completo è stato salvato nella directory ESPHome di HA e in ESPHome Dashboard. Il relè è stato aggiunto una sola volta alla sezione Living Room della seconda pagina della dashboard. Un futuro deployment deve preservare tali identità del registro o migrarle esplicitamente.

## Se un passaggio fallisce

- **Nessuna risposta seriale:** verificare VCC sotto carico, massa comune, TX adattatore → RX modulo, TX modulo → RX adattatore e che nessun terminale occupi la porta.
- **Byte illeggibili:** acquisire un nuovo reset a 74880 baud per il log ROM; usare il baud rate esptool scelto per il trasferimento effettivo.
- **Ancora in modalità download:** rimuovere il ponticello GPIO0–massa e riavviare.
- **LED di stato acceso durante reset:** GPIO0 pilota anche quel LED; il ponticello di avvio a massa può spiegarlo. Non usarlo come test del reset.
- **Pulsante non funzionante con programmatore collegato:** scollegare UART; GPIO3 è condiviso.
- **API funzionante ma carico no:** lo stato dichiarato del relè non diagnostica contatti, alimentazione della bobina o cablaggio di rete. Non sondare una scheda esposta alimentata dalla rete.
