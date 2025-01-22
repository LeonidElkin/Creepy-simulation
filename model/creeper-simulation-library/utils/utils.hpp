#pragma once

#include <functional>
#include <random>

/**
 * @struct Point
 * @brief Represents a 2D point with x and y coordinates.
 */
struct Point {
  double x;
  double y;
  /**
   * @brief Equality operator for Point.
   * @param p2 Another point to compare with.
   * @return True if the points are approximately equal, false otherwise.
   */
  bool operator==(const Point& p2) const { return std::abs(x - p2.x) < 1e-9 && std::abs(y - p2.y) < 1e-9; }
};
/**
 * @struct Rectangle
 * @brief Represents a rectangle defined by two points: bottom-left and top-right.
 */
struct Rectangle {
  Point leftDownBound;
  Point rightUpBound;
  /**
   * @brief Constructs a Rectangle object.
   * @param leftDownBound The bottom-left corner.
   * @param rightUpBound The top-right corner.
   */
  Rectangle(Point leftDownBound, Point rightUpBound) : leftDownBound(leftDownBound), rightUpBound(rightUpBound) {}
    /**
     * @brief Equality operator for Rectangle.
     * @param r2 Another rectangle to compare with.
     * @return True if the rectangles are equal, false otherwise.
     */
  bool operator==(const Rectangle& r2) const {
    return leftDownBound == r2.leftDownBound && rightUpBound == r2.rightUpBound;
  }
};
/**
 * @brief Retrieves a shared random number generator.
 * @return A reference to the random number generator.
 */
std::mt19937& getRandom();
/**
 * @namespace DistanceFunc
 * @brief Namespace containing distance calculation functions and types.
 */
namespace DistanceFunc {
 /**
  * @enum Type
  * @brief Enumerates supported distance calculation types.
  */
enum class Type : std::uint8_t { Euclid, Polar, Manhattan };
 /**
  * @brief Computes the squared Euclidean distance between two points.
  * @param p1 The first point.
  * @param p2 The second point.
  * @return The squared Euclidean distance.
  */
double euclideanSquared(const Point& p1, const Point& p2);
 /**
  * @brief Computes the squared polar distance between two points.
  * @param p1 The first point.
  * @param p2 The second point.
  * @return The squared polar distance.
  */
double polarSquared(const Point& p1, const Point& p2);
 /**
  * @brief Computes the squared Manhattan distance between two points.
  * @param p1 The first point.
  * @param p2 The second point.
  * @return The squared Manhattan distance.
  */
double manhattanSquared(const Point& p1, const Point& p2);
 /**
  * @brief Maps a distance function type to its corresponding function.
  * @param funcType The type of distance function.
  * @return A function for calculating the specified distance.
  */
std::function<double(Point p1, Point p2)> funcToType(Type funcType);
}  // namespace DistanceFunc
