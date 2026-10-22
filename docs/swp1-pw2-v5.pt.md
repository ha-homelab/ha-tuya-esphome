# SWP1-PW2-V5 / TYWE3S: conversão serial verificada

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Um exemplar SWP1-PW2-V5 foi convertido em 2026-10-18 após a tentativa convencional de Tuya-Convert falhar com identidade PSK `02`. A sondagem por fio identificou ESP8266EX, cristal de 26 MHz e flash de 2 MiB. Um backup de fábrica verificado forneceu o mapa GPIO antes da gravação do firmware final. Depois, o proprietário confirmou o funcionamento normal como tomada da estante.

Estas evidências referem-se a esse exemplar, não a todos os produtos com aparência semelhante. O interruptor antigo queimado usado na comparação de hardware era outro dispositivo; sua identidade Home Assistant e configuração LocalTuya foram preservadas.

## Hardware confirmado

- Relé: **GPIO13, ativo em nível alto**, restauração `ALWAYS_OFF`.
- Botão físico: **GPIO3 / RXD0, ativo em nível baixo**, pull-up e debounce de 30 ms.
- Indicador do relé: **GPIO14, ativo em nível baixo**, acompanha o estado comandado do relé.
- Indicador de conexão: **GPIO0, ativo em nível baixo**.
- Log serial: desativado; desconecte os fios UART do programador antes de testar o botão, pois a entrada compartilha RXD0.

O JSON de hardware da aplicação de fábrica identificou essas atribuições; as observações posteriores do botão, relé e indicadores concordaram. Não foi necessária uma varredura das saídas GPIO nem firmware diagnóstico neutro. O perfil não configura medição elétrica. LED ou estado da API não fornecem retorno dos contatos do relé.

## Ligações de baixa tensão

**Desconecte completamente da rede elétrica antes de abrir ou conectar qualquer coisa. Mantenha desconectado durante toda a programação.** Use alimentação regulada de 3,3 V e lógica UART de 3,3 V verificada. Um conversor de nível adapta sinais; não fornece alimentação regulada ao dispositivo.

![Ligações seriais funcionais: alimentação externa de 3,3 V, adaptador UART de 5 V, conversor de nível e TYWE3S](images/swp1-serial-wiring.svg)

O desenho mostra ligações elétricas, **não posições físicas dos pontos de solda**. Identifique os pinos pelo [datasheet Tuya TYWE3S](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv), comparando a orientação com a placa. Não deduza a função de pontos de teste da placa principal pela posição. A alimentação nominal documentada é 3,3 V.

Para o adaptador com lógica de 5 V usado aqui:

1. **5V do adaptador → referência HV** do conversor.
2. Fonte externa regulada **3.3V → VCC do módulo e LV do conversor**.
3. GND do adaptador, GND do conversor, negativo da fonte e GND do módulo compartilham o mesmo terra.
4. **TX do adaptador → HV1**, com o correspondente **LV1 → RXD0 do módulo**.
5. **TXD0 do módulo → LV2**, com o correspondente **HV2 → RX do adaptador**.
6. Deixe a saída 3V3 do adaptador desconectada. Nunca coloque duas saídas de alimentação em paralelo.

Use um conversor adequado à velocidade e direção UART. Esta cadeia funcionou a 115200 baud após corrigir as ligações; isso não qualifica toda placa HV/LV barata. Um adaptador UART genuinamente de 3,3 V pode dispensar o conversor após verificar o nível de saída.

O adaptador media 3,3 V sem carga, mas o dispositivo conectado recebia apenas **1,9 V**. Além disso, TX fornecia **5,1 V**. São problemas distintos: a alimentação externa corrigiu VCC e o conversor ajustou os níveis UART. Meça VCC no módulo sob carga e os sinais em relação ao mesmo terra. Consulte o [guia ESPHome de conexões físicas](https://esphome.io/guides/physical_device_connection/).

## Modo de download, backup e firmware

Com a alimentação desligada, mantenha **GPIO0 ligado a GND**. Restabeleça a baixa tensão e **ligue brevemente RST a GND, soltando RST em seguida**. Mantenha EN alto; não mantenha RST baixo. GPIO0 pode continuar aterrado durante a gravação, mas retire a ponte antes da inicialização normal. A mensagem legível da ROM `boot mode:(1,0)` confirmou o modo de download. Veja a [documentação Espressif dos modos de inicialização](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html).

Apenas um programa pode usar a porta serial. Feche Miniterm antes de esptool. Cruzar TX/RX corretamente resolveu a última falha de comunicação; um LED aceso não provava uma conexão serial funcional.

Antes de gravar, o operador leu **todos os 2,097,152 bytes** da flash de fábrica e verificou o backup contra o dispositivo com esptool. Mantenha backups, logs seriais brutos, imagens compiladas e credenciais fora do Git público: um dump de fábrica pode conter segredos de provisionamento. A [referência de comandos esptool](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html) descreve identificação, `read-flash`, `verify-flash` e `write-flash`. Escolha o tamanho da leitura pela identificação real da flash, não pelo nome da carcaça.

Compile o [perfil independente](../examples/swp1-pw2-v5.yaml) em uma nova pasta privada. Execute estes comandos na raiz do repositório; copie somente este perfil, não a base genérica nem um pacote XS-SSA01:

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

O assistente solicita credenciais Wi-Fi, gera chaves distintas e recusa sobrescrever segredos existentes. Estes comandos compilam sem gravar a flash. Veja as [notas de provisionamento criptografado](security-profile.md). Este exemplar usava **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz**. A imagem instalada tinha **429,600 bytes**, gravados em `0x0` a 115200 baud; esptool confirmou o hash gravado. Outras compilações podem ter tamanhos diferentes: esse número é uma observação, não um requisito de instalação.

## Inicialização normal e aceitação

Desligue, remova GPIO0–GND e os dois fios de sinal UART, depois restabeleça somente os 3,3 V externos. A API nativa criptografada conectou; ON/OFF funcionou e uma reinicialização por software a partir de ON restaurou OFF. O proprietário confirmou dois apertos do botão com cliques do relé e indicador acompanhando.

Depois, todos os fios temporários e a alimentação externa foram removidos, e a carcaça foi fechada antes da instalação normal. O proprietário confirmou que a tomada instalada funciona. **Não foram feitos teste controlado de interrupção/restauração da rede a partir de ON, medições de tensão dos contatos nem de transientes de inicialização.** Cliques na bancada, sozinhos, não provariam comutação da carga.

Home Assistant recebeu um relé e diagnósticos de conexão, sinal, versão e reinicialização. A função instalada foi renomeada no HA sem regravar; o hostname original do firmware permanece válido. O código privado completo foi salvo na pasta ESPHome do HA e no ESPHome Dashboard. O relé foi adicionado uma única vez à seção Living Room da segunda página do painel. Futuras implantações do repositório devem preservar essas identidades de registro ou migrá-las explicitamente.

## Se uma etapa falhar

- **Sem resposta serial:** verifique VCC sob carga, terra comum, TX do adaptador → RX do módulo, TX do módulo → RX do adaptador e se nenhum terminal ocupa a porta.
- **Bytes ilegíveis:** capture um novo reset a 74880 baud para o log ROM; use a taxa esptool escolhida para a transferência efetiva.
- **Ainda em download:** remova a ponte GPIO0–terra e reinicie.
- **LED de status aceso durante reset:** GPIO0 também controla esse LED; a ponte de inicialização aterrada pode explicar isso. Não use como teste de reset.
- **Botão falha com programador conectado:** desconecte UART; GPIO3 é compartilhado.
- **API funciona, carga não:** o estado relatado não diagnostica contatos, alimentação da bobina nem fiação da rede. Não sonde uma placa exposta energizada pela rede.
