#include <gtest/gtest.h>

#include <ranges>
#include <chrono>
#include <iostream>
#include "Field.hpp"

TEST(Field, InitTest) {
  constexpr auto creeps_num = 10;
  auto field = Field({100, 100}, 5, creeps_num, 0, FuncType::Euclid);  // NOLINT
  auto creepers = field.getCreepers();
  EXPECT_EQ(creepers.size(), creeps_num);
}

TEST(Field, LetsWalk) {
  constexpr auto creeps_num = 10;
  auto field = Field({100, 100}, 5, creeps_num, 20, FuncType::Euclid);  // NOLINT
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

TEST(Field, Lets) {
  constexpr auto creeps_num = 50000;
  auto field = Field({100, 100}, 5, creeps_num, 20, FuncType::Euclid);  // NOLINT
  std::chrono::steady_clock::time_point begin =
      std::chrono::steady_clock::now();
  field.updateField();
  std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
  std::cout << "Time difference = "
            << std::chrono::duration_cast<std::chrono::microseconds>(end -
                                                                     begin)
                   .count()
            << "[µs]" << '\n';
  EXPECT_EQ(1, 1);

}
