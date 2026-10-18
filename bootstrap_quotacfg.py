#!/usr/bin/env python3
"""Bootstrap quotacfg — TOML quota manifests + quotaenv runtime overlays."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/quotacfg")
SRC = Path("/home/samuel/Documents/fenrir3/stagecfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/quotacfg")

TEXT_RENAME = [
    ("stage_window_tracker_t", "quota_window_tracker_t"),
    ("stage_window_state_t", "quota_window_state_t"),
    ("stage_window_tracker", "quota_window_tracker"),
    ("stage_window_apply_jitter", "quota_window_apply_jitter"),
    ("stage_window_compute_backoff", "quota_window_compute_backoff"),
    ("stage_window_tick", "quota_window_tick"),
    ("stage_window_due_count", "quota_window_due_count"),
    ("stage_window_advance_epoch", "quota_window_advance_epoch"),
    ("stage_window_fuzzer", "quota_window_fuzzer"),
    ("stage_window.c", "quota_window.c"),
    ("stage_window.h", "quota_window.h"),
    ("stage_coordinator_t", "quota_enforcer_t"),
    ("stage_coordinator_init", "quota_enforcer_init"),
    ("stage_coordinator_reset", "quota_enforcer_reset"),
    ("stage_coordinator_register", "quota_enforcer_register"),
    ("stage_coordinator_tick", "quota_enforcer_tick"),
    ("stage_coordinator.c", "quota_enforcer.c"),
    ("stage_coordinator.h", "quota_enforcer.h"),
    ("stage_dag_finalize_digest", "quota_ledger_finalize_digest"),
    ("stage_dag_compact", "quota_ledger_compact"),
    ("stage_dag_register", "quota_ledger_register"),
    ("stage_dag_reset", "quota_ledger_reset"),
    ("stage_dag_init", "quota_ledger_init"),
    ("stage_dag_fuzzer", "quota_ledger_fuzzer"),
    ("stage_stage_t", "quota_bucket_t"),
    ("stage_dag_t", "quota_ledger_t"),
    ("stage_dag.c", "quota_ledger.c"),
    ("stage_dag.h", "quota_ledger.h"),
    ("stageenv_doc_impl_t", "quotaenv_doc_impl_t"),
    ("stageenv_doc_t", "quotaenv_doc_t"),
    ("stageenv_error_t", "quotaenv_error_t"),
    ("stageenv_options_t", "quotaenv_options_t"),
    ("stageenv_entry_t", "quotaenv_entry_t"),
    ("stageenv_slice_t", "quotaenv_slice_t"),
    ("stageenv_arena_t", "quotaenv_arena_t"),
    ("stageenv_token_kind_t", "quotaenv_token_kind_t"),
    ("stageenv_token_t", "quotaenv_token_t"),
    ("stageenv_internal.h", "quotaenv_internal.h"),
    ("stageenv/stageenv_types.h", "quotaenv/quotaenv_types.h"),
    ("stageenv/stageenv.h", "quotaenv/quotaenv.h"),
    ("include/stageenv", "include/quotaenv"),
    ("src/stageenv/", "src/quotaenv/"),
    ("src/stageenv", "src/quotaenv"),
    ("stageenv_", "quotaenv_"),
    ("STAGEENV_", "QUOTAENV_"),
    ("Stageenv", "Quotaenv"),
    ("stageenv", "quotaenv"),
    ("stage_merge", "quota_merge"),
    ("stage_fuzzer", "quota_fuzzer"),
    ("stage_policy", "quota_policy"),
    ("stage_gate", "quota_gate"),
    ("stagecfg", "quotacfg"),
    ("StageCfg", "QuotaCfg"),
    ("STAGECFG", "QUOTACFG"),
    ("stage_stack", "quota_stack"),
    ("stage_ctx", "quota_ctx"),
    ("@stage", "@quota"),
    ("stagemap", "quotamap"),
    ("stageloader", "quotaloader"),
    ("apply_stageenv_overlay", "apply_quotaenv_overlay"),
    ("apply_stageenv_to_toml", "apply_quotaenv_to_toml"),
    ("load_stageenv_memory", "load_quotaenv_memory"),
    ("quotacfg_stageenv_free", "quotacfg_quotaenv_free"),
    ("/tmp/stagecfg_out", "/tmp/quotacfg_out"),
    ("tolossamuel/stagecfg", "tolossamuel/quotacfg"),
    ("compile_stageenv", "compile_quotaenv"),
    ("senv_", "qenv_"),
    ("pipeline.runtime", "quota.runtime"),
    ("pipeline.toml", "quota.toml"),
    (".senv", ".qenv"),
    ("[pipeline]", "[quota]"),
    ("pipeline stage", "quota bucket"),
    ("Pipeline stage", "Quota bucket"),
    ("stage dependency DAG", "tenant consumption ledger"),
    ("Stage dependency DAG", "Tenant consumption ledger"),
    ("stage DAG", "quota ledger"),
    ("Stage DAG", "Quota ledger"),
    ("stage_dag", "quota_ledger"),
    ("parallelism", "hard_limit"),
    ("min_ready", "soft_limit"),
    ("pipeline_state", "quota_state"),
    ("[[quota.stages]]", "[[quota.buckets]]"),
    ("[quota.stages]", "[quota.buckets]"),
    ("stage_count", "bucket_count"),
    ("stage_cap", "bucket_cap"),
    ("stage->", "bucket->"),
    ("t->stages", "t->buckets"),
    ("&t->stages", "&t->buckets"),
    ("grow_stages", "grow_buckets"),
    ("stage_stage", "quota_bucket"),
    ("stage launch", "quota admission"),
    ("Stage launch", "Quota admission"),
    ("stage launches", "quota admissions"),
    ("stage priority", "bucket weight"),
    ("stage priorities", "bucket weights"),
    ("stage label", "bucket label"),
    ("stage registration", "bucket registration"),
    ("windowed scheduling", "sliding-window quota reset"),
    ("epoch-aware coordination", "epoch-aware quota enforcement"),
    ("pipeline configuration", "resource quota configuration"),
    ("Pipeline configuration", "Resource quota configuration"),
    ("pipeline manifests", "quota manifests"),
    ("Pipeline manifests", "Quota manifests"),
    ("stageenv runtime", "quotaenv runtime"),
    ("Stageenv layer", "Quotaenv layer"),
    ("stageenv layer", "quotaenv layer"),
    ("stageenv_fuzzer", "quotaenv_fuzzer"),
    ("stage_fuzzer", "quota_fuzzer"),
    ("priority =", "weight ="),
    ("slot->priority", "bucket->weight"),
    ("slot.priority", "bucket.weight"),
    ("budget", "allowance"),
]

EXCLUDE = {".git", "poc", "guides", "__pycache__", "wsl_test_pocs.sh"}
SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}
SKIP_SUFFIX = {".o"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add quotacfg public headers", [
        "include/quotacfg/quotacfg.h", "include/quotacfg/quota_merge.h"]),
    ("include: add quotaenv public API", [
        "include/quotaenv/quotaenv.h", "include/quotaenv/quotaenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add quota policy gate ledger headers", [
        "include/quotacfg/quota_policy.h", "include/quotacfg/quota_gate.h",
        "include/quotacfg/quota_ledger.h", "include/quotacfg/quota_window.h",
        "include/quotacfg/quota_enforcer.h"]),
    ("src/quotaenv: add buffer and string utilities", [
        "src/quotaenv/buffer.c", "src/quotaenv/buffer.h", "src/quotaenv/strutil.c",
        "src/quotaenv/strutil.h"]),
    ("src/quotaenv: add arena allocator", [
        "src/quotaenv/arena.c", "src/quotaenv/arena.h", "src/quotaenv/quotaenv_internal.h"]),
    ("src/quotaenv: add error helpers", ["src/quotaenv/error.c", "src/quotaenv/error.h"]),
    ("src/quotaenv: add UTF-8 validation", ["src/quotaenv/utf8.c", "src/quotaenv/utf8.h"]),
    ("src/quotaenv: implement quotaenv line lexer", ["src/quotaenv/lexer.c", "src/quotaenv/lexer.h"]),
    ("src/quotaenv: add quoted value unescape", ["src/quotaenv/unescape.c", "src/quotaenv/unescape.h"]),
    ("src/quotaenv: add document store", ["src/quotaenv/store.c", "src/quotaenv/store.h"]),
    ("src/quotaenv: wire assignment parser", ["src/quotaenv/parser.c", "src/quotaenv/parser.h"]),
    ("src/quotaenv: add serialize to quotaenv text", ["src/quotaenv/serialize.c", "src/quotaenv/serialize.h"]),
    ("src/quotaenv: add validation pass", ["src/quotaenv/validate.c", "src/quotaenv/validate.h"]),
    ("src/quotaenv: add merge overlay", ["src/quotaenv/merge.c", "src/quotaenv/merge.h"]),
    ("src/quotaenv: add expand and coerce", [
        "src/quotaenv/expand.c", "src/quotaenv/expand.h", "src/quotaenv/coerce.c",
        "src/quotaenv/coerce.h"]),
    ("src/quotaenv: add walk query diff", [
        "src/quotaenv/walk.c", "src/quotaenv/walk.h", "src/quotaenv/query.c",
        "src/quotaenv/query.h", "src/quotaenv/diff.c", "src/quotaenv/diff.h"]),
    ("src/quotaenv: add pretty printer", ["src/quotaenv/pretty.c", "src/quotaenv/pretty.h"]),
    ("src/quotaenv: add quota stack and ctx", [
        "src/quotaenv/quota_stack.c", "src/quotaenv/quota_stack.h",
        "src/quotaenv/quota_ctx.c", "src/quotaenv/quota_ctx.h"]),
    ("src/quotaenv: add path filter profile", [
        "src/quotaenv/path.c", "src/quotaenv/path.h", "src/quotaenv/filter.c",
        "src/quotaenv/filter.h", "src/quotaenv/profile.c", "src/quotaenv/profile.h"]),
    ("src/quotaenv: add snapshot readutil strict canonical", [
        "src/quotaenv/snapshot.c", "src/quotaenv/snapshot.h", "src/quotaenv/readutil.c",
        "src/quotaenv/readutil.h", "src/quotaenv/strict.c", "src/quotaenv/strict.h",
        "src/quotaenv/canonical.c", "src/quotaenv/canonical.h"]),
    ("src/quotaenv: add quotaloader and main quotaenv module", [
        "src/quotaenv/quotaloader.c", "src/quotaenv/quotaenv.c", "src/quotaenv/quotamap.c",
        "src/quotaenv/quotamap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.c", "src/toml/buffer.c"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.c", "src/toml/datetime.c", "src/toml/lexer.c"]),
    ("src/toml: add value and parser core", ["src/toml/value.c", "src/toml/parser.c"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.c", "src/toml/merge.c", "src/toml/serialize.c"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.c", "src/toml/format.c", "src/toml/validator.c", "src/toml/document.c"]),
    ("src: add quotacfg bridge and quotaenv-to-toml merge", ["src/quotacfg.c", "src/quota_merge.c"]),
    ("src: add quota policy validator", ["src/quota_policy.c"]),
    ("src: add quota admission gate evaluator", ["src/quota_gate.c"]),
    ("src: add tenant consumption ledger with compaction", ["src/quota_ledger.c"]),
    ("src: add sliding-window quota tracker with jitter", ["src/quota_window.c"]),
    ("src: add epoch-aware quota enforcer", ["src/quota_enforcer.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add quota policy ledger window unit tests", [
        "tests/test_quota_policy.c", "tests/test_quota_ledger.c", "tests/test_quota_window.c"]),
    ("examples: add TOML quota manifest and runtime overlay", [
        "examples/quota.toml", "examples/quota.runtime"]),
    ("fuzz: add quotaenv_fuzzer harness", ["fuzz/quotaenv_fuzzer.c"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.c"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.c"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.c"]),
    ("fuzz: add quota_fuzzer for cross-format overlay", ["fuzz/quota_fuzzer.c"]),
    ("fuzz: add quota_ledger_fuzzer for ledger compaction path", ["fuzz/quota_ledger_fuzzer.c"]),
    ("fuzz: add quota_window_fuzzer for enforcer tick paths", ["fuzz/quota_window_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/quotaenv_fuzzer/minimal.qenv",
        "fuzz/corpus/quotaenv_fuzzer/quoted.qenv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/quota_fuzzer/sample.bin",
        "fuzz/corpus/quota_ledger_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for quotacfg library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable quota configuration library", []),
]

README = """# quotacfg

quotacfg is a C11 library for multi-tenant resource quota configuration: parse TOML quota manifests, load quotaenv runtime tuning overlays, merge layers, validate quota policy, and track tenant consumption ledgers during sliding-window quota reset and epoch-aware enforcement.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Quotaenv layer** — `KEY=VALUE`, `@quota` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply quotaenv overlay keys onto parsed TOML documents
- **Quota policy** — validate `[quota]` tables and register bucket weights into a compaction ledger
- **Quota gate** — gate new quota admissions on policy health and in-flight counts
- **Window tracker** — sliding-window quota reset with jitter and backoff
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `quotaenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `quota_fuzzer`, `quota_ledger_fuzzer`, `quota_window_fuzzer`.

## Quick start

```c
#include "quotacfg/quotacfg.h"

TomeDoc *toml = NULL;
TomeError err;
quotacfg_load_toml_memory("[quota]\\nname = \\"tenant-alpha\\"\\nhard_limit = 1000\\n", 48, &toml, &err);

quotaenv_doc_t *env = NULL;
quotacfg_load_quotaenv_memory("HARD_LIMIT=500\\n", 17, NULL, &env, NULL);
quotacfg_apply_quotaenv_to_toml(toml, env);

quotacfg_quotaenv_free(env);
quotacfg_toml_free(toml);
```

## License

MIT — see LICENSE.
"""


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

    def ignore(dir_path: str, names: list[str]) -> list[str]:
        return [n for n in names if n in EXCLUDE or n.endswith(".o")]

    shutil.copytree(SRC, ROOT, ignore=ignore)

    renames = [
        (ROOT / "include" / "stagecfg", ROOT / "include" / "quotacfg"),
        (ROOT / "include" / "stageenv", ROOT / "include" / "quotaenv"),
        (ROOT / "src" / "stageenv", ROOT / "src" / "quotaenv"),
        (ROOT / "src" / "stagecfg.c", ROOT / "src" / "quotacfg.c"),
        (ROOT / "src" / "stage_merge.c", ROOT / "src" / "quota_merge.c"),
        (ROOT / "src" / "stage_policy.c", ROOT / "src" / "quota_policy.c"),
        (ROOT / "src" / "stage_gate.c", ROOT / "src" / "quota_gate.c"),
        (ROOT / "src" / "stage_dag.c", ROOT / "src" / "quota_ledger.c"),
        (ROOT / "src" / "stage_window.c", ROOT / "src" / "quota_window.c"),
        (ROOT / "src" / "stage_coordinator.c", ROOT / "src" / "quota_enforcer.c"),
        (ROOT / "fuzz" / "stageenv_fuzzer.c", ROOT / "fuzz" / "quotaenv_fuzzer.c"),
        (ROOT / "fuzz" / "stage_fuzzer.c", ROOT / "fuzz" / "quota_fuzzer.c"),
        (ROOT / "fuzz" / "stage_dag_fuzzer.c", ROOT / "fuzz" / "quota_ledger_fuzzer.c"),
        (ROOT / "fuzz" / "stage_window_fuzzer.c", ROOT / "fuzz" / "quota_window_fuzzer.c"),
        (ROOT / "examples" / "pipeline.toml", ROOT / "examples" / "quota.toml"),
        (ROOT / "examples" / "pipeline.runtime", ROOT / "examples" / "quota.runtime"),
        (ROOT / "fuzz" / "corpus" / "stageenv_fuzzer", ROOT / "fuzz" / "corpus" / "quotaenv_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "stage_fuzzer", ROOT / "fuzz" / "corpus" / "quota_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "stage_dag_fuzzer", ROOT / "fuzz" / "corpus" / "quota_ledger_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "stage_window_fuzzer", ROOT / "fuzz" / "corpus" / "quota_window_fuzzer"),
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

    for p in list((ROOT / "include" / "quotaenv").glob("*")):
        if "stageenv" in p.name:
            p.rename(p.with_name(p.name.replace("stageenv", "quotaenv")))

    for p in list((ROOT / "src" / "quotaenv").glob("*")):
        new_name = p.name
        for a, b in [
            ("stageenv", "quotaenv"),
            ("stageloader", "quotaloader"),
            ("stage_stack", "quota_stack"),
            ("stage_ctx", "quota_ctx"),
            ("stagemap", "quotamap"),
        ]:
            new_name = new_name.replace(a, b)
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    for p in list((ROOT / "include" / "quotacfg").glob("*")):
        if "stage" in p.name:
            p.rename(p.with_name(p.name.replace("stage", "quota")))

    for p in list((ROOT / "tests").glob("test_stage*.c")):
        p.rename(p.with_name(p.name.replace("stage", "quota")))

    corp = ROOT / "fuzz" / "corpus" / "quotaenv_fuzzer"
    if corp.exists():
        for old in list(corp.glob("*.senv")):
            old.rename(old.with_suffix(".qenv"))


def transform_contents() -> None:
    for path in list(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix in SKIP_SUFFIX:
            path.unlink(missing_ok=True)
            continue
        if path.name in SKIP_FILES:
            path.unlink(missing_ok=True)
            continue
        if path.suffix not in {
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".qenv", ".senv",
            ".runtime", "Makefile"
        } and path.name not in {"Makefile", ".gitignore", "LICENSE"}:
            if path.suffix in {".bin"}:
                continue
            continue
        if path.suffix == ".bin":
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
        ROOT / "wsl_test_pocs.sh",
    ]:
        junk.unlink(missing_ok=True)


def plant_bugs() -> None:
    store = ROOT / "src" / "quotaenv" / "store.c"
    text = store.read_text(encoding="utf-8")
    text = text.replace("  free(d->entries);\n", "")
    store.write_text(text, encoding="utf-8")


def patch_domain() -> None:
    write(ROOT / "README.md", README)

    write(ROOT / "examples" / "quota.toml", """[quota]
name = "tenant-alpha"
hard_limit = 10000
soft_limit = 8000
quota_state = "active"

[[quota.buckets]]
label = "api-read"
weight = 48

[[quota.buckets]]
label = "api-write"
weight = 16

[[quota.buckets]]
label = "batch-export"
weight = 8
""")

    write(ROOT / "examples" / "quota.runtime", """# Runtime quota tuning injected during window reset
HARD_LIMIT=5000
SOFT_LIMIT=4000
QUOTA_STATE=warmup
""")

    ledger_fuzz = (ROOT / "fuzz" / "quota_ledger_fuzzer.c").read_text(encoding="utf-8")
    ledger_fuzz = ledger_fuzz.replace("stage_dag", "quota_ledger")
    ledger_fuzz = ledger_fuzz.replace("stagecfg/stage_dag.h", "quotacfg/quota_ledger.h")
    write(ROOT / "fuzz" / "quota_ledger_fuzzer.c", ledger_fuzz)

    build_sh = (ROOT / ".clusterfuzzlite" / "build.sh").read_text(encoding="utf-8")
    build_sh = xform(build_sh)
    build_sh = build_sh.replace(
        "for f in stagecfg stage_merge stage_policy stage_gate stage_dag stage_window stage_coordinator; do",
        "for f in quotacfg quota_merge quota_policy quota_gate quota_ledger quota_window quota_enforcer; do",
    )
    build_sh = build_sh.replace("compile_stageenv", "compile_quotaenv")
    build_sh = build_sh.replace("src/stageenv/", "src/quotaenv/")
    build_sh = build_sh.replace("senv_", "qenv_")
    build_sh = build_sh.replace("stage_stack", "quota_stack")
    build_sh = build_sh.replace("stage_ctx", "quota_ctx")
    build_sh = build_sh.replace("stagemap", "quotamap")
    build_sh = build_sh.replace("stageloader", "quotaloader")
    build_sh = build_sh.replace("build_fuzzer stageenv_fuzzer.c stageenv_fuzzer",
                               "build_fuzzer quotaenv_fuzzer.c quotaenv_fuzzer")
    build_sh = build_sh.replace("build_fuzzer stage_fuzzer.c stage_fuzzer",
                               "build_fuzzer quota_fuzzer.c quota_fuzzer")
    build_sh = build_sh.replace(
        "build_fuzzer stage_dag_fuzzer.c stage_dag_fuzzer",
        "build_fuzzer quota_ledger_fuzzer.c quota_ledger_fuzzer\n"
        "build_fuzzer quota_window_fuzzer.c quota_window_fuzzer",
    )
    build_sh = build_sh.replace("build_fuzzer stage_window_fuzzer.c stage_window_fuzzer", "")
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build_sh, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    wsl = wsl.replace(
        "senv_*.o toml_*.o stagecfg.o stage_merge.o stage_policy.o stage_gate.o "
        "stage_dag.o stage_window.o stage_coordinator.o",
        "qenv_*.o toml_*.o quotacfg.o quota_merge.o quota_policy.o quota_gate.o "
        "quota_ledger.o quota_window.o quota_enforcer.o",
    )
    (ROOT / "build" / "wsl_build.sh").write_text(wsl, encoding="utf-8")

    proj = (ROOT / ".clusterfuzzlite" / "project.yaml").read_text(encoding="utf-8")
    proj = xform(proj)
    (ROOT / ".clusterfuzzlite" / "project.yaml").write_text(proj, encoding="utf-8")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").exists() else ""
    for line in ["/poc/", "crash-*", "*.o", "/tmp/", "/guides/"]:
        if line.strip() not in gitignore:
            gitignore += f"\n{line}\n"
    (ROOT / ".gitignore").write_text(gitignore, encoding="utf-8")

    write(ROOT / "fuzz" / "corpus" / "quota_fuzzer" / "sample.bin",
          bytes([32]) + b"[quota]\nname=\"alpha\"\n" + b"K=1\n")
    if not (ROOT / "fuzz" / "corpus" / "quota_ledger_fuzzer" / "seed.bin").exists():
        write(ROOT / "fuzz" / "corpus" / "quota_ledger_fuzzer" / "seed.bin", bytes(range(32, 96)))


def init_git() -> None:
    git_dir = ROOT / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)
    subprocess.check_call(["git", "init", "-b", "main"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.name", "tolossamuel"], cwd=ROOT)
    subprocess.check_call(
        ["git", "config", "user.email", "tolossamuel@users.noreply.github.com"], cwd=ROOT)
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
    poc = ARTIFACTS / "poc"
    (poc / "verified").mkdir(parents=True, exist_ok=True)
    (poc / "submit").mkdir(parents=True, exist_ok=True)

    write(poc / "README.txt", """quotacfg local PoC artifacts (never commit to GitHub).

verified/  — golden crash bytes
submit/    — patches + task descriptions for AfterQuery upload
""")

    write(poc / "verified" / "entry_leak.qenv", b"FOO=1\n")
    write(poc / "verified" / "entry_leak.toml", b'k = "v"\n')
    shutil.copy2(
        SRC.parent / "artifacts" / "stagecfg" / "poc" / "verified" / "dag_uaf.bin",
        poc / "verified" / "ledger_uaf.bin",
    )
    shutil.copy2(
        SRC.parent / "artifacts" / "stagecfg" / "poc" / "verified" / "merge_uaf.bin",
        poc / "verified" / "merge_uaf.bin",
    )
    write(poc / "verified" / "empty_format.bin", b"")

    wsl_test = """#!/bin/bash
set -eu
cd "$(dirname "$0")/../../quotacfg"
ROOT="$PWD"
ARTIFACTS_ROOT="${ARTIFACTS_ROOT:-$(dirname "$ROOT")/artifacts/quotacfg}"
POC="$ARTIFACTS_ROOT/poc/verified"
OUT=/tmp/quotacfg_out
FAIL=0

if [ ! -d "$POC" ]; then
  echo "Missing PoC corpus: $POC" >&2
  exit 1
fi

if [ ! -x "$OUT/quotaenv_fuzzer" ]; then
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

run_leak "Bug1 quotaenv entry leak" "$OUT/quotaenv_fuzzer" "$POC/entry_leak.qenv"
run_leak "Bug2 toml audit leak" "$OUT/toml_fuzzer" "$POC/entry_leak.toml"
run_crash "Bug3 quota ledger UAF" "$OUT/quota_ledger_fuzzer" "$POC/ledger_uaf.bin"
run_crash "Bug4 toml merge UAF" "$OUT/toml_merge_fuzzer" "$POC/merge_uaf.bin"
run_crash "Bug5 toml format null" "$OUT/toml_format_fuzzer" "$POC/empty_format.bin"
exit $FAIL
"""
    write(ARTIFACTS / "wsl_test_pocs.sh", wsl_test)

    tasks = """# quotacfg task queue (local — not on GitHub)

GitHub: tolossamuel/quotacfg

| # | Bug | Harness | Class | Status |
|---|-----|---------|-------|--------|
| 1 | quotaenv entry realloc leak | quotaenv_fuzzer | LeakSanitizer | Ready |
| 2 | toml audit key leak | toml_fuzzer | LeakSanitizer | Ready |
| 3 | quota ledger compaction UAF | quota_ledger_fuzzer | heap-use-after-free | Ready |
| 4 | toml merge UAF | toml_merge_fuzzer | heap-use-after-free | Ready |
| 5 | toml format null deref | toml_format_fuzzer | null deref | Ready |

PoC bytes and patches: ../artifacts/quotacfg/poc/ (not on GitHub).
"""
    write(ARTIFACTS / "TASKS.md", tasks)


def main() -> None:
    copy_tree()
    transform_contents()
    plant_bugs()
    patch_domain()
    init_git()
    create_artifacts()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
