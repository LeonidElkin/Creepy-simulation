#include "Steve.hpp"

void Steve::updateState(const Unit &another, const std::function<double(Point, Point)> &distanceFun) {}

void Steve::walk() {}

StevesParams::StevesParams(const double moveRadius, const std::shared_ptr<FieldParams> &fieldParams)
    : UnitsParams(moveRadius, fieldParams) {}
