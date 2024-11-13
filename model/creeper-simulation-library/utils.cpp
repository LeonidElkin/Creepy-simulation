#include "utils.hpp"

std::mt19937& getRandom() {
  static auto rd = std::random_device();
  static auto gen = std::mt19937(rd());
  return gen;
}
