# SWP1-PW2-V5 / TYWE3S: conversión serie verificada

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Se convirtió una unidad SWP1-PW2-V5 el 2026-10-18, después de que Tuya-Convert convencional fallara con la identidad PSK `02`. Una comprobación por cable identificó un ESP8266EX, un cristal de 26 MHz y 2 MiB de flash. Una copia de fábrica verificada proporcionó el mapa GPIO antes de escribir el firmware final. El propietario confirmó después el funcionamiento normal como toma de corriente de una estantería.

Esta evidencia corresponde a esa unidad, no a cualquier producto con una carcasa similar. El interruptor antiguo y quemado usado como referencia de hardware era otro dispositivo: se conservaron su identidad de Home Assistant y su configuración LocalTuya.

## Hardware confirmado

- Relé: **GPIO13, activo en alto**, restauración `ALWAYS_OFF`.
- Botón físico: **GPIO3 / RXD0, activo en bajo**, pull-up y antirrebote de 30 ms.
- Indicador del relé: **GPIO14, activo en bajo**, sigue el estado ordenado al relé.
- Indicador de conexión: **GPIO0, activo en bajo**.
- Registro serie: desactivado; desconecte los cables UART del programador antes de probar el botón, porque su entrada comparte RXD0.

El JSON de hardware de la aplicación de fábrica identificó estas asignaciones; las observaciones posteriores del botón, relé e indicadores coincidieron. No fue necesario barrer las salidas GPIO ni usar firmware de diagnóstico neutro. El perfil no configura medición eléctrica. Un LED o estado de API no es realimentación de los contactos del relé.

## Cableado de baja tensión

**Desconecte completamente el dispositivo de la red eléctrica antes de abrirlo o conectar cualquier cosa. Manténgalo desconectado durante toda la programación.** Use una fuente regulada de 3,3 V y lógica UART de 3,3 V comprobada. Un conversor de nivel modifica las señales; no suministra alimentación regulada al dispositivo.

![Cableado serie funcional: fuente externa de 3,3 V, adaptador UART de 5 V, conversor de nivel y TYWE3S](images/swp1-serial-wiring.svg)

El dibujo muestra conexiones eléctricas, **no posiciones físicas de pads**. Localice los pines con la [hoja de datos Tuya TYWE3S](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv), comprobando la orientación del dibujo respecto a la placa. No deduzca la función de un pad de prueba de la placa portadora por su posición. La alimentación nominal documentada es 3,3 V.

Para el adaptador con lógica de 5 V usado en este caso:

1. **5V del adaptador → referencia HV** del conversor.
2. Fuente externa regulada **3.3V → VCC del módulo y LV del conversor**.
3. GND del adaptador, GND del conversor, negativo de la fuente y GND del módulo comparten una masa.
4. **TX del adaptador → HV1**, y su canal correspondiente **LV1 → RXD0 del módulo**.
5. **TXD0 del módulo → LV2**, y su canal correspondiente **HV2 → RX del adaptador**.
6. Deje desconectada la salida 3V3 del adaptador. No conecte dos salidas de alimentación en paralelo.

Use un conversor adecuado para la velocidad y dirección UART. Esta cadena concreta funcionó a 115200 baudios tras corregir el cableado; eso no valida cualquier placa HV/LV barata. Un adaptador UART auténtico de 3,3 V puede prescindir del conversor una vez verificado su nivel de salida.

El adaptador medía inicialmente 3,3 V sin carga, pero el dispositivo conectado recibía solo **1,9 V**. Además, llevaba TX a **5,1 V**. Son problemas distintos: una fuente externa resolvió la alimentación y el conversor adaptó los niveles UART. Mida VCC en el módulo bajo carga y las señales respecto a la misma masa. Consulte la [guía de conexión física de ESPHome](https://esphome.io/guides/physical_device_connection/).

## Modo de descarga, copia y firmware

Con la alimentación apagada, mantenga **GPIO0 conectado a GND**. Restablezca la baja tensión y después **conecte brevemente RST a GND y suelte RST**. Mantenga EN alto; no mantenga RST bajo. GPIO0 puede seguir a masa durante la escritura, pero quite el puente antes del arranque normal. El mensaje ROM legible `boot mode:(1,0)` confirmó aquí el modo de descarga. Consulte la [documentación de arranque de Espressif](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html).

Solo un programa puede controlar el puerto serie. Cierre Miniterm antes de ejecutar esptool. El cruce correcto de TX/RX resolvió el último fallo de comunicación; un LED encendido no demostraba un enlace serie operativo.

Antes de escribir, el operador leyó **los 2,097,152 bytes completos** de la flash de fábrica y verificó la copia contra el dispositivo con esptool. Guarde copias, registros serie sin procesar, imágenes compiladas y credenciales fuera del Git público: un volcado de fábrica puede contener secretos de aprovisionamiento. La [referencia de esptool](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html) documenta identificación, `read-flash`, `verify-flash` y `write-flash`. Elija el tamaño de lectura según la comprobación real de la flash, no el nombre de la carcasa.

Compile el [perfil independiente](../examples/swp1-pw2-v5.yaml) en un directorio privado nuevo. Ejecute estos comandos desde la raíz del repositorio; copie solo este perfil, no la base genérica ni un paquete XS-SSA01:

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

El asistente solicita las credenciales Wi-Fi, genera claves distintas y se niega a sobrescribir secretos existentes. Estos comandos compilan sin escribir la flash. Consulte las [notas de aprovisionamiento cifrado](security-profile.md) para gestionar credenciales. Esta unidad usó **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz**. La imagen instalada tenía **429,600 bytes**, escritos en `0x0` a 115200 baudios; esptool confirmó el hash escrito. Otra compilación puede tener un tamaño distinto: esta cifra es una observación, no un requisito de instalación.

## Arranque normal y aceptación

Apague, quite GPIO0–GND y ambos cables de señal UART, y restablezca solo los 3,3 V externos. Se conectó la API nativa cifrada; funcionaron los controles ON/OFF y un reinicio por software desde ON devolvió el relé a OFF. El propietario confirmó dos pulsaciones con clics del relé y el indicador siguiéndolas.

Después se retiraron todo el cableado temporal y la alimentación externa, y se cerró la carcasa antes de la instalación normal. El propietario confirmó funcionamiento en la toma instalada. **No se realizaron una prueba controlada de corte y retorno de red desde ON, mediciones de tensión en los contactos ni mediciones de transitorios de arranque.** Los clics en el banco no habrían demostrado por sí solos la conmutación de carga.

Home Assistant recibió un relé y diagnósticos de conexión, señal, versión y reinicio. Se cambió el nombre de la función instalada en HA sin volver a flashear: el hostname original del firmware sigue siendo válido. El código privado completo se guardó en el directorio ESPHome de HA y en ESPHome Dashboard. El relé se añadió una sola vez a la sección Living Room de la segunda página del panel. Un despliegue futuro debe conservar esas identidades del registro o migrarlas explícitamente.

## Si falla un paso

- **Sin respuesta serie:** compruebe VCC bajo carga, masa común, TX del adaptador → RX del módulo, TX del módulo → RX del adaptador y que ningún terminal ocupe el puerto.
- **Bytes ilegibles:** capture un reinicio nuevo a 74880 baudios para el registro ROM; use la velocidad esptool elegida para la transferencia real.
- **Sigue en modo de descarga:** quite el puente GPIO0 a masa y reinicie.
- **LED de estado encendido durante reset:** GPIO0 también controla ese LED; el puente de arranque a masa puede explicarlo. No lo use como prueba de reset.
- **El botón falla con el programador conectado:** desconecte UART; GPIO3 es compartido.
- **La API funciona pero la carga no:** el estado informado del relé no diagnostica contactos, alimentación de bobina ni cableado de red. No sondee una placa expuesta conectada a la red.
