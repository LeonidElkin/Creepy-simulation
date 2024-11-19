#include "Field.hpp"

#include <algorithm>
#include <random>
#include <ranges>

constexpr auto creepers_num_changing_state = 250;

Field::Field(Point size, double r0, size_t creepersNum, double moveRadius,
             FuncType funcType)
    : leftDownBound_(-size.x / 2, -size.y / 2),
      rightUpBound_(size.x / 2, size.y / 2),
      r_0_(r0),
      moveRadius_(moveRadius),
      generatePosition_([this](std::optional<Point> curPosition = {}) -> Point {
        auto xDist =
            curPosition
                ? std::uniform_real_distribution(
                      std::max(leftDownBound_.x, curPosition->x - moveRadius_),
                      std::min(rightUpBound_.x, curPosition->x + moveRadius_))
                : std::uniform_real_distribution(leftDownBound_.x,
                                                 rightUpBound_.x);
        auto yDist =
            curPosition
                ? std::uniform_real_distribution(
                      std::max(leftDownBound_.y, curPosition->y - moveRadius_),
                      std::min(rightUpBound_.y, curPosition->y + moveRadius_))
                : std::uniform_real_distribution(leftDownBound_.y,
                                                 rightUpBound_.y);
        return Point(xDist(getRandom()), yDist(getRandom()));
      }),
      distanceFunc_(getFuncFromEnum(funcType)) {
  if (size.x <= 0 | size.y <= 0) {
    throw std::invalid_argument("The field size must be greater than 0");
  }

  creepers_ = std::views::iota(0LU, creepersNum) |
              std::views::transform(
                  [&](auto i) { return Creeper(generatePosition_, i); }) |
              std::ranges::to<std::vector>();
}

void Field::updateField() {
  std::ranges::for_each(
      creepers_, [this](auto& creeper) { creeper.walk(generatePosition_); });

  auto dist = std::uniform_int_distribution<size_t>(0, creepers_.size());

  std::vector<size_t> creepersChangingState =
      std::views::repeat(dist) | std::views::take(creepers_num_changing_state) |
      std::views::transform([&](auto d) { return d(getRandom()); }) |
      std::ranges::to<std::vector>();

  const double radius = r_0_ * r_0_;

  for (auto i : creepersChangingState) {
    for (auto& creeper2 : creepers_) {
      creepers_[i].updateState(creeper2, distanceFunc_, radius);
    }
  }
}
