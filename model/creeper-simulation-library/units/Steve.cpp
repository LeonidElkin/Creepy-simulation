#include "Steve.hpp"

#include <glog/logging.h>

void Steve::walk() {
  if (state_ == StevesParams::State::Dead) {
    return;
  }
  const auto newCoord = params_->generatePos(getCoord());
  setCoord(params_->getFieldParams()->checkIntersections(getCoord(), newCoord).value_or(newCoord));
}

void Steve::updateState(const std::shared_ptr<Unit> &another) {}

void Steve::die() { state_ = StevesParams::State::Dead; }

StevesParams::StevesParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams, uint32_t unitsCount)
    : UnitsParams(moveRadius, fieldParams, unitsCount) {}
