#include "Field.hpp"

#include <omp.h>

#include <algorithm>
#include <memory>
#include <random>
#include <ranges>

constexpr size_t creepers_num_changing_state = 250;

Field::Field(Point size, double r0, size_t creepersNum, double moveRadius,
             FuncType funcType)
    : leftDownBound_(-size.x / 2, -size.y / 2),
      rightUpBound_(size.x / 2, size.y / 2),
      distanceFunc_(getFuncFromEnum(funcType)) {
  if (size.x <= 0 | size.y <= 0) {
    throw std::invalid_argument("The field size must be greater than 0");
  }

  std::shared_ptr<CreeperParams> creeperParams =
      std::make_shared<CreeperParams>(moveRadius, r0 * r0, leftDownBound_,
                                      rightUpBound_);

  creepers_ =
      std::views::iota(0LU, creepersNum) |
      std::views::transform([&](auto i) { return Creeper(i, creeperParams); }) |
      std::ranges::to<std::vector>();
}

void Field::updateField() {
#pragma omp parallel for
  for (auto & creeper : creepers_) {
    creeper.walk();
  }
  auto dist = std::uniform_int_distribution<size_t>(0, creepers_.size());

  auto creepersChangingState =
      std::views::repeat(dist) |
      std::views::take(
          std::min(creepers_num_changing_state, creepers_.size())) |
      std::views::transform([](auto d) { return d(getRandom()); }) |
      std::ranges::to<std::vector>();

#pragma omp parallel for
  for (int idx = 0; idx < creepersChangingState.size(); ++idx) {
    auto i = creepersChangingState[idx];
    for (const auto& creeper2 : creepers_) {
      if (&creepers_[i] != &creeper2) {
        creepers_[i].updateState(creeper2, distanceFunc_);
      }
    }
  }
}
