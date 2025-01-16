#include "FieldParams.hpp"

#include <optional>

const std::optional<Point> FieldParams::checkIntersection(Point unitsOldCoord, Point unitsNewCoord, Point corner1,
                                                          Point corner2) const {
  double A1 = unitsNewCoord.y - unitsOldCoord.y;
  double B1 = unitsOldCoord.x - unitsNewCoord.x;
  double A2 = corner2.y - corner1.y;
  double B2 = corner1.x - corner2.x;
  double det = A1 * B2 - A2 * B1;

  if (std::abs(det) < 1e-9) return std::nullopt;

  double C1 = A1 * unitsOldCoord.x + B1 * unitsOldCoord.y;
  double C2 = A2 * corner1.x + B2 * corner1.y;

  Point intersection = {(B2 * C1 - B1 * C2) / det, (A1 * C2 - A2 * C1) / det};

  if (intersection.x < std::min(unitsOldCoord.x, unitsNewCoord.x) ||
      intersection.x > std::max(unitsOldCoord.x, unitsNewCoord.x) ||
      intersection.y < std::min(unitsOldCoord.y, unitsNewCoord.y) ||
      intersection.y > std::max(unitsOldCoord.y, unitsNewCoord.y) || intersection.x < std::min(corner1.x, corner2.x) ||
      intersection.x > std::max(corner1.x, corner2.x) || intersection.y < std::min(corner1.y, corner2.y) ||
      intersection.y > std::max(corner1.y, corner2.y))
    return std::nullopt;

  return intersection;
}

std::vector<Point> FieldParams::getCorners(Rectangle bedrock) const {
  return {{bedrock.leftDownBound.x, bedrock.leftDownBound.y},
          {bedrock.rightUpBound.x, bedrock.leftDownBound.y},
          {bedrock.rightUpBound.x, bedrock.rightUpBound.y},
          {bedrock.leftDownBound.x, bedrock.rightUpBound.y}};
}

Point FieldParams::checkIntersections(Point unitsOldCoord, Point unitsNewCoord) const {
  for (auto bedrock : bedrocks_) {
    std::vector<Point> corners = getCorners(bedrock);
    for (int i = 0; i < corners.size(); ++i) {
      auto intersection = checkIntersection(unitsOldCoord, unitsNewCoord, corners[i], corners[(i + 1) % 4]);
      if (intersection.has_value()) return intersection.value();
    }
  }

  return unitsNewCoord;
}
