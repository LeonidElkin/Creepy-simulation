#include "Unit.hpp"

#include <glog/logging.h>

UnitsParams::UnitsParams(double moveRadius, const std::shared_ptr<FieldParams> &fieldParams, uint32_t unitsCount)
    : fieldParams_(fieldParams), moveRadius_(moveRadius), unitsCount_(unitsCount) {}

Point UnitsParams::generatePos(const std::optional<Point> initialPoint) {
  const auto &[ldx, ldy] = getFieldParams()->getBounds().leftDownBound;
  const auto &[rux, ruy] = getFieldParams()->getBounds().rightUpBound;
  auto xDist = initialPoint ? std::uniform_real_distribution(std::max(ldx, initialPoint->x - getMoveRadius()),
                                                             std::min(rux, initialPoint->x + getMoveRadius()))
                            : std::uniform_real_distribution(ldx, rux);
  auto yDist = initialPoint ? std::uniform_real_distribution(std::max(ldy, initialPoint->y - getMoveRadius()),
                                                             std::min(ruy, initialPoint->y + getMoveRadius()))
                            : std::uniform_real_distribution(ldy, ruy);

  return Point(xDist(getRandom()), yDist(getRandom()));
}

Unit::Unit(const size_t id, const std::shared_ptr<UnitsParams> &params) : id_(id) {
  do {
    setCoord(params->generatePos({}));
  } while (params->getFieldParams()->checkInsideBlock(getCoord()));
  DLOG(INFO) << "spawn on (" << coord_.x << ", " << coord_.y << ")";
}
