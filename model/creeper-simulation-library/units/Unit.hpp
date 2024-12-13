#pragma once

#include <memory>
#include <optional>

#include "FieldParams.hpp"
#include "utils.hpp"

class UnitsParams {
  std::shared_ptr<FieldParams> fieldParams_;
  double moveRadius_;

 public:
  UnitsParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams);

  [[nodiscard]] auto getMoveRadius() const { return moveRadius_; }
  [[nodiscard]] auto getLeftDownBound() const { return fieldParams_->leftDownBound; }
  [[nodiscard]] auto getRightUpBound() const { return fieldParams_->rightUpBound; }

  virtual Point generatePos(std::optional<Point> initialPoint);

  virtual ~UnitsParams() = default;

  UnitsParams(const UnitsParams &) = delete;

  void operator=(const UnitsParams &) = delete;

  UnitsParams(UnitsParams &&) = delete;

  void operator=(UnitsParams &&) = delete;
};

class Unit {
  Point coord_;
  size_t id_;

 protected:
  void setID(const size_t id) { id_ = id; }
  void setCoord(const Point coord) { coord_ = coord; }

 public:
  explicit Unit(size_t id, const std::shared_ptr<UnitsParams> &params);

  [[nodiscard]] auto getCoord() const { return coord_; }
  [[nodiscard]] auto getID() const { return id_; }

  virtual void updateState(const Unit &another, const std::function<double(Point, Point)> &distanceFun) = 0;

  virtual void walk() = 0;

  virtual ~Unit() = default;

  Unit(const Unit &other) = delete;

  Unit &operator=(const Unit &other) = delete;

  Unit(Unit &&other) = delete;

  Unit &operator=(Unit &&other) = delete;
};
