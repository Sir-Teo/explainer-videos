from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, load, real_data


class Doob(VoiceoverScene):
    def construct(self):
        d = load("doob")
        iv = load("ivey_sim")
        self.card()
        self.theorem(d)
        self.unique()
        self.ivey(iv)
        self.market(d)
        self.square(d)

    def card(self):
        c = chapter_card(11, r"Doob's decomposition", r"How much of a price is predictable?", lit=(1953,), part=PART)
        with self.voiceover("Chapter eleven. Doob's decomposition."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorem(self, d):
        th = theorem_card(r"Doob decomposition",
                          r"Any adapted process with finite means splits, uniquely, as $X_n = X_0 + A_n + M_n$: $A$ is "
                          r"predictable (each step known one period ahead), $A_n = \sum_{k \le n} \mathbb{E}[X_k - X_{k-1} "
                          r"\mid \mathcal{F}_{k-1}]$, and $M$ is a martingale.", who=r"Doob (1953)", color=DRIFT,
                          width=9.6, font_size=24).to_edge(UP, buff=0.4)
        x, A, M = (np.asarray(d[k]) for k in ("coin_x", "coin_A", "coin_M"))
        n = np.arange(len(x))
        g = axes([0, 400], [-20, 60], x_length=8.0, y_length=3.4, xlabel=r"tosses of a coin that lands heads 55\% of "
                 r"the time", xticks=[0, 100, 200, 300, 400], yticks=[-20, 0, 20, 40, 60], font_size=18)
        g.next_to(th, DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        ax = g.ax
        lx = curve(ax, n, x, P_C, stroke_width=3)
        la = curve(ax, n, A, DRIFT, stroke_width=3)
        lm = curve(ax, n, M, MART, stroke_width=2.5)
        leg = legend([(P_C, r"the walk $X_n$"), (DRIFT, r"its drift $A_n = 0.1\,n$"), (MART, r"the martingale "
                      r"$M_n = X_n - A_n$")], font_size=21).next_to(g, RIGHT, buff=0.4).align_to(g, UP)
        with self.voiceover(
            "Most processes are not martingales: prices drift. Doob showed that any process with finite means splits, "
            "in exactly one way, into a predictable part and a martingale. The predictable part adds up, step by "
            "step, the expected change given what was known the step before. What is left over is a fair game. "
            "<bookmark mark='a'/> Take a coin that lands heads fifty-five percent of the time, and a walk that steps "
            "up on heads and down on tails. <bookmark mark='b'/> Its expected step is a tenth, so the predictable part "
            "is a straight line of slope a tenth. <bookmark mark='c'/> And the walk minus that line is a martingale: "
            "all of the surprise, none of the drift."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(lx), FadeIn(leg[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(la), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(Create(lm), FadeIn(leg[2]))
        self.wait(0.4)
        self.clear_scene()

    def market(self, d):
        t = np.asarray(d["t"])
        X, A, M = (np.asarray(d[k]) for k in ("X", "A", "M"))
        g = axes([1926, 2021], [-2, 10], x_length=8.0, y_length=4.6, ylabel=r"log of wealth from \$1 in the US market",
                 xticks=[1930, 1960, 1990, 2020], xfmt=lambda u: f"{int(u)}", yticks=[-2, 0, 2, 4, 6, 8, 10],
                 font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        tk = ValueTracker(0.0)
        lx = tracing(ax, t, X, tk, P_C, stroke_width=3)
        la = curve(ax, t, A, DRIFT, stroke_width=3)
        lm = curve(ax, t, M, MART, stroke_width=2.5)
        yr = always_redraw(lambda: MathTex(rf"{int(at_index(t, tk))}", font_size=36, color=P_C).next_to(
            ax.c2p(1926, 10), RIGHT, buff=0.2))
        side = VGroup(
            legend([(P_C, r"log wealth $X$"), (DRIFT, r"predictable drift $A$"), (MART, r"martingale $M$")], font_size=21),
            MathTex(rf"{d['X_end']:.2f}", r"=", rf"{d['A_end']:.2f}", r"+", rf"{d['M_end']:.2f}", font_size=36),
            label(rf"\$1 became \${np.exp(d['X_end']):,.0f}".replace(",", "{,}"), font_size=22, color=GREY_A),
            wrapped_label(r"drift as known each day: the average daily return up to the day before", 4.2, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        side[1][0].set_color(P_C)
        side[1][2].set_color(DRIFT)
        side[1][4].set_color(MART)
        src = real_data(r"Kenneth French's daily US market (value-weighted, with dividends), July 1926 -- December 2020")
        with self.voiceover(
            "Now the market. Here is the logarithm of a dollar invested in the American market in 1926, with "
            "dividends reinvested. <bookmark mark='a'/> Split it the way Doob says. For the predictable part, use "
            "what an investor could have known each day: the average daily return up to the day before. Add those "
            "forecasts up. <bookmark mark='b'/> What's left is the martingale, the market's surprises. "
            f"<bookmark mark='c'/> By the end of 2020 a dollar had become about {np.exp(d['X_end']):,.0f}. Of the "
            "nine log points it gained, a little over seven were the predictable drift, and under two were luck. "
            "Over decades the drift dominates; over a day or a year, the martingale does, which is why the drift is so "
            "hard to see."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0][0]))
            self.add(lx, yr)
            self.play(tk.animate.set_value(float(len(t) - 1)), run_time=4, rate_func=linear)
            lx.clear_updaters()
            yr.clear_updaters()
            vo.wait_until("a")
            self.play(Create(la), FadeIn(side[0][1]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(Create(lm), FadeIn(side[0][2]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def square(self, d):
        t = np.asarray(d["t"])
        M2, A2, qv = (np.asarray(d[k]) for k in ("M2", "A2", "qv"))
        g = axes([1926, 2021], [0, 5], x_length=8.0, y_length=4.4, ylabel=r"squared martingale and its compensator",
                 xticks=[1930, 1960, 1990, 2020], xfmt=lambda u: f"{int(u)}", yticks=[0, 1, 2, 3, 4, 5], font_size=18)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lm = curve(ax, t, M2, MART, stroke_width=2.5)
        la = curve(ax, t, A2, DRIFT, stroke_width=3.5)
        lq = DashedVMobject(curve(ax, t, qv, WHITE, stroke_width=2), num_dashes=80)
        side = VGroup(
            legend([(MART, r"$M_n^2$"), (DRIFT, r"$\sum$ each day's variance forecast"),
                    (WHITE, r"$\sum$ realized squared surprises")], font_size=21),
            MathTex(rf"{d['A2_end']:.3f}\ \text{{vs}}\ {d['qv_end']:.3f}", font_size=34),
            wrapped_label(r"$M^2$ minus its compensator is a martingale: the variance is the predictable part of the "
                          r"square. Part 5 calls the realized sum the quadratic variation, and builds It\^o's calculus "
                          r"on it.", 4.4, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Doob's decomposition has a second use. Square the martingale. A squared fair game is not fair: it drifts "
            "up, because surprises of either sign add to it. <bookmark mark='a'/> Its predictable part is the sum of "
            "each day's variance forecast, here a simple weighted average of recent squared surprises, known the day "
            "before. <bookmark mark='b'/> And the sum of the squared surprises that actually happened, day by day, "
            "lands almost exactly on it: two point eight nine against two point eight nine. <bookmark mark='c'/> The "
            "variance is the predictable part of the square. Part five calls that realized sum the quadratic "
            "variation, and builds the whole of Itô's calculus on it."
        ) as vo:
            self.play(FadeIn(g), Create(lm), FadeIn(side[0][0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(la), FadeIn(side[0][1]))
            vo.wait_until("b")
            self.play(Create(lq), FadeIn(side[0][2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def unique(self):
        rows = [cmath(r"\mathbb{E}[\Delta M_k \mid \mathcal{F}_{k-1}]", r"=",
                      r"\mathbb{E}[\Delta X_k \mid \mathcal{F}_{k-1}] - \Delta A_k = 0", font_size=38),
                cmath(r"A - A' = M' - M", r"\Rightarrow",
                      r"\Delta = \mathbb{E}[\Delta \mid \mathcal{F}_{k-1}] = 0", font_size=38,
                      colors={r"\Delta = \mathbb{E}[\Delta \mid \mathcal{F}_{k-1}] = 0": MART}),
                cmath(r"M_n^2", r"=", r"\langle M \rangle_n + N_n, \quad \langle M \rangle_n = \sum_{k \le n} "
                      r"\mathbb{E}[(\Delta M_k)^2 \mid \mathcal{F}_{k-1}]", font_size=36,
                      colors={r"\langle M \rangle_n + N_n, \quad \langle M \rangle_n = \sum_{k \le n} \mathbb{E}[(\Delta M_k)^2 \mid \mathcal{F}_{k-1}]": DRIFT}),
                cmath(r"\mathcal{G}_n \supset \mathcal{F}_n", r"\Rightarrow", r"A^{\mathcal{G}} \ne A^{\mathcal{F}} "
                      r"\text{ in general}", font_size=38, colors={r"A^{\mathcal{G}} \ne A^{\mathcal{F}} \text{ in general}": LOSS})]
        whys = [why(r"by construction: $A$ adds up each step's forecast, so what is left has forecast zero"),
                why(r"uniqueness: a difference that is both predictable and a martingale is known in advance and has "
                    r"mean-zero steps, so its steps are zero"),
                why(r"apply it to $M^2$: $\mathbb{E}[\Delta(M^2) \mid \mathcal{F}] = \mathbb{E}[(\Delta M)^2 \mid "
                    r"\mathcal{F}]$; the predictable quadratic variation"),
                why(r"the drift is a forecast, so it depends on what you know")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.8, buff=0.75, edge=6.9)
        with self.voiceover(
            "Why unique? The predictable part adds up each step's forecast, so the rest has forecast zero. "
            "<bookmark mark='a'/> Two splits would differ by something both predictable and a martingale, and a step "
            "known in advance with forecast zero is zero. <bookmark mark='b'/> Applied to a squared martingale, the "
            "predictable part is the sum of conditional variances, the angle bracket. <bookmark mark='c'/> But the "
            "predictable part is a forecast, and a forecast depends on what you know."
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

    def ivey(self, iv):
        n = iv["n"]
        k = np.arange(0, n + 1, 20)[: len(iv["X"])]
        X, AF, AG, Y, AY = (np.asarray(iv[c], float) for c in ("X", "AF", "AG", "Y", "AY"))
        g = axes([0, n], [-250, 800], x_length=7.8, y_length=4.6, xlabel=r"hands of punto banco (simulated)",
                 ylabel=r"units won", xticks=[0, 5000, 10000], yticks=[-200, 0, 200, 400, 600, 800],
                 font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        tk = ValueTracker(0.0)
        lx = tracing(ax, k, X, tk, P_C, stroke_width=2.2)
        laf = tracing(ax, k, AF, tk, LOSS, stroke_width=3)
        ly = tracing(ax, k, Y, tk, QC.IDEA, stroke_width=2.2)
        lay = tracing(ax, k, AY, tk, MART, stroke_width=3)
        leg = legend([(P_C, r"bet player every hand"), (LOSS, r"its drift, casino's information: $-1.24\%$ a hand"),
                      (QC.IDEA, r"pick the side from the sorted card"), (MART, r"its drift: $+6.5\%$ a hand")],
                     font_size=18)
        side = VGroup(
            leg,
            MathTex(rf"\text{{after {n:,} hands: }} {iv['X_end']:+.0f}\ \text{{vs}}\ {iv['Y_end']:+.0f}".replace(",", "{,}"),
                    font_size=26),
            label(r"edge figures from the court record: house edge 1.24\% (player), 1.06\% (banker); perfect edge "
                  r"sorting, about 6.5\% to the punter", font_size=17, color=GREY_B),
            label(r"\textit{Ivey v Genting Casinos} [2014] EWHC 3394 (QB); [2017] UKSC 67", font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        for s_ in side[2:]:
            if s_.width > 5.0:
                s_.scale_to_fit_width(5.0)
        tag = label(r"simulated, with the court's edge figures; ties ignored", font_size=18, color=QC.IDEA).to_edge(
            UP, buff=0.3)
        pred = desk_question(r"Is the drift a property of the price, or of what you know?",
                             r"Of what you know: it is a conditional expectation, and changing the information "
                             r"changes it.", width=5.0, font_size=20)
        pred.next_to(side[0], DOWN, buff=0.3).align_to(side, LEFT)
        with self.voiceover(
            "A casino learned this in court. In August 2012 Phil Ivey won just over seven point seven million pounds "
            "at punto banco at Crockfords in London. The house edge on a player bet was one point two four percent. "
            "<bookmark mark='a'/> To the casino, a punter backing player every hand has a predictable part sloping "
            "down by that much a hand. <bookmark mark='b'/> But Ivey's partner sorted the cards, learning something "
            "about the first card before the deal. Choosing the side on that information, the same game has a "
            "predictable part sloping up about six and a half percent a hand, in the High Court's figures. "
            "<bookmark mark='c'/> The cards did not change; the filtration did. The courts, up to the Supreme Court "
            "in 2017, held it was cheating, and Ivey was not paid. <bookmark mark='d'/> So the drift is a property of "
            "what you know."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(side[3]))
            vo.wait_until("a")
            self.add(lx, laf)
            self.play(FadeIn(leg[:2]), tk.animate.set_value(float(n)), run_time=4, rate_func=linear)
            lx.clear_updaters()
            laf.clear_updaters()
            vo.wait_until("b")
            tk.set_value(0.0)
            self.add(ly, lay)
            self.play(FadeIn(leg[2:]), tk.animate.set_value(float(n)), run_time=4, rate_func=linear)
            ly.clear_updaters()
            lay.clear_updaters()
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            vo.wait_until("d")
            self.play(FadeOut(side[1:3]), FadeIn(pred, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
