#pragma once

#include <cstdint>
#include <functional>
#include <optional>

#include "Steve.hpp"
#include "Unit.hpp"
#include "utils.hpp"

class CreepersParams final : public UnitsParams {
 public:
  enum class State : std::uint8_t { Born, Walk, Hissing, Explodes, Sleep, Dead, GoToSteve, Bonk };
  double explodeRadiusSquare;
  static constexpr size_t creepers_num_changing_state = 250;
  CreepersParams(double moveRadius, double explodeRadius, const std::shared_ptr<FieldParams> &fieldParams,
                 uint32_t unitsCount);
};

class Creeper final : public Unit, public std::enable_shared_from_this<Creeper> {
  std::shared_ptr<CreepersParams> params_;
  CreepersParams::State state_{CreepersParams::State::Born};
  std::shared_ptr<Steve> target_;

  Point moveTo(Point to);

  Point bonkedMove(Point to);

 public:
  Creeper(size_t id, const std::shared_ptr<CreepersParams> &params);

  void begin();

  void steveSearch(const std::shared_ptr<Steve> &steve);

  void walk() override;

  void updateState(const std::shared_ptr<Unit> &another) override;

  void die() override;

  [[nodiscard]] decltype(state_) getState() const { return state_; }
};
