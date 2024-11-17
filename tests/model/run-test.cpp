#include <glog/logging.h>
#include <gtest/gtest.h>

int main(int argc, char *argv[]) {
  google::InitGoogleLogging(*argv);
  FLAGS_alsologtostderr = true;
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
