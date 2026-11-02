from __future__ import annotations

import itertools

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import LOSS, MART, P_C, PART, Q_C, load, real_data


class Measure(VoiceoverScene):
    def construct(self):
        m = load("measure")
        es = load("esscher")
        self.card()
        self.table()
        self.process()
        self.recolour()
        self.paths(m)
        self.esscher(es)

    def card(self):
        c = chapter_card(12, r"Change of measure", r"What if the coin were different?", lit=(1981,), part=PART)
        with self.voiceover("Chapter twelve. Change of measure."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def table(self):
        outs = ["".join(o) for o in itertools.product("HT", repeat=3)]
        head = VGroup(*[label(t, font_size=22, color=c) for t, c in
                        [(r"world", GREY_B), (r"$P$: fair coin", P_C), (r"$Q$: heads 60\%", Q_C),
                         (r"$L = dQ/dP$", MART)]])
        rows = []
        for o in outs:
            h = o.count("H")
            p, q = 0.125, 0.6 ** h * 0.4 ** (3 - h)
            rows.append([MathTex(o, font_size=28), MathTex(r"0.125", font_size=28, color=P_C),
                         MathTex(f"{q:.3f}", font_size=28, color=Q_C), MathTex(f"{q / p:.3f}", font_size=28, color=MART)])
        cells = [*head] + [c for r in rows for c in r]
        grid = VGroup(*cells).arrange_in_grid(rows=9, cols=4, buff=(0.7, 0.14), col_alignments="cccc")
        grid.scale_to_fit_height(5.6).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        side = VGroup(
            MathTex(r"L(\omega) = \frac{Q(\omega)}{P(\omega)}", font_size=40, color=MART),
            MathTex(r"\mathbb{E}_Q[X] = \mathbb{E}_P[L\,X]", font_size=40),
            MathTex(r"\mathbb{E}_P[L] = 1", font_size=40),
            wrapped_label(r"the Radon--Nikodym derivative: reweight each world, and one probability becomes another",
                          4.6, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "The same worlds can carry different probabilities. Toss a coin three times. Under P the coin is fair, "
            "and each of the eight worlds has probability one eighth. Under Q the coin lands heads sixty percent of "
            "the time, and the worlds with more heads are more likely. <bookmark mark='a'/> Divide one by the other, "
            "world by world. This ratio, L, is the Radon-Nikodym derivative of Q with respect to P. "
            "<bookmark mark='b'/> It converts one into the other: any expectation under Q is an expectation under P "
            "of the variable reweighted by L. And because Q's probabilities add up to one, L averages to one under P. "
            "This is the whole of the change of measure. In Part nine the second measure will be the one in which "
            "every asset earns the riskless rate, and prices will be expectations under it."
        ) as vo:
            self.play(FadeIn(VGroup(*cells[:4])), LaggedStart(*[FadeIn(VGroup(*r[:3])) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r[3]) for r in rows], lag_ratio=0.15), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def paths(self, m):
        n = m["n"]
        k = np.arange(n + 1)
        g = axes([0, n], [-6, 6], x_length=7.4, y_length=4.6, xlabel=r"tosses", ylabel=r"$L_n = dQ/dP$ on the first $n$ "
                 r"tosses (log scale)", xticks=[0, 100, 200, 300], yticks=[-6, -3, 0, 3, 6],
                 yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        pp = VGroup(*[curve(ax, k, np.clip(np.asarray(p), -6, 6), P_C, stroke_width=1.5).set_stroke(opacity=0.6)
                      for p in m["paths_p"]])
        qq = VGroup(*[curve(ax, k, np.clip(np.asarray(p), -6, 6), Q_C, stroke_width=1.5).set_stroke(opacity=0.6)
                      for p in m["paths_q"]])
        med = curve(ax, k, np.log10(np.asarray(m["median_p"])), WHITE, stroke_width=3.5)
        one = DashedLine(ax.c2p(0, 0), ax.c2p(n, 0), color=GREY_B, stroke_width=2)
        side = VGroup(
            label(r"if the coin is fair ($P$):", font_size=22, color=P_C),
            MathTex(r"\mathbb{E}_P[L_n] = 1 \text{ for every } n", font_size=30),
            MathTex(rf"\text{{median after {n}: }} {m['median_end_p']:.3f}", font_size=30, color=WHITE),
            label(rf"{100 * m['frac_below_001']:.0f}\% of paths end below 0.01", font_size=22, color=GREY_A),
            label(r"if the coin is the 60\% one ($Q$):", font_size=22, color=Q_C),
            label(rf"{100 * m['frac_q_above_100']:.0f}\% of paths end above 100", font_size=22, color=GREY_A),
            wrapped_label(r"$L$ is the wealth of a gambler betting that the coin is $Q$: a fair game if it isn't, a "
                          r"fortune if it is. Testing by betting is a change of measure.", 4.6, 21, MART),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now follow L as the tosses go on, say for three hundred. Under the fair coin, L is a martingale with "
            "mean one: we built it to average one. <bookmark mark='a'/> Yet look at the paths. Almost all of them "
            "sink toward zero. The median after three hundred tosses is about two thousandths, and two thirds of "
            "the paths end below a hundredth. The mean stays at one only because of a few paths that soar, so rare "
            "that two thousand simulated paths average under a half. A nonnegative martingale must converge, and "
            "this one converges to zero. <bookmark mark='b'/> If the coin really is the sixty-percent one, the same "
            "L grows: two thirds of the paths end above a hundred. <bookmark mark='c'/> Read L as the wealth of a "
            "gambler who bets, toss by toss, that the coin is Q. If it isn't, the gambler is playing a fair game and "
            "almost surely goes broke. If it is, the gambler gets rich. That is the idea behind testing by betting, "
            "in chapter fifteen."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(side[:2]))
            self.play(LaggedStart(*[Create(p) for p in pp], lag_ratio=0.05, run_time=4))
            vo.wait_until("a")
            self.play(Create(med), FadeIn(side[2:4]))
            vo.wait_until("b")
            self.play(pp.animate.set_stroke(opacity=0.15), LaggedStart(*[Create(p) for p in qq], lag_ratio=0.05,
                                                                       run_time=4), FadeIn(side[4:6]))
            vo.wait_until("c")
            self.play(FadeIn(side[6]))
        self.wait(0.4)
        self.clear_scene()

    def process(self):
        rows = [cmath(r"Z_n = \mathbb{E}_P[L \mid \mathcal{F}_n]", r"=", r"\prod_{k \le n} \frac{q(\omega_k)}{p(\omega_k)}",
                      font_size=38, colors={r"\prod_{k \le n} \frac{q(\omega_k)}{p(\omega_k)}": MART}),
                cmath(r"\mathbb{E}_Q[X \mid \mathcal{F}_n]", r"=", r"\frac{\mathbb{E}_P[X L \mid \mathcal{F}_n]}{Z_n}",
                      font_size=38),
                cmath(r"\xi = \pm 1:\ \mathbb{E}_P\xi = 0,\ \mathbb{E}_Q\xi = 2q - 1", r"\Rightarrow",
                      r"S_n - (2q - 1)\,n \text{ is a } Q\text{-martingale}", font_size=36,
                      colors={r"S_n - (2q - 1)\,n \text{ is a } Q\text{-martingale}": Q_C}),
                cmath(r"\frac{dQ}{dP}", r"=", r"\frac{e^{\theta R}}{\mathbb{E}_P e^{\theta R}}, \quad "
                      r"\mathbb{E}_Q[e^{R}] = e^{r_f}", font_size=38, colors={r"\frac{dQ}{dP}": MART})]
        whys = [why(r"the density process: a Doob martingale under $P$, the likelihood ratio of the first $n$ tosses"),
                why(r"Bayes' rule for conditional expectations: check the definition on each $A \in \mathcal{F}_n$"),
                why(r"discrete Girsanov: the same paths, a new drift; the martingale part is reweighted, not moved"),
                why(r"the Esscher transform (1932): tilt by $e^{\theta R}$, with $\theta$ chosen so every asset earns the "
                    r"riskless rate (Gerber and Shiu 1994)")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "Over time the change of measure is a process: the likelihood ratio of the first n tosses, a Doob "
            "martingale under P. <bookmark mark='a'/> Conditional expectations under Q are those under P, reweighted "
            "and divided by the density so far: Bayes' rule. <bookmark mark='b'/> The drift changes: the walk minus "
            "two q minus one per step is a Q-martingale, Girsanov on a coin. <bookmark mark='c'/> On real returns, "
            "Fredrik Esscher's 1932 choice tilts by an exponential of the return, so that every asset earns the "
            "riskless rate under Q."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def recolour(self):
        rng = np.random.default_rng(4)  # illustrative paths: no number from them is quoted
        n, k, q = 50, 200, 0.6
        H = rng.random((k, n)) < 0.5
        S = np.concatenate([np.zeros((k, 1)), np.cumsum(np.where(H, 1, -1), axis=1)], axis=1)
        logL = (H * np.log(q / 0.5) + (~H) * np.log((1 - q) / 0.5)).sum(1)
        w = np.exp(logL - logL.max())
        g = axes([0, n], [-22, 22], x_length=7.6, y_length=4.6, xlabel=r"tosses", ylabel=r"200 coin walks $S_n$",
                 xticks=[0, 25, 50], yticks=[-20, 0, 20], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        fan = path_fan(ax, np.arange(n + 1), S, color=GREY_B, opacity=0.25, max_paths=k)
        tk = ValueTracker(0.0)

        def restyle(m):
            u = tk.get_value()
            for path, wi in zip(m, w):
                op = (1 - u) * 0.25 + u * min(1.0, 0.04 + 0.96 * wi ** 0.5)
                m_col = interpolate_color(ManimColor(GREY_B), ManimColor(Q_C), u)
                path.set_stroke(color=m_col, opacity=op, width=(1 - u) * 1.2 + u * (0.6 + 2.6 * wi ** 0.5))

        fan.add_updater(restyle)
        ends = S[:, -1]
        bins = np.arange(-23, 24, 2)
        hp = np.histogram(ends, bins=bins)[0].astype(float)
        hq = np.histogram(ends, bins=bins, weights=w)[0]
        hp, hq = hp / hp.max(), hq / hq.max()

        def dens(h, col):
            grp = VGroup()
            for i, v in enumerate(h):
                y0, y1 = ax.c2p(0, bins[i])[1], ax.c2p(0, bins[i + 1])[1]
                grp.add(Rectangle(width=max(1.4 * v, 0.01), height=y1 - y0 - 0.02, stroke_width=0, fill_color=col,
                                  fill_opacity=0.7).move_to([ax.get_right()[0] + 0.2 + 0.7 * v, (y0 + y1) / 2, 0]))
            return grp

        dp, dq = dens(hp, P_C), dens(hq, Q_C)
        cap = label(r"a change of measure moves weight, not paths", font_size=30, color=Q_C).to_edge(UP, buff=0.35)
        side = VGroup(
            label(r"under $P$: every path weighs $2^{-50}$", font_size=21, color=P_C),
            label(r"under $Q$ (heads 60\%): weight $\times\ L = (1.2)^{\#H}(0.8)^{\#T}$", font_size=21, color=Q_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.5)
        with self.voiceover(
            "Here is the picture to keep. Two hundred coin walks, drawn under the fair coin, every path equally "
            "likely. <bookmark mark='a'/> Now change the measure to the sixty-percent coin. No path moves. Each path "
            "is simply redrawn with a thickness proportional to its likelihood ratio: walks with many heads grow "
            "heavy, walks with many tails fade. <bookmark mark='b'/> The visible centre of the fan swings upward, and "
            "the distribution at the end slides with it. A change of measure moves weight, not paths, which is why "
            "anything that is impossible stays impossible, and anything possible stays possible."
        ) as vo:
            self.play(FadeIn(g), FadeIn(fan), FadeIn(dp), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(tk.animate.set_value(1.0), FadeIn(side[1]), run_time=4)
            fan.clear_updaters()
            vo.wait_until("b")
            self.play(Transform(dp, dq), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def esscher(self, es):
        edges = np.asarray(es["edges"]) * 100
        hp, hq = np.asarray(es["hist_p"]), np.asarray(es["hist_q"])
        g = axes([-8, 8], [-5, -0.5], x_length=6.6, y_length=4.0, xlabel=r"daily log return, \%",
                 ylabel=r"share of days (log scale)", xticks=[-8, -4, 0, 4, 8], yticks=[-5, -3, -1],
                 yfmt=lambda u: rf"10^{{{int(u)}}}", font_size=16).to_corner(DL, buff=0.5)
        ax = g.ax
        c = (edges[:-1] + edges[1:]) / 2

        def steps_(h, col):
            ys = np.log10(np.maximum(h, 1e-5))
            pts = []
            for i in range(len(c)):
                pts += [ax.c2p(edges[i], max(ys[i], -5)), ax.c2p(edges[i + 1], max(ys[i], -5))]
            return VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts)

        lp, lq = steps_(hp, P_C), steps_(hq, Q_C)
        card = lab_card(r"the Esscher tilt", [
            "def esscher_tilt(x, target):",
            "    def w(th):",
            "        v = np.exp(th * (x - x.mean())); return v / v.sum()",
            "    th = brentq(lambda t: np.log(w(t) @ np.exp(x)) - target,",
            "                -200, 200)",
            "    return th, w(th)",
        ], source="explainer/quant/house/martingale.py", width=6.4).to_corner(UR, buff=0.35)
        leg = legend([(P_C, r"$P$: the days as they came"), (Q_C, r"$Q$: the Esscher measure")], font_size=18)
        leg.next_to(g, UP, buff=0.15).align_to(g, LEFT)
        src = real_data(r"Kenneth French's daily US market and riskless rate, 1926--2020")
        pred = desk_question(r"Under $Q$, are crash days more or less likely than under $P$?",
                             rf"More: the worst 1\% of days carry {100 * es['tail_q']:.2f}\% of $Q$'s weight.",
                             width=5.6, font_size=20)
        with self.voiceover(
            "Let us find Q for the American market: every day since 1926 a possible world. The House searches for the "
            "tilt that makes the reweighted market earn the riskless rate. <bookmark mark='a'/> Theta is "
            f"{es['theta']:.2f}: Q leans toward bad days. The mean daily log return falls from {es['mean_p']:.2f} "
            f"basis points to {es['mean_q']:.2f}. <bookmark mark='b'/> The weight went into the left tail: the worst "
            f"one percent of days carry {100 * es['tail_q']:.2f} percent of Q's weight. <bookmark mark='c'/> So under "
            "Q crash days are more likely. That is what the premium pays for, and Part nine prices options in this "
            "world."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            out = lab_run(self, card, ["th, w = esscher_tilt(log1p(mkt), log1p(rf).mean())",
                                       f"theta = {es['theta']:.3f}",
                                       f"mean: {es['mean_p']:.2f} bp under P -> {es['mean_q']:.2f} bp under Q"])
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(leg), Create(lp), run_time=1.5)
            self.play(Create(lq), run_time=1.5)
            vo.wait_until("c")
            pred.next_to(out, DOWN, buff=0.3).align_to(card, LEFT)
            keep_in_frame(pred)
            self.play(FadeIn(pred, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
