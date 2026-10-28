#ifndef TLVPACK_CRC_H
#define TLVPACK_CRC_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct { size_t seen; uint32_t last_tag; } tlv_crc_ctx_t;
typedef int (*tlv_crc_fn)(void *ctx, const tlv_node_t *node, uint32_t depth);
int tlv_crc_walk_tree(const tlv_tree_t *tree, tlv_crc_fn fn, void *ctx);
size_t tlv_crc_count_nodes(const tlv_tree_t *tree);
int tlv_crc_reset(tlv_crc_ctx_t *ctx);
#ifdef __cplusplus
}
#endif
#endif
