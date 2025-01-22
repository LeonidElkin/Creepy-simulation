#pragma once

#include <glog/logging.h>

#include <list>

#include "Creeper.hpp"
#include "Steve.hpp"

class Simulation;
/**
 * @class CreepersManager
 * @brief Manages a collection of creeper entities and their interactions.
 */
class CreepersManager {
  std::shared_ptr<CreepersParams> params_;
  std::vector<std::shared_ptr<Creeper>> creepers_;
  std::vector<std::shared_ptr<Creeper>> actives_;

 protected:
  /**
   * @brief Provides access to the collection of all creepers.
   * @return Reference to the vector of creepers.
   */
  [[nodiscard]] decltype(creepers_)& getCreepersRef() { return creepers_; }

 public:
/**
 * @brief Constructs a CreepersManager object.
 * @param params Shared pointer to creeper parameters.
 */
  CreepersManager(std::shared_ptr<CreepersParams> params);
  /**
   * @brief Initializes creepers and associates them with nearby Steves.
   * @param steves A vector of shared pointers to Steve objects.
   */
  void beginAndFindSteves(const std::vector<std::shared_ptr<Steve>>& steves);
  /**
   * @brief Provides constant access to the collection of all creepers.
   * @return Constant reference to the vector of creepers.
   */
  [[nodiscard]] const decltype(creepers_)& getCreepers() const { return creepers_; }
  /**
   * @brief Executes the walking behavior for all creepers.
   */
  void walk();
 /**
  * @brief Refreshes the list of active creepers.
  */
  void refreshActives();
 /**
  * @brief Allows creepers to interact with a collection of other units.
  * @tparam Units A collection of unit objects.
  * @param units The units with which the creepers interact.
  */
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
