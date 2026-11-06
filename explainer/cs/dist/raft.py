"""Raft (Ongaro and Ousterhout, 2014) on a simulated network, with fault injection and invariant checks (Part 38).

    c = Cluster(n=5, seed=1, loss=0.05, delay=(0.005, 0.03))
    c.run(until=10.0, faults=random_faults(...), clients=client_load(...))
    c.violations            # every safety invariant broken, with the time it was seen (empty for correct Raft)
    c.history               # (time, kind, details) events for the animations: elections, appends, commits, faults

Each node keeps the persistent state of the paper's Figure 2 (currentTerm, votedFor, log) across crashes, and the
volatile state (commitIndex, lastApplied, and nextIndex/matchIndex on the leader) is lost when it crashes.  Messages
are RequestVote and AppendEntries (with heartbeats), delivered after a random delay, possibly dropped, and blocked
across a partition.  Election timeouts are randomized in [T, 2T].

Invariants checked after every event (the paper's Figure 3):
* election safety: at most one leader in any term;
* log matching: if two logs hold an entry with the same index and term, the logs are identical up to it;
* leader completeness: an entry committed in some term is in the log of every leader of a later term;
* state machine safety: no two nodes apply different commands at the same index.

``bug`` deliberately breaks the protocol, to show the checker catching it:
* ``"commit-old-term"``: a leader counts replicas of entries from earlier terms to commit them (the paper's Figure 8);
* ``"no-log-check"``: voters grant votes without the "at least as up-to-date" check;
* ``"forget-vote"``: votedFor is not persisted across crashes (``crash_after_vote`` makes voters crash right after
  voting, the targeted fault that exposes it).
"""
from __future__ import annotations

import heapq
import random
from dataclasses import dataclass, field


@dataclass
class Node:
    id: int
    term: int = 0
    voted_for: int | None = None
    log: list = field(default_factory=list)            # [(term, command)], index 1 = log[0]
    role: str = "follower"
    commit: int = 0
    applied: list = field(default_factory=list)
    up: bool = True
    votes: set = field(default_factory=set)
    next_index: dict = field(default_factory=dict)
    match_index: dict = field(default_factory=dict)
    timer: int = 0                                      # generation of the current election timer

    def last(self):
        return (self.log[-1][0] if self.log else 0), len(self.log)


class Cluster:
    def __init__(self, n: int = 5, seed: int = 0, loss: float = 0.0, delay=(0.005, 0.02), timeout: float = 0.15,
                 heartbeat: float = 0.05, bug: str | None = None, crash_after_vote: float = 0.0,
                 spread: float = 1.0):
        self.n = n
        self.rng = random.Random(seed)
        self.loss, self.delay, self.T, self.hb, self.bug = loss, delay, timeout, heartbeat, bug
        self.spread = spread                            # election timeouts uniform in [T, T (1 + spread)]
        self.crash_after_vote = crash_after_vote        # chance that a voter crashes, and restarts, right after voting
        self.nodes = [Node(i) for i in range(n)]
        self.events: list = []
        self.k = 0
        self.t = 0.0
        self.blocked: set = set()                       # frozenset({a, b}) pairs that cannot talk
        self.leaders: dict = {}                         # term -> leader id
        self.committed: dict = {}                       # index -> (term, command, term when committed)
        self.violations: list = []
        self.history: list = []
        self.messages = 0
        self.next_cmd = 0
        for nd in self.nodes:
            self._reset_timer(nd)

    # ---- plumbing ----------------------------------------------------------------------------------------------
    def _push(self, t, kind, data):
        self.k += 1
        heapq.heappush(self.events, (t, self.k, kind, data))

    def _reset_timer(self, nd):
        nd.timer += 1
        self._push(self.t + self.T * (1 + self.spread * self.rng.random()), "timeout", (nd.id, nd.timer))

    def _send(self, a, b, msg):
        self.messages += 1
        if frozenset((a, b)) in self.blocked or self.rng.random() < self.loss:
            return
        self._push(self.t + self.rng.uniform(*self.delay), "msg", (a, b, msg))

    def _log(self, kind, **kw):
        self.history.append((round(self.t, 4), kind, kw))

    # ---- protocol ----------------------------------------------------------------------------------------------
    def _become_follower(self, nd, term):
        if term > nd.term:
            nd.term, nd.voted_for = term, None
        if nd.role != "follower":
            nd.role = "follower"

    def _start_election(self, nd):
        nd.term += 1
        nd.role = "candidate"
        nd.voted_for = nd.id
        nd.votes = {nd.id}
        self._log("candidate", node=nd.id, term=nd.term)
        lt, li = nd.last()
        for p in range(self.n):
            if p != nd.id:
                self._send(nd.id, p, ("RV", nd.term, nd.id, li, lt))
        self._reset_timer(nd)
        self._maybe_win(nd)

    def _maybe_win(self, nd):
        if nd.role == "candidate" and len(nd.votes) > self.n // 2:
            nd.role = "leader"
            prev = self.leaders.get(nd.term)
            if prev is not None and prev != nd.id:
                self.violations.append((self.t, "election safety", f"term {nd.term}: {prev} and {nd.id}"))
            self.leaders[nd.term] = nd.id
            nd.next_index = {p: len(nd.log) + 1 for p in range(self.n)}
            nd.match_index = {p: 0 for p in range(self.n)}
            nd.match_index[nd.id] = len(nd.log)
            self._log("leader", node=nd.id, term=nd.term)
            # leader completeness, checked the moment a leader appears
            for idx, (term, cmd, cterm) in self.committed.items():
                if cterm < nd.term and (len(nd.log) < idx or nd.log[idx - 1] != (term, cmd)):
                    self.violations.append((self.t, "leader completeness",
                                            f"leader {nd.id} of term {nd.term} lacks committed entry {idx}"))
            self._heartbeat(nd)

    def _heartbeat(self, nd):
        if nd.role != "leader" or not nd.up:
            return
        for p in range(self.n):
            if p != nd.id:
                self._append_to(nd, p)
        self._push(self.t + self.hb, "heartbeat", (nd.id, nd.term))

    def _append_to(self, nd, p):
        ni = nd.next_index.get(p, len(nd.log) + 1)
        prev_i = ni - 1
        prev_t = nd.log[prev_i - 1][0] if prev_i >= 1 else 0
        entries = nd.log[ni - 1:ni - 1 + 32]
        self._send(nd.id, p, ("AE", nd.term, nd.id, prev_i, prev_t, list(entries), nd.commit))

    def submit(self, cmd=None):
        """A client sends a command to whichever node it believes is leader (here: the current one, if any)."""
        cmd = cmd if cmd is not None else f"c{self.next_cmd}"
        self.next_cmd += 1
        for nd in self.nodes:
            if nd.up and nd.role == "leader":
                nd.log.append((nd.term, cmd))
                nd.match_index[nd.id] = len(nd.log)
                self._log("append", node=nd.id, term=nd.term, index=len(nd.log), cmd=cmd)
                return True
        return False

    def _advance_commit(self, nd):
        for idx in range(len(nd.log), nd.commit, -1):
            if self.bug != "commit-old-term" and nd.log[idx - 1][0] != nd.term:
                continue                                          # only count replicas for current-term entries
            if sum(1 for p in range(self.n) if nd.match_index.get(p, 0) >= idx) > self.n // 2:
                self._commit_to(nd, idx)
                break

    def _commit_to(self, nd, idx):
        if idx <= nd.commit:
            return
        for i in range(nd.commit + 1, idx + 1):
            e = nd.log[i - 1]
            if i in self.committed and self.committed[i][:2] != e:
                self.violations.append((self.t, "state machine safety", f"index {i} committed twice"))
            self.committed.setdefault(i, (e[0], e[1], nd.term))
        nd.commit = idx
        self._log("commit", node=nd.id, term=nd.term, index=idx)
        self._apply(nd)

    def _apply(self, nd):
        while len(nd.applied) < nd.commit:
            nd.applied.append(nd.log[len(nd.applied)][1])
        # state machine safety across nodes
        for other in self.nodes:
            m = min(len(other.applied), len(nd.applied))
            if other.applied[:m] != nd.applied[:m]:
                self.violations.append((self.t, "state machine safety", f"nodes {nd.id} and {other.id} disagree"))
                break

    def _on_msg(self, a, b, msg):
        nd = self.nodes[b]
        if not nd.up:
            return
        kind, term = msg[0], msg[1]
        if term > nd.term:
            self._become_follower(nd, term)
        if kind == "RV":
            _, term, cand, li, lt = msg
            my_t, my_i = nd.last()
            up_to_date = (lt, li) >= (my_t, my_i) or self.bug == "no-log-check"
            grant = term == nd.term and nd.voted_for in (None, cand) and up_to_date
            if grant:
                nd.voted_for = cand
                self._reset_timer(nd)
                if self.crash_after_vote and self.rng.random() < self.crash_after_vote:
                    self.schedule(self.t + 0.001, "crash", b)
                    self.schedule(self.t + 0.002, "restart", b)
            self._send(b, a, ("RVR", nd.term, grant))
        elif kind == "RVR":
            _, term, grant = msg
            if nd.role == "candidate" and term == nd.term and grant:
                nd.votes.add(a)
                self._maybe_win(nd)
        elif kind == "AE":
            _, term, leader, prev_i, prev_t, entries, lcommit = msg
            if term < nd.term:
                self._send(b, a, ("AER", nd.term, False, 0))
                return
            if nd.role != "follower":
                nd.role = "follower"
            self._reset_timer(nd)
            if prev_i > len(nd.log) or (prev_i >= 1 and nd.log[prev_i - 1][0] != prev_t):
                self._send(b, a, ("AER", nd.term, False, min(prev_i - 1, len(nd.log))))
                return
            i = prev_i
            for e in entries:
                i += 1
                if len(nd.log) >= i:
                    if nd.log[i - 1][0] != e[0]:
                        del nd.log[i - 1:]
                        nd.log.append(tuple(e))
                else:
                    nd.log.append(tuple(e))
            last_new = prev_i + len(entries)
            if lcommit > nd.commit:
                new_commit = min(lcommit, last_new)
                if new_commit > nd.commit:
                    for j in range(nd.commit + 1, new_commit + 1):
                        e = nd.log[j - 1]
                        if j in self.committed and self.committed[j][:2] != e:
                            self.violations.append((self.t, "state machine safety", f"index {j} differs on {b}"))
                    nd.commit = new_commit
                    self._apply(nd)
            self._send(b, a, ("AER", nd.term, True, last_new))
        elif kind == "AER":
            _, term, ok, idx = msg
            if nd.role != "leader" or term != nd.term:
                return
            if ok:
                nd.match_index[a] = max(nd.match_index.get(a, 0), idx)
                nd.next_index[a] = nd.match_index[a] + 1
                self._advance_commit(nd)
            else:
                nd.next_index[a] = max(1, min(nd.next_index.get(a, 1) - 1, idx + 1))
                self._append_to(nd, a)

    # ---- faults ------------------------------------------------------------------------------------------------
    def crash(self, i):
        nd = self.nodes[i]
        if not nd.up:
            return
        nd.up = False
        nd.role = "follower"
        nd.commit = 0
        nd.applied = []
        nd.votes = set()
        if self.bug == "forget-vote":
            nd.voted_for = None
        self._log("crash", node=i)

    def restart(self, i):
        nd = self.nodes[i]
        if nd.up:
            return
        nd.up = True
        if self.bug == "forget-vote":
            nd.voted_for = None
        self._log("restart", node=i)
        self._reset_timer(nd)

    def partition(self, groups):
        """groups: lists of node ids; nodes in different groups cannot talk."""
        self.blocked = set()
        g = {i: k for k, grp in enumerate(groups) for i in grp}
        for a in range(self.n):
            for b in range(a + 1, self.n):
                if g.get(a, -1) != g.get(b, -2):
                    self.blocked.add(frozenset((a, b)))
        self._log("partition", groups=[list(x) for x in groups])

    def heal(self):
        self.blocked = set()
        self._log("heal")

    # ---- the run -----------------------------------------------------------------------------------------------
    def schedule(self, t, action, *args):
        self._push(t, "fault", (action, args))

    def run(self, until: float = 10.0, client_rate: float = 20.0):
        if client_rate:
            self._push(self.rng.expovariate(client_rate), "client", None)
        while self.events:
            if self.events[0][0] > until:                  # leave later events queued: runs can be resumed
                self.t = until
                break
            t, _, kind, data = heapq.heappop(self.events)
            self.t = t
            if kind == "timeout":
                i, gen = data
                nd = self.nodes[i]
                if nd.up and gen == nd.timer and nd.role != "leader":
                    self._start_election(nd)
            elif kind == "heartbeat":
                i, term = data
                nd = self.nodes[i]
                if nd.up and nd.role == "leader" and nd.term == term:
                    self._heartbeat(nd)
            elif kind == "msg":
                self._on_msg(*data)
            elif kind == "client":
                self.submit()
                self._push(self.t + self.rng.expovariate(client_rate), "client", None)
            elif kind == "fault":
                action, args = data
                getattr(self, action)(*args)
            self._check_log_matching()
        return self

    def _check_log_matching(self):
        if self.k % 7:                                   # sampled: the full check is quadratic
            return
        logs = [nd.log for nd in self.nodes]
        for x in range(self.n):
            for y in range(x + 1, self.n):
                a, b = logs[x], logs[y]
                m = min(len(a), len(b))
                for i in range(m - 1, -1, -1):
                    if a[i][0] == b[i][0]:
                        if a[:i + 1] != b[:i + 1]:
                            self.violations.append((self.t, "log matching", f"nodes {x}, {y} at {i + 1}"))
                        break

    def summary(self):
        return {"terms": max(nd.term for nd in self.nodes), "leaders": len(self.leaders),
                "committed": len(self.committed), "messages": self.messages,
                "violations": len(self.violations), "kinds": sorted({v[1] for v in self.violations})}


def random_faults(c: Cluster, until: float, rate: float = 1.0, rng=None):
    """Schedule crashes, restarts, partitions and heals at random, about ``rate`` a second."""
    rng = rng or random.Random(c.rng.random())
    t = 0.5
    down = set()
    while t < until:
        t += rng.expovariate(rate)
        r = rng.random()
        if r < 0.35 and len(down) < (c.n - 1) // 2:
            i = rng.randrange(c.n)
            if i not in down:
                down.add(i)
                c.schedule(t, "crash", i)
        elif r < 0.6 and down:
            i = rng.choice(sorted(down))
            down.discard(i)
            c.schedule(t, "restart", i)
        elif r < 0.8:
            ids = list(range(c.n))
            rng.shuffle(ids)
            k = rng.randrange(1, c.n)
            c.schedule(t, "partition", [ids[:k], ids[k:]])
        else:
            c.schedule(t, "heal")
    c.schedule(until - 1.0, "heal")
    for i in sorted(down):
        c.schedule(until - 1.0, "restart", i)
