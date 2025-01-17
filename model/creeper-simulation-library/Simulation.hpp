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
