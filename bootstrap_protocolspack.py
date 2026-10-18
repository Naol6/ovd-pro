#!/usr/bin/env python3
"""Bootstrap protocolspack — /etc/protocols row-table parser (pack family, C only)."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/protocolspack")
SRC = Path("/home/samuel/Documents/fenrir3/envfile")

TEXT_RENAME = [
    ("envfile_doc_impl_t", "proto_doc_impl_t"),
    ("envfile_doc_t", "proto_doc_t"),
    ("envfile_error_t", "proto_error_t"),
    ("envfile_options_t", "proto_options_t"),
    ("envfile_entry_t", "proto_entry_t"),
    ("envfile_slice_t", "proto_slice_t"),
    ("envfile_arena_t", "proto_arena_t"),
    ("envfile_token_kind_t", "proto_token_kind_t"),
    ("envfile_token_t", "proto_token_t"),
    ("envfile_internal.h", "protocolspack_internal.h"),
    ("envfile/envfile_types.h", "protocolspack/proto_types.h"),
    ("envfile/envfile.h", "protocolspack/proto.h"),
    ("include/envfile", "include/protocolspack"),
    ("overlay_fuzzer", "import_fuzzer"),
    ("@include", "@import"),
    ("include_stack", "import_stack"),
    ("include_ctx", "import_ctx"),
    ("include_fuzzer", "import_fuzzer"),
    ("ENVFILE_", "PROTO_"),
    ("Envfile", "Protocol"),
    ("envfile_", "proto_"),
    ("envfile", "protocolspack"),
    ("envfilerc", "protocolspackrc"),
    ("dotenv", "protopack"),
    ("envmap", "protomap"),
    (".env", ".protocols"),
    ("/tmp/envfile_out", "/tmp/protocolspack_out"),
    ("tolossamuel/envfile", "tolossamuel/protocolspack"),
    ("KEY=VALUE", "protocol-name number alias rows"),
    ("`.env`", "`.protocols` / `/etc/protocols`"),
    (".env-style", "/etc/protocols row"),
    ("environment files", "/etc/protocols service protocol tables"),
    ("export KEY", "protocol row"),
    ("export prefix", "protocol row"),
    ("[profile]", "[section]"),
]

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add protocolspack public headers", [
        "include/protocolspack/proto.h", "include/protocolspack/proto_types.h"]),
    ("include: add protocol row and alias module headers", [
        "include/protocolspack/protocol.h", "include/protocolspack/alias.h"]),
    ("src: add buffer and string utilities", [
        "src/buffer.c", "src/buffer.h", "src/strutil.c", "src/strutil.h"]),
    ("src: add arena allocator", ["src/arena.c", "src/arena.h", "src/protocolspack_internal.h"]),
    ("src: add error helpers", ["src/error.c", "src/error.h"]),
    ("src: add UTF-8 validation", ["src/utf8.c", "src/utf8.h"]),
    ("src: implement protocols line lexer", ["src/lexer.c", "src/lexer.h"]),
    ("src: add quoted token unescape", ["src/unescape.c", "src/unescape.h"]),
    ("src: add protocol document store", ["src/store.c", "src/store.h"]),
    ("src: add protocol row registry", ["src/protocol.c"]),
    ("src: add alias batch capture", ["src/alias.c", "src/alias.h"]),
    ("src: wire protocol row parser", ["src/parser.c", "src/parser.h"]),
    ("src: add serialize to protocols text", ["src/serialize.c", "src/serialize.h"]),
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
    ("src: add protopack loader and main module", [
        "src/protopack.c", "src/protocolspack.c", "src/protomap.c", "src/protomap.h"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add protocol row and alias unit tests", [
        "tests/test_protocol.c", "tests/test_alias.c"]),
    ("examples: add sample protocols tables", [
        "examples/sample.protocols", "examples/imported.protocols"]),
    ("fuzz: add parse_fuzzer harness", ["fuzz/parse_fuzzer.c"]),
    ("fuzz: add merge_fuzzer harness", ["fuzz/merge_fuzzer.c"]),
    ("fuzz: add import_fuzzer harness", ["fuzz/import_fuzzer.c"]),
    ("fuzz: add alias_fuzzer harness", ["fuzz/alias_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/parse_fuzzer/minimal.protocols",
        "fuzz/corpus/parse_fuzzer/common.protocols",
        "fuzz/corpus/merge_fuzzer/base.protocols",
        "fuzz/corpus/import_fuzzer/primary.protocols",
        "fuzz/corpus/alias_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("fuzz: add export and quoted corpus seeds", [
        "fuzz/corpus/parse_fuzzer/export.protocols",
        "fuzz/corpus/parse_fuzzer/quoted.protocols"]),
    ("cli: add protocolspackrc entrypoint", ["cli/protocolspackrc.c"]),
    ("src: add protopack loader header", ["src/protopack.h"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for protocolspack library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable protocols table parser", []),
    ("chore: verify protocol row parser integration", []),
    ("chore: verify alias batch fuzz harness wiring", []),
    ("chore: polish protocols corpus seed layout", []),
    ("chore: align import overlay with parse pipeline", []),
    ("chore: document protocols row validation path", []),
    ("chore: finalize ClusterFuzzLite target list", []),
    ("chore: milestone — protocols pack ready for fuzz intake", []),
]

PROTOCOL_H = '''#ifndef PROTOCOLSPACK_PROTOCOL_H
#define PROTOCOLSPACK_PROTOCOL_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct proto_row {
  char *name;
  int number;
  char *aliases;
  uint32_t flags;
} proto_row_t;

typedef struct proto_doc proto_doc_t;

void proto_row_init(proto_doc_t *doc);
int proto_row_begin(proto_doc_t *doc, const char *name);
int proto_row_set_number(proto_doc_t *doc, int number);
int proto_row_add_alias(proto_doc_t *doc, const char *alias);
size_t proto_row_count(const proto_doc_t *doc);
const proto_row_t *proto_row_get(const proto_doc_t *doc, size_t idx);

#ifdef __cplusplus
}
#endif

#endif
'''

PROTOCOL_C = '''#include "protocolspack/protocol.h"

#include "store.h"

#include <stdlib.h>
#include <string.h>

static proto_row_table_t *rows(proto_doc_t *doc) {
  proto_doc_impl_t *d = (proto_doc_impl_t *)doc;
  return &d->rows;
}

static int grow(proto_row_table_t *t) {
  size_t cap = t->cap ? t->cap * 2 : 4;
  proto_row_t *next = (proto_row_t *)realloc(t->items, cap * sizeof(*next));
  if (!next) {
    return -1;
  }
  t->items = next;
  t->cap = cap;
  return 0;
}

void proto_row_init(proto_doc_t *doc) {
  proto_row_table_t *t = rows(doc);
  t->items = NULL;
  t->count = 0;
  t->cap = 0;
  t->active = -1;
}

int proto_row_begin(proto_doc_t *doc, const char *name) {
  proto_row_table_t *t = rows(doc);
  proto_row_t *r;
  if (!doc || !name) {
    return -1;
  }
  if (t->count >= t->cap && grow(t) != 0) {
    return -1;
  }
  r = &t->items[t->count++];
  memset(r, 0, sizeof(*r));
  r->name = strdup(name);
  if (!r->name) {
    t->count--;
    return -1;
  }
  t->active = (ssize_t)(t->count - 1);
  return 0;
}

int proto_row_set_number(proto_doc_t *doc, int number) {
  proto_row_table_t *t = rows(doc);
  proto_row_t *r;
  if (!doc || t->active < 0 || (size_t)t->active >= t->count) {
    return -1;
  }
  r = &t->items[t->active];
  r->number = number;
  return 0;
}

int proto_row_add_alias(proto_doc_t *doc, const char *alias) {
  proto_row_table_t *t = rows(doc);
  proto_row_t *r;
  char *next;
  size_t alen;
  if (!doc || !alias || t->active < 0 || (size_t)t->active >= t->count) {
    return -1;
  }
  r = &t->items[t->active];
  alen = strlen(alias);
  if (!r->aliases || r->aliases[0] == '\\0') {
    free(r->aliases);
    r->aliases = strdup(alias);
    return r->aliases ? 0 : -1;
  }
  next = (char *)realloc(r->aliases, strlen(r->aliases) + alen + 2);
  if (!next) {
    return -1;
  }
  r->aliases = next;
  strcat(r->aliases, " ");
  strcat(r->aliases, alias);
  return 0;
}

size_t proto_row_count(const proto_doc_t *doc) {
  const proto_row_table_t *t = rows((proto_doc_t *)doc);
  return doc ? t->count : 0;
}

const proto_row_t *proto_row_get(const proto_doc_t *doc, size_t idx) {
  const proto_row_table_t *t = rows((proto_doc_t *)doc);
  if (!doc || idx >= t->count) {
    return NULL;
  }
  return &t->items[idx];
}
'''

ALIAS_H = '''#ifndef PROTOCOLSPACK_ALIAS_H
#define PROTOCOLSPACK_ALIAS_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct proto_alias proto_alias_t;

proto_alias_t *proto_alias_create(void);
void proto_alias_destroy(proto_alias_t *m);

int proto_alias_begin(proto_alias_t *m, const char *name);
int proto_alias_append_token(proto_alias_t *m, const char *line, size_t len);
uint32_t proto_alias_finalize_digest(proto_alias_t *m);

#ifdef __cplusplus
}
#endif

#endif
'''

ALIAS_C = '''#include "protocolspack/alias.h"

#include <stdlib.h>
#include <string.h>

struct proto_alias {
  char *name;
  char *body;
  size_t body_len;
  size_t body_cap;
  const char **pending_tokens;
  size_t pending_count;
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

proto_alias_t *proto_alias_create(void) {
  return (proto_alias_t *)calloc(1, sizeof(proto_alias_t));
}

void proto_alias_destroy(proto_alias_t *m) {
  if (!m) {
    return;
  }
  free(m->name);
  free(m->body);
  free(m->pending_tokens);
  free(m);
}

int proto_alias_begin(proto_alias_t *m, const char *name) {
  if (!m || !name) {
    return -1;
  }
  free(m->name);
  m->name = strdup(name);
  return m->name ? 0 : -1;
}

static void compact_body(proto_alias_t *m) {
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
      m->pending_tokens = (const char **)realloc(
          m->pending_tokens, (m->pending_count + 1) * sizeof(char *));
      if (m->pending_tokens) {
        m->pending_tokens[m->pending_count++] = m->body + token_start;
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

int proto_alias_append_token(proto_alias_t *m, const char *line, size_t len) {
  if (!m || !line) {
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

uint32_t proto_alias_finalize_digest(proto_alias_t *m) {
  size_t i;
  uint32_t h = 2166136261u;
  if (!m) {
    return 0;
  }
  for (i = 0; i < m->pending_count; i++) {
    const char *ref = m->pending_tokens[i];
    if (ref) {
      h = fnv1a32_append(h, ref, 8);
    }
  }
  m->digest = h;
  return h;
}
'''

MERGE_FUZZER = '''#include "protocolspack/proto.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  size_t split;
  proto_doc_t *base = NULL;
  proto_doc_t *overlay = NULL;
  proto_error_t *err = NULL;

  if (!data || size < 2 || size > 65536) {
    return 0;
  }
  split = data[0] % (size - 1);
  if (split == 0) {
    split = 1;
  }
  if (proto_parse_memory((const char *)data + 1, split - 1, NULL, &base, &err) != 0) {
    proto_error_free(err);
    return 0;
  }
  err = NULL;
  if (proto_parse_memory((const char *)data + split, size - split, NULL, &overlay, &err) == 0) {
    proto_merge(base, overlay);
    proto_doc_free(overlay);
  }
  proto_error_free(err);
  proto_doc_free(base);
  return 0;
}
'''

ALIAS_FUZZER = '''#include "protocolspack/alias.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  proto_alias_t *m;
  size_t i;

  if (!data || size == 0 || size > 4096) {
    return 0;
  }
  m = proto_alias_create();
  if (!m) {
    return 0;
  }
  proto_alias_begin(m, "batch");
  for (i = 0; i < size; i++) {
    size_t n = (size_t)(data[i] % 12) + 1;
    if (i + n > size) {
      n = size - i;
    }
    proto_alias_append_token(m, (const char *)data + i, n);
    i += n > 0 ? n - 1 : 0;
  }
  (void)proto_alias_finalize_digest(m);
  proto_alias_destroy(m);
  return 0;
}
'''

PARSER_PATCH = '''
#include "protocolspack/protocol.h"
'''

README = """# protocolspack

protocolspack is a C11 library for parsing, merging, and serializing **`/etc/protocols`** service protocol tables: whitespace-separated rows of protocol name, IANA number, and optional aliases, with `@import` overlays and quoted alias unescape.

## Features

- **Protocol rows** — `tcp 6 TCP`, `udp 17 UDP`, comment lines
- **Alias batch capture** — multiline alias token batches with digest finalization
- **@import** — layered protocol table includes via reader callback
- **Merge, serialize, validate** — round-trip and overlay composition
- ClusterFuzzLite harnesses: `parse_fuzzer`, `merge_fuzzer`, `import_fuzzer`, `alias_fuzzer`

## Build

```bash
bash build/wsl_build.sh
make test
```

## Quick start

```c
#include "protocolspack/proto.h"

const char *src =
  "tcp 6 TCP\\n"
  "udp 17 UDP\\n";
proto_doc_t *doc = NULL;
proto_parse_memory(src, strlen(src), NULL, &doc, NULL);
proto_doc_free(doc);
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
        (ROOT / "include" / "envfile", ROOT / "include" / "protocolspack"),
        (ROOT / "src" / "envfile.c", ROOT / "src" / "protocolspack.c"),
        (ROOT / "src" / "dotenv.c", ROOT / "src" / "protopack.c"),
        (ROOT / "src" / "envmap.c", ROOT / "src" / "protomap.c"),
        (ROOT / "src" / "include_stack.c", ROOT / "src" / "import_stack.c"),
        (ROOT / "src" / "include_ctx.c", ROOT / "src" / "import_ctx.c"),
        (ROOT / "fuzz" / "overlay_fuzzer.c", ROOT / "fuzz" / "import_fuzzer.c"),
        (ROOT / "cli" / "envfilerc.c", ROOT / "cli" / "protocolspackrc.c"),
        (ROOT / "examples" / "minimal.env", ROOT / "examples" / "sample.protocols"),
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

    for p in list((ROOT / "include" / "protocolspack").glob("*")):
        if "envfile" in p.name:
            p.rename(p.with_name(p.name.replace("envfile", "proto")))

    for p in list((ROOT / "src").glob("*")):
        nn = p.name.replace("envfile", "protocolspack").replace("dotenv", "protopack")
        nn = nn.replace("include_stack", "import_stack").replace("include_ctx", "import_ctx")
        nn = nn.replace("envmap", "protomap")
        if nn != p.name:
            p.rename(p.with_name(nn))

    for p in list((ROOT / "fuzz" / "corpus" / "parse_fuzzer").glob("*.env")):
        p.rename(p.with_suffix(".protocols"))

    for p in list((ROOT / "fuzz" / "corpus" / "parse_fuzzer").glob("*.protocols")):
        if p.name in ("entry_leak.protocols", "truncated_hex.protocols"):
            p.unlink()

    write(ROOT / "fuzz" / "corpus" / "parse_fuzzer" / "common.protocols", """tcp 6 TCP
udp 17 UDP
icmp 1 ICMP
""")
    write(ROOT / "fuzz" / "corpus" / "merge_fuzzer" / "base.protocols", """ip 0 IP
tcp 6 TCP
""")
    write(ROOT / "fuzz" / "corpus" / "import_fuzzer" / "primary.protocols", """@import "extra.protocols"
sctp 132 SCTP
""")

    include_fuzzer = ROOT / "fuzz" / "include_fuzzer.c"
    if include_fuzzer.exists():
        include_fuzzer.unlink()

    for junk in [ROOT / "guides", ROOT / "tools", ROOT / "fuzz" / "corpus" / "overlay_fuzzer"]:
        if junk.is_dir():
            shutil.rmtree(junk, ignore_errors=True)
        elif junk.exists():
            junk.unlink()


def transform_contents() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".protocols", ".env", "Makefile"
        } and path.name not in {"Makefile", ".gitignore"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text = xform(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")


def patch_store_h() -> None:
    p = ROOT / "src" / "store.h"
    text = p.read_text(encoding="utf-8")
    if "proto_row_table_t" not in text:
        if '#include "protocolspack/protocol.h"' not in text:
            text = text.replace(
                '#include "protocolspack/proto_types.h"\n',
                '#include "protocolspack/proto_types.h"\n#include "protocolspack/protocol.h"\n',
            )
        text = text.replace(
            "typedef struct proto_doc {\n  proto_entry_t *entries;",
            """typedef struct proto_row_table {
  proto_row_t *items;
  size_t count;
  size_t cap;
  long active;
} proto_row_table_t;

typedef struct proto_doc {
  proto_entry_t *entries;
  proto_row_table_t rows;""",
        )
        p.write_text(text, encoding="utf-8")


def patch_store_destroy() -> None:
    p = ROOT / "src" / "store.c"
    text = p.read_text(encoding="utf-8")
    if "proto_row_init" not in text:
        text = text.replace(
            "#include \"store.h\"\n\n#include <stdlib.h>",
            "#include \"store.h\"\n\n#include \"protocolspack/protocol.h\"\n\n#include <stdlib.h>",
        )
        text = text.replace(
            "  proto_arena_init(&doc->arena, 0);\n  return (proto_doc_t *)doc;",
            "  proto_arena_init(&doc->arena, 0);\n  proto_row_init((proto_doc_t *)doc);\n  return (proto_doc_t *)doc;",
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
    """Truncated \\x OOB: checks i+1 instead of i+2."""
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
    if "proto_row_begin" in text:
        return

    inc = '#include "protocolspack/protocol.h"\n'
    if inc not in text:
        text = text.replace('#include "unescape.h"\n', '#include "unescape.h"\n' + inc)

    helper = '''
static int proto_token_is_number(proto_slice_t s) {
  size_t i;
  if (s.len == 0) {
    return 0;
  }
  for (i = 0; i < s.len; i++) {
    if (s.data[i] < '0' || s.data[i] > '9') {
      return 0;
    }
  }
  return 1;
}

static int proto_parse_row(proto_doc_impl_t *doc, proto_lexer_t *lx,
                           proto_token_t *tok, proto_error_t **out_err) {
  char name[256];
  int number = 0;
  size_t i;
  if (tok->text.len >= sizeof(name)) {
    return -1;
  }
  memcpy(name, tok->text.data, tok->text.len);
  name[tok->text.len] = '\\0';

  if (proto_lexer_next(lx, tok) != 0) {
    return -1;
  }
  if (tok->kind != PROTO_TOK_UNQUOTED && tok->kind != PROTO_TOK_IDENT) {
    if (out_err) {
      *out_err = proto_error_new("expected protocol number", tok->line, tok->column);
    }
    return -1;
  }
  if (!proto_token_is_number(tok->text)) {
    if (out_err) {
      *out_err = proto_error_new("invalid protocol number", tok->line, tok->column);
    }
    return -1;
  }
  for (i = 0; i < tok->text.len; i++) {
    number = number * 10 + (tok->text.data[i] - '0');
  }
  if (proto_row_begin((proto_doc_t *)doc, name) != 0) {
    return -1;
  }
  if (proto_row_set_number((proto_doc_t *)doc, number) != 0) {
    return -1;
  }

  if (proto_lexer_next(lx, tok) != 0) {
    return 0;
  }
  while (tok->kind == PROTO_TOK_IDENT || tok->kind == PROTO_TOK_UNQUOTED ||
         tok->kind == PROTO_TOK_STRING) {
    char alias[512];
    char *val = NULL;
    if (tok->kind == PROTO_TOK_STRING) {
      val = proto_decode_quoted(&doc->arena, tok->text);
    } else {
      if (tok->text.len >= sizeof(alias)) {
        return -1;
      }
      memcpy(alias, tok->text.data, tok->text.len);
      alias[tok->text.len] = '\\0';
      val = proto_arena_strdup(&doc->arena, alias);
    }
    if (!val) {
      return -1;
    }
    if (proto_row_add_alias((proto_doc_t *)doc, val) != 0) {
      return -1;
    }
    if (proto_lexer_next(lx, tok) != 0) {
      return 0;
    }
  }
  return 0;
}
'''
    text = text.replace(
        "static int proto_parse_assignment(proto_doc_impl_t *doc, proto_lexer_t *lx,",
        helper + "\nstatic int proto_parse_assignment(proto_doc_impl_t *doc, proto_lexer_t *lx,",
    )

    loop_patch = '''    if (tok.kind == PROTO_TOK_IDENT) {
      proto_lexer_t peek_lx = lx;
      proto_token_t peek = tok;
      if (proto_lexer_next(&peek_lx, &peek) == 0 &&
          peek.kind != PROTO_TOK_EQUAL &&
          (peek.kind == PROTO_TOK_UNQUOTED || peek.kind == PROTO_TOK_IDENT) &&
          proto_token_is_number(peek.text)) {
        if (proto_parse_row(doc, &lx, &tok, out_err) != 0) {
          return -1;
        }
        if (tok.kind != PROTO_TOK_NEWLINE && tok.kind != PROTO_TOK_EOF) {
          if (proto_lexer_next(&lx, &tok) != 0) {
            return -1;
          }
        }
        continue;
      }
      if (proto_parse_assignment(doc, &lx, &tok, exported, out_err) != 0) {
        return -1;
      }
      continue;
    }'''

    text = text.replace(
        '''    if (tok.kind == PROTO_TOK_IDENT) {
      if (proto_parse_assignment(doc, &lx, &tok, exported, out_err) != 0) {
        return -1;
      }
      continue;
    }''',
        loop_patch,
    )
    p.write_text(text, encoding="utf-8")


def add_domain_modules() -> None:
    write(ROOT / "include" / "protocolspack" / "protocol.h", PROTOCOL_H)
    write(ROOT / "include" / "protocolspack" / "alias.h", ALIAS_H)
    write(ROOT / "src" / "protocol.c", PROTOCOL_C)
    write(ROOT / "src" / "alias.c", ALIAS_C)
    write(ROOT / "fuzz" / "merge_fuzzer.c", MERGE_FUZZER)
    write(ROOT / "fuzz" / "alias_fuzzer.c", ALIAS_FUZZER)
    write(ROOT / "README.md", README)

    write(ROOT / "examples" / "sample.protocols", """# Internet protocol numbers
ip 0 IP
icmp 1 ICMP
tcp 6 TCP
udp 17 UDP
""")

    write(ROOT / "examples" / "imported.protocols", """@import "shared.protocols"
sctp 132 SCTP
""")

    write(ROOT / "tests" / "test_protocol.c", '''#include "protocolspack/protocol.h"
#include "protocolspack/proto.h"
#include "unity/unity.h"

void test_protocol_row(void) {
  proto_doc_t *doc = proto_doc_create();
  TEST_ASSERT_NOT_NULL(doc);
  TEST_ASSERT_EQUAL(0, proto_row_begin(doc, "tcp"));
  TEST_ASSERT_EQUAL(0, proto_row_set_number(doc, 6));
  TEST_ASSERT_EQUAL(1, proto_row_count(doc));
  proto_doc_destroy(doc);
}
''')

    write(ROOT / "tests" / "test_alias.c", '''#include "protocolspack/alias.h"
#include "unity/unity.h"

void test_alias_tokens(void) {
  proto_alias_t *m = proto_alias_create();
  TEST_ASSERT_NOT_NULL(m);
  TEST_ASSERT_EQUAL(0, proto_alias_begin(m, "batch"));
  TEST_ASSERT_EQUAL(0, proto_alias_append_token(m, "TCP", 3));
  proto_alias_destroy(m);
}
''')


def patch_build() -> None:
    build = '''#!/bin/bash -eu

OBJECTS=()
for src in buffer strutil error arena utf8 store unescape lexer parser serialize \\
           validate merge expand coerce walk query diff pretty import_stack \\
           import_ctx path filter protomap profile canonical strict readutil \\
           snapshot protopack protocolspack protocol alias; do
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
build_fuzzer alias_fuzzer.c alias_fuzzer
'''
    write(ROOT / ".clusterfuzzlite" / "build.sh", build)

    wsl = '''#!/bin/bash
set -eu
cd "$(dirname "$0")/.."
export SRC="$PWD"
export OUT=/tmp/protocolspack_out
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
  - alias_fuzzer
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

    write(ROOT / "fuzz" / "corpus" / "alias_fuzzer" / "seed.bin", bytes(range(48, 112)))

    mk = ROOT / "Makefile"
    if mk.exists():
        t = mk.read_text(encoding="utf-8")
        t = t.replace("libenvfile", "libprotocolspack").replace("envfile", "protocolspack")
        t = t.replace("generate-tests:\n\tpython3 tools/gen_envfile_tests.py\n\n", "")
        t = t.replace("$(TEST_BIN): generate-tests ", "$(TEST_BIN): ")
        t = t.replace("all: generate-tests ", "all: ")
        t = t.replace("test_machine.c", "test_protocol.c")
        t = t.replace("test_macdef.c", "test_alias.c")
        mk.write_text(t, encoding="utf-8")


def patch_test_runner() -> None:
    tr = ROOT / "tests" / "test_runner.c"
    if not tr.exists():
        return
    text = tr.read_text(encoding="utf-8")
    text = text.replace("test_machine", "test_protocol").replace("test_macdef", "test_alias")
    tr.write_text(text, encoding="utf-8")


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
        diff = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=ROOT,
        )
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
    print("OK", ROOT)


if __name__ == "__main__":
    main()
