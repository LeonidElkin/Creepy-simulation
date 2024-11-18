#include "utils.hpp"

#include <cmath>

std::mt19937& getRandom() {
  static auto rd = std::random_device();
  static auto gen = std::mt19937(rd());
  return gen;
}

double euclideanDistance(Point p1, Point p2) {
  return std::sqrt(std::pow(p1.x - p2.x, 2) + std::pow(p1.y - p2.y, 2));
}
