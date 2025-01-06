#pragma once

#include <memory>
#include <optional>

#include "FieldParams.hpp"
#include "utils.hpp"

class UnitsParams {
  std::shared_ptr<FieldParams> fieldParams_;
  double moveRadius_;
  std::uint32_t unitsCount_;

 public:
  UnitsParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams, uint32_t unitsCount);

  [[nodiscard]] auto getMoveRadius() const { return moveRadius_; }
  [[nodiscard]] auto getLeftDownBound() const { return fieldParams_->leftDownBound; }
  [[nodiscard]] auto getRightUpBound() const { return fieldParams_->rightUpBound; }
  [[nodiscard]] auto getDistanceFunc() const { return fieldParams_->distanceFunc; }
  [[nodiscard]] auto getUnitsCount() const { return unitsCount_; }

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

  virtual void updateState(const Unit &another) = 0;

  virtual void walk() = 0;

  virtual ~Unit() = default;

  Unit(const Unit &other) = default;

  Unit &operator=(const Unit &other) = default;

  Unit(Unit &&other) = default;

  Unit &operator=(Unit &&other) = default;
};