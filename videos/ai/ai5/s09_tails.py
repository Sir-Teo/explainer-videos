from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, PART, curve, hist_shape, load

BOUNDS = {"markov": GREY_B, "cheb": C.INTERVAL, "chern": C.BITS, "hoeff": C.MODEL_Q}
NAMES = {"markov": r"Markov", "cheb": r"Chebyshev", "chern": r"Chernoff", "hoeff": r"Hoeffding"}
TAIL = C.SURPRISE


class Tails(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.derive()
        self.compare()
        self.sizes()

    def card(self):
        card = chapter_card(7, r"How far from the average?", r"How often can an average be badly wrong?",
                            lit=(1963,), part=PART)
        with self.voiceover("Chapter seven. How far from the average?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def setup_(self):
        d = load("tails")
        n = int(d["n"])
        h = np.asarray(d["hist"], float)
        ax = Axes(x_range=[0.25, 0.75, 0.05], y_range=[0, 0.09, 0.02], x_length=10.0, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([0, -0.6, 0])
        xt = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                      for v in (0.3, 0.4, 0.5, 0.6, 0.7)])
        xl = label(rf"the share of heads in ${n}$ fair flips", font_size=24, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        p = h / h.sum()
        bars = VGroup()
        tail = VGroup()
        j10 = int(d["j10"])
        eps = float(np.asarray(d["eps"])[j10])
        for k, v in enumerate(p):
            x = k / n
            if 0.25 <= x <= 0.75 and v > 0:
                r = Rectangle(width=0.9 * ax.x_length / 50, height=ax.y_length * v / 0.09, stroke_width=0,
                              fill_color=TAIL if x >= 0.5 + eps - 1e-9 else DATA, fill_opacity=0.75)
                r.move_to(ax.c2p(x, v / 2))
                (tail if x >= 0.5 + eps - 1e-9 else bars).add(r)
        ex = float(np.asarray(d["exact"])[j10])
        eps_l = DashedLine(ax.c2p(0.5 + eps, 0), ax.c2p(0.5 + eps, 0.085), color=TAIL, stroke_width=2.5)
        tl = label(rf"$\bar X - \tfrac12 \ge {eps:g}$: \ probability ${ex:.4f}$", font_size=26, color=TAIL)
        tl.next_to(eps_l.get_end(), RIGHT, buff=0.15)
        head = label(r"$1{,}000{,}000$ runs of $100$ flips", font_size=30).to_edge(UP, buff=0.4)
        q = label(r"a bound that needs no picture: \ only that each flip lies in $[0, 1]$", font_size=26, color=C.BITS)
        q.to_edge(UP, buff=1.0)
        with self.voiceover(
            "The law of large numbers says an average settles. Learning from data needs more: how often is it still "
            "far off? A million runs of a hundred fair flips. <bookmark mark='a'/> The share of heads reaches "
            f"{0.5 + eps:g} in a fraction {ex:.3f} of them. <bookmark mark='b'/> Here we can count, but a model's test "
            "data never shows us this picture. We need a guarantee that holds whatever the distribution, knowing only "
            "that each value lies between zero and one."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in tail], lag_ratio=0.05), Create(eps_l), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"P(X \ge a)", r"\le", r"\frac{\mathbb{E}[X]}{a}", font_size=34),
            cmath(r"P(|\bar X - \mu| \ge \varepsilon)", r"\le", r"\frac{\operatorname{Var}(\bar X)}{\varepsilon^2} = "
                  r"\frac{\sigma^2}{n\varepsilon^2}", font_size=34),
            cmath(r"P(\bar X - \mu \ge \varepsilon)", r"\le", r"e^{-tn\varepsilon}\, \mathbb{E}\big[e^{t(X - \mu)}\big]^n",
                  font_size=34),
            cmath(r"\mathbb{E}\big[e^{t(X - \mu)}\big]", r"\le", r"e^{t^2/8}", font_size=34),
            cmath(r"P(\bar X - \mu \ge \varepsilon)", r"\le", r"e^{-2n\varepsilon^2}", font_size=36,
                  colors={r"e^{-2n\varepsilon^2}": BOUNDS["hoeff"]}),
        ]
        whys = [why(r"Markov: \ $a\,\mathbf{1}[X \ge a] \le X$ \ for $X \ge 0$"),
                why(r"Chebyshev: \ Markov on $(\bar X - \mu)^2$"),
                why(r"Chernoff: \ Markov on $e^{tn\bar X}$; \ independence"),
                why(r"Hoeffding's lemma: \ $X$ in $[0, 1]$"),
                why(r"choose $t = 4\varepsilon$")]
        step = ladder(self, rows, whys, keep=5, top=3.25, x=-1.4, buff=0.42, edge=6.8)
        cite_ = cite(r"I.-J.~Bienaym\'e (1853), \ P.~Chebyshev (1867), \ H.~Chernoff (1952), \ W.~Hoeffding (1963)",
                     corner=DR)
        with self.voiceover(
            "Each bound comes from the one before. <bookmark mark='a'/> Markov's: a quantity that is never negative "
            "can't often be much bigger than its average. <bookmark mark='b'/> Apply it to the squared distance from "
            "the mean: Chebyshev's, the variance over epsilon squared, and an average of n has n times less variance. "
            "<bookmark mark='c'/> Chernoff's idea: apply Markov to e to the t times the sum; independence splits it "
            "into a product, and the tail falls exponentially in n. <bookmark mark='d'/> For values between zero and "
            "one, Hoeffding's lemma bounds each factor, <bookmark mark='e'/> and the best t gives e to the minus two "
            "n epsilon squared: Hoeffding's inequality, from 1963."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("tails")
        eps = np.asarray(d["eps"])
        ex, sim = np.asarray(d["exact"]), np.asarray(d["sim"])
        ax = Axes(x_range=[0, 0.3, 0.05], y_range=[-8, 0, 2], x_length=8.0, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -0.4, 0])
        xt = VGroup(*[MathTex(f"{v:g}", font_size=22, color=GREY_B).next_to(ax.c2p(v, -8), DOWN, buff=0.12)
                      for v in (0.1, 0.2, 0.3)])
        yt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for t, v in (("1", 0), ("10^{-4}", -4), ("10^{-8}", -8))])
        xl = label(r"$\varepsilon$", font_size=28, color=GREY_A).next_to(ax.c2p(0.3, -8), DOWN, buff=0.45)
        yl = label(r"$P(\bar X - \tfrac12 \ge \varepsilon)$, \ $n = 100$", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        m = ex > 0
        truth = curve(ax, eps[m], np.log10(ex[m]), color=WHITE, stroke_width=4)
        sm = sim > 0
        sdots = VGroup(*[Dot(ax.c2p(a, math.log10(b)), radius=0.05, color=TAIL) for a, b in zip(eps[sm], sim[sm])])
        lines, labs = {}, VGroup()
        for k in ("markov", "cheb", "chern", "hoeff"):
            v = np.log10(np.minimum(np.asarray(d[k]), 1.0))
            lines[k] = curve(ax, eps, np.maximum(v, -8), color=BOUNDS[k], stroke_width=3)
        leg = VGroup(label(r"exact", font_size=22, color=WHITE), label(r"simulated, $10^6$ runs", font_size=22, color=TAIL),
                     *[label(NAMES[k], font_size=22, color=BOUNDS[k]) for k in ("markov", "cheb", "chern", "hoeff")])
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, RIGHT, buff=0.3).align_to(ax, UP)
        j = int(d["j10"])
        vals = {k: float(np.asarray(d[k])[j]) for k in ("markov", "cheb", "chern", "hoeff")}
        tbl = VGroup(*[label(rf"{NAMES[k]}: \ ${vals[k]:.3f}$", font_size=22, color=BOUNDS[k]) for k in vals],
                     label(rf"exact: \ ${ex[j]:.4f}$", font_size=22, color=WHITE))
        tbl.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        tt = label(rf"at $\varepsilon = {eps[j]:g}$", font_size=22, color=GREY_A).next_to(tbl, UP, buff=0.1).align_to(tbl, LEFT)
        ratio = vals["hoeff"] / ex[j]
        order_ok = vals["markov"] > vals["cheb"] > vals["hoeff"] >= vals["chern"] > ex[j]
        verdict = ("Each bound is tighter than the one before, and all of them are loose." if order_ok else
                   "Each bound holds here, but all of them loosely.")
        with self.voiceover(
            "Now put them against the truth, on a log scale. The exact tail, and a million simulated runs on top of "
            f"it. <bookmark mark='a'/> Markov's bound hardly falls at all; at epsilon of {eps[j]:g} it allows "
            f"{vals['markov']:.2f}. <bookmark mark='b'/> Chebyshev's falls like one over epsilon squared: "
            f"{vals['cheb']:.2f}. <bookmark mark='c'/> Chernoff's and Hoeffding's fall exponentially, and nearly "
            f"coincide here: {vals['chern']:.3f} and {vals['hoeff']:.3f}. {verdict} Hoeffding's is still "
            f"{ratio:.0f} times the true {ex[j]:.3f}: the price of knowing nothing about the shape."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(leg[:2]))
            self.play(Create(truth), LaggedStart(*[FadeIn(x) for x in sdots], lag_ratio=0.05), run_time=1.5)
            self.play(FadeIn(tt))
            vo.wait_until("a")
            self.play(Create(lines["markov"]), FadeIn(leg[2]), FadeIn(tbl[0]))
            vo.wait_until("b")
            self.play(Create(lines["cheb"]), FadeIn(leg[3]), FadeIn(tbl[1]))
            vo.wait_until("c")
            self.play(Create(lines["chern"]), Create(lines["hoeff"]), FadeIn(leg[4:]), FadeIn(tbl[2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sizes(self):
        d = load("tails")
        need = dict(d["need"])
        e0, d0 = float(d["e0"]), float(d["d0"])
        keys = [("cheb", "chebyshev"), ("hoeff", "hoeffding"), ("chern", "chernoff")]
        head = label(rf"How many flips guarantee $P(\bar X - \tfrac12 \ge {e0:g}) \le {d0:g}$?", font_size=34)
        head.to_edge(UP, buff=0.45)
        vals = [need[k2] for _, k2 in keys] + [need["exact"]]
        cols = [BOUNDS[k] for k, _ in keys] + [WHITE]
        names = [NAMES[k] for k, _ in keys] + [r"exact, \ for fair coins"]
        top = max(vals)
        rows = VGroup()
        for v, c_, nm in zip(vals, cols, names):
            bar = Rectangle(width=7.0 * v / top, height=0.5, stroke_width=0, fill_color=c_, fill_opacity=0.85)
            t = label(nm, font_size=26, color=c_)
            num = MathTex(f"{v:,}".replace(",", "{,}"), font_size=32, color=c_)
            rows.add(VGroup(t, bar, num))
        for i, r in enumerate(rows):
            r[0].move_to([-4.2, 1.4 - 0.85 * i, 0], aligned_edge=RIGHT)
            r[1].move_to([-3.9, 1.4 - 0.85 * i, 0], aligned_edge=LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        best = min(need["hoeffding"], need["chernoff"])
        uses = VGroup(label(r"Part 8: \ how far a model's test score can be from its true error", font_size=24, color=GREY_A),
                      label(r"Part 26: \ the bonus in UCB, \ exploring a slot machine", font_size=24, color=GREY_A))
        uses.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            f"Turn it around. How many flips guarantee that the share overshoots by {e0:g} at most {100 * d0:g} "
            f"percent of the time? <bookmark mark='a'/> Chebyshev's bound asks for {need['chebyshev']:,}; Hoeffding's, "
            f"{need['hoeffding']:,}; Chernoff's, {need['chernoff']:,}. <bookmark mark='b'/> For fair coins the truth "
            f"is {need['exact']}: the best bound asks for {best / need['exact']:.1f} times as many, the price of "
            "holding for every distribution. <bookmark mark='c'/> Part eight uses exactly this to bound a model's "
            "true error from its test score, and part twenty-six used Hoeffding's bound to explore."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for r in rows[:3]:
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(rows[3][0]), GrowFromEdge(rows[3][1], LEFT), FadeIn(rows[3][2]))
            vo.wait_until("c")
            self.play(FadeIn(uses))
        self.wait(0.3)
        self.clear_scene()
