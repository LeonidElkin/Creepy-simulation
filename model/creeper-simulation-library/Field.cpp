#include "Field.hpp"

#include <algorithm>
#include <random>
#include <ranges>

Field::Field(Point size, double r0, size_t creepersNum, double moveRadius)
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
      distanceFunc_(&euclideanDistance) {
  if (size.x <= 0 | size.y <= 0) {
    throw std::invalid_argument("The field size must be greater than 0");
  }
  creepers_ = std::views::repeat(Creeper(generatePosition_)) |
              std::views::take(creepersNum) | std::ranges::to<std::vector>();
}

void Field::updateField() {
  std::ranges::for_each(
      creepers_, [this](auto& creeper) { creeper.walk(generatePosition_); });

  for (auto [i, creeper1] : creepers_ | std::views::enumerate) {
    for (auto creeper2 : creepers_ | std::views::drop(i)) {
      creeper1.updateState(creeper2, distanceFunc_, r_0_);
    }
  }
}
