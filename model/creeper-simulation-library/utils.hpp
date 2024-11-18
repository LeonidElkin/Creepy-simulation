#ifndef CREEPY_SIMULATION_UTILS_HPP
#define CREEPY_SIMULATION_UTILS_HPP

#include <random>

struct Point {
  double x;
  double y;
};

std::mt19937& getRandom();

double euclideanDistance(Point p1, Point p2);

#endif  // CREEPY_SIMULATION_UTILS_HPP
