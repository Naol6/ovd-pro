#include "unity/unity.h"
extern void test_basic_parse(void);
extern void test_merge_trees(void);
extern void test_stream_feed(void);
extern void test_integration_suite(void);
int main(void) {
  UnityBegin("tlvpack");
  test_basic_parse();
  test_merge_trees();
  test_stream_feed();
  test_integration_suite();
  return UnityEnd();
}
