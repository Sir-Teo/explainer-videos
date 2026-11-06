"""Parnas's KWIC index (1972), built both ways (Part 40).

Decomposition 1 follows the flowchart: Input, Circular Shift, Alphabetizer, Output and a Master control, all reading
and writing shared data (the words of every line, where each line starts, the list of shifts).  Decomposition 2 hides
one design decision in each module: Line Storage hides how lines are stored, the Circular Shifter how shifts are
represented, the Alphabetizer when and how sorting happens.

Each version is real source code.  Four changes Parnas discussed are applied to each decomposition; every variant
is run on the same input and must produce the same index, and the modules whose source changed are counted."""

from __future__ import annotations

D1 = {
    "Input": '''
def input_(text):
    G["WORDS"] = []
    G["START"] = []
    for line in text.split("\\n"):
        G["START"].append(len(G["WORDS"]))
        G["WORDS"].extend(line.split())
''',
    "Circular Shift": '''
def shift():
    W, S = G["WORDS"], G["START"]
    ends = S[1:] + [len(W)]
    G["SHIFTS"] = [(l, k) for l in range(len(S)) for k in range(ends[l] - S[l])]
''',
    "Alphabetizer": '''
def alphabetize():
    W, S = G["WORDS"], G["START"]
    ends = S[1:] + [len(W)]
    def key(sh):
        l, k = sh
        ws = W[S[l]:ends[l]]
        return [w.lower() for w in ws[k:] + ws[:k]]
    G["SORTED"] = sorted(G["SHIFTS"], key=key)
''',
    "Output": '''
def output():
    W, S = G["WORDS"], G["START"]
    ends = S[1:] + [len(W)]
    out = []
    for l, k in G["SORTED"]:
        ws = W[S[l]:ends[l]]
        out.append(" ".join(ws[k:] + ws[:k]))
    return out
''',
    "Master": '''
def master(text):
    input_(text)
    shift()
    alphabetize()
    return output()
''',
}

D2 = {
    "Line Storage": '''
class LineStorage:
    def __init__(self):
        self._words, self._start = [], []
    def new_line(self):
        self._start.append(len(self._words))
    def add_word(self, w):
        self._words.append(w)
    def lines(self):
        return len(self._start)
    def words(self, l):
        end = self._start[l + 1] if l + 1 < len(self._start) else len(self._words)
        return end - self._start[l]
    def word(self, l, i):
        return self._words[self._start[l] + i]
''',
    "Input": '''
def input_(text, store):
    for line in text.split("\\n"):
        store.new_line()
        for w in line.split():
            store.add_word(w)
''',
    "Circular Shifter": '''
class Shifter:
    def __init__(self, store):
        self.store = store
        self._shifts = [(l, k) for l in range(store.lines()) for k in range(store.words(l))]
    def count(self):
        return len(self._shifts)
    def words(self, i):
        l, k = self._shifts[i]
        n = self.store.words(l)
        return [self.store.word(l, (k + j) % n) for j in range(n)]
''',
    "Alphabetizer": '''
class Alphabetizer:
    def __init__(self, shifter):
        self.shifter = shifter
        self._order = sorted(range(shifter.count()), key=lambda i: [w.lower() for w in shifter.words(i)])
    def count(self):
        return len(self._order)
    def ith(self, i):
        return self._order[i]
''',
    "Output": '''
def output(alpha, shifter):
    return [" ".join(shifter.words(alpha.ith(i))) for i in range(alpha.count())]
''',
    "Master": '''
def master(text):
    store = LineStorage()
    input_(text, store)
    shifter = Shifter(store)
    alpha = Alphabetizer(shifter)
    return output(alpha, shifter)
''',
}


def _change_packed(d1: bool):
    """Store each word as a number in a shared vocabulary (Parnas: 'packing characters four to a word')."""
    if d1:
        return {
            "Input": '''
def input_(text):
    G["WORDS"] = []
    G["START"] = []
    G["VOCAB"] = []
    ids = {}
    for line in text.split("\\n"):
        G["START"].append(len(G["WORDS"]))
        for w in line.split():
            if w not in ids:
                ids[w] = len(G["VOCAB"])
                G["VOCAB"].append(w)
            G["WORDS"].append(ids[w])
''',
            "Alphabetizer": '''
def alphabetize():
    W, S, V = G["WORDS"], G["START"], G["VOCAB"]
    ends = S[1:] + [len(W)]
    def key(sh):
        l, k = sh
        ws = W[S[l]:ends[l]]
        return [V[w].lower() for w in ws[k:] + ws[:k]]
    G["SORTED"] = sorted(G["SHIFTS"], key=key)
''',
            "Output": '''
def output():
    W, S, V = G["WORDS"], G["START"], G["VOCAB"]
    ends = S[1:] + [len(W)]
    out = []
    for l, k in G["SORTED"]:
        ws = W[S[l]:ends[l]]
        out.append(" ".join(V[w] for w in ws[k:] + ws[:k]))
    return out
''',
        }
    return {"Line Storage": '''
class LineStorage:
    def __init__(self):
        self._words, self._start, self._vocab, self._ids = [], [], [], {}
    def new_line(self):
        self._start.append(len(self._words))
    def add_word(self, w):
        if w not in self._ids:
            self._ids[w] = len(self._vocab)
            self._vocab.append(w)
        self._words.append(self._ids[w])
    def lines(self):
        return len(self._start)
    def words(self, l):
        end = self._start[l + 1] if l + 1 < len(self._start) else len(self._words)
        return end - self._start[l]
    def word(self, l, i):
        return self._vocab[self._words[self._start[l] + i]]
'''}


def _change_input(d1: bool):
    """Lines arrive separated by semicolons instead of newlines."""
    if d1:
        return {"Input": D1["Input"].replace('split("\\n")', 'split(";")')}
    return {"Input": D2["Input"].replace('split("\\n")', 'split(";")')}


def _change_shifts(d1: bool):
    """Store every shifted line in full instead of (line, offset) pairs."""
    if d1:
        return {
            "Circular Shift": '''
def shift():
    W, S = G["WORDS"], G["START"]
    ends = S[1:] + [len(W)]
    G["SHIFTS"] = []
    for l in range(len(S)):
        ws = W[S[l]:ends[l]]
        G["SHIFTS"] += [ws[k:] + ws[:k] for k in range(len(ws))]
''',
            "Alphabetizer": '''
def alphabetize():
    G["SORTED"] = sorted(G["SHIFTS"], key=lambda ws: [w.lower() for w in ws])
''',
            "Output": '''
def output():
    return [" ".join(ws) for ws in G["SORTED"]]
''',
        }
    return {"Circular Shifter": '''
class Shifter:
    def __init__(self, store):
        self._lines = []
        for l in range(store.lines()):
            ws = [store.word(l, i) for i in range(store.words(l))]
            self._lines += [ws[k:] + ws[:k] for k in range(len(ws))]
    def count(self):
        return len(self._lines)
    def words(self, i):
        return self._lines[i]
'''}


def _change_lazy(d1: bool):
    """Alphabetize on demand: find each next entry when it is asked for, instead of sorting everything first."""
    if d1:
        return {
            "Alphabetizer": '''
def alphabetize():
    W, S = G["WORDS"], G["START"]
    ends = S[1:] + [len(W)]
    def key(sh):
        l, k = sh
        ws = W[S[l]:ends[l]]
        return [w.lower() for w in ws[k:] + ws[:k]]
    import heapq
    G["HEAP"] = [(key(sh), sh) for sh in G["SHIFTS"]]
    heapq.heapify(G["HEAP"])
''',
            "Output": '''
def output():
    import heapq
    W, S = G["WORDS"], G["START"]
    ends = S[1:] + [len(W)]
    out = []
    while G["HEAP"]:
        _, (l, k) = heapq.heappop(G["HEAP"])
        ws = W[S[l]:ends[l]]
        out.append(" ".join(ws[k:] + ws[:k]))
    return out
''',
        }
    return {"Alphabetizer": '''
class Alphabetizer:
    def __init__(self, shifter):
        import heapq
        self.shifter = shifter
        self._heap = [([w.lower() for w in shifter.words(i)], i) for i in range(shifter.count())]
        heapq.heapify(self._heap)
        self._done = []
    def count(self):
        return self.shifter.count()
    def ith(self, i):
        import heapq
        while len(self._done) <= i:
            self._done.append(heapq.heappop(self._heap)[1])
        return self._done[i]
'''}


CHANGES = {
    "store words packed": _change_packed,
    "change the input format": _change_input,
    "store shifts in full": _change_shifts,
    "alphabetize on demand": _change_lazy,
}

SAMPLE = ("Designing Programs for Ease of Extension and Contraction\n"
          "On the Criteria To Be Used in Decomposing Systems into Modules\n"
          "The Structure of the THE Multiprogramming System\n"
          "Go To Statement Considered Harmful")


def run(mods: dict, text: str):
    ns = {"G": {}}
    for src in mods.values():
        exec(src, ns)
    return ns["master"](text)


def experiment(text: str = SAMPLE):
    """For each change and each decomposition: modules changed (by source comparison), lines changed, and whether
    the index is unchanged."""
    import difflib
    base1, base2 = run(D1, text), run(D2, text)
    assert base1 == base2
    rows = []
    for name, fn in CHANGES.items():
        row = {"change": name}
        for tag, base, d1 in (("d1", D1, True), ("d2", D2, False)):
            new = dict(base) | fn(d1)
            t = text.replace("\n", ";") if name == "change the input format" else text
            ok = run(new, t) == base1
            changed = [m for m in base if new[m] != base[m]]
            nl = sum(sum(1 for ln in difflib.unified_diff(base[m].splitlines(), new[m].splitlines(), lineterm="")
                         if ln[:1] in "+-" and ln[:3] not in ("+++", "---")) for m in changed)
            row[tag] = {"modules": changed, "n": len(changed), "of": len(base), "lines": nl, "same_output": ok}
        rows.append(row)
    return {"rows": rows, "index": base1, "lines_in": len(text.splitlines())}
