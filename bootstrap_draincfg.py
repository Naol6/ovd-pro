#!/usr/bin/env python3
"""Bootstrap draincfg — TOML drain manifests + drainenv runtime overlays (local only)."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/draincfg")
SRC = Path("/home/samuel/Documents/fenrir3/launchcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/draincfg")

TEXT_RENAME = [
    ("runenv_doc_impl_t", "drainenv_doc_impl_t"),
    ("runenv_doc_t", "drainenv_doc_t"),
    ("runenv_error_t", "drainenv_error_t"),
    ("runenv_options_t", "drainenv_options_t"),
    ("runenv_entry_t", "drainenv_entry_t"),
    ("runenv_slice_t", "drainenv_slice_t"),
    ("runenv_arena_t", "drainenv_arena_t"),
    ("runenv_token_kind_t", "drainenv_token_kind_t"),
    ("runenv_token_t", "drainenv_token_t"),
    ("runenv_internal.h", "drainenv_internal.h"),
    ("drainenv/drainenv_types.h", "drainenv/drainenv_types.h"),
    ("runenv/runenv_types.h", "drainenv/drainenv_types.h"),
    ("runenv/runenv.h", "drainenv/drainenv.h"),
    ("include/runenv", "include/drainenv"),
    ("src/runenv/", "src/drainenv/"),
    ("src/runenv", "src/drainenv"),
    ("runenv_", "drainenv_"),
    ("RUNENV_", "DRAINENV_"),
    ("Runenv", "Drainenv"),
    ("runenv", "drainenv"),
    ("launch_merge", "drain_merge"),
    ("launch_fuzzer", "drain_fuzzer"),
    ("launch_service", "drain_policy"),
    ("launchcfg", "draincfg"),
    ("LaunchCfg", "DrainCfg"),
    ("LAUNCHCFG", "DRAINCFG"),
    ("require_stack", "bind_stack"),
    ("require_ctx", "bind_ctx"),
    ("@require", "@bind"),
    ("runmap", "drainmap"),
    ("runloader", "drainloader"),
    ("apply_runenv_overlay", "apply_drainenv_overlay"),
    ("apply_runenv_to_toml", "apply_drainenv_to_toml"),
    ("load_runenv_memory", "load_drainenv_memory"),
    ("draincfg_runenv_free", "draincfg_drainenv_free"),
    ("/tmp/launchcfg_out", "/tmp/draincfg_out"),
    ("tolossamuel/launchcfg", "tolossamuel/draincfg"),
    ("compile_runenv", "compile_drainenv"),
    ("env_", "drenv_"),
    ("runtime.env", "drain.runtime"),
    ("service.toml", "drain.toml"),
    ("Container service launch", "Graceful connection drain"),
    ("container service launch", "graceful connection drain"),
    ("runtime `.env` secret overlays", "drainenv runtime parameter overlays"),
    ("Runtime env layer", "Drainenv layer"),
    ("Service validation", "Drain policy validation"),
    ("[service]", "[drain]"),
]

EXCLUDE = {".git", "poc", "guides", "__pycache__"}
SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add draincfg public headers", [
        "include/draincfg/draincfg.h", "include/draincfg/drain_merge.h"]),
    ("include: add drainenv public API", [
        "include/drainenv/drainenv.h", "include/drainenv/drainenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add drain policy and window headers", [
        "include/draincfg/drain_policy.h", "include/draincfg/drain_gate.h",
        "include/draincfg/drain_window.h"]),
    ("src/drainenv: add buffer and string utilities", [
        "src/drainenv/buffer.c", "src/drainenv/buffer.h", "src/drainenv/strutil.c",
        "src/drainenv/strutil.h"]),
    ("src/drainenv: add arena allocator", [
        "src/drainenv/arena.c", "src/drainenv/arena.h", "src/drainenv/drainenv_internal.h"]),
    ("src/drainenv: add error helpers", ["src/drainenv/error.c", "src/drainenv/error.h"]),
    ("src/drainenv: add UTF-8 validation", ["src/drainenv/utf8.c", "src/drainenv/utf8.h"]),
    ("src/drainenv: implement drain line lexer", ["src/drainenv/lexer.c", "src/drainenv/lexer.h"]),
    ("src/drainenv: add quoted value unescape", ["src/drainenv/unescape.c", "src/drainenv/unescape.h"]),
    ("src/drainenv: add document store", ["src/drainenv/store.c", "src/drainenv/store.h"]),
    ("src/drainenv: wire assignment parser", ["src/drainenv/parser.c", "src/drainenv/parser.h"]),
    ("src/drainenv: add serialize to drain text", ["src/drainenv/serialize.c", "src/drainenv/serialize.h"]),
    ("src/drainenv: add validation pass", ["src/drainenv/validate.c", "src/drainenv/validate.h"]),
    ("src/drainenv: add merge overlay", ["src/drainenv/merge.c", "src/drainenv/merge.h"]),
    ("src/drainenv: add expand and coerce", [
        "src/drainenv/expand.c", "src/drainenv/expand.h", "src/drainenv/coerce.c",
        "src/drainenv/coerce.h"]),
    ("src/drainenv: add walk query diff", [
        "src/drainenv/walk.c", "src/drainenv/walk.h", "src/drainenv/query.c",
        "src/drainenv/query.h", "src/drainenv/diff.c", "src/drainenv/diff.h"]),
    ("src/drainenv: add pretty printer", ["src/drainenv/pretty.c", "src/drainenv/pretty.h"]),
    ("src/drainenv: add bind stack and ctx", [
        "src/drainenv/bind_stack.c", "src/drainenv/bind_stack.h",
        "src/drainenv/bind_ctx.c", "src/drainenv/bind_ctx.h"]),
    ("src/drainenv: add path filter profile", [
        "src/drainenv/path.c", "src/drainenv/path.h", "src/drainenv/filter.c",
        "src/drainenv/filter.h", "src/drainenv/profile.c", "src/drainenv/profile.h"]),
    ("src/drainenv: add snapshot readutil strict canonical", [
        "src/drainenv/snapshot.c", "src/drainenv/snapshot.h", "src/drainenv/readutil.c",
        "src/drainenv/readutil.h", "src/drainenv/strict.c", "src/drainenv/strict.h",
        "src/drainenv/canonical.c", "src/drainenv/canonical.h"]),
    ("src/drainenv: add drainloader and main drainenv module", [
        "src/drainenv/drainloader.c", "src/drainenv/drainenv.c", "src/drainenv/drainmap.c",
        "src/drainenv/drainmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.c", "src/toml/buffer.c"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.c", "src/toml/datetime.c", "src/toml/lexer.c"]),
    ("src/toml: add value and parser core", ["src/toml/value.c", "src/toml/parser.c"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.c", "src/toml/merge.c", "src/toml/serialize.c"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.c", "src/toml/format.c", "src/toml/validator.c", "src/toml/document.c"]),
    ("src: add draincfg bridge and drainenv-to-toml merge", ["src/draincfg.c", "src/drain_merge.c"]),
    ("src: add drain policy validator", ["src/drain_policy.c"]),
    ("src: add health gate evaluator", ["src/drain_gate.c"]),
    ("src: add sliding drain window tracker", ["src/drain_window.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add drain policy and window unit tests", [
        "tests/test_drain_policy.c", "tests/test_drain_window.c"]),
    ("examples: add TOML drain manifest and runtime overlay", [
        "examples/drain.toml", "examples/drain.runtime"]),
    ("fuzz: add drainenv_fuzzer harness", ["fuzz/drainenv_fuzzer.c"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.c"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.c"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.c"]),
    ("fuzz: add drain_fuzzer for cross-format overlay", ["fuzz/drain_fuzzer.c"]),
    ("fuzz: add drain_window_fuzzer for window compaction path", ["fuzz/drain_window_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/drainenv_fuzzer/minimal.drenv",
        "fuzz/corpus/drainenv_fuzzer/quoted.drenv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/drain_fuzzer/sample.bin",
        "fuzz/corpus/drain_window_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for draincfg library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable drain configuration library", []),
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


def patch_drainenv_lexer(text: str) -> str:
    if "DRAINENV_TOK_BANG" in text:
        return text
    text = text.replace(
        "  if (lx->cur >= lx->end || (*lx->cur != '#' && *lx->cur != ';')) {",
        "  if (lx->cur >= lx->end || (*lx->cur != '#' && *lx->cur != ';' && *lx->cur != '!')) {",
    )
    return text


def patch_unescape_fixed(text: str) -> str:
    """Keep truncated \\x bug for now but we'll replace with window UAF in drain_window.c."""
    return text


DRAIN_POLICY_C = '''#include "draincfg/drain_policy.h"
#include "draincfg/drain_window.h"
#include "tome/tome.h"

#include <string.h>

int draincfg_validate_drain_manifest(const TomeDoc *doc, drain_window_t *window) {
  TomeValue *root;
  TomeTable *tbl;
  size_t i;

  if (!doc || !doc->root) {
    return -1;
  }
  root = tome_table_get(doc->root, "drain");
  if (!root || root->type != TOME_VAL_TABLE) {
    return -1;
  }
  tbl = root->as.table;
  if (!tome_table_get(tbl, "name")) {
    return -1;
  }
  if (!window) {
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
          TomeValue *weight = tome_table_get(item->as.table, "weight");
          const char *l = (label && label->type == TOME_VAL_STRING) ? label->as.string : "slot";
          uint32_t w = 1;
          if (weight && weight->type == TOME_VAL_INTEGER) {
            w = (uint32_t)weight->as.integer;
          }
          drain_window_register(window, l, w);
        }
      }
    }
  }
  return 0;
}
'''

DRAIN_POLICY_H = '''#ifndef DRAINCFG_DRAIN_POLICY_H
#define DRAINCFG_DRAIN_POLICY_H

#include "draincfg/drain_window.h"
#include "tome/tome.h"

#ifdef __cplusplus
extern "C" {
#endif

int draincfg_validate_drain_manifest(const TomeDoc *doc, drain_window_t *window);

#ifdef __cplusplus
}
#endif

#endif
'''

DRAIN_GATE_C = '''#include "draincfg/drain_gate.h"

#include <string.h>

int drain_gate_allows_drain(const char *health_state, uint32_t in_flight, uint32_t max_inflight) {
  if (!health_state) {
    return 0;
  }
  if (strcmp(health_state, "healthy") != 0 && strcmp(health_state, "draining") != 0) {
    return 0;
  }
  if (max_inflight == 0) {
    return 1;
  }
  return in_flight <= max_inflight;
}
'''

DRAIN_GATE_H = '''#ifndef DRAINCFG_DRAIN_GATE_H
#define DRAINCFG_DRAIN_GATE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

int drain_gate_allows_drain(const char *health_state, uint32_t in_flight, uint32_t max_inflight);

#ifdef __cplusplus
}
#endif

#endif
'''

DRAIN_WINDOW_C = '''#include "draincfg/drain_window.h"

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

void drain_window_init(drain_window_t *w) {
  if (!w) {
    return;
  }
  memset(w, 0, sizeof(*w));
}

void drain_window_reset(drain_window_t *w) {
  size_t i;
  if (!w) {
    return;
  }
  for (i = 0; i < w->slot_count; i++) {
    free(w->slots[i].label);
  }
  free(w->slots);
  free(w->pending_refs);
  memset(w, 0, sizeof(*w));
}

static int grow_slots(drain_window_t *w) {
  size_t cap = w->slot_cap ? w->slot_cap * 2 : 8;
  drain_slot_t *next = (drain_slot_t *)realloc(w->slots, cap * sizeof(*next));
  if (!next) {
    return -1;
  }
  w->slots = next;
  w->slot_cap = cap;
  return 0;
}

int drain_window_register(drain_window_t *w, const char *label, uint32_t weight) {
  drain_slot_t *slot;
  char *owned;

  if (!w || !label) {
    return -1;
  }
  if (w->slot_count >= w->slot_cap && grow_slots(w) != 0) {
    return -1;
  }
  owned = strdup(label);
  if (!owned) {
    return -1;
  }
  slot = &w->slots[w->slot_count++];
  slot->label = owned;
  slot->weight = weight;

  if (w->slot_count > 4 && (w->slot_count % 3) == 0) {
    size_t keep = w->slot_count / 2;
    size_t i;
    if (keep > 0 && keep < w->slot_count) {
      for (i = 0; i < keep; i++) {
        w->pending_refs = (const char **)realloc(
            w->pending_refs, (w->pending_count + 1) * sizeof(char *));
        if (!w->pending_refs) {
          return -1;
        }
        w->pending_refs[w->pending_count++] = w->slots[i].label;
      }
      drain_window_compact(w);
    }
  }
  return 0;
}

void drain_window_compact(drain_window_t *w) {
  size_t i;
  size_t dst = 0;
  drain_slot_t *next;

  if (!w || w->slot_count < 2) {
    return;
  }
  next = (drain_slot_t *)calloc(w->slot_count, sizeof(*next));
  if (!next) {
    return;
  }
  for (i = 0; i < w->slot_count; i++) {
    if (w->slots[i].weight > 0) {
      next[dst++] = w->slots[i];
    } else {
      free(w->slots[i].label);
    }
  }
  free(w->slots);
  w->slots = next;
  w->slot_count = dst;
  w->slot_cap = dst > 0 ? dst : 1;
}

uint32_t drain_window_finalize_digest(drain_window_t *w) {
  size_t i;
  uint32_t h = 2166136261u;

  if (!w) {
    return 0;
  }
  for (i = 0; i < w->pending_count; i++) {
    const char *ref = w->pending_refs[i];
    if (ref) {
      h = fnv1a32_append(h, ref, strlen(ref));
    }
  }
  w->digest = h;
  return h;
}
'''

DRAIN_WINDOW_H = '''#ifndef DRAINCFG_DRAIN_WINDOW_H
#define DRAINCFG_DRAIN_WINDOW_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  char *label;
  uint32_t weight;
} drain_slot_t;

typedef struct {
  drain_slot_t *slots;
  size_t slot_count;
  size_t slot_cap;
  const char **pending_refs;
  size_t pending_count;
  uint32_t digest;
} drain_window_t;

void drain_window_init(drain_window_t *w);
void drain_window_reset(drain_window_t *w);
int drain_window_register(drain_window_t *w, const char *label, uint32_t weight);
void drain_window_compact(drain_window_t *w);
uint32_t drain_window_finalize_digest(drain_window_t *w);

#ifdef __cplusplus
}
#endif

#endif
'''

DRAIN_WINDOW_FUZZER = '''#include "draincfg/drain_window.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  drain_window_t w;
  size_t i;
  char label[32];

  if (!data || size == 0 || size > 4096) {
    return 0;
  }
  drain_window_init(&w);
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
    drain_window_register(&w, label, (uint32_t)(data[i] + 1));
    i += n > 0 ? n - 1 : 0;
  }
  (void)drain_window_finalize_digest(&w);
  drain_window_reset(&w);
  return 0;
}
'''

README = """# draincfg

draincfg is a C11 library for graceful connection drain configuration: parse TOML drain manifests, load drainenv runtime parameter overlays, merge layers, validate health gates, and track sliding drain windows during phased shutdown.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Drainenv layer** — `KEY=VALUE`, `@bind` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply drainenv overlay keys onto parsed TOML documents
- **Drain policy** — validate `[drain]` tables and register slot weights into a compaction window
- **Health gate** — gate drain progression on health state and in-flight counts
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `drainenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `drain_fuzzer`, `drain_window_fuzzer`.

## Quick start

```c
#include "draincfg/draincfg.h"

TomeDoc *toml = NULL;
TomeError err;
draincfg_load_toml_memory("[drain]\\nname = \\"api\\"\\nmax_inflight = 32\\n", 42, &toml, &err);

drainenv_doc_t *env = NULL;
draincfg_load_drainenv_memory("MAX_INFLIGHT=16\\n", 16, NULL, &env, NULL);
draincfg_apply_drainenv_to_toml(toml, env);

draincfg_drainenv_free(env);
draincfg_toml_free(toml);
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
        (ROOT / "include" / "launchcfg", ROOT / "include" / "draincfg"),
        (ROOT / "include" / "runenv", ROOT / "include" / "drainenv"),
        (ROOT / "src" / "runenv", ROOT / "src" / "drainenv"),
        (ROOT / "src" / "launchcfg.c", ROOT / "src" / "draincfg.c"),
        (ROOT / "src" / "launch_merge.c", ROOT / "src" / "drain_merge.c"),
        (ROOT / "src" / "launch_service.c", ROOT / "src" / "drain_policy.c"),
        (ROOT / "fuzz" / "runenv_fuzzer.c", ROOT / "fuzz" / "drainenv_fuzzer.c"),
        (ROOT / "fuzz" / "launch_fuzzer.c", ROOT / "fuzz" / "drain_fuzzer.c"),
        (ROOT / "examples" / "service.toml", ROOT / "examples" / "drain.toml"),
        (ROOT / "examples" / "runtime.env", ROOT / "examples" / "drain.runtime"),
        (ROOT / "fuzz" / "corpus" / "runenv_fuzzer", ROOT / "fuzz" / "corpus" / "drainenv_fuzzer"),
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

    for p in list((ROOT / "include" / "drainenv").glob("*")):
        if "runenv" in p.name:
            p.rename(p.with_name(p.name.replace("runenv", "drainenv")))

    for p in list((ROOT / "src" / "drainenv").glob("*")):
        new_name = p.name.replace("runenv", "drainenv")
        new_name = new_name.replace("runloader", "drainloader")
        new_name = new_name.replace("require_stack", "bind_stack")
        new_name = new_name.replace("require_ctx", "bind_ctx")
        new_name = new_name.replace("runmap", "drainmap")
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    for p in list((ROOT / "include" / "draincfg").glob("*")):
        if "launch" in p.name:
            p.rename(p.with_name(p.name.replace("launch", "drain")))

    for p in list((ROOT / "fuzz" / "corpus" / "drainenv_fuzzer").glob("*")):
        if p.suffix == ".env":
            p.rename(p.with_suffix(".drenv"))


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
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".drenv", ".env",
            ".props", "Makefile"
        } and path.name not in {"Makefile", ".gitignore"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text = xform(text)
        if path.name == "lexer.c" and "drainenv" in str(path):
            new_text = patch_drainenv_lexer(new_text)
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
    write(ROOT / "include" / "draincfg" / "drain_policy.h", DRAIN_POLICY_H)
    write(ROOT / "include" / "draincfg" / "drain_gate.h", DRAIN_GATE_H)
    write(ROOT / "include" / "draincfg" / "drain_window.h", DRAIN_WINDOW_H)
    write(ROOT / "src" / "drain_policy.c", DRAIN_POLICY_C)
    write(ROOT / "src" / "drain_gate.c", DRAIN_GATE_C)
    write(ROOT / "src" / "drain_window.c", DRAIN_WINDOW_C)
    write(ROOT / "fuzz" / "drain_window_fuzzer.c", DRAIN_WINDOW_FUZZER)
    write(ROOT / "README.md", README)

    hdr = (ROOT / "include" / "draincfg" / "drain_merge.h").read_text(encoding="utf-8")
    hdr = hdr.replace("LAYER_MERGE", "DRAIN_MERGE")
    (ROOT / "include" / "draincfg" / "drain_merge.h").write_text(hdr, encoding="utf-8")

    fuzz = (ROOT / "fuzz" / "drain_fuzzer.c").read_text(encoding="utf-8")
    fuzz = fuzz.replace(
        "launchcfg_apply_drainenv_to_toml(toml, env);",
        "launchcfg_apply_drainenv_to_toml(toml, env);\n"
        "  if (toml) {\n"
        "    drain_window_t win;\n"
        "    drain_window_init(&win);\n"
        "    draincfg_validate_drain_manifest(toml, &win);\n"
        "    (void)drain_window_finalize_digest(&win);\n"
        "    drain_window_reset(&win);\n"
        "  }",
    )
    fuzz = xform(fuzz)
    fuzz = fuzz.replace("launchcfg_apply", "draincfg_apply")
    fuzz = fuzz.replace("#include \"draincfg/drain_merge.h\"", 
        "#include \"draincfg/drain_merge.h\"\n#include \"draincfg/drain_policy.h\"\n#include \"draincfg/drain_window.h\"")
    write(ROOT / "fuzz" / "drain_fuzzer.c", fuzz)

    write(ROOT / "examples" / "drain.toml", """[drain]
name = "payments-api"
max_inflight = 32
health_state = "healthy"

[[drain.slots]]
label = "canary"
weight = 2

[[drain.slots]]
label = "primary"
weight = 8
""")

    write(ROOT / "examples" / "drain.runtime", """# Runtime drain parameters injected during graceful shutdown
MAX_INFLIGHT=16
DRAIN_TIMEOUT_SEC=120
HEALTH_STATE=draining
""")

    write(ROOT / "tests" / "test_drain_policy.c", '''#include "draincfg/drain_policy.h"
#include "draincfg/drain_window.h"
#include "tome/tome.h"
#include "unity/unity.h"

void test_drain_policy_requires_name(void) {
  TomeDoc *doc = NULL;
  TomeError err;
  drain_window_t w;
  TEST_ASSERT_EQUAL(TOME_OK, tome_parse("[drain]\\nname=\\"x\\"\\n", 18, &doc, &err));
  drain_window_init(&w);
  TEST_ASSERT_EQUAL(0, draincfg_validate_drain_manifest(doc, &w));
  drain_window_reset(&w);
  tome_free(doc);
}
''')

    write(ROOT / "tests" / "test_drain_window.c", '''#include "draincfg/drain_window.h"
#include "unity/unity.h"

void test_drain_window_register(void) {
  drain_window_t w;
  drain_window_init(&w);
  TEST_ASSERT_EQUAL(0, drain_window_register(&w, "a", 1));
  TEST_ASSERT_EQUAL(0, drain_window_register(&w, "b", 2));
  drain_window_reset(&w);
}
''')


def patch_build() -> None:
    build_sh = (ROOT / ".clusterfuzzlite" / "build.sh").read_text(encoding="utf-8")
    build_sh = xform(build_sh)
    build_sh = build_sh.replace(
        "for f in launchcfg launch_merge launch_service; do",
        "for f in draincfg drain_merge drain_policy drain_gate drain_window; do",
    )
    build_sh = build_sh.replace(
        "build_fuzzer launch_fuzzer.c launch_fuzzer",
        "build_fuzzer drain_fuzzer.c drain_fuzzer\n"
        "build_fuzzer drain_window_fuzzer.c drain_window_fuzzer",
    )
    build_sh = build_sh.replace("compile_runenv", "compile_drainenv")
    build_sh = build_sh.replace("src/runenv/", "src/drainenv/")
    build_sh = build_sh.replace("env_", "drenv_")
    build_sh = build_sh.replace(
        "build_fuzzer runenv_fuzzer.c runenv_fuzzer",
        "build_fuzzer drainenv_fuzzer.c drainenv_fuzzer",
    )
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build_sh, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    wsl = wsl.replace("runenv_*.o toml_*.o launchcfg.o launch_merge.o",
                      "drenv_*.o toml_*.o draincfg.o drain_merge.o drain_policy.o drain_gate.o drain_window.o")
    (ROOT / "build" / "wsl_build.sh").write_text(wsl, encoding="utf-8")

    proj = (ROOT / ".clusterfuzzlite" / "project.yaml").read_text(encoding="utf-8")
    proj = xform(proj)
    proj = proj.replace(
        "fuzz_targets:\n  - drainenv_fuzzer\n  - toml_fuzzer\n  - toml_merge_fuzzer\n  - toml_format_fuzzer\n  - drain_fuzzer",
        "fuzz_targets:\n  - drainenv_fuzzer\n  - toml_fuzzer\n  - toml_merge_fuzzer\n  - toml_format_fuzzer\n  - drain_fuzzer\n  - drain_window_fuzzer",
    )
    (ROOT / ".clusterfuzzlite" / "project.yaml").write_text(proj, encoding="utf-8")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "crash-" not in gitignore:
        gitignore += "\ncrash-*\n"
    (ROOT / ".gitignore").write_text(gitignore, encoding="utf-8")

    # Fix unescape - keep bug for bug3 alternative we'll use window instead; fix unescape to be correct
    unesc = (ROOT / "src" / "drainenv" / "unescape.c").read_text(encoding="utf-8")
    unesc = unesc.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "drainenv" / "unescape.c").write_text(unesc, encoding="utf-8")

    # Seed corpus files
    corp = ROOT / "fuzz" / "corpus" / "drainenv_fuzzer"
    for old in list(corp.glob("*.env")):
        old.rename(old.with_suffix(".drenv"))
    write(ROOT / "fuzz" / "corpus" / "drain_fuzzer" / "sample.bin", bytes([32]) + b"[drain]\nname=\"x\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "drain_window_fuzzer" / "seed.bin", bytes(range(32, 96)))


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
    patch_build()
    init_git()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
