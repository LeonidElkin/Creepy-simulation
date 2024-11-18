#ifndef CREEPY_SIMULATION_CREEPER_HPP
#define CREEPY_SIMULATION_CREEPER_HPP

#include <cstdint>
#include <functional>
#include <utility>
#include <vector>

#include "utils.hpp"

class Creeper {
 public:
  enum class State : std::uint8_t { Born, Walk, Hissing, Explodes };

 private:
  Point coord_{};
  State state_ = State::Born;

 public:
  auto getState() const { return state_; }
  auto getCoord() const { return coord_; }

  void walk(const std::function<Point()> &posGenerator);

  Creeper::State updateState(
      Creeper &another,
      const std::function<double(Point, Point)> &distanceFun,
      double explodeRadius);

  explicit Creeper(const std::function<Point()> &posGenerator);

 protected:
  void updatePositions(const std::function<Point()> &posGenerator);
};

#endif  // CREEPY_SIMULATION_CREEPER_HPP
