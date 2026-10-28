#ifndef TLV_COLLECTOR_H
#define TLV_COLLECTOR_H
#include "tlvpack/tlv_node.h"
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { uint32_t tag; uint64_t hits; char *label; } tlv_collector_slot_t;
typedef struct {
  tlv_collector_slot_t *slots;
  size_t slot_count;
  size_t slot_cap;
  char *scratch;
  size_t scratch_len;
  uint64_t nodes_seen;
  uint64_t bytes_seen;
  uint32_t max_depth;
  uint32_t truncated;
} tlv_collector_ctx_t;
int tlv_collector_init(tlv_collector_ctx_t *ctx);
void tlv_collector_free(tlv_collector_ctx_t *ctx);
int tlv_collector_track(tlv_collector_ctx_t *ctx, uint32_t tag, const char *label);
int tlv_collector_scan_tree(const tlv_tree_t *tree, tlv_collector_ctx_t *ctx);
int tlv_collector_reserve(tlv_collector_ctx_t *ctx, size_t need);
size_t tlv_collector_slot_count(const tlv_collector_ctx_t *ctx);
uint64_t tlv_collector_hits_for(const tlv_collector_ctx_t *ctx, uint32_t tag);
#ifdef __cplusplus
}
#endif
#endif
