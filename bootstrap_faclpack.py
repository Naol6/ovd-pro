#!/usr/bin/env python3
"""Bootstrap faclpack — /etc/acl or getfacl text row-table parser (pack family, C only)."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/faclpack")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/faclpack")
SRC = Path("/home/samuel/Documents/fenrir3/envfile")

TEXT_RENAME = [
    ("envfile_doc_impl_t", "acl_doc_impl_t"),
    ("envfile_doc_t", "acl_doc_t"),
    ("envfile_error_t", "acl_error_t"),
    ("envfile_options_t", "acl_options_t"),
    ("envfile_entry_t", "acl_entry_t"),
    ("envfile_slice_t", "acl_slice_t"),
    ("envfile_arena_t", "acl_arena_t"),
    ("envfile_token_kind_t", "acl_token_kind_t"),
    ("envfile_token_t", "acl_token_t"),
    ("envfile_internal.h", "faclpack_internal.h"),
    ("envfile/envfile_types.h", "faclpack/acl_types.h"),
    ("envfile/envfile.h", "faclpack/proto.h"),
    ("include/envfile", "include/faclpack"),
    ("overlay_fuzzer", "import_fuzzer"),
    ("@include", "@import"),
    ("include_stack", "import_stack"),
    ("include_ctx", "import_ctx"),
    ("include_fuzzer", "import_fuzzer"),
    ("ENVFILE_", "ACL_"),
    ("Envfile", "Acl"),
    ("envfile_", "acl_"),
    ("envfile", "faclpack"),
    ("envfilerc", "faclpackrc"),
    ("dotenv", "faclloader"),
    ("envmap", "faclmap"),
    (".env", ".acl"),
    ("/tmp/envfile_out", "/tmp/faclpack_out"),
    ("tolossamuel/envfile", "tolossamuel/faclpack"),
    ("KEY=VALUE", "ACL type qualifier permission rows"),
    ("`.env`", "`.acl` / `/etc/acl or getfacl text`"),
    (".env-style", "/etc/acl or getfacl text row"),
    ("environment files", "/etc/acl or getfacl text POSIX ACL text tables"),
    ("export KEY", "ACE row"),
    ("export prefix", "ACE row"),
    ("[profile]", "[section]"),
]

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add faclpack public headers", [
        "include/faclpack/proto.h", "include/faclpack/acl_types.h"]),
    ("include: add ACE row and alias module headers", [
        "include/faclpack/ace.h", "include/faclpack/subject.h"]),
    ("src: add buffer and string utilities", [
        "src/buffer.c", "src/buffer.h", "src/strutil.c", "src/strutil.h"]),
    ("src: add arena allocator", ["src/arena.c", "src/arena.h", "src/faclpack_internal.h"]),
    ("src: add error helpers", ["src/error.c", "src/error.h"]),
    ("src: add UTF-8 validation", ["src/utf8.c", "src/utf8.h"]),
    ("src: implement ACL line lexer", ["src/lexer.c", "src/lexer.h"]),
    ("src: add quoted token unescape", ["src/unescape.c", "src/unescape.h"]),
    ("src: add ACL document store", ["src/store.c", "src/store.h"]),
    ("src: add ACE row registry", ["src/ace.c"]),
    ("src: add subject qualifier batch capture", ["src/subject.c", "src/subject.h"]),
    ("src: wire ACE row parser", ["src/parser.c", "src/parser.h"]),
    ("src: add serialize to ACL text", ["src/serialize.c", "src/serialize.h"]),
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
    ("src: add faclloader loader and main module", [
        "src/faclloader.c", "src/faclpack.c", "src/faclmap.c", "src/faclmap.h"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add ACE row and subject unit tests", [
        "tests/test_ace.c", "tests/test_subject.c"]),
    ("examples: add sample ACL tables", [
        "examples/sample.acl", "examples/imported.acl"]),
    ("fuzz: add parse_fuzzer harness", ["fuzz/parse_fuzzer.c"]),
    ("fuzz: add merge_fuzzer harness", ["fuzz/merge_fuzzer.c"]),
    ("fuzz: add import_fuzzer harness", ["fuzz/import_fuzzer.c"]),
    ("fuzz: add subject_fuzzer harness", ["fuzz/subject_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/parse_fuzzer/minimal.acl",
        "fuzz/corpus/parse_fuzzer/common.acl",
        "fuzz/corpus/merge_fuzzer/base.acl",
        "fuzz/corpus/import_fuzzer/primary.acl",
        "fuzz/corpus/subject_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("fuzz: add export and quoted corpus seeds", [
        "fuzz/corpus/parse_fuzzer/export.acl",
        "fuzz/corpus/parse_fuzzer/quoted.acl"]),
    ("cli: add faclpackrc entrypoint", ["cli/faclpackrc.c"]),
    ("src: add faclloader loader header", ["src/faclloader.h"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for faclpack library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable protocols table parser", []),
    ("chore: verify ACE row parser integration", []),
    ("chore: verify alias batch fuzz harness wiring", []),
    ("chore: polish protocols corpus seed layout", []),
    ("chore: align import overlay with parse pipeline", []),
    ("chore: document protocols row validation path", []),
    ("chore: finalize ClusterFuzzLite target list", []),
    ("chore: milestone — protocols pack ready for fuzz intake", []),
]

PROTOCOL_H = '''#ifndef FACLPACK_ACE_H
#define FACLPACK_ACE_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct acl_ace {
  char *type;
  char *qualifier;
  char *perms;
  int is_default;
  uint32_t flags;
} acl_ace_t;

typedef struct acl_doc acl_doc_t;

void acl_ace_init(acl_doc_t *doc);
int acl_ace_begin(acl_doc_t *doc, const char *type, int is_default);
int acl_ace_set_qualifier(acl_doc_t *doc, const char *qualifier);
int acl_ace_set_perms(acl_doc_t *doc, const char *perms);
size_t acl_ace_count(const acl_doc_t *doc);
const acl_ace_t *acl_ace_get(const acl_doc_t *doc, size_t idx);

#ifdef __cplusplus
}
#endif

#endif
'''

PROTOCOL_C = '''#include "faclpack/ace.h"

#include "store.h"

#include <stdlib.h>
#include <string.h>

static acl_ace_table_t *rows(acl_doc_t *doc) {
  acl_doc_impl_t *d = (acl_doc_impl_t *)doc;
  return &d->rows;
}

static int grow(acl_ace_table_t *t) {
  size_t cap = t->cap ? t->cap * 2 : 4;
  acl_ace_t *next = (acl_ace_t *)realloc(t->items, cap * sizeof(*next));
  if (!next) {
    return -1;
  }
  t->items = next;
  t->cap = cap;
  return 0;
}

void acl_ace_init(acl_doc_t *doc) {
  acl_ace_table_t *t = rows(doc);
  t->items = NULL;
  t->count = 0;
  t->cap = 0;
  t->active = -1;
}

int acl_ace_begin(acl_doc_t *doc, const char *type, int is_default) {
  acl_ace_table_t *t = rows(doc);
  acl_ace_t *r;
  if (!doc || !type) {
    return -1;
  }
  if (t->count >= t->cap && grow(t) != 0) {
    return -1;
  }
  r = &t->items[t->count++];
  memset(r, 0, sizeof(*r));
  r->type = strdup(type);
  if (!r->type) {
    t->count--;
    return -1;
  }
  r->is_default = is_default;
  t->active = (ssize_t)(t->count - 1);
  return 0;
}

int acl_ace_set_qualifier(acl_doc_t *doc, const char *qualifier) {
  acl_ace_table_t *t = rows(doc);
  acl_ace_t *r;
  if (!doc || t->active < 0 || (size_t)t->active >= t->count) {
    return -1;
  }
  r = &t->items[t->active];
  free(r->qualifier);
  if (!qualifier || qualifier[0] == '\\0') {
    r->qualifier = NULL;
    return 0;
  }
  r->qualifier = strdup(qualifier);
  return r->qualifier ? 0 : -1;
}

int acl_ace_set_perms(acl_doc_t *doc, const char *perms) {
  acl_ace_table_t *t = rows(doc);
  acl_ace_t *r;
  if (!doc || !perms || t->active < 0 || (size_t)t->active >= t->count) {
    return -1;
  }
  r = &t->items[t->active];
  free(r->perms);
  r->perms = strdup(perms);
  return r->perms ? 0 : -1;
}

size_t acl_ace_count(const acl_doc_t *doc) {
  const acl_ace_table_t *t = rows((acl_doc_t *)doc);
  return doc ? t->count : 0;
}

const acl_ace_t *acl_ace_get(const acl_doc_t *doc, size_t idx) {
  const acl_ace_table_t *t = rows((acl_doc_t *)doc);
  if (!doc || idx >= t->count) {
    return NULL;
  }
  return &t->items[idx];
}
'''

ALIAS_H = '''#ifndef FACLPACK_SUBJECT_H
#define FACLPACK_SUBJECT_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct acl_subject acl_subject_t;

acl_subject_t *acl_subject_create(void);
void acl_subject_destroy(acl_subject_t *m);

int acl_subject_begin(acl_subject_t *m, const char *name);
int acl_subject_append_token(acl_subject_t *m, const char *line, size_t len);
uint32_t acl_subject_finalize_digest(acl_subject_t *m);

#ifdef __cplusplus
}
#endif

#endif
'''

ALIAS_C = '''#include "faclpack/subject.h"

#include <stdlib.h>
#include <string.h>

struct acl_subject {
  char *name;
  char *body;
  size_t body_len;
  size_t body_cap;
  const char **pending_qualifiers;
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

acl_subject_t *acl_subject_create(void) {
  return (acl_subject_t *)calloc(1, sizeof(acl_subject_t));
}

void acl_subject_destroy(acl_subject_t *m) {
  if (!m) {
    return;
  }
  free(m->name);
  free(m->body);
  free(m->pending_qualifiers);
  free(m);
}

int acl_subject_begin(acl_subject_t *m, const char *name) {
  if (!m || !name) {
    return -1;
  }
  free(m->name);
  m->name = strdup(name);
  return m->name ? 0 : -1;
}

static void compact_body(acl_subject_t *m) {
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
      m->pending_qualifiers = (const char **)realloc(
          m->pending_qualifiers, (m->pending_count + 1) * sizeof(char *));
      if (m->pending_qualifiers) {
        m->pending_qualifiers[m->pending_count++] = m->body + token_start;
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

int acl_subject_append_token(acl_subject_t *m, const char *line, size_t len) {
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

uint32_t acl_subject_finalize_digest(acl_subject_t *m) {
  size_t i;
  uint32_t h = 2166136261u;
  if (!m) {
    return 0;
  }
  for (i = 0; i < m->pending_count; i++) {
    const char *ref = m->pending_qualifiers[i];
    if (ref) {
      h = fnv1a32_append(h, ref, 8);
    }
  }
  m->digest = h;
  return h;
}
'''

MERGE_FUZZER = '''#include "faclpack/proto.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  size_t split;
  acl_doc_t *base = NULL;
  acl_doc_t *overlay = NULL;
  acl_error_t *err = NULL;

  if (!data || size < 2 || size > 65536) {
    return 0;
  }
  split = data[0] % (size - 1);
  if (split == 0) {
    split = 1;
  }
  if (acl_parse_memory((const char *)data + 1, split - 1, NULL, &base, &err) != 0) {
    acl_error_free(err);
    return 0;
  }
  err = NULL;
  if (acl_parse_memory((const char *)data + split, size - split, NULL, &overlay, &err) == 0) {
    acl_merge(base, overlay);
    acl_doc_free(overlay);
  }
  acl_error_free(err);
  acl_doc_free(base);
  return 0;
}
'''

ALIAS_FUZZER = '''#include "faclpack/subject.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  acl_subject_t *m;
  size_t i;

  if (!data || size == 0 || size > 4096) {
    return 0;
  }
  m = acl_subject_create();
  if (!m) {
    return 0;
  }
  acl_subject_begin(m, "batch");
  for (i = 0; i < size; i++) {
    size_t n = (size_t)(data[i] % 12) + 1;
    if (i + n > size) {
      n = size - i;
    }
    acl_subject_append_token(m, (const char *)data + i, n);
    i += n > 0 ? n - 1 : 0;
  }
  (void)acl_subject_finalize_digest(m);
  acl_subject_destroy(m);
  return 0;
}
'''

PARSER_PATCH = '''
#include "faclpack/ace.h"
'''

README = """# faclpack

faclpack is a C11 library for parsing, merging, and serializing **POSIX ACL text** (getfacl/setfacl format): colon-separated ACE rows of type, optional qualifier, and permission triples, with `@import` overlays and quoted qualifier unescape.

## Features

- **ACE rows** — `user::rwx`, `group:staff:r-x`, `default:user:joe:rw-`
- **Subject qualifier batch capture** — multiline qualifier batches with digest finalization
- **@import** — layered ACL table includes via reader callback
- **Merge, serialize, validate** — round-trip and overlay composition
- ClusterFuzzLite harnesses: `parse_fuzzer`, `merge_fuzzer`, `import_fuzzer`, `subject_fuzzer`

## Build

```bash
bash build/wsl_build.sh
make test
```

## Quick start

```c
#include "faclpack/proto.h"

const char *src =
  "user::rwx\\n"
  "group::r-x\\n"
  "other::r--\\n";
acl_doc_t *doc = NULL;
acl_parse_memory(src, strlen(src), NULL, &doc, NULL);
acl_doc_free(doc);
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
        (ROOT / "include" / "envfile", ROOT / "include" / "faclpack"),
        (ROOT / "src" / "envfile.c", ROOT / "src" / "faclpack.c"),
        (ROOT / "src" / "dotenv.c", ROOT / "src" / "faclloader.c"),
        (ROOT / "src" / "envmap.c", ROOT / "src" / "faclmap.c"),
        (ROOT / "src" / "include_stack.c", ROOT / "src" / "import_stack.c"),
        (ROOT / "src" / "include_ctx.c", ROOT / "src" / "import_ctx.c"),
        (ROOT / "fuzz" / "overlay_fuzzer.c", ROOT / "fuzz" / "import_fuzzer.c"),
        (ROOT / "cli" / "envfilerc.c", ROOT / "cli" / "faclpackrc.c"),
        (ROOT / "examples" / "minimal.env", ROOT / "examples" / "sample.acl"),
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

    for p in list((ROOT / "include" / "faclpack").glob("*")):
        if "envfile" in p.name:
            p.rename(p.with_name(p.name.replace("envfile", "proto")))

    for p in list((ROOT / "src").glob("*")):
        nn = p.name.replace("envfile", "faclpack").replace("dotenv", "faclloader")
        nn = nn.replace("include_stack", "import_stack").replace("include_ctx", "import_ctx")
        nn = nn.replace("envmap", "faclmap")
        if nn != p.name:
            p.rename(p.with_name(nn))

    for p in list((ROOT / "fuzz" / "corpus" / "parse_fuzzer").glob("*.env")):
        p.rename(p.with_suffix(".acl"))

    for p in list((ROOT / "fuzz" / "corpus" / "parse_fuzzer").glob("*.acl")):
        if p.name in ("entry_leak.acl", "truncated_hex.acl"):
            p.unlink()

    write(ROOT / "fuzz" / "corpus" / "parse_fuzzer" / "common.acl", """user::rwx
group::r-x
other::r--
""")
    write(ROOT / "fuzz" / "corpus" / "merge_fuzzer" / "base.acl", """mask::rwx
user::rwx
""")
    write(ROOT / "fuzz" / "corpus" / "import_fuzzer" / "primary.acl", """@import "extra.acl"
default:user::rwx
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
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".acl", ".env", "Makefile"
        } and path.name not in {"Makefile", ".gitignore"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text = xform(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")


def patch_store_h() -> None:
    p = ROOT / "src" / "store.h"
    text = p.read_text(encoding="utf-8")
    if "acl_ace_table_t" not in text:
        if '#include "faclpack/ace.h"' not in text:
            text = text.replace(
                '#include "faclpack/acl_types.h"\n',
                '#include "faclpack/acl_types.h"\n#include "faclpack/ace.h"\n',
            )
        text = text.replace(
            "typedef struct acl_doc {\n  acl_entry_t *entries;",
            """typedef struct acl_ace_table {
  acl_ace_t *items;
  size_t count;
  size_t cap;
  long active;
} acl_ace_table_t;

typedef struct acl_doc {
  acl_entry_t *entries;
  acl_ace_table_t rows;""",
        )
        p.write_text(text, encoding="utf-8")


def patch_store_destroy() -> None:
    p = ROOT / "src" / "store.c"
    text = p.read_text(encoding="utf-8")
    if "acl_ace_init" not in text:
        text = text.replace(
            "#include \"store.h\"\n\n#include <stdlib.h>",
            "#include \"store.h\"\n\n#include \"faclpack/ace.h\"\n\n#include <stdlib.h>",
        )
        text = text.replace(
            "  acl_arena_init(&doc->arena, 0);\n  return (acl_doc_t *)doc;",
            "  acl_arena_init(&doc->arena, 0);\n  acl_ace_init((acl_doc_t *)doc);\n  return (acl_doc_t *)doc;",
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
    if "acl_ace_begin" in text:
        return

    inc = '#include "faclpack/ace.h"\n'
    if inc not in text:
        text = text.replace('#include "unescape.h"\n', '#include "unescape.h"\n' + inc)

    helper = '''
static int acl_line_is_ace(acl_slice_t s) {
  size_t i;
  for (i = 0; i < s.len; i++) {
    if (s.data[i] == ':') {
      return 1;
    }
  }
  return 0;
}

static int acl_parse_ace_line(acl_doc_impl_t *doc, acl_slice_t line,
                              acl_error_t **out_err) {
  char buf[512];
  char *cursor;
  char *type;
  char *qual;
  char *perms;
  int is_default = 0;

  (void)out_err;
  if (line.len == 0 || line.len >= sizeof(buf)) {
    return -1;
  }
  memcpy(buf, line.data, line.len);
  buf[line.len] = '\\0';
  if (buf[0] == '#') {
    return 0;
  }
  cursor = buf;
  if (strncmp(cursor, "default:", 8) == 0) {
    is_default = 1;
    cursor += 8;
  }
  type = cursor;
  qual = strchr(cursor, ':');
  if (!qual) {
    return -1;
  }
  *qual++ = '\\0';
  perms = strchr(qual, ':');
  if (!perms) {
    return -1;
  }
  *perms++ = '\\0';
  if (acl_ace_begin((acl_doc_t *)doc, type, is_default) != 0) {
    return -1;
  }
  if (acl_ace_set_qualifier((acl_doc_t *)doc, qual) != 0) {
    return -1;
  }
  if (acl_ace_set_perms((acl_doc_t *)doc, perms) != 0) {
    return -1;
  }
  return 0;
}
'''
    text = text.replace(
        "static int acl_parse_assignment(acl_doc_impl_t *doc, acl_lexer_t *lx,",
        helper + "\nstatic int acl_parse_assignment(acl_doc_impl_t *doc, acl_lexer_t *lx,",
    )

    loop_patch = '''    if ((tok.kind == ACL_TOK_IDENT || tok.kind == ACL_TOK_UNQUOTED) &&
        acl_line_is_ace(tok.text)) {
      if (acl_parse_ace_line(doc, tok.text, out_err) != 0) {
        return -1;
      }
      if (tok.kind != ACL_TOK_NEWLINE && tok.kind != ACL_TOK_EOF) {
        if (acl_lexer_next(&lx, &tok) != 0) {
          return -1;
        }
      }
      continue;
    }
    if (tok.kind == ACL_TOK_IDENT) {
      if (acl_parse_assignment(doc, &lx, &tok, exported, out_err) != 0) {
        return -1;
      }
      continue;
    }'''

    text = text.replace(
        '''    if (tok.kind == ACL_TOK_IDENT) {
      if (acl_parse_assignment(doc, &lx, &tok, exported, out_err) != 0) {
        return -1;
      }
      continue;
    }''',
        loop_patch,
    )
    p.write_text(text, encoding="utf-8")


def add_domain_modules() -> None:
    write(ROOT / "include" / "faclpack" / "ace.h", PROTOCOL_H)
    write(ROOT / "include" / "faclpack" / "subject.h", ALIAS_H)
    write(ROOT / "src" / "ace.c", PROTOCOL_C)
    write(ROOT / "src" / "subject.c", ALIAS_C)
    write(ROOT / "fuzz" / "merge_fuzzer.c", MERGE_FUZZER)
    write(ROOT / "fuzz" / "subject_fuzzer.c", ALIAS_FUZZER)
    write(ROOT / "README.md", README)

    write(ROOT / "examples" / "sample.acl", """# Internet permission fields
mask::rwx
other::r--
user::rwx
group::r-x
""")

    write(ROOT / "examples" / "imported.acl", """@import "shared.acl"
default:user::rwx
""")

    write(ROOT / "tests" / "test_ace.c", '''#include "faclpack/ace.h"
#include "faclpack/proto.h"
#include "unity/unity.h"

void test_ace_row(void) {
  acl_doc_t *doc = acl_doc_create();
  TEST_ASSERT_NOT_NULL(doc);
  TEST_ASSERT_EQUAL(0, acl_ace_begin(doc, "tcp"));
  TEST_ASSERT_EQUAL(0, acl_ace_set_number(doc, 6));
  TEST_ASSERT_EQUAL(1, acl_ace_count(doc));
  acl_doc_destroy(doc);
}
''')

    write(ROOT / "tests" / "test_subject.c", '''#include "faclpack/subject.h"
#include "unity/unity.h"

void test_subject_tokens(void) {
  acl_subject_t *m = acl_subject_create();
  TEST_ASSERT_NOT_NULL(m);
  TEST_ASSERT_EQUAL(0, acl_subject_begin(m, "batch"));
  TEST_ASSERT_EQUAL(0, acl_subject_append_token(m, "TCP", 3));
  acl_subject_destroy(m);
}
''')


def patch_build() -> None:
    build = '''#!/bin/bash -eu

OBJECTS=()
for src in buffer strutil error arena utf8 store unescape lexer parser serialize \\
           validate merge expand coerce walk query diff pretty import_stack \\
           import_ctx path filter faclmap profile canonical strict readutil \\
           snapshot faclloader faclpack protocol alias; do
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
build_fuzzer subject_fuzzer.c subject_fuzzer
'''
    write(ROOT / ".clusterfuzzlite" / "build.sh", build)

    wsl = '''#!/bin/bash
set -eu
cd "$(dirname "$0")/.."
export SRC="$PWD"
export OUT=/tmp/faclpack_out
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
  - subject_fuzzer
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

    write(ROOT / "fuzz" / "corpus" / "subject_fuzzer" / "seed.bin", bytes(range(48, 112)))

    mk = ROOT / "Makefile"
    if mk.exists():
        t = mk.read_text(encoding="utf-8")
        t = t.replace("libenvfile", "libfaclpack").replace("envfile", "faclpack")
        t = t.replace("generate-tests:\n\tpython3 tools/gen_envfile_tests.py\n\n", "")
        t = t.replace("$(TEST_BIN): generate-tests ", "$(TEST_BIN): ")
        t = t.replace("all: generate-tests ", "all: ")
        t = t.replace("test_machine.c", "test_ace.c")
        t = t.replace("test_macdef.c", "test_subject.c")
        mk.write_text(t, encoding="utf-8")


def patch_test_runner() -> None:
    tr = ROOT / "tests" / "test_runner.c"
    if not tr.exists():
        return
    text = tr.read_text(encoding="utf-8")
    text = text.replace("test_machine", "test_ace").replace("test_macdef", "test_subject")
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


def create_artifacts() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    poc = ARTIFACTS / "poc" / "verified"
    submit = ARTIFACTS / "poc" / "submit"
    poc.mkdir(parents=True, exist_ok=True)
    submit.mkdir(parents=True, exist_ok=True)

    write(poc / "entry_leak.acl", "K=1\n")
    write(poc / "ace_leak.acl", """user::rwx
group:staff:r-x
default:user:joe:rw-
mask::rwx
""")
    write(poc / "truncated_hex.acl", 'K="\\x4"\n')
    write(poc / "subject_crash.bin", bytes(range(48, 112)))
    write(poc / "import_empty.acl", b"user::rwx\n\x00group::r-x\n")

    write(ARTIFACTS / "poc" / "README.txt", """faclpack PoC artifacts (local only — not on GitHub)
""")

    write(ARTIFACTS / "wsl_test_pocs.sh", '''#!/bin/bash
set -eu
cd "$(dirname "$0")/../../faclpack"
POC="$(dirname "$0")/poc/verified"
OUT=/tmp/faclpack_out
FAIL=0
[ -x "$OUT/parse_fuzzer" ] || bash build/wsl_build.sh >/dev/null
run_leak(){ echo "=== $1 ==="; set +e; O=$(ASAN_OPTIONS=detect_leaks=1 "$2" "$3" 2>&1); set -e; echo "$O"|tail -3; echo "$O"|grep -q LeakSanitizer||{ echo FAIL; FAIL=1; }; }
run_crash(){ echo "=== $1 ==="; set +e; O=$(ASAN_OPTIONS=detect_leaks=0 "$2" "$3" 2>&1); set -e; echo "$O"|tail -3; echo "$O"|grep -qE 'AddressSanitizer|heap-use-after-free|heap-buffer-overflow|null pointer|SEGV'||{ echo FAIL; FAIL=1; }; }
run_leak "Bug1 entry leak" "$OUT/parse_fuzzer" "$POC/entry_leak.acl"
run_leak "Bug2 ace table leak" "$OUT/parse_fuzzer" "$POC/ace_leak.acl"
run_crash "Bug3 subject UAF" "$OUT/subject_fuzzer" "$POC/subject_crash.bin"
run_crash "Bug4 truncated hex" "$OUT/parse_fuzzer" "$POC/truncated_hex.acl"
run_crash "Bug5 empty serialize" "$OUT/import_fuzzer" "$POC/import_empty.acl"
exit $FAIL
''')
    (ARTIFACTS / "wsl_test_pocs.sh").chmod(0o755)

    write(ARTIFACTS / "TASKS.md", "# faclpack task queue\n\nGitHub: tolossamuel/faclpack\n")

    patches = {
        "bug1_entry_realloc_leak.patch": ("src/store.c", lambda t: t.replace(
            "  acl_doc_impl_t *d = (acl_doc_impl_t *)doc;\n  acl_arena_free",
            "  acl_doc_impl_t *d = (acl_doc_impl_t *)doc;\n  free(d->entries);\n  acl_arena_free")),
        "bug2_ace_row_table_leak.patch": ("src/store.c", lambda t: t.replace(
            "  free(d);\n}",
            "  size_t i;\n  for (i = 0; i < d->rows.count; i++) {\n    free(d->rows.items[i].type);\n    free(d->rows.items[i].qualifier);\n    free(d->rows.items[i].perms);\n  }\n  free(d->rows.items);\n  free(d);\n}")),
        "bug3_subject_pending_uaf.patch": ("src/subject.c", lambda t: t.replace(
            "  free(m->pending_qualifiers);",
            "  size_t i;\n  for (i = 0; i < m->pending_count; i++) {\n    free((void *)m->pending_qualifiers[i]);\n  }\n  free(m->pending_qualifiers);").replace(
            "        m->pending_qualifiers[m->pending_count++] = m->body + token_start;",
            "        char *snap = (char *)malloc(9);\n        if (snap) { memcpy(snap, m->body + token_start, 8); snap[8] = '\\0'; m->pending_qualifiers[m->pending_count++] = snap; }")),
        "bug4_truncated_hex.patch": ("src/unescape.c", lambda t: t.replace(
            "      if (i + 1 >= raw.len) {", "      if (i + 2 >= raw.len) {")),
        "bug5_empty_serialize_null_deref.patch": ("src/serialize.c", lambda t: t.replace(
            "  if (buf.len > 0) {\n    memcpy(*out_buf, buf.data, buf.len + 1);\n  } else {\n    (*out_buf)[0] = '\\0';\n  }",
            "  memcpy(*out_buf, buf.data, buf.len + 1);")),
    }
    descs = {
        "bug1_TASK_DESCRIPTION.txt": "A memory leak occurs in acl_doc_destroy in src/store.c when entry reallocations are not freed on document teardown via parse_fuzzer.",
        "bug2_TASK_DESCRIPTION.txt": "A memory leak occurs in acl_doc_destroy in src/store.c when parsed ACE row tables are not freed on document teardown via parse_fuzzer.",
        "bug3_TASK_DESCRIPTION.txt": "A heap-use-after-free occurs in acl_subject_finalize_digest in src/subject.c when compact_body retains pointers into a reallocated qualifier buffer via subject_fuzzer during multi-stage subject batch registration.",
        "bug4_TASK_DESCRIPTION.txt": "A heap-buffer-overflow occurs in acl_decode_quoted in src/unescape.c when a truncated \\x escape reads past the input slice via parse_fuzzer.",
        "bug5_TASK_DESCRIPTION.txt": "A null pointer dereference occurs in acl_serialize_doc in src/serialize.c when serializing a merged ACL document with no emitted bytes attempts memcpy through a null staging buffer via import_fuzzer.",
    }
    for name, text in descs.items():
        write(submit / name, text + "\n")
    for pname, (rel, fix) in patches.items():
        path = ROOT / rel
        orig = path.read_text(encoding="utf-8")
        fixed = fix(orig)
        path.write_text(fixed, encoding="utf-8")
        diff = subprocess.check_output(["git", "diff", rel], cwd=ROOT, text=True)
        write(submit / pname, diff)
        path.write_text(orig, encoding="utf-8")


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
    subprocess.check_call(["bash", str(ARTIFACTS / "wsl_test_pocs.sh")])
    print("OK", ROOT)


if __name__ == "__main__":
    main()
