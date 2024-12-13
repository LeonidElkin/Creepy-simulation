#pragma once

#include <cstdint>
#include <functional>
#include <optional>

#include "Unit.hpp"
#include "utils.hpp"

class CreepersParams final : public UnitsParams {
 public:
  enum class State : std::uint8_t { Born, Walk, Hissing, Explodes, Sleep };
  double explodeRadiusSquare;
  CreepersParams(double moveRadius, double explodeRadius, const std::shared_ptr<FieldParams> &fieldParams,
                 uint32_t unitsCount);
};

class Creeper final : public Unit {
  std::shared_ptr<CreepersParams> params_;
  CreepersParams::State state_{CreepersParams::State::Born};

 public:
  Creeper(size_t id, const std::shared_ptr<CreepersParams> &params);

  void walk() override;

  void updateState(const Unit &another) override;

  decltype(state_) getState() const { return state_; }
};
