#pragma once
#include <cmath>
#include <cstdint>

struct EnergyTotals {
  double total_kwh;
  double today_kwh;
  double yesterday_kwh;
  int32_t local_day;
};

inline void update_energy_day(EnergyTotals &s, int32_t day) {
  if (day <= s.local_day) return;
  s.yesterday_kwh = day == s.local_day + 1 ? s.today_kwh : 0.0;
  s.today_kwh = 0.0;
  s.local_day = day;
}

inline void add_energy_sample(EnergyTotals &s, double cumulative_wh, double &previous_wh) {
  if (!std::isfinite(cumulative_wh) || cumulative_wh < 0.0) return;
  double delta_wh = cumulative_wh >= previous_wh ? cumulative_wh - previous_wh : cumulative_wh;
  previous_wh = cumulative_wh;
  s.total_kwh += delta_wh / 1000.0;
  s.today_kwh += delta_wh / 1000.0;
}
