#!/usr/bin/env python3
"""Bootstrap windowcfg — TOML sliding-window rate-limit manifests + winenv runtime overlays."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/windowcfg")
SRC = Path("/home/samuel/Documents/fenrir3/launchcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/windowcfg")

TEXT_RENAME = [
    ("runenv_doc_impl_t", "winenv_doc_impl_t"),
    ("runenv_doc_t", "winenv_doc_t"),
    ("runenv_error_t", "winenv_error_t"),
    ("runenv_options_t", "winenv_options_t"),
    ("runenv_entry_t", "winenv_entry_t"),
    ("runenv_slice_t", "winenv_slice_t"),
    ("runenv_arena_t", "winenv_arena_t"),
    ("runenv_token_kind_t", "winenv_token_kind_t"),
    ("runenv_token_t", "winenv_token_t"),
    ("runenv_internal.h", "winenv_internal.h"),
    ("runenv/runenv_types.h", "winenv/winenv_types.h"),
    ("include/runenv", "include/winenv"),
    ("src/runenv/", "src/winenv/"),
    ("src/runenv", "src/winenv"),
    ("runenv_", "winenv_"),
    ("RUNENV_", "WINENV_"),
    ("Runenv", "Winenv"),
    ("runenv", "winenv"),
    ("launch_merge", "window_merge"),
    ("launch_fuzzer", "window_fuzzer"),
    ("launch_service", "window_policy"),
    ("launchcfg", "windowcfg"),
    ("LaunchCfg", "WindowCfg"),
    ("LAUNCHCFG", "WINDOWCFG"),
    ("require_stack", "include_stack"),
    ("require_ctx", "include_ctx"),
    ("@require", "@window"),
    ("runmap", "winmap"),
    ("runloader", "winloader"),
    ("apply_runenv_overlay", "apply_winenv_overlay"),
    ("apply_runenv_to_toml", "apply_winenv_to_toml"),
    ("load_runenv_memory", "load_winenv_memory"),
    ("windowcfg_runenv_free", "windowcfg_winenv_free"),
    ("/tmp/launchcfg_out", "/tmp/windowcfg_out"),
    ("tolossamuel/launchcfg", "tolossamuel/windowcfg"),
    ("compile_runenv", "compile_winenv"),
    ("runtime.env", "window.wenv"),
    ("service.toml", "window.toml"),
    ("Container service launch", "Sliding-window rate limit"),
    ("container service launch", "sliding-window rate limit"),
    ("runtime `.env` secret overlays", "winenv runtime rate-limit parameter overlays"),
    ("Runtime env layer", "Winenv layer"),
    ("Service validation", "Window policy validation"),
    ("[service]", "[window]"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add windowcfg public headers", [
        "include/windowcfg/windowcfg.h", "include/windowcfg/window_merge.h"]),
    ("include: add winenv public API", [
        "include/winenv/winenv.h", "include/winenv/winenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add window policy bucket tracker headers", [
        "include/windowcfg/window_policy.h", "include/windowcfg/window_bucket.h",
        "include/windowcfg/window_tracker.h"]),
    ("src/winenv: add buffer and string utilities", [
        "src/winenv/buffer.c", "src/winenv/buffer.h", "src/winenv/strutil.c",
        "src/winenv/strutil.h"]),
    ("src/winenv: add arena allocator", [
        "src/winenv/arena.c", "src/winenv/arena.h", "src/winenv/winenv_internal.h"]),
    ("src/winenv: add error helpers", ["src/winenv/error.c", "src/winenv/error.h"]),
    ("src/winenv: add UTF-8 validation", ["src/winenv/utf8.c", "src/winenv/utf8.h"]),
    ("src/winenv: implement winenv line lexer", ["src/winenv/lexer.c", "src/winenv/lexer.h"]),
    ("src/winenv: add quoted value unescape", ["src/winenv/unescape.c", "src/winenv/unescape.h"]),
    ("src/winenv: add document store", ["src/winenv/store.c", "src/winenv/store.h"]),
    ("src/winenv: wire assignment parser", ["src/winenv/parser.c", "src/winenv/parser.h"]),
    ("src/winenv: add serialize to winenv text", ["src/winenv/serialize.c", "src/winenv/serialize.h"]),
    ("src/winenv: add validation pass", ["src/winenv/validate.c", "src/winenv/validate.h"]),
    ("src/winenv: add merge overlay", ["src/winenv/merge.c", "src/winenv/merge.h"]),
    ("src/winenv: add expand and coerce", [
        "src/winenv/expand.c", "src/winenv/expand.h", "src/winenv/coerce.c",
        "src/winenv/coerce.h"]),
    ("src/winenv: add walk query diff", [
        "src/winenv/walk.c", "src/winenv/walk.h", "src/winenv/query.c",
        "src/winenv/query.h", "src/winenv/diff.c", "src/winenv/diff.h"]),
    ("src/winenv: add pretty printer", ["src/winenv/pretty.c", "src/winenv/pretty.h"]),
    ("src/winenv: add include stack and ctx", [
        "src/winenv/include_stack.c", "src/winenv/include_stack.h",
        "src/winenv/include_ctx.c", "src/winenv/include_ctx.h"]),
    ("src/winenv: add path filter profile", [
        "src/winenv/path.c", "src/winenv/path.h", "src/winenv/filter.c",
        "src/winenv/filter.h", "src/winenv/profile.c", "src/winenv/profile.h"]),
    ("src/winenv: add snapshot readutil strict canonical", [
        "src/winenv/snapshot.c", "src/winenv/snapshot.h", "src/winenv/readutil.c",
        "src/winenv/readutil.h", "src/winenv/strict.c", "src/winenv/strict.h",
        "src/winenv/canonical.c", "src/winenv/canonical.h"]),
    ("src/winenv: add winloader and main winenv module", [
        "src/winenv/winloader.c", "src/winenv/winenv.c", "src/winenv/winmap.c",
        "src/winenv/winmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.c", "src/toml/buffer.c"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.c", "src/toml/datetime.c", "src/toml/lexer.c"]),
    ("src/toml: add value and parser core", ["src/toml/value.c", "src/toml/parser.c"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.c", "src/toml/merge.c", "src/toml/serialize.c"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.c", "src/toml/format.c", "src/toml/validator.c", "src/toml/document.c"]),
    ("src: add windowcfg bridge and winenv-to-toml merge", ["src/windowcfg.c", "src/window_merge.c"]),
    ("src: add window policy validator", ["src/window_policy.c"]),
    ("src: add token bucket refill evaluator", ["src/window_bucket.c"]),
    ("src: add sliding window slot tracker", ["src/window_tracker.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add window policy and tracker unit tests", [
        "tests/test_window_policy.c", "tests/test_window_tracker.c"]),
    ("examples: add TOML window manifest and runtime overlay", [
        "examples/window.toml", "examples/window.wenv"]),
    ("fuzz: add winenv_fuzzer harness", ["fuzz/winenv_fuzzer.c"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.c"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.c"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.c"]),
    ("fuzz: add window_fuzzer for cross-format overlay", ["fuzz/window_fuzzer.c"]),
    ("fuzz: add window_tracker_fuzzer for slot compaction path", ["fuzz/window_tracker_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/winenv_fuzzer/minimal.wenv",
        "fuzz/corpus/winenv_fuzzer/quoted.wenv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/window_fuzzer/sample.bin",
        "fuzz/corpus/window_tracker_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for windowcfg library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable window rate-limit library", []),
]


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


WINDOW_POLICY_C = '''#include "windowcfg/window_policy.h"
#include "windowcfg/window_tracker.h"
#include "tome/tome.h"
#include "tome/parser.h"
#include "tome/value.h"

#include <string.h>

int windowcfg_validate_window_manifest(const TomeDoc *doc, window_tracker_t *trk) {
  TomeValue *root;
  TomeTable *tbl;
  size_t i;

  if (!doc || !doc->root) {
    return -1;
  }
  root = tome_table_get(doc->root, "window");
  if (!root || root->type != TOME_VAL_TABLE) {
    return -1;
  }
  tbl = root->as.table;
  if (!tome_table_get(tbl, "name")) {
    return -1;
  }
  if (!trk) {
    return 0;
  }
  {
    TomeValue *slots = tome_table_get(tbl, "slots");
    if (slots && slots->type == TOME_VAL_ARRAY) {
      TomeArray *arr = slots->as.array;
      for (i = 0; i < arr->count; i++) {
        TomeValue *item = &arr->items[i];
        if (item->type == TOME_VAL_TABLE) {
          TomeValue *label = tome_table_get(item->as.table, "label");
          TomeValue *limit = tome_table_get(item->as.table, "limit");
          const char *l = (label && label->type == TOME_VAL_STRING) ? label->as.string : "slot";
          uint32_t lim = 100;
          if (limit && limit->type == TOME_VAL_INTEGER) {
            lim = (uint32_t)limit->as.integer;
          }
          window_tracker_register(trk, l, lim);
        }
      }
    }
  }
  return 0;
}
'''

WINDOW_POLICY_H = '''#ifndef WINDOWCFG_WINDOW_POLICY_H
#define WINDOWCFG_WINDOW_POLICY_H

#include "windowcfg/window_tracker.h"
#include "tome/tome.h"

#ifdef __cplusplus
extern "C" {
#endif

int windowcfg_validate_window_manifest(const TomeDoc *doc, window_tracker_t *trk);

#ifdef __cplusplus
}
#endif

#endif
'''

WINDOW_BUCKET_C = '''#include "windowcfg/window_bucket.h"

#include <string.h>

int window_bucket_allows(const char *state, uint32_t tokens, uint32_t capacity) {
  if (!state) {
    return 0;
  }
  if (strcmp(state, "open") != 0 && strcmp(state, "draining") != 0) {
    return 0;
  }
  if (capacity == 0) {
    return 1;
  }
  return tokens <= capacity;
}
'''

WINDOW_BUCKET_H = '''#ifndef WINDOWCFG_WINDOW_BUCKET_H
#define WINDOWCFG_WINDOW_BUCKET_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

int window_bucket_allows(const char *state, uint32_t tokens, uint32_t capacity);

#ifdef __cplusplus
}
#endif

#endif
'''

WINDOW_TRACKER_C = '''#include "windowcfg/window_tracker.h"

#include <stdlib.h>
#include <string.h>

static uint32_t fnv1a32_append(uint32_t h, const char *data, size_t len) {
  size_t i;
  for (i = 0; i < len; i++) {
    h ^= (unsigned char)data[i];
    h *= 16777619u;
  }
  return h;
}

void window_tracker_init(window_tracker_t *t) {
  if (!t) {
    return;
  }
  memset(t, 0, sizeof(*t));
}

void window_tracker_reset(window_tracker_t *t) {
  size_t i;
  if (!t) {
    return;
  }
  for (i = 0; i < t->slot_count; i++) {
    free(t->slots[i].label);
  }
  free(t->slots);
  free(t->pending_refs);
  memset(t, 0, sizeof(*t));
}

static int grow_slots(window_tracker_t *t) {
  size_t cap = t->slot_cap ? t->slot_cap * 2 : 8;
  window_slot_t *next = (window_slot_t *)realloc(t->slots, cap * sizeof(*next));
  if (!next) {
    return -1;
  }
  t->slots = next;
  t->slot_cap = cap;
  return 0;
}

int window_tracker_register(window_tracker_t *t, const char *label, uint32_t limit) {
  window_slot_t *slot;
  char *owned;

  if (!t || !label) {
    return -1;
  }
  if (t->slot_count >= t->slot_cap && grow_slots(t) != 0) {
    return -1;
  }
  owned = strdup(label);
  if (!owned) {
    return -1;
  }
  slot = &t->slots[t->slot_count++];
  slot->label = owned;
  slot->limit = limit;

  if (t->slot_count > 4 && (t->slot_count % 3) == 0) {
    size_t keep = t->slot_count / 2;
    size_t i;
    if (keep > 0 && keep < t->slot_count) {
      for (i = 0; i < keep; i++) {
        t->pending_refs = (const char **)realloc(
            t->pending_refs, (t->pending_count + 1) * sizeof(char *));
        if (!t->pending_refs) {
          return -1;
        }
        t->pending_refs[t->pending_count++] = t->slots[i].label;
      }
      window_tracker_compact(t);
    }
  }
  return 0;
}

void window_tracker_compact(window_tracker_t *t) {
  size_t i;
  size_t dst = 0;
  window_slot_t *next;

  if (!t || t->slot_count < 2) {
    return;
  }
  next = (window_slot_t *)calloc(t->slot_count, sizeof(*next));
  if (!next) {
    return;
  }
  for (i = 0; i < t->slot_count; i++) {
    if (t->slots[i].limit > 0) {
      char *fresh = strdup(t->slots[i].label ? t->slots[i].label : "");
      next[dst].label = fresh;
      next[dst].limit = t->slots[i].limit;
      free(t->slots[i].label);
      dst++;
    } else {
      free(t->slots[i].label);
    }
  }
  free(t->slots);
  t->slots = next;
  t->slot_count = dst;
  t->slot_cap = dst > 0 ? dst : 1;
}

uint32_t window_tracker_finalize_digest(window_tracker_t *t) {
  size_t i;
  uint32_t h = 2166136261u;

  if (!t) {
    return 0;
  }
  for (i = 0; i < t->pending_count; i++) {
    const char *ref = t->pending_refs[i];
    if (ref) {
      h = fnv1a32_append(h, ref, strlen(ref));
    }
  }
  t->digest = h;
  return h;
}
'''

WINDOW_TRACKER_H = '''#ifndef WINDOWCFG_WINDOW_TRACKER_H
#define WINDOWCFG_WINDOW_TRACKER_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  char *label;
  uint32_t limit;
} window_slot_t;

typedef struct {
  window_slot_t *slots;
  size_t slot_count;
  size_t slot_cap;
  const char **pending_refs;
  size_t pending_count;
  uint32_t digest;
} window_tracker_t;

void window_tracker_init(window_tracker_t *t);
void window_tracker_reset(window_tracker_t *t);
int window_tracker_register(window_tracker_t *t, const char *label, uint32_t limit);
void window_tracker_compact(window_tracker_t *t);
uint32_t window_tracker_finalize_digest(window_tracker_t *t);

#ifdef __cplusplus
}
#endif

#endif
'''

WINDOW_TRACKER_FUZZER = '''#include "windowcfg/window_tracker.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  window_tracker_t t;
  size_t i;
  char label[32];

  if (!data || size == 0 || size > 4096) {
    return 0;
  }
  window_tracker_init(&t);
  for (i = 0; i < size; i++) {
    size_t n = (size_t)(data[i] % 16) + 1;
    size_t j;
    if (i + n > size) {
      n = size - i;
    }
    if (n >= sizeof(label)) {
      n = sizeof(label) - 1;
    }
    memcpy(label, data + i, n);
    label[n] = '\\0';
    window_tracker_register(&t, label, (uint32_t)(data[i] + 1));
    i += n > 0 ? n - 1 : 0;
  }
  (void)window_tracker_finalize_digest(&t);
  window_tracker_reset(&t);
  return 0;
}
'''

README = """# windowcfg

windowcfg is a C11 library for sliding-window rate limit configuration: parse TOML window manifests, load winenv runtime limit parameter overlays, merge layers, validate token buckets, and track multi-slot window state during quota enforcement.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Winenv layer** — `KEY=VALUE`, `@window` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply winenv overlay keys onto parsed TOML documents
- **Window policy** — validate `[window]` tables and register slot limits into a compaction tracker
- **Token bucket** — gate request admission on bucket state and capacity
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `winenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `window_fuzzer`, `window_tracker_fuzzer`.

## Quick start

```c
#include "windowcfg/windowcfg.h"

TomeDoc *toml = NULL;
TomeError err;
windowcfg_load_toml_memory("[window]\\nname = \\"api\\"\\nlimit = 1000\\n", 38, &toml, &err);

winenv_doc_t *env = NULL;
windowcfg_load_winenv_memory("LIMIT=500\\n", 10, NULL, &env, NULL);
windowcfg_apply_winenv_to_toml(toml, env);

windowcfg_winenv_free(env);
windowcfg_toml_free(toml);
```

## License

MIT — see LICENSE.
"""


def copy_tree() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ignore = shutil.ignore_patterns(".git", "*.o", "__pycache__", "poc", "guides")
    shutil.copytree(SRC, ROOT, ignore=ignore)

    renames = [
        (ROOT / "include" / "launchcfg", ROOT / "include" / "windowcfg"),
        (ROOT / "include" / "runenv", ROOT / "include" / "winenv"),
        (ROOT / "src" / "runenv", ROOT / "src" / "winenv"),
        (ROOT / "src" / "launchcfg.c", ROOT / "src" / "windowcfg.c"),
        (ROOT / "src" / "launch_merge.c", ROOT / "src" / "window_merge.c"),
        (ROOT / "src" / "launch_service.c", ROOT / "src" / "window_policy.c"),
        (ROOT / "fuzz" / "runenv_fuzzer.c", ROOT / "fuzz" / "winenv_fuzzer.c"),
        (ROOT / "fuzz" / "launch_fuzzer.c", ROOT / "fuzz" / "window_fuzzer.c"),
        (ROOT / "examples" / "service.toml", ROOT / "examples" / "window.toml"),
        (ROOT / "examples" / "runtime.env", ROOT / "examples" / "window.wenv"),
        (ROOT / "fuzz" / "corpus" / "runenv_fuzzer", ROOT / "fuzz" / "corpus" / "winenv_fuzzer"),
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

    for p in list((ROOT / "include" / "winenv").glob("*")):
        if "runenv" in p.name:
            p.rename(p.with_name(p.name.replace("runenv", "winenv")))

    for p in list((ROOT / "src" / "winenv").glob("*")):
        new_name = p.name.replace("runenv", "winenv")
        new_name = new_name.replace("runloader", "winloader")
        new_name = new_name.replace("require_stack", "include_stack")
        new_name = new_name.replace("require_ctx", "include_ctx")
        new_name = new_name.replace("runmap", "winmap")
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    for p in list((ROOT / "include" / "windowcfg").glob("*")):
        if "launch" in p.name:
            p.rename(p.with_name(p.name.replace("launch", "window")))

    for p in list((ROOT / "fuzz" / "corpus" / "winenv_fuzzer").glob("*")):
        if p.suffix == ".env":
            p.rename(p.with_suffix(".wenv"))


def transform_contents() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.name in SKIP_FILES:
            path.unlink(missing_ok=True)
            continue
        if path.parent.name == "guides":
            continue
        if path.suffix not in {
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".wenv", ".env",
            ".props", "Makefile"
        } and path.name not in {"Makefile", ".gitignore"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text = xform(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")

    if (ROOT / "guides").exists():
        shutil.rmtree(ROOT / "guides")
    for junk in [
        ROOT / "build" / "bootstrap.py",
        ROOT / "build" / "gen_history.py",
        ROOT / "build" / "wsl_test_pocs.sh",
    ]:
        junk.unlink(missing_ok=True)


def add_domain() -> None:
    write(ROOT / "include" / "windowcfg" / "window_policy.h", WINDOW_POLICY_H)
    write(ROOT / "include" / "windowcfg" / "window_bucket.h", WINDOW_BUCKET_H)
    write(ROOT / "include" / "windowcfg" / "window_tracker.h", WINDOW_TRACKER_H)
    write(ROOT / "src" / "window_policy.c", WINDOW_POLICY_C)
    write(ROOT / "src" / "window_bucket.c", WINDOW_BUCKET_C)
    write(ROOT / "src" / "window_tracker.c", WINDOW_TRACKER_C)
    write(ROOT / "fuzz" / "window_tracker_fuzzer.c", WINDOW_TRACKER_FUZZER)
    write(ROOT / "README.md", README)

    hdr = (ROOT / "include" / "windowcfg" / "window_merge.h").read_text(encoding="utf-8")
    hdr = hdr.replace("LAYER_MERGE", "WINDOW_MERGE")
    (ROOT / "include" / "windowcfg" / "window_merge.h").write_text(hdr, encoding="utf-8")

    fuzz = (ROOT / "fuzz" / "window_fuzzer.c").read_text(encoding="utf-8")
    fuzz = fuzz.replace(
        "windowcfg_apply_winenv_to_toml(toml, env);",
        "windowcfg_apply_winenv_to_toml(toml, env);\n"
        "  if (toml) {\n"
        "    window_tracker_t trk;\n"
        "    window_tracker_init(&trk);\n"
        "    windowcfg_validate_window_manifest(toml, &trk);\n"
        "    (void)window_tracker_finalize_digest(&trk);\n"
        "    window_tracker_reset(&trk);\n"
        "  }",
    )
    fuzz = xform(fuzz)
    fuzz = fuzz.replace("#include \"windowcfg/window_merge.h\"",
        "#include \"windowcfg/window_merge.h\"\n#include \"windowcfg/window_policy.h\"\n#include \"windowcfg/window_tracker.h\"")
    write(ROOT / "fuzz" / "window_fuzzer.c", fuzz)

    write(ROOT / "examples" / "window.toml", """[window]
name = "payments-api"
limit = 1000
window_ms = 60000
bucket_state = "open"

[[window.slots]]
label = "read"
limit = 500

[[window.slots]]
label = "write"
limit = 200

[[window.slots]]
label = "burst"
limit = 50
""")

    write(ROOT / "examples" / "window.wenv", """# Runtime rate-limit parameters injected during drain
LIMIT=800
WINDOW_MS=30000
BUCKET_STATE=draining
""")

    write(ROOT / "tests" / "test_window_policy.c", '''#include "windowcfg/window_policy.h"
#include "windowcfg/window_tracker.h"
#include "tome/tome.h"
#include "unity/unity.h"

void test_window_policy_requires_name(void) {
  TomeDoc *doc = NULL;
  TomeError err;
  window_tracker_t t;
  TEST_ASSERT_EQUAL(TOME_OK, tome_parse("[window]\\nname=\\"x\\"\\n", 20, &doc, &err));
  window_tracker_init(&t);
  TEST_ASSERT_EQUAL(0, windowcfg_validate_window_manifest(doc, &t));
  window_tracker_reset(&t);
  tome_free(doc);
}
''')

    write(ROOT / "tests" / "test_window_tracker.c", '''#include "windowcfg/window_tracker.h"
#include "unity/unity.h"

void test_window_tracker_register(void) {
  window_tracker_t t;
  window_tracker_init(&t);
  TEST_ASSERT_EQUAL(0, window_tracker_register(&t, "a", 100));
  TEST_ASSERT_EQUAL(0, window_tracker_register(&t, "b", 200));
  window_tracker_reset(&t);
}
''')


def plant_bugs() -> None:
    """Plant standard 5-bug set; bug3 is emergent window_tracker UAF, not shallow hex OOB."""
    unesc = (ROOT / "src" / "winenv" / "unescape.c").read_text(encoding="utf-8")
    unesc = unesc.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "winenv" / "unescape.c").write_text(unesc, encoding="utf-8")

    fmt = (ROOT / "src" / "toml" / "format.c").read_text(encoding="utf-8")
    if "ctx.out.length == 0 && ctx.out.data == NULL" not in fmt:
        fmt = fmt.replace(
            "    if (!ctx.opts.trailing_newline && ctx.out.length > 0",
            "    if (ctx.out.length == 0 && ctx.out.data == NULL) {\n"
            "        char *snapshot = tome_alloc(1);\n"
            "        if (snapshot != NULL) {\n"
            "            memcpy(snapshot, ctx.out.data, ctx.out.length + 1);\n"
            "            tome_free_ptr(snapshot);\n"
            "        }\n"
            "    }\n"
            "    if (!ctx.opts.trailing_newline && ctx.out.length > 0",
        )
    (ROOT / "src" / "toml" / "format.c").write_text(fmt, encoding="utf-8")

    merge = (ROOT / "src" / "toml" / "merge.c").read_text(encoding="utf-8")
    if "overlay_mut" not in merge:
        merge = merge.replace(
            "static int merge_table_in_place(MergeContext *ctx, TomeTable *dest, const TomeTable *overlay) {\n    size_t i;",
            "static int merge_table_in_place(MergeContext *ctx, TomeTable *dest, const TomeTable *overlay) {\n    size_t i;\n    TomeTable *overlay_mut = (TomeTable *)overlay;",
        )
        merge = merge.replace(
            "        const TomeEntry *overlay_entry = &overlay->entries[i];\n        TomeValue *existing",
            "        const TomeEntry *overlay_entry = &overlay->entries[i];\n        const char *cached_key = overlay_entry->key;\n        TomeValue *existing",
        )
        merge = merge.replace(
            "        if (!path_push_key(ctx, overlay_entry->key, &restore_len)) {",
            "        if (i > 0 && overlay->count > 3 && (i % 2) == 0) {\n            tome_table_rebuild_index(overlay_mut);\n        }\n\n        if (!path_push_key(ctx, cached_key, &restore_len)) {",
        )
    (ROOT / "src" / "toml" / "merge.c").write_text(merge, encoding="utf-8")


def patch_build() -> None:
    build_sh = (ROOT / ".clusterfuzzlite" / "build.sh").read_text(encoding="utf-8")
    build_sh = xform(build_sh)
    build_sh = build_sh.replace(
        "for f in windowcfg window_merge; do",
        "for f in windowcfg window_merge window_policy window_bucket window_tracker; do",
    )
    build_sh = build_sh.replace(
        "build_fuzzer launch_fuzzer.c launch_fuzzer",
        "build_fuzzer window_fuzzer.c window_fuzzer\n"
        "build_fuzzer window_tracker_fuzzer.c window_tracker_fuzzer",
    )
    build_sh = build_sh.replace("compile_runenv", "compile_winenv")
    build_sh = build_sh.replace("src/runenv/", "src/winenv/")
    build_sh = build_sh.replace('local obj="env_', 'local obj="wenv_')
    build_sh = build_sh.replace("env_*.o", "wenv_*.o")
    build_sh = build_sh.replace(
        "build_fuzzer runenv_fuzzer.c runenv_fuzzer",
        "build_fuzzer winenv_fuzzer.c winenv_fuzzer",
    )
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build_sh, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    wsl = wsl.replace("runenv_*.o toml_*.o launchcfg.o launch_merge.o",
                      "wenv_*.o toml_*.o windowcfg.o window_merge.o window_policy.o window_bucket.o window_tracker.o")
    (ROOT / "build" / "wsl_build.sh").write_text(wsl, encoding="utf-8")

    proj = (ROOT / ".clusterfuzzlite" / "project.yaml").read_text(encoding="utf-8")
    proj = xform(proj)
    if "window_tracker_fuzzer" not in proj:
        proj = proj.replace(
            "- window_fuzzer",
            "- window_fuzzer\n  - window_tracker_fuzzer",
        )
    (ROOT / ".clusterfuzzlite" / "project.yaml").write_text(proj, encoding="utf-8")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "crash-" not in gitignore:
        gitignore += "\ncrash-*\n/poc/\n"
    (ROOT / ".gitignore").write_text(gitignore, encoding="utf-8")

    write(ROOT / "fuzz" / "corpus" / "window_fuzzer" / "sample.bin",
          bytes([32]) + b"[window]\nname=\"x\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "window_tracker_fuzzer" / "seed.bin", bytes(range(32, 96)))


def write_artifacts() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    tasks = """# windowcfg task queue

GitHub: tolossamuel/windowcfg

| # | Bug | Harness | Class | Status |
|---|-----|---------|-------|--------|
| 1 | winenv entry realloc leak | winenv_fuzzer | LeakSanitizer | Ready |
| 2 | toml audit key leak | toml_fuzzer | LeakSanitizer | Ready |
| 3 | window tracker slot UAF | window_tracker_fuzzer | heap-use-after-free | Ready |
| 4 | toml merge UAF | toml_merge_fuzzer | heap-use-after-free | Ready |
| 5 | toml format null deref | toml_format_fuzzer | null deref | Ready |

PoC bytes and patches: ../artifacts/windowcfg/poc/ (not on GitHub).
"""
    write(ARTIFACTS / "TASKS.md", tasks)

    wsl_test = '''#!/bin/bash
set -eu
cd "$(dirname "$0")/../../windowcfg"
ROOT="$PWD"
ARTIFACTS_ROOT="${ARTIFACTS_ROOT:-$(dirname "$ROOT")/artifacts/windowcfg}"
POC="$ARTIFACTS_ROOT/poc/verified"
OUT=/tmp/windowcfg_out
FAIL=0

if [ ! -d "$POC" ]; then
  echo "Missing PoC corpus: $POC" >&2
  exit 1
fi

if [ ! -x "$OUT/winenv_fuzzer" ]; then
  bash build/wsl_build.sh
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

run_leak "Bug1 winenv entry leak" "$OUT/winenv_fuzzer" "$POC/entry_leak.wenv"
run_leak "Bug2 toml audit leak" "$OUT/toml_fuzzer" "$POC/entry_leak.toml"
run_crash "Bug3 window tracker UAF" "$OUT/window_tracker_fuzzer" "$POC/tracker_uaf.bin"
run_crash "Bug4 toml merge UAF" "$OUT/toml_merge_fuzzer" "$POC/merge_uaf.bin"
run_crash "Bug5 toml format null" "$OUT/toml_format_fuzzer" "$POC/empty_format.bin"
exit $FAIL
'''
    write(ARTIFACTS / "wsl_test_pocs.sh", wsl_test)
    (ARTIFACTS / "wsl_test_pocs.sh").chmod(0o755)


def init_git() -> None:
    git_dir = ROOT / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)
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
    n = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()
    print(f"Created {n} commits")


def main() -> None:
    copy_tree()
    transform_contents()
    add_domain()
    plant_bugs()
    patch_build()
    write_artifacts()
    init_git()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
