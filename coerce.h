#ifndef TLVPACK_COERCE_H
#define TLVPACK_COERCE_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { size_t seen; uint32_t last_tag; } tlv_coerce_ctx_t;
typedef int (*tlv_coerce_fn)(void *ctx, const tlv_node_t *node, uint32_t depth);
int tlv_coerce_walk_tree(const tlv_tree_t *tree, tlv_coerce_fn fn, void *ctx);
size_t tlv_coerce_count_nodes(const tlv_tree_t *tree);
int tlv_coerce_reset(tlv_coerce_ctx_t *ctx);
#ifdef __cplusplus
}
#endif
#endif
