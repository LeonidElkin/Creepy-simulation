#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "Field.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(field_provider, handle) {
  handle.doc() = "field provider";
  py::class_<Point>(handle, "Point")
      .def(py::init<double, double>(), "x"_a, "y"_a)
      .def("to_tuple", [](const Point& p) { return py::make_tuple(p.x, p.y); });
  py::class_<Creeper>(handle, "Creeper")
      .def("get_coord", &Creeper::getCoord)
      .def("get_state", &Creeper::getState);
  py::enum_<Creeper::State>(handle, "CreeperState")
      .value("Born", Creeper::State::Born)
      .value("Walk", Creeper::State::Walk)
      .value("Hissing", Creeper::State::Hissing)
      .value("Explodes", Creeper::State::Explodes);
  py::class_<Field>(handle, "Field")
      .def(py::init<Point, double, size_t>(), "size_of_field"_a,
           "creepers_num"_a, "explosion_radius"_a)
      .def("update_field", &Field::updateField)
      .def("get_creepers", &Field::getCreepers);
}
