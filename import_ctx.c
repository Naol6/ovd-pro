#include "import_ctx.h"
#include "node.h"
#include <stdlib.h>
#include <string.h>

static int tlv_import_ctx_visit_node(const tlv_node_t *n, tlv_import_ctx_fn fn, void *ctx, uint32_t depth) {
  size_t i;
  if (!n || !fn) return -1;
  if (fn(ctx, n, depth) != 0) return -1;
  for (i = 0; i < n->child_count; i++)
    if (tlv_import_ctx_visit_node(&n->children[i], fn, ctx, depth + 1) != 0) return -1;
  return 0;
}

int tlv_import_ctx_walk_tree(const tlv_tree_t *tree, tlv_import_ctx_fn fn, void *ctx) {
  size_t i;
  if (!tree || !fn) return -1;
  for (i = 0; i < tree->root_count; i++)
    if (tlv_import_ctx_visit_node(&tree->roots[i], fn, ctx, 0) != 0) return -1;
  return 0;
}

size_t tlv_import_ctx_count_nodes(const tlv_tree_t *tree) {
  size_t total = 0, i;
  if (!tree) return 0;
  for (i = 0; i < tree->root_count; i++) {
    size_t j;
    total++;
    for (j = 0; j < tree->roots[i].child_count; j++) total += tree->roots[i].children[j].child_count + 1;
  }
  return total;
}

int tlv_import_ctx_reset(tlv_import_ctx_ctx_t *ctx) {
  if (!ctx) return -1;
  ctx->seen = 0;
  ctx->last_tag = 0;
  return 0;
}
