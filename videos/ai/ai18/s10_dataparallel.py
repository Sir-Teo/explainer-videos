from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (ACTS, COMM, F, GPU, GRADS, KEPT, N_COL, PART, ShardGrid, load, node_box, play_fly,
                                   spoken_int, take_away)

CHUNK = [C.EMBED, C.MOMENTUM, C.PROB, C.MLP]


class DataParallel(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.allreduce()
        self.bound()
        self.timed()

    def card(self):
        card = chapter_card(9, r"Data parallelism and the all-reduce", r"Many copies of one model: how fast can they "
                            r"agree?", lit=(1994,), part=PART)
        with self.voiceover("Chapter nine. Data parallelism and the all-reduce."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        Pr = load("parallel")
        p = Pr["p"]
        gpus = VGroup()
        for r in range(p):
            box = RoundedRectangle(width=2.6, height=1.7, corner_radius=0.12, stroke_color=GPU, stroke_width=2)
            model = VGroup(*[Rectangle(width=1.4, height=0.18, stroke_width=0, fill_color=N_COL, fill_opacity=0.8)
                             for _ in range(4)]).arrange(DOWN, buff=0.06)
            data = VGroup(*[Square(0.16, stroke_width=0, fill_color=ACTS, fill_opacity=0.8) for _ in range(4)])
            data.arrange(RIGHT, buff=0.05)
            inner = VGroup(model, data).arrange(DOWN, buff=0.18)
            nm = label(rf"GPU {r}", font_size=20, color=GPU)
            g = VGroup(box, inner.move_to(box), nm.next_to(box, UP, buff=0.08))
            gpus.add(g)
        gpus.arrange(RIGHT, buff=0.45).move_to(UP * 1.2)
        lab = VGroup(label(r"the whole model on every GPU", font_size=22, color=N_COL),
                     label(rf"a quarter of the batch each", font_size=22, color=ACTS)).arrange(RIGHT, buff=1.2)
        lab.next_to(gpus, DOWN, buff=0.3)
        ar = node_box(r"all-reduce: \ every GPU gets the average gradient", COMM, font_size=24).move_to(DOWN * 2.3)
        grads = VGroup(*[Arrow(g.get_bottom() + DOWN * 0.7, [ar.get_left()[0] + ar.width * (i + 0.5) / p,
                                                             ar.get_top()[1] + 0.05, 0],
                               buff=0.1, color=GRADS, stroke_width=3, max_tip_length_to_length_ratio=0.12)
                         for i, g in enumerate(gpus)])
        L = Pr["losses"]
        dl = max(abs(a - b) / abs(a) for a, b in zip(L["ref"], L["dp"]))
        digits = int(math.floor(-math.log10(max(dl, 1e-12))))
        meas = label(rf"checked here: \ ${p}$ processes against one, \ ${Pr['steps']}$ steps: \ parameters equal to "
                     rf"${sci(Pr['err']['dp'], 0)}$".replace("{-}", "-"), font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        # the check's own training: the loss at each step, one process (line) and four (dots)
        ls = np.asarray(L["ref"]), np.asarray(L["dp"])
        k = np.arange(1, len(ls[0]) + 1)
        llo, lhi = math.floor(min(ls[0].min(), ls[1].min()) * 10) / 10, math.ceil(max(ls[0].max(), ls[1].max()) * 10) / 10
        gl = axes([1, len(k)], [llo, lhi], x_length=2.3, y_length=1.5, xlabel=r"step", ylabel=r"loss",
                  xticks=[1, len(k)], yticks=[llo, lhi], yfmt=lambda v: f"{v:.1f}", center=[5.5, -1.75, 0], font_size=15)
        mini = VGroup(gl, curve(gl.ax, k, ls[0], GREY_B, 2.5),
                      *[Dot(gl.ax.c2p(a, b), radius=0.05, color=COMM) for a, b in zip(k, ls[1])],
                      note(r"line: \ one process; \ dots: \ four", font_size=15).next_to(gl, DOWN, buff=0.05))
        with self.voiceover(
            "The simplest way to use many GPUs: give each one a full copy of the model and a slice of the batch. "
            "<bookmark mark='a'/> Each computes the gradient of its slice. <bookmark mark='b'/> Then they average "
            "the gradients, so that every copy takes exactly the same step, and they stay identical. The averaging "
            "is an all-reduce, the operation of Part 17. <bookmark mark='c'/> It is the same step as one big batch on "
            f"one device. We checked: {p} processes of this computer, each with a quarter of the batch, against one "
            f"process with all of it, for {Pr['steps']} steps of AdamW: the losses agree to {digits} digits, and every "
            f"parameter to within {Pr['err']['dp']:.5f}; only the order of the additions differs."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in gpus], lag_ratio=0.2), FadeIn(lab[0]))
            vo.wait_until("a")
            self.play(FadeIn(lab[1]), *[Indicate(g[1][1], color=ACTS) for g in gpus])
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in grads], lag_ratio=0.15), FadeIn(ar))
            vo.wait_until("c")
            self.play(FadeIn(meas, shift=UP * 0.1), FadeIn(mini[0]), FadeIn(mini[-1]), Create(mini[1]))
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in mini[2:-1]], lag_ratio=0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def allreduce(self):
        p = 4
        grid = ShardGrid(p, p, cell=0.82, row_gap=0.34).move_to([-2.4, -0.45, 0])
        for r in range(p):
            for c in range(p):
                grid.set(r, c, CHUNK[c], 0.25)
        cols = grid.label_cols([rf"chunk {c + 1}" for c in range(p)])
        title = label(r"each GPU's gradient, \ cut into $p$ chunks", font_size=24, color=GRADS).to_edge(UP, buff=0.4)
        step_l = label(r"reduce-scatter", font_size=26, color=COMM).move_to([3.6, 1.6, 0])
        step_r = label(r"all-gather", font_size=26, color=COMM).move_to([3.6, 1.6, 0])
        eq = VGroup(cmath(r"\text{all-reduce}", r"=", r"\text{reduce-scatter}", r"+", r"\text{all-gather}",
                          font_size=28),
                    label(r"each GPU sends $2\,\frac{p-1}{p}\,n$ bytes", font_size=24, color=COMM)).arrange(DOWN, buff=0.25)
        eq.move_to([3.6, -1.4, 0])
        cnt = Integer(0, font_size=28, color=COMM)
        cl = VGroup(label(r"steps:", font_size=22, color=GREY_A), cnt).arrange(RIGHT, buff=0.15).move_to([3.6, 0.8, 0])
        sch = note(r"schematic: \ the ring of Part 17, \ chunk by chunk", font_size=18).to_corner(DR, buff=0.2)
        with self.voiceover(
            "Recall the ring of Part 17. Cut each GPU's gradient into p chunks. <bookmark mark='a'/> At each step every "
            "GPU passes one chunk to its neighbour, which adds it to its own; after p minus one steps each GPU holds the "
            "full sum of one chunk: a reduce-scatter. <bookmark mark='b'/> Then p minus one more steps pass the finished "
            "chunks around: an all-gather. <bookmark mark='c'/> Each GPU sends two times p minus one over p of the "
            "gradient's bytes. ZeRO, next, does useful work between the two halves."
        ) as vo:
            self.play(FadeIn(title), FadeIn(grid), FadeIn(cols), FadeIn(sch), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(step_l))
            for s in range(p - 1):
                moves = [(r, (r - s) % p, (r + 1) % p, (r - s) % p) for r in range(p)]
                play_fly(self, grid, moves, run_time=0.7, opacity_after=0.25 + 0.75 * (s + 2) / p)
                self.play(cnt.animate.set_value(s + 1), run_time=0.2)
            vo.wait_until("b")
            self.play(ReplacementTransform(step_l, step_r))
            for s in range(p - 1):
                moves = [(r, (r + 1 - s) % p, (r + 1) % p, (r + 1 - s) % p) for r in range(p)]
                play_fly(self, grid, moves, run_time=0.7, opacity_after=1.0)
                self.play(cnt.animate.set_value(p + s), run_time=0.2)
            vo.wait_until("c")
            self.play(FadeIn(eq, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bound(self):
        th = theorem_card(r"The ring is bandwidth-optimal", r"Any all-reduce of $n$ numbers over $p$ devices, each "
                          r"receiving at most $B$ per second, takes at least $2\,\frac{p-1}{p}\,\frac{n}{B}$.",
                          who=r"Patarasuk \& Yuan (2009)", color=COMM, width=8.6, font_size=22).to_edge(UP, buff=0.35)
        rows = [
            cmath(r"\text{first GPU to hold one number's sum}", r":", r"\ge p-1 \text{ messages in}", font_size=26),
            cmath(r"\text{then each of the other } p-1", r":", r"\ge 1 \text{ message more}", font_size=26),
            cmath(r"\text{all } n \text{ numbers}", r":", r"\ge 2(p-1)\,n \text{ numbers sent}", font_size=26),
            cmath(r"T", r"\ge", r"\frac{2(p-1)\,n}{p\,B}", r"=", r"2\,\frac{p-1}{p}\,\frac{n}{B}", font_size=32),
        ]
        whys = [why(r"every other GPU's value must reach it", font_size=19),
                why(r"before that moment, nobody had the sum", font_size=19),
                why(r"the same for every number", font_size=19),
                why(r"$p$ GPUs receive at once, \ $B$ each", font_size=19)]
        step = ladder(self, rows, whys, keep=4, top=1.35, x=-0.8, buff=0.36, edge=6.9)
        # one number on four GPUs: a chain of messages into the first to hold the sum, then one more to each other
        nodes = VGroup(*[VGroup(Circle(0.3, color=GPU, stroke_width=2.5, fill_color=GPU, fill_opacity=0.12),
                                MathTex(rf"v_{i}", font_size=26, color=WHITE)) for i in range(4)])
        nodes.arrange(RIGHT, buff=1.5).move_to([0.6, -2.95, 0])
        chain_ = VGroup(*[CurvedArrow(nodes[i][0].get_top() + UP * 0.02, nodes[i + 1][0].get_top() + UP * 0.02,
                                      angle=-PI / 3, color=COMM, stroke_width=3, tip_length=0.14) for i in range(3)])
        back_ = VGroup(*[CurvedArrow(nodes[3][0].get_bottom() + DOWN * 0.02, nodes[i][0].get_bottom() + DOWN * 0.02,
                                     angle=-PI / 5, color=KEPT, stroke_width=2.5, tip_length=0.14) for i in range(3)])
        sums = VGroup(*[MathTex(r"\Sigma", font_size=26, color=COMM).move_to(n_[0]) for n_ in nodes])
        nnote = note(r"one number on four GPUs \ (schematic)", font_size=17).next_to(nodes, LEFT, buff=0.5)
        tw = take_away(r"no algorithm sends less than the ring: \ only latency and overlap are left to win", color=COMM,
                       font_size=24)
        with self.voiceover(
            "Part 17 said that no algorithm beats the ring on bandwidth. Here is why. Follow a single number, whose "
            "sum all p GPUs must end up holding. Each message carries one value, perhaps a partial sum. "
            "<bookmark mark='a'/> Some GPU is the first to hold the full sum. Every other GPU's value must have "
            "reached it, through a chain of messages: that takes at least p minus one messages. "
            "<bookmark mark='b'/> At that moment, nobody else has the sum, so each of the other p minus one GPUs "
            "needs at least one more message. <bookmark mark='c'/> Two times p minus one messages per number, for "
            "all n numbers. <bookmark mark='d'/> The p GPUs can receive at the same time, B bytes per second each, "
            "so the time is at least two times p minus one, over p, times n over B: exactly the ring's. "
            "<bookmark mark='e'/> The ring is optimal in bandwidth. What's left to win is latency, with trees for "
            "small messages, and overlap: sending the gradients of the last layers while the backward pass is still "
            "computing the first."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.1))
            self.play(LaggedStart(*[FadeIn(n_, scale=0.8) for n_ in nodes], lag_ratio=0.2), FadeIn(nnote))
            vo.wait_until("a")
            step(0)
            self.play(LaggedStart(*[Create(a_) for a_ in chain_], lag_ratio=0.6), run_time=2.5)
            self.play(ReplacementTransform(nodes[3][1], sums[3]))
            vo.wait_until("b")
            step(1)
            self.play(LaggedStart(*[Create(a_) for a_ in back_], lag_ratio=0.3), run_time=1.8)
            self.play(*[ReplacementTransform(nodes[i][1], sums[i]) for i in range(3)])
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeOut(VGroup(nodes, chain_, back_, sums, nnote)))
            self.play(FadeIn(tw, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def timed(self):
        Cc = load("collectives")
        ns = np.asarray(Cc["bytes"], float)
        g = axes([3, 8], [-4, 0], x_length=6.4, y_length=4.2, xlabel=r"message size (bytes)",
                 ylabel=r"time (seconds)", xticks=[3, 4, 5, 6, 7, 8], yticks=[-4, -3, -2, -1, 0],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.6, -0.4, 0],
                 font_size=18)
        cols = {"all_reduce": COMM, "reduce_scatter": C.PROB, "all_gather": C.EMBED}
        names = {"all_reduce": r"all-reduce", "reduce_scatter": r"reduce-scatter", "all_gather": r"all-gather"}
        meas, pred = VGroup(), VGroup()
        for k in ("all_reduce", "reduce_scatter", "all_gather"):
            m_ = np.asarray(Cc[f"m_{k}"])
            pr = np.asarray(Cc[f"p_{k}"])
            meas.add(VGroup(*[Dot(g.ax.c2p(math.log10(n), math.log10(t)), radius=0.05, color=cols[k])
                              for n, t in zip(ns, m_)]))
            pred.add(DashedVMobject(curve(g.ax, np.log10(ns), np.log10(pr), cols[k], 2.5), num_dashes=30))
        lg = VGroup(legend([(cols[k], names[k]) for k in cols], font_size=18),
                    label(r"dots: \ measured; \ dashes: \ the $\alpha$--$\beta$ model", font_size=18, color=GREY_A))
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(g, RIGHT, buff=0.3).shift(UP * 0.8)
        fit = label(rf"from point-to-point messages: \ $\alpha = {Cc['alpha'] * 1e6:.0f}\,\mu$s, \ "
                    rf"$B = {Cc['B'] / 1e9:.1f}$ GB/s", font_size=20, color=GREY_A).next_to(lg, DOWN, buff=0.3)
        fit.align_to(lg, LEFT)
        r = Cc["ratio"]
        worst = max(r.values())
        if worst < 2:
            verdict = ("Beyond a few hundred kilobytes, every measured time is within a factor of two of the model's "
                       "prediction.")
        else:
            verdict = (f"Large messages took {min(r.values()):.0f} to {worst:.0f} times the model's prediction, on a "
                       "computer whose four cores were shared with other jobs: the model describes devices with a link "
                       "each and nothing else to do. But the shape holds: a floor of latency for small messages, then "
                       "time growing in proportion to the bytes.")
        tag = note(rf"computed: \ ${Cc['p']}$ processes, \ PyTorch's gloo backend; \ sums checked", font_size=18)
        tag.to_corner(DR, buff=0.2)
        with self.voiceover(
            "We timed the three operations with PyTorch's own distributed library, on four processes of this "
            "computer, for messages from a kilobyte to 32 megabytes. <bookmark mark='a'/> The dashed lines are the "
            "alpha-beta model of Part 17, with the latency and bandwidth fitted to point-to-point messages: one latency "
            "for each step of the ring, and the ring's bytes. <bookmark mark='b'/> " + verdict
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(*[Create(p_) for p_ in pred], FadeIn(lg[1]), FadeIn(fit), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_, lag_ratio=0.1) for m_ in meas], lag_ratio=0.3), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()
