#!/usr/bin/env python3
"""Bootstrap mountcfg — TOML container volume mount manifests + mountenv runtime overlays."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/mountcfg")
SRC = Path("/home/samuel/Documents/fenrir3/launchcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/mountcfg")

TEXT_RENAME = [
    ("runenv_doc_impl_t", "mountenv_doc_impl_t"),
    ("runenv_doc_t", "mountenv_doc_t"),
    ("runenv_error_t", "mountenv_error_t"),
    ("runenv_options_t", "mountenv_options_t"),
    ("runenv_entry_t", "mountenv_entry_t"),
    ("runenv_slice_t", "mountenv_slice_t"),
    ("runenv_arena_t", "mountenv_arena_t"),
    ("runenv_token_kind_t", "mountenv_token_kind_t"),
    ("runenv_token_t", "mountenv_token_t"),
    ("runenv_internal.h", "mountenv_internal.h"),
    ("runenv/runenv_types.h", "mountenv/mountenv_types.h"),
    ("include/runenv", "include/mountenv"),
    ("src/runenv/", "src/mountenv/"),
    ("src/runenv", "src/mountenv"),
    ("runenv_", "mountenv_"),
    ("RUNENV_", "MOUNTENV_"),
    ("Runenv", "Mountenv"),
    ("runenv", "mountenv"),
    ("launch_merge", "mount_merge"),
    ("launch_fuzzer", "mount_fuzzer"),
    ("launch_service", "mount_policy"),
    ("launchcfg", "mountcfg"),
    ("LaunchCfg", "MountCfg"),
    ("LAUNCHCFG", "MOUNTCFG"),
    ("require_stack", "bind_stack"),
    ("require_ctx", "bind_ctx"),
    ("@require", "@mount"),
    ("runmap", "mountmap"),
    ("runloader", "mountloader"),
    ("apply_runenv_overlay", "apply_mountenv_overlay"),
    ("apply_runenv_to_toml", "apply_mountenv_to_toml"),
    ("load_runenv_memory", "load_mountenv_memory"),
    ("mountcfg_runenv_free", "mountcfg_mountenv_free"),
    ("/tmp/launchcfg_out", "/tmp/mountcfg_out"),
    ("tolossamuel/launchcfg", "tolossamuel/mountcfg"),
    ("compile_runenv", "compile_mountenv"),
    ("runtime.env", "mount.runtime"),
    ("service.toml", "mount.toml"),
    ("Container service launch", "Container volume mount orchestration"),
    ("container service launch", "Container volume mount orchestration"),
    ("runtime `.env` secret overlays", "mountenv runtime mount-option parameter overlays"),
    ("Runtime env layer", "Mountenv layer"),
    ("Service validation", "Mount policy validation"),
    ("[service]", "[mount]"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add mountcfg public headers", [
        "include/mountcfg/mountcfg.h", "include/mountcfg/mount_merge.h"]),
    ("include: add mountenv public API", [
        "include/mountenv/mountenv.h", "include/mountenv/mountenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add mount policy gate registry headers", [
        "include/mountcfg/mount_policy.h", "include/mountcfg/mount_gate.h",
        "include/mountcfg/mount_registry.h"]),
    ("src/mountenv: add buffer and string utilities", [
        "src/mountenv/buffer.c", "src/mountenv/buffer.h", "src/mountenv/strutil.c",
        "src/mountenv/strutil.h"]),
    ("src/mountenv: add arena allocator", [
        "src/mountenv/arena.c", "src/mountenv/arena.h", "src/mountenv/mountenv_internal.h"]),
    ("src/mountenv: add error helpers", ["src/mountenv/error.c", "src/mountenv/error.h"]),
    ("src/mountenv: add UTF-8 validation", ["src/mountenv/utf8.c", "src/mountenv/utf8.h"]),
    ("src/mountenv: implement mountenv line lexer", ["src/mountenv/lexer.c", "src/mountenv/lexer.h"]),
    ("src/mountenv: add quoted value unescape", ["src/mountenv/unescape.c", "src/mountenv/unescape.h"]),
    ("src/mountenv: add document store", ["src/mountenv/store.c", "src/mountenv/store.h"]),
    ("src/mountenv: wire assignment parser", ["src/mountenv/parser.c", "src/mountenv/parser.h"]),
    ("src/mountenv: add serialize to mountenv text", ["src/mountenv/serialize.c", "src/mountenv/serialize.h"]),
    ("src/mountenv: add validation pass", ["src/mountenv/validate.c", "src/mountenv/validate.h"]),
    ("src/mountenv: add merge overlay", ["src/mountenv/merge.c", "src/mountenv/merge.h"]),
    ("src/mountenv: add expand and coerce", [
        "src/mountenv/expand.c", "src/mountenv/expand.h", "src/mountenv/coerce.c",
        "src/mountenv/coerce.h"]),
    ("src/mountenv: add walk query diff", [
        "src/mountenv/walk.c", "src/mountenv/walk.h", "src/mountenv/query.c",
        "src/mountenv/query.h", "src/mountenv/diff.c", "src/mountenv/diff.h"]),
    ("src/mountenv: add pretty printer", ["src/mountenv/pretty.c", "src/mountenv/pretty.h"]),
    ("src/mountenv: add include stack and ctx", [
        "src/mountenv/bind_stack.c", "src/mountenv/bind_stack.h",
        "src/mountenv/bind_ctx.c", "src/mountenv/bind_ctx.h"]),
    ("src/mountenv: add path filter profile", [
        "src/mountenv/path.c", "src/mountenv/path.h", "src/mountenv/filter.c",
        "src/mountenv/filter.h", "src/mountenv/profile.c", "src/mountenv/profile.h"]),
    ("src/mountenv: add snapshot readutil strict canonical", [
        "src/mountenv/snapshot.c", "src/mountenv/snapshot.h", "src/mountenv/readutil.c",
        "src/mountenv/readutil.h", "src/mountenv/strict.c", "src/mountenv/strict.h",
        "src/mountenv/canonical.c", "src/mountenv/canonical.h"]),
    ("src/mountenv: add mountloader and main mountenv module", [
        "src/mountenv/mountloader.c", "src/mountenv/mountenv.c", "src/mountenv/mountmap.c",
        "src/mountenv/mountmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.c", "src/toml/buffer.c"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.c", "src/toml/datetime.c", "src/toml/lexer.c"]),
    ("src/toml: add value and parser core", ["src/toml/value.c", "src/toml/parser.c"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.c", "src/toml/merge.c", "src/toml/serialize.c"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.c", "src/toml/format.c", "src/toml/validator.c", "src/toml/document.c"]),
    ("src: add mountcfg bridge and mountenv-to-toml merge", ["src/mountcfg.c", "src/mount_merge.c"]),
    ("src: add window policy validator", ["src/mount_policy.c"]),
    ("src: add latency budget gate evaluator", ["src/mount_gate.c"]),
    ("src: add mount volume registry with compaction", ["src/mount_registry.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add mount policy and registry unit tests", [
        "tests/test_mount_policy.c", "tests/test_mount_registry.c"]),
    ("examples: add TOML mount manifest and runtime overlay", [
        "examples/mount.toml", "examples/mount.runtime"]),
    ("fuzz: add mountenv_fuzzer harness", ["fuzz/mountenv_fuzzer.c"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.c"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.c"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.c"]),
    ("fuzz: add mount_fuzzer for cross-format overlay", ["fuzz/mount_fuzzer.c"]),
    ("fuzz: add mount_registry_fuzzer for volume compaction path", ["fuzz/mount_registry_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/mountenv_fuzzer/minimal.menv",
        "fuzz/corpus/mountenv_fuzzer/quoted.menv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/mount_fuzzer/sample.bin",
        "fuzz/corpus/mount_registry_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for mountcfg library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable volume mount orchestration library", []),
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


MOUNT_POLICY_C = '''#include "mountcfg/mount_policy.h"
#include "mountcfg/mount_registry.h"
#include "tome/tome.h"
#include "tome/parser.h"
#include "tome/value.h"

#include <string.h>

int mountcfg_validate_mount_manifest(const TomeDoc *doc, mount_registry_t *trk) {
  TomeValue *root;
  TomeTable *tbl;
  size_t i;

  if (!doc || !doc->root) {
    return -1;
  }
  root = tome_table_get(doc->root, "mount");
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
    TomeValue *slots = tome_table_get(tbl, "volumes");
    if (slots && slots->type == TOME_VAL_ARRAY) {
      TomeArray *arr = slots->as.array;
      for (i = 0; i < arr->count; i++) {
        TomeValue *item = &arr->items[i];
        if (item->type == TOME_VAL_TABLE) {
          TomeValue *label = tome_table_get(item->as.table, "volume");
          TomeValue *label2 = tome_table_get(item->as.table, "passno");
          const char *l = (label && label->type == TOME_VAL_STRING) ? label->as.string : "volume";
          uint32_t budget = 100;
          if (label2 && label2->type == TOME_VAL_INTEGER) {
            budget = (uint32_t)label2->as.integer;
          }
          mount_registry_register(trk, l, budget);
        }
      }
    }
  }
  return 0;
}
'''

MOUNT_POLICY_HDR = '''#ifndef MOUNTCFG_MOUNT_POLICY_HDR
#define MOUNTCFG_MOUNT_POLICY_HDR

#include "mountcfg/mount_registry.h"
#include "tome/tome.h"

#ifdef __cplusplus
extern "C" {
#endif

int mountcfg_validate_mount_manifest(const TomeDoc *doc, mount_registry_t *trk);

#ifdef __cplusplus
}
#endif

#endif
'''

MOUNT_GATE_C = '''#include "mountcfg/mount_gate.h"

#include <string.h>

int mount_gate_allows(const char *state, uint32_t tokens, uint32_t capacity) {
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

MOUNT_GATE_HDR = '''#ifndef MOUNTCFG_MOUNT_GATE_HDR
#define MOUNTCFG_MOUNT_GATE_HDR

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

int mount_gate_allows(const char *state, uint32_t tokens, uint32_t capacity);

#ifdef __cplusplus
}
#endif

#endif
'''

MOUNT_REGISTRY_C = '''#include "mountcfg/mount_registry.h"

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

void mount_registry_init(mount_registry_t *t) {
  if (!t) {
    return;
  }
  memset(t, 0, sizeof(*t));
}

void mount_registry_reset(mount_registry_t *t) {
  size_t i;
  if (!t) {
    return;
  }
  for (i = 0; i < t->volume_count; i++) {
    free(t->volumes[i].label);
  }
  free(t->volumes);
  free(t->pending_refs);
  memset(t, 0, sizeof(*t));
}

static int grow_volumes(mount_registry_t *t) {
  size_t cap = t->volume_cap ? t->volume_cap * 2 : 8;
  mount_volume_t *next = (mount_volume_t *)realloc(t->volumes, cap * sizeof(*next));
  if (!next) {
    return -1;
  }
  t->volumes = next;
  t->volume_cap = cap;
  return 0;
}

int mount_registry_register(mount_registry_t *t, const char *label, uint32_t budget) {
  mount_volume_t *slot;
  char *owned;

  if (!t || !label) {
    return -1;
  }
  if (t->volume_count >= t->volume_cap && grow_volumes(t) != 0) {
    return -1;
  }
  owned = strdup(label);
  if (!owned) {
    return -1;
  }
  slot = &t->volumes[t->volume_count++];
  slot->label = owned;
  slot->passno = budget;

  if (t->volume_count > 4 && (t->volume_count % 3) == 0) {
    size_t keep = t->volume_count / 2;
    size_t i;
    if (keep > 0 && keep < t->volume_count) {
      for (i = 0; i < keep; i++) {
        t->pending_refs = (const char **)realloc(
            t->pending_refs, (t->pending_count + 1) * sizeof(char *));
        if (!t->pending_refs) {
          return -1;
        }
        t->pending_refs[t->pending_count++] = t->volumes[i].label;
      }
      mount_registry_compact(t);
    }
  }
  return 0;
}

void mount_registry_compact(mount_registry_t *t) {
  size_t i;
  size_t dst = 0;
  mount_volume_t *next;

  if (!t || t->volume_count < 2) {
    return;
  }
  next = (mount_volume_t *)calloc(t->volume_count, sizeof(*next));
  if (!next) {
    return;
  }
  for (i = 0; i < t->volume_count; i++) {
    if (t->volumes[i].passno > 0) {
      char *fresh = strdup(t->volumes[i].label ? t->volumes[i].label : "");
      next[dst].label = fresh;
      next[dst].passno = t->volumes[i].passno;
      free(t->volumes[i].label);
      dst++;
    } else {
      free(t->volumes[i].label);
    }
  }
  free(t->volumes);
  t->volumes = next;
  t->volume_count = dst;
  t->volume_cap = dst > 0 ? dst : 1;
}

uint32_t mount_registry_finalize_digest(mount_registry_t *t) {
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

MOUNT_REGISTRY_H = '''#ifndef MOUNTCFG_MOUNT_REGISTRY_H
#define MOUNTCFG_MOUNT_REGISTRY_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  char *label;
  uint32_t passno;
} mount_volume_t;

typedef struct {
  mount_volume_t *volumes;
  size_t volume_count;
  size_t volume_cap;
  const char **pending_refs;
  size_t pending_count;
  uint32_t digest;
} mount_registry_t;

void mount_registry_init(mount_registry_t *t);
void mount_registry_reset(mount_registry_t *t);
int mount_registry_register(mount_registry_t *t, const char *label, uint32_t budget);
void mount_registry_compact(mount_registry_t *t);
uint32_t mount_registry_finalize_digest(mount_registry_t *t);

#ifdef __cplusplus
}
#endif

#endif
'''

MOUNT_REGISTRY_FUZZER = '''#include "mountcfg/mount_registry.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  mount_registry_t t;
  size_t i;
  char label[32];

  if (!data || size == 0 || size > 4096) {
    return 0;
  }
  mount_registry_init(&t);
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
    mount_registry_register(&t, label, (uint32_t)(data[i] + 1));
    i += n > 0 ? n - 1 : 0;
  }
  (void)mount_registry_finalize_digest(&t);
  mount_registry_reset(&t);
  return 0;
}
'''

README = """# mountcfg

mountcfg is a C11 library for Container volume mount orchestration configuration: parse TOML mount manifests, load mountenv runtime limit parameter overlays, merge layers, validate mount pass numbers, and track duplicate-request volume registry during bind mount sequencing.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Mountenv layer** — `KEY=VALUE`, `@mount` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply mountenv overlay keys onto parsed TOML documents
- **Mount policy** — validate `[mount]` tables and register volume pass numbers into a compaction registry
- **Mount gate** — gate request admission on bucket state and capacity
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `mountenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `mount_fuzzer`, `mount_registry_fuzzer`.

## Quick start

```c
#include "mountcfg/mountcfg.h"

TomeDoc *toml = NULL;
TomeError err;
mountcfg_load_toml_memory("[mount]\\nname = \\"api\\"\\nlimit = 1000\\n", 38, &toml, &err);

mountenv_doc_t *env = NULL;
mountcfg_load_mountenv_memory("LIMIT=500\\n", 10, NULL, &env, NULL);
mountcfg_apply_mountenv_to_toml(toml, env);

mountcfg_mountenv_free(env);
mountcfg_toml_free(toml);
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
        (ROOT / "include" / "launchcfg", ROOT / "include" / "mountcfg"),
        (ROOT / "include" / "runenv", ROOT / "include" / "mountenv"),
        (ROOT / "src" / "runenv", ROOT / "src" / "mountenv"),
        (ROOT / "src" / "launchcfg.c", ROOT / "src" / "mountcfg.c"),
        (ROOT / "src" / "launch_merge.c", ROOT / "src" / "mount_merge.c"),
        (ROOT / "src" / "launch_service.c", ROOT / "src" / "mount_policy.c"),
        (ROOT / "fuzz" / "runenv_fuzzer.c", ROOT / "fuzz" / "mountenv_fuzzer.c"),
        (ROOT / "fuzz" / "launch_fuzzer.c", ROOT / "fuzz" / "mount_fuzzer.c"),
        (ROOT / "examples" / "service.toml", ROOT / "examples" / "mount.toml"),
        (ROOT / "examples" / "runtime.env", ROOT / "examples" / "mount.runtime"),
        (ROOT / "fuzz" / "corpus" / "runenv_fuzzer", ROOT / "fuzz" / "corpus" / "mountenv_fuzzer"),
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

    for p in list((ROOT / "include" / "mountenv").glob("*")):
        if "runenv" in p.name:
            p.rename(p.with_name(p.name.replace("runenv", "mountenv")))

    for p in list((ROOT / "src" / "mountenv").glob("*")):
        new_name = p.name.replace("runenv", "mountenv")
        new_name = new_name.replace("runloader", "mountloader")
        new_name = new_name.replace("require_stack", "bind_stack")
        new_name = new_name.replace("require_ctx", "bind_ctx")
        new_name = new_name.replace("runmap", "mountmap")
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    for p in list((ROOT / "include" / "mountcfg").glob("*")):
        if "launch" in p.name:
            p.rename(p.with_name(p.name.replace("launch", "mount")))

    for p in list((ROOT / "fuzz" / "corpus" / "mountenv_fuzzer").glob("*")):
        if p.suffix == ".env":
            p.rename(p.with_suffix(".menv"))


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
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".menv", ".env",
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
    write(ROOT / "include" / "mountcfg" / "mount_policy.h", MOUNT_POLICY_HDR)
    write(ROOT / "include" / "mountcfg" / "mount_gate.h", MOUNT_GATE_HDR)
    write(ROOT / "include" / "mountcfg" / "mount_registry.h", MOUNT_REGISTRY_H)
    write(ROOT / "src" / "mount_policy.c", MOUNT_POLICY_C)
    write(ROOT / "src" / "mount_gate.c", MOUNT_GATE_C)
    write(ROOT / "src" / "mount_registry.c", MOUNT_REGISTRY_C)
    write(ROOT / "fuzz" / "mount_registry_fuzzer.c", MOUNT_REGISTRY_FUZZER)
    write(ROOT / "README.md", README)

    hdr = (ROOT / "include" / "mountcfg" / "mount_merge.h").read_text(encoding="utf-8")
    hdr = hdr.replace("LAYER_MERGE", "MOUNT_MERGE")
    (ROOT / "include" / "mountcfg" / "mount_merge.h").write_text(hdr, encoding="utf-8")

    fuzz = (ROOT / "fuzz" / "mount_fuzzer.c").read_text(encoding="utf-8")
    fuzz = fuzz.replace(
        "mountcfg_apply_mountenv_to_toml(toml, env);",
        "mountcfg_apply_mountenv_to_toml(toml, env);\n"
        "  if (toml) {\n"
        "    mount_registry_t trk;\n"
        "    mount_registry_init(&trk);\n"
        "    mountcfg_validate_mount_manifest(toml, &trk);\n"
        "    (void)mount_registry_finalize_digest(&trk);\n"
        "    mount_registry_reset(&trk);\n"
        "  }",
    )
    fuzz = xform(fuzz)
    fuzz = fuzz.replace("#include \"mountcfg/mount_merge.h\"",
        "#include \"mountcfg/mount_merge.h\"\n#include \"mountcfg/mount_policy.h\"\n#include \"mountcfg/mount_registry.h\"")
    write(ROOT / "fuzz" / "mount_fuzzer.c", fuzz)

    write(ROOT / "examples" / "mount.toml", """[mount]
name = "web-data"
limit = 1000
bind_timeout_ms = 60000
mount_mode = "open"

[[mount.volumes]]
volume = "/var/lib/data"
passno = 1

[[mount.volumes]]
volume = "/var/log/app"
passno = 2

[[mount.volumes]]
volume = "/tmp/cache"
passno = 40
""")

    write(ROOT / "examples" / "mount.runtime", """# Runtime hedging parameters for duplicate-request fanout
MOUNT_AFTER_MS=150
MAX_FANOUT=3
MOUNT_MODE=active
""")

    write(ROOT / "tests" / "test_mount_policy.c", '''#include "mountcfg/mount_policy.h"
#include "mountcfg/mount_registry.h"
#include "tome/tome.h"
#include "unity/unity.h"

void test_mount_policy_requires_name(void) {
  TomeDoc *doc = NULL;
  TomeError err;
  mount_registry_t t;
  TEST_ASSERT_EQUAL(TOME_OK, tome_parse("[mount]\\nname=\\"x\\"\\n", 20, &doc, &err));
  mount_registry_init(&t);
  TEST_ASSERT_EQUAL(0, mountcfg_validate_mount_manifest(doc, &t));
  mount_registry_reset(&t);
  tome_free(doc);
}
''')

    write(ROOT / "tests" / "test_mount_registry.c", '''#include "mountcfg/mount_registry.h"
#include "unity/unity.h"

void test_mount_registry_register(void) {
  mount_registry_t t;
  mount_registry_init(&t);
  TEST_ASSERT_EQUAL(0, mount_registry_register(&t, "a", 100));
  TEST_ASSERT_EQUAL(0, mount_registry_register(&t, "b", 200));
  mount_registry_reset(&t);
}
''')


def plant_bugs() -> None:
    """Plant standard 5-bug set; bug3 is emergent mount_registry UAF, not shallow hex OOB."""
    unesc = (ROOT / "src" / "mountenv" / "unescape.c").read_text(encoding="utf-8")
    unesc = unesc.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "mountenv" / "unescape.c").write_text(unesc, encoding="utf-8")

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
        "for f in mountcfg mount_merge; do",
        "for f in mountcfg mount_merge mount_policy mount_gate mount_registry; do",
    )
    build_sh = build_sh.replace(
        "build_fuzzer mount_fuzzer.c mount_fuzzer",
        "build_fuzzer mount_fuzzer.c mount_fuzzer\n"
        "build_fuzzer mount_registry_fuzzer.c mount_registry_fuzzer",
    )
    build_sh = build_sh.replace("compile_runenv", "compile_mountenv")
    build_sh = build_sh.replace("src/runenv/", "src/mountenv/")
    build_sh = build_sh.replace('local obj="env_', 'local obj="menv_')
    build_sh = build_sh.replace("env_*.o", "menv_*.o")
    build_sh = build_sh.replace(
        "build_fuzzer runenv_fuzzer.c runenv_fuzzer",
        "build_fuzzer mountenv_fuzzer.c mountenv_fuzzer",
    )
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build_sh, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    wsl = wsl.replace("runenv_*.o toml_*.o launchcfg.o launch_merge.o",
                      "menv_*.o toml_*.o mountcfg.o mount_merge.o mount_policy.o mount_gate.o mount_registry.o")
    (ROOT / "build" / "wsl_build.sh").write_text(wsl, encoding="utf-8")

    proj = (ROOT / ".clusterfuzzlite" / "project.yaml").read_text(encoding="utf-8")
    proj = xform(proj)
    if "mount_registry_fuzzer" not in proj:
        proj = proj.replace(
            "- mount_fuzzer",
            "- mount_fuzzer\n  - mount_registry_fuzzer",
        )
    (ROOT / ".clusterfuzzlite" / "project.yaml").write_text(proj, encoding="utf-8")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "crash-" not in gitignore:
        gitignore += "\ncrash-*\n/poc/\n"
    (ROOT / ".gitignore").write_text(gitignore, encoding="utf-8")

    write(ROOT / "fuzz" / "corpus" / "mount_fuzzer" / "sample.bin",
          bytes([32]) + b"[mount]\nname=\"api\"\nbind_timeout_ms=100\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "mount_registry_fuzzer" / "seed.bin", bytes(range(32, 96)))


def write_artifacts() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    tasks = """# mountcfg task queue

GitHub: tolossamuel/mountcfg

| # | Bug | Harness | Class | Status |
|---|-----|---------|-------|--------|
| 1 | mountenv entry realloc leak | mountenv_fuzzer | LeakSanitizer | Ready |
| 2 | toml audit key leak | toml_fuzzer | LeakSanitizer | Ready |
| 3 | mount registry volume UAF | mount_registry_fuzzer | heap-use-after-free | Ready |
| 4 | toml merge UAF | toml_merge_fuzzer | heap-use-after-free | Ready |
| 5 | toml format null deref | toml_format_fuzzer | null deref | Ready |

PoC bytes and patches: ../artifacts/mountcfg/poc/ (not on GitHub).
"""
    write(ARTIFACTS / "TASKS.md", tasks)

    wsl_test = '''#!/bin/bash
set -eu
cd "$(dirname "$0")/../../mountcfg"
ROOT="$PWD"
ARTIFACTS_ROOT="${ARTIFACTS_ROOT:-$(dirname "$ROOT")/artifacts/mountcfg}"
POC="$ARTIFACTS_ROOT/poc/verified"
OUT=/tmp/mountcfg_out
FAIL=0

if [ ! -d "$POC" ]; then
  echo "Missing PoC corpus: $POC" >&2
  exit 1
fi

if [ ! -x "$OUT/mountenv_fuzzer" ]; then
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

run_leak "Bug1 mountenv entry leak" "$OUT/mountenv_fuzzer" "$POC/entry_leak.menv"
run_leak "Bug2 toml audit leak" "$OUT/toml_fuzzer" "$POC/entry_leak.toml"
run_crash "Bug3 mount registry UAF" "$OUT/mount_registry_fuzzer" "$POC/registry_uaf.bin"
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
    out = Path("/tmp/mountcfg_out")

    write(poc_dir / "entry_leak.menv", "MOUNT_KEY=1\n")
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
        ("bug1_mountenv_entry_leak.patch", "src/mountenv/store.c",
         lambda t: t.replace(
             "  mountenv_doc_impl_t *d = (mountenv_doc_impl_t *)doc;\n  mountenv_arena_free",
             "  mountenv_doc_impl_t *d = (mountenv_doc_impl_t *)doc;\n  free(d->entries);\n  mountenv_arena_free",
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
        ("bug3_mount_registry_uaf.patch", "src/mount_registry.c",
         lambda t: t.replace(
             "  free(t->volumes);\n  free(t->pending_refs);",
             "  free(t->volumes);\n  for (i = 0; i < t->pending_count; i++) {\n    free((void *)t->pending_refs[i]);\n  }\n  free(t->pending_refs);",
         ).replace(
             "        t->pending_refs[t->pending_count++] = t->volumes[i].label;",
             "        char *snap = strdup(t->volumes[i].label ? t->volumes[i].label : \"\");\n        if (!snap) {\n          return -1;\n        }\n        t->pending_refs[t->pending_count++] = snap;",
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
            "A memory leak occurs when parsing a mountenv assignment: mountenv_set_entry "
            "reallocates internal entry storage, but that heap memory is not freed when "
            "mountenv_doc_destroy runs in src/mountenv/store.c."
        ),
        "bug2_TASK_DESCRIPTION.txt": (
            "A memory leak occurs in tome_free in src/toml/parser.c when TOML parsing records "
            "table-header audit keys: doc_audit_key heap-allocates key copies that are never "
            "released when the document is destroyed."
        ),
        "bug3_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in mount_registry_finalize_digest in src/mount_registry.c "
            "when FNV digest finalization reads volume label bytes through pending references "
            "registered before mount_registry_compact reallocates and frees the original label "
            "storage during multi-volume registration in the mount registry pipeline, triggered "
            "via mount_registry_fuzzer."
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
