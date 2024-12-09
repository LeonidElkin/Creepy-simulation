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
  Point leftDownBound_;
  Point rightUpBound_;
 public:
  double explodeRadius;
  CreeperParams(double moveRadius, double explodeRadius, Point leftDownBound, Point rightUpBound);
  Point generatePos(std::optional<Point> initialPoint) override;
};

class Creeper : public Unit {
 public:
  enum class State : std::uint8_t { Born, Walk, Hissing, Explodes, Sleep };

 private:
  std::shared_ptr<CreeperParams> params_;
  State state_{State::Born};

 public:
  Creeper(size_t id, const std::shared_ptr<CreeperParams>& params);

  void walk() override;

  void updateState( const Unit &another, const std::function<double(Point, Point)> &distanceFun) override;
};

#endif  // CREEPY_SIMULATION_CREEPER_HPP
