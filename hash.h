#ifndef TLVPACK_HASH_H
#define TLVPACK_HASH_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { size_t seen; uint32_t last_tag; } tlv_hash_ctx_t;
typedef int (*tlv_hash_fn)(void *ctx, const tlv_node_t *node, uint32_t depth);
int tlv_hash_walk_tree(const tlv_tree_t *tree, tlv_hash_fn fn, void *ctx);
size_t tlv_hash_count_nodes(const tlv_tree_t *tree);
int tlv_hash_reset(tlv_hash_ctx_t *ctx);
#ifdef __cplusplus
}
#endif
#endif
