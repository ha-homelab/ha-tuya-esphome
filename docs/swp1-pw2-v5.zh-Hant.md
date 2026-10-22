# SWP1-PW2-V5 / TYWE3S：已驗證的序列埠改裝

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

一台 SWP1-PW2-V5 在一般 Tuya-Convert 因 PSK 識別碼 `02` 失敗後，於 2026-10-18 完成改裝。有線探測辨識出 ESP8266EX、26 MHz 晶振和 2 MiB 快閃記憶體。經驗證的出廠備份在寫入最終韌體前提供了 GPIO 對應。之後，機主確認它作為書架插座正常運作。

這些證據僅適用於這台樣機，不代表所有外殼相似的產品。用來比對硬體的舊燒毀開關是另一台裝置；其 Home Assistant 身分與 LocalTuya 設定均予以保留。

## 已確認的硬體

- 繼電器：**GPIO13，高電位有效**，還原模式為 `ALWAYS_OFF`。
- 實體按鈕：**GPIO3 / RXD0，低電位有效**，啟用上拉及 30 ms 去彈跳。
- 繼電器指示燈：**GPIO14，低電位有效**，跟隨繼電器的命令狀態。
- 連線狀態燈：**GPIO0，低電位有效**。
- 序列日誌：停用；按鈕輸入與 RXD0 共用，因此測試按鈕前須拔除燒錄器的 UART 線。

出廠應用程式的硬體 JSON 提供了這些接腳分配，後續的按鈕、繼電器與指示燈觀察結果均相符。不必逐一掃描 GPIO 輸出，也不必使用中性診斷韌體。此設定不提供電氣計量。LED 或 API 狀態都不是繼電器接點回授。

## 低壓接線

**開啟裝置或連接任何東西之前，必須完全切斷市電。整個燒錄過程都必須保持市電斷開。** 使用穩壓 3.3 V 電源及經確認的 3.3 V UART 邏輯電位。電位轉換器只轉換訊號，不為目標裝置提供穩壓電源。

![功能性序列接線：外部 3.3 V 電源、5 V UART 轉接器、電位轉換器與 TYWE3S](images/swp1-serial-wiring.svg)

圖中表示電氣連接，**並非焊墊的實際位置**。依照 [Tuya TYWE3S 資料表](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv)辨識模組接腳，並核對圖示方向與電路板方向。不可僅憑載板測試焊墊的位置判斷功能。文件記載的額定供電為 3.3 V。

對於本次使用的 5 V 邏輯轉接器：

1. 轉接器 **5V → 轉換器 HV 參考端**。
2. 外部穩壓 **3.3V → 模組 VCC 及轉換器 LV**。
3. 轉接器 GND、轉換器 GND、電源負極及模組 GND 共地。
4. 轉接器 **TX → HV1**，對應的 **LV1 → 模組 RXD0**。
5. 模組 **TXD0 → LV2**，對應的 **HV2 → 轉接器 RX**。
6. 轉接器的 3V3 輸出保持未連接。絕不可並聯兩個電源輸出。

轉換器必須適用於 UART 的速度與方向。修正接線後，本次整條鏈路在 115200 baud 下正常運作；這不保證所有廉價 HV/LV 小板都適用。真正的 3.3 V UART 轉接器在確認輸出電位後可省略轉換器。

轉接器空載時量得 3.3 V，但接上目標後只剩 **1.9 V**。此外，TX 輸出為 **5.1 V**。這是兩個獨立問題：外部電源解決 VCC 供電，轉換器解決 UART 電位。應在模組帶載時量測 VCC，並以同一地為基準量測訊號。參閱 [ESPHome 實體連接指南](https://esphome.io/guides/physical_device_connection/)。

## 下載模式、備份與韌體

斷電時將 **GPIO0 接到 GND**。恢復低壓供電，然後**短暫將 RST 接地，再釋放 RST**。保持 EN 為高電位，不可持續拉低 RST。燒錄時 GPIO0 可維持接地，但正常啟動前須拆除跳線。可讀的 ROM 訊息 `boot mode:(1,0)` 在此確認了下載模式。參閱 [Espressif 啟動模式文件](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html)。

同一時間只能由一個程式占用序列埠。執行 esptool 前須退出 Miniterm。正確交叉連接 TX/RX 解決了最後一項通訊故障；LED 亮起不能證明序列連接正常。

寫入前，操作人員讀取了出廠快閃記憶體的**全部 2,097,152 位元組**，並以 esptool 對照裝置內容驗證備份。備份、原始序列日誌、建置映像與憑證應保存在公開 Git 之外：出廠傾印可能含有佈建機密。[esptool 指令參考](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html)說明了識別、`read-flash`、`verify-flash` 和 `write-flash`。讀取大小應依實際快閃記憶體探測結果決定，而非外殼名稱。

在新的私人目錄中建置[獨立設定](../examples/swp1-pw2-v5.yaml)。從儲存庫根目錄執行以下指令；只複製此設定，不要複製通用基礎設定或 XS-SSA01 套件：

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

輔助程式會詢問 Wi-Fi 憑證，產生各自獨立的金鑰，並拒絕覆寫既有機密。以上指令只編譯，不燒錄。憑證處理見[加密佈建說明](security-profile.md)。這台樣機使用 **ESPHome 2026.9.1**、`esp_wroom_02`、**2 MiB、DOUT、40 MHz**。安裝的映像為 **429,600 位元組**，以 115200 baud 寫入 `0x0`；esptool 確認了寫入後的雜湊值。重新建置後大小可能不同：此位元組數是觀察值，不是安裝要求。

## 正常啟動與驗收

斷電，移除 GPIO0–GND 跳線及兩條 UART 訊號線，然後僅恢復外部 3.3 V 電源。加密原生 API 成功連線，ON/OFF 指令正常，從 ON 狀態軟體重新啟動後還原為 OFF。機主確認兩次按鈕操作都有繼電器動作聲，指示燈也同步改變。

之後移除所有臨時接線與外部電源，合上外殼才進行正常安裝。機主確認安裝後的插座可用。**未進行從 ON 狀態受控切斷及恢復市電的測試，也未量測接點電壓或啟動暫態。** 僅憑工作檯上的動作聲，不能證明負載被切換。

Home Assistant 中新增了一個繼電器及連線、訊號、版本和重新啟動診斷。安裝用途在 HA 中重新命名，無須重刷；韌體原始主機名稱仍有效。完整私人原始檔同時保存在 HA 的 ESPHome 目錄及 ESPHome Dashboard。繼電器只加入一次，位於第二個儀表板頁面的 Living Room 區域。後續從儲存庫部署時，必須保留這些登錄身分或明確遷移。

## 若某一步失敗

- **序列埠沒有回應：**檢查帶載 VCC、共地、轉接器 TX → 模組 RX、模組 TX → 轉接器 RX，並確認沒有其他終端程式占用埠。
- **位元組無法讀取：**以 74880 baud 擷取一次新重設的 ROM 日誌；實際傳輸則使用選定的 esptool 鮑率。
- **仍在下載模式：**移除 GPIO0–地跳線，再重新啟動。
- **重設時狀態燈亮：**GPIO0 也驅動此 LED，接地的啟動跳線可能是原因。不可把它當作重設測試。
- **連著燒錄器時按鈕無效：**拔除 UART；GPIO3 是共用接腳。
- **API 正常但負載不工作：**回報的繼電器狀態不能診斷接點、線圈供電或市電接線。不可探測外露且連接市電的電路板。
