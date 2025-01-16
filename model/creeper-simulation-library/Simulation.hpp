#pragma once

#include <vector>

#include "Creeper.hpp"
#include "CreepersManager.hpp"
#include "Steve.hpp"
#include "StevesManager.hpp"

class Simulation {
  std::shared_ptr<FieldParams> fieldParams_;
  CreepersManager creepersManager_;
  StevesManager stevesManager_;

 public:
  Simulation(const std::shared_ptr<FieldParams>& fieldParams, const std::shared_ptr<CreepersParams>& creepersParams,
             const std::shared_ptr<StevesParams>& stevesParams);
  void updateField();
  CreepersManager& getCreepersManager() { return creepersManager_; }
  StevesManager& getStevesManager() { return stevesManager_; }

  Simulation& setBedrock(const Rectangle& bedrock) {
    if (!fieldParams_) {
      throw std::invalid_argument("fieldParams_ is not set");
    }
    fieldParams_->setBedrock(bedrock);
    return *this;
  }

  Simulation& deleteBedrock(const Rectangle& bedrock) {
    if (!fieldParams_) {
      throw std::invalid_argument("fieldParams_ is not set");
    }
    fieldParams_->deleteBedrock(bedrock);
    return *this;
  }
};
