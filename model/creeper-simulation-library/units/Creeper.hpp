#pragma once

#include <cstdint>
#include <functional>
#include <optional>

#include "Steve.hpp"
#include "Unit.hpp"
#include "utils.hpp"
/**
 * @class CreepersParams
 * @brief Configuration parameters for creepers in the simulation.
 */
class CreepersParams final : public UnitsParams {
 public:
 /**
  * @enum State
  * @brief Possible states of a creeper.
  */
  enum class State : std::uint8_t { Born, Walk, Hissing, Explodes, Sleep, Dead, GoToSteve, Bonk };
  double explodeRadiusSquare;
  static constexpr size_t creepers_num_changing_state = 250;
 /**
  * @brief Constructs the CreepersParams object.
  * @param moveRadius Movement radius for creepers.
  * @param explodeRadius Explosion radius for creepers.
  * @param fieldParams Shared pointer to field parameters.
  * @param unitsCount Number of creepers in the simulation.
  */
  CreepersParams(double moveRadius, double explodeRadius, const std::shared_ptr<FieldParams> &fieldParams,
                 uint32_t unitsCount);
};
/**
 * @class Creeper
 * @brief Represents an individual creeper in the simulation.
 *
 * The Creeper class manages the behavior, state, and interactions of a single creeper
 * within the simulation.
 */
class Creeper final : public Unit, public std::enable_shared_from_this<Creeper> {
  std::shared_ptr<CreepersParams> params_;
  CreepersParams::State state_{CreepersParams::State::Born};
  std::shared_ptr<Steve> target_;
 /**
  * @brief Moves the creeper towards a specified point.
  * @param to Target point.
  * @return New position of the creeper.
  */
  Point moveTo(Point to);
 /**
  * @brief Moves the creeper after being bonked.
  * @param to Target point.
  * @return New position after the bonk.
  */
  Point bonkedMove(Point to);

 public:
 /**
  * @brief Constructs a Creeper object.
  * @param id Unique ID of the creeper.
  * @param params Shared pointer to creeper parameters.
  */
  Creeper(size_t id, const std::shared_ptr<CreepersParams> &params);
 /**
  * @brief Initializes the creeper's behavior.
  */
  void begin();
 /**
  * @brief Searches for a Steve target.
  * @param steve Shared pointer to a Steve object.
  */
  void steveSearch(const std::shared_ptr<Steve> &steve);
 /**
  * @brief Executes the walking behavior of the creeper.
  */
  void walk() override;

  void updateState(const std::shared_ptr<Unit> &another) override;

  void die() override;

  [[nodiscard]] decltype(state_) getState() const { return state_; }
};
