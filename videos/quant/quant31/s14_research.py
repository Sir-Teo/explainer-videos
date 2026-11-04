from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import riskmodel as RM
from videos.quant.quant31.common import BAD, GOOD, HURDLE, IC_C, OOS_C, PART, REAL_C, fit_right, load


class Research(VoiceoverScene):
    def construct(self):
        t = load("theory")
        self.card()
        self.setup_()
        self.proof()
        self.theorem()
        self.sims(t)
        self.breadth()
        self.coins(t)
        self.tails(t)
        self.ladder_of_corrections(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The information ratio when the IC moves", r"What does a forecast's instability cost, exactly?",
                          part=PART)
        with self.voiceover("For the researcher. The fundamental law treats the information coefficient as a constant. "
                            "It is not. Here is the exact cost of its movement, proved, simulated, and measured on the "
                            "coins."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"r_{i,t}", r"=", r"IC_t\, z_{i,t} + \sqrt{1 - IC_t^2}\;\varepsilon_{i,t}", font_size=36,
                      colors={r"IC_t": IC_C}),
                cmath(r"IC_t", r"\overset{\text{iid}}{\sim}", r"(\mu,\ \sigma^2),\quad z_{\cdot,t} \text{ standardised},\ "
                      r"\varepsilon_{i,t} \overset{\text{iid}}{\sim} (0, 1)", font_size=32),
                cmath(r"\pi_t", r"=", r"\tfrac1N\textstyle\sum_i z_{i,t}\, r_{i,t}", font_size=36)]
        whys = [why(r"standardised returns whose correlation with the scores is $IC_t$ in period $t$"),
                why(r"the IC varies across periods with mean $\mu$ and standard deviation $\sigma$, independently of the "
                    r"noise; the scores have mean 0 and variance 1 across the $N$ assets"),
                why(r"the long--short book with holdings proportional to the scores: its return in period $t$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The setup. <bookmark mark='a'/> In period t, standardised returns are the IC of that period times the "
            "scores, plus independent noise. <bookmark mark='b'/> The IC itself is drawn each period with mean mu and "
            "standard deviation sigma. <bookmark mark='c'/> The book holds the scores, so its return is their average "
            "product with the returns."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"\pi_t", r"=", r"IC_t\cdot\tfrac1N\textstyle\sum_i z_{i,t}^2 + \sqrt{1 - IC_t^2}\cdot\tfrac1N\sum_i "
                      r"z_{i,t}\varepsilon_{i,t}", font_size=30),
                cmath(r"\pi_t", r"=", r"IC_t + \sqrt{1 - IC_t^2}\;\frac{\xi_t}{\sqrt N},\qquad \xi_t \sim (0, 1)", font_size=34),
                cmath(r"\mathbb E\,\pi_t", r"=", r"\mu", font_size=36),
                cmath(r"\operatorname{Var}\pi_t", r"=", r"\sigma^2 + \frac{\mathbb E(1 - IC_t^2)}{N} = \sigma^2\Big(1 - "
                      r"\frac1N\Big) + \frac{1 - \mu^2}{N}", font_size=30, colors={r"\operatorname{Var}\pi_t": HURDLE})]
        whys = [why(r"substitute the return model into the book's return"),
                why(r"the scores are standardised, so the first average is one; the second is noise with variance "
                    r"$1/N$, independent of $IC_t$"),
                why(r"the expected return is the mean IC"),
                why(r"the law of total variance: the IC's own variance, plus the noise averaged over $N$ assets, where "
                    r"$\mathbb E\,IC_t^2 = \mu^2 + \sigma^2$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "The proof is four lines. <bookmark mark='a'/> Substitute the return model into the book's return. "
            "<bookmark mark='b'/> The scores are standardised, so the first average is exactly one; the second is noise "
            "with variance one over N, independent of the IC. So the book earns the period's IC plus noise that "
            "diversifies with breadth. <bookmark mark='c'/> Its mean is mu. <bookmark mark='d'/> Its variance, by the law "
            "of total variance, is the IC's own variance, which does not diversify, plus the noise term, which does."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def theorem(self):
        st = VGroup(MathTex(r"IR \;=\; \frac{\mu}{\sqrt{\sigma^2(1 - 1/N) + (1 - \mu^2)/N}}", font_size=40),
                    MathTex(r"\sigma = 0:\ IR = \frac{\mu\sqrt N}{\sqrt{1 - \mu^2}} \approx \mu\sqrt N,\qquad "
                            r"N\to\infty:\ IR \to \frac{\mu}{\sigma}", font_size=30),
                    wrapped_label(r"per period; for $T$ independent periods a year, the annual IR is $\sqrt T$ times it. "
                                  r"The form $\mu/\sqrt{\sigma^2 + (1-\mu^2)/N}$ is Qian and Hua (2004) and Ding (2010); "
                                  r"the factor $1 - 1/N$ is exact in this model", 9.6, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"The law with a moving IC", st, r"Qian and Hua (2004); Ding (2010)", width=11.4, font_size=22)
        per = RM.ir_time_varying(0.05, 0.10, 500)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> The information ratio is the mean IC over the square root of the IC's "
            "variance plus the noise variance over N. <bookmark mark='b'/> When the IC never moves, it is the "
            "fundamental law, IC root N. When breadth grows without limit, it tends to mu over sigma: the information "
            "ratio of the IC series itself, which no amount of breadth can beat. <bookmark mark='c'/> The hook's numbers: "
            f"mu five percent, sigma ten, five hundred stocks, gives {per:.2f} a month, and {per * math.sqrt(12):.2f} a "
            "year, not three point nine."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
            vo.wait_until("c")
            self.wait(0.1)
        self.wait(0.5)
        self.clear_scene()

    def sims(self, t):
        rows = t["sims"]
        g = axes([1.2, 3.1], [0, 1.4], x_length=7.4, y_length=4.4, xlabel=r"breadth $N$", ylabel=r"IR per period",
                 xticks=[1.3, 2, 3], yticks=[0, 0.5, 1.0], xfmt=lambda v: {1.3: "20", 2: "100", 3: "1000"}[v],
                 yfmt=lambda v: f"{v:.1f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        xs = np.linspace(1.2, 3.1, 80)
        Ns = 10 ** xs
        naive = curve(ax, xs, 0.04 * np.sqrt(Ns), IC_C, stroke_width=3)
        cols = {0.03: GOOD, 0.08: BAD}
        forms, lims, dots = VGroup(), VGroup(), VGroup()
        for sd, col in cols.items():
            forms.add(curve(ax, xs, [RM.ir_time_varying(0.04, sd, int(n)) for n in Ns], col, stroke_width=3))
            lims.add(DashedLine(ax.c2p(1.2, min(0.04 / sd, 1.4)), ax.c2p(3.1, min(0.04 / sd, 1.4)), color=col,
                                stroke_width=1.5))
            for r in rows:
                if r["ic_sd"] == sd:
                    dots.add(Dot(ax.c2p(math.log10(r["N"]), r["sim"]), radius=0.07, color=col))
        leg = legend([(IC_C, r"$0.04\sqrt N$"), (GOOD, r"$\sigma = 0.03$"), (BAD, r"$\sigma = 0.08$")], font_size=17)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        txt = wrapped_label(r"dots: simulated strategies, 6 of 1{,}500 periods each, mean IC 0.04; dashed: the limits "
                            r"$\mu/\sigma$", 3.8, 16, GREY_A).next_to(leg, DOWN, buff=0.5)
        fit_right(txt)
        big = [r for r in rows if r["N"] == 1000]
        with self.voiceover(
            "Simulated. A mean IC of four percent, at breadths from twenty to a thousand. <bookmark mark='a'/> The "
            "fundamental law's promise rises without limit. <bookmark mark='b'/> With an IC that wanders by three "
            "percent, the information ratio bends toward its ceiling of one point three three; with eight percent, it "
            f"flattens near point five. <bookmark mark='c'/> The simulated strategies sit on the formula: at a thousand "
            f"assets, {big[0]['sim']:.2f} and {big[1]['sim']:.2f} simulated, against {big[0]['formula']:.2f} and "
            f"{big[1]['formula']:.2f} predicted, where the naive law says {big[0]['naive']:.2f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(txt))
            vo.wait_until("a")
            self.play(Create(naive))
            vo.wait_until("b")
            self.play(*[Create(f) for f in forms], *[Create(l_) for l_ in lims], run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.1))
        self.wait(0.4)
        self.clear_scene()

    def breadth(self):
        rows = [cmath(r"N^*", r"=", r"\frac{1 - \mu^2}{\sigma^2} \approx \frac{1}{\sigma^2}", font_size=40,
                      colors={r"N^*": HURDLE}),
                cmath(r"IR(N^*)", r"=", r"\frac{\mu}{\sigma\sqrt 2}\ \approx\ 71\%\ \text{of the ceiling}", font_size=36),
                cmath(r"\sigma = 0.10", r":", r"N^* \approx 100", font_size=36)]
        whys = [why(r"the breadth at which the IC's own variance equals the noise variance: beyond it, extra assets buy "
                    r"little"),
                why(r"at that breadth the information ratio is already $1/\sqrt2$ of its limit"),
                why(r"a typical monthly equity signal: past about a hundred independent bets, the IC's stability, not "
                    r"breadth, sets the information ratio")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A corollary every researcher should know. <bookmark mark='a'/> The two variance terms are equal at a breadth "
            "of about one over sigma squared. <bookmark mark='b'/> There, the information ratio is already seventy-one "
            "percent of its ceiling. <bookmark mark='c'/> With an IC that wanders by ten percent, that breadth is about a "
            "hundred. Beyond it, the way to a higher information ratio is a more stable forecast, not more assets. That "
            "is why desks track the IC's standard deviation month by month, and why a signal that works steadily is worth "
            "more than one that works brilliantly now and then."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def coins(self, t):
        rows = t["coins"]
        hx = [-4.6, -2.6, -0.9, 0.8, 2.7, 4.9]
        head = VGroup(label(r"signal", font_size=17, color=GREY_B), label(r"mean IC", font_size=17, color=IC_C),
                      label(r"sd of IC", font_size=17, color=HURDLE), label(r"$|\mu|\sqrt N$", font_size=17, color=IC_C),
                      label(r"theorem", font_size=17, color=GOOD), label(r"realised", font_size=17, color=REAL_C))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(label(r["signal"], font_size=19), MathTex(f"{r['ic']:+.3f}", font_size=24),
                           MathTex(f"{r['ic_sd']:.2f}", font_size=24), MathTex(f"{r['naive']:.2f}", font_size=24),
                           MathTex(f"{r['formula']:.2f}", font_size=24), MathTex(f"{r['realised']:.3f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.5 - 0.6 * j, 0])
        foot = wrapped_label(rf"daily rank ICs, 2018--2020; an average breadth of {rows[0]['N']:.0f} coins; IR per day; "
                             r"realised: the long--short book's own daily Sharpe ratio", 11.6, 16,
                             GREY_A).to_edge(DOWN, buff=0.4)
        m = [r for r in rows if r["signal"] == "mined"][0]
        with self.voiceover(
            "Now the coins: the six signals of Chapter seven. <bookmark mark='a'/> Their daily ICs are small and wander "
            f"enormously: the mined alpha's averages {m['ic']:.3f} with a standard deviation of {m['ic_sd']:.2f}. "
            f"<bookmark mark='b'/> The naive law promises it a daily information ratio of {m['naive']:.2f}; the theorem "
            f"cuts that to {m['formula']:.2f}. <bookmark mark='c'/> The book actually earned {m['realised']:.3f} a day. "
            "Closer, but still a factor of more than two away. Something else is missing."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[:3])) for r_ in tab[1:]], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[3:5])) for r_ in tab[1:]], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_[5]) for r_ in tab[1:]], lag_ratio=0.15))
        self.wait(0.4)
        self.clear_scene()

    def tails(self, t):
        rows = [cmath(r"\pi_t", r"=", r"\textstyle\sum_i w_{i,t}\, r_{i,t} \;\propto\; \operatorname{Corr}_{\text{Pearson}}(w_t, "
                      r"r_t)\cdot\operatorname{sd}(r_t)", font_size=32),
                cmath(r"\operatorname{Corr}_{\text{Spearman}}", r"\neq", r"\operatorname{Corr}_{\text{Pearson}}\ \ "
                      r"\text{when returns are fat-tailed}", font_size=32, colors={r"\neq": BAD}),
                cmath(r"\text{kurtosis}", r"=", rf"{t['kurtosis']:.0f}\ \text{{(excess, the coins' daily returns)}}",
                      font_size=32)]
        whys = [why(r"the book's return is the linear correlation of its weights with the returns, not the rank "
                    r"correlation the IC measures"),
                why(r"the rank IC ignores how large the winners and losers were; a few extreme moves dominate the linear "
                    r"one"),
                why(r"a normal distribution has zero excess kurtosis: the coins have a handful of enormous days")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The missing piece is the shape of the returns. <bookmark mark='a'/> The book's return is the linear "
            "correlation between its weights and the returns, scaled by their dispersion. <bookmark mark='b'/> The IC we "
            "measured is a rank correlation, and with fat tails the two differ: a few extreme moves dominate the linear "
            f"correlation and add noise to it. <bookmark mark='c'/> The coins' daily returns have an excess kurtosis of "
            f"{t['kurtosis']:.0f}; a normal distribution has zero."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def ladder_of_corrections(self, t):
        m = [r for r in t["coins"] if r["signal"] == "mined"][0]
        steps_ = [(r"the fundamental law, $|\mu|\sqrt N$", m["naive"], IC_C),
                  (r"the theorem, with the IC's variance", m["formula"], GOOD),
                  (r"mean over sd of the Pearson IC of the weights", m["pearson_ir"], HURDLE),
                  (r"what the book earned", m["realised"], REAL_C)]
        mx = max(v for _, v, _ in steps_)
        bars = VGroup()
        for j, (nm, v, col) in enumerate(steps_):
            r = Rectangle(width=6.0 * v / mx, height=0.55, fill_color=col, fill_opacity=0.8, stroke_width=0)
            r.move_to([-1.0, 1.6 - 1.0 * j, 0], aligned_edge=LEFT)
            bars.add(VGroup(label(nm, font_size=19, color=col).next_to(r, UP, buff=0.08).align_to(r, LEFT), r,
                            MathTex(f"{v:.3f}", font_size=26).next_to(r, RIGHT, buff=0.2)))
        bars.move_to(DOWN * 0.1)
        se = 1 / math.sqrt(950)
        foot = wrapped_label(rf"the mined alpha, daily, 2018--2020; the Pearson IC of its rank weights averages "
                             rf"{m['pearson']:.3f} with sd {m['pearson_sd']:.2f}; a daily Sharpe ratio over about 950 days "
                             rf"has a standard error of about {se:.3f}", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The ladder of corrections, for the mined alpha. <bookmark mark='a'/> The fundamental law: "
            f"{m['naive']:.2f}. The moving IC: {m['formula']:.2f}. <bookmark mark='b'/> Replace the rank IC by the "
            "linear correlation of the book's actual weights with the returns, day by day, and take its mean over its "
            f"standard deviation, which already contains the noise term: {m['pearson_ir']:.3f}. <bookmark mark='c'/> The book earned {m['realised']:.3f}, within one "
            f"standard error, about {se:.3f}. Three corrections, each with a reason, take the promise from half a Sharpe "
            "ratio a day to what was actually earned."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(bars[1]))
            vo.wait_until("b")
            self.play(FadeIn(bars[2]))
            vo.wait_until("c")
            self.play(FadeIn(bars[3]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: an IC with memory", r"when the IC is autocorrelated across periods, the annual IR is not "
                          r"$\sqrt T$ times the per-period one; the multi-period law, with costs and Chapter 5's dynamic "
                          r"trading, has no closed form", width=12.4, font_size=18),
            desk_question(r"open: effective breadth", r"with correlated assets and overlapping signals, breadth is an "
                          r"effective number of bets; estimating it from data without overstating it is unsolved in "
                          r"general (Buckle 2004; Ding and Martin 2017 give generalised laws)", width=12.4, font_size=18),
            desk_question(r"open: weights for fat tails", r"rank weights are robust but their Pearson IC is low; the "
                          r"weighting that maximises the information ratio under heavy-tailed returns is not known in "
                          r"closed form", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> When the IC is autocorrelated, the annual information ratio is not "
            "the square root of the number of periods times the daily one; with costs and dynamic trading, there is no "
            "closed form. <bookmark mark='b'/> Breadth, with correlated assets and overlapping signals, is an effective "
            "number of bets, and estimating it without overstating it is unsolved in general. <bookmark mark='c'/> And "
            "the weighting of scores that maximises the information ratio when returns are heavy-tailed is not known in "
            "closed form."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a signal's monthly IC has mean 0.03 and sd 0.06. What is the largest annual IR any breadth can "
                       r"give it?")
        with self.voiceover(
            "Pause and predict. A signal's monthly IC has mean point zero three and standard deviation point zero six. "
            "What is the largest annual information ratio any breadth can give it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
