#ifndef TLV_CODEC_H
#define TLV_CODEC_H
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
} tlv_codec_ctx_t;
int tlv_codec_init(tlv_codec_ctx_t *ctx);
void tlv_codec_free(tlv_codec_ctx_t *ctx);
int tlv_codec_analyze(const tlv_tree_t *tree, tlv_codec_ctx_t *ctx);
int tlv_codec_encode_tag(uint32_t tag, uint8_t *out, size_t cap, size_t *n);
int tlv_codec_clone_subtree(const tlv_node_t *src, tlv_node_t *dst);
size_t tlv_codec_estimate_size(const tlv_tree_t *tree);
int tlv_codec_reserve(tlv_codec_ctx_t *ctx, size_t need);
#ifdef __cplusplus
}
#endif
#endif
