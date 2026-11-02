from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, Q_C, load


class Doubling(VoiceoverScene):
    def construct(self):
        d = load("doubling")
        self.card()
        self.derive()
        self.cliffs(d)
        self.admissible()

    def card(self):
        c = chapter_card(7, r"Doubling and admissible strategies", r"How does the doubling system cheat the theorem?",
                         lit=(1981,), part=PART)
        with self.voiceover("Chapter seven. Doubling, and admissible strategies."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"\text{unlimited credit:}\ M_\tau", r"=", r"M_0 + 1 \quad \text{always}, \quad \mathbb{E}\tau = 2",
                      font_size=36, colors={r"M_0 + 1 \quad \text{always}, \quad \mathbb{E}\tau = 2": LOSS}),
                cmath(r"\text{bets } 1, 2, 4, \dots, 2^{\tau - 1}", r"\Rightarrow",
                      r"\text{steps unbounded; the loss before the win is } 2^{\tau-1} - 1", font_size=34),
                cmath(r"\text{bankroll } 2^k - 1:\ \mathbb{E}\,\text{gain}", r"=",
                      r"(1 - 2^{-k})\cdot 1 - 2^{-k}(2^k - 1) = 0", font_size=36,
                      colors={r"(1 - 2^{-k})\cdot 1 - 2^{-k}(2^k - 1) = 0": MART}),
                cmath(r"\text{sessions to first ruin}", r"\sim", r"\text{Geometric}(2^{-k}), \quad \text{mean } 2^k",
                      font_size=36)]
        whys = [why(r"stop at the first win: one unit up with probability one, after two tosses on average"),
                why(r"no bound on the stopped process, and the losses along the way are unbounded: condition (b) fails "
                    r"and so does (c)"),
                why(r"ten doublings from 1{,}023: the bets are bounded, optional stopping holds, the game is fair again"),
                why(r"each session is an independent trial that ruins with probability $2^{-k}$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.4, buff=0.75, edge=6.9)
        with self.voiceover(
            "The doubling system is the original martingale: bet one, and double the bet after every loss, until the "
            "first win. With unlimited credit you stop at the first win, after two tosses on average, always exactly "
            "one unit up. <bookmark mark='a'/> The theorem is not broken. The bets one, two, four, eight grow without "
            "limit, and so do the losses you carry before the win, so none of its three conditions holds. "
            "<bookmark mark='b'/> Give the gambler a real bankroll, a thousand and twenty-three units, enough for ten "
            "doublings. Now a thousand and twenty-three sessions in a thousand and twenty-four win one unit, and one "
            "loses everything. The expected gain is exactly zero. <bookmark mark='c'/> Each session ruins with "
            "probability one in a thousand and twenty-four, so the wait for the first ruin is geometric, with mean "
            "one thousand and twenty-four sessions, and the units won along the way are lost at once."
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

    def cliffs(self, d):
        S = np.asarray(d["sessions"], float)
        P = np.asarray(d["paths"], float)
        mean, med = np.asarray(d["mean"]), np.asarray(d["median"])
        lo = float(min(P.min(), -3200))
        g = axes([0, 3000], [lo, 3200], x_length=8.2, y_length=4.8, xlabel=r"sessions played",
                 ylabel=r"80 doublers' cumulative P\&L, bankroll 1{,}023 (refilled after ruin)",
                 xticks=[0, 1000, 2000, 3000], yticks=[-3000, 0, 3000],
                 yfmt=lambda u: f"{int(u):,}".replace(",", "{,}"), font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        tk = ValueTracker(0.0)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(3000, 0), color=GREY_C, stroke_width=1.5)

        def paths():
            i = tk.get_value()
            m = int(np.clip(np.floor(i), 1, len(S) - 1))
            grp = VGroup()
            for row in P:
                pts = [ax.c2p(0, 0)] + [ax.c2p(S[j], row[j]) for j in range(m + 1)]
                fell = np.any(np.diff(row[:m + 1]) < -100)
                grp.add(VMobject(stroke_width=1.3, stroke_color=LOSS if fell else QC.IDEA,
                                 stroke_opacity=0.45).set_points_as_corners(pts))
            return grp

        fan = always_redraw(paths)
        r_mean = readout(r"\text{mean of 1{,}000:}", lambda: at_index(mean, tk), digits=0, font_size=30,
                         color=MART).to_corner(UR, buff=0.5)
        r_med = readout(r"\text{median:}", lambda: at_index(med, tk), digits=0, font_size=30,
                        color=QC.IDEA).next_to(r_mean, DOWN, buff=0.2).align_to(r_mean, LEFT)
        side = VGroup(
            MathTex(rf"\text{{after 3{{,}}000: mean }} {d['mean_end']:+.1f} \pm {d['mean_se_end']:.1f}", font_size=28,
                    color=MART),
            MathTex(rf"\text{{ruined at least once: }} {100 * d['frac_ruined']:.1f}\%", font_size=28, color=LOSS),
            MathTex(rf"\text{{theory: }} 1 - (1023/1024)^{{3000}} = {100 * d['frac_ruined_theory']:.1f}\%", font_size=26,
                    color=GREY_A),
            MathTex(rf"\text{{mean wait for first ruin: }} {d['first_ruin_mean']:,.0f}".replace(",", "{,}"), font_size=26),
            label(rf"the House's \texttt{{doubling()}} on real coin flips: ruin {100 * d['check_ruin']:.2f}\% per session "
                  rf"vs.\ $2^{{-10}} = {100 * d['check_theory']:.2f}\%$", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.8)
        pred = desk_question(r"With a bankroll of 1{,}023, how many sessions until the first ruin, on average?",
                             r"1{,}024: each session ruins with probability $2^{-10}$.", width=5.4, font_size=20)
        with self.voiceover(
            "Watch a thousand doublers, each with a bankroll of a thousand and twenty-three, refilled whenever it is "
            "lost. Eighty are drawn. <bookmark mark='a'/> Gold staircases climb one unit per session. Then, at random "
            "moments, one turns into a red cliff, a thousand and twenty-three units straight down. The median doubler "
            "climbs happily for a long time; the mean stays near zero throughout, because the cliffs pay for every "
            f"step. <bookmark mark='b'/> After three thousand sessions, {100 * d['frac_ruined']:.0f} percent have been "
            f"ruined at least once, as the formula predicts, and the average result is {d['mean_end']:+.0f}, within "
            "sampling error of zero. <bookmark mark='c'/> With a bankroll of a thousand and twenty-three, how many "
            f"sessions until the first ruin? On average a thousand and twenty-four; simulated, {d['first_ruin_mean']:,.0f}."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            self.add(fan, r_mean, r_med)
            vo.wait_until("a")
            self.play(tk.animate.set_value(float(len(S) - 1)), run_time=10, rate_func=linear)
            for m_ in (fan, r_mean, r_med):
                m_.clear_updaters()
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in side[:3]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(side[3:]))
            self.play(FadeIn(pred.move_to(ax.c2p(1500, lo * 0.62))))
        self.wait(0.4)
        self.clear_scene()

    def admissible(self):
        d = definition_card(r"Admissible strategy",
                            r"A self-financing strategy whose wealth never falls below some fixed $-c$: $V_t \ge -c$ "
                            r"for all $t$. Under a martingale measure $Q$ its wealth is then a supermartingale, so "
                            r"$\mathbb{E}_Q V_T \le V_0$: no free lunch.", width=10.4, color=Q_C, font_size=24)
        h1 = history_card(1981, r"Harrison and Pliska, ``Martingales and stochastic integrals in the theory of "
                          r"continuous trading''", r"prices are martingales under an equivalent measure exactly when "
                          r"admissible strategies cannot make something from nothing", width=10.4)
        h2 = history_card(1988, r"Dybvig and Huang, \textit{Review of Financial Studies} 1(4)",
                          r"a lower bound on wealth (a credit constraint) is what rules out doubling in continuous time",
                          width=10.4)
        short = wrapped_label(r"the same shape on a desk: selling options collects small premiums most days and pays a "
                              r"rare large loss (Part 11). The staircase and the cliff.", 10.4, 22, LOSS)
        VGroup(d, h1, h2, short).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        with self.voiceover(
            "In continuous time doubling is worse: betting ever faster, a doubler with unlimited credit can make any "
            "sum in a finite time. Finance closes the loophole with one rule: a strategy is admissible if its wealth "
            "never falls below some fixed floor. <bookmark mark='a'/> Michael Harrison and Stanley Pliska showed in "
            "1981 that when prices are martingales under an equivalent measure, admissible strategies cannot make "
            "something from nothing: their wealth is a supermartingale. <bookmark mark='b'/> Philip Dybvig and "
            "Chi-fu Huang showed in 1988 that this credit limit is exactly what rules out doubling; the proof belongs "
            "to Part nine. <bookmark mark='c'/> And remember the shape: selling options earns small premiums most "
            "days and pays a rare large loss. The staircase and the cliff."
            " One trader tried doubling with a bank's money. Next: Barings."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(h1))
            vo.wait_until("b")
            self.play(FadeIn(h2))
            vo.wait_until("c")
            self.play(FadeIn(short))
        self.wait(0.4)
        self.clear_scene()
