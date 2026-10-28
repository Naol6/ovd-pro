#ifndef TLV_DECODER_H
#define TLV_DECODER_H
#include "tlvpack/tlv_node.h"
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { uint32_t tag; uint64_t hits; char *label; } tlv_decoder_slot_t;
typedef struct {
  tlv_decoder_slot_t *slots;
  size_t slot_count;
  size_t slot_cap;
  char *scratch;
  size_t scratch_len;
  uint64_t nodes_seen;
  uint64_t bytes_seen;
  uint32_t max_depth;
  uint32_t truncated;
} tlv_decoder_ctx_t;
int tlv_decoder_init(tlv_decoder_ctx_t *ctx);
void tlv_decoder_free(tlv_decoder_ctx_t *ctx);
int tlv_decoder_track(tlv_decoder_ctx_t *ctx, uint32_t tag, const char *label);
int tlv_decoder_scan_tree(const tlv_tree_t *tree, tlv_decoder_ctx_t *ctx);
int tlv_decoder_reserve(tlv_decoder_ctx_t *ctx, size_t need);
size_t tlv_decoder_slot_count(const tlv_decoder_ctx_t *ctx);
uint64_t tlv_decoder_hits_for(const tlv_decoder_ctx_t *ctx, uint32_t tag);
#ifdef __cplusplus
}
#endif
#endif
