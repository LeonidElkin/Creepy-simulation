#include "Unit.hpp"

UnitsParams::UnitsParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams, uint32_t unitsCount)
    : fieldParams_(fieldParams), moveRadius_(moveRadius), unitsCount_(unitsCount) {}

Point UnitsParams::generatePos(const std::optional<Point> initialPoint) {
  const auto &[ldx, ldy] = getLeftDownBound();
  const auto &[rux, ruy] = getRightUpBound();
  auto xDist = initialPoint ? std::uniform_real_distribution(std::max(ldx, initialPoint->x - getMoveRadius()),
                                                             std::min(rux, initialPoint->x + getMoveRadius()))
                            : std::uniform_real_distribution(ldx, rux);
  auto yDist = initialPoint ? std::uniform_real_distribution(std::max(ldy, initialPoint->y - getMoveRadius()),
                                                             std::min(ruy, initialPoint->y + getMoveRadius()))
                            : std::uniform_real_distribution(ldy, ruy);

  return Point(xDist(getRandom()), yDist(getRandom()));
}

Unit::Unit(const size_t id, const std::shared_ptr<UnitsParams> &params) : coord_(params->generatePos({})), id_(id) {}
