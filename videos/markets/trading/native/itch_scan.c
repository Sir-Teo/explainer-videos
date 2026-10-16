/* One pass over a full day of Nasdaq TotalView-ITCH 5.0 (binary, 2-byte big-endian length prefixes),
 * read from stdin.  Built and run by videos/trading/compute.py:
 *
 *     gzip -dc S121025-v50.txt.gz | itch_scan OUTDIR SPY QQQ NVDA ...
 *
 * Writes into OUTDIR:
 *   summary.json        message counts by type (whole day / regular hours), bytes, symbols, peak rates
 *                       over windows of 1 us .. 1 s, system-event times, order-fate counts
 *   per_ms.u32          messages in every millisecond of the day (86,400,000 uint32)
 *   per_ms_bytes.u32    message bytes (incl. the 2-byte length) in every millisecond
 *   burst_<HHMMSS>.u32  messages per microsecond in [t - 100 ms, t + 400 ms) around 9:30, 14:00, 16:00
 *   lifetimes.u64       [4 fates][LT_BINS] log-binned order lifetimes (orders added 9:30-16:00)
 *   reaction.u64        [6 kinds][RX_BINS] log-binned gap from an execution to the next order message
 *                       of the same stock (kinds: A/F, D, X, U, any non-exec, same side cancel/delete)
 *   gaps.u64            [RX_BINS] log-binned gap between consecutive messages of the same stock
 *   sym_<SYM>.bin       every message of each requested stock as a fixed 40-byte record (see struct rec)
 *   raw_<SYM>.bin       the first 4,000 raw messages of each requested stock at or after 9:30:00
 *   head.bin            the first 64 KiB of the raw stream
 *   directory.tsv       stock locate -> symbol, market category, ETP flag, round lot
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define NS 1000000000ULL
#define DAY_MS 86400000ULL
#define RTH_OPEN (34200ULL * NS)   /* 9:30:00 */
#define RTH_CLOSE (57600ULL * NS)  /* 16:00:00 */
#define LT_BINS 160                /* 10 per decade, 1 ns .. 1e16 ns */
#define RX_BINS 200                /* 20 per decade, 1 ns .. 1e10 ns */
#define MAXSYM 32
#define RAW_N 4000

static inline uint64_t be(const uint8_t *p, int n) {
    uint64_t v = 0;
    for (int i = 0; i < n; i++) v = (v << 8) | p[i];
    return v;
}

#pragma pack(push, 1)
struct rec {
    uint64_t ts;     /* ns since midnight */
    uint64_t ref;    /* order reference number (orig ref for U) */
    uint64_t ref2;   /* new ref for U, match number for E/C/P/Q */
    uint32_t shares; /* shares (added / executed / canceled / replaced / crossed) */
    uint32_t price;  /* price x 10,000 (A/F/U/C/P/Q) */
    uint8_t type;
    uint8_t side;    /* 'B' / 'S' for A/F/P */
    uint8_t flag;    /* printable for C, cross type for Q, trading state for H */
    uint8_t pad[5];
};
#pragma pack(pop)

/* --- open-addressing hash map: live orders --------------------------------------------------- */
struct ord {
    uint64_t ref;   /* 0 = empty */
    uint64_t t_add;
    uint32_t shares;
    uint16_t locate;
    uint8_t side;
    uint8_t rth;    /* added during regular hours */
    uint8_t traded; /* has had at least one execution */
    uint8_t xed;    /* has had a partial cancel */
};
static struct ord *H;
static uint64_t HMASK, HLIVE, HPEAK;

static inline uint64_t hsh(uint64_t x) {
    x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33;
    return x;
}
static struct ord *hfind(uint64_t ref) {
    uint64_t i = hsh(ref) & HMASK;
    while (H[i].ref) {
        if (H[i].ref == ref) return &H[i];
        i = (i + 1) & HMASK;
    }
    return NULL;
}
static struct ord *hins(uint64_t ref) {
    uint64_t i = hsh(ref) & HMASK;
    while (H[i].ref && H[i].ref != ref) i = (i + 1) & HMASK;
    if (!H[i].ref) { HLIVE++; if (HLIVE > HPEAK) HPEAK = HLIVE; }
    memset(&H[i], 0, sizeof H[i]);
    H[i].ref = ref;
    return &H[i];
}
static void hdel(struct ord *o) { /* backward-shift deletion */
    uint64_t i = (uint64_t)(o - H), j = i;
    H[i].ref = 0;
    HLIVE--;
    for (;;) {
        j = (j + 1) & HMASK;
        if (!H[j].ref) return;
        uint64_t k = hsh(H[j].ref) & HMASK;
        if ((j > i && (k <= i || k > j)) || (j < i && (k <= i && k > j))) {
            H[i] = H[j];
            H[j].ref = 0;
            i = j;
        }
    }
}

/* --- histograms ------------------------------------------------------------------------------ */
static uint64_t lifet[4][LT_BINS]; /* 0 deleted, 1 fully executed, 2 replaced, 3 first partial cancel */
static uint64_t react[6][RX_BINS];
static uint64_t gaps[RX_BINS];
static inline int lbin(uint64_t dt, int per_decade, int nb) {
    if (dt < 1) return 0;
    int b = (int)floor(log10((double)dt) * per_decade);
    return b < 0 ? 0 : (b >= nb ? nb - 1 : b);
}

/* --- peak rates over windows ----------------------------------------------------------------- */
static const uint64_t WIN[] = {1000ULL, 10000ULL, 100000ULL, 1000000ULL, 10000000ULL, 100000000ULL, NS};
#define NWIN 7
static uint64_t wcur[NWIN], wcnt[NWIN], wmax[NWIN], wmax_at[NWIN];

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: itch_scan OUTDIR [SYMBOLS...]\n"); return 2; }
    const char *out = argv[1];
    int nsym = argc - 2;
    if (nsym > MAXSYM) nsym = MAXSYM;
    char want[MAXSYM][9];
    for (int i = 0; i < nsym; i++) { memset(want[i], ' ', 8); want[i][8] = 0; memcpy(want[i], argv[2 + i], strlen(argv[2 + i])); }

    char path[4096];
    FILE *fsym[MAXSYM] = {0}, *fraw[MAXSYM] = {0};
    int rawn[MAXSYM] = {0};
    static int loc2sym[65536];
    for (int i = 0; i < 65536; i++) loc2sym[i] = -1;

    uint32_t *per_ms = calloc(DAY_MS, 4), *per_ms_b = calloc(DAY_MS, 4);
    const uint64_t burst_t[3] = {RTH_OPEN, 50400ULL * NS, RTH_CLOSE};
    const char *burst_name[3] = {"093000", "140000", "160000"};
    const uint64_t BPRE = 100000ULL, BLEN = 500000ULL; /* in microseconds */
    uint32_t *burst[3];
    for (int i = 0; i < 3; i++) burst[i] = calloc(BLEN, 4);

    HMASK = (1ULL << 26) - 1;
    H = calloc(HMASK + 1, sizeof(struct ord));
    if (!per_ms || !per_ms_b || !H) { fprintf(stderr, "out of memory\n"); return 1; }

    uint64_t cnt_all[256] = {0}, cnt_rth[256] = {0}, bytes_all = 0, bytes_rth = 0, nmsg = 0, nsyms = 0;
    uint64_t sys_t[256]; char sys_c[256]; int nsys = 0;
    static uint64_t last_t[65536], last_exec[65536];
    static uint8_t last_exec_side[65536];
    uint64_t fate[4] = {0}, added_rth = 0, added_rth_traded = 0, nonmono = 0, last_ts = 0;
    uint64_t rth_lifetime_deleted_under[6] = {0}; /* deleted within 1us,10us,100us,1ms,10ms,100ms */

    FILE *fhead;
    snprintf(path, sizeof path, "%s/head.bin", out);
    fhead = fopen(path, "wb");
    uint64_t head_left = 65536;

    static uint8_t buf[1 << 22];
    size_t have = 0, pos = 0;
    uint8_t msg[256];
    for (;;) {
        if (have - pos < 2 + 255) {
            memmove(buf, buf + pos, have - pos);
            have -= pos; pos = 0;
            size_t r = fread(buf + have, 1, sizeof buf - have, stdin);
            have += r;
            if (have - pos < 2) break;
        }
        uint32_t len = (uint32_t)be(buf + pos, 2);
        if (len == 0 || have - pos < 2 + len) break;
        const uint8_t *m = buf + pos + 2;
        if (head_left) { size_t k = (2 + len < head_left) ? 2 + len : head_left; fwrite(buf + pos, 1, k, fhead); head_left -= k; }
        memcpy(msg, m, len);
        pos += 2 + len;
        nmsg++;

        uint8_t type = m[0];
        uint16_t loc = (uint16_t)be(m + 1, 2);
        uint64_t ts = be(m + 5, 6);
        if (ts < last_ts) nonmono++; else last_ts = ts;
        int rth = ts >= RTH_OPEN && ts < RTH_CLOSE;
        cnt_all[type]++; bytes_all += len + 2;
        if (rth) { cnt_rth[type]++; bytes_rth += len + 2; }
        uint64_t ms = ts / 1000000ULL;
        if (ms < DAY_MS) { per_ms[ms]++; per_ms_b[ms] += len + 2; }
        uint64_t us = ts / 1000ULL;
        for (int b = 0; b < 3; b++) {
            uint64_t s = burst_t[b] / 1000ULL - BPRE;
            if (us >= s && us < s + BLEN) burst[b][us - s]++;
        }
        for (int w = 0; w < NWIN; w++) {
            uint64_t k = ts / WIN[w];
            if (k != wcur[w]) { wcur[w] = k; wcnt[w] = 0; }
            if (++wcnt[w] > wmax[w]) { wmax[w] = wcnt[w]; wmax_at[w] = k * WIN[w]; }
        }

        if (type == 'S') {
            if (nsys < 256) { sys_t[nsys] = ts; sys_c[nsys] = (char)m[11]; nsys++; }
        } else if (type == 'R') {
            nsyms++;
            for (int i = 0; i < nsym; i++) {
                if (!memcmp(m + 11, want[i], 8)) {
                    loc2sym[loc] = i;
                    char s[9]; memcpy(s, want[i], 9);
                    for (int k = 7; k >= 0 && s[k] == ' '; k--) s[k] = 0;
                    snprintf(path, sizeof path, "%s/sym_%s.bin", out, s);
                    fsym[i] = fopen(path, "wb");
                    snprintf(path, sizeof path, "%s/raw_%s.bin", out, s);
                    fraw[i] = fopen(path, "wb");
                }
            }
            snprintf(path, sizeof path, "%s/directory.tsv", out);
            static FILE *fdir = NULL;
            if (!fdir) fdir = fopen(path, "w");
            char s[9]; memcpy(s, m + 11, 8); s[8] = 0;
            for (int k = 7; k >= 0 && s[k] == ' '; k--) s[k] = 0;
            fprintf(fdir, "%u\t%s\t%c\t%c\t%u\n", loc, s, m[19], m[33], (unsigned)be(m + 21, 4));
        }

        /* inter-arrival and reaction statistics, per stock */
        if (loc && (type == 'A' || type == 'F' || type == 'E' || type == 'C' || type == 'X' || type == 'D' ||
                    type == 'U' || type == 'P')) {
            if (last_t[loc] && rth) gaps[lbin(ts - last_t[loc], 20, RX_BINS)]++;
            last_t[loc] = ts;
            int is_exec = type == 'E' || type == 'C' || type == 'P';
            if (is_exec) {
                if (!last_exec[loc]) {
                    last_exec[loc] = ts;
                    if (type == 'P') last_exec_side[loc] = m[19];
                    else { struct ord *o = hfind(be(m + 11, 8)); last_exec_side[loc] = o ? o->side : 0; }
                }
            } else if (last_exec[loc]) {
                if (rth) {
                    int b = lbin(ts - last_exec[loc], 20, RX_BINS);
                    int kind = (type == 'A' || type == 'F') ? 0 : type == 'D' ? 1 : type == 'X' ? 2 : 3;
                    react[kind][b]++;
                    react[4][b]++;
                    if (type == 'D' || type == 'X') {
                        struct ord *o = hfind(be(m + 11, 8));
                        if (o && o->side == last_exec_side[loc]) react[5][b]++;
                    }
                }
                last_exec[loc] = 0;
            }
        }

        /* order fates */
        if (type == 'A' || type == 'F') {
            struct ord *o = hins(be(m + 11, 8));
            o->t_add = ts; o->shares = (uint32_t)be(m + 20, 4); o->locate = loc; o->side = m[19]; o->rth = rth;
            if (rth) added_rth++;
        } else if (type == 'E' || type == 'C') {
            struct ord *o = hfind(be(m + 11, 8));
            if (o) {
                uint32_t ex = (uint32_t)be(m + 19, 4);
                if (o->rth && !o->traded) added_rth_traded++;
                o->traded = 1;
                o->shares = ex >= o->shares ? 0 : o->shares - ex;
                if (!o->shares) {
                    if (o->rth && rth) { lifet[1][lbin(ts - o->t_add, 10, LT_BINS)]++; fate[1]++; }
                    hdel(o);
                }
            }
        } else if (type == 'X') {
            struct ord *o = hfind(be(m + 11, 8));
            if (o) {
                uint32_t cx = (uint32_t)be(m + 19, 4);
                if (o->rth && rth && !o->xed) lifet[3][lbin(ts - o->t_add, 10, LT_BINS)]++;
                o->xed = 1;
                o->shares = cx >= o->shares ? 0 : o->shares - cx;
                if (!o->shares) hdel(o);
            }
        } else if (type == 'D') {
            struct ord *o = hfind(be(m + 11, 8));
            if (o) {
                if (o->rth && rth) {
                    uint64_t dt = ts - o->t_add;
                    lifet[0][lbin(dt, 10, LT_BINS)]++; fate[0]++;
                    for (int k = 0; k < 6; k++) if (dt < 1000ULL * (uint64_t)pow(10, k)) rth_lifetime_deleted_under[k]++;
                }
                hdel(o);
            }
        } else if (type == 'U') {
            struct ord *o = hfind(be(m + 11, 8));
            uint8_t side = 0; uint16_t l = loc; int was_rth = rth;
            if (o) {
                side = o->side; l = o->locate;
                if (o->rth && rth) { lifet[2][lbin(ts - o->t_add, 10, LT_BINS)]++; fate[2]++; }
                hdel(o);
            }
            struct ord *n = hins(be(m + 19, 8));
            n->t_add = ts; n->shares = (uint32_t)be(m + 27, 4); n->locate = l; n->side = side; n->rth = was_rth;
            if (rth) added_rth++;
        }

        /* per-stock record files */
        int si = loc2sym[loc];
        if (si >= 0 && type != 'R') {
            struct rec r; memset(&r, 0, sizeof r);
            r.ts = ts; r.type = type;
            switch (type) {
            case 'A': case 'F':
                r.ref = be(m + 11, 8); r.side = m[19]; r.shares = (uint32_t)be(m + 20, 4); r.price = (uint32_t)be(m + 32, 4); break;
            case 'E':
                r.ref = be(m + 11, 8); r.shares = (uint32_t)be(m + 19, 4); r.ref2 = be(m + 23, 8); break;
            case 'C':
                r.ref = be(m + 11, 8); r.shares = (uint32_t)be(m + 19, 4); r.ref2 = be(m + 23, 8); r.flag = m[31];
                r.price = (uint32_t)be(m + 32, 4); break;
            case 'X':
                r.ref = be(m + 11, 8); r.shares = (uint32_t)be(m + 19, 4); break;
            case 'D':
                r.ref = be(m + 11, 8); break;
            case 'U':
                r.ref = be(m + 11, 8); r.ref2 = be(m + 19, 8); r.shares = (uint32_t)be(m + 27, 4); r.price = (uint32_t)be(m + 31, 4); break;
            case 'P':
                r.ref = be(m + 11, 8); r.side = m[19]; r.shares = (uint32_t)be(m + 20, 4); r.price = (uint32_t)be(m + 32, 4);
                r.ref2 = be(m + 36, 8); break;
            case 'Q':
                r.shares = (uint32_t)be(m + 11, 8); r.price = (uint32_t)be(m + 27, 4); r.ref2 = be(m + 31, 8); r.flag = m[39]; break;
            case 'H':
                r.flag = m[19]; break;
            default: break;
            }
            fwrite(&r, sizeof r, 1, fsym[si]);
            if (ts >= RTH_OPEN && rawn[si] < RAW_N) {
                uint8_t lp[2] = {(uint8_t)(len >> 8), (uint8_t)len};
                fwrite(lp, 1, 2, fraw[si]); fwrite(msg, 1, len, fraw[si]);
                rawn[si]++;
            }
        }
        if ((nmsg & ((1 << 26) - 1)) == 0) {
            fprintf(stderr, "%llu M messages, t = %02llu:%02llu:%02llu, live orders %llu\n", (unsigned long long)(nmsg >> 20),
                    (unsigned long long)(ts / NS / 3600), (unsigned long long)(ts / NS / 60 % 60), (unsigned long long)(ts / NS % 60),
                    (unsigned long long)HLIVE);
        }
    }
    fclose(fhead);
    for (int i = 0; i < nsym; i++) { if (fsym[i]) fclose(fsym[i]); if (fraw[i]) fclose(fraw[i]); }

    FILE *f;
    snprintf(path, sizeof path, "%s/per_ms.u32", out); f = fopen(path, "wb"); fwrite(per_ms, 4, DAY_MS, f); fclose(f);
    snprintf(path, sizeof path, "%s/per_ms_bytes.u32", out); f = fopen(path, "wb"); fwrite(per_ms_b, 4, DAY_MS, f); fclose(f);
    for (int b = 0; b < 3; b++) {
        snprintf(path, sizeof path, "%s/burst_%s.u32", out, burst_name[b]); f = fopen(path, "wb");
        fwrite(burst[b], 4, BLEN, f); fclose(f);
    }
    snprintf(path, sizeof path, "%s/lifetimes.u64", out); f = fopen(path, "wb"); fwrite(lifet, 8, 4 * LT_BINS, f); fclose(f);
    snprintf(path, sizeof path, "%s/reaction.u64", out); f = fopen(path, "wb"); fwrite(react, 8, 6 * RX_BINS, f); fclose(f);
    snprintf(path, sizeof path, "%s/gaps.u64", out); f = fopen(path, "wb"); fwrite(gaps, 8, RX_BINS, f); fclose(f);

    snprintf(path, sizeof path, "%s/summary.json", out); f = fopen(path, "w");
    uint64_t nmsg_rth = 0;
    for (int t = 0; t < 256; t++) nmsg_rth += cnt_rth[t];
    fprintf(f, "{\n \"messages\": %llu,\n \"bytes\": %llu,\n \"messages_rth\": %llu,\n \"bytes_rth\": %llu,\n",
            (unsigned long long)nmsg, (unsigned long long)bytes_all,
            (unsigned long long)nmsg_rth, (unsigned long long)bytes_rth);
    fprintf(f, " \"symbols\": %llu,\n \"nonmonotonic\": %llu,\n \"live_orders_peak\": %llu,\n \"live_orders_end\": %llu,\n",
            (unsigned long long)nsyms, (unsigned long long)nonmono, (unsigned long long)HPEAK, (unsigned long long)HLIVE);
    fprintf(f, " \"added_rth\": %llu,\n \"added_rth_traded\": %llu,\n", (unsigned long long)added_rth, (unsigned long long)added_rth_traded);
    fprintf(f, " \"fate_rth\": {\"deleted\": %llu, \"executed\": %llu, \"replaced\": %llu},\n",
            (unsigned long long)fate[0], (unsigned long long)fate[1], (unsigned long long)fate[2]);
    fprintf(f, " \"deleted_within\": {\"1us\": %llu, \"10us\": %llu, \"100us\": %llu, \"1ms\": %llu, \"10ms\": %llu, \"100ms\": %llu},\n",
            (unsigned long long)rth_lifetime_deleted_under[0], (unsigned long long)rth_lifetime_deleted_under[1],
            (unsigned long long)rth_lifetime_deleted_under[2], (unsigned long long)rth_lifetime_deleted_under[3],
            (unsigned long long)rth_lifetime_deleted_under[4], (unsigned long long)rth_lifetime_deleted_under[5]);
    fprintf(f, " \"count_by_type\": {");
    int first = 1;
    for (int t = 0; t < 256; t++) if (cnt_all[t]) { fprintf(f, "%s\"%c\": %llu", first ? "" : ", ", t, (unsigned long long)cnt_all[t]); first = 0; }
    fprintf(f, "},\n \"count_by_type_rth\": {");
    first = 1;
    for (int t = 0; t < 256; t++) if (cnt_rth[t]) { fprintf(f, "%s\"%c\": %llu", first ? "" : ", ", t, (unsigned long long)cnt_rth[t]); first = 0; }
    fprintf(f, "},\n \"peaks\": [");
    for (int w = 0; w < NWIN; w++)
        fprintf(f, "%s{\"window_ns\": %llu, \"max\": %llu, \"at_ns\": %llu}", w ? ", " : "", (unsigned long long)WIN[w],
                (unsigned long long)wmax[w], (unsigned long long)wmax_at[w]);
    fprintf(f, "],\n \"system_events\": [");
    for (int i = 0; i < nsys; i++) fprintf(f, "%s[\"%c\", %llu]", i ? ", " : "", sys_c[i], (unsigned long long)sys_t[i]);
    fprintf(f, "]\n}\n");
    fclose(f);
    fprintf(stderr, "done: %llu messages\n", (unsigned long long)nmsg);
    return 0;
}
