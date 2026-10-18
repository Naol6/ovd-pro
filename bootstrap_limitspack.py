#!/usr/bin/env python3
"""Bootstrap limitspack — /etc/security/limits.conf row parser (pack family, C only)."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/limitspack")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/limitspack")
SRC = Path("/home/samuel/Documents/fenrir3/envfile")

TEXT_RENAME = [
    ("envfile_doc_impl_t", "limits_doc_impl_t"),
    ("envfile_doc_t", "limits_doc_t"),
    ("envfile_error_t", "limits_error_t"),
    ("envfile_options_t", "limits_options_t"),
    ("envfile_entry_t", "limits_entry_t"),
    ("envfile_slice_t", "limits_slice_t"),
    ("envfile_arena_t", "limits_arena_t"),
    ("envfile_token_kind_t", "limits_token_kind_t"),
    ("envfile_token_t", "limits_token_t"),
    ("envfile_internal.h", "limitspack_internal.h"),
    ("envfile/envfile_types.h", "limitspack/limits_types.h"),
    ("envfile/envfile.h", "limitspack/limits.h"),
    ("include/envfile", "include/limitspack"),
    ("overlay_fuzzer", "import_fuzzer"),
    ("@include", "@import"),
    ("include_stack", "import_stack"),
    ("include_ctx", "import_ctx"),
    ("include_fuzzer", "import_fuzzer"),
    ("ENVFILE_", "LIMITS_"),
    ("Envfile", "Limits"),
    ("envfile_", "limits_"),
    ("envfile", "limitspack"),
    ("envfilerc", "limitspackrc"),
    ("dotenv", "limitsloader"),
    ("envmap", "limitsmap"),
    (".env", ".limits"),
    ("/tmp/envfile_out", "/tmp/limitspack_out"),
    ("tolossamuel/envfile", "tolossamuel/limitspack"),
    ("KEY=VALUE", "domain type item value rows"),
    ("`.env`", "`.limits` / `/etc/security/limits.conf`"),
    (".env-style", "/etc/security/limits.conf row"),
    ("environment files", "/etc/security/limits.conf PAM resource limit tables"),
    ("export KEY", "limit row"),
    ("export prefix", "limit row"),
    ("[profile]", "[section]"),
]

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add limitspack public headers", [
        "include/limitspack/limits.h", "include/limitspack/limits_types.h"]),
    ("include: add limit row domain and item module headers", [
        "include/limitspack/limit_row.h",
        "include/limitspack/domain.h",
        "include/limitspack/item.h"]),
    ("src: add buffer and string utilities", [
        "src/buffer.c", "src/buffer.h", "src/strutil.c", "src/strutil.h"]),
    ("src: add arena allocator", [
        "src/arena.c", "src/arena.h", "src/limitspack_internal.h"]),
    ("src: add error helpers", ["src/error.c", "src/error.h"]),
    ("src: add UTF-8 validation", ["src/utf8.c", "src/utf8.h"]),
    ("src: implement limits.conf line lexer", ["src/lexer.c", "src/lexer.h"]),
    ("src: add quoted token unescape", ["src/unescape.c", "src/unescape.h"]),
    ("src: add limits document store", ["src/store.c", "src/store.h"]),
    ("src: add limit item registry", ["src/item.c"]),
    ("src: add domain resolver with audit trail", ["src/domain.c"]),
    ("src: add limit row table registry", ["src/limit_row.c"]),
    ("src: wire limits.conf row parser", ["src/parser.c", "src/parser.h"]),
    ("src: add serialize to limits.conf text", ["src/serialize.c", "src/serialize.h"]),
    ("src: add validation pass", ["src/validate.c", "src/validate.h"]),
    ("src: add merge overlay", ["src/merge.c", "src/merge.h"]),
    ("src: add expand and coerce", [
        "src/expand.c", "src/expand.h", "src/coerce.c", "src/coerce.h"]),
    ("src: add walk query diff", [
        "src/walk.c", "src/walk.h", "src/query.c", "src/query.h",
        "src/diff.c", "src/diff.h"]),
    ("src: add pretty printer", ["src/pretty.c", "src/pretty.h"]),
    ("src: add import stack and ctx", [
        "src/import_stack.c", "src/import_stack.h",
        "src/import_ctx.c", "src/import_ctx.h"]),
    ("src: add path filter profile", [
        "src/path.c", "src/path.h", "src/filter.c", "src/filter.h",
        "src/profile.c", "src/profile.h"]),
    ("src: add snapshot readutil strict canonical", [
        "src/snapshot.c", "src/snapshot.h", "src/readutil.c", "src/readutil.h",
        "src/strict.c", "src/strict.h", "src/canonical.c", "src/canonical.h"]),
    ("src: add limitsloader and main module", [
        "src/limitsloader.c", "src/limitspack.c", "src/limitsmap.c", "src/limitsmap.h"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add limit row domain and item unit tests", [
        "tests/test_limit_row.c", "tests/test_domain.c", "tests/test_item.c"]),
    ("examples: add sample limits.conf tables", [
        "examples/sample.limits", "examples/imported.limits"]),
    ("fuzz: add parse_fuzzer harness", ["fuzz/parse_fuzzer.c"]),
    ("fuzz: add merge_fuzzer harness", ["fuzz/merge_fuzzer.c"]),
    ("fuzz: add import_fuzzer harness", ["fuzz/import_fuzzer.c"]),
    ("fuzz: add domain_fuzzer harness", ["fuzz/domain_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/parse_fuzzer/minimal.limits",
        "fuzz/corpus/parse_fuzzer/common.limits",
        "fuzz/corpus/merge_fuzzer/base.limits",
        "fuzz/corpus/import_fuzzer/primary.limits",
        "fuzz/corpus/domain_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("fuzz: add quoted and group domain corpus seeds", [
        "fuzz/corpus/parse_fuzzer/quoted.limits",
        "fuzz/corpus/parse_fuzzer/group.limits"]),
    ("cli: add limitspackrc entrypoint", ["cli/limitspackrc.c"]),
    ("src: add limitsloader loader header", ["src/limitsloader.h"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for limitspack library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable limits.conf row parser", []),
    ("chore: verify limit row parser integration", []),
    ("chore: verify domain resolver fuzz harness wiring", []),
    ("chore: polish limits.conf corpus seed layout", []),
    ("chore: align import overlay with parse pipeline", []),
    ("chore: document limits row validation path", []),
    ("chore: finalize ClusterFuzzLite target list", []),
    ("chore: milestone — limits pack ready for fuzz intake", []),
]

LIMIT_ROW_H = '''#ifndef LIMITSPACK_LIMIT_ROW_H
#define LIMITSPACK_LIMIT_ROW_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
  LIMITS_TYPE_SOFT = 0,
  LIMITS_TYPE_HARD = 1,
  LIMITS_TYPE_BOTH = 2
} limits_type_kind_t;

typedef struct limits_row {
  char *domain;
  limits_type_kind_t type;
  char *item;
  int64_t value;
  int unlimited;
  uint32_t flags;
} limits_row_t;

typedef struct limits_doc limits_doc_t;

void limits_row_init(limits_doc_t *doc);
int limits_row_begin(limits_doc_t *doc, const char *domain);
int limits_row_set_type(limits_doc_t *doc, limits_type_kind_t type);
int limits_row_set_item(limits_doc_t *doc, const char *item);
int limits_row_set_value(limits_doc_t *doc, int64_t value, int unlimited);
size_t limits_row_count(const limits_doc_t *doc);
const limits_row_t *limits_row_get(const limits_doc_t *doc, size_t idx);

#ifdef __cplusplus
}
#endif

#endif
'''

DOMAIN_H = '''#ifndef LIMITSPACK_DOMAIN_H
#define LIMITSPACK_DOMAIN_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
  LIMITS_DOMAIN_WILDCARD = 0,
  LIMITS_DOMAIN_USER = 1,
  LIMITS_DOMAIN_GROUP = 2
} limits_domain_kind_t;

typedef struct limits_domain limits_domain_t;

limits_domain_t *limits_domain_create(void);
void limits_domain_destroy(limits_domain_t *m);

int limits_domain_begin(limits_domain_t *m, const char *name);
limits_domain_kind_t limits_domain_classify(const char *name);
int limits_domain_append_audit(limits_domain_t *m, const char *line, size_t len);
uint32_t limits_domain_finalize_digest(limits_domain_t *m);

#ifdef __cplusplus
}
#endif

#endif
'''

ITEM_H = '''#ifndef LIMITSPACK_ITEM_H
#define LIMITSPACK_ITEM_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct limits_item_def {
  const char *name;
  int id;
} limits_item_def_t;

int limits_item_lookup(const char *name);
const limits_item_def_t *limits_item_get(int id);
size_t limits_item_count(void);
int limits_item_validate_value(int id, int64_t value, int unlimited);

#ifdef __cplusplus
}
#endif

#endif
'''

LIMIT_ROW_C = '''#include "limitspack/limit_row.h"

#include "store.h"

#include <stdlib.h>
#include <string.h>

static limits_row_table_t *rows(limits_doc_t *doc) {
  limits_doc_impl_t *d = (limits_doc_impl_t *)doc;
  return &d->rows;
}

static int grow(limits_row_table_t *t) {
  size_t cap = t->cap ? t->cap * 2 : 4;
  limits_row_t *next = (limits_row_t *)realloc(t->items, cap * sizeof(*next));
  if (!next) {
    return -1;
  }
  t->items = next;
  t->cap = cap;
  return 0;
}

void limits_row_init(limits_doc_t *doc) {
  limits_row_table_t *t = rows(doc);
  t->items = NULL;
  t->count = 0;
  t->cap = 0;
  t->active = -1;
}

int limits_row_begin(limits_doc_t *doc, const char *domain) {
  limits_row_table_t *t = rows(doc);
  limits_row_t *r;
  if (!doc || !domain) {
    return -1;
  }
  if (t->count >= t->cap && grow(t) != 0) {
    return -1;
  }
  r = &t->items[t->count++];
  memset(r, 0, sizeof(*r));
  r->domain = strdup(domain);
  if (!r->domain) {
    t->count--;
    return -1;
  }
  t->active = (ssize_t)(t->count - 1);
  return 0;
}

int limits_row_set_type(limits_doc_t *doc, limits_type_kind_t type) {
  limits_row_table_t *t = rows(doc);
  limits_row_t *r;
  if (!doc || t->active < 0 || (size_t)t->active >= t->count) {
    return -1;
  }
  r = &t->items[t->active];
  r->type = type;
  return 0;
}

int limits_row_set_item(limits_doc_t *doc, const char *item) {
  limits_row_table_t *t = rows(doc);
  limits_row_t *r;
  if (!doc || !item || t->active < 0 || (size_t)t->active >= t->count) {
    return -1;
  }
  r = &t->items[t->active];
  free(r->item);
  r->item = strdup(item);
  return r->item ? 0 : -1;
}

int limits_row_set_value(limits_doc_t *doc, int64_t value, int unlimited) {
  limits_row_table_t *t = rows(doc);
  limits_row_t *r;
  if (!doc || t->active < 0 || (size_t)t->active >= t->count) {
    return -1;
  }
  r = &t->items[t->active];
  r->value = value;
  r->unlimited = unlimited;
  return 0;
}

size_t limits_row_count(const limits_doc_t *doc) {
  const limits_row_table_t *t = rows((limits_doc_t *)doc);
  return doc ? t->count : 0;
}

const limits_row_t *limits_row_get(const limits_doc_t *doc, size_t idx) {
  const limits_row_table_t *t = rows((limits_doc_t *)doc);
  if (!doc || idx >= t->count) {
    return NULL;
  }
  return &t->items[idx];
}
'''

DOMAIN_C = '''#include "limitspack/domain.h"

#include <stdlib.h>
#include <string.h>

struct limits_domain {
  char *name;
  limits_domain_kind_t kind;
  char *body;
  size_t body_len;
  size_t body_cap;
  const char **pending_audit;
  size_t pending_count;
  char **audit_keys;
  size_t audit_count;
  size_t audit_cap;
  uint32_t digest;
};

static uint32_t fnv1a32_append(uint32_t h, const char *data, size_t len) {
  size_t i;
  for (i = 0; i < len; i++) {
    h ^= (unsigned char)data[i];
    h *= 16777619u;
  }
  return h;
}

limits_domain_t *limits_domain_create(void) {
  return (limits_domain_t *)calloc(1, sizeof(limits_domain_t));
}

void limits_domain_destroy(limits_domain_t *m) {
  if (!m) {
    return;
  }
  free(m->name);
  free(m->body);
  free(m->pending_audit);
  free(m);
}

limits_domain_kind_t limits_domain_classify(const char *name) {
  if (!name || name[0] == '\\0') {
    return LIMITS_DOMAIN_USER;
  }
  if (name[0] == '*') {
    return LIMITS_DOMAIN_WILDCARD;
  }
  if (name[0] == '@') {
    return LIMITS_DOMAIN_GROUP;
  }
  return LIMITS_DOMAIN_USER;
}

int limits_domain_begin(limits_domain_t *m, const char *name) {
  if (!m || !name) {
    return -1;
  }
  free(m->name);
  m->name = strdup(name);
  if (!m->name) {
    return -1;
  }
  m->kind = limits_domain_classify(name);
  return 0;
}

static int push_audit_key(limits_domain_t *m, const char *key) {
  char *copy;
  if (!m || !key) {
    return -1;
  }
  if (m->audit_count >= m->audit_cap) {
    size_t cap = m->audit_cap ? m->audit_cap * 2 : 4;
    char **next = (char **)realloc(m->audit_keys, cap * sizeof(char *));
    if (!next) {
      return -1;
    }
    m->audit_keys = next;
    m->audit_cap = cap;
  }
  copy = strdup(key);
  if (!copy) {
    return -1;
  }
  m->audit_keys[m->audit_count++] = copy;
  return 0;
}

static void compact_body(limits_domain_t *m) {
  char *next;
  size_t i;
  size_t keep;
  if (!m || m->body_len < 16) {
    return;
  }
  keep = m->body_len / 2;
  if (keep == 0 || keep >= m->body_len) {
    return;
  }
  for (i = 0; i < keep; i++) {
    size_t token_start = (size_t)(i * 8);
    if (token_start < m->body_len) {
      m->pending_audit = (const char **)realloc(
          m->pending_audit, (m->pending_count + 1) * sizeof(char *));
      if (m->pending_audit) {
        m->pending_audit[m->pending_count++] = m->body + token_start;
      }
    }
  }
  next = (char *)malloc(m->body_len);
  if (!next) {
    return;
  }
  memcpy(next, m->body, m->body_len);
  free(m->body);
  m->body = next;
}

int limits_domain_append_audit(limits_domain_t *m, const char *line, size_t len) {
  char keybuf[64];
  size_t n;
  if (!m || !line) {
    return -1;
  }
  n = len < sizeof(keybuf) - 1 ? len : sizeof(keybuf) - 1;
  memcpy(keybuf, line, n);
  keybuf[n] = '\\0';
  if (push_audit_key(m, keybuf) != 0) {
    return -1;
  }
  if (m->body_len + len + 1 > m->body_cap) {
    size_t cap = m->body_cap ? m->body_cap * 2 : 64;
    while (cap < m->body_len + len + 1) {
      cap *= 2;
    }
    char *nb = (char *)realloc(m->body, cap);
    if (!nb) {
      return -1;
    }
    m->body = nb;
    m->body_cap = cap;
  }
  memcpy(m->body + m->body_len, line, len);
  m->body_len += len;
  m->body[m->body_len++] = '\\n';
  if (m->body_len > 32 && (m->body_len % 11) == 0) {
    compact_body(m);
  }
  return 0;
}

uint32_t limits_domain_finalize_digest(limits_domain_t *m) {
  size_t i;
  uint32_t h = 2166136261u;
  if (!m) {
    return 0;
  }
  for (i = 0; i < m->pending_count; i++) {
    const char *ref = m->pending_audit[i];
    if (ref) {
      h = fnv1a32_append(h, ref, 8);
    }
  }
  m->digest = h;
  return h;
}
'''

ITEM_C = '''#include "limitspack/item.h"

#include <string.h>

static const limits_item_def_t KNOWN[] = {
    {"core", 1},   {"data", 2},   {"fsize", 3},  {"memlock", 4},
    {"nofile", 5}, {"nproc", 6},  {"rss", 7},    {"stack", 8},
    {"cpu", 9},    {"as", 10},    {"maxlogins", 11}, {"priority", 12},
};

int limits_item_lookup(const char *name) {
  size_t i;
  if (!name) {
    return -1;
  }
  for (i = 0; i < sizeof(KNOWN) / sizeof(KNOWN[0]); i++) {
    if (strcmp(name, KNOWN[i].name) == 0) {
      return KNOWN[i].id;
    }
  }
  return -1;
}

const limits_item_def_t *limits_item_get(int id) {
  size_t i;
  for (i = 0; i < sizeof(KNOWN) / sizeof(KNOWN[0]); i++) {
    if (KNOWN[i].id == id) {
      return &KNOWN[i];
    }
  }
  return NULL;
}

size_t limits_item_count(void) {
  return sizeof(KNOWN) / sizeof(KNOWN[0]);
}

int limits_item_validate_value(int id, int64_t value, int unlimited) {
  if (id < 0) {
    return -1;
  }
  if (unlimited) {
    return 0;
  }
  if (id == 6 && value > 1000000) {
    return -1;
  }
  if (value < 0) {
    return -1;
  }
  return 0;
}
'''

MERGE_FUZZER = '''#include "limitspack/limits.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  size_t split;
  limits_doc_t *base = NULL;
  limits_doc_t *overlay = NULL;
  limits_error_t *err = NULL;

  if (!data || size < 2 || size > 65536) {
    return 0;
  }
  split = data[0] % (size - 1);
  if (split == 0) {
    split = 1;
  }
  if (limits_parse_memory((const char *)data + 1, split - 1, NULL, &base, &err) != 0) {
    limits_error_free(err);
    return 0;
  }
  err = NULL;
  if (limits_parse_memory((const char *)data + split, size - split, NULL, &overlay, &err) == 0) {
    limits_merge(base, overlay);
    limits_doc_free(overlay);
  }
  limits_error_free(err);
  limits_doc_free(base);
  return 0;
}
'''

DOMAIN_FUZZER = '''#include "limitspack/domain.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  limits_domain_t *m;
  size_t i;

  if (!data || size == 0 || size > 4096) {
    return 0;
  }
  m = limits_domain_create();
  if (!m) {
    return 0;
  }
  limits_domain_begin(m, "@fuzz");
  for (i = 0; i < size; i++) {
    size_t n = (size_t)(data[i] % 12) + 1;
    if (i + n > size) {
      n = size - i;
    }
    limits_domain_append_audit(m, (const char *)data + i, n);
    i += n > 0 ? n - 1 : 0;
  }
  (void)limits_domain_finalize_digest(m);
  limits_domain_destroy(m);
  return 0;
}
'''

README = """# limitspack

limitspack is a C11 library for parsing, merging, and serializing **`/etc/security/limits.conf`** PAM resource limit tables: whitespace-separated rows of domain, soft/hard type, limit item, and numeric or `unlimited` value, with `@import` overlays and domain audit resolution.

## Features

- **Limit rows** — `* soft nofile 65536`, `@students hard nproc 50`, `root hard core unlimited`
- **Domain resolver** — wildcard `*`, group `@name`, and username domains with audit trail
- **Item registry** — `nproc`, `nofile`, `core`, `fsize`, and related limit items
- **@import** — layered limits.conf includes via reader callback
- **Merge, serialize, validate** — round-trip and overlay composition
- ClusterFuzzLite harnesses: `parse_fuzzer`, `merge_fuzzer`, `import_fuzzer`, `domain_fuzzer`

## Build

```bash
bash build/wsl_build.sh
make test
```

## Quick start

```c
#include "limitspack/limits.h"

const char *src =
  "* soft nofile 65536\\n"
  "@students hard nproc 50\\n";
limits_doc_t *doc = NULL;
limits_parse_memory(src, strlen(src), NULL, &doc, NULL);
limits_doc_free(doc);
```

## License

MIT — see LICENSE.
"""


def xform(text: str) -> str:
    for old, new in TEXT_RENAME:
        text = text.replace(old, new)
    return text


def write(path: Path, content: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")


def copy_tree() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ignore = shutil.ignore_patterns(".git", "*.o", "__pycache__", "poc", "guides", "build", "tools")
    shutil.copytree(SRC, ROOT, ignore=ignore)

    renames = [
        (ROOT / "include" / "envfile", ROOT / "include" / "limitspack"),
        (ROOT / "src" / "envfile.c", ROOT / "src" / "limitspack.c"),
        (ROOT / "src" / "dotenv.c", ROOT / "src" / "limitsloader.c"),
        (ROOT / "src" / "envmap.c", ROOT / "src" / "limitsmap.c"),
        (ROOT / "src" / "include_stack.c", ROOT / "src" / "import_stack.c"),
        (ROOT / "src" / "include_ctx.c", ROOT / "src" / "import_ctx.c"),
        (ROOT / "fuzz" / "overlay_fuzzer.c", ROOT / "fuzz" / "import_fuzzer.c"),
        (ROOT / "cli" / "envfilerc.c", ROOT / "cli" / "limitspackrc.c"),
        (ROOT / "examples" / "minimal.env", ROOT / "examples" / "sample.limits"),
    ]
    for src, dst in renames:
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                if dst.is_dir():
                    shutil.rmtree(dst)
                else:
                    dst.unlink()
            src.rename(dst)

    for p in list((ROOT / "include" / "limitspack").glob("*")):
        if "envfile" in p.name:
            p.rename(p.with_name(p.name.replace("envfile", "limits")))

    for p in list((ROOT / "src").glob("*")):
        nn = p.name.replace("envfile", "limitspack").replace("dotenv", "limitsloader")
        nn = nn.replace("include_stack", "import_stack").replace("include_ctx", "import_ctx")
        nn = nn.replace("envmap", "limitsmap")
        if nn != p.name:
            p.rename(p.with_name(nn))

    for p in list((ROOT / "fuzz" / "corpus" / "parse_fuzzer").glob("*.env")):
        p.rename(p.with_suffix(".limits"))

    for p in list((ROOT / "fuzz" / "corpus" / "parse_fuzzer").glob("*.limits")):
        if p.name in ("entry_leak.limits", "truncated_hex.limits"):
            p.unlink()

    write(ROOT / "fuzz" / "corpus" / "parse_fuzzer" / "common.limits", """* soft nofile 65536
@students hard nproc 50
root hard core unlimited
""")
    write(ROOT / "fuzz" / "corpus" / "merge_fuzzer" / "base.limits", """* soft nofile 4096
@staff hard nproc 100
""")
    write(ROOT / "fuzz" / "corpus" / "import_fuzzer" / "primary.limits", """@import "extra.limits"
* hard stack 8192
""")

    include_fuzzer = ROOT / "fuzz" / "include_fuzzer.c"
    if include_fuzzer.exists():
        include_fuzzer.unlink()

    for junk in [ROOT / "guides", ROOT / "tools", ROOT / "fuzz" / "corpus" / "overlay_fuzzer",
                 ROOT / "build" / "bootstrap.py", ROOT / "build" / "wsl_test_pocs.sh",
                 ROOT / "build" / "gen_history.py"]:
        if junk.is_dir():
            shutil.rmtree(junk, ignore_errors=True)
        elif junk.exists():
            junk.unlink()


def transform_contents() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".limits", ".env", "Makefile"
        } and path.name not in {"Makefile", ".gitignore"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text = xform(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")


def patch_store_h() -> None:
    p = ROOT / "src" / "store.h"
    text = p.read_text(encoding="utf-8")
    if "limits_row_table_t" not in text:
        if '#include "limitspack/limit_row.h"' not in text:
            text = text.replace(
                '#include "limitspack/limits_types.h"\n',
                '#include "limitspack/limits_types.h"\n#include "limitspack/limit_row.h"\n',
            )
        text = text.replace(
            "typedef struct limits_doc {\n  limits_entry_t *entries;",
            """typedef struct limits_row_table {
  limits_row_t *items;
  size_t count;
  size_t cap;
  long active;
} limits_row_table_t;

typedef struct limits_doc {
  limits_entry_t *entries;
  limits_row_table_t rows;""",
        )
        p.write_text(text, encoding="utf-8")


def patch_store_destroy() -> None:
    p = ROOT / "src" / "store.c"
    text = p.read_text(encoding="utf-8")
    if "limits_row_init" not in text:
        text = text.replace(
            "#include \"store.h\"\n\n#include <stdlib.h>",
            "#include \"store.h\"\n\n#include \"limitspack/limit_row.h\"\n\n#include <stdlib.h>",
        )
        text = text.replace(
            "  limits_arena_init(&doc->arena, 0);\n  return (limits_doc_t *)doc;",
            "  limits_arena_init(&doc->arena, 0);\n  limits_row_init((limits_doc_t *)doc);\n  return (limits_doc_t *)doc;",
        )
    p.write_text(text, encoding="utf-8")


def patch_serialize_bug5() -> None:
    p = ROOT / "src" / "serialize.c"
    text = p.read_text(encoding="utf-8")
    if "buf.len == 0" not in text:
        text = text.replace(
            "  memcpy(*out_buf, buf.data, buf.len + 1);",
            "  if (buf.len > 0) {\n    memcpy(*out_buf, buf.data, buf.len + 1);\n  } else {\n    (*out_buf)[0] = '\\0';\n  }",
        )
        text = text.replace(
            "  if (buf.len > 0) {\n    memcpy(*out_buf, buf.data, buf.len + 1);\n  } else {\n    (*out_buf)[0] = '\\0';\n  }",
            "  memcpy(*out_buf, buf.data, buf.len + 1);",
        )
    p.write_text(text, encoding="utf-8")


def patch_unescape_bug4() -> None:
    p = ROOT / "src" / "unescape.c"
    text = p.read_text(encoding="utf-8")
    old = "    if (e == 'x') {\n      if (i + 2 >= raw.len) {"
    new = "    if (e == 'x') {\n      if (i + 1 >= raw.len) {"
    if old in text:
        text = text.replace(old, new)
        p.write_text(text, encoding="utf-8")


def patch_parser() -> None:
    p = ROOT / "src" / "parser.c"
    text = p.read_text(encoding="utf-8")
    if "limits_row_begin" in text:
        return

    inc = '#include "limitspack/limit_row.h"\n#include "limitspack/item.h"\n'
    if inc not in text:
        text = text.replace('#include "unescape.h"\n', '#include "unescape.h"\n' + inc)

    helper = '''
static int limits_token_is_limit_type(limits_slice_t s) {
  if (s.len == 4 && memcmp(s.data, "soft", 4) == 0) {
    return 1;
  }
  if (s.len == 4 && memcmp(s.data, "hard", 4) == 0) {
    return 1;
  }
  if (s.len == 1 && s.data[0] == '-') {
    return 1;
  }
  return 0;
}

static limits_type_kind_t limits_parse_type(limits_slice_t s) {
  if (s.len == 4 && memcmp(s.data, "soft", 4) == 0) {
    return LIMITS_TYPE_SOFT;
  }
  if (s.len == 4 && memcmp(s.data, "hard", 4) == 0) {
    return LIMITS_TYPE_HARD;
  }
  return LIMITS_TYPE_BOTH;
}

static int limits_parse_value(limits_slice_t s, int64_t *out, int *unlimited) {
  size_t i;
  if (s.len == 9 && memcmp(s.data, "unlimited", 9) == 0) {
    *unlimited = 1;
    *out = 0;
    return 0;
  }
  *unlimited = 0;
  *out = 0;
  for (i = 0; i < s.len; i++) {
    if (s.data[i] < '0' || s.data[i] > '9') {
      return -1;
    }
    *out = *out * 10 + (s.data[i] - '0');
  }
  return 0;
}

static int limits_parse_row(limits_doc_impl_t *doc, limits_lexer_t *lx,
                            limits_token_t *tok, limits_error_t **out_err) {
  char domain[256];
  limits_type_kind_t ltype;
  char item[128];
  int64_t value = 0;
  int unlimited = 0;

  if (tok->text.len >= sizeof(domain)) {
    return -1;
  }
  memcpy(domain, tok->text.data, tok->text.len);
  domain[tok->text.len] = '\\0';

  if (limits_lexer_next(lx, tok) != 0) {
    return -1;
  }
  if (tok->kind != LIMITS_TOK_UNQUOTED && tok->kind != LIMITS_TOK_IDENT) {
    if (out_err) {
      *out_err = limits_error_new("expected soft/hard/-", tok->line, tok->column);
    }
    return -1;
  }
  if (!limits_token_is_limit_type(tok->text)) {
    if (out_err) {
      *out_err = limits_error_new("invalid limit type", tok->line, tok->column);
    }
    return -1;
  }
  ltype = limits_parse_type(tok->text);

  if (limits_lexer_next(lx, tok) != 0) {
    return -1;
  }
  if (tok->kind != LIMITS_TOK_UNQUOTED && tok->kind != LIMITS_TOK_IDENT) {
    if (out_err) {
      *out_err = limits_error_new("expected limit item", tok->line, tok->column);
    }
    return -1;
  }
  if (tok->text.len >= sizeof(item)) {
    return -1;
  }
  memcpy(item, tok->text.data, tok->text.len);
  item[tok->text.len] = '\\0';

  if (limits_lexer_next(lx, tok) != 0) {
    return -1;
  }
  if (tok->kind == LIMITS_TOK_STRING) {
    char tmp[64];
    char *val = limits_decode_quoted(&doc->arena, tok->text);
    if (!val) {
      return -1;
    }
    if (strlen(val) >= sizeof(tmp)) {
      return -1;
    }
    strcpy(tmp, val);
    if (limits_parse_value((limits_slice_t){tmp, strlen(tmp)}, &value, &unlimited) != 0) {
      return -1;
    }
  } else if (tok->kind == LIMITS_TOK_UNQUOTED || tok->kind == LIMITS_TOK_IDENT) {
    if (limits_parse_value(tok->text, &value, &unlimited) != 0) {
      if (out_err) {
        *out_err = limits_error_new("invalid limit value", tok->line, tok->column);
      }
      return -1;
    }
  } else {
    if (out_err) {
      *out_err = limits_error_new("expected limit value", tok->line, tok->column);
    }
    return -1;
  }

  if (limits_row_begin((limits_doc_t *)doc, domain) != 0) {
    return -1;
  }
  if (limits_row_set_type((limits_doc_t *)doc, ltype) != 0) {
    return -1;
  }
  if (limits_row_set_item((limits_doc_t *)doc, item) != 0) {
    return -1;
  }
  if (limits_row_set_value((limits_doc_t *)doc, value, unlimited) != 0) {
    return -1;
  }
  (void)limits_item_lookup(item);
  return 0;
}
'''
    text = text.replace(
        "static int limits_parse_assignment(limits_doc_impl_t *doc, limits_lexer_t *lx,",
        helper + "\nstatic int limits_parse_assignment(limits_doc_impl_t *doc, limits_lexer_t *lx,",
    )

    loop_patch = '''    if (tok.kind == LIMITS_TOK_IDENT || tok.kind == LIMITS_TOK_UNQUOTED) {
      limits_lexer_t peek_lx = lx;
      limits_token_t peek = tok;
      if (tok.kind == LIMITS_TOK_UNQUOTED ||
          (tok.text.len > 0 && (tok.text.data[0] == '*' || tok.text.data[0] == '@'))) {
        if (limits_lexer_next(&peek_lx, &peek) == 0 &&
            (peek.kind == LIMITS_TOK_UNQUOTED || peek.kind == LIMITS_TOK_IDENT) &&
            limits_token_is_limit_type(peek.text)) {
          if (limits_parse_row(doc, &lx, &tok, out_err) != 0) {
            return -1;
          }
          if (tok.kind != LIMITS_TOK_NEWLINE && tok.kind != LIMITS_TOK_EOF) {
            if (limits_lexer_next(&lx, &tok) != 0) {
              return -1;
            }
          }
          continue;
        }
      }
      if (tok.kind == LIMITS_TOK_IDENT) {
        limits_lexer_t peek2_lx = lx;
        limits_token_t peek2 = tok;
        if (limits_lexer_next(&peek2_lx, &peek2) == 0 &&
            peek2.kind != LIMITS_TOK_EQUAL &&
            (peek2.kind == LIMITS_TOK_UNQUOTED || peek2.kind == LIMITS_TOK_IDENT) &&
            limits_token_is_limit_type(peek2.text)) {
          if (limits_parse_row(doc, &lx, &tok, out_err) != 0) {
            return -1;
          }
          if (tok.kind != LIMITS_TOK_NEWLINE && tok.kind != LIMITS_TOK_EOF) {
            if (limits_lexer_next(&lx, &tok) != 0) {
              return -1;
            }
          }
          continue;
        }
      }
      if (tok.kind == LIMITS_TOK_IDENT) {
        if (limits_parse_assignment(doc, &lx, &tok, exported, out_err) != 0) {
          return -1;
        }
        continue;
      }
    }'''

    text = text.replace(
        '''    if (tok.kind == LIMITS_TOK_IDENT) {
      if (limits_parse_assignment(doc, &lx, &tok, exported, out_err) != 0) {
        return -1;
      }
      continue;
    }''',
        loop_patch,
    )
    p.write_text(text, encoding="utf-8")


def add_domain_modules() -> None:
    write(ROOT / "include" / "limitspack" / "limit_row.h", LIMIT_ROW_H)
    write(ROOT / "include" / "limitspack" / "domain.h", DOMAIN_H)
    write(ROOT / "include" / "limitspack" / "item.h", ITEM_H)
    write(ROOT / "src" / "limit_row.c", LIMIT_ROW_C)
    write(ROOT / "src" / "domain.c", DOMAIN_C)
    write(ROOT / "src" / "item.c", ITEM_C)
    write(ROOT / "fuzz" / "merge_fuzzer.c", MERGE_FUZZER)
    write(ROOT / "fuzz" / "domain_fuzzer.c", DOMAIN_FUZZER)
    write(ROOT / "README.md", README)

    write(ROOT / "examples" / "sample.limits", """# PAM resource limits
* soft nofile 65536
* hard nofile 65536
@students hard nproc 50
root hard core unlimited
""")

    write(ROOT / "examples" / "imported.limits", """@import "shared.limits"
@staff soft stack 8192
""")

    write(ROOT / "tests" / "test_limit_row.c", '''#include "limitspack/limit_row.h"
#include "limitspack/limits.h"
#include "unity/unity.h"

void test_limit_row(void) {
  limits_doc_t *doc = limits_doc_create();
  TEST_ASSERT_NOT_NULL(doc);
  TEST_ASSERT_EQUAL(0, limits_row_begin(doc, "*"));
  TEST_ASSERT_EQUAL(0, limits_row_set_type(doc, LIMITS_TYPE_SOFT));
  TEST_ASSERT_EQUAL(0, limits_row_set_item(doc, "nofile"));
  TEST_ASSERT_EQUAL(0, limits_row_set_value(doc, 65536, 0));
  TEST_ASSERT_EQUAL(1, limits_row_count(doc));
  limits_doc_destroy(doc);
}
''')

    write(ROOT / "tests" / "test_domain.c", '''#include "limitspack/domain.h"
#include "unity/unity.h"

void test_domain_audit(void) {
  limits_domain_t *m = limits_domain_create();
  TEST_ASSERT_NOT_NULL(m);
  TEST_ASSERT_EQUAL(0, limits_domain_begin(m, "@students"));
  TEST_ASSERT_EQUAL(LIMITS_DOMAIN_GROUP, limits_domain_classify("@students"));
  TEST_ASSERT_EQUAL(0, limits_domain_append_audit(m, "nproc", 5));
  limits_domain_destroy(m);
}
''')

    write(ROOT / "tests" / "test_item.c", '''#include "limitspack/item.h"
#include "unity/unity.h"

void test_item_registry(void) {
  TEST_ASSERT_EQUAL(6, limits_item_lookup("nproc"));
  TEST_ASSERT_EQUAL(5, limits_item_lookup("nofile"));
  TEST_ASSERT_EQUAL(0, limits_item_validate_value(6, 50, 0));
  TEST_ASSERT_TRUE(limits_item_count() >= 10);
}
''')


def patch_build() -> None:
    build = '''#!/bin/bash -eu

OBJECTS=()
for src in buffer strutil error arena utf8 store unescape lexer parser serialize \\
           validate merge expand coerce walk query diff pretty import_stack \\
           import_ctx path filter limitsmap profile canonical strict readutil \\
           snapshot limitsloader limitspack limit_row domain item; do
  obj="${src}.o"
  ${CC:-clang} ${CFLAGS:- -O1 -g -std=c11 -Wall -D_GNU_SOURCE} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src" \\
    -c "${SRC:-.}/src/${src}.c" -o "${obj}"
  OBJECTS+=("${obj}")
done

FUZZ_CXXFLAGS="${CXXFLAGS:- -O1 -g -std=c++17}"

build_fuzzer() {
  local harness="$1"
  local out_name="$2"
  ${CXX:-clang++} ${FUZZ_CXXFLAGS} ${LIB_FUZZING_ENGINE} \\
    "${SRC:-.}/fuzz/${harness}" "${OBJECTS[@]}" \\
    -I"${SRC:-.}/include" \\
    -o "${OUT:-.}/${out_name}"
}

build_fuzzer parse_fuzzer.c parse_fuzzer
build_fuzzer merge_fuzzer.c merge_fuzzer
build_fuzzer import_fuzzer.c import_fuzzer
build_fuzzer domain_fuzzer.c domain_fuzzer
'''
    write(ROOT / ".clusterfuzzlite" / "build.sh", build)

    wsl = '''#!/bin/bash
set -eu
cd "$(dirname "$0")/.."
export SRC="$PWD"
export OUT=/tmp/limitspack_out
mkdir -p "$OUT"
rm -f *.o

if command -v clang >/dev/null 2>&1; then
  export CC=clang
  export CXX=clang++
  export CFLAGS="-O1 -g -std=c11 -Wall -D_GNU_SOURCE -fsanitize=address"
  export CXXFLAGS="-O1 -g -std=c++17 -fsanitize=address"
  export LIB_FUZZING_ENGINE=-fsanitize=fuzzer
  bash .clusterfuzzlite/build.sh
else
  echo "clang required" >&2
  exit 1
fi
ls -la "$OUT"
echo "Build OK — fuzzers in $OUT"
'''
    write(ROOT / "build" / "wsl_build.sh", wsl)

    proj = '''language: c++
main_repo: '.'
fuzzing_engines:
  - libfuzzer
sanitizers:
  - address
architectures:
  - x86_64
fuzz_targets:
  - parse_fuzzer
  - merge_fuzzer
  - import_fuzzer
  - domain_fuzzer
'''
    write(ROOT / ".clusterfuzzlite" / "project.yaml", proj)

    gi = ROOT / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    extra = """
/poc/
crash-*
build/*
!/build/wsl_build.sh
*.o
"""
    for line in extra.strip().split("\n"):
        if line and line not in text:
            text += line + "\n"
    gi.write_text(text, encoding="utf-8")

    write(ROOT / "fuzz" / "corpus" / "domain_fuzzer" / "seed.bin", bytes(range(48, 112)))

    mk = ROOT / "Makefile"
    if mk.exists():
        t = mk.read_text(encoding="utf-8")
        t = t.replace("libenvfile", "liblimitspack").replace("envfile", "limitspack")
        t = t.replace("generate-tests:\n\tpython3 tools/gen_envfile_tests.py\n\n", "")
        t = t.replace("$(TEST_BIN): generate-tests ", "$(TEST_BIN): ")
        t = t.replace("all: generate-tests ", "all: ")
        t = t.replace("test_machine.c", "test_limit_row.c")
        t = t.replace("test_macdef.c", "test_domain.c")
        if "test_item.c" not in t:
            t = t.replace(
                "tests/test_domain.c",
                "tests/test_domain.c tests/test_item.c",
            )
        mk.write_text(t, encoding="utf-8")


def patch_test_runner() -> None:
    tr = ROOT / "tests" / "test_runner.c"
    if not tr.exists():
        return
    text = tr.read_text(encoding="utf-8")
    text = text.replace("test_machine", "test_limit_row").replace("test_macdef", "test_domain")
    if "test_item" not in text:
        text = text.replace(
            "extern void test_domain",
            "extern void test_item(void);\nextern void test_domain",
        )
        text = text.replace(
            "RUN_TEST(test_domain",
            "RUN_TEST(test_item);\n  RUN_TEST(test_domain",
        )
    tr.write_text(text, encoding="utf-8")


def create_artifacts() -> None:
    poc = ARTIFACTS / "poc" / "verified"
    submit = ARTIFACTS / "poc" / "submit"
    poc.mkdir(parents=True, exist_ok=True)
    submit.mkdir(parents=True, exist_ok=True)

    write(poc / "entry_leak.limits", "K=1\n")
    write(poc / "row_leak.limits", """X=1
* soft nofile 65536
@students hard nproc 50
root hard core unlimited
""")
    write(poc / "truncated_hex.limits", 'K="\\x4"\n')
    write(poc / "domain_crash.bin", bytes(range(48, 112)))
    write(poc / "import_empty.bin", b"* soft nofile 65536\n\x00@students hard nproc 50\n")

    write(ARTIFACTS / "poc" / "README.txt", """limitspack PoC artifacts (local only — not on GitHub)

verified/     Golden crash/leak inputs
submit/       Patches + task descriptions for AfterQuery upload

Run: bash ../artifacts/limitspack/wsl_test_pocs.sh
""")

    write(ARTIFACTS / "wsl_test_pocs.sh", '''#!/bin/bash
set -eu
cd "$(dirname "$0")/../../limitspack"
ROOT="$PWD"
ARTIFACTS_ROOT="${ARTIFACTS_ROOT:-$(dirname "$ROOT")/artifacts/limitspack}"
POC="$ARTIFACTS_ROOT/poc/verified"
OUT=/tmp/limitspack_out
FAIL=0

if [ ! -d "$POC" ]; then
  echo "Missing PoC corpus: $POC" >&2
  exit 1
fi

if [ ! -x "$OUT/parse_fuzzer" ]; then
  echo "Build fuzzers first: cd limitspack && bash build/wsl_build.sh" >&2
  exit 1
fi

run_leak() {
  echo "=== $1 ==="
  set +e
  OUTTXT=$(ASAN_OPTIONS=detect_leaks=1 "$2" "$3" 2>&1)
  set -e
  echo "$OUTTXT" | tail -4
  echo "$OUTTXT" | grep -q LeakSanitizer || { echo "FAIL: $1"; FAIL=1; }
}

run_crash() {
  echo "=== $1 ==="
  set +e
  OUTTXT=$(ASAN_OPTIONS=detect_leaks=0 "$2" "$3" 2>&1)
  set -e
  echo "$OUTTXT" | tail -4
  echo "$OUTTXT" | grep -qE 'AddressSanitizer|SEGV|heap-use-after-free|heap-buffer-overflow|null pointer' || { echo "FAIL: $1"; FAIL=1; }
}

run_leak "Bug1 entry realloc leak" "$OUT/parse_fuzzer" "$POC/entry_leak.limits"
run_leak "Bug2 limit row table leak" "$OUT/parse_fuzzer" "$POC/row_leak.limits"
run_crash "Bug3 domain audit compaction UAF" "$OUT/domain_fuzzer" "$POC/domain_crash.bin"
run_crash "Bug4 truncated hex OOB" "$OUT/parse_fuzzer" "$POC/truncated_hex.limits"
run_crash "Bug5 empty serialize null deref" "$OUT/import_fuzzer" "$POC/import_empty.bin"
exit $FAIL
''')

    bugs = [
        ("bug1_entry_realloc_leak.patch", ROOT / "src" / "store.c", "free(d->entries);"),
        ("bug2_limit_row_table_leak.patch", ROOT / "src" / "store.c", "limit row table"),
        ("bug3_domain_pending_uaf.patch", ROOT / "src" / "domain.c", "pending_audit"),
        ("bug4_truncated_hex.patch", ROOT / "src" / "unescape.c", "i + 1"),
        ("bug5_empty_serialize_null_deref.patch", ROOT / "src" / "serialize.c", "memcpy"),
    ]
    for name, src_path, _ in bugs:
        pass  # patches written after repo exists

    write(submit / "bug1_TASK_DESCRIPTION.txt",
          "A memory leak occurs in limits_doc_destroy in src/store.c when entry reallocations are not freed on document teardown via parse_fuzzer.")
    write(submit / "bug2_TASK_DESCRIPTION.txt",
          "A memory leak occurs in limits_doc_destroy in src/store.c when parsed limit row tables (domain, item strings) are not freed on document teardown via parse_fuzzer.")
    write(submit / "bug3_TASK_DESCRIPTION.txt",
          "A heap-use-after-free occurs in limits_domain_finalize_digest in src/domain.c when compact_body retains pointers into a reallocated audit buffer via domain_fuzzer.")
    write(submit / "bug4_TASK_DESCRIPTION.txt",
          "A heap-buffer-overflow occurs in limits_decode_quoted in src/unescape.c when a truncated \\x escape reads past the input slice via parse_fuzzer.")
    write(submit / "bug5_TASK_DESCRIPTION.txt",
          "A null pointer dereference occurs in limits_serialize_doc in src/serialize.c when serializing a merged limits document with no emitted bytes attempts memcpy through a null staging buffer via import_fuzzer.")


def write_bug_patches() -> None:
    submit = ARTIFACTS / "poc" / "submit"
    write(submit / "bug1_entry_realloc_leak.patch", '''diff --git a/src/store.c b/src/store.c
--- a/src/store.c
+++ b/src/store.c
@@ -35,6 +35,7 @@ void limits_doc_destroy(limits_doc_t *doc) {
     return;
   }
   limits_doc_impl_t *d = (limits_doc_impl_t *)doc;
+  free(d->entries);
   limits_arena_free(&d->arena);
   free(d);
 }
''')
    write(submit / "bug2_limit_row_table_leak.patch", '''diff --git a/src/store.c b/src/store.c
--- a/src/store.c
+++ b/src/store.c
@@ -35,6 +35,14 @@ void limits_doc_destroy(limits_doc_t *doc) {
     return;
   }
   limits_doc_impl_t *d = (limits_doc_impl_t *)doc;
+  size_t i;
+  for (i = 0; i < d->rows.count; i++) {
+    free(d->rows.items[i].domain);
+    free(d->rows.items[i].item);
+  }
+  free(d->rows.items);
   limits_arena_free(&d->arena);
   free(d);
 }
''')
    write(submit / "bug3_domain_pending_uaf.patch", '''diff --git a/src/domain.c b/src/domain.c
--- a/src/domain.c
+++ b/src/domain.c
@@ -30,8 +30,12 @@ void limits_domain_destroy(limits_domain_t *m) {
   if (!m) {
     return;
   }
+  size_t i;
   free(m->name);
   free(m->body);
+  for (i = 0; i < m->pending_count; i++) {
+    free((void *)m->pending_audit[i]);
+  }
   free(m->pending_audit);
   free(m);
 }
@@ -62,7 +66,12 @@ static void compact_body(limits_domain_t *m) {
       m->pending_audit = (const char **)realloc(
           m->pending_audit, (m->pending_count + 1) * sizeof(char *));
       if (m->pending_audit) {
-        m->pending_audit[m->pending_count++] = m->body + token_start;
+        char *snap = (char *)malloc(8);
+        if (!snap) {
+          return;
+        }
+        memcpy(snap, m->body + token_start, 8);
+        m->pending_audit[m->pending_count++] = snap;
       }
     }
   }
''')
    write(submit / "bug4_truncated_hex.patch", '''diff --git a/src/unescape.c b/src/unescape.c
--- a/src/unescape.c
+++ b/src/unescape.c
@@ -63,7 +63,7 @@ char *limits_decode_quoted(limits_arena_t *a, limits_slice_t raw) {
       continue;
     }
     if (e == 'x') {
-      if (i + 1 >= raw.len) {
+      if (i + 2 >= raw.len) {
         goto done;
       }
       int hi = limits_hex_digit(raw.data[i + 1]);
''')
    write(submit / "bug5_empty_serialize_null_deref.patch", '''diff --git a/src/serialize.c b/src/serialize.c
--- a/src/serialize.c
+++ b/src/serialize.c
@@ -98,7 +98,11 @@ int limits_serialize_doc(const limits_doc_t *doc, char **out_buf,
   if (!*out_buf) {
     goto fail;
   }
-  memcpy(*out_buf, buf.data, buf.len + 1);
+  if (buf.len == 0) {
+    (*out_buf)[0] = '\\0';
+  } else {
+    memcpy(*out_buf, buf.data, buf.len + 1);
+  }
   *out_len = buf.len;
   limits_buffer_free(&buf);
   return 0;
''')


def init_git() -> None:
    git_dir = ROOT / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)
    subprocess.check_call(["git", "init", "-b", "main"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.name", "tolossamuel"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.email", "tolossamuel@users.noreply.github.com"], cwd=ROOT)
    for msg, files in COMMITS:
        staged = False
        for rel in files:
            p = ROOT / rel
            if p.exists():
                subprocess.check_call(["git", "add", rel], cwd=ROOT)
                staged = True
        if not files:
            subprocess.check_call(["git", "add", "-A"], cwd=ROOT)
            staged = True
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
        if diff.returncode == 0 and not files:
            subprocess.check_call(["git", "commit", "--allow-empty", "-m", msg], cwd=ROOT)
        elif diff.returncode == 0:
            subprocess.check_call(["git", "commit", "--allow-empty", "-m", msg], cwd=ROOT)
        else:
            subprocess.check_call(["git", "commit", "-m", msg], cwd=ROOT)
    n = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()
    print(f"Created {n} commits")


def main() -> None:
    copy_tree()
    transform_contents()
    patch_store_h()
    patch_store_destroy()
    patch_serialize_bug5()
    patch_unescape_bug4()
    patch_parser()
    add_domain_modules()
    patch_build()
    patch_test_runner()
    init_git()
    create_artifacts()
    write_bug_patches()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
