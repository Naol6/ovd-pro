#include "tlvpack/tlvpack.h"
#include "unity/unity.h"
#include <stdlib.h>
void test_merge_trees(void) {
  uint8_t a[] = {0x01, 0x01, 'x'};
  uint8_t b[] = {0x02, 0x01, 'y'};
  tlv_tree_t *ta = NULL, *tb = NULL;
  tlv_error_t e;
  tlv_parse_buffer(a, sizeof(a), &ta, &e);
  tlv_parse_buffer(b, sizeof(b), &tb, &e);
  tlv_merge_trees(ta, tb);
  tlv_tree_free(ta); free(ta);
  tlv_tree_free(tb); free(tb);
}
