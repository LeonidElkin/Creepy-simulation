from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain


class CreepersLib(ConanFile):
    name = "creepers_lib"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"
    requires = "glog/[>=0.7.1]", "gtest/[>=1.15.0]", "pybind11/[>=1.13.0]"
    build_policy = "missing"
    build_requires = "ninja/[>=1.11.1]"

    def layout(self):
        self.folders.source = "."
        self.folders.build = "build"
        self.folders.package = "build"
        self.folders.generators = "build"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()
