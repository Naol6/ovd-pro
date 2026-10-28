#include "collector.h"
#include "node.h"
#include "buffer.h"
#include "varint.h"
#include <stdlib.h>
#include <string.h>

int tlv_collector_init(tlv_collector_ctx_t *ctx) {
  if (!ctx) return -1;
  memset(ctx, 0, sizeof(*ctx));
  return 0;
}

void tlv_collector_free(tlv_collector_ctx_t *ctx) {
  size_t i;
  if (!ctx) return;
  for (i = 0; i < ctx->slot_count; i++) free(ctx->slots[i].label);
  free(ctx->slots);
  free(ctx->scratch);
  ctx->slots = NULL;
  ctx->scratch = NULL;
  ctx->slot_count = ctx->slot_cap = ctx->scratch_len = 0;
}

static int collector_grow(tlv_collector_ctx_t *ctx) {
  size_t cap = ctx->slot_cap ? ctx->slot_cap * 2 : 8;
  tlv_collector_slot_t *next = (tlv_collector_slot_t *)realloc(ctx->slots, cap * sizeof(*next));
  if (!next) return -1;
  ctx->slots = next;
  ctx->slot_cap = cap;
  return 0;
}

int tlv_collector_track(tlv_collector_ctx_t *ctx, uint32_t tag, const char *label) {
  tlv_collector_slot_t *slot;
  if (!ctx) return -1;
  if (ctx->slot_count >= ctx->slot_cap && collector_grow(ctx) != 0) return -1;
  slot = &ctx->slots[ctx->slot_count++];
  slot->tag = tag;
  slot->hits = 0;
  slot->label = label ? strdup(label) : NULL;
  return 0;
}

static void collector_bump(tlv_collector_ctx_t *ctx, uint32_t tag) {
  size_t i;
  for (i = 0; i < ctx->slot_count; i++)
    if (ctx->slots[i].tag == tag) ctx->slots[i].hits++;
}

static int collector_walk(const tlv_node_t *n, tlv_collector_ctx_t *ctx, uint32_t depth) {
  size_t i;
  if (!n || !ctx) return -1;
  if (depth > ctx->max_depth) { ctx->truncated++; return 0; }
  ctx->nodes_seen++;
  collector_bump(ctx, n->tag);
  ctx->bytes_seen += n->value_len;
  for (i = 0; i < n->child_count; i++)
    if (collector_walk(&n->children[i], ctx, depth + 1) != 0) return -1;
  return 0;
}

int tlv_collector_scan_tree(const tlv_tree_t *tree, tlv_collector_ctx_t *ctx) {
  size_t i;
  if (!tree || !ctx) return -1;
  for (i = 0; i < tree->root_count; i++)
    if (collector_walk(&tree->roots[i], ctx, 0) != 0) return -1;
  return 0;
}

int tlv_collector_reserve(tlv_collector_ctx_t *ctx, size_t need) {
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

size_t tlv_collector_slot_count(const tlv_collector_ctx_t *ctx) {
  return ctx ? ctx->slot_count : 0;
}

uint64_t tlv_collector_hits_for(const tlv_collector_ctx_t *ctx, uint32_t tag) {
  size_t i;
  if (!ctx) return 0;
  for (i = 0; i < ctx->slot_count; i++)
    if (ctx->slots[i].tag == tag) return ctx->slots[i].hits;
  return 0;
}
