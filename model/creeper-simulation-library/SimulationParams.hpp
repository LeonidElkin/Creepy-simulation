#pragma once

#include <memory>

#include "Creeper.hpp"
#include "FieldParams.hpp"
#include "Steve.hpp"

class SimulationParams {
  std::shared_ptr<FieldParams> fieldParams_;
  std::shared_ptr<CreepersParams> CreepersParams_;
  std::shared_ptr<StevesParams> StevesParams_;

 public:
  SimulationParams() = default;
  SimulationParams& setFieldParams(const Point &leftDownBound, const Point &rightUpBound,
                      const std::function<double(Point p1, Point p2)> &distanceFunc) {
    fieldParams_ = std::make_shared<FieldParams>(leftDownBound, rightUpBound, distanceFunc);
    return *this;
  }
  decltype(fieldParams_) getFieldParams() {
    if (!fieldParams_) throw std::invalid_argument("FieldParams_ is not set");
    return fieldParams_;
  }
  SimulationParams& setCreeperParams(double moveRadius, double explodeRadius, uint32_t count) {
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

  SimulationParams& setSteveParams(double moveRadius, uint32_t count) {
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
};
