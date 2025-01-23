#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <functional>

#include "FieldParams.hpp"
#include "Steve.hpp"
#include "utils.hpp"

TEST(Steve, InitTest) {
  auto point = Point(3, 3);
  auto fieldsParams = std::make_shared<FieldParams>(Rectangle{point, point}, DistanceFunc::euclideanSquared);
  auto steveParams = std::make_shared<StevesParams>(1, fieldsParams, 1);
  auto steve = Steve(1, steveParams);
  EXPECT_EQ(steve.getCoord().x, point.x);
  EXPECT_EQ(steve.getCoord().y, point.y);
  EXPECT_EQ(steve.getState(), StevesParams::State::Walk);
}

TEST(Steve, DeadTest) {
  auto point = Point(3, 3);
  auto fieldsParams = std::make_shared<FieldParams>(Rectangle{point, point}, DistanceFunc::euclideanSquared);
  auto steveParams = std::make_shared<StevesParams>(1, fieldsParams, 1);
  auto steve = Steve(1, steveParams);
  steve.die();
  EXPECT_EQ(steve.getState(), StevesParams::State::Dead);
}

TEST(Steve, WalkTest) {
  using namespace testing;
  auto point1 = Point(2, 2);
  auto point2 = Point(3, 3);
  auto fieldsParams = std::make_shared<FieldParams>(Rectangle{point1, point2}, DistanceFunc::euclideanSquared);
  auto steveParams = std::make_shared<StevesParams>(1, fieldsParams, 1);
  auto steve = Steve(1, steveParams);
  auto steve2 = std::make_shared<Steve>(2, steveParams);
  steve.walk();
  steve.updateState(steve2);
  auto steveCoord = steve.getCoord();
  EXPECT_THAT(steveCoord.x, AllOf(Ge(point1.x), Le(point2.x)));
  EXPECT_THAT(steveCoord.y, AllOf(Ge(point1.y), Le(point2.y)));
}

TEST(Steve, GetIdTest) {
  auto point = Point(3, 3);
  auto fieldsParams = std::make_shared<FieldParams>(Rectangle{point, point}, DistanceFunc::euclideanSquared);
  auto steveParams = std::make_shared<StevesParams>(1, fieldsParams, 1);
  auto steve = Steve(1, steveParams);
  EXPECT_EQ(steve.getID(), 1);
}

TEST(SteveParams, GetTrivialTest) {
  auto point = Point(3, 3);
  auto fieldsParams = std::make_shared<FieldParams>(Rectangle{point, point}, DistanceFunc::euclideanSquared);
  auto steveParams = std::make_shared<StevesParams>(1, fieldsParams, 1);
  EXPECT_EQ(steveParams->getMoveRadius(), 1);
  EXPECT_EQ(steveParams->getUnitsCount(), 1);
  EXPECT_EQ(steveParams->getFieldParams(), fieldsParams);
}
