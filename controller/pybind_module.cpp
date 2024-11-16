#include <pybind11/pybind11.h>

#include "Field.hpp"

namespace py = pybind11;

PYBIND11_MODULE(field_provider, handle) {
  handle.doc() = "This is the doc";
  py::class_<Field>(handle, "Field").def(py::init<Point, double, size_t>());
}
