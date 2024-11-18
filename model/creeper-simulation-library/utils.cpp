#include "utils.hpp"

#include <cmath>

struct PolarPoint {
  double r;
  double t;
};

std::mt19937& getRandom() {
  static auto rd = std::random_device();
  static auto gen = std::mt19937(rd());
  return gen;
}

double euclideanDistance(Point p1, Point p2) {
  return std::sqrt(std::pow(p1.x - p2.x, 2) + std::pow(p1.y - p2.y, 2));
}

double manhattanDistance(Point p1, Point p2) {
  return std::abs(p1.x - p2.x) + std::abs(p1.y - p2.y);
}

static PolarPoint toPolar(Point p) {
  return {.r = std::sqrt((p.x * p.x) + (p.y * p.y)), .t = std::atan2(p.y, p.x)};
}

double polarDistance(Point p1, Point p2) {
  auto pp1 = toPolar(p1);
  auto pp2 = toPolar(p2);

  return std::sqrt((pp1.r * pp1.r) + (pp2.r * pp2.r) -
                   (2 * pp1.r * pp2.r * std::cos(pp1.t - pp2.t)));
}

auto getFuncFromEnum(FuncType funcType) {
  switch (funcType) {
    case FuncType::Euclid:
      return &euclideanDistance;
    case FuncType::Manhattan:
      return &manhattanDistance;
    case FuncType::Polar:
      return &polarDistance;
  }
}