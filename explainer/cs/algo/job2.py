"""The Job v2 (Part 17): count the words in a hash table, in the Pebble language.

The Pebble language has no bitwise operators, so the hash is polynomial, computed as the letters arrive:
h = (33 h + c) mod 16,777,213 (a prime, so 33 h + c stays below 2^31).  The table holds entry numbers in ``cap``
slots, a power of two, probed linearly from h mod cap; it doubles when it would pass half full, re-inserting every
entry by its stored hash (Part 16's amortized analysis, in use).  Entries are created in order of first occurrence,
so the report (twenty times, the largest count, ties to the lowest entry) prints exactly the Job v0's output.

    c = compile_job()                 # Part 13's compiler, -O2
    m = run(c, text)                  # the emulator; m.steps
    features(text)                    # the counts that determine m.steps exactly
    features_native(text)             # the same counts, by a C program that follows v2 step for step
"""
from __future__ import annotations

from explainer.cs.algo.job import fit, predict  # noqa: F401  (the same least-squares model as the Job v1)

P = 16777213
CAP0 = 64

JOB_HASH = r"""
// The Job v2: a hash table of the distinct words.
var pool: [131072]char;
var used: int = 0;
var slot: [32768]int;
var cap: int = 64;
var estart: [16384]int;
var elen: [16384]int;
var ehash: [16384]int;
var ecount: [16384]int;
var ne: int = 0;

// put entry e into the table, by its stored hash (used when the table grows)
fn place(e: int) {
    var i: int = ehash[e] % cap;
    while slot[i] != 0 {
        i = i + 1;
        if i == cap { i = 0; }
    }
    slot[i] = e + 1;
}

fn grow() {
    cap = 2 * cap;
    var i: int = 0;
    while i < cap { slot[i] = 0; i = i + 1; }
    var e: int = 0;
    while e < ne { place(e); e = e + 1; }
}

// the word of n letters at pool[used..used+n), with hash h: count it
fn count(h: int, n: int) {
    var i: int = h % cap;
    while slot[i] != 0 {
        var e: int = slot[i] - 1;
        if ehash[e] == h && elen[e] == n {
            var p: int = estart[e];
            var k: int = 0;
            while k < n && pool[p + k] == pool[used + k] { k = k + 1; }
            if k == n { ecount[e] = ecount[e] + 1; return; }
        }
        i = i + 1;
        if i == cap { i = 0; }
    }
    // a new word: keep its letters, make an entry
    estart[ne] = used; elen[ne] = n; ehash[ne] = h; ecount[ne] = 1;
    slot[i] = ne + 1;
    ne = ne + 1;
    used = used + n;
    if 2 * ne > cap { grow(); }
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
    var h: int = 0;
    var c: int = getc();
    while c != -1 {
        if c >= 'A' && c <= 'Z' { c = c + 32; }
        if c >= 'a' && c <= 'z' {
            pool[used + n] = c;
            h = (33 * h + c) % 16777213;
            n = n + 1;
        } else if n > 0 {
            count(h, n);
            n = 0; h = 0;
        }
        c = getc();
    }
    if n > 0 { count(h, n); }
    // the report: twenty times, the largest count; entries are in order of first occurrence
    var shown: int = 0;
    while shown < 20 {
        var best: int = 0;
        var at: int = 0;
        var e: int = 0;
        while e < ne {
            if ecount[e] > best { best = ecount[e]; at = e; }
            e = e + 1;
        }
        if best == 0 { return 0; }
        var k: int = 0;
        while k < elen[at] { putc(pool[estart[at] + k]); k = k + 1; }
        putc(' ');
        printnum(best);
        putc('\n');
        ecount[at] = 0;
        shown = shown + 1;
    }
    return 0;
}
"""

NAMES = ["bytes", "capitals", "letters", "words", "probes", "hash_eq", "len_eq", "k_steps", "found", "new",
         "grows", "cleared", "placed", "place_probes", "wraps", "place_wraps", "rep_iter", "rep_gt", "printed",
         "digits", "shown", "last_word", "above_z", "between",
         "count_loops", "place_loops", "rep_stop"]


def compile_job(level: int = 2):
    from explainer.cs.lang.compiler import driver as D
    return D.compile_program(JOB_HASH, level)


def run(c, text: bytes, **kw):
    from explainer.cs.lang.compiler import driver as D
    return D.run(c, text, **kw)


def features(text: bytes) -> dict:
    """The events the Job v2's instruction count depends on, by following its control flow exactly."""
    f = dict.fromkeys(NAMES, 0)
    f["bytes"] = len(text)
    pool = bytearray()
    estart, elen, ehash, ecount = [], [], [], []
    cap = CAP0
    slot = [0] * cap

    def place(e):
        i = ehash[e] % cap
        if slot[i] != 0:
            f["place_loops"] += 1  # the loop's preheader (hoisted loads) runs once when the loop is entered
        while slot[i] != 0:
            f["place_probes"] += 1
            i += 1
            if i == cap:
                f["place_wraps"] += 1
                i = 0
        slot[i] = e + 1
        f["placed"] += 1

    def count(h, word):
        nonlocal cap, slot
        n = len(word)
        f["words"] += 1
        i = h % cap
        if slot[i] != 0:
            f["count_loops"] += 1
        while slot[i] != 0:
            f["probes"] += 1
            e = slot[i] - 1
            if ehash[e] == h:
                f["hash_eq"] += 1
                if elen[e] == n:
                    f["len_eq"] += 1
                    p, k = estart[e], 0
                    while k < n and pool[p + k] == word[k]:
                        k += 1
                    f["k_steps"] += k
                    if k == n:
                        f["found"] += 1
                        ecount[e] += 1
                        return
            i += 1
            if i == cap:
                f["wraps"] += 1
                i = 0
        f["new"] += 1
        estart.append(len(pool))
        elen.append(n)
        ehash.append(h)
        ecount.append(1)
        pool.extend(word)
        slot[i] = len(estart)
        if 2 * len(estart) > cap:
            f["grows"] += 1
            cap *= 2
            slot = [0] * cap
            f["cleared"] += cap
            for e in range(len(estart)):
                place(e)

    word, h = bytearray(), 0
    for b in text:
        if b > 122:
            f["above_z"] += 1
        elif 90 < b < 97:
            f["between"] += 1
        if 65 <= b <= 90:
            f["capitals"] += 1
            b += 32
        if 97 <= b <= 122:
            word.append(b)
            h = (33 * h + b) % P
            f["letters"] += 1
        elif word:
            count(h, bytes(word))
            word, h = bytearray(), 0
    if word:
        f["last_word"] = 1
        count(h, bytes(word))
    counts = list(ecount)
    for _ in range(20):
        best, at = 0, 0
        for e in range(len(counts)):
            f["rep_iter"] += 1
            if counts[e] > best:
                f["rep_gt"] += 1
                best, at = counts[e], e
        if best == 0:
            f["rep_stop"] = 1  # fewer than twenty distinct words: a last, empty pass
            break
        f["shown"] += 1
        f["printed"] += elen[at]
        f["digits"] += len(str(best))
        counts[at] = 0
    return f


FEATURES_C = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
#define P 16777213
#define NF 27
enum { BYTES, CAPITALS, LETTERS, WORDS, PROBES, HASHEQ, LENEQ, KSTEPS, FOUND, NEW, GROWS, CLEARED, PLACED,
       PLACEPROBES, WRAPS, PLACEWRAPS, REPITER, REPGT, PRINTED, DIGITS, SHOWN, LASTWORD, ABOVEZ, BETWEEN,
       COUNTLOOPS, PLACELOOPS, REPSTOP };
static const char *NAMES[NF] = {"bytes","capitals","letters","words","probes","hash_eq","len_eq","k_steps","found",
  "new","grows","cleared","placed","place_probes","wraps","place_wraps","rep_iter","rep_gt","printed","digits",
  "shown","last_word","above_z","between","count_loops","place_loops","rep_stop"};
static ll F[NF];
static unsigned char *pool; static long used;
static int *slot, *estart, *elen, *ehash, *ecount; static long cap = 64, ne = 0, emax;
static void place(long e) {
  long i = ehash[e] % cap;
  if (slot[i] != 0) F[PLACELOOPS]++;
  while (slot[i] != 0) { F[PLACEPROBES]++; i++; if (i == cap) { F[PLACEWRAPS]++; i = 0; } }
  slot[i] = e + 1; F[PLACED]++;
}
static void count(int h, int n, const unsigned char *w) {
  F[WORDS]++;
  long i = h % cap;
  if (slot[i] != 0) F[COUNTLOOPS]++;
  while (slot[i] != 0) {
    F[PROBES]++;
    int e = slot[i] - 1;
    if (ehash[e] == h) {
      F[HASHEQ]++;
      if (elen[e] == n) {
        F[LENEQ]++;
        int k = 0; while (k < n && pool[estart[e] + k] == w[k]) k++;
        F[KSTEPS] += k;
        if (k == n) { F[FOUND]++; ecount[e]++; return; }
      }
    }
    i++; if (i == cap) { F[WRAPS]++; i = 0; }
  }
  F[NEW]++;
  estart[ne] = used; elen[ne] = n; ehash[ne] = h; ecount[ne] = 1;
  memcpy(pool + used, w, n); used += n;
  slot[i] = ne + 1; ne++;
  if (2 * ne > cap) {
    F[GROWS]++; cap *= 2; free(slot); slot = calloc(cap, sizeof(int)); F[CLEARED] += cap;
    for (long e = 0; e < ne; e++) place(e);
  }
}
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "rb"); fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
  unsigned char *t = malloc(sz); if (fread(t, 1, sz, f) != (size_t)sz) return 1; fclose(f);
  emax = sz / 2 + 2;
  pool = malloc(sz + 1); estart = malloc(sizeof(int) * emax); elen = malloc(sizeof(int) * emax);
  ehash = malloc(sizeof(int) * emax); ecount = malloc(sizeof(int) * emax); slot = calloc(cap, sizeof(int));
  F[BYTES] = sz;
  unsigned char word[4096]; int n = 0; int h = 0;
  for (long i = 0; i < sz; i++) {
    int c = t[i];
    if (c > 'z') F[ABOVEZ]++; else if (c > 'Z' && c < 'a') F[BETWEEN]++;
    if (c >= 'A' && c <= 'Z') { F[CAPITALS]++; c += 32; }
    if (c >= 'a' && c <= 'z') { word[n++] = c; h = (int)((33LL * h + c) % P); F[LETTERS]++; }
    else if (n > 0) { count(h, n, word); n = 0; h = 0; }
  }
  if (n > 0) { F[LASTWORD] = 1; count(h, n, word); }
  for (int shown = 0; shown < 20; shown++) {
    int best = 0; long at = 0;
    for (long e = 0; e < ne; e++) { F[REPITER]++; if (ecount[e] > best) { F[REPGT]++; best = ecount[e]; at = e; } }
    if (best == 0) { F[REPSTOP] = 1; break; }
    F[SHOWN]++; F[PRINTED] += elen[at];
    char buf[24]; F[DIGITS] += sprintf(buf, "%d", best);
    fwrite(pool + estart[at], 1, elen[at], stderr); fprintf(stderr, " %d\n", best);
    ecount[at] = 0;
  }
  for (int k = 0; k < NF; k++) printf("%s %lld\n", NAMES[k], F[k]);
  return 0;
}
"""


def features_native(text: bytes) -> tuple[dict, bytes]:
    """The same counts as :func:`features`, by a C program; also returns what the Job prints, as a check."""
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
