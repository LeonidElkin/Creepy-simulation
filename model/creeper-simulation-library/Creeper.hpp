#ifndef CREEPY_SIMULATION_CREEPER_HPP
#define CREEPY_SIMULATION_CREEPER_HPP

#include <cstdint>
#include <functional>
#include <utility>
#include <vector>

struct Point {
    double x;
    double y;
};

class Creeper {
    Point coord_;
    std::function<Point()> posGenerator_;
    enum class State : std::uint8_t { Born,
                                      Walk,
                                      Hissing,
                                      Explodes } state_;

public:
    void walk();

    Creeper::State updateState(Creeper const &another, const std::function<double(Point, Point)> &distanceFun, double explodeRadius);

    explicit Creeper(decltype(posGenerator_) posGenerator);

protected:
    void updatePositions();
};


#endif//CREEPY_SIMULATION_CREEPER_HPP
