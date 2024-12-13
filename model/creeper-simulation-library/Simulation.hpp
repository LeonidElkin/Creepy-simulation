#pragma once

#include <functional>
#include <optional>
#include <vector>

#include "Creeper.hpp"
#include "utils.hpp"

class Simulation {
  std::vector<Creeper> creepers_;
  std::vector<std::reference_wrapper<Creeper>> deadCreepers_;

 public:
  explicit Simulation(Point size, double creeperExplodeRadius_, size_t creepersNum, double moveRadius,
                      FuncType funcType);

  void updateField();

  auto const& getCreepers() { return creepers_; }
};
