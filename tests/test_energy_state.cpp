#include "energy_state.h"
#include <cassert>
#include <limits>

int main() {
  // Synthetic migrated counters: no operational readings belong in this test.
  EnergyTotals state{123.450, 0.010, 0.002, 100};
  double previous = 0.0;
  add_energy_sample(state, 1.0, previous);
  assert(std::abs(state.total_kwh - 123.451) < 1e-8);
  assert(std::abs(state.today_kwh - 0.011) < 1e-8);

  // Duplicates and invalid readings cannot change totals or the raw baseline.
  add_energy_sample(state, 1.0, previous);
  add_energy_sample(state, NAN, previous);
  add_energy_sample(state, -1.0, previous);
  add_energy_sample(state, std::numeric_limits<double>::infinity(), previous);
  assert(std::abs(state.total_kwh - 123.451) < 1e-8);
  assert(previous == 1.0);

  update_energy_day(state, 101);
  assert(std::abs(state.yesterday_kwh - 0.011) < 1e-8);
  assert(state.today_kwh == 0.0);
  add_energy_sample(state, 2.0, previous);
  assert(std::abs(state.today_kwh - 0.001) < 1e-8);

  // Backward clock corrections cannot repeat a daily rollover.
  update_energy_day(state, 100);
  assert(state.local_day == 101);
  update_energy_day(state, 103);
  assert(state.yesterday_kwh == 0.0 && state.today_kwh == 0.0);

  // Firmware restart resets its raw counter, but keeps migrated totals.
  previous = 0.0;
  add_energy_sample(state, 1.0, previous);
  assert(std::abs(state.total_kwh - 123.453) < 1e-8);

  // A raw counter reset must not subtract previously accumulated energy.
  EnergyTotals reset{7.0, 0.5, 0.25, 103};
  previous = 10.0;
  add_energy_sample(reset, 2.0, previous);
  assert(std::abs(reset.total_kwh - 7.002) < 1e-8);
  assert(std::abs(reset.today_kwh - 0.502) < 1e-8);
  assert(previous == 2.0);
}
