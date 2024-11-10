#ifndef CREEPY_SIMULATION_FIELD_HPP
#define CREEPY_SIMULATION_FIELD_HPP

#include <cstdlib>
#include <vector>
#include "Creeper.hpp"

class Field {
	size_t X_;
	size_t Y_;
	std::vector<Creeper> creepers_;
public:
	void updateField();

	explicit Field(size_t height, size_t width, size_t creepsNum);
};


#endif //CREEPY_SIMULATION_FIELD_HPP
