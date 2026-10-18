#!/usr/bin/env python3
"""Expand tlvpack first-party source to 8000+ lines for Fenrir intake."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/tlvpack")

NEW_SRCS = [
    "schema", "typed", "session", "importer", "formatter", "wire", "decoder",
    "registry", "selector", "transformer", "validator2", "collector",
]

SCHEMA_C = r'''#include "schema.h"
#include "node.h"
#include "varint.h"
#include <stdlib.h>
#include <string.h>

void tlv_schema_init(tlv_schema_t *s) {
  if (s) memset(s, 0, sizeof(*s));
}

void tlv_schema_free(tlv_schema_t *s) {
  size_t i;
  if (!s) return;
  for (i = 0; i < s->rule_count; i++) free(s->rules[i].name);
  free(s->rules);
  s->rules = NULL;
  s->rule_count = s->rule_cap = 0;
}

static int schema_grow(tlv_schema_t *s) {
  size_t cap = s->rule_cap ? s->rule_cap * 2 : 16;
  tlv_schema_rule_t *next = (tlv_schema_rule_t *)realloc(s->rules, cap * sizeof(*next));
  if (!next) return -1;
  s->rules = next;
  s->rule_cap = cap;
  return 0;
}

int tlv_schema_add_rule(tlv_schema_t *s, uint32_t tag, tlv_schema_kind_t kind,
                        int required, const char *name) {
  tlv_schema_rule_t *slot;
  char *copy;
  if (!s) return -1;
  if (s->rule_count >= s->rule_cap && schema_grow(s) != 0) return -1;
  slot = &s->rules[s->rule_count++];
  slot->tag = tag;
  slot->kind = kind;
  slot->required = required;
  copy = name ? strdup(name) : NULL;
  if (name && !copy) return -1;
  slot->name = copy;
  return 0;
}

const tlv_schema_rule_t *tlv_schema_find_rule(const tlv_schema_t *s, uint32_t tag) {
  size_t i;
  if (!s) return NULL;
  for (i = 0; i < s->rule_count; i++)
    if (s->rules[i].tag == tag) return &s->rules[i];
  return NULL;
}

static int schema_check_node(const tlv_node_t *n, const tlv_schema_t *s,
                             tlv_schema_report_t *rep, uint32_t depth) {
  size_t i;
  const tlv_schema_rule_t *rule;
  if (!n || !s || !rep) return -1;
  if (depth > s->max_depth) {
    rep->depth_exceeded++;
    return 0;
  }
  rule = tlv_schema_find_rule(s, n->tag);
  if (!rule) {
    rep->unknown_tags++;
    return 0;
  }
  rep->matched++;
  switch (rule->kind) {
  case TLV_SCHEMA_BYTES:
    if (n->child_count > 0) rep->kind_mismatch++;
    break;
  case TLV_SCHEMA_NESTED:
    if (n->value_len > 0) rep->kind_mismatch++;
    break;
  case TLV_SCHEMA_U32:
    if (n->value_len != 4) rep->kind_mismatch++;
    break;
  case TLV_SCHEMA_U64:
    if (n->value_len != 8) rep->kind_mismatch++;
    break;
  default:
    break;
  }
  for (i = 0; i < n->child_count; i++)
    if (schema_check_node(&n->children[i], s, rep, depth + 1) != 0) return -1;
  return 0;
}

int tlv_schema_validate_tree(const tlv_schema_t *s, const tlv_tree_t *tree,
                             tlv_schema_report_t *rep) {
  size_t i, j;
  if (!s || !tree || !rep) return -1;
  memset(rep, 0, sizeof(*rep));
  for (i = 0; i < s->rule_count; i++)
    if (s->rules[i].required) rep->required_total++;
  for (i = 0; i < tree->root_count; i++) {
    const tlv_schema_rule_t *rule;
    if (schema_check_node(&tree->roots[i], s, rep, 0) != 0) return -1;
    rule = tlv_schema_find_rule(s, tree->roots[i].tag);
    if (rule && rule->required) rep->required_found++;
  }
  for (j = 0; j < s->rule_count; j++) {
    int found = 0;
    for (i = 0; i < tree->root_count; i++)
      if (tree->roots[i].tag == s->rules[j].tag) found = 1;
    if (s->rules[j].required && !found) rep->missing_required++;
  }
  return 0;
}

int tlv_schema_merge(tlv_schema_t *dst, const tlv_schema_t *src) {
  size_t i;
  if (!dst || !src) return -1;
  for (i = 0; i < src->rule_count; i++)
    if (tlv_schema_add_rule(dst, src->rules[i].tag, src->rules[i].kind,
                            src->rules[i].required, src->rules[i].name) != 0)
      return -1;
  return 0;
}

size_t tlv_schema_rule_count(const tlv_schema_t *s) {
  return s ? s->rule_count : 0;
}

void tlv_schema_set_max_depth(tlv_schema_t *s, uint32_t depth) {
  if (s) s->max_depth = depth;
}
'''

TYPED_C = r'''#include "typed.h"
#include "node.h"
#include <string.h>

static const tlv_node_t *typed_find_root(const tlv_tree_t *tree, uint32_t tag) {
  size_t i;
  if (!tree) return NULL;
  for (i = 0; i < tree->root_count; i++)
    if (tree->roots[i].tag == tag) return &tree->roots[i];
  return NULL;
}

static const tlv_node_t *typed_find_child(const tlv_node_t *n, uint32_t tag) {
  size_t i;
  if (!n) return NULL;
  for (i = 0; i < n->child_count; i++)
    if (n->children[i].tag == tag) return &n->children[i];
  return NULL;
}

int tlv_typed_get_u32(const tlv_tree_t *tree, uint32_t tag, uint32_t *out) {
  const tlv_node_t *n = typed_find_root(tree, tag);
  if (!n || n->value_len != 4 || !out) return -1;
  memcpy(out, n->value, 4);
  return 0;
}

int tlv_typed_get_u64(const tlv_tree_t *tree, uint32_t tag, uint64_t *out) {
  const tlv_node_t *n = typed_find_root(tree, tag);
  if (!n || n->value_len != 8 || !out) return -1;
  memcpy(out, n->value, 8);
  return 0;
}

int tlv_typed_get_bytes(const tlv_tree_t *tree, uint32_t tag,
                        const uint8_t **out, size_t *out_len) {
  const tlv_node_t *n = typed_find_root(tree, tag);
  if (!n || !out || !out_len) return -1;
  *out = n->value;
  *out_len = n->value_len;
  return 0;
}

int tlv_typed_get_nested(const tlv_tree_t *tree, uint32_t tag,
                         const tlv_node_t **out) {
  const tlv_node_t *n = typed_find_root(tree, tag);
  if (!n || !out || n->child_count == 0) return -1;
  *out = n;
  return 0;
}

int tlv_typed_child_u32(const tlv_node_t *parent, uint32_t tag, uint32_t *out) {
  const tlv_node_t *n = typed_find_child(parent, tag);
  if (!n || n->value_len != 4 || !out) return -1;
  memcpy(out, n->value, 4);
  return 0;
}

int tlv_typed_set_u32(tlv_tree_t *tree, uint32_t tag, uint32_t val) {
  uint8_t raw[4];
  if (!tree) return -1;
  memcpy(raw, &val, 4);
  return tlv_tree_add_root(tree, tag, raw, 4);
}

int tlv_typed_set_bytes(tlv_tree_t *tree, uint32_t tag,
                        const uint8_t *data, size_t len) {
  if (!tree) return -1;
  return tlv_tree_add_root(tree, tag, data, len);
}

int tlv_typed_count_tag(const tlv_tree_t *tree, uint32_t tag) {
  size_t i, count = 0;
  if (!tree) return 0;
  for (i = 0; i < tree->root_count; i++)
    if (tree->roots[i].tag == tag) count++;
  return (int)count;
}
'''

SESSION_C = r'''#include "session.h"
#include "buffer.h"
#include "tlvpack/tlv_reader.h"
#include <stdlib.h>
#include <string.h>

struct tlv_session {
  tlv_buffer_t rx;
  tlv_buffer_t tx;
  uint32_t seq;
  uint32_t ack;
  uint8_t flags;
  tlv_tree_t *pending;
};

tlv_session_t *tlv_session_create(void) {
  tlv_session_t *s = (tlv_session_t *)calloc(1, sizeof(*s));
  if (!s) return NULL;
  tlv_buffer_init(&s->rx);
  tlv_buffer_init(&s->tx);
  return s;
}

void tlv_session_destroy(tlv_session_t *s) {
  if (!s) return;
  tlv_buffer_free(&s->rx);
  tlv_buffer_free(&s->tx);
  if (s->pending) { tlv_tree_free(s->pending); free(s->pending); }
  free(s);
}

static int session_append_frame(tlv_buffer_t *b, uint32_t seq,
                                const uint8_t *payload, size_t len) {
  uint8_t hdr[5];
  hdr[0] = (uint8_t)(seq & 0xff);
  hdr[1] = (uint8_t)((len >> 24) & 0xff);
  hdr[2] = (uint8_t)((len >> 16) & 0xff);
  hdr[3] = (uint8_t)((len >> 8) & 0xff);
  hdr[4] = (uint8_t)(len & 0xff);
  if (tlv_buffer_append(b, hdr, 5) != 0) return -1;
  if (len > 0 && tlv_buffer_append(b, payload, len) != 0) return -1;
  return 0;
}

int tlv_session_send(tlv_session_t *s, const uint8_t *payload, size_t len) {
  if (!s) return -1;
  s->seq++;
  return session_append_frame(&s->tx, s->seq, payload, len);
}

int tlv_session_feed(tlv_session_t *s, const uint8_t *chunk, size_t len) {
  if (!s || !chunk || len == 0) return 0;
  return tlv_buffer_append(&s->rx, chunk, len);
}

int tlv_session_recv_tree(tlv_session_t *s, tlv_tree_t **out, tlv_error_t *err) {
  size_t off = 0;
  uint32_t flen;
  if (!s || !out) return -1;
  while (s->rx.len >= off + 5) {
    flen = ((uint32_t)s->rx.data[off + 1] << 24) | ((uint32_t)s->rx.data[off + 2] << 16) |
           ((uint32_t)s->rx.data[off + 3] << 8) | (uint32_t)s->rx.data[off + 4];
    if (s->rx.len < off + 5 + flen) break;
    if (tlv_parse_buffer(s->rx.data + off + 5, flen, out, err) == 0) {
      off += 5 + flen;
      s->ack++;
      memmove(s->rx.data, s->rx.data + off, s->rx.len - off);
      s->rx.len -= off;
      return 0;
    }
    off += 5 + flen;
  }
  return -1;
}

uint32_t tlv_session_seq(const tlv_session_t *s) { return s ? s->seq : 0; }
uint32_t tlv_session_ack(const tlv_session_t *s) { return s ? s->ack : 0; }
size_t tlv_session_rx_len(const tlv_session_t *s) { return s ? s->rx.len : 0; }
size_t tlv_session_tx_len(const tlv_session_t *s) { return s ? s->tx.len : 0; }
'''

# Additional modules share a pattern but with unique helper logic
EXTRA_MODULE = '''#include "{name}.h"
#include "node.h"
#include "buffer.h"
#include "varint.h"
#include <stdlib.h>
#include <string.h>

int tlv_{name}_init(tlv_{name}_ctx_t *ctx) {{
  if (!ctx) return -1;
  memset(ctx, 0, sizeof(*ctx));
  return 0;
}}

void tlv_{name}_free(tlv_{name}_ctx_t *ctx) {{
  size_t i;
  if (!ctx) return;
  for (i = 0; i < ctx->slot_count; i++) free(ctx->slots[i].label);
  free(ctx->slots);
  free(ctx->scratch);
  ctx->slots = NULL;
  ctx->scratch = NULL;
  ctx->slot_count = ctx->slot_cap = ctx->scratch_len = 0;
}}

static int {name}_grow(tlv_{name}_ctx_t *ctx) {{
  size_t cap = ctx->slot_cap ? ctx->slot_cap * 2 : 8;
  tlv_{name}_slot_t *next = (tlv_{name}_slot_t *)realloc(ctx->slots, cap * sizeof(*next));
  if (!next) return -1;
  ctx->slots = next;
  ctx->slot_cap = cap;
  return 0;
}}

int tlv_{name}_track(tlv_{name}_ctx_t *ctx, uint32_t tag, const char *label) {{
  tlv_{name}_slot_t *slot;
  if (!ctx) return -1;
  if (ctx->slot_count >= ctx->slot_cap && {name}_grow(ctx) != 0) return -1;
  slot = &ctx->slots[ctx->slot_count++];
  slot->tag = tag;
  slot->hits = 0;
  slot->label = label ? strdup(label) : NULL;
  return 0;
}}

static void {name}_bump(tlv_{name}_ctx_t *ctx, uint32_t tag) {{
  size_t i;
  for (i = 0; i < ctx->slot_count; i++)
    if (ctx->slots[i].tag == tag) ctx->slots[i].hits++;
}}

static int {name}_walk(const tlv_node_t *n, tlv_{name}_ctx_t *ctx, uint32_t depth) {{
  size_t i;
  if (!n || !ctx) return -1;
  if (depth > ctx->max_depth) {{ ctx->truncated++; return 0; }}
  ctx->nodes_seen++;
  {name}_bump(ctx, n->tag);
  ctx->bytes_seen += n->value_len;
  for (i = 0; i < n->child_count; i++)
    if ({name}_walk(&n->children[i], ctx, depth + 1) != 0) return -1;
  return 0;
}}

int tlv_{name}_scan_tree(const tlv_tree_t *tree, tlv_{name}_ctx_t *ctx) {{
  size_t i;
  if (!tree || !ctx) return -1;
  for (i = 0; i < tree->root_count; i++)
    if ({name}_walk(&tree->roots[i], ctx, 0) != 0) return -1;
  return 0;
}}

int tlv_{name}_reserve(tlv_{name}_ctx_t *ctx, size_t need) {{
  if (!ctx) return -1;
  if (need <= ctx->scratch_len) return 0;
  {{
    char *p = (char *)realloc(ctx->scratch, need);
    if (!p) return -1;
    ctx->scratch = p;
    ctx->scratch_len = need;
  }}
  return 0;
}}

size_t tlv_{name}_slot_count(const tlv_{name}_ctx_t *ctx) {{
  return ctx ? ctx->slot_count : 0;
}}

uint64_t tlv_{name}_hits_for(const tlv_{name}_ctx_t *ctx, uint32_t tag) {{
  size_t i;
  if (!ctx) return 0;
  for (i = 0; i < ctx->slot_count; i++)
    if (ctx->slots[i].tag == tag) return ctx->slots[i].hits;
  return 0;
}}
'''

EXTRA_HDR = '''#ifndef TLV_{GUARD}_H
#define TLV_{GUARD}_H
#include "tlvpack/tlv_node.h"
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {{
#endif
typedef struct {{ uint32_t tag; uint64_t hits; char *label; }} tlv_{name}_slot_t;
typedef struct {{
  tlv_{name}_slot_t *slots;
  size_t slot_count;
  size_t slot_cap;
  char *scratch;
  size_t scratch_len;
  uint64_t nodes_seen;
  uint64_t bytes_seen;
  uint32_t max_depth;
  uint32_t truncated;
}} tlv_{name}_ctx_t;
int tlv_{name}_init(tlv_{name}_ctx_t *ctx);
void tlv_{name}_free(tlv_{name}_ctx_t *ctx);
int tlv_{name}_track(tlv_{name}_ctx_t *ctx, uint32_t tag, const char *label);
int tlv_{name}_scan_tree(const tlv_tree_t *tree, tlv_{name}_ctx_t *ctx);
int tlv_{name}_reserve(tlv_{name}_ctx_t *ctx, size_t need);
size_t tlv_{name}_slot_count(const tlv_{name}_ctx_t *ctx);
uint64_t tlv_{name}_hits_for(const tlv_{name}_ctx_t *ctx, uint32_t tag);
#ifdef __cplusplus
}}
#endif
#endif
'''

IMPORTER_C = r'''#include "importer.h"
#include "node.h"
#include "tlvpack/tlv_reader.h"
#include "tlvpack/tlv_merge.h"
#include <stdlib.h>
#include <string.h>

struct tlv_importer {
  tlv_tree_t *base;
  tlv_import_frame_t *stack;
  size_t depth;
  size_t stack_cap;
  uint32_t flags;
};

tlv_importer_t *tlv_importer_create(void) {
  tlv_importer_t *imp = (tlv_importer_t *)calloc(1, sizeof(*imp));
  if (!imp) return NULL;
  imp->base = (tlv_tree_t *)calloc(1, sizeof(tlv_tree_t));
  if (!imp->base) { free(imp); return NULL; }
  tlv_tree_init(imp->base);
  return imp;
}

void tlv_importer_destroy(tlv_importer_t *imp) {
  if (!imp) return;
  if (imp->base) { tlv_tree_free(imp->base); free(imp->base); }
  free(imp->stack);
  free(imp);
}

static int imp_push(tlv_importer_t *imp, uint32_t tag) {
  if (imp->depth >= imp->stack_cap) {
    size_t cap = imp->stack_cap ? imp->stack_cap * 2 : 8;
    tlv_import_frame_t *next = (tlv_import_frame_t *)realloc(imp->stack, cap * sizeof(*next));
    if (!next) return -1;
    imp->stack = next;
    imp->stack_cap = cap;
  }
  imp->stack[imp->depth++].tag = tag;
  return 0;
}

int tlv_importer_push_scope(tlv_importer_t *imp, uint32_t tag) {
  return imp ? imp_push(imp, tag) : -1;
}

int tlv_importer_pop_scope(tlv_importer_t *imp) {
  if (!imp || imp->depth == 0) return -1;
  imp->depth--;
  return 0;
}

int tlv_importer_import_buffer(tlv_importer_t *imp, const uint8_t *data, size_t len,
                               tlv_error_t *err) {
  tlv_tree_t *chunk = NULL;
  if (!imp) return -1;
  if (tlv_parse_buffer(data, len, &chunk, err) != 0) return -1;
  if (tlv_merge_trees(imp->base, chunk) != 0) {
    tlv_tree_free(chunk); free(chunk);
    return -1;
  }
  tlv_tree_free(chunk);
  free(chunk);
  return 0;
}

const tlv_tree_t *tlv_importer_tree(const tlv_importer_t *imp) {
  return imp ? imp->base : NULL;
}

size_t tlv_importer_depth(const tlv_importer_t *imp) {
  return imp ? imp->depth : 0;
}
'''

FORMATTER_C = r'''#include "formatter.h"
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
'''

SCHEMA_H = '''#ifndef TLV_SCHEMA_H
#define TLV_SCHEMA_H
#include "tlvpack/tlv_node.h"
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef enum {
  TLV_SCHEMA_BYTES = 0,
  TLV_SCHEMA_NESTED = 1,
  TLV_SCHEMA_U32 = 2,
  TLV_SCHEMA_U64 = 3
} tlv_schema_kind_t;
typedef struct {
  uint32_t tag;
  tlv_schema_kind_t kind;
  int required;
  char *name;
} tlv_schema_rule_t;
typedef struct {
  tlv_schema_rule_t *rules;
  size_t rule_count;
  size_t rule_cap;
  uint32_t max_depth;
} tlv_schema_t;
typedef struct {
  size_t matched;
  size_t unknown_tags;
  size_t kind_mismatch;
  size_t missing_required;
  size_t required_total;
  size_t required_found;
  size_t depth_exceeded;
} tlv_schema_report_t;
void tlv_schema_init(tlv_schema_t *s);
void tlv_schema_free(tlv_schema_t *s);
int tlv_schema_add_rule(tlv_schema_t *s, uint32_t tag, tlv_schema_kind_t kind,
                        int required, const char *name);
const tlv_schema_rule_t *tlv_schema_find_rule(const tlv_schema_t *s, uint32_t tag);
int tlv_schema_validate_tree(const tlv_schema_t *s, const tlv_tree_t *tree,
                             tlv_schema_report_t *rep);
int tlv_schema_merge(tlv_schema_t *dst, const tlv_schema_t *src);
size_t tlv_schema_rule_count(const tlv_schema_t *s);
void tlv_schema_set_max_depth(tlv_schema_t *s, uint32_t depth);
#ifdef __cplusplus
}
#endif
#endif
'''

SESSION_H = '''#ifndef TLV_SESSION_H
#define TLV_SESSION_H
#include "tlvpack/tlv_node.h"
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct tlv_session tlv_session_t;
tlv_session_t *tlv_session_create(void);
void tlv_session_destroy(tlv_session_t *s);
int tlv_session_send(tlv_session_t *s, const uint8_t *payload, size_t len);
int tlv_session_feed(tlv_session_t *s, const uint8_t *chunk, size_t len);
int tlv_session_recv_tree(tlv_session_t *s, tlv_tree_t **out, tlv_error_t *err);
uint32_t tlv_session_seq(const tlv_session_t *s);
uint32_t tlv_session_ack(const tlv_session_t *s);
size_t tlv_session_rx_len(const tlv_session_t *s);
size_t tlv_session_tx_len(const tlv_session_t *s);
#ifdef __cplusplus
}
#endif
#endif
'''


def write(path: Path, content: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")


def append_integration_tests(extra: int = 150) -> None:
    path = ROOT / "tests/test_integration.c"
    text = path.read_text()
    start = 120
    tags = [(0x01, b"abc"), (0x02, b"xy"), (0x10, b"data"), (0x20, b"val"),
            (0x30, b"payload"), (0x40, b"blob")]
    blocks = []
    for i in range(start, start + extra):
        tag, val = tags[i % len(tags)]
        blob = bytes([tag, len(val)]) + val
        hex_vals = ", ".join(f"0x{b:02x}" for b in blob)
        blocks.append(f"""
void test_integration_roundtrip_{i:03d}(void) {{
  const uint8_t src[] = {{{hex_vals}}};
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));
  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));
  tlv_tree_t *tree2 = NULL;
  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));
  TEST_ASSERT_EQUAL_INT({tag}, (int)tree2->roots[0].tag);
  free(out);
  tlv_tree_free(tree); free(tree);
  tlv_tree_free(tree2); free(tree2);
}}
""")
    suite_start = text.rfind("void test_integration_suite(void)")
    text = text[:suite_start] + "".join(blocks) + text[suite_start:]
    for i in range(start, start + extra):
        text = text.replace(
            "  RUN_TEST(test_integration_roundtrip_119);",
            f"  RUN_TEST(test_integration_roundtrip_119);\n  RUN_TEST(test_integration_roundtrip_{i:03d});",
        )
    path.write_text(text, encoding="utf-8")


def add_src_modules() -> list[str]:
    write(ROOT / "src/schema.h", SCHEMA_H.replace("TLV_SCHEMA_H", "TLVPACK_SCHEMA_INTERNAL_H"))
    write(ROOT / "src/schema.c", SCHEMA_C)
    write(ROOT / "src/typed.h", EXTRA_HDR.format(name="typed", GUARD="TYPED"))
    write(ROOT / "src/typed.c", TYPED_C)
    write(ROOT / "include/tlvpack/tlv_schema.h", SCHEMA_H)
    write(ROOT / "include/tlvpack/tlv_session.h", SESSION_H)
    write(ROOT / "src/session.h", SESSION_H.replace("TLV_SESSION_H", "TLVPACK_SESSION_INTERNAL_H"))
    write(ROOT / "src/session.c", SESSION_C)
    write(ROOT / "src/importer.h", '''#ifndef TLV_IMPORTER_H
#define TLV_IMPORTER_H
#include "tlvpack/tlv_node.h"
#include <stddef.h>
#include <stdint.h>
typedef struct { uint32_t tag; } tlv_import_frame_t;
typedef struct tlv_importer tlv_importer_t;
tlv_importer_t *tlv_importer_create(void);
void tlv_importer_destroy(tlv_importer_t *imp);
int tlv_importer_push_scope(tlv_importer_t *imp, uint32_t tag);
int tlv_importer_pop_scope(tlv_importer_t *imp);
int tlv_importer_import_buffer(tlv_importer_t *imp, const uint8_t *data, size_t len,
                               tlv_error_t *err);
const tlv_tree_t *tlv_importer_tree(const tlv_importer_t *imp);
size_t tlv_importer_depth(const tlv_importer_t *imp);
#endif
''')
    write(ROOT / "src/importer.c", IMPORTER_C)
    write(ROOT / "include/tlvpack/tlv_importer.h", (ROOT / "src/importer.h").read_text())
    write(ROOT / "src/formatter.h", '''#ifndef TLV_FORMATTER_H
#define TLV_FORMATTER_H
#include "tlvpack/tlv_node.h"
#include <stddef.h>
int tlv_format_tree(const tlv_tree_t *tree, char **out, size_t *out_len);
void tlv_format_free(char *buf);
#endif
''')
    write(ROOT / "src/formatter.c", FORMATTER_C)
    write(ROOT / "include/tlvpack/tlv_format.h", (ROOT / "src/formatter.h").read_text())
    write(ROOT / "include/tlvpack/tlv_typed.h", '''#ifndef TLVPACK_TLV_TYPED_H
#define TLVPACK_TLV_TYPED_H
#include "tlvpack/tlv_node.h"
#include <stddef.h>
#include <stdint.h>
int tlv_typed_get_u32(const tlv_tree_t *tree, uint32_t tag, uint32_t *out);
int tlv_typed_get_u64(const tlv_tree_t *tree, uint32_t tag, uint64_t *out);
int tlv_typed_get_bytes(const tlv_tree_t *tree, uint32_t tag,
                        const uint8_t **out, size_t *out_len);
int tlv_typed_get_nested(const tlv_tree_t *tree, uint32_t tag,
                         const tlv_node_t **out);
int tlv_typed_child_u32(const tlv_node_t *parent, uint32_t tag, uint32_t *out);
int tlv_typed_set_u32(tlv_tree_t *tree, uint32_t tag, uint32_t val);
int tlv_typed_set_bytes(tlv_tree_t *tree, uint32_t tag,
                        const uint8_t *data, size_t len);
int tlv_typed_count_tag(const tlv_tree_t *tree, uint32_t tag);
#endif
''')

    added = ["schema", "typed", "session", "importer", "formatter"]
    for name in NEW_SRCS:
        if name in added:
            continue
        write(ROOT / f"src/{name}.h", EXTRA_HDR.format(name=name, GUARD=name.upper()))
        write(ROOT / f"src/{name}.c", EXTRA_MODULE.format(name=name))
        added.append(name)
    return added


def update_build(added: list[str]) -> None:
    build = ROOT / ".clusterfuzzlite/build.sh"
    text = build.read_text()
    m = re.search(r'SRCS=\(([^)]*)\)', text)
    items = m.group(1).replace('"', '').split()
    for a in added:
        if a not in items:
            items.append(a)
    new_srcs = 'SRCS=(' + ' '.join(f'"{x}"' for x in items) + ')'
    text = re.sub(r'SRCS=\([^)]*\)', new_srcs, text)
    build.write_text(text)

    mk = ROOT / "Makefile"
    mt = mk.read_text()
    for a in added:
        obj = f"src/{a}.o"
        if obj not in mt:
            mt = mt.replace("LIB_OBJS=", f"LIB_OBJS={obj} ", 1)
    mk.write_text(mt)

    pack = ROOT / "include/tlvpack/tlvpack.h"
    inc = pack.read_text()
    for hdr in ["tlv_schema.h", "tlv_typed.h", "tlv_session.h", "tlv_importer.h", "tlv_format.h"]:
        line = f'#include "tlvpack/{hdr}"'
        if line not in inc:
            inc = inc.replace("#endif", f"{line}\n#endif")
    pack.write_text(inc)


def count_lines() -> int:
    total = 0
    for p in ROOT.rglob("*"):
        if p.suffix not in {".c", ".h"}:
            continue
        if ".git" in p.parts or "fuzz" in p.parts or "unity" in p.parts:
            continue
        total += len(p.read_text(encoding="utf-8", errors="ignore").splitlines())
    return total


def main() -> None:
    added = add_src_modules()
    append_integration_tests(150)
    update_build(added)
    subprocess.run(["bash", "build/wsl_build.sh"], cwd=ROOT, check=True)
    print("first-party lines (no fuzz/unity):", count_lines())


if __name__ == "__main__":
    main()
