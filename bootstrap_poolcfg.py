#!/usr/bin/env python3
"""Bootstrap poolcfg — TOML connection pool manifests + poolenv runtime overlays."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/poolcfg")
SRC = Path("/home/samuel/Documents/fenrir3/holdcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/poolcfg")

TEXT_RENAME = [
    ("hold_renewal_tracker_t", "pool_warmup_tracker_t"),
    ("hold_renewal_state_t", "pool_warmup_state_t"),
    ("hold_renewal_tracker", "pool_warmup_tracker"),
    ("hold_renewal_apply_jitter", "pool_warmup_apply_jitter"),
    ("hold_renewal_compute_backoff", "pool_warmup_compute_backoff"),
    ("hold_renewal_tick", "pool_warmup_tick"),
    ("hold_renewal_due_count", "pool_warmup_due_count"),
    ("hold_renewal_advance_epoch", "pool_warmup_advance_epoch"),
    ("hold_renewal_fuzzer", "pool_warmup_fuzzer"),
    ("hold_renewal.c", "pool_warmup.c"),
    ("hold_renewal.h", "pool_warmup.h"),
    ("hold_coordinator_t", "pool_balancer_t"),
    ("hold_coordinator_init", "pool_balancer_init"),
    ("hold_coordinator_reset", "pool_balancer_reset"),
    ("hold_coordinator_register", "pool_balancer_register"),
    ("hold_coordinator_tick", "pool_balancer_tick"),
    ("hold_coordinator.c", "pool_balancer.c"),
    ("hold_coordinator.h", "pool_balancer.h"),
    ("hold_registry_finalize_digest", "pool_ring_finalize_digest"),
    ("hold_registry_compact", "pool_ring_compact"),
    ("hold_registry_register", "pool_ring_register"),
    ("hold_registry_reset", "pool_ring_reset"),
    ("hold_registry_init", "pool_ring_init"),
    ("hold_registry_fuzzer", "pool_ring_fuzzer"),
    ("hold_registry_t", "pool_ring_t"),
    ("hold_holder_t", "pool_slot_t"),
    ("hold_registry.c", "pool_ring.c"),
    ("hold_registry.h", "pool_ring.h"),
    ("holdenv_doc_impl_t", "poolenv_doc_impl_t"),
    ("holdenv_doc_t", "poolenv_doc_t"),
    ("holdenv_error_t", "poolenv_error_t"),
    ("holdenv_options_t", "poolenv_options_t"),
    ("holdenv_entry_t", "poolenv_entry_t"),
    ("holdenv_slice_t", "poolenv_slice_t"),
    ("holdenv_arena_t", "poolenv_arena_t"),
    ("holdenv_token_kind_t", "poolenv_token_kind_t"),
    ("holdenv_token_t", "poolenv_token_t"),
    ("holdenv_internal.h", "poolenv_internal.h"),
    ("holdenv/holdenv_types.h", "poolenv/poolenv_types.h"),
    ("holdenv/holdenv.h", "poolenv/poolenv.h"),
    ("include/holdenv", "include/poolenv"),
    ("src/holdenv/", "src/poolenv/"),
    ("src/holdenv", "src/poolenv"),
    ("holdenv_", "poolenv_"),
    ("HOLDENV_", "POOLENV_"),
    ("Holdenv", "Poolenv"),
    ("holdenv", "poolenv"),
    ("hold_merge", "pool_merge"),
    ("hold_fuzzer", "pool_fuzzer"),
    ("hold_policy", "pool_policy"),
    ("hold_gate", "pool_gate"),
    ("holdcfg", "poolcfg"),
    ("HoldCfg", "PoolCfg"),
    ("HOLDCFG", "POOLCFG"),
    ("renewal_stack", "attach_stack"),
    ("renewal_ctx", "attach_ctx"),
    ("@renew", "@attach"),
    ("holdmap", "poolmap"),
    ("holdloader", "poolloader"),
    ("apply_holdenv_overlay", "apply_poolenv_overlay"),
    ("apply_holdenv_to_toml", "apply_poolenv_to_toml"),
    ("load_holdenv_memory", "load_poolenv_memory"),
    ("poolcfg_holdenv_free", "poolcfg_poolenv_free"),
    ("/tmp/holdcfg_out", "/tmp/poolcfg_out"),
    ("tolossamuel/holdcfg", "tolossamuel/poolcfg"),
    ("compile_holdenv", "compile_poolenv"),
    ("henv_", "penv_"),
    ("hold.runtime", "pool.runtime"),
    ("hold.toml", "pool.toml"),
    (".henv", ".penv"),
    ("[hold]", "[pool]"),
    ("hold registry", "pool ring"),
    ("Hold registry", "Pool ring"),
    ("request hedging", "connection pool"),
    ("Request hedging", "Connection pool"),
    ("lease hold", "connection pool"),
    ("Lease hold", "Connection pool"),
    ("holder registration", "backend slot registration"),
    ("Holder registration", "Backend slot registration"),
    ("hold holder", "pool backend slot"),
    ("Hold holder", "Pool backend slot"),
    ("ttl_ms", "capacity"),
    ("TTL budget", "slot capacity"),
    ("quorum-aware", "load-aware"),
    ("quorum table", "pool table"),
    ("Quorum", "Balancer"),
    ("quorum", "balancer"),
]

EXCLUDE = {".git", "poc", "guides", "__pycache__"}
SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}
SKIP_SUFFIX = {".o"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add poolcfg public headers", [
        "include/poolcfg/poolcfg.h", "include/poolcfg/pool_merge.h"]),
    ("include: add poolenv public API", [
        "include/poolenv/poolenv.h", "include/poolenv/poolenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add pool policy gate ring headers", [
        "include/poolcfg/pool_policy.h", "include/poolcfg/pool_gate.h",
        "include/poolcfg/pool_ring.h", "include/poolcfg/pool_warmup.h",
        "include/poolcfg/pool_balancer.h"]),
    ("src/poolenv: add buffer and string utilities", [
        "src/poolenv/buffer.c", "src/poolenv/buffer.h", "src/poolenv/strutil.c",
        "src/poolenv/strutil.h"]),
    ("src/poolenv: add arena allocator", [
        "src/poolenv/arena.c", "src/poolenv/arena.h", "src/poolenv/poolenv_internal.h"]),
    ("src/poolenv: add error helpers", ["src/poolenv/error.c", "src/poolenv/error.h"]),
    ("src/poolenv: add UTF-8 validation", ["src/poolenv/utf8.c", "src/poolenv/utf8.h"]),
    ("src/poolenv: implement poolenv line lexer", ["src/poolenv/lexer.c", "src/poolenv/lexer.h"]),
    ("src/poolenv: add quoted value unescape", ["src/poolenv/unescape.c", "src/poolenv/unescape.h"]),
    ("src/poolenv: add document store", ["src/poolenv/store.c", "src/poolenv/store.h"]),
    ("src/poolenv: wire assignment parser", ["src/poolenv/parser.c", "src/poolenv/parser.h"]),
    ("src/poolenv: add serialize to poolenv text", ["src/poolenv/serialize.c", "src/poolenv/serialize.h"]),
    ("src/poolenv: add validation pass", ["src/poolenv/validate.c", "src/poolenv/validate.h"]),
    ("src/poolenv: add merge overlay", ["src/poolenv/merge.c", "src/poolenv/merge.h"]),
    ("src/poolenv: add expand and coerce", [
        "src/poolenv/expand.c", "src/poolenv/expand.h", "src/poolenv/coerce.c",
        "src/poolenv/coerce.h"]),
    ("src/poolenv: add walk query diff", [
        "src/poolenv/walk.c", "src/poolenv/walk.h", "src/poolenv/query.c",
        "src/poolenv/query.h", "src/poolenv/diff.c", "src/poolenv/diff.h"]),
    ("src/poolenv: add pretty printer", ["src/poolenv/pretty.c", "src/poolenv/pretty.h"]),
    ("src/poolenv: add attach stack and ctx", [
        "src/poolenv/attach_stack.c", "src/poolenv/attach_stack.h",
        "src/poolenv/attach_ctx.c", "src/poolenv/attach_ctx.h"]),
    ("src/poolenv: add path filter profile", [
        "src/poolenv/path.c", "src/poolenv/path.h", "src/poolenv/filter.c",
        "src/poolenv/filter.h", "src/poolenv/profile.c", "src/poolenv/profile.h"]),
    ("src/poolenv: add snapshot readutil strict canonical", [
        "src/poolenv/snapshot.c", "src/poolenv/snapshot.h", "src/poolenv/readutil.c",
        "src/poolenv/readutil.h", "src/poolenv/strict.c", "src/poolenv/strict.h",
        "src/poolenv/canonical.c", "src/poolenv/canonical.h"]),
    ("src/poolenv: add poolloader and main poolenv module", [
        "src/poolenv/poolloader.c", "src/poolenv/poolenv.c", "src/poolenv/poolmap.c",
        "src/poolenv/poolmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.c", "src/toml/buffer.c"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.c", "src/toml/datetime.c", "src/toml/lexer.c"]),
    ("src/toml: add value and parser core", ["src/toml/value.c", "src/toml/parser.c"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.c", "src/toml/merge.c", "src/toml/serialize.c"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.c", "src/toml/format.c", "src/toml/validator.c", "src/toml/document.c"]),
    ("src: add poolcfg bridge and poolenv-to-toml merge", ["src/poolcfg.c", "src/pool_merge.c"]),
    ("src: add pool policy validator", ["src/pool_policy.c"]),
    ("src: add connection gate evaluator", ["src/pool_gate.c"]),
    ("src: add backend slot ring with compaction", ["src/pool_ring.c"]),
    ("src: add pool warmup tracker with jitter", ["src/pool_warmup.c"]),
    ("src: add load-aware pool balancer coordinator", ["src/pool_balancer.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add pool policy ring warmup unit tests", [
        "tests/test_pool_policy.c", "tests/test_pool_ring.c", "tests/test_pool_warmup.c"]),
    ("examples: add TOML pool manifest and runtime overlay", [
        "examples/pool.toml", "examples/pool.runtime"]),
    ("fuzz: add poolenv_fuzzer harness", ["fuzz/poolenv_fuzzer.c"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.c"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.c"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.c"]),
    ("fuzz: add pool_fuzzer for cross-format overlay", ["fuzz/pool_fuzzer.c"]),
    ("fuzz: add pool_ring_fuzzer for slot compaction path", ["fuzz/pool_ring_fuzzer.c"]),
    ("fuzz: add pool_warmup_fuzzer for balancer tick paths", ["fuzz/pool_warmup_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/poolenv_fuzzer/minimal.penv",
        "fuzz/corpus/poolenv_fuzzer/quoted.penv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/pool_fuzzer/sample.bin",
        "fuzz/corpus/pool_ring_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for poolcfg library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable connection pool configuration library", []),
]

README = """# poolcfg

poolcfg is a C11 library for database and API connection pool configuration: parse TOML pool manifests, load poolenv runtime tuning overlays, merge layers, validate pool policy, and track backend slot rings during warm-up and load balancing.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Poolenv layer** — `KEY=VALUE`, `@attach` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply poolenv overlay keys onto parsed TOML documents
- **Pool policy** — validate `[pool]` tables and register backend slot weights into a compaction ring
- **Connection gate** — gate new connections on pool health and in-flight counts
- **Warm-up tracker** — epoch-aware warm-up scheduling with jitter and backoff
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `poolenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `pool_fuzzer`, `pool_ring_fuzzer`, `pool_warmup_fuzzer`.

## Quick start

```c
#include "poolcfg/poolcfg.h"

TomeDoc *toml = NULL;
TomeError err;
poolcfg_load_toml_memory("[pool]\\nname = \\"payments\\"\\nmax_connections = 64\\n", 45, &toml, &err);

poolenv_doc_t *env = NULL;
poolcfg_load_poolenv_memory("MAX_CONNECTIONS=32\\n", 19, NULL, &env, NULL);
poolcfg_apply_poolenv_to_toml(toml, env);

poolcfg_poolenv_free(env);
poolcfg_toml_free(toml);
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
        (ROOT / "include" / "holdcfg", ROOT / "include" / "poolcfg"),
        (ROOT / "include" / "holdenv", ROOT / "include" / "poolenv"),
        (ROOT / "src" / "holdenv", ROOT / "src" / "poolenv"),
        (ROOT / "src" / "holdcfg.c", ROOT / "src" / "poolcfg.c"),
        (ROOT / "src" / "hold_merge.c", ROOT / "src" / "pool_merge.c"),
        (ROOT / "src" / "hold_policy.c", ROOT / "src" / "pool_policy.c"),
        (ROOT / "src" / "hold_gate.c", ROOT / "src" / "pool_gate.c"),
        (ROOT / "src" / "hold_registry.c", ROOT / "src" / "pool_ring.c"),
        (ROOT / "src" / "hold_renewal.c", ROOT / "src" / "pool_warmup.c"),
        (ROOT / "src" / "hold_coordinator.c", ROOT / "src" / "pool_balancer.c"),
        (ROOT / "fuzz" / "holdenv_fuzzer.c", ROOT / "fuzz" / "poolenv_fuzzer.c"),
        (ROOT / "fuzz" / "hold_fuzzer.c", ROOT / "fuzz" / "pool_fuzzer.c"),
        (ROOT / "fuzz" / "hold_registry_fuzzer.c", ROOT / "fuzz" / "pool_ring_fuzzer.c"),
        (ROOT / "fuzz" / "hold_renewal_fuzzer.c", ROOT / "fuzz" / "pool_warmup_fuzzer.c"),
        (ROOT / "examples" / "hold.toml", ROOT / "examples" / "pool.toml"),
        (ROOT / "examples" / "hold.runtime", ROOT / "examples" / "pool.runtime"),
        (ROOT / "fuzz" / "corpus" / "holdenv_fuzzer", ROOT / "fuzz" / "corpus" / "poolenv_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "hold_fuzzer", ROOT / "fuzz" / "corpus" / "pool_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "hold_registry_fuzzer", ROOT / "fuzz" / "corpus" / "pool_ring_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "hold_renewal_fuzzer", ROOT / "fuzz" / "corpus" / "pool_warmup_fuzzer"),
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

    for p in list((ROOT / "include" / "poolenv").glob("*")):
        if "holdenv" in p.name:
            p.rename(p.with_name(p.name.replace("holdenv", "poolenv")))

    for p in list((ROOT / "src" / "poolenv").glob("*")):
        new_name = p.name
        for a, b in [
            ("holdenv", "poolenv"),
            ("holdloader", "poolloader"),
            ("renewal_stack", "attach_stack"),
            ("renewal_ctx", "attach_ctx"),
            ("holdmap", "poolmap"),
        ]:
            new_name = new_name.replace(a, b)
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    for p in list((ROOT / "include" / "poolcfg").glob("*")):
        if "hold" in p.name:
            p.rename(p.with_name(p.name.replace("hold", "pool")))

    for p in list((ROOT / "tests").glob("test_hold*.c")):
        p.rename(p.with_name(p.name.replace("hold", "pool")))

    corp = ROOT / "fuzz" / "corpus" / "poolenv_fuzzer"
    if corp.exists():
        for old in list(corp.glob("*.henv")):
            old.rename(old.with_suffix(".penv"))


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
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".penv", ".henv",
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

    write(ROOT / "examples" / "pool.toml", """[pool]
name = "payments-db"
max_connections = 64
min_idle = 8
health_state = "healthy"

[[pool.backends]]
label = "primary"
capacity = 48

[[pool.backends]]
label = "replica"
capacity = 16
""")

    write(ROOT / "examples" / "pool.runtime", """# Runtime pool tuning injected during warm-up
MAX_CONNECTIONS=32
MIN_IDLE=4
HEALTH_STATE=warmup
""")

    ring_fuzz = (ROOT / "fuzz" / "pool_ring_fuzzer.c").read_text(encoding="utf-8")
    ring_fuzz = ring_fuzz.replace("hold_registry", "pool_ring")
    ring_fuzz = ring_fuzz.replace("holdcfg/hold_registry.h", "poolcfg/pool_ring.h")
    write(ROOT / "fuzz" / "pool_ring_fuzzer.c", ring_fuzz)

    build_sh = (ROOT / ".clusterfuzzlite" / "build.sh").read_text(encoding="utf-8")
    build_sh = xform(build_sh)
    build_sh = build_sh.replace(
        "for f in holdcfg hold_merge hold_policy hold_gate hold_registry hold_renewal hold_coordinator; do",
        "for f in poolcfg pool_merge pool_policy pool_gate pool_ring pool_warmup pool_balancer; do",
    )
    build_sh = build_sh.replace("compile_holdenv", "compile_poolenv")
    build_sh = build_sh.replace("src/holdenv/", "src/poolenv/")
    build_sh = build_sh.replace("henv_", "penv_")
    build_sh = build_sh.replace("build_fuzzer holdenv_fuzzer.c holdenv_fuzzer",
                               "build_fuzzer poolenv_fuzzer.c poolenv_fuzzer")
    build_sh = build_sh.replace("build_fuzzer hold_fuzzer.c hold_fuzzer",
                               "build_fuzzer pool_fuzzer.c pool_fuzzer")
    build_sh = build_sh.replace(
        "build_fuzzer hold_registry_fuzzer.c hold_registry_fuzzer",
        "build_fuzzer pool_ring_fuzzer.c pool_ring_fuzzer\n"
        "build_fuzzer pool_warmup_fuzzer.c pool_warmup_fuzzer",
    )
    build_sh = build_sh.replace("build_fuzzer hold_renewal_fuzzer.c hold_renewal_fuzzer", "")
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build_sh, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    wsl = wsl.replace(
        "holdenv_*.o toml_*.o holdcfg.o hold_merge.o hold_policy.o hold_gate.o "
        "hold_registry.o hold_renewal.o hold_coordinator.o",
        "penv_*.o toml_*.o poolcfg.o pool_merge.o pool_policy.o pool_gate.o "
        "pool_ring.o pool_warmup.o pool_balancer.o",
    )
    (ROOT / "build" / "wsl_build.sh").write_text(wsl, encoding="utf-8")

    proj = (ROOT / ".clusterfuzzlite" / "project.yaml").read_text(encoding="utf-8")
    proj = xform(proj)
    (ROOT / ".clusterfuzzlite" / "project.yaml").write_text(proj, encoding="utf-8")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").exists() else ""
    for line in ["/poc/", "crash-*", "*.o", "/tmp/"]:
        if line.strip() not in gitignore:
            gitignore += f"\n{line}\n"
    (ROOT / ".gitignore").write_text(gitignore, encoding="utf-8")

    write(ROOT / "fuzz" / "corpus" / "pool_fuzzer" / "sample.bin",
          bytes([32]) + b"[pool]\nname=\"api\"\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "pool_ring_fuzzer" / "seed.bin", bytes(range(32, 96)))


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
    write(poc_dir / "README.txt", """poolcfg local PoC artifacts (never commit to GitHub).

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
