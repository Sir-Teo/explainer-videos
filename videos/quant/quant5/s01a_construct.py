from __future__ import annotations

import numpy as np
from scipy.stats import norm

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause


class Construct(VoiceoverScene):
    def construct(self):
        c = load("construct")
        r = load("reflection")
        self.card()
        self.donsker(c)
        self.levy(c)
        self.reflection(r)
        self.arcsine(r)

    def card(self):
        cc = chapter_card(1, r"Building Brownian motion", r"Does such a path exist, and what does it do first?",
                          lit=(1923,), part=PART)
        with self.voiceover("Chapter one. Building Brownian motion."):
            self.play(FadeIn(cc[0], shift=UP * 0.2), FadeIn(cc[1]))
        self.play(FadeOut(cc))

    def donsker(self, c):
        laws = [("coin", r"coin: $\pm 1$", BM), ("uniform", r"uniform on $\pm\sqrt{3}$", ITO),
                ("skewed", r"skewed: $+2$ or $-\tfrac12$", STRAT)]
        panels, lines = VGroup(), []
        for key, name, col in laws:
            g = axes([0, 1], [-2.2, 2.2], x_length=3.9, y_length=2.6, xticks=[0, 1], yticks=[-2, 0, 2], font_size=16)
            t = label(name, font_size=20, color=col).next_to(g, UP, buff=0.1)
            panels.add(VGroup(g, t))
            ls = []
            for n in ("16", "128", "4096"):
                y = np.asarray(c["laws"][key][n])
                ls.append(curve(g.ax, np.linspace(0, 1, len(y)), np.clip(y, -2.2, 2.2), col,
                                stroke_width=2.5 if n != "4096" else 1.4))
            lines.append(ls)
        panels.arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.5)
        nlab = VGroup(*[MathTex(rf"n = {n}", font_size=30, color=GREY_A) for n in ("16", "128", "4{,}096")])
        for m in nlab:
            m.next_to(panels, UP, buff=0.5)
        defn = definition_card(r"Brownian motion", r"$W_0 = 0$; increments $W_t - W_s$ independent of the past and "
                               r"$N(0, t - s)$; paths continuous.", color=BM, width=6.6, font_size=22).to_corner(UL,
                                                                                                         buff=0.3)
        rule = MathTex(r"\frac{S_{\lfloor nt \rfloor}}{\sqrt n} \;\Rightarrow\; W_t", font_size=36).to_corner(UR, buff=0.5)
        with self.voiceover(
            "The gentle introduction drew Brownian motion. This chapter builds it, two ways, and proves the first "
            "thing it does. Here is the definition: it starts at zero, its increments are independent of the past and "
            "Gaussian with variance equal to the elapsed time, and its paths are continuous. Does such a thing exist? "
            "<bookmark mark='a'/> The first construction is a limit. Take a random walk with steps of mean zero and "
            "variance one, shrink time by n and space by the square root of n. Three walks, built from the same "
            "random numbers: a coin, a uniform step, and a lopsided step that is usually a small loss and "
            "occasionally a large gain. <bookmark mark='b'/> At sixteen steps they look different. At a hundred and "
            "twenty-eight, less so. <bookmark mark='c'/> At four thousand they are the same kind of scrawl. Donsker "
            "proved in 1951 that the limit is always the same Brownian motion: only the mean and the variance of "
            "the steps survive."
        ) as vo:
            self.play(FadeIn(defn, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(panels), FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(nlab[0]), *[Create(ls[0]) for ls in lines], run_time=1.5)
            self.play(FadeTransform(nlab[0], nlab[1]), *[ReplacementTransform(ls[0], ls[1]) for ls in lines], run_time=1.5)
            vo.wait_until("c")
            self.play(FadeTransform(nlab[1], nlab[2]), *[ReplacementTransform(ls[1], ls[2]) for ls in lines], run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def levy(self, c):
        lv = [np.asarray(x) for x in c["levels"]]
        lo, hi = min(x.min() for x in lv) - 0.2, max(x.max() for x in lv) + 0.2
        g = axes([0, 1], [lo, hi], x_length=7.4, y_length=4.2, xlabel=r"time", ylabel=r"$W_t$", xticks=[0, 0.5, 1],
                 yticks=[], font_size=18).to_edge(LEFT, buff=0.5).shift(DOWN * 0.4)
        ax = g.ax
        paths = [VMobject(stroke_width=3 if k < 6 else 2, stroke_color=BM).set_points_as_corners(
            [ax.c2p(t, y) for t, y in zip(np.linspace(0, 1, len(x)), x)]) for k, x in enumerate(lv)]
        dots = [VGroup(*[Dot(ax.c2p(t, y), radius=0.05, color=ITO) for t, y in
                         zip(np.linspace(0, 1, len(x))[1::2], x[1::2])]) for x in lv[1:6]]
        rows = [cmath(r"W_{\frac{s+t}{2}} \mid W_s, W_t", r"\sim", r"N\!\Big(\tfrac{W_s + W_t}{2},\ \tfrac{t - s}{4}\Big)",
                      font_size=32, colors={r"N\!\Big(\tfrac{W_s + W_t}{2},\ \tfrac{t - s}{4}\Big)": ITO})]
        side = VGroup(rows[0],
                      wrapped_label(r"the Brownian bridge: given the two ends, the midpoint is their average plus "
                                    r"independent Gaussian noise, a quarter of the gap's length in variance", 5.2, 20,
                                    GREY_A),
                      MathTex(rf"\text{{measured over 20{{,}}000 draws: }} {c['bridge_var']:.3f} \text{{ (theory }} 0.250)",
                              font_size=26, color=ITO),
                      wrapped_label(r"L\'evy (1948); the limit is continuous by Kolmogorov--Chentsov, since "
                                    r"$\mathbb{E}|W_t - W_s|^4 = 3|t - s|^2$", 5.2, 19, GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        lvl = VGroup(*[MathTex(rf"\text{{level }} {k}:\ {2 ** k + 1}\text{{ points}}", font_size=26, color=GREY_A)
                       .next_to(g, UP, buff=0.1).align_to(g, RIGHT) for k in range(11)])
        with self.voiceover(
            "The second construction is Paul Lévy's, and it builds the path directly, coarse to fine. Draw the endpoint "
            "at time one: a single Gaussian. Join it to the origin with a straight chord. <bookmark mark='a'/> Now "
            "fill in the midpoint. Given the two ends, the midpoint of a Brownian path is Gaussian, centred on the "
            "chord, with a variance of a quarter of the interval's length. That is the Brownian bridge. "
            "<bookmark mark='b'/> Displace every midpoint, then every quarter point, then every eighth, each level "
            "with half the variance of the last. The path crystallises. <bookmark mark='c'/> The sum converges "
            "uniformly, so the limit is a continuous path with exactly the right increments. Our twenty thousand "
            f"draws put the midpoint variance at {c['bridge_var']:.3f}. This construction is not just theory: Monte "
            "Carlo libraries build paths this way, the largest moves first, which suits quasi-random numbers, as "
            "Part sixteen shows."
        ) as vo:
            self.play(FadeIn(g), Create(paths[0]), FadeIn(lvl[0]))
            vo.wait_until("a")
            self.play(FadeIn(dots[0], scale=1.5), FadeIn(side[0]), FadeIn(side[1]))
            self.play(ReplacementTransform(paths[0], paths[1]), FadeTransform(lvl[0], lvl[1]))
            vo.wait_until("b")
            cur = paths[1]
            for k in range(2, 11):
                anims = [ReplacementTransform(cur, paths[k]), FadeTransform(lvl[k - 1], lvl[k])]
                if k <= 5:
                    anims.append(FadeIn(dots[k - 1], scale=1.5))
                    anims.append(FadeOut(dots[k - 2]))
                elif k == 6:
                    anims.append(FadeOut(dots[4]))
                self.play(*anims, run_time=0.7)
                cur = paths[k]
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def reflection(self, r):
        p, q = np.asarray(r["path"]), np.asarray(r["refl"])
        t = np.linspace(0, 1, len(p))
        g = axes([0, 1], [-1.6, 2.6], x_length=6.0, y_length=3.4, xlabel=r"time", xticks=[0, 0.5, 1],
                 yticks=[-1, 0, 1, 2], font_size=16).to_corner(UL, buff=0.4)
        ax = g.ax
        k = int(np.argmin(np.abs(t - r["t_cross"])))
        before = curve(ax, t[:k + 1], p[:k + 1], BM, stroke_width=2.5)
        after = curve(ax, t[k:], p[k:], BM, stroke_width=2.5)
        mirror = curve(ax, t[k:], np.clip(q[k:], -1.6, 2.6), STRAT, stroke_width=2.5)
        level = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=JUMP, stroke_width=2)
        al = MathTex(r"a = 1", font_size=24, color=JUMP).next_to(ax.c2p(1, 1), RIGHT, buff=0.08)
        tau = DashedLine(ax.c2p(t[k], -1.6), ax.c2p(t[k], 1), color=GREY_B, stroke_width=1.5)
        tl = MathTex(r"\tau_a", font_size=24, color=GREY_B).next_to(ax.c2p(t[k], -1.6), DOWN, buff=0.08)
        rows = [cmath(r"P(M_T \ge a)", r"=", r"P(M_T \ge a,\, W_T \ge a) + P(M_T \ge a,\, W_T < a)", font_size=30),
                cmath(r"P(M_T \ge a,\, W_T < a)", r"=", r"P(W_T > a)", font_size=30,
                      colors={r"P(W_T > a)": STRAT}),
                cmath(r"P(M_T \ge a)", r"=", r"2\,P(W_T \ge a) = 2\big(1 - \Phi(a/\sqrt{T})\big)", font_size=30,
                      colors={r"2\,P(W_T \ge a) = 2\big(1 - \Phi(a/\sqrt{T})\big)": ITO}),
                cmath(r"f_{\tau_a}(t)", r"=", r"\frac{a}{\sqrt{2\pi t^3}}\,e^{-a^2/2t},\quad \mathbb{E}\,\tau_a = \infty",
                      font_size=30)]
        whys = [why(r"split on where the path ends", 20),
                why(r"strong Markov at $\tau_a$: after it, the path and its mirror are equally likely", 20),
                why(r"add: every path ending above $a$ has crossed it", 20),
                why(r"differentiate in $T$; the tail falls like $t^{-1/2}$, too slowly for a mean", 20)]
        step = ladder(self, rows, whys, keep=4, top=-0.05, x=-1.6, buff=0.35, edge=6.9)
        res = VGroup(
            MathTex(rf"\text{{simulated: }} {r['p_sim']:.4f}", font_size=28, color=BM),
            MathTex(rf"2(1 - \Phi(1)) = {r['p_theory']:.4f}", font_size=28, color=ITO),
            MathTex(rf"\text{{shifted barrier: }} {r['p_bgk']:.4f}", font_size=28, color=DRIFT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.45)
        cap = wrapped_label(r"20{,}000 paths of 1{,}000 steps; a path watched only on the grid misses crossings "
                            r"between steps (Broadie, Glasserman and Kou 1997: move the barrier up by "
                            r"$0.5826\,\sigma\sqrt{\Delta t}$)", 5.4, 17, GREY_B).next_to(res, DOWN, buff=0.2)
        cap.align_to(res, LEFT)
        with self.voiceover(
            "What does the path do first? Ask for the probability that it reaches a level a by time T. Here is a path "
            "that crosses one. <bookmark mark='a'/> At the moment it first touches the level, the future is a fresh "
            "Brownian motion, independent of the past: the strong Markov property. So the path and its mirror image "
            "after that moment are equally likely. <bookmark mark='b'/> Split on where the path ends. Paths that "
            "touched the level and end below it are matched, one for one, by their mirrors, which end above it. "
            "<bookmark mark='c'/> So the chance of touching is twice the chance of ending above: the reflection "
            "principle. Differentiate, and you get the density of the first-passage time, whose tail is so heavy that "
            "its mean is infinite. <bookmark mark='d'/> Check it on twenty thousand paths. Theory says "
            f"{r['p_theory']:.4f}; the simulation says {r['p_sim']:.4f}, a little low, because a path watched on a "
            "grid can cross between two looks. Broadie, Glasserman and Kou showed how to correct for that: shift the "
            f"barrier, and the formula gives {r['p_bgk']:.4f}. Part fifteen prices barrier options with it."
        ) as vo:
            self.play(FadeIn(g), Create(level), FadeIn(al), Create(before), run_time=1.5)
            self.play(Create(after), run_time=1.2)
            vo.wait_until("a")
            self.play(Create(tau), FadeIn(tl), Create(mirror), run_time=1.5)
            vo.wait_until("b")
            step(0)
            step(1)
            vo.wait_until("c")
            step(2)
            step(3)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(x) for x in res], lag_ratio=0.4), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def arcsine(self, r):
        h = np.asarray(r["pos_hist"], float)
        e = np.asarray(r["pos_edges"])
        w = e[1] - e[0]
        dens = h / h.sum() / w
        g = axes([0, 1], [0, 3.2], x_length=6.6, y_length=3.8, xlabel=r"fraction of $[0, 1]$ spent above zero",
                 ylabel=r"density", xticks=[0, 0.5, 1], yticks=[0, 1, 2, 3], font_size=18).to_edge(RIGHT, buff=0.6)
        g.shift(DOWN * 0.4)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=ax.c2p(w * 0.9, 0)[0] - ax.c2p(0, 0)[0],
                                  height=ax.c2p(0, min(d, 3.2))[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=BM,
                                  fill_opacity=0.75).move_to(ax.c2p(m, 0), aligned_edge=DOWN)
                        for m, d in zip((e[:-1] + e[1:]) / 2, dens)])
        xs = np.linspace(0.01, 0.99, 120)
        arc = curve(ax, xs, np.minimum(1 / (np.pi * np.sqrt(xs * (1 - xs))), 3.2), DRIFT, stroke_width=3)
        lab = MathTex(r"\frac{1}{\pi\sqrt{x(1 - x)}}", font_size=30, color=DRIFT).next_to(ax.c2p(0.5, 0.9), UP,
                                                                                        buff=0.3)
        pc, ans = pause(r"A fair game in continuous time. What fraction of the time has the winner most likely been "
                        r"ahead?", rf"Near 0 or near 1, not near a half: {100 * r['frac_extreme']:.0f}\% of paths spend "
                        rf"less than a tenth or more than nine tenths of the time above zero, only "
                        rf"{100 * r['frac_middle']:.0f}\% between 40 and 60\% (L\'evy's arcsine law).", width=5.4)
        pc.to_corner(UL, buff=0.5)
        ans.next_to(pc, DOWN, buff=0.3).align_to(pc, LEFT)
        with self.voiceover(
            "A question to pause on. Two players play a fair game in continuous time. Over the whole game, what "
            "fraction of the time has one of them most likely been ahead? <bookmark mark='a'/> Intuition says about "
            "half. The same twenty thousand paths say otherwise. <bookmark mark='b'/> The histogram is a U: "
            f"{100 * r['frac_extreme']:.0f} percent of the paths spend less than a tenth, or more than nine tenths, "
            f"of the time above zero, and only {100 * r['frac_middle']:.0f} percent are near the middle. This is "
            "Lévy's arcsine law. A lead, once taken, tends to last, which is a useful thing to remember the next time "
            "a strategy has been ahead of its benchmark for most of a year."
        ) as vo:
            self.play(FadeIn(pc))
            vo.wait_until("a")
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05, run_time=2))
            vo.wait_until("b")
            self.play(Create(arc), FadeIn(lab), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
