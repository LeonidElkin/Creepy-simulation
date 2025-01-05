#include "Creeper.hpp"

#include <random>

#include "utils.hpp"

constexpr auto sleep_probability = 0.1;

Creeper::Creeper(const size_t id, const std::shared_ptr<CreepersParams> &params) : Unit(id, params), params_(params) {}

void Creeper::walk() {
  static auto dist_sleep = std::bernoulli_distribution(sleep_probability);
  switch (state_) {
    case CreepersParams::State::Explodes:
      state_ = CreepersParams::State::Born;
      setCoord(params_->generatePos({}));
      break;
    case CreepersParams::State::Sleep:
      if (dist_sleep(getRandom())) {
        state_ = CreepersParams::State::Walk;
        break;
      }
      break;
    case CreepersParams::State::Walk:
      if (dist_sleep(getRandom())) {
        state_ = CreepersParams::State::Sleep;
        break;
      }
    default:
      state_ = CreepersParams::State::Walk;
      setCoord(params_->generatePos(getCoord()));
  }
}

void Creeper::updateState(const Unit &another) {
  if (&another == this) return;

  if (state_ == CreepersParams::State::Born) {
    return;
  }

  if (state_ == CreepersParams::State::Explodes) {
    return;
  }

  const auto distance = params_->getDistanceFunc()(getCoord(), another.getCoord());
  if (distance <= params_->explodeRadiusSquare) {
    state_ = CreepersParams::State::Explodes;
    return;
  }

  if (state_ == CreepersParams::State::Hissing) return;

  auto distHissing = std::bernoulli_distribution(1. / (distance));

  if (distHissing(getRandom())) {
    state_ = CreepersParams::State::Hissing;
  } else if (state_ != CreepersParams::State::Sleep) {
    state_ = CreepersParams::State::Walk;
  }
}

CreepersParams::CreepersParams(double moveRadius, double explodeRadius, const std::shared_ptr<FieldParams> &fieldParams,
                               uint32_t unitsCount)
    : UnitsParams(moveRadius, fieldParams, unitsCount), explodeRadiusSquare(std::pow(explodeRadius, 2)) {}
