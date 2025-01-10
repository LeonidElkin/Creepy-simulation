#pragma once

#include <list>
#include <vector>

#include "Steve.hpp"

class Simulation;

class StevesManager {
  std::shared_ptr<StevesParams> params_;
  std::list<std::shared_ptr<Steve>> steves_;

 protected:
  [[nodiscard]] decltype(steves_)& getStevesRef() { return steves_; }

 public:
  StevesManager(std::shared_ptr<StevesParams> params);

  [[nodiscard]] const std::list<std::shared_ptr<Steve>>& getSteves() const { return steves_; }

  void walk();

  friend class Simulation;
};
