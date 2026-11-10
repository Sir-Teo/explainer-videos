"""The Job v1 (Part 16): sort, then count, in the Pebble language.

Every word of the text is recorded as an occurrence (where its letters start in the pool, and its length).  A stable
merge sort orders the occurrences by their letters, so equal words become neighbours and the first occurrence of
each word comes first among them.  One pass over the sorted order counts each run of equal words and remembers its
first position, and the report picks the twenty largest counts, ties broken by first position: exactly the output
of the Job v0 (``programs.job_reference``).

    c = compile_job()                 # Part 13's compiler, -O2
    m = run(c, text)                  # the emulator; m.steps
    features(text)                    # event counts used to fit m.steps (see fit / predict)

The running time is not a fixed multiple of the text any more, so the ledger cannot scale it by bytes. Instead the
emulator's instruction count is fitted, by least squares on passages of many sizes, as a linear function of
counts that Python computes from the text alone (bytes, letters, words, merge comparisons, letters compared inside
those comparisons, merge moves, distinct words, report work); the fit is checked on passages it did not see, and
then applied to the counts of the full thirty novels.
"""
from __future__ import annotations

JOB_SORT = r"""
// The Job v1: sort the words, then count runs of equal words.
var pool: [262144]char;
var used: int = 0;
var wstart: [32768]int;
var wlen: [32768]int;
var nw: int = 0;
var idx: [32768]int;
var tmp: [32768]int;
var ecount: [16384]int;
var efirst: [16384]int;
var ne: int = 0;

// compare occurrences a and b by their letters: negative, zero or positive
fn cmpw(a: int, b: int) -> int {
    var p: int = wstart[a];
    var q: int = wstart[b];
    var la: int = wlen[a];
    var lb: int = wlen[b];
    var n: int = la;
    if lb < n { n = lb; }
    var k: int = 0;
    while k < n {
        var d: int = pool[p + k] - pool[q + k];
        if d != 0 { return d; }
        k = k + 1;
    }
    return la - lb;
}

// stable bottom-up merge sort of idx[0..nw)
fn sortw() {
    var width: int = 1;
    while width < nw {
        var lo: int = 0;
        while lo < nw {
            var mid: int = lo + width;
            if mid > nw { mid = nw; }
            var hi: int = lo + 2 * width;
            if hi > nw { hi = nw; }
            var i: int = lo;
            var j: int = mid;
            var o: int = lo;
            while i < mid && j < hi {
                if cmpw(idx[j], idx[i]) < 0 { tmp[o] = idx[j]; j = j + 1; }
                else { tmp[o] = idx[i]; i = i + 1; }
                o = o + 1;
            }
            while i < mid { tmp[o] = idx[i]; i = i + 1; o = o + 1; }
            while j < hi { tmp[o] = idx[j]; j = j + 1; o = o + 1; }
            lo = hi;
        }
        var k: int = 0;
        while k < nw { idx[k] = tmp[k]; k = k + 1; }
        width = 2 * width;
    }
}

fn printnum(n: int) {
    var digits: [12]char;
    var k: int = 0;
    if n == 0 { putc('0'); return; }
    while n > 0 { digits[k] = '0' + n % 10; n = n / 10; k = k + 1; }
    while k > 0 { k = k - 1; putc(digits[k]); }
}

fn main() -> int {
    var n: int = 0;
    var c: int = getc();
    while c != -1 {
        if c >= 'A' && c <= 'Z' { c = c + 32; }
        if c >= 'a' && c <= 'z' {
            pool[used + n] = c;
            n = n + 1;
        } else if n > 0 {
            wstart[nw] = used; wlen[nw] = n; idx[nw] = nw; nw = nw + 1;
            used = used + n;
            n = 0;
        }
        c = getc();
    }
    if n > 0 { wstart[nw] = used; wlen[nw] = n; idx[nw] = nw; nw = nw + 1; used = used + n; }
    sortw();
    // runs of equal words: count, and the first occurrence (stable sort: the first in the run)
    var i: int = 0;
    while i < nw {
        var j: int = i + 1;
        while j < nw && cmpw(idx[i], idx[j]) == 0 { j = j + 1; }
        ecount[ne] = j - i;
        efirst[ne] = idx[i];
        ne = ne + 1;
        i = j;
    }
    // the report: twenty times, the largest count, ties to the earliest first occurrence
    var shown: int = 0;
    while shown < 20 {
        var best: int = 0;
        var at: int = -1;
        var e: int = 0;
        while e < ne {
            if ecount[e] > best || (ecount[e] == best && best > 0 && efirst[e] < efirst[at]) {
                best = ecount[e]; at = e;
            }
            e = e + 1;
        }
        if best == 0 { return 0; }
        var w: int = efirst[at];
        var k: int = 0;
        while k < wlen[w] { putc(pool[wstart[w] + k]); k = k + 1; }
        putc(' ');
        printnum(best);
        putc('\n');
        ecount[at] = 0;
        shown = shown + 1;
    }
    return 0;
}
"""


def job_source(*,word_capacity=32768,letter_capacity=262144,distinct_capacity=16384):
    """Size the static arrays explicitly; callers still must provide sufficient emulated RAM."""
    sizes=(word_capacity,letter_capacity,distinct_capacity)
    if any(not isinstance(n,int) or n<=0 for n in sizes):
        raise ValueError("Job capacities must be positive integers")
    return (JOB_SORT.replace("[262144]char",f"[{letter_capacity}]char")
            .replace("[32768]int",f"[{word_capacity}]int")
            .replace("[16384]int",f"[{distinct_capacity}]int"))


def compile_job(level:int=2,**capacities):
    from explainer.cs.lang.compiler import driver as D
    return D.compile_program(job_source(**capacities),level)


def run(c, text: bytes, **kw):
    from explainer.cs.lang.compiler import driver as D
    return D.run(c, text, **kw)


def features(text: bytes) -> dict:
    """The events the Job v1's instruction count depends on, counted in Python by following the program's control
    flow exactly (every loop iteration and every branch taken), from the text alone."""
    from explainer.cs.pebble import programs as PR
    f = dict.fromkeys(["bytes", "letters", "capitals", "words", "passes", "merges", "sort_cmp", "sort_right",
                       "tail_copies", "copy_back", "k_steps", "ret_diff", "ret_len", "short_n", "scan_cmp",
                       "runs", "rep_iter", "rep_gt", "rep_eq", "rep_tie_win", "rep_update", "printed", "digits",
                       "shown"], 0)
    f["bytes"] = len(text)
    f["capitals"] = sum(1 for b in text if 65 <= b <= 90)
    words = list(PR.job_words(text))
    n = len(words)
    f["words"] = n
    f["letters"] = sum(len(w) for w in words)

    def cmpw(a, b):
        x, y = words[a], words[b]
        m = min(len(x), len(y))
        if len(y) < len(x):
            f["short_n"] += 1
        k = 0
        while k < m:
            f["k_steps"] += 1
            if x[k] != y[k]:
                f["ret_diff"] += 1
                return x[k] - y[k]
            k += 1
        f["ret_len"] += 1
        return len(x) - len(y)
    idx = list(range(n))
    width = 1
    while width < n:
        f["passes"] += 1
        tmp = [0] * n
        lo = 0
        while lo < n:
            f["merges"] += 1
            mid, hi = min(lo + width, n), min(lo + 2 * width, n)
            i, j, o = lo, mid, lo
            while i < mid and j < hi:
                f["sort_cmp"] += 1
                if cmpw(idx[j], idx[i]) < 0:
                    f["sort_right"] += 1
                    tmp[o] = idx[j]
                    j += 1
                else:
                    tmp[o] = idx[i]
                    i += 1
                o += 1
            f["tail_copies"] += (mid - i) + (hi - j)
            tmp[o:hi] = idx[i:mid] + idx[j:hi]
            lo = hi
        f["copy_back"] += n
        idx = tmp
        width *= 2
    counts, firsts = [], []
    i = 0
    while i < n:
        j = i + 1
        while j < n:
            f["scan_cmp"] += 1
            if cmpw(idx[i], idx[j]) != 0:
                break
            j += 1
        counts.append(j - i)
        firsts.append(idx[i])
        i = j
    f["runs"] = len(counts)
    for shown in range(20):
        best, at = 0, -1
        for e in range(len(counts)):
            f["rep_iter"] += 1
            if counts[e] > best:
                f["rep_gt"] += 1
                best, at = counts[e], e
                f["rep_update"] += 1
            elif counts[e] == best:
                f["rep_eq"] += 1
                if best > 0 and firsts[e] < firsts[at]:
                    f["rep_tie_win"] += 1
                    best, at = counts[e], e
                    f["rep_update"] += 1
        if best == 0:
            break
        f["shown"] += 1
        f["printed"] += len(words[firsts[at]])
        f["digits"] += len(str(best))
        counts[at] = 0
    return f


def fit(samples):
    """Least squares: steps ~ c . features, over (features, steps) pairs; returns the coefficients by name and the
    largest relative error on the samples."""
    import numpy as np
    names = sorted(samples[0][0])
    X = np.array([[1.0] + [s[0][k] for k in names] for s in samples])
    y = np.array([s[1] for s in samples], dtype=float)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    err = float(np.max(np.abs(pred - y) / y))
    return {"names": ["const"] + names, "coef": coef.tolist(), "max_rel_err": err}


def predict(model, f):
    return model["coef"][0] + sum(c * f[k] for k, c in zip(model["names"][1:], model["coef"][1:]))


FEATURES_C = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
static unsigned char *pool; static int *ws, *wl, *idx, *tmp; static int n;
static ll F[24];
enum { BYTES, LETTERS, CAPITALS, WORDS, PASSES, MERGES, SORT_CMP, SORT_RIGHT, TAIL, COPYBACK, KSTEPS, RETDIFF,
       RETLEN, SHORTN, SCANCMP, RUNS, REPITER, REPGT, REPEQ, REPTIE, REPUPD, PRINTED, DIGITS, SHOWN };
static const char *NAMES[24] = {"bytes","letters","capitals","words","passes","merges","sort_cmp","sort_right",
  "tail_copies","copy_back","k_steps","ret_diff","ret_len","short_n","scan_cmp","runs","rep_iter","rep_gt",
  "rep_eq","rep_tie_win","rep_update","printed","digits","shown"};
static int cmpw(int a, int b) {
  int la = wl[a], lb = wl[b], m = la < lb ? la : lb;
  if (lb < la) F[SHORTN]++;
  const unsigned char *x = pool + ws[a], *y = pool + ws[b];
  for (int k = 0; k < m; k++) { F[KSTEPS]++; if (x[k] != y[k]) { F[RETDIFF]++; return (int)x[k] - (int)y[k]; } }
  F[RETLEN]++; return la - lb;
}
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "rb"); fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
  unsigned char *t = malloc(sz); if (fread(t, 1, sz, f) != (size_t)sz) return 1; fclose(f);
  pool = malloc(sz + 1); ws = malloc(sizeof(int) * (sz / 2 + 2)); wl = malloc(sizeof(int) * (sz / 2 + 2));
  F[BYTES] = sz; long used = 0; int cur = 0; n = 0;
  for (long i = 0; i <= sz; i++) {
    int c = i < sz ? t[i] : -1;
    if (c >= 'A' && c <= 'Z') { F[CAPITALS]++; c += 32; }
    if (c >= 'a' && c <= 'z') { pool[used + cur] = c; cur++; }
    else if (cur > 0) { ws[n] = used; wl[n] = cur; n++; used += cur; cur = 0; }
  }
  F[WORDS] = n; F[LETTERS] = used;
  idx = malloc(sizeof(int) * (n + 1)); tmp = malloc(sizeof(int) * (n + 1));
  for (int i = 0; i < n; i++) idx[i] = i;
  for (long width = 1; width < n; width *= 2) {
    F[PASSES]++;
    for (long lo = 0; lo < n; ) {
      F[MERGES]++;
      long mid = lo + width < n ? lo + width : n, hi = lo + 2 * width < n ? lo + 2 * width : n;
      long i = lo, j = mid, o = lo;
      while (i < mid && j < hi) {
        F[SORT_CMP]++;
        if (cmpw(idx[j], idx[i]) < 0) { F[SORT_RIGHT]++; tmp[o++] = idx[j++]; } else tmp[o++] = idx[i++];
      }
      F[TAIL] += (mid - i) + (hi - j);
      while (i < mid) tmp[o++] = idx[i++];
      while (j < hi) tmp[o++] = idx[j++];
      lo = hi;
    }
    F[COPYBACK] += n;
    int *s = idx; idx = tmp; tmp = s;
  }
  int *cnt = malloc(sizeof(int) * (n + 1)), *first = malloc(sizeof(int) * (n + 1)); int ne = 0;
  for (int i = 0; i < n; ) {
    int j = i + 1;
    while (j < n) { F[SCANCMP]++; if (cmpw(idx[i], idx[j]) != 0) break; j++; }
    cnt[ne] = j - i; first[ne] = idx[i]; ne++; i = j;
  }
  F[RUNS] = ne;
  for (int shown = 0; shown < 20; shown++) {
    int best = 0, at = -1;
    for (int e = 0; e < ne; e++) {
      F[REPITER]++;
      if (cnt[e] > best) { F[REPGT]++; best = cnt[e]; at = e; F[REPUPD]++; }
      else if (cnt[e] == best) { F[REPEQ]++; if (best > 0 && first[e] < first[at]) { F[REPTIE]++; best = cnt[e]; at = e; F[REPUPD]++; } }
    }
    if (best == 0) break;
    F[SHOWN]++; F[PRINTED] += wl[first[at]];
    char buf[24]; F[DIGITS] += sprintf(buf, "%d", best);
    fwrite(pool + ws[first[at]], 1, wl[first[at]], stderr); fprintf(stderr, " %d\n", best);
    cnt[at] = 0;
  }
  for (int k = 0; k < 24; k++) printf("%s %lld\n", NAMES[k], F[k]);
  return 0;
}
"""


def features_native(text: bytes) -> tuple[dict, bytes]:
    """The same counts as :func:`features`, by a C program (fast enough for the thirty novels); also returns what the
    Job prints, as a check."""
    import subprocess
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as d:
        Path(d, "f.c").write_text(FEATURES_C)
        subprocess.run(["gcc", "-O2", "-o", "f", "f.c"], cwd=d, check=True)
        Path(d, "t").write_bytes(text)
        r = subprocess.run(["./f", "t"], cwd=d, capture_output=True, check=True)
    f = {}
    for line in r.stdout.decode().splitlines():
        k, v = line.split()
        f[k] = int(v)
    return f, r.stderr
