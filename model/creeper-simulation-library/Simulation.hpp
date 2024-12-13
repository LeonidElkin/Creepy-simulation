#pragma once

#include <functional>
#include <optional>
#include <vector>

#include "Creeper.hpp"
#include "SimulationParams.hpp"
#include "Steve.hpp"
#include "utils.hpp"

class Simulation {
  SimulationParams simulationParams_;
  std::vector<Creeper> creepers_;
  std::vector<Steve> steves_;

 public:
  explicit Simulation(const SimulationParams& simulationParams);
  void updateField();
  const std::vector<Creeper>& getCreepers() const { return creepers_; }
  const std::vector<Steve>& getSteves() const { return steves_; }
};
