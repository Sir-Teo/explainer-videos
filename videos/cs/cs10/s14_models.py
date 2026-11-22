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


class Models(WatchScene):
    def construct(self):
        self.card()
        self.pram()
        self.bsp()
        self.networks()

    def card(self):
        self.chapter(13, r"Models and networks", r"What is a parallel computer, \ abstractly?", lit=(1978, 1990, 1993), extra=((1978, r"the PRAM"), (1990, r"Valiant: \ BSP"),
                                                           (1993, r"LogP")), part=PART, said="Chapter thirteen. Models and networks.")

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
            (
            "Parallel-algorithm models make their assumptions explicit. <bookmark mark='a'/> A classical PRAM has "
            "p synchronous processors and ideal unit-time access to shared cells, without charging for caches or "
            "a network. Fortune and Wyllie's 1978 work is one early reference. <bookmark mark='b'/> EREW forbids "
            "concurrent reads and writes to one cell; CREW permits shared reads; CRCW also permits shared writes "
            "under a specified conflict rule. <bookmark mark='c'/> With n processors and common-value concurrent "
            "writes, initialize an answer to zero and let every one-bit write one: OR takes constant time. In the "
            "standard bounded-fan-in exclusive-write setting it requires logarithmic time. Processor count, word "
            "operations and write-conflict rules matter. PRAM is a useful abstraction, while real communication "
            "still has a cost."
        )
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(procs), FadeIn(pl), Create(links), FadeIn(mem), FadeIn(ml), run_time=0.6)
            vo.wait_until('a')
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
            (
            "In 1990 Leslie Valiant proposed a model that charges for communication, bulk-synchronous "
            "parallelism. <bookmark mark='a'/> A computation is a series of supersteps. In each, every processor "
            "computes on its own data, then sends messages, and then all wait at a barrier until every message "
            "has arrived. <bookmark mark='b'/> A superstep costs the largest local work, plus g times the largest "
            "number of words any processor sends or receives, plus the cost of the barrier. Two numbers, g and l, "
            "summarize the whole network. <bookmark mark='c'/> LogP, from David Culler and colleagues in 1993, "
            "prices each message individually: its latency, the processor's overhead to send it, and the gap "
            "between messages. <bookmark mark='d'/> Many clusters use MPI. Broadcast, reduce and all-reduce can "
            "implement bulk-synchronous phases, but MPI also supports point-to-point and asynchronous "
            "communication; it is not identical to BSP. The all-reduce is how AI, Built's Part 18 trains one "
            "model on many GPUs."
        )
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(g), FadeIn(labs), run_time=0.6)
            vo.wait_until('a')
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
        self.ask(r"1024 processors wired as a hypercube. \\ Hops between the farthest pair?", [r"10", r"32", r"1023"], 0,
                 say="A thousand and twenty-four processors, wired as a hypercube. How many hops between the farthest two?",
                 reveal="Ten: one hop for each bit of the address that differs.")
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
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(f) for f in figs], lag_ratio=0.4), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(FadeIn(fat))
        self.wait(0.3)
        self.clear_scene()


