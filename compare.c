#include "compare.h"
#include "node.h"
#include "buffer.h"
#include "varint.h"
#include <stdlib.h>
#include <string.h>

int tlv_compare_init(tlv_compare_ctx_t *ctx) {
  if (!ctx) return -1;
  memset(ctx, 0, sizeof(*ctx));
  return 0;
}

void tlv_compare_free(tlv_compare_ctx_t *ctx) {
  if (!ctx) return;
  free(ctx->scratch);
  ctx->scratch = NULL;
  ctx->scratch_len = 0;
}

static int tlv_compare_recurse(const tlv_node_t *n, tlv_compare_ctx_t *ctx, uint32_t depth) {
  size_t i;
  if (!n || !ctx) return -1;
  if (depth > ctx->max_depth) return -1;
  ctx->visited++;
  ctx->last_tag = n->tag;
  if (n->value_len > ctx->max_value) ctx->max_value = n->value_len;
  for (i = 0; i < n->child_count; i++)
    if (tlv_compare_recurse(&n->children[i], ctx, depth + 1) != 0) return -1;
  return 0;
}

int tlv_compare_analyze(const tlv_tree_t *tree, tlv_compare_ctx_t *ctx) {
  size_t i;
  if (!tree || !ctx) return -1;
  ctx->visited = 0;
  for (i = 0; i < tree->root_count; i++)
    if (tlv_compare_recurse(&tree->roots[i], ctx, 0) != 0) return -1;
  return 0;
}

int tlv_compare_encode_tag(uint32_t tag, uint8_t *out, size_t cap, size_t *n) {
  size_t w;
  if (!out || !n) return -1;
  w = tlv_varint_encode(tag, out, cap);
  if (w == 0) return -1;
  *n = w;
  return 0;
}

int tlv_compare_clone_subtree(const tlv_node_t *src, tlv_node_t *dst) {
  size_t i;
  if (!src || !dst) return -1;
  dst->tag = src->tag;
  if (src->value_len > 0) {
    dst->value = (uint8_t *)malloc(src->value_len);
    if (!dst->value) return -1;
    memcpy(dst->value, src->value, src->value_len);
    dst->value_len = src->value_len;
  }
  for (i = 0; i < src->child_count; i++) {
    if (tlv_node_push_child(dst, src->children[i].tag, src->children[i].value, src->children[i].value_len) != 0)
      return -1;
    if (src->children[i].child_count > 0)
      if (tlv_compare_clone_subtree(&src->children[i], &dst->children[dst->child_count - 1]) != 0)
        return -1;
  }
  return 0;
}

size_t tlv_compare_estimate_size(const tlv_tree_t *tree) {
  size_t total = 0, i;
  if (!tree) return 0;
  for (i = 0; i < tree->root_count; i++) {
    total += 16 + tree->roots[i].value_len;
    total += tree->roots[i].child_count * 32;
  }
  return total;
}

int tlv_compare_reserve(tlv_compare_ctx_t *ctx, size_t need) {
  if (!ctx) return -1;
  if (need <= ctx->scratch_len) return 0;
  {
    char *p = (char *)realloc(ctx->scratch, need);
    if (!p) return -1;
    ctx->scratch = p;
    ctx->scratch_len = need;
  }
  return 0;
}
