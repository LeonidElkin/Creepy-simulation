add_executable(creeper-simulation-test field-tests.cpp creeper-tests.cpp)
target_include_directories(creeper-simulation-test PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(creeper-simulation-test PUBLIC GTest::gtest_main creeper-simulation-library)

gtest_discover_tests(creeper-simulation-test)
