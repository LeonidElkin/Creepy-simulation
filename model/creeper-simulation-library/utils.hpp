#ifndef CREEPY_SIMULATION_UTILS_HPP
#define CREEPY_SIMULATION_UTILS_HPP

#include <random>

struct Point {
  double x;
  double y;
};

std::mt19937& getRandom();

#endif  // CREEPY_SIMULATION_UTILS_HPP
