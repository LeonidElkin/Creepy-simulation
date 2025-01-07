#include "Simulation.hpp"

#include <omp.h>

#include <algorithm>
#include <memory>
#include <random>
#include <ranges>

Simulation::Simulation(const std::shared_ptr<FieldParams> &fieldParams,
                       const std::shared_ptr<CreepersParams> &creepersParams,
                       const std::shared_ptr<StevesParams> &stevesParams)
    : fieldParams(fieldParams), creepersManager_(creepersParams), stevesManager_(stevesParams) {}

void Simulation::updateField() {
  creepersManager_.beginAndFindSteves(stevesManager_.getSteves());
  creepersManager_.walk();
  stevesManager_.walk();
  creepersManager_.refreshActives();
  creepersManager_.interactWith(creepersManager_.creepers_);
  creepersManager_.interactWith(stevesManager_.steves_);
}
