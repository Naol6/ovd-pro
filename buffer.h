#ifndef TLV_BUFFER_H
#define TLV_BUFFER_H
#include <stddef.h>
#include <stdint.h>
typedef struct { uint8_t *data; size_t len; size_t cap; } tlv_buffer_t;
void tlv_buffer_init(tlv_buffer_t *b);
void tlv_buffer_free(tlv_buffer_t *b);
int tlv_buffer_append(tlv_buffer_t *b, const uint8_t *p, size_t n);
#endif
