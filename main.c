#include "tome/tome.h"
#include "tome/format.h"
#include "tome/validator.h"
#include "tome/diag.h"
#include "tome/memory.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *read_file(const char *path, size_t *out_len) {
    FILE *file = fopen(path, "rb");
    char *buffer;
    long size;

    if (file == NULL) {
        return NULL;
    }
    if (fseek(file, 0, SEEK_END) != 0) {
        fclose(file);
        return NULL;
    }
    size = ftell(file);
    if (size < 0) {
        fclose(file);
        return NULL;
    }
    rewind(file);
    buffer = malloc((size_t)size + 1);
    if (buffer == NULL) {
        fclose(file);
        return NULL;
    }
    if (fread(buffer, 1, (size_t)size, file) != (size_t)size) {
        free(buffer);
        fclose(file);
        return NULL;
    }
    buffer[size] = '\0';
    fclose(file);
    *out_len = (size_t)size;
    return buffer;
}

static int cmd_validate(const char *path) {
    char *text;
    size_t len;
    TomeDoc *doc;
    TomeError err;

    text = read_file(path, &len);
    if (text == NULL) {
        fprintf(stderr, "tome: cannot read %s\n", path);
        return 1;
    }
    if (tome_parse(text, len, &doc, &err) != TOME_OK) {
        fprintf(stderr, "tome: parse error at %zu:%zu: %s\n", err.line, err.column, err.message);
        free(text);
        return 1;
    }
    tome_free(doc);
    free(text);
    printf("OK %s\n", path);
    return 0;
}

static int cmd_get(const char *path, const char *key_path) {
    char *text;
    size_t len;
    TomeDoc *doc;
    TomeError err;
    char out[512];
    TomeStatus status;

    text = read_file(path, &len);
    if (text == NULL) {
        return 1;
    }
    if (tome_parse(text, len, &doc, &err) != TOME_OK) {
        free(text);
        return 1;
    }
    status = tome_get_path(doc, key_path, out, sizeof(out));
    tome_free(doc);
    free(text);
    if (status != TOME_OK) {
        fprintf(stderr, "tome: key not found: %s\n", key_path);
        return 1;
    }
    printf("%s\n", out);
    return 0;
}

static int cmd_merge(const char *base_path, const char *overlay_path) {
    char *base_text;
    char *overlay_text;
    size_t base_len;
    size_t overlay_len;
    TomeDoc *base;
    TomeDoc *overlay;
    TomeError err;
    char *serialized;
    size_t serialized_len;

    base_text = read_file(base_path, &base_len);
    overlay_text = read_file(overlay_path, &overlay_len);
    if (base_text == NULL || overlay_text == NULL) {
        free(base_text);
        free(overlay_text);
        return 1;
    }
    if (tome_parse(base_text, base_len, &base, &err) != TOME_OK ||
        tome_parse(overlay_text, overlay_len, &overlay, &err) != TOME_OK) {
        free(base_text);
        free(overlay_text);
        return 1;
    }
    if (tome_merge(base, overlay, &err) != TOME_OK) {
        tome_free(base);
        tome_free(overlay);
        free(base_text);
        free(overlay_text);
        return 1;
    }
    if (tome_serialize(base, &serialized, &serialized_len) != TOME_OK) {
        tome_free(base);
        tome_free(overlay);
        free(base_text);
        free(overlay_text);
        return 1;
    }
    fwrite(serialized, 1, serialized_len, stdout);
    tome_free_ptr(serialized);
    tome_free(base);
    tome_free(overlay);
    free(base_text);
    free(overlay_text);
    return 0;
}

static int cmd_lint(const char *path) {
    char *text;
    size_t len;
    TomeDoc *doc;
    TomeError err;
    TomeValidateRules rules;
    TomeDiagList diags;
    size_t i;

    text = read_file(path, &len);
    if (text == NULL) {
        return 1;
    }
    if (tome_parse(text, len, &doc, &err) != TOME_OK) {
        free(text);
        return 1;
    }
    memset(&rules, 0, sizeof(rules));
    rules.max_table_depth = 64;
    rules.max_array_length = 512;
    rules.max_key_length = 256;
    rules.max_string_length = 8192;
    tome_diag_init(&diags);
    if (tome_validate_document(doc, &rules, &diags) != TOME_OK || diags.count > 0) {
        for (i = 0; i < diags.count; i++) {
            fprintf(stderr, "lint: %s\n", diags.items[i].message);
        }
        tome_diag_free(&diags);
        tome_free(doc);
        free(text);
        return 1;
    }
    tome_diag_free(&diags);
    tome_free(doc);
    free(text);
    printf("lint ok %s\n", path);
    return 0;
}

static int cmd_format(const char *path) {
    char *text;
    size_t len;
    TomeDoc *doc;
    TomeError err;
    TomeFormatOptions opts;
    char *out;
    size_t out_len;

    text = read_file(path, &len);
    if (text == NULL) {
        return 1;
    }
    if (tome_parse(text, len, &doc, &err) != TOME_OK) {
        free(text);
        return 1;
    }
    memset(&opts, 0, sizeof(opts));
    opts.indent_width = 2;
    opts.sort_keys = 1;
    opts.trailing_newline = 1;
    if (tome_format_document(doc, &opts, &out, &out_len) != TOME_OK) {
        tome_free(doc);
        free(text);
        return 1;
    }
    fwrite(out, 1, out_len, stdout);
    tome_free_ptr(out);
    tome_free(doc);
    free(text);
    return 0;
}

static void usage(void) {
    fprintf(stderr, "Usage:\n");
    fprintf(stderr, "  tome validate <file.toml>\n");
    fprintf(stderr, "  tome lint <file.toml>\n");
    fprintf(stderr, "  tome format <file.toml>\n");
    fprintf(stderr, "  tome get <file.toml> <dotted.key>\n");
    fprintf(stderr, "  tome merge <base.toml> <overlay.toml>\n");
}

int main(int argc, char **argv) {
    if (argc < 2) {
        usage();
        return 1;
    }
    if (strcmp(argv[1], "validate") == 0 && argc == 3) {
        return cmd_validate(argv[2]);
    }
    if (strcmp(argv[1], "lint") == 0 && argc == 3) {
        return cmd_lint(argv[2]);
    }
    if (strcmp(argv[1], "format") == 0 && argc == 3) {
        return cmd_format(argv[2]);
    }
    if (strcmp(argv[1], "get") == 0 && argc == 4) {
        return cmd_get(argv[2], argv[3]);
    }
    if (strcmp(argv[1], "merge") == 0 && argc == 4) {
        return cmd_merge(argv[2], argv[3]);
    }
    usage();
    return 1;
}
