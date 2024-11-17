#include <gtest/gtest.h>

#include "Field.hpp"

TEST(Field, InitTest) {
  constexpr auto creeps_num = 10;
  auto field = Field({100, 100}, 5, creeps_num, 0); // NOLINT
  auto creepers = field.getCreepers();
  EXPECT_EQ(creepers.size(), creeps_num);
}
