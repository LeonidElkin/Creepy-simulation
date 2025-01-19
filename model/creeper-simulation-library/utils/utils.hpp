#pragma once

#include <functional>
#include <random>

struct Point {
  double x;
  double y;

  bool operator==(const Point& p2) const { return std::abs(x - p2.x) < 1e-9 && std::abs(y - p2.y) < 1e-9; }
};

struct Rectangle {
  Point leftDownBound;
  Point rightUpBound;

  Rectangle(Point leftDownBound, Point rightUpBound) : leftDownBound(leftDownBound), rightUpBound(rightUpBound) {}

  bool operator==(const Rectangle& r2) const {
    return leftDownBound == r2.leftDownBound && rightUpBound == r2.rightUpBound;
  }
};

std::mt19937& getRandom();

namespace DistanceFunc {
enum class Type : std::uint8_t { Euclid, Polar, Manhattan };
double euclideanSquared(const Point& p1, const Point& p2);
double polarSquared(const Point& p1, const Point& p2);
double manhattanSquared(const Point& p1, const Point& p2);
std::function<double(Point p1, Point p2)> funcToType(Type funcType);
}  // namespace DistanceFunc
