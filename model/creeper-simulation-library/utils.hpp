#ifndef CREEPY_SIMULATION_UTILS_HPP
#define CREEPY_SIMULATION_UTILS_HPP

#include <functional>
#include <random>

struct Point {
  double x;
  double y;
};

enum class FuncType : std::uint8_t { Euclid, Polar, Manhattan };

std::mt19937& getRandom();

double euclideanDistanceSquared(const Point& p1, const Point& p2);
double polarDistanceSquared(const Point& p1, const Point& p2);
double manhattanDistanceSquared(const Point& p1, const Point& p2);
std::function<double(Point p1, Point p2)> getFuncFromEnum(FuncType funcType);

#endif  // CREEPY_SIMULATION_UTILS_HPP
