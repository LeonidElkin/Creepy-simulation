#pragma once

#include <vector>

#include "Steve.hpp"

class Simulation;

class StevesManager {
  std::shared_ptr<StevesParams> params_;
  std::vector<std::shared_ptr<Steve>> steves_;

 public:
  StevesManager(std::shared_ptr<StevesParams> params);

  const std::vector<std::shared_ptr<Steve>>& getSteves() const { return steves_; }

  void walk();

  friend class Simulation;
};
