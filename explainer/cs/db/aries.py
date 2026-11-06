"""ARIES recovery (Mohan et al., 1992), on a toy database of integer pages (Part 35).

Updates are logged before they reach the disk (write-ahead logging); the buffer manager may write a dirty page at
any time, even one an uncommitted transaction changed (**steal**), and need not write a committed transaction's pages
at commit (**no-force**): commit only forces the log.  A crash loses the buffer pool and the log's unforced tail.
Recovery then makes three passes over the log:

* **analysis**, forward from the last checkpoint: which transactions were active (the losers), and which pages may
  be dirty, each with the LSN of the first record that dirtied it (recLSN);
* **redo**, forward from the smallest recLSN: repeat history, reapplying every logged update (and compensation)
  whose page is older than the record (pageLSN < LSN), losers included;
* **undo**, backward: roll back the losers, newest record first, logging a compensation record (CLR) for each undone
  update, whose ``undo_next`` skips what is already undone, so a crash during recovery never undoes anything twice.

``workload`` makes random transactions; ``crash_and_recover`` runs one to a random crash point and recovers;
``check`` compares the recovered pages with the effect of the committed transactions alone.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class Rec:
    lsn: int
    kind: str                 # update, commit, abort, clr, end, ckpt
    txn: int = 0
    prev: int = 0             # the transaction's previous record
    page: int = -1
    before: int = 0
    after: int = 0
    undo_next: int = 0        # CLR: the next record of this transaction still to undo
    att: dict = field(default_factory=dict)   # checkpoint: active transactions {txn: last lsn}
    dpt: dict = field(default_factory=dict)   # checkpoint: dirty pages {page: recLSN}


class System:
    def __init__(self, npages: int = 8, seed: int = 0, flush_p: float = 0.3):
        self.rng = random.Random(seed)
        self.disk = {p: (0, 0) for p in range(npages)}      # page -> (value, pageLSN), on disk
        self.buf: dict = {}                                 # page -> [value, pageLSN, recLSN]
        self.log: list[Rec] = []
        self.flushed = 0                                    # log records on disk: log[:flushed]
        self.last: dict = {}                                # txn -> last LSN
        self.flush_p = flush_p
        self.page_writes = 0

    def _append(self, r: Rec) -> int:
        r.lsn = len(self.log) + 1
        self.log.append(r)
        return r.lsn

    def _page(self, p):
        if p not in self.buf:
            v, plsn = self.disk[p]
            self.buf[p] = [v, plsn, None]
        return self.buf[p]

    def force_log(self, upto: int) -> None:
        self.flushed = max(self.flushed, upto)

    def write_page(self, p) -> None:
        v, plsn, _ = self.buf[p]
        self.force_log(plsn)                                # the write-ahead rule
        self.disk[p] = (v, plsn)
        self.buf[p][2] = None
        self.page_writes += 1

    def maybe_steal(self) -> None:
        for p in list(self.buf):
            if self.buf[p][2] is not None and self.rng.random() < self.flush_p:
                self.write_page(p)

    def update(self, t: int, p: int, val: int) -> None:
        pg = self._page(p)
        lsn = self._append(Rec(0, "update", t, self.last.get(t, 0), p, pg[0], val))
        self.last[t] = lsn
        pg[0], pg[1] = val, lsn
        if pg[2] is None:
            pg[2] = lsn
        self.maybe_steal()

    def commit(self, t: int) -> None:
        lsn = self._append(Rec(0, "commit", t, self.last.get(t, 0)))
        self.force_log(lsn)                                 # no-force: only the log reaches the disk
        self._append(Rec(0, "end", t, lsn))
        self.last.pop(t, None)

    def abort(self, t: int) -> None:
        lsn = self._append(Rec(0, "abort", t, self.last.get(t, 0)))
        self.last[t] = lsn
        self._rollback(t)

    def _rollback(self, t: int) -> int:
        clrs = 0
        nxt = self.log[self.last[t] - 1].prev if self.log[self.last[t] - 1].kind == "abort" else self.last[t]
        while nxt:
            r = self.log[nxt - 1]
            if r.kind == "update":
                pg = self._page(r.page)
                lsn = self._append(Rec(0, "clr", t, self.last[t], r.page, r.after, r.before, undo_next=r.prev))
                self.last[t] = lsn
                pg[0], pg[1] = r.before, lsn
                if pg[2] is None:
                    pg[2] = lsn
                clrs += 1
                nxt = r.prev
            elif r.kind == "clr":
                nxt = r.undo_next
            else:
                nxt = r.prev
        self._append(Rec(0, "end", t, self.last[t]))
        self.last.pop(t, None)
        return clrs

    def checkpoint(self) -> None:
        dpt = {p: b[2] for p, b in self.buf.items() if b[2] is not None}
        lsn = self._append(Rec(0, "ckpt", att=dict(self.last), dpt=dpt))
        self.force_log(lsn)
        self.master = lsn

    def crash(self) -> None:
        self.buf = {}
        self.log = self.log[:self.flushed]
        self.last = {}


def workload(sys_: System, n_txn: int = 6, ops: int = 4, crash_at: int | None = None, ckpt_every: int = 7):
    """Interleave n_txn transactions of ``ops`` updates each, under strict two-phase locking of pages (as ARIES
    assumes); most commit, some abort.  Stops (crashes) after ``crash_at`` steps.  Returns the steps taken."""
    rng = sys_.rng
    todo = {t: ops for t in range(1, n_txn + 1)}
    fate = {t: ("abort" if rng.random() < 0.25 else "commit") for t in todo}
    owner: dict = {}                                    # strict 2PL on pages: held until the end
    steps = 0
    while todo:
        t = rng.choice(sorted(todo))
        free = [p for p in range(len(sys_.disk)) if owner.get(p, t) == t]
        if todo[t] and free:
            p = rng.choice(free)
            owner[p] = t
            sys_.update(t, p, rng.randrange(1, 100))
            todo[t] -= 1
        else:
            (sys_.commit if fate[t] == "commit" else sys_.abort)(t)
            del todo[t]
            for p in [p for p, u in owner.items() if u == t]:
                del owner[p]
        steps += 1
        if ckpt_every and steps % ckpt_every == 0:
            sys_.checkpoint()
        if crash_at is not None and steps >= crash_at:
            break
    return steps


def recover(sys_: System, crash_during_undo: int | None = None) -> dict:
    """ARIES on what survived: the disk pages and the forced log.  Returns per-pass statistics."""
    log = sys_.log
    start = 0
    for r in log:
        if r.kind == "ckpt":
            start = r.lsn
    att: dict = {}
    dpt: dict = {}
    if start:
        ck = log[start - 1]
        att = {t: [l, "active"] for t, l in ck.att.items()}
        dpt = dict(ck.dpt)
    scanned = 0
    for r in log[start:] if start else log:            # analysis
        scanned += 1
        if r.kind in ("update", "clr", "abort", "commit"):
            att[r.txn] = [r.lsn, "committed" if r.kind == "commit" else "active"]
        if r.kind == "end":
            att.pop(r.txn, None)
        if r.kind in ("update", "clr") and r.page not in dpt:
            dpt[r.page] = r.lsn
    analysis = {"from": start, "scanned": scanned, "losers": sorted(t for t, (_, s) in att.items() if s == "active"),
                "dpt": dict(sorted(dpt.items()))}
    for t in [t for t, (_, s) in att.items() if s == "committed"]:
        sys_._append(Rec(0, "end", t, att[t][0]))
        del att[t]
    redo_from = min(dpt.values()) if dpt else len(log) + 1
    redone = skipped = 0
    pages = {p: list(v) for p, v in sys_.disk.items()}
    for r in log[redo_from - 1:]:                      # redo: repeat history
        if r.kind not in ("update", "clr"):
            continue
        if r.page not in dpt or r.lsn < dpt[r.page] or pages[r.page][1] >= r.lsn:
            skipped += 1
            continue
        pages[r.page] = [r.after, r.lsn]
        redone += 1
    sys_.buf = {p: [v, l, None] for p, (v, l) in pages.items()}
    sys_.last = {t: l for t, (l, _) in att.items()}
    undone = clrs = 0
    order = []
    to_undo = {t: l for t, (l, _) in att.items()}
    while to_undo:                                     # undo: losers, newest record first
        t = max(to_undo, key=lambda u: to_undo[u])
        lsn = to_undo[t]
        r = sys_.log[lsn - 1]
        order.append(lsn)
        if r.kind == "update":
            pg = sys_.buf[r.page]
            c = sys_._append(Rec(0, "clr", t, sys_.last[t], r.page, r.after, r.before, undo_next=r.prev))
            sys_.last[t] = c
            pg[0], pg[1] = r.before, c
            undone += 1
            clrs += 1
            nxt = r.prev
            if crash_during_undo is not None and clrs >= crash_during_undo:
                sys_.force_log(len(sys_.log))
                for p in list(sys_.buf):
                    if sys_.rng.random() < 0.5:
                        sys_.disk[p] = tuple(sys_.buf[p][:2])
                sys_.crash()
                return {"analysis": analysis, "crashed_in_undo": True}
        elif r.kind == "clr":
            nxt = r.undo_next
        else:
            nxt = r.prev
        if nxt:
            to_undo[t] = nxt
        else:
            sys_._append(Rec(0, "end", t, sys_.last[t]))
            del to_undo[t]
    for p, (v, l, _) in sys_.buf.items():
        sys_.disk[p] = (v, l)
    sys_.force_log(len(sys_.log))
    return {"analysis": analysis, "redo_from": redo_from, "redone": redone, "skipped": skipped, "undone": undone,
            "clrs": clrs, "undo_order": order, "log_length": len(log)}


def committed_state(sys_: System, npages: int) -> dict:
    """The pages if only committed transactions had ever run (applied in log order)."""
    done = {r.txn for r in sys_.log if r.kind == "commit"}
    pages = {p: 0 for p in range(npages)}
    for r in sys_.log:
        if r.kind == "update" and r.txn in done:
            pages[r.page] = r.after
    return pages


def crash_and_recover(seed: int, n_txn: int = 6, ops: int = 4, npages: int = 8, crash_in_undo: bool = False):
    s = System(npages, seed)
    total = workload(System(npages, seed), n_txn, ops)       # how many steps the full run takes
    rng = random.Random(seed + 1000)
    s = System(npages, seed)
    workload(s, n_txn, ops, crash_at=rng.randint(1, total))
    s.crash()
    expect = committed_state(s, npages)
    if crash_in_undo:
        r1 = recover(s, crash_during_undo=1)
        if r1.get("crashed_in_undo"):
            r = recover(s)
            r["recrashed"] = True
        else:
            r = r1
    else:
        r = recover(s)
    got = {p: v for p, (v, _) in s.disk.items()}
    r["ok"] = got == expect
    return r
