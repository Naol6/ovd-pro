#ifndef TLVPACK_COPY_H
#define TLVPACK_COPY_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { size_t seen; uint32_t last_tag; } tlv_copy_ctx_t;
typedef int (*tlv_copy_fn)(void *ctx, const tlv_node_t *node, uint32_t depth);
int tlv_copy_walk_tree(const tlv_tree_t *tree, tlv_copy_fn fn, void *ctx);
size_t tlv_copy_count_nodes(const tlv_tree_t *tree);
int tlv_copy_reset(tlv_copy_ctx_t *ctx);
#ifdef __cplusplus
}
#endif
#endif
