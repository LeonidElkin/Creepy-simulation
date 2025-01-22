#pragma once

#include <memory>
#include <optional>

#include "FieldParams.hpp"
#include "utils.hpp"
/**
 * @class UnitsParams
 * @brief Configuration parameters shared among multiple units.
 */
class UnitsParams {
  std::shared_ptr<FieldParams> fieldParams_;
  double moveRadius_;
  std::uint32_t unitsCount_;

 public:
 /**
  * @brief Constructs the UnitsParams object.
  * @param moveRadius The movement radius for units.
  * @param fieldParams Shared pointer to field parameters.
  * @param unitsCount The number of units in the simulation.
  */
  UnitsParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams, uint32_t unitsCount);
 /**
  * @brief Retrieves the movement radius of the units.
  * @return The movement radius.
  */
  [[nodiscard]] auto getMoveRadius() const { return moveRadius_; }
 /**
  * @brief Retrieves the shared field parameters.
  * @return A shared pointer to the field parameters.
  */
  [[nodiscard]] auto getFieldParams() const { return fieldParams_; }
 /**
  * @brief Retrieves the total number of units.
  * @return The number of units.
  */
  [[nodiscard]] auto getUnitsCount() const { return unitsCount_; }
 /**
  * @brief Generates a position for a unit, optionally starting from an initial point.
  * @param initialPoint An optional initial point.
  * @return The generated position.
  */
  virtual Point generatePos(std::optional<Point> initialPoint);
 /**
  * @brief Virtual destructor for UnitsParams.
  */
  virtual ~UnitsParams() = default;

  UnitsParams(const UnitsParams &) = delete;

  void operator=(const UnitsParams &) = delete;

  UnitsParams(UnitsParams &&) = delete;

  void operator=(UnitsParams &&) = delete;
};

/**
 * @class Unit
 * @brief Represents a generic unit in the simulation.
 */
class Unit {
  Point coord_{};
  size_t id_;

 protected:
 /**
  * @brief Sets the ID of the unit.
  * @param id The unique ID.
  */
  void setID(const size_t id) { id_ = id; }
 /**
  * @brief Sets the coordinates of the unit.
  * @param coord The new coordinates.
  */
  void setCoord(const Point coord) { coord_ = coord; }

 public:
 /**
  * @brief Constructs a Unit object.
  * @param id The unique ID of the unit.
  */
  explicit Unit(size_t id, const std::shared_ptr<UnitsParams> &params);
 /**
  * @brief Retrieves the current coordinates of the unit.
  * @return The current coordinates.
  */
  [[nodiscard]] auto getCoord() const { return coord_; }
 /**
  * @brief Retrieves the ID of the unit.
  * @return The unique ID of the unit.
  */
  [[nodiscard]] auto getID() const { return id_; }
 /**
  * @brief Updates the state of the unit based on interaction with another unit.
  * @param another Shared pointer to another unit.
  */
  virtual void updateState(const std::shared_ptr<Unit> &another) = 0;
 /**
  * @brief Executes the walking behavior of the unit.
  */
  virtual void walk() = 0;
 /**
  * @brief Executes the death behavior of the unit.
  */
  virtual void die() = 0;
 /**
  * @brief Virtual destructor for Unit.
  */
  virtual ~Unit() = default;

  Unit(const Unit &other) = default;

  Unit &operator=(const Unit &other) = default;

  Unit(Unit &&other) = default;

  Unit &operator=(Unit &&other) = default;
};
