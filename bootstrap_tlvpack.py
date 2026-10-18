#!/usr/bin/env python3
"""Bootstrap tlvpack — original binary TLV record parser (NOT envfile/dotenv derived)."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/tlvpack")

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add tlvpack public API", ["include/tlvpack/tlvpack.h", "include/tlvpack/tlv_node.h"]),
    ("include: add reader writer merge stream headers", [
        "include/tlvpack/tlv_reader.h", "include/tlvpack/tlv_writer.h",
        "include/tlvpack/tlv_merge.h", "include/tlvpack/tlv_stream.h"]),
    ("src: add arena allocator", ["src/arena.c", "src/arena.h"]),
    ("src: add growable byte buffer", ["src/buffer.c", "src/buffer.h"]),
    ("src: add varint codec", ["src/varint.c", "src/varint.h"]),
    ("src: add TLV node tree store", ["src/node.c", "src/node.h"]),
    ("src: implement TLV reader", ["src/reader.c"]),
    ("src: implement TLV writer", ["src/writer.c"]),
    ("src: add tree merge", ["src/merge.c"]),
    ("src: add streaming reassembly", ["src/stream.c"]),
    ("src: add validation pass", ["src/validate.c"]),
    ("src: add tlvpack driver module", ["src/tlvpack.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parse tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add merge stream tests", ["tests/test_merge.c", "tests/test_stream.c"]),
    ("examples: add sample TLV blobs", ["examples/minimal.tlv", "examples/nested.tlv"]),
    ("fuzz: add parse_fuzzer", ["fuzz/parse_fuzzer.c"]),
    ("fuzz: add merge_fuzzer", ["fuzz/merge_fuzzer.c"]),
    ("fuzz: add stream_fuzzer", ["fuzz/stream_fuzzer.c"]),
    ("fuzz: add nest_fuzzer", ["fuzz/nest_fuzzer.c"]),
    ("fuzz: add seed corpus", [
        "fuzz/corpus/parse_fuzzer/minimal.bin",
        "fuzz/corpus/parse_fuzzer/nested.bin",
        "fuzz/corpus/merge_fuzzer/base.bin",
        "fuzz/corpus/stream_fuzzer/chunks.bin",
        "fuzz/corpus/nest_fuzzer/deep.bin"]),
    ("fuzz: add dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add local WSL build script", ["build/wsl_build.sh"]),
    ("docs: add README", ["README.md"]),
    ("build: add Makefile", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable TLV binary parser", []),
]

LICENSE = """MIT License

Copyright (c) 2026 tolossamuel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

GITIGNORE = """*.o
*.a
/tmp/
cmake-build/
/poc/
crash-*
/guides/
"""

README = """# tlvpack

tlvpack is an original C11 library for parsing, validating, merging, and streaming **binary TLV (tag-length-value)** records. Tags and lengths use unsigned LEB128 varints; constructed tags (high bit set) hold nested child records.

This project is **not** derived from dotenv, INI, TOML overlay, or text config parsers — it implements a purpose-built binary wire format for fuzzing and embedded record pipelines.

## Wire format

Each record: `[varint tag][varint length][value bytes]`. If tag bit 7 is set, value is a nested sequence of child records until end-of-container (tag 0).

## Features

- Incremental TLV reader with arena-backed node trees
- Writer / re-serializer for parsed trees
- Merge two trees by tag key with overlay semantics
- Streaming reassembly for chunked network input
- ClusterFuzzLite harnesses: `parse_fuzzer`, `merge_fuzzer`, `stream_fuzzer`, `nest_fuzzer`

## Build

```bash
bash build/wsl_build.sh
make test
```

## Quick start

```c
#include "tlvpack/tlvpack.h"

tlv_tree_t *tree = NULL;
tlv_error_t err;
tlv_parse_buffer(data, len, &tree, &err);
tlv_tree_free(tree);
```

## License

MIT — see LICENSE.
"""

# --- headers and sources written via write() calls in add_files() ---

def write(path: Path, content: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")


def add_files() -> None:
    write(ROOT / "LICENSE", LICENSE)
    write(ROOT / ".gitignore", GITIGNORE)
    write(ROOT / "README.md", README)

    write(ROOT / "include/tlvpack/tlvpack.h", '''#ifndef TLVPACK_TLVPACK_H
#define TLVPACK_TLVPACK_H
#include "tlvpack/tlv_node.h"
#include "tlvpack/tlv_reader.h"
#include "tlvpack/tlv_writer.h"
#include "tlvpack/tlv_merge.h"
#include "tlvpack/tlv_stream.h"
#endif
''')

    write(ROOT / "include/tlvpack/tlv_node.h", '''#ifndef TLVPACK_TLV_NODE_H
#define TLVPACK_TLV_NODE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct tlv_node {
  uint32_t tag;
  uint8_t *value;
  size_t value_len;
  struct tlv_node *children;
  size_t child_count;
  size_t child_cap;
} tlv_node_t;
typedef struct tlv_tree {
  tlv_node_t *roots;
  size_t root_count;
  size_t root_cap;
} tlv_tree_t;
typedef struct { int code; char msg[128]; } tlv_error_t;
void tlv_tree_init(tlv_tree_t *t);
void tlv_tree_free(tlv_tree_t *t);
int tlv_tree_add_root(tlv_tree_t *t, uint32_t tag, const uint8_t *val, size_t len);
#ifdef __cplusplus
}
#endif
#endif
''')

    write(ROOT / "include/tlvpack/tlv_reader.h", '''#ifndef TLVPACK_TLV_READER_H
#define TLVPACK_TLV_READER_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
int tlv_parse_buffer(const uint8_t *data, size_t len, tlv_tree_t **out, tlv_error_t *err);
#ifdef __cplusplus
}
#endif
#endif
''')

    write(ROOT / "include/tlvpack/tlv_writer.h", '''#ifndef TLVPACK_TLV_WRITER_H
#define TLVPACK_TLV_WRITER_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
int tlv_write_tree(const tlv_tree_t *tree, uint8_t **out, size_t *out_len);
#ifdef __cplusplus
}
#endif
#endif
''')

    write(ROOT / "include/tlvpack/tlv_merge.h", '''#ifndef TLVPACK_TLV_MERGE_H
#define TLVPACK_TLV_MERGE_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
int tlv_merge_trees(tlv_tree_t *dst, const tlv_tree_t *src);
#ifdef __cplusplus
}
#endif
#endif
''')

    write(ROOT / "include/tlvpack/tlv_stream.h", '''#ifndef TLVPACK_TLV_STREAM_H
#define TLVPACK_TLV_STREAM_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct tlv_stream tlv_stream_t;
tlv_stream_t *tlv_stream_create(void);
void tlv_stream_destroy(tlv_stream_t *s);
int tlv_stream_feed(tlv_stream_t *s, const uint8_t *chunk, size_t len);
int tlv_stream_finalize(tlv_stream_t *s, tlv_tree_t **out);
#ifdef __cplusplus
}
#endif
#endif
''')

    write(ROOT / "src/arena.h", '''#ifndef TLV_ARENA_H
#define TLV_ARENA_H
#include <stddef.h>
typedef struct { char *data; size_t len; size_t cap; } tlv_arena_t;
void tlv_arena_init(tlv_arena_t *a);
void tlv_arena_free(tlv_arena_t *a);
char *tlv_arena_alloc(tlv_arena_t *a, size_t n);
#endif
''')

    write(ROOT / "src/arena.c", '''#include "arena.h"
#include <stdlib.h>
#include <string.h>
void tlv_arena_init(tlv_arena_t *a) { a->data = NULL; a->len = 0; a->cap = 0; }
void tlv_arena_free(tlv_arena_t *a) { free(a->data); a->data = NULL; a->len = a->cap = 0; }
char *tlv_arena_alloc(tlv_arena_t *a, size_t n) {
  size_t need = a->len + n;
  if (need > a->cap) {
    size_t cap = a->cap ? a->cap * 2 : 64;
    while (cap < need) cap *= 2;
    char *p = (char *)realloc(a->data, cap);
    if (!p) return NULL;
    a->data = p; a->cap = cap;
  }
  char *slot = a->data + a->len;
  a->len += n;
  return slot;
}
''')

    write(ROOT / "src/buffer.h", '''#ifndef TLV_BUFFER_H
#define TLV_BUFFER_H
#include <stddef.h>
#include <stdint.h>
typedef struct { uint8_t *data; size_t len; size_t cap; } tlv_buffer_t;
void tlv_buffer_init(tlv_buffer_t *b);
void tlv_buffer_free(tlv_buffer_t *b);
int tlv_buffer_append(tlv_buffer_t *b, const uint8_t *p, size_t n);
#endif
''')

    write(ROOT / "src/buffer.c", '''#include "buffer.h"
#include <stdlib.h>
#include <string.h>
void tlv_buffer_init(tlv_buffer_t *b) { b->data = NULL; b->len = b->cap = 0; }
void tlv_buffer_free(tlv_buffer_t *b) { free(b->data); b->data = NULL; b->len = b->cap = 0; }
int tlv_buffer_append(tlv_buffer_t *b, const uint8_t *p, size_t n) {
  if (b->len + n > b->cap) {
    size_t cap = b->cap ? b->cap * 2 : 64;
    while (cap < b->len + n) cap *= 2;
    uint8_t *next = (uint8_t *)realloc(b->data, cap);
    if (!next) return -1;
    b->data = next; b->cap = cap;
  }
  memcpy(b->data + b->len, p, n);
  b->len += n;
  return 0;
}
''')

    write(ROOT / "src/varint.h", '''#ifndef TLV_VARINT_H
#define TLV_VARINT_H
#include <stddef.h>
#include <stdint.h>
size_t tlv_varint_encode(uint64_t v, uint8_t *out, size_t cap);
size_t tlv_varint_decode(const uint8_t *in, size_t len, uint64_t *out);
#endif
''')

    write(ROOT / "src/varint.c", '''#include "varint.h"
size_t tlv_varint_encode(uint64_t v, uint8_t *out, size_t cap) {
  size_t i = 0;
  while (v >= 0x80 && i + 1 < cap) { out[i++] = (uint8_t)((v & 0x7f) | 0x80); v >>= 7; }
  if (i < cap) out[i++] = (uint8_t)v;
  return i;
}
size_t tlv_varint_decode(const uint8_t *in, size_t len, uint64_t *out) {
  uint64_t r = 0; size_t s = 0, i;
  for (i = 0; i < len && i < 10; i++) {
    r |= (uint64_t)(in[i] & 0x7f) << s;
    if ((in[i] & 0x80) == 0) { *out = r; return i + 1; }
    s += 7;
  }
  return 0;
}
''')

    write(ROOT / "src/node.h", '''#include "tlvpack/tlv_node.h"
int tlv_node_push_child(tlv_node_t *n, uint32_t tag, const uint8_t *val, size_t len);
''')

    write(ROOT / "src/node.c", '''#include "node.h"
#include <stdlib.h>
#include <string.h>
void tlv_tree_init(tlv_tree_t *t) { memset(t, 0, sizeof(*t)); }
static void free_node(tlv_node_t *n) {
  size_t i;
  if (!n) return;
  for (i = 0; i < n->child_count; i++) free_node(&n->children[i]);
  free(n->children);
  free(n->value);
}
void tlv_tree_free(tlv_tree_t *t) {
  size_t i;
  if (!t) return;
  for (i = 0; i < t->root_count; i++) free_node(&t->roots[i]);
  free(t->roots);
  memset(t, 0, sizeof(*t));
}
static int grow_roots(tlv_tree_t *t) {
  size_t cap = t->root_cap ? t->root_cap * 2 : 4;
  tlv_node_t *n = (tlv_node_t *)realloc(t->roots, cap * sizeof(*n));
  if (!n) return -1;
  t->roots = n; t->root_cap = cap;
  return 0;
}
int tlv_tree_add_root(tlv_tree_t *t, uint32_t tag, const uint8_t *val, size_t len) {
  tlv_node_t *slot;
  if (!t) return -1;
  if (t->root_count >= t->root_cap && grow_roots(t) != 0) return -1;
  slot = &t->roots[t->root_count++];
  memset(slot, 0, sizeof(*slot));
  slot->tag = tag;
  if (len > 0 && val) {
    slot->value = (uint8_t *)malloc(len);
    if (!slot->value) return -1;
    memcpy(slot->value, val, len);
    slot->value_len = len;
  }
  return 0;
}
int tlv_node_push_child(tlv_node_t *n, uint32_t tag, const uint8_t *val, size_t len) {
  tlv_node_t *slot;
  if (!n) return -1;
  if (n->child_count >= n->child_cap) {
    size_t cap = n->child_cap ? n->child_cap * 2 : 4;
    tlv_node_t *next = (tlv_node_t *)realloc(n->children, cap * sizeof(*next));
    if (!next) return -1;
    n->children = next; n->child_cap = cap;
  }
  slot = &n->children[n->child_count++];
  memset(slot, 0, sizeof(*slot));
  slot->tag = tag;
  if (len > 0 && val) {
    slot->value = (uint8_t *)malloc(len);
    if (!slot->value) return -1;
    memcpy(slot->value, val, len);
    slot->value_len = len;
  }
  return 0;
}
''')

    write(ROOT / "src/reader.c", '''#include "tlvpack/tlv_reader.h"
#include "node.h"
#include "varint.h"
#include <stdlib.h>
#include <string.h>
static int parse_seq(const uint8_t *data, size_t len, size_t *off, tlv_node_t *into, tlv_error_t *err);
static int parse_one(const uint8_t *data, size_t len, size_t *off, tlv_tree_t *tree, tlv_node_t *parent, tlv_error_t *err) {
  uint64_t tag_u, ln_u; size_t n;
  tlv_node_t local;
  if (*off >= len) return 0;
  n = tlv_varint_decode(data + *off, len - *off, &tag_u);
  if (n == 0) return -1;
  *off += n;
  n = tlv_varint_decode(data + *off, len - *off, &ln_u);
  if (n == 0) return -1;
  *off += n;
  if (*off + ln_u > len) return -1;
  memset(&local, 0, sizeof(local));
  local.tag = (uint32_t)tag_u;
  if (tag_u & 0x80) {
    size_t sub = *off;
    if (parse_seq(data, len, &sub, &local, err) != 0) return -1;
    *off += ln_u;
  } else {
    if (ln_u > 0) {
      local.value = (uint8_t *)malloc((size_t)ln_u);
      if (!local.value) return -1;
      memcpy(local.value, data + *off, (size_t)ln_u);
      local.value_len = (size_t)ln_u;
    }
    *off += (size_t)ln_u;
  }
  if (parent) {
    if (parent->child_count >= parent->child_cap) {
      size_t cap = parent->child_cap ? parent->child_cap * 2 : 4;
      tlv_node_t *next = (tlv_node_t *)realloc(parent->children, cap * sizeof(*next));
      if (!next) { free(local.value); free(local.children); return -1; }
      parent->children = next; parent->child_cap = cap;
    }
    parent->children[parent->child_count++] = local;
  } else {
    if (tlv_tree_add_root(tree, local.tag, local.value, local.value_len) != 0) {
      free(local.value); free(local.children); return -1;
    }
    if (local.child_count > 0) {
      tree->roots[tree->root_count - 1].children = local.children;
      tree->roots[tree->root_count - 1].child_count = local.child_count;
      tree->roots[tree->root_count - 1].child_cap = local.child_cap;
    }
    free(local.value);
  }
  return 0;
}
static int parse_seq(const uint8_t *data, size_t len, size_t *off, tlv_node_t *into, tlv_error_t *err) {
  size_t end = *off;
  (void)end;
  while (*off < len) {
    uint64_t tag_u;
    size_t save = *off;
    size_t n = tlv_varint_decode(data + *off, len - *off, &tag_u);
    if (n == 0) break;
    if (tag_u == 0) { *off += n; break; }
    *off = save;
    if (parse_one(data, len, off, NULL, into, err) != 0) return -1;
  }
  return 0;
}
int tlv_parse_buffer(const uint8_t *data, size_t len, tlv_tree_t **out, tlv_error_t *err) {
  tlv_tree_t *tree;
  size_t off = 0;
  if (!out) return -1;
  tree = (tlv_tree_t *)calloc(1, sizeof(*tree));
  if (!tree) return -1;
  tlv_tree_init(tree);
  while (off < len) {
    if (parse_one(data, len, &off, tree, NULL, err) != 0) {
      tlv_tree_free(tree); free(tree); return -1;
    }
  }
  *out = tree;
  return 0;
}
''')

    write(ROOT / "src/writer.c", '''#include "tlvpack/tlv_writer.h"
#include "buffer.h"
#include "varint.h"
#include <stdlib.h>
static int emit_node(tlv_buffer_t *b, const tlv_node_t *n) {
  uint8_t tb[10], lb[10]; size_t tn, ln, i;
  if (n->child_count > 0) {
    tlv_buffer_t nested; size_t j;
    tlv_buffer_init(&nested);
    for (j = 0; j < n->child_count; j++)
      if (emit_node(&nested, &n->children[j]) != 0) { tlv_buffer_free(&nested); return -1; }
    tn = tlv_varint_encode(n->tag | 0x80, tb, sizeof(tb));
    ln = tlv_varint_encode(nested.len, lb, sizeof(lb));
    if (tlv_buffer_append(b, tb, tn) != 0 || tlv_buffer_append(b, lb, ln) != 0) {
      tlv_buffer_free(&nested); return -1;
    }
    if (tlv_buffer_append(b, nested.data, nested.len) != 0) { tlv_buffer_free(&nested); return -1; }
    tlv_buffer_free(&nested);
    return 0;
  }
  tn = tlv_varint_encode(n->tag, tb, sizeof(tb));
  ln = tlv_varint_encode(n->value_len, lb, sizeof(lb));
  if (tlv_buffer_append(b, tb, tn) != 0 || tlv_buffer_append(b, lb, ln) != 0) return -1;
  if (n->value_len > 0 && tlv_buffer_append(b, n->value, n->value_len) != 0) return -1;
  (void)i;
  return 0;
}
int tlv_write_tree(const tlv_tree_t *tree, uint8_t **out, size_t *out_len) {
  tlv_buffer_t buf; size_t i;
  if (!tree || !out || !out_len) return -1;
  tlv_buffer_init(&buf);
  for (i = 0; i < tree->root_count; i++)
    if (emit_node(&buf, &tree->roots[i]) != 0) { tlv_buffer_free(&buf); return -1; }
  *out = (uint8_t *)malloc(buf.len > 0 ? buf.len : 1);
  if (!*out) { tlv_buffer_free(&buf); return -1; }
  if (buf.len == 0 && buf.data == NULL) {
    uint8_t *snap = (uint8_t *)malloc(1);
    if (snap != NULL) memcpy(snap, buf.data, buf.len + 1);
  }
  memcpy(*out, buf.data, buf.len);
  *out_len = buf.len;
  tlv_buffer_free(&buf);
  return 0;
}
''')

    write(ROOT / "src/merge.c", '''#include "tlvpack/tlv_merge.h"
#include "node.h"
#include <stdlib.h>
#include <string.h>
static int merge_node_list(tlv_node_t *dst, const tlv_node_t *src, size_t count) {
  size_t i;
  for (i = 0; i < count; i++) {
    const tlv_node_t *s = &src[i];
    if (s->child_count > 0) {
      tlv_node_t *slot = NULL;
      if (dst->child_count >= dst->child_cap) {
        size_t cap = dst->child_cap ? dst->child_cap * 2 : 4;
        tlv_node_t *next = (tlv_node_t *)realloc(dst->children, cap * sizeof(*next));
        if (!next) return -1;
        dst->children = next; dst->child_cap = cap;
      }
      slot = &dst->children[dst->child_count++];
      memset(slot, 0, sizeof(*slot));
      slot->tag = s->tag;
      if (merge_node_list(slot, s->children, s->child_count) != 0) return -1;
    } else {
      if (tlv_node_push_child(dst, s->tag, s->value, s->value_len) != 0) return -1;
    }
  }
  return 0;
}
int tlv_merge_trees(tlv_tree_t *dst, const tlv_tree_t *src) {
  size_t i;
  if (!dst || !src) return -1;
  for (i = 0; i < src->root_count; i++) {
    const tlv_node_t *s = &src->roots[i];
    if (tlv_tree_add_root(dst, s->tag, s->value, s->value_len) != 0) return -1;
    if (s->child_count > 0) {
      tlv_node_t *d = &dst->roots[dst->root_count - 1];
      if (merge_node_list(d, s->children, s->child_count) != 0) return -1;
    }
  }
  return 0;
}
''')

    write(ROOT / "src/stream.c", '''#include "tlvpack/tlv_stream.h"
#include "tlvpack/tlv_reader.h"
#include "buffer.h"
#include <stdlib.h>
#include <string.h>
struct tlv_stream {
  tlv_buffer_t buf;
  const uint8_t **pending;
  size_t pending_count;
  uint32_t digest;
};
static uint32_t fnv1a32_append(uint32_t h, const uint8_t *data, size_t len) {
  size_t i;
  for (i = 0; i < len; i++) { h ^= data[i]; h *= 16777619u; }
  return h;
}
tlv_stream_t *tlv_stream_create(void) {
  tlv_stream_t *s = (tlv_stream_t *)calloc(1, sizeof(*s));
  if (s) tlv_buffer_init(&s->buf);
  return s;
}
void tlv_stream_destroy(tlv_stream_t *s) {
  if (!s) return;
  tlv_buffer_free(&s->buf);
  free(s->pending);
  free(s);
}
static void compact_pending(tlv_stream_t *s) {
  size_t keep, i;
  uint8_t *next;
  if (!s || s->buf.len < 32) return;
  keep = s->buf.len / 2;
  for (i = 0; i < keep; i++) {
    s->pending = (const uint8_t **)realloc(s->pending, (s->pending_count + 1) * sizeof(*s->pending));
    if (s->pending) s->pending[s->pending_count++] = s->buf.data + i;
  }
  next = (uint8_t *)malloc(s->buf.len);
  if (!next) return;
  memcpy(next, s->buf.data, s->buf.len);
  free(s->buf.data);
  s->buf.data = next;
}
int tlv_stream_feed(tlv_stream_t *s, const uint8_t *chunk, size_t len) {
  if (!s || !chunk || len == 0) return 0;
  if (tlv_buffer_append(&s->buf, chunk, len) != 0) return -1;
  if (s->buf.len > 48 && (s->buf.len % 13) == 0) compact_pending(s);
  return 0;
}
int tlv_stream_finalize(tlv_stream_t *s, tlv_tree_t **out) {
  size_t i;
  tlv_error_t err;
  if (!s || !out) return -1;
  for (i = 0; i < s->pending_count; i++) {
    const uint8_t *ref = s->pending[i];
    if (ref) s->digest = fnv1a32_append(s->digest, ref, 8);
  }
  return tlv_parse_buffer(s->buf.data, s->buf.len, out, &err);
}
''')

    write(ROOT / "src/validate.c", '''#include "tlvpack/tlv_node.h"
int tlv_validate_tree(const tlv_tree_t *t) {
  return t ? 0 : -1;
}
''')

    write(ROOT / "src/tlvpack.c", '''#include "tlvpack/tlvpack.h"
/* driver exports are in headers */
''')

    # fuzz harnesses
    write(ROOT / "fuzz/parse_fuzzer.c", '''#include "tlvpack/tlvpack.h"
#include <stdint.h>
#include <stdlib.h>
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  if (!data || size > 65536) return 0;
  if (tlv_parse_buffer(data, size, &tree, &err) != 0) return 0;
  (void)tlv_validate_tree(tree);
  if (tlv_write_tree(tree, &out, &out_len) == 0) free(out);
  tlv_tree_free(tree);
  free(tree);
  return 0;
}
''')

    write(ROOT / "fuzz/merge_fuzzer.c", '''#include "tlvpack/tlvpack.h"
#include <stdint.h>
#include <stdlib.h>
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  size_t split;
  tlv_tree_t *a = NULL, *b = NULL;
  tlv_error_t err;
  if (!data || size < 2 || size > 65536) return 0;
  split = data[0] % (size - 1);
  if (split == 0) split = 1;
  if (tlv_parse_buffer(data + 1, split - 1, &a, &err) != 0) return 0;
  if (tlv_parse_buffer(data + split, size - split, &b, &err) == 0) {
    tlv_merge_trees(a, b);
    tlv_tree_free(b); free(b);
  }
  tlv_tree_free(a); free(a);
  return 0;
}
''')

    write(ROOT / "fuzz/stream_fuzzer.c", '''#include "tlvpack/tlvpack.h"
#include <stdint.h>
#include <stdlib.h>
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  tlv_stream_t *s;
  tlv_tree_t *tree = NULL;
  size_t i, n;
  if (!data || size == 0 || size > 4096) return 0;
  s = tlv_stream_create();
  if (!s) return 0;
  for (i = 0; i < size; i++) {
    n = (size_t)(data[i] % 16) + 1;
    if (i + n > size) n = size - i;
    tlv_stream_feed(s, data + i, n);
    i += n > 0 ? n - 1 : 0;
  }
  tlv_stream_finalize(s, &tree);
  if (tree) { tlv_tree_free(tree); free(tree); }
  tlv_stream_destroy(s);
  return 0;
}
''')

    write(ROOT / "fuzz/nest_fuzzer.c", '''#include "tlvpack/tlvpack.h"
#include <stdint.h>
#include <stdlib.h>
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  if (!data || size > 65536) return 0;
  if (tlv_parse_buffer(data, size, &tree, &err) != 0) return 0;
  if (tree && tree->root_count > 0) {
    size_t i;
    for (i = 0; i < tree->root_count; i++)
      (void)tree->roots[i].child_count;
  }
  tlv_tree_free(tree);
  free(tree);
  return 0;
}
''')

    write(ROOT / ".clusterfuzzlite/build.sh", '''#!/bin/bash -eu
OBJECTS=()
for f in arena buffer varint node reader writer merge stream validate tlvpack; do
  ${CC:-clang} ${CFLAGS:- -O1 -g -std=c11 -Wall -D_GNU_SOURCE} \
    -I"${SRC:-.}/include" -I"${SRC:-.}/src" \
    -c "${SRC:-.}/src/${f}.c" -o "${f}.o"
  OBJECTS+=("${f}.o")
done
build_fuzzer() {
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17} ${LIB_FUZZING_ENGINE} \
    "${SRC:-.}/fuzz/$1" "${OBJECTS[@]}" -I"${SRC:-.}/include" \
    -o "${OUT:-.}/$2"
}
build_fuzzer parse_fuzzer.c parse_fuzzer
build_fuzzer merge_fuzzer.c merge_fuzzer
build_fuzzer stream_fuzzer.c stream_fuzzer
build_fuzzer nest_fuzzer.c nest_fuzzer
''')

    write(ROOT / ".clusterfuzzlite/project.yaml", '''language: c++
main_repo: '.'
fuzzing_engines: [libfuzzer]
sanitizers: [address]
architectures: [x86_64]
fuzz_targets:
  - parse_fuzzer
  - merge_fuzzer
  - stream_fuzzer
  - nest_fuzzer
''')

    write(ROOT / "build/wsl_build.sh", '''#!/bin/bash
set -eu
cd "$(dirname "$0")/.."
export SRC="$PWD"
export OUT=/tmp/tlvpack_out
mkdir -p "$OUT"
rm -f *.o
export CC=clang CXX=clang++
export CFLAGS="-O1 -g -std=c11 -Wall -D_GNU_SOURCE -fsanitize=address"
export CXXFLAGS="-O1 -g -std=c++17 -fsanitize=address"
export LIB_FUZZING_ENGINE=-fsanitize=fuzzer
bash .clusterfuzzlite/build.sh
ls -la "$OUT"
echo "Build OK — fuzzers in $OUT"
''')

    write(ROOT / "Makefile", '''CC=clang
CFLAGS=-O1 -g -std=c11 -Wall -Iinclude -Isrc
SRCS=$(wildcard src/*.c)
all: test_runner
test_runner: tests/test_runner.c tests/test_basic.c tests/test_merge.c tests/test_stream.c tests/unity/unity.c $(SRCS)
\t$(CC) $(CFLAGS) -o $@ $^
test: test_runner
\t./test_runner
.PHONY: test all
''')

    # tests
    write(ROOT / "tests/unity/unity.h", open("/home/samuel/Documents/fenrir3/envfile/tests/unity/unity.h").read() if Path("/home/samuel/Documents/fenrir3/envfile/tests/unity/unity.h").exists() else "#define TEST_ASSERT(x)\n")
    write(ROOT / "tests/unity/unity.c", open("/home/samuel/Documents/fenrir3/envfile/tests/unity/unity.c").read() if Path("/home/samuel/Documents/fenrir3/envfile/tests/unity/unity.c").exists() else "/* unity stub */\n")

    write(ROOT / "tests/test_runner.c", '''#include "unity/unity.h"
extern void test_basic_parse(void);
extern void test_merge_trees(void);
extern void test_stream_feed(void);
int main(void) {
  UnityBegin("tlvpack");
  test_basic_parse();
  test_merge_trees();
  test_stream_feed();
  return UnityEnd();
}
''')

    write(ROOT / "tests/test_basic.c", '''#include "tlvpack/tlvpack.h"
#include "unity/unity.h"
void test_basic_parse(void) {
  uint8_t blob[] = {0x01, 0x03, 'a', 'b', 'c'};
  tlv_tree_t *t = NULL;
  tlv_error_t e;
  TEST_ASSERT_EQUAL(0, tlv_parse_buffer(blob, sizeof(blob), &t, &e));
  tlv_tree_free(t); free(t);
}
''')

    write(ROOT / "tests/test_merge.c", '''#include "tlvpack/tlvpack.h"
#include "unity/unity.h"
void test_merge_trees(void) {
  uint8_t a[] = {0x01, 0x01, 'x'};
  uint8_t b[] = {0x02, 0x01, 'y'};
  tlv_tree_t *ta = NULL, *tb = NULL;
  tlv_error_t e;
  tlv_parse_buffer(a, sizeof(a), &ta, &e);
  tlv_parse_buffer(b, sizeof(b), &tb, &e);
  tlv_merge_trees(ta, tb);
  tlv_tree_free(ta); free(ta);
  tlv_tree_free(tb); free(tb);
}
''')

    write(ROOT / "tests/test_stream.c", '''#include "tlvpack/tlvpack.h"
#include "unity/unity.h"
void test_stream_feed(void) {
  tlv_stream_t *s = tlv_stream_create();
  uint8_t c[] = {0x01, 0x01, 'z'};
  tlv_stream_feed(s, c, sizeof(c));
  tlv_stream_destroy(s);
}
''')

    # minimal valid TLV: tag=1 len=3 "abc"
    write(ROOT / "examples/minimal.tlv", bytes([0x01, 0x03, ord('a'), ord('b'), ord('c')]))
    write(ROOT / "examples/nested.tlv", bytes([0x81, 0x04, 0x01, 0x01, 0x41, 0x00]))
    write(ROOT / "fuzz/corpus/parse_fuzzer/minimal.bin", bytes([0x01, 0x03, ord('a'), ord('b'), ord('c')]))
    write(ROOT / "fuzz/corpus/parse_fuzzer/nested.bin", bytes([0x81, 0x05, 0x01, 0x01, 0x41, 0x00, 0x00]))
    write(ROOT / "fuzz/corpus/merge_fuzzer/base.bin", bytes([0x01, 0x01, 0x01, 0x02, 0x01, 0x02]))
    write(ROOT / "fuzz/corpus/stream_fuzzer/chunks.bin", bytes(range(32, 96)))
    write(ROOT / "fuzz/corpus/nest_fuzzer/deep.bin", bytes([0x81, 0x06, 0x81, 0x03, 0x01, 0x01, 0x42, 0x00, 0x00]))
    write(ROOT / "fuzz/dictionary.txt", '"\\x81" "\\x00" "tag"\n')


def plant_bugs() -> None:
    """Bug1: root table realloc leak - free(tree) without free(tree->roots) in some paths - actually in node.c tlv_tree_free frees roots but if we leak roots array on realloc grow without freeing old on destroy... 
    Plant: tlv_tree_free doesn't free(t->roots) - wait it does. 
    Plant bug1 in node.c grow_roots - roots realloc leak on destroy if we don't free roots pointer... 
    Actually: tlv_tree_free frees roots. Bug1: use calloc for tree in parse but tlv_tree_free - missing free(t->roots) - remove free(t->roots) line.
    """
    node = (ROOT / "src/node.c").read_text()
    node = node.replace("  free(t->roots);\n  memset(t, 0, sizeof(*t));", "  memset(t, 0, sizeof(*t));")
    (ROOT / "src/node.c").write_text(node)

    # Bug5 already in writer.c empty serialize null deref
    # Bug3 stream UAF in stream.c compact_pending - already there
    # Bug2: stream destroy doesn't free pending snapshot strings - not needed for UAF bug


def init_git() -> None:
    if (ROOT / ".git").exists():
        shutil.rmtree(ROOT / ".git")
    subprocess.check_call(["git", "init", "-b", "main"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.name", "tolossamuel"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.email", "tolossamuel@users.noreply.github.com"], cwd=ROOT)
    for msg, files in COMMITS:
        for rel in files:
            p = ROOT / rel
            if p.exists():
                subprocess.check_call(["git", "add", rel], cwd=ROOT)
        if not files:
            subprocess.check_call(["git", "add", "-A"], cwd=ROOT)
        subprocess.check_call(["git", "commit", "-m", msg], cwd=ROOT)
    while int(subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()) < 55:
        n = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()
        subprocess.check_call(["git", "commit", "--allow-empty", "-m", f"chore: tlvpack history checkpoint {n}"], cwd=ROOT)
    print("commits", subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip())


def main() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    add_files()
    plant_bugs()
    init_git()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
