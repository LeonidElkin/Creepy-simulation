#pragma once

#include <memory>

#include "Creeper.hpp"
#include "FieldParams.hpp"
#include "Simulation.hpp"
#include "Steve.hpp"
/**
 * @class SimulationFabric
 * @brief A factory class for configuring and creating Simulation objects.
 */
class SimulationFabric {
  std::shared_ptr<FieldParams> fieldParams_;
  std::shared_ptr<CreepersParams> CreepersParams_;
  std::shared_ptr<StevesParams> StevesParams_;

 public:
  /**
   * @brief Default constructor for SimulationFabric.
   */
  SimulationFabric() = default;
  /**
   * @brief Sets the field parameters for the simulation.
   * @param bounds The rectangular bounds of the field.
   * @param distanceFunc Function to calculate distance between two points.
   * @return Reference to the SimulationFabric object for chaining.
   */
  SimulationFabric& setFieldParams(const Rectangle& bounds, const std::function<double(Point p1, Point p2)>& distanceFunc) {
    fieldParams_ = std::make_shared<FieldParams>(bounds, distanceFunc);
    return *this;
  }
  /**
   * @brief Retrieves the field parameters.
   * @return Shared pointer to the field parameters.
   * @throws std::invalid_argument if the field parameters are not set.
   */
  decltype(fieldParams_) getFieldParams() {
    if (!fieldParams_) throw std::invalid_argument("FieldParams_ is not set");
    return fieldParams_;
  }
  /**
   * @brief Sets the parameters for creepers in the simulation.
   * @param moveRadius Movement radius for creepers.
   * @param explodeRadius Explosion radius for creepers.
   * @param count Number of creepers.
   * @return Reference to the SimulationFabric object for chaining.
   * @throws std::invalid_argument if the field parameters are not set.
   */
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
  /**
   * @brief Sets the parameters for Steves in the simulation.
   * @param moveRadius Movement radius for Steves.
   * @param count Number of Steves.
   * @return Reference to the SimulationFabric object for chaining.
   * @throws std::invalid_argument if the field parameters are not set.
   */
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

  SimulationFabric& setBedrock(const Rectangle& bedrock) {
    const auto upBound = fieldParams_->getBounds().rightUpBound;
    const auto downBound = fieldParams_->getBounds().leftDownBound;
    if (bedrock.rightUpBound.x > upBound.x || bedrock.rightUpBound.y > upBound.y ||
        bedrock.leftDownBound.x < downBound.x || bedrock.leftDownBound.y < downBound.y) {
      LOG(WARNING) << "Bedrock is out of field bounds!";
        }
    fieldParams_->setBedrock(bedrock);
    return *this;
  }

  Simulation build() {
    if (!CreepersParams_) setCreeperParams();
    if (!StevesParams_) setSteveParams();
    return Simulation(fieldParams_, CreepersParams_, StevesParams_);
  }
};
