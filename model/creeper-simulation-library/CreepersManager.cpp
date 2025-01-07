#include "CreepersManager.hpp"

#include <ranges>

CreepersManager::CreepersManager(std::shared_ptr<CreepersParams> params) : params_(std::move(params)) {
  creepers_ = std::views::iota(0LU, params_->getUnitsCount()) |
              std::views::transform([&](auto i) { return std::make_shared<Creeper>(i, params_); }) |
              std::ranges::to<std::vector>();
}

void CreepersManager::beginAndFindSteves(const std::vector<std::shared_ptr<Steve>>& steves) {
#pragma omp parallel for
  for (const auto& creeper : creepers_) {
    creeper->begin();
    for (const auto& steve : steves) {
      creeper->steveSearch(steve);
    }
  }
}

void CreepersManager::walk() {
#pragma omp parallel for
  for (const auto& creeper : creepers_) {
    creeper->walk();
  }
}
void CreepersManager::refreshActives() {
  auto dist = std::uniform_int_distribution<size_t>(0, creepers_.size());
  actives_ =
      std::views::repeat(dist) | std::views::take(std::min(params_->creepers_num_changing_state, creepers_.size())) |
      std::views::transform([this](auto d) { return creepers_[d(getRandom())]; }) | std::ranges::to<std::vector>();
}
