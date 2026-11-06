from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs48.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, module_box, mono


def maglev_fill(prefs, M):
    """Maglev's table fill (Eisenbud et al. 2016): backends take turns claiming their next preferred free slot.
    Returns the table and the claims in order, each (backend, slots tried, slot taken)."""
    table, nxt, claims, filled = [-1] * M, [0] * len(prefs), [], 0
    while filled < M:
        for i, p in enumerate(prefs):
            tried = []
            while table[p[nxt[i]]] >= 0:
                tried.append(p[nxt[i]])
                nxt[i] += 1
            c = p[nxt[i]]
            table[c] = i
            nxt[i] += 1
            filled += 1
            claims.append((i, tried, c))
            if filled == M:
                break
    return table, claims


class Balancing(VoiceoverScene):
    def construct(self):
        self.card()
        self.layers()
        self.policies()
        self.ring()
        self.maglev()
        self.health()

    def card(self):
        card = chapter_card(2, r"Load balancing", r"Which server should take the next request?",
                            lit=(1997, 2016), extra=((1997, r"Karger et al.: \ consistent hashing"),
                                                     (2001, r"Mitzenmacher: \ two choices"),
                                                     (2016, r"Eisenbud et al.: \ Maglev")), part=PART)
        with self.voiceover("Chapter two. Load balancing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def layers(self):
        head = label(r"Layer 4 \ against layer 7", font_size=36).to_edge(UP, buff=0.3)
        segs = [(r"\textbf{IP} \ addresses", 2.4, DATA), (r"\textbf{TCP} \ ports", 2.2, DATA),
                (r"\textbf{TLS} \ encryption", 2.4, GREY_B),
                (r"\textbf{HTTP} \ GET /pastes/5c1e, \ Host, \ Cookie", 5.0, LAM)]
        packet = VGroup()
        for t, w, c in segs:
            r = Rectangle(width=w, height=0.75, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.12)
            packet.add(VGroup(r, label(t, font_size=20, color=WHITE).move_to(r)))
        packet.arrange(RIGHT, buff=0).move_to([0, 0.75, 0])
        pl = label(r"one request, \ as it crosses the network", font_size=18, color=GREY_B).next_to(packet, UP,
                                                                                                  buff=0.15)
        b4 = Brace(packet[:2], UP, buff=0.55, color=HEAD)
        l4 = wrapped_label(r"\textbf{L4} reads only this: \ it forwards whole TCP connections", 5.6, font_size=20,
                           color=HEAD).next_to(b4, UP, buff=0.12).align_to(packet, LEFT)
        b7 = Brace(packet, DOWN, buff=0.15, color=YES)
        l7 = wrapped_label(r"\textbf{L7} ends the connection, \ decrypts it and reads every request: \ routes by "
                           r"path, \ retries elsewhere, \ balances request by request", 12.0, font_size=20,
                           color=YES).next_to(b7, DOWN, buff=0.15)
        ex = VGroup(
            wrapped_label(r"L4: \ Google's Maglev, \ Linux IPVS: \ cheap per packet, \ blind to the request", 6.0,
                          font_size=19, color=HEAD),
            wrapped_label(r"L7: \ NGINX, \ Envoy, \ HAProxy: \ more work per request, \ far more control", 6.0,
                          font_size=19, color=YES),
        ).arrange(RIGHT, buff=0.6, aligned_edge=UP).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A load balancer stands in front of many servers and decides which one gets each piece of work. It can "
            "decide at two levels. <bookmark mark='a'/> A layer-four balancer reads only addresses and ports, and "
            "forwards whole TCP connections; it never sees the request inside. Google's Maglev and Linux's IPVS work "
            "this way, and they are cheap. <bookmark mark='b'/> A layer-seven balancer, like NGINX, Envoy or "
            "HAProxy, ends the connection, decrypts it and reads each HTTP request, so it can route by path, retry "
            "a failed request on another server, and balance request by request rather than connection by "
            "connection. <bookmark mark='c'/> That control costs work on every request."
        ) as vo:
            self.play(FadeIn(head), FadeIn(packet), FadeIn(pl))
            vo.wait_until("a")
            self.play(GrowFromCenter(b4), FadeIn(l4), packet[2:].animate.set_opacity(0.35))
            vo.wait_until("b")
            self.play(packet[2:].animate.set_opacity(1), GrowFromCenter(b7), FadeIn(l7))
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.wait(0.4)
        self.clear_scene()

    def policies(self):
        b = load("balance")
        P = b["policies"]
        head = label(r"Which server next?", font_size=36).to_edge(UP, buff=0.3)
        # an illustrative fleet of six queues, for the picture of two choices
        qlen = [3, 1, 4, 2, 5, 2]
        sw, x0, yb = 0.62, -6.1, -1.7
        servers, stacks = VGroup(), VGroup()
        for k, n in enumerate(qlen):
            x = x0 + k * (sw + 0.18) + sw / 2
            servers.add(VGroup(Rectangle(width=sw, height=0.42, stroke_color=KERN, stroke_width=2, fill_color=BG,
                                         fill_opacity=1).move_to([x, yb, 0]),
                               mono(f"s{k}", size=15, color=KERN).move_to([x, yb, 0])))
            stacks.add(VGroup(*[Square(side_length=0.34, stroke_width=0, fill_color=DATA, fill_opacity=0.8)
                                .move_to([x, yb + 0.42 + j * 0.4, 0]) for j in range(n)]))
        fleet = VGroup(servers, stacks)
        req = Square(side_length=0.34, stroke_width=0, fill_color=HEAD, fill_opacity=1).move_to(
            [fleet.get_center()[0], 2.25, 0])
        a, c = 1, 4
        picks = VGroup(*[SurroundingRectangle(VGroup(servers[k], stacks[k]), color=HEAD, buff=0.08)
                         for k in (a, c)])
        win = a if qlen[a] <= qlen[c] else c
        dest = [servers[win].get_x(), yb + 0.42 + qlen[win] * 0.4, 0]
        cap = wrapped_label(r"two random picks: \ join the shorter queue", 4.6, font_size=19, color=HEAD).next_to(
            fleet, DOWN, buff=0.3)
        ill = note(r"illustrative", font_size=16).next_to(cap, DOWN, buff=0.12)
        names = [(r"random", "random", NO), (r"round robin", "round robin", KERN),
                 (r"two random choices", "two choices", YES), (r"least loaded of all", "least loaded", LAM)]
        rows = [[t, f"{P[k]['mean']:.1f}", f"{P[k]['p99']:.1f}"] for t, k, _ in names]
        colors = [[c_, WHITE, WHITE] for _, _, c_ in names]
        tab = grid_table([r"policy", r"mean", r"99th pct."], rows, widths=[3.3, 1.5, 1.7], row_h=0.6,
                         font_size=21, colors=colors, mono_cols=())
        tab.move_to([3.4, 0.9, 0])
        tnote = wrapped_label(rf"{b['servers']} servers at {100 * b['load']:.0f}\% load; \ time in the system, \ in "
                              r"mean service times; \ computed", 6.4, font_size=18, color=GREY_B).next_to(
            tab, DOWN, buff=0.35).align_to(tab, LEFT)
        herd = wrapped_label(r"asking every server needs fresh counts: \ many balancers with stale ones all pick "
                             r"the same idle-looking server", 6.4, font_size=19, color=LAM).next_to(
            tnote, DOWN, buff=0.3).align_to(tab, LEFT)
        with self.voiceover(
            "<bookmark mark='a'/> To compare policies we simulated "
            f"{b['servers']} servers at {100 * b['load']:.0f} percent load. Choosing at random gives each server "
            "its own random queue, Part 31's single-server queue, with a mean of ten service times and a tail near "
            "fifty. <bookmark mark='b'/> Round robin spaces each server's arrivals evenly, and roughly halves both. "
            "<bookmark mark='c'/> The power of two choices, from Part 20: pick two servers at random and join the "
            f"shorter queue. The mean falls below three, and the tail to {P['two choices']['p99']:.0f}. "
            "<bookmark mark='d'/> Asking every server, least connections in its ideal form, does better still, but "
            "needs fresh counts from every queue; with many balancers and stale counts, all pile onto the same "
            "idle-looking server. Two choices needs two looks, and avoids the herd."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fleet), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(tnote))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1]), shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[2]), shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(req, shift=DOWN * 0.2))
            self.play(Create(picks))
            self.play(req.animate.move_to(dest), FadeIn(cap), FadeIn(ill))
            self.play(FadeIn(VGroup(*tab.cells[3]), shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[4]), shift=RIGHT * 0.15), FadeIn(herd))
        self.wait(0.4)
        self.clear_scene()

    def ring(self):
        head = label(r"Same key, \ same server", font_size=36).to_edge(UP, buff=0.3)
        cx, cy, R = -3.4, -0.35, 2.3
        # illustrative: five servers, three virtual nodes each, at fixed angles (degrees)
        vn = {"A": (10, 140, 250), "B": (40, 190, 300), "C": (75, 165, 330), "D": (100, 220, 280),
              "E": (120, 235, 355)}
        col = {"A": DATA, "B": YES, "C": NO, "D": KERN, "E": LAM}

        def pos(deg, r=R):
            return [cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)), 0]

        def owner(deg, servers):
            pts = [(a, s) for s in servers for a in vn[s]]
            return min(pts, key=lambda p: (deg - p[0]) % 360)[1]      # the next point clockwise
        circle = Circle(radius=R, color=GREY_C, stroke_width=2).move_to([cx, cy, 0])
        snodes = {s: VGroup(*[Dot(pos(a), radius=0.12, color=col[s]) for a in vn[s]]) for s in vn}
        slabels = {s: VGroup(*[label(s, font_size=18, color=col[s]).move_to(pos(a, R + 0.35)) for a in vn[s]])
                   for s in vn}
        kdeg = [5 + 18 * i for i in range(20)]
        before = [owner(d, list(vn)) for d in kdeg]
        after = [owner(d, [s for s in vn if s != "C"]) for d in kdeg]
        keys = VGroup(*[Dot(pos(d, R - 0.32), radius=0.07, color=col[o]) for d, o in zip(kdeg, before)])
        cw = label(r"clockwise", font_size=16, color=GREY_B).move_to([cx, cy, 0])
        arc = Arc(radius=0.7, start_angle=PI * 0.75, angle=-PI / 2, color=GREY_B, stroke_width=2).move_arc_center_to(
            [cx, cy, 0]).add_tip(tip_length=0.15)
        moved = [i for i in range(20) if before[i] != after[i]]
        notes = VGroup(
            wrapped_label(r"hash mod $N$: \ change $N$, \ and most keys move", 5.6, font_size=20, color=NO),
            wrapped_label(r"the ring \ (Part 39): \ a key belongs to the next server point clockwise; \ each server "
                          r"sits at many points, \ \textbf{virtual nodes}, \ to even out the arcs", 5.6,
                          font_size=20, color=WHITE),
            wrapped_label(rf"remove C: \ only C's keys move \ ({len(moved)} of {len(kdeg)} here), \ each to its "
                          r"clockwise neighbour; \ nothing else changes", 5.6, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.6, -0.2, 0])
        ill = note(r"illustrative", font_size=16).next_to(circle, DOWN, buff=0.55)
        with self.voiceover(
            "Sometimes the same key must reach the same server: a user's session, or a shard of a cache. "
            "<bookmark mark='a'/> Hashing the key modulo the number of servers does that, until a server leaves; "
            "then most keys move. <bookmark mark='b'/> Part 39's consistent hashing puts servers and keys on a "
            "ring. A key belongs to the next server clockwise, and each server sits at many points, virtual nodes, "
            "to even out the arcs. <bookmark mark='c'/> Remove a server, and only its own keys move, each to its "
            "clockwise neighbour. Everything else stays where it was."
        ) as vo:
            self.play(FadeIn(head), Create(circle), FadeIn(ill), Create(arc), FadeIn(cw))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(snodes[s]) for s in vn], *[FadeIn(slabels[s]) for s in vn], FadeIn(notes[1]))
            self.play(LaggedStart(*[FadeIn(k, scale=0.5) for k in keys], lag_ratio=0.08), run_time=2)
            vo.wait_until("c")
            self.play(FadeOut(snodes["C"]), FadeOut(slabels["C"]))
            self.play(*[keys[i].animate.set_color(col[after[i]]).scale(1.6) for i in moved], FadeIn(notes[2]))
            self.play(*[keys[i].animate.scale(1 / 1.6) for i in moved], run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    def maglev(self):
        m = load("maglev")
        head = label(r"Maglev hashing", font_size=36).to_edge(UP, buff=0.3)
        M = 7
        offs, skips = (3, 0, 3), (4, 2, 1)            # illustrative: in Maglev both come from hashes of the name
        prefs = [[(o + j * s) % M for j in range(M)] for o, s in zip(offs, skips)]
        table, claims = maglev_fill(prefs, M)
        bcol = [DATA, YES, LAM]
        cw = 0.5
        rows = VGroup()
        for i, p in enumerate(prefs):
            nums = VGroup(*[mono(f"{v}", size=18, color=GREY_A) for v in p]).arrange(RIGHT, buff=0.26)
            rows.add(VGroup(label(rf"B{i}", font_size=20, color=bcol[i]), nums).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-4.4, 1.75, 0])
        rt = label(r"each backend's order of preference over the slots", font_size=18, color=GREY_B).next_to(
            rows, UP, buff=0.2).align_to(rows, LEFT)
        slots = VGroup(*[Square(side_length=cw, stroke_color=GREY_C, stroke_width=1.5) for _ in range(M)]).arrange(
            RIGHT, buff=0.08).move_to([-4.4, -0.35, 0])
        idx = VGroup(*[mono(f"{k}", size=15, color=GREY_B).next_to(slots[k], UP, buff=0.1) for k in range(M)])
        st = label(r"the lookup table", font_size=18, color=GREY_B).next_to(idx, UP, buff=0.12)
        fills = VGroup()
        for b_, _, c in claims:
            sq = Square(side_length=cw, stroke_width=0, fill_color=bcol[b_], fill_opacity=0.5).move_to(slots[c])
            fills.add(VGroup(sq, label(rf"B{b_}", font_size=16, color=WHITE).move_to(sq)))
        ill = wrapped_label(r"illustrative: \ 3 backends, \ 7 slots; \ preference $j$ is offset $+ j \times$ skip, "
                            r"\ mod 7", 5.4, font_size=18, color=GREY_B).next_to(slots, DOWN, buff=0.35).align_to(
            rows, LEFT)
        look = wrapped_label(r"a packet: \ hash its connection, \ take the slot, \ read off the backend --- \ one "
                             r"lookup", 5.4, font_size=19, color=HEAD).next_to(ill, DOWN, buff=0.3).align_to(rows,
                                                                                                         LEFT)
        res = grid_table([r"", r"Maglev", r"ring"], [[r"keys moved needlessly", f"{100 * m['maglev']['moved_needlessly']:.2f}\\%",
                                                     f"{100 * m['ring']['moved_needlessly']:.0f}\\%"],
                                                    [r"busiest backend $\div$ mean", f"{m['maglev']['max_over_mean']:.2f}",
                                                     f"{m['ring']['max_over_mean']:.2f}"]],
                         widths=[3.3, 1.5, 1.5], row_h=0.6, font_size=20, colors=[[WHITE, NO, YES],
                                                                                  [WHITE, YES, NO]], mono_cols=())
        res.move_to([3.6, 1.2, 0])
        sp = m["slots_per_backend"]
        rnote = wrapped_label(rf"20 backends, \ 50,000 keys, \ a table of 65,537 slots: \ each backend owns "
                              rf"{sp['min']:,} or {sp['max']:,}; \ one removed, \ so {100 * m['removed_share']:.0f}\% "
                              r"of keys must move; \ the ring has 100 virtual nodes each; \ computed", 6.2,
                              font_size=18, color=GREY_B).next_to(res, DOWN, buff=0.35).align_to(res, LEFT)
        with self.voiceover(
            "Google's Maglev balancer, described by Eisenbud and colleagues in 2016, replaces the ring with a "
            "lookup table. <bookmark mark='a'/> Each backend derives, from two hashes of its name, its own order of "
            "preference over the table's slots. <bookmark mark='b'/> The backends take turns, each claiming its most "
            "preferred slot still free, until the table is full. A packet's hash picks a slot, and the slot names "
            "the backend. <bookmark mark='c'/> With twenty backends and sixty-five thousand "
            "five hundred and thirty-seven slots, every backend owns three thousand two hundred and seventy-six "
            "slots, or one more. <bookmark mark='d'/> Then we removed one. Its five percent of the keys must move; "
            "Maglev also moved a third of a percent of the others, which the ring did not. In return, "
            "its busiest backend carried three percent more than the mean, against the ring's thirteen."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rt), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(st), FadeIn(idx), Create(slots))
            nxt = [0, 0, 0]
            for (b_, tried, c), f in zip(claims, fills):
                anims = []
                for _ in tried:
                    anims.append(rows[b_][1][nxt[b_]].animate.set_color(GREY_D))
                    nxt[b_] += 1
                anims.append(rows[b_][1][nxt[b_]].animate.set_color(bcol[b_]))
                nxt[b_] += 1
                self.play(*anims, FadeIn(f), run_time=0.45)
            self.play(FadeIn(ill), FadeIn(look))
            vo.wait_until("c")
            self.play(FadeIn(rnote))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*res.cells[0])), Create(res.rule), FadeIn(VGroup(*res.cells[1])))
            self.play(FadeIn(VGroup(*res.cells[2])))
        self.wait(0.4)
        self.clear_scene()

    def health(self):
        head = label(r"Health checks \ and outlier ejection", font_size=36).to_edge(UP, buff=0.3)
        lb = module_box(r"balancer", HEAD, w=1.9, h=0.8, font=20).move_to([-5.4, 0.1, 0])
        ys = [2.0, 1.25, 0.5, -0.25, -1.0, -1.75]
        servers = VGroup(*[module_box(rf"server {k + 1}", DATA, w=1.7, h=0.5, font=17).move_to([-1.6, y, 0])
                           for k, y in enumerate(ys)])
        links = VGroup(*[Line(lb[0].get_right(), s[0].get_left(), color=GREY_B, stroke_width=1.8) for s in servers])
        probes = VGroup(*[Dot(lb[0].get_right(), radius=0.06, color=YES) for _ in servers])
        dead, bad = 2, 4
        fails = VGroup(*[label(r"$\times$", font_size=26, color=NO) for _ in range(3)]).arrange(RIGHT, buff=0.08)
        fails.next_to(servers[dead], RIGHT, buff=0.15)
        errs = VGroup(*[mono("5xx", size=14, color=NO) for _ in range(3)]).arrange(RIGHT, buff=0.1)
        errs.next_to(servers[bad], RIGHT, buff=0.15)
        notes = VGroup(
            wrapped_label(r"\textbf{active}: \ probe each server every few seconds; \ out after several failures in "
                          r"a row, \ back after several successes", 5.0, font_size=19, color=YES),
            wrapped_label(r"\textbf{passive}: \ watch real responses; \ a run of errors ejects the server for a while, "
                          r"\ longer each time it recurs \ (Envoy's outlier ejection)", 5.0, font_size=19, color=NO),
            wrapped_label(r"cap the share that may be ejected: \ a bad check must not empty the fleet", 5.0,
                          font_size=19, color=HEAD),
            wrapped_label(r"a slow server is often worse than a dead one \ (Part 39's tail): \ watch latency, \ not "
                          r"just errors", 5.0, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, 0.1, 0])
        with self.voiceover(
            "A balancer must also know which servers are healthy. <bookmark mark='a'/> Active health checks probe "
            "each server every few seconds. After several failures in a row the server is taken out; after "
            "several successes it comes back. "
            "<bookmark mark='b'/> Passive checks watch the real traffic instead. Envoy calls this outlier ejection: "
            "a server that returns a run of errors is ejected for a while, and for longer each time it happens "
            "again. <bookmark mark='c'/> Two cautions. Cap the share of servers that can be ejected, so that a "
            "broken check cannot empty the fleet. <bookmark mark='d'/> And remember Part 39: a slow server is often "
            "worse than a dead one, so watch latency, not just errors."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lb), FadeIn(servers), Create(links))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for rnd in range(3):
                self.play(*[p.animate.move_to(s[0].get_left()) for p, s in zip(probes, servers)], run_time=0.6)
                self.play(FadeIn(fails[rnd]), *[p.animate.set_opacity(0) for p in probes], run_time=0.3)
                for p in probes:
                    p.move_to(lb[0].get_right()).set_opacity(1)
            self.play(servers[dead].animate.set_opacity(0.25), links[dead].animate.set_opacity(0.1))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), LaggedStart(*[FadeIn(e) for e in errs], lag_ratio=0.4))
            self.play(servers[bad].animate.set_opacity(0.25), links[bad].animate.set_opacity(0.1))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]), servers[bad].animate.set_opacity(1), links[bad].animate.set_opacity(1),
                      FadeOut(errs))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
