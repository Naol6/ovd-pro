#include "tlvpack/tlvpack.h"
#include "unity/unity.h"
#include <stdlib.h>
void test_basic_parse(void) {
  uint8_t blob[] = {0x01, 0x03, 'a', 'b', 'c'};
  tlv_tree_t *t = NULL;
  tlv_error_t e;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(blob, sizeof(blob), &t, &e));
  tlv_tree_free(t); free(t);
}
