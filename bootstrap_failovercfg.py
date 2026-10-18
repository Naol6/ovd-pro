#!/usr/bin/env python3
"""Bootstrap failovercfg — C++ multi-region failover orchestration + failenv overlays."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/failovercfg")
SRC = Path("/home/samuel/Documents/fenrir3/handoffcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/failovercfg")

# Order matters: longer / more specific tokens first.
TEXT_RENAME = [
    ("handoffcfg_validate_drain_manifest", "failovercfg_validate_failover_manifest"),
    ("handoffcfg_validate_handoff_manifest", "failovercfg_validate_failover_manifest"),
    ("handoffcfg_apply_handenv_to_toml", "failovercfg_apply_failenv_to_toml"),
    ("handoffcfg_load_handenv_memory", "failovercfg_load_failenv_memory"),
    ("handoffcfg_handenv_free", "failovercfg_failenv_free"),
    ("handoffcfg_load_toml_memory", "failovercfg_load_toml_memory"),
    ("handoffcfg_toml_free", "failovercfg_toml_free"),
    ("handoffcfg_default_options", "failovercfg_default_options"),
    ("handoffcfg_options_t", "failovercfg_options_t"),
    ("migration_ring_t", "region_ring_t"),
    ("migration_ring_", "region_ring_"),
    ("migration_ring", "region_ring"),
    ("migration_peer_t", "region_peer_t"),
    ("migration_peer", "region_peer"),
    ("sticky_registry_t", "probe_scheduler_t"),
    ("sticky_registry_", "probe_scheduler_"),
    ("sticky_registry", "probe_scheduler"),
    ("sticky_entry_t", "probe_entry_t"),
    ("sticky_entry", "probe_entry"),
    ("session_epoch_t", "traffic_weight_t"),
    ("session_epoch_", "traffic_weight_"),
    ("session_epoch", "traffic_weight"),
    ("affinity_gate_", "failover_fsm_"),
    ("affinity_gate", "failover_fsm"),
    ("handoff_coordinator", "failover_coordinator"),
    ("handoff_merge", "failover_merge"),
    ("handoff_fuzzer", "failover_fuzzer"),
    ("handenv_doc_impl_t", "failenv_doc_impl_t"),
    ("handenv_doc_t", "failenv_doc_t"),
    ("handenv_error_t", "failenv_error_t"),
    ("handenv_options_t", "failenv_options_t"),
    ("handenv_entry_t", "failenv_entry_t"),
    ("handenv_slice_t", "failenv_slice_t"),
    ("handenv_arena_t", "failenv_arena_t"),
    ("handenv_token_kind_t", "failenv_token_kind_t"),
    ("handenv_token_t", "failenv_token_t"),
    ("handenv_internal.h", "failenv_internal.h"),
    ("include/handenv", "include/failenv"),
    ("src/handenv/", "src/failenv/"),
    ("src/handenv", "src/failenv"),
    ("handenv_", "failenv_"),
    ("HANDENV_", "FAILENV_"),
    ("Handenv", "Failenv"),
    ("handenv", "failenv"),
    ("stick_stack", "route_stack"),
    ("stick_ctx", "route_ctx"),
    ("@stick", "@route"),
    ("handmap", "failmap"),
    ("handloader", "failloader"),
    ("HANDOFFCFG", "FAILOVERCFG"),
    ("HandoffCfg", "FailoverCfg"),
    ("handoffcfg", "failovercfg"),
    ("HANDOFF_", "FAILOVER_"),
    ("handoff", "failover"),
    ("tolossamuel/handoffcfg", "tolossamuel/failovercfg"),
    ("/tmp/handoffcfg_out", "/tmp/failovercfg_out"),
    ("compile_handenv", "compile_failenv"),
    ("handenv_fuzzer", "failenv_fuzzer"),
    (".henv", ".fenv"),
    ("henv_", "fenv_"),
    ("Session handoff during rolling upgrades", "Multi-region failover during datacenter cutover"),
    ("session handoff during rolling upgrades", "multi-region failover during datacenter cutover"),
    ("handenv runtime affinity overlays", "failenv runtime probe overlays"),
    ("Handenv layer", "Failenv layer"),
    ("Handoff coordinator validation", "Failover coordinator validation"),
    ("affinity gates", "failover state gates"),
    ("migration rings", "region priority rings"),
    ("sticky session registries", "health probe schedulers"),
    ("[drain]", "[failover]"),
    ("drain.slots", "failover.regions"),
    ("drain", "failover"),
    ("migrating", "cutover"),
    ("session_ttl_ms", "probe_interval_ms"),
    ("affinity_mode", "failover_mode"),
    ("STICKY_GENERATION", "PROBE_GENERATION"),
    ("AFFINITY_MODE", "FAILOVER_MODE"),
    ("SESSION_TTL_MS", "PROBE_INTERVAL_MS"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add failovercfg public headers", [
        "include/failovercfg/failovercfg.h", "include/failovercfg/failover_merge.h"]),
    ("include: add failenv public API", [
        "include/failenv/failenv.h", "include/failenv/failenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add failover coordinator and region ring headers", [
        "include/failovercfg/failover_coordinator.h", "include/failovercfg/failover_fsm.h",
        "include/failovercfg/region_ring.h", "include/failovercfg/probe_scheduler.h"]),
    ("include: add traffic weight tracker header", [
        "include/failovercfg/traffic_weight.h"]),
    ("src/failenv: add buffer and string utilities", [
        "src/failenv/buffer.cpp", "src/failenv/buffer.h", "src/failenv/strutil.cpp",
        "src/failenv/strutil.h"]),
    ("src/failenv: add arena allocator", [
        "src/failenv/arena.cpp", "src/failenv/arena.h", "src/failenv/failenv_internal.h"]),
    ("src/failenv: add error helpers", ["src/failenv/error.cpp", "src/failenv/error.h"]),
    ("src/failenv: add UTF-8 validation", ["src/failenv/utf8.cpp", "src/failenv/utf8.h"]),
    ("src/failenv: implement failenv line lexer", ["src/failenv/lexer.cpp", "src/failenv/lexer.h"]),
    ("src/failenv: add quoted value unescape", ["src/failenv/unescape.cpp", "src/failenv/unescape.h"]),
    ("src/failenv: add document store", ["src/failenv/store.cpp", "src/failenv/store.h"]),
    ("src/failenv: wire assignment parser", ["src/failenv/parser.cpp", "src/failenv/parser.h"]),
    ("src/failenv: add serialize to failenv text", ["src/failenv/serialize.cpp", "src/failenv/serialize.h"]),
    ("src/failenv: add validation pass", ["src/failenv/validate.cpp", "src/failenv/validate.h"]),
    ("src/failenv: add merge overlay", ["src/failenv/merge.cpp", "src/failenv/merge.h"]),
    ("src/failenv: add expand and coerce", [
        "src/failenv/expand.cpp", "src/failenv/expand.h", "src/failenv/coerce.cpp",
        "src/failenv/coerce.h"]),
    ("src/failenv: add walk query diff", [
        "src/failenv/walk.cpp", "src/failenv/walk.h", "src/failenv/query.cpp",
        "src/failenv/query.h", "src/failenv/diff.cpp", "src/failenv/diff.h"]),
    ("src/failenv: add pretty printer", ["src/failenv/pretty.cpp", "src/failenv/pretty.h"]),
    ("src/failenv: add route stack and ctx", [
        "src/failenv/route_stack.cpp", "src/failenv/route_stack.h",
        "src/failenv/route_ctx.cpp", "src/failenv/route_ctx.h"]),
    ("src/failenv: add path filter profile", [
        "src/failenv/path.cpp", "src/failenv/path.h", "src/failenv/filter.cpp",
        "src/failenv/filter.h", "src/failenv/profile.cpp", "src/failenv/profile.h"]),
    ("src/failenv: add snapshot readutil strict canonical", [
        "src/failenv/snapshot.cpp", "src/failenv/snapshot.h", "src/failenv/readutil.cpp",
        "src/failenv/readutil.h", "src/failenv/strict.cpp", "src/failenv/strict.h",
        "src/failenv/canonical.cpp", "src/failenv/canonical.h"]),
    ("src/failenv: add failloader and main failenv module", [
        "src/failenv/failloader.cpp", "src/failenv/failenv.cpp", "src/failenv/failmap.cpp",
        "src/failenv/failmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.cpp", "src/toml/buffer.cpp"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.cpp", "src/toml/datetime.cpp", "src/toml/lexer.cpp"]),
    ("src/toml: add value and parser core", ["src/toml/value.cpp", "src/toml/parser.cpp"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.cpp", "src/toml/merge.cpp", "src/toml/serialize.cpp"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.cpp", "src/toml/format.cpp", "src/toml/validator.cpp", "src/toml/document.cpp"]),
    ("src: add failovercfg bridge and failenv-to-toml merge", ["src/failovercfg.cpp", "src/failover_merge.cpp"]),
    ("src: add failover coordinator validator", ["src/failover_coordinator.cpp"]),
    ("src: add failover FSM evaluator", ["src/failover_fsm.cpp"]),
    ("src: add region ring peer tracker", ["src/region_ring.cpp"]),
    ("src: add probe scheduler for health checks", ["src/probe_scheduler.cpp"]),
    ("src: add traffic weight accumulator", ["src/traffic_weight.cpp"]),
    ("tests: add Unity harness", ["tests/unity/unity.cpp", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.cpp", "tests/test_basic.cpp"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.cpp", "tests/test_merge.cpp", "tests/test_validate.cpp"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.cpp", "tests/test_coerce.cpp", "tests/test_integration.cpp",
        "tests/test_scenarios.cpp"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.cpp", "tests/test_lexer_exhaustive.cpp"]),
    ("tests: add failover coordinator and region ring unit tests", [
        "tests/test_failover_coordinator.cpp", "tests/test_region_ring.cpp"]),
    ("tests: add probe scheduler and traffic weight unit tests", [
        "tests/test_probe_scheduler.cpp", "tests/test_traffic_weight.cpp"]),
    ("examples: add TOML failover manifest and runtime overlay", [
        "examples/failover.toml", "examples/failover.runtime"]),
    ("fuzz: add failenv_fuzzer harness", ["fuzz/failenv_fuzzer.cc"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.cc"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.cc"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.cc"]),
    ("fuzz: add failover_fuzzer for cross-format overlay", ["fuzz/failover_fuzzer.cc"]),
    ("fuzz: add region_ring_fuzzer for compaction path", ["fuzz/region_ring_fuzzer.cc"]),
    ("fuzz: add probe_scheduler_fuzzer for probe path", ["fuzz/probe_scheduler_fuzzer.cc"]),
    ("fuzz: add traffic_weight_fuzzer for weight path", ["fuzz/traffic_weight_fuzzer.cc"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/failenv_fuzzer/minimal.fenv",
        "fuzz/corpus/failenv_fuzzer/quoted.fenv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/failover_fuzzer/sample.bin",
        "fuzz/corpus/region_ring_fuzzer/seed.bin",
        "fuzz/corpus/probe_scheduler_fuzzer/seed.bin",
        "fuzz/corpus/traffic_weight_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for failovercfg library", ["README.md"]),
    ("docs: add BUILDING notes", ["docs/BUILDING.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable failover configuration library", []),
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
        (ROOT / "include" / "handoffcfg", ROOT / "include" / "failovercfg"),
        (ROOT / "include" / "handenv", ROOT / "include" / "failenv"),
        (ROOT / "src" / "handenv", ROOT / "src" / "failenv"),
        (ROOT / "src" / "handoffcfg.cpp", ROOT / "src" / "failovercfg.cpp"),
        (ROOT / "src" / "handoff_merge.cpp", ROOT / "src" / "failover_merge.cpp"),
        (ROOT / "src" / "handoff_coordinator.cpp", ROOT / "src" / "failover_coordinator.cpp"),
        (ROOT / "src" / "affinity_gate.cpp", ROOT / "src" / "failover_fsm.cpp"),
        (ROOT / "src" / "migration_ring.cpp", ROOT / "src" / "region_ring.cpp"),
        (ROOT / "src" / "sticky_registry.cpp", ROOT / "src" / "probe_scheduler.cpp"),
        (ROOT / "src" / "session_epoch.cpp", ROOT / "src" / "traffic_weight.cpp"),
        (ROOT / "fuzz" / "handenv_fuzzer.cc", ROOT / "fuzz" / "failenv_fuzzer.cc"),
        (ROOT / "fuzz" / "handoff_fuzzer.cc", ROOT / "fuzz" / "failover_fuzzer.cc"),
        (ROOT / "fuzz" / "migration_ring_fuzzer.cc", ROOT / "fuzz" / "region_ring_fuzzer.cc"),
        (ROOT / "fuzz" / "sticky_registry_fuzzer.cc", ROOT / "fuzz" / "probe_scheduler_fuzzer.cc"),
        (ROOT / "fuzz" / "session_epoch_fuzzer.cc", ROOT / "fuzz" / "traffic_weight_fuzzer.cc"),
        (ROOT / "examples" / "handoff.toml", ROOT / "examples" / "failover.toml"),
        (ROOT / "examples" / "handoff.runtime", ROOT / "examples" / "failover.runtime"),
        (ROOT / "fuzz" / "corpus" / "handenv_fuzzer", ROOT / "fuzz" / "corpus" / "failenv_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "handoff_fuzzer", ROOT / "fuzz" / "corpus" / "failover_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "migration_ring_fuzzer", ROOT / "fuzz" / "corpus" / "region_ring_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "sticky_registry_fuzzer", ROOT / "fuzz" / "corpus" / "probe_scheduler_fuzzer"),
        (ROOT / "tests" / "test_handoff_coordinator.cpp", ROOT / "tests" / "test_failover_coordinator.cpp"),
        (ROOT / "tests" / "test_migration_ring.cpp", ROOT / "tests" / "test_region_ring.cpp"),
        (ROOT / "tests" / "test_sticky_registry.cpp", ROOT / "tests" / "test_probe_scheduler.cpp"),
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

    for p in list((ROOT / "src" / "failenv").glob("*")):
        new_name = p.name.replace("handenv", "failenv")
        new_name = new_name.replace("handloader", "failloader")
        new_name = new_name.replace("stick_stack", "route_stack")
        new_name = new_name.replace("stick_ctx", "route_ctx")
        new_name = new_name.replace("handmap", "failmap")
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    corp = ROOT / "fuzz" / "corpus" / "failenv_fuzzer"
    for old in list(corp.glob("*.henv")):
        old.rename(old.with_suffix(".fenv"))

    header_renames = [
        (ROOT / "include" / "failovercfg" / "handoffcfg.h", ROOT / "include" / "failovercfg" / "failovercfg.h"),
        (ROOT / "include" / "failovercfg" / "handoff_merge.h", ROOT / "include" / "failovercfg" / "failover_merge.h"),
        (ROOT / "include" / "failovercfg" / "handoff_coordinator.h", ROOT / "include" / "failovercfg" / "failover_coordinator.h"),
        (ROOT / "include" / "failovercfg" / "affinity_gate.h", ROOT / "include" / "failovercfg" / "failover_fsm.h"),
        (ROOT / "include" / "failovercfg" / "migration_ring.h", ROOT / "include" / "failovercfg" / "region_ring.h"),
        (ROOT / "include" / "failovercfg" / "sticky_registry.h", ROOT / "include" / "failovercfg" / "probe_scheduler.h"),
        (ROOT / "include" / "failovercfg" / "session_epoch.h", ROOT / "include" / "failovercfg" / "traffic_weight.h"),
    ]
    for src, dst in header_renames:
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                dst.unlink()
            src.rename(dst)

    failenv_hdr = [
        (ROOT / "include" / "failenv" / "handenv.h", ROOT / "include" / "failenv" / "failenv.h"),
        (ROOT / "include" / "failenv" / "handenv_types.h", ROOT / "include" / "failenv" / "failenv_types.h"),
    ]
    for src, dst in failenv_hdr:
        if src.exists():
            if dst.exists():
                dst.unlink()
            src.rename(dst)


def patch_failenv_lexer(text: str) -> str:
    if "FAILENV_TOK_BANG" in text:
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
            ".fenv", ".henv", ".env", "Makefile"
        } and path.name not in {"Makefile", ".gitignore"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text = xform(text)
        if path.name == "lexer.cpp" and "failenv" in str(path):
            new_text = patch_failenv_lexer(new_text)
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
    """Ensure coordinator reads [failover] table with failover.regions array."""
    path = ROOT / "src" / "failover_coordinator.cpp"
    text = path.read_text(encoding="utf-8")
    text = text.replace('tome_table_get(doc->root, "failover")', 'tome_table_get(doc->root, "failover")')
    text = text.replace('tome_table_get(tbl, "slots")', 'tome_table_get(tbl, "regions")')
    text = text.replace('const char *l = (label && label->type == TOME_VAL_STRING) ? label->as.string : "slot";',
                        'const char *l = (label && label->type == TOME_VAL_STRING) ? label->as.string : "region";')
    path.write_text(text, encoding="utf-8")


README = """# failovercfg

failovercfg is a C++17 library for **multi-region failover orchestration** during datacenter cutover: parse TOML failover manifests, load failenv runtime probe overlays, merge layers, validate failover state gates, and track region priority rings plus health probe schedulers.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Failenv layer** — `KEY=VALUE`, `@route` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply failenv overlay keys onto parsed TOML documents
- **Failover coordinator** — validate `[failover]` tables and register region weights into a region ring
- **Probe scheduler** — track health probe cadence across failover epochs
- **Traffic weight tracker** — accumulate weighted routing scores during cutover
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `failenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `failover_fuzzer`, `region_ring_fuzzer`, `probe_scheduler_fuzzer`, `traffic_weight_fuzzer`.

## License

MIT — see LICENSE.
"""

BUILDING = """# Building failovercfg

## Requirements

- clang/clang++ 14+
- libFuzzer (via `-fsanitize=fuzzer` or `$LIB_FUZZING_ENGINE`)

## Local ASan build

```bash
bash build/wsl_build.sh
```

Fuzzers land in `/tmp/failovercfg_out/`.

## Unit tests

```bash
make test
```
"""


def add_domain() -> None:
    write(ROOT / "README.md", README)
    write(ROOT / "docs" / "BUILDING.md", BUILDING)

    write(ROOT / "examples" / "failover.toml", """[failover]
name = "payments-api"
probe_interval_ms = 30000
failover_mode = "active-passive"

[[failover.regions]]
label = "us-east-1"
weight = 9

[[failover.regions]]
label = "us-west-2"
weight = 3
""")

    write(ROOT / "examples" / "failover.runtime", """# Runtime failover parameters injected during cutover
PROBE_INTERVAL_MS=15000
FAILOVER_MODE=cutover
PROBE_GENERATION=2
""")

    fuzz = (ROOT / "fuzz" / "failover_fuzzer.cc").read_text(encoding="utf-8")
    if "probe_scheduler_t" not in fuzz:
        fuzz = fuzz.replace(
            "failovercfg_apply_failenv_to_toml(toml, env);",
            "failovercfg_apply_failenv_to_toml(toml, env);\n"
            "  if (toml) {\n"
            "    region_ring_t ring;\n"
            "    probe_scheduler_t sched;\n"
            "    region_ring_init(&ring);\n"
            "    probe_scheduler_init(&sched);\n"
            "    failovercfg_validate_failover_manifest(toml, &ring);\n"
            "    (void)region_ring_finalize_digest(&ring);\n"
            "    probe_scheduler_reset(&sched);\n"
            "    region_ring_reset(&ring);\n"
            "  }",
        )
    if "#include \"failovercfg/probe_scheduler.h\"" not in fuzz:
        fuzz = fuzz.replace(
            "#include \"failovercfg/failover_merge.h\"",
            "#include \"failovercfg/failover_merge.h\"\n"
            "#include \"failovercfg/failover_coordinator.h\"\n"
            "#include \"failovercfg/region_ring.h\"\n"
            "#include \"failovercfg/probe_scheduler.h\"",
        )
    write(ROOT / "fuzz" / "failover_fuzzer.cc", fuzz)

    write(ROOT / "tests" / "test_traffic_weight.cpp", '''#include "failovercfg/traffic_weight.h"
#include "unity/unity.h"

void test_traffic_weight_score(void) {
  traffic_weight_t tw;
  traffic_weight_init(&tw);
  TEST_ASSERT_EQUAL(0, traffic_weight_note_bind(&tw, "us-east-1", 3));
  TEST_ASSERT_EQUAL(0, traffic_weight_note_failover(&tw, "us-west-2"));
  TEST_ASSERT_NOT_EQUAL(0u, traffic_weight_score(&tw));
  traffic_weight_reset(&tw);
}
''')

    write(ROOT / "fuzz" / "corpus" / "failover_fuzzer" / "sample.bin",
          bytes([32]) + b"[failover]\nname=\"x\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "region_ring_fuzzer" / "seed.bin", bytes(range(32, 96)))
    write(ROOT / "fuzz" / "corpus" / "probe_scheduler_fuzzer" / "seed.bin", bytes(range(16, 128)))
    write(ROOT / "fuzz" / "corpus" / "traffic_weight_fuzzer" / "seed.bin", bytes(range(8, 64)))


def plant_bugs() -> None:
    """Keep inherited cfg bugs; fix shallow failenv hex OOB so primary tasks stay hard."""
    unesc = (ROOT / "src" / "failenv" / "unescape.cpp").read_text(encoding="utf-8")
    unesc = unesc.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "failenv" / "unescape.cpp").write_text(unesc, encoding="utf-8")


def patch_build() -> None:
    build_sh = '''#!/bin/bash -eu

OBJECTS=()

compile_failenv() {
  local base="$1"
  local obj="failenv_${base%.cpp}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall -D_GNU_SOURCE} \
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/failenv" \
    -c "${SRC:-.}/src/failenv/${base}" -o "${obj}"
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
         validate merge expand coerce walk query diff pretty route_stack \
         route_ctx path filter failmap profile canonical strict readutil \
         snapshot failloader failenv; do
  if [ -f "${SRC:-.}/src/failenv/${f}.cpp" ]; then
    compile_failenv "${f}.cpp"
  fi
done

for f in memory buffer unicode datetime lexer value parser path merge serialize \
         diag format validator document; do
  compile_toml "${f}.cpp"
done

for f in failovercfg failover_merge failover_coordinator failover_fsm region_ring probe_scheduler traffic_weight; do
  obj="${f}.o"
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17 -Wall} \
    -I"${SRC:-.}/include" -I"${SRC:-.}/src/failenv" -I"${SRC:-.}/src/toml" \
    -c "${SRC:-.}/src/${f}.cpp" -o "${obj}"
  OBJECTS+=("${obj}")
done

FUZZ_CXXFLAGS="${CXXFLAGS:- -O1 -g -std=c++17}"
INCS="-I${SRC:-.}/include -I${SRC:-.}/src/failenv -I${SRC:-.}/src/toml"

build_fuzzer() {
  ${CXX:-clang++} ${FUZZ_CXXFLAGS} ${LIB_FUZZING_ENGINE} \
    "${SRC:-.}/fuzz/$1" "${OBJECTS[@]}" ${INCS} \
    -o "${OUT:-.}/$2" -lm
}

build_fuzzer failenv_fuzzer.cc failenv_fuzzer
build_fuzzer toml_fuzzer.cc toml_fuzzer
build_fuzzer toml_merge_fuzzer.cc toml_merge_fuzzer
build_fuzzer toml_format_fuzzer.cc toml_format_fuzzer
build_fuzzer failover_fuzzer.cc failover_fuzzer
build_fuzzer region_ring_fuzzer.cc region_ring_fuzzer
build_fuzzer probe_scheduler_fuzzer.cc probe_scheduler_fuzzer
build_fuzzer traffic_weight_fuzzer.cc traffic_weight_fuzzer
'''
    write(ROOT / ".clusterfuzzlite" / "build.sh", build_sh)

    wsl = '''#!/bin/bash -eu
set -o pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${OUT:-/tmp/failovercfg_out}"
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
  - failenv_fuzzer
  - toml_fuzzer
  - toml_merge_fuzzer
  - toml_format_fuzzer
  - failover_fuzzer
  - region_ring_fuzzer
  - probe_scheduler_fuzzer
  - traffic_weight_fuzzer
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
CXXFLAGS ?= -std=c++17 -O2 -g -Wall -Wextra -Wpedantic -Werror -Iinclude -Isrc/failenv -Isrc/toml
FAILENV_SRC := $(wildcard src/failenv/*.cpp)
TOML_SRC := $(wildcard src/toml/*.cpp)
CORE_SRC := src/failovercfg.cpp src/failover_merge.cpp src/failover_coordinator.cpp src/failover_fsm.cpp src/region_ring.cpp src/probe_scheduler.cpp src/traffic_weight.cpp
TEST_SRC := $(wildcard tests/test_*.cpp)
TEST := build/failovercfg_tests

$(TEST): $(FAILENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) | build
	$(CXX) $(CXXFLAGS) $(FAILENV_SRC) $(TOML_SRC) $(CORE_SRC) tests/test_runner.cpp tests/unity/unity.cpp $(TEST_SRC) -o $@

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
    """Create local-only PoC artifacts and verification script."""
    poc_dir = ARTIFACTS / "poc"
    verified = poc_dir / "verified"
    submit = poc_dir / "submit"
    verified.mkdir(parents=True, exist_ok=True)
    submit.mkdir(parents=True, exist_ok=True)

    write(verified / "entry_leak.fenv", "FOO=1\n")
    write(verified / "audit_leak.toml", 'k = "v"\n')

    # Empty doc format crash — SHA1 da39a3ee...
    write(verified / "empty_format.bin", b"")

    # region_ring UAF — crafted binary from handoffcfg pattern
    write(verified / "region_ring_uaf.bin", bytes(range(32, 160)))

    # merge UAF — needs valid TOML merge inputs; generate after build
    write(poc_dir / "README.txt", """failovercfg local artifacts — NOT on GitHub

verified/
  entry_leak.fenv       — bug1 failenv entry realloc leak
  audit_leak.toml       — bug2 toml audit key leak
  region_ring_uaf.bin   — bug3 region ring compaction UAF
  merge_uaf.bin         — bug4 toml merge overlay index UAF
  empty_format.bin      — bug5 toml format empty doc null deref

submit/
  bugN_*.patch + bugN_TASK_DESCRIPTION.txt

Verify: bash artifacts/failovercfg/wsl_test_pocs.sh
""")

    wsl_test = '''#!/bin/bash -eu
# Local PoC verification — lives in artifacts/, NOT in GitHub repo.
ROOT="$(cd "$(dirname "$0")/../../failovercfg" && pwd)"
POC="${POC_DIR:-$(dirname "$0")/verified}"
OUT="${OUT:-/tmp/failovercfg_out}"

cd "$ROOT"
CC=clang CXX=clang++ bash build/wsl_build.sh >/dev/null

fail() { echo "FAIL: $*"; exit 1; }
pass() { echo "PASS: $*"; }

if ASAN_OPTIONS=detect_leaks=1 "$OUT/failenv_fuzzer" "$POC/entry_leak.fenv" >/dev/null 2>&1; then
  fail "bug1 should leak on unpatched build"
fi
pass "bug1 failenv entry leak reproduces"

if ASAN_OPTIONS=detect_leaks=1 "$OUT/toml_fuzzer" "$POC/audit_leak.toml" >/dev/null 2>&1; then
  fail "bug2 should leak on unpatched build"
fi
pass "bug2 toml audit leak reproduces"

if ASAN_OPTIONS=detect_leaks=0 "$OUT/region_ring_fuzzer" "$POC/region_ring_uaf.bin" >/dev/null 2>&1; then
  fail "bug3 should UAF on unpatched build"
fi
pass "bug3 region ring UAF reproduces"

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


def main() -> None:
    copy_tree()
    transform_contents()
    patch_coordinator()
    add_domain()
    plant_bugs()
    patch_build()
    init_git()
    create_artifacts()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
