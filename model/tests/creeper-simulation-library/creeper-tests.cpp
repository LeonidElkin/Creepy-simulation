#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <functional>

#include "Creeper.hpp"
#include "SimulationFabric.hpp"
#include "utils.hpp"

TEST(Creeper, InitTest) {
  auto point = Point(3, 3);
  auto fieldsParams = std::make_shared<FieldParams>(point, point, DistanceFunc::euclideanSquared);
  auto creeperParams = std::make_shared<CreepersParams>(1, 1, fieldsParams, 1);
  auto creeper = Creeper(1, creeperParams);
  EXPECT_EQ(creeper.getCoord().x, point.x);
  EXPECT_EQ(creeper.getCoord().y, point.y);
  EXPECT_EQ(creeper.getState(), CreepersParams::State::Born);
}

TEST(Creeper, WalkTest) {
  auto point1 = Point(2, 2);
  auto point2 = Point(3, 3);
  auto moveRadius = 1;
  auto fieldsParams = std::make_shared<FieldParams>(point1, point2, DistanceFunc::euclideanSquared);
  auto creeperParams = std::make_shared<CreepersParams>(moveRadius, 0, fieldsParams, 2);
  auto creeper1 = Creeper(1, creeperParams);
  auto creeper2 = Creeper(2, creeperParams);
  auto fCoordCreeper1 = creeper1.getCoord();
  auto fCoordCreeper2 = creeper2.getCoord();
  creeper1.begin();
  creeper1.walk();
  creeper2.begin();
  creeper2.walk();

  auto checkCreeper = [&](const Creeper& creeper, auto origCoord) {
    using namespace ::testing;
    switch (creeper.getState()) {
      case CreepersParams::State::Sleep:
        EXPECT_EQ(creeper.getCoord().x, origCoord.x);
        EXPECT_EQ(creeper.getCoord().y, origCoord.y);
        break;
      case CreepersParams::State::Walk:
        EXPECT_THAT(creeper.getCoord().x, AllOf(Ge(point1.x), Le(point2.x)));
        EXPECT_THAT(creeper.getCoord().y, AllOf(Ge(point1.y), Le(point2.y)));
        break;
      default:
        FAIL() << "Unexpected creeper state: " << static_cast<int>(creeper.getState());
    }
  };
  checkCreeper(creeper1, fCoordCreeper1);
  checkCreeper(creeper2, fCoordCreeper2);
}

TEST(Creeper, HissingTest) {
  // may be false positive
  auto point1 = Point(2, 2);
  auto point2 = Point(3, 3);
  auto moveRadius = 1;
  auto fieldsParams =
      std::make_shared<FieldParams>(point1, point2, [](Point, Point) { return std::numeric_limits<double>::min(); });
  auto creeperParams = std::make_shared<CreepersParams>(moveRadius, 0, fieldsParams, 2);
  auto creeper1 = std::make_shared<Creeper>(1, creeperParams);
  auto creeper2 = std::make_shared<Creeper>(2, creeperParams);
  for (auto i = 0; i < 1000; i++) {
    creeper1->begin();
    creeper2->begin();
    creeper1->walk();
    creeper2->walk();
    creeper1->updateState(creeper2);
    creeper2->updateState(creeper1);
    if (creeper1->getState() == CreepersParams::State::Hissing) {
      break;
    }
  }
  EXPECT_EQ(creeper1->getState(), CreepersParams::State::Hissing);
}

TEST(Creeper, ExplodeTest) {
  auto point1 = Point(2, 2);
  auto point2 = Point(3, 3);
  auto moveRadius = 1;
  auto fieldsParams =
      std::make_shared<FieldParams>(point1, point2, [](Point, Point) { return std::numeric_limits<double>::min(); });
  auto creeperParams = std::make_shared<CreepersParams>(moveRadius, 10, fieldsParams, 2);
  auto creeper1 = std::make_shared<Creeper>(1, creeperParams);
  auto creeper2 = std::make_shared<Creeper>(2, creeperParams);
  for (auto i = 0; i < 1000; i++) {
    creeper1->begin();
    creeper2->begin();
    creeper1->walk();
    creeper2->walk();
    creeper1->updateState(creeper2);
    creeper2->updateState(creeper1);

    if (creeper1->getState() == CreepersParams::State::Explodes ||
        creeper2->getState() == CreepersParams::State::Explodes) {
      break;
    }
  }
  EXPECT_EQ(creeper1->getState(), CreepersParams::State::Explodes);
  EXPECT_EQ(creeper2->getState(), CreepersParams::State::Explodes);
}

TEST(Creeper, SleepTest) {
  auto point1 = Point(2, 2);
  auto point2 = Point(3, 3);
  auto moveRadius = 1;
  auto explodeRadius = 10;
  auto fieldsParams =
      std::make_shared<FieldParams>(point1, point2, [](Point, Point) { return std::numeric_limits<double>::min(); });
  auto creeperParams = std::make_shared<CreepersParams>(moveRadius, explodeRadius, fieldsParams, 1);
  auto creeper = Creeper(1, creeperParams);
  creeper.begin();
  for (auto i = 0; i < 1000u && creeper.getState() != CreepersParams::State::Sleep; i++) {
    creeper.walk();
  }
  EXPECT_EQ(creeper.getState(), CreepersParams::State::Sleep);
}
