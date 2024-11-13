#ifndef CREEPY_SIMULATION_CREEPER_HPP
#define CREEPY_SIMULATION_CREEPER_HPP

#include <cstdint>
#include <functional>
#include <utility>
#include <vector>

#include "Utils.hpp"

class Creeper {
 public:
  enum class State : std::uint8_t { Born, Walk, Hissing, Explodes };

 private:
  Point coord_{};
  std::function<Point()> posGenerator_;
  State state_ = State::Born;

 public:
  void rebornTheDead();

  void walk();

  Creeper::State updateState(
      Creeper const &another,
      const std::function<double(Point, Point)> &distanceFun,
      double explodeRadius);

  explicit Creeper(decltype(posGenerator_) posGenerator);

 protected:
  void updatePositions();
};

#endif  // CREEPY_SIMULATION_CREEPER_HPP
