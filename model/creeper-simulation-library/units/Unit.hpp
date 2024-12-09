#ifndef CREEPY_SIMULATION_UNIT_HPP
#define CREEPY_SIMULATION_UNIT_HPP

#include <memory>
#include <optional>

#include "utils.hpp"

class UnitParams { // NOLINT: No need to change due to "Rule of five"
 public:
  double moveRadius;
  UnitParams(double moveRadius);
  virtual ~UnitParams() = default;
  virtual Point generatePos(std::optional<Point> initialPoint) = 0;
};

class Unit {  // NOLINT: No need to change due to "Rule of five"
  Point coord_;
  size_t id_;

 protected:
  void setID(size_t id) { id_ = id; }
  void setCoord(Point coord) { coord_ = coord; }

 public:

  [[nodiscard]] auto getID() const { return id_; }
  [[nodiscard]] auto getCoord() const { return coord_; }

  explicit Unit(size_t id, const std::shared_ptr<UnitParams>& params);

  virtual ~Unit() = default;

  virtual void updateState(
      const Unit &another,
      const std::function<double(Point, Point)> &distanceFun) = 0;

  virtual void walk() = 0;
};

#endif  // CREEPY_SIMULATION_UNIT_HPP
