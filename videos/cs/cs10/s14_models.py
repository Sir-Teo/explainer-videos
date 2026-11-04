from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.pebble import parallel as Pa
from videos.cs.cs10.common import (BG, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, grid_table, load)


def draw_graph(g, pos, n_proc, color=DATA, r=0.09, scale=1.0, wrap=False):
    dots = VGroup(*[Dot([*(np.array(pos[v]) * scale), 0], radius=r if v < n_proc else r * 0.7,
                        color=color if v < n_proc else GREY_B) for v in g])
    edges = VGroup()
    seen = set()
    for u in g:
        for v in g[u]:
            if (v, u) in seen:
                continue
            seen.add((u, v))
            a, b = np.array(pos[u]) * scale, np.array(pos[v]) * scale
            if wrap and np.linalg.norm(a - b) > 1.0 * scale:  # a wrap-around link: drawn as an arc
                edges.add(ArcBetweenPoints([*a, 0], [*b, 0], angle=0.6, color=GREY_D, stroke_width=1.2))
            else:
                edges.add(Line([*a, 0], [*b, 0], color=GREY_D, stroke_width=1.5))
    return VGroup(edges, dots)


class Models(VoiceoverScene):
    def construct(self):
        self.card()
        self.pram()
        self.bsp()
        self.networks()
        self.table()
        self.top500()

    def card(self):
        card = chapter_card(13, r"Models and networks", r"What is a parallel computer, \ abstractly?",
                            lit=(1978, 1990, 1993), extra=((1978, r"the PRAM"), (1990, r"Valiant: \ BSP"),
                                                           (1993, r"LogP")), part=PART)
        with self.voiceover("Chapter thirteen. Models and networks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pram(self):
        head = label(r"The PRAM \ (Fortune and Wyllie, \ 1978)", font_size=34).to_edge(UP, buff=0.3)
        procs = VGroup(*[Circle(radius=0.25, stroke_color=CORE_COLORS[k % 4], stroke_width=2) for k in range(8)]
                       ).arrange(RIGHT, buff=0.35).shift(UP * 1.5)
        pl = VGroup(*[label(rf"$P_{k}$", font_size=16, color=GREY_A).move_to(c) for k, c in enumerate(procs)])
        mem = Rectangle(width=procs.width + 0.6, height=0.6, stroke_color=GREY_B).next_to(procs, DOWN, buff=0.9)
        ml = label(r"one shared memory, \ any cell in one step", font_size=20, color=GREY_B).move_to(mem)
        links = VGroup(*[Line(c.get_bottom(), [c.get_x(), mem.get_top()[1], 0], color=GREY_D, stroke_width=1.5)
                         for c in procs])
        kinds = VGroup(
            label(r"EREW: \ exclusive read, \ exclusive write", font_size=21, color=GREY_A),
            label(r"CREW: \ concurrent reads allowed", font_size=21, color=DATA),
            label(r"CRCW: \ concurrent writes too \ (some rule picks the winner)", font_size=21, color=CTRL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(mem, DOWN, buff=0.45)
        ex = label(r"the OR of $n$ bits: \ $O(1)$ steps on a CRCW PRAM \ (every 1 writes 1), \ "
                   r"$\Theta(\log n)$ on a CREW one", font_size=21, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "To design parallel algorithms without a particular machine, theorists use models. <bookmark mark='a'/> "
            "The first, the parallel random-access machine of Steven Fortune and James Wyllie in 1978, is the "
            "idealist's machine: p processors in lockstep, sharing one memory in which any cell can be read or "
            "written in a single step, with no caches and no network. <bookmark mark='b'/> Its variants differ only "
            "in what happens when processors collide: exclusive read and write, concurrent reads, or concurrent "
            "writes too. <bookmark mark='c'/> And the differences are real. The OR of n bits takes constant time if "
            "concurrent writes are allowed, since every processor holding a one simply writes one to the answer, but "
            "provably needs logarithmic time without them. The PRAM made work and span precise, but it ignores the "
            "one thing real machines cannot: communication costs time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(procs), FadeIn(pl), Create(links), FadeIn(mem), FadeIn(ml))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(k) for k in kinds], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bsp(self):
        head = label(r"Pricing communication: \ BSP and LogP", font_size=34).to_edge(UP, buff=0.3)
        procs = 4
        g = VGroup()
        x0 = -5.6
        for s in range(2):
            xs = x0 + s * 4.3
            for k in range(procs):
                w = [1.6, 1.1, 1.9, 1.3][(k + s) % 4]
                g.add(Rectangle(width=w, height=0.32, stroke_width=0, fill_color=CORE_COLORS[k],
                                fill_opacity=0.7).move_to([xs + w / 2, 1.3 - k * 0.45, 0]))
            for k in range(procs):
                a = [xs + 2.0, 1.3 - k * 0.45, 0]
                b = [xs + 2.9, 1.3 - ((k + 1 + s) % procs) * 0.45, 0]
                g.add(Arrow(a, b, buff=0.02, color=GREY_B, stroke_width=1.5, max_tip_length_to_length_ratio=0.15))
            g.add(DashedLine([xs + 3.2, 1.6, 0], [xs + 3.2, -0.2, 0], color=HEAD, stroke_width=2.5))
        labs = VGroup(label(r"compute", font_size=17, color=GREY_A).move_to([x0 + 0.9, 1.9, 0]),
                      label(r"send", font_size=17, color=GREY_A).move_to([x0 + 2.45, 1.9, 0]),
                      label(r"barrier", font_size=17, color=HEAD).move_to([x0 + 3.2, 1.9, 0]))
        cost = MathTex(r"\text{superstep} = w + g\,h + \ell", font_size=36, color=HEAD).move_to(DOWN * 0.8)
        cl = label(r"$w$: \ the most local work; \ $h$: \ the most words any processor sends or receives; \ "
                   r"$g$: \ time per word; \ $\ell$: \ the barrier", font_size=19, color=GREY_A).next_to(cost, DOWN,
                                                                                                buff=0.2)
        logp = label(r"LogP \ (Culler et al., \ 1993): \ latency $L$, \ overhead $o$, \ gap $g$, \ processors $P$: \ "
                     r"one message at a time", font_size=20, color=DATA).next_to(cl, DOWN, buff=0.35)
        mpi = label(r"in practice: \ MPI's collectives, \ broadcast, \ reduce, \ all-reduce \ (\textit{AI, Built} 18)",
                    font_size=20, color=YES).next_to(logp, DOWN, buff=0.25)
        with self.voiceover(
            "In 1990 Leslie Valiant proposed a model that charges for communication, bulk-synchronous parallelism. "
            "<bookmark mark='a'/> A computation is a series of supersteps. In each, every processor computes on its "
            "own data, then sends messages, and then all wait at a barrier until every message has arrived. "
            "<bookmark mark='b'/> A superstep costs the largest local work, plus g times the largest number of words "
            "any processor sends or receives, plus the cost of the barrier. Two numbers, g and l, summarize the "
            "whole network. <bookmark mark='c'/> LogP, from David Culler and colleagues in 1993, prices each message "
            "individually: its latency, the processor's overhead to send it, and the gap between messages. <bookmark "
            "mark='d'/> Real clusters are programmed with MPI, whose collective operations, broadcast, reduce and "
            "all-reduce, are the BSP model in a library. The all-reduce is how AI, Built's Part 18 trains one model "
            "on many GPUs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(labs), run_time=2)
            vo.wait_until("b")
            self.play(Write(cost), FadeIn(cl))
            vo.wait_until("c")
            self.play(FadeIn(logp))
            vo.wait_until("d")
            self.play(FadeIn(mpi))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def networks(self):
        head = label(r"How processors are wired: \ 16 nodes", font_size=34).to_edge(UP, buff=0.3)
        ring = Pa.ring(16)
        rpos = {v: (np.cos(2 * np.pi * v / 16) * 1.1, np.sin(2 * np.pi * v / 16) * 1.1) for v in range(16)}
        mesh = Pa.mesh(4)
        mpos = {v: ((v % 4) * 0.7 - 1.05, (v // 4) * 0.7 - 1.05) for v in range(16)}
        torus = Pa.mesh(4, wrap=True)
        cube = Pa.hypercube(4)
        cpos = {}
        for v in range(16):
            x = (v & 1) * 0.8 + ((v >> 2) & 1) * 0.4
            y = ((v >> 1) & 1) * 0.8 + ((v >> 2) & 1) * 0.3
            off = 1.4 if v & 8 else 0
            cpos[v] = (x + off - 1.3, y - 0.6 + (0.25 if v & 8 else 0))
        tree = Pa.tree(16)
        tpos = {v: (v * 0.18 - 1.35, -1.1) for v in range(16)}
        level, y, k = list(range(16)), -1.1, 16
        while len(level) > 1:
            nxt = []
            y += 0.55
            for a, b in zip(level[::2], level[1::2]):
                tpos[k] = ((tpos[a][0] + tpos[b][0]) / 2, y)
                nxt.append(k)
                k += 1
            level = nxt
        nets = [(r"ring", ring, rpos, 16), (r"2-D mesh", mesh, mpos, 16), (r"2-D torus", torus, mpos, 16),
                (r"hypercube", cube, cpos, 16), (r"tree", tree, tpos, 16)]
        figs = VGroup()
        for name, g, pos, n in nets:
            f = draw_graph(g, pos, n, wrap=name == r"2-D torus")
            figs.add(VGroup(f, label(name, font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.2)))
        figs.arrange(RIGHT, buff=0.55)
        figs.scale_to_fit_width(min(figs.width, 12.8)).move_to(DOWN * 0.2)
        fat = note(r"a \textit{fat tree} \ (Leiserson, \ 1985) \ makes the links thicker toward the root, \ so the top "
                   r"is no bottleneck: \ today's data-centre networks", font_size=17).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Real machines connect their processors with a network, and its shape matters. <bookmark mark='a'/> A "
            "ring is cheap but slow to cross. A two-dimensional mesh, the shape of many on-chip networks, connects "
            "each node to its neighbours. A torus wraps the mesh's edges around. A hypercube connects each of two to "
            "the d nodes to the d nodes that differ from it in one bit. A tree is cheap, but everything between its "
            "halves passes through the root. <bookmark mark='b'/> Charles Leiserson's fat tree fixes that by making "
            "the links thicker toward the root, and today's data-centre networks are built that way."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in figs], lag_ratio=0.4), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(fat))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        tp = load("topology")
        head = label(r"Diameter and bisection width", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        for r in tp["rows"]:
            f = tp["formulas"].get(r["name"], {})
            rows.append([r["name"], str(r["n"]), str(r["links"]), str(r["diameter"]), str(r["bisection"]),
                         str(f.get("diameter", "")), f"{f.get('bisection', ''):,}" if f else ""])
        hdr = [r"network", r"nodes", r"links", r"diameter", r"bisection", r"diameter, \ 1024", r"bisection, \ 1024"]
        colors = [[GREY_A, GREY_B, GREY_B, CTRL, YES, CTRL, YES]] * len(rows)
        t = grid_table(hdr, rows, [2.0, 1.0, 1.0, 1.4, 1.5, 2.1, 2.2], row_h=0.48, font_size=19, colors=colors,
                       mono_cols=()).move_to(UP * 0.4)
        defs = VGroup(
            label(r"\textit{diameter}: \ the most hops between two nodes", font_size=20, color=CTRL),
            label(r"\textit{bisection width}: \ the fewest links that cut the nodes into two halves \ (found here by "
                  r"trying every split)", font_size=20, color=YES),
            label(r"an all-to-all exchange must push half the data across the bisection", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Two numbers summarize a network. <bookmark mark='a'/> The diameter is the most hops between any two "
            "nodes: the worst latency. <bookmark mark='b'/> The bisection width is the smallest number of links you "
            "must cut to split the nodes into two equal halves. We found it for each sixteen-node network by trying "
            "all six thousand four hundred and thirty-five ways of splitting it. <bookmark mark='c'/> It matters "
            "because in an all-to-all exchange, like the shuffle that sorts data between machines, half the data "
            "must cross that cut. A ring has a bisection of two links however large it grows; a hypercube of a "
            "thousand and twenty-four nodes, five hundred and twelve. The tree's bisection is a single link, which is "
            "exactly what the fat tree repairs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.3))
            for mk, d in zip("abc", defs):
                vo.wait_until(mk)
                self.play(FadeIn(d))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def top500(self):
        tp = load("top500")
        ms = tp["milestones"]
        head = label(r"Supercomputers, \ 1976 to 2024", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[1975, 2026, 10], y_range=[8, 19, 1], x_length=9.0, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).shift(DOWN * 0.4 + LEFT * 0.3)
        xt = VGroup(*[label(str(y), font_size=16, color=GREY_B).next_to(ax.c2p(y, 8), DOWN, buff=0.1)
                      for y in (1980, 1990, 2000, 2010, 2020)])
        units = {9: r"giga", 12: r"tera", 15: r"peta", 18: r"exa"}
        yt = VGroup(*[label(rf"1 {u}flop/s", font_size=15, color=GREY_B).next_to(ax.c2p(1975, e), LEFT, buff=0.1)
                      for e, u in units.items()])
        dots = VGroup()
        for m in ms:
            p = ax.c2p(m["year"], np.log10(m["flops"]))
            d = Dot(p, radius=0.08, color=YES)
            side = DOWN if m["year"] >= 2024 else (UL if m["year"] > 2015 else UR)
            t = label(rf"{m['name']} \ ({m['year']})", font_size=17, color=GREY_A).next_to(d, side, buff=0.12)
            dots.add(VGroup(d, t))
        fit = DashedLine(ax.c2p(1976, np.log10(160e6)), ax.c2p(2024, np.log10(1.742e18)), color=GREY_D)
        gain = (1.742e18 / 160e6) ** (1 / 48)
        cap = label(rf"ten billion times faster in 48 years: \ $\times {gain:.2f}$ a year, \ nearly all of it from "
                    r"parallelism", font_size=21, color=HEAD).to_edge(DOWN, buff=0.3)
        fr = note(rf"Frontier \ (2022): \ {tp['frontier_cores']:,} cores, \ {tp['frontier_power_mw']:.0f} MW", font_size=17
                  ).next_to(cap, UP, buff=0.12)
        with self.voiceover(
            "And the machines themselves. <bookmark mark='a'/> In 1976 the Cray-1 peaked at a hundred and sixty "
            "million floating-point operations a second. ASCI Red, in 1997, was the first to pass a trillion on the "
            "LINPACK benchmark; Roadrunner, in 2008, a thousand trillion. In 2022 Frontier, at Oak Ridge, passed a "
            "quintillion, an exaflop, and in 2024 El Capitan reached one point seven. <bookmark mark='b'/> Ten "
            "billion times faster in forty-eight years, about sixty percent a year, and since 2005 nearly all of it "
            "from parallelism: Frontier has almost nine million cores, mostly in GPUs, and draws twenty-one "
            "megawatts."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(cap), FadeIn(fr))
        self.wait(0.3)
        self.clear_scene()
