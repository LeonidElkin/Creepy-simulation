#include "Unit.hpp"

Unit::Unit(size_t id, const std::shared_ptr<UnitParams>& params)
    : id_(id), coord_(params->generatePos({})) {}

UnitParams::UnitParams(double moveRadius, const Point &leftDownBound,
                       const Point &rightUpBound)
    : moveRadius(moveRadius),
      leftDownBound_(leftDownBound),
      rightUpBound_(rightUpBound) {}
