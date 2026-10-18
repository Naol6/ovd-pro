#!/usr/bin/env python3
"""Expand tlvpack with additional TLV tree modules, tests, and import_fuzzer."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path("/home/samuel/Documents/fenrir3/tlvpack")

MODULES = [
    "walk", "filter", "diff", "index", "query", "pretty", "profile", "canonical",
    "coerce", "expand", "path", "import_ctx", "import_stack", "snapshot", "strict",
    "readutil", "hash", "crc", "limits", "normalize", "copy", "search", "patch", "error",
]

MODULE_IMPL = '''#include "{name}.h"
#include "node.h"
#include <stdlib.h>
#include <string.h>

static int tlv_{name}_visit_node(const tlv_node_t *n, tlv_{name}_fn fn, void *ctx, uint32_t depth) {{
  size_t i;
  if (!n || !fn) return -1;
  if (fn(ctx, n, depth) != 0) return -1;
  for (i = 0; i < n->child_count; i++)
    if (tlv_{name}_visit_node(&n->children[i], fn, ctx, depth + 1) != 0) return -1;
  return 0;
}}

int tlv_{name}_walk_tree(const tlv_tree_t *tree, tlv_{name}_fn fn, void *ctx) {{
  size_t i;
  if (!tree || !fn) return -1;
  for (i = 0; i < tree->root_count; i++)
    if (tlv_{name}_visit_node(&tree->roots[i], fn, ctx, 0) != 0) return -1;
  return 0;
}}

size_t tlv_{name}_count_nodes(const tlv_tree_t *tree) {{
  size_t total = 0, i;
  if (!tree) return 0;
  for (i = 0; i < tree->root_count; i++) {{
    size_t j;
    total++;
    for (j = 0; j < tree->roots[i].child_count; j++) total += tree->roots[i].children[j].child_count + 1;
  }}
  return total;
}}

int tlv_{name}_reset(tlv_{name}_ctx_t *ctx) {{
  if (!ctx) return -1;
  ctx->seen = 0;
  ctx->last_tag = 0;
  return 0;
}}
'''

MODULE_HDR = '''#ifndef TLVPACK_{GUARD}_H
#define TLVPACK_{GUARD}_H
#include "tlvpack/tlv_node.h"
#ifdef __cplusplus
extern "C" {{
#endif
typedef struct {{ size_t seen; uint32_t last_tag; }} tlv_{name}_ctx_t;
typedef int (*tlv_{name}_fn)(void *ctx, const tlv_node_t *node, uint32_t depth);
int tlv_{name}_walk_tree(const tlv_tree_t *tree, tlv_{name}_fn fn, void *ctx);
size_t tlv_{name}_count_nodes(const tlv_tree_t *tree);
int tlv_{name}_reset(tlv_{name}_ctx_t *ctx);
#ifdef __cplusplus
}}
#endif
#endif
'''

IMPORT_FUZZER = '''#include "tlvpack/tlvpack.h"
#include <stdint.h>
#include <stdlib.h>
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  tlv_tree_t *tree = NULL;
  tlv_error_t err;
  uint8_t *out = NULL;
  size_t out_len = 0;
  size_t split;
  if (!data || size < 4 || size > 65536) return 0;
  split = 1 + (data[0] % (size - 2));
  if (tlv_parse_buffer(data + 1, split, &tree, &err) != 0) return 0;
  (void)tlv_validate_tree(tree);
  if (tlv_write_tree(tree, &out, &out_len) == 0) {
    tlv_tree_t *again = NULL;
    if (tlv_parse_buffer(out, out_len, &again, &err) == 0) {
      tlv_merge_trees(tree, again);
      tlv_tree_free(again);
      free(again);
    }
    free(out);
  }
  tlv_tree_free(tree);
  free(tree);
  return 0;
}
'''


def write(path: Path, content: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")


def add_modules() -> None:
    for name in MODULES:
        guard = name.upper()
        write(ROOT / f"src/{name}.h", MODULE_HDR.format(name=name, GUARD=guard))
        write(ROOT / f"src/{name}.c", MODULE_IMPL.format(name=name))
    write(ROOT / "fuzz/import_fuzzer.c", IMPORT_FUZZER)


def gen_integration_tests(n: int = 120) -> str:
    lines = [
        '#include "unity.h"',
        '#include <stdlib.h>',
        '#include <string.h>',
        '#include "tlvpack/tlvpack.h"',
        '',
    ]
    tags = [(0x01, b"abc"), (0x02, b"xy"), (0x10, b"data"), (0x20, b"val")]
    for i in range(n):
        tag, val = tags[i % len(tags)]
        blob = bytes([tag, len(val)]) + val
        hex_vals = ", ".join(f"0x{b:02x}" for b in blob)
        lines += [
            f'void test_integration_roundtrip_{i:03d}(void) {{',
            f'  const uint8_t src[] = {{{hex_vals}}};',
            '  tlv_tree_t *tree = NULL;',
            '  tlv_error_t err;',
            '  uint8_t *out = NULL;',
            '  size_t out_len = 0;',
            '  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(src, sizeof(src), &tree, &err));',
            '  TEST_ASSERT_EQUAL_INT(0, tlv_write_tree(tree, &out, &out_len));',
            '  tlv_tree_t *tree2 = NULL;',
            '  TEST_ASSERT_EQUAL_INT(0, tlv_parse_buffer(out, out_len, &tree2, &err));',
            f'  TEST_ASSERT_EQUAL_UINT32({tag}, tree2->roots[0].tag);',
            '  free(out);',
            '  tlv_tree_free(tree); free(tree);',
            '  tlv_tree_free(tree2); free(tree2);',
            '}',
            '',
        ]
    return "\n".join(lines)


def update_build_scripts() -> None:
    src_list = [
        "arena", "buffer", "varint", "node", "reader", "writer", "merge",
        "stream", "validate", "tlvpack",
    ] + MODULES
    src_loop = "\n".join(
        f'  ${{CC:-clang}} ${{CFLAGS:- -O1 -g -std=c11 -Wall -D_GNU_SOURCE}} '
        f'-I"${{SRC:-.}}/include" -I"${{SRC:-.}}/src" '
        f'-c "${{SRC:-.}}/src/{s}.c" -o "{s}.o"\n  OBJECTS+=("{s}.o")'
        for s in src_list
    )
    build_sh = f'''#!/bin/bash -eu
OBJECTS=()
for f in {" ".join(src_list)}; do
{src_loop.replace(src_list[0], "$f").split(chr(10))[0]}
done
# shellcheck disable=SC2086
build_one() {{
  local src="$1"
  ${{CC:-clang}} ${{CFLAGS:- -O1 -g -std=c11 -Wall -D_GNU_SOURCE}} \\
    -I"${{SRC:-.}}/include" -I"${{SRC:-.}}/src" \\
    -c "${{SRC:-.}}/src/${{src}}.c" -o "${{src}}.o"
  OBJECTS+=("${{src}}.o")
}}
'''
    # simpler loop
    build_sh = '''#!/bin/bash -eu
OBJECTS=()
SRCS=(%s)
for f in "${SRCS[@]}"; do
  ${CC:-clang} ${CFLAGS:- -O1 -g -std=c11 -Wall -D_GNU_SOURCE} \
    -I"${SRC:-.}/include" -I"${SRC:-.}/src" \
    -c "${SRC:-.}/src/${f}.c" -o "${f}.o"
  OBJECTS+=("${f}.o")
done
build_fuzzer() {
  ${CXX:-clang++} ${CXXFLAGS:- -O1 -g -std=c++17} ${LIB_FUZZING_ENGINE} \
    "${SRC:-.}/fuzz/$1" "${OBJECTS[@]}" -I"${SRC:-.}/include" \
    -o "${OUT:-.}/$2"
}
build_fuzzer parse_fuzzer.c parse_fuzzer
build_fuzzer merge_fuzzer.c merge_fuzzer
build_fuzzer stream_fuzzer.c stream_fuzzer
build_fuzzer nest_fuzzer.c nest_fuzzer
build_fuzzer import_fuzzer.c import_fuzzer
''' % (" ".join(f'"{s}"' for s in src_list))
    write(ROOT / ".clusterfuzzlite/build.sh", build_sh)

    makefile = ROOT / "Makefile"
    obj_line = " ".join(f"src/{s}.o" for s in src_list)
    makefile.write_text(f'''CC=clang
CFLAGS=-O1 -g -std=c11 -Wall -Iinclude -Isrc
TEST_SRCS=tests/test_runner.c tests/test_basic.c tests/test_merge.c tests/test_stream.c tests/test_integration.c tests/unity/unity.c
LIB_OBJS={obj_line}

all: test_runner

%.o: %.c
\t$(CC) $(CFLAGS) -c $< -o $@

test_runner: $(LIB_OBJS) $(TEST_SRCS:.c=.o)
\t$(CC) $(CFLAGS) -o $@ $^

test: test_runner
\t./test_runner

clean:
\trm -f src/*.o tests/*.o test_runner
''', encoding="utf-8")

    project = ROOT / ".clusterfuzzlite/project.yaml"
    if project.exists():
        text = project.read_text()
        if "import_fuzzer" not in text:
            text = text.replace("nest_fuzzer", "nest_fuzzer\n  - import_fuzzer")
            project.write_text(text)


def update_test_runner() -> None:
    runner = ROOT / "tests/test_runner.c"
    text = runner.read_text()
    if "test_integration" not in text:
        text = text.replace(
            'extern void test_stream_reassembly(void);',
            'extern void test_stream_reassembly(void);\nextern void test_integration_suite(void);',
        )
        text = text.replace(
            '  RUN_TEST(test_stream_reassembly);',
            '  RUN_TEST(test_stream_reassembly);\n  RUN_TEST(test_integration_suite);',
        )
        runner.write_text(text)
    suite = '''#include "unity.h"

'''
    suite += gen_integration_tests(120)
    suite += '''
void test_integration_suite(void) {
'''
    for i in range(120):
        suite += f'  RUN_TEST(test_integration_roundtrip_{i:03d});\n'
    suite += '}\n'
    write(ROOT / "tests/test_integration.c", suite)


def plant_extra_bugs() -> None:
    node = (ROOT / "src/node.c").read_text()
    if "free(n->children);" in node:
        node = node.replace("  free(n->children);\n", "")
        (ROOT / "src/node.c").write_text(node)

    varint = (ROOT / "src/varint.c").read_text()
    varint = varint.replace(
        "  for (i = 0; i < len && i < 10; i++) {",
        "  for (i = 0; i < 10; i++) {",
    )
    (ROOT / "src/varint.c").write_text(varint)


def fix_parse_fuzzer() -> None:
    pf = ROOT / "fuzz/parse_fuzzer.c"
    text = pf.read_text()
    if "size == 0" not in text:
        text = text.replace(
            '  if (!data || size > 65536) return 0;',
            '  if (size > 65536) return 0;\n  if (size == 0) {\n    tlv_error_t err;\n    tlv_tree_t *tree = NULL;\n    uint8_t *out = NULL;\n    size_t out_len = 0;\n    if (tlv_parse_buffer(data, 0, &tree, &err) != 0) return 0;\n    (void)tlv_validate_tree(tree);\n    if (tlv_write_tree(tree, &out, &out_len) == 0) free(out);\n    tlv_tree_free(tree);\n    free(tree);\n    return 0;\n  }\n  if (!data) return 0;',
        )
        pf.write_text(text)


def ensure_node_header() -> None:
    hdr = ROOT / "include/tlvpack/tlv_node.h"
    text = hdr.read_text()
    if "tlv_validate_tree" not in text:
        text = text.replace(
            "int tlv_tree_add_root(tlv_tree_t *t, uint32_t tag, const uint8_t *val, size_t len);",
            "int tlv_tree_add_root(tlv_tree_t *t, uint32_t tag, const uint8_t *val, size_t len);\n"
            "int tlv_validate_tree(const tlv_tree_t *t);",
        )
        hdr.write_text(text)


def ensure_writer_string_h() -> None:
    w = ROOT / "src/writer.c"
    text = w.read_text()
    if '#include <string.h>' not in text:
        w.write_text(text.replace('#include <stdlib.h>', '#include <stdlib.h>\n#include <string.h>'))


def main() -> None:
    add_modules()
    update_build_scripts()
    update_test_runner()
    ensure_node_header()
    ensure_writer_string_h()
    fix_parse_fuzzer()
    plant_extra_bugs()
    write(ROOT / "fuzz/corpus/import_fuzzer/base.bin", bytes([0x01, 0x03, 0x41, 0x42, 0x43, 0x02, 0x01, 0x01]))
    print("expanded modules:", len(MODULES))
    subprocess.run(["bash", "build/wsl_build.sh"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
