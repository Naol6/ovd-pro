#ifndef TLVPACK_IMPORT_CTX_H
#define TLVPACK_IMPORT_CTX_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { size_t seen; uint32_t last_tag; } tlv_import_ctx_ctx_t;
typedef int (*tlv_import_ctx_fn)(void *ctx, const tlv_node_t *node, uint32_t depth);
int tlv_import_ctx_walk_tree(const tlv_tree_t *tree, tlv_import_ctx_fn fn, void *ctx);
size_t tlv_import_ctx_count_nodes(const tlv_tree_t *tree);
int tlv_import_ctx_reset(tlv_import_ctx_ctx_t *ctx);
#ifdef __cplusplus
}
#endif
#endif
