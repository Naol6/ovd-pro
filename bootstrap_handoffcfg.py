#!/usr/bin/env python3
"""Bootstrap handoffcfg — C++ session handoff manifests + handenv overlays."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/handoffcfg")
SRC = Path("/home/samuel/Documents/fenrir3/draincfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/handoffcfg")

TEXT_RENAME = [
    ("drain_window_t", "migration_ring_t"),
    ("drain_window_", "migration_ring_"),
    ("drain_window", "migration_ring"),
    ("drain_slot_t", "migration_peer_t"),
    ("drain_policy", "handoff_coordinator"),
    ("drain_gate", "affinity_gate"),
    ("drainenv_doc_impl_t", "handenv_doc_impl_t"),
    ("drainenv_doc_t", "handenv_doc_t"),
    ("drainenv_error_t", "handenv_error_t"),
    ("drainenv_options_t", "handenv_options_t"),
    ("drainenv_entry_t", "handenv_entry_t"),
    ("drainenv_slice_t", "handenv_slice_t"),
    ("drainenv_arena_t", "handenv_arena_t"),
    ("drainenv_token_kind_t", "handenv_token_kind_t"),
    ("drainenv_token_t", "handenv_token_t"),
    ("drainenv_internal.h", "handenv_internal.h"),
    ("include/drainenv", "include/handenv"),
    ("src/drainenv/", "src/handenv/"),
    ("src/drainenv", "src/handenv"),
    ("drainenv_", "handenv_"),
    ("DRAINENV_", "HANDENV_"),
    ("Drainenv", "Handenv"),
    ("drainenv", "handenv"),
    ("drain_merge", "handoff_merge"),
    ("drain_fuzzer", "handoff_fuzzer"),
    ("draincfg", "handoffcfg"),
    ("DrainCfg", "HandoffCfg"),
    ("DRAINCFG", "HANDOFFCFG"),
    ("bind_stack", "stick_stack"),
    ("bind_ctx", "stick_ctx"),
    ("@bind", "@stick"),
    ("drainmap", "handmap"),
    ("drainloader", "handloader"),
    ("apply_drainenv_overlay", "apply_handenv_overlay"),
    ("apply_drainenv_to_toml", "apply_handenv_to_toml"),
    ("load_drainenv_memory", "load_handenv_memory"),
    ("handoffcfg_drainenv_free", "handoffcfg_handenv_free"),
    ("/tmp/draincfg_out", "/tmp/handoffcfg_out"),
    ("tolossamuel/draincfg", "tolossamuel/handoffcfg"),
    ("compile_drainenv", "compile_handenv"),
    ("drenv_", "henv_"),
    ("drain.runtime", "handoff.runtime"),
    ("drain.toml", "handoff.toml"),
    ("Graceful connection drain", "Session handoff during rolling upgrades"),
    ("graceful connection drain", "session handoff during rolling upgrades"),
    ("drainenv runtime parameter overlays", "handenv runtime affinity overlays"),
    ("Drainenv layer", "Handenv layer"),
    ("Drain policy validation", "Handoff coordinator validation"),
    ("[drain]", "[handoff]"),
    ("drain.slots", "handoff.peers"),
    ("DRAIN_", "HANDOFF_"),
    ("draining", "migrating"),
    ("max_inflight", "session_ttl_ms"),
    ("health_state", "affinity_mode"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add handoffcfg public headers", [
        "include/handoffcfg/handoffcfg.h", "include/handoffcfg/handoff_merge.h"]),
    ("include: add handenv public API", [
        "include/handenv/handenv.h", "include/handenv/handenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add handoff coordinator and migration ring headers", [
        "include/handoffcfg/handoff_coordinator.h", "include/handoffcfg/affinity_gate.h",
        "include/handoffcfg/migration_ring.h", "include/handoffcfg/sticky_registry.h"]),
    ("src/handenv: add buffer and string utilities", [
        "src/handenv/buffer.cpp", "src/handenv/buffer.h", "src/handenv/strutil.cpp",
        "src/handenv/strutil.h"]),
    ("src/handenv: add arena allocator", [
        "src/handenv/arena.cpp", "src/handenv/arena.h", "src/handenv/handenv_internal.h"]),
    ("src/handenv: add error helpers", ["src/handenv/error.cpp", "src/handenv/error.h"]),
    ("src/handenv: add UTF-8 validation", ["src/handenv/utf8.cpp", "src/handenv/utf8.h"]),
    ("src/handenv: implement handenv line lexer", ["src/handenv/lexer.cpp", "src/handenv/lexer.h"]),
    ("src/handenv: add quoted value unescape", ["src/handenv/unescape.cpp", "src/handenv/unescape.h"]),
    ("src/handenv: add document store", ["src/handenv/store.cpp", "src/handenv/store.h"]),
    ("src/handenv: wire assignment parser", ["src/handenv/parser.cpp", "src/handenv/parser.h"]),
    ("src/handenv: add serialize to handenv text", ["src/handenv/serialize.cpp", "src/handenv/serialize.h"]),
    ("src/handenv: add validation pass", ["src/handenv/validate.cpp", "src/handenv/validate.h"]),
    ("src/handenv: add merge overlay", ["src/handenv/merge.cpp", "src/handenv/merge.h"]),
    ("src/handenv: add expand and coerce", [
        "src/handenv/expand.cpp", "src/handenv/expand.h", "src/handenv/coerce.cpp",
        "src/handenv/coerce.h"]),
    ("src/handenv: add walk query diff", [
        "src/handenv/walk.cpp", "src/handenv/walk.h", "src/handenv/query.cpp",
        "src/handenv/query.h", "src/handenv/diff.cpp", "src/handenv/diff.h"]),
    ("src/handenv: add pretty printer", ["src/handenv/pretty.cpp", "src/handenv/pretty.h"]),
    ("src/handenv: add stick stack and ctx", [
        "src/handenv/stick_stack.cpp", "src/handenv/stick_stack.h",
        "src/handenv/stick_ctx.cpp", "src/handenv/stick_ctx.h"]),
    ("src/handenv: add path filter profile", [
        "src/handenv/path.cpp", "src/handenv/path.h", "src/handenv/filter.cpp",
        "src/handenv/filter.h", "src/handenv/profile.cpp", "src/handenv/profile.h"]),
    ("src/handenv: add snapshot readutil strict canonical", [
        "src/handenv/snapshot.cpp", "src/handenv/snapshot.h", "src/handenv/readutil.cpp",
        "src/handenv/readutil.h", "src/handenv/strict.cpp", "src/handenv/strict.h",
        "src/handenv/canonical.cpp", "src/handenv/canonical.h"]),
    ("src/handenv: add handloader and main handenv module", [
        "src/handenv/handloader.cpp", "src/handenv/handenv.cpp", "src/handenv/handmap.cpp",
        "src/handenv/handmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.cpp", "src/toml/buffer.cpp"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.cpp", "src/toml/datetime.cpp", "src/toml/lexer.cpp"]),
    ("src/toml: add value and parser core", ["src/toml/value.cpp", "src/toml/parser.cpp"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.cpp", "src/toml/merge.cpp", "src/toml/serialize.cpp"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.cpp", "src/toml/format.cpp", "src/toml/validator.cpp", "src/toml/document.cpp"]),
    ("src: add handoffcfg bridge and handenv-to-toml merge", ["src/handoffcfg.cpp", "src/handoff_merge.cpp"]),
    ("src: add handoff coordinator validator", ["src/handoff_coordinator.cpp"]),
    ("src: add affinity gate evaluator", ["src/affinity_gate.cpp"]),
    ("src: add migration ring peer tracker", ["src/migration_ring.cpp"]),
    ("src: add sticky session registry", ["src/sticky_registry.cpp"]),
    ("tests: add Unity harness", ["tests/unity/unity.cpp", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.cpp", "tests/test_basic.cpp"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.cpp", "tests/test_merge.cpp", "tests/test_validate.cpp"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.cpp", "tests/test_coerce.cpp", "tests/test_integration.cpp",
        "tests/test_scenarios.cpp"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.cpp", "tests/test_lexer_exhaustive.cpp"]),
    ("tests: add handoff coordinator and migration ring unit tests", [
        "tests/test_handoff_coordinator.cpp", "tests/test_migration_ring.cpp"]),
    ("tests: add sticky registry unit tests", ["tests/test_sticky_registry.cpp"]),
    ("examples: add TOML handoff manifest and runtime overlay", [
        "examples/handoff.toml", "examples/handoff.runtime"]),
    ("fuzz: add handenv_fuzzer harness", ["fuzz/handenv_fuzzer.cc"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.cc"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.cc"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.cc"]),
    ("fuzz: add handoff_fuzzer for cross-format overlay", ["fuzz/handoff_fuzzer.cc"]),
    ("fuzz: add migration_ring_fuzzer for compaction path", ["fuzz/migration_ring_fuzzer.cc"]),
    ("fuzz: add sticky_registry_fuzzer for affinity path", ["fuzz/sticky_registry_fuzzer.cc"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/handenv_fuzzer/minimal.henv",
        "fuzz/corpus/handenv_fuzzer/quoted.henv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/handoff_fuzzer/sample.bin",
        "fuzz/corpus/migration_ring_fuzzer/seed.bin",
        "fuzz/corpus/sticky_registry_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for handoffcfg library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable handoff configuration library", []),
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


def rename_c_to_cpp(root: Path) -> None:
    for path in sorted(root.rglob("*.c"), reverse=True):
        dst = path.with_suffix(".cpp")
        path.rename(dst)


def copy_tree() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ignore = shutil.ignore_patterns(".git", "*.o", "__pycache__", "poc", "guides")
    shutil.copytree(SRC, ROOT, ignore=ignore)

    renames = [
        (ROOT / "include" / "draincfg", ROOT / "include" / "handoffcfg"),
        (ROOT / "include" / "drainenv", ROOT / "include" / "handenv"),
        (ROOT / "src" / "drainenv", ROOT / "src" / "handenv"),
        (ROOT / "src" / "draincfg.c", ROOT / "src" / "handoffcfg.cpp"),
        (ROOT / "src" / "drain_merge.c", ROOT / "src" / "handoff_merge.cpp"),
        (ROOT / "src" / "drain_policy.c", ROOT / "src" / "handoff_coordinator.cpp"),
        (ROOT / "src" / "drain_gate.c", ROOT / "src" / "affinity_gate.cpp"),
        (ROOT / "src" / "drain_window.c", ROOT / "src" / "migration_ring.cpp"),
        (ROOT / "fuzz" / "drainenv_fuzzer.c", ROOT / "fuzz" / "handenv_fuzzer.cc"),
        (ROOT / "fuzz" / "launch_fuzzer.c", ROOT / "fuzz" / "handoff_fuzzer.cc"),
        (ROOT / "fuzz" / "drain_fuzzer.c", ROOT / "fuzz" / "handoff_fuzzer.cc"),
        (ROOT / "fuzz" / "toml_fuzzer.c", ROOT / "fuzz" / "toml_fuzzer.cc"),
        (ROOT / "fuzz" / "toml_merge_fuzzer.c", ROOT / "fuzz" / "toml_merge_fuzzer.cc"),
        (ROOT / "fuzz" / "toml_format_fuzzer.c", ROOT / "fuzz" / "toml_format_fuzzer.cc"),
        (ROOT / "fuzz" / "drain_window_fuzzer.c", ROOT / "fuzz" / "migration_ring_fuzzer.cc"),
        (ROOT / "examples" / "drain.toml", ROOT / "examples" / "handoff.toml"),
        (ROOT / "examples" / "drain.runtime", ROOT / "examples" / "handoff.runtime"),
        (ROOT / "fuzz" / "corpus" / "drainenv_fuzzer", ROOT / "fuzz" / "corpus" / "handenv_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "drain_fuzzer", ROOT / "fuzz" / "corpus" / "handoff_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "drain_window_fuzzer", ROOT / "fuzz" / "corpus" / "migration_ring_fuzzer"),
    ]
    for src, dst in renames:
        if not src.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        src.rename(dst)

    rename_c_to_cpp(ROOT)

    for p in list((ROOT / "include" / "handenv").glob("*")):
        if "drainenv" in p.name:
            p.rename(p.with_name(p.name.replace("drainenv", "handenv")))

    for p in list((ROOT / "src" / "handenv").glob("*")):
        new_name = p.name.replace("drainenv", "handenv")
        new_name = new_name.replace("drainloader", "handloader")
        new_name = new_name.replace("bind_stack", "stick_stack")
        new_name = new_name.replace("bind_ctx", "stick_ctx")
        new_name = new_name.replace("drainmap", "handmap")
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    for p in list((ROOT / "include" / "handoffcfg").glob("*")):
        if "drain" in p.name:
            p.rename(p.with_name(p.name.replace("drain", "handoff").replace("window", "migration_ring")))

    corp = ROOT / "fuzz" / "corpus" / "handenv_fuzzer"
    for old in list(corp.glob("*.drenv")):
        old.rename(old.with_suffix(".henv"))


def patch_handenv_lexer(text: str) -> str:
    if "HANDENV_TOK_BANG" in text:
        return text
    return text.replace(
        "  if (lx->cur >= lx->end || (*lx->cur != '#' && *lx->cur != ';')) {",
        "  if (lx->cur >= lx->end || (*lx->cur != '#' && *lx->cur != ';' && *lx->cur != '!')) {",
    )


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
            ".cpp", ".h", ".cc", ".sh", ".yaml", ".md", ".txt", ".toml",
            ".henv", ".drenv", ".env", "Makefile"
        } and path.name not in {"Makefile", ".gitignore"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text = xform(text)
        if path.name == "lexer.cpp" and "handenv" in str(path):
            new_text = patch_handenv_lexer(new_text)
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


STICKY_REGISTRY_H = '''#ifndef HANDOFFCFG_STICKY_REGISTRY_H
#define HANDOFFCFG_STICKY_REGISTRY_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  char *token;
  char *target;
  uint32_t generation;
} sticky_entry_t;

typedef struct {
  sticky_entry_t *entries;
  size_t count;
  size_t cap;
  uint32_t epoch;
  uint32_t digest;
} sticky_registry_t;

void sticky_registry_init(sticky_registry_t *r);
void sticky_registry_reset(sticky_registry_t *r);
int sticky_registry_bind(sticky_registry_t *r, const char *token, const char *target);
int sticky_registry_promote_epoch(sticky_registry_t *r);
uint32_t sticky_registry_finalize_digest(sticky_registry_t *r);

#ifdef __cplusplus
}
#endif

#endif
'''

STICKY_REGISTRY_CPP = '''#include "handoffcfg/sticky_registry.h"

#include <stdlib.h>
#include <string.h>

static uint32_t djb2_append(uint32_t h, const char *data, size_t len) {
  size_t i;
  for (i = 0; i < len; i++) {
    h = ((h << 5) + h) + (unsigned char)data[i];
  }
  return h;
}

void sticky_registry_init(sticky_registry_t *r) {
  if (!r) {
    return;
  }
  memset(r, 0, sizeof(*r));
}

void sticky_registry_reset(sticky_registry_t *r) {
  size_t i;
  if (!r) {
    return;
  }
  for (i = 0; i < r->count; i++) {
    free(r->entries[i].token);
    free(r->entries[i].target);
  }
  free(r->entries);
  memset(r, 0, sizeof(*r));
}

static int grow_entries(sticky_registry_t *r) {
  size_t cap = r->cap ? r->cap * 2 : 8;
  sticky_entry_t *next = (sticky_entry_t *)realloc(r->entries, cap * sizeof(*next));
  if (!next) {
    return -1;
  }
  r->entries = next;
  r->cap = cap;
  return 0;
}

int sticky_registry_bind(sticky_registry_t *r, const char *token, const char *target) {
  char *tok_copy;
  char *tgt_copy;
  sticky_entry_t *e;

  if (!r || !token || !target) {
    return -1;
  }
  if (r->count >= r->cap && grow_entries(r) != 0) {
    return -1;
  }
  tok_copy = strdup(token);
  tgt_copy = strdup(target);
  if (!tok_copy || !tgt_copy) {
    free(tok_copy);
    free(tgt_copy);
    return -1;
  }
  e = &r->entries[r->count++];
  e->token = tok_copy;
  e->target = tgt_copy;
  e->generation = r->epoch;
  return 0;
}

int sticky_registry_promote_epoch(sticky_registry_t *r) {
  if (!r) {
    return -1;
  }
  r->epoch++;
  return 0;
}

uint32_t sticky_registry_finalize_digest(sticky_registry_t *r) {
  size_t i;
  uint32_t h = 5381u;
  if (!r) {
    return 0;
  }
  for (i = 0; i < r->count; i++) {
    if (r->entries[i].generation < r->epoch) {
      continue;
    }
    if (r->entries[i].token) {
      h = djb2_append(h, r->entries[i].token, strlen(r->entries[i].token));
    }
    if (r->entries[i].target) {
      h = djb2_append(h, r->entries[i].target, strlen(r->entries[i].target));
    }
  }
  r->digest = h;
  return h;
}
'''

STICKY_FUZZER = '''#include "handoffcfg/sticky_registry.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  sticky_registry_t reg;
  size_t i = 0;
  char tok[24];
  char tgt[24];

  if (!data || size < 8 || size > 4096) {
    return 0;
  }
  sticky_registry_init(&reg);
  while (i + 2 < size) {
    size_t tn = (size_t)(data[i] % 8) + 1;
    size_t gn = (size_t)(data[i + 1] % 8) + 1;
    if (i + 2 + tn + gn > size) {
      break;
    }
    if (tn >= sizeof(tok)) {
      tn = sizeof(tok) - 1;
    }
    if (gn >= sizeof(tgt)) {
      gn = sizeof(tgt) - 1;
    }
    memcpy(tok, data + i + 2, tn);
    tok[tn] = '\\0';
    memcpy(tgt, data + i + 2 + tn, gn);
    tgt[gn] = '\\0';
    sticky_registry_bind(&reg, tok, tgt);
    if ((data[i] & 7) == 0) {
      sticky_registry_promote_epoch(&reg);
    }
    i += 2 + tn + gn;
  }
  (void)sticky_registry_finalize_digest(&reg);
  sticky_registry_reset(&reg);
  return 0;
}
'''

README = """# handoffcfg

handoffcfg is a C++17 library for **session handoff** configuration during rolling upgrades: parse TOML handoff manifests, load handenv runtime affinity overlays, merge layers, validate affinity gates, and track migration rings plus sticky session registries.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Handenv layer** — `KEY=VALUE`, `@stick` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply handenv overlay keys onto parsed TOML documents
- **Handoff coordinator** — validate `[handoff]` tables and register peer weights into a migration ring
- **Sticky registry** — track session token affinity across migration epochs
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `handenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `handoff_fuzzer`, `migration_ring_fuzzer`, `sticky_registry_fuzzer`.

## License

MIT — see LICENSE.
"""


def add_domain() -> None:
    write(ROOT / "include" / "handoffcfg" / "sticky_registry.h", STICKY_REGISTRY_H)
    write(ROOT / "src" / "sticky_registry.cpp", STICKY_REGISTRY_CPP)
    write(ROOT / "fuzz" / "sticky_registry_fuzzer.cc", STICKY_FUZZER)
    write(ROOT / "README.md", README)

    hdr = (ROOT / "include" / "handoffcfg" / "handoff_merge.h").read_text(encoding="utf-8")
    hdr = hdr.replace("LAYER_MERGE", "HANDOFF_MERGE")
    (ROOT / "include" / "handoffcfg" / "handoff_merge.h").write_text(hdr, encoding="utf-8")

    fuzz = (ROOT / "fuzz" / "handoff_fuzzer.cc").read_text(encoding="utf-8")
    if "migration_ring_t" not in fuzz:
        fuzz = fuzz.replace(
            "handoffcfg_apply_handenv_to_toml(toml, env);",
            "handoffcfg_apply_handenv_to_toml(toml, env);\n"
            "  if (toml) {\n"
            "    migration_ring_t ring;\n"
            "    sticky_registry_t reg;\n"
            "    migration_ring_init(&ring);\n"
            "    sticky_registry_init(&reg);\n"
            "    handoffcfg_validate_handoff_manifest(toml, &ring);\n"
            "    (void)migration_ring_finalize_digest(&ring);\n"
            "    sticky_registry_reset(&reg);\n"
            "    migration_ring_reset(&ring);\n"
            "  }",
        )
    if "#include \"handoffcfg/sticky_registry.h\"" not in fuzz:
        fuzz = fuzz.replace(
            "#include \"handoffcfg/handoff_merge.h\"",
            "#include \"handoffcfg/handoff_merge.h\"\n"
            "#include \"handoffcfg/handoff_coordinator.h\"\n"
            "#include \"handoffcfg/migration_ring.h\"\n"
            "#include \"handoffcfg/sticky_registry.h\"",
        )
    write(ROOT / "fuzz" / "handoff_fuzzer.cc", fuzz)

    write(ROOT / "examples" / "handoff.toml", """[handoff]
name = "checkout-api"
session_ttl_ms = 45000
affinity_mode = "sticky"

[[handoff.peers]]
label = "canary"
weight = 3

[[handoff.peers]]
label = "primary"
weight = 9
""")

    write(ROOT / "examples" / "handoff.runtime", """# Runtime handoff parameters injected during rolling upgrade
SESSION_TTL_MS=30000
AFFINITY_MODE=migrating
STICKY_GENERATION=2
""")

    write(ROOT / "tests" / "test_handoff_coordinator.cpp", '''#include "handoffcfg/handoff_coordinator.h"
#include "handoffcfg/migration_ring.h"
#include "tome/tome.h"
#include "unity/unity.h"

void test_handoff_coordinator_requires_name(void) {
  TomeDoc *doc = NULL;
  TomeError err;
  migration_ring_t ring;
  TEST_ASSERT_EQUAL(TOME_OK, tome_parse("[handoff]\\nname=\\"x\\"\\n", 20, &doc, &err));
  migration_ring_init(&ring);
  TEST_ASSERT_EQUAL(0, handoffcfg_validate_handoff_manifest(doc, &ring));
  migration_ring_reset(&ring);
  tome_free(doc);
}
''')

    write(ROOT / "tests" / "test_migration_ring.cpp", '''#include "handoffcfg/migration_ring.h"
#include "unity/unity.h"

void test_migration_ring_register(void) {
  migration_ring_t ring;
  migration_ring_init(&ring);
  TEST_ASSERT_EQUAL(0, migration_ring_register(&ring, "a", 1));
  TEST_ASSERT_EQUAL(0, migration_ring_register(&ring, "b", 2));
  migration_ring_reset(&ring);
}
''')

    write(ROOT / "tests" / "test_sticky_registry.cpp", '''#include "handoffcfg/sticky_registry.h"
#include "unity/unity.h"

void test_sticky_registry_bind(void) {
  sticky_registry_t reg;
  sticky_registry_init(&reg);
  TEST_ASSERT_EQUAL(0, sticky_registry_bind(&reg, "sess1", "node-a"));
  TEST_ASSERT_NOT_EQUAL(0u, sticky_registry_finalize_digest(&reg));
  sticky_registry_reset(&reg);
}
''')


def plant_bugs() -> None:
    """Keep inherited cfg bugs; fix shallow handenv hex OOB so primary tasks stay hard."""
    unesc = (ROOT / "src" / "handenv" / "unescape.cpp").read_text(encoding="utf-8")
    unesc = unesc.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "handenv" / "unescape.cpp").write_text(unesc, encoding="utf-8")


def patch_build() -> None:
    build_sh = '''#!/bin/bash -eu

OBJECTS=()

compile_handenv() {
  local base="$1"
  local obj="handenv_${base%.cpp}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall -D_GNU_SOURCE} \
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/handenv" \
    -c "${SRC:-.}/src/handenv/${base}" -o "${obj}"
  OBJECTS+=("${obj}")
}

compile_toml() {
  local base="$1"
  local obj="toml_${base%.cpp}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall} \
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/toml" \
    -c "${SRC:-.}/src/toml/${base}" -o "${obj}"
  OBJECTS+=("${obj}")
}

for f in buffer strutil error arena utf8 store unescape lexer parser serialize \
         validate merge expand coerce walk query diff pretty stick_stack \
         stick_ctx path filter handmap profile canonical strict readutil \
         snapshot handloader handenv; do
  if [ -f "${SRC:-.}/src/handenv/${f}.cpp" ]; then
    compile_handenv "${f}.cpp"
  fi
done

for f in memory buffer unicode datetime lexer value parser path merge serialize \
         diag format validator document; do
  compile_toml "${f}.cpp"
done

for f in handoffcfg handoff_merge handoff_coordinator affinity_gate migration_ring sticky_registry; do
  obj="${f}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall} \
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/handenv" -I"${SRC:-.}/src/toml" \
    -c "${SRC:-.}/src/${f}.cpp" -o "${obj}"
  OBJECTS+=("${obj}")
done

FUZZ_CXXFLAGS="${CXXFLAGS:- -O1 -g -std=c++17}"
INCS="-I${SRC:-.}/include -I${SRC:-.}/src/handenv -I${SRC:-.}/src/toml"

build_fuzzer() {
  ${CXX:-clang++} ${FUZZ_CXXFLAGS} ${LIB_FUZZING_ENGINE} \
    "${SRC:-.}/fuzz/$1" "${OBJECTS[@]}" ${INCS} \
    -o "${OUT:-.}/$2" -lm
}

build_fuzzer handenv_fuzzer.cc handenv_fuzzer
build_fuzzer toml_fuzzer.cc toml_fuzzer
build_fuzzer toml_merge_fuzzer.cc toml_merge_fuzzer
build_fuzzer toml_format_fuzzer.cc toml_format_fuzzer
build_fuzzer handoff_fuzzer.cc handoff_fuzzer
build_fuzzer migration_ring_fuzzer.cc migration_ring_fuzzer
build_fuzzer sticky_registry_fuzzer.cc sticky_registry_fuzzer
'''
    write(ROOT / ".clusterfuzzlite" / "build.sh", build_sh)

    wsl = '''#!/bin/bash -eu
set -o pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${OUT:-/tmp/handoffcfg_out}"
mkdir -p "$OUT"
export SRC="$ROOT"
export OUT="$OUT"
export CC="${CC:-clang}"
export CXX="${CXX:-clang++}"
export LIB_FUZZING_ENGINE="${LIB_FUZZING_ENGINE:--fsanitize=fuzzer,address}"
export CXXFLAGS="${CXXFLAGS:--fsanitize=address -g -O1 -std=c++17}"
export CFLAGS="${CFLAGS:--fsanitize=address -g -O1 -std=c++17}"
bash "$ROOT/.clusterfuzzlite/build.sh"
echo "Built fuzzers in $OUT"
'''
    write(ROOT / "build" / "wsl_build.sh", wsl)

    proj = '''language: c++
sanitizers:
  - address
fuzz_targets:
  - handenv_fuzzer
  - toml_fuzzer
  - toml_merge_fuzzer
  - toml_format_fuzzer
  - handoff_fuzzer
  - migration_ring_fuzzer
  - sticky_registry_fuzzer
'''
    write(ROOT / ".clusterfuzzlite" / "project.yaml", proj)

    gitignore = """*.o
*.a
/tmp/
cmake-build/
build-asan/
/poc/
/guides/
crash-*
"""
    write(ROOT / ".gitignore", gitignore)

    makefile = '''CXX ?= clang++
CXXFLAGS ?= -std=c++17 -O2 -g -Wall -Wextra -Wpedantic -Werror -Iinclude -Isrc/handenv -Isrc/toml
HANDENV_SRC := $(wildcard src/handenv/*.cpp)
TOML_SRC := $(wildcard src/toml/*.cpp)
CORE_SRC := src/handoffcfg.cpp src/handoff_merge.cpp src/handoff_coordinator.cpp src/affinity_gate.cpp src/migration_ring.cpp src/sticky_registry.cpp
TEST_SRC := $(wildcard tests/test_*.cpp)
TEST := build/handoffcfg_tests

$(TEST): $(HANDENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) | build
	$(CXX) $(CXXFLAGS) $(HANDENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) -o $@

build:
	mkdir -p build

test: $(TEST)
	$(TEST)

fuzz:
	rm -rf out && OUT=$$(pwd)/out CXX=clang++ bash .clusterfuzzlite/build.sh

clean:
	rm -f $(TEST)
	rm -rf out
.PHONY: test fuzz clean
'''
    write(ROOT / "Makefile", makefile)

    corp = ROOT / "fuzz" / "corpus" / "handenv_fuzzer"
    for old in list(corp.glob("*.drenv")):
        old.rename(old.with_suffix(".henv"))
    write(ROOT / "fuzz" / "corpus" / "handoff_fuzzer" / "sample.bin",
          bytes([32]) + b"[handoff]\nname=\"x\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "migration_ring_fuzzer" / "seed.bin", bytes(range(32, 96)))
    write(ROOT / "fuzz" / "corpus" / "sticky_registry_fuzzer" / "seed.bin", bytes(range(16, 128)))


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
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    print("OK", ROOT)


if __name__ == "__main__":
    main()
