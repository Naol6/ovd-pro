#ifndef TLVPACK_CANONICAL_H
#define TLVPACK_CANONICAL_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { size_t seen; uint32_t last_tag; } tlv_canonical_ctx_t;
typedef int (*tlv_canonical_fn)(void *ctx, const tlv_node_t *node, uint32_t depth);
int tlv_canonical_walk_tree(const tlv_tree_t *tree, tlv_canonical_fn fn, void *ctx);
size_t tlv_canonical_count_nodes(const tlv_tree_t *tree);
int tlv_canonical_reset(tlv_canonical_ctx_t *ctx);
#ifdef __cplusplus
}
#endif
#endif
