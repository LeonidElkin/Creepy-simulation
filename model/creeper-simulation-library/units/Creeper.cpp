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
      if (target_ && target_->getState() == StevesParams::State::Dead) {
        target_ = nullptr;
        state_ = CreepersParams::State::Walk;
      }
      break;
    case CreepersParams::State::Hissing:
    case CreepersParams::State::Born:
      state_ = CreepersParams::State::Walk;
    default:
      break;
  }
}

void Creeper::steveSearch(const std::shared_ptr<Steve> &steve) {
  switch (state_) {
    case CreepersParams::State::Born:
    case CreepersParams::State::Bonk:
      return;
    default:
      if (state_ == CreepersParams::State::Born || steve->getState() == StevesParams::State::Dead) {
        return;
      }
  }
  const auto distance = std::sqrt(params_->getFieldParams()->getDistanceFunc()(getCoord(), steve->getCoord()));
  auto distSteve = std::bernoulli_distribution(std::min(10. / distance, 1.));
  if (distSteve(getRandom())) {
    DLOG(INFO) << "Creeper " << getID() << " find Steve " << steve->getID();
    target_ = steve;
    state_ = CreepersParams::State::GoToSteve;
  }
}

Point Creeper::moveTo(const Point to) {
  const auto position = getCoord();
  const auto t =
      std::min(1., params_->getMoveRadius() / std::sqrt(params_->getFieldParams()->getDistanceFunc()(position, to)));
  Point newPosition = {position.x + t * (to.x - position.x), position.y + t * (to.y - position.y)};
  return bonkedMove(newPosition);
}

Point Creeper::bonkedMove(const Point to) {
  const auto inters = params_->getFieldParams()->checkIntersections(getCoord(), to);
  if (inters) {
    state_ = CreepersParams::State::Bonk;
    return inters.value();
  }
  return to;
}

void Creeper::walk() {
  static auto dist_sleep = std::bernoulli_distribution(sleep_probability);
  static auto dist_wake_up = std::bernoulli_distribution(wake_up_probability);

  if (state_ != CreepersParams::State::Born && params_->getFieldParams()->checkInsideBlock(getCoord())) {
    die();
    return;
  }
  switch (state_) {
    case CreepersParams::State::Born:
      do {
        setCoord(params_->generatePos({}));
      } while (params_->getFieldParams()->checkInsideBlock(getCoord()));
      break;
    case CreepersParams::State::Bonk:
      break;
    case CreepersParams::State::GoToSteve:
      setCoord(moveTo(target_->getCoord()));
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
      setCoord(bonkedMove(params_->generatePos(getCoord())));
      break;
    default:
      DLOG(WARNING) << "Invalid creeper state when walking: " << static_cast<int>(state_);
  }
}

void Creeper::die() { state_ = CreepersParams::State::Explodes; }

void Creeper::updateState(const std::shared_ptr<Unit> &another) {
  if (another.get() == this) return;
  switch (state_) {
    case CreepersParams::State::Born:
    case CreepersParams::State::Bonk:
      return;
    default:
      break;
  }

  const auto distanceSquare = params_->getFieldParams()->getDistanceFunc()(getCoord(), another->getCoord());
  if (distanceSquare <= params_->explodeRadiusSquare) {
    DLOG(INFO) << "Creeper " << getID() << " exploded and kill " << typeid(*another).name() << " " << another->getID();
    state_ = CreepersParams::State::Explodes;
    another->die();
    return;
  }

  switch (state_) {
    case CreepersParams::State::Explodes:
    case CreepersParams::State::Hissing:
    case CreepersParams::State::GoToSteve:
    case CreepersParams::State::Dead:
      return;
    default:
      break;
  }

  auto distHissing = std::bernoulli_distribution(std::min(1. / (distanceSquare), 1.));

  if (distHissing(getRandom())) {
    state_ = CreepersParams::State::Hissing;
  } else if (state_ != CreepersParams::State::Sleep) {
    state_ = CreepersParams::State::Walk;
  }
}

CreepersParams::CreepersParams(double moveRadius, double explodeRadius, const std::shared_ptr<FieldParams> &fieldParams,
                               uint32_t unitsCount)
    : UnitsParams(moveRadius, fieldParams, unitsCount), explodeRadiusSquare(std::pow(explodeRadius, 2)) {}
