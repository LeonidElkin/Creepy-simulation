import os
import subprocess


class CMakeBuild(build_ext):
    def run(self):
        build_dir = os.path.abspath(self.build_temp)
        os.makedirs(build_dir, exist_ok=True)

        subprocess.check_call(["cmake", "-S", "model", "-B", build_dir])
        subprocess.check_call(["cmake", "--build", build_dir])

        output_dir = os.path.abspath(self.build_lib)
        os.makedirs(output_dir, exist_ok=True)
        for file in os.listdir(os.path.join(build_dir, "pybind")):
            if file.endswith(".so"):
                self.copy_file(
                    os.path.join(build_dir, "pybind", file),
                    os.path.join(output_dir, file),
                )
