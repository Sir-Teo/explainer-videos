"""Bridges (Part 36): learning switches, the broadcast storm a loop causes, and Perlman's spanning tree.

    topology: {bridge id: {port: (neighbour kind, neighbour)}} built by ``lan(links, hosts)``
    flood(topo, start, active=None, limit)   copies of one broadcast frame, hop by hop, until the limit; with
                                             ``active`` (the ports a spanning tree leaves on) it dies out
    spanning_tree(topo)  Perlman's algorithm, run as rounds of configuration messages: each bridge believes
                         (root, cost to root, its own id); it adopts any better offer heard on a port; then the root
                         port and designated ports stay active and the rest block
    learning(topo, frames, active)           MAC learning: each frame floods until its destination's port is known
"""
from __future__ import annotations


def lan(links: list[tuple[int, int]], hosts: dict[str, int]) -> dict:
    topo: dict = {}
    for a, b in links:
        topo.setdefault(a, {})
        topo.setdefault(b, {})
        pa, pb = len(topo[a]), len(topo[b])
        topo[a][pa] = ("bridge", b, pb)
        topo[b][pb] = ("bridge", a, pa)
    for h, b in hosts.items():
        topo.setdefault(b, {})
        topo[b][len(topo[b])] = ("host", h, None)
    return topo


def flood(topo: dict, start: int, active: dict | None = None, limit: int = 200) -> dict:
    """A broadcast arriving at bridge ``start`` from a host.  Each bridge forwards a copy out of every active port
    except the one it came in on.  Returns copies per hop and the hosts reached."""
    frontier = [(start, None)]
    per_hop, delivered = [], {}
    sent = 0
    for hop in range(limit):
        nxt = []
        for b, inport in frontier:
            for p, (kind, nb, nbport) in topo[b].items():
                if p == inport or (active is not None and p not in active[b]):
                    continue
                sent += 1
                if kind == "host":
                    delivered[nb] = delivered.get(nb, 0) + 1
                else:
                    nxt.append((nb, nbport))
        per_hop.append(len(nxt))
        frontier = nxt
        if not frontier or sent > 10 ** 6:
            break
    return {"per_hop": per_hop, "sent": sent, "delivered": delivered, "ended": not frontier}


def spanning_tree(topo: dict, max_rounds: int = 50) -> dict:
    bridges = sorted(topo)
    best = {b: (b, 0, b) for b in bridges}                 # (root, cost, sender) as believed by b
    root_port = {b: None for b in bridges}
    rounds = 0
    for rounds in range(1, max_rounds + 1):
        changed = False
        msgs = []
        for b in bridges:
            r, c, _ = best[b]
            for p, (kind, nb, nbport) in topo[b].items():
                if kind == "bridge":
                    msgs.append((nb, nbport, (r, c + 1, b)))
        for nb, port, offer in msgs:
            if offer < best[nb]:
                best[nb] = offer
                root_port[nb] = port
                changed = True
        if not changed:
            break
    root = min(bridges)
    active = {b: set() for b in bridges}
    for b in bridges:
        for p, (kind, nb, nbport) in topo[b].items():
            if kind == "host":
                active[b].add(p)
            elif p == root_port[b]:
                active[b].add(p)
            else:
                # designated port: this bridge offers the better path to the root on this segment
                mine = (best[b][0], best[b][1], b)
                theirs = (best[nb][0], best[nb][1], nb)
                if mine < theirs and root_port[nb] == nbport:
                    active[b].add(p)
    blocked = sum(1 for b in bridges for p, (k, _, _) in topo[b].items() if k == "bridge" and p not in active[b])
    return {"root": root, "best": best, "root_port": root_port, "active": active, "rounds": rounds,
            "blocked_ports": blocked}


def learning(topo: dict, frames: list[tuple[str, str]], active: dict, host_at: dict) -> dict:
    """Frames (src host, dst host).  Each bridge learns src -> in-port; forwards to the learned port of dst, or
    floods.  Returns the copies sent per frame."""
    tables = {b: {} for b in topo}
    out = []
    for src, dst in frames:
        start = host_at[src]
        sent = 0
        frontier = [(start, next(p for p, v in topo[start].items() if v[0] == "host" and v[1] == src))]
        seen = set()
        while frontier:
            nxt = []
            for b, inport in frontier:
                if (b, inport) in seen:
                    continue
                seen.add((b, inport))
                tables[b][src] = inport
                ports = [tables[b][dst]] if dst in tables[b] else [p for p in active[b] if p != inport]
                for p in ports:
                    kind, nb, nbport = topo[b][p]
                    sent += 1
                    if kind == "bridge":
                        nxt.append((nb, nbport))
            frontier = nxt
        out.append(sent)
    return {"copies": out, "tables": {b: dict(t) for b, t in tables.items()}}
