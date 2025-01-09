import shutil
import subprocess
from pathlib import Path

import click

build_dir = Path(__file__).parent


@click.command()
@click.option("-d", "--debug", is_flag=True, default=False, help="Turn on debug build mod")
def run_conan_build(debug):
    build_mode = "Debug" if debug else "Release"
    print(f"Build mode: {build_mode}, building path: {build_dir}")
    subprocess.run(["conan", "build", ".", f"--settings=build_type={build_mode}"], check=True, cwd=build_dir)
    print("Conan build completed.")


def clean():
    shutil.rmtree(Path(build_dir).joinpath("build"))
