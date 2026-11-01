#include "energy_state.h"
#include <fuzzer/FuzzedDataProvider.h>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <cstring>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  FuzzedDataProvider input(data, size);
  EnergyTotals state{0.0, 0.0, 0.0, 0};
  double previous = 0.0;
  // At most 512 samples: even DBL_MAX / 1000 per reset cannot overflow totals.
  for (unsigned step = 0; step < 512 && input.remaining_bytes(); ++step) {
    const EnergyTotals before = state;
    if (input.ConsumeBool()) {
      const auto day = input.ConsumeIntegral<int32_t>();
      update_energy_day(state, day);
      assert(state.total_kwh == before.total_kwh);
      if (day <= before.local_day) {
        assert(state.local_day == before.local_day && state.today_kwh == before.today_kwh &&
               state.yesterday_kwh == before.yesterday_kwh);
      } else {
        assert(state.local_day == day && state.today_kwh == 0.0);
        const int64_t distance = static_cast<int64_t>(day) - before.local_day;
        assert(state.yesterday_kwh == (distance == 1 ? before.today_kwh : 0.0));
      }
    } else {
      const uint64_t bits = input.ConsumeIntegral<uint64_t>();
      double sample;
      std::memcpy(&sample, &bits, sizeof(sample));
      const double old_previous = previous;
      add_energy_sample(state, sample, previous);
      if (!std::isfinite(sample) || sample < 0.0) {
        assert(previous == old_previous && state.total_kwh == before.total_kwh &&
               state.today_kwh == before.today_kwh);
      } else {
        assert(previous == sample && state.total_kwh >= before.total_kwh &&
               state.today_kwh >= before.today_kwh);
        const EnergyTotals once = state;
        add_energy_sample(state, sample, previous);
        assert(state.total_kwh == once.total_kwh && state.today_kwh == once.today_kwh);
      }
      assert(state.local_day == before.local_day && state.yesterday_kwh == before.yesterday_kwh);
    }
    assert(std::isfinite(state.total_kwh) && std::isfinite(state.today_kwh) &&
           std::isfinite(state.yesterday_kwh));
  }
  return 0;
}
