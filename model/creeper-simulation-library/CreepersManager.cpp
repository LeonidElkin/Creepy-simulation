#include "CreepersManager.hpp"

#include <ranges>

CreepersManager::CreepersManager(std::shared_ptr<CreepersParams> params)
    : params_(params) {
  creepers_ = std::views::iota(0, 10) |
                std::views::transform([&](auto i) -> Creeper { return Creeper(i, params); }) |
                std::ranges::to<std::vector>();
}
