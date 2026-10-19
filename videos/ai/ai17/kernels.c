/* The kernels Part 17 measures on the machine that renders it (compiled at compute time by native.py).
 *
 * Plain C99 with GCC/Clang vector extensions, so the same file builds with gcc on Linux and Apple clang on macOS
 * (x86-64 or arm64). Single-threaded on purpose: these measure one core.
 *
 *   read_sum      stream an array and add it up (the memory hierarchy, bandwidth per level)
 *   triad, copy   STREAM's triad a = b + s*c and copy a = b (main-memory bandwidth)
 *   chase         follow a random cycle of pointers (the latency of each level)
 *   mm_naive      C = AB, the textbook triple loop: a dot product per output, B read down its columns
 *   mm_ikj        the same arithmetic, loops reordered so every inner loop streams along rows
 *   mm_blocked    the same arithmetic, in bs x bs tiles that stay in cache while they are reused
 *   alloc_big     memory aligned to 2 MiB, asking Linux for huge pages, so that a random walk measures the caches
 *                 and not the address-translation cache (TLB)
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#ifdef __linux__
#include <sys/mman.h>
#endif

typedef float v8f __attribute__((vector_size(32)));

static inline v8f load8(const float *p) {
    v8f v;
    memcpy(&v, p, sizeof v);
    return v;
}

void *alloc_big(size_t bytes) {
    void *p = NULL;
    size_t align = (size_t)2 << 20;
    size_t n = (bytes + align - 1) / align * align;
    if (posix_memalign(&p, align, n) != 0) return NULL;
#ifdef __linux__
#ifdef MADV_HUGEPAGE
    madvise(p, n, MADV_HUGEPAGE);
#endif
#endif
    memset(p, 0, n);
    return p;
}

void free_big(void *p) { free(p); }

/* n must be a multiple of 64; eight independent sums keep enough loads in flight to see each cache's bandwidth */
float read_sum(const float *a, long n, long reps) {
    v8f s0 = {0}, s1 = {0}, s2 = {0}, s3 = {0}, s4 = {0}, s5 = {0}, s6 = {0}, s7 = {0};
    for (long r = 0; r < reps; r++) {
        for (long i = 0; i < n; i += 64) {
            s0 += load8(a + i);
            s1 += load8(a + i + 8);
            s2 += load8(a + i + 16);
            s3 += load8(a + i + 24);
            s4 += load8(a + i + 32);
            s5 += load8(a + i + 40);
            s6 += load8(a + i + 48);
            s7 += load8(a + i + 56);
        }
    }
    v8f s = (s0 + s1) + (s2 + s3) + (s4 + s5) + (s6 + s7);
    float t = 0.0f;
    for (int k = 0; k < 8; k++) t += s[k];
    return t;
}

void triad(float *restrict a, const float *restrict b, const float *restrict c, float s, long n, long reps) {
    for (long r = 0; r < reps; r++) {
        for (long i = 0; i < n; i++) a[i] = b[i] + s * c[i];
        __asm__ __volatile__("" ::: "memory");
    }
}

void copy(float *restrict a, const float *restrict b, long n, long reps) {
    for (long r = 0; r < reps; r++) {
        for (long i = 0; i < n; i++) a[i] = b[i];
        __asm__ __volatile__("" ::: "memory");
    }
}

/* next[i] holds the index of the next node; nodes sit one cache line (8 int64) apart */
int64_t chase(const int64_t *next, long steps) {
    int64_t i = 0;
    for (long s = 0; s < steps; s++) i = next[i];
    return i;
}

void mm_naive(const float *A, const float *B, float *C, int n) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            float s = 0.0f;
            for (int k = 0; k < n; k++) s += A[(long)i * n + k] * B[(long)k * n + j];
            C[(long)i * n + j] = s;
        }
}

void mm_ikj(const float *A, const float *B, float *restrict C, int n) {
    memset(C, 0, sizeof(float) * (size_t)n * n);
    for (int i = 0; i < n; i++)
        for (int k = 0; k < n; k++) {
            float a = A[(long)i * n + k];
            const float *b = B + (long)k * n;
            float *c = C + (long)i * n;
            for (int j = 0; j < n; j++) c[j] += a * b[j];
        }
}

void mm_blocked(const float *A, const float *B, float *restrict C, int n, int bs) {
    memset(C, 0, sizeof(float) * (size_t)n * n);
    for (int ii = 0; ii < n; ii += bs)
        for (int kk = 0; kk < n; kk += bs)
            for (int jj = 0; jj < n; jj += bs) {
                int ie = ii + bs < n ? ii + bs : n, ke = kk + bs < n ? kk + bs : n, je = jj + bs < n ? jj + bs : n;
                for (int i = ii; i < ie; i++)
                    for (int k = kk; k < ke; k++) {
                        float a = A[(long)i * n + k];
                        const float *b = B + (long)k * n;
                        float *c = C + (long)i * n;
                        for (int j = jj; j < je; j++) c[j] += a * b[j];
                    }
            }
}
