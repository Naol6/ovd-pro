#!/usr/bin/env python3
"""Bootstrap synccfg — TOML distributed replication sync policy + syncenv runtime overlays."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/synccfg")
SRC = Path("/home/samuel/Documents/fenrir3/holdcfg")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/synccfg")

TEXT_RENAME = [
    ("hold_renewal_tracker_t", "sync_watermark_tracker_t"),
    ("hold_renewal_state_t", "sync_watermark_state_t"),
    ("hold_renewal_tracker", "sync_watermark_tracker"),
    ("hold_renewal_apply_jitter", "sync_watermark_apply_jitter"),
    ("hold_renewal_compute_backoff", "sync_watermark_compute_backoff"),
    ("hold_renewal_tick", "sync_watermark_tick"),
    ("hold_renewal_due_count", "sync_watermark_due_count"),
    ("hold_renewal_advance_epoch", "sync_watermark_advance_epoch"),
    ("hold_renewal_fuzzer", "sync_watermark_fuzzer"),
    ("hold_renewal.c", "sync_watermark.c"),
    ("hold_renewal.h", "sync_watermark.h"),
    ("hold_coordinator_t", "sync_coordinator_t"),
    ("hold_coordinator_init", "sync_coordinator_init"),
    ("hold_coordinator_reset", "sync_coordinator_reset"),
    ("hold_coordinator_load_manifest", "sync_coordinator_load_manifest"),
    ("hold_coordinator_register", "sync_coordinator_register"),
    ("hold_coordinator_tick", "sync_coordinator_tick"),
    ("hold_coordinator_finalize", "sync_coordinator_finalize"),
    ("hold_coordinator.c", "sync_coordinator.c"),
    ("hold_coordinator.h", "sync_coordinator.h"),
    ("hold_registry_finalize_digest", "sync_registry_finalize_digest"),
    ("hold_registry_compact", "sync_registry_compact"),
    ("hold_registry_register", "sync_registry_register"),
    ("hold_registry_reset", "sync_registry_reset"),
    ("hold_registry_init", "sync_registry_init"),
    ("hold_registry_fuzzer", "sync_registry_fuzzer"),
    ("hold_registry_t", "sync_registry_t"),
    ("hold_holder_t", "sync_replica_t"),
    ("hold_registry.c", "sync_registry.c"),
    ("hold_registry.h", "sync_registry.h"),
    ("hold_registry", "sync_registry"),
    ("hold_renewal", "sync_watermark"),
    ("hold_coordinator", "sync_coordinator"),
    ("holdcfg_validate_hold_manifest", "synccfg_validate_sync_manifest"),
    ("holdenv_doc_impl_t", "syncenv_doc_impl_t"),
    ("holdenv_doc_t", "syncenv_doc_t"),
    ("holdenv_error_t", "syncenv_error_t"),
    ("holdenv_options_t", "syncenv_options_t"),
    ("holdenv_entry_t", "syncenv_entry_t"),
    ("holdenv_slice_t", "syncenv_slice_t"),
    ("holdenv_arena_t", "syncenv_arena_t"),
    ("holdenv_token_kind_t", "syncenv_token_kind_t"),
    ("holdenv_token_t", "syncenv_token_t"),
    ("holdenv_internal.h", "syncenv_internal.h"),
    ("holdenv/holdenv_types.h", "syncenv/syncenv_types.h"),
    ("holdenv/holdenv.h", "syncenv/syncenv.h"),
    ("include/holdenv", "include/syncenv"),
    ("src/holdenv/", "src/syncenv/"),
    ("src/holdenv", "src/syncenv"),
    ("holdenv_", "syncenv_"),
    ("HOLDENV_", "SYNCENV_"),
    ("Holdenv", "Syncenv"),
    ("holdenv", "syncenv"),
    ("hold_merge", "sync_merge"),
    ("hold_fuzzer", "sync_fuzzer"),
    ("hold_policy", "sync_policy"),
    ("hold_gate", "sync_gate"),
    ("holdcfg", "synccfg"),
    ("HoldCfg", "SyncCfg"),
    ("HOLDCFG", "SYNCCFG"),
    ("renewal_stack", "chain_stack"),
    ("renewal_ctx", "chain_ctx"),
    ("@hold", "@sync"),
    ("holdmap", "syncmap"),
    ("holdloader", "syncloader"),
    ("apply_holdenv_overlay", "apply_syncenv_overlay"),
    ("apply_holdenv_to_toml", "apply_syncenv_to_toml"),
    ("load_holdenv_memory", "load_syncenv_memory"),
    ("synccfg_holdenv_free", "synccfg_syncenv_free"),
    ("/tmp/holdcfg_out", "/tmp/synccfg_out"),
    ("tolossamuel/holdcfg", "tolossamuel/synccfg"),
    ("compile_holdenv", "compile_syncenv"),
    ("henv_", "senv_"),
    ("hold.runtime", "sync.runtime"),
    ("hold.toml", "sync.toml"),
    (".henv", ".senv"),
    ("[hold]", "[sync]"),
    ("hold registry", "sync registry"),
    ("Hold registry", "Sync registry"),
    ("distributed resource hold coordination", "distributed database replication sync policy"),
    ("Distributed resource hold coordination", "Distributed database replication sync policy"),
    ("hold manifests", "sync policy manifests"),
    ("Hold manifests", "Sync policy manifests"),
    ("TTL and renewal parameter overlays", "replication lag and watermark parameter overlays"),
    ("holder TTL budgets", "replica lag budgets"),
    ("hold member registry", "replica sync registry"),
    ("multi-stage coordination", "multi-replica replication sync"),
    ("Hold policy", "Sync policy"),
    ("hold policy", "sync policy"),
    ("hold admission", "sync admission"),
    ("Hold admission", "Sync admission"),
    ("max_holders", "max_replicas"),
    ("renew_ms", "watermark_ms"),
    ("hold_mode", "sync_mode"),
    ("holders", "replicas"),
    ("holder", "replica"),
    ("ttl_ms", "lag_ms"),
    ("HOLD_KEY", "SYNC_KEY"),
    ("HOLD_MODE", "SYNC_MODE"),
    ("quorum_service.h", "sync_service.h"),
    ("Quorum", "Coordinator"),
    ("quorum", "coordinator"),
]

EXCLUDE = {".git", "poc", "guides", "__pycache__"}
SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}
SKIP_SUFFIX = {".o"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add synccfg public headers", [
        "include/synccfg/synccfg.h", "include/synccfg/sync_merge.h"]),
    ("include: add syncenv public API", [
        "include/syncenv/syncenv.h", "include/syncenv/syncenv_types.h"]),
    ("include: add tome public headers", [
        "include/tome/tome.h", "include/tome/buffer.h", "include/tome/value.h",
        "include/tome/lexer.h", "include/tome/parser.h", "include/tome/format.h",
        "include/tome/memory.h", "include/tome/unicode.h", "include/tome/datetime.h",
        "include/tome/diag.h", "include/tome/document.h", "include/tome/validator.h"]),
    ("include: add sync policy gate registry headers", [
        "include/synccfg/sync_policy.h", "include/synccfg/sync_gate.h",
        "include/synccfg/sync_registry.h", "include/synccfg/sync_watermark.h",
        "include/synccfg/sync_coordinator.h"]),
    ("src/syncenv: add buffer and string utilities", [
        "src/syncenv/buffer.c", "src/syncenv/buffer.h", "src/syncenv/strutil.c",
        "src/syncenv/strutil.h"]),
    ("src/syncenv: add arena allocator", [
        "src/syncenv/arena.c", "src/syncenv/arena.h", "src/syncenv/syncenv_internal.h"]),
    ("src/syncenv: add error helpers", ["src/syncenv/error.c", "src/syncenv/error.h"]),
    ("src/syncenv: add UTF-8 validation", ["src/syncenv/utf8.c", "src/syncenv/utf8.h"]),
    ("src/syncenv: implement syncenv line lexer", ["src/syncenv/lexer.c", "src/syncenv/lexer.h"]),
    ("src/syncenv: add quoted value unescape", ["src/syncenv/unescape.c", "src/syncenv/unescape.h"]),
    ("src/syncenv: add document store", ["src/syncenv/store.c", "src/syncenv/store.h"]),
    ("src/syncenv: wire assignment parser", ["src/syncenv/parser.c", "src/syncenv/parser.h"]),
    ("src/syncenv: add serialize to syncenv text", ["src/syncenv/serialize.c", "src/syncenv/serialize.h"]),
    ("src/syncenv: add validation pass", ["src/syncenv/validate.c", "src/syncenv/validate.h"]),
    ("src/syncenv: add merge overlay", ["src/syncenv/merge.c", "src/syncenv/merge.h"]),
    ("src/syncenv: add expand and coerce", [
        "src/syncenv/expand.c", "src/syncenv/expand.h", "src/syncenv/coerce.c",
        "src/syncenv/coerce.h"]),
    ("src/syncenv: add walk query diff", [
        "src/syncenv/walk.c", "src/syncenv/walk.h", "src/syncenv/query.c",
        "src/syncenv/query.h", "src/syncenv/diff.c", "src/syncenv/diff.h"]),
    ("src/syncenv: add pretty printer", ["src/syncenv/pretty.c", "src/syncenv/pretty.h"]),
    ("src/syncenv: add chain stack and ctx", [
        "src/syncenv/chain_stack.c", "src/syncenv/chain_stack.h",
        "src/syncenv/chain_ctx.c", "src/syncenv/chain_ctx.h"]),
    ("src/syncenv: add path filter profile", [
        "src/syncenv/path.c", "src/syncenv/path.h", "src/syncenv/filter.c",
        "src/syncenv/filter.h", "src/syncenv/profile.c", "src/syncenv/profile.h"]),
    ("src/syncenv: add snapshot readutil strict canonical", [
        "src/syncenv/snapshot.c", "src/syncenv/snapshot.h", "src/syncenv/readutil.c",
        "src/syncenv/readutil.h", "src/syncenv/strict.c", "src/syncenv/strict.h",
        "src/syncenv/canonical.c", "src/syncenv/canonical.h"]),
    ("src/syncenv: add syncloader and main syncenv module", [
        "src/syncenv/syncloader.c", "src/syncenv/syncenv.c", "src/syncenv/syncmap.c",
        "src/syncenv/syncmap.h"]),
    ("src/toml: add memory and buffer modules", ["src/toml/memory.c", "src/toml/buffer.c"]),
    ("src/toml: add unicode datetime lexer", [
        "src/toml/unicode.c", "src/toml/datetime.c", "src/toml/lexer.c"]),
    ("src/toml: add value and parser core", ["src/toml/value.c", "src/toml/parser.c"]),
    ("src/toml: add path merge serialize", [
        "src/toml/path.c", "src/toml/merge.c", "src/toml/serialize.c"]),
    ("src/toml: add diag format validator document", [
        "src/toml/diag.c", "src/toml/format.c", "src/toml/validator.c", "src/toml/document.c"]),
    ("src: add synccfg bridge and syncenv-to-toml merge", ["src/synccfg.c", "src/sync_merge.c"]),
    ("src: add sync policy validator", ["src/sync_policy.c"]),
    ("src: add replication gate evaluator", ["src/sync_gate.c"]),
    ("src: add replica sync registry with compaction", ["src/sync_registry.c"]),
    ("src: add sync watermark tracker with jitter", ["src/sync_watermark.c"]),
    ("src: add replication sync coordinator", ["src/sync_coordinator.c"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add sync policy registry watermark unit tests", [
        "tests/test_sync_policy.c", "tests/test_sync_registry.c", "tests/test_sync_watermark.c"]),
    ("examples: add TOML sync manifest and runtime overlay", [
        "examples/sync.toml", "examples/sync.runtime"]),
    ("fuzz: add syncenv_fuzzer harness", ["fuzz/syncenv_fuzzer.c"]),
    ("fuzz: add toml_fuzzer harness", ["fuzz/toml_fuzzer.c"]),
    ("fuzz: add toml_merge_fuzzer harness", ["fuzz/toml_merge_fuzzer.c"]),
    ("fuzz: add toml_format_fuzzer harness", ["fuzz/toml_format_fuzzer.c"]),
    ("fuzz: add sync_fuzzer for cross-format overlay", ["fuzz/sync_fuzzer.c"]),
    ("fuzz: add sync_registry_fuzzer for replica compaction path", ["fuzz/sync_registry_fuzzer.c"]),
    ("fuzz: add sync_watermark_fuzzer for coordinator tick paths", ["fuzz/sync_watermark_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/syncenv_fuzzer/minimal.senv",
        "fuzz/corpus/syncenv_fuzzer/quoted.senv",
        "fuzz/corpus/toml_fuzzer/basic.toml",
        "fuzz/corpus/toml_merge_fuzzer/base.toml",
        "fuzz/corpus/toml_format_fuzzer/empty.toml",
        "fuzz/corpus/sync_fuzzer/sample.bin",
        "fuzz/corpus/sync_registry_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for synccfg library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable replication sync policy library", []),
]

README = """# synccfg

synccfg is a C11 library for distributed database replication sync policy configuration: parse TOML sync manifests, load syncenv runtime lag and watermark parameter overlays, merge layers, validate replica lag budgets, and track replica sync registry during multi-replica replication sync.

## Features

- **TOML manifest layer** — tables, arrays, merge, format, validate (tome toolkit)
- **Syncenv layer** — `KEY=VALUE`, `@sync` includes, `${VAR}` expansion, quoted escapes
- **Bridge** — apply syncenv overlay keys onto parsed TOML documents
- **Sync policy** — validate `[sync]` tables and register replica slots into a compaction registry
- **Replication gate** — gate sync admission on coordinator state and replica capacity
- **Watermark tracker** — epoch-aware replication watermark scheduling with jitter and backoff
- ClusterFuzzLite harnesses for each entry point

## Build

```bash
bash build/wsl_build.sh
make test
```

Fuzz targets: `syncenv_fuzzer`, `toml_fuzzer`, `toml_merge_fuzzer`, `toml_format_fuzzer`, `sync_fuzzer`, `sync_registry_fuzzer`, `sync_watermark_fuzzer`.

## Quick start

```c
#include "synccfg/synccfg.h"

TomeDoc *toml = NULL;
TomeError err;
synccfg_load_toml_memory("[sync]\\nname = \\"primary-shard\\"\\nmax_replicas = 3\\n", 45, &toml, &err);

syncenv_doc_t *env = NULL;
synccfg_load_syncenv_memory("MAX_REPLICAS=5\\n", 15, NULL, &env, NULL);
synccfg_apply_syncenv_to_toml(toml, env);

synccfg_syncenv_free(env);
synccfg_toml_free(toml);
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
        (ROOT / "include" / "holdcfg", ROOT / "include" / "synccfg"),
        (ROOT / "include" / "holdenv", ROOT / "include" / "syncenv"),
        (ROOT / "src" / "holdenv", ROOT / "src" / "syncenv"),
        (ROOT / "src" / "holdcfg.c", ROOT / "src" / "synccfg.c"),
        (ROOT / "src" / "hold_merge.c", ROOT / "src" / "sync_merge.c"),
        (ROOT / "src" / "hold_policy.c", ROOT / "src" / "sync_policy.c"),
        (ROOT / "src" / "hold_gate.c", ROOT / "src" / "sync_gate.c"),
        (ROOT / "src" / "hold_registry.c", ROOT / "src" / "sync_registry.c"),
        (ROOT / "src" / "hold_renewal.c", ROOT / "src" / "sync_watermark.c"),
        (ROOT / "src" / "hold_coordinator.c", ROOT / "src" / "sync_coordinator.c"),
        (ROOT / "fuzz" / "holdenv_fuzzer.c", ROOT / "fuzz" / "syncenv_fuzzer.c"),
        (ROOT / "fuzz" / "hold_fuzzer.c", ROOT / "fuzz" / "sync_fuzzer.c"),
        (ROOT / "fuzz" / "hold_registry_fuzzer.c", ROOT / "fuzz" / "sync_registry_fuzzer.c"),
        (ROOT / "fuzz" / "hold_renewal_fuzzer.c", ROOT / "fuzz" / "sync_watermark_fuzzer.c"),
        (ROOT / "examples" / "hold.toml", ROOT / "examples" / "sync.toml"),
        (ROOT / "examples" / "hold.runtime", ROOT / "examples" / "sync.runtime"),
        (ROOT / "fuzz" / "corpus" / "holdenv_fuzzer", ROOT / "fuzz" / "corpus" / "syncenv_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "hold_fuzzer", ROOT / "fuzz" / "corpus" / "sync_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "hold_registry_fuzzer", ROOT / "fuzz" / "corpus" / "sync_registry_fuzzer"),
        (ROOT / "fuzz" / "corpus" / "hold_renewal_fuzzer", ROOT / "fuzz" / "corpus" / "sync_watermark_fuzzer"),
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

    for p in list((ROOT / "include" / "syncenv").glob("*")):
        if "holdenv" in p.name:
            p.rename(p.with_name(p.name.replace("holdenv", "syncenv")))

    for p in list((ROOT / "src" / "syncenv").glob("*")):
        new_name = p.name
        for a, b in [
            ("holdenv", "syncenv"),
            ("holdloader", "syncloader"),
            ("renewal_stack", "chain_stack"),
            ("renewal_ctx", "chain_ctx"),
            ("holdmap", "syncmap"),
        ]:
            new_name = new_name.replace(a, b)
        if new_name != p.name:
            p.rename(p.with_name(new_name))

    synccfg_inc = ROOT / "include" / "synccfg"
    for old, new in [
        ("hold_renewal.h", "sync_watermark.h"),
        ("quorum_service.h", "sync_service.h"),
    ]:
        src = synccfg_inc / old
        if src.exists():
            src.rename(synccfg_inc / new)

    for p in list(synccfg_inc.glob("*")):
        if "hold" in p.name:
            p.rename(p.with_name(p.name.replace("hold", "sync")))

    renewal_test = ROOT / "tests" / "test_hold_renewal.c"
    if renewal_test.exists():
        renewal_test.rename(ROOT / "tests" / "test_sync_watermark.c")

    for p in list((ROOT / "tests").glob("test_hold*.c")):
        p.rename(p.with_name(p.name.replace("hold", "sync")))

    corp = ROOT / "fuzz" / "corpus" / "syncenv_fuzzer"
    if corp.exists():
        for old in list(corp.glob("*.henv")):
            old.rename(old.with_suffix(".senv"))


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
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".senv", ".henv",
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


def strip_fuzzer_extern_c() -> None:
    for path in (ROOT / "fuzz").glob("*.c"):
        text = path.read_text(encoding="utf-8")
        text = text.replace('extern "C" int LLVMFuzzerTestOneInput', "int LLVMFuzzerTestOneInput")
        path.write_text(text, encoding="utf-8")


def patch_domain() -> None:
    write(ROOT / "README.md", README)

    write(ROOT / "examples" / "sync.toml", """[sync]
name = "primary-shard"
max_replicas = 3
watermark_ms = 60000
sync_mode = "streaming"

[[sync.replicas]]
replica = "node-a"
lag_ms = 120

[[sync.replicas]]
replica = "node-b"
lag_ms = 80

[[sync.replicas]]
replica = "node-c"
lag_ms = 40
""")

    write(ROOT / "examples" / "sync.runtime", """# Runtime replication sync tuning injected during watermark advance
MAX_REPLICAS=5
WATERMARK_MS=150
SYNC_MODE=active
""")

    sync_fuzz = (ROOT / "fuzz" / "sync_fuzzer.c").read_text(encoding="utf-8")
    sync_fuzz = re.sub(
        r'#include "synccfg/sync_policy\.h"\n#include "synccfg/sync_registry\.h"\n'
        r'#include "synccfg/sync_policy\.h"\n#include "synccfg/sync_registry\.h"\n',
        '#include "synccfg/sync_policy.h"\n#include "synccfg/sync_registry.h"\n',
        sync_fuzz,
    )
    sync_fuzz = re.sub(
        r'if \(toml && env\) \{\n'
        r'    synccfg_apply_syncenv_to_toml\(toml, env\);\n'
        r'  if \(toml\) \{[^}]+\}\n'
        r'  if \(toml\) \{[^}]+\}\n'
        r'  \}',
        'if (toml && env) {\n'
        '    synccfg_apply_syncenv_to_toml(toml, env);\n'
        '  }\n'
        '  if (toml) {\n'
        '    sync_registry_t trk;\n'
        '    sync_registry_init(&trk);\n'
        '    synccfg_validate_sync_manifest(toml, &trk);\n'
        '    (void)sync_registry_finalize_digest(&trk);\n'
        '    sync_registry_reset(&trk);\n'
        '  }',
        sync_fuzz,
        flags=re.DOTALL,
    )
    write(ROOT / "fuzz" / "sync_fuzzer.c", sync_fuzz)

    reg_fuzz = (ROOT / "fuzz" / "sync_registry_fuzzer.c").read_text(encoding="utf-8")
    reg_fuzz = reg_fuzz.replace("hold_registry", "sync_registry")
    reg_fuzz = reg_fuzz.replace("synccfg/hold_registry.h", "synccfg/sync_registry.h")
    write(ROOT / "fuzz" / "sync_registry_fuzzer.c", reg_fuzz)


def plant_bugs() -> None:
    """Plant standard 5-bug set; bug1 syncenv store leak left unfixed; bug3 emergent registry UAF."""
    unesc = (ROOT / "src" / "syncenv" / "unescape.c").read_text(encoding="utf-8")
    unesc = unesc.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "syncenv" / "unescape.c").write_text(unesc, encoding="utf-8")

    fmt = (ROOT / "src" / "toml" / "format.c").read_text(encoding="utf-8")
    if "ctx.out.length == 0 && ctx.out.data == NULL" not in fmt:
        fmt = fmt.replace(
            "    if (!ctx.opts.trailing_newline && ctx.out.length > 0",
            "    if (ctx.out.length == 0 && ctx.out.data == NULL) {\n"
            "        char *snapshot = tome_alloc(1);\n"
            "        if (snapshot != NULL) {\n"
            "            memcpy(snapshot, ctx.out.data, ctx.out.length + 1);\n"
            "            tome_free_ptr(snapshot);\n"
            "        }\n"
            "    }\n"
            "    if (!ctx.opts.trailing_newline && ctx.out.length > 0",
        )
    (ROOT / "src" / "toml" / "format.c").write_text(fmt, encoding="utf-8")

    merge = (ROOT / "src" / "toml" / "merge.c").read_text(encoding="utf-8")
    if "overlay_mut" not in merge:
        merge = merge.replace(
            "static int merge_table_in_place(MergeContext *ctx, TomeTable *dest, const TomeTable *overlay) {\n    size_t i;",
            "static int merge_table_in_place(MergeContext *ctx, TomeTable *dest, const TomeTable *overlay) {\n    size_t i;\n    TomeTable *overlay_mut = (TomeTable *)overlay;",
        )
        merge = merge.replace(
            "        const TomeEntry *overlay_entry = &overlay->entries[i];\n        TomeValue *existing",
            "        const TomeEntry *overlay_entry = &overlay->entries[i];\n        const char *cached_key = overlay_entry->key;\n        TomeValue *existing",
        )
        merge = merge.replace(
            "        if (!path_push_key(ctx, overlay_entry->key, &restore_len)) {",
            "        if (i > 0 && overlay->count > 3 && (i % 2) == 0) {\n            tome_table_rebuild_index(overlay_mut);\n        }\n\n        if (!path_push_key(ctx, cached_key, &restore_len)) {",
        )
    (ROOT / "src" / "toml" / "merge.c").write_text(merge, encoding="utf-8")


def patch_build() -> None:
    build_sh = (ROOT / ".clusterfuzzlite" / "build.sh").read_text(encoding="utf-8")
    build_sh = xform(build_sh)
    build_sh = build_sh.replace(
        "for f in holdcfg hold_merge hold_policy hold_gate hold_registry hold_renewal hold_coordinator; do",
        "for f in synccfg sync_merge sync_policy sync_gate sync_registry sync_watermark sync_coordinator; do",
    )
    build_sh = build_sh.replace("compile_holdenv", "compile_syncenv")
    build_sh = build_sh.replace("src/holdenv/", "src/syncenv/")
    build_sh = build_sh.replace("henv_", "senv_")
    build_sh = build_sh.replace("renewal_stack", "chain_stack")
    build_sh = build_sh.replace("renewal_ctx", "chain_ctx")
    build_sh = build_sh.replace("holdmap", "syncmap")
    build_sh = build_sh.replace("holdloader", "syncloader")
    build_sh = build_sh.replace("build_fuzzer holdenv_fuzzer.c holdenv_fuzzer",
                               "build_fuzzer syncenv_fuzzer.c syncenv_fuzzer")
    build_sh = build_sh.replace("build_fuzzer hold_fuzzer.c hold_fuzzer",
                               "build_fuzzer sync_fuzzer.c sync_fuzzer")
    build_sh = build_sh.replace(
        "build_fuzzer hold_registry_fuzzer.c hold_registry_fuzzer",
        "build_fuzzer sync_registry_fuzzer.c sync_registry_fuzzer\n"
        "build_fuzzer sync_watermark_fuzzer.c sync_watermark_fuzzer",
    )
    build_sh = build_sh.replace("build_fuzzer hold_renewal_fuzzer.c hold_renewal_fuzzer", "")
    build_sh = re.sub(
        r'FUZZ_CXXFLAGS="\$\{CXXFLAGS:-[^"]+\}"',
        'FUZZ_CFLAGS="${CFLAGS:- -O1 -g -std=c11 -Wall -fsanitize=fuzzer,address}"',
        build_sh,
    )
    build_sh = build_sh.replace(
        "${CXX:-clang++} ${FUZZ_CXXFLAGS} ${LIB_FUZZING_ENGINE}",
        "${CC:-clang} ${FUZZ_CFLAGS}",
    )
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build_sh, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    wsl = re.sub(
        r"rm -f .*",
        "rm -f senv_*.o toml_*.o synccfg.o sync_merge.o sync_policy.o sync_gate.o "
        "sync_registry.o sync_watermark.o sync_coordinator.o",
        wsl,
    )
    wsl = re.sub(r"export CXX=clang\+\+\n", "", wsl)
    wsl = re.sub(r'export CXXFLAGS="[^"]*"\n', "", wsl)
    wsl = re.sub(r"export LIB_FUZZING_ENGINE=.*\n", "", wsl)
    wsl = re.sub(
        r'export CFLAGS="[^"]*"',
        'export CFLAGS="-O1 -g -std=c11 -Wall -D_GNU_SOURCE -fsanitize=fuzzer,address"',
        wsl,
    )
    (ROOT / "build" / "wsl_build.sh").write_text(wsl, encoding="utf-8")

    proj = (ROOT / ".clusterfuzzlite" / "project.yaml").read_text(encoding="utf-8")
    proj = xform(proj)
    proj = proj.replace("language: c++", "language: c")
    proj = proj.replace("hold_renewal_fuzzer", "sync_watermark_fuzzer")
    (ROOT / ".clusterfuzzlite" / "project.yaml").write_text(proj, encoding="utf-8")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").exists() else ""
    for line in ["/poc/", "crash-*", "*.o", "/tmp/", "/guides/"]:
        if line.strip() not in gitignore:
            gitignore += f"\n{line}\n"
    (ROOT / ".gitignore").write_text(gitignore, encoding="utf-8")

    write(ROOT / "fuzz" / "corpus" / "sync_fuzzer" / "sample.bin",
          bytes([32]) + b"[sync]\nname=\"shard\"\nwatermark_ms=100\n" + b"K=1\n")
    write(ROOT / "fuzz" / "corpus" / "sync_registry_fuzzer" / "seed.bin", bytes(range(32, 96)))

    strip_fuzzer_extern_c()


def write_artifacts() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    tasks = """# synccfg task queue

GitHub: tolossamuel/synccfg

| # | Bug | Harness | Class | Status |
|---|-----|---------|-------|--------|
| 1 | syncenv entry realloc leak | syncenv_fuzzer | LeakSanitizer | Ready |
| 2 | toml audit key leak | toml_fuzzer | LeakSanitizer | Ready |
| 3 | sync registry replica UAF | sync_registry_fuzzer | heap-use-after-free | Ready |
| 4 | toml merge UAF | toml_merge_fuzzer | heap-use-after-free | Ready |
| 5 | toml format null deref | toml_format_fuzzer | null deref | Ready |

PoC bytes and patches: ../artifacts/synccfg/poc/ (not on GitHub).
"""
    write(ARTIFACTS / "TASKS.md", tasks)

    wsl_test = '''#!/bin/bash
set -eu
cd "$(dirname "$0")/../../synccfg"
ROOT="$PWD"
ARTIFACTS_ROOT="${ARTIFACTS_ROOT:-$(dirname "$ROOT")/artifacts/synccfg}"
POC="$ARTIFACTS_ROOT/poc/verified"
OUT=/tmp/synccfg_out
FAIL=0

if [ ! -d "$POC" ]; then
  echo "Missing PoC corpus: $POC" >&2
  exit 1
fi

if [ ! -x "$OUT/syncenv_fuzzer" ]; then
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

run_leak "Bug1 syncenv entry leak" "$OUT/syncenv_fuzzer" "$POC/entry_leak.senv"
run_leak "Bug2 toml audit leak" "$OUT/toml_fuzzer" "$POC/entry_leak.toml"
run_crash "Bug3 sync registry UAF" "$OUT/sync_registry_fuzzer" "$POC/registry_uaf.bin"
run_crash "Bug4 toml merge UAF" "$OUT/toml_merge_fuzzer" "$POC/merge_uaf.bin"
run_crash "Bug5 toml format null" "$OUT/toml_format_fuzzer" "$POC/empty_format.bin"
exit $FAIL
'''
    write(ARTIFACTS / "wsl_test_pocs.sh", wsl_test)
    (ARTIFACTS / "wsl_test_pocs.sh").chmod(0o755)


def generate_pocs_and_patches() -> None:
    """Build, capture golden PoCs, and emit git patches into artifacts/."""
    poc_dir = ARTIFACTS / "poc" / "verified"
    submit_dir = ARTIFACTS / "poc" / "submit"
    poc_dir.mkdir(parents=True, exist_ok=True)
    submit_dir.mkdir(parents=True, exist_ok=True)

    subprocess.check_call(["bash", "build/wsl_build.sh"], cwd=ROOT)
    out = Path("/tmp/synccfg_out")

    write(poc_dir / "entry_leak.senv", "SYNC_KEY=1\n")
    write(poc_dir / "entry_leak.toml", 'k = "v"\n')
    write(poc_dir / "empty_format.bin", b"")
    shutil.copy2(
        Path("/home/samuel/Documents/fenrir3/artifacts/throttlecfg/poc/verified/merge_uaf.bin"),
        poc_dir / "merge_uaf.bin",
    )
    shutil.copy2(
        Path("/home/samuel/Documents/fenrir3/artifacts/throttlecfg/poc/verified/tracker_uaf.bin"),
        poc_dir / "registry_uaf.bin",
    )

    patches = [
        ("bug1_syncenv_entry_leak.patch", "src/syncenv/store.c",
         lambda t: t.replace(
             "  syncenv_doc_impl_t *d = (syncenv_doc_impl_t *)doc;\n  syncenv_arena_free",
             "  syncenv_doc_impl_t *d = (syncenv_doc_impl_t *)doc;\n  free(d->entries);\n  syncenv_arena_free",
         )),
        ("bug2_toml_audit_leak.patch", "src/toml/parser.c",
         lambda t: t.replace(
             """void tome_free(TomeDoc *doc) {
    if (doc == NULL) {
        return;
    }
    tome_table_free(doc->root);
    tome_free_ptr(doc);
}""",
             """void tome_free(TomeDoc *doc) {
    size_t i;
    if (doc == NULL) {
        return;
    }
    for (i = 0; i < doc->audit_count; i++) {
        tome_free_ptr(doc->audit_keys[i]);
    }
    tome_free_ptr(doc->audit_keys);
    tome_table_free(doc->root);
    tome_free_ptr(doc);
}""",
         )),
        ("bug3_sync_registry_uaf.patch", "src/sync_registry.c",
         lambda t: t.replace(
             "  free(t->slots);\n  free(t->pending_refs);",
             "  free(t->slots);\n  for (i = 0; i < t->pending_count; i++) {\n    free((void *)t->pending_refs[i]);\n  }\n  free(t->pending_refs);",
         ).replace(
             "        t->pending_refs[t->pending_count++] = t->slots[i].label;",
             "        char *snap = strdup(t->slots[i].label ? t->slots[i].label : \"\");\n        if (!snap) {\n          return -1;\n        }\n        t->pending_refs[t->pending_count++] = snap;",
         )),
        ("bug4_toml_merge_uaf.patch", "src/toml/merge.c",
         lambda t: t.replace(
             "    TomeTable *overlay_mut = (TomeTable *)overlay;",
             "    (void)overlay;",
         ).replace(
             "        if (i > 0 && overlay->count > 3 && (i % 2) == 0) {\n            tome_table_rebuild_index(overlay_mut);\n        }\n\n        ",
             "        ",
         ).replace(
             "        const TomeEntry *overlay_entry = &overlay->entries[i];\n        const char *cached_key = overlay_entry->key;\n        TomeValue *existing",
             "        const TomeEntry *overlay_entry = &overlay->entries[i];\n        TomeValue *existing",
         ).replace(
             "        if (!path_push_key(ctx, cached_key, &restore_len)) {",
             "        if (!path_push_key(ctx, overlay_entry->key, &restore_len)) {",
         )),
        ("bug5_toml_format_null_deref.patch", "src/toml/format.c",
         lambda t: t.replace(
             "    if (ctx.out.length == 0 && ctx.out.data == NULL) {\n        char *snapshot = tome_alloc(1);\n        if (snapshot != NULL) {\n            memcpy(snapshot, ctx.out.data, ctx.out.length + 1);\n            tome_free_ptr(snapshot);\n        }\n    }\n    ",
             "",
         )),
    ]

    for patch_name, rel_path, fix_fn in patches:
        path = ROOT / rel_path
        original = path.read_text(encoding="utf-8")
        fixed = fix_fn(original)
        if fixed == original:
            print(f"WARN: no change for {patch_name}")
        path.write_text(fixed, encoding="utf-8")
        diff = subprocess.check_output(
            ["git", "diff", rel_path], cwd=ROOT, text=True
        )
        (submit_dir / patch_name).write_text(diff, encoding="utf-8")
        path.write_text(original, encoding="utf-8")

    descriptions = {
        "bug1_TASK_DESCRIPTION.txt": (
            "A memory leak occurs when parsing a syncenv assignment: syncenv_set_entry "
            "reallocates internal entry storage, but that heap memory is not freed when "
            "syncenv_doc_destroy runs in src/syncenv/store.c."
        ),
        "bug2_TASK_DESCRIPTION.txt": (
            "A memory leak occurs in tome_free in src/toml/parser.c when TOML parsing records "
            "table-header audit keys: doc_audit_key heap-allocates key copies that are never "
            "released when the document is destroyed."
        ),
        "bug3_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in sync_registry_finalize_digest in src/sync_registry.c "
            "when FNV digest finalization reads replica label bytes through pending references "
            "registered before sync_registry_compact reallocates and frees the original label "
            "storage during multi-replica registration in the sync registry pipeline, triggered "
            "via sync_registry_fuzzer."
        ),
        "bug4_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in merge_table_in_place in src/toml/merge.c when overlay "
            "table index rebuild invalidates cached entry key pointers during multi-table TOML "
            "document merge, triggered via toml_merge_fuzzer."
        ),
        "bug5_TASK_DESCRIPTION.txt": (
            "A null pointer dereference occurs in tome_format_document in src/toml/format.c when "
            "formatting an empty document causes memcpy to read through a NULL output buffer, "
            "triggered via toml_format_fuzzer."
        ),
    }
    for name, text in descriptions.items():
        write(submit_dir / name, text + "\n")

    subprocess.check_call(["bash", str(ARTIFACTS / "wsl_test_pocs.sh")])


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


def main() -> None:
    copy_tree()
    transform_contents()
    patch_domain()
    plant_bugs()
    patch_build()
    write_artifacts()
    init_git()
    generate_pocs_and_patches()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
