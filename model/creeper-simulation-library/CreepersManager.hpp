#pragma once

#include "Creeper.hpp"

class CreepersManager {
  std::vector<Creeper> creepers_;
  std::vector<std::reference_wrapper<Creeper>> deadCreepers_;

 public:
  CreepersManager(std::shared_ptr<FieldParams> fieldParams, double moveRadius, double explodeRadius);

  void updateField();

  auto const& getCreepers() { return creepers_; }
};
