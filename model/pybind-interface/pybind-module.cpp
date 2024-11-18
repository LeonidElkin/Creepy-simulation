#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <vector>

#include "Field.hpp"
#include "utils.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(creepers, handle) {
  handle.doc() =
      "pybind module to provide Field from creeper-simulation-library";
  py::class_<Creeper>(handle, "Creeper")
      .def("get_coord",
           [](const Creeper& creeper) {
             auto p = creeper.getCoord();
             return py::make_tuple(p.x, p.y);
           })
      .def("get_state", &Creeper::getState);
  py::enum_<Creeper::State>(handle, "CreeperState")
      .value("Born", Creeper::State::Born)
      .value("Walk", Creeper::State::Walk)
      .value("Hissing", Creeper::State::Hissing)
      .value("Explodes", Creeper::State::Explodes)
      .value("Sleep", Creeper::State::Sleep);
  py::class_<Field>(handle, "Field")
      .def(py::init([](const py::tuple& point, double r0, size_t creepersNum,
                       double moveRadius, FuncType type) {
             return Field(
                 {.x = point[0].cast<double>(), .y = point[1].cast<double>()},
                 r0, creepersNum, moveRadius, type);
           }),
           "size_of_field"_a, "explosion_radius"_a, "creepers_num"_a
           "move_radius"_a, "func_type"_a)
      .def("update_field", &Field::updateField)
      .def("get_creepers", &Field::getCreepers);
  py::enum_<FuncType>(handle, "DistFunc")
      .value("Polar", FuncType::Polar)
      .value("Euclid", FuncType::Euclid)
      .value("Manhattan", FuncType::Manhattan);
}
