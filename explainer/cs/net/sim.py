"""Our internet (Part 36): an event-driven simulation of hosts and routers joined by links with bandwidth,
propagation delay and loss; IP forwarding by longest-prefix match; TTL and ICMP time-exceeded; ping and
traceroute.

    net = Internet(seed)
    net.router("r1"); net.host("pebble1", "10.1.0.2/24", gateway="r1")
    net.link("r1", "r2", mbps=100, km=800, loss=0.0)
    net.converge()                       # link-state routing: every router runs Dijkstra on the whole graph
    net.ping("pebble1", "pebble2")       # round-trip time, measured in the simulation
    net.traceroute("pebble1", "pebble2") # TTL 1, 2, 3, ...: who sent each time-exceeded, and when
    net.fail("r2", "r3"); net.converge(delays={router: seconds})  # routers adopt new tables at different times

A packet's delay on a link is its size / bandwidth (serialization) plus distance / c in fibre (propagation), plus
time waiting behind earlier packets on that link's queue.
"""
from __future__ import annotations

import heapq
import random

from explainer.cs.net.ip import Prefix, ip
from explainer.cs.net.phy import C_FIBRE
from explainer.cs.net.routing import spf


class Link:
    def __init__(self, a, b, mbps, km, loss):
        self.ends = (a, b)
        self.bps = mbps * 1e6
        self.prop = km * 1000 / C_FIBRE
        self.loss = loss
        self.free_at = {a: 0.0, b: 0.0}          # per direction: when the transmitter is next idle
        self.up = True
        self.sent = 0


class Internet:
    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)
        self.routers: dict = {}
        self.hosts: dict = {}
        self.links: dict = {}
        self.adj: dict = {}
        self.tables: dict = {}
        self.pending: list = []
        self.now = 0.0
        self.events: list = []
        self.seq = 0
        self.log: list = []

    # ---------------------------------------------------------------- building
    def router(self, name):
        self.routers[name] = {}
        self.adj.setdefault(name, {})

    def host(self, name, addr_prefix: str, gateway: str):
        a, n = addr_prefix.split("/")
        self.hosts[name] = {"addr": ip(a), "prefix": Prefix(ip(a), int(n)), "gw": gateway}
        self.adj.setdefault(name, {})
        self.link(name, gateway, mbps=1000, km=0.1)

    def link(self, a, b, mbps=100, km=100, loss=0.0):
        L = Link(a, b, mbps, km, loss)
        self.links[frozenset((a, b))] = L
        self.adj.setdefault(a, {})[b] = L
        self.adj.setdefault(b, {})[a] = L

    def fail(self, a, b):
        self.links[frozenset((a, b))].up = False

    def addr(self, name):
        if name in self.hosts:
            return self.hosts[name]["addr"]
        return None

    # ---------------------------------------------------------------- routing
    def graph(self, routers_only=True):
        g = {}
        for x in self.routers:
            g[x] = {}
            for y, L in self.adj[x].items():
                if L.up and y in self.routers:
                    g[x][y] = L.prop * 1000 + 1          # cost: delay in ms, plus one per hop
        return g

    def compute_tables(self):
        g = self.graph()
        tables = {}
        for r in self.routers:
            sp = spf(g, r)
            t = []
            for h, info in self.hosts.items():
                gw = info["gw"]
                if gw == r:
                    t.append((info["prefix"], h))
                elif gw in sp:
                    t.append((info["prefix"], sp[gw][1]))
            tables[r] = t
        return tables

    def converge(self, delays: dict | None = None):
        new = self.compute_tables()
        if not delays:
            self.tables = new
            return
        for r, d in delays.items():
            self.pending.append((self.now + d, r, new[r]))
        for r in self.routers:
            if r not in delays:
                self.tables[r] = new[r]

    def _apply_pending(self):
        keep = []
        for t, r, tab in self.pending:
            if t <= self.now:
                self.tables[r] = tab
            else:
                keep.append((t, r, tab))
        self.pending = keep

    def next_hop(self, r, dst):
        best, bl = None, -1
        for p, hop in self.tables.get(r, []):
            if p.len > bl and p.contains(dst):
                best, bl = hop, p.len
        return best

    # ---------------------------------------------------------------- packets
    def _schedule(self, t, what):
        self.seq += 1
        heapq.heappush(self.events, (t, self.seq, what))

    def _send(self, frm, to, pkt):
        L = self.adj[frm][to]
        if not L.up:
            self.log.append((self.now, "dropped: link down", frm, to, pkt["id"]))
            return
        start = max(self.now, L.free_at[frm])
        ser = pkt["size"] * 8 / L.bps
        L.free_at[frm] = start + ser
        L.sent += 1
        if self.rng.random() < L.loss:
            self.log.append((self.now, "lost", frm, to, pkt["id"]))
            return
        self._schedule(start + ser + L.prop, ("arrive", to, frm, pkt))

    def inject(self, src_host, dst_addr, ttl=64, size=84, kind="echo", ident=None, at=None):
        self.seq += 1
        pkt = {"id": ident if ident is not None else self.seq, "src": self.hosts[src_host]["addr"], "dst": dst_addr,
               "ttl": ttl, "size": size, "kind": kind, "path": [src_host], "sent": at if at is not None else self.now}
        self._schedule(pkt["sent"], ("send", src_host, self.hosts[src_host]["gw"], pkt))
        return pkt["id"]

    def run(self, until=10.0):
        delivered = []
        while self.events and self.events[0][0] <= until:
            t, _, what = heapq.heappop(self.events)
            self.now = t
            self._apply_pending()
            if what[0] == "send":
                _, frm, to, pkt = what
                self._send(frm, to, pkt)
                continue
            _, node, came, pkt = what
            pkt = dict(pkt)
            pkt["path"] = pkt["path"] + [node]
            if node in self.hosts:
                if self.hosts[node]["addr"] == pkt["dst"]:
                    delivered.append((t, node, pkt))
                    if pkt["kind"] == "echo":
                        reply = {"id": pkt["id"], "src": pkt["dst"], "dst": pkt["src"], "ttl": 64,
                                 "size": pkt["size"], "kind": "echo-reply", "path": [node], "sent": pkt["sent"],
                                 "orig_ttl": pkt["ttl"]}
                        self._send(node, self.hosts[node]["gw"], reply)
                continue
            # a router
            pkt["ttl"] -= 1
            if pkt["ttl"] <= 0:
                self.log.append((t, "ttl expired", node, None, pkt["id"]))
                if pkt["kind"] in ("echo", "probe"):
                    err = {"id": pkt["id"], "src": None, "dst": pkt["src"], "ttl": 64, "size": 56,
                           "kind": "time-exceeded", "by": node, "path": [node], "sent": pkt["sent"]}
                    hop = self.next_hop(node, pkt["src"])
                    if hop:
                        self._send(node, hop, err)
                continue
            hop = self.next_hop(node, pkt["dst"])
            if hop is None:
                self.log.append((t, "no route", node, None, pkt["id"]))
                continue
            self._send(node, hop, pkt)
        return delivered

    # ---------------------------------------------------------------- tools
    def ping(self, a, b, count=1, size=84):
        out = []
        for k in range(count):
            self.events.clear()
            ident = self.inject(a, self.hosts[b]["addr"], size=size)
            got = self.run(until=self.now + 5)
            for t, node, pkt in got:
                if pkt["kind"] == "echo-reply" and pkt["id"] == ident:
                    out.append({"rtt": t - pkt["sent"], "path": pkt["path"]})
        return out

    def traceroute(self, a, b, max_ttl=16):
        hops = []
        for ttl in range(1, max_ttl + 1):
            self.events.clear()
            ident = self.inject(a, self.hosts[b]["addr"], ttl=ttl, kind="echo")
            got = self.run(until=self.now + 5)
            hit = [(t, pkt) for t, node, pkt in got if pkt["id"] == ident and node == a]
            if not hit:
                hops.append({"ttl": ttl, "by": None, "rtt": None})
                continue
            t, pkt = hit[0]
            by = pkt.get("by", b) if pkt["kind"] == "time-exceeded" else b
            hops.append({"ttl": ttl, "by": by, "rtt": t - pkt["sent"]})
            if pkt["kind"] == "echo-reply":
                break
        return hops
