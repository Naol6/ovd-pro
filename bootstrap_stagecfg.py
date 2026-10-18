#!/usr/bin/env python3
"""Bootstrap batchcfg — TOML batch pipeline manifests + batchenv runtime overlays."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/batchcfg")
SRC = Path("/home/samuel/Documents/fenrir3/poolcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/batchcfg")

TEXT_RENAME = [
    ("pool_warmup_tracker_t", "batch_window_tracker_t"),
    ("pool_warmup_state_t", "batch_window_state_t"),
    ("pool_warmup_tracker", "batch_window_tracker"),
    ("pool_warmup_apply_jitter", "batch_window_apply_jitter"),
    ("pool_warmup_compute_backoff", "batch_window_compute_backoff"),
    ("pool_warmup_tick", "batch_window_tick"),
    ("pool_warmup_due_count", "batch_window_due_count"),
    ("pool_warmup_advance_epoch", "batch_window_advance_epoch"),
    ("pool_warmup_fuzzer", "batch_window_fuzzer"),
    ("pool_warmup.c", "batch_window.c"),
    ("pool_warmup.h", "batch_window.h"),
    ("pool_balancer_t", "batch_coordinator_t"),
    ("pool_balancer_init", "batch_coordinator_init"),
    ("pool_balancer_reset", "batch_coordinator_reset"),
    ("pool_balancer_register", "batch_coordinator_register"),
    ("pool_balancer_tick", "batch_coordinator_tick"),
    ("pool_balancer.c", "batch_coordinator.c"),
    ("pool_balancer.h", "batch_coordinator.h"),
    ("pool_ring_finalize_digest", "batch_dag_finalize_digest"),
    ("pool_ring_compact", "batch_dag_compact"),
    ("pool_ring_register", "batch_dag_register"),
    ("pool_ring_reset", "batch_dag_reset"),
    ("pool_ring_init", "batch_dag_init"),
    ("pool_ring_fuzzer", "batch_dag_fuzzer"),
    ("pool_slot_t", "batch_stage_t"),
    ("pool_ring_t", "batch_dag_t"),
    ("pool_ring.c", "batch_dag.c"),
    ("pool_ring.h", "batch_dag.h"),
    ("poolenv_doc_impl_t", "batchenv_doc_impl_t"),
    ("poolenv_doc_t", "batchenv_doc_t"),
    ("poolenv_error_t", "batchenv_error_t"),
    ("poolenv_options_t", "batchenv_options_t"),
    ("poolenv_entry_t", "batchenv_entry_t"),
    ("poolenv_slice_t", "batchenv_slice_t"),
    ("poolenv_arena_t", "batchenv_arena_t"),
    ("poolenv_token_kind_t", "batchenv_token_kind_t"),
    ("poolenv_token_t", "batchenv_token_t"),
    ("poolenv_internal.h", "batchenv_internal.h"),
    ("poolenv/poolenv_types.h", "batchenv/batchenv_types.h"),
    ("poolenv/poolenv.h", "batchenv/batchenv.h"),
    ("include/poolenv", "include/batchenv"),
    ("src/poolenv/", "src/batchenv/"),
    ("src/poolenv", "src/batchenv"),
    ("poolenv_", "batchenv_"),
    ("POOLENV_", "BATCHENV_"),
    ("Poolenv", "Batchenv"),
    ("poolenv", "batchenv"),
    ("pool_merge", "batch_merge"),
    ("pool_fuzzer", "batch_fuzzer"),
    ("pool_policy", "batch_policy"),
    ("pool_gate", "batch_gate"),
    ("poolcfg", "batchcfg"),
    ("PoolCfg", "BatchCfg"),
    ("POOLCFG", "BATCHCFG"),
    ("attach_stack", "stage_stack"),
    ("attach_ctx", "stage_ctx"),
    ("@attach", "@stage"),
    ("poolmap", "batchmap"),
    ("poolloader", "batchloader"),
    ("apply_poolenv_overlay", "apply_batchenv_overlay"),
    ("apply_poolenv_to_toml", "apply_batchenv_to_toml"),
    ("load_poolenv_memory", "load_batchenv_memory"),
    ("batchcfg_poolenv_free", "batchcfg_batchenv_free"),
    ("/tmp/poolcfg_out", "/tmp/batchcfg_out"),
    ("tolossamuel/poolcfg", "tolossamuel/batchcfg"),
    ("compile_poolenv", "compile_batchenv"),
    ("penv_", "benv_"),
    ("pool.runtime", "batch.runtime"),
    ("pool.toml", "batch.toml"),
    (".penv", ".benv"),
    ("[pool]", "[batch]"),
    ("pool ring", "batch DAG"),
    ("Pool ring", "Batch DAG"),
    ("connection pool", "batch pipeline"),
    ("Connection pool", "Batch pipeline"),
    ("backend slot", "pipeline stage"),
    ("Backend slot", "Pipeline stage"),
    ("slot capacity", "stage priority"),
    ("load-aware", "epoch-aware"),
    ("Balancer", "Coordinator"),
    ("balancer", "coordinator"),
    ("max_connections", "parallelism"),
    ("min_idle", "min_ready"),
    ("health_state", "pipeline_state"),
    ("backends", "stages"),
    ("capacity", "priority"),
    ("slot_count", "stage_count"),
    ("slot_cap", "stage_cap"),
    ("slots", "stages"),
    ("slot->", "stage->"),
    ("slot.", "stage."),
    ("&t->slots", "&t->stages"),
    ("t->slots", "t->stages"),
    ("pool_slot", "batch_stage"),
    ("pool_ring", "batch_dag"),
]

EXCLUDE = {".git", "poc", "guides", "__pycache__"}
SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}
SKIP_SUFFIX = {".o"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add batchcfg public headers", [
        "include/batchcfg/batchcfg.h", "include/batchcfg/batch_merge.h"]),
    ("include: add batchenv public API", [
        "include/batchenv/batchenv.h", "include/batchenv/batchenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add batch policy gate dag headers", [
        "include/batchcfg/batch_policy.h", "include/batchcfg/batch_gate.h",
        "include/batchcfg/batch_dag.h", "include/batchcfg/batch_window.h",
        "include/batchcfg/batch_coordinator.h"]),
    ("src/batchenv: add buffer and string utilities", [
        "src/batchenv/buffer.c", "src/batchenv/buffer.h", "src/batchenv/strutil.c",
        "src/batchenv/strutil.h"]),
    ("src/batchenv: add arena allocator", [
        "src/batchenv/arena.c", "src/batchenv/arena.h", "src/batchenv/batchenv_internal.h"]),
    ("src/batchenv: add error helpers", ["src/batchenv/error.c", "src/batchenv/error.h"]),
    ("src/batchenv: add UTF-8 validation", ["src/batchenv/utf8.c", "src/batchenv/utf8.h"]),
    ("src/batchenv: implement batchenv line lexer", ["src/batchenv/lexer.c", "src/batchenv/lexer.h"]),
    ("src/batchenv: add quoted value unescape", ["src/batchenv/unescape.c", "src/batchenv/unescape.h"]),
    ("src/batchenv: add document store", ["src/batchenv/store.c", "src/batchenv/store.h"]),
    ("src/batchenv: wire assignment parser", ["src/batchenv/parser.c", "src/batchenv/parser.h"]),
    ("src/batchenv: add serialize to batchenv text", ["src/batchenv/serialize.c", "src/batchenv/serialize.h"]),
    ("src/batchenv: add validation pass", ["src/batchenv/validate.c", "src/batchenv/validate.h"]),
    ("src/batchenv: add merge overlay", ["src/batchenv/merge.c", "src/batchenv/merge.h"]),
    ("src/batchenv: add expand and coerce", [
        "src/batchenv/expand.c", "src/batchenv/expand.h", "src/batchenv/coerce.c",
        "src/batchenv/coerce.h"]),
    ("src/batchenv: add walk query diff", [
        "src/batchenv/walk.c", "src/batchenv/walk.h", "src/batchenv/query.c",
        "src/batchenv/query.h", "src/batchenv/diff.c", "src/batchenv/diff.h"]),
    ("src/batchenv: add pretty printer", ["src/batchenv/pretty.c", "src/batchenv/pretty.h"]),
    ("src/batchenv: add stage stack and ctx", [
        "src/batchenv/stage_stack.c", "src/batchenv/stage_stack.h",
        "src/batchenv/stage_ctx.c", "src/batchenv/stage_ctx.h"]),
    ("src/batchenv: add path filter profile", [
        "src/batchenv/path.c", "src/batchenv/path.h", "src/batchenv/filter.c",
        "src/batchenv/filter.h", "src/batchenv/profile.c", "src/batchenv/profile.h"]),
    ("src/batchenv: add snapshot readutil strict canonical", [
        "src/batchenv/snapshot.c", "src/batchenv/snapshot.h", "src/batchenv/readutil.c",
        "src/batchenv/readutil.h", "src/batchenv/strict.c", "src/batchenv/strict.h",
        "src/batchenv/canonical.c", "src/batchenv/canonical.h"]),
    ("src/batchenv: add batchloader and main batchenv module", [
        "src/batchenv/batchloader.c", "src/batchenv/batchenv.c", "src/batchenv/batchmap.c",
        "src/batchenv/batchmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.c", "src/toml/buffer.c"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.c", "src/toml/datetime.c", "src/toml/lexer.c"]),
    ("src/toml: add value and parser core", ["src/toml/value.c", "src/toml/parser.c"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.c", "src/toml/merge.c", "src/toml/serialize.c"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.c", "src/toml/format.c", "src/toml/validator.c", "src/toml/document.c"]),
    ("src: add batchcfg bridge and batchenv-to-toml merge", ["src/batchcfg.c", "src/batch_merge.c"]),
    ("src: add batch policy validator", ["src/batch_policy.c"]),
    ("src: add pipeline gate evaluator", ["src/batch_gate.c"]),
    ("src: add stage dependency DAG with compaction", ["src/batch_dag.c"]),
    ("src: add batch window tracker with jitter", ["src/batch_window.c"]),
    ("src: add epoch-aware batch coordinator", ["src/batch_coordinator.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add batch policy dag window unit tests", [
        "tests/test_batch_policy.c", "tests/test_batch_dag.c", "tests/test_batch_window.c"]),
    ("examples: add TOML batch manifest and runtime overlay", [
        "examples/batch.toml", "examples/batch.runtime"]),
    ("fuzz: add batchenv_fuzzer harness", ["fuzz/batchenv_fuzzer.c"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.c"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.c"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.c"]),
    ("fuzz: add batch_fuzzer for cross-format overlay", ["fuzz/batch_fuzzer.c"]),
    ("fuzz: add batch_dag_fuzzer for stage compaction path", ["fuzz/batch_dag_fuzzer.c"]),
    ("fuzz: add batch_window_fuzzer for coordinator tick paths", ["fuzz/batch_window_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/batchenv_fuzzer/minimal.benv",
        "fuzz/corpus/batchenv_fuzzer/quoted.benv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/batch_fuzzer/sample.bin",
        "fuzz/corpus/batch_dag_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for batchcfg library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable batch pipeline configuration library", []),
]

README = """# batchcfg

batchcfg is a C11 library for batch job pipeline configuration: parse TOML batch manifests, load batchenv runtime tuning overlays, merge layers, validate pipeline policy, and track stage dependency DAGs during windowed scheduling and epoch-aware coordination.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Batchenv layer** — `KEY=VALUE`, `@stage` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply batchenv overlay keys onto parsed TOML documents
- **Batch policy** — validate `[batch]` tables and register pipeline stage priorities into a compaction DAG
- **Pipeline gate** — gate new stage launches on pipeline health and in-flight counts
- **Window tracker** — epoch-aware scheduling windows with jitter and backoff
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `batchenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `batch_fuzzer`, `batch_dag_fuzzer`, `batch_window_fuzzer`.

## Quick start

```c
#include "batchcfg/batchcfg.h"

TomeDoc *toml = NULL;
TomeError err;
batchcfg_load_toml_memory("[batch]\\nname = \\"etl-nightly\\"\\nparallelism = 16\\n", 44, &toml, &err);

batchenv_doc_t *env = NULL;
batchcfg_load_batchenv_memory("PARALLELISM=8\\n", 16, NULL, &env, NULL);
batchcfg_apply_batchenv_to_toml(toml, env);

batchcfg_batchenv_free(env);
batchcfg_toml_free(toml);
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
        out = []
        for n in names:
            if n in EXCLUDE or n.endswith(".o"):
                out.append(n)
        return out

    shutil.copytree(SRC, ROOT, ignore=ignore)

    renames = [
        (ROOT / "include" / "poolcfg", ROOT / "include" / "batchcfg"),
        (ROOT / "include" / "poolenv", ROOT / "include" / "batchenv"),
        (ROOT / "src" / "poolenv", ROOT / "src" / "batchenv"),
        (ROOT / "src" / "poolcfg.c", ROOT / "src" / "batchcfg.c"),
        (ROOT / "src" / "pool_merge.c", ROOT / "src" / "batch_merge.c"),
        (ROOT / "src" / "pool_policy.c", ROOT / "src" / "batch_policy.c"),
        (ROOT / "src" / "pool_gate.c", ROOT / "src" / "batch_gate.c"),
        (ROOT / "src" / "pool_ring.c", ROOT / "src" / "batch_dag.c"),
        (ROOT / "src" / "pool_warmup.c", ROOT / "src" / "batch_window.c"),
        (ROOT / "src" / "pool_balancer.c", ROOT / "src" / "batch_coordinator.c"),
        (ROOT / "fuzz" / "poolenv_fuzzer.c", ROOT / "fuzz" / "batchenv_fuzzer.c"),
        (ROOT / "fuzz" / "pool_fuzzer.c", ROOT / "fuzz" / "batch_fuzzer.c"),
        (ROOT / "fuzz" / "pool_ring_fuzzer.c", ROOT / "fuzz" / "batch_dag_fuzzer.c"),
        (ROOT / "fuzz" / "pool_warmup_fuzzer.c", ROOT / "fuzz" / "batch_window_fuzzer.c"),
        (ROOT / "examples" / "pool.toml", ROOT / "examples" / "batch.toml"),
        (ROOT / "examples" / "pool.runtime", ROOT / "examples" / "batch.runtime"),
        (ROOT / "fuzz" / "corpus" / "poolenv_fuzzer", ROOT / "fuzz" / "corpus" / "batchenv_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "pool_fuzzer", ROOT / "fuzz" / "corpus" / "batch_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "pool_ring_fuzzer", ROOT / "fuzz" / "corpus" / "batch_dag_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "pool_warmup_fuzzer", ROOT / "fuzz" / "corpus" / "batch_window_fuzzer"),
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

    for p in list((ROOT / "include" / "batchenv").glob("*")):
        if "poolenv" in p.name:
            p.rename(p.with_name(p.name.replace("poolenv", "batchenv")))

    for p in list((ROOT / "src" / "batchenv").glob("*")):
        new_name = p.name
        for a, b in [
            ("poolenv", "batchenv"),
            ("poolloader", "batchloader"),
            ("attach_stack", "stage_stack"),
            ("attach_ctx", "stage_ctx"),
            ("poolmap", "batchmap"),
        ]:
            new_name = new_name.replace(a, b)
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    for p in list((ROOT / "include" / "batchcfg").glob("*")):
        if "pool" in p.name:
            p.rename(p.with_name(p.name.replace("pool", "batch")))

    for p in list((ROOT / "tests").glob("test_pool*.c")):
        p.rename(p.with_name(p.name.replace("pool", "batch")))

    corp = ROOT / "fuzz" / "corpus" / "batchenv_fuzzer"
    if corp.exists():
        for old in list(corp.glob("*.penv")):
            old.rename(old.with_suffix(".benv"))


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
        if path.parent.name == "guides":
            continue
        if path.suffix not in {
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".benv", ".penv",
            ".runtime", "Makefile"
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


def patch_domain() -> None:
    write(ROOT / "README.md", README)

    write(ROOT / "examples" / "batch.toml", """[batch]
name = "etl-nightly"
parallelism = 32
min_ready = 4
pipeline_state = "active"

[[batch.stages]]
label = "extract"
priority = 48

[[batch.stages]]
label = "transform"
priority = 16

[[batch.stages]]
label = "load"
priority = 8
""")

    write(ROOT / "examples" / "batch.runtime", """# Runtime batch tuning injected during window scheduling
PARALLELISM=16
MIN_READY=2
PIPELINE_STATE=warmup
""")

    dag_fuzz = (ROOT / "fuzz" / "batch_dag_fuzzer.c").read_text(encoding="utf-8")
    dag_fuzz = dag_fuzz.replace("pool_ring", "batch_dag")
    dag_fuzz = dag_fuzz.replace("poolcfg/pool_ring.h", "batchcfg/batch_dag.h")
    write(ROOT / "fuzz" / "batch_dag_fuzzer.c", dag_fuzz)

    build_sh = (ROOT / ".clusterfuzzlite" / "build.sh").read_text(encoding="utf-8")
    build_sh = xform(build_sh)
    build_sh = build_sh.replace(
        "for f in poolcfg pool_merge pool_policy pool_gate pool_ring pool_warmup pool_balancer; do",
        "for f in batchcfg batch_merge batch_policy batch_gate batch_dag batch_window batch_coordinator; do",
    )
    build_sh = build_sh.replace("compile_poolenv", "compile_batchenv")
    build_sh = build_sh.replace("src/poolenv/", "src/batchenv/")
    build_sh = build_sh.replace("penv_", "benv_")
    build_sh = build_sh.replace("build_fuzzer poolenv_fuzzer.c poolenv_fuzzer",
                               "build_fuzzer batchenv_fuzzer.c batchenv_fuzzer")
    build_sh = build_sh.replace("build_fuzzer pool_fuzzer.c pool_fuzzer",
                               "build_fuzzer batch_fuzzer.c batch_fuzzer")
    build_sh = build_sh.replace(
        "build_fuzzer pool_ring_fuzzer.c pool_ring_fuzzer",
        "build_fuzzer batch_dag_fuzzer.c batch_dag_fuzzer\n"
        "build_fuzzer batch_window_fuzzer.c batch_window_fuzzer",
    )
    build_sh = build_sh.replace("build_fuzzer pool_warmup_fuzzer.c pool_warmup_fuzzer", "")
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build_sh, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    wsl = wsl.replace(
        "penv_*.o toml_*.o poolcfg.o pool_merge.o pool_policy.o pool_gate.o "
        "pool_ring.o pool_warmup.o pool_balancer.o",
        "benv_*.o toml_*.o batchcfg.o batch_merge.o batch_policy.o batch_gate.o "
        "batch_dag.o batch_window.o batch_coordinator.o",
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

    write(ROOT / "fuzz" / "corpus" / "batch_fuzzer" / "sample.bin",
          bytes([32]) + b"[batch]\nname=\"etl\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "batch_dag_fuzzer" / "seed.bin", bytes(range(32, 96)))


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


def create_artifacts_template() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    poc_dir = ARTIFACTS / "poc"
    (poc_dir / "verified").mkdir(parents=True, exist_ok=True)
    (poc_dir / "submit").mkdir(parents=True, exist_ok=True)
    write(poc_dir / "README.txt", """batchcfg local PoC artifacts (never commit to GitHub).

verified/  — golden crash bytes
submit/    — patches + task descriptions for AfterQuery upload
""")


def main() -> None:
    copy_tree()
    transform_contents()
    patch_domain()
    init_git()
    create_artifacts_template()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
