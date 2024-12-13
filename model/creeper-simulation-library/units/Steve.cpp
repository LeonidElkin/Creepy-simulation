#include "Steve.hpp"

void Steve::updateState(const Unit &another) {}

void Steve::walk() {}

StevesParams::StevesParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams, uint32_t unitsCount)
    : UnitsParams(moveRadius, fieldParams, unitsCount) {}
