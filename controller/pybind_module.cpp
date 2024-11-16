#include <pybind11/pybind11.h>

#include "Field.hpp"

namespace py = pybind11;

class Bruhnya {
  double b_;

 public:
  explicit Bruhnya(double b) : b_(b) {}
  double mult(double a) { return a * b_; }
};

PYBIND11_MODULE(field_provider, handle) {
  handle.doc() = "This is the doc";
//  py::class_<Field>(handle, "Field").def(py::init<Point, double, size_t>());
  py::class_<Bruhnya>(handle, "Bruh").def(py::init<double>()).def("mult", &Bruhnya::mult);
}
