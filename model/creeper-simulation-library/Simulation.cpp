#include "Simulation.hpp"

#include <glog/logging.h>
#include <iostream>
#include <omp.h>

#include <algorithm>
#include <iostream>
#include <memory>
#include <random>
#include <ranges>

Simulation::Simulation(const std::shared_ptr<FieldParams> &fieldParams,
                       const std::shared_ptr<CreepersParams> &creepersParams,
                       const std::shared_ptr<StevesParams> &stevesParams)
    : fieldParams(fieldParams), creepersManager_(creepersParams), stevesManager_(stevesParams) {}

void Simulation::updateField() {
  DLOG(INFO) << "start updating field";
  creepersManager_.beginAndFindSteves(stevesManager_.getSteves());
  DLOG(INFO) << "start walking";
  creepersManager_.walk();
  stevesManager_.walk();
  DLOG(INFO) << "end walking, start interacting";
  creepersManager_.refreshActives();
  creepersManager_.interactWith(creepersManager_.creepers_);
  creepersManager_.interactWith(stevesManager_.steves_);
  DLOG(INFO) << "end interacting";
}
