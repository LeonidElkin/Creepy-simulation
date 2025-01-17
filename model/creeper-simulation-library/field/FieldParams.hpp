#pragma once

#include <list>
#include <optional>

#include "utils.hpp"

class FieldParams {
  std::list<Rectangle> bedrocks_;
  Rectangle bounds_;
  std::function<double(Point p1, Point p2)> distanceFunc;

  [[nodiscard]] static const std::optional<Point> checkIntersection(Point unitsOldCoord, Point unitsNewCoord, Point corner1,
                                                             Point corner2) ;
  [[nodiscard]] std::vector<Point> getCorners(Rectangle bedrock) const;

 public:
  [[nodiscard]] auto& getDistanceFunc() { return distanceFunc; }
  [[nodiscard]] auto& getBounds() { return bounds_; }
  [[nodiscard]] std::optional<Point> checkIntersections(Point unitsOldCoord, Point unitsNewCoord) const;

  FieldParams(const Rectangle& bounds, const std::function<double(Point p1, Point p2)>& distanceFunc)
      : bounds_(bounds), distanceFunc(distanceFunc) {};

  void setBedrock(const Rectangle& bedrock) { bedrocks_.push_front(bedrock); }

  void deleteBedrock(const Rectangle& bedrock) { bedrocks_.remove(bedrock); }
};
