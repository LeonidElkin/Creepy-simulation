#include "Creeper.hpp"

#include <random>

constexpr auto sleep_probability = 0.1;

Creeper::Creeper(
    const std::function<Point(std::optional<Point>)> &posGenerator) {
  coord_ = posGenerator({});
}

void Creeper::walk(
    const std::function<Point(std::optional<Point>)> &posGenerator) {
  switch (state_) {
    case State::Explodes:
      state_ = State::Born;
      coord_ = posGenerator({});
      break;
    default:
      state_ = State::Walk;
      coord_ = posGenerator(coord_);
  }
}

Creeper::State Creeper::updateState(
    Creeper &another, const std::function<double(Point, Point)> &distanceFun,
    double explodeRadius) {
  if (state_ == State::Born || another.state_ == State::Born) {
    return state_;
  }

  auto distance = distanceFun(coord_, another.coord_);
  if (distance <= explodeRadius) {
    state_ = State::Explodes;
    return state_;
  }

  auto distHissing = std::bernoulli_distribution(1. / (distance * distance));
  static auto dist_sleep = std::bernoulli_distribution(sleep_probability);

  if (distHissing(getRandom())) {
    state_ = State::Hissing;
    another.state_ = State::Hissing;
  } else if (dist_sleep(getRandom())) {
    state_ = State::Sleep;
  } else {
    state_ = State::Walk;
  }

  return state_;
}
