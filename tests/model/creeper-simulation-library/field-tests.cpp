#include <gtest/gtest.h>

#include "Field.hpp"

TEST(Field, InitTest) {
  constexpr auto creepsNum = 10;
  auto field = Field({100, 100}, 5, creepsNum);
  auto creepers = field.getCreepers();
  EXPECT_EQ(creepers.size(), creepsNum);
}
