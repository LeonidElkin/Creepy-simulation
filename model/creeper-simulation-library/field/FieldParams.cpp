#include "FieldParams.hpp"

#include <optional>
#include <ranges>

const std::optional<Point> FieldParams::checkIntersection(Point unitsOldCoord, Point unitsNewCoord, Point corner1,
                                                          Point corner2) {
  double A1 = unitsNewCoord.y - unitsOldCoord.y;
  double B1 = unitsOldCoord.x - unitsNewCoord.x;
  double A2 = corner2.y - corner1.y;
  double B2 = corner1.x - corner2.x;
  double det = A1 * B2 - A2 * B1;

  if (std::abs(det) < 1e-9) return std::nullopt;

  double C1 = A1 * unitsOldCoord.x + B1 * unitsOldCoord.y;
  double C2 = A2 * corner1.x + B2 * corner1.y;

  Point intersection = {(B2 * C1 - B1 * C2) / det, (A1 * C2 - A2 * C1) / det};

  auto isBetween = [](double a, double b, double c) { return (c >= std::min(a, b) && c <= std::max(a, b)); };

  if (isBetween(corner1.x, corner2.x, intersection.x) && isBetween(corner1.y, corner2.y, intersection.y) &&
      isBetween(unitsOldCoord.x, unitsNewCoord.x, intersection.x) &&
      isBetween(unitsOldCoord.y, unitsNewCoord.y, intersection.y)) {
    return intersection;
  }
  return std::nullopt;
}

std::vector<Point> FieldParams::getCorners(Rectangle bedrock) const {
  return {{bedrock.leftDownBound.x, bedrock.leftDownBound.y},
          {bedrock.rightUpBound.x, bedrock.leftDownBound.y},
          {bedrock.rightUpBound.x, bedrock.rightUpBound.y},
          {bedrock.leftDownBound.x, bedrock.rightUpBound.y}};
}

std::optional<Point> FieldParams::checkIntersections(const Point unitsOldCoord, const Point unitsNewCoord) const {
  auto range = std::vector<std::optional<Point>>(bedrocks_.size() * 4);
  if (range.empty()) return std::nullopt;
  for (const auto &bedrock : bedrocks_) {
      auto corners = getCorners(bedrock);
      range.append_range(std::views::iota(0, 4) | std::views::transform([&](auto i) {
               return checkIntersection(unitsOldCoord, unitsNewCoord, corners[i], corners[(i + 1) % 4]);
             }));
  }
  return std::ranges::min(range, std::ranges::less{}, [&](const std::optional<Point>& nearest) {
    return nearest ? std::abs(unitsOldCoord.x - nearest->x) + std::abs(unitsOldCoord.y - nearest->y)
                   : std::numeric_limits<double>::max();
  });
}
