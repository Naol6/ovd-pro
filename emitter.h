#ifndef TLV_EMITTER_H
#define TLV_EMITTER_H
#include "tlvpack/tlv_node.h"
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct {
  size_t visited;
  size_t scratch_len;
  char *scratch;
  uint32_t last_tag;
  uint32_t max_depth;
  size_t max_value;
} tlv_emitter_ctx_t;
int tlv_emitter_init(tlv_emitter_ctx_t *ctx);
void tlv_emitter_free(tlv_emitter_ctx_t *ctx);
int tlv_emitter_analyze(const tlv_tree_t *tree, tlv_emitter_ctx_t *ctx);
int tlv_emitter_encode_tag(uint32_t tag, uint8_t *out, size_t cap, size_t *n);
int tlv_emitter_clone_subtree(const tlv_node_t *src, tlv_node_t *dst);
size_t tlv_emitter_estimate_size(const tlv_tree_t *tree);
int tlv_emitter_reserve(tlv_emitter_ctx_t *ctx, size_t need);
#ifdef __cplusplus
}
#endif
#endif
