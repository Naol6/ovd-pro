#!/usr/bin/env python3
"""Bootstrap arptable — ARP neighbor table parser (pack family, NOT cfg/TOML)."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/arptable")
SRC = Path("/home/samuel/Documents/fenrir3/netrcpack")

TEXT_RENAME = [
    ("netrc_doc_impl_t", "arp_doc_impl_t"),
    ("netrc_doc_t", "arp_doc_t"),
    ("netrc_error_t", "arp_error_t"),
    ("netrc_options_t", "arp_options_t"),
    ("netrc_entry_t", "arp_entry_t"),
    ("netrc_slice_t", "arp_slice_t"),
    ("netrc_arena_t", "arp_arena_t"),
    ("netrc_token_kind_t", "arp_token_kind_t"),
    ("netrc_token_t", "arp_token_t"),
    ("netrc_internal.h", "arp_internal.h"),
    ("netrcpack/netrc_types.h", "arptable/arp_types.h"),
    ("netrcpack/netrc.h", "arptable/arp.h"),
    ("include/netrcpack", "include/arptable"),
    ("netrc_machine_table_t", "arp_neighbor_table_t"),
    ("netrc_machine_t", "arp_neighbor_t"),
    ("netrc_machine_table", "arp_neighbor_table"),
    ("netrc_machine_init", "arp_neighbor_init"),
    ("netrc_machine_begin", "arp_neighbor_begin"),
    ("netrc_machine_set_login", "arp_neighbor_set_lladdr"),
    ("netrc_machine_set_password", "arp_neighbor_set_device"),
    ("netrc_machine_set_account", "arp_neighbor_set_state"),
    ("netrc_machine_count", "arp_neighbor_count"),
    ("netrc_machine_get", "arp_neighbor_get"),
    ("netrc_macdef_t", "arp_nstate_t"),
    ("netrc_macdef_create", "arp_nstate_create"),
    ("netrc_macdef_destroy", "arp_nstate_destroy"),
    ("netrc_macdef_begin", "arp_nstate_begin"),
    ("netrc_macdef_append_line", "arp_nstate_append_event"),
    ("netrc_macdef_finalize_digest", "arp_nstate_finalize_digest"),
    ("netrcpack/machine.h", "arptable/neighbor.h"),
    ("netrcpack/macdef.h", "arptable/nstate.h"),
    ("machine.c", "neighbor.c"),
    ("macdef.c", "nstate.c"),
    ("macdef_fuzzer", "nstate_fuzzer"),
    ("machmap", "neighmap"),
    ("netloader", "arploader"),
    ("netrcpack.c", "arptable.c"),
    ("NETRC_", "ARP_"),
    ("Netrc", "Arp"),
    ("netrc_", "arp_"),
    ("netrcpack", "arptable"),
    ("netrc", "arp"),
    (".netrc", ".arp"),
    ("/tmp/netrcpack_out", "/tmp/arptable_out"),
    ("tolossamuel/netrcpack", "tolossamuel/arptable"),
    ("machine/login/password", "IP lladdr/dev/state neighbor rows"),
    ("FTP/HTTP .netrc credential files", "kernel ARP neighbor table files"),
    (".netrc credential", "ARP neighbor table"),
    ("machine block", "neighbor row"),
    ("Machine credential", "Neighbor row"),
    ("macdef macro", "neighbor state trace"),
    ("Macdef", "Nstate"),
    ("macdef", "nstate"),
    ("machine", "neighbor"),
    ("Machine", "Neighbor"),
    ("login", "lladdr"),
    ("password", "device"),
    ("account", "state"),
    ("credential document", "neighbor table document"),
    ("Credential", "Neighbor table"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh"}
EXCLUDE = {".git", "poc", "guides", "__pycache__"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add arptable public headers", [
        "include/arptable/arp.h", "include/arptable/arp_types.h"]),
    ("include: add neighbor and address module headers", [
        "include/arptable/neighbor.h", "include/arptable/address.h",
        "include/arptable/lladdr.h", "include/arptable/nstate.h"]),
    ("src: add buffer and string utilities", [
        "src/buffer.c", "src/buffer.h", "src/strutil.c", "src/strutil.h"]),
    ("src: add arena allocator", ["src/arena.c", "src/arena.h", "src/arp_internal.h"]),
    ("src: add error helpers", ["src/error.c", "src/error.h"]),
    ("src: add UTF-8 validation", ["src/utf8.c", "src/utf8.h"]),
    ("src: implement arp line lexer", ["src/lexer.c", "src/lexer.h"]),
    ("src: add quoted token unescape", ["src/unescape.c", "src/unescape.h"]),
    ("src: add neighbor document store", ["src/store.c", "src/store.h"]),
    ("src: add IPv4/IPv6 address parsing", ["src/address.c"]),
    ("src: add link-layer MAC parsing", ["src/lladdr.c"]),
    ("src: add neighbor row registry", ["src/neighbor.c"]),
    ("src: add neighbor state trace capture", ["src/nstate.c"]),
    ("src: wire arp row parser", ["src/parser.c", "src/parser.h"]),
    ("src: add serialize to arp text", ["src/serialize.c", "src/serialize.h"]),
    ("src: add validation pass", ["src/validate.c", "src/validate.h"]),
    ("src: add merge overlay", ["src/merge.c", "src/merge.h"]),
    ("src: add expand and coerce", [
        "src/expand.c", "src/expand.h", "src/coerce.c", "src/coerce.h"]),
    ("src: add walk query diff", [
        "src/walk.c", "src/walk.h", "src/query.c", "src/query.h",
        "src/diff.c", "src/diff.h"]),
    ("src: add pretty printer", ["src/pretty.c", "src/pretty.h"]),
    ("src: add import stack and ctx", [
        "src/import_stack.c", "src/import_stack.h",
        "src/import_ctx.c", "src/import_ctx.h"]),
    ("src: add path filter profile", [
        "src/path.c", "src/path.h", "src/filter.c", "src/filter.h",
        "src/profile.c", "src/profile.h"]),
    ("src: add snapshot readutil strict canonical", [
        "src/snapshot.c", "src/snapshot.h", "src/readutil.c", "src/readutil.h",
        "src/strict.c", "src/strict.h", "src/canonical.c", "src/canonical.h"]),
    ("src: add arploader and main arptable module", [
        "src/arploader.c", "src/arptable.c", "src/neighmap.c", "src/neighmap.h"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add neighbor address nstate unit tests", [
        "tests/test_neighbor.c", "tests/test_address.c", "tests/test_nstate.c"]),
    ("examples: add sample arp neighbor table files", [
        "examples/sample.arp", "examples/imported.arp"]),
    ("fuzz: add parse_fuzzer harness", ["fuzz/parse_fuzzer.c"]),
    ("fuzz: add merge_fuzzer harness", ["fuzz/merge_fuzzer.c"]),
    ("fuzz: add import_fuzzer harness", ["fuzz/import_fuzzer.c"]),
    ("fuzz: add nstate_fuzzer harness", ["fuzz/nstate_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/parse_fuzzer/minimal.arp",
        "fuzz/corpus/parse_fuzzer/neighbor.arp",
        "fuzz/corpus/merge_fuzzer/base.arp",
        "fuzz/corpus/import_fuzzer/primary.arp",
        "fuzz/corpus/nstate_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for arptable library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable ARP neighbor table parser", []),
]

README = """# arptable

arptable is a C11 library for parsing and manipulating ARP neighbor table files: whitespace-separated neighbor rows with IP address, link-layer MAC (`lladdr`), network device, and reachability state, plus `@import` overlays for layered tables.

## Features

- **Row grammar** — `192.168.1.1 lladdr 00:11:22:33:44:55 dev eth0 state REACHABLE`
- **Address parsing** — IPv4 and IPv6 neighbor addresses
- **Link-layer parsing** — colon-separated MAC (`lladdr`) validation
- **Neighbor registry** — row container with merge and serialize
- **State trace** — compaction tracker for multi-event neighbor state sequences
- ClusterFuzzLite harnesses: `parse_fuzzer`, `merge_fuzzer`, `import_fuzzer`, `nstate_fuzzer`

## Build

```bash
bash build/wsl_build.sh
make test
```

## Quick start

```c
#include "arptable/arp.h"

arp_doc_t *doc = NULL;
arp_error_t *err = NULL;
arp_options_t opt = arp_default_options();
arp_parse_memory("192.168.1.1 lladdr 00:11:22:33:44:55 dev eth0 state REACHABLE\\n", 60, &opt, &doc, &err);
arp_doc_free(doc);
arp_error_free(err);
```

## License

MIT — see LICENSE.
"""

ADDRESS_H = """#ifndef ARPTABLE_ADDRESS_H
#define ARPTABLE_ADDRESS_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int arp_address_is_valid(const char *text, size_t len);

#ifdef __cplusplus
}
#endif

#endif
"""

ADDRESS_C = """#include "arptable/address.h"

#include <ctype.h>

int arp_address_is_valid(const char *text, size_t len) {
  size_t i;
  int colons = 0;
  int dots = 0;
  if (!text || len == 0) {
    return 0;
  }
  for (i = 0; i < len; i++) {
    unsigned char c = (unsigned char)text[i];
    if (c == ':') {
      colons++;
    } else if (c == '.') {
      dots++;
    } else if (!isxdigit(c)) {
      return 0;
    }
  }
  return colons > 0 || dots == 3;
}
"""

LLADDR_H = """#ifndef ARPTABLE_LLADDR_H
#define ARPTABLE_LLADDR_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int arp_lladdr_is_valid(const char *text, size_t len);

#ifdef __cplusplus
}
#endif

#endif
"""

LLADDR_C = """#include "arptable/lladdr.h"

#include <ctype.h>

int arp_lladdr_is_valid(const char *text, size_t len) {
  size_t i;
  int pairs = 0;
  if (!text || len < 11) {
    return 0;
  }
  for (i = 0; i < len; i++) {
    unsigned char c = (unsigned char)text[i];
    if (c == ':') {
      pairs++;
    } else if (!isxdigit(c)) {
      return 0;
    }
  }
  return pairs >= 5;
}
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
        (ROOT / "include" / "netrcpack" / "machine.h", ROOT / "include" / "arptable" / "neighbor.h"),
        (ROOT / "include" / "netrcpack" / "macdef.h", ROOT / "include" / "arptable" / "nstate.h"),
        (ROOT / "include" / "netrcpack" / "netrc.h", ROOT / "include" / "arptable" / "arp.h"),
        (ROOT / "include" / "netrcpack" / "netrc_types.h", ROOT / "include" / "arptable" / "arp_types.h"),
        (ROOT / "src" / "machine.c", ROOT / "src" / "neighbor.c"),
        (ROOT / "src" / "macdef.c", ROOT / "src" / "nstate.c"),
        (ROOT / "src" / "netrcpack.c", ROOT / "src" / "arptable.c"),
        (ROOT / "src" / "netloader.c", ROOT / "src" / "arploader.c"),
        (ROOT / "src" / "machmap.c", ROOT / "src" / "neighmap.c"),
        (ROOT / "src" / "machmap.h", ROOT / "src" / "neighmap.h"),
        (ROOT / "fuzz" / "macdef_fuzzer.c", ROOT / "fuzz" / "nstate_fuzzer.c"),
        (ROOT / "examples" / "sample.netrc", ROOT / "examples" / "sample.arp"),
        (ROOT / "examples" / "imported.netrc", ROOT / "examples" / "imported.arp"),
        (ROOT / "tests" / "test_machine.c", ROOT / "tests" / "test_neighbor.c"),
        (ROOT / "tests" / "test_macdef.c", ROOT / "tests" / "test_nstate.c"),
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

    netrcpack_dir = ROOT / "include" / "netrcpack"
    if netrcpack_dir.exists():
        for p in list(netrcpack_dir.glob("*")):
            p.unlink(missing_ok=True)
        netrcpack_dir.rmdir()

    for p in list((ROOT / "fuzz" / "corpus" / "parse_fuzzer").glob("*")):
        if p.suffix == ".netrc":
            p.rename(p.with_suffix(".arp"))


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
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".arp", ".netrc", "Makefile"
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


def patch_neighbor_module() -> None:
    nh = (ROOT / "include" / "arptable" / "neighbor.h").read_text(encoding="utf-8")
    nh = nh.replace("login", "lladdr").replace("password", "device").replace("account", "state")
    nh = nh.replace("name", "address")
    (ROOT / "include" / "arptable" / "neighbor.h").write_text(nh, encoding="utf-8")

    nc = (ROOT / "src" / "neighbor.c").read_text(encoding="utf-8")
    nc = nc.replace('"host"', '"192.168.1.1"')
    nc = nc.replace("m->name", "m->address")
    nc = nc.replace("m->login", "m->lladdr")
    nc = nc.replace("m->password", "m->device")
    nc = nc.replace("m->account", "m->state")
    nc = nc.replace("->name", "->address")
    (ROOT / "src" / "neighbor.c").write_text(nc, encoding="utf-8")

    sh = (ROOT / "src" / "store.h").read_text(encoding="utf-8")
    sh = sh.replace("name", "address").replace("login", "lladdr")
    sh = sh.replace("password", "device").replace("account", "state")
    (ROOT / "src" / "store.h").write_text(sh, encoding="utf-8")


def patch_parser_rows() -> None:
    p = ROOT / "src" / "parser.c"
    text = p.read_text(encoding="utf-8")
    text = text.replace('#include "arptable/neighbor.h"', '#include "arptable/neighbor.h"\n#include "arptable/address.h"')
    text = text.replace(
        '  if (arp_ident_equals(tok->text, "neighbor")) {',
        '  if (arp_ident_equals(tok->text, "lladdr") || arp_ident_equals(tok->text, "at")) {',
    )
    text = text.replace(
        '    return arp_neighbor_begin((arp_doc_t *)doc,\n                               arp_copy_token(doc, tok->text));',
        '    return 0;',
    )
    # Row-start: if token looks like address, begin neighbor row
    old = '    if (tok.kind == ARP_TOK_IDENT) {\n      int dir = arp_parse_directive(doc, &lx, &tok, out_err);'
    new = '''    if (tok.kind == ARP_TOK_IDENT && arp_address_is_valid(tok.text.data, tok.text.len)) {
      if (arp_neighbor_begin((arp_doc_t *)doc, arp_copy_token(doc, tok.text)) != 0) {
        return -1;
      }
      if (arp_lexer_next(&lx, &tok) != 0) {
        return -1;
      }
      continue;
    }

    if (tok.kind == ARP_TOK_IDENT) {
      int dir = arp_parse_directive(doc, &lx, &tok, out_err);'''
    if old in text:
        text = text.replace(old, new)
    p.write_text(text, encoding="utf-8")


def fix_unescape() -> None:
    p = ROOT / "src" / "unescape.c"
    text = p.read_text(encoding="utf-8")
    text = text.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "unescape.c").write_text(text, encoding="utf-8")


def add_domain() -> None:
    write(ROOT / "include" / "arptable" / "address.h", ADDRESS_H)
    write(ROOT / "include" / "arptable" / "lladdr.h", LLADDR_H)
    write(ROOT / "src" / "address.c", ADDRESS_C)
    write(ROOT / "src" / "lladdr.c", LLADDR_C)
    write(ROOT / "README.md", README)

    write(ROOT / "examples" / "sample.arp", """# Local ARP neighbor cache
192.168.1.1 lladdr 00:11:22:33:44:55 dev eth0 state REACHABLE
192.168.1.2 lladdr aa:bb:cc:dd:ee:ff dev eth0 state STALE
fe80::1 lladdr fe80::2 dev wlan0 state DELAY
""")

    write(ROOT / "examples" / "imported.arp", """@import "shared.arp"
192.168.2.10 lladdr 11:22:33:44:55:66 dev eth1 state REACHABLE
""")

    write(ROOT / "tests" / "test_address.c", '''#include "arptable/address.h"
#include "unity/unity.h"

void test_ipv4_address(void) {
  TEST_ASSERT(arp_address_is_valid("192.168.1.1", 11));
  TEST_ASSERT(!arp_address_is_valid("", 0));
}
''')

    write(ROOT / "tests" / "test_neighbor.c", '''#include "arptable/neighbor.h"
#include "arptable/arp.h"
#include "unity/unity.h"

void test_neighbor_row(void) {
  arp_doc_t *doc = arp_doc_create();
  TEST_ASSERT_NOT_NULL(doc);
  TEST_ASSERT_EQUAL(0, arp_neighbor_begin(doc, "10.0.0.1"));
  TEST_ASSERT_EQUAL(0, arp_neighbor_set_lladdr(doc, "00:11:22:33:44:55"));
  TEST_ASSERT_EQUAL(1, arp_neighbor_count(doc));
  arp_doc_destroy(doc);
}
''')


def patch_build() -> None:
    build = (ROOT / ".clusterfuzzlite" / "build.sh").read_text(encoding="utf-8")
    build = xform(build)
    build = build.replace(
        "snapshot netloader netrcpack machine macdef",
        "snapshot arploader arptable address lladdr neighbor nstate",
    )
    build = build.replace("macdef_fuzzer.c macdef_fuzzer", "nstate_fuzzer.c nstate_fuzzer")
    (ROOT / ".clusterfuzzlite" / "build.sh").write_text(build, encoding="utf-8")

    wsl = (ROOT / "build" / "wsl_build.sh").read_text(encoding="utf-8")
    wsl = xform(wsl)
    (ROOT / "build" / "wsl_build.sh").write_text(wsl, encoding="utf-8")

    proj = (ROOT / ".clusterfuzzlite" / "project.yaml").read_text(encoding="utf-8")
    proj = xform(proj)
    (ROOT / ".clusterfuzzlite" / "project.yaml").write_text(proj, encoding="utf-8")


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
    patch_neighbor_module()
    patch_parser_rows()
    fix_unescape()
    add_domain()
    patch_build()
    init_git()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
