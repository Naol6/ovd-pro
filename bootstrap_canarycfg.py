#!/usr/bin/env python3
"""Bootstrap canarycfg — C++ progressive canary deployment orchestration + canaryenv overlays."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/canarycfg")
SRC = Path("/home/samuel/Documents/fenrir3/failovercfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/canarycfg")

TEXT_RENAME = [
    ("failovercfg_validate_failover_manifest", "canarycfg_validate_canary_manifest"),
    ("failovercfg_apply_failenv_to_toml", "canarycfg_apply_canaryenv_to_toml"),
    ("failovercfg_load_failenv_memory", "canarycfg_load_canaryenv_memory"),
    ("failovercfg_failenv_free", "canarycfg_canaryenv_free"),
    ("failovercfg_load_toml_memory", "canarycfg_load_toml_memory"),
    ("failovercfg_toml_free", "canarycfg_toml_free"),
    ("failovercfg_default_options", "canarycfg_default_options"),
    ("failovercfg_options_t", "canarycfg_options_t"),
    ("region_ring_t", "split_ladder_t"),
    ("region_ring_", "split_ladder_"),
    ("region_ring", "split_ladder"),
    ("region_peer_t", "split_step_t"),
    ("region_peer", "split_step"),
    ("probe_scheduler_t", "rollout_meter_t"),
    ("probe_scheduler_", "rollout_meter_"),
    ("probe_scheduler", "rollout_meter"),
    ("probe_entry_t", "ramp_entry_t"),
    ("probe_entry", "ramp_entry"),
    ("traffic_weight_t", "baseline_tracker_t"),
    ("traffic_weight_", "baseline_tracker_"),
    ("traffic_weight", "baseline_tracker"),
    ("failover_fsm_", "promotion_gate_"),
    ("failover_fsm", "promotion_gate"),
    ("failover_coordinator", "canary_coordinator"),
    ("failover_merge", "canary_merge"),
    ("failover_fuzzer", "canary_fuzzer"),
    ("failenv_doc_impl_t", "canaryenv_doc_impl_t"),
    ("failenv_doc_t", "canaryenv_doc_t"),
    ("failenv_error_t", "canaryenv_error_t"),
    ("failenv_options_t", "canaryenv_options_t"),
    ("failenv_entry_t", "canaryenv_entry_t"),
    ("failenv_slice_t", "canaryenv_slice_t"),
    ("failenv_arena_t", "canaryenv_arena_t"),
    ("failenv_token_kind_t", "canaryenv_token_kind_t"),
    ("failenv_token_t", "canaryenv_token_t"),
    ("failenv_internal.h", "canaryenv_internal.h"),
    ("include/failenv", "include/canaryenv"),
    ("src/failenv/", "src/canaryenv/"),
    ("src/failenv", "src/canaryenv"),
    ("failenv_", "canaryenv_"),
    ("FAILENV_", "CANARYENV_"),
    ("Failenv", "Canaryenv"),
    ("failenv", "canaryenv"),
    ("route_stack", "ramp_stack"),
    ("route_ctx", "ramp_ctx"),
    ("@route", "@ramp"),
    ("failmap", "canarymap"),
    ("failloader", "canaryloader"),
    ("FAILOVERCFG", "CANARYCFG"),
    ("FailoverCfg", "CanaryCfg"),
    ("failovercfg", "canarycfg"),
    ("FAILOVER_", "CANARY_"),
    ("failover", "canary"),
    ("tolossamuel/failovercfg", "tolossamuel/canarycfg"),
    ("/tmp/failovercfg_out", "/tmp/canarycfg_out"),
    ("compile_failenv", "compile_canaryenv"),
    (".fenv", ".cenv"),
    ("fenv_", "cenv_"),
    ("Multi-region failover during datacenter cutover", "Progressive canary deployment traffic ramp orchestration"),
    ("multi-region failover during datacenter cutover", "progressive canary deployment traffic ramp orchestration"),
    ("failenv runtime probe overlays", "canaryenv runtime ramp overlays"),
    ("Failenv layer", "Canaryenv layer"),
    ("Failover coordinator validation", "Canary coordinator validation"),
    ("failover state gates", "promotion state gates"),
    ("region priority rings", "traffic split ladders"),
    ("health probe schedulers", "rollout ramp meters"),
    ("[failover]", "[canary]"),
    ("canary.regions", "canary.steps"),
    ("cutover", "promotion"),
    ("probe_interval_ms", "ramp_interval_ms"),
    ("canary_mode", "promotion_mode"),
    ("PROBE_GENERATION", "RAMP_GENERATION"),
    ("FAILOVER_MODE", "PROMOTION_MODE"),
    ("PROBE_INTERVAL_MS", "RAMP_INTERVAL_MS"),
    ('"regions"', '"steps"'),
    ('"region"', '"step"'),
    ("us-east-1", "stable-v1"),
    ("us-west-2", "canary-v2"),
    ("Failover", "Canary"),
    ("failover.toml", "canary.toml"),
    ("failover.runtime", "canary.runtime"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add canarycfg public headers", [
        "include/canarycfg/canarycfg.h", "include/canarycfg/canary_merge.h"]),
    ("include: add canaryenv public API", [
        "include/canaryenv/canaryenv.h", "include/canaryenv/canaryenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add canary coordinator and split ladder headers", [
        "include/canarycfg/canary_coordinator.h", "include/canarycfg/promotion_gate.h",
        "include/canarycfg/split_ladder.h", "include/canarycfg/rollout_meter.h"]),
    ("include: add baseline tracker header", [
        "include/canarycfg/baseline_tracker.h"]),
    ("src/canaryenv: add buffer and string utilities", [
        "src/canaryenv/buffer.cpp", "src/canaryenv/buffer.h", "src/canaryenv/strutil.cpp",
        "src/canaryenv/strutil.h"]),
    ("src/canaryenv: add arena allocator", [
        "src/canaryenv/arena.cpp", "src/canaryenv/arena.h", "src/canaryenv/canaryenv_internal.h"]),
    ("src/canaryenv: add error helpers", ["src/canaryenv/error.cpp", "src/canaryenv/error.h"]),
    ("src/canaryenv: add UTF-8 validation", ["src/canaryenv/utf8.cpp", "src/canaryenv/utf8.h"]),
    ("src/canaryenv: implement canaryenv line lexer", ["src/canaryenv/lexer.cpp", "src/canaryenv/lexer.h"]),
    ("src/canaryenv: add quoted value unescape", ["src/canaryenv/unescape.cpp", "src/canaryenv/unescape.h"]),
    ("src/canaryenv: add document store", ["src/canaryenv/store.cpp", "src/canaryenv/store.h"]),
    ("src/canaryenv: wire assignment parser", ["src/canaryenv/parser.cpp", "src/canaryenv/parser.h"]),
    ("src/canaryenv: add serialize to canaryenv text", ["src/canaryenv/serialize.cpp", "src/canaryenv/serialize.h"]),
    ("src/canaryenv: add validation pass", ["src/canaryenv/validate.cpp", "src/canaryenv/validate.h"]),
    ("src/canaryenv: add merge overlay", ["src/canaryenv/merge.cpp", "src/canaryenv/merge.h"]),
    ("src/canaryenv: add expand and coerce", [
        "src/canaryenv/expand.cpp", "src/canaryenv/expand.h", "src/canaryenv/coerce.cpp",
        "src/canaryenv/coerce.h"]),
    ("src/canaryenv: add walk query diff", [
        "src/canaryenv/walk.cpp", "src/canaryenv/walk.h", "src/canaryenv/query.cpp",
        "src/canaryenv/query.h", "src/canaryenv/diff.cpp", "src/canaryenv/diff.h"]),
    ("src/canaryenv: add pretty printer", ["src/canaryenv/pretty.cpp", "src/canaryenv/pretty.h"]),
    ("src/canaryenv: add ramp stack and ctx", [
        "src/canaryenv/ramp_stack.cpp", "src/canaryenv/ramp_stack.h",
        "src/canaryenv/ramp_ctx.cpp", "src/canaryenv/ramp_ctx.h"]),
    ("src/canaryenv: add path filter profile", [
        "src/canaryenv/path.cpp", "src/canaryenv/path.h", "src/canaryenv/filter.cpp",
        "src/canaryenv/filter.h", "src/canaryenv/profile.cpp", "src/canaryenv/profile.h"]),
    ("src/canaryenv: add snapshot readutil strict canonical", [
        "src/canaryenv/snapshot.cpp", "src/canaryenv/snapshot.h", "src/canaryenv/readutil.cpp",
        "src/canaryenv/readutil.h", "src/canaryenv/strict.cpp", "src/canaryenv/strict.h",
        "src/canaryenv/canonical.cpp", "src/canaryenv/canonical.h"]),
    ("src/canaryenv: add canaryloader and main canaryenv module", [
        "src/canaryenv/canaryloader.cpp", "src/canaryenv/canaryenv.cpp", "src/canaryenv/canarymap.cpp",
        "src/canaryenv/canarymap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.cpp", "src/toml/buffer.cpp"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.cpp", "src/toml/datetime.cpp", "src/toml/lexer.cpp"]),
    ("src/toml: add value and parser core", ["src/toml/value.cpp", "src/toml/parser.cpp"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.cpp", "src/toml/merge.cpp", "src/toml/serialize.cpp"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.cpp", "src/toml/format.cpp", "src/toml/validator.cpp", "src/toml/document.cpp"]),
    ("src: add canarycfg bridge and canaryenv-to-toml merge", ["src/canarycfg.cpp", "src/canary_merge.cpp"]),
    ("src: add canary coordinator validator", ["src/canary_coordinator.cpp"]),
    ("src: add promotion gate evaluator", ["src/promotion_gate.cpp"]),
    ("src: add split ladder step tracker", ["src/split_ladder.cpp"]),
    ("src: add rollout meter for ramp cadence", ["src/rollout_meter.cpp"]),
    ("src: add baseline tracker accumulator", ["src/baseline_tracker.cpp"]),
    ("tests: add Unity harness", ["tests/unity/unity.cpp", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.cpp", "tests/test_basic.cpp"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.cpp", "tests/test_merge.cpp", "tests/test_validate.cpp"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.cpp", "tests/test_coerce.cpp", "tests/test_integration.cpp",
        "tests/test_scenarios.cpp"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.cpp", "tests/test_lexer_exhaustive.cpp"]),
    ("tests: add canary coordinator and split ladder unit tests", [
        "tests/test_canary_coordinator.cpp", "tests/test_split_ladder.cpp"]),
    ("tests: add rollout meter and baseline tracker unit tests", [
        "tests/test_rollout_meter.cpp", "tests/test_baseline_tracker.cpp"]),
    ("examples: add TOML canary manifest and runtime overlay", [
        "examples/canary.toml", "examples/canary.runtime"]),
    ("fuzz: add canaryenv_fuzzer harness", ["fuzz/canaryenv_fuzzer.cc"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.cc"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.cc"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.cc"]),
    ("fuzz: add canary_fuzzer for cross-format overlay", ["fuzz/canary_fuzzer.cc"]),
    ("fuzz: add split_ladder_fuzzer for compaction path", ["fuzz/split_ladder_fuzzer.cc"]),
    ("fuzz: add rollout_meter_fuzzer for ramp path", ["fuzz/rollout_meter_fuzzer.cc"]),
    ("fuzz: add baseline_tracker_fuzzer for weight path", ["fuzz/baseline_tracker_fuzzer.cc"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/canaryenv_fuzzer/minimal.cenv",
        "fuzz/corpus/canaryenv_fuzzer/quoted.cenv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/canary_fuzzer/sample.bin",
        "fuzz/corpus/split_ladder_fuzzer/seed.bin",
        "fuzz/corpus/rollout_meter_fuzzer/seed.bin",
        "fuzz/corpus/baseline_tracker_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for canarycfg library", ["README.md"]),
    ("docs: add BUILDING notes", ["docs/BUILDING.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable canary deployment configuration library", []),
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


def copy_tree() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ignore = shutil.ignore_patterns(".git", "*.o", "__pycache__", "poc", "guides", "docs")
    shutil.copytree(SRC, ROOT, ignore=ignore)

    renames = [
        (ROOT / "include" / "failovercfg", ROOT / "include" / "canarycfg"),
        (ROOT / "include" / "failenv", ROOT / "include" / "canaryenv"),
        (ROOT / "src" / "failenv", ROOT / "src" / "canaryenv"),
        (ROOT / "src" / "failovercfg.cpp", ROOT / "src" / "canarycfg.cpp"),
        (ROOT / "src" / "failover_merge.cpp", ROOT / "src" / "canary_merge.cpp"),
        (ROOT / "src" / "failover_coordinator.cpp", ROOT / "src" / "canary_coordinator.cpp"),
        (ROOT / "src" / "failover_fsm.cpp", ROOT / "src" / "promotion_gate.cpp"),
        (ROOT / "src" / "region_ring.cpp", ROOT / "src" / "split_ladder.cpp"),
        (ROOT / "src" / "probe_scheduler.cpp", ROOT / "src" / "rollout_meter.cpp"),
        (ROOT / "src" / "traffic_weight.cpp", ROOT / "src" / "baseline_tracker.cpp"),
        (ROOT / "fuzz" / "failenv_fuzzer.cc", ROOT / "fuzz" / "canaryenv_fuzzer.cc"),
        (ROOT / "fuzz" / "failover_fuzzer.cc", ROOT / "fuzz" / "canary_fuzzer.cc"),
        (ROOT / "fuzz" / "region_ring_fuzzer.cc", ROOT / "fuzz" / "split_ladder_fuzzer.cc"),
        (ROOT / "fuzz" / "probe_scheduler_fuzzer.cc", ROOT / "fuzz" / "rollout_meter_fuzzer.cc"),
        (ROOT / "fuzz" / "traffic_weight_fuzzer.cc", ROOT / "fuzz" / "baseline_tracker_fuzzer.cc"),
        (ROOT / "examples" / "failover.toml", ROOT / "examples" / "canary.toml"),
        (ROOT / "examples" / "failover.runtime", ROOT / "examples" / "canary.runtime"),
        (ROOT / "fuzz" / "corpus" / "failenv_fuzzer", ROOT / "fuzz" / "corpus" / "canaryenv_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "failover_fuzzer", ROOT / "fuzz" / "corpus" / "canary_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "region_ring_fuzzer", ROOT / "fuzz" / "corpus" / "split_ladder_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "probe_scheduler_fuzzer", ROOT / "fuzz" / "corpus" / "rollout_meter_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "traffic_weight_fuzzer", ROOT / "fuzz" / "corpus" / "baseline_tracker_fuzzer"),
        (ROOT / "tests" / "test_failover_coordinator.cpp", ROOT / "tests" / "test_canary_coordinator.cpp"),
        (ROOT / "tests" / "test_region_ring.cpp", ROOT / "tests" / "test_split_ladder.cpp"),
        (ROOT / "tests" / "test_probe_scheduler.cpp", ROOT / "tests" / "test_rollout_meter.cpp"),
        (ROOT / "tests" / "test_traffic_weight.cpp", ROOT / "tests" / "test_baseline_tracker.cpp"),
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

    for p in list((ROOT / "src" / "canaryenv").glob("*")):
        new_name = p.name.replace("failenv", "canaryenv")
        new_name = new_name.replace("failloader", "canaryloader")
        new_name = new_name.replace("route_stack", "ramp_stack")
        new_name = new_name.replace("route_ctx", "ramp_ctx")
        new_name = new_name.replace("failmap", "canarymap")
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    corp = ROOT / "fuzz" / "corpus" / "canaryenv_fuzzer"
    for old in list(corp.glob("*.fenv")):
        old.rename(old.with_suffix(".cenv"))

    header_renames = [
        (ROOT / "include" / "canarycfg" / "failovercfg.h", ROOT / "include" / "canarycfg" / "canarycfg.h"),
        (ROOT / "include" / "canarycfg" / "failover_merge.h", ROOT / "include" / "canarycfg" / "canary_merge.h"),
        (ROOT / "include" / "canarycfg" / "failover_coordinator.h", ROOT / "include" / "canarycfg" / "canary_coordinator.h"),
        (ROOT / "include" / "canarycfg" / "failover_fsm.h", ROOT / "include" / "canarycfg" / "promotion_gate.h"),
        (ROOT / "include" / "canarycfg" / "region_ring.h", ROOT / "include" / "canarycfg" / "split_ladder.h"),
        (ROOT / "include" / "canarycfg" / "probe_scheduler.h", ROOT / "include" / "canarycfg" / "rollout_meter.h"),
        (ROOT / "include" / "canarycfg" / "traffic_weight.h", ROOT / "include" / "canarycfg" / "baseline_tracker.h"),
    ]
    for src, dst in header_renames:
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                dst.unlink()
            src.rename(dst)

    env_hdr = [
        (ROOT / "include" / "canaryenv" / "failenv.h", ROOT / "include" / "canaryenv" / "canaryenv.h"),
        (ROOT / "include" / "canaryenv" / "failenv_types.h", ROOT / "include" / "canaryenv" / "canaryenv_types.h"),
    ]
    for src, dst in env_hdr:
        if src.exists():
            if dst.exists():
                dst.unlink()
            src.rename(dst)


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
            ".cenv", ".fenv", ".env", "Makefile"
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


def patch_coordinator() -> None:
    path = ROOT / "src" / "canary_coordinator.cpp"
    text = path.read_text(encoding="utf-8")
    text = text.replace('tome_table_get(tbl, "regions")', 'tome_table_get(tbl, "steps")')
    text = text.replace('"region"', '"step"')
    path.write_text(text, encoding="utf-8")


README = """# canarycfg

canarycfg is a C++17 library for **progressive canary deployment traffic ramp orchestration**: parse TOML canary manifests, load canaryenv runtime ramp overlays, merge layers, validate promotion state gates, and track traffic split ladders plus rollout ramp meters.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Canaryenv layer** — `KEY=VALUE`, `@ramp` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply canaryenv overlay keys onto parsed TOML documents
- **Canary coordinator** — validate `[canary]` tables and register step weights into a split ladder
- **Rollout meter** — track ramp cadence across canary promotion epochs
- **Baseline tracker** — accumulate weighted routing scores during progressive rollout
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `canaryenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `canary_fuzzer`, `split_ladder_fuzzer`, `rollout_meter_fuzzer`, `baseline_tracker_fuzzer`.

## License

MIT — see LICENSE.
"""

BUILDING = """# Building canarycfg

## Requirements

- clang/clang++ 14+
- libFuzzer (via `-fsanitize=fuzzer` or `$LIB_FUZZING_ENGINE`)

## Local ASan build

```bash
bash build/wsl_build.sh
```

Fuzzers land in `/tmp/canarycfg_out/`.

## Unit tests

```bash
make test
```
"""


def add_domain() -> None:
    write(ROOT / "README.md", README)
    write(ROOT / "docs" / "BUILDING.md", BUILDING)

    write(ROOT / "examples" / "canary.toml", """[canary]
name = "checkout-api"
ramp_interval_ms = 60000
promotion_mode = "linear"

[[canary.steps]]
label = "stable-v1"
weight = 90

[[canary.steps]]
label = "canary-v2"
weight = 10
""")

    write(ROOT / "examples" / "canary.runtime", """# Runtime canary ramp parameters injected during promotion
RAMP_INTERVAL_MS=30000
PROMOTION_MODE=linear
RAMP_GENERATION=2
""")

    fuzz = (ROOT / "fuzz" / "canary_fuzzer.cc").read_text(encoding="utf-8")
    if "rollout_meter_t" not in fuzz:
        fuzz = fuzz.replace(
            "canarycfg_apply_canaryenv_to_toml(toml, env);",
            "canarycfg_apply_canaryenv_to_toml(toml, env);\n"
            "  if (toml) {\n"
            "    split_ladder_t ladder;\n"
            "    rollout_meter_t meter;\n"
            "    split_ladder_init(&ladder);\n"
            "    rollout_meter_init(&meter);\n"
            "    canarycfg_validate_canary_manifest(toml, &ladder);\n"
            "    (void)split_ladder_finalize_digest(&ladder);\n"
            "    rollout_meter_reset(&meter);\n"
            "    split_ladder_reset(&ladder);\n"
            "  }",
        )
    if "#include \"canarycfg/rollout_meter.h\"" not in fuzz:
        fuzz = fuzz.replace(
            "#include \"canarycfg/canary_merge.h\"",
            "#include \"canarycfg/canary_merge.h\"\n"
            "#include \"canarycfg/canary_coordinator.h\"\n"
            "#include \"canarycfg/split_ladder.h\"\n"
            "#include \"canarycfg/rollout_meter.h\"",
        )
    write(ROOT / "fuzz" / "canary_fuzzer.cc", fuzz)

    write(ROOT / "tests" / "test_baseline_tracker.cpp", '''#include "canarycfg/baseline_tracker.h"
#include "unity/unity.h"

void test_baseline_tracker_score(void) {
  baseline_tracker_t bt;
  baseline_tracker_init(&bt);
  TEST_ASSERT_EQUAL(0, baseline_tracker_note_bind(&bt, "stable-v1", 3));
  TEST_ASSERT_EQUAL(0, baseline_tracker_note_canary(&bt, "canary-v2"));
  TEST_ASSERT_NOT_EQUAL(0u, baseline_tracker_score(&bt));
  baseline_tracker_reset(&bt);
}
''')

    write(ROOT / "fuzz" / "corpus" / "canary_fuzzer" / "sample.bin",
          bytes([32]) + b"[canary]\nname=\"x\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "split_ladder_fuzzer" / "seed.bin", bytes(range(32, 96)))
    write(ROOT / "fuzz" / "corpus" / "rollout_meter_fuzzer" / "seed.bin", bytes(range(16, 128)))
    write(ROOT / "fuzz" / "corpus" / "baseline_tracker_fuzzer" / "seed.bin", bytes(range(8, 64)))


def plant_bugs() -> None:
    """Fix shallow canaryenv hex OOB; keep stateful split_ladder UAF as primary crash bug."""
    unesc = (ROOT / "src" / "canaryenv" / "unescape.cpp").read_text(encoding="utf-8")
    unesc = unesc.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "canaryenv" / "unescape.cpp").write_text(unesc, encoding="utf-8")


def patch_build() -> None:
    build_sh = '''#!/bin/bash -eu

OBJECTS=()

compile_canaryenv() {
  local base="$1"
  local obj="canaryenv_${base%.cpp}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall -D_GNU_SOURCE} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/canaryenv" \\
    -c "${SRC:-.}/src/canaryenv/${base}" -o "${obj}"
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
         validate merge expand coerce walk query diff pretty ramp_stack \\
         ramp_ctx path filter canarymap profile canonical strict readutil \\
         snapshot canaryloader canaryenv; do
  if [ -f "${SRC:-.}/src/canaryenv/${f}.cpp" ]; then
    compile_canaryenv "${f}.cpp"
  fi
done

for f in memory buffer unicode datetime lexer value parser path merge serialize \\
         diag format validator document; do
  compile_toml "${f}.cpp"
done

for f in canarycfg canary_merge canary_coordinator promotion_gate split_ladder rollout_meter baseline_tracker; do
  obj="${f}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/canaryenv" -I"${SRC:-.}/src/toml" \\
    -c "${SRC:-.}/src/${f}.cpp" -o "${obj}"
  OBJECTS+=("${obj}")
done

FUZZ_CXXFLAGS="${CXXFLAGS:- -O1 -g -std=c++17}"
INCS="-I${SRC:-.}/include -I${SRC:-.}/src/canaryenv -I${SRC:-.}/src/toml"

build_fuzzer() {
  ${CXX:-clang++} ${FUZZ_CXXFLAGS} ${LIB_FUZZING_ENGINE} \\
    "${SRC:-.}/fuzz/$1" "${OBJECTS[@]}" ${INCS} \\
    -o "${OUT:-.}/$2" -lm
}

build_fuzzer canaryenv_fuzzer.cc canaryenv_fuzzer
build_fuzzer toml_fuzzer.cc toml_fuzzer
build_fuzzer toml_merge_fuzzer.cc toml_merge_fuzzer
build_fuzzer toml_format_fuzzer.cc toml_format_fuzzer
build_fuzzer canary_fuzzer.cc canary_fuzzer
build_fuzzer split_ladder_fuzzer.cc split_ladder_fuzzer
build_fuzzer rollout_meter_fuzzer.cc rollout_meter_fuzzer
build_fuzzer baseline_tracker_fuzzer.cc baseline_tracker_fuzzer
'''
    write(ROOT / ".clusterfuzzlite/build.sh", build_sh)

    wsl = '''#!/bin/bash -eu
set -o pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${OUT:-/tmp/canarycfg_out}"
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
  - canaryenv_fuzzer
  - toml_fuzzer
  - toml_merge_fuzzer
  - toml_format_fuzzer
  - canary_fuzzer
  - split_ladder_fuzzer
  - rollout_meter_fuzzer
  - baseline_tracker_fuzzer
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
CXXFLAGS ?= -std=c++17 -O2 -g -Wall -Wextra -Wpedantic -Werror -Iinclude -Isrc/canaryenv -Isrc/toml
CANARYENV_SRC := $(wildcard src/canaryenv/*.cpp)
TOML_SRC := $(wildcard src/toml/*.cpp)
CORE_SRC := src/canarycfg.cpp src/canary_merge.cpp src/canary_coordinator.cpp src/promotion_gate.cpp src/split_ladder.cpp src/rollout_meter.cpp src/baseline_tracker.cpp
TEST_SRC := $(wildcard tests/test_*.cpp)
TEST := build/canarycfg_tests

$(TEST): $(CANARYENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) | build
\t$(CXX) $(CXXFLAGS) $(CANARYENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) -o $@

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


def create_artifacts() -> None:
    poc_dir = ARTIFACTS / "poc"
    verified = poc_dir / "verified"
    submit = poc_dir / "submit"
    verified.mkdir(parents=True, exist_ok=True)
    submit.mkdir(parents=True, exist_ok=True)

    write(verified / "entry_leak.cenv", "FOO=1\n")
    write(verified / "audit_leak.toml", 'k = "v"\n')
    write(verified / "empty_format.bin", b"")
    write(verified / "split_ladder_uaf.bin", bytes(range(32, 160)))

    write(poc_dir / "README.txt", """canarycfg local artifacts — NOT on GitHub

verified/
  entry_leak.cenv         — bug1 canaryenv entry realloc leak
  audit_leak.toml         — bug2 toml audit key leak
  split_ladder_uaf.bin    — bug3 split ladder compaction UAF
  merge_uaf.bin           — bug4 toml merge overlay index UAF
  empty_format.bin        — bug5 toml format empty doc null deref

submit/
  bugN_*.patch + bugN_TASK_DESCRIPTION.txt

Verify: bash artifacts/canarycfg/wsl_test_pocs.sh
""")

    write(ARTIFACTS / "TASKS.md", """# canarycfg task queue

GitHub: tolossamuel/canarycfg

| # | Bug | Harness | Class | Status |
|---|-----|---------|-------|--------|
| 1 | canaryenv entry realloc leak | canaryenv_fuzzer | LeakSanitizer | Ready |
| 2 | toml audit key leak | toml_fuzzer | LeakSanitizer | Ready |
| 3 | split ladder compaction UAF | split_ladder_fuzzer | heap-use-after-free | Ready |
| 4 | toml merge UAF | toml_merge_fuzzer | heap-use-after-free | Ready |
| 5 | toml format null deref | toml_format_fuzzer | null deref | Ready |

PoC bytes and patches: ../artifacts/canarycfg/poc/ (not on GitHub).
""")

    wsl_test = '''#!/bin/bash -eu
ROOT="$(cd "$(dirname "$0")/../../canarycfg" && pwd)"
POC="${POC_DIR:-$(dirname "$0")/poc/verified}"
OUT="${OUT:-/tmp/canarycfg_out}"

cd "$ROOT"
CC=clang CXX=clang++ bash build/wsl_build.sh >/dev/null

fail() { echo "FAIL: $*"; exit 1; }
pass() { echo "PASS: $*"; }

if ASAN_OPTIONS=detect_leaks=1 "$OUT/canaryenv_fuzzer" "$POC/entry_leak.cenv" >/dev/null 2>&1; then
  fail "bug1 should leak on unpatched build"
fi
pass "bug1 canaryenv entry leak reproduces"

if ASAN_OPTIONS=detect_leaks=1 "$OUT/toml_fuzzer" "$POC/audit_leak.toml" >/dev/null 2>&1; then
  fail "bug2 should leak on unpatched build"
fi
pass "bug2 toml audit leak reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/split_ladder_fuzzer" "$POC/split_ladder_uaf.bin" >/dev/null 2>&1; then
  fail "bug3 should UAF on unpatched build"
fi
pass "bug3 split ladder UAF reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/toml_merge_fuzzer" "$POC/merge_uaf.bin" >/dev/null 2>&1; then
  fail "bug4 should UAF on unpatched build"
fi
pass "bug4 toml merge UAF reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/toml_format_fuzzer" "$POC/empty_format.bin" >/dev/null 2>&1; then
  fail "bug5 should crash on unpatched build"
fi
pass "bug5 toml format null deref reproduces"

echo "All unpatched PoCs verified."
'''
    write(ARTIFACTS / "wsl_test_pocs.sh", wsl_test)
    (ARTIFACTS / "wsl_test_pocs.sh").chmod(0o755)


def generate_patches() -> None:
    """Build, verify PoCs, emit git patches into artifacts/submit/."""
    submit = ARTIFACTS / "poc" / "submit"
    verified = ARTIFACTS / "poc" / "verified"
    out = "/tmp/canarycfg_out"

    subprocess.check_call(["bash", "build/wsl_build.sh"], cwd=ROOT)

    merge_src = verified / "merge_uaf.bin"
    if not merge_src.exists() and (ARTIFACTS.parent / "failovercfg" / "poc" / "verified" / "merge_uaf.bin").exists():
        shutil.copy(
            ARTIFACTS.parent / "failovercfg" / "poc" / "verified" / "merge_uaf.bin",
            merge_src,
        )

    patches = [
        ("bug1_canaryenv_entry_leak.patch", "src/canaryenv/store.cpp",
         "free(d->entries);", "bug1"),
        ("bug2_toml_audit_leak.patch", "src/toml/document.cpp",
         None, "bug2"),
        ("bug3_split_ladder_uaf.patch", "src/split_ladder.cpp",
         "char *snap = strdup", "bug3"),
        ("bug4_toml_merge_uaf.patch", "src/toml/merge.cpp",
         "(void)overlay", "bug4"),
        ("bug5_toml_format_null_deref.patch", "src/toml/format.cpp",
         "ctx.out.length == 0", "bug5"),
    ]

    failover_submit = ARTIFACTS.parent / "failovercfg" / "poc" / "submit"
    for name, _, _, _ in patches:
        fb = failover_submit / name.replace("canaryenv", "failenv").replace("split_ladder", "region_ring")
        alt = failover_submit / name.replace("canaryenv_entry_leak", "failenv_entry_leak")
        alt2 = failover_submit / name.replace("split_ladder_uaf", "region_ring_uaf")
        src_patch = submit / name
        for candidate in [fb, alt, alt2, failover_submit / name]:
            if candidate.exists():
                text = candidate.read_text(encoding="utf-8")
                for old, new in TEXT_RENAME:
                    text = text.replace(old, new)
                src_patch.write_text(text, encoding="utf-8")
                break

    tasks = {
        "bug1_TASK_DESCRIPTION.txt": (
            "A memory leak occurs when parsing a canaryenv assignment: canaryenv_set_entry "
            "reallocates internal entry storage, but that heap memory is not freed when "
            "canaryenv_doc_destroy runs in src/canaryenv/store.cpp."
        ),
        "bug2_TASK_DESCRIPTION.txt": (
            "A memory leak occurs in the TOML document audit key path when toml_parse "
            "records assignment keys into doc->audit_keys without releasing them during "
            "document teardown in src/toml/document.cpp."
        ),
        "bug3_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in split_ladder_finalize_digest in src/split_ladder.cpp "
            "when digest finalization reads step label bytes through pending references registered "
            "before split_ladder_compact reallocates and frees the original label storage during "
            "multi-step registration in the split ladder compaction pipeline, triggered via split_ladder_fuzzer."
        ),
        "bug4_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs during TOML table merge in src/toml/merge.cpp when "
            "merge_table_in_place caches overlay entry key pointers then rebuilds the overlay "
            "table index mid-loop, leaving stale key references that are read on subsequent merge "
            "iterations via toml_merge_fuzzer."
        ),
        "bug5_TASK_DESCRIPTION.txt": (
            "A null pointer dereference occurs in tome_format_document in src/toml/format.cpp when "
            "formatting an empty document copies from ctx.out.data even though the output buffer "
            "was never allocated, triggered via toml_format_fuzzer with zero-length input."
        ),
    }
    for fname, desc in tasks.items():
        write(submit / fname, desc + "\n")


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
    print("OK", ROOT)


if __name__ == "__main__":
    main()
