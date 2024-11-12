#include "Field.hpp"

#include <algorithm>
#include <array>
#include <random>

constexpr auto moving_creepers = 250;

auto Field::shuffleCreepers() {

    std::random_device dev;
    std::mt19937 rng(dev());
    std::uniform_int_distribution<std::mt19937::result_type> dist(0, creepers_.size());

    std::vector<unsigned int> creepersToMoveIndices(moving_creepers);

    std::ranges::generate_n(creepersToMoveIndices.begin(), moving_creepers, [&] { return dist(rng); });

    return creepersToMoveIndices;
}


Field::Field(size_t height, size_t width, double r0, size_t creepersNum) : Y_(height), X_(width), r_0_(r0), creepers_(creepersNum), dead_creepers_(0) {}

void Field::updateField() {

    for (auto i: dead_creepers_) {
        creepers_[i].rebornTheDead();
    }

    dead_creepers_.clear();

    auto creepersToMoveIndices = shuffleCreepers();

    for (auto i: creepersToMoveIndices) {
        creepers_[i].updatePositions();
    }

    for (auto i: creepersToMoveIndices) {
        for (int j = 0; j < creepers_.size(); ++j) {
            if (creepers_[j].updateRelations(creepers_[i], r_0_, distance_func_) == DEAD) {
                dead_creepers_.insert(dead_creepers_.begin(), j);
            }
        }
    }

}
