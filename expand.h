#ifndef TLVPACK_EXPAND_H
#define TLVPACK_EXPAND_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { size_t seen; uint32_t last_tag; } tlv_expand_ctx_t;
typedef int (*tlv_expand_fn)(void *ctx, const tlv_node_t *node, uint32_t depth);
int tlv_expand_walk_tree(const tlv_tree_t *tree, tlv_expand_fn fn, void *ctx);
size_t tlv_expand_count_nodes(const tlv_tree_t *tree);
int tlv_expand_reset(tlv_expand_ctx_t *ctx);
#ifdef __cplusplus
}
#endif
#endif
