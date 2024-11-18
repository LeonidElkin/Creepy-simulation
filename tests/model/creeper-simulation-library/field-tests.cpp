#include <gtest/gtest.h>

#include <ranges>

#include "Field.hpp"

TEST(Field, InitTest) {
  constexpr auto creeps_num = 10;
  auto field = Field({100, 100}, 5, creeps_num);  // NOLINT
  auto creepers = field.getCreepers();
  EXPECT_EQ(creepers.size(), creeps_num);
}

TEST(Field, LetsWalk) {
  constexpr auto creeps_num = 10;
  auto field = Field({100, 100}, 5, creeps_num);  // NOLINT
  field.updateField();
  auto creepers = field.getCreepers();
  EXPECT_EQ(creepers.size(), creeps_num);
  for (auto [creep1, creep2] : field.getCreepers() |
                                   std::views::transform(&Creeper::getCoord) |
                                   std::views::adjacent<2>) {
    EXPECT_NE(creep1.x, creep2.x);
    EXPECT_NE(creep1.y, creep2.y);
  }
}
