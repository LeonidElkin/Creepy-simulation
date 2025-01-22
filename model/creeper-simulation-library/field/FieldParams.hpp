#pragma once

#include <list>
#include <optional>

#include "utils.hpp"
/**
 * @class FieldParams
 * @brief A class for managing game field parameters.
 *
 * FieldParams provides functionality to define field boundaries, add obstacles, and
 * check object collisions with these obstacles.
 */
class FieldParams {
  std::list<Rectangle> bedrocks_;
  Rectangle bounds_;
  std::function<double(Point p1, Point p2)> distanceFunc;
  /**
   * @brief Checks the intersection of an object's trajectory with a specified obstacle.
   * @param unitsOldCoord The old coordinates of the object.
   * @param unitsNewCoord The new coordinates of the object.
   * @param corner1 One corner of the obstacle.
   * @param corner2 The opposite corner of the obstacle.
   * @return The intersection point or std::nullopt if no intersection occurs.
   */
  [[nodiscard]] static std::optional<Point> checkIntersection(Point unitsOldCoord, Point unitsNewCoord, Point corner1,
                                                             Point corner2) ;
 /**
  * @brief Returns the corners of a given obstacle.
  * @param bedrock A rectangle representing the obstacle.
  * @return A vector containing the coordinates of the obstacle's corners.
  */
  [[nodiscard]] std::vector<Point> getCorners(Rectangle bedrock) const;

 public:
 /**
  * @brief Retrieves the distance calculation function.
  * @return A reference to the function.
  */
  [[nodiscard]] auto& getDistanceFunc() { return distanceFunc; }
 /**
  * @brief Retrieves the field boundaries.
  * @return A reference to the Rectangle object representing the field boundaries.
  */
  [[nodiscard]] auto& getBounds() { return bounds_; }
 /**
  * @brief Checks for intersections of an object's trajectory with any obstacle on the field.
  * @param unitsOldCoord The old coordinates of the object.
  * @param unitsNewCoord The new coordinates of the object.
  * @return The intersection point or std::nullopt if no intersection occurs.
  */
  [[nodiscard]] std::optional<Point> checkIntersections(Point unitsOldCoord, Point unitsNewCoord) const;
 /**
  * @brief Checks if a point is inside an obstacle.
  * @param coord The coordinates of the point.
  * @return true if the point is inside an obstacle, false otherwise.
  */
  [[nodiscard]] bool checkInsideBlock(Point coord) const;
 /**
  * @brief Constructor for the FieldParams class.
  * @param bounds The boundaries of the game field.
  * @param distanceFunc A function to calculate the distance between points.
  */
  FieldParams(const Rectangle& bounds, const std::function<double(Point p1, Point p2)>& distanceFunc)
      : bounds_(bounds), distanceFunc(distanceFunc) {};
 /**
  * @brief Adds a new obstacle to the field.
  * @param bedrock A rectangle representing the obstacle.
  */
  void setBedrock(const Rectangle& bedrock) { bedrocks_.push_front(bedrock); }

  void deleteBedrock(const Rectangle& bedrock) { bedrocks_.remove(bedrock); }
};
