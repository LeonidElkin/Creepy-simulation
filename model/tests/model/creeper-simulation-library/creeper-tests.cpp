#include <gtest/gtest.h>

#include "Creeper.hpp"
#include "utils.hpp"

TEST(Creeper, InitTest) {
  auto point = Point(3, 3);
  auto distFunc = std::function([=](std::optional<Point> _) { return point; });
  auto creeper = Creeper(distFunc, 0);
  EXPECT_EQ(creeper.getCoord().x, point.x);
  EXPECT_EQ(creeper.getCoord().y, point.y);
  EXPECT_EQ(creeper.getState(), Creeper::State::Born);
}

TEST(Creeper, WalkTest) {
  auto point1 = Point(3, 3);
  auto point2 = Point(2, 2);
  auto num = 0;
  auto distFunc = std::function([&](std::optional<Point> _) { return num++ ? point2 : point1; });
  auto creeper = Creeper(distFunc, 0);
  creeper.walk(distFunc);
  EXPECT_EQ(creeper.getCoord().x, point2.x);
  EXPECT_EQ(creeper.getCoord().y, point2.y);
  EXPECT_EQ(creeper.getState(), Creeper::State::Walk);
}

TEST(Creeper, HissingTest) {
  auto distFunc = std::function([&](std::optional<Point> _) { return Point(3, 3); });
  auto creeper1 = Creeper(distFunc, 0);
  auto creeper2 = Creeper(distFunc, 1);
  creeper1.walk(distFunc);
  creeper2.walk(distFunc);
  creeper1.updateState(
      creeper2, [](Point a, Point b) { return 0.5; }, 0);  // NOLINT
  EXPECT_EQ(creeper1.getState(), Creeper::State::Hissing);
  EXPECT_EQ(creeper2.getState(), Creeper::State::Hissing);
}

TEST(Creeper, ExplodeTest) {
  auto distFunc = std::function([&](std::optional<Point> _) { return Point(3, 3); });
  auto creeper1 = Creeper(distFunc, 0);
  auto creeper2 = Creeper(distFunc, 1);
  creeper1.walk(distFunc);
  creeper2.walk(distFunc);
  creeper1.updateState(
      creeper2, [](Point a, Point b) { return 0.5; }, 1);  // NOLINT
  creeper2.updateState(
      creeper1, [](Point a, Point b) { return 0.5; }, 1);  // NOLINT
  EXPECT_EQ(creeper1.getState(), Creeper::State::Explodes);
  EXPECT_EQ(creeper2.getState(), Creeper::State::Explodes);
}

TEST(Creeper, SleepTest) {
  auto distFunc = std::function([](std::optional<Point> _) { return Point(2, 2); });
  auto creeper = Creeper(distFunc, 0);
  while (creeper.getState() != Creeper::State::Sleep) {
    creeper.walk(distFunc);
  }
  EXPECT_EQ(creeper.getState(), Creeper::State::Sleep);
}
