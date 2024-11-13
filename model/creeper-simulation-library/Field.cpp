#include "Field.hpp"

#include <algorithm>
#include <random>
#include <ranges>

constexpr auto moving_creepers = 250;

auto Field::shuffleCreepers() {
  std::uniform_int_distribution<decltype(creepers_.size())> dist(
      0, creepers_.size());
  std::vector<unsigned int> creepersToMoveIndices(moving_creepers);
  std::ranges::generate_n(creepersToMoveIndices.begin(), moving_creepers,
                          [&] { return dist(getRandom()); });
  return creepersToMoveIndices;
}

Field::Field(Point size, double r0, size_t creepersNum)
    : size_(size),
      leftDownBound_(-size.x / 2, -size.y / 2),
      rightUpBound_(size.x / 2, size.y / 2),
      r_0_(r0) {
  creepers_ =
      std::views::repeat([this] -> Point {
        static auto x_unif =
            std::uniform_real_distribution(leftDownBound_.x, rightUpBound_.x);
        static auto y_unif =
            std::uniform_real_distribution(leftDownBound_.y, rightUpBound_.y);
        return Point(x_unif(getRandom()), y_unif(getRandom()));
      }) |
      std::views::transform([](auto dist) { return Creeper(dist); }) |
      std::views::take(creepersNum) | std::ranges::to<std::vector>();
}

void Field::updateField() {
  std::ranges::for_each(dead_creepers_, &Creeper::rebornTheDead);

  dead_creepers_.clear();

  auto creepersToMoveIndices = shuffleCreepers();

  for (auto i : creepersToMoveIndices) {
    creepers_[i].walk();
  }

  dead_creepers_ =
      creepers_ | std::views::filter([&](auto &creeper) {
        return bool(creepersToMoveIndices | std::views::filter([&](auto i) {
                      return creeper.updateState(creepers_[i], distance_func_,
                                                 r_0_) ==
                             Creeper::State::Explodes;
                    }));
      }) |
      std::ranges::to<decltype(dead_creepers_)>();
}
