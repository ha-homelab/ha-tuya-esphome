#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <cstring>

namespace radio_pilot {

constexpr size_t HEADER_SIZE = 19;
constexpr size_t TAG_SIZE = 16;
constexpr size_t FRAME_SIZE = HEADER_SIZE + TAG_SIZE;
constexpr uint32_t LEASE_MS = 5000;
using Wire = std::array<uint8_t, FRAME_SIZE>;
using Tag = std::array<uint8_t, TAG_SIZE>;
enum class Kind : uint8_t { GET = 1, SNAPSHOT, SET, RESULT };

struct Frame {
  Kind kind;
  uint64_t request;
  uint64_t token;
  bool on;
};

inline uint64_t load_id(const uint8_t *data) {
  uint64_t id = 0;
  for (size_t i = 0; i < 8; ++i) id = (id << 8) | data[i];
  return id;
}

inline void store_id(uint8_t *data, uint64_t id) {
  for (size_t i = 8; i != 0; --i) {
    data[i - 1] = static_cast<uint8_t>(id);
    id >>= 8;
  }
}

// Auth must compute truncated HMAC-SHA256 using the per-endpoint secret.
template<typename Auth> bool encode(const Auth &auth, Frame frame, Wire &wire) {
  wire[0] = 1;
  wire[1] = static_cast<uint8_t>(frame.kind);
  store_id(wire.data() + 2, frame.request);
  store_id(wire.data() + 10, frame.token);
  wire[18] = frame.on;
  Tag tag{};
  if (!auth(wire.data(), tag)) return false;
  std::memcpy(wire.data() + HEADER_SIZE, tag.data(), tag.size());
  return true;
}

template<typename Auth> bool decode(const Auth &auth, const uint8_t *wire, size_t size, Frame &frame) {
  if (size != FRAME_SIZE || wire[0] != 1 || wire[1] < 1 || wire[1] > 4 || wire[18] > 1) return false;
  Tag tag{};
  if (!auth(wire, tag)) return false;
  volatile uint8_t difference = 0;
  for (size_t i = 0; i < tag.size(); ++i) {
    difference = static_cast<uint8_t>(difference | (tag[i] ^ wire[HEADER_SIZE + i]));
  }
  if (difference != 0) return false;
  frame = {static_cast<Kind>(wire[1]), load_id(wire + 2), load_id(wire + 10), wire[18] != 0};
  if (frame.request == 0) return false;
  return frame.kind == Kind::GET ? frame.token == 0 && !frame.on : frame.token != 0;
}

class Endpoint {
 public:
  // A local button or other authoritative writer must invalidate old leases.
  void local_state(bool on) {
    on_ = on;
    request_ = 0;
  }

  template<typename Auth, typename Random, typename Apply>
  bool exchange(const Auth &auth, Random random, Apply apply, uint64_t now,
                const uint8_t *data, size_t size, Wire &reply) {
    Frame frame{};
    if (!decode(auth, data, size, frame)) return false;
    if (request_ != 0 && (now - issued_at_) >= LEASE_MS) request_ = 0;
    if (frame.kind == Kind::GET) {
      if (frame.request == request_) {
        return encode(auth, {Kind::SNAPSHOT, request_, token_, initial_state_}, reply);
      }
      const auto fresh_token = random();
      if (fresh_token == 0) return false;
      token_ = fresh_token;
      request_ = frame.request;
      issued_at_ = now;
      initial_state_ = on_;
      committed_ = false;
      return encode(auth, {Kind::SNAPSHOT, request_, token_, initial_state_}, reply);
    }
    if (frame.kind != Kind::SET || frame.request != request_ || frame.token != token_) return false;
    if (!committed_) {
      on_ = apply(frame.on);
      desired_ = frame.on;
      committed_ = true;
    }
    if (frame.on != desired_) return false;
    return encode(auth, {Kind::RESULT, request_, token_, on_}, reply);
  }

 private:
  uint64_t request_{0};
  uint64_t token_{0};
  uint64_t issued_at_{0};
  bool initial_state_{false};
  bool committed_{false};
  bool desired_{false};
  bool on_{false};
};

}  // namespace radio_pilot
