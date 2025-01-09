find_package(GTest REQUIRED)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
include(GoogleTest)

add_subdirectory(creeper-simulation-library)
