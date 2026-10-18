#!/usr/bin/env python3
"""Rename quorumcfg tree to holdcfg in place."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/quorumcfg")
ART = Path("/home/samuel/Documents/fenrir3/artifacts/quorumcfg")
TARGET = Path("/home/samuel/Documents/fenrir3/holdcfg")
ART_TARGET = Path("/home/samuel/Documents/fenrir3/artifacts/holdcfg")

PAIRS = [
    ("quorum_registry_fuzzer", "hold_registry_fuzzer"),
    ("quorum_renewal_fuzzer", "hold_renewal_fuzzer"),
    ("quorum_registry_finalize_digest", "hold_registry_finalize_digest"),
    ("quorum_registry_compact", "hold_registry_compact"),
    ("quorum_registry_register", "hold_registry_register"),
    ("quorum_registry_reset", "hold_registry_reset"),
    ("quorum_registry_init", "hold_registry_init"),
    ("quorum_registry_t", "hold_registry_t"),
    ("quorum_registry", "hold_registry"),
    ("quorum_renewal_tracker", "hold_renewal_tracker"),
    ("quorum_renewal_state", "hold_renewal_state"),
    ("quorum_renewal_", "hold_renewal_"),
    ("quorum_coordinator_", "hold_coordinator_"),
    ("quorum_coordinator_t", "hold_coordinator_t"),
    ("quorum_coordinator", "hold_coordinator"),
    ("quorum_member_t", "hold_member_t"),
    ("quorumcfg_validate_quorum_manifest", "holdcfg_validate_hold_manifest"),
    ("quorumcfg_apply_quorumenv_to_toml", "holdcfg_apply_holdenv_to_toml"),
    ("quorumcfg_load_quorumenv_memory", "holdcfg_load_holdenv_memory"),
    ("quorumcfg_load_toml_memory", "holdcfg_load_toml_memory"),
    ("quorumcfg_quorumenv_free", "holdcfg_holdenv_free"),
    ("quorumcfg_toml_free", "holdcfg_toml_free"),
    ("quorum_gate_allows", "hold_gate_allows"),
    ("quorum_gate", "hold_gate"),
    ("quorum_policy", "hold_policy"),
    ("quorum_fuzzer", "hold_fuzzer"),
    ("quorum_merge", "hold_merge"),
    ("quorumenv_doc_impl_t", "holdenv_doc_impl_t"),
    ("quorumenv_doc_t", "holdenv_doc_t"),
    ("quorumenv_", "holdenv_"),
    ("QUORUMENV_", "HOLDENV_"),
    ("Quorumenv", "Holdenv"),
    ("quorumenv", "holdenv"),
    ("quorumcfg", "holdcfg"),
    ("QuorumCfg", "HoldCfg"),
    ("QUORUMCFG", "HOLDCFG"),
    ("quorumloader", "holdloader"),
    ("quorummap", "holdmap"),
    ("@quorum", "@hold"),
    ("qenv_", "henv_"),
    ("quorum.runtime", "hold.runtime"),
    ("quorum.toml", "hold.toml"),
    ("/tmp/quorumcfg_out", "/tmp/holdcfg_out"),
    ("tolossamuel/quorumcfg", "tolossamuel/holdcfg"),
    ("compile_quorumenv", "compile_holdenv"),
    ("[quorum]", "[hold]"),
    ("heartbeat_ms", "renew_ms"),
    ("QUORUM_KEY", "HOLD_KEY"),
    (".qenv", ".henv"),
    ("QUORUM_MODE", "HOLD_MODE"),
    ("quorum_mode", "hold_mode"),
    ("distributed quorum coordination", "distributed resource hold coordination"),
    ("quorum coordination", "hold coordination"),
    ("quorum manifest", "hold manifest"),
    ("quorum member registry", "hold member registry"),
    ("quorum member", "hold member"),
    ("members", "holders"),
    ("member", "holder"),
    ("max_members", "max_holders"),
    ("MAX_MEMBERS", "MAX_HOLDERS"),
    ("quorum manifests", "hold manifests"),
    ("quorumenv runtime TTL", "holdenv runtime TTL"),
    ("bug1_quorumenv_entry_leak", "bug1_holdenv_entry_leak"),
    ("bug3_quorum_registry_uaf", "bug3_hold_registry_uaf"),
    ("quorumenv entry realloc leak", "holdenv entry realloc leak"),
    ("quorum registry member UAF", "hold registry holder UAF"),
    ("quorumenv assignment", "holdenv assignment"),
    ("quorumenv_set_entry", "holdenv_set_entry"),
    ("quorumenv_doc_destroy", "holdenv_doc_destroy"),
    ("src/quorumenv/", "src/holdenv/"),
    ("include/quorumenv/", "include/holdenv/"),
    ("include/quorumcfg/", "include/holdcfg/"),
    ("src/quorum_registry.c", "src/hold_registry.c"),
    ("src/quorum_renewal.c", "src/hold_renewal.c"),
    ("src/quorum_coordinator.c", "src/hold_coordinator.c"),
    ("src/quorum_policy.c", "src/hold_policy.c"),
    ("src/quorum_gate.c", "src/hold_gate.c"),
    ("src/quorumcfg.c", "src/holdcfg.c"),
    ("src/quorum_merge.c", "src/hold_merge.c"),
    ("test_quorum_", "test_hold_"),
    ("quorumenv_fuzzer", "holdenv_fuzzer"),
    ("quorum_required", "hold_required"),
    ("quorum arithmetic", "hold arithmetic"),
]


def xform(text: str) -> str:
    for old, new in PAIRS:
        text = text.replace(old, new)
    return text


def rename_paths(base: Path) -> None:
    for path in sorted([p for p in base.rglob("*")], key=lambda p: len(str(p)), reverse=True):
        new_name = xform(path.name)
        if new_name != path.name:
            target = path.with_name(new_name)
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            path.rename(target)


def rewrite_files(base: Path) -> None:
    for path in base.rglob("*"):
        if not path.is_file() or path.suffix == ".o":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = xform(text)
        if new != text:
            path.write_text(new, encoding="utf-8")


def main() -> None:
    if TARGET.exists():
        shutil.rmtree(TARGET)
    if ART_TARGET.exists():
        shutil.rmtree(ART_TARGET)
    shutil.move(ROOT, TARGET)
    if ART.exists():
        shutil.move(ART, ART_TARGET)
    rename_paths(TARGET)
    rename_paths(ART_TARGET)
    rewrite_files(TARGET)
    rewrite_files(ART_TARGET)
    # fix over-replace: hold_required field reading quorum table key
    for path in TARGET.rglob("*.c"):
        t = path.read_text(encoding="utf-8")
        t = t.replace('tome_table_get(doc->root, "hold")', 'tome_table_get(doc->root, "hold")')
        t = t.replace("holdcfg_validate_hold_hold_manifest", "holdcfg_validate_hold_manifest")
        t = t.replace("tome_table_get(tbl, \"hold\")", "tome_table_get(tbl, \"quorum\")")
        path.write_text(t, encoding="utf-8")
    print("holdcfg ready at", TARGET)


if __name__ == "__main__":
    main()
