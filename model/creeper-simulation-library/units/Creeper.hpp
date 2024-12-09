#ifndef CREEPY_SIMULATION_CREEPER_HPP
#define CREEPY_SIMULATION_CREEPER_HPP

#include <cstdint>
#include <functional>
#include <optional>
#include <utility>
#include <vector>

#include "Unit.hpp"
#include "utils.hpp"

class CreeperParams : public UnitParams {
 public:
  enum class State : std::uint8_t { Born, Walk, Hissing, Explodes, Sleep };
  double explodeRadius;
  CreeperParams(double moveRadius, double explodeRadius,
                const Point &leftDownBound, const Point &rightUpBound);
  Point generatePos(std::optional<Point> initialPoint) override;
};

class Creeper : public Unit {
  std::shared_ptr<CreeperParams> params_;
  CreeperParams::State state_{CreeperParams::State::Born};

 public:
  Creeper(size_t id, const std::shared_ptr<CreeperParams> &params);

  virtual ~Creeper() = default;

  void walk() override;

  void updateState(
      const Unit &another,
      const std::function<double(Point, Point)> &distanceFun) override;
};

#endif  // CREEPY_SIMULATION_CREEPER_HPP
