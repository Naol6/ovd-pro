#ifndef TLVPACK_DIFF_H
#define TLVPACK_DIFF_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { size_t seen; uint32_t last_tag; } tlv_diff_ctx_t;
typedef int (*tlv_diff_fn)(void *ctx, const tlv_node_t *node, uint32_t depth);
int tlv_diff_walk_tree(const tlv_tree_t *tree, tlv_diff_fn fn, void *ctx);
size_t tlv_diff_count_nodes(const tlv_tree_t *tree);
int tlv_diff_reset(tlv_diff_ctx_t *ctx);
#ifdef __cplusplus
}
#endif
#endif
