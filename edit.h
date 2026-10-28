#ifndef TLV_EDIT_H
#define TLV_EDIT_H
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
} tlv_edit_ctx_t;
int tlv_edit_init(tlv_edit_ctx_t *ctx);
void tlv_edit_free(tlv_edit_ctx_t *ctx);
int tlv_edit_analyze(const tlv_tree_t *tree, tlv_edit_ctx_t *ctx);
int tlv_edit_encode_tag(uint32_t tag, uint8_t *out, size_t cap, size_t *n);
int tlv_edit_clone_subtree(const tlv_node_t *src, tlv_node_t *dst);
size_t tlv_edit_estimate_size(const tlv_tree_t *tree);
int tlv_edit_reserve(tlv_edit_ctx_t *ctx, size_t need);
#ifdef __cplusplus
}
#endif
#endif
