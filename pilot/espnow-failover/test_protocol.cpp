#include "hex.h"
#include "protocol.h"

#include <cassert>
#include <openssl/hmac.h>

using namespace radio_pilot;

bool authenticate(const uint8_t *data, Tag &tag) {
  std::array<uint8_t, 32> key{}, digest{};
  for (size_t i = 0; i < key.size(); ++i) key[i] = static_cast<uint8_t>(i);
  unsigned int size = 0;
  if (!HMAC(EVP_sha256(), key.data(), key.size(), data, HEADER_SIZE, digest.data(), &size)) return false;
  if (size != digest.size()) return false;
  std::memcpy(tag.data(), digest.data(), tag.size());
  return true;
}

int main() {
  Wire request{}, response{};
  const uint64_t sample_id = 0x0102030405060708, sample_token = 0x1112131415161718;
  assert(encode(authenticate, {Kind::SET, sample_id, sample_token, true}, request));
  // Independent Python controller vector checks endianness and HMAC framing.
  assert(to_hex(request.data(), request.size()) ==
         "010301020304050607081112131415161718012469e6ce27de476370189587d7f02a45");
  uint8_t mac[6];
  assert(from_mac("02:00:00:00:00:01", mac) && mac[0] == 2 && mac[5] == 1);
  assert(!from_mac("02.00:00:00:00:aF", mac));
  assert(!from_mac("02:00:00:00:00:zz", mac));

  Endpoint endpoint;
  uint64_t issued = sample_token - 1;
  const auto random = [&issued]() { return ++issued; };
  int transitions = 0;
  const auto apply = [&transitions](bool state) { ++transitions; return state; };
  const auto exchange = [&](Frame input, uint64_t now) {
    assert(encode(authenticate, input, request));
    return endpoint.exchange(authenticate, random, apply, now, request.data(), request.size(), response);
  };
  const auto read_response = [&]() {
    Frame frame{};
    assert(decode(authenticate, response.data(), response.size(), frame));
    return frame;
  };
  const Frame on{Kind::SET, sample_id, sample_token, true};
  const Frame get{Kind::GET, sample_id, 0, false};
  assert(!exchange(on, 0));
  assert(exchange(get, 1));
  const auto snapshot = read_response();
  assert(snapshot.kind == Kind::SNAPSHOT && snapshot.token == sample_token && !snapshot.on);
  assert(exchange(get, 2) && read_response().token == sample_token);
  request.back() ^= 1;
  assert(!endpoint.exchange(authenticate, random, apply, 3, request.data(), request.size(), response));
  assert(!endpoint.exchange(authenticate, random, apply, 3, request.data(), 18, response));
  assert(exchange(on, 4));
  assert(read_response().kind == Kind::RESULT && read_response().on);
  const auto first_ack = response;
  assert(exchange(on, 5) && response == first_ack && transitions == 1);
  assert(!exchange({Kind::SET, sample_id, sample_token, false}, 6) && transitions == 1);
  endpoint.local_state(false);
  assert(!exchange(on, 7));
  assert(exchange(get, 8) && read_response().token != sample_token && !read_response().on);
  auto newer = read_response();
  assert(!exchange({Kind::SET, newer.request, newer.token, true}, 8 + LEASE_MS));
  assert(transitions == 1);
  assert(exchange({Kind::GET, sample_id + 1, 0, false}, 10000));
  const auto failed = read_response();
  const auto no_readback = [](bool) { return false; };
  assert(encode(authenticate, {Kind::SET, failed.request, failed.token, true}, request));
  assert(endpoint.exchange(authenticate, random, no_readback, 10001, request.data(), request.size(), response));
  assert(read_response().kind == Kind::RESULT && !read_response().on);
}
