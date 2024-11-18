#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

#include "Field.hpp"
#include "utils.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(provider, handle) {
  handle.doc() = "field provider";
  py::class_<Point>(handle, "PointCPP")
      .def(py::init<double, double>(), "x"_a, "y"_a)
      .def("to_tuple", [](const Point& p) { return py::make_tuple(p.x, p.y); });
  py::class_<Creeper>(handle, "CreeperCPP")
      .def("get_coord", &Creeper::getCoord)
      .def("get_state", &Creeper::getState);
  py::enum_<Creeper::State>(handle, "CreeperStateCPP")
      .value("Born", Creeper::State::Born)
      .value("Walk", Creeper::State::Walk)
      .value("Hissing", Creeper::State::Hissing)
      .value("Explodes", Creeper::State::Explodes)
      .value("Sleep", Creeper::State::Sleep);
  py::enum_<FuncType>(handle, "FieldFuncTypeCPP")
      .value("Polar", FuncType::Polar)
      .value("Euclid", FuncType::Euclid)
      .value("Manhattan", FuncType::Manhattan);
  py::class_<Field>(handle, "FieldCPP")
      .def(py::init<Point, double, size_t, FuncType>(), "size_of_field"_a,
           "explosion_radius"_a, "creepers_num"_a, "func_type"_a)
      .def("update_field", &Field::updateField)
      .def("get_creepers", &Field::getCreepers);
}
