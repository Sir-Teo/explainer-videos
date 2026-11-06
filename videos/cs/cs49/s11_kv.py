from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load,
                                   module_box, mono, tag_box)


def ring(center, r, names="ABCDEFGH", font=18, dot=0.12):
    """Nodes on a hash ring, the first at the top, the rest clockwise."""
    center = np.array([*center, 0][:3], dtype=float)
    circ = Circle(radius=r, color=GREY_C, stroke_width=2).move_to(center)
    nodes, names_ = VGroup(), VGroup()
    for k, n in enumerate(names):
        ang = PI / 2 - k * TAU / len(names)
        u = np.array([np.cos(ang), np.sin(ang), 0])
        nodes.add(Dot(center + r * u, radius=dot, color=GREY_A))
        names_.add(label(n, font_size=font, color=GREY_A).move_to(center + (r + 0.32) * u))
    g = VGroup(circ, nodes, names_)
    g.circ, g.nodes, g.names, g.center_, g.r = circ, nodes, names_, center, r
    return g


def on_ring(g, deg, extra=0.0):
    a = deg * DEGREES
    return g.center_ + (g.r + extra) * np.array([np.cos(a), np.sin(a), 0])


class Kv(VoiceoverScene):
    def construct(self):
        self.card()
        self.requirements()
        self.ring_()
        self.quorums()
        self.failures()
        self.conflicts()

    def card(self):
        card = chapter_card(10, r"A Dynamo-style key-value store",
                            r"How does a store stay writable while machines fail?", lit=(1997, 2007),
                            extra=((1997, r"Karger et al.: \ consistent hashing"),
                                   (2007, r"DeCandia et al.: \ Dynamo")), part=PART)
        with self.voiceover("Chapter ten. A Dynamo-style key-value store."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def packets(self, pairs, color=HEAD, run_time=0.8):
        """Dots travelling from a to b, all at once."""
        dots = [Dot(a, radius=0.08, color=color) for a, _ in pairs]
        self.add(*dots)
        self.play(*[d.animate.move_to(b) for d, (_, b) in zip(dots, pairs)], run_time=run_time)
        self.remove(*dots)

    def requirements(self):
        head = label(r"Requirements: \ always writable", font_size=36).to_edge(UP, buff=0.3)
        api_t = label(r"the whole interface", font_size=18, color=GREY_B)
        api = code_block([r"get(key)                 -> values, context",
                          r"put(key, context, value)"], size=17)
        api_g = VGroup(api_t, api).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        reqs = VGroup(
            wrapped_label(r"Amazon's shopping cart: \ adding to it must succeed even while machines and links fail",
                          6.0, font_size=19, color=YES),
            wrapped_label(r"latency promised at the 99.9th percentile, \ not the mean \ (the paper's example: \ "
                          r"300 ms)", 6.0, font_size=19, color=HEAD),
            wrapped_label(r"no master: \ every node equal; \ the cluster grows a machine at a time", 6.0,
                          font_size=19, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        left = VGroup(reqs[0], api_g, reqs[1], reqs[2]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        left.next_to(head, DOWN, buff=0.55).to_edge(LEFT, buff=0.5)
        keys, size_kb, n, disk_tb, fill, peak = 1e9, 2, 3, 1.0, 0.5, 50_000
        one = keys * size_kb * 1e3 / 1e12
        machines = int(round(one * n / (disk_tb * fill)))
        rows = [[r"data", r"$10^9$ keys $\times$ 2 kB", rf"{one:.0f} TB"],
                [r"replicas", rf"N $=$ {n}", rf"{one * n:.0f} TB"],
                [r"machines", r"1 TB disks, \ half full", rf"{machines}"],
                [r"peak load", rf"{peak:,} requests a second", rf"{peak / machines:,.0f} each"]]
        tab = grid_table([r"quantity", r"assumption", r"result"], rows, widths=[1.6, 3.4, 1.5], row_h=0.52,
                         font_size=18, mono_cols=())
        for r in range(1, len(rows) + 1):
            tab.cells[r][2].set_color(HEAD)
        nap = label(r"the napkin", font_size=21, color=WHITE)
        ill = note(r"illustrative", font_size=16)
        VGroup(nap, tab, ill).arrange(DOWN, buff=0.25).move_to([3.55, 0.3, 0])
        with self.voiceover(
            "In 2007 Giuseppe DeCandia and colleagues at Amazon described Dynamo, the store behind the shopping "
            "cart. <bookmark mark='a'/> Adding to a cart must succeed even while machines and networks fail. "
            "<bookmark mark='b'/> The interface is two calls, get and put, with a context that carries version "
            "information. <bookmark mark='c'/> Latency is promised at the ninety-nine point nine percentile, not the "
            "mean: three hundred milliseconds, in the paper's example. <bookmark mark='d'/> There is no master. "
            "Every node is equal, and the cluster grows a machine at a time. <bookmark mark='e'/> On a napkin, a "
            "billion two-kilobyte values, three copies, on half-full one-terabyte disks, need twelve machines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nap), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(ill),
                      *[FadeIn(VGroup(*tab.cells[r][:2])) for r in range(1, len(rows) + 1)])
            vo.wait_until("a")
            self.play(FadeIn(reqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(api_g))
            vo.wait_until("c")
            self.play(FadeIn(reqs[1]))
            vo.wait_until("d")
            self.play(FadeIn(reqs[2]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(tab.cells[r][2]) for r in range(1, len(rows) + 1)], lag_ratio=0.4),
                      run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def ring_(self):
        head = label(r"Partitioning and replication on a ring", font_size=36).to_edge(UP, buff=0.3)
        g = ring([-2.9, -0.5], 2.05)
        client = module_box(r"client", DATA, w=1.3, h=0.55).move_to([-5.9, 2.45, 0])
        kd = 20
        key = Dot(on_ring(g, kd), radius=0.1, color=HEAD)
        kl = mono("hash(cart:42)", size=16, color=HEAD).next_to(on_ring(g, kd, 0.2), RIGHT, buff=0.08)
        arc = Arc(radius=g.r, start_angle=kd * DEGREES, angle=-110 * DEGREES, arc_center=g.center_, color=HEAD,
                  stroke_width=6)
        pref = [2, 3, 4]                     # C, D, E
        notes = VGroup(
            wrapped_label(r"hash keys and nodes onto one ring \ (Part 39's consistent hashing); \ many virtual "
                          r"nodes per machine even out the load", 5.5, font_size=19, color=WHITE),
            wrapped_label(r"the next \textbf{N} $=$ 3 distinct nodes clockwise hold the key: \ its "
                          r"\textbf{preference list}, \ C, \ D, \ E", 5.5, font_size=19, color=KERN),
            wrapped_label(r"a put goes to the coordinator \ (C), \ which writes and forwards; \ it answers once "
                          r"\textbf{W} $=$ 2 copies are written; \ a get waits for \textbf{R} replies", 5.5,
                          font_size=19, color=HEAD),
            wrapped_label(r"a new machine takes over only the keys on its new arcs", 5.5, font_size=19,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.9, -0.3, 0])
        ok = label(r"ok", font_size=18, color=YES).next_to(client, DOWN, buff=0.12)
        with self.voiceover(
            "Dynamo partitions keys by consistent hashing, from Part 39. <bookmark mark='a'/> Keys and nodes are "
            "hashed onto one ring, and many virtual nodes per machine even out the load. <bookmark mark='b'/> Walk "
            "clockwise from a key: the first N distinct nodes, here three, hold its copies. That is its preference "
            "list. <bookmark mark='c'/> A put goes to the first, the coordinator, which writes locally and forwards "
            "to the others. It answers as soon as W copies, here two, are written; the third catches up. A get "
            "likewise waits for R replies. <bookmark mark='d'/> And adding a machine moves only the keys on its new "
            "arcs."
        ) as vo:
            self.play(FadeIn(head), Create(g.circ), FadeIn(g.nodes), FadeIn(g.names), FadeIn(client))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(key), FadeIn(kl))
            vo.wait_until("b")
            self.play(Create(arc), *[g.nodes[i].animate.set_color(KERN).scale(1.35) for i in pref],
                      *[g.names[i].animate.set_color(KERN) for i in pref], FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            c, d_, e = (g.nodes[i].get_center() for i in pref)
            self.packets([(client.get_bottom(), c)])
            self.play(Indicate(g.nodes[2], color=YES))
            self.packets([(c, d_), (c, e)], run_time=0.9)
            self.packets([(d_, c)], color=YES, run_time=0.7)
            self.packets([(c, client.get_bottom())], color=YES)
            self.play(FadeIn(ok))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def quorums(self):
        q = load("quorum")["rows"]
        head = label(r"Quorums: \ $R + W > N$", font_size=36).to_edge(UP, buff=0.3)

        def sets(w_set, r_set, ok):
            boxes = VGroup(*[VGroup(Square(side_length=0.75, stroke_color=GREY_B, stroke_width=2, fill_color=BG,
                                           fill_opacity=1), label(f"{i + 1}", font_size=20, color=GREY_A))
                             for i in range(3)])
            for b in boxes:
                b[1].move_to(b[0])
            boxes.arrange(RIGHT, buff=0.35)
            wr = SurroundingRectangle(VGroup(*[boxes[i] for i in w_set]), color=KERN, buff=0.1, stroke_width=3)
            rr = SurroundingRectangle(VGroup(*[boxes[i] for i in r_set]), color=DATA, buff=0.2, stroke_width=3)
            wl = label(rf"write waits for W $=$ {len(w_set)}", font_size=18, color=KERN).next_to(wr, UP, buff=0.22)
            rl = label(rf"read waits for R $=$ {len(r_set)}", font_size=18, color=DATA).next_to(rr, DOWN, buff=0.1)
            both = set(w_set) & set(r_set)
            for i in both:
                boxes[i][0].set_fill(YES, opacity=0.35)
            v = wrapped_label(r"they share a replica: \ the read sees the write" if ok else
                              r"no replica in common: \ the read can miss the write", 2.4, font_size=18,
                              color=YES if ok else NO).next_to(rr, RIGHT, buff=0.3)
            return VGroup(boxes, wr, rr, wl, rl, v)
        top = sets((0, 1), (1, 2), True)
        bot = sets((0,), (2,), False)
        VGroup(top, bot).arrange(DOWN, buff=0.6, aligned_edge=LEFT).next_to(head, DOWN, buff=0.45).to_edge(
            LEFT, buff=0.5)
        rows, colors = [], []
        for r in q:
            c = YES if r["overlap"] else NO
            pct = (lambda v: r"0\%" if v == 0 else rf"{100 * v:.1f}\%")
            rows.append([f"{r['N']}", f"{r['R']}", f"{r['W']}", r"yes" if r["overlap"] else r"no",
                         pct(r["stale_now"]), pct(r["stale_after_10ms"])])
            common = (r["N"], r["R"], r["W"]) == (3, 2, 2)
            colors.append([HEAD if common else WHITE] * 3 + [c, c, c])
        tab = grid_table([r"N", r"R", r"W", r"overlap", r"stale at once", r"after 10 ms"], rows,
                         widths=[0.6, 0.6, 0.6, 1.2, 1.75, 1.6], row_h=0.46, font_size=18, colors=colors,
                         mono_cols=())
        tt = label(r"a read just after the write is acknowledged", font_size=19, color=WHITE)
        common_note = label(r"(3, 2, 2): \ the paper's common setting", font_size=18, color=HEAD)
        foot = wrapped_label(r"stale: \ the read returns an older value; \ 20{,}000 simulated writes per row, \ "
                             r"replication delays exponential, \ mean 10 ms \ (the PBS model, \ Bailis et al., \ "
                             r"2012; \ Part 39)", 6.2, font_size=17, color=GREY_B)
        VGroup(tt, tab, common_note, foot).arrange(DOWN, buff=0.28).move_to([3.5, -0.15, 0])
        with self.voiceover(
            "How many replies are enough? <bookmark mark='a'/> If a write waits for W copies and a read for R, and R "
            "plus W exceeds N, every read set overlaps every write set, so a read always meets the latest write. "
            "Three, two, two is the setting the Dynamo paper reports as common. <bookmark mark='b'/> With R and W "
            "both one, the sets can miss. <bookmark mark='c'/> We simulated reads with Part 39's model of "
            "replication delays. Right after a write is acknowledged, with N three and R and W one, a read returns "
            "the old value fifty-three percent of the time; ten milliseconds later, nineteen percent. "
            "<bookmark mark='d'/> With overlapping quorums, never. Small quorums buy speed with staleness."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top[0]), Create(top[1]), Create(top[2]), FadeIn(top[3]), FadeIn(top[4]))
            self.play(FadeIn(top[5]))
            self.play(FadeIn(tt), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            self.play(FadeIn(common_note))
            vo.wait_until("b")
            self.play(FadeIn(bot[0]), Create(bot[1]), Create(bot[2]), FadeIn(bot[3]), FadeIn(bot[4]))
            self.play(FadeIn(bot[5]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(1, len(rows) + 1)],
                                  lag_ratio=0.4), FadeIn(foot), run_time=2.4)
            vo.wait_until("d")
            self.play(*[Indicate(tab.cells[r][4], color=YES) for r in range(1, len(rows) + 1)
                        if q[r - 1]["overlap"]])
        self.wait(0.4)
        self.clear_scene()

    def failures(self):
        head = label(r"When a node fails: \ hints and Merkle trees", font_size=36).to_edge(UP, buff=0.3)
        g = ring([-4.0, 0.0], 1.55, font=17, dot=0.11)
        pref = [2, 3, 4]
        for i in pref:
            g.nodes[i].set_color(KERN)
            g.names[i].set_color(KERN)
        down = Cross(g.nodes[3], stroke_color=NO, stroke_width=4, scale_factor=2.2)
        hint = tag_box("hint: for D", NO, size=15).next_to(g.names[5], DOWN, buff=0.12)
        rnotes = VGroup(
            wrapped_label(r"\textbf{sloppy quorum}: \ D is down, \ so the next healthy node, \ F, \ takes its copy",
                          5.6, font_size=18, color=WHITE),
            wrapped_label(r"\textbf{hinted handoff}: \ when D returns, \ F hands the copy over and deletes its own",
                          5.6, font_size=18, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.9, -2.75, 0])

        def tree(cx, hashes):
            pos = [(cx, 1.85), (cx - 0.8, 0.95), (cx + 0.8, 0.95)] + [(cx + dx, 0.05) for dx in (-1.2, -0.4, 0.4,
                                                                                                   1.2)]
            nodes = VGroup(*[tag_box(h, GREY_B, size=16, w=0.62, h=0.45).move_to([x, y, 0])
                             for h, (x, y) in zip(hashes, pos)])
            edges = VGroup(*[Line(nodes[p].get_bottom(), nodes[c].get_top(), color=GREY_D, stroke_width=1.6)
                             for p, c in ((0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6))])
            return VGroup(edges, nodes)
        tx = tree(1.7, ["7f", "3a", "c2", "11", "9e", "4b", "d0"])
        ty = tree(5.2, ["e5", "3a", "08", "11", "9e", "4b", "6c"])
        titles = VGroup(label(r"replica X", font_size=18, color=GREY_A).next_to(tx[1][0], UP, buff=0.15),
                        label(r"replica Y", font_size=18, color=GREY_A).next_to(ty[1][0], UP, buff=0.15))

        def paint(i, col):
            return [t[1][i][0].animate.set_stroke(col, width=2.6) for t in (tx, ty)] + \
                   [t[1][i][1].animate.set_color(col) for t in (tx, ty)]
        swap = CurvedArrow(tx[1][6].get_bottom() + DOWN * 0.05, ty[1][6].get_bottom() + DOWN * 0.05, angle=0.6,
                           color=HEAD, stroke_width=2.5)
        sl = label(r"exchange this key range only", font_size=17, color=HEAD).next_to(swap, DOWN, buff=0.08)
        mnote = wrapped_label(r"equal hashes, \ equal data; \ descend only where they differ: \ the cost grows "
                              r"with the differences, \ not with the data \ (Part 39 measured it; \ Part 41's "
                              r"content addressing)", 5.8, font_size=18, color=WHITE).move_to([3.55, -2.35, 0])
        ill = note(r"hashes illustrative", font_size=16).to_corner(DR, buff=0.3)
        c, e, f, dd = (g.nodes[i].get_center() for i in (2, 4, 5, 3))
        with self.voiceover(
            "At this scale machines fail constantly, and Dynamo keeps writing through it. <bookmark mark='a'/> "
            "Suppose D, in the key's preference list, is down. Rather than refuse, the coordinator sends D's copy to "
            "the next healthy node, F, with a hint saying whom it is for: a sloppy quorum. <bookmark mark='b'/> When "
            "D returns, F hands the copy over and deletes its own. That is hinted handoff. <bookmark mark='c'/> "
            "Replicas still drift apart, so in the background they compare Merkle trees, hash trees over their key "
            "ranges. <bookmark mark='d'/> Equal roots mean equal data. Where hashes differ, descend, and exchange "
            "only those ranges: the cost grows with the differences, not with the data."
        ) as vo:
            self.play(FadeIn(head), Create(g.circ), FadeIn(g.nodes), FadeIn(g.names))
            vo.wait_until("a")
            self.play(g.nodes[3].animate.set_color(NO), g.names[3].animate.set_color(NO), Create(down))
            self.packets([(c, e), (c, f)], run_time=1.0)
            self.play(g.nodes[5].animate.set_color(KERN), g.names[5].animate.set_color(KERN), FadeIn(hint),
                      FadeIn(rnotes[0]))
            vo.wait_until("b")
            self.play(FadeOut(down), g.nodes[3].animate.set_color(KERN), g.names[3].animate.set_color(KERN))
            self.packets([(f, dd)], color=YES, run_time=1.0)
            self.play(FadeOut(hint), g.nodes[5].animate.set_color(GREY_A), g.names[5].animate.set_color(GREY_A),
                      FadeIn(rnotes[1]))
            vo.wait_until("c")
            self.play(FadeIn(tx), FadeIn(ty), FadeIn(titles), FadeIn(ill))
            vo.wait_until("d")
            self.play(*paint(0, NO))
            self.play(*paint(1, YES), *paint(2, NO))
            self.play(*paint(5, YES), *paint(6, NO))
            self.play(Create(swap), FadeIn(sl))
            self.play(FadeIn(mnote))
        self.wait(0.4)
        self.clear_scene()

    def conflicts(self):
        head = label(r"Conflicts, \ and the price of availability", font_size=36).to_edge(UP, buff=0.3)
        specs = [("[X:1]", r"\{book\}", WHITE, [-5.6, 1.6]),
                 ("[X:2]", r"\{book, pen\}", WHITE, [-3.6, 1.6]),
                 ("[X:2, Y:1]", r"\{book, pen, mug\}", DATA, [-0.9, 2.3]),
                 ("[X:2, Z:1]", r"\{book\}", LAM, [-0.9, 0.85]),
                 ("[X:3, Y:1, Z:1]", r"\{book, pen, mug\}", YES, [2.4, 1.6])]
        vs = VGroup()
        for vv, cart, col, (x, y) in specs:
            t = tag_box(vv, col, size=17).move_to([x, y, 0])
            c = label(cart, font_size=16, color=GREY_A).next_to(t, DOWN, buff=0.08)
            vs.add(VGroup(t, c))
        edges = VGroup(*[Arrow(vs[a][0].get_right(), vs[b][0].get_left(), buff=0.08, color=GREY_C, stroke_width=2,
                               max_tip_length_to_length_ratio=0.12)
                         for a, b in ((0, 1), (1, 2), (1, 3), (2, 4), (3, 4))])
        via = VGroup(label(r"via Y", font_size=16, color=DATA).next_to(edges[1], UP, buff=0.02),
                     label(r"via Z: \ pen removed", font_size=16, color=LAM).next_to(
                         edges[2].point_from_proportion(0.3), DL, buff=0.05))
        sib = wrapped_label(r"neither descends from the other: \ a get returns both \ (\textbf{siblings}); \ the cart "
                            r"merges them by union, \ so the removed pen comes back", 3.0, font_size=18,
                            color=HEAD).move_to([5.25, 1.55, 0])
        ill = note(r"illustrative; \ version vectors as in Part 38", font_size=16).next_to(vs, DOWN, buff=0.25)
        ill.align_to(vs, LEFT)
        bar = Line([-4.6, -1.35, 0], [4.6, -1.35, 0], color=GREY_B, stroke_width=3)
        knob = Dot(bar.get_start(), radius=0.13, color=HEAD)
        lo = wrapped_label(r"small quorums: \ fast, \ always writable, \ stale reads", 3.4, font_size=18,
                           color=KERN).next_to(bar, DOWN, buff=0.25).align_to(bar, LEFT)
        hi = wrapped_label(r"overlapping quorums: \ fresh reads, \ slower, \ fewer failures survived", 3.4,
                           font_size=18, color=DATA).next_to(bar, DOWN, buff=0.25).align_to(bar, RIGHT)
        dial = label(r"R and W: \ the dial", font_size=18, color=GREY_A).next_to(bar, UP, buff=0.12)
        foot = wrapped_label(r"Dynamo chose availability \ (CAP, \ Part 39); \ Cassandra and Riak followed its "
                             r"design; \ a payment ledger \ (Chapter 8) \ could not", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Because any node can accept a write, two clients can update one cart while the network is split. "
            "<bookmark mark='a'/> Dynamo tags every version with a version vector, Part 38's vector clock, one "
            "counter per coordinating node. <bookmark mark='b'/> Here two versions descend from the second through "
            "different nodes, and neither has seen the other. <bookmark mark='c'/> A get returns both, as siblings, "
            "and the cart merges them by union; as the paper notes, a removed item can come back. "
            "<bookmark mark='d'/> The quorum sizes are a dial, from fast and always writable but sometimes stale, to "
            "fresh but slower. <bookmark mark='e'/> Dynamo chose availability, and Cassandra and Riak followed. A "
            "payment ledger, from chapter eight, could not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(vs[0]))
            vo.wait_until("a")
            self.play(GrowArrow(edges[0]), FadeIn(vs[1]), FadeIn(ill))
            vo.wait_until("b")
            self.play(GrowArrow(edges[1]), FadeIn(vs[2]), FadeIn(via[0]))
            self.play(GrowArrow(edges[2]), FadeIn(vs[3]), FadeIn(via[1]))
            vo.wait_until("c")
            self.play(FadeIn(sib))
            self.play(GrowArrow(edges[3]), GrowArrow(edges[4]), FadeIn(vs[4]))
            vo.wait_until("d")
            self.play(Create(bar), FadeIn(knob), FadeIn(dial), FadeIn(lo), FadeIn(hi))
            self.play(knob.animate.move_to(bar.get_end()), run_time=1.5)
            self.play(knob.animate.move_to(bar.get_start()), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, YES)
