#include "Creeper.hpp"

#include <glog/logging.h>

#include <random>

#include "utils.hpp"

constexpr auto sleep_probability = 0.1;
constexpr auto wake_up_probability = 0.1;

Creeper::Creeper(const size_t id, const std::shared_ptr<CreepersParams> &params) : Unit(id, params), params_(params) {}

void Creeper::begin() {
  switch (state_) {
    case CreepersParams::State::Explodes:
    case CreepersParams::State::Dead:
      state_ = CreepersParams::State::Born;
      break;
    case CreepersParams::State::GoToSteve:
      if (target_ && target_->getState() != StevesParams::State::Die) {
        target_ = nullptr;
        state_ = CreepersParams::State::Walk;
      }
      break;
    case CreepersParams::State::Born:
      state_ = CreepersParams::State::Walk;
    default:
      break;
  }
}

void Creeper::steveSearch(const std::shared_ptr<Steve> &steve) {
  if (state_ == CreepersParams::State::Born) {
    return;
  }
  const auto distance = params_->getDistanceFunc()(getCoord(), steve->getCoord());
  auto distSteve = std::bernoulli_distribution(std::min(3. / distance, 1.));
  if (distSteve(getRandom())) {
    target_ = steve;
    state_ = CreepersParams::State::GoToSteve;
  }
}

Point Creeper::moveTo(const Point to) const {
  const auto t = params_->getMoveRadius() / std::sqrt(params_->getDistanceFunc()(getCoord(), to));
  return {getCoord().x + (t * getCoord().x), getCoord().y + t * getCoord().y};
}

void Creeper::walk() {
  static auto dist_sleep = std::bernoulli_distribution(sleep_probability);
  static auto dist_wake_up = std::bernoulli_distribution(wake_up_probability);
  switch (state_) {
    case CreepersParams::State::GoToSteve:
      setCoord(moveTo(getCoord()));
      break;
    case CreepersParams::State::Born:
      setCoord(params_->generatePos({}));
      break;
    case CreepersParams::State::Sleep:
      if (dist_wake_up(getRandom())) {
        state_ = CreepersParams::State::Walk;
      }
      break;
    case CreepersParams::State::Walk:
      if (dist_sleep(getRandom())) {
        state_ = CreepersParams::State::Sleep;
        break;
      }
      setCoord(params_->generatePos(getCoord()));
      break;
    default:
      DLOG(WARNING) << "Invalid creeper state when walking: " << static_cast<int>(state_);
  }
}

void Creeper::die() {
  switch (state_) {
    case CreepersParams::State::Explodes:
      break;
    default:
      state_ = CreepersParams::State::Dead;
  }
}

void Creeper::updateState(const std::shared_ptr<Unit> &another) {
  if (another.get() == this) return;

  const auto distance = params_->getDistanceFunc()(getCoord(), another->getCoord());
  if (distance <= params_->explodeRadiusSquare) {
    state_ = CreepersParams::State::Explodes;
    another->die();
    return;
  }

  switch (state_) {
    case CreepersParams::State::Hissing:
    case CreepersParams::State::GoToSteve:
    case CreepersParams::State::Dead:
      return;
    default:
      break;
  }

  auto distHissing = std::bernoulli_distribution(std::min(1. / (distance), 1.));

  if (distHissing(getRandom())) {
    state_ = CreepersParams::State::Hissing;
  } else if (state_ != CreepersParams::State::Sleep) {
    state_ = CreepersParams::State::Walk;
  }
}

CreepersParams::CreepersParams(double moveRadius, double explodeRadius, const std::shared_ptr<FieldParams> &fieldParams,
                               uint32_t unitsCount)
    : UnitsParams(moveRadius, fieldParams, unitsCount), explodeRadiusSquare(std::pow(explodeRadius, 2)) {}
