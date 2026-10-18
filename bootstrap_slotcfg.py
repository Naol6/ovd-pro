#!/usr/bin/env python3
"""Bootstrap slotcfg — TOML worker slot manifests + slotenv runtime overlays."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/slotcfg")
SRC = Path("/home/samuel/Documents/fenrir3/budgetcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/slotcfg")

TEXT_RENAME = [
    ("budgetenv_doc_impl_t", "slotenv_doc_impl_t"),
    ("budgetenv_doc_t", "slotenv_doc_t"),
    ("budgetenv_error_t", "slotenv_error_t"),
    ("budgetenv_options_t", "slotenv_options_t"),
    ("budgetenv_entry_t", "slotenv_entry_t"),
    ("budgetenv_slice_t", "slotenv_slice_t"),
    ("budgetenv_arena_t", "slotenv_arena_t"),
    ("budgetenv_token_kind_t", "slotenv_token_kind_t"),
    ("budgetenv_token_t", "slotenv_token_t"),
    ("budgetenv_internal.h", "slotenv_internal.h"),
    ("budgetenv/budgetenv_types.h", "slotenv/slotenv_types.h"),
    ("budgetenv/budgetenv.h", "slotenv/slotenv.h"),
    ("include/budgetenv", "include/slotenv"),
    ("src/budgetenv/", "src/slotenv/"),
    ("src/budgetenv", "src/slotenv"),
    ("budgetenv_", "slotenv_"),
    ("BUDGETENV_", "SLOTENV_"),
    ("Budgetenv", "Slotenv"),
    ("budgetenv", "slotenv"),
    ("budget_merge", "slot_merge"),
    ("budget_fuzzer", "slot_fuzzer"),
    ("budget_policy", "slot_policy"),
    ("budget_gate", "slot_gate"),
    ("budget_ledger", "slot_ledger"),
    ("budget_window", "slot_window"),
    ("budget_enforcer", "slot_enforcer"),
    ("budgetcfg", "slotcfg"),
    ("BudgetCfg", "SlotCfg"),
    ("BUDGETCFG", "SLOTCFG"),
    ("budget_stack", "slot_stack"),
    ("budget_ctx", "slot_ctx"),
    ("@budget", "@slot"),
    ("budgetmap", "slotmap"),
    ("budgetloader", "slotloader"),
    ("apply_budgetenv_overlay", "apply_slotenv_overlay"),
    ("apply_budgetenv_to_toml", "apply_slotenv_to_toml"),
    ("load_budgetenv_memory", "load_slotenv_memory"),
    ("slotcfg_budgetenv_free", "slotcfg_slotenv_free"),
    ("/tmp/budgetcfg_out", "/tmp/slotcfg_out"),
    ("tolossamuel/budgetcfg", "tolossamuel/slotcfg"),
    ("compile_budgetenv", "compile_slotenv"),
    ("benv_", "senv_"),
    ("budget.runtime", "slot.runtime"),
    ("budget.toml", "slot.toml"),
    ("[budget]", "[slot]"),
    ("Budget policy", "Slot policy"),
    ("budget policy", "slot policy"),
    ("budget ledger", "slot ledger"),
    ("Budget ledger", "Slot ledger"),
    ("capacity budget", "worker slot allocation"),
    ("Capacity budget", "Worker slot allocation"),
    ("allowance", "capacity"),
    ("Allowance", "Capacity"),
    ("budget_bucket", "slot_bucket"),
    ("budget_bucket_t", "slot_bucket_t"),
    (".benv", ".senv"),
    ("penv_", "senv_"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}
EXCLUDE = {".git", "poc", "guides", "__pycache__"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add slotcfg public headers", [
        "include/slotcfg/slotcfg.h", "include/slotcfg/slot_merge.h"]),
    ("include: add slotenv public API", [
        "include/slotenv/slotenv.h", "include/slotenv/slotenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add slot policy gate ledger headers", [
        "include/slotcfg/slot_policy.h", "include/slotcfg/slot_gate.h",
        "include/slotcfg/slot_ledger.h", "include/slotcfg/slot_window.h",
        "include/slotcfg/slot_enforcer.h"]),
    ("src/slotenv: add buffer and string utilities", [
        "src/slotenv/buffer.c", "src/slotenv/buffer.h", "src/slotenv/strutil.c",
        "src/slotenv/strutil.h"]),
    ("src/slotenv: add arena allocator", [
        "src/slotenv/arena.c", "src/slotenv/arena.h", "src/slotenv/slotenv_internal.h"]),
    ("src/slotenv: add error helpers", ["src/slotenv/error.c", "src/slotenv/error.h"]),
    ("src/slotenv: add UTF-8 validation", ["src/slotenv/utf8.c", "src/slotenv/utf8.h"]),
    ("src/slotenv: implement slotenv line lexer", ["src/slotenv/lexer.c", "src/slotenv/lexer.h"]),
    ("src/slotenv: add quoted value unescape", ["src/slotenv/unescape.c", "src/slotenv/unescape.h"]),
    ("src/slotenv: add document store", ["src/slotenv/store.c", "src/slotenv/store.h"]),
    ("src/slotenv: wire assignment parser", ["src/slotenv/parser.c", "src/slotenv/parser.h"]),
    ("src/slotenv: add serialize to slotenv text", ["src/slotenv/serialize.c", "src/slotenv/serialize.h"]),
    ("src/slotenv: add validation pass", ["src/slotenv/validate.c", "src/slotenv/validate.h"]),
    ("src/slotenv: add merge overlay", ["src/slotenv/merge.c", "src/slotenv/merge.h"]),
    ("src/slotenv: add expand and coerce", [
        "src/slotenv/expand.c", "src/slotenv/expand.h", "src/slotenv/coerce.c",
        "src/slotenv/coerce.h"]),
    ("src/slotenv: add walk query diff", [
        "src/slotenv/walk.c", "src/slotenv/walk.h", "src/slotenv/query.c",
        "src/slotenv/query.h", "src/slotenv/diff.c", "src/slotenv/diff.h"]),
    ("src/slotenv: add pretty printer", ["src/slotenv/pretty.c", "src/slotenv/pretty.h"]),
    ("src/slotenv: add slot stack and ctx", [
        "src/slotenv/slot_stack.c", "src/slotenv/slot_stack.h",
        "src/slotenv/slot_ctx.c", "src/slotenv/slot_ctx.h"]),
    ("src/slotenv: add path filter profile", [
        "src/slotenv/path.c", "src/slotenv/path.h", "src/slotenv/filter.c",
        "src/slotenv/filter.h", "src/slotenv/profile.c", "src/slotenv/profile.h"]),
    ("src/slotenv: add snapshot readutil strict canonical", [
        "src/slotenv/snapshot.c", "src/slotenv/snapshot.h", "src/slotenv/readutil.c",
        "src/slotenv/readutil.h", "src/slotenv/strict.c", "src/slotenv/strict.h",
        "src/slotenv/canonical.c", "src/slotenv/canonical.h"]),
    ("src/slotenv: add slotloader and main slotenv module", [
        "src/slotenv/slotloader.c", "src/slotenv/slotenv.c", "src/slotenv/slotmap.c",
        "src/slotenv/slotmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.c", "src/toml/buffer.c"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.c", "src/toml/datetime.c", "src/toml/lexer.c"]),
    ("src/toml: add value and parser core", ["src/toml/value.c", "src/toml/parser.c"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.c", "src/toml/merge.c", "src/toml/serialize.c"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.c", "src/toml/format.c", "src/toml/validator.c", "src/toml/document.c"]),
    ("src: add slotcfg bridge and slotenv-to-toml merge", ["src/slotcfg.c", "src/slot_merge.c"]),
    ("src: add slot policy validator", ["src/slot_policy.c"]),
    ("src: add admission gate evaluator", ["src/slot_gate.c"]),
    ("src: add slot reservation ledger with compaction", ["src/slot_ledger.c"]),
    ("src: add slot release window tracker", ["src/slot_window.c"]),
    ("src: add slot enforcer for capacity limits", ["src/slot_enforcer.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add slot policy ledger window unit tests", [
        "tests/test_slot_policy.c", "tests/test_slot_ledger.c", "tests/test_slot_window.c"]),
    ("examples: add TOML slot manifest and runtime overlay", [
        "examples/slot.toml", "examples/slot.runtime"]),
    ("fuzz: add slotenv_fuzzer harness", ["fuzz/slotenv_fuzzer.c"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.c"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.c"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.c"]),
    ("fuzz: add slot_fuzzer for cross-format overlay", ["fuzz/slot_fuzzer.c"]),
    ("fuzz: add slot_ledger_fuzzer for reservation compaction path", ["fuzz/slot_ledger_fuzzer.c"]),
    ("fuzz: add slot_window_fuzzer for release window tick paths", ["fuzz/slot_window_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/slotenv_fuzzer/minimal.senv",
        "fuzz/corpus/slotenv_fuzzer/quoted.senv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/slot_fuzzer/sample.bin",
        "fuzz/corpus/slot_ledger_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for slotcfg library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable slot allocation configuration library", []),
]

README = """# slotcfg

slotcfg is a C11 library for distributed worker slot allocation configuration: parse TOML slot manifests, load slotenv runtime capacity overlays, merge layers, validate slot policy, and track slot reservation ledgers during epoch window release and admission gating.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Slotenv layer** — `KEY=VALUE`, `@slot` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply slotenv overlay keys onto parsed TOML documents
- **Slot policy** — validate `[slot]` tables and register worker capacities into a compaction ledger
- **Admission gate** — gate new slot claims on pool health and in-flight reservations
- **Release window** — epoch-aware slot release windows with jitter
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `slotenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `slot_fuzzer`, `slot_ledger_fuzzer`, `slot_window_fuzzer`.

## Quick start

```c
#include "slotcfg/slotcfg.h"

TomeDoc *toml = NULL;
TomeError err;
slotcfg_load_toml_memory("[slot]\\nname = \\"workers-east\\"\\nmax_slots = 64\\n", 44, &toml, &err);

slotenv_doc_t *env = NULL;
slotcfg_load_slotenv_memory("MAX_SLOTS=48\\n", 14, NULL, &env, NULL);
slotcfg_apply_slotenv_to_toml(toml, env);

slotcfg_slotenv_free(env);
slotcfg_toml_free(toml);
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
        (ROOT / "include" / "budgetcfg", ROOT / "include" / "slotcfg"),
        (ROOT / "include" / "budgetenv", ROOT / "include" / "slotenv"),
        (ROOT / "src" / "budgetenv", ROOT / "src" / "slotenv"),
        (ROOT / "src" / "budgetcfg.c", ROOT / "src" / "slotcfg.c"),
        (ROOT / "src" / "budget_merge.c", ROOT / "src" / "slot_merge.c"),
        (ROOT / "src" / "budget_policy.c", ROOT / "src" / "slot_policy.c"),
        (ROOT / "src" / "budget_gate.c", ROOT / "src" / "slot_gate.c"),
        (ROOT / "src" / "budget_ledger.c", ROOT / "src" / "slot_ledger.c"),
        (ROOT / "src" / "budget_window.c", ROOT / "src" / "slot_window.c"),
        (ROOT / "src" / "budget_enforcer.c", ROOT / "src" / "slot_enforcer.c"),
        (ROOT / "fuzz" / "budgetenv_fuzzer.c", ROOT / "fuzz" / "slotenv_fuzzer.c"),
        (ROOT / "fuzz" / "budget_fuzzer.c", ROOT / "fuzz" / "slot_fuzzer.c"),
        (ROOT / "fuzz" / "budget_ledger_fuzzer.c", ROOT / "fuzz" / "slot_ledger_fuzzer.c"),
        (ROOT / "fuzz" / "budget_window_fuzzer.c", ROOT / "fuzz" / "slot_window_fuzzer.c"),
        (ROOT / "examples" / "budget.toml", ROOT / "examples" / "slot.toml"),
        (ROOT / "examples" / "budget.runtime", ROOT / "examples" / "slot.runtime"),
        (ROOT / "fuzz" / "corpus" / "budgetenv_fuzzer", ROOT / "fuzz" / "corpus" / "slotenv_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "budget_fuzzer", ROOT / "fuzz" / "corpus" / "slot_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "budget_ledger_fuzzer", ROOT / "fuzz" / "corpus" / "slot_ledger_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "budget_window_fuzzer", ROOT / "fuzz" / "corpus" / "slot_window_fuzzer"),
        (ROOT / "tests" / "test_budget_policy.c", ROOT / "tests" / "test_slot_policy.c"),
        (ROOT / "tests" / "test_budget_ledger.c", ROOT / "tests" / "test_slot_ledger.c"),
        (ROOT / "tests" / "test_budget_window.c", ROOT / "tests" / "test_slot_window.c"),
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

    for p in list((ROOT / "include" / "slotenv").glob("*")):
        if "budgetenv" in p.name:
            p.rename(p.with_name(p.name.replace("budgetenv", "slotenv")))

    for p in list((ROOT / "src" / "slotenv").glob("*")):
        new_name = p.name.replace("budgetenv", "slotenv")
        new_name = new_name.replace("budgetloader", "slotloader")
        new_name = new_name.replace("budget_stack", "slot_stack")
        new_name = new_name.replace("budget_ctx", "slot_ctx")
        new_name = new_name.replace("budgetmap", "slotmap")
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    for p in list((ROOT / "include" / "slotcfg").glob("*")):
        if "budget" in p.name:
            p.rename(p.with_name(p.name.replace("budget", "slot")))

    for p in list((ROOT / "fuzz" / "corpus" / "slotenv_fuzzer").glob("*")):
        if p.suffix == ".benv":
            p.rename(p.with_suffix(".senv"))


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
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".benv", ".senv",
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


def plant_bugs() -> None:
    """Plant standard 5-bug set; hard ledger UAF instead of shallow hex OOB."""
    store = (ROOT / "src" / "slotenv" / "store.c").read_text(encoding="utf-8")
    store = store.replace("  free(d->entries);\n", "")
    (ROOT / "src" / "slotenv" / "store.c").write_text(store, encoding="utf-8")

    write(ROOT / "README.md", README)

    write(ROOT / "examples" / "slot.toml", """[slot]
name = "workers-east"
max_slots = 64
min_free = 4
release_epoch_ms = 5000

[[slot.pools]]
label = "cpu-heavy"
capacity = 32

[[slot.pools]]
label = "io-bound"
capacity = 16
""")

    write(ROOT / "examples" / "slot.runtime", """# Runtime slot capacity injected during rolling deploy
MAX_SLOTS=48
MIN_FREE=2
RELEASE_EPOCH_MS=3000
""")


def patch_build() -> None:
    build_sh = (ROOT / ".clusterfuzzlite" / "build.sh").read_text(encoding="utf-8")
    build_sh = xform(build_sh)
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build_sh, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    (ROOT / "build" / "wsl_build.sh").write_text(wsl, encoding="utf-8")

    proj = (ROOT / ".clusterfuzzlite" / "project.yaml").read_text(encoding="utf-8")
    proj = xform(proj)
    (ROOT / ".clusterfuzzlite" / "project.yaml").write_text(proj, encoding="utf-8")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "crash-" not in gitignore:
        gitignore += "\ncrash-*\n/poc/\n"
    (ROOT / ".gitignore").write_text(gitignore, encoding="utf-8")


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
    plant_bugs()
    patch_build()
    init_git()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
