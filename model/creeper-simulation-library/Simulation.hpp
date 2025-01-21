#pragma once

#include <vector>

#include "Creeper.hpp"
#include "CreepersManager.hpp"
#include "Steve.hpp"
#include "StevesManager.hpp"
/**
 * @class Simulation
 * @brief Main controller for managing the simulation of creepers and Steves.
 *
 * The Simulation class coordinates the field, creepers, and Steves, handling updates,
 * interactions, and field configuration.
 */
class Simulation {
  std::shared_ptr<FieldParams> fieldParams_;
  CreepersManager creepersManager_;
  StevesManager stevesManager_;

 public:
  /**
   * @brief Constructs a Simulation object.
   * @param fieldParams Shared pointer to the field parameters.
   * @param creepersParams Shared pointer to creeper parameters.
   * @param stevesParams Shared pointer to Steve parameters.
   */
  Simulation(const std::shared_ptr<FieldParams>& fieldParams, const std::shared_ptr<CreepersParams>& creepersParams,
             const std::shared_ptr<StevesParams>& stevesParams);
  /**
   * @brief Updates the simulation field.
   *
   * This method manages the interactions and updates between creepers and Steves.
   */
  void updateField();
  /**
   * @brief Provides access to the CreepersManager.
   * @return Reference to the CreepersManager.
   */
  CreepersManager& getCreepersManager() { return creepersManager_; }
  /**
   * @brief Provides access to the StevesManager.
   * @return Reference to the StevesManager.
   */
  StevesManager& getStevesManager() { return stevesManager_; }
  /**
   * @brief Configures bedrock for the simulation field.
   * @param bedrock Rectangle representing the bedrock boundaries.
   * @return Reference to the Simulation object.
   */
  Simulation& setBedrock(const Rectangle& bedrock) {
    const auto upBound = fieldParams_->getBounds().rightUpBound;
    const auto downBound = fieldParams_->getBounds().leftDownBound;
    if (bedrock.rightUpBound.x > upBound.x || bedrock.rightUpBound.y > upBound.y ||
        bedrock.leftDownBound.x < downBound.x || bedrock.leftDownBound.y < downBound.y) {
      LOG(WARNING) << "Bedrock is out of field bounds!";
    }
    fieldParams_->setBedrock(bedrock);
    return *this;
  }

  Simulation& deleteBedrock(const Rectangle& bedrock) {
    fieldParams_->deleteBedrock(bedrock);
    return *this;
  }
};
