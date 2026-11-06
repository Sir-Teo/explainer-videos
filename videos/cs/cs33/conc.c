/* Part 33's measurements on this machine: races, locks and hardware transactions.
 *   conc race <threads> <n>        plain, atomic and mutex counters: final value and ns per increment
 *   conc lock <kind> <threads> <n> tas, ttas, ticket, mcs, mutex: ns per acquisition, and each thread's share
 *   conc tsx <n>                   how many RTM transactions commit (Intel TSX), if the instructions run at all
 *   conc spawn <n>                 microseconds to create and join a thread, and to fork and wait for a process
 */
#define _GNU_SOURCE
#include <pthread.h>
#include <signal.h>
#include <setjmp.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <immintrin.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }

/* ---------------- the race ---------------- */
static volatile long plain;
static _Atomic long atom;
static long locked;
static pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;
static long N;
static int MODE;
static pthread_barrier_t bar;

static void *inc(void *arg) {
    (void)arg;
    pthread_barrier_wait(&bar);
    if (MODE == 0) for (long i = 0; i < N; i++) plain = plain + 1;
    else if (MODE == 1) for (long i = 0; i < N; i++) atomic_fetch_add(&atom, 1);
    else for (long i = 0; i < N; i++) { pthread_mutex_lock(&mtx); locked++; pthread_mutex_unlock(&mtx); }
    return NULL;
}

static void race(int T, long n) {
    const char *names[] = {"plain", "atomic", "mutex"};
    for (MODE = 0; MODE < 3; MODE++) {
        plain = 0; atom = 0; locked = 0; N = n;
        pthread_t th[64];
        pthread_barrier_init(&bar, NULL, T);
        double t0 = now();
        for (int i = 0; i < T; i++) pthread_create(&th[i], NULL, inc, NULL);
        for (int i = 0; i < T; i++) pthread_join(th[i], NULL);
        double dt = now() - t0;
        long v = MODE == 0 ? plain : MODE == 1 ? atom : locked;
        printf("%s %d %ld %ld %.3f\n", names[MODE], T, v, (long)T * n, 1e9 * dt / ((double)T * n));
        pthread_barrier_destroy(&bar);
    }
}

/* ---------------- locks ---------------- */
static _Atomic int tas_l;
static _Atomic unsigned next_t, serving;
typedef struct qnode { _Atomic(struct qnode *) next; _Atomic int locked; char pad[48]; } qnode;
static _Atomic(qnode *) tail;
static int KIND;
static long shared_data;
static long per[64];

static void lk(qnode *me) {
    if (KIND == 0) { while (atomic_exchange_explicit(&tas_l, 1, memory_order_acquire)) ; }
    else if (KIND == 1) {
        for (;;) {
            while (atomic_load_explicit(&tas_l, memory_order_relaxed)) __builtin_ia32_pause();
            if (!atomic_exchange_explicit(&tas_l, 1, memory_order_acquire)) return;
        }
    } else if (KIND == 2) {
        unsigned t = atomic_fetch_add_explicit(&next_t, 1, memory_order_relaxed);
        while (atomic_load_explicit(&serving, memory_order_acquire) != t) __builtin_ia32_pause();
    } else if (KIND == 3) {
        atomic_store_explicit(&me->next, NULL, memory_order_relaxed);
        atomic_store_explicit(&me->locked, 1, memory_order_relaxed);
        qnode *pred = atomic_exchange_explicit(&tail, me, memory_order_acq_rel);
        if (pred) {
            atomic_store_explicit(&pred->next, me, memory_order_release);
            while (atomic_load_explicit(&me->locked, memory_order_acquire)) __builtin_ia32_pause();
        }
    } else pthread_mutex_lock(&mtx);
}

static void ulk(qnode *me) {
    if (KIND <= 1) atomic_store_explicit(&tas_l, 0, memory_order_release);
    else if (KIND == 2) atomic_fetch_add_explicit(&serving, 1, memory_order_release);
    else if (KIND == 3) {
        qnode *succ = atomic_load_explicit(&me->next, memory_order_acquire);
        if (!succ) {
            qnode *expect = me;
            if (atomic_compare_exchange_strong_explicit(&tail, &expect, NULL, memory_order_acq_rel,
                                                        memory_order_acquire)) return;
            while (!(succ = atomic_load_explicit(&me->next, memory_order_acquire))) __builtin_ia32_pause();
        }
        atomic_store_explicit(&succ->locked, 0, memory_order_release);
    } else pthread_mutex_unlock(&mtx);
}

static _Atomic int stop;
static void *worker(void *arg) {
    long id = (long)arg;
    qnode me;
    pthread_barrier_wait(&bar);
    long k = 0;
    while (!atomic_load_explicit(&stop, memory_order_relaxed)) {
        lk(&me);
        shared_data++;
        ulk(&me);
        k++;
    }
    per[id] = k;
    return NULL;
}

static void locks(const char *kind, int T, double secs) {
    const char *names[] = {"tas", "ttas", "ticket", "mcs", "mutex"};
    for (KIND = 0; KIND < 5; KIND++) if (!strcmp(kind, names[KIND])) break;
    tas_l = 0; next_t = 0; serving = 0; tail = NULL; shared_data = 0; stop = 0;
    pthread_t th[64];
    pthread_barrier_init(&bar, NULL, T + 1);
    for (long i = 0; i < T; i++) pthread_create(&th[i], NULL, worker, (void *)i);
    pthread_barrier_wait(&bar);
    double t0 = now();
    struct timespec d = {(time_t)secs, (long)((secs - (long)secs) * 1e9)};
    nanosleep(&d, NULL);
    atomic_store(&stop, 1);
    for (int i = 0; i < T; i++) pthread_join(th[i], NULL);
    double dt = now() - t0;
    long total = 0, mn = per[0], mx = per[0];
    for (int i = 0; i < T; i++) { total += per[i]; if (per[i] < mn) mn = per[i]; if (per[i] > mx) mx = per[i]; }
    printf("%s %d %ld %.2f %.3f %ld\n", kind, T, total, 1e9 * dt / total, (double)mn / mx, shared_data);
    pthread_barrier_destroy(&bar);
}

/* ---------------- hardware transactions ---------------- */
static sigjmp_buf jb;
static void onill(int s) { (void)s; siglongjmp(jb, 1); }
__attribute__((target("rtm"))) static int try_rtm(volatile long *x) {
    unsigned st = _xbegin();
    if (st == _XBEGIN_STARTED) { (*x)++; _xend(); return 1; }
    return 0;
}
static void tsx(long n) {
    signal(SIGILL, onill);
    volatile long x = 0;
    if (sigsetjmp(jb, 1)) { printf("tsx illegal 0 %ld\n", n); return; }
    long ok = 0;
    for (long i = 0; i < n; i++) ok += try_rtm(&x);
    printf("tsx ran %ld %ld\n", ok, n);
}

/* ---------------- a thread against a process ---------------- */
#include <sys/wait.h>
#include <unistd.h>
static void *nothing(void *a) { return a; }
static void spawn(int n) {
    double t0 = now();
    for (int i = 0; i < n; i++) { pthread_t t; pthread_create(&t, NULL, nothing, NULL); pthread_join(t, NULL); }
    double th = (now() - t0) / n;
    t0 = now();
    for (int i = 0; i < n; i++) { pid_t p = fork(); if (!p) _exit(0); waitpid(p, NULL, 0); }
    double pr = (now() - t0) / n;
    printf("spawn %.2f %.2f\n", th * 1e6, pr * 1e6);
}

int main(int argc, char **argv) {
    if (argc > 1 && !strcmp(argv[1], "race")) race(atoi(argv[2]), atol(argv[3]));
    else if (argc > 1 && !strcmp(argv[1], "lock")) locks(argv[2], atoi(argv[3]), atof(argv[4]));
    else if (argc > 1 && !strcmp(argv[1], "tsx")) tsx(atol(argv[2]));
    else if (argc > 1 && !strcmp(argv[1], "spawn")) spawn(atoi(argv[2]));
    return 0;
}
