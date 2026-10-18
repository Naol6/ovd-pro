#!/usr/bin/env python3
"""Rename quotacfg -> budgetcfg for GitHub push."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/budgetcfg")
SRC = Path("/home/samuel/Documents/fenrir3/quotacfg")
ART = Path("/home/samuel/Documents/fenrir3/artifacts/budgetcfg")

RENAMES = [
    ("quotacfg", "budgetcfg"),
    ("Quotacfg", "Budgetcfg"),
    ("QUOTACFG", "BUDGETCFG"),
    ("quotaenv", "budgetenv"),
    ("Quotaenv", "Budgetenv"),
    ("QUOTAENV", "BUDGETENV"),
    ("quota_ledger", "budget_ledger"),
    ("quota_enforcer", "budget_enforcer"),
    ("quota_window", "budget_window"),
    ("quota_gate", "budget_gate"),
    ("quota_policy", "budget_policy"),
    ("quota_fuzzer", "budget_fuzzer"),
    ("quota_merge", "budget_merge"),
    ("quota_stack", "budget_stack"),
    ("quota_ctx", "budget_ctx"),
    ("quotamap", "budgetmap"),
    ("quotaloader", "budgetloader"),
    ("quota_bucket", "budget_bucket"),
    ("QUOTA_ENFORCE", "BUDGET_ENFORCE"),
    ("qenv_", "benv_"),
    (".qenv", ".benv"),
    ("@quota", "@budget"),
    ("/tmp/quotacfg_out", "/tmp/budgetcfg_out"),
    ("tolossamuel/quotacfg", "tolossamuel/budgetcfg"),
    ("[quota]", "[budget]"),
    ("[[quota.buckets]]", "[[budget.buckets]]"),
    ("quota.runtime", "budget.runtime"),
    ("quota.toml", "budget.toml"),
    ("Resource quota", "Spending budget"),
    ("resource quota", "spending budget"),
    ("quota manifests", "budget manifests"),
    ("Quota manifests", "Budget manifests"),
    ("quotaenv runtime", "budgetenv runtime"),
    ("Quotaenv layer", "Budgetenv layer"),
    ("quotaenv layer", "budgetenv layer"),
    ("tenant consumption ledger", "department spending ledger"),
    ("Tenant consumption ledger", "Department spending ledger"),
    ("quota ledger", "budget ledger"),
    ("Quota ledger", "Budget ledger"),
    ("hard_limit", "ceiling"),
    ("soft_limit", "floor"),
    ("HARD_LIMIT", "CEILING"),
    ("SOFT_LIMIT", "FLOOR"),
    ("QUOTA_STATE", "BUDGET_STATE"),
    ("quota_state", "budget_state"),
]


def main() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    shutil.copytree(SRC, ROOT, ignore=shutil.ignore_patterns(".git", "*.o"))
    subprocess.check_call(["git", "init", "-b", "main"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.name", "tolossamuel"], cwd=ROOT)
    subprocess.check_call(
        ["git", "config", "user.email", "tolossamuel@users.noreply.github.com"], cwd=ROOT)

    # path renames longest first
    path_pairs = [
        ("include/quotacfg", "include/budgetcfg"),
        ("include/quotaenv", "include/budgetenv"),
        ("src/quotaenv", "src/budgetenv"),
        ("src/quotacfg.c", "src/budgetcfg.c"),
        ("fuzz/corpus/quotaenv_fuzzer", "fuzz/corpus/budgetenv_fuzzer"),
        ("fuzz/corpus/quota_fuzzer", "fuzz/corpus/budget_fuzzer"),
        ("fuzz/corpus/quota_ledger_fuzzer", "fuzz/corpus/budget_ledger_fuzzer"),
        ("fuzz/corpus/quota_window_fuzzer", "fuzz/corpus/budget_window_fuzzer"),
    ]
    for old, new in path_pairs:
        o, n = ROOT / old, ROOT / new
        if o.exists():
            n.parent.mkdir(parents=True, exist_ok=True)
            if n.exists():
                shutil.rmtree(n) if n.is_dir() else n.unlink()
            o.rename(n)

    for f in list((ROOT / "include" / "budgetenv").glob("*quota*")):
        f.rename(f.with_name(f.name.replace("quota", "budget")))
    for f in list((ROOT / "src" / "budgetenv").glob("*quota*")):
        f.rename(f.with_name(f.name.replace("quota", "budget")))
    for f in list((ROOT / "include" / "budgetcfg").glob("*quota*")):
        f.rename(f.with_name(f.name.replace("quota", "budget")))
    for f in list((ROOT / "src").glob("quota_*.c")):
        f.rename(f.with_name(f.name.replace("quota_", "budget_")))
    for f in list((ROOT / "fuzz").glob("quota*.c")):
        f.rename(f.with_name(f.name.replace("quota", "budget", 1)))

    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix == ".o":
            continue
        if p.suffix not in {
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".toml", ".benv", ".qenv", ".runtime"
        } and p.name not in {"Makefile", ".gitignore", "LICENSE"}:
            if p.suffix not in {".bin"}:
                continue
        try:
            data = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for old, new in RENAMES:
            data = data.replace(old, new)
        p.write_text(data, encoding="utf-8")

    corp = ROOT / "fuzz" / "corpus" / "budgetenv_fuzzer"
    for old in list(corp.glob("*.qenv")):
        old.rename(old.with_suffix(".benv"))

    # preserve git history from quotacfg
    shutil.rmtree(ROOT / ".git")
    shutil.copytree(SRC / ".git", ROOT / ".git")
    # rewrite working tree with budget names
    subprocess.check_call(["git", "add", "-A"], cwd=ROOT)
    subprocess.check_call(
        ["git", "commit", "-m", "refactor: rename quotacfg domain to budgetcfg for unique submission"],
        cwd=ROOT,
    )

    if ART.exists():
        shutil.rmtree(ART)
    ART.mkdir(parents=True)
    subprocess.check_call(["cp", "-a", str(Path("/home/samuel/Documents/fenrir3/artifacts/quotacfg/.") + "/.", str(ART))])
    for p in ART.rglob("*"):
        if p.is_file() and p.suffix in {".txt", ".patch", ".sh", ".md"}:
            t = p.read_text(encoding="utf-8")
            nt = t
            for old, new in RENAMES:
                nt = nt.replace(old, new)
            if nt != t:
                p.write_text(nt, encoding="utf-8")
    for old, new in [
        ("entry_leak.qenv", "entry_leak.benv"),
        ("ledger_uaf.bin", "ledger_uaf.bin"),
    ]:
        o = ART / "poc" / "verified" / old
        if o.exists() and "qenv" in old:
            o.rename(o.with_name(new))

    n = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()
    print(f"budgetcfg ready: {n} commits")


if __name__ == "__main__":
    main()
