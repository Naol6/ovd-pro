#include "formatter.h"
#include "node.h"
#include "varint.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int fmt_append(char **buf, size_t *len, size_t *cap, const char *piece) {
  size_t need, plen = strlen(piece);
  if (!buf || !len || !cap || !piece) return -1;
  need = *len + plen + 1;
  if (need > *cap) {
    size_t ncap = *cap ? *cap * 2 : 128;
    while (ncap < need) ncap *= 2;
    char *next = (char *)realloc(*buf, ncap);
    if (!next) return -1;
    *buf = next;
    *cap = ncap;
  }
  memcpy(*buf + *len, piece, plen);
  *len += plen;
  (*buf)[*len] = '\0';
  return 0;
}

static int fmt_node(const tlv_node_t *n, char **buf, size_t *len, size_t *cap,
                    int indent) {
  char line[256];
  size_t i;
  if (!n) return -1;
  snprintf(line, sizeof(line), "%*s tag=%u len=%zu children=%zu\n",
           indent, "", n->tag, n->value_len, n->child_count);
  if (fmt_append(buf, len, cap, line) != 0) return -1;
  for (i = 0; i < n->child_count; i++)
    if (fmt_node(&n->children[i], buf, len, cap, indent + 2) != 0) return -1;
  return 0;
}

int tlv_format_tree(const tlv_tree_t *tree, char **out, size_t *out_len) {
  char *buf = NULL;
  size_t len = 0, cap = 0;
  size_t i;
  if (!tree || !out || !out_len) return -1;
  for (i = 0; i < tree->root_count; i++)
    if (fmt_node(&tree->roots[i], &buf, &len, &cap, 0) != 0) {
      free(buf);
      return -1;
    }
  *out = buf;
  *out_len = len;
  return 0;
}

void tlv_format_free(char *buf) { free(buf); }
