#!/usr/bin/env python3
"""Bootstrap backoffcfg — TOML retry/backoff manifests + backoffenv runtime overlays."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/backoffcfg")
SRC = Path("/home/samuel/Documents/fenrir3/launchcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/backoffcfg")

TEXT_RENAME = [
    ("runenv_doc_impl_t", "backoffenv_doc_impl_t"),
    ("runenv_doc_t", "backoffenv_doc_t"),
    ("runenv_error_t", "backoffenv_error_t"),
    ("runenv_options_t", "backoffenv_options_t"),
    ("runenv_entry_t", "backoffenv_entry_t"),
    ("runenv_slice_t", "backoffenv_slice_t"),
    ("runenv_arena_t", "backoffenv_arena_t"),
    ("runenv_token_kind_t", "backoffenv_token_kind_t"),
    ("runenv_token_t", "backoffenv_token_t"),
    ("runenv_internal.h", "backoffenv_internal.h"),
    ("backoffenv/backoffenv_types.h", "backoffenv/backoffenv_types.h"),
    ("runenv/runenv_types.h", "backoffenv/backoffenv_types.h"),
    ("runenv/runenv.h", "backoffenv/backoffenv.h"),
    ("include/runenv", "include/backoffenv"),
    ("src/runenv/", "src/backoffenv/"),
    ("src/runenv", "src/backoffenv"),
    ("runenv_", "backoffenv_"),
    ("RUNENV_", "BACKOFFENV_"),
    ("Runenv", "Backoffenv"),
    ("runenv", "backoffenv"),
    ("launch_merge", "backoff_merge"),
    ("launch_fuzzer", "backoff_fuzzer"),
    ("launch_service", "backoff_policy"),
    ("launchcfg", "backoffcfg"),
    ("LaunchCfg", "BackoffCfg"),
    ("LAUNCHCFG", "BACKOFFCFG"),
    ("require_stack", "retry_stack"),
    ("require_ctx", "retry_ctx"),
    ("@require", "@retry"),
    ("runmap", "backoffmap"),
    ("runloader", "backoffloader"),
    ("apply_runenv_overlay", "apply_backoffenv_overlay"),
    ("apply_runenv_to_toml", "apply_backoffenv_to_toml"),
    ("load_runenv_memory", "load_backoffenv_memory"),
    ("backoffcfg_runenv_free", "backoffcfg_backoffenv_free"),
    ("/tmp/launchcfg_out", "/tmp/backoffcfg_out"),
    ("tolossamuel/launchcfg", "tolossamuel/backoffcfg"),
    ("compile_runenv", "compile_backoffenv"),
    ("runtime.env", "backoff.runtime"),
    ("service.toml", "backoff.toml"),
    ("Container service launch", "Exponential backoff retry policy"),
    ("container service launch", "exponential backoff retry policy"),
    ("runtime `.env` secret overlays", "backoffenv runtime retry parameter overlays"),
    ("Runtime env layer", "Backoffenv layer"),
    ("Service validation", "Backoff policy validation"),
    ("[service]", "[backoff]"),
]

EXCLUDE = {".git", "poc", "guides", "__pycache__"}
SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add backoffcfg public headers", [
        "include/backoffcfg/backoffcfg.h", "include/backoffcfg/backoff_merge.h"]),
    ("include: add backoffenv public API", [
        "include/backoffenv/backoffenv.h", "include/backoffenv/backoffenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add backoff policy jitter schedule headers", [
        "include/backoffcfg/backoff_policy.h", "include/backoffcfg/backoff_jitter.h",
        "include/backoffcfg/backoff_schedule.h"]),
    ("src/backoffenv: add buffer and string utilities", [
        "src/backoffenv/buffer.c", "src/backoffenv/buffer.h", "src/backoffenv/strutil.c",
        "src/backoffenv/strutil.h"]),
    ("src/backoffenv: add arena allocator", [
        "src/backoffenv/arena.c", "src/backoffenv/arena.h", "src/backoffenv/backoffenv_internal.h"]),
    ("src/backoffenv: add error helpers", ["src/backoffenv/error.c", "src/backoffenv/error.h"]),
    ("src/backoffenv: add UTF-8 validation", ["src/backoffenv/utf8.c", "src/backoffenv/utf8.h"]),
    ("src/backoffenv: implement backoff line lexer", ["src/backoffenv/lexer.c", "src/backoffenv/lexer.h"]),
    ("src/backoffenv: add quoted value unescape", ["src/backoffenv/unescape.c", "src/backoffenv/unescape.h"]),
    ("src/backoffenv: add document store", ["src/backoffenv/store.c", "src/backoffenv/store.h"]),
    ("src/backoffenv: wire assignment parser", ["src/backoffenv/parser.c", "src/backoffenv/parser.h"]),
    ("src/backoffenv: add serialize to backoff text", ["src/backoffenv/serialize.c", "src/backoffenv/serialize.h"]),
    ("src/backoffenv: add validation pass", ["src/backoffenv/validate.c", "src/backoffenv/validate.h"]),
    ("src/backoffenv: add merge overlay", ["src/backoffenv/merge.c", "src/backoffenv/merge.h"]),
    ("src/backoffenv: add expand and coerce", [
        "src/backoffenv/expand.c", "src/backoffenv/expand.h", "src/backoffenv/coerce.c",
        "src/backoffenv/coerce.h"]),
    ("src/backoffenv: add walk query diff", [
        "src/backoffenv/walk.c", "src/backoffenv/walk.h", "src/backoffenv/query.c",
        "src/backoffenv/query.h", "src/backoffenv/diff.c", "src/backoffenv/diff.h"]),
    ("src/backoffenv: add pretty printer", ["src/backoffenv/pretty.c", "src/backoffenv/pretty.h"]),
    ("src/backoffenv: add retry stack and ctx", [
        "src/backoffenv/retry_stack.c", "src/backoffenv/retry_stack.h",
        "src/backoffenv/retry_ctx.c", "src/backoffenv/retry_ctx.h"]),
    ("src/backoffenv: add path filter profile", [
        "src/backoffenv/path.c", "src/backoffenv/path.h", "src/backoffenv/filter.c",
        "src/backoffenv/filter.h", "src/backoffenv/profile.c", "src/backoffenv/profile.h"]),
    ("src/backoffenv: add snapshot readutil strict canonical", [
        "src/backoffenv/snapshot.c", "src/backoffenv/snapshot.h", "src/backoffenv/readutil.c",
        "src/backoffenv/readutil.h", "src/backoffenv/strict.c", "src/backoffenv/strict.h",
        "src/backoffenv/canonical.c", "src/backoffenv/canonical.h"]),
    ("src/backoffenv: add backoffloader and main backoffenv module", [
        "src/backoffenv/backoffloader.c", "src/backoffenv/backoffenv.c", "src/backoffenv/backoffmap.c",
        "src/backoffenv/backoffmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.c", "src/toml/buffer.c"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.c", "src/toml/datetime.c", "src/toml/lexer.c"]),
    ("src/toml: add value and parser core", ["src/toml/value.c", "src/toml/parser.c"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.c", "src/toml/merge.c", "src/toml/serialize.c"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.c", "src/toml/format.c", "src/toml/validator.c", "src/toml/document.c"]),
    ("src: add backoffcfg bridge and backoffenv-to-toml merge", ["src/backoffcfg.c", "src/backoff_merge.c"]),
    ("src: add backoff policy validator", ["src/backoff_policy.c"]),
    ("src: add jitter gate evaluator", ["src/backoff_jitter.c"]),
    ("src: add retry attempt schedule tracker", ["src/backoff_schedule.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add backoff policy and schedule unit tests", [
        "tests/test_backoff_policy.c", "tests/test_backoff_schedule.c"]),
    ("examples: add TOML backoff manifest and runtime overlay", [
        "examples/backoff.toml", "examples/backoff.runtime"]),
    ("fuzz: add backoffenv_fuzzer harness", ["fuzz/backoffenv_fuzzer.c"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.c"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.c"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.c"]),
    ("fuzz: add backoff_fuzzer for cross-format overlay", ["fuzz/backoff_fuzzer.c"]),
    ("fuzz: add backoff_schedule_fuzzer for schedule compaction path", ["fuzz/backoff_schedule_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/backoffenv_fuzzer/minimal.benv",
        "fuzz/corpus/backoffenv_fuzzer/quoted.benv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/backoff_fuzzer/sample.bin",
        "fuzz/corpus/backoff_schedule_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for backoffcfg library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable backoff configuration library", []),
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


BACKOFF_POLICY_C = '''#include "backoffcfg/backoff_policy.h"
#include "backoffcfg/backoff_schedule.h"
#include "tome/tome.h"
#include "tome/parser.h"
#include "tome/value.h"

#include <string.h>

int backoffcfg_validate_backoff_manifest(const TomeDoc *doc, backoff_schedule_t *sched) {
  TomeValue *root;
  TomeTable *tbl;
  size_t i;

  if (!doc || !doc->root) {
    return -1;
  }
  root = tome_table_get(doc->root, "backoff");
  if (!root || root->type != TOME_VAL_TABLE) {
    return -1;
  }
  tbl = root->as.table;
  if (!tome_table_get(tbl, "name")) {
    return -1;
  }
  if (!sched) {
    return 0;
  }
  {
    TomeValue *attempts = tome_table_get(tbl, "attempts");
    if (attempts && attempts->type == TOME_VAL_ARRAY) {
      TomeArray *arr = attempts->as.array;
      for (i = 0; i < arr->count; i++) {
        TomeValue *item = &arr->items[i];
        if (item->type == TOME_VAL_TABLE) {
          TomeValue *label = tome_table_get(item->as.table, "label");
          TomeValue *delay_ms = tome_table_get(item->as.table, "delay_ms");
          const char *l = (label && label->type == TOME_VAL_STRING) ? label->as.string : "attempt";
          uint32_t d = 100;
          if (delay_ms && delay_ms->type == TOME_VAL_INTEGER) {
            d = (uint32_t)delay_ms->as.integer;
          }
          backoff_schedule_register(sched, l, d);
        }
      }
    }
  }
  return 0;
}
'''

BACKOFF_POLICY_H = '''#ifndef BACKOFFCFG_BACKOFF_POLICY_H
#define BACKOFFCFG_BACKOFF_POLICY_H

#include "backoffcfg/backoff_schedule.h"
#include "tome/tome.h"

#ifdef __cplusplus
extern "C" {
#endif

int backoffcfg_validate_backoff_manifest(const TomeDoc *doc, backoff_schedule_t *sched);

#ifdef __cplusplus
}
#endif

#endif
'''

BACKOFF_JITTER_C = '''#include "backoffcfg/backoff_jitter.h"

#include <string.h>

int backoff_jitter_allows_retry(const char *circuit_state, uint32_t attempt, uint32_t max_attempts) {
  if (!circuit_state) {
    return 0;
  }
  if (strcmp(circuit_state, "closed") != 0 && strcmp(circuit_state, "half_open") != 0) {
    return 0;
  }
  if (max_attempts == 0) {
    return 1;
  }
  return attempt <= max_attempts;
}
'''

BACKOFF_JITTER_H = '''#ifndef BACKOFFCFG_BACKOFF_JITTER_H
#define BACKOFFCFG_BACKOFF_JITTER_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

int backoff_jitter_allows_retry(const char *circuit_state, uint32_t attempt, uint32_t max_attempts);

#ifdef __cplusplus
}
#endif

#endif
'''

BACKOFF_SCHEDULE_C = '''#include "backoffcfg/backoff_schedule.h"

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

void backoff_schedule_init(backoff_schedule_t *s) {
  if (!s) {
    return;
  }
  memset(s, 0, sizeof(*s));
}

void backoff_schedule_reset(backoff_schedule_t *s) {
  size_t i;
  if (!s) {
    return;
  }
  for (i = 0; i < s->attempt_count; i++) {
    free(s->attempts[i].label);
  }
  free(s->attempts);
  free(s->pending_refs);
  memset(s, 0, sizeof(*s));
}

static int grow_attempts(backoff_schedule_t *s) {
  size_t cap = s->attempt_cap ? s->attempt_cap * 2 : 8;
  backoff_attempt_t *next = (backoff_attempt_t *)realloc(s->attempts, cap * sizeof(*next));
  if (!next) {
    return -1;
  }
  s->attempts = next;
  s->attempt_cap = cap;
  return 0;
}

int backoff_schedule_register(backoff_schedule_t *s, const char *label, uint32_t delay_ms) {
  backoff_attempt_t *slot;
  char *owned;

  if (!s || !label) {
    return -1;
  }
  if (s->attempt_count >= s->attempt_cap && grow_attempts(s) != 0) {
    return -1;
  }
  owned = strdup(label);
  if (!owned) {
    return -1;
  }
  slot = &s->attempts[s->attempt_count++];
  slot->label = owned;
  slot->delay_ms = delay_ms;

  if (s->attempt_count > 4 && (s->attempt_count % 3) == 0) {
    size_t keep = s->attempt_count / 2;
    size_t i;
    if (keep > 0 && keep < s->attempt_count) {
      for (i = 0; i < keep; i++) {
        s->pending_refs = (const char **)realloc(
            s->pending_refs, (s->pending_count + 1) * sizeof(char *));
        if (!s->pending_refs) {
          return -1;
        }
        s->pending_refs[s->pending_count++] = s->attempts[i].label;
      }
      backoff_schedule_compact(s);
    }
  }
  return 0;
}

void backoff_schedule_compact(backoff_schedule_t *s) {
  size_t i;
  size_t dst = 0;
  backoff_attempt_t *next;

  if (!s || s->attempt_count < 2) {
    return;
  }
  next = (backoff_attempt_t *)calloc(s->attempt_count, sizeof(*next));
  if (!next) {
    return;
  }
  for (i = 0; i < s->attempt_count; i++) {
    if (s->attempts[i].delay_ms > 0) {
      char *fresh = strdup(s->attempts[i].label ? s->attempts[i].label : "");
      next[dst].label = fresh;
      next[dst].delay_ms = s->attempts[i].delay_ms;
      free(s->attempts[i].label);
      dst++;
    } else {
      free(s->attempts[i].label);
    }
  }
  free(s->attempts);
  s->attempts = next;
  s->attempt_count = dst;
  s->attempt_cap = dst > 0 ? dst : 1;
}

uint32_t backoff_schedule_finalize_digest(backoff_schedule_t *s) {
  size_t i;
  uint32_t h = 2166136261u;

  if (!s) {
    return 0;
  }
  for (i = 0; i < s->pending_count; i++) {
    const char *ref = s->pending_refs[i];
    if (ref) {
      h = fnv1a32_append(h, ref, strlen(ref));
    }
  }
  s->digest = h;
  return h;
}
'''

BACKOFF_SCHEDULE_H = '''#ifndef BACKOFFCFG_BACKOFF_SCHEDULE_H
#define BACKOFFCFG_BACKOFF_SCHEDULE_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  char *label;
  uint32_t delay_ms;
} backoff_attempt_t;

typedef struct {
  backoff_attempt_t *attempts;
  size_t attempt_count;
  size_t attempt_cap;
  const char **pending_refs;
  size_t pending_count;
  uint32_t digest;
} backoff_schedule_t;

void backoff_schedule_init(backoff_schedule_t *s);
void backoff_schedule_reset(backoff_schedule_t *s);
int backoff_schedule_register(backoff_schedule_t *s, const char *label, uint32_t delay_ms);
void backoff_schedule_compact(backoff_schedule_t *s);
uint32_t backoff_schedule_finalize_digest(backoff_schedule_t *s);

#ifdef __cplusplus
}
#endif

#endif
'''

BACKOFF_SCHEDULE_FUZZER = '''#include "backoffcfg/backoff_schedule.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  backoff_schedule_t s;
  size_t i;
  char label[32];

  if (!data || size == 0 || size > 4096) {
    return 0;
  }
  backoff_schedule_init(&s);
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
    backoff_schedule_register(&s, label, (uint32_t)(data[i] + 1));
    i += n > 0 ? n - 1 : 0;
  }
  (void)backoff_schedule_finalize_digest(&s);
  backoff_schedule_reset(&s);
  return 0;
}
'''

README = """# backoffcfg

backoffcfg is a C11 library for exponential backoff and retry policy configuration: parse TOML backoff manifests, load backoffenv runtime retry parameter overlays, merge layers, validate jitter gates, and track multi-attempt retry schedules during circuit-aware retries.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Backoffenv layer** — `KEY=VALUE`, `@retry` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply backoffenv overlay keys onto parsed TOML documents
- **Backoff policy** — validate `[backoff]` tables and register attempt delays into a compaction schedule
- **Jitter gate** — gate retry progression on circuit state and attempt counts
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `backoffenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `backoff_fuzzer`, `backoff_schedule_fuzzer`.

## Quick start

```c
#include "backoffcfg/backoffcfg.h"

TomeDoc *toml = NULL;
TomeError err;
backoffcfg_load_toml_memory("[backoff]\\nname = \\"payments\\"\\nmax_attempts = 5\\n", 44, &toml, &err);

backoffenv_doc_t *env = NULL;
backoffcfg_load_backoffenv_memory("MAX_ATTEMPTS=3\\n", 16, NULL, &env, NULL);
backoffcfg_apply_backoffenv_to_toml(toml, env);

backoffcfg_backoffenv_free(env);
backoffcfg_toml_free(toml);
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
        (ROOT / "include" / "launchcfg", ROOT / "include" / "backoffcfg"),
        (ROOT / "include" / "runenv", ROOT / "include" / "backoffenv"),
        (ROOT / "src" / "runenv", ROOT / "src" / "backoffenv"),
        (ROOT / "src" / "launchcfg.c", ROOT / "src" / "backoffcfg.c"),
        (ROOT / "src" / "launch_merge.c", ROOT / "src" / "backoff_merge.c"),
        (ROOT / "src" / "launch_service.c", ROOT / "src" / "backoff_policy.c"),
        (ROOT / "fuzz" / "runenv_fuzzer.c", ROOT / "fuzz" / "backoffenv_fuzzer.c"),
        (ROOT / "fuzz" / "launch_fuzzer.c", ROOT / "fuzz" / "backoff_fuzzer.c"),
        (ROOT / "examples" / "service.toml", ROOT / "examples" / "backoff.toml"),
        (ROOT / "examples" / "runtime.env", ROOT / "examples" / "backoff.runtime"),
        (ROOT / "fuzz" / "corpus" / "runenv_fuzzer", ROOT / "fuzz" / "corpus" / "backoffenv_fuzzer"),
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

    for p in list((ROOT / "include" / "backoffenv").glob("*")):
        if "runenv" in p.name:
            p.rename(p.with_name(p.name.replace("runenv", "backoffenv")))

    for p in list((ROOT / "src" / "backoffenv").glob("*")):
        new_name = p.name.replace("runenv", "backoffenv")
        new_name = new_name.replace("runloader", "backoffloader")
        new_name = new_name.replace("require_stack", "retry_stack")
        new_name = new_name.replace("require_ctx", "retry_ctx")
        new_name = new_name.replace("runmap", "backoffmap")
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    for p in list((ROOT / "include" / "backoffcfg").glob("*")):
        if "launch" in p.name:
            p.rename(p.with_name(p.name.replace("launch", "backoff")))

    for p in list((ROOT / "fuzz" / "corpus" / "backoffenv_fuzzer").glob("*")):
        if p.suffix == ".env":
            p.rename(p.with_suffix(".benv"))


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
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".benv", ".env",
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
    write(ROOT / "include" / "backoffcfg" / "backoff_policy.h", BACKOFF_POLICY_H)
    write(ROOT / "include" / "backoffcfg" / "backoff_jitter.h", BACKOFF_JITTER_H)
    write(ROOT / "include" / "backoffcfg" / "backoff_schedule.h", BACKOFF_SCHEDULE_H)
    write(ROOT / "src" / "backoff_policy.c", BACKOFF_POLICY_C)
    write(ROOT / "src" / "backoff_jitter.c", BACKOFF_JITTER_C)
    write(ROOT / "src" / "backoff_schedule.c", BACKOFF_SCHEDULE_C)
    write(ROOT / "fuzz" / "backoff_schedule_fuzzer.c", BACKOFF_SCHEDULE_FUZZER)
    write(ROOT / "README.md", README)

    hdr = (ROOT / "include" / "backoffcfg" / "backoff_merge.h").read_text(encoding="utf-8")
    hdr = hdr.replace("LAYER_MERGE", "BACKOFF_MERGE")
    (ROOT / "include" / "backoffcfg" / "backoff_merge.h").write_text(hdr, encoding="utf-8")

    fuzz = (ROOT / "fuzz" / "backoff_fuzzer.c").read_text(encoding="utf-8")
    fuzz = fuzz.replace(
        "backoffcfg_apply_backoffenv_to_toml(toml, env);",
        "backoffcfg_apply_backoffenv_to_toml(toml, env);\n"
        "  if (toml) {\n"
        "    backoff_schedule_t sched;\n"
        "    backoff_schedule_init(&sched);\n"
        "    backoffcfg_validate_backoff_manifest(toml, &sched);\n"
        "    (void)backoff_schedule_finalize_digest(&sched);\n"
        "    backoff_schedule_reset(&sched);\n"
        "  }",
    )
    fuzz = xform(fuzz)
    fuzz = fuzz.replace("#include \"backoffcfg/backoff_merge.h\"",
        "#include \"backoffcfg/backoff_merge.h\"\n#include \"backoffcfg/backoff_policy.h\"\n#include \"backoffcfg/backoff_schedule.h\"")
    write(ROOT / "fuzz" / "backoff_fuzzer.c", fuzz)

    write(ROOT / "examples" / "backoff.toml", """[backoff]
name = "payments-api"
max_attempts = 5
initial_delay_ms = 100
multiplier = 2.0
circuit_state = "closed"

[[backoff.attempts]]
label = "first"
delay_ms = 100

[[backoff.attempts]]
label = "second"
delay_ms = 250

[[backoff.attempts]]
label = "third"
delay_ms = 500
""")

    write(ROOT / "examples" / "backoff.runtime", """# Runtime retry parameters injected during circuit half-open
MAX_ATTEMPTS=3
INITIAL_DELAY_MS=50
CIRCUIT_STATE=half_open
""")

    write(ROOT / "tests" / "test_backoff_policy.c", '''#include "backoffcfg/backoff_policy.h"
#include "backoffcfg/backoff_schedule.h"
#include "tome/tome.h"
#include "unity/unity.h"

void test_backoff_policy_requires_name(void) {
  TomeDoc *doc = NULL;
  TomeError err;
  backoff_schedule_t s;
  TEST_ASSERT_EQUAL(TOME_OK, tome_parse("[backoff]\\nname=\\"x\\"\\n", 20, &doc, &err));
  backoff_schedule_init(&s);
  TEST_ASSERT_EQUAL(0, backoffcfg_validate_backoff_manifest(doc, &s));
  backoff_schedule_reset(&s);
  tome_free(doc);
}
''')

    write(ROOT / "tests" / "test_backoff_schedule.c", '''#include "backoffcfg/backoff_schedule.h"
#include "unity/unity.h"

void test_backoff_schedule_register(void) {
  backoff_schedule_t s;
  backoff_schedule_init(&s);
  TEST_ASSERT_EQUAL(0, backoff_schedule_register(&s, "a", 100));
  TEST_ASSERT_EQUAL(0, backoff_schedule_register(&s, "b", 200));
  backoff_schedule_reset(&s);
}
''')


def plant_bugs() -> None:
    """Plant standard 5-bug set with hard schedule UAF instead of shallow hex OOB."""
    unesc = (ROOT / "src" / "backoffenv" / "unescape.c").read_text(encoding="utf-8")
    unesc = unesc.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "backoffenv" / "unescape.c").write_text(unesc, encoding="utf-8")

    fmt = (ROOT / "src" / "toml" / "format.c").read_text(encoding="utf-8")
    if "ctx.out.length == 0 && ctx.out.data == NULL" not in fmt:
        fmt = fmt.replace(
            "    if (!emit_table(&ctx, doc->root, \"\", 0)) {",
            "    if (!emit_table(&ctx, doc->root, \"\", 0)) {",
        )
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
        "for f in backoffcfg backoff_merge; do",
        "for f in backoffcfg backoff_merge backoff_policy backoff_jitter backoff_schedule; do",
    )
    build_sh = build_sh.replace(
        "build_fuzzer launch_fuzzer.c launch_fuzzer",
        "build_fuzzer backoff_fuzzer.c backoff_fuzzer\n"
        "build_fuzzer backoff_schedule_fuzzer.c backoff_schedule_fuzzer",
    )
    build_sh = build_sh.replace("compile_runenv", "compile_backoffenv")
    build_sh = build_sh.replace("src/runenv/", "src/backoffenv/")
    build_sh = build_sh.replace('local obj="env_', 'local obj="boenv_')
    build_sh = build_sh.replace("env_*.o", "boenv_*.o")
    build_sh = build_sh.replace(
        "build_fuzzer runenv_fuzzer.c runenv_fuzzer",
        "build_fuzzer backoffenv_fuzzer.c backoffenv_fuzzer",
    )
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build_sh, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    wsl = wsl.replace("runenv_*.o toml_*.o launchcfg.o launch_merge.o",
                      "boenv_*.o toml_*.o backoffcfg.o backoff_merge.o backoff_policy.o backoff_jitter.o backoff_schedule.o")
    (ROOT / "build" / "wsl_build.sh").write_text(wsl, encoding="utf-8")

    proj = (ROOT / ".clusterfuzzlite" / "project.yaml").read_text(encoding="utf-8")
    proj = xform(proj)
    if "backoff_schedule_fuzzer" not in proj:
        proj = proj.replace(
            "- backoff_fuzzer",
            "- backoff_fuzzer\n  - backoff_schedule_fuzzer",
        )
    (ROOT / ".clusterfuzzlite" / "project.yaml").write_text(proj, encoding="utf-8")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "crash-" not in gitignore:
        gitignore += "\ncrash-*\n/poc/\n"
    (ROOT / ".gitignore").write_text(gitignore, encoding="utf-8")

    write(ROOT / "fuzz" / "corpus" / "backoff_fuzzer" / "sample.bin",
          bytes([32]) + b"[backoff]\nname=\"x\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "backoff_schedule_fuzzer" / "seed.bin", bytes(range(32, 96)))


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
    init_git()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
