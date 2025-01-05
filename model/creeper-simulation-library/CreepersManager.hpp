#pragma once

#include "Creeper.hpp"

class CreepersManager {
  std::shared_ptr<CreepersParams> params_;
  std::vector<Creeper> creepers_;
public:
  CreepersManager(std::shared_ptr<CreepersParams> params);
};
