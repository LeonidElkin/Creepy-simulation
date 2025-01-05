#include <gtest/gtest.h>

#include <chrono>
#include <ranges>

#include "Simulation.hpp"
#include "utils.hpp"

TEST(Simulation, InitTest) {
  constexpr auto creeps_num = 10;
  auto simulationParams = SimulationParams();
  simulationParams.setFieldParams({0, 0}, {1, 1}, DistanceFunc::euclideanSquared);
  simulationParams.setCreeperParams(1, 1, creeps_num);
  auto simulation = Simulation(simulationParams);
  auto creepers = simulation.getCreepers();
  EXPECT_EQ(creepers.size(), creeps_num);
}

TEST(Simulation, LetsWalk) {
  // may be false positive
  constexpr auto creeps_num = 10;
  auto simulationParams = SimulationParams();
  simulationParams.setFieldParams({0, 0}, {100, 100}, DistanceFunc::euclideanSquared);
  simulationParams.setCreeperParams(100, 1, creeps_num);
  auto simulation = Simulation(simulationParams);
  simulation.updateField();
  auto creepers = simulation.getCreepers();
  EXPECT_EQ(creepers.size(), creeps_num);
  for (auto [creep1, creep2] : creepers | std::views::adjacent<2>) {
    if (creep1.getState() == CreepersParams::State::Sleep && creep2.getState() == CreepersParams::State::Sleep)
      continue;
    EXPECT_NE(creep1.getCoord().x, creep2.getCoord().x);
    EXPECT_NE(creep1.getCoord().y, creep2.getCoord().y);
  }
}
