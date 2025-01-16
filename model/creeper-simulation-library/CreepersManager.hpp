#pragma once

#include <glog/logging.h>

#include <list>

#include "Creeper.hpp"
#include "Steve.hpp"

class Simulation;

class CreepersManager {
  std::shared_ptr<CreepersParams> params_;
  std::vector<std::shared_ptr<Creeper>> creepers_;
  std::vector<std::shared_ptr<Creeper>> actives_;

 protected:
  [[nodiscard]] decltype(creepers_)& getCreepersRef() { return creepers_; }

 public:
  CreepersManager(std::shared_ptr<CreepersParams> params);

  void beginAndFindSteves(const std::list<std::shared_ptr<Steve>>& steves);

  [[nodiscard]] const decltype(creepers_)& getCreepers() const { return creepers_; }

  void walk();

  void refreshActives();

  template <typename Units>
  void interactWith(Units units) {
#pragma omp parallel for
    for (auto i = 0; i < actives_.size(); ++i) {
      for (const auto& unit : units) {
        if (static_cast<Unit*>(actives_[i].get()) != static_cast<Unit*>(unit.get())) {
          actives_[i]->updateState(unit);
        }
      }
    }
  }

  friend Simulation;
};
