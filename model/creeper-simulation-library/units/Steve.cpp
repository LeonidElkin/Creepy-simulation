#include "Steve.hpp"

#include <glog/logging.h>

void Steve::walk() {
  DLOG_IF(WARNING, state_ == StevesParams::State::Dead) << "Dead Steve walking! Steve id: " << getID();
  setCoord(params_->getFieldParams()->checkIntersections(getCoord(), params_->generatePos(getCoord())));
}

void Steve::updateState(const std::shared_ptr<Unit> &another) {}

void Steve::die() { state_ = StevesParams::State::Dead; }

StevesParams::StevesParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams, uint32_t unitsCount)
    : UnitsParams(moveRadius, fieldParams, unitsCount) {}
