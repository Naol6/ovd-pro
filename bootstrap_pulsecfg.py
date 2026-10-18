#!/usr/bin/env python3
"""Bootstrap pulsecfg — C++ pulse telemetry export pipeline orchestration + pulseenv overlays."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/pulsecfg")
SRC = Path("/home/samuel/Documents/fenrir3/ingestcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/pulsecfg")

TEXT_RENAME = [
    ("ingestcfg_validate_ingest_manifest", "pulsecfg_validate_pulse_manifest"),
    ("ingestcfg_apply_ingestenv_to_toml", "pulsecfg_apply_pulseenv_to_toml"),
    ("ingestcfg_load_ingestenv_memory", "pulsecfg_load_pulseenv_memory"),
    ("ingestcfg_ingestenv_free", "pulsecfg_pulseenv_free"),
    ("ingestcfg_load_toml_memory", "pulsecfg_load_toml_memory"),
    ("ingestcfg_toml_free", "pulsecfg_toml_free"),
    ("ingestcfg_default_options", "pulsecfg_default_options"),
    ("ingestcfg_options_t", "pulsecfg_options_t"),
    ("partition_router_t", "sink_router_t"),
    ("partition_router_", "sink_router_"),
    ("partition_router", "sink_router"),
    ("partition_lane_t", "export_sink_t"),
    ("partition_lane", "export_sink"),
    ("batch_window_t", "window_rollup_t"),
    ("batch_window_", "window_rollup_"),
    ("batch_window", "window_rollup"),
    ("batch_tick_t", "rollup_tick_t"),
    ("batch_tick", "rollup_tick"),
    ("schema_tracker_t", "cardinality_tracker_t"),
    ("schema_tracker_", "cardinality_tracker_"),
    ("schema_tracker", "cardinality_tracker"),
    ("ack_gate_", "rate_gate_"),
    ("ack_gate", "rate_gate"),
    ("ingest_coordinator", "pulse_coordinator"),
    ("ingest_merge", "pulse_merge"),
    ("ingest_fuzzer", "pulse_fuzzer"),
    ("ingestenv_doc_impl_t", "pulseenv_doc_impl_t"),
    ("ingestenv_doc_t", "pulseenv_doc_t"),
    ("ingestenv_error_t", "pulseenv_error_t"),
    ("ingestenv_options_t", "pulseenv_options_t"),
    ("ingestenv_entry_t", "pulseenv_entry_t"),
    ("ingestenv_slice_t", "pulseenv_slice_t"),
    ("ingestenv_arena_t", "pulseenv_arena_t"),
    ("ingestenv_token_kind_t", "pulseenv_token_kind_t"),
    ("ingestenv_token_t", "pulseenv_token_t"),
    ("ingestenv_internal.h", "pulseenv_internal.h"),
    ("include/ingestenv", "include/pulseenv"),
    ("src/ingestenv/", "src/pulseenv/"),
    ("src/ingestenv", "src/pulseenv"),
    ("ingestenv_", "pulseenv_"),
    ("INGESTENV_", "PULSEENV_"),
    ("Ingestenv", "Pulseenv"),
    ("ingestenv", "pulseenv"),
    ("pipeline_stack", "pulse_stack"),
    ("pipeline_ctx", "pulse_ctx"),
    ("@pipeline", "@pulse"),
    ("ingestmap", "pulsemap"),
    ("ingestloader", "pulseloader"),
    ("INGESTCFG", "PULSECFG"),
    ("IngestCfg", "PulseCfg"),
    ("ingestcfg", "pulsecfg"),
    ("INGEST_", "PULSE_"),
    ("tolossamuel/ingestcfg", "tolossamuel/pulsecfg"),
    ("/tmp/ingestcfg_out", "/tmp/pulsecfg_out"),
    ("compile_ingestenv", "compile_pulseenv"),
    (".ienv", ".penv"),
    ("Data ingestion pipeline orchestration for stream processing",
     "Pulse telemetry collection and export pipeline orchestration"),
    ("data ingestion pipeline orchestration for stream processing",
     "pulse telemetry collection and export pipeline orchestration"),
    ("ingestenv runtime pipeline overlays", "pulseenv runtime export overlays"),
    ("Ingestenv layer", "Pulseenv layer"),
    ("Ingest coordinator validation", "Pulse coordinator validation"),
    ("acknowledgment gates", "rate limiting gates"),
    ("partition routing lanes", "telemetry export sink lanes"),
    ("batch flush window trackers", "time window rollup trackers"),
    ("[ingest]", "[pulse]"),
    ("ingest.partitions", "pulse.sinks"),
    ("ingest pipeline", "pulse export pipeline"),
    ("ingest.toml", "pulse.toml"),
    ("ingest.runtime", "pulse.runtime"),
    ("flush_interval_ms", "rollup_interval_ms"),
    ("pipeline_mode", "export_mode"),
    ("PIPELINE_GENERATION", "PULSE_GENERATION"),
    ("PIPELINE_MODE", "EXPORT_MODE"),
    ("FLUSH_INTERVAL_MS", "ROLLUP_INTERVAL_MS"),
    ('"partitions"', '"sinks"'),
    ('"partition"', '"sink"'),
    ("shard-a", "metrics-a"),
    ("shard-b", "metrics-b"),
    ("Ingest", "Pulse"),
    ("ingest", "pulse"),
    ("pipeline", "export"),
    ("commit", "emit"),
    ("Partition router", "Sink router"),
    ("partition router", "sink router"),
    ("Batch window", "Window rollup"),
    ("batch window", "window rollup"),
    ("Schema tracker", "Cardinality tracker"),
    ("schema tracker", "cardinality tracker"),
    ("partition_router_uaf", "sink_router_uaf"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

NAME_SUBS = [
    ("partition_router", "sink_router"),
    ("batch_window", "window_rollup"),
    ("schema_tracker", "cardinality_tracker"),
    ("ack_gate", "rate_gate"),
    ("ingest_coordinator", "pulse_coordinator"),
    ("ingest_merge", "pulse_merge"),
    ("ingest_fuzzer", "pulse_fuzzer"),
    ("ingestenv_fuzzer", "pulseenv_fuzzer"),
    ("ingestloader", "pulseloader"),
    ("ingestenv_internal", "pulseenv_internal"),
    ("ingestenv_types", "pulseenv_types"),
    ("ingestenv", "pulseenv"),
    ("ingestmap", "pulsemap"),
    ("ingestcfg", "pulsecfg"),
    ("pipeline_stack", "pulse_stack"),
    ("pipeline_ctx", "pulse_ctx"),
    ("ingest.runtime", "pulse.runtime"),
    ("ingest.toml", "pulse.toml"),
]

DIR_RENAMES = [
    ("include/ingestcfg", "include/pulsecfg"),
    ("include/ingestenv", "include/pulseenv"),
    ("src/ingestenv", "src/pulseenv"),
    ("fuzz/corpus/ingestenv_fuzzer", "fuzz/corpus/pulseenv_fuzzer"),
    ("fuzz/corpus/ingest_fuzzer", "fuzz/corpus/pulse_fuzzer"),
    ("fuzz/corpus/partition_router_fuzzer", "fuzz/corpus/sink_router_fuzzer"),
    ("fuzz/corpus/batch_window_fuzzer", "fuzz/corpus/window_rollup_fuzzer"),
    ("fuzz/corpus/schema_tracker_fuzzer", "fuzz/corpus/cardinality_tracker_fuzzer"),
]

COMMITS_RAW = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add pulsecfg public headers", [
        "include/pulsecfg/pulsecfg.h", "include/pulsecfg/pulse_merge.h"]),
    ("include: add pulseenv public API", [
        "include/pulseenv/pulseenv.h", "include/pulseenv/pulseenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add pulse coordinator and sink router headers", [
        "include/pulsecfg/pulse_coordinator.h", "include/pulsecfg/rate_gate.h",
        "include/pulsecfg/sink_router.h", "include/pulsecfg/window_rollup.h"]),
    ("include: add cardinality tracker header", ["include/pulsecfg/cardinality_tracker.h"]),
    ("src/pulseenv: add buffer and string utilities", [
        "src/pulseenv/buffer.cpp", "src/pulseenv/buffer.h", "src/pulseenv/strutil.cpp",
        "src/pulseenv/strutil.h"]),
    ("src/pulseenv: add arena allocator", [
        "src/pulseenv/arena.cpp", "src/pulseenv/arena.h", "src/pulseenv/pulseenv_internal.h"]),
    ("src/pulseenv: add error helpers", ["src/pulseenv/error.cpp", "src/pulseenv/error.h"]),
    ("src/pulseenv: add UTF-8 validation", ["src/pulseenv/utf8.cpp", "src/pulseenv/utf8.h"]),
    ("src/pulseenv: implement pulseenv line lexer", ["src/pulseenv/lexer.cpp", "src/pulseenv/lexer.h"]),
    ("src/pulseenv: add quoted value unescape", ["src/pulseenv/unescape.cpp", "src/pulseenv/unescape.h"]),
    ("src/pulseenv: add document store", ["src/pulseenv/store.cpp", "src/pulseenv/store.h"]),
    ("src/pulseenv: wire assignment parser", ["src/pulseenv/parser.cpp", "src/pulseenv/parser.h"]),
    ("src/pulseenv: add serialize to pulseenv text", ["src/pulseenv/serialize.cpp", "src/pulseenv/serialize.h"]),
    ("src/pulseenv: add validation pass", ["src/pulseenv/validate.cpp", "src/pulseenv/validate.h"]),
    ("src/pulseenv: add merge overlay", ["src/pulseenv/merge.cpp", "src/pulseenv/merge.h"]),
    ("src/pulseenv: add expand and coerce", [
        "src/pulseenv/expand.cpp", "src/pulseenv/expand.h", "src/pulseenv/coerce.cpp",
        "src/pulseenv/coerce.h"]),
    ("src/pulseenv: add walk query diff", [
        "src/pulseenv/walk.cpp", "src/pulseenv/walk.h", "src/pulseenv/query.cpp",
        "src/pulseenv/query.h", "src/pulseenv/diff.cpp", "src/pulseenv/diff.h"]),
    ("src/pulseenv: add pretty printer", ["src/pulseenv/pretty.cpp", "src/pulseenv/pretty.h"]),
    ("src/pulseenv: add pulse stack and ctx", [
        "src/pulseenv/pulse_stack.cpp", "src/pulseenv/pulse_stack.h",
        "src/pulseenv/pulse_ctx.cpp", "src/pulseenv/pulse_ctx.h"]),
    ("src/pulseenv: add path filter profile", [
        "src/pulseenv/path.cpp", "src/pulseenv/path.h", "src/pulseenv/filter.cpp",
        "src/pulseenv/filter.h", "src/pulseenv/profile.cpp", "src/pulseenv/profile.h"]),
    ("src/pulseenv: add snapshot readutil strict canonical", [
        "src/pulseenv/snapshot.cpp", "src/pulseenv/snapshot.h", "src/pulseenv/readutil.cpp",
        "src/pulseenv/readutil.h", "src/pulseenv/strict.cpp", "src/pulseenv/strict.h",
        "src/pulseenv/canonical.cpp", "src/pulseenv/canonical.h"]),
    ("src/pulseenv: add pulseloader and main pulseenv module", [
        "src/pulseenv/pulseloader.cpp", "src/pulseenv/pulseenv.cpp", "src/pulseenv/pulsemap.cpp",
        "src/pulseenv/pulsemap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.cpp", "src/toml/buffer.cpp"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.cpp", "src/toml/datetime.cpp", "src/toml/lexer.cpp"]),
    ("src/toml: add value and parser core", ["src/toml/value.cpp", "src/toml/parser.cpp"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.cpp", "src/toml/merge.cpp", "src/toml/serialize.cpp"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.cpp", "src/toml/format.cpp", "src/toml/validator.cpp", "src/toml/document.cpp"]),
    ("src: add pulsecfg bridge and pulseenv-to-toml merge", ["src/pulsecfg.cpp", "src/pulse_merge.cpp"]),
    ("src: add pulse coordinator validator", ["src/pulse_coordinator.cpp"]),
    ("src: add rate gate evaluator", ["src/rate_gate.cpp"]),
    ("src: add sink router slot tracker", ["src/sink_router.cpp"]),
    ("src: add window rollup for telemetry batching", ["src/window_rollup.cpp"]),
    ("src: add cardinality tracker for metric evolution", ["src/cardinality_tracker.cpp"]),
    ("tests: add Unity harness", ["tests/unity/unity.cpp", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.cpp", "tests/test_basic.cpp"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.cpp", "tests/test_merge.cpp", "tests/test_validate.cpp"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.cpp", "tests/test_coerce.cpp", "tests/test_integration.cpp",
        "tests/test_scenarios.cpp"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.cpp", "tests/test_lexer_exhaustive.cpp"]),
    ("tests: add pulse coordinator and sink router unit tests", [
        "tests/test_pulse_coordinator.cpp", "tests/test_sink_router.cpp"]),
    ("tests: add window rollup and cardinality tracker unit tests", [
        "tests/test_window_rollup.cpp", "tests/test_cardinality_tracker.cpp"]),
    ("examples: add TOML pulse manifest and runtime overlay", [
        "examples/pulse.toml", "examples/pulse.runtime"]),
    ("fuzz: add pulseenv_fuzzer harness", ["fuzz/pulseenv_fuzzer.cc"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.cc"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.cc"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.cc"]),
    ("fuzz: add pulse_fuzzer for cross-format overlay", ["fuzz/pulse_fuzzer.cc"]),
    ("fuzz: add sink_router_fuzzer for compaction path", ["fuzz/sink_router_fuzzer.cc"]),
    ("fuzz: add window_rollup_fuzzer for rollup path", ["fuzz/window_rollup_fuzzer.cc"]),
    ("fuzz: add cardinality_tracker_fuzzer for cardinality path", ["fuzz/cardinality_tracker_fuzzer.cc"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/pulseenv_fuzzer/minimal.penv",
        "fuzz/corpus/pulseenv_fuzzer/quoted.penv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/pulse_fuzzer/sample.bin",
        "fuzz/corpus/sink_router_fuzzer/seed.bin",
        "fuzz/corpus/window_rollup_fuzzer/seed.bin",
        "fuzz/corpus/cardinality_tracker_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for pulsecfg library", ["README.md"]),
    ("docs: add BUILDING notes", ["docs/BUILDING.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable pulse telemetry library", []),
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

    corp = ROOT / "fuzz" / "corpus" / "pulseenv_fuzzer"
    if corp.exists():
        for old in list(corp.glob("*.ienv")) + list(corp.glob("*.penv")):
            old.rename(old.with_suffix(".penv"))


def transform_contents() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.name in SKIP_FILES:
            path.unlink(missing_ok=True)
            continue
        if path.suffix not in {
            ".cpp", ".h", ".cc", ".sh", ".yaml", ".md", ".txt", ".toml",
            ".penv", ".ienv", ".env", "Makefile"
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
    path = ROOT / "src" / "pulse_coordinator.cpp"
    text = path.read_text(encoding="utf-8")
    text = text.replace('tome_table_get(tbl, "lanes")', 'tome_table_get(tbl, "sinks")')
    text = text.replace('"lane"', '"sink"')
    path.write_text(text, encoding="utf-8")


README = """# pulsecfg

pulsecfg is a C++17 library for **pulse telemetry collection and export pipeline orchestration**: parse TOML pulse manifests, load pulseenv runtime export overlays, merge layers, validate rate limiting gates, and track telemetry export sink lanes plus time window rollup trackers.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Pulseenv layer** — `KEY=VALUE`, `@pulse` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply pulseenv overlay keys onto parsed TOML documents
- **Pulse coordinator** — validate `[pulse]` tables and register export weights into a sink router
- **Window rollup** — track telemetry batch rollup cadence across export epochs
- **Cardinality tracker** — accumulate metric cardinality scores during progressive export
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `pulseenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `pulse_fuzzer`, `sink_router_fuzzer`, `window_rollup_fuzzer`, `cardinality_tracker_fuzzer`.

## License

MIT — see LICENSE.
"""

BUILDING = """# Building pulsecfg

## Requirements

- clang/clang++ 14+
- libFuzzer (via `-fsanitize=fuzzer` or `$LIB_FUZZING_ENGINE`)

## Local ASan build

```bash
bash build/wsl_build.sh
```

Fuzzers land in `/tmp/pulsecfg_out/`.

## Unit tests

```bash
make test
```
"""


def add_domain() -> None:
    write(ROOT / "README.md", README)
    write(ROOT / "docs" / "BUILDING.md", BUILDING)

    write(ROOT / "examples" / "pulse.toml", """[pulse]
name = "metrics-stream"
rollup_interval_ms = 60000
export_mode = "linear"

[[pulse.sinks]]
label = "metrics-a"
weight = 90

[[pulse.sinks]]
label = "metrics-b"
weight = 10
""")

    write(ROOT / "examples" / "pulse.runtime", """# Runtime pulse export parameters injected during emit
ROLLUP_INTERVAL_MS=30000
EXPORT_MODE=linear
PULSE_GENERATION=2
""")

    write(ROOT / "tests" / "test_cardinality_tracker.cpp", '''#include "pulsecfg/cardinality_tracker.h"
#include "unity/unity.h"

void test_cardinality_tracker_score(void) {
  cardinality_tracker_t rw;
  cardinality_tracker_init(&rw);
  TEST_ASSERT_EQUAL(0, cardinality_tracker_note_bind(&rw, "metrics-a", 3));
  TEST_ASSERT_EQUAL(0, cardinality_tracker_note_migration(&rw, "metrics-b"));
  TEST_ASSERT_NOT_EQUAL(0u, cardinality_tracker_score(&rw));
  cardinality_tracker_reset(&rw);
}
''')

    write(ROOT / "fuzz" / "corpus" / "pulse_fuzzer" / "sample.bin",
          bytes([32]) + b"[pulse]\nname=\"x\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "sink_router_fuzzer" / "seed.bin", bytes(range(32, 96)))
    write(ROOT / "fuzz" / "corpus" / "window_rollup_fuzzer" / "seed.bin", bytes(range(16, 128)))
    write(ROOT / "fuzz" / "corpus" / "cardinality_tracker_fuzzer" / "seed.bin", bytes(range(8, 64)))


def plant_bugs() -> None:
    """Keep hardened unescape; plant pulseenv empty-serialize null deref for bug5."""
    ser = (ROOT / "src" / "pulseenv" / "serialize.cpp").read_text(encoding="utf-8")
    ser = ser.replace(
        "  if (buf.len > 0) {\n"
        "    memcpy(*out_buf, buf.data, buf.len + 1);\n"
        "  } else {\n"
        "    (*out_buf)[0] = '\\0';\n"
        "  }",
        "  memcpy(*out_buf, buf.data, buf.len + 1);",
    )
    (ROOT / "src" / "pulseenv" / "serialize.cpp").write_text(ser, encoding="utf-8")


def patch_build() -> None:
    build_sh = '''#!/bin/bash -eu

OBJECTS=()

compile_pulseenv() {
  local base="$1"
  local obj="pulseenv_${base%.cpp}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall -D_GNU_SOURCE} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/pulseenv" \\
    -c "${SRC:-.}/src/pulseenv/${base}" -o "${obj}"
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
         validate merge expand coerce walk query diff pretty pulse_stack \\
         pulse_ctx path filter pulsemap profile canonical strict readutil \\
         snapshot pulseloader pulseenv; do
  if [ -f "${SRC:-.}/src/pulseenv/${f}.cpp" ]; then
    compile_pulseenv "${f}.cpp"
  fi
done

for f in memory buffer unicode datetime lexer value parser path merge serialize \\
         diag format validator document; do
  compile_toml "${f}.cpp"
done

for f in pulsecfg pulse_merge pulse_coordinator rate_gate sink_router window_rollup cardinality_tracker; do
  obj="${f}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/pulseenv" -I"${SRC:-.}/src/toml" \\
    -c "${SRC:-.}/src/${f}.cpp" -o "${obj}"
  OBJECTS+=("${obj}")
done

FUZZ_CXXFLAGS="${CXXFLAGS:- -O1 -g -std=c++17}"
INCS="-I${SRC:-.}/include -I${SRC:-.}/src/pulseenv -I${SRC:-.}/src/toml"

build_fuzzer() {
  ${CXX:-clang++} ${FUZZ_CXXFLAGS} ${LIB_FUZZING_ENGINE} \\
    "${SRC:-.}/fuzz/$1" "${OBJECTS[@]}" ${INCS} \\
    -o "${OUT:-.}/$2" -lm
}

build_fuzzer pulseenv_fuzzer.cc pulseenv_fuzzer
build_fuzzer toml_fuzzer.cc toml_fuzzer
build_fuzzer toml_merge_fuzzer.cc toml_merge_fuzzer
build_fuzzer toml_format_fuzzer.cc toml_format_fuzzer
build_fuzzer pulse_fuzzer.cc pulse_fuzzer
build_fuzzer sink_router_fuzzer.cc sink_router_fuzzer
build_fuzzer window_rollup_fuzzer.cc window_rollup_fuzzer
build_fuzzer cardinality_tracker_fuzzer.cc cardinality_tracker_fuzzer
'''
    write(ROOT / ".clusterfuzzlite/build.sh", build_sh)

    wsl = '''#!/bin/bash -eu
set -o pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${OUT:-/tmp/pulsecfg_out}"
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
  - pulseenv_fuzzer
  - toml_fuzzer
  - toml_merge_fuzzer
  - toml_format_fuzzer
  - pulse_fuzzer
  - sink_router_fuzzer
  - window_rollup_fuzzer
  - cardinality_tracker_fuzzer
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
CXXFLAGS ?= -std=c++17 -O2 -g -Wall -Wextra -Wpedantic -Werror -Iinclude -Isrc/pulseenv -Isrc/toml
PULSEENV_SRC := $(wildcard src/pulseenv/*.cpp)
TOML_SRC := $(wildcard src/toml/*.cpp)
CORE_SRC := src/pulsecfg.cpp src/pulse_merge.cpp src/pulse_coordinator.cpp src/rate_gate.cpp src/sink_router.cpp src/window_rollup.cpp src/cardinality_tracker.cpp
TEST_SRC := $(wildcard tests/test_*.cpp)
TEST := build/pulsecfg_tests

$(TEST): $(PULSEENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) | build
\t$(CXX) $(CXXFLAGS) $(PULSEENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) -o $@

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

    write(verified / "entry_leak.penv", "FOO=1\n")
    write(verified / "audit_leak.toml", 'k = "v"\n')
    write(verified / "empty_serialize.penv", b"")
    write(verified / "sink_router_uaf.bin", bytes(range(32, 160)))

    ic_verified = Path("/home/samuel/Documents/fenrir3/artifacts/ingestcfg/poc/verified")
    if (ic_verified / "merge_uaf.bin").exists():
        shutil.copy(ic_verified / "merge_uaf.bin", verified / "merge_uaf.bin")

    write(poc_dir / "README.txt", """pulsecfg local artifacts — NOT on GitHub

verified/
  entry_leak.penv              — bug1 pulseenv entry realloc leak
  audit_leak.toml              — bug2 toml audit key leak
  sink_router_uaf.bin          — bug3 sink router compaction UAF
  merge_uaf.bin                — bug4 toml merge overlay index UAF
  empty_serialize.penv         — bug5 pulseenv empty serialize null deref

submit/
  bugN_*.patch + bugN_TASK_DESCRIPTION.txt

Verify: bash artifacts/pulsecfg/wsl_test_pocs.sh
""")

    write(ARTIFACTS / "TASKS.md", """# pulsecfg task queue

GitHub: tolossamuel/pulsecfg

| # | Bug | Harness | Class | Status |
|---|-----|---------|-------|--------|
| 1 | pulseenv entry realloc leak | pulseenv_fuzzer | LeakSanitizer | Ready |
| 2 | toml audit key leak | toml_fuzzer | LeakSanitizer | Ready |
| 3 | sink router compaction UAF | sink_router_fuzzer | heap-use-after-free | Ready |
| 4 | toml merge UAF | toml_merge_fuzzer | heap-use-after-free | Ready |
| 5 | pulseenv empty serialize null deref | pulseenv_fuzzer | null deref | Ready |

PoC bytes and patches: artifacts/pulsecfg/poc/ (not on GitHub).
""")

    wsl_test = '''#!/bin/bash -eu
ROOT="$(cd "$(dirname "$0")/../../pulsecfg" && pwd)"
POC="${POC_DIR:-$(dirname "$0")/poc/verified}"
OUT="${OUT:-/tmp/pulsecfg_out}"

cd "$ROOT"
CC=clang CXX=clang++ bash build/wsl_build.sh >/dev/null

fail() { echo "FAIL: $*"; exit 1; }
pass() { echo "PASS: $*"; }

if ASAN_OPTIONS=detect_leaks=1 "$OUT/pulseenv_fuzzer" "$POC/entry_leak.penv" >/dev/null 2>&1; then
  fail "bug1 should leak on unpatched build"
fi
pass "bug1 pulseenv entry leak reproduces"

if ASAN_OPTIONS=detect_leaks=1 "$OUT/toml_fuzzer" "$POC/audit_leak.toml" >/dev/null 2>&1; then
  fail "bug2 should leak on unpatched build"
fi
pass "bug2 toml audit leak reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/sink_router_fuzzer" "$POC/sink_router_uaf.bin" >/dev/null 2>&1; then
  fail "bug3 should UAF on unpatched build"
fi
pass "bug3 sink router UAF reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/toml_merge_fuzzer" "$POC/merge_uaf.bin" >/dev/null 2>&1; then
  fail "bug4 should UAF on unpatched build"
fi
pass "bug4 toml merge UAF reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/pulseenv_fuzzer" "$POC/empty_serialize.penv" >/dev/null 2>&1; then
  fail "bug5 should crash on unpatched build"
fi
pass "bug5 pulseenv empty serialize null deref reproduces"

echo "All unpatched PoCs verified."
'''
    write(ARTIFACTS / "wsl_test_pocs.sh", wsl_test)
    (ARTIFACTS / "wsl_test_pocs.sh").chmod(0o755)


def generate_patches() -> None:
    submit = ARTIFACTS / "poc" / "submit"
    ic_submit = Path("/home/samuel/Documents/fenrir3/artifacts/ingestcfg/poc/submit")

    patch_map = [
        ("bug1_pulseenv_entry_leak.patch", ic_submit / "bug1_ingestenv_entry_leak.patch"),
        ("bug2_toml_audit_leak.patch", ic_submit / "bug2_toml_audit_leak.patch"),
        ("bug3_sink_router_uaf.patch", ic_submit / "bug3_partition_router_uaf.patch"),
        ("bug4_toml_merge_uaf.patch", ic_submit / "bug4_toml_merge_uaf.patch"),
        ("bug5_pulseenv_empty_serialize_null_deref.patch",
         ic_submit / "bug5_ingestenv_empty_serialize_null_deref.patch"),
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
            "A memory leak occurs when parsing a pulseenv assignment: pulseenv_set_entry "
            "reallocates internal entry storage, but that heap memory is not freed when "
            "pulseenv_doc_destroy runs in src/pulseenv/store.cpp."
        ),
        "bug2_TASK_DESCRIPTION.txt": (
            "A memory leak occurs in the TOML document audit key path when tome_parse "
            "records assignment keys into doc->audit_keys without releasing them during "
            "document teardown in src/toml/parser.cpp."
        ),
        "bug3_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in sink_router_finalize_digest in src/sink_router.cpp "
            "when digest finalization reads export sink label bytes through pending references "
            "registered before sink_router_compact reallocates and frees the original label storage "
            "during multi-slot registration in the sink router compaction pipeline, triggered via "
            "sink_router_fuzzer."
        ),
        "bug4_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs during TOML table merge in src/toml/merge.cpp when "
            "merge_table_in_place caches overlay entry key pointers then rebuilds the overlay "
            "table index mid-loop, leaving stale key references that are read on subsequent merge "
            "iterations via toml_merge_fuzzer."
        ),
        "bug5_TASK_DESCRIPTION.txt": (
            "A null pointer dereference occurs in pulseenv_serialize_doc in src/pulseenv/serialize.cpp "
            "when serializing a document with zero entries copies from buf.data even though the "
            "internal buffer was never allocated, triggered via pulseenv_fuzzer with zero-length input."
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
    out = "/tmp/pulsecfg_out"
    tests = [
        ("bug1_pulseenv_entry_leak.patch", "pulseenv_fuzzer", "entry_leak.penv", "detect_leaks=1", True),
        ("bug2_toml_audit_leak.patch", "toml_fuzzer", "audit_leak.toml", "detect_leaks=1", True),
        ("bug3_sink_router_uaf.patch", "sink_router_fuzzer", "sink_router_uaf.bin", "detect_leaks=0", True),
        ("bug4_toml_merge_uaf.patch", "toml_merge_fuzzer", "merge_uaf.bin", "detect_leaks=0", True),
        ("bug5_pulseenv_empty_serialize_null_deref.patch", "pulseenv_fuzzer", "empty_serialize.penv", "detect_leaks=0", True),
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
        ["gh", "repo", "create", "tolossamuel/pulsecfg",
         "--private",
         "--description", "C++ pulse telemetry export pipeline config library (TOML + pulseenv) for ClusterFuzzLite",
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
    print(f"OK pulsecfg — {n} commits, {len(loc)} source files, ~{kb} KB src+include")


if __name__ == "__main__":
    main()
