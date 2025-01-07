#pragma once

#include <functional>
#include <random>

struct Point {
  double x;
  double y;
};

std::mt19937& getRandom();

namespace DistanceFunc {
enum class Type : std::uint8_t { Euclid, Polar, Manhattan };
double euclideanSquared(const Point& p1, const Point& p2);
double polarSquared(const Point& p1, const Point& p2);
double manhattanSquared(const Point& p1, const Point& p2);
std::function<double(Point p1, Point p2)> funcToType(Type funcType);
}  // namespace DistanceFunc
