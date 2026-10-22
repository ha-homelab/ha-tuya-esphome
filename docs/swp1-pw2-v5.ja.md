# SWP1-PW2-V5 / TYWE3S：検証済みのシリアル書き換え

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

通常の Tuya-Convert が PSK 識別子 `02` で失敗したため、2026-10-18 に SWP1-PW2-V5 の1台を変換しました。有線での調査により ESP8266EX、26 MHz 水晶発振子、2 MiB フラッシュを確認しました。検証済みの工場出荷時バックアップから GPIO 割り当てを得て、最終ファームウェアを書き込みました。その後、所有者は本棚のコンセントとして正常に動作することを確認しました。

この証拠は当該個体についてのもので、似た筐体の全製品には適用できません。ハードウェア比較に使った古い焼損スイッチは別の機器であり、その Home Assistant の識別情報と LocalTuya 設定は維持しました。

## 確認したハードウェア

- リレー：**GPIO13、アクティブ High**、復帰モード `ALWAYS_OFF`。
- 物理ボタン：**GPIO3 / RXD0、アクティブ Low**、プルアップと 30 ms のチャタリング除去。
- リレー表示灯：**GPIO14、アクティブ Low**、リレーに指示した状態に追従。
- 接続表示灯：**GPIO0、アクティブ Low**。
- シリアルログ：無効。ボタン入力は RXD0 と共用のため、ボタンのテスト前に書き込み器の UART 配線を外します。

工場出荷時アプリケーションのハードウェア JSON がこの割り当てを示し、後のボタン、リレー、表示灯の観察と一致しました。GPIO 出力の総当たりや中立的な診断ファームウェアは不要でした。このプロファイルは電力などの電気計測を設定しません。LED や API 状態はリレー接点からのフィードバックではありません。

## 低電圧配線

**開封または何かを接続する前に、商用電源から完全に切り離してください。書き込み中は最後まで切り離したままにします。** 安定化された 3.3 V 電源と、確認済みの 3.3 V UART ロジックを使用します。レベル変換器は信号を変換するもので、対象への安定化電源にはなりません。

![機能上のシリアル配線：外部 3.3 V 電源、5 V UART アダプター、レベル変換器、TYWE3S](images/swp1-serial-wiring.svg)

図は電気的な接続を示しており、**実際のパッド位置ではありません**。[Tuya TYWE3S データシート](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv)でピンを特定し、図の向きと基板を照合してください。キャリア基板のテストパッドの機能を位置だけで推測しないでください。記載された公称電源電圧は 3.3 V です。

今回使った 5 V ロジックのアダプターでは：

1. アダプターの **5V → 変換器の HV 基準端子**。
2. 外部安定化 **3.3V → モジュール VCC と変換器 LV**。
3. アダプター GND、変換器 GND、電源負極、モジュール GND を共通接地します。
4. アダプター **TX → HV1**、対応する **LV1 → モジュール RXD0**。
5. モジュール **TXD0 → LV2**、対応する **HV2 → アダプター RX**。
6. アダプターの 3V3 出力は接続しません。2つの電源出力を並列に接続しないでください。

UART の速度と方向に適した変換器を使います。この構成は配線修正後に 115200 baud で動作しましたが、安価な HV/LV 基板すべての適合性を示すものではありません。真正の 3.3 V UART アダプターなら、出力レベル確認後は変換器を省けます。

アダプターは無負荷で 3.3 V でしたが、接続した対象には **1.9 V** しか供給できませんでした。さらに TX は **5.1 V** でした。これは別々の問題で、外部電源が VCC を、変換器が UART レベルを解決しました。負荷を接続したモジュールで VCC を測定し、同じ GND を基準に信号を測定します。[ESPHome の物理接続ガイド](https://esphome.io/guides/physical_device_connection/)を参照してください。

## ダウンロードモード、バックアップ、ファームウェア

電源を切った状態で **GPIO0 を GND に接続**します。低電圧電源を戻し、**RST を短時間 GND に接続してから離します**。EN は High に保ち、RST を Low のままにしないでください。書き込み中は GPIO0 を接地したままでも構いませんが、通常起動前にはジャンパーを外します。読み取れた ROM メッセージ `boot mode:(1,0)` によりダウンロードモードを確認しました。[Espressif の起動モード資料](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html)を参照してください。

シリアルポートを占有できるプログラムは1つだけです。esptool の前に Miniterm を終了してください。TX/RX を正しく交差接続して最後の通信不良が解消しました。LED の点灯だけではシリアル接続の正常性は証明できません。

書き込み前に、作業者は工場出荷時フラッシュの **2,097,152 バイトすべて**を読み出し、esptool でバックアップと機器の内容を照合しました。バックアップ、生のシリアルログ、ビルドしたイメージ、認証情報は公開 Git の外に保存します。工場出荷時ダンプにはプロビジョニングの機密情報が含まれる可能性があります。[esptool コマンドリファレンス](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html)は識別、`read-flash`、`verify-flash`、`write-flash` を説明しています。読み出しサイズは筐体名ではなく、実際に検出したフラッシュから決めてください。

新しい非公開ディレクトリで[独立プロファイル](../examples/swp1-pw2-v5.yaml)をビルドします。次のコマンドはリポジトリのルートで実行します。このプロファイルだけをコピーし、汎用ベースや XS-SSA01 パッケージはコピーしません。

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

補助プログラムは Wi-Fi 認証情報を尋ね、異なる鍵を生成し、既存の機密情報の上書きを拒否します。これらのコマンドはコンパイルのみで、フラッシュには書き込みません。[暗号化プロビジョニングの注意事項](security-profile.md)を参照してください。この個体は **ESPHome 2026.9.1**、`esp_wroom_02`、**2 MiB、DOUT、40 MHz** を使用しました。導入したイメージは **429,600 バイト**で、115200 baud にて `0x0` に書き込み、esptool が書き込み後のハッシュを確認しました。再ビルド時にはサイズが変わることがあります。このバイト数は観察値であり、導入要件ではありません。

## 通常起動と受け入れ確認

電源を切り、GPIO0–GND と UART 信号線2本を外して、外部 3.3 V のみを再供給します。暗号化ネイティブ API が接続し、ON/OFF コマンドが動作し、ON からソフト再起動すると OFF に戻りました。所有者は2回のボタン操作でリレー音と表示灯の追従を確認しました。

その後、仮配線と外部電源をすべて外し、筐体を組み立ててから通常設置しました。所有者は設置済みコンセントの動作を確認しました。**ON 状態からの管理された商用電源の切断・再投入試験、接点電圧測定、起動過渡現象の測定は実施していません。** 作業台上のクリック音だけでは負荷の開閉は証明できません。

Home Assistant にはリレー1つと、接続、信号、バージョン、再起動の診断を追加しました。設置用途は再書き込みせず HA で名前を変更し、元のファームウェアホスト名は有効なままです。完全な非公開ソースを HA の ESPHome フォルダーと ESPHome Dashboard の両方に保存しました。リレーはダッシュボード2ページ目の Living Room セクションに1回だけ追加しました。今後のリポジトリからの展開ではレジストリ識別情報を維持するか、明示的に移行する必要があります。

## 手順が失敗した場合

- **シリアル応答なし：**負荷接続時の VCC、共通 GND、アダプター TX → モジュール RX、モジュール TX → アダプター RX、他の端末によるポート占有を確認します。
- **文字化け：**新たにリセットし、ROM ログを 74880 baud で取得します。実際の転送には選択した esptool の速度を使います。
- **ダウンロードモードのまま：**GPIO0–GND ジャンパーを外して再起動します。
- **リセット中に状態 LED が点灯：**GPIO0 はこの LED も駆動します。接地した起動ジャンパーが原因になり得るため、リセットの確認手段には使わないでください。
- **書き込み器接続中にボタンが動かない：**UART を外します。GPIO3 は共用です。
- **API は正常だが負荷が動かない：**報告されたリレー状態では接点、コイル電源、商用電源配線を診断できません。商用電源につながった露出基板をプローブで測定しないでください。
