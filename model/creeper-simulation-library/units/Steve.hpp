#pragma once

#include "Unit.hpp"

class StevesParams final : public UnitsParams {
 public:
  enum class State : std::uint8_t { Born, Walk, Dead };

  StevesParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams, uint32_t unitsCount);
};

class Steve final : public Unit, std::enable_shared_from_this<Steve> {
  std::shared_ptr<StevesParams> params_;
  StevesParams::State state_{StevesParams::State::Born};

 public:
  Steve(const size_t id, const std::shared_ptr<StevesParams> &params) : Unit(id, params), params_(params) {}

  void updateState(const std::shared_ptr<Unit> &another) override;

  void walk() override;

  void die() override;

  decltype(state_) getState() { return state_; }
};
