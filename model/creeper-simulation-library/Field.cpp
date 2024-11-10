#include "Field.hpp"

void Field::updateField() {}

Field::Field(size_t height, size_t width, size_t creepsNum) : Y_(height), X_(width), creepers_(creepsNum) {}
