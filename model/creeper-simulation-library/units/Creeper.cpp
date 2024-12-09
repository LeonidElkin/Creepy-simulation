#include "Creeper.hpp"

#include <random>

#include "utils.hpp"

constexpr auto sleep_probability = 0.1;

Creeper::Creeper(size_t id, const std::shared_ptr<CreeperParams>& params)
    : Unit(id, params), params_(params) {}

void Creeper::walk() {
  static auto dist_sleep = std::bernoulli_distribution(sleep_probability);
  switch (state_) {
    case State::Explodes:
      state_ = State::Born;
      setCoord(params_->generatePos({}));
      break;
    case State::Sleep:
      if (dist_sleep(getRandom())) {
        state_ = State::Walk;
        break;
      }
      break;
    case State::Walk:
      if (dist_sleep(getRandom())) {
        state_ = State::Sleep;
        break;
      }
    default:
      state_ = State::Walk;
      setCoord(params_->generatePos(getCoord()));
  }
}

void Creeper::updateState(
    const Unit &another,
    const std::function<double(Point, Point)> &distanceFun) {
  if (&another == this) return;

  if (state_ == State::Born) {
    return;
  }

  if (state_ == State::Explodes) {
    return;
  }

  auto distance = distanceFun(getCoord(), another.getCoord());
  if (distance <= params_->explodeRadius) {
    state_ = State::Explodes;
    return;
  }

  if (state_ == State::Hissing) return;

  auto distHissing = std::bernoulli_distribution(1. / (distance));

  if (distHissing(getRandom())) {
    state_ = State::Hissing;
  } else if (state_ != State::Sleep) {
    state_ = State::Walk;
  }
}

CreeperParams::CreeperParams(double moveRadius, double explodeRadius,
                             Point leftDownBound, Point rightUpBound)
    : UnitParams(moveRadius),
      explodeRadius(explodeRadius),
      leftDownBound_(leftDownBound),
      rightUpBound_(rightUpBound) {}

Point CreeperParams::generatePos(std::optional<Point> initialPoint) {
  auto xDist =
      initialPoint
          ? std::uniform_real_distribution(
                std::max(leftDownBound_.x, initialPoint->x - moveRadius),
                std::min(rightUpBound_.x, initialPoint->x + moveRadius))
          : std::uniform_real_distribution(leftDownBound_.x, rightUpBound_.x);
  auto yDist =
      initialPoint
          ? std::uniform_real_distribution(
                std::max(leftDownBound_.y, initialPoint->y - moveRadius),
                std::min(rightUpBound_.y, initialPoint->y + moveRadius))
          : std::uniform_real_distribution(leftDownBound_.y, rightUpBound_.y);

  return Point(xDist(getRandom()), yDist(getRandom()));
}
