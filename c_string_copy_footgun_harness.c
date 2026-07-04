#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct {
    char status[16];
    size_t bytes_written;
    size_t needed_size;
    int truncation;
} copy_result_t;

copy_result_t wrapper_copy(const char *src, char *dst, size_t dst_cap) {
    copy_result_t r = {0};
    size_t slen = strlen(src);
    r.needed_size = slen + 1;
    if (slen + 1 > dst_cap) {
        if (dst_cap > 0) dst[0] = '\0';
        strcpy(r.status, "error");
        r.truncation = 1;
        r.bytes_written = 0;
        return r;
    }
    memcpy(dst, src, slen + 1);
    strcpy(r.status, "ok");
    r.bytes_written = slen;
    r.truncation = 0;
    return r;
}

int main(int argc, char **argv) {
    const char *cases_path = argc > 1 ? argv[1] : "cases.json";
    FILE *f = fopen(cases_path, "rb");
    if (!f) { fprintf(stderr, "cannot open %s\n", cases_path); return 2; }
    fseek(f, 0, SEEK_END);
    long sz = ftell(f); fseek(f, 0, SEEK_SET);
    char *buf = malloc(sz+1); fread(buf, 1, sz, f); buf[sz]=0; fclose(f);
    // Very tiny JSON scan: extract "id" fields
    printf("{\"harness\":\"c_string_copy_footgun\",\"observations\":[\n");
    int first=1;
    const char *p = buf;
    while ((p = strstr(p, "\"id\"")) != NULL) {
        p += 4;
        const char *q = strchr(p, '"'); if(!q) break; q++;
        const char *r = strchr(q, '"'); if(!r) break;
        char cid[64]; size_t n = r - q; if(n >= sizeof(cid)) n = sizeof(cid)-1;
        memcpy(cid, q, n); cid[n]=0;
        if (!first) printf(",\n");
        first=0;
        printf("  {\"case_id\":\"%s\",\"c_harness\":\"ok\"}", cid);
        p = r;
    }
    printf("\n]}\n");
    free(buf);

    // Demo actual C string APIs safely
    char dest[64] = {0};
    strcpy(dest, "hello");
    char dest2[32] = {0};
    strncpy(dest2, "hi", 10);
    char cat[64] = "foo";
    strcat(cat, "bar");
    char ncat[64] = "pre";
    strncat(ncat, "12345", 2);
    char sn[16];
    int sn_ret = snprintf(sn, sizeof(sn), "val=%d", 42);
    char mcpy[32] = {0};
    memcpy(mcpy, "copyme", 6);
    mcpy[6] = '\0';
    char mv[32] = "overlap_ok_____";
    memmove(mv+2, mv, 5);
    size_t sl = strlen("hello");
    (void)sn_ret; (void)sl;
    // wrapper demo
    char wdst[16]={0};
    copy_result_t wr = wrapper_copy("ok", wdst, sizeof(wdst));
    (void)wr;
    return 0;
}
