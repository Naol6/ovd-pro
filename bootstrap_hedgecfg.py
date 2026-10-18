#!/usr/bin/env python3
"""Bootstrap hedgecfg — TOML HTTP request-hedging manifests + hedgeenv runtime overlays."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/hedgecfg")
SRC = Path("/home/samuel/Documents/fenrir3/launchcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/hedgecfg")

TEXT_RENAME = [
    ("runenv_doc_impl_t", "hedgeenv_doc_impl_t"),
    ("runenv_doc_t", "hedgeenv_doc_t"),
    ("runenv_error_t", "hedgeenv_error_t"),
    ("runenv_options_t", "hedgeenv_options_t"),
    ("runenv_entry_t", "hedgeenv_entry_t"),
    ("runenv_slice_t", "hedgeenv_slice_t"),
    ("runenv_arena_t", "hedgeenv_arena_t"),
    ("runenv_token_kind_t", "hedgeenv_token_kind_t"),
    ("runenv_token_t", "hedgeenv_token_t"),
    ("runenv_internal.h", "hedgeenv_internal.h"),
    ("runenv/runenv_types.h", "hedgeenv/hedgeenv_types.h"),
    ("include/runenv", "include/hedgeenv"),
    ("src/runenv/", "src/hedgeenv/"),
    ("src/runenv", "src/hedgeenv"),
    ("runenv_", "hedgeenv_"),
    ("RUNENV_", "HEDGEENV_"),
    ("Runenv", "Hedgeenv"),
    ("runenv", "hedgeenv"),
    ("launch_merge", "hedge_merge"),
    ("launch_fuzzer", "hedge_fuzzer"),
    ("launch_service", "hedge_policy"),
    ("launchcfg", "hedgecfg"),
    ("LaunchCfg", "HedgeCfg"),
    ("LAUNCHCFG", "HEDGECFG"),
    ("require_stack", "fanout_stack"),
    ("require_ctx", "fanout_ctx"),
    ("@require", "@hedge"),
    ("runmap", "hedgemap"),
    ("runloader", "hedgeloader"),
    ("apply_runenv_overlay", "apply_hedgeenv_overlay"),
    ("apply_runenv_to_toml", "apply_hedgeenv_to_toml"),
    ("load_runenv_memory", "load_hedgeenv_memory"),
    ("hedgecfg_runenv_free", "hedgecfg_hedgeenv_free"),
    ("/tmp/launchcfg_out", "/tmp/hedgecfg_out"),
    ("tolossamuel/launchcfg", "tolossamuel/hedgecfg"),
    ("compile_runenv", "compile_hedgeenv"),
    ("runtime.env", "hedge.runtime"),
    ("service.toml", "hedge.toml"),
    ("Container service launch", "HTTP request hedging policy"),
    ("container service launch", "HTTP request hedging policy"),
    ("runtime `.env` secret overlays", "hedgeenv runtime rate-limit parameter overlays"),
    ("Runtime env layer", "Hedgeenv layer"),
    ("Service validation", "Hedge policy validation"),
    ("[service]", "[hedge]"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add hedgecfg public headers", [
        "include/hedgecfg/hedgecfg.h", "include/hedgecfg/hedge_merge.h"]),
    ("include: add hedgeenv public API", [
        "include/hedgeenv/hedgeenv.h", "include/hedgeenv/hedgeenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add hedge policy gate registry headers", [
        "include/hedgecfg/hedge_policy.h", "include/hedgecfg/hedge_gate.h",
        "include/hedgecfg/hedge_registry.h"]),
    ("src/hedgeenv: add buffer and string utilities", [
        "src/hedgeenv/buffer.c", "src/hedgeenv/buffer.h", "src/hedgeenv/strutil.c",
        "src/hedgeenv/strutil.h"]),
    ("src/hedgeenv: add arena allocator", [
        "src/hedgeenv/arena.c", "src/hedgeenv/arena.h", "src/hedgeenv/hedgeenv_internal.h"]),
    ("src/hedgeenv: add error helpers", ["src/hedgeenv/error.c", "src/hedgeenv/error.h"]),
    ("src/hedgeenv: add UTF-8 validation", ["src/hedgeenv/utf8.c", "src/hedgeenv/utf8.h"]),
    ("src/hedgeenv: implement hedgeenv line lexer", ["src/hedgeenv/lexer.c", "src/hedgeenv/lexer.h"]),
    ("src/hedgeenv: add quoted value unescape", ["src/hedgeenv/unescape.c", "src/hedgeenv/unescape.h"]),
    ("src/hedgeenv: add document store", ["src/hedgeenv/store.c", "src/hedgeenv/store.h"]),
    ("src/hedgeenv: wire assignment parser", ["src/hedgeenv/parser.c", "src/hedgeenv/parser.h"]),
    ("src/hedgeenv: add serialize to hedgeenv text", ["src/hedgeenv/serialize.c", "src/hedgeenv/serialize.h"]),
    ("src/hedgeenv: add validation pass", ["src/hedgeenv/validate.c", "src/hedgeenv/validate.h"]),
    ("src/hedgeenv: add merge overlay", ["src/hedgeenv/merge.c", "src/hedgeenv/merge.h"]),
    ("src/hedgeenv: add expand and coerce", [
        "src/hedgeenv/expand.c", "src/hedgeenv/expand.h", "src/hedgeenv/coerce.c",
        "src/hedgeenv/coerce.h"]),
    ("src/hedgeenv: add walk query diff", [
        "src/hedgeenv/walk.c", "src/hedgeenv/walk.h", "src/hedgeenv/query.c",
        "src/hedgeenv/query.h", "src/hedgeenv/diff.c", "src/hedgeenv/diff.h"]),
    ("src/hedgeenv: add pretty printer", ["src/hedgeenv/pretty.c", "src/hedgeenv/pretty.h"]),
    ("src/hedgeenv: add include stack and ctx", [
        "src/hedgeenv/fanout_stack.c", "src/hedgeenv/fanout_stack.h",
        "src/hedgeenv/fanout_ctx.c", "src/hedgeenv/fanout_ctx.h"]),
    ("src/hedgeenv: add path filter profile", [
        "src/hedgeenv/path.c", "src/hedgeenv/path.h", "src/hedgeenv/filter.c",
        "src/hedgeenv/filter.h", "src/hedgeenv/profile.c", "src/hedgeenv/profile.h"]),
    ("src/hedgeenv: add snapshot readutil strict canonical", [
        "src/hedgeenv/snapshot.c", "src/hedgeenv/snapshot.h", "src/hedgeenv/readutil.c",
        "src/hedgeenv/readutil.h", "src/hedgeenv/strict.c", "src/hedgeenv/strict.h",
        "src/hedgeenv/canonical.c", "src/hedgeenv/canonical.h"]),
    ("src/hedgeenv: add hedgeloader and main hedgeenv module", [
        "src/hedgeenv/hedgeloader.c", "src/hedgeenv/hedgeenv.c", "src/hedgeenv/hedgemap.c",
        "src/hedgeenv/hedgemap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.c", "src/toml/buffer.c"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.c", "src/toml/datetime.c", "src/toml/lexer.c"]),
    ("src/toml: add value and parser core", ["src/toml/value.c", "src/toml/parser.c"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.c", "src/toml/merge.c", "src/toml/serialize.c"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.c", "src/toml/format.c", "src/toml/validator.c", "src/toml/document.c"]),
    ("src: add hedgecfg bridge and hedgeenv-to-toml merge", ["src/hedgecfg.c", "src/hedge_merge.c"]),
    ("src: add window policy validator", ["src/hedge_policy.c"]),
    ("src: add latency budget gate evaluator", ["src/hedge_gate.c"]),
    ("src: add hedge endpoint registry with compaction", ["src/hedge_registry.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add hedge policy and registry unit tests", [
        "tests/test_hedge_policy.c", "tests/test_hedge_registry.c"]),
    ("examples: add TOML hedge manifest and runtime overlay", [
        "examples/hedge.toml", "examples/hedge.runtime"]),
    ("fuzz: add hedgeenv_fuzzer harness", ["fuzz/hedgeenv_fuzzer.c"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.c"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.c"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.c"]),
    ("fuzz: add hedge_fuzzer for cross-format overlay", ["fuzz/hedge_fuzzer.c"]),
    ("fuzz: add hedge_registry_fuzzer for slot compaction path", ["fuzz/hedge_registry_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/hedgeenv_fuzzer/minimal.henv",
        "fuzz/corpus/hedgeenv_fuzzer/quoted.henv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/hedge_fuzzer/sample.bin",
        "fuzz/corpus/hedge_registry_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for hedgecfg library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable request hedging policy library", []),
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


HEDGE_POLICY_C = '''#include "hedgecfg/hedge_policy.h"
#include "hedgecfg/hedge_registry.h"
#include "tome/tome.h"
#include "tome/parser.h"
#include "tome/value.h"

#include <string.h>

int hedgecfg_validate_hedge_manifest(const TomeDoc *doc, hedge_registry_t *trk) {
  TomeValue *root;
  TomeTable *tbl;
  size_t i;

  if (!doc || !doc->root) {
    return -1;
  }
  root = tome_table_get(doc->root, "hedge");
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
    TomeValue *slots = tome_table_get(tbl, "endpoints");
    if (slots && slots->type == TOME_VAL_ARRAY) {
      TomeArray *arr = slots->as.array;
      for (i = 0; i < arr->count; i++) {
        TomeValue *item = &arr->items[i];
        if (item->type == TOME_VAL_TABLE) {
          TomeValue *label = tome_table_get(item->as.table, "endpoint");
          TomeValue *label2 = tome_table_get(item->as.table, "latency_budget_ms");
          const char *l = (label && label->type == TOME_VAL_STRING) ? label->as.string : "endpoint";
          uint32_t budget = 100;
          if (label2 && label2->type == TOME_VAL_INTEGER) {
            budget = (uint32_t)label2->as.integer;
          }
          hedge_registry_register(trk, l, budget);
        }
      }
    }
  }
  return 0;
}
'''

WINDOW_POLICY_H = '''#ifndef HEDGECFG_WINDOW_POLICY_H
#define HEDGECFG_WINDOW_POLICY_H

#include "hedgecfg/hedge_registry.h"
#include "tome/tome.h"

#ifdef __cplusplus
extern "C" {
#endif

int hedgecfg_validate_hedge_manifest(const TomeDoc *doc, hedge_registry_t *trk);

#ifdef __cplusplus
}
#endif

#endif
'''

HEDGE_GATE_C = '''#include "hedgecfg/hedge_gate.h"

#include <string.h>

int hedge_gate_allows(const char *state, uint32_t tokens, uint32_t capacity) {
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

WINDOW_BUCKET_H = '''#ifndef HEDGECFG_WINDOW_BUCKET_H
#define HEDGECFG_WINDOW_BUCKET_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

int hedge_gate_allows(const char *state, uint32_t tokens, uint32_t capacity);

#ifdef __cplusplus
}
#endif

#endif
'''

HEDGE_REGISTRY_C = '''#include "hedgecfg/hedge_registry.h"

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

void hedge_registry_init(hedge_registry_t *t) {
  if (!t) {
    return;
  }
  memset(t, 0, sizeof(*t));
}

void hedge_registry_reset(hedge_registry_t *t) {
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

static int grow_slots(hedge_registry_t *t) {
  size_t cap = t->slot_cap ? t->slot_cap * 2 : 8;
  hedge_endpoint_t *next = (hedge_endpoint_t *)realloc(t->slots, cap * sizeof(*next));
  if (!next) {
    return -1;
  }
  t->slots = next;
  t->slot_cap = cap;
  return 0;
}

int hedge_registry_register(hedge_registry_t *t, const char *label, uint32_t budget) {
  hedge_endpoint_t *slot;
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
  slot->latency_budget_ms = budget;

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
      hedge_registry_compact(t);
    }
  }
  return 0;
}

void hedge_registry_compact(hedge_registry_t *t) {
  size_t i;
  size_t dst = 0;
  hedge_endpoint_t *next;

  if (!t || t->slot_count < 2) {
    return;
  }
  next = (hedge_endpoint_t *)calloc(t->slot_count, sizeof(*next));
  if (!next) {
    return;
  }
  for (i = 0; i < t->slot_count; i++) {
    if (t->slots[i].latency_budget_ms > 0) {
      char *fresh = strdup(t->slots[i].label ? t->slots[i].label : "");
      next[dst].label = fresh;
      next[dst].latency_budget_ms = t->slots[i].latency_budget_ms;
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

uint32_t hedge_registry_finalize_digest(hedge_registry_t *t) {
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

HEDGE_REGISTRY_H = '''#ifndef HEDGECFG_HEDGE_REGISTRY_H
#define HEDGECFG_HEDGE_REGISTRY_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  char *label;
  uint32_t latency_budget_ms;
} hedge_endpoint_t;

typedef struct {
  hedge_endpoint_t *slots;
  size_t slot_count;
  size_t slot_cap;
  const char **pending_refs;
  size_t pending_count;
  uint32_t digest;
} hedge_registry_t;

void hedge_registry_init(hedge_registry_t *t);
void hedge_registry_reset(hedge_registry_t *t);
int hedge_registry_register(hedge_registry_t *t, const char *label, uint32_t budget);
void hedge_registry_compact(hedge_registry_t *t);
uint32_t hedge_registry_finalize_digest(hedge_registry_t *t);

#ifdef __cplusplus
}
#endif

#endif
'''

HEDGE_REGISTRY_FUZZER = '''#include "hedgecfg/hedge_registry.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  hedge_registry_t t;
  size_t i;
  char label[32];

  if (!data || size == 0 || size > 4096) {
    return 0;
  }
  hedge_registry_init(&t);
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
    hedge_registry_register(&t, label, (uint32_t)(data[i] + 1));
    i += n > 0 ? n - 1 : 0;
  }
  (void)hedge_registry_finalize_digest(&t);
  hedge_registry_reset(&t);
  return 0;
}
'''

README = """# hedgecfg

hedgecfg is a C11 library for HTTP request hedging policy configuration: parse TOML hedge manifests, load hedgeenv runtime limit parameter overlays, merge layers, validate latency budgets, and track duplicate-request endpoint registry during hedged fanout.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Hedgeenv layer** — `KEY=VALUE`, `@hedge` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply hedgeenv overlay keys onto parsed TOML documents
- **Hedge policy** — validate `[hedge]` tables and register slot limits into a compaction tracker
- **Latency gate** — gate request admission on bucket state and capacity
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `hedgeenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `hedge_fuzzer`, `hedge_registry_fuzzer`.

## Quick start

```c
#include "hedgecfg/hedgecfg.h"

TomeDoc *toml = NULL;
TomeError err;
hedgecfg_load_toml_memory("[hedge]\\nname = \\"api\\"\\nlimit = 1000\\n", 38, &toml, &err);

hedgeenv_doc_t *env = NULL;
hedgecfg_load_hedgeenv_memory("LIMIT=500\\n", 10, NULL, &env, NULL);
hedgecfg_apply_hedgeenv_to_toml(toml, env);

hedgecfg_hedgeenv_free(env);
hedgecfg_toml_free(toml);
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
        (ROOT / "include" / "launchcfg", ROOT / "include" / "hedgecfg"),
        (ROOT / "include" / "runenv", ROOT / "include" / "hedgeenv"),
        (ROOT / "src" / "runenv", ROOT / "src" / "hedgeenv"),
        (ROOT / "src" / "launchcfg.c", ROOT / "src" / "hedgecfg.c"),
        (ROOT / "src" / "launch_merge.c", ROOT / "src" / "hedge_merge.c"),
        (ROOT / "src" / "launch_service.c", ROOT / "src" / "hedge_policy.c"),
        (ROOT / "fuzz" / "runenv_fuzzer.c", ROOT / "fuzz" / "hedgeenv_fuzzer.c"),
        (ROOT / "fuzz" / "launch_fuzzer.c", ROOT / "fuzz" / "hedge_fuzzer.c"),
        (ROOT / "examples" / "service.toml", ROOT / "examples" / "hedge.toml"),
        (ROOT / "examples" / "runtime.env", ROOT / "examples" / "hedge.runtime"),
        (ROOT / "fuzz" / "corpus" / "runenv_fuzzer", ROOT / "fuzz" / "corpus" / "hedgeenv_fuzzer"),
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

    for p in list((ROOT / "include" / "hedgeenv").glob("*")):
        if "runenv" in p.name:
            p.rename(p.with_name(p.name.replace("runenv", "hedgeenv")))

    for p in list((ROOT / "src" / "hedgeenv").glob("*")):
        new_name = p.name.replace("runenv", "hedgeenv")
        new_name = new_name.replace("runloader", "hedgeloader")
        new_name = new_name.replace("require_stack", "fanout_stack")
        new_name = new_name.replace("require_ctx", "fanout_ctx")
        new_name = new_name.replace("runmap", "hedgemap")
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    for p in list((ROOT / "include" / "hedgecfg").glob("*")):
        if "launch" in p.name:
            p.rename(p.with_name(p.name.replace("launch", "hedge")))

    for p in list((ROOT / "fuzz" / "corpus" / "hedgeenv_fuzzer").glob("*")):
        if p.suffix == ".env":
            p.rename(p.with_suffix(".henv"))


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
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".henv", ".env",
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
    write(ROOT / "include" / "hedgecfg" / "hedge_policy.h", WINDOW_POLICY_H)
    write(ROOT / "include" / "hedgecfg" / "hedge_gate.h", WINDOW_BUCKET_H)
    write(ROOT / "include" / "hedgecfg" / "hedge_registry.h", HEDGE_REGISTRY_H)
    write(ROOT / "src" / "hedge_policy.c", HEDGE_POLICY_C)
    write(ROOT / "src" / "hedge_gate.c", HEDGE_GATE_C)
    write(ROOT / "src" / "hedge_registry.c", HEDGE_REGISTRY_C)
    write(ROOT / "fuzz" / "hedge_registry_fuzzer.c", HEDGE_REGISTRY_FUZZER)
    write(ROOT / "README.md", README)

    hdr = (ROOT / "include" / "hedgecfg" / "hedge_merge.h").read_text(encoding="utf-8")
    hdr = hdr.replace("LAYER_MERGE", "HEDGE_MERGE")
    (ROOT / "include" / "hedgecfg" / "hedge_merge.h").write_text(hdr, encoding="utf-8")

    fuzz = (ROOT / "fuzz" / "hedge_fuzzer.c").read_text(encoding="utf-8")
    fuzz = fuzz.replace(
        "hedgecfg_apply_hedgeenv_to_toml(toml, env);",
        "hedgecfg_apply_hedgeenv_to_toml(toml, env);\n"
        "  if (toml) {\n"
        "    hedge_registry_t trk;\n"
        "    hedge_registry_init(&trk);\n"
        "    hedgecfg_validate_hedge_manifest(toml, &trk);\n"
        "    (void)hedge_registry_finalize_digest(&trk);\n"
        "    hedge_registry_reset(&trk);\n"
        "  }",
    )
    fuzz = xform(fuzz)
    fuzz = fuzz.replace("#include \"hedgecfg/hedge_merge.h\"",
        "#include \"hedgecfg/hedge_merge.h\"\n#include \"hedgecfg/hedge_policy.h\"\n#include \"hedgecfg/hedge_registry.h\"")
    write(ROOT / "fuzz" / "hedge_fuzzer.c", fuzz)

    write(ROOT / "examples" / "hedge.toml", """[hedge]
name = "payments-api"
limit = 1000
hedge_after_ms = 60000
hedge_mode = "open"

[[hedge.endpoints]]
endpoint = "primary"
latency_budget_ms = 120

[[hedge.endpoints]]
endpoint = "backup-a"
latency_budget_ms = 80

[[hedge.endpoints]]
endpoint = "backup-b"
latency_budget_ms = 40
""")

    write(ROOT / "examples" / "hedge.runtime", """# Runtime hedging parameters for duplicate-request fanout
HEDGE_AFTER_MS=150
MAX_FANOUT=3
HEDGE_MODE=active
""")

    write(ROOT / "tests" / "test_hedge_policy.c", '''#include "hedgecfg/hedge_policy.h"
#include "hedgecfg/hedge_registry.h"
#include "tome/tome.h"
#include "unity/unity.h"

void test_hedge_policy_requires_name(void) {
  TomeDoc *doc = NULL;
  TomeError err;
  hedge_registry_t t;
  TEST_ASSERT_EQUAL(TOME_OK, tome_parse("[hedge]\\nname=\\"x\\"\\n", 20, &doc, &err));
  hedge_registry_init(&t);
  TEST_ASSERT_EQUAL(0, hedgecfg_validate_hedge_manifest(doc, &t));
  hedge_registry_reset(&t);
  tome_free(doc);
}
''')

    write(ROOT / "tests" / "test_hedge_registry.c", '''#include "hedgecfg/hedge_registry.h"
#include "unity/unity.h"

void test_hedge_registry_register(void) {
  hedge_registry_t t;
  hedge_registry_init(&t);
  TEST_ASSERT_EQUAL(0, hedge_registry_register(&t, "a", 100));
  TEST_ASSERT_EQUAL(0, hedge_registry_register(&t, "b", 200));
  hedge_registry_reset(&t);
}
''')


def plant_bugs() -> None:
    """Plant standard 5-bug set; bug3 is emergent hedge_registry UAF, not shallow hex OOB."""
    unesc = (ROOT / "src" / "hedgeenv" / "unescape.c").read_text(encoding="utf-8")
    unesc = unesc.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "hedgeenv" / "unescape.c").write_text(unesc, encoding="utf-8")

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
        "for f in hedgecfg hedge_merge; do",
        "for f in hedgecfg hedge_merge hedge_policy hedge_gate hedge_registry; do",
    )
    build_sh = build_sh.replace(
        "build_fuzzer hedge_fuzzer.c hedge_fuzzer",
        "build_fuzzer hedge_fuzzer.c hedge_fuzzer\n"
        "build_fuzzer hedge_registry_fuzzer.c hedge_registry_fuzzer",
    )
    build_sh = build_sh.replace("compile_runenv", "compile_hedgeenv")
    build_sh = build_sh.replace("src/runenv/", "src/hedgeenv/")
    build_sh = build_sh.replace('local obj="env_', 'local obj="henv_')
    build_sh = build_sh.replace("env_*.o", "henv_*.o")
    build_sh = build_sh.replace(
        "build_fuzzer runenv_fuzzer.c runenv_fuzzer",
        "build_fuzzer hedgeenv_fuzzer.c hedgeenv_fuzzer",
    )
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build_sh, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    wsl = wsl.replace("runenv_*.o toml_*.o launchcfg.o launch_merge.o",
                      "henv_*.o toml_*.o hedgecfg.o hedge_merge.o hedge_policy.o hedge_gate.o hedge_registry.o")
    (ROOT / "build" / "wsl_build.sh").write_text(wsl, encoding="utf-8")

    proj = (ROOT / ".clusterfuzzlite" / "project.yaml").read_text(encoding="utf-8")
    proj = xform(proj)
    if "hedge_registry_fuzzer" not in proj:
        proj = proj.replace(
            "- hedge_fuzzer",
            "- hedge_fuzzer\n  - hedge_registry_fuzzer",
        )
    (ROOT / ".clusterfuzzlite" / "project.yaml").write_text(proj, encoding="utf-8")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "crash-" not in gitignore:
        gitignore += "\ncrash-*\n/poc/\n"
    (ROOT / ".gitignore").write_text(gitignore, encoding="utf-8")

    write(ROOT / "fuzz" / "corpus" / "hedge_fuzzer" / "sample.bin",
          bytes([32]) + b"[hedge]\nname=\"api\"\nhedge_after_ms=100\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "hedge_registry_fuzzer" / "seed.bin", bytes(range(32, 96)))


def write_artifacts() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    tasks = """# hedgecfg task queue

GitHub: tolossamuel/hedgecfg

| # | Bug | Harness | Class | Status |
|---|-----|---------|-------|--------|
| 1 | hedgeenv entry realloc leak | hedgeenv_fuzzer | LeakSanitizer | Ready |
| 2 | toml audit key leak | toml_fuzzer | LeakSanitizer | Ready |
| 3 | hedge registry endpoint UAF | hedge_registry_fuzzer | heap-use-after-free | Ready |
| 4 | toml merge UAF | toml_merge_fuzzer | heap-use-after-free | Ready |
| 5 | toml format null deref | toml_format_fuzzer | null deref | Ready |

PoC bytes and patches: ../artifacts/hedgecfg/poc/ (not on GitHub).
"""
    write(ARTIFACTS / "TASKS.md", tasks)

    wsl_test = '''#!/bin/bash
set -eu
cd "$(dirname "$0")/../../hedgecfg"
ROOT="$PWD"
ARTIFACTS_ROOT="${ARTIFACTS_ROOT:-$(dirname "$ROOT")/artifacts/hedgecfg}"
POC="$ARTIFACTS_ROOT/poc/verified"
OUT=/tmp/hedgecfg_out
FAIL=0

if [ ! -d "$POC" ]; then
  echo "Missing PoC corpus: $POC" >&2
  exit 1
fi

if [ ! -x "$OUT/hedgeenv_fuzzer" ]; then
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

run_leak "Bug1 hedgeenv entry leak" "$OUT/hedgeenv_fuzzer" "$POC/entry_leak.henv"
run_leak "Bug2 toml audit leak" "$OUT/toml_fuzzer" "$POC/entry_leak.toml"
run_crash "Bug3 hedge registry UAF" "$OUT/hedge_registry_fuzzer" "$POC/registry_uaf.bin"
run_crash "Bug4 toml merge UAF" "$OUT/toml_merge_fuzzer" "$POC/merge_uaf.bin"
run_crash "Bug5 toml format null" "$OUT/toml_format_fuzzer" "$POC/empty_format.bin"
exit $FAIL
'''
    write(ARTIFACTS / "wsl_test_pocs.sh", wsl_test)
    (ARTIFACTS / "wsl_test_pocs.sh").chmod(0o755)


def generate_pocs_and_patches() -> None:
    """Build, capture golden PoCs, and emit git patches into artifacts/."""
    poc_dir = ARTIFACTS / "poc" / "verified"
    submit_dir = ARTIFACTS / "poc" / "submit"
    poc_dir.mkdir(parents=True, exist_ok=True)
    submit_dir.mkdir(parents=True, exist_ok=True)

    subprocess.check_call(["bash", "build/wsl_build.sh"], cwd=ROOT)
    out = Path("/tmp/hedgecfg_out")

    write(poc_dir / "entry_leak.henv", "HEDGE_KEY=1\n")
    write(poc_dir / "entry_leak.toml", 'k = "v"\n')
    write(poc_dir / "empty_format.bin", b"")
    shutil.copy2(
        Path("/home/samuel/Documents/fenrir3/artifacts/throttlecfg/poc/verified/merge_uaf.bin"),
        poc_dir / "merge_uaf.bin",
    )
    shutil.copy2(
        Path("/home/samuel/Documents/fenrir3/artifacts/throttlecfg/poc/verified/tracker_uaf.bin"),
        poc_dir / "registry_uaf.bin",
    )

    patches = [
        ("bug1_hedgeenv_entry_leak.patch", "src/hedgeenv/store.c",
         lambda t: t.replace(
             "  hedgeenv_doc_impl_t *d = (hedgeenv_doc_impl_t *)doc;\n  hedgeenv_arena_free",
             "  hedgeenv_doc_impl_t *d = (hedgeenv_doc_impl_t *)doc;\n  free(d->entries);\n  hedgeenv_arena_free",
         )),
        ("bug2_toml_audit_leak.patch", "src/toml/parser.c",
         lambda t: t.replace(
             """void tome_free(TomeDoc *doc) {
    if (doc == NULL) {
        return;
    }
    tome_table_free(doc->root);
    tome_free_ptr(doc);
}""",
             """void tome_free(TomeDoc *doc) {
    size_t i;
    if (doc == NULL) {
        return;
    }
    for (i = 0; i < doc->audit_count; i++) {
        tome_free_ptr(doc->audit_keys[i]);
    }
    tome_free_ptr(doc->audit_keys);
    tome_table_free(doc->root);
    tome_free_ptr(doc);
}""",
         )),
        ("bug3_hedge_registry_uaf.patch", "src/hedge_registry.c",
         lambda t: t.replace(
             "  free(t->slots);\n  free(t->pending_refs);",
             "  free(t->slots);\n  for (i = 0; i < t->pending_count; i++) {\n    free((void *)t->pending_refs[i]);\n  }\n  free(t->pending_refs);",
         ).replace(
             "        t->pending_refs[t->pending_count++] = t->slots[i].label;",
             "        char *snap = strdup(t->slots[i].label ? t->slots[i].label : \"\");\n        if (!snap) {\n          return -1;\n        }\n        t->pending_refs[t->pending_count++] = snap;",
         )),
        ("bug4_toml_merge_uaf.patch", "src/toml/merge.c",
         lambda t: t.replace(
             "    TomeTable *overlay_mut = (TomeTable *)overlay;",
             "    (void)overlay;",
         ).replace(
             "        if (i > 0 && overlay->count > 3 && (i % 2) == 0) {\n            tome_table_rebuild_index(overlay_mut);\n        }\n\n        ",
             "        ",
         ).replace(
             "        const TomeEntry *overlay_entry = &overlay->entries[i];\n        const char *cached_key = overlay_entry->key;\n        TomeValue *existing",
             "        const TomeEntry *overlay_entry = &overlay->entries[i];\n        TomeValue *existing",
         ).replace(
             "        if (!path_push_key(ctx, cached_key, &restore_len)) {",
             "        if (!path_push_key(ctx, overlay_entry->key, &restore_len)) {",
         )),
        ("bug5_toml_format_null_deref.patch", "src/toml/format.c",
         lambda t: t.replace(
             "    if (ctx.out.length == 0 && ctx.out.data == NULL) {\n        char *snapshot = tome_alloc(1);\n        if (snapshot != NULL) {\n            memcpy(snapshot, ctx.out.data, ctx.out.length + 1);\n            tome_free_ptr(snapshot);\n        }\n    }\n    ",
             "",
         )),
    ]

    for patch_name, rel_path, fix_fn in patches:
        path = ROOT / rel_path
        original = path.read_text(encoding="utf-8")
        fixed = fix_fn(original)
        if fixed == original:
            print(f"WARN: no change for {patch_name}")
        path.write_text(fixed, encoding="utf-8")
        diff = subprocess.check_output(
            ["git", "diff", rel_path], cwd=ROOT, text=True
        )
        (submit_dir / patch_name).write_text(diff, encoding="utf-8")
        path.write_text(original, encoding="utf-8")

    descriptions = {
        "bug1_TASK_DESCRIPTION.txt": (
            "A memory leak occurs when parsing a hedgeenv assignment: hedgeenv_set_entry "
            "reallocates internal entry storage, but that heap memory is not freed when "
            "hedgeenv_doc_destroy runs in src/hedgeenv/store.c."
        ),
        "bug2_TASK_DESCRIPTION.txt": (
            "A memory leak occurs in tome_free in src/toml/parser.c when TOML parsing records "
            "table-header audit keys: doc_audit_key heap-allocates key copies that are never "
            "released when the document is destroyed."
        ),
        "bug3_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in hedge_registry_finalize_digest in src/hedge_registry.c "
            "when FNV digest finalization reads endpoint label bytes through pending references "
            "registered before hedge_registry_compact reallocates and frees the original label "
            "storage during multi-endpoint registration in the hedge registry pipeline, triggered "
            "via hedge_registry_fuzzer."
        ),
        "bug4_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in merge_table_in_place in src/toml/merge.c when overlay "
            "table index rebuild invalidates cached entry key pointers during multi-table TOML "
            "document merge, triggered via toml_merge_fuzzer."
        ),
        "bug5_TASK_DESCRIPTION.txt": (
            "A null pointer dereference occurs in tome_format_document in src/toml/format.c when "
            "formatting an empty document causes memcpy to read through a NULL output buffer, "
            "triggered via toml_format_fuzzer."
        ),
    }
    for name, text in descriptions.items():
        write(submit_dir / name, text + "\n")

    subprocess.check_call(["bash", str(ARTIFACTS / "wsl_test_pocs.sh")])


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
    generate_pocs_and_patches()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
