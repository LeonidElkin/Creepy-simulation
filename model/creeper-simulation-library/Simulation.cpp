#include "Simulation.hpp"

#include <omp.h>

#include <algorithm>
#include <memory>
#include <random>
#include <ranges>

constexpr size_t creepers_num_changing_state = 250;

void Simulation::updateField() {
#pragma omp parallel for
  for (auto &creeper : creepers_) {
    creeper.walk();
  }
  auto dist = std::uniform_int_distribution<size_t>(0, creepers_.size());

  const auto creepersChangingState =
      std::views::repeat(dist) | std::views::take(std::min(creepers_num_changing_state, creepers_.size())) |
      std::views::transform([](auto d) { return d(getRandom()); }) | std::ranges::to<std::vector>();

#pragma omp parallel for
  for (auto idx : creepersChangingState) {
    for (const auto &creeper2 : creepers_) {
      if (&creepers_[idx] != &creeper2) {
        creepers_[idx].updateState(creeper2);
      }
    }
  }
}

Simulation::Simulation(const SimulationParams &simulationParams)
    : simulationParams_(simulationParams),
      creepers_(std::views::iota(0LU, simulationParams_.getCreepersParams_()->getUnitsCount()) |
                std::views::transform([&](auto i) { return Creeper(i, simulationParams_.getCreepersParams_()); }) |
                std::ranges::to<std::vector>()) {}
