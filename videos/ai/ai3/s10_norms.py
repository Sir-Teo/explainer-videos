from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, RANDOM, SIG, chapter, dots_on, ex, load

KINDS = {"attn": (C.QUERY, r"attention in ($768 \times 2304$)"), "attn_out": (C.VALUE, r"attention out ($768 \times 768$)"),
         "mlp_in": (C.MLP, r"MLP in ($768 \times 3072$)"), "mlp_out": (C.TRUE_P, r"MLP out ($3072 \times 768$)")}
F64, F32 = C.TRUE_P, C.MODEL_Q


class Norms(VoiceoverScene):
    def construct(self):
        chapter(self, 9, r"How big is a matrix?", r"Which size matters, and when does a matrix lose precision?",
                "Chapter nine. How big is a matrix?")
        self.two_sizes()
        self.gpt2()
        self.depth()
        self.condition()
        self.muon()

    # ------------------------------------------------------------------
    def two_sizes(self):
        defs = VGroup(
            definition_card(r"Frobenius norm", MathTex(r"\|A\|_F = \sqrt{\textstyle\sum_{ij} a_{ij}^2}", font_size=34),
                            width=5.2, color=C.TRUE_P),
            definition_card(r"spectral norm", MathTex(r"\|A\|_2 = \max_{\mathbf{x} \ne 0} \frac{|A\mathbf{x}|}{|\mathbf{x}|}"
                                                      r" = \sigma_1", font_size=34), width=5.2, color=SIG),
        ).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.3)
        rows = [
            cmath(r"\|A\|_F^2", "=", r"\operatorname{tr}(A^{\top}A)", font_size=36),
            cmath(r"\|A\|_F^2", "=", r"\textstyle\sum_i \lambda_i(A^{\top}A) = \sum_i \sigma_i^2", font_size=36),
            cmath(r"\sigma_1", r"\le", r"\|A\|_F \le \sqrt{r}\,\sigma_1", font_size=36),
            cmath(r"\text{stable rank}", "=", r"\|A\|_F^2 / \sigma_1^2 \ \in [1, r]", font_size=36),
        ]
        whys = [why(r"the diagonal of $A^{\top}A$: \ each column's squared length"),
                why(r"trace $=$ sum of eigenvalues \ (spectral theorem)"),
                why(r"one term $\le$ the sum $\le r$ copies of the largest"),
                why(r"how many directions carry the size")]
        step = ladder(self, rows, whys, keep=4, top=1.2, x=-1.4, buff=0.4, edge=6.9)
        with self.voiceover(
            "A matrix has two natural sizes. <bookmark mark='a'/> The Frobenius norm treats it as a long list of "
            "numbers: the square root of the sum of their squares. The spectral norm treats it as a map: the most "
            "it stretches any vector, the top singular value. <bookmark mark='b'/> They are related. The squared "
            "Frobenius norm is the trace of A transpose A, <bookmark mark='c'/> and the trace is the sum of the "
            "eigenvalues: the sum of the squared singular values. That was the missing step in chapter eight. "
            "<bookmark mark='d'/> So the spectral norm is at most the Frobenius norm, which is at most root r "
            "times it. <bookmark mark='e'/> Their squared ratio, the stable rank, counts how many directions carry "
            "a matrix's size: one, if a single direction dominates; r, if all are equal."
        ) as vo:
            self.play(FadeIn(defs[0], shift=DOWN * 0.2), FadeIn(defs[1], shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(Indicate(defs[0], scale_factor=1.03), Indicate(defs[1], scale_factor=1.03), run_time=1.5)
            for k, mk in enumerate("bcde"):
                vo.wait_until(mk)
                step(k)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gpt2(self):
        d = load("norms")
        rows = d["rows"]
        rnd = d["random"]
        top = 370
        g = axes([-0.5, 11.5, 1], [0, top, 100], x_length=7.4, y_length=4.4, xticks=list(range(0, 12)),
                 yticks=[0, 100, 200, 300], xlabel=r"layer", ylabel=r"stable rank $\|W\|_F^2/\sigma_1^2$",
                 center=[-2.0, -0.4, 0])
        ax = g.ax
        ref = DashedLine(ax.c2p(-0.5, rnd["stable"]), ax.c2p(11.5, rnd["stable"]), color=RANDOM, stroke_width=2)
        refl = label(rf"a random $768 \times 3072$ matrix: \ ${rnd['stable']:.0f}$", font_size=22, color=RANDOM)
        refl.next_to(ax.c2p(5.5, rnd["stable"]), UP, buff=0.08)
        lines, leg = VGroup(), VGroup()
        for kind, (col, name) in KINDS.items():
            r = [x for x in rows if x["kind"] == kind]
            xs = [x["layer"] for x in r]
            ys = [x["stable"] for x in r]
            lines.add(VGroup(curve(ax, xs, ys, col, 3), dots_on(ax, xs, ys, col, 0.05)))
            leg.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=col, stroke_width=5), label(name, font_size=22, color=col))
                    .arrange(RIGHT, buff=0.15))
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.6, 0.6, 0])
        allst = [x["stable"] for x in rows]
        lo, hi = min(allst), max(allst)
        full = 768
        cap = note(r"computed: \ all $48$ weight matrices in GPT-2 small's blocks").to_corner(DR, buff=0.25)
        verdict = ("every one of them far below a random matrix of the same shape" if hi < 0.5 * rnd["stable"]
                   else "some of them close to a random matrix")
        with self.voiceover(
            f"Here are the stable ranks of all 48 matrices in GPT-2's blocks. Each could have up to {full}. "
            f"<bookmark mark='a'/> A random matrix of the MLP's shape has a stable rank of {rnd['stable']:.0f}; "
            f"theory predicts {rnd['stable_pred']:.0f}. <bookmark mark='b'/> The trained ones run from {lo:.0f} to "
            f"{hi:.0f}: {verdict}. Training concentrates a matrix's size in a few directions. Chapter ten looks "
            "at those directions."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(ref), FadeIn(refl))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(Create(l_), FadeIn(lg)) for l_, lg in zip(lines, leg)],
                                  lag_ratio=0.4), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def depth(self):
        d = load("depth")
        L = int(d["layers"])
        gains = [float(x) for x in d["gains"]]
        lens = {gn: np.asarray(d[f"len{gn}"]) for gn in gains}
        ax = Axes(x_range=[0, L, 10], y_range=[-14, 12, 2], x_length=8.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to(DOWN * 0.5 + LEFT * 1.4)
        xl = VGroup(*[MathTex(str(v), font_size=24, color=GREY_B).next_to(ax.c2p(v, -14), DOWN, buff=0.12)
                      for v in range(0, L + 1, 10)])
        yl = VGroup(*[MathTex(t, font_size=24, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for t, v in (("2^{-12}", -12), ("2^{-6}", -6), ("1", 0), ("2^{6}", 6), ("2^{12}", 12))])
        xn = label(r"layer", font_size=26, color=GREY_A).next_to(ax, DOWN, buff=0.5)
        yn = label(r"the vector's length", font_size=26, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        cols = {gains[0]: C.PENALTY, gains[1]: WHITE, gains[2]: C.BITS}
        lines, tags = VGroup(), VGroup()
        for gain in gains:
            ys = np.log2(np.maximum(lens[gain], 1e-12))
            lines.add(ax.plot_line_graph(np.arange(L + 1), ys, add_vertex_dots=False, line_color=cols[gain], stroke_width=4))
            end = lens[gain][-1]
            txt = rf"\times {end:.4f}" if end < 0.01 else (rf"\times {end:.1f}" if end < 100 else rf"\times {end:,.0f}")
            tags.add(MathTex(rf"\text{{gain }} {gain:g}: \ " + txt.replace(",", "{,}"), font_size=28, color=cols[gain])
                     .next_to(ax.c2p(L, float(ys[-1])), RIGHT, buff=0.15))
        sub = MathTex(r"\|AB\| \le \|A\|\,\|B\|", font_size=36, color=SIG).to_corner(UR, buff=0.5)
        sub_w = why(r"stretch by $A$, then by $B$").next_to(sub, DOWN, buff=0.1)
        head = label(rf"A vector through ${L}$ layers of random matrices", font_size=34).to_edge(UP, buff=0.35)
        big, small = lens[gains[2]][-1], lens[gains[0]][-1]
        with self.voiceover(
            "Norms multiply through a network. <bookmark mark='a'/> Stretching by A and then by B stretches by at "
            f"most the product of the two. A deep network applies one matrix after another: push a vector through "
            f"{L} random layers. <bookmark mark='b'/> If each layer stretches a typical vector by {gains[2]:g}, the "
            f"length after {L} layers has grown {big:,.0f} times. <bookmark mark='c'/> At {gains[0]:g}, it shrinks to "
            f"{small:.5f}. Only near one does the signal survive. That knife edge is Part 9's subject."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(FadeIn(sub), FadeIn(sub_w))
            self.play(Create(lines[1]), FadeIn(tags[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(tags[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[0]), FadeIn(tags[0]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def condition(self):
        d = load("norms")
        sol = d["solve"]
        e64, e32 = float(d["eps64"]), float(d["eps32"])
        rows = [
            cmath(r"A(\mathbf{x} + \delta\mathbf{x})", "=", r"\mathbf{b} + \delta\mathbf{b}", font_size=32),
            cmath(r"|\delta\mathbf{x}|", r"\le", r"|\delta\mathbf{b}| \,/\, \sigma_n", font_size=32),
            cmath(r"|\mathbf{b}|", r"\le", r"\sigma_1\,|\mathbf{x}|", font_size=32),
            cmath(r"\frac{|\delta\mathbf{x}|}{|\mathbf{x}|}", r"\le", r"\kappa\,\frac{|\delta\mathbf{b}|}{|\mathbf{b}|}, "
                  r"\quad \kappa = \frac{\sigma_1}{\sigma_n}", font_size=32, colors={r"\kappa": SIG}),
        ]
        whys = [why(r"a small error in $\mathbf{b}$", font_size=22), why(r"$A^{-1}$ stretches by at most $1/\sigma_n$", font_size=22),
                why(r"$A$ stretches by at most $\sigma_1$", font_size=22), why(r"divide", font_size=22)]
        for r_, w_ in zip(rows, whys):
            r_.scale(0.95)
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-4.0, buff=0.3, edge=6.9)
        lk = [math.log10(s["kappa"]) for s in sol]
        g = axes([0, 14, 2], [-16, 2, 4], x_length=5.4, y_length=3.3, xticks=[0, 4, 8, 12],
                 yticks=[-16, -12, -8, -4, 0], xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}",
                 xlabel=r"condition number $\kappa$", ylabel=r"error in the computed $\mathbf{x}$", center=[3.6, -1.7, 0])
        ax = g.ax
        c64 = VGroup(curve(ax, lk, [math.log10(max(s["e64"], 1e-17)) for s in sol], F64, 3),
                     dots_on(ax, lk, [math.log10(max(s["e64"], 1e-17)) for s in sol], F64, 0.045))
        c32 = VGroup(curve(ax, lk, [min(2, math.log10(max(s["e32"], 1e-17))) for s in sol], F32, 3),
                     dots_on(ax, lk, [min(2, math.log10(max(s["e32"], 1e-17))) for s in sol], F32, 0.045))
        p64 = DashedLine(ax.c2p(0, math.log10(e64)), ax.c2p(14, math.log10(e64) + 14), color=F64, stroke_width=1.5)
        p32 = DashedLine(ax.c2p(0, math.log10(e32)), ax.c2p(-math.log10(e32) + 2, 2), color=F32, stroke_width=1.5)
        leg = legend([(F64, r"64-bit"), (F32, r"32-bit"), (GREY_B, r"dashed: \ $\kappa \times$ rounding unit")],
                     font_size=20).next_to(ax, LEFT, buff=0.4).shift(DOWN * 0.6)
        cap = note(r"computed: \ $60 \times 60$ systems, \ median of $5$").to_corner(DR, buff=0.2)
        s6 = next(s for s in sol if abs(math.log10(s["kappa"]) - 6) < 0.01)
        dead32 = next((s["kappa"] for s in sol if s["e32"] > 0.5), None)
        kmax = max(r["kappa"] for r in d["rows"])
        lost = (f" From a condition number of ten to the {ex(dead32)}, the 32-bit answer is no answer at all."
                if dead32 else "")
        with self.voiceover(
            "The ratio of the largest and smallest stretch is the condition number, and it says how much a matrix "
            "can amplify errors. <bookmark mark='a'/> Solve A x equals b with a small error in b. "
            "<bookmark mark='b'/> The error in x is at most the error in b over the smallest singular value, "
            "<bookmark mark='c'/> and b is at most the largest singular value times x. <bookmark mark='d'/> "
            "Divide: relative errors grow by at most kappa. <bookmark mark='e'/> Computers round every number, so "
            "the rounding unit plays the part of the error in b. At a condition number of a million, 64-bit "
            f"arithmetic loses about ten to the minus {-ex(s6['e64'])} of the answer; 32-bit loses ten to the "
            f"minus {-ex(s6['e32'])}.{lost} GPT-2's worst-conditioned matrix has kappa about ten to the "
            f"{ex(kmax)}: low precision is something to design around, as Part 18 does."
        ) as vo:
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
            vo.wait_until("e")
            self.play(FadeIn(g), FadeIn(cap), FadeIn(leg))
            self.play(Create(p64), Create(c64), run_time=1.5)
            self.play(Create(p32), Create(c32), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def muon(self):
        gl = load("galore")
        ns = [np.asarray(x) for x in gl["ns_sv"]]
        g0 = np.asarray(gl["g_sv"])
        rows = [
            cmath(r"\max_{\|\Delta\|_2 \le 1} \operatorname{tr}(G^{\top}\Delta)", "=",
                  r"\max \textstyle\sum_i \sigma_i\, (U^{\top}\Delta V)_{ii}", font_size=32),
            cmath(r"\max_{\|\Delta\|_2 \le 1} \operatorname{tr}(G^{\top}\Delta)", r"\le", r"\textstyle\sum_i \sigma_i",
                  r"\quad \text{at } \Delta = UV^{\top}", font_size=32),
        ]
        whys = [why(r"$G = U\Sigma V^{\top}$", font_size=22),
                why(r"$|(U^{\top}\Delta V)_{ii}| \le \|\Delta\|_2 \le 1$", font_size=22)]
        step = ladder(self, rows, whys, keep=2, top=3.2, x=-0.6, buff=0.4, edge=6.9)
        n = len(ns[0])
        g = axes([0, n, max(1, n // 4)], [0, 1.25, 0.5], x_length=5.6, y_length=3.0, yticks=[0, 0.5, 1.0],
                 xlabel=r"singular values, \ largest first", ylabel=r"$\sigma_i$, \ relative", center=[-3.0, -1.6, 0])
        ax = g.ax
        xs = np.arange(n) + 0.5
        tr = ValueTracker(0)
        first = curve(ax, xs, g0, GREY_B, 3)
        lab = label(r"a real gradient \ (chapter eleven's run)", font_size=22, color=GREY_B).next_to(ax.c2p(n * 0.5, 0.5),
                                                                                                   UP, buff=0.3)
        rd = always_redraw(lambda: label(rf"Newton--Schulz step ${int(round(tr.get_value()))}$ of ${len(ns) - 1}$",
                                         font_size=26, color=C.MUON).next_to(ax, UP, buff=0.5).align_to(ax, LEFT))
        hist = history_card(2024, r"K.~Jordan et al., \ Muon",
                            r"momentum, then orthogonalize: \ the update $UV^{\top}$, \ by five Newton--Schulz "
                            r"iterations; \ Moonshot's Kimi K2 (2025) was trained with it", color=HIST, width=5.4)
        hist.move_to([3.6, -1.6, 0])
        fin = ns[-1]
        spread = (float(fin.min()), float(fin.max()))
        with self.voiceover(
            "The spectral norm has become an optimizer. <bookmark mark='a'/> Ask which step of spectral size one "
            "changes the loss the most, along a gradient G. Write G with its SVD. <bookmark mark='b'/> Each "
            "diagonal entry is at most one, so the best is the sum of the singular values, reached by U V "
            "transpose: the gradient with every stretch set to one. <bookmark mark='c'/> That is Muon's update. "
            "Instead of an SVD it runs five Newton-Schulz iterations, a few matrix products that push every "
            "singular value towards one. On a real gradient, they start spread out, <bookmark mark='d'/> and after "
            f"five steps they lie between {spread[0]:.2f} and {spread[1]:.2f}. Part 11 builds the optimizer."
        ) as vo:
            self.play(FadeIn(hist, shift=UP * 0.2))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(g), Create(first), FadeIn(lab))
            self.add(rd)
            cur = first
            vo.wait_until("d")
            for k in range(1, len(ns)):
                nxt = curve(ax, xs, ns[k], C.MUON, 3)
                self.play(Transform(cur, nxt), tr.animate.set_value(k), FadeOut(lab) if k == 1 else Wait(0.01),
                          run_time=0.8)
        rd.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
