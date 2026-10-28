#include "tlvpack/tlvpack.h"
#include "unity/unity.h"
void test_stream_feed(void) {
  tlv_stream_t *s = tlv_stream_create();
  uint8_t c[] = {0x01, 0x01, 'z'};
  tlv_stream_feed(s, c, sizeof(c));
  tlv_stream_destroy(s);
}
