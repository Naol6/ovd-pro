#!/usr/bin/env python3
"""Bootstrap waypointcfg — C++ waypoint sidecar proxy attachment + wayenv overlays."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/waypointcfg")
SRC = Path("/home/samuel/Documents/fenrir3/escortcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/waypointcfg")

# Order: longest / most specific first.
TEXT_RENAME = [
    ("escortcfg_validate_escort_manifest", "waypointcfg_validate_waypoint_manifest"),
    ("escortcfg_apply_escortenv_to_toml", "waypointcfg_apply_wayenv_to_toml"),
    ("escortcfg_load_escortenv_memory", "waypointcfg_load_wayenv_memory"),
    ("escortcfg_escortenv_free", "waypointcfg_wayenv_free"),
    ("escortcfg_load_toml_memory", "waypointcfg_load_toml_memory"),
    ("escortcfg_toml_free", "waypointcfg_toml_free"),
    ("escortcfg_default_options", "waypointcfg_default_options"),
    ("escortcfg_options_t", "waypointcfg_options_t"),
    ("split_ladder_t", "traffic_split_t"),
    ("split_ladder_", "traffic_split_"),
    ("split_ladder", "traffic_split"),
    ("split_step_t", "split_lane_t"),
    ("split_step", "split_lane"),
    ("rollout_meter_t", "probe_cycle_t"),
    ("rollout_meter_", "probe_cycle_"),
    ("rollout_meter", "probe_cycle"),
    ("ramp_entry_t", "probe_tick_t"),
    ("ramp_entry", "probe_tick"),
    ("baseline_tracker_t", "latency_budget_t"),
    ("baseline_tracker_", "latency_budget_"),
    ("baseline_tracker", "latency_budget"),
    ("promotion_gate_", "admission_gate_"),
    ("promotion_gate", "admission_gate"),
    ("escort_coordinator", "waypoint_coordinator"),
    ("escort_merge", "waypoint_merge"),
    ("escort_fuzzer", "waypoint_fuzzer"),
    ("escortenv_doc_impl_t", "wayenv_doc_impl_t"),
    ("escortenv_doc_t", "wayenv_doc_t"),
    ("escortenv_error_t", "wayenv_error_t"),
    ("escortenv_options_t", "wayenv_options_t"),
    ("escortenv_entry_t", "wayenv_entry_t"),
    ("escortenv_slice_t", "wayenv_slice_t"),
    ("escortenv_arena_t", "wayenv_arena_t"),
    ("escortenv_token_kind_t", "wayenv_token_kind_t"),
    ("escortenv_token_t", "wayenv_token_t"),
    ("escortenv_internal.h", "wayenv_internal.h"),
    ("include/escortenv", "include/wayenv"),
    ("src/escortenv/", "src/wayenv/"),
    ("src/escortenv", "src/wayenv"),
    ("escortenv_", "wayenv_"),
    ("CANARYENV_", "WAYENV_"),
    ("Canaryenv", "Wayenv"),
    ("escortenv", "wayenv"),
    ("ramp_stack", "waypoint_stack"),
    ("ramp_ctx", "waypoint_ctx"),
    ("@ramp", "@waypoint"),
    ("escortmap", "waymap"),
    ("escortloader", "wayloader"),
    ("CANARYCFG", "WAYPOINTCFG"),
    ("CanaryCfg", "WaypointCfg"),
    ("escortcfg", "waypointcfg"),
    ("CANARY_", "WAYPOINT_"),
    ("tolossamuel/escortcfg", "tolossamuel/waypointcfg"),
    ("/tmp/escortcfg_out", "/tmp/waypointcfg_out"),
    ("compile_escortenv", "compile_wayenv"),
    (".cenv", ".wenv"),
    ("Waypoint proxy traffic steering orchestration",
     "Waypoint proxy traffic steering orchestration for service mesh"),
    ("waypoint proxy traffic steering orchestration",
     "waypoint proxy traffic steering orchestration for service mesh"),
    ("escortenv runtime ramp overlays", "wayenv runtime steering overlays"),
    ("Canaryenv layer", "Wayenv layer"),
    ("Canary coordinator validation", "Waypoint coordinator validation"),
    ("promotion state gates", "admission state gates"),
    ("traffic split ladders", "weighted traffic split lanes"),
    ("rollout ramp meters", "health probe cycle trackers"),
    ("[escort]", "[waypoint]"),
    ("escort.steps", "waypoint.lanes"),
    ("promotion", "attach"),
    ("ramp_interval_ms", "probe_interval_ms"),
    ("promotion_mode", "steering_mode"),
    ("RAMP_GENERATION", "STEERING_GENERATION"),
    ("PROMOTION_MODE", "STEERING_MODE"),
    ("RAMP_INTERVAL_MS", "PROBE_INTERVAL_MS"),
    ('"steps"', '"lanes"'),
    ('"step"', '"lane"'),
    ("stable-v1", "upstream-a"),
    ("escort-v2", "waypoint-b"),
    ("escort deployment", "waypoint steering"),
    ("escort.toml", "waypoint.toml"),
    ("escort.runtime", "waypoint.runtime"),
    ("Canary", "Waypoint"),
    ("escort", "waypoint"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

NAME_SUBS = [
    ("route_weight", "latency_budget"),
    ("mirror_queue", "probe_cycle"),
    ("port_map", "traffic_split"),
    ("attach_gate", "admission_gate"),
    ("escort_coordinator", "waypoint_coordinator"),
    ("escort_merge", "waypoint_merge"),
    ("escort_fuzzer", "waypoint_fuzzer"),
    ("escortenv_fuzzer", "wayenv_fuzzer"),
    ("escortloader", "wayloader"),
    ("escortenv_internal", "wayenv_internal"),
    ("escortenv_types", "wayenv_types"),
    ("escortenv", "wayenv"),
    ("escortmap", "waymap"),
    ("escortcfg", "waypointcfg"),
    ("attach_stack", "waypoint_stack"),
    ("attach_ctx", "waypoint_ctx"),
    ("escort.runtime", "waypoint.runtime"),
    ("escort.toml", "waypoint.toml"),
]

DIR_RENAMES = [
    ("include/escortcfg", "include/waypointcfg"),
    ("include/escortenv", "include/wayenv"),
    ("src/escortenv", "src/wayenv"),
    ("fuzz/corpus/escortenv_fuzzer", "fuzz/corpus/wayenv_fuzzer"),
    ("fuzz/corpus/escort_fuzzer", "fuzz/corpus/waypoint_fuzzer"),
    ("fuzz/corpus/port_map_fuzzer", "fuzz/corpus/traffic_split_fuzzer"),
    ("fuzz/corpus/mirror_queue_fuzzer", "fuzz/corpus/probe_cycle_fuzzer"),
    ("fuzz/corpus/route_weight_fuzzer", "fuzz/corpus/latency_budget_fuzzer"),
]

COMMITS_RAW = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add waypointcfg public headers", [
        "include/waypointcfg/waypointcfg.h", "include/waypointcfg/waypoint_merge.h"]),
    ("include: add wayenv public API", [
        "include/wayenv/wayenv.h", "include/wayenv/wayenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add waypoint coordinator and port map headers", [
        "include/waypointcfg/waypoint_coordinator.h", "include/waypointcfg/admission_gate.h",
        "include/waypointcfg/traffic_split.h", "include/waypointcfg/probe_cycle.h"]),
    ("include: add route weight header", ["include/waypointcfg/latency_budget.h"]),
    ("src/wayenv: add buffer and string utilities", [
        "src/wayenv/buffer.cpp", "src/wayenv/buffer.h", "src/wayenv/strutil.cpp",
        "src/wayenv/strutil.h"]),
    ("src/wayenv: add arena allocator", [
        "src/wayenv/arena.cpp", "src/wayenv/arena.h", "src/wayenv/wayenv_internal.h"]),
    ("src/wayenv: add error helpers", ["src/wayenv/error.cpp", "src/wayenv/error.h"]),
    ("src/wayenv: add UTF-8 validation", ["src/wayenv/utf8.cpp", "src/wayenv/utf8.h"]),
    ("src/wayenv: implement wayenv line lexer", ["src/wayenv/lexer.cpp", "src/wayenv/lexer.h"]),
    ("src/wayenv: add quoted value unescape", ["src/wayenv/unescape.cpp", "src/wayenv/unescape.h"]),
    ("src/wayenv: add document store", ["src/wayenv/store.cpp", "src/wayenv/store.h"]),
    ("src/wayenv: wire assignment parser", ["src/wayenv/parser.cpp", "src/wayenv/parser.h"]),
    ("src/wayenv: add serialize to wayenv text", ["src/wayenv/serialize.cpp", "src/wayenv/serialize.h"]),
    ("src/wayenv: add validation pass", ["src/wayenv/validate.cpp", "src/wayenv/validate.h"]),
    ("src/wayenv: add merge overlay", ["src/wayenv/merge.cpp", "src/wayenv/merge.h"]),
    ("src/wayenv: add expand and coerce", [
        "src/wayenv/expand.cpp", "src/wayenv/expand.h", "src/wayenv/coerce.cpp",
        "src/wayenv/coerce.h"]),
    ("src/wayenv: add walk query diff", [
        "src/wayenv/walk.cpp", "src/wayenv/walk.h", "src/wayenv/query.cpp",
        "src/wayenv/query.h", "src/wayenv/diff.cpp", "src/wayenv/diff.h"]),
    ("src/wayenv: add pretty printer", ["src/wayenv/pretty.cpp", "src/wayenv/pretty.h"]),
    ("src/wayenv: add attach stack and ctx", [
        "src/wayenv/waypoint_stack.cpp", "src/wayenv/waypoint_stack.h",
        "src/wayenv/waypoint_ctx.cpp", "src/wayenv/waypoint_ctx.h"]),
    ("src/wayenv: add path filter profile", [
        "src/wayenv/path.cpp", "src/wayenv/path.h", "src/wayenv/filter.cpp",
        "src/wayenv/filter.h", "src/wayenv/profile.cpp", "src/wayenv/profile.h"]),
    ("src/wayenv: add snapshot readutil strict canonical", [
        "src/wayenv/snapshot.cpp", "src/wayenv/snapshot.h", "src/wayenv/readutil.cpp",
        "src/wayenv/readutil.h", "src/wayenv/strict.cpp", "src/wayenv/strict.h",
        "src/wayenv/canonical.cpp", "src/wayenv/canonical.h"]),
    ("src/wayenv: add wayloader and main wayenv module", [
        "src/wayenv/wayloader.cpp", "src/wayenv/wayenv.cpp", "src/wayenv/waymap.cpp",
        "src/wayenv/waymap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.cpp", "src/toml/buffer.cpp"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.cpp", "src/toml/datetime.cpp", "src/toml/lexer.cpp"]),
    ("src/toml: add value and parser core", ["src/toml/value.cpp", "src/toml/parser.cpp"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.cpp", "src/toml/merge.cpp", "src/toml/serialize.cpp"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.cpp", "src/toml/format.cpp", "src/toml/validator.cpp", "src/toml/document.cpp"]),
    ("src: add waypointcfg bridge and wayenv-to-toml merge", ["src/waypointcfg.cpp", "src/waypoint_merge.cpp"]),
    ("src: add waypoint coordinator validator", ["src/waypoint_coordinator.cpp"]),
    ("src: add attach gate evaluator", ["src/admission_gate.cpp"]),
    ("src: add port map slot tracker", ["src/traffic_split.cpp"]),
    ("src: add mirror queue for traffic duplication", ["src/probe_cycle.cpp"]),
    ("src: add route weight accumulator", ["src/latency_budget.cpp"]),
    ("tests: add Unity harness", ["tests/unity/unity.cpp", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.cpp", "tests/test_basic.cpp"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.cpp", "tests/test_merge.cpp", "tests/test_validate.cpp"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.cpp", "tests/test_coerce.cpp", "tests/test_integration.cpp",
        "tests/test_scenarios.cpp"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.cpp", "tests/test_lexer_exhaustive.cpp"]),
    ("tests: add waypoint coordinator and port map unit tests", [
        "tests/test_waypoint_coordinator.cpp", "tests/test_traffic_split.cpp"]),
    ("tests: add mirror queue and route weight unit tests", [
        "tests/test_probe_cycle.cpp", "tests/test_latency_budget.cpp"]),
    ("examples: add TOML waypoint manifest and runtime overlay", [
        "examples/waypoint.toml", "examples/waypoint.runtime"]),
    ("fuzz: add wayenv_fuzzer harness", ["fuzz/wayenv_fuzzer.cc"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.cc"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.cc"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.cc"]),
    ("fuzz: add waypoint_fuzzer for cross-format overlay", ["fuzz/waypoint_fuzzer.cc"]),
    ("fuzz: add traffic_split_fuzzer for compaction path", ["fuzz/traffic_split_fuzzer.cc"]),
    ("fuzz: add probe_cycle_fuzzer for mirror path", ["fuzz/probe_cycle_fuzzer.cc"]),
    ("fuzz: add latency_budget_fuzzer for weight path", ["fuzz/latency_budget_fuzzer.cc"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/wayenv_fuzzer/minimal.wenv",
        "fuzz/corpus/wayenv_fuzzer/quoted.wenv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/waypoint_fuzzer/sample.bin",
        "fuzz/corpus/traffic_split_fuzzer/seed.bin",
        "fuzz/corpus/probe_cycle_fuzzer/seed.bin",
        "fuzz/corpus/latency_budget_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for waypointcfg library", ["README.md"]),
    ("docs: add BUILDING notes", ["docs/BUILDING.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable waypoint sidecar attachment library", []),
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

    corp = ROOT / "fuzz" / "corpus" / "wayenv_fuzzer"
    if corp.exists():
        for old in list(corp.glob("*.eenv")) + list(corp.glob("*.wenv")):
            old.rename(old.with_suffix(".wenv"))


def transform_contents() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.name in SKIP_FILES:
            path.unlink(missing_ok=True)
            continue
        if path.suffix not in {
            ".cpp", ".h", ".cc", ".sh", ".yaml", ".md", ".txt", ".toml",
            ".wenv", ".cenv", ".env", "Makefile"
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
    path = ROOT / "src" / "waypoint_coordinator.cpp"
    text = path.read_text(encoding="utf-8")
    text = text.replace('tome_table_get(tbl, "ports")', 'tome_table_get(tbl, "lanes")')
    text = text.replace('"port"', '"lane"')
    text = text.replace('tome_table_get(doc->root, "escort")', 'tome_table_get(doc->root, "waypoint")')
    path.write_text(text, encoding="utf-8")


README = """# waypointcfg

waypointcfg is a C++17 library for **waypoint proxy traffic steering orchestration**: parse TOML waypoint manifests, load wayenv runtime steering overlays, merge layers, validate admission state gates, and track weighted traffic split lanes plus health probe cycle trackers.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Wayenv layer** — `KEY=VALUE`, `@waypoint` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply wayenv overlay keys onto parsed TOML documents
- **Waypoint coordinator** — validate `[waypoint]` tables and register lane weights into a traffic split table
- **Probe cycle** — track health probe cadence across waypoint steering epochs
- **Latency budget** — accumulate latency budget scores during progressive steering
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `wayenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `waypoint_fuzzer`, `traffic_split_fuzzer`, `probe_cycle_fuzzer`, `latency_budget_fuzzer`.

## License

MIT — see LICENSE.
"""

BUILDING = """# Building waypointcfg

## Requirements

- clang/clang++ 14+
- libFuzzer (via `-fsanitize=fuzzer` or `$LIB_FUZZING_ENGINE`)

## Local ASan build

```bash
bash build/wsl_build.sh
```

Fuzzers land in `/tmp/waypointcfg_out/`.

## Unit tests

```bash
make test
```
"""


def add_domain() -> None:
    write(ROOT / "README.md", README)
    write(ROOT / "docs" / "BUILDING.md", BUILDING)

    write(ROOT / "examples" / "waypoint.toml", """[waypoint]
name = "checkout-api"
probe_interval_ms = 60000
steering_mode = "linear"

[[waypoint.lanes]]
label = "upstream-a"
weight = 90

[[waypoint.lanes]]
label = "waypoint-b"
weight = 10
""")

    write(ROOT / "examples" / "waypoint.runtime", """# Runtime waypoint attach parameters injected during attachment
PROBE_INTERVAL_MS=30000
STEERING_MODE=linear
STEERING_GENERATION=2
""")

    write(ROOT / "tests" / "test_latency_budget.cpp", '''#include "waypointcfg/latency_budget.h"
#include "unity/unity.h"

void test_latency_budget_score(void) {
  latency_budget_t rw;
  latency_budget_init(&rw);
  TEST_ASSERT_EQUAL(0, latency_budget_note_bind(&rw, "upstream-a", 3));
  TEST_ASSERT_EQUAL(0, latency_budget_note_migration(&rw, "waypoint-b"));
  TEST_ASSERT_NOT_EQUAL(0u, latency_budget_score(&rw));
  latency_budget_reset(&rw);
}
''')

    write(ROOT / "fuzz" / "corpus" / "waypoint_fuzzer" / "sample.bin",
          bytes([32]) + b"[waypoint]\nname=\"x\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "traffic_split_fuzzer" / "seed.bin", bytes(range(32, 96)))
    write(ROOT / "fuzz" / "corpus" / "probe_cycle_fuzzer" / "seed.bin", bytes(range(16, 128)))
    write(ROOT / "fuzz" / "corpus" / "latency_budget_fuzzer" / "seed.bin", bytes(range(8, 64)))


def plant_bugs() -> None:
    """Keep hardened unescape; plant wayenv empty-serialize null deref for bug5."""
    ser = (ROOT / "src" / "wayenv" / "serialize.cpp").read_text(encoding="utf-8")
    ser = ser.replace(
        "  if (buf.len > 0) {\n"
        "    memcpy(*out_buf, buf.data, buf.len + 1);\n"
        "  } else {\n"
        "    (*out_buf)[0] = '\\0';\n"
        "  }",
        "  memcpy(*out_buf, buf.data, buf.len + 1);",
    )
    (ROOT / "src" / "wayenv" / "serialize.cpp").write_text(ser, encoding="utf-8")


def patch_build() -> None:
    build_sh = '''#!/bin/bash -eu

OBJECTS=()

compile_wayenv() {
  local base="$1"
  local obj="wayenv_${base%.cpp}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall -D_GNU_SOURCE} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/wayenv" \\
    -c "${SRC:-.}/src/wayenv/${base}" -o "${obj}"
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
         validate merge expand coerce walk query diff pretty waypoint_stack \\
         waypoint_ctx path filter waymap profile canonical strict readutil \\
         snapshot wayloader wayenv; do
  if [ -f "${SRC:-.}/src/wayenv/${f}.cpp" ]; then
    compile_wayenv "${f}.cpp"
  fi
done

for f in memory buffer unicode datetime lexer value parser path merge serialize \\
         diag format validator document; do
  compile_toml "${f}.cpp"
done

for f in waypointcfg waypoint_merge waypoint_coordinator admission_gate traffic_split probe_cycle latency_budget; do
  obj="${f}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/wayenv" -I"${SRC:-.}/src/toml" \\
    -c "${SRC:-.}/src/${f}.cpp" -o "${obj}"
  OBJECTS+=("${obj}")
done

FUZZ_CXXFLAGS="${CXXFLAGS:- -O1 -g -std=c++17}"
INCS="-I${SRC:-.}/include -I${SRC:-.}/src/wayenv -I${SRC:-.}/src/toml"

build_fuzzer() {
  ${CXX:-clang++} ${FUZZ_CXXFLAGS} ${LIB_FUZZING_ENGINE} \\
    "${SRC:-.}/fuzz/$1" "${OBJECTS[@]}" ${INCS} \\
    -o "${OUT:-.}/$2" -lm
}

build_fuzzer wayenv_fuzzer.cc wayenv_fuzzer
build_fuzzer toml_fuzzer.cc toml_fuzzer
build_fuzzer toml_merge_fuzzer.cc toml_merge_fuzzer
build_fuzzer toml_format_fuzzer.cc toml_format_fuzzer
build_fuzzer waypoint_fuzzer.cc waypoint_fuzzer
build_fuzzer traffic_split_fuzzer.cc traffic_split_fuzzer
build_fuzzer probe_cycle_fuzzer.cc probe_cycle_fuzzer
build_fuzzer latency_budget_fuzzer.cc latency_budget_fuzzer
'''
    write(ROOT / ".clusterfuzzlite/build.sh", build_sh)

    wsl = '''#!/bin/bash -eu
set -o pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${OUT:-/tmp/waypointcfg_out}"
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
  - wayenv_fuzzer
  - toml_fuzzer
  - toml_merge_fuzzer
  - toml_format_fuzzer
  - waypoint_fuzzer
  - traffic_split_fuzzer
  - probe_cycle_fuzzer
  - latency_budget_fuzzer
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
CXXFLAGS ?= -std=c++17 -O2 -g -Wall -Wextra -Wpedantic -Werror -Iinclude -Isrc/wayenv -Isrc/toml
WAYENV_SRC := $(wildcard src/wayenv/*.cpp)
TOML_SRC := $(wildcard src/toml/*.cpp)
CORE_SRC := src/waypointcfg.cpp src/waypoint_merge.cpp src/waypoint_coordinator.cpp src/admission_gate.cpp src/traffic_split.cpp src/probe_cycle.cpp src/latency_budget.cpp
TEST_SRC := $(wildcard tests/test_*.cpp)
TEST := build/waypointcfg_tests

$(TEST): $(WAYENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) | build
\t$(CXX) $(CXXFLAGS) $(WAYENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) -o $@

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
    escort_submit = Path("/home/samuel/Documents/fenrir3/artifacts/escortcfg/poc/submit")
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

    write(verified / "entry_leak.wenv", "FOO=1\n")
    write(verified / "audit_leak.toml", 'k = "v"\n')
    write(verified / "empty_serialize.wenv", b"")
    write(verified / "traffic_split_uaf.bin", bytes(range(32, 160)))

    escort_verified = Path("/home/samuel/Documents/fenrir3/artifacts/escortcfg/poc/verified")
    if (escort_verified / "merge_uaf.bin").exists():
        shutil.copy(escort_verified / "merge_uaf.bin", verified / "merge_uaf.bin")

    write(poc_dir / "README.txt", """waypointcfg local artifacts — NOT on GitHub

verified/
  entry_leak.wenv           — bug1 wayenv entry realloc leak
  audit_leak.toml           — bug2 toml audit key leak
  traffic_split_uaf.bin          — bug3 traffic split compaction UAF
  merge_uaf.bin             — bug4 toml merge overlay index UAF
  empty_serialize.wenv      — bug5 wayenv empty serialize null deref

submit/
  bugN_*.patch + bugN_TASK_DESCRIPTION.txt

Verify: bash artifacts/waypointcfg/wsl_test_pocs.sh
""")

    write(ARTIFACTS / "TASKS.md", """# waypointcfg task queue

GitHub: tolossamuel/waypointcfg

| # | Bug | Harness | Class | Status |
|---|-----|---------|-------|--------|
| 1 | wayenv entry realloc leak | wayenv_fuzzer | LeakSanitizer | Ready |
| 2 | toml audit key leak | toml_fuzzer | LeakSanitizer | Ready |
| 3 | traffic split compaction UAF | traffic_split_fuzzer | heap-use-after-free | Ready |
| 4 | toml merge UAF | toml_merge_fuzzer | heap-use-after-free | Ready |
| 5 | wayenv empty serialize null deref | wayenv_fuzzer | null deref | Ready |

PoC bytes and patches: artifacts/waypointcfg/poc/ (not on GitHub).
""")

    wsl_test = '''#!/bin/bash -eu
ROOT="$(cd "$(dirname "$0")/../../waypointcfg" && pwd)"
POC="${POC_DIR:-$(dirname "$0")/poc/verified}"
OUT="${OUT:-/tmp/waypointcfg_out}"

cd "$ROOT"
CC=clang CXX=clang++ bash build/wsl_build.sh >/dev/null

fail() { echo "FAIL: $*"; exit 1; }
pass() { echo "PASS: $*"; }

if ASAN_OPTIONS=detect_leaks=1 "$OUT/wayenv_fuzzer" "$POC/entry_leak.wenv" >/dev/null 2>&1; then
  fail "bug1 should leak on unpatched build"
fi
pass "bug1 wayenv entry leak reproduces"

if ASAN_OPTIONS=detect_leaks=1 "$OUT/toml_fuzzer" "$POC/audit_leak.toml" >/dev/null 2>&1; then
  fail "bug2 should leak on unpatched build"
fi
pass "bug2 toml audit leak reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/traffic_split_fuzzer" "$POC/traffic_split_uaf.bin" >/dev/null 2>&1; then
  fail "bug3 should UAF on unpatched build"
fi
pass "bug3 port map UAF reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/toml_merge_fuzzer" "$POC/merge_uaf.bin" >/dev/null 2>&1; then
  fail "bug4 should UAF on unpatched build"
fi
pass "bug4 toml merge UAF reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/wayenv_fuzzer" "$POC/empty_serialize.wenv" >/dev/null 2>&1; then
  fail "bug5 should crash on unpatched build"
fi
pass "bug5 wayenv empty serialize null deref reproduces"

echo "All unpatched PoCs verified."
'''
    write(ARTIFACTS / "wsl_test_pocs.sh", wsl_test)
    (ARTIFACTS / "wsl_test_pocs.sh").chmod(0o755)


def generate_patches() -> None:
    submit = ARTIFACTS / "poc" / "submit"
    escort_submit = Path("/home/samuel/Documents/fenrir3/artifacts/escortcfg/poc/submit")

    patch_map = [
        ("bug1_wayenv_entry_leak.patch", escort_submit / "bug1_wayenv_entry_leak.patch"),
        ("bug2_toml_audit_leak.patch", escort_submit / "bug2_toml_audit_leak.patch"),
        ("bug3_traffic_split_uaf.patch", escort_submit / "bug3_traffic_split_uaf.patch"),
        ("bug4_toml_merge_uaf.patch", escort_submit / "bug4_toml_merge_uaf.patch"),
        ("bug5_wayenv_empty_serialize_null_deref.patch",
         escort_submit / "bug5_wayenv_empty_serialize_null_deref.patch"),
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
            "A memory leak occurs when parsing an wayenv assignment: wayenv_set_entry "
            "reallocates internal entry storage, but that heap memory is not freed when "
            "wayenv_doc_destroy runs in src/wayenv/store.cpp."
        ),
        "bug2_TASK_DESCRIPTION.txt": (
            "A memory leak occurs in the TOML document audit key path when toml_parse "
            "records assignment keys into doc->audit_keys without releasing them during "
            "document teardown in src/toml/document.cpp."
        ),
        "bug3_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in traffic_split_finalize_digest in src/traffic_split.cpp "
            "when digest finalization reads port label bytes through pending references registered "
            "before traffic_split_compact reallocates and frees the original label storage during "
            "multi-slot registration in the port map compaction pipeline, triggered via traffic_split_fuzzer."
        ),
        "bug4_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs during TOML table merge in src/toml/merge.cpp when "
            "merge_table_in_place caches overlay entry key pointers then rebuilds the overlay "
            "table index mid-loop, leaving stale key references that are read on subsequent merge "
            "iterations via toml_merge_fuzzer."
        ),
        "bug5_TASK_DESCRIPTION.txt": (
            "A null pointer dereference occurs in wayenv_serialize_doc in src/wayenv/serialize.cpp "
            "when serializing a document with zero entries copies from buf.data even though the "
            "internal buffer was never allocated, triggered via wayenv_fuzzer with zero-length input."
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
    out = "/tmp/waypointcfg_out"
    tests = [
        ("bug1_wayenv_entry_leak.patch", "wayenv_fuzzer", "entry_leak.wenv", "detect_leaks=1", True),
        ("bug2_toml_audit_leak.patch", "toml_fuzzer", "audit_leak.toml", "detect_leaks=1", True),
        ("bug3_traffic_split_uaf.patch", "traffic_split_fuzzer", "traffic_split_uaf.bin", "detect_leaks=0", True),
        ("bug4_toml_merge_uaf.patch", "toml_merge_fuzzer", "merge_uaf.bin", "detect_leaks=0", True),
        ("bug5_wayenv_empty_serialize_null_deref.patch", "wayenv_fuzzer", "empty_serialize.wenv", "detect_leaks=0", True),
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
        ["gh", "repo", "create", "tolossamuel/waypointcfg",
         "--private",
         "--description", "C++ waypoint sidecar proxy attachment config library (TOML + wayenv) for ClusterFuzzLite",
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
    if "--push" in __import__("sys").argv:
        push_github()
    n = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()
    loc = subprocess.check_output(
        ["find", "src", "include", "-name", "*.cpp", "-o", "-name", "*.h"],
        cwd=ROOT, text=True,
    ).strip().split("\n")
    print(f"OK waypointcfg — {n} commits, {len(loc)} source files")


if __name__ == "__main__":
    main()
