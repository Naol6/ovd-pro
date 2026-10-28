#ifndef TLV_ARENA_H
#define TLV_ARENA_H
#include <stddef.h>
typedef struct { char *data; size_t len; size_t cap; } tlv_arena_t;
void tlv_arena_init(tlv_arena_t *a);
void tlv_arena_free(tlv_arena_t *a);
char *tlv_arena_alloc(tlv_arena_t *a, size_t n);
#endif
