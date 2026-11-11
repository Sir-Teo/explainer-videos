from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, FALSE, GOOD, HURDLE, NOISE, PART, RULE, TRUE, ask, comma, illustration, load


class Planted(VoiceoverScene):
    def construct(self):
        p = load("planted")
        self.card()
        self.market(p)
        self.picture(p)
        self.table(p)
        self.lesson(p)
        self.question()

    def card(self):
        c = chapter_card(13, r"Planted alpha", r"Do the tests find what is really there?", lit=(2019,), part=PART)
        with self.voiceover("Chapter thirteen. Testing the tests: plant real alpha in a simulated market, and see what "
                            "each method finds, and what it invents."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def market(self, p):
        rows = [cmath(r"r_{k,t}", r"=", r"\tfrac{SR_k}{\sqrt{252}} + \sqrt{0.2}\,f_t + \sqrt{0.8}\,\varepsilon_{k,t}",
                      font_size=38, colors={r"r_{k,t}": RULE}),
                cmath(r"SR_k", r"=", r"\begin{cases} 1\ \text{or}\ 2 & \text{for 10 planted strategies} \\ 0 & "
                      r"\text{for the other 990} \end{cases}", font_size=36, colors={r"SR_k": TRUE})]
        whys = [why(rf"{comma(p['n'])} strategies, {p['T'] // 252} years of daily returns, unit volatility, sharing a "
                    r"common factor with correlation 0.2, as strategies on one market do"),
                why(r"ten of them have a real edge planted in them; the rest have none. The House knows which, the "
                    rf"methods do not. {p['sims']} markets of each kind")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.5, buff=0.5, edge=6.9)
        with self.voiceover(
            "Every check in this part can itself be checked, by running it where the truth is known. <bookmark mark='a'/> "
            "A simulated market of a thousand strategies, five years of daily returns, all sharing a common factor, as "
            "strategies on one market do. <bookmark mark='b'/> In ten of them the House plants a real edge, a Sharpe "
            "ratio of one, or in a second experiment of two; the other nine hundred and ninety have none. The methods "
            "are not told which are which. Forty markets of each kind."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def picture(self, p):
        t = np.asarray(p["example"]["t"])
        pl = np.asarray(p["example"]["planted"], bool)
        o = np.argsort(t)
        t, pl = t[o], pl[o]
        n = len(t)
        g = axes([0, n], [-4, 5], x_length=9.0, y_length=4.2, xlabel=r"1{,}000 strategies, sorted by $t$-statistic",
                 ylabel=r"$t$-statistic of the mean", xticks=[], yticks=[-4, -2, 0, 2, 4], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        lines = VGroup(*[Line(ax.c2p(i, 0), ax.c2p(i, v), color=TRUE if q else NOISE, stroke_width=4 if q else 1.2,
                              stroke_opacity=1 if q else 0.5) for i, (v, q) in enumerate(zip(t, pl))])
        bon = stats.norm.ppf(1 - 0.05 / n)
        h1 = DashedLine(ax.c2p(0, 1.96), ax.c2p(n, 1.96), color=HURDLE, stroke_width=1.8)
        h2 = DashedLine(ax.c2p(0, bon), ax.c2p(n, bon), color=BAD, stroke_width=1.8)
        side = VGroup(
            MathTex(r"1.96", font_size=22, color=HURDLE), MathTex(rf"{bon:.2f}\ \text{{(Bonferroni)}}", font_size=22,
                                                                   color=BAD),
            wrapped_label(r"one market, planted Sharpe ratio 1. Green: the ten real ones. With five years of data a "
                          r"Sharpe ratio of one has an expected $t$ of only about 2.2", 3.2, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            f"This is the original saved single simulated market, sorted by its realised test statistics. <bookmark mark='a'/> Green marks the ten planted effects; their positions also reflect the realised shared factor. <bookmark mark='b'/> In this particular sample, {int(np.sum(t>1.96))} strategies exceed the one-point-nine-six line. A planted positive mean need not produce a significant statistic in one realised market. The next table averages all forty simulated markets per edge rather than treating this selected picture as representative performance."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.002), run_time=3)
            vo.wait_until("b")
            self.play(Create(h1), Create(h2), FadeIn(side))
        self.add(illustration(r"simulated: the House's \texttt{backtest.planted\_market}"))
        self.wait(0.4)
        self.clear_scene()

    def table(self, p):
        R = p["rows"]
        head = VGroup(*[label(h, font_size=18, color=GREY_A) for h in (r"", r"planted $SR = 1$", r"planted $SR = 2$")])
        sub = VGroup(label(r""), label(r"real found \;/\; false", font_size=15, color=GREY_B),
                     label(r"real found \;/\; false", font_size=15, color=GREY_B))
        data = [(r"$t > 1.96$, one at a time", "naive"), (r"Bonferroni, 5\%", "bonferroni"),
                (r"Romano--Wolf step-down, 5\%", "rw")]
        rows = [head, sub]
        for t, k in data:
            rows.append(VGroup(label(t, font_size=19, color=RULE),
                               MathTex(rf"{R['1.0'][k]['true']:.1f}\ /\ {R['1.0'][k]['false']:.1f}", font_size=26),
                               MathTex(rf"{R['2.0'][k]['true']:.1f}\ /\ {R['2.0'][k]['false']:.1f}", font_size=26)))
        rows.append(VGroup(label(r"DSR of the best $> 0.95$", font_size=19, color=RULE),
                           MathTex(rf"{100 * R['1.0']['dsr']['pass']:.0f}\%\ \text{{of markets}}", font_size=24),
                           MathTex(rf"{100 * R['2.0']['dsr']['pass']:.0f}\%\ \text{{of markets}}", font_size=24)))
        rows.append(VGroup(label(r"the best is a planted one", font_size=19, color=RULE),
                           MathTex(rf"{100 * R['1.0']['best_is_true']:.0f}\%", font_size=24),
                           MathTex(rf"{100 * R['2.0']['best_is_true']:.0f}\%", font_size=24)))
        xs = [-3.8, 1.3, 4.6]
        for j, row in enumerate(rows):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 2.6 - 0.72 * j, 0])
            if j > 1:
                row[0].align_to(np.array([xs[0] - 2.7, 0, 0]), LEFT)
        foot = wrapped_label(rf"averages over {p['sims']} simulated markets of each kind; ten strategies of "
                             rf"{comma(p['n'])} are real", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"These are averages over {p['sims']} fixed-seed simulated markets for each planted edge. <bookmark mark='a'/> With planted Sharpe one, the naive test finds {R['1.0']['naive']['true']:.2f} real and {R['1.0']['naive']['false']:.2f} false strategies on average. Bonferroni finds {R['1.0']['bonferroni']['true']:.2f} real and {R['1.0']['bonferroni']['false']:.3f} false; the step-down implementation finds {R['1.0']['rw']['true']:.2f} real and {R['1.0']['rw']['false']:.2f} false. <bookmark mark='b'/> At Sharpe two, their real discoveries rise to {R['2.0']['bonferroni']['true']:.2f} and {R['2.0']['rw']['true']:.2f}. Zero observed false discoveries in that finite run does not imply zero population error. <bookmark mark='c'/> The selected-rule DSR proxy exceeds point nine five in {100*R['1.0']['dsr']['pass']:.1f} and {100*R['2.0']['dsr']['pass']:.1f} percent of markets. Those are simulation frequencies, not universal posterior probabilities or error guarantees."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in rows[2:5]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in rows[2:5]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(rows[5]), FadeIn(rows[6]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lesson(self, p):
        cards = VGroup(
            desk_question(r"few observed false discoveries", r"finite simulation averages do not prove zero population error; "
                          r"theoretical control requires the relevant null and resampling assumptions", width=12.2, font_size=20),
            desk_question(r"power is low in this setup", r"a planted Sharpe ratio of one among a thousand tries is rarely "
                          r"detected by these strict procedures in this saved five-year simulation; no universal impossibility is proved", width=12.2,
                          font_size=20),
            desk_question(r"which is the case for trying fewer things", r"a narrower motivated search can lower the "
                          r"multiplicity hurdle; benefits depend on signal, dependence and how the search was chosen", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "This experiment illustrates a power tradeoff. <bookmark mark='a'/> The stricter procedures produce fewer false discoveries in the saved simulated markets. Their theoretical guarantees still require their own assumptions. <bookmark mark='b'/> At planted Sharpe one, power is low in this particular five-year search. That does not prove an information-theoretic impossibility for every method, prior or market. <bookmark mark='c'/> A narrower, well-motivated search can lower a multiplicity hurdle. Its benefit depends on dependence, signal strength and what information was used to choose the search."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"in the planted market with Sharpe ratio 1, how many years of data would Bonferroni need to find "
                r"about half of the ten real strategies? (A Sharpe ratio $SR$ over $Y$ years has $t \approx SR\sqrt{Y}$.)")
        with self.voiceover(
            "Pause and predict. In the market with a planted Sharpe ratio of one, roughly how many years of data would "
            "Bonferroni need to find about half of the ten real strategies?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
