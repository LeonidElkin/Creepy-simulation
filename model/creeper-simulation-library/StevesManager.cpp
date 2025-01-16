#include "StevesManager.hpp"

#include <ranges>

StevesManager::StevesManager(std::shared_ptr<StevesParams> params) : params_(std::move(params)) {
  steves_ = std::views::iota(0LU, params_->getUnitsCount()) |
            std::views::transform([&](auto i) { return std::make_shared<Steve>(i, params_); }) |
            std::ranges::to<std::vector>();
}

void StevesManager::walk() {
  std::ranges::for_each(steves_, &Steve::walk);
}
