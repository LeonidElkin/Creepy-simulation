#include "Creeper.hpp"

#include <random>

#include "utils.hpp"

constexpr auto sleep_probability = 0.1;

Creeper::Creeper(size_t id, const std::shared_ptr<CreeperParams> &params)
    : Unit(id, params), params_(params) {}

void Creeper::walk() {
  static auto dist_sleep = std::bernoulli_distribution(sleep_probability);
  switch (state_) {
    case CreeperParams::State::Explodes:
      state_ = CreeperParams::State::Born;
      setCoord(params_->generatePos({}));
      break;
    case CreeperParams::State::Sleep:
      if (dist_sleep(getRandom())) {
        state_ = CreeperParams::State::Walk;
        break;
      }
      break;
    case CreeperParams::State::Walk:
      if (dist_sleep(getRandom())) {
        state_ = CreeperParams::State::Sleep;
        break;
      }
    default:
      state_ = CreeperParams::State::Walk;
      setCoord(params_->generatePos(getCoord()));
  }
}

void Creeper::updateState(
    const Unit &another,
    const std::function<double(Point, Point)> &distanceFun) {
  if (&another == this) return;

  if (state_ == CreeperParams::State::Born) {
    return;
  }

  if (state_ == CreeperParams::State::Explodes) {
    return;
  }

  auto distance = distanceFun(getCoord(), another.getCoord());
  if (distance <= params_->explodeRadius) {
    state_ = CreeperParams::State::Explodes;
    return;
  }

  if (state_ == CreeperParams::State::Hissing) return;

  auto distHissing = std::bernoulli_distribution(1. / (distance));

  if (distHissing(getRandom())) {
    state_ = CreeperParams::State::Hissing;
  } else if (state_ != CreeperParams::State::Sleep) {
    state_ = CreeperParams::State::Walk;
  }
}

CreeperParams::CreeperParams(double moveRadius, double explodeRadius,
                             const Point &leftDownBound,
                             const Point &rightUpBound)
    : UnitParams(moveRadius, leftDownBound, rightUpBound),
      explodeRadius(explodeRadius) {}

Point CreeperParams::generatePos(std::optional<Point> initialPoint) {
  const auto &leftDownBound = getLeftDownBound();
  const auto &rightUpBound = getRightUpBound();
  auto xDist =
      initialPoint
          ? std::uniform_real_distribution(
                std::max(leftDownBound.x, initialPoint->x - moveRadius),
                std::min(rightUpBound.x, initialPoint->x + moveRadius))
          : std::uniform_real_distribution(leftDownBound.x, rightUpBound.x);
  auto yDist =
      initialPoint
          ? std::uniform_real_distribution(
                std::max(leftDownBound.y, initialPoint->y - moveRadius),
                std::min(rightUpBound.y, initialPoint->y + moveRadius))
          : std::uniform_real_distribution(leftDownBound.y, rightUpBound.y);

  return Point(xDist(getRandom()), yDist(getRandom()));
}
