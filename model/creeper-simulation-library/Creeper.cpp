#include "Creeper.hpp"

#include <random>

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

  static auto dist = std::bernoulli_distribution(1. / (distance * distance));
  if (dist(getRandom())) {
    state_ = State::Hissing;
    another.state_ = State::Hissing;
  } else {
    state_ = State::Walk;
  }

  return state_;
}
