#include "Simulation.hpp"

#include <glog/logging.h>
#include <omp.h>

#include <algorithm>
#include <iostream>
#include <memory>
#include <random>
#include <ranges>

Simulation::Simulation(const std::shared_ptr<FieldParams> &fieldParams,
                       const std::shared_ptr<CreepersParams> &creepersParams,
                       const std::shared_ptr<StevesParams> &stevesParams)
    : fieldParams_(fieldParams), creepersManager_(creepersParams), stevesManager_(stevesParams) {}

void Simulation::updateField() {
  DLOG(INFO) << "start updating field";
  creepersManager_.beginAndFindSteves(stevesManager_.getSteves());
  DLOG(INFO) << "start walking";
  creepersManager_.walk();
  stevesManager_.walk();
  DLOG(INFO) << "end walking, start interacting";
  creepersManager_.refreshActives();
  creepersManager_.interactWith(creepersManager_.getCreepersRef() | std::views::filter([](auto &creeper) {
                                  return creeper->getState() != CreepersParams::State::Born;
                                }));
  creepersManager_.interactWith(stevesManager_.getStevesRef() | std::views::filter([](auto &steve) {
                                  return steve->getState() != StevesParams::State::Dead;
                                }));
  DLOG(INFO) << "end interacting";
}
