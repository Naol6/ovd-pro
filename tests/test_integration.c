#include "unity/unity.h"
#include <stdlib.h>
#include <string.h>
#include "tlvpack/tlvpack.h"

void test_integration_roundtrip_000(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_001(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_002(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_003(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_004(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_005(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_006(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_007(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_008(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_009(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_010(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_011(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_012(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_013(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_014(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_015(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_016(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_017(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_018(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_019(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_020(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_021(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_022(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_023(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_024(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_025(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_026(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_027(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_028(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_029(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_030(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_031(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_032(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_033(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_034(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_035(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_036(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_037(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_038(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_039(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_040(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_041(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_042(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_043(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_044(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_045(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_046(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_047(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_048(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_049(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_050(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_051(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_052(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_053(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_054(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_055(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_056(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_057(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_058(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_059(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_060(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_061(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_062(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_063(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_064(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_065(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_066(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_067(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_068(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_069(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_070(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_071(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_072(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_073(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_074(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_075(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_076(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_077(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_078(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_079(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_080(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_081(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_082(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_083(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_084(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_085(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_086(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_087(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_088(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_089(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_090(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_091(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_092(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_093(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_094(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_095(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_096(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_097(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_098(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_099(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_100(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_101(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_102(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_103(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_104(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_105(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_106(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_107(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_108(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_109(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_110(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_111(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_112(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_113(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_114(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_115(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_116(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_117(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_118(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_119(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}


void test_integration_roundtrip_120(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_121(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_122(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_123(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_124(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_125(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_126(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_127(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_128(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_129(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_130(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_131(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_132(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_133(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_134(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_135(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_136(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_137(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_138(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_139(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_140(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_141(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_142(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_143(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_144(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_145(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_146(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_147(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_148(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_149(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_150(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_151(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_152(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_153(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_154(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_155(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_156(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_157(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_158(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_159(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_160(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_161(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_162(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_163(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_164(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_165(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_166(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_167(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_168(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_169(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_170(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_171(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_172(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_173(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_174(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_175(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_176(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_177(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_178(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_179(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_180(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_181(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_182(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_183(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_184(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_185(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_186(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_187(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_188(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_189(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_190(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_191(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_192(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_193(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_194(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_195(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_196(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_197(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_198(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_199(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_200(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_201(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_202(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_203(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_204(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_205(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_206(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_207(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_208(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_209(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_210(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_211(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_212(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_213(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_214(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_215(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_216(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_217(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_218(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_219(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_220(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_221(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_222(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_223(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_224(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_225(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_226(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_227(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_228(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_229(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_230(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_231(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_232(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_233(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_234(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_235(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_236(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_237(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_238(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_239(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_240(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_241(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_242(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_243(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_244(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_245(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_246(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_247(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_248(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_249(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_250(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_251(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_252(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_253(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_254(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_255(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_256(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_257(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_258(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_259(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_260(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_261(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_262(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_263(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_264(void) {
  const uint8_t src[] = {0x01, 0x03, 0x61, 0x62, 0x63};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(1, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_265(void) {
  const uint8_t src[] = {0x02, 0x02, 0x78, 0x79};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(2, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_266(void) {
  const uint8_t src[] = {0x10, 0x04, 0x64, 0x61, 0x74, 0x61};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(16, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_267(void) {
  const uint8_t src[] = {0x20, 0x03, 0x76, 0x61, 0x6c};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(32, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_268(void) {
  const uint8_t src[] = {0x30, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(48, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}

void test_integration_roundtrip_269(void) {
  const uint8_t src[] = {0x40, 0x04, 0x62, 0x6c, 0x6f, 0x62};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT(64, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}
void test_integration_suite(void) {
  RUN_TEST(test_integration_roundtrip_000);
  RUN_TEST(test_integration_roundtrip_001);
  RUN_TEST(test_integration_roundtrip_002);
  RUN_TEST(test_integration_roundtrip_003);
  RUN_TEST(test_integration_roundtrip_004);
  RUN_TEST(test_integration_roundtrip_005);
  RUN_TEST(test_integration_roundtrip_006);
  RUN_TEST(test_integration_roundtrip_007);
  RUN_TEST(test_integration_roundtrip_008);
  RUN_TEST(test_integration_roundtrip_009);
  RUN_TEST(test_integration_roundtrip_010);
  RUN_TEST(test_integration_roundtrip_011);
  RUN_TEST(test_integration_roundtrip_012);
  RUN_TEST(test_integration_roundtrip_013);
  RUN_TEST(test_integration_roundtrip_014);
  RUN_TEST(test_integration_roundtrip_015);
  RUN_TEST(test_integration_roundtrip_016);
  RUN_TEST(test_integration_roundtrip_017);
  RUN_TEST(test_integration_roundtrip_018);
  RUN_TEST(test_integration_roundtrip_019);
  RUN_TEST(test_integration_roundtrip_020);
  RUN_TEST(test_integration_roundtrip_021);
  RUN_TEST(test_integration_roundtrip_022);
  RUN_TEST(test_integration_roundtrip_023);
  RUN_TEST(test_integration_roundtrip_024);
  RUN_TEST(test_integration_roundtrip_025);
  RUN_TEST(test_integration_roundtrip_026);
  RUN_TEST(test_integration_roundtrip_027);
  RUN_TEST(test_integration_roundtrip_028);
  RUN_TEST(test_integration_roundtrip_029);
  RUN_TEST(test_integration_roundtrip_030);
  RUN_TEST(test_integration_roundtrip_031);
  RUN_TEST(test_integration_roundtrip_032);
  RUN_TEST(test_integration_roundtrip_033);
  RUN_TEST(test_integration_roundtrip_034);
  RUN_TEST(test_integration_roundtrip_035);
  RUN_TEST(test_integration_roundtrip_036);
  RUN_TEST(test_integration_roundtrip_037);
  RUN_TEST(test_integration_roundtrip_038);
  RUN_TEST(test_integration_roundtrip_039);
  RUN_TEST(test_integration_roundtrip_040);
  RUN_TEST(test_integration_roundtrip_041);
  RUN_TEST(test_integration_roundtrip_042);
  RUN_TEST(test_integration_roundtrip_043);
  RUN_TEST(test_integration_roundtrip_044);
  RUN_TEST(test_integration_roundtrip_045);
  RUN_TEST(test_integration_roundtrip_046);
  RUN_TEST(test_integration_roundtrip_047);
  RUN_TEST(test_integration_roundtrip_048);
  RUN_TEST(test_integration_roundtrip_049);
  RUN_TEST(test_integration_roundtrip_050);
  RUN_TEST(test_integration_roundtrip_051);
  RUN_TEST(test_integration_roundtrip_052);
  RUN_TEST(test_integration_roundtrip_053);
  RUN_TEST(test_integration_roundtrip_054);
  RUN_TEST(test_integration_roundtrip_055);
  RUN_TEST(test_integration_roundtrip_056);
  RUN_TEST(test_integration_roundtrip_057);
  RUN_TEST(test_integration_roundtrip_058);
  RUN_TEST(test_integration_roundtrip_059);
  RUN_TEST(test_integration_roundtrip_060);
  RUN_TEST(test_integration_roundtrip_061);
  RUN_TEST(test_integration_roundtrip_062);
  RUN_TEST(test_integration_roundtrip_063);
  RUN_TEST(test_integration_roundtrip_064);
  RUN_TEST(test_integration_roundtrip_065);
  RUN_TEST(test_integration_roundtrip_066);
  RUN_TEST(test_integration_roundtrip_067);
  RUN_TEST(test_integration_roundtrip_068);
  RUN_TEST(test_integration_roundtrip_069);
  RUN_TEST(test_integration_roundtrip_070);
  RUN_TEST(test_integration_roundtrip_071);
  RUN_TEST(test_integration_roundtrip_072);
  RUN_TEST(test_integration_roundtrip_073);
  RUN_TEST(test_integration_roundtrip_074);
  RUN_TEST(test_integration_roundtrip_075);
  RUN_TEST(test_integration_roundtrip_076);
  RUN_TEST(test_integration_roundtrip_077);
  RUN_TEST(test_integration_roundtrip_078);
  RUN_TEST(test_integration_roundtrip_079);
  RUN_TEST(test_integration_roundtrip_080);
  RUN_TEST(test_integration_roundtrip_081);
  RUN_TEST(test_integration_roundtrip_082);
  RUN_TEST(test_integration_roundtrip_083);
  RUN_TEST(test_integration_roundtrip_084);
  RUN_TEST(test_integration_roundtrip_085);
  RUN_TEST(test_integration_roundtrip_086);
  RUN_TEST(test_integration_roundtrip_087);
  RUN_TEST(test_integration_roundtrip_088);
  RUN_TEST(test_integration_roundtrip_089);
  RUN_TEST(test_integration_roundtrip_090);
  RUN_TEST(test_integration_roundtrip_091);
  RUN_TEST(test_integration_roundtrip_092);
  RUN_TEST(test_integration_roundtrip_093);
  RUN_TEST(test_integration_roundtrip_094);
  RUN_TEST(test_integration_roundtrip_095);
  RUN_TEST(test_integration_roundtrip_096);
  RUN_TEST(test_integration_roundtrip_097);
  RUN_TEST(test_integration_roundtrip_098);
  RUN_TEST(test_integration_roundtrip_099);
  RUN_TEST(test_integration_roundtrip_100);
  RUN_TEST(test_integration_roundtrip_101);
  RUN_TEST(test_integration_roundtrip_102);
  RUN_TEST(test_integration_roundtrip_103);
  RUN_TEST(test_integration_roundtrip_104);
  RUN_TEST(test_integration_roundtrip_105);
  RUN_TEST(test_integration_roundtrip_106);
  RUN_TEST(test_integration_roundtrip_107);
  RUN_TEST(test_integration_roundtrip_108);
  RUN_TEST(test_integration_roundtrip_109);
  RUN_TEST(test_integration_roundtrip_110);
  RUN_TEST(test_integration_roundtrip_111);
  RUN_TEST(test_integration_roundtrip_112);
  RUN_TEST(test_integration_roundtrip_113);
  RUN_TEST(test_integration_roundtrip_114);
  RUN_TEST(test_integration_roundtrip_115);
  RUN_TEST(test_integration_roundtrip_116);
  RUN_TEST(test_integration_roundtrip_117);
  RUN_TEST(test_integration_roundtrip_118);
  RUN_TEST(test_integration_roundtrip_119);
  RUN_TEST(test_integration_roundtrip_269);
  RUN_TEST(test_integration_roundtrip_268);
  RUN_TEST(test_integration_roundtrip_267);
  RUN_TEST(test_integration_roundtrip_266);
  RUN_TEST(test_integration_roundtrip_265);
  RUN_TEST(test_integration_roundtrip_264);
  RUN_TEST(test_integration_roundtrip_263);
  RUN_TEST(test_integration_roundtrip_262);
  RUN_TEST(test_integration_roundtrip_261);
  RUN_TEST(test_integration_roundtrip_260);
  RUN_TEST(test_integration_roundtrip_259);
  RUN_TEST(test_integration_roundtrip_258);
  RUN_TEST(test_integration_roundtrip_257);
  RUN_TEST(test_integration_roundtrip_256);
  RUN_TEST(test_integration_roundtrip_255);
  RUN_TEST(test_integration_roundtrip_254);
  RUN_TEST(test_integration_roundtrip_253);
  RUN_TEST(test_integration_roundtrip_252);
  RUN_TEST(test_integration_roundtrip_251);
  RUN_TEST(test_integration_roundtrip_250);
  RUN_TEST(test_integration_roundtrip_249);
  RUN_TEST(test_integration_roundtrip_248);
  RUN_TEST(test_integration_roundtrip_247);
  RUN_TEST(test_integration_roundtrip_246);
  RUN_TEST(test_integration_roundtrip_245);
  RUN_TEST(test_integration_roundtrip_244);
  RUN_TEST(test_integration_roundtrip_243);
  RUN_TEST(test_integration_roundtrip_242);
  RUN_TEST(test_integration_roundtrip_241);
  RUN_TEST(test_integration_roundtrip_240);
  RUN_TEST(test_integration_roundtrip_239);
  RUN_TEST(test_integration_roundtrip_238);
  RUN_TEST(test_integration_roundtrip_237);
  RUN_TEST(test_integration_roundtrip_236);
  RUN_TEST(test_integration_roundtrip_235);
  RUN_TEST(test_integration_roundtrip_234);
  RUN_TEST(test_integration_roundtrip_233);
  RUN_TEST(test_integration_roundtrip_232);
  RUN_TEST(test_integration_roundtrip_231);
  RUN_TEST(test_integration_roundtrip_230);
  RUN_TEST(test_integration_roundtrip_229);
  RUN_TEST(test_integration_roundtrip_228);
  RUN_TEST(test_integration_roundtrip_227);
  RUN_TEST(test_integration_roundtrip_226);
  RUN_TEST(test_integration_roundtrip_225);
  RUN_TEST(test_integration_roundtrip_224);
  RUN_TEST(test_integration_roundtrip_223);
  RUN_TEST(test_integration_roundtrip_222);
  RUN_TEST(test_integration_roundtrip_221);
  RUN_TEST(test_integration_roundtrip_220);
  RUN_TEST(test_integration_roundtrip_219);
  RUN_TEST(test_integration_roundtrip_218);
  RUN_TEST(test_integration_roundtrip_217);
  RUN_TEST(test_integration_roundtrip_216);
  RUN_TEST(test_integration_roundtrip_215);
  RUN_TEST(test_integration_roundtrip_214);
  RUN_TEST(test_integration_roundtrip_213);
  RUN_TEST(test_integration_roundtrip_212);
  RUN_TEST(test_integration_roundtrip_211);
  RUN_TEST(test_integration_roundtrip_210);
  RUN_TEST(test_integration_roundtrip_209);
  RUN_TEST(test_integration_roundtrip_208);
  RUN_TEST(test_integration_roundtrip_207);
  RUN_TEST(test_integration_roundtrip_206);
  RUN_TEST(test_integration_roundtrip_205);
  RUN_TEST(test_integration_roundtrip_204);
  RUN_TEST(test_integration_roundtrip_203);
  RUN_TEST(test_integration_roundtrip_202);
  RUN_TEST(test_integration_roundtrip_201);
  RUN_TEST(test_integration_roundtrip_200);
  RUN_TEST(test_integration_roundtrip_199);
  RUN_TEST(test_integration_roundtrip_198);
  RUN_TEST(test_integration_roundtrip_197);
  RUN_TEST(test_integration_roundtrip_196);
  RUN_TEST(test_integration_roundtrip_195);
  RUN_TEST(test_integration_roundtrip_194);
  RUN_TEST(test_integration_roundtrip_193);
  RUN_TEST(test_integration_roundtrip_192);
  RUN_TEST(test_integration_roundtrip_191);
  RUN_TEST(test_integration_roundtrip_190);
  RUN_TEST(test_integration_roundtrip_189);
  RUN_TEST(test_integration_roundtrip_188);
  RUN_TEST(test_integration_roundtrip_187);
  RUN_TEST(test_integration_roundtrip_186);
  RUN_TEST(test_integration_roundtrip_185);
  RUN_TEST(test_integration_roundtrip_184);
  RUN_TEST(test_integration_roundtrip_183);
  RUN_TEST(test_integration_roundtrip_182);
  RUN_TEST(test_integration_roundtrip_181);
  RUN_TEST(test_integration_roundtrip_180);
  RUN_TEST(test_integration_roundtrip_179);
  RUN_TEST(test_integration_roundtrip_178);
  RUN_TEST(test_integration_roundtrip_177);
  RUN_TEST(test_integration_roundtrip_176);
  RUN_TEST(test_integration_roundtrip_175);
  RUN_TEST(test_integration_roundtrip_174);
  RUN_TEST(test_integration_roundtrip_173);
  RUN_TEST(test_integration_roundtrip_172);
  RUN_TEST(test_integration_roundtrip_171);
  RUN_TEST(test_integration_roundtrip_170);
  RUN_TEST(test_integration_roundtrip_169);
  RUN_TEST(test_integration_roundtrip_168);
  RUN_TEST(test_integration_roundtrip_167);
  RUN_TEST(test_integration_roundtrip_166);
  RUN_TEST(test_integration_roundtrip_165);
  RUN_TEST(test_integration_roundtrip_164);
  RUN_TEST(test_integration_roundtrip_163);
  RUN_TEST(test_integration_roundtrip_162);
  RUN_TEST(test_integration_roundtrip_161);
  RUN_TEST(test_integration_roundtrip_160);
  RUN_TEST(test_integration_roundtrip_159);
  RUN_TEST(test_integration_roundtrip_158);
  RUN_TEST(test_integration_roundtrip_157);
  RUN_TEST(test_integration_roundtrip_156);
  RUN_TEST(test_integration_roundtrip_155);
  RUN_TEST(test_integration_roundtrip_154);
  RUN_TEST(test_integration_roundtrip_153);
  RUN_TEST(test_integration_roundtrip_152);
  RUN_TEST(test_integration_roundtrip_151);
  RUN_TEST(test_integration_roundtrip_150);
  RUN_TEST(test_integration_roundtrip_149);
  RUN_TEST(test_integration_roundtrip_148);
  RUN_TEST(test_integration_roundtrip_147);
  RUN_TEST(test_integration_roundtrip_146);
  RUN_TEST(test_integration_roundtrip_145);
  RUN_TEST(test_integration_roundtrip_144);
  RUN_TEST(test_integration_roundtrip_143);
  RUN_TEST(test_integration_roundtrip_142);
  RUN_TEST(test_integration_roundtrip_141);
  RUN_TEST(test_integration_roundtrip_140);
  RUN_TEST(test_integration_roundtrip_139);
  RUN_TEST(test_integration_roundtrip_138);
  RUN_TEST(test_integration_roundtrip_137);
  RUN_TEST(test_integration_roundtrip_136);
  RUN_TEST(test_integration_roundtrip_135);
  RUN_TEST(test_integration_roundtrip_134);
  RUN_TEST(test_integration_roundtrip_133);
  RUN_TEST(test_integration_roundtrip_132);
  RUN_TEST(test_integration_roundtrip_131);
  RUN_TEST(test_integration_roundtrip_130);
  RUN_TEST(test_integration_roundtrip_129);
  RUN_TEST(test_integration_roundtrip_128);
  RUN_TEST(test_integration_roundtrip_127);
  RUN_TEST(test_integration_roundtrip_126);
  RUN_TEST(test_integration_roundtrip_125);
  RUN_TEST(test_integration_roundtrip_124);
  RUN_TEST(test_integration_roundtrip_123);
  RUN_TEST(test_integration_roundtrip_122);
  RUN_TEST(test_integration_roundtrip_121);
  RUN_TEST(test_integration_roundtrip_120);
}
