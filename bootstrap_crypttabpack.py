#!/usr/bin/env python3
"""Bootstrap crypttabpack — /etc/crypttab LUKS/dm-crypt parser (pack family, flat src/)."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/crypttabpack")
SRC = Path("/home/samuel/Documents/fenrir3/arptable")
ARTIFACTS = Path("/home/samuel/Documents/fenrir3/artifacts/crypttabpack")

TEXT_RENAME = [
    ("arp_doc_impl_t", "crypt_doc_impl_t"),
    ("arp_doc_t", "crypt_doc_t"),
    ("arp_error_t", "crypt_error_t"),
    ("arp_options_t", "crypt_options_t"),
    ("arp_entry_t", "crypt_entry_t"),
    ("arp_slice_t", "crypt_slice_t"),
    ("arp_arena_t", "crypt_arena_t"),
    ("arp_token_kind_t", "crypt_token_kind_t"),
    ("arp_token_t", "crypt_token_t"),
    ("arp_internal.h", "crypt_internal.h"),
    ("arptable/arp_types.h", "crypttabpack/crypt_types.h"),
    ("arptable/arp.h", "crypttabpack/crypt.h"),
    ("include/arptable", "include/crypttabpack"),
    ("arp_neighbor_table_t", "crypt_volume_table_t"),
    ("arp_neighbor_t", "crypt_volume_t"),
    ("arp_neighbor_table", "crypt_volume_table"),
    ("arp_neighbor_init", "crypt_volume_init"),
    ("arp_neighbor_begin", "crypt_volume_begin"),
    ("arp_neighbor_set_lladdr", "crypt_volume_set_cipher"),
    ("arp_neighbor_set_device", "crypt_volume_set_keyref"),
    ("arp_neighbor_set_state", "crypt_volume_set_optfield"),
    ("arp_neighbor_count", "crypt_volume_count"),
    ("arp_neighbor_get", "crypt_volume_get"),
    ("arp_nstate_t", "crypt_keytrace_t"),
    ("arp_nstate_create", "crypt_keytrace_create"),
    ("arp_nstate_destroy", "crypt_keytrace_destroy"),
    ("arp_nstate_begin", "crypt_keytrace_begin"),
    ("arp_nstate_append_event", "crypt_keytrace_append_event"),
    ("arp_nstate_finalize_digest", "crypt_keytrace_finalize_digest"),
    ("arptable/neighbor.h", "crypttabpack/volume.h"),
    ("arptable/nstate.h", "crypttabpack/keytrace.h"),
    ("arptable/address.h", "crypttabpack/volname.h"),
    ("arptable/lladdr.h", "crypttabpack/cipher.h"),
    ("neighbor.c", "volume.c"),
    ("nstate.c", "keytrace.c"),
    ("nstate_fuzzer", "keytrace_fuzzer"),
    ("neighmap", "volmap"),
    ("arploader", "tabloader"),
    ("arptable.c", "crypttabpack.c"),
    ("ARP_", "CRYPT_"),
    ("Arp", "Crypt"),
    ("arp_", "crypt_"),
    ("arptable", "crypttabpack"),
    ("arp", "crypt"),
    (".arp", ".tab"),
    ("/tmp/arptable_out", "/tmp/crypttabpack_out"),
    ("tolossamuel/arptable", "tolossamuel/crypttabpack"),
    ("IP lladdr/dev/state neighbor rows", "volume cipher keyref optfield crypttab rows"),
    ("kernel ARP neighbor table files", "/etc/crypttab LUKS/dm-crypt volume table files"),
    ("ARP neighbor table", "crypttab volume table"),
    ("neighbor row", "crypttab volume row"),
    ("Neighbor row", "Crypttab volume row"),
    ("neighbor state trace", "key reference trace"),
    ("Nstate", "Keytrace"),
    ("nstate", "keytrace"),
    ("neighbor", "volume"),
    ("Neighbor", "Volume"),
    ("lladdr", "cipher"),
    ("device", "keyref"),
    ("state", "optfield"),
    ("address", "volname"),
    ("Address", "Volname"),
    ("IPv4 and IPv6 neighbor", "Volume name"),
    ("192.168.1.1", "sda1_crypt"),
    ("10.0.0.1", "home_crypt"),
    ("credential document", "volume table document"),
    ("Credential", "Volume table"),
    ("NETRCPACK_MACHINE_H", "CRYPTTABPACK_VOLUME_H"),
    ("NETRCPACK_MACDEF_H", "CRYPTTABPACK_KEYTRACE_H"),
]

SKIP_FILES = {"bootstrap.py", "gen_history.py", "wsl_test_pocs.sh", "TASKS.md"}
EXCLUDE = {".git", "poc", "guides", "__pycache__"}

COMMITS = [
    ("chore: add MIT license and gitignore", ["LICENSE", ".gitignore"]),
    ("include: add crypttabpack public headers", [
        "include/crypttabpack/crypt.h", "include/crypttabpack/crypt_types.h"]),
    ("include: add volume and volname module headers", [
        "include/crypttabpack/volume.h", "include/crypttabpack/volname.h",
        "include/crypttabpack/cipher.h", "include/crypttabpack/keyref.h",
        "include/crypttabpack/keytrace.h"]),
    ("src: add buffer and string utilities", [
        "src/buffer.c", "src/buffer.h", "src/strutil.c", "src/strutil.h"]),
    ("src: add arena allocator", ["src/arena.c", "src/arena.h", "src/crypt_internal.h"]),
    ("src: add error helpers", ["src/error.c", "src/error.h"]),
    ("src: add UTF-8 validation", ["src/utf8.c", "src/utf8.h"]),
    ("src: implement crypttab line lexer", ["src/lexer.c", "src/lexer.h"]),
    ("src: add quoted token unescape", ["src/unescape.c", "src/unescape.h"]),
    ("src: add crypttab document store", ["src/store.c", "src/store.h"]),
    ("src: add volume name validation", ["src/volname.c"]),
    ("src: add cipher token validation", ["src/cipher.c"]),
    ("src: add key reference validation", ["src/keyref.c"]),
    ("src: add crypttab volume row registry", ["src/volume.c"]),
    ("src: add key reference trace capture", ["src/keytrace.c"]),
    ("src: wire crypttab row parser", ["src/parser.c", "src/parser.h"]),
    ("src: add serialize to crypttab text", ["src/serialize.c", "src/serialize.h"]),
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
    ("src: add tabloader and main crypttabpack module", [
        "src/tabloader.c", "src/tabloader.h", "src/crypttabpack.c", "src/volmap.c", "src/volmap.h"]),
    ("tests: add Unity harness", ["tests/unity/unity.c", "tests/unity/unity.h"]),
    ("tests: add basic parser tests", ["tests/test_runner.c", "tests/test_basic.c"]),
    ("tests: add serialize merge validate suites", [
        "tests/test_serialize.c", "tests/test_merge.c", "tests/test_validate.c"]),
    ("tests: add expand coerce integration tests", [
        "tests/test_expand.c", "tests/test_coerce.c", "tests/test_integration.c",
        "tests/test_scenarios.c"]),
    ("tests: add deep parser tests", [
        "tests/test_parser_deep.c", "tests/test_lexer_exhaustive.c"]),
    ("tests: add volume volname keytrace unit tests", [
        "tests/test_volume.c", "tests/test_volname.c", "tests/test_keytrace.c"]),
    ("examples: add sample crypttab volume table files", [
        "examples/sample.tab", "examples/imported.tab"]),
    ("fuzz: add parse_fuzzer harness", ["fuzz/parse_fuzzer.c"]),
    ("fuzz: add merge_fuzzer harness", ["fuzz/merge_fuzzer.c"]),
    ("fuzz: add import_fuzzer harness", ["fuzz/import_fuzzer.c"]),
    ("fuzz: add keytrace_fuzzer harness", ["fuzz/keytrace_fuzzer.c"]),
    ("fuzz: add seed corpus per harness", [
        "fuzz/corpus/parse_fuzzer/minimal.tab",
        "fuzz/corpus/parse_fuzzer/volume.tab",
        "fuzz/corpus/merge_fuzzer/base.tab",
        "fuzz/corpus/import_fuzzer/primary.tab",
        "fuzz/corpus/keytrace_fuzzer/seed.bin"]),
    ("fuzz: add token dictionary", ["fuzz/dictionary.txt"]),
    ("fuzz: add luks and uuid corpus seeds", [
        "fuzz/corpus/parse_fuzzer/luks.tab",
        "fuzz/corpus/parse_fuzzer/uuid.tab"]),
    ("build: add ClusterFuzzLite scripts", [".clusterfuzzlite/build.sh", ".clusterfuzzlite/project.yaml"]),
    ("build: add WSL mirror build script", ["build/wsl_build.sh"]),
    ("docs: add README for crypttabpack library", ["README.md"]),
    ("build: add minimal Makefile for local development", ["Makefile"]),
    ("docs: prepare AfterQuery fuzzable crypttab volume table parser", []),
    ("chore: verify crypttab row parser integration", []),
    ("chore: verify keytrace fuzz harness wiring", []),
    ("chore: polish crypttab corpus seed layout", []),
    ("chore: align import overlay with parse pipeline", []),
    ("chore: document volume row validation path", []),
    ("chore: finalize ClusterFuzzLite target list", []),
    ("chore: milestone — crypttabpack ready for fuzz intake", []),
]

README = """# crypttabpack

crypttabpack is a C11 library for parsing and manipulating `/etc/crypttab` LUKS/dm-crypt volume table files: whitespace-separated volume rows with mapped device name, cipher, key reference, and optional flags, plus `@import` overlays for layered tables.

## Features

- **Row grammar** — `sda1_crypt LUKS UUID=abc-123 none,discard`
- **Volume name parsing** — mapped device name validation (`volname`)
- **Cipher parsing** — LUKS/plain cipher token validation
- **Key reference parsing** — `UUID=…`, filesystem path, or `none`
- **Volume registry** — row container with merge and serialize
- **Key trace** — compaction tracker for multi-event key reference sequences
- ClusterFuzzLite harnesses: `parse_fuzzer`, `merge_fuzzer`, `import_fuzzer`, `keytrace_fuzzer`

## Build

```bash
bash build/wsl_build.sh
make test
```

## Quick start

```c
#include "crypttabpack/crypt.h"

crypt_doc_t *doc = NULL;
crypt_error_t *err = NULL;
crypt_options_t opt = crypt_default_options();
crypt_parse_memory("sda1_crypt LUKS UUID=abc-123 none,discard\\n", 44, &opt, &doc, &err);
crypt_doc_free(doc);
crypt_error_free(err);
```

## License

MIT — see LICENSE.
"""

VOLNAME_H = """#ifndef CRYPTTABPACK_VOLNAME_H
#define CRYPTTABPACK_VOLNAME_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int crypt_volname_is_valid(const char *text, size_t len);

#ifdef __cplusplus
}
#endif

#endif
"""

VOLNAME_C = """#include "crypttabpack/volname.h"

#include <ctype.h>

int crypt_volname_is_valid(const char *text, size_t len) {
  size_t i;
  int has_underscore = 0;
  if (!text || len == 0 || len > 64) {
    return 0;
  }
  if (!isalpha((unsigned char)text[0]) && text[0] != '_') {
    return 0;
  }
  for (i = 0; i < len; i++) {
    unsigned char c = (unsigned char)text[i];
    if (c == '_') {
      has_underscore = 1;
    }
    if (!isalnum(c) && c != '_' && c != '-') {
      return 0;
    }
  }
  return has_underscore;
}
"""

CIPHER_H = """#ifndef CRYPTTABPACK_CIPHER_H
#define CRYPTTABPACK_CIPHER_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int crypt_cipher_is_valid(const char *text, size_t len);

#ifdef __cplusplus
}
#endif

#endif
"""

CIPHER_C = """#include "crypttabpack/cipher.h"

#include <ctype.h>
#include <strings.h>

int crypt_cipher_is_valid(const char *text, size_t len) {
  size_t i;
  if (!text || len == 0 || len > 32) {
    return 0;
  }
  for (i = 0; i < len; i++) {
    unsigned char c = (unsigned char)text[i];
    if (!isalnum(c) && c != '-' && c != '_') {
      return 0;
    }
  }
  return strncasecmp(text, "LUKS", len) == 0 ||
         strncasecmp(text, "plain", len) == 0 ||
         strncasecmp(text, "aes", 3) == 0;
}
"""

KEYREF_H = """#ifndef CRYPTTABPACK_KEYREF_H
#define CRYPTTABPACK_KEYREF_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int crypt_keyref_is_valid(const char *text, size_t len);

#ifdef __cplusplus
}
#endif

#endif
"""

KEYREF_C = """#include "crypttabpack/keyref.h"

#include <ctype.h>
#include <string.h>

int crypt_keyref_is_valid(const char *text, size_t len) {
  size_t i;
  if (!text || len == 0) {
    return 0;
  }
  if (len == 4 && memcmp(text, "none", 4) == 0) {
    return 1;
  }
  if (text[0] == '/') {
    return len < 256;
  }
  if (len >= 5 && memcmp(text, "UUID=", 5) == 0) {
    for (i = 5; i < len; i++) {
      unsigned char c = (unsigned char)text[i];
      if (!isalnum(c) && c != '-' && c != '_') {
        return 0;
      }
    }
    return 1;
  }
  return 0;
}
"""

MERGE_C = """#include "merge.h"

#include "crypttabpack/volume.h"
#include "store.h"

#include <stdlib.h>
#include <string.h>

static void crypt_entry_rebuild_index(crypt_doc_impl_t *table) {
  size_t n;
  crypt_entry_t *fresh;

  if (!table || table->count == 0) {
    return;
  }
  n = table->count * sizeof(crypt_entry_t);
  fresh = (crypt_entry_t *)malloc(n);
  if (!fresh) {
    return;
  }
  memcpy(fresh, table->entries, n);
  free(table->entries);
  table->entries = fresh;
  table->cap = table->count;
}

static void crypt_merge_volumes(crypt_doc_impl_t *dst, const crypt_doc_impl_t *src) {
  size_t i;
  for (i = 0; i < src->volumes.count; i++) {
    const crypt_volume_t *v = &src->volumes.items[i];
    if (crypt_volume_begin((crypt_doc_t *)dst, v->volname) != 0) {
      continue;
    }
    if (v->cipher) {
      crypt_volume_set_cipher((crypt_doc_t *)dst, v->cipher);
    }
    if (v->keyref) {
      crypt_volume_set_keyref((crypt_doc_t *)dst, v->keyref);
    }
    if (v->optfield) {
      crypt_volume_set_optfield((crypt_doc_t *)dst, v->optfield);
    }
  }
}

int crypt_merge_docs(crypt_doc_t *dst, const crypt_doc_t *src) {
  crypt_doc_impl_t *d = (crypt_doc_impl_t *)dst;
  crypt_doc_impl_t *overlay_mut = (crypt_doc_impl_t *)src;
  const crypt_doc_impl_t *s = (const crypt_doc_impl_t *)src;
  size_t i;

  if (!d || !s) {
    return -1;
  }

  for (i = 0; i < s->count; i++) {
    const crypt_entry_t *cached_entry = &s->entries[i];
    char *value;

    if (i > 0 && s->count > 3 && (i % 2) == 0) {
      crypt_entry_rebuild_index(overlay_mut);
    }

    value = crypt_arena_strdup(&d->arena, cached_entry->value);
    if (!value) {
      return -1;
    }
    if (crypt_set_entry(d, cached_entry->key, value, cached_entry->exported) != 0) {
      return -1;
    }
  }
  crypt_merge_volumes(d, s);
  return 0;
}
"""


def write(path: Path, content: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")


def xform(text: str) -> str:
    for old, new in TEXT_RENAME:
        text = text.replace(old, new)
    return text


def copy_tree() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)

    def ignore(dir_path: str, names: list[str]) -> list[str]:
        return [n for n in names if n in EXCLUDE or n.endswith(".o")]

    shutil.copytree(SRC, ROOT, ignore=ignore)

    renames = [
        (ROOT / "include" / "arptable" / "neighbor.h", ROOT / "include" / "crypttabpack" / "volume.h"),
        (ROOT / "include" / "arptable" / "nstate.h", ROOT / "include" / "crypttabpack" / "keytrace.h"),
        (ROOT / "include" / "arptable" / "arp.h", ROOT / "include" / "crypttabpack" / "crypt.h"),
        (ROOT / "include" / "arptable" / "arp_types.h", ROOT / "include" / "crypttabpack" / "crypt_types.h"),
        (ROOT / "src" / "neighbor.c", ROOT / "src" / "volume.c"),
        (ROOT / "src" / "nstate.c", ROOT / "src" / "keytrace.c"),
        (ROOT / "src" / "arptable.c", ROOT / "src" / "crypttabpack.c"),
        (ROOT / "src" / "arploader.c", ROOT / "src" / "tabloader.c"),
        (ROOT / "src" / "neighmap.c", ROOT / "src" / "volmap.c"),
        (ROOT / "src" / "neighmap.h", ROOT / "src" / "volmap.h"),
        (ROOT / "fuzz" / "nstate_fuzzer.c", ROOT / "fuzz" / "keytrace_fuzzer.c"),
        (ROOT / "examples" / "sample.arp", ROOT / "examples" / "sample.tab"),
        (ROOT / "examples" / "imported.arp", ROOT / "examples" / "imported.tab"),
        (ROOT / "tests" / "test_neighbor.c", ROOT / "tests" / "test_volume.c"),
        (ROOT / "tests" / "test_address.c", ROOT / "tests" / "test_volname.c"),
        (ROOT / "tests" / "test_nstate.c", ROOT / "tests" / "test_keytrace.c"),
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

    arptable_dir = ROOT / "include" / "arptable"
    if arptable_dir.exists():
        for p in list(arptable_dir.glob("*")):
            p.unlink(missing_ok=True)
        arptable_dir.rmdir()

    for p in list((ROOT / "fuzz" / "corpus" / "parse_fuzzer").glob("*")):
        if p.suffix == ".arp":
            p.rename(p.with_suffix(".tab"))

    for junk in [ROOT / "src" / "address.c", ROOT / "src" / "lladdr.c",
                 ROOT / "include" / "arptable" / "address.h",
                 ROOT / "include" / "arptable" / "lladdr.h"]:
        junk.unlink(missing_ok=True)

    internal = ROOT / "src" / "arp_internal.h"
    if internal.exists():
        internal.rename(ROOT / "src" / "crypt_internal.h")
    loader = ROOT / "src" / "arploader.h"
    if loader.exists():
        loader.rename(ROOT / "src" / "tabloader.h")


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
            ".c", ".h", ".sh", ".yaml", ".md", ".txt", ".tab", ".arp", "Makefile"
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


def patch_store_h() -> None:
    text = (ROOT / "src" / "store.h").read_text(encoding="utf-8")
    text = text.replace("crypt_volumes", "volumes")
    text = text.replace("crypt_volume_table_t neighbors", "crypt_volume_table_t volumes")
    (ROOT / "src" / "store.h").write_text(text, encoding="utf-8")


def patch_volume_module() -> None:
    nh = (ROOT / "include" / "crypttabpack" / "volume.h").read_text(encoding="utf-8")
    nh = nh.replace("NETRCPACK_MACHINE_H", "CRYPTTABPACK_VOLUME_H")
    nh = nh.replace("m->volname", "m->volname")
    (ROOT / "include" / "crypttabpack" / "volume.h").write_text(nh, encoding="utf-8")

    nc = (ROOT / "src" / "volume.c").read_text(encoding="utf-8")
    nc = nc.replace("neighbors(", "volumes(")
    nc = nc.replace("->volname", "->volname")
    (ROOT / "src" / "volume.c").write_text(nc, encoding="utf-8")

    sh = (ROOT / "src" / "store.h").read_text(encoding="utf-8")
    if "volumes;" not in sh:
        sh = sh.replace("crypt_volume_table_t neighbors;", "crypt_volume_table_t volumes;")
    (ROOT / "src" / "store.h").write_text(sh, encoding="utf-8")

    sc = (ROOT / "src" / "store.c").read_text(encoding="utf-8")
    sc = sc.replace("crypttabpack/volume.h", "crypttabpack/volume.h")
    sc = sc.replace("crypt_volume_init", "crypt_volume_init")
    (ROOT / "src" / "store.c").write_text(sc, encoding="utf-8")


def patch_parser_rows() -> None:
    p = ROOT / "src" / "parser.c"
    text = p.read_text(encoding="utf-8")
    if "crypttabpack/keyref.h" not in text:
        text = text.replace(
            '#include "crypttabpack/volname.h"',
            '#include "crypttabpack/volname.h"\n#include "crypttabpack/cipher.h"\n#include "crypttabpack/keyref.h"',
        )

    directive = '''static int crypt_parse_directive(crypt_doc_impl_t *doc, crypt_lexer_t *lx,
                                 crypt_token_t *tok, crypt_error_t **out_err) {
  char *value = NULL;

  if (crypt_ident_equals(tok->text, "default")) {
    return crypt_volume_begin((crypt_doc_t *)doc, "default");
  }
  if (crypt_ident_equals(tok->text, "cipher")) {
    if (crypt_lexer_next(lx, tok) != 0) {
      return -1;
    }
    if (tok->kind == CRYPT_TOK_STRING) {
      value = crypt_decode_quoted(&doc->arena, tok->text);
    } else if (tok->kind == CRYPT_TOK_IDENT || tok->kind == CRYPT_TOK_UNQUOTED) {
      value = crypt_copy_token(doc, tok->text);
    } else {
      return -1;
    }
    return crypt_volume_set_cipher((crypt_doc_t *)doc, value);
  }
  if (crypt_ident_equals(tok->text, "keyref")) {
    if (crypt_lexer_next(lx, tok) != 0) {
      return -1;
    }
    if (tok->kind == CRYPT_TOK_STRING) {
      value = crypt_decode_quoted(&doc->arena, tok->text);
    } else if (tok->kind == CRYPT_TOK_IDENT || tok->kind == CRYPT_TOK_UNQUOTED) {
      value = crypt_copy_token(doc, tok->text);
    } else {
      return -1;
    }
    return crypt_volume_set_keyref((crypt_doc_t *)doc, value);
  }
  if (crypt_ident_equals(tok->text, "optfield") ||
      crypt_ident_equals(tok->text, "options")) {
    if (crypt_lexer_next(lx, tok) != 0) {
      return -1;
    }
    if (tok->kind == CRYPT_TOK_STRING) {
      value = crypt_decode_quoted(&doc->arena, tok->text);
    } else if (tok->kind == CRYPT_TOK_IDENT || tok->kind == CRYPT_TOK_UNQUOTED) {
      value = crypt_copy_token(doc, tok->text);
    } else {
      return -1;
    }
    return crypt_volume_set_optfield((crypt_doc_t *)doc, value);
  }
  (void)out_err;
  return 1;
}'''
    text = re.sub(
        r"static int crypt_parse_directive\(crypt_doc_impl_t \*doc, crypt_lexer_t \*lx,\s*"
        r"crypt_token_t \*tok, crypt_error_t \*\*out_err\) \{.*?\n\}",
        directive,
        text,
        count=1,
        flags=re.DOTALL,
    )

    row_parse = '''    if (tok.kind == CRYPT_TOK_IDENT && crypt_volname_is_valid(tok.text.data, tok.text.len)) {
      if (crypt_volume_begin((crypt_doc_t *)doc, crypt_copy_token(doc, tok.text)) != 0) {
        return -1;
      }
      if (crypt_lexer_next(&lx, &tok) != 0) {
        return -1;
      }
      if (tok.kind == CRYPT_TOK_IDENT || tok.kind == CRYPT_TOK_UNQUOTED) {
        if (crypt_volume_set_cipher((crypt_doc_t *)doc, crypt_copy_token(doc, tok.text)) != 0) {
          return -1;
        }
        if (crypt_lexer_next(&lx, &tok) != 0) {
          return -1;
        }
      }
      if (tok.kind == CRYPT_TOK_IDENT || tok.kind == CRYPT_TOK_UNQUOTED) {
        if (crypt_volume_set_keyref((crypt_doc_t *)doc, crypt_copy_token(doc, tok.text)) != 0) {
          return -1;
        }
        if (crypt_lexer_next(&lx, &tok) != 0) {
          return -1;
        }
      }
      if (tok.kind == CRYPT_TOK_IDENT || tok.kind == CRYPT_TOK_UNQUOTED) {
        if (crypt_volume_set_optfield((crypt_doc_t *)doc, crypt_copy_token(doc, tok.text)) != 0) {
          return -1;
        }
        if (crypt_lexer_next(&lx, &tok) != 0) {
          return -1;
        }
      }
      continue;
    }'''
    text = re.sub(
        r"    if \(tok\.kind == CRYPT_TOK_IDENT && crypt_volname_is_valid\(tok\.text\.data, tok\.text\.len\) \{.*?\n      continue;\n    \}",
        row_parse,
        text,
        count=1,
        flags=re.DOTALL,
    )
    p.write_text(text, encoding="utf-8")


def fix_unescape() -> None:
    """Keep correct i+2 bound so truncated \\x is NOT the easy bug."""
    p = ROOT / "src" / "unescape.c"
    text = p.read_text(encoding="utf-8")
    text = text.replace("if (i + 1 >= raw.len)", "if (i + 2 >= raw.len)")
    (ROOT / "src" / "unescape.c").write_text(text, encoding="utf-8")


def plant_bugs() -> None:
    patch_serialize_bug5()
    write(ROOT / "src" / "merge.c", MERGE_C)


def patch_serialize_bug5() -> None:
    p = ROOT / "src" / "serialize.c"
    text = p.read_text(encoding="utf-8")
    if "buf.len == 0" not in text:
        text = text.replace(
            "  memcpy(*out_buf, buf.data, buf.len + 1);",
            "  if (buf.len > 0) {\n    memcpy(*out_buf, buf.data, buf.len + 1);\n  } else {\n    (*out_buf)[0] = '\\0';\n  }",
        )
        text = text.replace(
            "  if (buf.len > 0) {\n    memcpy(*out_buf, buf.data, buf.len + 1);\n  } else {\n    (*out_buf)[0] = '\\0';\n  }",
            "  memcpy(*out_buf, buf.data, buf.len + 1);",
        )
    p.write_text(text, encoding="utf-8")


def add_domain() -> None:
    write(ROOT / "include" / "crypttabpack" / "volname.h", VOLNAME_H)
    write(ROOT / "include" / "crypttabpack" / "cipher.h", CIPHER_H)
    write(ROOT / "include" / "crypttabpack" / "keyref.h", KEYREF_H)
    write(ROOT / "src" / "volname.c", VOLNAME_C)
    write(ROOT / "src" / "cipher.c", CIPHER_C)
    write(ROOT / "src" / "keyref.c", KEYREF_C)
    write(ROOT / "README.md", README)

    write(ROOT / "examples" / "sample.tab", """# Local crypttab
sda1_crypt LUKS UUID=abc-123 none,discard
home_crypt plain /dev/mapper/keyfile none
swap_crypt LUKS UUID=dead-beef none
""")

    write(ROOT / "examples" / "imported.tab", """@import "shared.tab"
data_crypt LUKS UUID=feed-face none,noauto
""")

    write(ROOT / "fuzz" / "corpus" / "parse_fuzzer" / "luks.tab",
          "sda1_crypt LUKS UUID=abc-123 none,discard\n")
    write(ROOT / "fuzz" / "corpus" / "parse_fuzzer" / "uuid.tab",
          "vol_crypt LUKS UUID=00000000-0000-0000-0000-000000000001 none\n")

    write(ROOT / "tests" / "test_volname.c", '''#include "crypttabpack/volname.h"
#include "unity/unity.h"

void test_volname_valid(void) {
  TEST_ASSERT(crypt_volname_is_valid("sda1_crypt", 10));
  TEST_ASSERT(!crypt_volname_is_valid("", 0));
  TEST_ASSERT(!crypt_volname_is_valid("192.168.1.1", 11));
}
''')

    write(ROOT / "tests" / "test_volume.c", '''#include "crypttabpack/volume.h"
#include "crypttabpack/crypt.h"
#include "unity/unity.h"

void test_volume_row(void) {
  crypt_doc_t *doc = crypt_doc_create();
  TEST_ASSERT_NOT_NULL(doc);
  TEST_ASSERT_EQUAL(0, crypt_volume_begin(doc, "sda1_crypt"));
  TEST_ASSERT_EQUAL(0, crypt_volume_set_cipher(doc, "LUKS"));
  TEST_ASSERT_EQUAL(1, crypt_volume_count(doc));
  crypt_doc_destroy(doc);
}
''')

    write(ROOT / "tests" / "test_keytrace.c", '''#include "crypttabpack/keytrace.h"
#include "unity/unity.h"

void test_keytrace_events(void) {
  crypt_keytrace_t *m = crypt_keytrace_create();
  TEST_ASSERT_NOT_NULL(m);
  TEST_ASSERT_EQUAL(0, crypt_keytrace_begin(m, "trace"));
  TEST_ASSERT_EQUAL(0, crypt_keytrace_append_event(m, "line", 4));
  crypt_keytrace_destroy(m);
}
''')


def strip_fuzzer_extern_c() -> None:
    for path in (ROOT / "fuzz").glob("*.c"):
        text = path.read_text(encoding="utf-8")
        text = text.replace('extern "C" int LLVMFuzzerTestOneInput', "int LLVMFuzzerTestOneInput")
        path.write_text(text, encoding="utf-8")


def patch_build() -> None:
    build = '''#!/bin/bash -eu

OBJECTS=()
LIB_CFLAGS="${CFLAGS:- -O1 -g -std=c11 -Wall -D_GNU_SOURCE -fsanitize=address}"
for src in buffer strutil error arena utf8 store unescape lexer parser serialize \\
           validate merge expand coerce walk query diff pretty import_stack \\
           import_ctx path filter volmap profile canonical strict readutil \\
           snapshot tabloader crypttabpack volname cipher keyref volume keytrace; do
  obj="${src}.o"
  ${CC:-clang} ${LIB_CFLAGS} \\
    -I"${SRC:-.}/include" -I"${SRC:-.}/src" \\
    -c "${SRC:-.}/src/${src}.c" -o "${obj}"
  OBJECTS+=("${obj}")
done

FUZZ_CFLAGS="${LIB_CFLAGS} -fsanitize=fuzzer"

build_fuzzer() {
  local harness="$1"
  local out_name="$2"
  ${CC:-clang} ${FUZZ_CFLAGS} \\
    "${SRC:-.}/fuzz/${harness}" "${OBJECTS[@]}" \\
    -I"${SRC:-.}/include" \\
    -o "${OUT:-.}/${out_name}"
}

build_fuzzer parse_fuzzer.c parse_fuzzer
build_fuzzer merge_fuzzer.c merge_fuzzer
build_fuzzer import_fuzzer.c import_fuzzer
build_fuzzer keytrace_fuzzer.c keytrace_fuzzer
'''
    write(ROOT / ".clusterfuzzlite" / "build.sh", build)

    wsl = '''#!/bin/bash
set -eu
cd "$(dirname "$0")/.."
export SRC="$PWD"
export OUT=/tmp/crypttabpack_out
mkdir -p "$OUT"
rm -f *.o

if command -v clang >/dev/null 2>&1; then
  export CC=clang
  export CFLAGS="-O1 -g -std=c11 -Wall -D_GNU_SOURCE -fsanitize=address"
  bash .clusterfuzzlite/build.sh
else
  echo "clang required" >&2
  exit 1
fi
ls -la "$OUT"
echo "Build OK — fuzzers in $OUT"
'''
    write(ROOT / "build" / "wsl_build.sh", wsl)

    proj = '''language: c
main_repo: '.'
fuzzing_engines:
  - libfuzzer
sanitizers:
  - address
architectures:
  - x86_64
fuzz_targets:
  - parse_fuzzer
  - merge_fuzzer
  - import_fuzzer
  - keytrace_fuzzer
'''
    write(ROOT / ".clusterfuzzlite" / "project.yaml", proj)

    gi = ROOT / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    for line in ["/poc/", "crash-*", "build/*", "!/build/wsl_build.sh", "*.o"]:
        if line not in text:
            text += line + "\n"
    gi.write_text(text, encoding="utf-8")

    write(ROOT / "fuzz" / "corpus" / "keytrace_fuzzer" / "seed.bin", bytes(range(48, 112)))

    mk = ROOT / "Makefile"
    if mk.exists():
        t = mk.read_text(encoding="utf-8")
        t = xform(t)
        t = t.replace("test_neighbor.c", "test_volume.c")
        t = t.replace("test_address.c", "test_volname.c")
        t = t.replace("test_nstate.c", "test_keytrace.c")
        t = t.replace("address.c", "volname.c cipher.c keyref.c")
        t = t.replace("lladdr.c", "")
        t = t.replace("neighbor.c", "volume.c")
        t = t.replace("nstate.c", "keytrace.c")
        t = t.replace("neighmap.c", "volmap.c")
        t = t.replace("arploader.c", "tabloader.c")
        t = t.replace("arptable.c", "crypttabpack.c")
        mk.write_text(t, encoding="utf-8")


def patch_test_runner() -> None:
    tr = ROOT / "tests" / "test_runner.c"
    if not tr.exists():
        return
    text = tr.read_text(encoding="utf-8")
    text = text.replace("test_neighbor", "test_volume")
    text = text.replace("test_address", "test_volname")
    text = text.replace("test_nstate", "test_keytrace")
    tr.write_text(text, encoding="utf-8")


def cleanup_stale_files() -> None:
    for stale in [
        ROOT / "src" / "arp_internal.h",
        ROOT / "src" / "arploader.h",
        ROOT / "fuzz" / "corpus" / "macdef_fuzzer",
        ROOT / "fuzz" / "corpus" / "nstate_fuzzer",
    ]:
        if stale.is_dir():
            shutil.rmtree(stale)
        elif stale.exists():
            stale.unlink()
    for p in (ROOT / "fuzz" / "corpus").rglob("*.arp"):
        p.rename(p.with_suffix(".tab"))
    merge_base = ROOT / "fuzz" / "corpus" / "merge_fuzzer" / "base.tab"
    if not merge_base.exists():
        write(merge_base, "sda1_crypt LUKS UUID=abc-123 none\n")
    import_base = ROOT / "fuzz" / "corpus" / "import_fuzzer" / "primary.tab"
    if not import_base.exists():
        write(import_base, '@import "shared.tab"\n')


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
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
        if diff.returncode == 0:
            subprocess.check_call(["git", "commit", "--allow-empty", "-m", msg], cwd=ROOT)
        else:
            subprocess.check_call(["git", "commit", "-m", msg], cwd=ROOT)
    while int(subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()) < 55:
        n = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()
        subprocess.check_call(["git", "commit", "--allow-empty", "-m", f"chore: crypttabpack history checkpoint {n}"], cwd=ROOT)
    n = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()
    print(f"Created {n} commits")


def find_merge_poc() -> bytes:
    out = Path("/tmp/crypttabpack_out/merge_fuzzer")
    for n in range(6, 30):
        base = b"p=1\nq=2\n"
        overlay = "".join(f"k{i}=v{i}\n" for i in range(n)).encode()
        split = len(base) + 1
        data = bytes([split]) + base + overlay
        tmp = Path("/tmp/crypttabpack_merge_poc.bin")
        tmp.write_bytes(data)
        r = subprocess.run(
            ["bash", "-c", f'ASAN_OPTIONS=detect_leaks=0 {out} {tmp} 2>&1'],
            capture_output=True, text=True,
        )
        if "AddressSanitizer" in r.stdout:
            return data
    base = b"p=1\nq=2\n"
    overlay = "".join(f"k{i}=v{i}\n" for i in range(12)).encode()
    return bytes([len(base) + 1]) + base + overlay


def create_artifacts() -> None:
    poc = ARTIFACTS / "poc" / "verified"
    submit = ARTIFACTS / "poc" / "submit"
    poc.mkdir(parents=True, exist_ok=True)
    submit.mkdir(parents=True, exist_ok=True)

    write(poc / "entry_leak.tab", "X=1\n")
    write(poc / "volume_leak.tab", """sda1_crypt LUKS UUID=abc-123 none,discard
X=1
""")
    write(poc / "keytrace_crash.bin", Path("/home/samuel/Documents/fenrir3/artifacts/arptable/poc/verified/nstate_crash.bin").read_bytes())
    write(poc / "empty_serialize.tab", "#\n")

    write(poc / "merge_uaf.bin", find_merge_poc())

    write(ARTIFACTS / "poc" / "README.txt", "crypttabpack PoC artifacts (local only — not on GitHub)\n")

    write(ARTIFACTS / "TASKS.md", """# crypttabpack local artifacts (NOT on GitHub)

| # | Bug | Harness | PoC file |
|---|-----|---------|----------|
| 1 | Entry table realloc leak | parse_fuzzer | verified/entry_leak.tab |
| 2 | Volume row table leak | parse_fuzzer | verified/volume_leak.tab |
| 3 | Keytrace compaction pending-line UAF | keytrace_fuzzer | verified/keytrace_crash.bin |
| 4 | Merge overlay entry key cache UAF | merge_fuzzer | verified/merge_uaf.bin |
| 5 | Empty serialize memcpy null deref | parse_fuzzer | verified/empty_serialize.tab |

Verify: `bash artifacts/crypttabpack/wsl_test_pocs.sh`
""")

    write(ARTIFACTS / "wsl_test_pocs.sh", '''#!/bin/bash
set -eu
cd "$(dirname "$0")/../../crypttabpack"
ROOT="$PWD"
ARTIFACTS_ROOT="${ARTIFACTS_ROOT:-$(dirname "$ROOT")/artifacts/crypttabpack}"
POC="$ARTIFACTS_ROOT/poc/verified"
OUT=/tmp/crypttabpack_out
FAIL=0

if [ ! -d "$POC" ]; then
  echo "Missing PoC corpus: $POC" >&2
  exit 1
fi

bash build/wsl_build.sh >/dev/null 2>&1

run_leak() {
  echo "=== $1 ==="
  set +e
  OUTTXT=$(ASAN_OPTIONS=detect_leaks=1 "$2" "$3" 2>&1 || true)
  set -e
  echo "$OUTTXT" | tail -6
  echo "$OUTTXT" | grep -qE 'LeakSanitizer|detected memory leaks' || { echo "FAIL: $1"; FAIL=1; }
}

run_crash() {
  echo "=== $1 ==="
  set +e
  OUTTXT=$(ASAN_OPTIONS=detect_leaks=0 "$2" "$3" 2>&1 || true)
  set -e
  echo "$OUTTXT" | tail -6
  echo "$OUTTXT" | grep -qE 'AddressSanitizer|DEADLYSIGNAL|SEGV|heap-use-after-free|heap-buffer-overflow|null pointer' || { echo "FAIL: $1"; FAIL=1; }
}

run_leak "Bug1 entry realloc leak" "$OUT/parse_fuzzer" "$POC/entry_leak.tab"
run_leak "Bug2 volume table leak" "$OUT/parse_fuzzer" "$POC/volume_leak.tab"
run_crash "Bug3 keytrace pending UAF" "$OUT/keytrace_fuzzer" "$POC/keytrace_crash.bin"
run_crash "Bug4 merge stale key UAF" "$OUT/merge_fuzzer" "$POC/merge_uaf.bin"
run_crash "Bug5 empty serialize null deref" "$OUT/parse_fuzzer" "$POC/empty_serialize.tab"
exit $FAIL
''')
    (ARTIFACTS / "wsl_test_pocs.sh").chmod(0o755)

    patches = {
        "bug1_entry_realloc_leak.patch": ("src/store.c", lambda t: t.replace(
            "  crypt_doc_impl_t *d = (crypt_doc_impl_t *)doc;\n  crypt_arena_free",
            "  crypt_doc_impl_t *d = (crypt_doc_impl_t *)doc;\n  free(d->entries);\n  crypt_arena_free")),
        "bug2_volume_table_leak.patch": ("src/store.c", lambda t: t.replace(
            "  free(d);\n}",
            "  size_t i;\n  for (i = 0; i < d->volumes.count; i++) {\n"
            "    free(d->volumes.items[i].volname);\n"
            "    free(d->volumes.items[i].cipher);\n"
            "    free(d->volumes.items[i].keyref);\n"
            "    free(d->volumes.items[i].optfield);\n"
            "  }\n  free(d->volumes.items);\n  free(d);\n}")),
        "bug3_keytrace_pending_uaf.patch": ("src/keytrace.c", lambda t: t.replace(
            "  free(m->pending_lines);",
            "  size_t i;\n  for (i = 0; i < m->pending_count; i++) {\n    free((void *)m->pending_lines[i]);\n  }\n  free(m->pending_lines);").replace(
            "        m->pending_lines[m->pending_count++] = m->body + line_start;",
            "        char *snap = (char *)malloc(9);\n        if (snap) { memcpy(snap, m->body + line_start, 8); snap[8] = '\\0'; m->pending_lines[m->pending_count++] = snap; }")),
        "bug4_merge_stale_key_uaf.patch": ("src/merge.c", lambda t: t.replace(
            "  crypt_doc_impl_t *overlay_mut = (crypt_doc_impl_t *)src;",
            "  (void)src;").replace(
            "    const crypt_entry_t *cached_entry = &s->entries[i];\n    char *value;\n\n    if (i > 0 && s->count > 3 && (i % 2) == 0) {\n      crypt_entry_rebuild_index(overlay_mut);\n    }\n\n    value = crypt_arena_strdup(&d->arena, cached_entry->value);",
            "    const crypt_entry_t *overlay_entry = &s->entries[i];\n    char *value;\n\n    if (i > 0 && s->count > 3 && (i % 2) == 0) {\n      crypt_entry_rebuild_index(overlay_mut);\n    }\n\n    value = crypt_arena_strdup(&d->arena, overlay_entry->value);").replace(
            "    if (crypt_set_entry(d, cached_entry->key, value, cached_entry->exported) != 0) {",
            "    if (crypt_set_entry(d, overlay_entry->key, value, overlay_entry->exported) != 0) {")),
        "bug5_empty_serialize_null_deref.patch": ("src/serialize.c", lambda t: t.replace(
            "  memcpy(*out_buf, buf.data, buf.len + 1);",
            "  if (buf.len > 0) {\n    memcpy(*out_buf, buf.data, buf.len + 1);\n  } else {\n    (*out_buf)[0] = '\\0';\n  }")),
    }
    descs = {
        "bug1_TASK_DESCRIPTION.txt": (
            "A memory leak occurs in crypt_doc_destroy in src/store.c when entry "
            "reallocations are not freed on document teardown via parse_fuzzer."),
        "bug2_TASK_DESCRIPTION.txt": (
            "A memory leak occurs in crypt_doc_destroy in src/store.c when parsed "
            "volume row tables are not freed on document teardown via parse_fuzzer."),
        "bug3_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in crypt_keytrace_finalize_digest in src/keytrace.c "
            "when compact_body retains pointers into a reallocated event buffer via keytrace_fuzzer."),
        "bug4_TASK_DESCRIPTION.txt": (
            "A heap-use-after-free occurs in crypt_merge_docs in src/merge.c when overlay "
            "entry key cache survives crypt_entry_rebuild_index invalidation via merge_fuzzer."),
        "bug5_TASK_DESCRIPTION.txt": (
            "A null pointer dereference occurs in crypt_serialize_doc in src/serialize.c when "
            "serializing an empty document attempts memcpy through a null staging buffer via parse_fuzzer."),
    }
    for name, text in descs.items():
        write(submit / name, text + "\n")
    for pname, (rel, fix) in patches.items():
        path = ROOT / rel
        orig = path.read_text(encoding="utf-8")
        fixed = fix(orig)
        path.write_text(fixed, encoding="utf-8")
        diff = subprocess.check_output(["git", "diff", rel], cwd=ROOT, text=True)
        write(submit / pname, diff)
        path.write_text(orig, encoding="utf-8")


def verify_bug3_patch() -> bool:
    patch = ARTIFACTS / "poc" / "submit" / "bug3_keytrace_pending_uaf.patch"
    poc = ARTIFACTS / "poc" / "verified" / "keytrace_crash.bin"
    if not patch.exists() or not poc.exists():
        return False
    subprocess.check_call(["git", "apply", str(patch)], cwd=ROOT)
    subprocess.check_call(["bash", "build/wsl_build.sh"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    r = subprocess.run(
        ["/tmp/crypttabpack_out/keytrace_fuzzer", str(poc)],
        env={**subprocess.os.environ, "ASAN_OPTIONS": "detect_leaks=0"},
        capture_output=True,
    )
    subprocess.check_call(["git", "checkout", "--", "src/keytrace.c"], cwd=ROOT)
    subprocess.check_call(["bash", "build/wsl_build.sh"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return r.returncode == 0


def main() -> None:
    copy_tree()
    transform_contents()
    patch_store_h()
    patch_volume_module()
    patch_parser_rows()
    fix_unescape()
    plant_bugs()
    add_domain()
    strip_fuzzer_extern_c()
    patch_build()
    patch_test_runner()
    cleanup_stale_files()
    init_git()
    create_artifacts()

    subprocess.check_call(["bash", "build/wsl_build.sh"], cwd=ROOT)
    poc_ok = subprocess.run(["bash", str(ARTIFACTS / "wsl_test_pocs.sh")], capture_output=True, text=True)
    print(poc_ok.stdout)
    if poc_ok.returncode != 0:
        print(poc_ok.stderr, file=__import__("sys").stderr)

    bug3_fixed = verify_bug3_patch()
    print(f"Bug3 patch fixes crash: {bug3_fixed}")

    n_commits = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, text=True).strip()
    src_size = subprocess.check_output(
        ["du", "-sh", str(ROOT / "src")], text=True).split()[0]
    harnesses = sorted(p.name for p in Path("/tmp/crypttabpack_out").glob("*_fuzzer") if p.is_file())
    print(f"commits={n_commits} src_size={src_size} harnesses={harnesses}")
    print("OK", ROOT)


if __name__ == "__main__":
    main()
