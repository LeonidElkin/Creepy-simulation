#ifndef CREEPY_SIMULATION_FIELD_HPP
#define CREEPY_SIMULATION_FIELD_HPP

#include <functional>
#include <optional>
#include <vector>

#include "Creeper.hpp"
#include "utils.hpp"

class Field {
  Point leftDownBound_;
  Point rightUpBound_;
  double r_0_;
  double moveRadius_;

  std::function<Point(std::optional<Point>)> generatePosition_;
  std::function<double(Point p1, Point p2)> distanceFunc_;

  std::vector<Creeper> creepers_;
  std::vector<std::reference_wrapper<Creeper>> deadCreepers_;

 public:
  explicit Field(Point size, double r0, size_t creepersNum, double moveRadius);

  void updateField();

  auto const& getCreepers() { return creepers_; }
};

#endif  // CREEPY_SIMULATION_FIELD_HPP
