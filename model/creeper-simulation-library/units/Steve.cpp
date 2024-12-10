#include "Steve.hpp"
void Steve::updateState(
    const Unit& another,
    const std::function<double(Point, Point)>& distanceFun) {}

void Steve::walk() {}

Point SteveParams::generatePos(std::optional<Point> initialPoint) {
  return Point();
}

SteveParams::SteveParams(double moveRadius, const Point& leftDownBound,
                         const Point& rightUpBound)
    : UnitParams(moveRadius, leftDownBound, rightUpBound) {}
