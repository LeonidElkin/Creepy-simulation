#include "FieldParams.hpp"

#include <algorithm>
#include <functional>
#include <optional>
#include <ranges>

static bool isBetween(double a, double b, double c) { return (c >= std::min(a, b) && c <= std::max(a, b)); }

std::optional<Point> FieldParams::checkIntersection(Point unitsOldCoord, Point unitsNewCoord, Point corner1,
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

  if (isBetween(corner1.x, corner2.x, intersection.x) && isBetween(corner1.y, corner2.y, intersection.y) &&
      isBetween(unitsOldCoord.x, unitsNewCoord.x, intersection.x) &&
      isBetween(unitsOldCoord.y, unitsNewCoord.y, intersection.y)) {
    constexpr auto stepback = 1;
    return {{intersection.x + (intersection.x - unitsOldCoord.x > 0 ? -stepback : stepback),
             intersection.y + (intersection.y - unitsOldCoord.y > 0 ? -stepback : stepback)}};
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
  auto range = std::vector<std::optional<Point>>();
  range.reserve(4 * bedrocks_.size());
  if (4 * bedrocks_.size() == 0) return std::nullopt;
  for (const auto& bedrock : bedrocks_) {
    auto corners = getCorners(bedrock);
    for (const auto i : std::views::iota(0, 4)) {
      range.push_back(checkIntersection(unitsOldCoord, unitsNewCoord, corners[i], corners[(i + 1) % 4]));
    }
  }
  return std::ranges::min(range, {}, [&](const std::optional<Point>& nearest) {
    return nearest ? std::abs(unitsOldCoord.x - nearest->x) + std::abs(unitsOldCoord.y - nearest->y)
                   : std::numeric_limits<double>::max();
  });
}

bool FieldParams::checkInsideBlock(Point coord) const {
  constexpr auto saveInterval = 10;
  return std::ranges::any_of(bedrocks_, [&](const auto& bedrock) {
    auto [leftDown, rightUp] = bedrock;
    return isBetween(leftDown.x + saveInterval, rightUp.x - saveInterval, coord.x) &&
           isBetween(leftDown.y + saveInterval, rightUp.y - saveInterval, coord.y);
  });
}
