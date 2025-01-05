poetry run conan profile detect --force
poetry run conan install . --output-folder=build/conan --build=missing --settings=build_type=Debug
