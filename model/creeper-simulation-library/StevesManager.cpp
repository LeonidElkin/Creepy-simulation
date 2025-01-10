#include "StevesManager.hpp"

#include <ranges>

StevesManager::StevesManager(std::shared_ptr<StevesParams> params) : params_(std::move(params)) {
  steves_ = std::views::iota(0LU, params_->getUnitsCount()) |
            std::views::transform([&](auto i) { return std::make_shared<Steve>(i, params_); }) |
            std::ranges::to<std::list>();
}

void StevesManager::walk() {
  for (auto it = steves_.begin(); it != steves_.end();) {
    if (it->get()->getState() == StevesParams::State::Dead) {
      it = steves_.erase(it);
    } else {
      it->get()->walk();
      ++it;
    }
  }
};
