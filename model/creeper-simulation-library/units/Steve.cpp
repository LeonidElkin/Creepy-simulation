#include "Steve.hpp"

#include <glog/logging.h>

void Steve::walk() {
  if (state_ == StevesParams::State::Dead) {
    return;
  }
  setCoord(params_->generatePos(getCoord()));
}

void Steve::updateState(const std::shared_ptr<Unit> &another) {}

void Steve::die() { state_ = StevesParams::State::Dead; }

StevesParams::StevesParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams, uint32_t unitsCount)
    : UnitsParams(moveRadius, fieldParams, unitsCount) {}
