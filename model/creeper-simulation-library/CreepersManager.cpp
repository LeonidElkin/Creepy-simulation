#include "CreepersManager.hpp"

CreepersManager::CreepersManager(std::shared_ptr<FieldParams> fieldParams, double moveRadius, double explodeRadius) {
  auto creepsParams = std::make_unique<CreepersParams>(moveRadius, explodeRadius, fieldParams);
}
