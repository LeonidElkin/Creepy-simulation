#pragma once

#include <memory>

#include "Creeper.hpp"
#include "FieldParams.hpp"
#include "Simulation.hpp"
#include "Steve.hpp"

class SimulationFabric {
  std::shared_ptr<FieldParams> fieldParams_;
  std::shared_ptr<CreepersParams> CreepersParams_;
  std::shared_ptr<StevesParams> StevesParams_;

 public:
  SimulationFabric() = default;
  SimulationFabric& setFieldParams(const Rectangle& bounds, const std::function<double(Point p1, Point p2)>& distanceFunc) {
    fieldParams_ = std::make_shared<FieldParams>(bounds, distanceFunc);
    return *this;
  }

  decltype(fieldParams_) getFieldParams() {
    if (!fieldParams_) throw std::invalid_argument("FieldParams_ is not set");
    return fieldParams_;
  }
  SimulationFabric& setCreeperParams(double moveRadius = 10, double explodeRadius = 10, uint32_t count = 0) {
    if (!fieldParams_) {
      throw std::invalid_argument("fieldParams_ is not set");
    }
    CreepersParams_ = std::make_shared<CreepersParams>(moveRadius, explodeRadius, fieldParams_, count);
    return *this;
  }
  decltype(CreepersParams_) getCreepersParams_() {
    if (!CreepersParams_) throw std::invalid_argument("CreepersParams_ is not set");
    return CreepersParams_;
  }

  SimulationFabric& setSteveParams(double moveRadius = 10, uint32_t count = 0) {
    if (!fieldParams_) {
      throw std::invalid_argument("fieldParams_ is not set");
    }
    StevesParams_ = std::make_shared<StevesParams>(moveRadius, fieldParams_, count);
    return *this;
  }
  decltype(StevesParams_) getStevesParams_() {
    if (!StevesParams_) throw std::invalid_argument("StevesParams_ is not set");
    return StevesParams_;
  }

  Simulation build() {
    if (!CreepersParams_) setCreeperParams();
    if (!StevesParams_) setSteveParams();
    return Simulation(fieldParams_, CreepersParams_, StevesParams_);
  }
};
