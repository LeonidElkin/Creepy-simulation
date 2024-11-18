#ifndef CREEPY_SIMULATION_UTILS_HPP
#define CREEPY_SIMULATION_UTILS_HPP

#include <random>

struct Point {
  double x;
  double y;
};

enum class FuncType : std::uint8_t { Euclid, Polar, Manhattan };

std::mt19937& getRandom();

double euclideanDistance(Point p1, Point p2);
double polarDistance(Point p1, Point p2);
double manhattanDistance(Point p1, Point p2);
std::function<double(Point p1, Point p2)> getFuncFromEnum(FuncType funcType);

#endif  // CREEPY_SIMULATION_UTILS_HPP
