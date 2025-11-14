#include <stdio.h>
#include <string.h>
#include <zlib.h>

int main() {
    const char* text = "Hello from zlib via conda forge!";
    unsigned char compressed[100];
    unsigned char decompressed[100];
    uLong compressedSize = sizeof(compressed);
    uLong decompressedSize = sizeof(decompressed);

    // Compress
    if (compress(compressed, &compressedSize, (const Bytef*)text, strlen(text)) != Z_OK) {
        printf("Fehler bei compress()\n");
        return 1;
    }

    // Decompress
    if (uncompress(decompressed, &decompressedSize, compressed, compressedSize) != Z_OK) {
        printf("Fehler bei uncompress()\n");
        return 1;
    }

    decompressed[decompressedSize] = '\0'; // null terminator

    printf("Original: %s\n", text);
    printf("Dekomprimiert: %s\n", decompressed);
    return 0;
}
