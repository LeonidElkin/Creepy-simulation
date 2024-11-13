#ifndef CREEPY_SIMULATION_UTILS_HPP
#define CREEPY_SIMULATION_UTILS_HPP

#include <random>

struct Point {
  double x;
  double y;
};

auto &getRandom() {
  static auto rd = std::random_device();
  static auto gen = std::mt19937(rd());
  return gen;
}

#endif  // CREEPY_SIMULATION_UTILS_HPP
