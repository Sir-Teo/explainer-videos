/* An order book built the way a latency-sensitive feed handler builds one, replaying one stock's real
 * Nasdaq messages (the 40-byte records written by itch_scan) and timing every update.
 *
 *     book sym_SPY.bin  ->  JSON on stdout
 *
 * Design (the usual one): every order lives in a preallocated pool and is found through an open-addressing
 * hash map keyed by its reference number; every price level is a slot in a flat array indexed by price in
 * cents, holding a FIFO of its orders as an intrusive doubly linked list; best bid and ask are tracked as
 * indices.  No allocation, no system calls, no locks on the update path.
 */
#define _GNU_SOURCE
#include <math.h>
#include <pthread.h>
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/mman.h>
#include <x86intrin.h>

#pragma pack(push, 1)
struct rec { uint64_t ts, ref, ref2; uint32_t shares, price; uint8_t type, side, flag, pad[5]; };
#pragma pack(pop)

#define NLEV (1 << 18) /* $0.00 .. $2,621.43 in cents */
#define POOL (1 << 20)
#define HBITS 20

struct order { uint64_t ref; uint32_t shares, level, prev, next; uint8_t side; };
struct level { uint64_t shares; uint32_t head, tail, count; };

static struct order *pool;
static uint32_t free_head;
static struct level *bid, *ask;
static int64_t best_bid = -1, best_ask = NLEV;
static uint64_t *hkey;
static uint32_t *hval;
#define HMASK ((1u << HBITS) - 1)

static inline uint32_t hh(uint64_t x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; return (uint32_t)x & HMASK; }
static inline uint32_t hget(uint64_t ref) {
    uint32_t i = hh(ref);
    while (hkey[i]) { if (hkey[i] == ref) return hval[i]; i = (i + 1) & HMASK; }
    return 0;
}
static inline void hput(uint64_t ref, uint32_t v) {
    uint32_t i = hh(ref);
    while (hkey[i] && hkey[i] != ref) i = (i + 1) & HMASK;
    hkey[i] = ref; hval[i] = v;
}
static inline void hdel(uint64_t ref) {
    uint32_t i = hh(ref);
    while (hkey[i] && hkey[i] != ref) i = (i + 1) & HMASK;
    if (!hkey[i]) return;
    hkey[i] = 0;
    uint32_t j = i;
    for (;;) { /* backward shift */
        j = (j + 1) & HMASK;
        if (!hkey[j]) return;
        uint32_t k = hh(hkey[j]);
        if ((j > i && (k <= i || k > j)) || (j < i && (k <= i && k > j))) {
            hkey[i] = hkey[j]; hval[i] = hval[j]; hkey[j] = 0; i = j;
        }
    }
}

static inline void add(uint64_t ref, uint8_t side, uint32_t shares, uint32_t price) {
    uint32_t o = free_head;
    free_head = pool[o].next;
    uint32_t lv = price / 100;
    if (lv >= NLEV) lv = NLEV - 1; /* stub quotes far from the market (up to $199,999.99) share the last level */
    struct level *L = side == 'B' ? &bid[lv] : &ask[lv];
    pool[o] = (struct order){ref, shares, lv, L->tail, 0, side};
    if (L->tail) pool[L->tail].next = o; else L->head = o;
    L->tail = o;
    L->shares += shares;
    L->count++;
    hput(ref, o);
    if (side == 'B') { if ((int64_t)lv > best_bid) best_bid = lv; }
    else if ((int64_t)lv < best_ask) best_ask = lv;
}
static inline void unlink_order(uint32_t o) {
    struct order *p = &pool[o];
    struct level *L = p->side == 'B' ? &bid[p->level] : &ask[p->level];
    if (p->prev) pool[p->prev].next = p->next; else L->head = p->next;
    if (p->next) pool[p->next].prev = p->prev; else L->tail = p->prev;
    L->shares -= p->shares;
    L->count--;
    if (!L->count) { /* the level emptied: if it was the best, walk to the next occupied one */
        if (p->side == 'B' && (int64_t)p->level == best_bid) { while (best_bid >= 0 && !bid[best_bid].count) best_bid--; }
        else if (p->side == 'S' && (int64_t)p->level == best_ask) { while (best_ask < NLEV && !ask[best_ask].count) best_ask++; }
    }
    hdel(p->ref);
    p->next = free_head;
    free_head = o;
}
static inline void reduce(uint64_t ref, uint32_t n) {
    uint32_t o = hget(ref);
    if (!o) return;
    struct order *p = &pool[o];
    if (n >= p->shares) { unlink_order(o); return; }
    p->shares -= n;
    (p->side == 'B' ? &bid[p->level] : &ask[p->level])->shares -= n;
}

static inline void apply(const struct rec *r) {
    switch (r->type) {
    case 'A': case 'F': add(r->ref, r->side, r->shares, r->price); break;
    case 'E': case 'C': case 'X': reduce(r->ref, r->shares); break;
    case 'D': { uint32_t o = hget(r->ref); if (o) unlink_order(o); break; }
    case 'U': {
        uint32_t o = hget(r->ref);
        if (!o) break;
        uint8_t side = pool[o].side;
        unlink_order(o);
        add(r->ref2, side, r->shares, r->price);
        break;
    }
    default: break;
    }
}

static int cmp_u32(const void *a, const void *b) { uint32_t x = *(const uint32_t *)a, y = *(const uint32_t *)b; return x < y ? -1 : x > y; }

static void *region(size_t bytes, int huge, int prefault) {
    size_t al = 2u << 20, map = (bytes + al - 1) & ~(al - 1);
    char *m = mmap(NULL, map + al, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    char *p = (char *)(((uintptr_t)m + al - 1) & ~(uintptr_t)(al - 1));
    madvise(p, map, huge ? MADV_HUGEPAGE : MADV_NOHUGEPAGE);
    if (prefault) memset(p, 0, map);
    return p;
}
static void setup(int huge, int prefault) {
    pool = region(POOL * sizeof *pool, huge, prefault);
    bid = region(NLEV * sizeof *bid, huge, prefault);
    ask = region(NLEV * sizeof *ask, huge, prefault);
    hkey = region((1u << HBITS) * sizeof *hkey, huge, prefault);
    hval = region((1u << HBITS) * sizeof *hval, huge, prefault);
    for (uint32_t i = 1; i < POOL - 1; i++) pool[i].next = i + 1; /* index 0 is "null" */
    free_head = 1; best_bid = -1; best_ask = NLEV;
}
static uint64_t touched_pages(void) {
    FILE *f = fopen("/proc/self/stat", "r");
    unsigned long minflt = 0; char buf[4096];
    if (f && fgets(buf, sizeof buf, f)) { char *p = strrchr(buf, ')'); sscanf(p + 2, "%*c %*d %*d %*d %*d %*d %*u %lu", &minflt); }
    if (f) fclose(f);
    return minflt;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: book sym_XXX.bin\n"); return 2; }
    cpu_set_t s; CPU_ZERO(&s); CPU_SET(2, &s); sched_setaffinity(0, sizeof s, &s);
    FILE *f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END);
    size_t n = ftell(f) / sizeof(struct rec);
    fseek(f, 0, SEEK_SET);
    struct rec *R = malloc(n * sizeof *R);
    if (fread(R, sizeof *R, n, f) != n) { fprintf(stderr, "short read\n"); return 1; }
    fclose(f);

    /* TSC calibration */
    struct timespec a, b;
    clock_gettime(CLOCK_MONOTONIC, &a);
    uint64_t t0 = __rdtsc();
    do clock_gettime(CLOCK_MONOTONIC, &b); while ((b.tv_sec - a.tv_sec) * 1e9 + (b.tv_nsec - a.tv_nsec) < 2e8);
    double tpn = (double)(__rdtsc() - t0) / ((b.tv_sec - a.tv_sec) * 1e9 + (b.tv_nsec - a.tv_nsec));

    /* three whole-day passes: cold 4 KiB pages, pre-faulted 4 KiB pages, pre-faulted 2 MiB pages */
    const char *names[3] = {"cold", "prefaulted", "prefaulted_huge"};
    printf("{\"messages\": %zu, \"variants\": {", n);
    int64_t end_bid = 0, end_ask = 0;
    for (int v = 0; v < 3; v++) {
        setup(v == 2, v > 0);
        uint64_t f0 = touched_pages();
        uint64_t c0 = __rdtsc();
        for (size_t i = 0; i < n; i++) apply(&R[i]);
        uint64_t c1 = __rdtsc();
        printf("%s\"%s\": {\"ns_per_message\": %.3f, \"total_ms\": %.3f, \"page_faults\": %lu}", v ? ", " : "", names[v],
               (c1 - c0) / tpn / n, (c1 - c0) / tpn / 1e6, (unsigned long)(touched_pages() - f0));
        end_bid = best_bid; end_ask = best_ask;
    }
    printf("},");

    /* per-message timing on the last (huge-page, pre-faulted) layout, replayed from scratch */
    setup(1, 1);
    uint32_t *lat = malloc(n * sizeof *lat);
    uint64_t ovh = UINT64_MAX;
    for (int k = 0; k < 100000; k++) { _mm_lfence(); uint64_t x = __rdtsc(); _mm_lfence(); _mm_lfence(); uint64_t y = __rdtsc(); if (y - x < ovh) ovh = y - x; }
    size_t m = 0;
    for (size_t i = 0; i < n; i++) {
        _mm_lfence();
        uint64_t x = __rdtsc();
        _mm_lfence();
        apply(&R[i]);
        _mm_lfence();
        uint64_t y = __rdtsc();
        char t = R[i].type;
        if (t == 'A' || t == 'F' || t == 'E' || t == 'C' || t == 'X' || t == 'D' || t == 'U') {
            double d = (double)(y - x - ovh) / tpn;
            lat[m++] = d < 0 ? 0 : (uint32_t)(d + 0.5);
        }
    }
    qsort(lat, m, sizeof *lat, cmp_u32);
    double mean = 0;
    for (size_t i = 0; i < m; i++) mean += lat[i];
    printf(" \"book_messages\": %zu, \"timer_overhead_ns\": %.2f, \"mean_ns_timed\": %.3f,", m, ovh / tpn, mean / m);
    printf(" \"pct\": {\"50\": %u, \"90\": %u, \"99\": %u, \"99.9\": %u, \"99.99\": %u, \"100\": %u},",
           lat[m / 2], lat[(size_t)(m * 0.9)], lat[(size_t)(m * 0.99)], lat[(size_t)(m * 0.999)], lat[(size_t)(m * 0.9999)], lat[m - 1]);
    uint64_t h[140] = {0};
    for (size_t i = 0; i < m; i++) { double x = lat[i] < 1 ? 1 : lat[i]; int bb = (int)(log10(x) * 20); if (bb > 139) bb = 139; h[bb]++; }
    printf(" \"hist\": [");
    for (int i = 0; i < 140; i++) printf("%s%lu", i ? "," : "", (unsigned long)h[i]);
    printf("], \"end_best_bid_cents\": %ld, \"end_best_ask_cents\": %ld}\n", (long)end_bid, (long)end_ask);
    return 0;
}
