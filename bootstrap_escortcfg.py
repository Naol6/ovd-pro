#!/usr/bin/env python3
"""Bootstrap escortcfg — C++ escort sidecar proxy attachment + escortenv overlays."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/escortcfg")
SRC = Path("/home/samuel/Documents/fenrir3/canarycfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/escortcfg")

# Order: longest / most specific first.
TEXT_RENAME = [
    ("canarycfg_validate_canary_manifest", "escortcfg_validate_escort_manifest"),
    ("canarycfg_apply_canaryenv_to_toml", "escortcfg_apply_escortenv_to_toml"),
    ("canarycfg_load_canaryenv_memory", "escortcfg_load_escortenv_memory"),
    ("canarycfg_canaryenv_free", "escortcfg_escortenv_free"),
    ("canarycfg_load_toml_memory", "escortcfg_load_toml_memory"),
    ("canarycfg_toml_free", "escortcfg_toml_free"),
    ("canarycfg_default_options", "escortcfg_default_options"),
    ("canarycfg_options_t", "escortcfg_options_t"),
    ("split_ladder_t", "port_map_t"),
    ("split_ladder_", "port_map_"),
    ("split_ladder", "port_map"),
    ("split_step_t", "port_slot_t"),
    ("split_step", "port_slot"),
    ("rollout_meter_t", "mirror_queue_t"),
    ("rollout_meter_", "mirror_queue_"),
    ("rollout_meter", "mirror_queue"),
    ("ramp_entry_t", "mirror_entry_t"),
    ("ramp_entry", "mirror_entry"),
    ("baseline_tracker_t", "route_weight_t"),
    ("baseline_tracker_", "route_weight_"),
    ("baseline_tracker", "route_weight"),
    ("promotion_gate_", "attach_gate_"),
    ("promotion_gate", "attach_gate"),
    ("canary_coordinator", "escort_coordinator"),
    ("canary_merge", "escort_merge"),
    ("canary_fuzzer", "escort_fuzzer"),
    ("canaryenv_doc_impl_t", "escortenv_doc_impl_t"),
    ("canaryenv_doc_t", "escortenv_doc_t"),
    ("canaryenv_error_t", "escortenv_error_t"),
    ("canaryenv_options_t", "escortenv_options_t"),
    ("canaryenv_entry_t", "escortenv_entry_t"),
    ("canaryenv_slice_t", "escortenv_slice_t"),
    ("canaryenv_arena_t", "escortenv_arena_t"),
    ("canaryenv_token_kind_t", "escortenv_token_kind_t"),
    ("canaryenv_token_t", "escortenv_token_t"),
    ("canaryenv_internal.h", "escortenv_internal.h"),
    ("include/canaryenv", "include/escortenv"),
    ("src/canaryenv/", "src/escortenv/"),
    ("src/canaryenv", "src/escortenv"),
    ("canaryenv_", "escortenv_"),
    ("CANARYENV_", "ESCORTENV_"),
    ("Canaryenv", "Escortenv"),
    ("canaryenv", "escortenv"),
    ("ramp_stack", "attach_stack"),
    ("ramp_ctx", "attach_ctx"),
    ("@ramp", "@attach"),
    ("canarymap", "escortmap"),
    ("canaryloader", "escortloader"),
    ("CANARYCFG", "ESCORTCFG"),
    ("CanaryCfg", "EscortCfg"),
    ("canarycfg", "escortcfg"),
    ("CANARY_", "ESCORT_"),
    ("tolossamuel/canarycfg", "tolossamuel/escortcfg"),
    ("/tmp/canarycfg_out", "/tmp/escortcfg_out"),
    ("compile_canaryenv", "compile_escortenv"),
    (".cenv", ".eenv"),
    ("Progressive canary deployment traffic ramp orchestration",
     "Escort sidecar proxy attachment orchestration for microservices"),
    ("progressive canary deployment traffic ramp orchestration",
     "escort sidecar proxy attachment orchestration for microservices"),
    ("canaryenv runtime ramp overlays", "escortenv runtime attach overlays"),
    ("Canaryenv layer", "Escortenv layer"),
    ("Canary coordinator validation", "Escort coordinator validation"),
    ("promotion state gates", "attachment state gates"),
    ("traffic split ladders", "container port mapping tables"),
    ("rollout ramp meters", "traffic mirror queues"),
    ("[canary]", "[escort]"),
    ("canary.steps", "escort.ports"),
    ("promotion", "attach"),
    ("ramp_interval_ms", "mirror_interval_ms"),
    ("promotion_mode", "escort_mode"),
    ("RAMP_GENERATION", "ATTACH_GENERATION"),
    ("PROMOTION_MODE", "ESCORT_MODE"),
    ("RAMP_INTERVAL_MS", "MIRROR_INTERVAL_MS"),
    ('"steps"', '"ports"'),
    ('"step"', '"port"'),
    ("stable-v1", "primary-svc"),
    ("canary-v2", "escort-proxy"),
    ("canary deployment", "escort attachment"),
    ("canary.toml", "escort.toml"),
    ("canary.runtime", "escort.runtime"),
    ("Canary", "Escort"),
    ("canary", "escort"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

NAME_SUBS = [
    ("baseline_tracker", "route_weight"),
    ("rollout_meter", "mirror_queue"),
    ("split_ladder", "port_map"),
    ("promotion_gate", "attach_gate"),
    ("canary_coordinator", "escort_coordinator"),
    ("canary_merge", "escort_merge"),
    ("canary_fuzzer", "escort_fuzzer"),
    ("canaryenv_fuzzer", "escortenv_fuzzer"),
    ("canaryloader", "escortloader"),
    ("canaryenv_internal", "escortenv_internal"),
    ("canaryenv_types", "escortenv_types"),
    ("canaryenv", "escortenv"),
    ("canarymap", "escortmap"),
    ("canarycfg", "escortcfg"),
    ("ramp_stack", "attach_stack"),
    ("ramp_ctx", "attach_ctx"),
    ("canary.runtime", "escort.runtime"),
    ("canary.toml", "escort.toml"),
]

DIR_RENAMES = [
    ("include/canarycfg", "include/escortcfg"),
    ("include/canaryenv", "include/escortenv"),
    ("src/canaryenv", "src/escortenv"),
    ("fuzz/corpus/canaryenv_fuzzer", "fuzz/corpus/escortenv_fuzzer"),
    ("fuzz/corpus/canary_fuzzer", "fuzz/corpus/escort_fuzzer"),
    ("fuzz/corpus/split_ladder_fuzzer", "fuzz/corpus/port_map_fuzzer"),
    ("fuzz/corpus/rollout_meter_fuzzer", "fuzz/corpus/mirror_queue_fuzzer"),
    ("fuzz/corpus/baseline_tracker_fuzzer", "fuzz/corpus/route_weight_fuzzer"),
]

COMMITS_RAW = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add escortcfg public headers", [
        "include/escortcfg/escortcfg.h", "include/escortcfg/escort_merge.h"]),
    ("include: add escortenv public API", [
        "include/escortenv/escortenv.h", "include/escortenv/escortenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add escort coordinator and port map headers", [
        "include/escortcfg/escort_coordinator.h", "include/escortcfg/attach_gate.h",
        "include/escortcfg/port_map.h", "include/escortcfg/mirror_queue.h"]),
    ("include: add route weight header", ["include/escortcfg/route_weight.h"]),
    ("src/escortenv: add buffer and string utilities", [
        "src/escortenv/buffer.cpp", "src/escortenv/buffer.h", "src/escortenv/strutil.cpp",
        "src/escortenv/strutil.h"]),
    ("src/escortenv: add arena allocator", [
        "src/escortenv/arena.cpp", "src/escortenv/arena.h", "src/escortenv/escortenv_internal.h"]),
    ("src/escortenv: add error helpers", ["src/escortenv/error.cpp", "src/escortenv/error.h"]),
    ("src/escortenv: add UTF-8 validation", ["src/escortenv/utf8.cpp", "src/escortenv/utf8.h"]),
    ("src/escortenv: implement escortenv line lexer", ["src/escortenv/lexer.cpp", "src/escortenv/lexer.h"]),
    ("src/escortenv: add quoted value unescape", ["src/escortenv/unescape.cpp", "src/escortenv/unescape.h"]),
    ("src/escortenv: add document store", ["src/escortenv/store.cpp", "src/escortenv/store.h"]),
    ("src/escortenv: wire assignment parser", ["src/escortenv/parser.cpp", "src/escortenv/parser.h"]),
    ("src/escortenv: add serialize to escortenv text", ["src/escortenv/serialize.cpp", "src/escortenv/serialize.h"]),
    ("src/escortenv: add validation pass", ["src/escortenv/validate.cpp", "src/escortenv/validate.h"]),
    ("src/escortenv: add merge overlay", ["src/escortenv/merge.cpp", "src/escortenv/merge.h"]),
    ("src/escortenv: add expand and coerce", [
        "src/escortenv/expand.cpp", "src/escortenv/expand.h", "src/escortenv/coerce.cpp",
        "src/escortenv/coerce.h"]),
    ("src/escortenv: add walk query diff", [
        "src/escortenv/walk.cpp", "src/escortenv/walk.h", "src/escortenv/query.cpp",
        "src/escortenv/query.h", "src/escortenv/diff.cpp", "src/escortenv/diff.h"]),
    ("src/escortenv: add pretty printer", ["src/escortenv/pretty.cpp", "src/escortenv/pretty.h"]),
    ("src/escortenv: add attach stack and ctx", [
        "src/escortenv/attach_stack.cpp", "src/escortenv/attach_stack.h",
        "src/escortenv/attach_ctx.cpp", "src/escortenv/attach_ctx.h"]),
    ("src/escortenv: add path filter profile", [
        "src/escortenv/path.cpp", "src/escortenv/path.h", "src/escortenv/filter.cpp",
        "src/escortenv/filter.h", "src/escortenv/profile.cpp", "src/escortenv/profile.h"]),
    ("src/escortenv: add snapshot readutil strict canonical", [
        "src/escortenv/snapshot.cpp", "src/escortenv/snapshot.h", "src/escortenv/readutil.cpp",
        "src/escortenv/readutil.h", "src/escortenv/strict.cpp", "src/escortenv/strict.h",
        "src/escortenv/canonical.cpp", "src/escortenv/canonical.h"]),
    ("src/escortenv: add escortloader and main escortenv module", [
        "src/escortenv/escortloader.cpp", "src/escortenv/escortenv.cpp", "src/escortenv/escortmap.cpp",
        "src/escortenv/escortmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.cpp", "src/toml/buffer.cpp"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.cpp", "src/toml/datetime.cpp", "src/toml/lexer.cpp"]),
    ("src/toml: add value and parser core", ["src/toml/value.cpp", "src/toml/parser.cpp"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.cpp", "src/toml/merge.cpp", "src/toml/serialize.cpp"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.cpp", "src/toml/format.cpp", "src/toml/validator.cpp", "src/toml/document.cpp"]),
    ("src: add escortcfg bridge and escortenv-to-toml merge", ["src/escortcfg.cpp", "src/escort_merge.cpp"]),
    ("src: add escort coordinator validator", ["src/escort_coordinator.cpp"]),
    ("src: add attach gate evaluator", ["src/attach_gate.cpp"]),
    ("src: add port map slot tracker", ["src/port_map.cpp"]),
    ("src: add mirror queue for traffic duplication", ["src/mirror_queue.cpp"]),
    ("src: add route weight accumulator", ["src/route_weight.cpp"]),
    ("tests: add Unity harness", ["tests/unity/unity.cpp", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.cpp", "tests/test_basic.cpp"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.cpp", "tests/test_merge.cpp", "tests/test_validate.cpp"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.cpp", "tests/test_coerce.cpp", "tests/test_integration.cpp",
        "tests/test_scenarios.cpp"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.cpp", "tests/test_lexer_exhaustive.cpp"]),
    ("tests: add escort coordinator and port map unit tests", [
        "tests/test_escort_coordinator.cpp", "tests/test_port_map.cpp"]),
    ("tests: add mirror queue and route weight unit tests", [
        "tests/test_mirror_queue.cpp", "tests/test_route_weight.cpp"]),
    ("examples: add TOML escort manifest and runtime overlay", [
        "examples/escort.toml", "examples/escort.runtime"]),
    ("fuzz: add escortenv_fuzzer harness", ["fuzz/escortenv_fuzzer.cc"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.cc"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.cc"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.cc"]),
    ("fuzz: add escort_fuzzer for cross-format overlay", ["fuzz/escort_fuzzer.cc"]),
    ("fuzz: add port_map_fuzzer for compaction path", ["fuzz/port_map_fuzzer.cc"]),
    ("fuzz: add mirror_queue_fuzzer for mirror path", ["fuzz/mirror_queue_fuzzer.cc"]),
    ("fuzz: add route_weight_fuzzer for weight path", ["fuzz/route_weight_fuzzer.cc"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/escortenv_fuzzer/minimal.eenv",
        "fuzz/corpus/escortenv_fuzzer/quoted.eenv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/escort_fuzzer/sample.bin",
        "fuzz/corpus/port_map_fuzzer/seed.bin",
        "fuzz/corpus/mirror_queue_fuzzer/seed.bin",
        "fuzz/corpus/route_weight_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for escortcfg library", ["README.md"]),
    ("docs: add BUILDING notes", ["docs/BUILDING.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable escort sidecar attachment library", []),
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


def rename_all_paths() -> None:
    paths = sorted(
        [p for p in ROOT.rglob("*") if p != ROOT],
        key=lambda p: len(str(p)),
        reverse=True,
    )
    for path in paths:
        if not path.exists():
            continue
        rel = path.relative_to(ROOT).as_posix()
        new_rel = rel
        for old, new in NAME_SUBS:
            new_rel = new_rel.replace(old, new)
        if new_rel == rel:
            continue
        target = ROOT / new_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        path.rename(target)


def copy_tree() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ignore = shutil.ignore_patterns(".git", "*.o", "__pycache__", "poc", "guides")
    shutil.copytree(SRC, ROOT, ignore=ignore)

    for old_rel, new_rel in DIR_RENAMES:
        old = ROOT / old_rel
        new = ROOT / new_rel
        if not old.exists():
            continue
        new.parent.mkdir(parents=True, exist_ok=True)
        if new.exists():
            if new.is_dir():
                shutil.rmtree(new)
            else:
                new.unlink()
        old.rename(new)

    rename_all_paths()

    corp = ROOT / "fuzz" / "corpus" / "escortenv_fuzzer"
    if corp.exists():
        for old in list(corp.glob("*.cenv")):
            old.rename(old.with_suffix(".eenv"))


def transform_contents() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.name in SKIP_FILES:
            path.unlink(missing_ok=True)
            continue
        if path.suffix not in {
            ".cpp", ".h", ".cc", ".sh", ".yaml", ".md", ".txt", ".toml",
            ".eenv", ".cenv", ".env", "Makefile"
        } and path.name not in {"Makefile", ".gitignore", "LICENSE"}:
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


def patch_coordinator() -> None:
    path = ROOT / "src" / "escort_coordinator.cpp"
    text = path.read_text(encoding="utf-8")
    text = text.replace('tome_table_get(tbl, "steps")', 'tome_table_get(tbl, "ports")')
    text = text.replace('"step"', '"port"')
    path.write_text(text, encoding="utf-8")


README = """# escortcfg

escortcfg is a C++17 library for **escort sidecar proxy attachment orchestration**: parse TOML escort manifests, load escortenv runtime attach overlays, merge layers, validate attachment state gates, and track container port mapping tables plus traffic mirror queues.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Escortenv layer** — `KEY=VALUE`, `@attach` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply escortenv overlay keys onto parsed TOML documents
- **Escort coordinator** — validate `[escort]` tables and register port weights into a port map
- **Mirror queue** — track mirror cadence across escort attachment epochs
- **Route weight** — accumulate weighted routing scores during progressive attachment
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `escortenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `escort_fuzzer`, `port_map_fuzzer`, `mirror_queue_fuzzer`, `route_weight_fuzzer`.

## License

MIT — see LICENSE.
"""

BUILDING = """# Building escortcfg

## Requirements

- clang/clang++ 14+
- libFuzzer (via `-fsanitize=fuzzer` or `$LIB_FUZZING_ENGINE`)

## Local ASan build

```bash
bash build/wsl_build.sh
```

Fuzzers land in `/tmp/escortcfg_out/`.

## Unit tests

```bash
make test
```
"""


def add_domain() -> None:
    write(ROOT / "README.md", README)
    write(ROOT / "docs" / "BUILDING.md", BUILDING)

    write(ROOT / "examples" / "escort.toml", """[escort]
name = "checkout-api"
mirror_interval_ms = 60000
escort_mode = "linear"

[[escort.ports]]
label = "primary-svc"
weight = 90

[[escort.ports]]
label = "escort-proxy"
weight = 10
""")

    write(ROOT / "examples" / "escort.runtime", """# Runtime escort attach parameters injected during attachment
MIRROR_INTERVAL_MS=30000
ESCORT_MODE=linear
ATTACH_GENERATION=2
""")

    write(ROOT / "tests" / "test_route_weight.cpp", '''#include "escortcfg/route_weight.h"
#include "unity/unity.h"

void test_route_weight_score(void) {
  route_weight_t rw;
  route_weight_init(&rw);
  TEST_ASSERT_EQUAL(0, route_weight_note_bind(&rw, "primary-svc", 3));
  TEST_ASSERT_EQUAL(0, route_weight_note_escort(&rw, "escort-proxy"));
  TEST_ASSERT_NOT_EQUAL(0u, route_weight_score(&rw));
  route_weight_reset(&rw);
}
''')

    write(ROOT / "fuzz" / "corpus" / "escort_fuzzer" / "sample.bin",
          bytes([32]) + b"[escort]\nname=\"x\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "port_map_fuzzer" / "seed.bin", bytes(range(32, 96)))
    write(ROOT / "fuzz" / "corpus" / "mirror_queue_fuzzer" / "seed.bin", bytes(range(16, 128)))
    write(ROOT / "fuzz" / "corpus" / "route_weight_fuzzer" / "seed.bin", bytes(range(8, 64)))


def plant_bugs() -> None:
    """Keep hardened unescape; plant escortenv empty-serialize null deref for bug5."""
    ser = (ROOT / "src" / "escortenv" / "serialize.cpp").read_text(encoding="utf-8")
    ser = ser.replace(
        "  if (buf.len > 0) {\n"
        "    memcpy(*out_buf, buf.data, buf.len + 1);\n"
        "  } else {\n"
        "    (*out_buf)[0] = '\\0';\n"
        "  }",
        "  memcpy(*out_buf, buf.data, buf.len + 1);",
    )
    (ROOT / "src" / "escortenv" / "serialize.cpp").write_text(ser, encoding="utf-8")


def patch_build() -> None:
    build_sh = '''#!/bin/bash -eu

OBJECTS=()

compile_escortenv() {
  local base="$1"
  local obj="escortenv_${base%.cpp}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall -D_GNU_SOURCE} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/escortenv" \\
    -c "${SRC:-.}/src/escortenv/${base}" -o "${obj}"
  OBJECTS+=("${obj}")
}

compile_toml() {
  local base="$1"
  local obj="toml_${base%.cpp}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/toml" \\
    -c "${SRC:-.}/src/toml/${base}" -o "${obj}"
  OBJECTS+=("${obj}")
}

for f in buffer strutil error arena utf8 store unescape lexer parser serialize \\
         validate merge expand coerce walk query diff pretty attach_stack \\
         attach_ctx path filter escortmap profile canonical strict readutil \\
         snapshot escortloader escortenv; do
  if [ -f "${SRC:-.}/src/escortenv/${f}.cpp" ]; then
    compile_escortenv "${f}.cpp"
  fi
done

for f in memory buffer unicode datetime lexer value parser path merge serialize \\
         diag format validator document; do
  compile_toml "${f}.cpp"
done

for f in escortcfg escort_merge escort_coordinator attach_gate port_map mirror_queue route_weight; do
  obj="${f}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/escortenv" -I"${SRC:-.}/src/toml" \\
    -c "${SRC:-.}/src/${f}.cpp" -o "${obj}"
  OBJECTS+=("${obj}")
done

FUZZ_CXXFLAGS="${CXXFLAGS:- -O1 -g -std=c++17}"
INCS="-I${SRC:-.}/include -I${SRC:-.}/src/escortenv -I${SRC:-.}/src/toml"

build_fuzzer() {
  ${CXX:-clang++} ${FUZZ_CXXFLAGS} ${LIB_FUZZING_ENGINE} \\
    "${SRC:-.}/fuzz/$1" "${OBJECTS[@]}" ${INCS} \\
    -o "${OUT:-.}/$2" -lm
}

build_fuzzer escortenv_fuzzer.cc escortenv_fuzzer
build_fuzzer toml_fuzzer.cc toml_fuzzer
build_fuzzer toml_merge_fuzzer.cc toml_merge_fuzzer
build_fuzzer toml_format_fuzzer.cc toml_format_fuzzer
build_fuzzer escort_fuzzer.cc escort_fuzzer
build_fuzzer port_map_fuzzer.cc port_map_fuzzer
build_fuzzer mirror_queue_fuzzer.cc mirror_queue_fuzzer
build_fuzzer route_weight_fuzzer.cc route_weight_fuzzer
'''
    write(ROOT / ".clusterfuzzlite/build.sh", build_sh)

    wsl = '''#!/bin/bash -eu
set -o pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${OUT:-/tmp/escortcfg_out}"
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
  - escortenv_fuzzer
  - toml_fuzzer
  - toml_merge_fuzzer
  - toml_format_fuzzer
  - escort_fuzzer
  - port_map_fuzzer
  - mirror_queue_fuzzer
  - route_weight_fuzzer
'''
    write(ROOT / ".clusterfuzzlite/project.yaml", proj)

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
CXXFLAGS ?= -std=c++17 -O2 -g -Wall -Wextra -Wpedantic -Werror -Iinclude -Isrc/escortenv -Isrc/toml
ESCORTENV_SRC := $(wildcard src/escortenv/*.cpp)
TOML_SRC := $(wildcard src/toml/*.cpp)
CORE_SRC := src/escortcfg.cpp src/escort_merge.cpp src/escort_coordinator.cpp src/attach_gate.cpp src/port_map.cpp src/mirror_queue.cpp src/route_weight.cpp
TEST_SRC := $(wildcard tests/test_*.cpp)
TEST := build/escortcfg_tests

$(TEST): $(ESCORTENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) | build
\t$(CXX) $(CXXFLAGS) $(ESCORTENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) -o $@

build:
\tmkdir -p build

test: $(TEST)
\t$(TEST)

fuzz:
\trm -rf out && OUT=$$(pwd)/out CXX=clang++ bash .clusterfuzzlite/build.sh

clean:
\trm -f $(TEST)
\trm -rf out
.PHONY: test fuzz clean
'''
    write(ROOT / "Makefile", makefile)


def init_git() -> None:
    git_dir = ROOT / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)
    subprocess.check_call(["git", "init", "-b", "main"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.name", "tolossamuel"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.email", "tolossamuel@users.noreply.github.com"], cwd=ROOT)
    for msg, files in COMMITS_RAW:
        staged = False
        for rel in files:
            p = ROOT / rel
            if p.exists():
                subprocess.check_call(["git", "add", rel], cwd=ROOT)
                staged = True
        if not files:
            subprocess.check_call(["git", "add", "-A"], cwd=ROOT)
            staged = True
        if staged:
            subprocess.check_call(["git", "commit", "-m", msg], cwd=ROOT)
        else:
            print(f"skip empty commit: {msg}")
    n = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()
    print(f"Created {n} commits")


def apply_patch_and_diff(patch_src: Path, target_file: Path, marker: str, out_patch: Path) -> None:
    """Apply fix locally, git diff, revert — produces verified patch."""
    original = target_file.read_text(encoding="utf-8")
    canary_submit = Path("/home/samuel/Documents/fenrir3/artifacts/canarycfg/poc/submit")
    if patch_src.exists():
        text = patch_src.read_text(encoding="utf-8")
        for old, new in TEXT_RENAME:
            text = text.replace(old, new)
        # apply unified diff
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".patch", delete=False) as tf:
            tf.write(text)
            tf.flush()
            subprocess.check_call(["git", "apply", tf.name], cwd=ROOT)
        out_patch.write_text(text, encoding="utf-8")
        subprocess.check_call(["git", "checkout", "--", str(target_file.relative_to(ROOT))], cwd=ROOT)
        return
    raise FileNotFoundError(patch_src)


def create_artifacts() -> None:
    poc_dir = ARTIFACTS / "poc"
    verified = poc_dir / "verified"
    submit = poc_dir / "submit"
    verified.mkdir(parents=True, exist_ok=True)
    submit.mkdir(parents=True, exist_ok=True)

    write(verified / "entry_leak.eenv", "FOO=1\n")
    write(verified / "audit_leak.toml", 'k = "v"\n')
    write(verified / "empty_serialize.eenv", b"")
    write(verified / "port_map_uaf.bin", bytes(range(32, 160)))

    canary_verified = Path("/home/samuel/Documents/fenrir3/artifacts/canarycfg/poc/verified")
    if (canary_verified / "merge_uaf.bin").exists():
        shutil.copy(canary_verified / "merge_uaf.bin", verified / "merge_uaf.bin")

    write(poc_dir / "README.txt", """escortcfg local artifacts — NOT on GitHub

verified/
  entry_leak.eenv           — bug1 escortenv entry realloc leak
  audit_leak.toml           — bug2 toml audit key leak
  port_map_uaf.bin          — bug3 port map compaction UAF
  merge_uaf.bin             — bug4 toml merge overlay index UAF
  empty_serialize.eenv      — bug5 escortenv empty serialize null deref

submit/
  bugN_*.patch + bugN_TASK_DESCRIPTION.txt

Verify: bash artifacts/escortcfg/wsl_test_pocs.sh
""")

    write(ARTIFACTS / "TASKS.md", """# escortcfg task queue

GitHub: tolossamuel/escortcfg

| # | Bug | Harness | Class | Status |
|---|-----|---------|-------|--------|
| 1 | escortenv entry realloc leak | escortenv_fuzzer | LeakSanitizer | Ready |
| 2 | toml audit key leak | toml_fuzzer | LeakSanitizer | Ready |
| 3 | port map compaction UAF | port_map_fuzzer | heap-use-after-free | Ready |
| 4 | toml merge UAF | toml_merge_fuzzer | heap-use-after-free | Ready |
| 5 | escortenv empty serialize null deref | escortenv_fuzzer | null deref | Ready |

PoC bytes and patches: artifacts/escortcfg/poc/ (not on GitHub).
""")

    wsl_test = '''#!/bin/bash -eu
ROOT="$(cd "$(dirname "$0")/../../escortcfg" && pwd)"
POC="${POC_DIR:-$(dirname "$0")/poc/verified}"
OUT="${OUT:-/tmp/escortcfg_out}"

cd "$ROOT"
CC=clang CXX=clang++ bash build/wsl_build.sh >/dev/null

fail() { echo "FAIL: $*"; exit 1; }
pass() { echo "PASS: $*"; }

if ASAN_OPTIONS=detect_leaks=1 "$OUT/escortenv_fuzzer" "$POC/entry_leak.eenv" >/dev/null 2>&1; then
  fail "bug1 should leak on unpatched build"
fi
pass "bug1 escortenv entry leak reproduces"

if ASAN_OPTIONS=detect_leaks=1 "$OUT/toml_fuzzer" "$POC/audit_leak.toml" >/dev/null 2>&1; then
  fail "bug2 should leak on unpatched build"
fi
pass "bug2 toml audit leak reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/port_map_fuzzer" "$POC/port_map_uaf.bin" >/dev/null 2>&1; then
  fail "bug3 should UAF on unpatched build"
fi
pass "bug3 port map UAF reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/toml_merge_fuzzer" "$POC/merge_uaf.bin" >/dev/null 2>&1; then
  fail "bug4 should UAF on unpatched build"
fi
pass "bug4 toml merge UAF reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/escortenv_fuzzer" "$POC/empty_serialize.eenv" >/dev/null 2>&1; then
  fail "bug5 should crash on unpatched build"
fi
pass "bug5 escortenv empty serialize null deref reproduces"

echo "All unpatched PoCs verified."
'''
    write(ARTIFACTS / "wsl_test_pocs.sh", wsl_test)
    (ARTIFACTS / "wsl_test_pocs.sh").chmod(0o755)


def generate_patches() -> None:
    submit = ARTIFACTS / "poc" / "submit"
    canary_submit = Path("/home/samuel/Documents/fenrir3/artifacts/canarycfg/poc/submit")

    patch_map = [
        ("bug1_escortenv_entry_leak.patch", canary_submit / "bug1_canaryenv_entry_leak.patch"),
        ("bug2_toml_audit_leak.patch", canary_submit / "bug2_toml_audit_leak.patch"),
        ("bug3_port_map_uaf.patch", canary_submit / "bug3_split_ladder_uaf.patch"),
        ("bug4_toml_merge_uaf.patch", canary_submit / "bug4_toml_merge_uaf.patch"),
        ("bug5_escortenv_empty_serialize_null_deref.patch",
         canary_submit / "bug5_canaryenv_empty_serialize_null_deref.patch"),
    ]
    for out_name, src in patch_map:
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        for old, new in TEXT_RENAME:
            text = text.replace(old, new)
        write(submit / out_name, text)

    tasks = {
        "bug1_TASK_DESCRIPTION.txt": (
            "A memory leak occurs when parsing an escortenv assignment: escortenv_set_entry "
            "reallocates internal entry storage, but that heap memory is not freed when "
            "escortenv_doc_destroy runs in src/escortenv/store.cpp."
        ),
        "bug2_TASK_DESCRIPTION.txt": (
            "A memory leak occurs in the TOML document audit key path when toml_parse "
            "records assignment keys into doc->audit_keys without releasing them during "
            "document teardown in src/toml/document.cpp."
        ),
        "bug3_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in port_map_finalize_digest in src/port_map.cpp "
            "when digest finalization reads port label bytes through pending references registered "
            "before port_map_compact reallocates and frees the original label storage during "
            "multi-slot registration in the port map compaction pipeline, triggered via port_map_fuzzer."
        ),
        "bug4_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs during TOML table merge in src/toml/merge.cpp when "
            "merge_table_in_place caches overlay entry key pointers then rebuilds the overlay "
            "table index mid-loop, leaving stale key references that are read on subsequent merge "
            "iterations via toml_merge_fuzzer."
        ),
        "bug5_TASK_DESCRIPTION.txt": (
            "A null pointer dereference occurs in escortenv_serialize_doc in src/escortenv/serialize.cpp "
            "when serializing a document with zero entries copies from buf.data even though the "
            "internal buffer was never allocated, triggered via escortenv_fuzzer with zero-length input."
        ),
    }
    for fname, desc in tasks.items():
        write(submit / fname, desc + "\n")


def verify_build_and_pocs() -> None:
    subprocess.check_call(["bash", "build/wsl_build.sh"], cwd=ROOT)
    subprocess.check_call(["bash", str(ARTIFACTS / "wsl_test_pocs.sh")])


def verify_patches() -> None:
    """Each patch must apply, fix its PoC, and revert cleanly."""
    submit = ARTIFACTS / "poc" / "submit"
    verified = ARTIFACTS / "poc" / "verified"
    out = "/tmp/escortcfg_out"
    tests = [
        ("bug1_escortenv_entry_leak.patch", "escortenv_fuzzer", "entry_leak.eenv", "detect_leaks=1", True),
        ("bug2_toml_audit_leak.patch", "toml_fuzzer", "audit_leak.toml", "detect_leaks=1", True),
        ("bug3_port_map_uaf.patch", "port_map_fuzzer", "port_map_uaf.bin", "detect_leaks=0", True),
        ("bug4_toml_merge_uaf.patch", "toml_merge_fuzzer", "merge_uaf.bin", "detect_leaks=0", True),
        ("bug5_escortenv_empty_serialize_null_deref.patch", "escortenv_fuzzer", "empty_serialize.eenv", "detect_leaks=0", True),
    ]
    for patch_name, harness, poc_file, asan, should_pass_after in tests:
        patch = submit / patch_name
        if not patch.exists():
            print(f"SKIP patch verify: {patch_name}")
            continue
        subprocess.check_call(["git", "apply", str(patch)], cwd=ROOT)
        subprocess.check_call(["bash", "build/wsl_build.sh"], cwd=ROOT)
        cmd = f'ASAN_OPTIONS={asan} {out}/{harness} {verified}/{poc_file}'
        rc = subprocess.call(cmd, shell=True, cwd=ROOT)
        if should_pass_after and rc != 0:
            subprocess.check_call(["git", "apply", "-R", str(patch)], cwd=ROOT)
            raise RuntimeError(f"Patch {patch_name} did not fix PoC (exit {rc})")
        subprocess.check_call(["git", "apply", "-R", str(patch)], cwd=ROOT)
    print("All patches verified")


def push_github() -> None:
    subprocess.check_call(
        ["gh", "repo", "create", "tolossamuel/escortcfg",
         "--private",
         "--description", "C++ escort sidecar proxy attachment config library (TOML + escortenv) for ClusterFuzzLite",
         "--source", str(ROOT), "--remote", "origin", "--push"],
    )


def main() -> None:
    copy_tree()
    transform_contents()
    patch_coordinator()
    add_domain()
    plant_bugs()
    patch_build()
    init_git()
    create_artifacts()
    generate_patches()
    verify_build_and_pocs()
    verify_patches()
    push_github()
    n = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()
    loc = subprocess.check_output(
        ["find", "src", "include", "-name", "*.cpp", "-o", "-name", "*.h"],
        cwd=ROOT, text=True,
    ).strip().split("\n")
    print(f"OK escortcfg — {n} commits, {len(loc)} source files")


if __name__ == "__main__":
    main()
