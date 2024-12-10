#include "utils.hpp"

#include <fmt/color.h>

#include <cmath>
#include <stdexcept>

// Random
std::mt19937& getRandom() {
  static auto rd = std::random_device();
  static auto gen = std::mt19937(rd());
  return gen;
}

// Distance functions
struct PolarPoint {
  double r;
  double t;
};

double euclideanDistanceSquared(const Point& p1, const Point& p2) {
  auto dx = p1.x - p2.x;
  auto dy = p1.y - p2.y;
  return (dx * dx) + (dy * dy);
}

double manhattanDistanceSquared(const Point& p1, const Point& p2) {
  auto distance = std::abs(p1.x - p2.x) + std::abs(p1.y - p2.y);
  return distance * distance;
}

static PolarPoint toPolar(const Point& p) {
  return {.r = std::sqrt((p.x * p.x) + (p.y * p.y)), .t = std::atan2(p.y, p.x)};
}

double polarDistanceSquared(const Point& p1, const Point& p2) {
  auto pp1 = toPolar(p1);
  auto pp2 = toPolar(p2);

  return (pp1.r * pp1.r) + (pp2.r * pp2.r) -
         (2 * pp1.r * pp2.r * std::cos(pp1.t - pp2.t));
}

std::function<double(Point p1, Point p2)> getFuncFromEnum(FuncType funcType) {
  switch (funcType) {
    case FuncType::Euclid:
      return &euclideanDistanceSquared;
    case FuncType::Manhattan:
      return &manhattanDistanceSquared;
    case FuncType::Polar:
      return &polarDistanceSquared;
  }
  throw std::runtime_error("unknown distance function enum was given");
}

// Logging
void logInfo(const std::string& msg) {
  fmt::print("{}{}\n", fmt::format(fmt::fg(fmt::color::green), "INFO: "), msg);
}
