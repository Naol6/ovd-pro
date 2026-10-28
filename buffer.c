#include "buffer.h"
#include <stdlib.h>
#include <string.h>
void tlv_buffer_init(tlv_buffer_t *b) { b->data = NULL; b->len = b->cap = 0; }
void tlv_buffer_free(tlv_buffer_t *b) { free(b->data); b->data = NULL; b->len = b->cap = 0; }
int tlv_buffer_append(tlv_buffer_t *b, const uint8_t *p, size_t n) {
  if (b->len + n > b->cap) {
    size_t cap = b->cap ? b->cap * 2 : 64;
    while (cap < b->len + n) cap *= 2;
    uint8_t *next = (uint8_t *)realloc(b->data, cap);
    if (!next) return -1;
    b->data = next; b->cap = cap;
  }
  memcpy(b->data + b->len, p, n);
  b->len += n;
  return 0;
}
