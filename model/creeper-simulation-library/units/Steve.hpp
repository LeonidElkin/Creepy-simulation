#ifndef CREEPY_SIMULATION_STEVE_HPP
#define CREEPY_SIMULATION_STEVE_HPP

#include "Unit.hpp"

class SteveParams : public UnitParams {
 public:
  enum class State : std::uint8_t { Born };
  SteveParams(double moveRadius, const Point& leftDownBound,
              const Point& rightUpBound);
  Point generatePos(std::optional<Point> initialPoint) override;
};

class Steve : public Unit {
  std::shared_ptr<SteveParams> params_;
  SteveParams::State state_{SteveParams::State::Born};
 public:
  ~Steve() override = default;
  void updateState(
      const Unit& another,
      const std::function<double(Point, Point)>& distanceFun) override;
  void walk() override;
};

#endif  // CREEPY_SIMULATION_STEVE_HPP
