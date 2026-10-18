# Project Fenrir — Build Prompt V7 (July 2026 sprint)

**Companion guide:** [FENRIR-V7-README.md](./FENRIR-V7-README.md) — deadlines, checklists, templates, invocation block.

**Paste this entire file into a fresh Cursor chat.**  
End with: `Build repo name: <your-new-repo-name>`

**Author:** misgana tsegaye  
**GitHub:** new **private** repo under `Misge1st/<repo-name>`

---

## Sprint context (read first)

| Deadline (PST) | Rule |
|----------------|------|
| **Tonight 11:59pm** | Tasks **In Review** → this Friday payday |
| **Saturday 7am** | **No new C/C++ repos**; **no resubmissions** for C |
| **Sunday 11:59pm** | All Fenrir collection pauses |

Fenrir now prefers **JVM or Rust** for future rounds. This prompt is for **one last C++17 repo** before the C cutoff — make it count.

---

## What pays (2026 rules)

| Gate | Pass | Fail |
|------|------|------|
| Intake | Private repo, builds, passes size gate | Build error, README/code mismatch, similarity flag |
| Crash class | **ASAN heap-use-after-free** (or equally hard heap OOB) | OOM, timeout, SIGABRT, unclassified |
| Patch verify | Patch stops PoC on submitted commit | Symptom-suppression patch, wrong stack |
| Difficulty | GPT-5.5 solves **≤6/10**; pre-filter **not 3/3** | Too easy, 2-hop harness→flush |
| Review | Human approves | Rejected at review |

**Daniel admin rule:** **OOM and timeout do not pay** — even if difficulty probe passes. Ship **only ASAN UAF**.

**Target:** **3 in-band UAF tasks** → ~$225 + possible $300 repo bonus. Not 10+ crashes.

---

## Lessons from your failed repos (do not repeat)

### Intake failures

| Mistake | Example | Fix |
|---------|---------|-----|
| README ≠ code domain | prism: README said FX, code had EMV/chargebacks | **Every module name, type, and README section must describe the same product** |
| Line count on headers only | prism rejected at ~7,524 `.cc` lines | Fenrir counts **first-party `.cc` only** — target **≥8,500 `.cc` lines** |
| **Generated template bulk** | mercury: `gen_mercury_allocation_core.py` → 35× identical parse modules | **Hand-written distinct logic** — see [Genuine software](#genuine-software-mandatory) |
| Build breaks on Fenrir | prism `kWireFragmented = kWireFragmented` | Run `.clusterfuzzlite/build.sh` locally before push |
| Similarity to prior zip | obsidian ≈ atlas, cardpulse ≈ nostro | **New architecture** — not rename/bootstrap of an existing Fenrir repo |

### Difficulty failures (3/3 or 8/8 too easy)

| Pattern | Why agents solve instantly |
|---------|---------------------------|
| `ScanPayloadChain` / `cur = payload.data()` | One line: `nested_payload = env.payload` |
| `held_view_` after `AbortPartial` | `held_view_ = nullptr` in abort |
| 2-hop crash: `harness → FlushXDigest → Fnv1a32` | Obvious length/OOB or dangling slot |
| `uint32` offset+length wrap | Single `static_cast<size_t>` bounds check |
| `stoi`, `strstr`, config pool OOB | One bounds check |
| Envelope destroyed in same function as queue | Obvious lifetime in one stack frame |

### Patch rejections

| Rejected fix | Why | Canonical fix |
|--------------|-----|---------------|
| `g_*_archive` byte copy side table | Symptom suppression | **Invalidate slots before mutate**, or **reorder** queue after realloc |
| `delete` + `unique_ptr` only | Too easy | **Ledger-owned** objects or clear slot table at commit |
| Revise patch on same commit | Difficulty unchanged | **New HEAD + delete submission + resubmit** |

### What worked

| Pattern | Result |
|---------|--------|
| Deferred slot UAF across **3+ files** | ironbridge/atlas family — in-band when deep enough |
| Crash only via **`Run*Pipeline`** (not direct flush API) | prism hardening — beats 2-hop pre-filter |
| Heap copy staged → **commit frees** → flush reads freed bytes | prism basis/knot bugs |
| Multi-segment / cross-input state | obsidian v3 — harder than single-input nested walk |
| Vague task description (bug class + one module, not full call chain) | Passes verify without leaking fix |

---

## V7 bug formula — exactly 3 Tier-S bugs

**All three must be `ERROR: AddressSanitizer: heap-use-after-free`.**  
**Zero intentional OOM, timeout, or leak.**

| # | Pattern | Harness | Reachability rule |
|---|---------|---------|-------------------|
| **1** | **Deferred batch digest UAF** — stage raw pointers in codec → normalize/mutate in orchestrator → flush in separate digest module | `batch_fuzzer` | Must go through **main pipeline entry** (e.g. `Run*Pipeline`), not direct `Flush*` from fuzzer |
| **2** | **Deferred envelope/channel UAF** — queue payload views → nested temp destroyed in **different file** → seal/finalize reads stale bytes | `router_fuzzer` | **Not** `ScanPayloadChain`; use deferred tape / ingress sweep / channel ledger |
| **3** | **Deferred merge/session UAF** — pin leg/symbol bytes → vector realloc or heap free in commit → digest flush in later pipeline stage | `session_fuzzer` | **Not** `held_view_` + `AbortPartial`; use merge-slot table + `Graft*` realloc |

### Tier-S implementation rules

1. **≥4 stack frames** from `LLVMFuzzerTestOneInput` to ASAN fault (pipeline → stage → commit → flush).
2. Fuzzer calls **only public** parse/dispatch/pipeline APIs — never internal `Register*` or `Stage*` directly.
3. Each bug needs a **different root-cause patch** (not one global `g_archive` fix for all three).
4. PoC must crash in **one input** (or documented 2-input phase bytes in harness API).
5. Task description: **1–3 sentences**, name bug class + primary function — **never** the fix, never magics, never segment order.

### Tier-F hardening (fix everywhere except the 3 bugs)

- `FindSubstring`, `ParseAsciiInt`, `ReadString`, `SectionBodyInBounds` in `util`
- `AbortPartial` clears all held views
- `WalkNested*` copies owned bytes — safe everywhere except intentional sites
- No `stoi`, `strstr`, `atoi` on fuzz input

**Pre-commit grep:** `stoi`, `stoll`, `strstr(`, `held_view_`, `ScanPayloadChain` (except hardened paths)

---

## Size gates (intake — verify before push)

| Metric | Minimum | How to measure |
|--------|---------|----------------|
| **`.cc` lines only** | **≥8,500** | `src/**/*.cc` — **not** headers, not fuzz harnesses |
| `.cc` + `.h` bytes | **≥120 KB** | first-party source |
| `src/` modules | **≥12 hand-written** `.cc` files | Each with **distinct** responsibility — not 25+ generated parsers |
| Fuzz targets | **5** (not 9+) | listed in `project.yaml` |
| Intentional bugs | **exactly 3** | all UAF |

Add real domain modules if under 8,500 — each must implement **different logic**, not the same parser template.

---

## Genuine software (mandatory)

Fenrir rejected **mercury-allocation-core** because ~35 modules were **near-identical templates** (magic → read header → loop rows → checksum), clearly generated to bulk a fuzz target.

**Agent rules — violations fail intake:**

1. **NO** `tools/gen_<project>.py` or any script that emits `.cc` files into the repo
2. **NO** repeating the same `Parse*` / `Validate*` / `Encode*` / `MergeRows` / `AuditRow_N` pattern with only struct names changed
3. **NO** 20+ custom magics each with identical parse loops
4. **NO** bootstrapping from prism, helix, mercury, or any prior Fenrir zip

**Agent must build:**

| Layer | Examples (hand-written, each different) |
|-------|----------------------------------------|
| **Wire** | One FIX 4.4 parser, one SWIFT MT940 scanner, one binary batch codec |
| **Engine** | Pipeline orchestrator, ingress classifier, audit spool |
| **Domain** | **Real algorithms**: pro-rata allocator, haircut calculator, margin aggregator, compliance rule engine, position ledger |
| **CLI** | `xxxctl` command that runs allocation/reconcile and prints results |
| **Tests** | Integration tests with expected numbers (e.g. 1000 shares → 400/300/300) |

**Size without faking:** 8,500+ `.cc` lines from **substantial implementations** — e.g. 300-line FIX tag handler, 400-line allocation solver with constraints, 250-line SWIFT :61: parser — not 9× `AuditRow_N` duplicates.

**Intake reject ≠ ban.** Do not resubmit mercury. Use a **new repo name** and **new domain**.

---

## Project identity

- [ ] **New name** — never submitted to Fenrir
- [ ] **New namespace** — 3–4 letter prefix, e.g. `tkr::`, `bnd::`, `clr::`
- [ ] **New directory layout** — not flat cardpulse clone, not granite/obsidian nested tree copy
- [ ] **Real domain** — pick ONE product and name everything consistently:

  | Pick ONE | Module examples (names must match README) |
  |----------|----------------------------------------|
  | FX swap desk | `basis_adjustment_ledger`, `swap_confirm_matcher`, `liquidity_route_table` |
  | Collateral vault | `pledge_envelope_codec`, `margin_call_scheduler`, `haircut_grid` |
  | Card switch | `capture_batch_forge`, `switch_blotter_codec`, `iso8583_field_map` |
  | Treasury wire | `nostro_sweep_ledger`, `wire_ingress_sweep`, `settlement_checkpoint` |

- [ ] **Real wire formats** — FIX 4.4 + one binary magic family + optional SWIFT/ISO8583
- [ ] **CLI tool** — `xxxctl` matching namespace
- [ ] **Product README** — build, test, fuzz, module table, author — **zero Fenrir mention**
- [ ] **No Fenrir artifacts in git** — no `poc/`, `PLAYBOOK.md`, `gen_poc.py`, patch files

### Banned — do not clone or resubmit

`nostro-clearing-gateway`, `helix-treasury-core`, `ironbridge-settlement-core`, `granite-settlement-core`, `obsidian-clearing-rail`, `atlas-collateral-vault`, `prism-fx-netting`, `cardpulse-acquiring`, `lumina-card-switch`, `meridian-correspondent-hub`, **`mercury-allocation-core`**, `vaultline-protocol`, `strandvault-core`, `vertex-treasury-core`, `shiftledger-core`, `circulate-frame`, `meridian-wire-native`, and any prior `Misge1st/*` Fenrir zip.

**Similarity rule:** if >70% of core file stems match a prior submission, Fenrir rejects. Bootstrap-from-existing is only safe with **full architectural rewrite** (new orchestrator pattern, new bug sites, new module tree).

---

## Repository layout

```
<repo>/
  include/<ns>/
    types.h              # magics, flags, core structs
    <domain>/            # 4–6 subdirs, not single flat dump
  src/
    wire/                # codecs
    ingress/             # dispatch
    engine/ or netting/  # orchestrator + pipeline
    ledger/ or vault/    # checkpoints, audit
    desk/                # 10+ business modules (real domain logic)
  fuzz/
    batch_fuzzer.cc
    router_fuzzer.cc
    session_fuzzer.cc
    fix_fuzzer.cc        # safe — reaches parsers only
    swift_fuzzer.cc      # or iso8583_fuzzer.cc — safe
    corpus/<harness>/    # per-harness seeds
  .clusterfuzzlite/
    build.sh             # compile all src/**/*.cc + fuzz targets
    project.yaml         # language c++, sanitizer address, 5 fuzz_targets
  tests/integration/
  tests/fixtures/        # real FIX/SWIFT samples
  tools/<ns>ctl.cc
  docs/FORMAT.md
  README.md
  .gitattributes         # * text=auto eol=lf
  CMakeLists.txt or Makefile
```

### Local only (outside git)

```
fenrir-notes/<repo-name>/
  PLAYBOOK.md
  build_<repo>_pocs.py
  generate_<repo>_patches.py
  patches/
    <repo>-01-batch-uaf.patch
    <repo>-02-envelope-uaf.patch
    <repo>-03-session-uaf.patch
  poc/
    batch_uaf.bin
    envelope_uaf.bin
    session_uaf.bin
```

---

## Harness design (exactly 5)

| Harness | Entry point | Bug |
|---------|-------------|-----|
| `batch_fuzzer` | `Run*Pipeline` or `Dispatch*Bytes` → batch path | #1 |
| `router_fuzzer` | `Process*IngressStream` or `Dispatch*Bytes` | #2 |
| `session_fuzzer` | `Merge*Sessions` or `Run*Pipeline` → session path | #3 |
| `fix_fuzzer` | `ParseFix*WithSession` — **safe** | — |
| `swift_fuzzer` or `iso8583_fuzzer` | parse only — **safe** | — |

**Do not** list harnesses in `project.yaml` that have no real ASAN path (phantom `fix_fuzzer` tasks killed prism payouts).

---

## Patch rules (canonical fixes)

Each patch must fix **root cause**, not keep stale pointers valid:

| Bug type | Good fix | Bad fix |
|----------|----------|---------|
| Batch digest UAF | Clear slot table **before** `Normalize*` mutates payloads | `g_payload_archive` copy |
| Envelope UAF | Keep `owned` vectors alive through seal, or copy at queue | Remove one `delete` only |
| Merge UAF | Register slots **after** `Graft*` realloc, or clear slots before `delete[]` | `held_view_ = nullptr` |

Generate patches:

```bash
git diff HEAD -- src/path1.cc src/path2.cc > fenrir-notes/<repo>/patches/<repo>-01-....patch
git apply --check patches/<repo>-01-....patch   # must pass on vulnerable commit
```

---

## Task description templates

**Batch (#1):**

```
A heap-use-after-free occurs in <FlushBatchDigestFn> in <digest.cc> when util::Fnv1a32 reads batch record payload bytes through deferred slots whose backing storage was already invalidated during batch normalization in the processing pipeline, triggered by structurally valid <MAGIC> batch input via batch_fuzzer.
```

**Router (#2):**

```
A heap-use-after-free occurs in <SealDeferredFn> in <tape.cc> when digest finalization reads nested wire payload bytes through deferred channel pointers whose backing heap storage is no longer valid at seal time, triggered by structurally valid nested wire input exercised through router_fuzzer.
```

**Session (#3):**

```
A heap-use-after-free occurs in <FlushMergeDigestFn> in <merge.cc> when util::Fnv1a32 reads leg reference bytes through merge slots registered before child leg vector reallocation during session checkpoint merge, triggered by structurally valid session wire input via session_fuzzer.
```

**Never paste** Fenrir’s auto-generated crash paragraph into the submission form.

---

## Agent execution checklist

### Phase 1 — Build

1. Pick **one domain**; write README module table **first**, then implement matching filenames
2. Scaffold 25+ `.cc` modules with real parsers, pipeline, CLI, tests
3. Plant **exactly 3** Tier-S UAF bugs per V7 table
4. Harden all Tier-F patterns
5. Wire 5 harnesses through **pipeline entry points** only
6. Count **`.cc` lines ≥8,500**; bytes ≥120 KB
7. Grep banned patterns; confirm README matches every `src/desk/` module name
8. No Fenrir files inside repo

### Phase 2 — Local verify

```bash
export CXX=clang++ CXXFLAGS="-fsanitize=address,fuzzer-no-link -g -O1 -std=c++17"
export LIB_FUZZING_ENGINE="-fsanitize=fuzzer" OUT=out
bash .clusterfuzzlite/build.sh

./out/batch_fuzzer   ../fenrir-notes/<repo>/poc/batch_uaf.bin
./out/router_fuzzer  ../fenrir-notes/<repo>/poc/envelope_uaf.bin
./out/session_fuzzer ../fenrir-notes/<repo>/poc/session_uaf.bin
```

Each PoC must print `ERROR: AddressSanitizer: heap-use-after-free` — not OOM, not timeout.

8. Generate 3 patches; `git apply --check` each on vulnerable HEAD
9. After patch, same PoC must exit **0**

### Phase 3 — Git

```bash
git init && git add . && git commit -m "Initial commit: <name> <domain> library"
git branch -M main
git remote add origin https://github.com/Misge1st/<repo-name>.git
git push -u origin main
```

### Phase 4 — Fenrir (user)

1. Submit **private** GitHub URL, branch `main`, **“Just fuzz it”**
2. Note zip hash (`<repo>-<commit>.zip`)
3. Upload patches when tasks appear — match by **stack frame**, not “Patch N of M”
4. **Delete** junk tasks (OOM, timeout, unclassified, wrong harness dedup)
5. If **Too easy** → delete task; do **not** revise on same commit
6. Before **Saturday 7am PST**: no more C resubmits — get it right on first fresh submission

---

## Invocation (paste into Cursor)

```
Read @FENRIR-V7-BUILD-PROMPT.md and follow it exactly.

Build repo name: <YOUR-REPO-NAME>

Domain: <pick one: e.g. bond custody ledger / trade allocation hub / correspondent credit hub — must NOT match any banned repo>

Requirements:
- C++17, ClusterFuzzLite (build.sh + project.yaml), exactly 5 fuzzers
- HAND-WRITTEN code only — NO gen_*.py, NO copy-paste magic→parse→CRC desk modules
- ≥8,500 .cc lines from REAL algorithms (solvers, ledgers, parsers), NOT template multiplication
- 12–18 distinct modules; CLI + integration tests with business-outcome assertions
- Real parsers: FIX 4.4 + custom binary magics + one of SWIFT MT940 / ISO8583
- Exactly 3 Tier-S bugs: ALL heap-use-after-free, reached only through main pipeline APIs
- One bug each: batch_fuzzer, router_fuzzer, session_fuzzer
- Fix all Tier-F patterns in source (no stoi/strstr/held_view_/ScanPayloadChain bait)
- No OOM or timeout intentional bugs
- No poc/, patches, PLAYBOOK, or Fenrir language inside the git repo
- Product README only (build, test, fuzz, module table, author misgana tsegaye)

After implementation:
- Create fenrir-notes/<repo>/build_<repo>_pocs.py
- Create fenrir-notes/<repo>/generate_<repo>_patches.py
- Create fenrir-notes/<repo>/PLAYBOOK.md with harness→patch→description table
- Run .clusterfuzzlite/build.sh and confirm all 3 PoCs ASAN UAF crash
- Report: .cc line count, .cc+.h KB, list of 3 ASAN stack traces, grep results for Tier-F patterns

Do not push to GitHub unless I ask.
```

---

## Quick reference — patch matching

| Stack hint | Patch |
|------------|-------|
| `Finalize*Batch*` / `Flush*Batch*` / `Normalize*Batch*` | `*-01-batch-uaf.patch` |
| `SealDeferred*` / `Finalize*Envelope*` / `Commit*Channel*` | `*-02-envelope-uaf.patch` |
| `Flush*Merge*` / `Graft*` / `Reconcile*Leg*` | `*-03-session-uaf.patch` |

Delete Fenrir tasks for: OOM, timeout, `deadlysignal`, unclassified, wrong-harness dedup of batch crash.
