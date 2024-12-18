#ifndef CREEPY_SIMULATION_CREEPER_HPP
#define CREEPY_SIMULATION_CREEPER_HPP

#include <cstdint>
#include <functional>
#include <optional>
#include <utility>
#include <vector>

#include "utils.hpp"

class Creeper {
 public:
  enum class State : std::uint8_t { Born, Walk, Hissing, Explodes, Sleep };

 private:
  Point coord_{};
  State state_ = State::Born;
  size_t id_;

 public:
  [[nodiscard]] auto getState() const { return state_; }
  [[nodiscard]] auto getCoord() const { return coord_; }

  void walk(const std::function<Point(std::optional<Point>)> &posGenerator);

  Creeper::State updateState(
      const Creeper &another, const std::function<double(Point, Point)> &distanceFun,
      double explodeRadius);

  explicit Creeper(
      const std::function<Point(std::optional<Point>)> &posGenerator,
      size_t id);
};

#endif  // CREEPY_SIMULATION_CREEPER_HPP
