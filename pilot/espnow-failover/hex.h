#pragma once

#include <cstddef>
#include <cstdint>
#include <string>

namespace radio_pilot {

inline int nibble(char value) {
  if (value >= '0' && value <= '9') return value - '0';
  if (value >= 'a' && value <= 'f') return value - 'a' + 10;
  if (value >= 'A' && value <= 'F') return value - 'A' + 10;
  return -1;
}

inline bool from_hex(const std::string &input, uint8_t *output, size_t size) {
  if (input.size() != size * 2) return false;
  for (size_t i = 0; i < size; ++i) {
    const auto high = nibble(input[2 * i]);
    const auto low = nibble(input[2 * i + 1]);
    if (high < 0 || low < 0) return false;
    output[i] = static_cast<uint8_t>((high << 4) | low);
  }
  return true;
}

inline bool from_mac(const std::string &input, uint8_t (&output)[6]) {
  if (input.size() != 17) return false;
  std::string compact;
  compact.reserve(12);
  for (size_t i = 0; i < input.size(); ++i) {
    if (i % 3 != 2) compact += input[i];
    else if (input[i] != ':') return false;
  }
  return from_hex(compact, output, sizeof(output));
}

inline std::string to_hex(const uint8_t *input, size_t size) {
  const char alphabet[] = "0123456789abcdef";
  std::string output(size * 2, '0');
  for (size_t i = 0; i < size; ++i) {
    output[2 * i] = alphabet[input[i] >> 4];
    output[2 * i + 1] = alphabet[input[i] & 15];
  }
  return output;
}

}  // namespace radio_pilot
