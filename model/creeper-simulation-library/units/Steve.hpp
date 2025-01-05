#pragma once

#include "Unit.hpp"

class StevesParams final : public UnitsParams {
 public:
  enum class State : std::uint8_t { Born };

  StevesParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams, uint32_t unitsCount);
};

class Steve final : public Unit {
  std::shared_ptr<StevesParams> params_;
  StevesParams::State state_{StevesParams::State::Born};

 public:
  Steve(const size_t id, const std::shared_ptr<StevesParams> &params) : Unit(id, params) {}

  void updateState(const Unit &another) override;

  void walk() override;

  decltype(state_) getState() { return state_; }
};
