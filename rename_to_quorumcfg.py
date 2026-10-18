#!/usr/bin/env python3
"""Rename leasecfg tree to quorumcfg in place."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/quorumcfg")
ART = Path("/home/samuel/Documents/fenrir3/artifacts/quorumcfg")

PAIRS = [
    ("lease_registry_fuzzer", "quorum_registry_fuzzer"),
    ("lease_renewal_fuzzer", "quorum_renewal_fuzzer"),
    ("lease_registry_finalize_digest", "quorum_registry_finalize_digest"),
    ("lease_registry_compact", "quorum_registry_compact"),
    ("lease_registry_register", "quorum_registry_register"),
    ("lease_registry_reset", "quorum_registry_reset"),
    ("lease_registry_init", "quorum_registry_init"),
    ("lease_registry_t", "quorum_registry_t"),
    ("lease_registry", "quorum_registry"),
    ("lease_renewal_tracker", "quorum_renewal_tracker"),
    ("lease_renewal_state", "quorum_renewal_state"),
    ("lease_renewal_", "quorum_renewal_"),
    ("lease_coordinator_", "quorum_coordinator_"),
    ("lease_coordinator_t", "quorum_coordinator_t"),
    ("lease_coordinator", "quorum_coordinator"),
    ("lease_holder_t", "quorum_member_t"),
    ("leasecfg_validate_lease_manifest", "quorumcfg_validate_quorum_manifest"),
    ("leasecfg_apply_leaseenv_to_toml", "quorumcfg_apply_quorumenv_to_toml"),
    ("leasecfg_load_leaseenv_memory", "quorumcfg_load_quorumenv_memory"),
    ("leasecfg_load_toml_memory", "quorumcfg_load_toml_memory"),
    ("leasecfg_leaseenv_free", "quorumcfg_quorumenv_free"),
    ("leasecfg_toml_free", "quorumcfg_toml_free"),
    ("lease_gate_allows", "quorum_gate_allows"),
    ("lease_gate", "quorum_gate"),
    ("lease_policy", "quorum_policy"),
    ("lease_fuzzer", "quorum_fuzzer"),
    ("lease_merge", "quorum_merge"),
    ("leaseenv_doc_impl_t", "quorumenv_doc_impl_t"),
    ("leaseenv_doc_t", "quorumenv_doc_t"),
    ("leaseenv_", "quorumenv_"),
    ("LEASEENV_", "QUORUMENV_"),
    ("Leaseenv", "Quorumenv"),
    ("leaseenv", "quorumenv"),
    ("leasecfg", "quorumcfg"),
    ("LeaseCfg", "QuorumCfg"),
    ("LEASECFG", "QUORUMCFG"),
    ("leaseloader", "quorumloader"),
    ("leasemap", "quorummap"),
    ("@lease", "@quorum"),
    ("lenv_", "qenv_"),
    ("lease.runtime", "quorum.runtime"),
    ("lease.toml", "quorum.toml"),
    ("/tmp/leasecfg_out", "/tmp/quorumcfg_out"),
    ("tolossamuel/leasecfg", "tolossamuel/quorumcfg"),
    ("compile_leaseenv", "compile_quorumenv"),
    ("[lease]", "[quorum]"),
    ("renew_interval_ms", "heartbeat_ms"),
    ("LEASE_KEY", "QUORUM_KEY"),
    (".lenv", ".qenv"),
    ("LEASE_MODE", "QUORUM_MODE"),
    ("lease_mode", "quorum_mode"),
    ("distributed lease coordination", "distributed quorum coordination"),
    ("lease coordination", "quorum coordination"),
    ("lease manifest", "quorum manifest"),
    ("lease holder registry", "quorum member registry"),
    ("lease registry pipeline", "quorum member registry pipeline"),
    ("lease holder", "quorum member"),
    ("holders", "members"),
    ("holder", "member"),
    ("max_holders", "max_members"),
    ("MAX_HOLDERS", "MAX_MEMBERS"),
    ("lease renewal", "quorum heartbeat"),
    ("lease manifests", "quorum manifests"),
    ("leaseenv runtime TTL", "quorumenv runtime TTL"),
    ("bug1_leaseenv_entry_leak", "bug1_quorumenv_entry_leak"),
    ("bug3_lease_registry_uaf", "bug3_quorum_registry_uaf"),
    ("leaseenv entry realloc leak", "quorumenv entry realloc leak"),
    ("lease registry holder UAF", "quorum registry member UAF"),
    ("leaseenv assignment", "quorumenv assignment"),
    ("leaseenv_set_entry", "quorumenv_set_entry"),
    ("leaseenv_doc_destroy", "quorumenv_doc_destroy"),
    ("src/leaseenv/", "src/quorumenv/"),
    ("src/lease_registry.c", "src/quorum_registry.c"),
    ("src/lease_renewal.c", "src/quorum_renewal.c"),
    ("src/lease_coordinator.c", "src/quorum_coordinator.c"),
    ("src/lease_policy.c", "src/quorum_policy.c"),
    ("src/lease_gate.c", "src/quorum_gate.c"),
    ("src/leasecfg.c", "src/quorumcfg.c"),
    ("src/lease_merge.c", "src/quorum_merge.c"),
    ("include/leasecfg/", "include/quorumcfg/"),
    ("include/leaseenv/", "include/quorumenv/"),
    ("test_lease_", "test_quorum_"),
    ("leaseenv_fuzzer", "quorumenv_fuzzer"),
]


def xform(text: str) -> str:
    for old, new in PAIRS:
        text = text.replace(old, new)
    return text


def rename_paths(base: Path) -> None:
    paths = sorted([p for p in base.rglob("*")], key=lambda p: len(str(p)), reverse=True)
    for path in paths:
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
        if not path.is_file():
            continue
        if path.suffix in {".o"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = xform(text)
        if new != text:
            path.write_text(new, encoding="utf-8")


def regen_patches() -> None:
    submit = ART / "poc" / "submit"
    verified = ART / "poc" / "verified"
    if (verified / "entry_leak.lenv").exists():
        (verified / "entry_leak.lenv").rename(verified / "entry_leak.qenv")

    patches = [
        ("bug1_quorumenv_entry_leak.patch", "src/quorumenv/store.c",
         lambda t: t.replace(
             "  quorumenv_doc_impl_t *d = (quorumenv_doc_impl_t *)doc;\n  quorumenv_arena_free",
             "  quorumenv_doc_impl_t *d = (quorumenv_doc_impl_t *)doc;\n  free(d->entries);\n  quorumenv_arena_free",
         )),
        ("bug2_toml_audit_leak.patch", "src/toml/parser.c", None),
        ("bug3_quorum_registry_uaf.patch", "src/quorum_registry.c",
         lambda t: t.replace(
             "  free(t->slots);\n  free(t->pending_refs);",
             "  free(t->slots);\n  for (i = 0; i < t->pending_count; i++) {\n    free((void *)t->pending_refs[i]);\n  }\n  free(t->pending_refs);",
         ).replace(
             "        t->pending_refs[t->pending_count++] = t->slots[i].label;",
             "        char *snap = strdup(t->slots[i].label ? t->slots[i].label : \"\");\n        if (!snap) {\n          return -1;\n        }\n        t->pending_refs[t->pending_count++] = snap;",
         )),
        ("bug4_toml_merge_uaf.patch", "src/toml/merge.c", None),
        ("bug5_toml_format_null_deref.patch", "src/toml/format.c", None),
    ]
    for name, rel, fix_fn in patches:
        old = submit / name.replace("quorum", "lease")
        if old.exists() and not (submit / name).exists():
            old.rename(submit / name)
        if fix_fn is None:
            p = submit / name
            if p.exists():
                text = p.read_text(encoding="utf-8")
                p.write_text(xform(text), encoding="utf-8")
            continue
        path = ROOT / rel
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        fixed = fix_fn(original)
        path.write_text(fixed, encoding="utf-8")
        diff = subprocess.check_output(["git", "diff", rel], cwd=ROOT, text=True)
        (submit / name).write_text(diff, encoding="utf-8")
        path.write_text(original, encoding="utf-8")


def main() -> None:
    if not ROOT.exists():
        raise SystemExit(f"missing {ROOT}")
    rename_paths(ROOT)
    rename_paths(ART)
    rewrite_files(ROOT)
    rewrite_files(ART)
    regen_patches()
    print("renamed to quorumcfg")


if __name__ == "__main__":
    main()
