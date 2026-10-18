#!/usr/bin/env python3
"""Bootstrap ingestcfg — C++ data ingestion pipeline orchestration + ingestenv overlays."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/ingestcfg")
SRC = Path("/home/samuel/Documents/fenrir3/waypointcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/ingestcfg")

TEXT_RENAME = [
    ("waypointcfg_validate_waypoint_manifest", "ingestcfg_validate_ingest_manifest"),
    ("waypointcfg_apply_wayenv_to_toml", "ingestcfg_apply_ingestenv_to_toml"),
    ("waypointcfg_load_wayenv_memory", "ingestcfg_load_ingestenv_memory"),
    ("waypointcfg_wayenv_free", "ingestcfg_ingestenv_free"),
    ("waypointcfg_load_toml_memory", "ingestcfg_load_toml_memory"),
    ("waypointcfg_toml_free", "ingestcfg_toml_free"),
    ("waypointcfg_default_options", "ingestcfg_default_options"),
    ("waypointcfg_options_t", "ingestcfg_options_t"),
    ("traffic_split_t", "partition_router_t"),
    ("traffic_split_", "partition_router_"),
    ("traffic_split", "partition_router"),
    ("split_lane_t", "partition_lane_t"),
    ("split_lane", "partition_lane"),
    ("probe_cycle_t", "batch_window_t"),
    ("probe_cycle_", "batch_window_"),
    ("probe_cycle", "batch_window"),
    ("probe_tick_t", "batch_tick_t"),
    ("probe_tick", "batch_tick"),
    ("latency_budget_t", "schema_tracker_t"),
    ("latency_budget_", "schema_tracker_"),
    ("latency_budget", "schema_tracker"),
    ("admission_gate_", "ack_gate_"),
    ("admission_gate", "ack_gate"),
    ("waypoint_coordinator", "ingest_coordinator"),
    ("waypoint_merge", "ingest_merge"),
    ("waypoint_fuzzer", "ingest_fuzzer"),
    ("wayenv_doc_impl_t", "ingestenv_doc_impl_t"),
    ("wayenv_doc_t", "ingestenv_doc_t"),
    ("wayenv_error_t", "ingestenv_error_t"),
    ("wayenv_options_t", "ingestenv_options_t"),
    ("wayenv_entry_t", "ingestenv_entry_t"),
    ("wayenv_slice_t", "ingestenv_slice_t"),
    ("wayenv_arena_t", "ingestenv_arena_t"),
    ("wayenv_token_kind_t", "ingestenv_token_kind_t"),
    ("wayenv_token_t", "ingestenv_token_t"),
    ("wayenv_internal.h", "ingestenv_internal.h"),
    ("include/wayenv", "include/ingestenv"),
    ("src/wayenv/", "src/ingestenv/"),
    ("src/wayenv", "src/ingestenv"),
    ("wayenv_", "ingestenv_"),
    ("WAYENV_", "INGESTENV_"),
    ("Wayenv", "Ingestenv"),
    ("wayenv", "ingestenv"),
    ("waypoint_stack", "pipeline_stack"),
    ("waypoint_ctx", "pipeline_ctx"),
    ("@waypoint", "@pipeline"),
    ("waymap", "ingestmap"),
    ("wayloader", "ingestloader"),
    ("WAYPOINTCFG", "INGESTCFG"),
    ("WaypointCfg", "IngestCfg"),
    ("waypointcfg", "ingestcfg"),
    ("WAYPOINT_", "INGEST_"),
    ("tolossamuel/waypointcfg", "tolossamuel/ingestcfg"),
    ("/tmp/waypointcfg_out", "/tmp/ingestcfg_out"),
    ("compile_wayenv", "compile_ingestenv"),
    (".wenv", ".ienv"),
    ("Waypoint proxy traffic steering orchestration for service mesh",
     "Data ingestion pipeline orchestration for stream processing"),
    ("waypoint proxy traffic steering orchestration for service mesh",
     "data ingestion pipeline orchestration for stream processing"),
    ("wayenv runtime steering overlays", "ingestenv runtime pipeline overlays"),
    ("Wayenv layer", "Ingestenv layer"),
    ("Waypoint coordinator validation", "Ingest coordinator validation"),
    ("admission state gates", "acknowledgment gates"),
    ("weighted traffic split lanes", "partition routing lanes"),
    ("health probe cycle trackers", "batch flush window trackers"),
    ("[waypoint]", "[ingest]"),
    ("waypoint.lanes", "ingest.partitions"),
    ("waypoint steering", "ingest pipeline"),
    ("waypoint.toml", "ingest.toml"),
    ("waypoint.runtime", "ingest.runtime"),
    ("probe_interval_ms", "flush_interval_ms"),
    ("steering_mode", "pipeline_mode"),
    ("STEERING_GENERATION", "PIPELINE_GENERATION"),
    ("STEERING_MODE", "PIPELINE_MODE"),
    ("PROBE_INTERVAL_MS", "FLUSH_INTERVAL_MS"),
    ('"lanes"', '"partitions"'),
    ('"lane"', '"partition"'),
    ("upstream-a", "shard-a"),
    ("waypoint-b", "shard-b"),
    ("Waypoint", "Ingest"),
    ("waypoint", "ingest"),
    ("steering", "pipeline"),
    ("attach", "commit"),
    ("port map", "partition router"),
    ("Port map", "Partition router"),
    ("mirror queue", "batch window"),
    ("Mirror queue", "Batch window"),
    ("route weight", "schema tracker"),
    ("Route weight", "Schema tracker"),
    ("traffic split", "partition router"),
    ("Traffic split", "Partition router"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

NAME_SUBS = [
    ("traffic_split", "partition_router"),
    ("probe_cycle", "batch_window"),
    ("latency_budget", "schema_tracker"),
    ("admission_gate", "ack_gate"),
    ("waypoint_coordinator", "ingest_coordinator"),
    ("waypoint_merge", "ingest_merge"),
    ("waypoint_fuzzer", "ingest_fuzzer"),
    ("wayenv_fuzzer", "ingestenv_fuzzer"),
    ("wayloader", "ingestloader"),
    ("wayenv_internal", "ingestenv_internal"),
    ("wayenv_types", "ingestenv_types"),
    ("wayenv", "ingestenv"),
    ("waymap", "ingestmap"),
    ("waypointcfg", "ingestcfg"),
    ("waypoint_stack", "pipeline_stack"),
    ("waypoint_ctx", "pipeline_ctx"),
    ("waypoint.runtime", "ingest.runtime"),
    ("waypoint.toml", "ingest.toml"),
]

DIR_RENAMES = [
    ("include/waypointcfg", "include/ingestcfg"),
    ("include/wayenv", "include/ingestenv"),
    ("src/wayenv", "src/ingestenv"),
    ("fuzz/corpus/wayenv_fuzzer", "fuzz/corpus/ingestenv_fuzzer"),
    ("fuzz/corpus/waypoint_fuzzer", "fuzz/corpus/ingest_fuzzer"),
    ("fuzz/corpus/traffic_split_fuzzer", "fuzz/corpus/partition_router_fuzzer"),
    ("fuzz/corpus/probe_cycle_fuzzer", "fuzz/corpus/batch_window_fuzzer"),
    ("fuzz/corpus/latency_budget_fuzzer", "fuzz/corpus/schema_tracker_fuzzer"),
]

COMMITS_RAW = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add ingestcfg public headers", [
        "include/ingestcfg/ingestcfg.h", "include/ingestcfg/ingest_merge.h"]),
    ("include: add ingestenv public API", [
        "include/ingestenv/ingestenv.h", "include/ingestenv/ingestenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add ingest coordinator and partition router headers", [
        "include/ingestcfg/ingest_coordinator.h", "include/ingestcfg/ack_gate.h",
        "include/ingestcfg/partition_router.h", "include/ingestcfg/batch_window.h"]),
    ("include: add schema tracker header", ["include/ingestcfg/schema_tracker.h"]),
    ("src/ingestenv: add buffer and string utilities", [
        "src/ingestenv/buffer.cpp", "src/ingestenv/buffer.h", "src/ingestenv/strutil.cpp",
        "src/ingestenv/strutil.h"]),
    ("src/ingestenv: add arena allocator", [
        "src/ingestenv/arena.cpp", "src/ingestenv/arena.h", "src/ingestenv/ingestenv_internal.h"]),
    ("src/ingestenv: add error helpers", ["src/ingestenv/error.cpp", "src/ingestenv/error.h"]),
    ("src/ingestenv: add UTF-8 validation", ["src/ingestenv/utf8.cpp", "src/ingestenv/utf8.h"]),
    ("src/ingestenv: implement ingestenv line lexer", ["src/ingestenv/lexer.cpp", "src/ingestenv/lexer.h"]),
    ("src/ingestenv: add quoted value unescape", ["src/ingestenv/unescape.cpp", "src/ingestenv/unescape.h"]),
    ("src/ingestenv: add document store", ["src/ingestenv/store.cpp", "src/ingestenv/store.h"]),
    ("src/ingestenv: wire assignment parser", ["src/ingestenv/parser.cpp", "src/ingestenv/parser.h"]),
    ("src/ingestenv: add serialize to ingestenv text", ["src/ingestenv/serialize.cpp", "src/ingestenv/serialize.h"]),
    ("src/ingestenv: add validation pass", ["src/ingestenv/validate.cpp", "src/ingestenv/validate.h"]),
    ("src/ingestenv: add merge overlay", ["src/ingestenv/merge.cpp", "src/ingestenv/merge.h"]),
    ("src/ingestenv: add expand and coerce", [
        "src/ingestenv/expand.cpp", "src/ingestenv/expand.h", "src/ingestenv/coerce.cpp",
        "src/ingestenv/coerce.h"]),
    ("src/ingestenv: add walk query diff", [
        "src/ingestenv/walk.cpp", "src/ingestenv/walk.h", "src/ingestenv/query.cpp",
        "src/ingestenv/query.h", "src/ingestenv/diff.cpp", "src/ingestenv/diff.h"]),
    ("src/ingestenv: add pretty printer", ["src/ingestenv/pretty.cpp", "src/ingestenv/pretty.h"]),
    ("src/ingestenv: add pipeline stack and ctx", [
        "src/ingestenv/pipeline_stack.cpp", "src/ingestenv/pipeline_stack.h",
        "src/ingestenv/pipeline_ctx.cpp", "src/ingestenv/pipeline_ctx.h"]),
    ("src/ingestenv: add path filter profile", [
        "src/ingestenv/path.cpp", "src/ingestenv/path.h", "src/ingestenv/filter.cpp",
        "src/ingestenv/filter.h", "src/ingestenv/profile.cpp", "src/ingestenv/profile.h"]),
    ("src/ingestenv: add snapshot readutil strict canonical", [
        "src/ingestenv/snapshot.cpp", "src/ingestenv/snapshot.h", "src/ingestenv/readutil.cpp",
        "src/ingestenv/readutil.h", "src/ingestenv/strict.cpp", "src/ingestenv/strict.h",
        "src/ingestenv/canonical.cpp", "src/ingestenv/canonical.h"]),
    ("src/ingestenv: add ingestloader and main ingestenv module", [
        "src/ingestenv/ingestloader.cpp", "src/ingestenv/ingestenv.cpp", "src/ingestenv/ingestmap.cpp",
        "src/ingestenv/ingestmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.cpp", "src/toml/buffer.cpp"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.cpp", "src/toml/datetime.cpp", "src/toml/lexer.cpp"]),
    ("src/toml: add value and parser core", ["src/toml/value.cpp", "src/toml/parser.cpp"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.cpp", "src/toml/merge.cpp", "src/toml/serialize.cpp"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.cpp", "src/toml/format.cpp", "src/toml/validator.cpp", "src/toml/document.cpp"]),
    ("src: add ingestcfg bridge and ingestenv-to-toml merge", ["src/ingestcfg.cpp", "src/ingest_merge.cpp"]),
    ("src: add ingest coordinator validator", ["src/ingest_coordinator.cpp"]),
    ("src: add ack gate evaluator", ["src/ack_gate.cpp"]),
    ("src: add partition router slot tracker", ["src/partition_router.cpp"]),
    ("src: add batch window for record batching", ["src/batch_window.cpp"]),
    ("src: add schema tracker for evolution scoring", ["src/schema_tracker.cpp"]),
    ("tests: add Unity harness", ["tests/unity/unity.cpp", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.cpp", "tests/test_basic.cpp"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.cpp", "tests/test_merge.cpp", "tests/test_validate.cpp"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.cpp", "tests/test_coerce.cpp", "tests/test_integration.cpp",
        "tests/test_scenarios.cpp"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.cpp", "tests/test_lexer_exhaustive.cpp"]),
    ("tests: add ingest coordinator and partition router unit tests", [
        "tests/test_ingest_coordinator.cpp", "tests/test_partition_router.cpp"]),
    ("tests: add batch window and schema tracker unit tests", [
        "tests/test_batch_window.cpp", "tests/test_schema_tracker.cpp"]),
    ("examples: add TOML ingest manifest and runtime overlay", [
        "examples/ingest.toml", "examples/ingest.runtime"]),
    ("fuzz: add ingestenv_fuzzer harness", ["fuzz/ingestenv_fuzzer.cc"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.cc"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.cc"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.cc"]),
    ("fuzz: add ingest_fuzzer for cross-format overlay", ["fuzz/ingest_fuzzer.cc"]),
    ("fuzz: add partition_router_fuzzer for compaction path", ["fuzz/partition_router_fuzzer.cc"]),
    ("fuzz: add batch_window_fuzzer for batching path", ["fuzz/batch_window_fuzzer.cc"]),
    ("fuzz: add schema_tracker_fuzzer for schema path", ["fuzz/schema_tracker_fuzzer.cc"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/ingestenv_fuzzer/minimal.ienv",
        "fuzz/corpus/ingestenv_fuzzer/quoted.ienv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/ingest_fuzzer/sample.bin",
        "fuzz/corpus/partition_router_fuzzer/seed.bin",
        "fuzz/corpus/batch_window_fuzzer/seed.bin",
        "fuzz/corpus/schema_tracker_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for ingestcfg library", ["README.md"]),
    ("docs: add BUILDING notes", ["docs/BUILDING.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable ingest pipeline library", []),
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

    corp = ROOT / "fuzz" / "corpus" / "ingestenv_fuzzer"
    if corp.exists():
        for old in list(corp.glob("*.wenv")) + list(corp.glob("*.ienv")):
            old.rename(old.with_suffix(".ienv"))


def transform_contents() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.name in SKIP_FILES:
            path.unlink(missing_ok=True)
            continue
        if path.suffix not in {
            ".cpp", ".h", ".cc", ".sh", ".yaml", ".md", ".txt", ".toml",
            ".ienv", ".wenv", ".env", "Makefile"
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
    path = ROOT / "src" / "ingest_coordinator.cpp"
    text = path.read_text(encoding="utf-8")
    text = text.replace('tome_table_get(tbl, "lanes")', 'tome_table_get(tbl, "partitions")')
    text = text.replace('"lane"', '"partition"')
    path.write_text(text, encoding="utf-8")


README = """# ingestcfg

ingestcfg is a C++17 library for **data ingestion pipeline orchestration**: parse TOML ingest manifests, load ingestenv runtime pipeline overlays, merge layers, validate acknowledgment gates, and track partition routing lanes plus batch flush window trackers.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Ingestenv layer** — `KEY=VALUE`, `@pipeline` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply ingestenv overlay keys onto parsed TOML documents
- **Ingest coordinator** — validate `[ingest]` tables and register partition weights into a partition router
- **Batch window** — track record batch flush cadence across pipeline epochs
- **Schema tracker** — accumulate schema evolution scores during progressive ingestion
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `ingestenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `ingest_fuzzer`, `partition_router_fuzzer`, `batch_window_fuzzer`, `schema_tracker_fuzzer`.

## License

MIT — see LICENSE.
"""

BUILDING = """# Building ingestcfg

## Requirements

- clang/clang++ 14+
- libFuzzer (via `-fsanitize=fuzzer` or `$LIB_FUZZING_ENGINE`)

## Local ASan build

```bash
bash build/wsl_build.sh
```

Fuzzers land in `/tmp/ingestcfg_out/`.

## Unit tests

```bash
make test
```
"""


def add_domain() -> None:
    write(ROOT / "README.md", README)
    write(ROOT / "docs" / "BUILDING.md", BUILDING)

    write(ROOT / "examples" / "ingest.toml", """[ingest]
name = "events-stream"
flush_interval_ms = 60000
pipeline_mode = "linear"

[[ingest.partitions]]
label = "shard-a"
weight = 90

[[ingest.partitions]]
label = "shard-b"
weight = 10
""")

    write(ROOT / "examples" / "ingest.runtime", """# Runtime ingest pipeline parameters injected during commit
FLUSH_INTERVAL_MS=30000
PIPELINE_MODE=linear
PIPELINE_GENERATION=2
""")

    write(ROOT / "tests" / "test_schema_tracker.cpp", '''#include "ingestcfg/schema_tracker.h"
#include "unity/unity.h"

void test_schema_tracker_score(void) {
  schema_tracker_t rw;
  schema_tracker_init(&rw);
  TEST_ASSERT_EQUAL(0, schema_tracker_note_bind(&rw, "shard-a", 3));
  TEST_ASSERT_EQUAL(0, schema_tracker_note_migration(&rw, "shard-b"));
  TEST_ASSERT_NOT_EQUAL(0u, schema_tracker_score(&rw));
  schema_tracker_reset(&rw);
}
''')

    write(ROOT / "fuzz" / "corpus" / "ingest_fuzzer" / "sample.bin",
          bytes([32]) + b"[ingest]\nname=\"x\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "partition_router_fuzzer" / "seed.bin", bytes(range(32, 96)))
    write(ROOT / "fuzz" / "corpus" / "batch_window_fuzzer" / "seed.bin", bytes(range(16, 128)))
    write(ROOT / "fuzz" / "corpus" / "schema_tracker_fuzzer" / "seed.bin", bytes(range(8, 64)))


def plant_bugs() -> None:
    """Keep hardened unescape; plant ingestenv empty-serialize null deref for bug5."""
    ser = (ROOT / "src" / "ingestenv" / "serialize.cpp").read_text(encoding="utf-8")
    ser = ser.replace(
        "  if (buf.len > 0) {\n"
        "    memcpy(*out_buf, buf.data, buf.len + 1);\n"
        "  } else {\n"
        "    (*out_buf)[0] = '\\0';\n"
        "  }",
        "  memcpy(*out_buf, buf.data, buf.len + 1);",
    )
    (ROOT / "src" / "ingestenv" / "serialize.cpp").write_text(ser, encoding="utf-8")


def patch_build() -> None:
    build_sh = '''#!/bin/bash -eu

OBJECTS=()

compile_ingestenv() {
  local base="$1"
  local obj="ingestenv_${base%.cpp}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall -D_GNU_SOURCE} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/ingestenv" \\
    -c "${SRC:-.}/src/ingestenv/${base}" -o "${obj}"
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
         validate merge expand coerce walk query diff pretty pipeline_stack \\
         pipeline_ctx path filter ingestmap profile canonical strict readutil \\
         snapshot ingestloader ingestenv; do
  if [ -f "${SRC:-.}/src/ingestenv/${f}.cpp" ]; then
    compile_ingestenv "${f}.cpp"
  fi
done

for f in memory buffer unicode datetime lexer value parser path merge serialize \\
         diag format validator document; do
  compile_toml "${f}.cpp"
done

for f in ingestcfg ingest_merge ingest_coordinator ack_gate partition_router batch_window schema_tracker; do
  obj="${f}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/ingestenv" -I"${SRC:-.}/src/toml" \\
    -c "${SRC:-.}/src/${f}.cpp" -o "${obj}"
  OBJECTS+=("${obj}")
done

FUZZ_CXXFLAGS="${CXXFLAGS:- -O1 -g -std=c++17}"
INCS="-I${SRC:-.}/include -I${SRC:-.}/src/ingestenv -I${SRC:-.}/src/toml"

build_fuzzer() {
  ${CXX:-clang++} ${FUZZ_CXXFLAGS} ${LIB_FUZZING_ENGINE} \\
    "${SRC:-.}/fuzz/$1" "${OBJECTS[@]}" ${INCS} \\
    -o "${OUT:-.}/$2" -lm
}

build_fuzzer ingestenv_fuzzer.cc ingestenv_fuzzer
build_fuzzer toml_fuzzer.cc toml_fuzzer
build_fuzzer toml_merge_fuzzer.cc toml_merge_fuzzer
build_fuzzer toml_format_fuzzer.cc toml_format_fuzzer
build_fuzzer ingest_fuzzer.cc ingest_fuzzer
build_fuzzer partition_router_fuzzer.cc partition_router_fuzzer
build_fuzzer batch_window_fuzzer.cc batch_window_fuzzer
build_fuzzer schema_tracker_fuzzer.cc schema_tracker_fuzzer
'''
    write(ROOT / ".clusterfuzzlite/build.sh", build_sh)

    wsl = '''#!/bin/bash -eu
set -o pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${OUT:-/tmp/ingestcfg_out}"
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
  - ingestenv_fuzzer
  - toml_fuzzer
  - toml_merge_fuzzer
  - toml_format_fuzzer
  - ingest_fuzzer
  - partition_router_fuzzer
  - batch_window_fuzzer
  - schema_tracker_fuzzer
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
CXXFLAGS ?= -std=c++17 -O2 -g -Wall -Wextra -Wpedantic -Werror -Iinclude -Isrc/ingestenv -Isrc/toml
INGESTENV_SRC := $(wildcard src/ingestenv/*.cpp)
TOML_SRC := $(wildcard src/toml/*.cpp)
CORE_SRC := src/ingestcfg.cpp src/ingest_merge.cpp src/ingest_coordinator.cpp src/ack_gate.cpp src/partition_router.cpp src/batch_window.cpp src/schema_tracker.cpp
TEST_SRC := $(wildcard tests/test_*.cpp)
TEST := build/ingestcfg_tests

$(TEST): $(INGESTENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) | build
\t$(CXX) $(CXXFLAGS) $(INGESTENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) -o $@

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


def create_artifacts() -> None:
    poc_dir = ARTIFACTS / "poc"
    verified = poc_dir / "verified"
    submit = poc_dir / "submit"
    verified.mkdir(parents=True, exist_ok=True)
    submit.mkdir(parents=True, exist_ok=True)

    write(verified / "entry_leak.ienv", "FOO=1\n")
    write(verified / "audit_leak.toml", 'k = "v"\n')
    write(verified / "empty_serialize.ienv", b"")
    write(verified / "partition_router_uaf.bin", bytes(range(32, 160)))

    wp_verified = Path("/home/samuel/Documents/fenrir3/artifacts/waypointcfg/poc/verified")
    if (wp_verified / "merge_uaf.bin").exists():
        shutil.copy(wp_verified / "merge_uaf.bin", verified / "merge_uaf.bin")

    write(poc_dir / "README.txt", """ingestcfg local artifacts — NOT on GitHub

verified/
  entry_leak.ienv              — bug1 ingestenv entry realloc leak
  audit_leak.toml              — bug2 toml audit key leak
  partition_router_uaf.bin     — bug3 partition router compaction UAF
  merge_uaf.bin                — bug4 toml merge overlay index UAF
  empty_serialize.ienv         — bug5 ingestenv empty serialize null deref

submit/
  bugN_*.patch + bugN_TASK_DESCRIPTION.txt

Verify: bash artifacts/ingestcfg/wsl_test_pocs.sh
""")

    write(ARTIFACTS / "TASKS.md", """# ingestcfg task queue

GitHub: tolossamuel/ingestcfg

| # | Bug | Harness | Class | Status |
|---|-----|---------|-------|--------|
| 1 | ingestenv entry realloc leak | ingestenv_fuzzer | LeakSanitizer | Ready |
| 2 | toml audit key leak | toml_fuzzer | LeakSanitizer | Ready |
| 3 | partition router compaction UAF | partition_router_fuzzer | heap-use-after-free | Ready |
| 4 | toml merge UAF | toml_merge_fuzzer | heap-use-after-free | Ready |
| 5 | ingestenv empty serialize null deref | ingestenv_fuzzer | null deref | Ready |

PoC bytes and patches: artifacts/ingestcfg/poc/ (not on GitHub).
""")

    wsl_test = '''#!/bin/bash -eu
ROOT="$(cd "$(dirname "$0")/../../ingestcfg" && pwd)"
POC="${POC_DIR:-$(dirname "$0")/poc/verified}"
OUT="${OUT:-/tmp/ingestcfg_out}"

cd "$ROOT"
CC=clang CXX=clang++ bash build/wsl_build.sh >/dev/null

fail() { echo "FAIL: $*"; exit 1; }
pass() { echo "PASS: $*"; }

if ASAN_OPTIONS=detect_leaks=1 "$OUT/ingestenv_fuzzer" "$POC/entry_leak.ienv" >/dev/null 2>&1; then
  fail "bug1 should leak on unpatched build"
fi
pass "bug1 ingestenv entry leak reproduces"

if ASAN_OPTIONS=detect_leaks=1 "$OUT/toml_fuzzer" "$POC/audit_leak.toml" >/dev/null 2>&1; then
  fail "bug2 should leak on unpatched build"
fi
pass "bug2 toml audit leak reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/partition_router_fuzzer" "$POC/partition_router_uaf.bin" >/dev/null 2>&1; then
  fail "bug3 should UAF on unpatched build"
fi
pass "bug3 partition router UAF reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/toml_merge_fuzzer" "$POC/merge_uaf.bin" >/dev/null 2>&1; then
  fail "bug4 should UAF on unpatched build"
fi
pass "bug4 toml merge UAF reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/ingestenv_fuzzer" "$POC/empty_serialize.ienv" >/dev/null 2>&1; then
  fail "bug5 should crash on unpatched build"
fi
pass "bug5 ingestenv empty serialize null deref reproduces"

echo "All unpatched PoCs verified."
'''
    write(ARTIFACTS / "wsl_test_pocs.sh", wsl_test)
    (ARTIFACTS / "wsl_test_pocs.sh").chmod(0o755)


def generate_patches() -> None:
    submit = ARTIFACTS / "poc" / "submit"
    wp_submit = Path("/home/samuel/Documents/fenrir3/artifacts/waypointcfg/poc/submit")

    patch_map = [
        ("bug1_ingestenv_entry_leak.patch", wp_submit / "bug1_wayenv_entry_leak.patch"),
        ("bug2_toml_audit_leak.patch", wp_submit / "bug2_toml_audit_leak.patch"),
        ("bug3_partition_router_uaf.patch", wp_submit / "bug3_traffic_split_uaf.patch"),
        ("bug4_toml_merge_uaf.patch", wp_submit / "bug4_toml_merge_uaf.patch"),
        ("bug5_ingestenv_empty_serialize_null_deref.patch",
         wp_submit / "bug5_wayenv_empty_serialize_null_deref.patch"),
    ]
    for out_name, src in patch_map:
        if not src.exists():
            print(f"WARN missing patch source: {src}")
            continue
        text = src.read_text(encoding="utf-8")
        for old, new in TEXT_RENAME:
            text = text.replace(old, new)
        write(submit / out_name, text)

    tasks = {
        "bug1_TASK_DESCRIPTION.txt": (
            "A memory leak occurs when parsing an ingestenv assignment: ingestenv_set_entry "
            "reallocates internal entry storage, but that heap memory is not freed when "
            "ingestenv_doc_destroy runs in src/ingestenv/store.cpp."
        ),
        "bug2_TASK_DESCRIPTION.txt": (
            "A memory leak occurs in the TOML document audit key path when toml_parse "
            "records assignment keys into doc->audit_keys without releasing them during "
            "document teardown in src/toml/document.cpp."
        ),
        "bug3_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in partition_router_finalize_digest in src/partition_router.cpp "
            "when digest finalization reads partition label bytes through pending references registered "
            "before partition_router_compact reallocates and frees the original label storage during "
            "multi-slot registration in the partition router compaction pipeline, triggered via partition_router_fuzzer."
        ),
        "bug4_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs during TOML table merge in src/toml/merge.cpp when "
            "merge_table_in_place caches overlay entry key pointers then rebuilds the overlay "
            "table index mid-loop, leaving stale key references that are read on subsequent merge "
            "iterations via toml_merge_fuzzer."
        ),
        "bug5_TASK_DESCRIPTION.txt": (
            "A null pointer dereference occurs in ingestenv_serialize_doc in src/ingestenv/serialize.cpp "
            "when serializing a document with zero entries copies from buf.data even though the "
            "internal buffer was never allocated, triggered via ingestenv_fuzzer with zero-length input."
        ),
    }
    for fname, desc in tasks.items():
        write(submit / fname, desc + "\n")


def verify_build_and_pocs() -> None:
    subprocess.check_call(["bash", "build/wsl_build.sh"], cwd=ROOT)
    subprocess.check_call(["bash", str(ARTIFACTS / "wsl_test_pocs.sh")])


def verify_patches() -> None:
    submit = ARTIFACTS / "poc" / "submit"
    verified = ARTIFACTS / "poc" / "verified"
    out = "/tmp/ingestcfg_out"
    tests = [
        ("bug1_ingestenv_entry_leak.patch", "ingestenv_fuzzer", "entry_leak.ienv", "detect_leaks=1", True),
        ("bug2_toml_audit_leak.patch", "toml_fuzzer", "audit_leak.toml", "detect_leaks=1", True),
        ("bug3_partition_router_uaf.patch", "partition_router_fuzzer", "partition_router_uaf.bin", "detect_leaks=0", True),
        ("bug4_toml_merge_uaf.patch", "toml_merge_fuzzer", "merge_uaf.bin", "detect_leaks=0", True),
        ("bug5_ingestenv_empty_serialize_null_deref.patch", "ingestenv_fuzzer", "empty_serialize.ienv", "detect_leaks=0", True),
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
        ["gh", "repo", "create", "tolossamuel/ingestcfg",
         "--private",
         "--description", "C++ data ingestion pipeline config library (TOML + ingestenv) for ClusterFuzzLite",
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
    if "--push" in sys.argv:
        push_github()
    n = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()
    loc = subprocess.check_output(
        ["find", "src", "include", "-name", "*.cpp", "-o", "-name", "*.h"],
        cwd=ROOT, text=True,
    ).strip().split("\n")
    kb = sum(
        (ROOT / p).stat().st_size
        for p in loc if p and (ROOT / p).exists()
    ) // 1024
    print(f"OK ingestcfg — {n} commits, {len(loc)} source files, ~{kb} KB src+include")


if __name__ == "__main__":
    main()
