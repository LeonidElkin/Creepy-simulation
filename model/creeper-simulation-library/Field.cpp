#include "Field.hpp"

void Field::updateField() {}

Field::Field(size_t height, size_t width, size_t creepersNum) : Y_(height), X_(width), creepers_(creepersNum) {}
