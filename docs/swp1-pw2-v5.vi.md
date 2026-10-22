# SWP1-PW2-V5 / TYWE3S: chuyển đổi qua cổng nối tiếp đã xác minh

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Một mẫu SWP1-PW2-V5 được chuyển đổi ngày 2026-10-18 sau khi Tuya-Convert thông thường thất bại với định danh PSK `02`. Kiểm tra có dây xác định ESP8266EX, thạch anh 26 MHz và flash 2 MiB. Bản sao lưu xuất xưởng đã xác minh cung cấp sơ đồ GPIO trước khi ghi firmware cuối cùng. Sau đó chủ thiết bị xác nhận hoạt động bình thường như ổ cắm tại giá sách.

Bằng chứng chỉ áp dụng cho mẫu này, không phải mọi sản phẩm có vỏ tương tự. Công tắc cũ bị cháy dùng để so sánh phần cứng là thiết bị khác; định danh Home Assistant và cấu hình LocalTuya của nó được giữ nguyên.

## Phần cứng đã xác nhận

- Rơ-le: **GPIO13, kích hoạt mức cao**, khôi phục `ALWAYS_OFF`.
- Nút vật lý: **GPIO3 / RXD0, kích hoạt mức thấp**, kéo lên và chống dội 30 ms.
- Đèn rơ-le: **GPIO14, kích hoạt mức thấp**, theo trạng thái được ra lệnh của rơ-le.
- Đèn kết nối: **GPIO0, kích hoạt mức thấp**.
- Nhật ký nối tiếp: tắt; tháo dây UART của bộ nạp trước khi thử nút vì đầu vào dùng chung RXD0.

JSON phần cứng của ứng dụng xuất xưởng xác định các gán chân này; quan sát nút, rơ-le và đèn sau đó khớp với chúng. Không cần quét đầu ra GPIO hay firmware chẩn đoán trung tính. Hồ sơ không cấu hình đo điện. Đèn LED hoặc trạng thái API không phải phản hồi từ tiếp điểm rơ-le.

## Đấu dây điện áp thấp

**Ngắt hoàn toàn thiết bị khỏi điện lưới trước khi mở hoặc kết nối bất kỳ thứ gì. Giữ thiết bị ngắt điện lưới suốt quá trình lập trình.** Dùng nguồn ổn áp 3,3 V và mức logic UART 3,3 V đã xác minh. Bộ chuyển mức điều chỉnh tín hiệu; không cấp nguồn ổn áp cho thiết bị.

![Đấu nối tiếp theo chức năng: nguồn ngoài 3,3 V, bộ UART 5 V, bộ chuyển mức và TYWE3S](images/swp1-serial-wiring.svg)

Hình thể hiện kết nối điện, **không phải vị trí vật lý của điểm hàn**. Xác định chân theo [datasheet Tuya TYWE3S](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv), đối chiếu hướng hình với bo mạch. Không suy đoán chức năng điểm thử trên bo chính từ vị trí của nó. Nguồn danh định được ghi là 3,3 V.

Với bộ chuyển USB-UART logic 5 V dùng ở đây:

1. **5V của bộ UART → tham chiếu HV** của bộ chuyển mức.
2. Nguồn ngoài ổn áp **3.3V → VCC mô-đun và LV bộ chuyển mức**.
3. GND bộ UART, GND bộ chuyển mức, cực âm nguồn và GND mô-đun dùng chung mass.
4. **TX bộ UART → HV1**, cặp tương ứng **LV1 → RXD0 mô-đun**.
5. **TXD0 mô-đun → LV2**, cặp tương ứng **HV2 → RX bộ UART**.
6. Để đầu ra 3V3 của bộ UART không nối. Tuyệt đối không nối song song hai đầu ra nguồn.

Dùng bộ chuyển mức phù hợp tốc độ và hướng UART. Chuỗi này hoạt động ở 115200 baud sau khi sửa dây; điều đó không xác nhận mọi bo HV/LV giá rẻ. Bộ UART 3,3 V thực sự có thể bỏ bộ chuyển mức sau khi kiểm tra mức đầu ra.

Bộ UART đo được 3,3 V khi không tải, nhưng thiết bị đã nối chỉ nhận **1,9 V**. TX còn xuất **5,1 V**. Đây là hai vấn đề riêng: nguồn ngoài sửa VCC, bộ chuyển mức điều chỉnh UART. Đo VCC tại mô-đun đang chịu tải và tín hiệu so với cùng mass. Xem [hướng dẫn kết nối vật lý ESPHome](https://esphome.io/guides/physical_device_connection/).

## Chế độ tải, sao lưu và firmware

Khi tắt nguồn, giữ **GPIO0 nối GND**. Cấp lại điện áp thấp, rồi **chạm RST vào GND trong chốc lát và nhả RST**. Giữ EN ở mức cao; không giữ RST thấp. GPIO0 có thể nối mass khi ghi, nhưng tháo cầu nối trước khi khởi động bình thường. Thông báo ROM đọc được `boot mode:(1,0)` xác nhận chế độ tải. Xem [tài liệu chế độ khởi động Espressif](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html).

Chỉ một chương trình được chiếm cổng nối tiếp. Thoát Miniterm trước esptool. Đấu chéo TX/RX đúng đã giải quyết lỗi liên lạc cuối cùng; LED sáng không chứng minh kết nối nối tiếp hoạt động.

Trước khi ghi, người vận hành đọc **toàn bộ 2,097,152 byte** flash xuất xưởng và dùng esptool kiểm chứng bản sao với thiết bị. Giữ bản sao, nhật ký nối tiếp thô, ảnh firmware đã dựng và thông tin xác thực ngoài Git công khai: bản dump xuất xưởng có thể chứa bí mật cấp cấu hình. [Tham chiếu lệnh esptool](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html) mô tả nhận dạng, `read-flash`, `verify-flash` và `write-flash`. Chọn kích thước đọc theo flash thực tế được phát hiện, không theo tên vỏ.

Dựng [hồ sơ độc lập](../examples/swp1-pw2-v5.yaml) trong thư mục riêng tư mới. Chạy các lệnh tại gốc kho mã; chỉ sao chép hồ sơ này, không dùng cơ sở chung hay gói XS-SSA01:

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

Trình trợ giúp hỏi thông tin Wi-Fi, tạo các khóa riêng biệt và từ chối ghi đè bí mật hiện có. Các lệnh chỉ biên dịch, không ghi flash. Xem [ghi chú cấp cấu hình mã hóa](security-profile.md). Mẫu này dùng **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz**. Ảnh được cài có **429,600 byte**, ghi tại `0x0` ở 115200 baud; esptool xác nhận hash đã ghi. Kích thước bản dựng khác có thể thay đổi: số byte này là quan sát, không phải yêu cầu cài đặt.

## Khởi động bình thường và nghiệm thu

Tắt nguồn, tháo GPIO0–GND và cả hai dây tín hiệu UART, rồi chỉ cấp lại nguồn ngoài 3,3 V. API native mã hóa kết nối được; ON/OFF hoạt động và khởi động lại bằng phần mềm từ ON đưa rơ-le về OFF. Chủ thiết bị xác nhận hai lần nhấn nút có tiếng rơ-le và đèn đi theo.

Sau đó tháo toàn bộ dây tạm và nguồn ngoài, đóng vỏ trước khi lắp đặt bình thường. Chủ thiết bị xác nhận ổ cắm đã lắp hoạt động. **Chưa thực hiện thử ngắt/cấp điện lưới có kiểm soát từ ON, đo điện áp tiếp điểm hay đo quá độ lúc khởi động.** Tiếng tách trên bàn thử đơn thuần không chứng minh đóng cắt tải.

Home Assistant nhận một rơ-le cùng chẩn đoán kết nối, tín hiệu, phiên bản và khởi động lại. Vai trò lắp đặt được đổi tên trong HA không cần nạp lại; tên máy gốc của firmware vẫn hợp lệ. Toàn bộ nguồn riêng tư được lưu trong thư mục ESPHome của HA và ESPHome Dashboard. Rơ-le được thêm đúng một lần vào phần Living Room trên trang dashboard thứ hai. Các lần triển khai kho mã sau phải giữ nguyên định danh registry đó hoặc di chuyển chúng rõ ràng.

## Nếu một bước thất bại

- **Không có phản hồi nối tiếp:** kiểm tra VCC có tải, mass chung, TX bộ UART → RX mô-đun, TX mô-đun → RX bộ UART và không có terminal khác chiếm cổng.
- **Byte không đọc được:** ghi một lần reset mới ở 74880 baud cho nhật ký ROM; dùng baud esptool đã chọn cho truyền dữ liệu thực tế.
- **Vẫn ở chế độ tải:** tháo cầu GPIO0–mass và khởi động lại.
- **LED trạng thái sáng khi reset:** GPIO0 cũng điều khiển LED này; cầu khởi động nối mass có thể giải thích hiện tượng. Không dùng nó để kiểm tra reset.
- **Nút không hoạt động khi nối bộ nạp:** tháo UART; GPIO3 được dùng chung.
- **API hoạt động nhưng tải không:** trạng thái rơ-le báo về không chẩn đoán tiếp điểm, nguồn cuộn dây hay dây điện lưới. Không dùng que đo trên bo hở đang mang điện lưới.
