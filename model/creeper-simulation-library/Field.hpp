#ifndef CREEPY_SIMULATION_FIELD_HPP
#define CREEPY_SIMULATION_FIELD_HPP

#include <functional>
#include <vector>

#include "Creeper.hpp"
#include "Utils.hpp"

class Field {
  Point size_;
  Point leftDownBound_;
  Point rightUpBound_;
  double r_0_;

  std::function<double(Point p1, Point p2)> distance_func_;

  std::vector<Creeper> creepers_;
  std::vector<std::reference_wrapper<Creeper>> dead_creepers_;

  auto shuffleCreepers();

 public:
  void updateField();

  explicit Field(Point size, double r0, size_t creepersNum);
};

#endif  // CREEPY_SIMULATION_FIELD_HPP
