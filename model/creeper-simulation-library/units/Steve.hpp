#pragma once

#include "Unit.hpp"
/**
 * @class StevesParams
 * @brief Configuration parameters for Steve units in the simulation.
 */
class StevesParams final : public UnitsParams {
 public:
 /**
  * @enum State
  * @brief Possible states of a Steve.
  */
  enum class State : std::uint8_t { Born, Walk, Dead };
 /**
  * @brief Constructs the StevesParams object.
  * @param moveRadius Movement radius for Steve units.
  * @param fieldParams Shared pointer to field parameters.
  * @param unitsCount Number of Steve units in the simulation.
  */
  StevesParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams, uint32_t unitsCount);
};
/**
 * @class Steve
 * @brief Represents an individual Steve unit in the simulation.
 *
 * The Steve class manages the behavior, state, and interactions of a single Steve
 * within the simulation.
 */
class Steve final : public Unit, std::enable_shared_from_this<Steve> {
  std::shared_ptr<StevesParams> params_;
  StevesParams::State state_{StevesParams::State::Born};

 public:
 /**
  * @brief Constructs a Steve object.
  * @param id Unique ID of the Steve.
  * @param params Shared pointer to Steve parameters.
  */
  Steve(const size_t id, const std::shared_ptr<StevesParams> &params) : Unit(id, params), params_(params) {}
 /**
  * @brief Updates the state of the Steve based on interaction with another unit.
  * @param another Shared pointer to another unit.
  */
  void updateState(const std::shared_ptr<Unit> &another) override;
 /**
  * @brief Executes the walking behavior of the Steve.
  */
  void walk() override;
 /**
  * @brief Executes the death behavior of the Steve.
  */
  void die() override;
 /**
  * @brief Retrieves the current state of the Steve.
  * @return The state of the Steve.
  */
  decltype(state_) getState() { return state_; }
};
