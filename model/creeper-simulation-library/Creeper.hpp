#ifndef CREEPY_SIMULATION_CREEPER_HPP
#define CREEPY_SIMULATION_CREEPER_HPP

class Creeper {
	double x_;
	double y_;
	enum class State;
	State state_;
public:
	void updatePositions();

	explicit Creeper(double x, double y);
};


#endif //CREEPY_SIMULATION_CREEPER_HPP
