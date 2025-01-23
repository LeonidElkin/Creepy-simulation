#include <gtest/gtest.h>

#include <chrono>
#include <ranges>

#include "SimulationFabric.hpp"
#include "utils.hpp"

TEST(Simulation, InitTest) {
  constexpr auto creeps_num = 10;
  auto simulationParams = SimulationFabric();
  simulationParams.setFieldParams({{0, 0}, {1, 1}}, DistanceFunc::euclideanSquared);
  simulationParams.setCreeperParams(1, 1, creeps_num);
  auto simulation = simulationParams.build();
  auto creepers = simulation.getCreepersManager().getCreepers();
  EXPECT_EQ(creepers.size(), creeps_num);
}

TEST(Simulation, LetsWalk) {
  // may be false positive
  constexpr auto creeps_num = 10;
  auto simulationParams = SimulationFabric();
  simulationParams.setFieldParams({{0, 0}, {1000, 1000}}, DistanceFunc::euclideanSquared);
  simulationParams.setCreeperParams(100, 1, creeps_num);
  auto simulation = simulationParams.build();
  simulation.updateField();
  auto creepers = simulation.getCreepersManager().getCreepers();
  EXPECT_EQ(creepers.size(), creeps_num);
  for (auto [creep1, creep2] : creepers | std::views::adjacent<2>) {
    if (creep1->getState() == CreepersParams::State::Sleep && creep2->getState() == CreepersParams::State::Sleep) {
      continue;
    }
    EXPECT_NE(creep1->getCoord().x, creep2->getCoord().x);
    EXPECT_NE(creep1->getCoord().y, creep2->getCoord().y);
  }
}

TEST(Simulation, CreeperAggresion) {
  // may be false positive
  constexpr auto creeps_num = 1;
  auto simulationParams = SimulationFabric();
  simulationParams.setFieldParams({{0, 0}, {100, 100}}, DistanceFunc::euclideanSquared);
  simulationParams.setCreeperParams(100, 1, creeps_num);
  simulationParams.setSteveParams(1, 1);
  auto simulation = simulationParams.build();

  CreepersParams::State state = CreepersParams::State::Born;
  for (auto i = 0; i < 1000; i++) {
    simulation.updateField();
    auto creeper = simulation.getCreepersManager().getCreepers()[0];
    if ((state = creeper->getState()) == CreepersParams::State::Explodes) {
      break;
    }
  }
  EXPECT_EQ(state, CreepersParams::State::Explodes);
  EXPECT_EQ(simulation.getStevesManager().getSteves().front()->getState(), StevesParams::State::Dead);
  simulation.updateField();
  state = simulation.getCreepersManager().getCreepers()[0]->getState();
  EXPECT_EQ(state, CreepersParams::State::Born);
  EXPECT_EQ(simulation.getStevesManager().getSteves()[0]->getState(), StevesParams::State::Dead);
}

TEST(Simulation, AndTwoWillExplode) {
  constexpr auto creeps_num = 2;
  auto simulationParams = SimulationFabric();
  simulationParams.setFieldParams({{0, 0}, {1, 1}}, DistanceFunc::euclideanSquared);
  simulationParams.setCreeperParams(1, 100, creeps_num);
  auto simulation = simulationParams.build();
  auto creepers = simulation.getCreepersManager().getCreepers();
  for (auto i = 0; i < 100; i++) {
    simulation.updateField();
    if (creepers[0]->getState() == CreepersParams::State::Explodes ||
        creepers[1]->getState() == CreepersParams::State::Explodes) {
      break;
    }
  }
  EXPECT_EQ(creepers[0]->getState(), CreepersParams::State::Explodes);
  EXPECT_EQ(creepers[1]->getState(), CreepersParams::State::Explodes);
}

TEST(Field, Trivial) {
  auto point = Point(3, 3);
  auto fieldsParams = std::make_shared<FieldParams>(Rectangle{point, point}, DistanceFunc::euclideanSquared);
  EXPECT_EQ(fieldsParams->getBounds(), Rectangle(point, point));
}
