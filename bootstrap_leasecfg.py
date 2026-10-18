#!/usr/bin/env python3
"""Bootstrap leasecfg — TOML distributed lease coordination manifests + leaseenv runtime overlays."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/leasecfg")
SRC = Path("/home/samuel/Documents/fenrir3/hedgecfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/leasecfg")

TEXT_RENAME = [
    ("hedgeenv_doc_impl_t", "leaseenv_doc_impl_t"),
    ("hedgeenv_doc_t", "leaseenv_doc_t"),
    ("hedgeenv_error_t", "leaseenv_error_t"),
    ("hedgeenv_options_t", "leaseenv_options_t"),
    ("hedgeenv_entry_t", "leaseenv_entry_t"),
    ("hedgeenv_slice_t", "leaseenv_slice_t"),
    ("hedgeenv_arena_t", "leaseenv_arena_t"),
    ("hedgeenv_token_kind_t", "leaseenv_token_kind_t"),
    ("hedgeenv_token_t", "leaseenv_token_t"),
    ("hedgeenv_internal.h", "leaseenv_internal.h"),
    ("hedgeenv/hedgeenv_types.h", "leaseenv/leaseenv_types.h"),
    ("include/hedgeenv", "include/leaseenv"),
    ("src/hedgeenv/", "src/leaseenv/"),
    ("src/hedgeenv", "src/leaseenv"),
    ("hedgeenv_", "leaseenv_"),
    ("HEDGEENV_", "LEASEENV_"),
    ("Hedgeenv", "Leaseenv"),
    ("hedgeenv", "leaseenv"),
    ("hedge_registry_fuzzer", "lease_registry_fuzzer"),
    ("hedge_registry_finalize_digest", "lease_registry_finalize_digest"),
    ("hedge_registry_compact", "lease_registry_compact"),
    ("hedge_registry_register", "lease_registry_register"),
    ("hedge_registry_reset", "lease_registry_reset"),
    ("hedge_registry_init", "lease_registry_init"),
    ("hedge_registry_t", "lease_registry_t"),
    ("hedge_registry", "lease_registry"),
    ("hedge_endpoint_t", "lease_holder_t"),
    ("hedgecfg_validate_hedge_manifest", "leasecfg_validate_lease_manifest"),
    ("hedge_gate_allows", "lease_gate_allows"),
    ("hedge_gate", "lease_gate"),
    ("hedge_policy", "lease_policy"),
    ("hedge_fuzzer", "lease_fuzzer"),
    ("hedge_merge", "lease_merge"),
    ("hedgecfg", "leasecfg"),
    ("HedgeCfg", "LeaseCfg"),
    ("HEDGECFG", "LEASECFG"),
    ("fanout_stack", "renewal_stack"),
    ("fanout_ctx", "renewal_ctx"),
    ("@hedge", "@lease"),
    ("hedgemap", "leasemap"),
    ("hedgeloader", "leaseloader"),
    ("apply_hedgeenv_overlay", "apply_leaseenv_overlay"),
    ("apply_hedgeenv_to_toml", "apply_leaseenv_to_toml"),
    ("load_hedgeenv_memory", "load_leaseenv_memory"),
    ("hedgecfg_hedgeenv_free", "leasecfg_leaseenv_free"),
    ("/tmp/hedgecfg_out", "/tmp/leasecfg_out"),
    ("tolossamuel/hedgecfg", "tolossamuel/leasecfg"),
    ("compile_hedgeenv", "compile_leaseenv"),
    ("henv_", "lenv_"),
    ("hedge.runtime", "lease.runtime"),
    ("hedge.toml", "lease.toml"),
    ("HTTP request hedging policy", "distributed lease coordination policy"),
    ("HTTP request hedging", "distributed lease coordination"),
    ("hedgeenv runtime rate-limit parameter overlays", "leaseenv runtime TTL and renewal parameter overlays"),
    ("Hedgeenv layer", "Leaseenv layer"),
    ("Hedge policy validation", "Lease policy validation"),
    ("[hedge]", "[lease]"),
    ("hedge_after_ms", "renew_interval_ms"),
    ("latency_budget_ms", "ttl_ms"),
    ("endpoints", "holders"),
    ("endpoint", "holder"),
    ("HEDGE_KEY", "LEASE_KEY"),
    (".henv", ".lenv"),
    ("HEDGE_AFTER_MS", "RENEW_INTERVAL_MS"),
    ("MAX_FANOUT", "MAX_HOLDERS"),
    ("HEDGE_MODE", "LEASE_MODE"),
    ("hedge_mode", "lease_mode"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add leasecfg public headers", [
        "include/leasecfg/leasecfg.h", "include/leasecfg/lease_merge.h"]),
    ("include: add leaseenv public API", [
        "include/leaseenv/leaseenv.h", "include/leaseenv/leaseenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add lease policy gate registry headers", [
        "include/leasecfg/lease_policy.h", "include/leasecfg/lease_gate.h",
        "include/leasecfg/lease_registry.h"]),
    ("src/leaseenv: add buffer and string utilities", [
        "src/leaseenv/buffer.c", "src/leaseenv/buffer.h", "src/leaseenv/strutil.c",
        "src/leaseenv/strutil.h"]),
    ("src/leaseenv: add arena allocator", [
        "src/leaseenv/arena.c", "src/leaseenv/arena.h", "src/leaseenv/leaseenv_internal.h"]),
    ("src/leaseenv: add error helpers", ["src/leaseenv/error.c", "src/leaseenv/error.h"]),
    ("src/leaseenv: add UTF-8 validation", ["src/leaseenv/utf8.c", "src/leaseenv/utf8.h"]),
    ("src/leaseenv: implement leaseenv line lexer", ["src/leaseenv/lexer.c", "src/leaseenv/lexer.h"]),
    ("src/leaseenv: add quoted value unescape", ["src/leaseenv/unescape.c", "src/leaseenv/unescape.h"]),
    ("src/leaseenv: add document store", ["src/leaseenv/store.c", "src/leaseenv/store.h"]),
    ("src/leaseenv: wire assignment parser", ["src/leaseenv/parser.c", "src/leaseenv/parser.h"]),
    ("src/leaseenv: add serialize to leaseenv text", ["src/leaseenv/serialize.c", "src/leaseenv/serialize.h"]),
    ("src/leaseenv: add validation pass", ["src/leaseenv/validate.c", "src/leaseenv/validate.h"]),
    ("src/leaseenv: add merge overlay", ["src/leaseenv/merge.c", "src/leaseenv/merge.h"]),
    ("src/leaseenv: add expand and coerce", [
        "src/leaseenv/expand.c", "src/leaseenv/expand.h", "src/leaseenv/coerce.c",
        "src/leaseenv/coerce.h"]),
    ("src/leaseenv: add walk query diff", [
        "src/leaseenv/walk.c", "src/leaseenv/walk.h", "src/leaseenv/query.c",
        "src/leaseenv/query.h", "src/leaseenv/diff.c", "src/leaseenv/diff.h"]),
    ("src/leaseenv: add pretty printer", ["src/leaseenv/pretty.c", "src/leaseenv/pretty.h"]),
    ("src/leaseenv: add include stack and ctx", [
        "src/leaseenv/renewal_stack.c", "src/leaseenv/renewal_stack.h",
        "src/leaseenv/renewal_ctx.c", "src/leaseenv/renewal_ctx.h"]),
    ("src/leaseenv: add path filter profile", [
        "src/leaseenv/path.c", "src/leaseenv/path.h", "src/leaseenv/filter.c",
        "src/leaseenv/filter.h", "src/leaseenv/profile.c", "src/leaseenv/profile.h"]),
    ("src/leaseenv: add snapshot readutil strict canonical", [
        "src/leaseenv/snapshot.c", "src/leaseenv/snapshot.h", "src/leaseenv/readutil.c",
        "src/leaseenv/readutil.h", "src/leaseenv/strict.c", "src/leaseenv/strict.h",
        "src/leaseenv/canonical.c", "src/leaseenv/canonical.h"]),
    ("src/leaseenv: add leaseloader and main leaseenv module", [
        "src/leaseenv/leaseloader.c", "src/leaseenv/leaseenv.c", "src/leaseenv/leasemap.c",
        "src/leaseenv/leasemap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.c", "src/toml/buffer.c"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.c", "src/toml/datetime.c", "src/toml/lexer.c"]),
    ("src/toml: add value and parser core", ["src/toml/value.c", "src/toml/parser.c"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.c", "src/toml/merge.c", "src/toml/serialize.c"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.c", "src/toml/format.c", "src/toml/validator.c", "src/toml/document.c"]),
    ("src: add leasecfg bridge and leaseenv-to-toml merge", ["src/leasecfg.c", "src/lease_merge.c"]),
    ("src: add window policy validator", ["src/lease_policy.c"]),
    ("src: add latency budget gate evaluator", ["src/lease_gate.c"]),
    ("src: add lease holder registry with compaction", ["src/lease_registry.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add lease policy and registry unit tests", [
        "tests/test_lease_policy.c", "tests/test_lease_registry.c"]),
    ("examples: add TOML lease manifest and runtime overlay", [
        "examples/lease.toml", "examples/lease.runtime"]),
    ("fuzz: add leaseenv_fuzzer harness", ["fuzz/leaseenv_fuzzer.c"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.c"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.c"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.c"]),
    ("fuzz: add lease_fuzzer for cross-format overlay", ["fuzz/lease_fuzzer.c"]),
    ("fuzz: add lease_registry_fuzzer for slot compaction path", ["fuzz/lease_registry_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/leaseenv_fuzzer/minimal.lenv",
        "fuzz/corpus/leaseenv_fuzzer/quoted.lenv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/lease_fuzzer/sample.bin",
        "fuzz/corpus/lease_registry_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for leasecfg library", ["README.md"]),
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


HEDGE_POLICY_C = '''#include "leasecfg/lease_policy.h"
#include "leasecfg/lease_registry.h"
#include "tome/tome.h"
#include "tome/parser.h"
#include "tome/value.h"

#include <string.h>

int leasecfg_validate_lease_manifest(const TomeDoc *doc, lease_registry_t *trk) {
  TomeValue *root;
  TomeTable *tbl;
  size_t i;

  if (!doc || !doc->root) {
    return -1;
  }
  root = tome_table_get(doc->root, "lease");
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
    TomeValue *slots = tome_table_get(tbl, "holders");
    if (slots && slots->type == TOME_VAL_ARRAY) {
      TomeArray *arr = slots->as.array;
      for (i = 0; i < arr->count; i++) {
        TomeValue *item = &arr->items[i];
        if (item->type == TOME_VAL_TABLE) {
          TomeValue *label = tome_table_get(item->as.table, "holder");
          TomeValue *label2 = tome_table_get(item->as.table, "ttl_ms");
          const char *l = (label && label->type == TOME_VAL_STRING) ? label->as.string : "holder";
          uint32_t budget = 100;
          if (label2 && label2->type == TOME_VAL_INTEGER) {
            budget = (uint32_t)label2->as.integer;
          }
          lease_registry_register(trk, l, budget);
        }
      }
    }
  }
  return 0;
}
'''

WINDOW_POLICY_H = '''#ifndef LEASECFG_LEASE_POLICY_H
#define LEASECFG_LEASE_POLICY_H

#include "leasecfg/lease_registry.h"
#include "tome/tome.h"

#ifdef __cplusplus
extern "C" {
#endif

int leasecfg_validate_lease_manifest(const TomeDoc *doc, lease_registry_t *trk);

#ifdef __cplusplus
}
#endif

#endif
'''

HEDGE_GATE_C = '''#include "leasecfg/lease_gate.h"

#include <string.h>

int lease_gate_allows(const char *state, uint32_t tokens, uint32_t capacity) {
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

WINDOW_BUCKET_H = '''#ifndef LEASECFG_LEASE_GATE_H
#define LEASECFG_LEASE_GATE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

int lease_gate_allows(const char *state, uint32_t tokens, uint32_t capacity);

#ifdef __cplusplus
}
#endif

#endif
'''

HEDGE_REGISTRY_C = '''#include "leasecfg/lease_registry.h"

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

void lease_registry_init(lease_registry_t *t) {
  if (!t) {
    return;
  }
  memset(t, 0, sizeof(*t));
}

void lease_registry_reset(lease_registry_t *t) {
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

static int grow_slots(lease_registry_t *t) {
  size_t cap = t->slot_cap ? t->slot_cap * 2 : 8;
  lease_holder_t *next = (lease_holder_t *)realloc(t->slots, cap * sizeof(*next));
  if (!next) {
    return -1;
  }
  t->slots = next;
  t->slot_cap = cap;
  return 0;
}

int lease_registry_register(lease_registry_t *t, const char *label, uint32_t budget) {
  lease_holder_t *slot;
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
  slot->ttl_ms = budget;

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
      lease_registry_compact(t);
    }
  }
  return 0;
}

void lease_registry_compact(lease_registry_t *t) {
  size_t i;
  size_t dst = 0;
  lease_holder_t *next;

  if (!t || t->slot_count < 2) {
    return;
  }
  next = (lease_holder_t *)calloc(t->slot_count, sizeof(*next));
  if (!next) {
    return;
  }
  for (i = 0; i < t->slot_count; i++) {
    if (t->slots[i].ttl_ms > 0) {
      char *fresh = strdup(t->slots[i].label ? t->slots[i].label : "");
      next[dst].label = fresh;
      next[dst].ttl_ms = t->slots[i].ttl_ms;
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

uint32_t lease_registry_finalize_digest(lease_registry_t *t) {
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

HEDGE_REGISTRY_H = '''#ifndef LEASECFG_LEASE_REGISTRY_H
#define LEASECFG_LEASE_REGISTRY_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  char *label;
  uint32_t ttl_ms;
} lease_holder_t;

typedef struct {
  lease_holder_t *slots;
  size_t slot_count;
  size_t slot_cap;
  const char **pending_refs;
  size_t pending_count;
  uint32_t digest;
} lease_registry_t;

void lease_registry_init(lease_registry_t *t);
void lease_registry_reset(lease_registry_t *t);
int lease_registry_register(lease_registry_t *t, const char *label, uint32_t budget);
void lease_registry_compact(lease_registry_t *t);
uint32_t lease_registry_finalize_digest(lease_registry_t *t);

#ifdef __cplusplus
}
#endif

#endif
'''

HEDGE_REGISTRY_FUZZER = '''#include "leasecfg/lease_registry.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  lease_registry_t t;
  size_t i;
  char label[32];

  if (!data || size == 0 || size > 4096) {
    return 0;
  }
  lease_registry_init(&t);
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
    lease_registry_register(&t, label, (uint32_t)(data[i] + 1));
    i += n > 0 ? n - 1 : 0;
  }
  (void)lease_registry_finalize_digest(&t);
  lease_registry_reset(&t);
  return 0;
}
'''

README = """# leasecfg

leasecfg is a C11 library for distributed lease coordination policy configuration: parse TOML lease manifests, load leaseenv runtime TTL and renewal parameter overlays, merge layers, validate holder TTL budgets, and track lease holder registry during distributed coordination.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Leaseenv layer** — `KEY=VALUE`, `@lease` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply leaseenv overlay keys onto parsed TOML documents
- **Hedge policy** — validate `[lease]` tables and register slot limits into a compaction tracker
- **Latency gate** — gate request admission on bucket state and capacity
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `leaseenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `lease_fuzzer`, `lease_registry_fuzzer`.

## Quick start

```c
#include "leasecfg/leasecfg.h"

TomeDoc *toml = NULL;
TomeError err;
leasecfg_load_toml_memory("[lease]\\nname = \\"api\\"\\nmax_holders = 1000\\n", 38, &toml, &err);

leaseenv_doc_t *env = NULL;
leasecfg_load_leaseenv_memory("LIMIT=500\\n", 10, NULL, &env, NULL);
leasecfg_apply_leaseenv_to_toml(toml, env);

leasecfg_leaseenv_free(env);
leasecfg_toml_free(toml);
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
        (ROOT / "include" / "hedgecfg", ROOT / "include" / "leasecfg"),
        (ROOT / "include" / "hedgeenv", ROOT / "include" / "leaseenv"),
        (ROOT / "src" / "hedgeenv", ROOT / "src" / "leaseenv"),
        (ROOT / "src" / "hedgecfg.c", ROOT / "src" / "leasecfg.c"),
        (ROOT / "src" / "hedge_merge.c", ROOT / "src" / "lease_merge.c"),
        (ROOT / "src" / "hedge_policy.c", ROOT / "src" / "lease_policy.c"),
        (ROOT / "src" / "hedge_gate.c", ROOT / "src" / "lease_gate.c"),
        (ROOT / "src" / "hedge_registry.c", ROOT / "src" / "lease_registry.c"),
        (ROOT / "fuzz" / "hedgeenv_fuzzer.c", ROOT / "fuzz" / "leaseenv_fuzzer.c"),
        (ROOT / "fuzz" / "hedge_fuzzer.c", ROOT / "fuzz" / "lease_fuzzer.c"),
        (ROOT / "fuzz" / "hedge_registry_fuzzer.c", ROOT / "fuzz" / "lease_registry_fuzzer.c"),
        (ROOT / "examples" / "hedge.toml", ROOT / "examples" / "lease.toml"),
        (ROOT / "examples" / "hedge.runtime", ROOT / "examples" / "lease.runtime"),
        (ROOT / "fuzz" / "corpus" / "hedgeenv_fuzzer", ROOT / "fuzz" / "corpus" / "leaseenv_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "hedge_fuzzer", ROOT / "fuzz" / "corpus" / "lease_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "hedge_registry_fuzzer", ROOT / "fuzz" / "corpus" / "lease_registry_fuzzer"),
        (ROOT / "tests" / "test_hedge_policy.c", ROOT / "tests" / "test_lease_policy.c"),
        (ROOT / "tests" / "test_hedge_registry.c", ROOT / "tests" / "test_lease_registry.c"),
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

    for p in list((ROOT / "include" / "leaseenv").glob("*")):
        if "hedgeenv" in p.name:
            p.rename(p.with_name(p.name.replace("hedgeenv", "leaseenv")))

    for p in list((ROOT / "src" / "leaseenv").glob("*")):
        new_name = p.name.replace("hedgeenv", "leaseenv")
        new_name = new_name.replace("hedgeloader", "leaseloader")
        new_name = new_name.replace("fanout_stack", "renewal_stack")
        new_name = new_name.replace("fanout_ctx", "renewal_ctx")
        new_name = new_name.replace("hedgemap", "leasemap")
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    for p in list((ROOT / "include" / "leasecfg").glob("*")):
        if "hedge" in p.name:
            p.rename(p.with_name(p.name.replace("hedge", "lease")))

    for p in list((ROOT / "fuzz" / "corpus" / "leaseenv_fuzzer").glob("*")):
        if p.suffix == ".henv":
            p.rename(p.with_suffix(".lenv"))


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
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".lenv", ".env",
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
    write(ROOT / "include" / "leasecfg" / "lease_policy.h", WINDOW_POLICY_H)
    write(ROOT / "include" / "leasecfg" / "lease_gate.h", WINDOW_BUCKET_H)
    write(ROOT / "include" / "leasecfg" / "lease_registry.h", HEDGE_REGISTRY_H)
    write(ROOT / "src" / "lease_policy.c", HEDGE_POLICY_C)
    write(ROOT / "src" / "lease_gate.c", HEDGE_GATE_C)
    write(ROOT / "src" / "lease_registry.c", HEDGE_REGISTRY_C)
    write(ROOT / "fuzz" / "lease_registry_fuzzer.c", HEDGE_REGISTRY_FUZZER)
    write(ROOT / "README.md", README)

    hdr = (ROOT / "include" / "leasecfg" / "lease_merge.h").read_text(encoding="utf-8")
    hdr = hdr.replace("HEDGE_MERGE", "LEASE_MERGE")
    (ROOT / "include" / "leasecfg" / "lease_merge.h").write_text(hdr, encoding="utf-8")

    fuzz = (ROOT / "fuzz" / "lease_fuzzer.c").read_text(encoding="utf-8")
    fuzz = fuzz.replace(
        "leasecfg_apply_leaseenv_to_toml(toml, env);",
        "leasecfg_apply_leaseenv_to_toml(toml, env);\n"
        "  if (toml) {\n"
        "    lease_registry_t trk;\n"
        "    lease_registry_init(&trk);\n"
        "    leasecfg_validate_lease_manifest(toml, &trk);\n"
        "    (void)lease_registry_finalize_digest(&trk);\n"
        "    lease_registry_reset(&trk);\n"
        "  }",
    )
    fuzz = xform(fuzz)
    fuzz = fuzz.replace("#include \"leasecfg/lease_merge.h\"",
        "#include \"leasecfg/lease_merge.h\"\n#include \"leasecfg/lease_policy.h\"\n#include \"leasecfg/lease_registry.h\"")
    write(ROOT / "fuzz" / "lease_fuzzer.c", fuzz)

    write(ROOT / "examples" / "lease.toml", """[lease]
name = "coordination-svc"
max_holders = 1000
renew_interval_ms = 60000
lease_mode = "open"

[[lease.holders]]
holder = "node-a"
ttl_ms = 120

[[lease.holders]]
holder = "node-b"
ttl_ms = 80

[[lease.holders]]
holder = "node-c"
ttl_ms = 40
""")

    write(ROOT / "examples" / "lease.runtime", """# Runtime lease renewal parameters for distributed coordination
RENEW_INTERVAL_MS=150
MAX_HOLDERS=3
LEASE_MODE=active
""")

    write(ROOT / "tests" / "test_lease_policy.c", '''#include "leasecfg/lease_policy.h"
#include "leasecfg/lease_registry.h"
#include "tome/tome.h"
#include "unity/unity.h"

void test_lease_policy_requires_name(void) {
  TomeDoc *doc = NULL;
  TomeError err;
  lease_registry_t t;
  TEST_ASSERT_EQUAL(TOME_OK, tome_parse("[lease]\\nname=\\"x\\"\\n", 20, &doc, &err));
  lease_registry_init(&t);
  TEST_ASSERT_EQUAL(0, leasecfg_validate_lease_manifest(doc, &t));
  lease_registry_reset(&t);
  tome_free(doc);
}
''')

    write(ROOT / "tests" / "test_lease_registry.c", '''#include "leasecfg/lease_registry.h"
#include "unity/unity.h"

void test_lease_registry_register(void) {
  lease_registry_t t;
  lease_registry_init(&t);
  TEST_ASSERT_EQUAL(0, lease_registry_register(&t, "a", 100));
  TEST_ASSERT_EQUAL(0, lease_registry_register(&t, "b", 200));
  lease_registry_reset(&t);
}
''')


def plant_bugs() -> None:
    """Plant standard 5-bug set; bug3 is emergent lease_registry UAF, not shallow hex OOB."""
    unesc = (ROOT / "src" / "leaseenv" / "unescape.c").read_text(encoding="utf-8")
    unesc = unesc.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "leaseenv" / "unescape.c").write_text(unesc, encoding="utf-8")

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
        "for f in leasecfg lease_merge; do",
        "for f in leasecfg lease_merge lease_policy lease_gate lease_registry; do",
    )
    build_sh = build_sh.replace(
        "build_fuzzer lease_fuzzer.c lease_fuzzer",
        "build_fuzzer lease_fuzzer.c lease_fuzzer\n"
        "build_fuzzer lease_registry_fuzzer.c lease_registry_fuzzer",
    )
    build_sh = build_sh.replace("compile_runenv", "compile_leaseenv")
    build_sh = build_sh.replace("src/runenv/", "src/leaseenv/")
    build_sh = build_sh.replace('local obj="env_', 'local obj="lenv_')
    build_sh = build_sh.replace("env_*.o", "lenv_*.o")
    build_sh = build_sh.replace(
        "build_fuzzer runenv_fuzzer.c runenv_fuzzer",
        "build_fuzzer leaseenv_fuzzer.c leaseenv_fuzzer",
    )
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build_sh, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    wsl = wsl.replace("hedgeenv_*.o toml_*.o hedgecfg.o hedge_merge.o",
                      "leaseenv_*.o toml_*.o leasecfg.o lease_merge.o lease_policy.o lease_gate.o lease_registry.o")
    wsl = wsl.replace("/tmp/hedgecfg_out", "/tmp/leasecfg_out")
    (ROOT / "build" / "wsl_build.sh").write_text(wsl, encoding="utf-8")

    proj = (ROOT / ".clusterfuzzlite" / "project.yaml").read_text(encoding="utf-8")
    proj = xform(proj)
    if "lease_registry_fuzzer" not in proj:
        proj = proj.replace(
            "- lease_fuzzer",
            "- lease_fuzzer\n  - lease_registry_fuzzer",
        )
    (ROOT / ".clusterfuzzlite" / "project.yaml").write_text(proj, encoding="utf-8")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "crash-" not in gitignore:
        gitignore += "\ncrash-*\n/poc/\n"
    (ROOT / ".gitignore").write_text(gitignore, encoding="utf-8")

    write(ROOT / "fuzz" / "corpus" / "lease_fuzzer" / "sample.bin",
          bytes([32]) + b"[lease]\nname=\"api\"\nrenew_interval_ms=100\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "lease_registry_fuzzer" / "seed.bin", bytes(range(32, 96)))


def write_artifacts() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    tasks = """# leasecfg task queue

GitHub: tolossamuel/leasecfg

| # | Bug | Harness | Class | Status |
|---|-----|---------|-------|--------|
| 1 | leaseenv entry realloc leak | leaseenv_fuzzer | LeakSanitizer | Ready |
| 2 | toml audit key leak | toml_fuzzer | LeakSanitizer | Ready |
| 3 | lease registry holder UAF | lease_registry_fuzzer | heap-use-after-free | Ready |
| 4 | toml merge UAF | toml_merge_fuzzer | heap-use-after-free | Ready |
| 5 | toml format null deref | toml_format_fuzzer | null deref | Ready |

PoC bytes and patches: ../artifacts/leasecfg/poc/ (not on GitHub).
"""
    write(ARTIFACTS / "TASKS.md", tasks)

    wsl_test = '''#!/bin/bash
set -eu
cd "$(dirname "$0")/../../leasecfg"
ROOT="$PWD"
ARTIFACTS_ROOT="${ARTIFACTS_ROOT:-$(dirname "$ROOT")/artifacts/leasecfg}"
POC="$ARTIFACTS_ROOT/poc/verified"
OUT=/tmp/leasecfg_out
FAIL=0

if [ ! -d "$POC" ]; then
  echo "Missing PoC corpus: $POC" >&2
  exit 1
fi

if [ ! -x "$OUT/leaseenv_fuzzer" ]; then
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

run_leak "Bug1 leaseenv entry leak" "$OUT/leaseenv_fuzzer" "$POC/entry_leak.lenv"
run_leak "Bug2 toml audit leak" "$OUT/toml_fuzzer" "$POC/entry_leak.toml"
run_crash "Bug3 lease registry UAF" "$OUT/lease_registry_fuzzer" "$POC/registry_uaf.bin"
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
    out = Path("/tmp/leasecfg_out")

    write(poc_dir / "entry_leak.lenv", "LEASE_KEY=1\n")
    write(poc_dir / "entry_leak.toml", 'k = "v"\n')
    write(poc_dir / "empty_format.bin", b"")
    shutil.copy2(
        Path("/home/samuel/Documents/fenrir3/artifacts/throttlecfg/poc/verified/merge_uaf.bin"),
        poc_dir / "merge_uaf.bin",
    )
    shutil.copy2(
        Path("/home/samuel/Documents/fenrir3/artifacts/hedgecfg/poc/verified/registry_uaf.bin"),
        poc_dir / "registry_uaf.bin",
    )

    patches = [
        ("bug1_leaseenv_entry_leak.patch", "src/leaseenv/store.c",
         lambda t: t.replace(
             "  leaseenv_doc_impl_t *d = (leaseenv_doc_impl_t *)doc;\n  leaseenv_arena_free",
             "  leaseenv_doc_impl_t *d = (leaseenv_doc_impl_t *)doc;\n  free(d->entries);\n  leaseenv_arena_free",
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
        ("bug3_lease_registry_uaf.patch", "src/lease_registry.c",
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
            "A memory leak occurs when parsing a leaseenv assignment: leaseenv_set_entry "
            "reallocates internal entry storage, but that heap memory is not freed when "
            "leaseenv_doc_destroy runs in src/leaseenv/store.c."
        ),
        "bug2_TASK_DESCRIPTION.txt": (
            "A memory leak occurs in tome_free in src/toml/parser.c when TOML parsing records "
            "table-header audit keys: doc_audit_key heap-allocates key copies that are never "
            "released when the document is destroyed."
        ),
        "bug3_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in lease_registry_finalize_digest in src/lease_registry.c "
            "when FNV digest finalization reads holder label bytes through pending references "
            "registered before lease_registry_compact reallocates and frees the original label "
            "storage during multi-holder registration in the lease registry pipeline, triggered "
            "via lease_registry_fuzzer."
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
