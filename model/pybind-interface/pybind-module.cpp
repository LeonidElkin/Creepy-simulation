#include <glog/logging.h>
#include <glog/types.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <future>
#include <iostream>
#include <vector>

#include "Simulation.hpp"
#include "SimulationFabric.hpp"
#include "utils/utils.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

[[nodiscard]] static Rectangle boundsToRectangle(const py::tuple& leftDownBound, const py::tuple& rightUpBound) {
  return {{leftDownBound[0].cast<double>(), leftDownBound[1].cast<double>()},
          {rightUpBound[0].cast<double>(), rightUpBound[1].cast<double>()}};
}

class SimulationProvider {
  Simulation original_;
  volatile bool algoRunning_ = false;
  volatile bool dataReady_ = true;
  std::jthread thread_;

 public:
  explicit SimulationProvider(Simulation simulation) : original_(std::move(simulation)) {
    thread_ = std::jthread([this](const std::stop_token& stopToken) {
      while (true) {
        if (stopToken.stop_requested()) {
          return;
        }
        if (algoRunning_) {
          DLOG(INFO) << "Start algo update";
          original_.updateField();
          DLOG(INFO) << "End algo update";
          algoRunning_ = false;
          dataReady_ = true;
        } else {
          std::this_thread::yield();
        }
      }
    });
  }

  auto runUpdateSimulation() {
    if (algoRunning_) {
      throw std::runtime_error("Field is already updating");
    }
    dataReady_ = false;
    algoRunning_ = true;
  }

  void waitUpdateSimulation() const {
    while (!dataReady_) {
    }
  }

  [[nodiscard]] bool dataIsReady() const { return dataReady_; }

  CreepersManager& getCreepersManager() {
    if (!dataReady_) {
      throw std::runtime_error("SimulationProvider::getCreepersManager() called while data is updating");
    }
    return original_.getCreepersManager();
  }
  StevesManager& getStevesManager() {
    if (!dataReady_) {
      throw std::runtime_error("SimulationProvider::getStevesManager() called while data is updating");
    }
    return original_.getStevesManager();
  }

  void setBedrock(const py::tuple& leftDownBound, const py::tuple& rightUpBound) {
    if (!dataReady_) {
      throw std::runtime_error("SimulationProvider::setBedrock() called while data is updating");
    }
    original_.setBedrock(boundsToRectangle(leftDownBound, rightUpBound));
  }

  void deleteBedrock(const py::tuple& leftDownBound, const py::tuple& rightUpBound) {
    if (!dataReady_) {
      throw std::runtime_error("SimulationProvider::deleteBedrock() called while data is updating");
    }
    original_.deleteBedrock(boundsToRectangle(leftDownBound, rightUpBound));
  }
};

PYBIND11_MODULE(creepers_lib, handle) {
  handle.doc() = "pybind module to provide field from creeper-simulation-library";

  if (!google::IsGoogleLoggingInitialized()) {
    google::InitGoogleLogging("creepers_lib");
    FLAGS_logtostderr = 1;                                   // Вывод логов в stderr
    FLAGS_stderrthreshold = google::LogSeverity::GLOG_INFO;  // Уровень логирования для stderr
#ifdef DEBUG
    google::SetStderrLogging(google::LogSeverity::GLOG_INFO);
#endif
  }

  py::enum_<StevesParams::State>(handle, "SteveState")
      .value("Walk", StevesParams::State::Walk)
      .value("Dead", StevesParams::State::Dead);
  py::class_<Steve, std::shared_ptr<Steve>>(handle, "Steve")
      .def("get_coord",
           [](const Steve& steve) {
             auto p = steve.getCoord();
             return py::make_tuple(p.x, p.y);
           })
      .def("get_state", &Steve::getState);
  py::class_<StevesManager>(handle, "SteveManager").def("get_steves", &StevesManager::getSteves);

  py::enum_<CreepersParams::State>(handle, "CreeperState")
      .value("Born", CreepersParams::State::Born)
      .value("Walk", CreepersParams::State::Walk)
      .value("Hissing", CreepersParams::State::Hissing)
      .value("Explodes", CreepersParams::State::Explodes)
      .value("Dead", CreepersParams::State::Dead)
      .value("Sleep", CreepersParams::State::Sleep)
      .value("GoToSteve", CreepersParams::State::GoToSteve)
      .value("Bonk", CreepersParams::State::Bonk);
  py::class_<Creeper, std::shared_ptr<Creeper>>(handle, "Creeper")
      .def("get_coord",
           [](const Creeper& creeper) {
             auto p = creeper.getCoord();
             return py::make_tuple(p.x, p.y);
           })
      .def("get_state", &Creeper::getState);
  py::class_<CreepersManager>(handle, "CreepersManager").def("get_creepers", &CreepersManager::getCreepers);

  py::class_<SimulationFabric>(handle, "SimulationFabric")
      .def(py::init<>())
      .def(
          "set_field_params",
          [](SimulationFabric& fabric, const py::tuple& leftDownBound, const py::tuple& rightUpBound,
             const DistanceFunc::Type distanceFunc) {
            return fabric.setFieldParams(boundsToRectangle(leftDownBound, rightUpBound), funcToType(distanceFunc));
          },
          "left_down_bound"_a, "right_up_bound"_a, "distance_func"_a)
      .def("set_creeper_params", &SimulationFabric::setCreeperParams, "move_radius"_a, "explode_radius"_a, "count"_a)
      .def("set_steve_params", &SimulationFabric::setSteveParams, "move_radius"_a, "count"_a)
      .def(
          "set_bedrock",
          [](SimulationFabric& fabric, const py::tuple& leftDownBound, const py::tuple& rightUpBound) {
            return fabric.setBedrock(boundsToRectangle(leftDownBound, rightUpBound));
          },
          "left_down_bound"_a, "right_up_bound"_a)
      .def("build", [](SimulationFabric& fabric) { return std::make_shared<SimulationProvider>(fabric.build()); });
  py::class_<SimulationProvider, std::shared_ptr<SimulationProvider>>(handle, "Simulation")
      .def("run_update_field", &SimulationProvider::runUpdateSimulation)
      .def("wait_update_field", &SimulationProvider::waitUpdateSimulation)
      .def("data_is_ready", &SimulationProvider::dataIsReady)
      .def("get_creepers_manager", &SimulationProvider::getCreepersManager)
      .def("get_steves_manager", &SimulationProvider::getStevesManager)
      .def("set_bedrock", &SimulationProvider::setBedrock, "left_down_bound"_a, "right_up_bound"_a)
      .def("delete_bedrock", &SimulationProvider::deleteBedrock, "left_down_bound"_a, "right_up_bound"_a);
  py::enum_<DistanceFunc::Type>(handle, "DistFunc")
      .value("Polar", DistanceFunc::Type::Polar)
      .value("Euclid", DistanceFunc::Type::Euclid)
      .value("Manhattan", DistanceFunc::Type::Manhattan);
}
