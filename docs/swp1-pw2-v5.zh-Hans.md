# SWP1-PW2-V5 / TYWE3S：已验证的串口改装

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

一台 SWP1-PW2-V5 在常规 Tuya-Convert 因 PSK 标识 `02` 失败后，于 2026-10-18 完成改装。有线探测识别出 ESP8266EX、26 MHz 晶振和 2 MiB 闪存。经过验证的出厂备份在写入最终固件前提供了 GPIO 映射。随后，机主确认它作为书架插座正常工作。

这些证据仅适用于这台样机，并不代表所有外壳相似的产品。用于硬件对照的旧烧毁开关是另一台设备；其 Home Assistant 身份和 LocalTuya 配置均予以保留。

## 已确认的硬件

- 继电器：**GPIO13，高电平有效**，恢复模式为 `ALWAYS_OFF`。
- 实体按键：**GPIO3 / RXD0，低电平有效**，启用上拉及 30 ms 消抖。
- 继电器指示灯：**GPIO14，低电平有效**，跟随继电器的指令状态。
- 连接状态灯：**GPIO0，低电平有效**。
- 串口日志：禁用；按键输入与 RXD0 共用，因此测试按键前须拔掉烧录器的 UART 线。

出厂应用的硬件 JSON 给出了这些引脚分配，之后的按键、继电器和指示灯观察结果与之吻合。无需逐一扫描 GPIO 输出，也无需中性诊断固件。该配置不提供电气计量。LED 或 API 状态都不是继电器触点反馈。

## 低压接线

**打开设备或连接任何东西之前，必须完全断开市电。整个烧录过程都必须保持市电断开。** 使用稳压 3.3 V 电源和经过确认的 3.3 V UART 逻辑电平。电平转换器只转换信号，不为目标设备提供稳压电源。

![功能性串口接线：外部 3.3 V 电源、5 V UART 适配器、电平转换器与 TYWE3S](images/swp1-serial-wiring.svg)

图中表示电气连接，**不是焊盘的实际位置**。依据 [Tuya TYWE3S 数据手册](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv)识别模块引脚，并核对图示方向与电路板方向。不能仅凭载板测试焊盘的位置判断其功能。文档规定的额定供电为 3.3 V。

对于本次使用的 5 V 逻辑适配器：

1. 适配器 **5V → 转换器 HV 参考端**。
2. 外部稳压 **3.3V → 模块 VCC 及转换器 LV**。
3. 适配器 GND、转换器 GND、电源负极和模块 GND 共地。
4. 适配器 **TX → HV1**，对应的 **LV1 → 模块 RXD0**。
5. 模块 **TXD0 → LV2**，对应的 **HV2 → 适配器 RX**。
6. 适配器的 3V3 输出保持悬空。绝不能并联两个电源输出。

转换器必须适合 UART 的速度与方向。修正接线后，本次整条链路在 115200 baud 下工作正常；这并不保证所有廉价 HV/LV 小板都适用。真正的 3.3 V UART 适配器在确认输出电平后可以不使用转换器。

适配器空载时测得 3.3 V，但连接目标后只剩 **1.9 V**。同时，其 TX 输出为 **5.1 V**。这是两个独立的问题：外部电源解决 VCC 供电，转换器解决 UART 电平。应在模块带载时测量 VCC，并以同一地为参考测量信号。参阅 [ESPHome 物理连接指南](https://esphome.io/guides/physical_device_connection/)。

## 下载模式、备份与固件

断电时将 **GPIO0 接至 GND**。恢复低压供电，然后**短暂将 RST 接地，再释放 RST**。保持 EN 为高电平，不要持续拉低 RST。烧录时 GPIO0 可以保持接地，但正常启动前须拆除跳线。可读的 ROM 信息 `boot mode:(1,0)` 在这里确认了下载模式。参阅 [Espressif 启动模式文档](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html)。

同一时间只能由一个程序占用串口。运行 esptool 前须退出 Miniterm。正确交叉连接 TX/RX 解决了最后一个通信故障；LED 亮起不能证明串口连接有效。

写入前，操作者读取了出厂闪存的**全部 2,097,152 字节**，并用 esptool 将备份与设备内容对照验证。备份、原始串口日志、构建镜像和凭据应保存在公共 Git 之外：出厂转储可能含有配置机密。[esptool 命令参考](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html)说明了识别、`read-flash`、`verify-flash` 和 `write-flash`。读取大小应依据实际闪存探测结果，而不是外壳名称。

在新的私有目录中构建[独立配置](../examples/swp1-pw2-v5.yaml)。从仓库根目录运行以下命令；只复制这个配置，不要复制通用基础配置或 XS-SSA01 包：

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

辅助程序会询问 Wi-Fi 凭据，生成各自独立的密钥，并拒绝覆盖已有机密。上述命令只编译，不烧录。凭据处理见[加密配置说明](security-profile.md)。这台样机使用 **ESPHome 2026.9.1**、`esp_wroom_02`、**2 MiB、DOUT、40 MHz**。安装的镜像为 **429,600 字节**，以 115200 baud 写入 `0x0`；esptool 确认了写入后的哈希。重新构建后大小可能变化：该字节数是观察值，不是安装要求。

## 正常启动与验收

断电，拆除 GPIO0–GND 跳线及两根 UART 信号线，然后仅恢复外部 3.3 V 电源。加密原生 API 成功连接，ON/OFF 命令正常，从 ON 状态软重启后恢复为 OFF。机主确认两次按键均有继电器动作声，指示灯也同步变化。

之后，拆除了所有临时接线和外部电源，合上外壳后才进行正常安装。机主确认安装后的插座可用。**没有进行从 ON 状态受控断开及恢复市电的测试，也未测量触点电压或启动瞬态。** 单凭工作台上的动作声并不能证明负载被切换。

Home Assistant 中增加了一个继电器及连接、信号、版本和重启诊断。安装用途在 HA 中重命名，无需重刷；固件原始主机名仍有效。完整私有源文件同时保存到 HA 的 ESPHome 目录和 ESPHome Dashboard。该继电器仅添加一次，位于第二个仪表板页面的 Living Room 区域。后续从仓库部署时必须保留这些注册表身份，或显式迁移。

## 如果某一步失败

- **串口没有响应：**检查带载 VCC、共地、适配器 TX → 模块 RX、模块 TX → 适配器 RX，并确认没有其他终端占用端口。
- **字节不可读：**以 74880 baud 捕获一次新复位的 ROM 日志；实际传输则使用选定的 esptool 波特率。
- **仍处于下载模式：**拆除 GPIO0–地跳线，再重启。
- **复位期间状态灯亮：**GPIO0 也驱动该 LED，接地的启动跳线可能是原因。不能将它当作复位测试。
- **连着烧录器时按键无效：**拔掉 UART；GPIO3 是共用引脚。
- **API 正常但负载不工作：**报告的继电器状态不能诊断触点、线圈供电或市电接线。不要探测暴露且连接市电的电路板。
