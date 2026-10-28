#ifndef TLVPACK_FILTER_H
#define TLVPACK_FILTER_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { size_t seen; uint32_t last_tag; } tlv_filter_ctx_t;
typedef int (*tlv_filter_fn)(void *ctx, const tlv_node_t *node, uint32_t depth);
int tlv_filter_walk_tree(const tlv_tree_t *tree, tlv_filter_fn fn, void *ctx);
size_t tlv_filter_count_nodes(const tlv_tree_t *tree);
int tlv_filter_reset(tlv_filter_ctx_t *ctx);
#ifdef __cplusplus
}
#endif
#endif
