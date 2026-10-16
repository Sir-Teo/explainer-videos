/* Latency microbenchmarks for the trading video, run on the machine that renders it.
 * Built and run by videos/trading/compute.py:   bench MODE  ->  JSON on stdout
 *
 *   chase      pointer-chasing load latency vs working-set size, 4 KiB pages and 2 MiB huge pages
 *   syscall    a trivial system call (getppid) and a vDSO clock read
 *   pingpong   one-way latency between two pinned cores: a shared cache line, kernel UDP over loopback
 *              (busy-polling and blocking), as distributions
 *   spsc       a single-producer single-consumer ring buffer: per-message latency and throughput
 *   falseshare two threads incrementing their own counters, on one cache line vs two
 *   branch     the same loop over sorted and shuffled data (branch prediction)
 *   jitter     a pinned core spinning on the clock: every gap > 300 ns it loses to the OS
 */
#define _GNU_SOURCE
#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <pthread.h>
#include <sched.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#include <time.h>
#include <unistd.h>
#include <x86intrin.h>
#include <math.h>

static double TPN; /* TSC ticks per nanosecond */

static uint64_t now_ns(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return (uint64_t)t.tv_sec * 1000000000ULL + t.tv_nsec;
}
static inline uint64_t tsc(void) { unsigned a; return __rdtscp(&a); }
static void calibrate(void) {
    uint64_t n0 = now_ns(), t0 = tsc();
    while (now_ns() - n0 < 200000000ULL) {}
    uint64_t n1 = now_ns(), t1 = tsc();
    TPN = (double)(t1 - t0) / (double)(n1 - n0);
}
static void pin(int cpu) {
    cpu_set_t s;
    CPU_ZERO(&s);
    CPU_SET(cpu, &s);
    pthread_setaffinity_np(pthread_self(), sizeof s, &s);
}
static int cmp_u32(const void *a, const void *b) { uint32_t x = *(const uint32_t *)a, y = *(const uint32_t *)b; return x < y ? -1 : x > y; }

/* Print a latency sample (in ns) as percentiles plus a log-binned histogram (20 bins per decade, 1 ns..1 s). */
static void emit_dist(const char *name, uint32_t *v, size_t n, int last) {
    qsort(v, n, sizeof *v, cmp_u32);
    double q[] = {0.0, 0.01, 0.1, 0.5, 0.9, 0.99, 0.999, 0.9999, 1.0};
    printf("  \"%s\": {\"n\": %zu, \"pct\": {", name, n);
    for (int i = 0; i < 9; i++) {
        size_t k = (size_t)(q[i] * (n - 1));
        printf("%s\"%g\": %u", i ? ", " : "", q[i] * 100, v[k]);
    }
    double mean = 0;
    for (size_t i = 0; i < n; i++) mean += v[i];
    printf("}, \"mean\": %.2f, \"hist\": [", mean / n);
    uint64_t h[180] = {0};
    for (size_t i = 0; i < n; i++) {
        double x = v[i] < 1 ? 1 : v[i];
        int b = (int)(log10(x) * 20);
        if (b > 179) b = 179;
        h[b]++;
    }
    for (int i = 0; i < 180; i++) printf("%s%lu", i ? "," : "", (unsigned long)h[i]);
    printf("]}%s\n", last ? "" : ",");
}

/* ---------------------------------------------------------------- chase */
static uint64_t rng = 88172645463325252ULL;
static inline uint64_t xr(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }

static double chase_one(size_t bytes, int huge) {
    size_t map = (bytes + (2u << 20) - 1) & ~((size_t)(2u << 20) - 1);
    char *mem = mmap(NULL, map + (2u << 20), PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    char *base = (char *)(((uintptr_t)mem + (2u << 20) - 1) & ~((uintptr_t)(2u << 20) - 1));
    madvise(base, map, huge ? MADV_HUGEPAGE : MADV_NOHUGEPAGE);
    size_t lines = bytes / 64;
    uint32_t *perm = malloc(lines * sizeof *perm);
    for (size_t i = 0; i < lines; i++) perm[i] = (uint32_t)i;
    for (size_t i = lines - 1; i > 0; i--) { /* Sattolo: one big cycle */
        size_t j = xr() % i;
        uint32_t t = perm[i]; perm[i] = perm[j]; perm[j] = t;
    }
    for (size_t i = 0; i < lines; i++) *(char **)(base + (size_t)perm[i] * 64) = base + (size_t)perm[(i + 1) % lines] * 64;
    free(perm);
    char *p = base;
    for (size_t i = 0; i < lines * 2 && i < 4000000; i++) p = *(char **)p; /* warm */
    size_t steps = 20000000;
    if (bytes > (64u << 20)) steps = 8000000;
    uint64_t t0 = now_ns();
    for (size_t i = 0; i < steps; i++) p = *(char **)p;
    uint64_t t1 = now_ns();
    if (!p) puts("");
    munmap(mem, map + (2u << 20));
    return (double)(t1 - t0) / steps;
}

static void mode_chase(void) {
    pin(1);
    printf("{\n  \"sizes\": [");
    int first = 1;
    double sizes[64]; int ns = 0;
    for (double lg = 12; lg <= 30.01; lg += 0.5) sizes[ns++] = pow(2, lg);
    for (int i = 0; i < ns; i++) { printf("%s%.0f", first ? "" : ", ", sizes[i]); first = 0; }
    printf("],\n");
    for (int huge = 0; huge < 2; huge++) {
        printf("  \"%s\": [", huge ? "huge" : "small");
        for (int i = 0; i < ns; i++) {
            size_t b = ((size_t)sizes[i] / 64) * 64;
            double best = 1e9;
            for (int r = 0; r < (b > (32u << 20) ? 1 : 3); r++) { double x = chase_one(b, huge); if (x < best) best = x; }
            printf("%s%.3f", i ? ", " : "", best);
            fflush(stdout);
        }
        printf("]%s\n", huge ? "" : ",");
    }
    printf("}\n");
}

/* ---------------------------------------------------------------- syscall */
static void mode_syscall(void) {
    pin(1);
    int n = 2000000;
    for (int i = 0; i < 100000; i++) syscall(SYS_getppid);
    uint64_t t0 = now_ns();
    for (int i = 0; i < n; i++) syscall(SYS_getppid);
    uint64_t t1 = now_ns();
    struct timespec ts;
    uint64_t t2 = now_ns();
    for (int i = 0; i < n; i++) clock_gettime(CLOCK_MONOTONIC, &ts);
    uint64_t t3 = now_ns();
    uint64_t t4 = now_ns();
    volatile uint64_t s = 0;
    for (int i = 0; i < n; i++) s += tsc();
    uint64_t t5 = now_ns();
    printf("{\"getppid_ns\": %.2f, \"clock_gettime_ns\": %.2f, \"rdtscp_ns\": %.2f, \"tsc_per_ns\": %.4f}\n",
           (double)(t1 - t0) / n, (double)(t3 - t2) / n, (double)(t5 - t4) / n, TPN);
}

/* ---------------------------------------------------------------- ping-pong */
#define PP_N 200000
#define PP_WARM 20000
static _Alignas(64) _Atomic uint64_t ball_a;
static _Alignas(64) _Atomic uint64_t ball_b;
static uint32_t pp_out[PP_N];

static void *pp_shm_echo(void *arg) {
    (void)arg;
    pin(3);
    for (uint64_t i = 1; i <= PP_N + PP_WARM; i++) {
        while (atomic_load_explicit(&ball_a, memory_order_acquire) != i) {}
        atomic_store_explicit(&ball_b, i, memory_order_release);
    }
    return NULL;
}
static void pp_shm(void) {
    pthread_t th;
    atomic_store(&ball_a, 0); atomic_store(&ball_b, 0);
    pthread_create(&th, NULL, pp_shm_echo, NULL);
    pin(2);
    for (uint64_t i = 1; i <= PP_N + PP_WARM; i++) {
        uint64_t t0 = tsc();
        atomic_store_explicit(&ball_a, i, memory_order_release);
        while (atomic_load_explicit(&ball_b, memory_order_acquire) != i) {}
        uint64_t t1 = tsc();
        if (i > PP_WARM) pp_out[i - PP_WARM - 1] = (uint32_t)((t1 - t0) / TPN / 2);
    }
    pthread_join(th, NULL);
}

static int udp_sock(int port) {
    int s = socket(AF_INET, SOCK_DGRAM, 0);
    struct sockaddr_in a = {.sin_family = AF_INET, .sin_port = htons(port), .sin_addr.s_addr = htonl(INADDR_LOOPBACK)};
    bind(s, (struct sockaddr *)&a, sizeof a);
    return s;
}
static int udp_busy;
static void *pp_udp_echo(void *arg) {
    (void)arg;
    pin(3);
    int s = udp_sock(47002);
    struct sockaddr_in to = {.sin_family = AF_INET, .sin_port = htons(47001), .sin_addr.s_addr = htonl(INADDR_LOOPBACK)};
    char buf[64];
    for (int i = 0; i < PP_N + PP_WARM; i++) {
        ssize_t r;
        do r = recv(s, buf, sizeof buf, udp_busy ? MSG_DONTWAIT : 0); while (r < 0);
        sendto(s, buf, 64, 0, (struct sockaddr *)&to, sizeof to);
    }
    close(s);
    return NULL;
}
static void pp_udp(int busy) {
    udp_busy = busy;
    int s = udp_sock(47001);
    pthread_t th;
    pthread_create(&th, NULL, pp_udp_echo, NULL);
    usleep(100000);
    pin(2);
    struct sockaddr_in to = {.sin_family = AF_INET, .sin_port = htons(47002), .sin_addr.s_addr = htonl(INADDR_LOOPBACK)};
    char buf[64] = {0};
    for (int i = 0; i < PP_N + PP_WARM; i++) {
        uint64_t t0 = tsc();
        sendto(s, buf, 64, 0, (struct sockaddr *)&to, sizeof to);
        ssize_t r;
        do r = recv(s, buf, sizeof buf, busy ? MSG_DONTWAIT : 0); while (r < 0);
        uint64_t t1 = tsc();
        if (i >= PP_WARM) pp_out[i - PP_WARM] = (uint32_t)((t1 - t0) / TPN / 2);
    }
    pthread_join(th, NULL);
    close(s);
}
static void mode_pingpong(void) {
    printf("{\n");
    pp_shm();
    emit_dist("shared_cache_line", pp_out, PP_N, 0);
    pp_udp(1);
    emit_dist("udp_busy_poll", pp_out, PP_N, 0);
    pp_udp(0);
    emit_dist("udp_blocking", pp_out, PP_N, 1);
    printf("}\n");
}

/* ---------------------------------------------------------------- spsc ring */
#define RING 1024
struct slot { uint64_t stamp; uint64_t seq; char payload[48]; };
static _Alignas(64) struct slot ring[RING];
static _Alignas(64) _Atomic uint64_t head; /* written by producer */
static _Alignas(64) _Atomic uint64_t tail; /* written by consumer */
#define SP_N 2000000
static uint32_t sp_lat[SP_N];
static int sp_paced;
static void *spsc_consumer(void *arg) {
    (void)arg;
    pin(3);
    uint64_t t = 0;
    while (t < SP_N) {
        uint64_t h;
        while ((h = atomic_load_explicit(&head, memory_order_acquire)) == t) {}
        for (; t < h; t++) {
            struct slot *s = &ring[t & (RING - 1)];
            uint64_t now = tsc();
            sp_lat[t] = (uint32_t)((now - s->stamp) / TPN);
        }
        atomic_store_explicit(&tail, t, memory_order_release);
    }
    return NULL;
}
static double spsc_run(int paced) {
    sp_paced = paced;
    atomic_store(&head, 0); atomic_store(&tail, 0);
    pthread_t th;
    pthread_create(&th, NULL, spsc_consumer, NULL);
    pin(2);
    uint64_t t0 = now_ns();
    uint64_t cached_tail = 0;
    for (uint64_t h = 0; h < SP_N; h++) {
        while (h - cached_tail >= RING) cached_tail = atomic_load_explicit(&tail, memory_order_acquire);
        if (paced) { uint64_t w = tsc() + (uint64_t)(500 * TPN); while (tsc() < w) {} } /* one message every ~0.5 us */
        struct slot *s = &ring[h & (RING - 1)];
        s->seq = h;
        s->stamp = tsc();
        atomic_store_explicit(&head, h + 1, memory_order_release);
    }
    pthread_join(th, NULL);
    uint64_t t1 = now_ns();
    return (double)SP_N / ((t1 - t0) / 1e9);
}
static void mode_spsc(void) {
    printf("{\n");
    double rate = spsc_run(0);
    printf("  \"throughput_msgs_per_s\": %.0f,\n", rate);
    spsc_run(1);
    emit_dist("paced_latency", sp_lat, SP_N, 1);
    printf("}\n");
}

/* ---------------------------------------------------------------- false sharing */
struct pair_same { _Atomic uint64_t a; _Atomic uint64_t b; } __attribute__((aligned(64)));
struct pair_apart { _Atomic uint64_t a; char pad[120]; _Atomic uint64_t b; } __attribute__((aligned(128)));
static struct pair_same ps;
static struct pair_apart pa;
#define FS_N 50000000ULL
struct fs_arg { _Atomic uint64_t *c; int cpu; };
static void *fs_worker(void *v) {
    struct fs_arg *a = v;
    pin(a->cpu);
    for (uint64_t i = 0; i < FS_N; i++) atomic_fetch_add_explicit(a->c, 1, memory_order_relaxed);
    return NULL;
}
static double fs_run(_Atomic uint64_t *x, _Atomic uint64_t *y) {
    pthread_t t1, t2;
    struct fs_arg a1 = {x, 2}, a2 = {y, 3};
    uint64_t t0 = now_ns();
    pthread_create(&t1, NULL, fs_worker, &a1);
    pthread_create(&t2, NULL, fs_worker, &a2);
    pthread_join(t1, NULL); pthread_join(t2, NULL);
    return (double)(now_ns() - t0) / FS_N;
}
static void mode_falseshare(void) {
    double same = 1e9, apart = 1e9;
    for (int r = 0; r < 3; r++) {
        double s = fs_run(&ps.a, &ps.b), a = fs_run(&pa.a, &pa.b);
        if (s < same) same = s;
        if (a < apart) apart = a;
    }
    printf("{\"same_line_ns_per_increment\": %.3f, \"separate_lines_ns_per_increment\": %.3f}\n", same, apart);
}

/* ---------------------------------------------------------------- branch */
#define BR_N (1 << 24)
static unsigned char br_data[BR_N];
static int cmp_u8(const void *a, const void *b) { return *(const unsigned char *)a - *(const unsigned char *)b; }
__attribute__((noinline, optimize("O1"))) static uint64_t branchy(const unsigned char *d, size_t n) {
    uint64_t s = 0;
    for (size_t i = 0; i < n; i++) {
        if (d[i] >= 128) { s += d[i]; __asm__ volatile("" ::: "memory"); }
    }
    return s;
}
static void mode_branch(void) {
    pin(1);
    for (int i = 0; i < BR_N; i++) br_data[i] = (unsigned char)(xr() & 255);
    double best_r = 1e9, best_s = 1e9;
    volatile uint64_t sink = 0;
    for (int r = 0; r < 5; r++) {
        uint64_t t0 = now_ns(); sink += branchy(br_data, BR_N); uint64_t t1 = now_ns();
        double x = (double)(t1 - t0) / BR_N; if (x < best_r) best_r = x;
    }
    qsort(br_data, BR_N, 1, cmp_u8);
    for (int r = 0; r < 5; r++) {
        uint64_t t0 = now_ns(); sink += branchy(br_data, BR_N); uint64_t t1 = now_ns();
        double x = (double)(t1 - t0) / BR_N; if (x < best_s) best_s = x;
    }
    printf("{\"shuffled_ns_per_element\": %.3f, \"sorted_ns_per_element\": %.3f}\n", best_r, best_s);
}

/* ---------------------------------------------------------------- jitter */
#define JT_MAX 200000
static uint64_t jt_at[JT_MAX];
static uint32_t jt_gap[JT_MAX];
static void mode_jitter(void) {
    pin(2);
    uint64_t dur = (uint64_t)(10e9 * TPN), thr = (uint64_t)(300 * TPN);
    size_t n = 0;
    uint64_t start = tsc(), prev = start, end = start + dur, loops = 0;
    for (;;) {
        uint64_t t = tsc();
        loops++;
        if (t - prev > thr && n < JT_MAX) { jt_at[n] = (uint64_t)((prev - start) / TPN); jt_gap[n] = (uint32_t)((t - prev) / TPN); n++; }
        prev = t;
        if (t > end) break;
    }
    uint64_t lost = 0;
    for (size_t i = 0; i < n; i++) lost += jt_gap[i];
    printf("{\"seconds\": 10, \"threshold_ns\": 300, \"loops\": %lu, \"events\": %zu, \"lost_ns\": %lu, \"at_ns\": [",
           (unsigned long)loops, n, (unsigned long)lost);
    for (size_t i = 0; i < n; i++) printf("%s%lu", i ? "," : "", (unsigned long)jt_at[i]);
    printf("], \"gap_ns\": [");
    for (size_t i = 0; i < n; i++) printf("%s%u", i ? "," : "", jt_gap[i]);
    printf("]}\n");
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: bench chase|syscall|pingpong|spsc|falseshare|branch|jitter\n"); return 2; }
    calibrate();
    const char *m = argv[1];
    if (!strcmp(m, "chase")) mode_chase();
    else if (!strcmp(m, "syscall")) mode_syscall();
    else if (!strcmp(m, "pingpong")) mode_pingpong();
    else if (!strcmp(m, "spsc")) mode_spsc();
    else if (!strcmp(m, "falseshare")) mode_falseshare();
    else if (!strcmp(m, "branch")) mode_branch();
    else if (!strcmp(m, "jitter")) mode_jitter();
    else { fprintf(stderr, "unknown mode %s\n", m); return 2; }
    return 0;
}
