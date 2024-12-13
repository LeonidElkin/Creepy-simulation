#pragma once

#include "utils.hpp"

struct FieldParams {
  Point leftDownBound;
  Point rightUpBound;
  std::function<double(Point p1, Point p2)> distanceFunc;
};
