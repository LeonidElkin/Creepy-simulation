#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <future>
#include <vector>

#include "Simulation.hpp"
#include "SimulationParams.hpp"
#include "utils/utils.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

class SimulationParamsProvider {
  SimulationParams params_;

 public:
  SimulationParamsProvider() = default;

  SimulationParams& getOrigParams() {return params_;}

  SimulationParamsProvider& setFieldParams(const py::tuple& leftDownBound, const py::tuple& rightUpBound,
                                           const DistanceFunc::Type distanceFunc) {
    params_.setFieldParams({leftDownBound[0].cast<double>(), leftDownBound[1].cast<double>()},
                           {rightUpBound[0].cast<double>(), rightUpBound[1].cast<double>()}, funcToType(distanceFunc));
    return *this;
  }

  SimulationParamsProvider& setCreeperParams(double moveRadius, double explodeRadius, uint32_t count) {
    params_.setCreeperParams(moveRadius, explodeRadius, count);
    return *this;
  }

  SimulationParamsProvider& setSteveParams(double moveRadius, uint32_t count) {
    params_.setSteveParams(moveRadius, count);
    return *this;
  }
};

class SimulationProvider {
  Simulation field_;
  std::optional<std::future<void>> future_;

 public:
  SimulationProvider(SimulationParamsProvider& simulationParams) : field_(simulationParams.getOrigParams()) {}

  auto runUpdateSimulation() {
    future_ = std::async(std::launch::async, [this] { field_.updateField(); });
  }

  void waitUpdateSimulation() const { future_->wait(); }

  auto getCreepers() const { return field_.getCreepers(); }
  auto getSteves() const { return field_.getSteves(); }
};

PYBIND11_MODULE(creepers, handle) {
  handle.doc() = "pybind module to provide field from creeper-simulation-library";
  py::class_<Creeper>(handle, "Creeper")
      .def("get_coord",
           [](const Creeper& creeper) {
             auto p = creeper.getCoord();
             return py::make_tuple(p.x, p.y);
           })
      .def("get_state", &Creeper::getState);
  py::enum_<StevesParams::State>(handle, "SteveState").value("Born", StevesParams::State::Born);
  py::class_<Steve>(handle, "Steve")
      .def("get_coord",
           [](const Steve& steve) {
             auto p = steve.getCoord();
             return py::make_tuple(p.x, p.y);
           })
      .def("get_state", &Steve::getState);
  py::enum_<CreepersParams::State>(handle, "CreeperState")
      .value("Born", CreepersParams::State::Born)
      .value("Walk", CreepersParams::State::Walk)
      .value("Hissing", CreepersParams::State::Hissing)
      .value("Explodes", CreepersParams::State::Explodes)
      .value("Sleep", CreepersParams::State::Sleep);
  py::class_<SimulationParamsProvider>(handle, "SimulationParams")
      .def(py::init<>())
      .def("set_field_params", &SimulationParamsProvider::setFieldParams, "left_down_bound"_a, "right_up_bound"_a,
           "distance_func"_a)
      .def("set_creeper_params", &SimulationParamsProvider::setCreeperParams, "move_radius"_a, "explode_radius"_a,
           "count"_a)
      .def("set_steve_params", &SimulationParamsProvider::setSteveParams, "move_radius"_a, "count"_a);
  py::class_<SimulationProvider>(handle, "Simulation")
      .def(py::init<SimulationParamsProvider&>(), "simulation_params"_a)
      .def("run_update_field", &SimulationProvider::runUpdateSimulation)
      .def("wait_update_field", &SimulationProvider::waitUpdateSimulation)
      .def("get_creepers", &SimulationProvider::getCreepers)
      .def("get_steves", &SimulationProvider::getSteves);
  py::enum_<DistanceFunc::Type>(handle, "DistFunc")
      .value("Polar", DistanceFunc::Type::Polar)
      .value("Euclid", DistanceFunc::Type::Euclid)
      .value("Manhattan", DistanceFunc::Type::Manhattan);
}
