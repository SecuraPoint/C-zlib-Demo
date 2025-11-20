/*
 * MIT License
 *
 * Copyright (c) 2025 Marco Berger
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#include <stdio.h>
#include <string.h>
#include <zlib.h>
#include <png.h>

int main(void) {
    const char* text = "Hello from zlib via conda forge!";
    unsigned char compressed[100];
    unsigned char decompressed[100];
    uLong compressedSize = sizeof(compressed);
    uLong decompressedSize = sizeof(decompressed);

    /* --- zlib Demo: simple compress / decompress --- */

    // Compress
    if (compress(compressed, &compressedSize,
                 (const Bytef*)text, strlen(text)) != Z_OK) {
        printf("Fehler bei compress()\n");
        return 1;
    }

    // Decompress
    if (uncompress(decompressed, &decompressedSize,
                   compressed, compressedSize) != Z_OK) {
        printf("Fehler bei uncompress()\n");
        return 1;
    }

    decompressed[decompressedSize] = '\0'; // null terminator

    printf("Original:     %s\n", text);
    printf("Dekomprimiert: %s\n", decompressed);

    /* --- libpng Demo: show compile-time and runtime version --- */

    printf("\nlibpng compile-time version: %s\n", PNG_LIBPNG_VER_STRING);

    unsigned long png_runtime_ver = png_access_version_number();
    printf("libpng runtime version (numeric): %lu\n", png_runtime_ver);

    if (png_runtime_ver == 0) {
        fprintf(stderr, "Fehler: libpng Runtime-Version konnte nicht ermittelt werden!\n");
        return 1;
    }

    printf("zlib und libpng sind erfolgreich gelinkt und verwendbar.\n");
    return 0;
}
