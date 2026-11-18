#pragma once

#include "hex.h"
#include "protocol.h"
#include <esp_random.h>
#include <esp_timer.h>
#include <mbedtls/md.h>

namespace radio_pilot {

class EspAuth {
 public:
  explicit EspAuth(const char *key_hex) : valid_(from_hex(key_hex, key_.data(), key_.size())) {
    // The public compile fixture must never authorize real traffic.
    bool build_key = true;
    bool all_zero = true;
    for (size_t i = 0; i < key_.size(); ++i) {
      build_key &= key_[i] == i;
      all_zero &= key_[i] == 0;
    }
    valid_ = valid_ && !build_key && !all_zero;
  }

  bool operator()(const uint8_t *data, Tag &tag) const {
    if (!valid_) return false;
    std::array<uint8_t, 32> digest{};
    const auto *sha256 = mbedtls_md_info_from_type(MBEDTLS_MD_SHA256);
    if (!sha256 || mbedtls_md_hmac(sha256, key_.data(), key_.size(), data, HEADER_SIZE, digest.data()) != 0) {
      return false;
    }
    std::memcpy(tag.data(), digest.data(), tag.size());
    return true;
  }

 private:
  std::array<uint8_t, 32> key_{};
  bool valid_;
};

inline uint64_t random_token() {
  uint64_t value = 0;
  esp_fill_random(&value, sizeof(value));
  return value;
}

}  // namespace radio_pilot
