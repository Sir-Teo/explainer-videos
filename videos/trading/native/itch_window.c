/* Dump every message inside the given time windows of a TotalView-ITCH 5.0 stream (stdin) as CSV:
 *     ts_ns,type,locate,symbol,side,shares,price,ref
 * (symbol comes from the stock directory; side/shares/price/ref are filled where the message has them).
 * Stops reading after the last window.  Used by videos/trading/compute.py ("windows").
 *
 *     gzip -dc FILE | itch_window OUT.csv START_NS END_NS [START_NS END_NS ...]
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static inline uint64_t be(const uint8_t *p, int n) { uint64_t v = 0; for (int i = 0; i < n; i++) v = (v << 8) | p[i]; return v; }

int main(int argc, char **argv) {
    if (argc < 4 || (argc - 2) % 2) { fprintf(stderr, "usage: itch_window OUT.csv START END [START END ...]\n"); return 2; }
    int nw = (argc - 2) / 2;
    uint64_t *a = calloc(nw, 8), *b = calloc(nw, 8), last = 0;
    for (int i = 0; i < nw; i++) { a[i] = strtoull(argv[2 + 2 * i], 0, 10); b[i] = strtoull(argv[3 + 2 * i], 0, 10); if (b[i] > last) last = b[i]; }
    FILE *out = fopen(argv[1], "w");
    fprintf(out, "ts_ns,type,locate,symbol,side,shares,price,ref\n");
    static char sym[65536][9];
    static uint8_t buf[1 << 22];
    size_t have = 0, pos = 0;
    for (;;) {
        if (have - pos < 2 + 255) {
            memmove(buf, buf + pos, have - pos); have -= pos; pos = 0;
            have += fread(buf + have, 1, sizeof buf - have, stdin);
            if (have - pos < 2) break;
        }
        uint32_t len = (uint32_t)be(buf + pos, 2);
        if (!len || have - pos < 2 + len) break;
        const uint8_t *m = buf + pos + 2;
        pos += 2 + len;
        uint16_t loc = (uint16_t)be(m + 1, 2);
        uint64_t ts = be(m + 5, 6);
        if (m[0] == 'R') { memcpy(sym[loc], m + 11, 8); for (int k = 7; k >= 0 && sym[loc][k] == ' '; k--) sym[loc][k] = 0; }
        if (ts > last) break;
        int in = 0;
        for (int i = 0; i < nw; i++) if (ts >= a[i] && ts < b[i]) in = 1;
        if (!in) continue;
        char side = 0; uint64_t shares = 0, price = 0, ref = 0;
        switch (m[0]) {
        case 'A': case 'F': ref = be(m + 11, 8); side = m[19]; shares = be(m + 20, 4); price = be(m + 32, 4); break;
        case 'E': case 'C': ref = be(m + 11, 8); shares = be(m + 19, 4); if (m[0] == 'C') price = be(m + 32, 4); break;
        case 'X': ref = be(m + 11, 8); shares = be(m + 19, 4); break;
        case 'D': ref = be(m + 11, 8); break;
        case 'U': ref = be(m + 11, 8); shares = be(m + 27, 4); price = be(m + 31, 4); break;
        case 'P': ref = be(m + 11, 8); side = m[19]; shares = be(m + 20, 4); price = be(m + 32, 4); break;
        default: break;
        }
        fprintf(out, "%llu,%c,%u,%s,%c,%llu,%llu,%llu\n", (unsigned long long)ts, m[0], loc, sym[loc], side ? side : '-',
                (unsigned long long)shares, (unsigned long long)price, (unsigned long long)ref);
    }
    fclose(out);
    return 0;
}
