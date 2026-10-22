# SWP1-PW2-V5 / TYWE3S: 검증된 직렬 변환

<!-- language-navigation:start -->
<p dir="ltr">
<a href="swp1-pw2-v5.md" lang="en" dir="ltr">English</a> · <a href="swp1-pw2-v5.ar.md" lang="ar" dir="rtl">العربية</a> · <a href="swp1-pw2-v5.bn.md" lang="bn" dir="ltr">বাংলা</a> · <a href="swp1-pw2-v5.cs.md" lang="cs" dir="ltr">Čeština</a> · <a href="swp1-pw2-v5.de.md" lang="de" dir="ltr">Deutsch</a> · <a href="swp1-pw2-v5.es.md" lang="es" dir="ltr">Español</a> · <a href="swp1-pw2-v5.fa.md" lang="fa" dir="rtl">فارسی</a> · <a href="swp1-pw2-v5.fr.md" lang="fr" dir="ltr">Français</a><br>
<a href="swp1-pw2-v5.he.md" lang="he" dir="rtl">עברית</a> · <a href="swp1-pw2-v5.hi.md" lang="hi" dir="ltr">हिन्दी</a> · <a href="swp1-pw2-v5.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> · <a href="swp1-pw2-v5.it.md" lang="it" dir="ltr">Italiano</a> · <a href="swp1-pw2-v5.ja.md" lang="ja" dir="ltr">日本語</a> · <a href="swp1-pw2-v5.ko.md" lang="ko" dir="ltr">한국어</a> · <a href="swp1-pw2-v5.nl.md" lang="nl" dir="ltr">Nederlands</a> · <a href="swp1-pw2-v5.pl.md" lang="pl" dir="ltr">Polski</a><br>
<a href="swp1-pw2-v5.pt.md" lang="pt" dir="ltr">Português</a> · <a href="swp1-pw2-v5.ru.md" lang="ru" dir="ltr">Русский</a> · <a href="swp1-pw2-v5.th.md" lang="th" dir="ltr">ไทย</a> · <a href="swp1-pw2-v5.tr.md" lang="tr" dir="ltr">Türkçe</a> · <a href="swp1-pw2-v5.uk.md" lang="uk" dir="ltr">Українська</a> · <a href="swp1-pw2-v5.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> · <a href="swp1-pw2-v5.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> · <a href="swp1-pw2-v5.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

일반 Tuya-Convert가 PSK 식별자 `02`로 실패한 뒤 2026-10-18에 SWP1-PW2-V5 한 대를 변환했습니다. 유선 탐색으로 ESP8266EX, 26 MHz 크리스털, 2 MiB 플래시를 확인했습니다. 검증한 공장 백업에서 GPIO 배치를 얻은 후 최종 펌웨어를 기록했습니다. 소유자는 이후 책장 콘센트로 정상 작동함을 확인했습니다.

이 증거는 해당 개체에만 적용되며 외형이 비슷한 모든 제품을 보장하지 않습니다. 하드웨어 비교에 쓴 오래된 불탄 스위치는 다른 장치였고, 그 Home Assistant 식별 정보와 LocalTuya 설정은 유지했습니다.

## 확인한 하드웨어

- 릴레이: **GPIO13, High 활성**, 복원 모드 `ALWAYS_OFF`.
- 물리 버튼: **GPIO3 / RXD0, Low 활성**, 풀업 및 30 ms 디바운스.
- 릴레이 표시등: **GPIO14, Low 활성**, 릴레이에 명령한 상태를 따름.
- 연결 표시등: **GPIO0, Low 활성**.
- 직렬 로그: 비활성. 버튼 입력이 RXD0를 공유하므로 버튼 시험 전에 프로그래머의 UART 선을 분리합니다.

공장 애플리케이션의 하드웨어 JSON이 이 배치를 식별했고 이후 버튼, 릴레이, 표시등 관찰과 일치했습니다. GPIO 출력을 순차 탐색하거나 중립 진단 펌웨어를 쓸 필요가 없었습니다. 이 프로필은 전기 계측을 설정하지 않습니다. LED나 API 상태는 릴레이 접점의 피드백이 아닙니다.

## 저전압 배선

**열거나 무엇이든 연결하기 전에 상용 전원에서 완전히 분리하십시오. 프로그래밍 내내 분리 상태를 유지하십시오.** 정전압 3.3 V 공급원과 검증한 3.3 V UART 논리를 사용합니다. 레벨 변환기는 신호를 변환할 뿐, 대상에 정전압 전원을 공급하지 않습니다.

![기능별 직렬 배선: 외부 3.3 V 전원, 5 V UART 어댑터, 레벨 변환기, TYWE3S](images/swp1-serial-wiring.svg)

그림은 전기 연결이며 **실제 패드 위치가 아닙니다**. [Tuya TYWE3S 데이터시트](https://developer.tuya.com/en/docs/iot/wifie3smodule?id=K9605ua1cx9tv)로 모듈 핀을 식별하고 그림 방향을 보드와 대조합니다. 캐리어 보드 테스트 패드의 기능을 위치만으로 추측하지 마십시오. 문서의 공칭 전압은 3.3 V입니다.

여기서 쓴 5 V 논리 어댑터의 배선:

1. 어댑터 **5V → 변환기 HV 기준**.
2. 외부 정전압 **3.3V → 모듈 VCC 및 변환기 LV**.
3. 어댑터 GND, 변환기 GND, 전원 음극, 모듈 GND를 공통 접지합니다.
4. 어댑터 **TX → HV1**, 대응하는 **LV1 → 모듈 RXD0**.
5. 모듈 **TXD0 → LV2**, 대응하는 **HV2 → 어댑터 RX**.
6. 어댑터의 3V3 출력은 연결하지 않습니다. 두 전원 출력을 병렬 연결하지 마십시오.

UART 속도와 방향에 맞는 변환기를 사용합니다. 이 구성은 배선 수정 후 115200 baud에서 동작했지만 모든 저가 HV/LV 보드의 적합성을 보장하지 않습니다. 실제 3.3 V UART 어댑터는 출력 레벨 확인 후 변환기를 생략할 수 있습니다.

어댑터는 무부하에서 3.3 V였지만 연결된 대상에는 **1.9 V**만 공급했습니다. TX도 **5.1 V**였습니다. 별개의 문제로, 외부 전원이 VCC를 해결하고 변환기가 UART 레벨을 맞췄습니다. 부하가 연결된 모듈에서 VCC를 측정하고 같은 접지 기준으로 신호를 측정하십시오. [ESPHome 물리 연결 가이드](https://esphome.io/guides/physical_device_connection/)를 참조하십시오.

## 다운로드 모드, 백업, 펌웨어

전원을 끈 상태에서 **GPIO0를 GND에 연결**합니다. 저전압 전원을 다시 공급한 후 **RST를 잠깐 GND에 연결했다가 해제**합니다. EN은 High로 유지하고 RST를 Low로 계속 잡지 마십시오. 기록 중 GPIO0를 접지해도 되지만 정상 부팅 전 점퍼를 제거합니다. 읽을 수 있는 ROM 메시지 `boot mode:(1,0)`가 다운로드 모드를 확인했습니다. [Espressif 부팅 모드 문서](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html)를 참조하십시오.

직렬 포트는 한 프로그램만 점유할 수 있습니다. esptool 전에 Miniterm을 종료하십시오. TX/RX를 올바르게 교차 연결하여 마지막 통신 오류를 해결했습니다. LED가 켜진 것만으로 직렬 연결이 정상임을 증명하지는 않습니다.

기록 전 작업자는 공장 플래시의 **전체 2,097,152바이트**를 읽고 esptool로 백업을 장치와 대조 검증했습니다. 백업, 원시 직렬 로그, 빌드 이미지, 인증 정보는 공개 Git 밖에 보관하십시오. 공장 덤프에는 프로비저닝 비밀이 있을 수 있습니다. [esptool 명령 참조](https://docs.espressif.com/projects/esptool/en/latest/esp8266/esptool/basic-commands.html)는 식별, `read-flash`, `verify-flash`, `write-flash`를 설명합니다. 읽기 크기는 케이스 이름이 아니라 실제 플래시 탐색 결과로 정하십시오.

새 비공개 디렉터리에서 [독립 프로필](../examples/swp1-pw2-v5.yaml)을 빌드합니다. 저장소 루트에서 다음 명령을 실행하며 이 프로필만 복사하고, 일반 기본 설정이나 XS-SSA01 패키지는 복사하지 않습니다.

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

도우미는 Wi-Fi 인증 정보를 묻고 서로 다른 키를 생성하며 기존 비밀의 덮어쓰기를 거부합니다. 명령은 컴파일만 하고 플래시에 기록하지 않습니다. [암호화 프로비저닝 안내](security-profile.md)를 참조하십시오. 이 개체는 **ESPHome 2026.9.1**, `esp_wroom_02`, **2 MiB, DOUT, 40 MHz**를 사용했습니다. 설치 이미지는 **429,600바이트**였으며 115200 baud로 `0x0`에 기록했고 esptool이 기록된 해시를 확인했습니다. 재빌드 크기는 달라질 수 있습니다. 바이트 수는 관찰값이지 설치 조건이 아닙니다.

## 정상 부팅 및 인수 확인

전원을 끄고 GPIO0–GND와 UART 신호선 두 개를 제거한 뒤 외부 3.3 V만 다시 공급합니다. 암호화된 네이티브 API가 연결되었고 ON/OFF 명령이 동작했으며 ON에서 소프트 재시작하면 OFF로 복원되었습니다. 소유자는 두 번의 버튼 누름에서 릴레이 소리와 표시등의 동기 동작을 확인했습니다.

이후 임시 배선과 외부 전원을 모두 제거하고 케이스를 조립한 다음 정상 설치했습니다. 소유자는 설치한 콘센트의 작동을 확인했습니다. **ON 상태에서 통제된 상용 전원 차단·복귀 시험, 접점 전압 측정, 부팅 과도현상 측정은 수행하지 않았습니다.** 작업대에서 나는 클릭 소리만으로 부하 전환을 입증할 수는 없습니다.

Home Assistant에는 릴레이 하나와 연결, 신호, 버전, 재시작 진단이 추가되었습니다. 재기록 없이 HA에서 설치 용도 이름을 바꿨으며 원래 펌웨어 호스트 이름은 유효합니다. 전체 비공개 소스를 HA의 ESPHome 폴더와 ESPHome Dashboard 양쪽에 저장했습니다. 릴레이는 두 번째 대시보드 페이지의 Living Room 구역에 한 번만 추가했습니다. 향후 저장소 배포는 이 레지스트리 식별 정보를 유지하거나 명시적으로 이전해야 합니다.

## 단계가 실패하는 경우

- **직렬 응답 없음:** 부하 시 VCC, 공통 접지, 어댑터 TX → 모듈 RX, 모듈 TX → 어댑터 RX, 다른 터미널의 포트 점유 여부를 확인합니다.
- **읽을 수 없는 바이트:** 새 리셋의 ROM 로그를 74880 baud로 캡처하고 실제 전송에는 선택한 esptool 속도를 사용합니다.
- **다운로드 모드가 계속됨:** GPIO0–접지 점퍼를 제거하고 재시작합니다.
- **리셋 중 상태 LED 켜짐:** GPIO0는 해당 LED도 구동하므로 접지된 부팅 점퍼 때문일 수 있습니다. 리셋 시험으로 사용하지 마십시오.
- **프로그래머 연결 중 버튼 불능:** UART를 분리합니다. GPIO3는 공유됩니다.
- **API는 정상이나 부하 불능:** 보고된 릴레이 상태로 접점, 코일 전원, 상용 전원 배선을 진단할 수 없습니다. 상용 전원에 연결된 노출 보드를 프로브로 측정하지 마십시오.
