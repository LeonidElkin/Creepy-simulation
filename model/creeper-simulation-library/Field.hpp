#ifndef CREEPY_SIMULATION_FIELD_HPP
#define CREEPY_SIMULATION_FIELD_HPP

#include <vector>
#include <functional>

#include "Creeper.hpp"
#include "Utils.hpp"

class Field {
    size_t X_;
    size_t Y_;
    double r_0_;

    std::function<double (Point p1, Point p2)> distance_func_;

    std::vector<Creeper> creepers_;
    std::vector<unsigned> dead_creepers_;

    auto shuffleCreepers();

public:
    void updateField();

    explicit Field(size_t height, size_t width, double r0, size_t creepersNum);
};


#endif//CREEPY_SIMULATION_FIELD_HPP
