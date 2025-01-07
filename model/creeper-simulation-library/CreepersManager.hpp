#pragma once

#include "Creeper.hpp"
#include "Steve.hpp"

class Simulation;

class CreepersManager {
  std::shared_ptr<CreepersParams> params_;
  std::vector<std::shared_ptr<Creeper>> creepers_;
  std::vector<std::shared_ptr<Creeper>> actives_;

 public:
  CreepersManager(std::shared_ptr<CreepersParams> params);

  void beginAndFindSteves(const std::vector<std::shared_ptr<Steve>>& steves);

  const decltype(creepers_)& getCreepers() const { return creepers_; }

  void walk();

  void refreshActives();

  template <class Units>
  void interactWith(Units units) {
#pragma omp parallel for
    for (const auto& activeCreeper : actives_) {
      for (const auto& unit : units) {
        if (static_cast<void*>(activeCreeper.get()) != static_cast<void*>(unit.get())) {
          activeCreeper->updateState(unit);
        }
      }
    }
  }

  friend Simulation;
};
