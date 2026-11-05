"""The Job v3 (Part 20): the top twenty words in a few kilobytes, in the Pebble language.

The Job v2 kept every distinct word.  The v3 keeps none of them: a Count-Min sketch of D = 4 rows of W = 1021
counters estimates every word's count, and only the K = 32 words whose estimates are largest are stored, as
candidates in a min-heap ordered by estimate.  The rows come from one letter hash by double hashing (Kirsch and
Mitzenmacher, 2006): row r looks at (h + r g) mod W, with g = 1 + (h / W) mod (W - 1), so one division per word
gives four row indices (the Pebble language has no bitwise operators, so tabulation hashing is out).  The update is
conservative (Estan and Varghese, 2002): only the counters at the minimum are raised.  A small open-addressed table
of 128 slots finds a word among the candidates; evicting a candidate deletes it by backward shifting (Knuth's
Algorithm R).  Words longer than 32 letters are counted but never become candidates.

    c = compile_job()                 # Part 13's compiler, -O2
    m = run(c, text)                  # the emulator; m.steps, m.output
    reference(text)                   # the same algorithm in Python: the same output, byte for byte
    footprint(c)                      # the data the program touches: address ranges and bytes
"""
from __future__ import annotations

P = 16777213
D, W, K, M, L = 4, 1021, 32, 128, 32

JOB_SKETCH = r"""
// The Job v3: a Count-Min sketch of every word, and a heap of the 32 words with the largest estimates.
var cm: [4084]int;         // 4 rows of 1021 counters
var word: [72]char;        // the current word's letters
var chash: [32]int;        // the candidates: hash, length, estimate, place in the heap, letters
var clen: [32]int;
var cest: [32]int;
var cpos: [32]int;
var cword: [1024]char;
var heap: [32]int;         // candidate numbers, smallest estimate first
var nc: int = 0;
var slot: [128]int;        // candidate e + 1 at (its hash mod 128), linear probing

fn swap(i: int, j: int) {
    var a: int = heap[i];
    var b: int = heap[j];
    heap[i] = b; heap[j] = a;
    cpos[b] = i; cpos[a] = j;
}

fn up(i: int) {
    while i > 0 {
        var p: int = (i - 1) / 2;
        if cest[heap[p]] <= cest[heap[i]] { return; }
        swap(i, p);
        i = p;
    }
}

fn down(i: int) {
    while 2 * i + 1 < nc {
        var m: int = 2 * i + 1;
        if m + 1 < nc && cest[heap[m + 1]] < cest[heap[m]] { m = m + 1; }
        if cest[heap[i]] <= cest[heap[m]] { return; }
        swap(i, m);
        i = m;
    }
}

// the candidate holding the current word (n letters, hash h), or -1
fn find(h: int, n: int) -> int {
    var i: int = h % 128;
    while slot[i] != 0 {
        var e: int = slot[i] - 1;
        if chash[e] == h && clen[e] == n {
            var k: int = 0;
            while k < n && cword[32 * e + k] == word[k] { k = k + 1; }
            if k == n { return e; }
        }
        i = i + 1;
        if i == 128 { i = 0; }
    }
    return -1;
}

fn putslot(e: int) {
    var i: int = chash[e] % 128;
    while slot[i] != 0 {
        i = i + 1;
        if i == 128 { i = 0; }
    }
    slot[i] = e + 1;
}

// delete candidate e from the slots, shifting later entries back over the gap (Knuth's Algorithm R)
fn unslot(e: int) {
    var i: int = chash[e] % 128;
    while slot[i] != e + 1 {
        i = i + 1;
        if i == 128 { i = 0; }
    }
    var j: int = i;
    while 1 == 1 {
        j = j + 1;
        if j == 128 { j = 0; }
        if slot[j] == 0 { break; }
        var k: int = chash[slot[j] - 1] % 128;
        // move slot[j] into the gap at i unless its home k lies cyclically in (i, j]
        var stay: int = 0;
        if i <= j {
            if i < k && k <= j { stay = 1; }
        } else {
            if i < k || k <= j { stay = 1; }
        }
        if stay == 0 { slot[i] = slot[j]; i = j; }
    }
    slot[i] = 0;
}

fn keep(e: int, h: int, n: int, est: int) {
    chash[e] = h; clen[e] = n; cest[e] = est;
    var k: int = 0;
    while k < n { cword[32 * e + k] = word[k]; k = k + 1; }
    putslot(e);
}

fn seen(h: int, n: int) {
    var g: int = 1 + (h / 1021) % 1020;
    var i0: int = h % 1021;
    // the next row's index is g further on, mod 1021: one subtraction instead of a division
    var x: int = i0 + g;
    if x >= 1021 { x = x - 1021; }
    var y: int = x + g;
    if y >= 1021 { y = y - 1021; }
    var z: int = y + g;
    if z >= 1021 { z = z - 1021; }
    var a: int = i0;
    var b: int = 1021 + x;
    var c: int = 2042 + y;
    var d: int = 3063 + z;
    var m: int = cm[a];
    if cm[b] < m { m = cm[b]; }
    if cm[c] < m { m = cm[c]; }
    if cm[d] < m { m = cm[d]; }
    // conservative update: raise only the counters at the minimum
    if cm[a] == m { cm[a] = m + 1; }
    if cm[b] == m { cm[b] = m + 1; }
    if cm[c] == m { cm[c] = m + 1; }
    if cm[d] == m { cm[d] = m + 1; }
    m = m + 1;
    if nc == 32 && m <= cest[heap[0]] { return; }   // cannot beat the smallest candidate
    if n > 32 { return; }
    var e: int = find(h, n);
    if e >= 0 { cest[e] = m; down(cpos[e]); return; }
    if nc < 32 {
        e = nc; nc = nc + 1;
        heap[e] = e; cpos[e] = e;
        keep(e, h, n, m);
        up(e);
        return;
    }
    e = heap[0];                                   // replace the smallest candidate
    unslot(e);
    keep(e, h, n, m);
    down(0);
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
            if n < 72 { word[n] = c; }
            h = (33 * h + c) % 16777213;
            n = n + 1;
        } else if n > 0 {
            seen(h, n);
            n = 0; h = 0;
        }
        c = getc();
    }
    if n > 0 { seen(h, n); }
    // the report: twenty times, the largest estimate (ties to the lowest candidate number)
    var shown: int = 0;
    while shown < 20 {
        var best: int = 0;
        var at: int = 0;
        var e: int = 0;
        while e < nc {
            if cest[e] > best { best = cest[e]; at = e; }
            e = e + 1;
        }
        if best == 0 { return 0; }
        var k: int = 0;
        while k < clen[at] { putc(cword[32 * at + k]); k = k + 1; }
        putc(' ');
        printnum(best);
        putc('\n');
        cest[at] = 0;
        shown = shown + 1;
    }
    return 0;
}
"""


def compile_job(level: int = 2):
    from explainer.cs.lang.compiler import driver as Dr
    return Dr.compile_program(JOB_SKETCH, level)


def run(c, text: bytes, **kw):
    from explainer.cs.lang.compiler import driver as Dr
    return Dr.run(c, text, **kw)


def rows(h: int, w: int = W, d: int = D) -> list[int]:
    g = 1 + (h // w) % (w - 1)
    return [(h + r * g) % w for r in range(d)]


def reference(text: bytes, d: int = D, w: int = W, k: int = K, seed: int = 0) -> tuple[bytes, dict]:
    """The same algorithm, in Python: (the report, {word: estimate} for the final candidates).  ``seed`` > 0 changes
    the letter hash's multiplier (33 + 2 seed) and so the whole hash family; the Pebble program uses seed 0."""
    mult = 33 + 2 * seed
    cm = [[0] * w for _ in range(d)]
    cand: dict[bytes, int] = {}         # word -> estimate, insertion-ordered like the candidate numbers
    order: list[bytes] = []             # candidate number -> word

    # an exact mirror of the program's heap, so ties are broken the same way
    heap: list[int] = []
    pos: list[int] = []

    def cest(e):
        return cand[order[e]]

    def swap(i, j):
        a, b = heap[i], heap[j]
        heap[i], heap[j] = b, a
        pos[b], pos[a] = i, j

    def up(i):
        while i > 0:
            p = (i - 1) // 2
            if cest(heap[p]) <= cest(heap[i]):
                return
            swap(i, p)
            i = p

    def down(i):
        while 2 * i + 1 < len(heap):
            m = 2 * i + 1
            if m + 1 < len(heap) and cest(heap[m + 1]) < cest(heap[m]):
                m += 1
            if cest(heap[i]) <= cest(heap[m]):
                return
            swap(i, m)
            i = m

    def seen(word: bytes, h: int):
        idx = rows(h, w, d)
        m = min(cm[r][idx[r]] for r in range(d))
        for r in range(d):
            if cm[r][idx[r]] == m:
                cm[r][idx[r]] = m + 1
        m += 1
        if len(heap) == k and m <= cest(heap[0]):
            return
        if len(word) > 32:
            return
        if word in cand:
            e = order.index(word)
            cand[word] = m
            down(pos[e])
            return
        if len(heap) < k:
            e = len(heap)
            order.append(word)
            cand[word] = m
            heap.append(e)
            pos.append(e)
            up(e)
            return
        e = heap[0]
        del cand[order[e]]
        order[e] = word
        cand[word] = m
        down(0)

    word, h = bytearray(), 0
    for b in text:
        if 65 <= b <= 90:
            b += 32
        if 97 <= b <= 122:
            word.append(b)
            h = (mult * h + b) % P
        elif word:
            seen(bytes(word), h)
            word, h = bytearray(), 0
    if word:
        seen(bytes(word), h)
    est = {order[e]: cand[order[e]] for e in range(len(order))}
    left = [cand[order[e]] for e in range(len(order))]
    out = bytearray()
    for _ in range(20):
        best, at = 0, 0
        for e in range(len(order)):
            if left[e] > best:
                best, at = left[e], e
        if best == 0:
            break
        out += order[at] + b" " + str(best).encode() + b"\n"
        left[at] = 0
    return bytes(out), est


def footprint(c) -> dict:
    """The program's static data: each global's address and size, from the assembler's labels and the IR."""
    labels = c.program.labels
    g = {name: (labels[name], size) for name, (size, _a, _i) in c.module.globals.items() if name in labels}
    lo = min(a for a, _ in g.values())
    hi = max(a + s for a, s in g.values())
    return {"globals": g, "lo": lo, "hi": hi, "bytes": hi - lo}
