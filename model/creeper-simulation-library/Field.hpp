#ifndef CREEPY_SIMULATION_FIELD_HPP
#define CREEPY_SIMULATION_FIELD_HPP

#include <functional>
#include <vector>

#include "Creeper.hpp"
#include "utils.hpp"

class Field {
  Point leftDownBound_;
  Point rightUpBound_;
  double r_0_;

  std::function<Point()> generatePosition_;
  std::function<double(Point p1, Point p2)> distanceFunc_;

  std::vector<Creeper> creepers_;
  std::vector<std::reference_wrapper<Creeper>> deadCreepers_;

 public:
  auto const& getCreepers() { return creepers_; }

  void updateField();

  explicit Field(Point size, double r0, size_t creepersNum);
};

#endif  // CREEPY_SIMULATION_FIELD_HPP
