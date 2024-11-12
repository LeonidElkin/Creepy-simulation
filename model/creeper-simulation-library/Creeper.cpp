#include "Creeper.hpp"

#include <random>

Creeper::Creeper(decltype(posGenerator_) posGenerator) : posGenerator_(std::move(posGenerator)) {
    updatePositions();
}

static auto &getRandom() {
    static auto rd = std::random_device();
    static auto gen = std::mt19937(rd());
    return gen;
}

void Creeper::updatePositions() {
    coord_ = posGenerator_();
}

void Creeper::walk() {
    updatePositions();
    state_ = State::Walk;
}

Creeper::State Creeper::updateState(Creeper const &another, const std::function<double(Point, Point)> &distanceFun, double explodeRadius) {
    if (&another == this) {
        return state_;
    }

    if (state_ == State::Born || state_ == State::Explodes || another.state_ == State::Born || another.state_ == State::Explodes) {
        return state_;
    }

    auto radius = distanceFun(coord_, another.coord_);
    if (radius <= explodeRadius) {
        state_ = State::Explodes;
        return state_;
    }

    static auto dist = std::bernoulli_distribution(1. / (radius * radius));
    if (dist(getRandom())) {
        state_ = State::Hissing;
    } else {
        state_ = State::Walk;
    }

    return state_;
}
