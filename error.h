#ifndef TLVPACK_ERROR_H
#define TLVPACK_ERROR_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { size_t seen; uint32_t last_tag; } tlv_error_ctx_t;
typedef int (*tlv_error_fn)(void *ctx, const tlv_node_t *node, uint32_t depth);
int tlv_error_walk_tree(const tlv_tree_t *tree, tlv_error_fn fn, void *ctx);
size_t tlv_error_count_nodes(const tlv_tree_t *tree);
int tlv_error_reset(tlv_error_ctx_t *ctx);
#ifdef __cplusplus
}
#endif
#endif
