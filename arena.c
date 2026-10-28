#include "arena.h"
#include <stdlib.h>
#include <string.h>
void tlv_arena_init(tlv_arena_t *a) { a->data = NULL; a->len = 0; a->cap = 0; }
void tlv_arena_free(tlv_arena_t *a) { free(a->data); a->data = NULL; a->len = a->cap = 0; }
char *tlv_arena_alloc(tlv_arena_t *a, size_t n) {
  size_t need = a->len + n;
  if (need > a->cap) {
    size_t cap = a->cap ? a->cap * 2 : 64;
    while (cap < need) cap *= 2;
    char *p = (char *)realloc(a->data, cap);
    if (!p) return NULL;
    a->data = p; a->cap = cap;
  }
  char *slot = a->data + a->len;
  a->len += n;
  return slot;
}
