#include "Creeper.hpp"

#include <fmt/color.h>

#include <random>

#include "utils.hpp"

constexpr auto sleep_probability = 0.1;

Creeper::Creeper(const std::function<Point(std::optional<Point>)> &posGenerator,
                 size_t id)
    : id_(id) {
  logInfo(fmt::format("Creeper {} has been born", id));
  coord_ = posGenerator({});
}

void Creeper::walk(
    const std::function<Point(std::optional<Point>)> &posGenerator) {
  switch (state_) {
    case State::Explodes:
      state_ = State::Born;
      logInfo(fmt::format("Creeper {} has been born again", id_));
      coord_ = posGenerator({});
      break;
    case State::Walk:
      static auto dist_sleep = std::bernoulli_distribution(sleep_probability);
      if (dist_sleep(getRandom())) {
        logInfo(fmt::format("Creeper {} is getting some rest", id_));
        state_ = State::Sleep;
        break;
      }
    default:
      state_ = State::Walk;
      logInfo(fmt::format("Creeper {} is hanging around", id_));
      coord_ = posGenerator(coord_);
  }
}

Creeper::State Creeper::updateState(
    Creeper &another, const std::function<double(Point, Point)> &distanceFun,
    double explodeRadius) {
  if (state_ == State::Born || another.state_ == State::Born) {
    logInfo(
        fmt::format("Creeper {} or Creeper {} is invulnerable at the moment",
                    id_, another.id_));
    return state_;
  }

  if (state_ == State::Explodes) {
    return state_;
  }

  auto distance = distanceFun(coord_, another.coord_);
  if (distance <= explodeRadius) {
    logInfo(fmt::format("Creeper {} and Creeper {} have just exploded", id_,
                        another.id_));
    state_ = State::Explodes;
    return state_;
  }

  if (state_ == State::Hissing) return state_;

  auto distHissing = std::bernoulli_distribution(1. / (distance));

  if (distHissing(getRandom())) {
    logInfo(fmt::format("Creeper {} and Creeper {} are hissing at each other",
                        id_, another.id_));
    state_ = State::Hissing;
  } else if (state_ != State::Sleep) {
    state_ = State::Walk;
  }

  return state_;
}
