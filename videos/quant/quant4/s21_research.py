from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import GAIN, LOSS, MART, P_C, PART, Q_C, load

FIX, MIX, ST = LOSS, Q_C, GAIN


class Research(VoiceoverScene):
    def construct(self):
        t = load("lil_theory")
        self.card()
        self.lil()
        self.proof()
        self.peeking(t)
        self.robbins()
        self.crossing(t)
        self.widths(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"How far can a fair walk wander?", r"The law of the iterated logarithm, and the price of "
                          r"looking forever", part=PART)
        with self.voiceover("For the researcher: Chapter 15 said a test checked forever rejects a true null. Here is "
                            "the theorem that says how far a fair walk wanders, and what an always-valid test must pay "
                            "for it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c), run_time=0.4)

    def lil(self):
        thm = theorem_card(r"The law of the iterated logarithm", VGroup(
            MathTex(r"\limsup_{t \to \infty} \frac{S_t}{\sqrt{2t \log\log t}} = 1\quad \text{almost surely}", font_size=34),
            MathTex(r"S_t = X_1 + \dots + X_t,\ \ X_i\ \text{iid},\ \mathbb E X = 0,\ \operatorname{Var} X = 1", font_size=26,
                    color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25), who=r"Khinchin (1924); Kolmogorov (1929); "
            r"Hartman and Wintner (1941)", width=10.2, font_size=24).move_to(UP * 0.6)
        notes_ = VGroup(
            why(r"For every $\epsilon>0$, the $(1-\epsilon)$ envelope is crossed infinitely often; "
                r"the $(1+\epsilon)$ envelope only finitely often. The exact envelope is not decided by the limsup alone."),
            why(r"so $|S_t| > 1.96\sqrt t$ happens for some $t$ with probability one: a fixed-sample test, read forever, "
                r"always rejects a true null"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        for w in notes_:
            if w.width > 12.6:
                w.scale_to_fit_width(12.6)
        with self.voiceover(
            "The theorem is Khinchin's, from 1924. <bookmark mark='a'/> A sum of independent fair steps, divided by the "
            "square root of two t log log t, has a lim sup of exactly one. <bookmark mark='b'/> The central limit "
            "theorem describes the walk at one time. The limsup describes all times: every envelope slightly below "
            "this scale is crossed infinitely often, and every envelope slightly above it only finitely often. "
            "It does not settle crossing of the exact envelope. Because log log t grows "
            "without bound, the walk eventually crosses one point nine six standard deviations, or any fixed number, "
            "with probability one."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(notes_[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes_[1]))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"\Pr\big(\max_{t \le n} S_t \ge x\big)", r"\le", r"e^{-x^2/2n}", font_size=30,
                      colors={r"\Pr\big(\max_{t \le n} S_t \ge x\big)": MART}),
                cmath(r"t_k", r"=", r"\theta^k,\quad x_k = (1 + \epsilon)\sqrt{2t_k \log\log t_k}", font_size=30,
                      colors={r"t_k": P_C}),
                cmath(r"\Pr\big(\max_{t \le t_{k+1}} S_t \ge x_k\big)", r"\le", r"\exp\Big(-\tfrac{(1 + \epsilon)^2}{\theta}\log\log "
                      r"t_k\Big) = (k\log\theta)^{-(1 + \epsilon)^2/\theta}", font_size=28,
                      colors={r"\Pr\big(\max_{t \le t_{k+1}} S_t \ge x_k\big)": MART}),
                cmath(r"\textstyle\sum_k (\cdot)", r"<", r"\infty\ \ \text{when}\ \theta < (1 + \epsilon)^2", font_size=30,
                      colors={r"\textstyle\sum_k (\cdot)": GAIN})]
        whys = [why(r"This proof assumes Gaussian or conditional 1-sub-Gaussian steps. "
                    r"The general finite-variance LIL needs additional truncation arguments."),
                why(r"check only at geometric times, with a boundary a little above the LIL's"),
                why(r"over the whole block $(t_k, t_{k+1}]$, $\max S_t \ge x_k$ is needed for any crossing of $x(t)$ there; "
                    r"the bound is a power of $k$"),
                why(r"the bounds are summable, so by Borel--Cantelli only finitely many blocks cross: $\limsup \le 1 + \epsilon$. "
                    r"The matching lower bound uses the second Borel--Cantelli lemma on independent block increments")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "For Gaussian or one-sub-Gaussian steps, the upper half has a short martingale proof. The general "
            "finite-variance result needs additional truncation. <bookmark "
            "mark='a'/> Doob's maximal inequality, applied to the exponential martingale with the best exponent, gives "
            "the running maximum of the walk a Gaussian tail. <bookmark mark='b'/> Check only at geometric times, theta "
            "to the k, against a boundary a little above the law's. <bookmark mark='c'/> The chance the walk crosses "
            "anywhere in a block is then bounded by a power of k. <bookmark mark='d'/> Those bounds are summable "
            "whenever theta is close enough to one, so by Borel and Cantelli only finitely many blocks are ever "
            "crossed. The matching lower half uses the second Borel-Cantelli lemma on the independent increments "
            "between blocks."
        ) as vo:
            step(0, run_time=0.5)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def _crossplot(self, t, keys, ylabel):
        mk = np.log10(np.asarray(t["marks"], float))
        g = axes([0, 5], [0, 1], x_length=8.4, y_length=4.0, xlabel=r"steps checked, $t$", ylabel=ylabel,
                 xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 0.05, 0.25, 0.5, 0.75, 1], yfmt=lambda v: rf"{100 * v:.0f}\%",
                 font_size=13, log_x=True).move_to(LEFT * 1.4 + DOWN * 0.3)
        ax = g.ax
        lines = VGroup(*[curve(ax, mk, np.asarray(t[k]["crossed"]), col, stroke_width=3) for k, col in keys])
        alpha_line = DashedLine(ax.c2p(0, t["alpha"]), ax.c2p(5, t["alpha"]), color=WHITE, stroke_width=1.5)
        return g, lines, alpha_line

    def peeking(self, t):
        g, lines, al = self._crossplot(t, [("fixed", FIX)], r"null paths that have crossed by $t$")
        mark_index = int(np.searchsorted(t["marks"], 2500))
        mark_time = int(t["marks"][mark_index])
        side = VGroup(
            MathTex(rf"t = {mark_time:,}:\ {100 * t['fixed']['crossed'][mark_index]:.0f}\%".replace(",", "{,}"),
                    font_size=26, color=FIX),
            MathTex(rf"t = 100{{,}}000:\ {100 * t['fixed']['final']:.0f}\%", font_size=26, color=FIX),
            wrapped_label(rf"{t['M']} random walks of N(0, 1) steps, the null true; red: the fixed-sample boundary "
                          r"$1.96\sqrt t$, checked from step 1. Chapter 15 instead uses coin steps and starts at 20.", 3.4, 15,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "See it happen. <bookmark mark='a'/> A thousand fair walks, each checked at every step against the "
            "fixed-sample boundary, one point nine six root t, starting at step one. This uses Gaussian rather "
            "than Chapter fifteen's coin steps. The share that has crossed keeps climbing. <bookmark mark='b'/> By a hundred "
            "thousand steps it is three quarters. The law of the iterated logarithm says it reaches one, but slowly: "
            "log log t is less than two and a half at a hundred thousand."
        ) as vo:
            self.play(FadeIn(g), Create(al))
            vo.wait_until("a")
            self.play(Create(lines[0]), run_time=2.5)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()

    def robbins(self):
        rows = [cmath(r"M^\lambda_t", r"=", r"e^{\lambda S_t - \lambda^2 t/2}", font_size=32, colors={r"M^\lambda_t": MART}),
                cmath(r"M_t", r"=", r"\int M^\lambda_t\, \sqrt{\tfrac{\rho}{2\pi}}e^{-\rho\lambda^2/2}\,d\lambda = "
                      r"\sqrt{\tfrac{\rho}{t + \rho}}\,\exp\Big(\frac{S_t^2}{2(t + \rho)}\Big)", font_size=30,
                      colors={r"M_t": MIX}),
                cmath(r"\Pr(\exists t:\ M_t \ge 1/\alpha)", r"\le", r"\alpha", font_size=32,
                      colors={r"\Pr(\exists t:\ M_t \ge 1/\alpha)": MART}),
                cmath(r"|S_t|", r"\ge", r"\sqrt{(t + \rho)\log\tfrac{t + \rho}{\rho\,\alpha^2}}", font_size=32,
                      colors={r"|S_t|": MIX})]
        whys = [why(r"Gaussian steps give a mean-one martingale; conditional 1-sub-Gaussian steps give a supermartingale"),
                why(r"Robbins (1970): mix over $\lambda \sim N(0, 1/\rho)$; a mixture of martingales is a martingale, and the "
                    r"Gaussian integral is done by completing the square"),
                why(r"Ville's inequality (Chapter 15): a nonnegative martingale started at one exceeds $1/\alpha$ ever, with "
                    r"probability at most $\alpha$"),
                why(r"solve $M_t = 1/\alpha$ for $|S_t|$: a boundary valid at every $t$ at once, growing like "
                    r"$\sqrt{t\log t}$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "How should a test look forever and stay honest? Herbert Robbins answered in 1970. <bookmark mark='a'/> "
            "For Gaussian null steps, the exponential of lambda S minus lambda squared t over two is a mean-one "
            "martingale; conditional one-sub-Gaussian steps give the same bound through a supermartingale. "
            "<bookmark mark='b'/> Average it over a normal distribution of lambdas. The average is "
            "still a martingale, and completing the square does the integral in closed form. <bookmark mark='c'/> "
            "Ville's inequality bounds the chance it ever reaches one over alpha by alpha. <bookmark mark='d'/> Solve "
            "for the walk, and the result is a boundary that holds at every time at once: it grows like the square "
            "root of t log t, a little faster than the law of the iterated logarithm allows a true walk to go."
        ) as vo:
            step(0, run_time=0.5)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def crossing(self, t):
        g, lines, al = self._crossplot(t, [("fixed", FIX), ("mix", MIX), ("stitched", ST)],
                                       r"null paths that have crossed by $t$")
        leg = legend([(FIX, r"fixed $1.96\sqrt t$"), (MIX, r"Robbins's mixture, $\rho = 100$"),
                      (ST, r"stitched (Howard et al.\ 2021)")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        side = VGroup(
            MathTex(rf"\text{{mixture}}:\ {100 * t['mix']['final']:.1f}\%", font_size=24, color=MIX),
            MathTex(rf"\text{{stitched}}:\ {100 * t['stitched']['final']:.1f}\%", font_size=24, color=ST),
            wrapped_label(r"Ville's inequality bounds each by 5\% over all time; 1{,}000 paths estimate the mixture's to "
                          r"within about 0.7 points. The stitched boundary spends little of its $\alpha$ this early",
                          3.3, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(leg, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Now the same thousand walks against the always-valid boundaries. <bookmark mark='a'/> Robbins's mixture, "
            "and a stitched boundary built by allocating error across exponential bounds on geometric time blocks, "
            "as in Howard, Ramdas, McAuliffe and Sekhon in 2021. <bookmark mark='b'/> Over a hundred thousand steps, the mixture is crossed "
            "by about five percent of the walks, within the sampling error of a thousand paths, and the stitched "
            "boundary by fewer than one percent. The guarantee holds whenever the test is read, because it was built "
            "for every time at once."
        ) as vo:
            self.play(FadeIn(g), Create(al), FadeIn(leg))
            self.play(Create(lines[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(lines[1]), Create(lines[2]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def widths(self, t):
        w = t["width"]
        keep = np.asarray(w["t"], float) >= 100
        mk = np.log10(np.asarray(w["t"], float)[keep])
        g = axes([2, 5], [0, 6], x_length=8.4, y_length=4.0, xlabel=r"steps, $t$ (view starts at 100)",
                 ylabel=r"boundary in standard deviations, $b(t)/\sqrt t$", xticks=[2, 3, 4, 5],
                 yticks=[0, 2, 4, 6], font_size=13, log_x=True).move_to(LEFT * 1.4 + DOWN * 0.3)
        ax = g.ax
        lines = VGroup(curve(ax, mk, np.asarray(w["fixed"])[keep], FIX, stroke_width=3),
                       curve(ax, mk, np.asarray(w["mix"])[keep], MIX, stroke_width=3),
                       curve(ax, mk, np.asarray(w["stitched"])[keep], ST, stroke_width=3),
                       curve(ax, mk, np.asarray(w["lil"])[keep], WHITE, stroke_width=2))
        leg = legend([(FIX, r"fixed: 1.96, valid once"), (MIX, r"mixture: $\sim\sqrt{\log t}$"),
                      (ST, r"stitched: $\sim\sqrt{\log\log t}$"), (WHITE, r"the LIL: $\sqrt{2\log\log t}$")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        with self.voiceover(
            "The price of looking forever is width. <bookmark mark='a'/> The fixed boundary stays at one point nine "
            "six standard deviations, valid only if you look once. Robbins's mixture widens like the square root of "
            "log t. The stitched boundary widens like the square root of log log t, the law of the iterated "
            "logarithm's own rate, in white, which no always-valid boundary can beat. <bookmark mark='b'/> But rates "
            "are asymptotic. At a hundred thousand steps the mixture is three point six standard deviations and the "
            "stitched boundary four point three with these tuning choices. Their ordering depends on the time "
            "horizon and tuning; this comparison is not a universal optimum. Both pay extra width for simultaneous coverage."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=3))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: the best boundary", r"which always-valid boundary is shortest, and for which stopping "
                          r"rule? The LIL fixes the rate; the constants, and the trade-off between early and late "
                          r"power, are design choices without a single optimum", width=12.4, font_size=18),
            desk_question(r"open: composite and nonparametric nulls", r"e-values for composite nulls (universal inference, "
                          r"Wasserman, Ramdas and Balakrishnan 2020) and growth-rate optimality (Grunwald, de Heide and "
                          r"Koolen 2024) are still being worked out", width=12.4, font_size=18),
            desk_question(r"open: heavy tails and dependence", r"returns are neither sub-Gaussian nor independent; "
                          r"time-uniform boundaries for them (Wang and Ramdas 2023) are recent and loose", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Which always-valid boundary is best? The law of the iterated "
            "logarithm fixes the rate, but the constants, and how a boundary trades early power for late power, are "
            "choices with no single answer. <bookmark mark='b'/> For composite nulls, such as 'the mean is at most "
            "zero, whatever the distribution', the theory of e-values is still being written. <bookmark mark='c'/> And "
            "returns are neither light-tailed nor independent; boundaries for them are recent, and loose."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"with $\rho = 100$ and $\alpha = 5\%$, how many standard deviations is Robbins's boundary at "
                       r"$t = 100$, and at $t = 10{,}000$? Compare with 1.96.").move_to(ORIGIN)
        with self.voiceover(
            "Pause and predict. With rho of a hundred and alpha of five percent, how many standard deviations is "
            "Robbins's boundary at a hundred steps, and at ten thousand? Compare with one point nine six."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
        self.answer()

    def answer(self):
        rho, alpha = 100.0, 0.05
        times = (100, 10000)
        widths = [np.sqrt((1 + rho / t) * np.log((t + rho) / (rho * alpha ** 2))) for t in times]
        title = label(r"Robbins's boundary in standard deviations", font_size=34, color=MIX).to_edge(UP, buff=0.45)
        formula = MathTex(r"\frac{b(t)}{\sqrt t}=\sqrt{\left(1+\frac{\rho}{t}\right)"
                          r"\log\frac{t+\rho}{\rho\alpha^2}},\quad \rho=100,\ \alpha=0.05",
                          font_size=32).next_to(title, DOWN, buff=0.4)
        rows = VGroup()
        for i, (text, value, color) in enumerate(((r"fixed, one look", 1.96, FIX),
                                                 (r"t=100", widths[0], MIX), (r"t=10{,}000", widths[1], MIX))):
            y = 0.25 - i * 1.05
            lab = label(text, font_size=24, color=color).move_to(LEFT * 5 + UP * y)
            bar = Rectangle(width=6 * value / 4, height=0.45, stroke_width=0, fill_color=color,
                            fill_opacity=0.85).move_to(LEFT * 2.8 + UP * y, aligned_edge=LEFT)
            number = MathTex(f"{value:.2f}", font_size=30, color=color).next_to(bar, RIGHT, buff=0.2)
            rows.add(VGroup(lab, bar, number))
        with self.voiceover(
            "Reveal the comparison. Divide the boundary by root t. <bookmark mark='a'/> At a hundred steps, "
            "the square root of two times log eight hundred is about three point six six standard deviations. "
            "<bookmark mark='b'/> At ten thousand, the answer is about three point two seven. Both exceed "
            "one point nine six because they protect repeated looks. The normalized width need not increase "
            "monotonically at these early times; rho tunes where the boundary is efficient."
        ) as vo:
            self.play(FadeIn(title), FadeIn(formula), FadeIn(rows[0]))
            for i, mark in enumerate(("a", "b"), 1):
                vo.wait_until(mark)
                self.play(FadeIn(rows[i][0]), GrowFromEdge(rows[i][1], LEFT), FadeIn(rows[i][2]))
        self.wait(0.4)
        self.clear_scene()
