from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, GOOD, HURDLE, IS_C, NOISE, OOS_C, PART, RULE, ask, comma, fit_right, load


class Deflated(VoiceoverScene):
    def construct(self):
        d = load("dsr")
        self.card()
        self.derive()
        self.neff(d)
        self.picture(d)
        self.table(d)
        self.curve_n(d["out"])
        self.question()

    def card(self):
        c = chapter_card(8, r"The deflated Sharpe ratio", r"Is the best of N better than the best of N noise?",
                         lit=(2014,), part=PART)
        with self.voiceover("Chapter eight. The deflated Sharpe ratio: one number that accounts for the selection, the "
                            "length of the backtest, and the shape of its returns."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"\widehat{SR} - SR", r"\approx", r"\mathcal{N}\Big(0,\ \tfrac{1}{T - 1}\big(1 - \gamma_3\widehat{SR} + "
                      r"\tfrac{\gamma_4 - 1}{4}\widehat{SR}^2\big)\Big)", font_size=34, colors={r"\widehat{SR} - SR": RULE}),
                cmath(r"\text{PSR}(SR_0)", r"=", r"\Phi\!\left(\frac{(\widehat{SR} - SR_0)\sqrt{T - 1}}{\sqrt{1 - \gamma_3"
                      r"\widehat{SR} + \frac{\gamma_4 - 1}{4}\widehat{SR}^2}}\right)", font_size=34,
                      colors={r"\text{PSR}(SR_0)": GOOD}),
                cmath(r"SR_0", r"=", r"\sqrt{V}\,\Big[(1 - \gamma)\,\Phi^{-1}\!\big(1 - \tfrac1N\big) + \gamma\,\Phi^{-1}"
                      r"\!\big(1 - \tfrac{1}{Ne}\big)\Big]", font_size=34, colors={r"SR_0": HURDLE}),
                cmath(r"\text{DSR}", r"=", r"\text{PSR}\big(SR_0\big)", font_size=40, colors={r"\text{DSR}": BAD})]
        whys = [why(r"chapter 5's error, per period, with the sample's skewness and kurtosis"),
                why(r"the probabilistic Sharpe ratio: the probability that the true Sharpe ratio exceeds a benchmark "
                    r"$SR_0$, given the estimate (Bailey and Lopez de Prado 2012)"),
                why(r"the benchmark that accounts for selection: chapter 3's expected best of $N$ trials, with $V$ the "
                    r"variance of the trials' own Sharpe ratios"),
                why(r"the deflated Sharpe ratio (Bailey and Lopez de Prado 2014): the probability that the chosen strategy "
                    r"beats the best that $N$ zero-skill tries would show. Above 0.95, believe it a little")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.5, buff=0.28, edge=6.9)
        with self.voiceover(
            "Put chapters three and five together. <bookmark mark='a'/> The estimated Sharpe ratio is close to normal "
            "around the true one, with the variance from chapter five, skewness and kurtosis included. <bookmark "
            "mark='b'/> So the probability that the true Sharpe ratio exceeds some benchmark, S R nought, is a normal "
            "probability: the probabilistic Sharpe ratio, which David Bailey and Marcos Lopez de Prado proposed in 2012. "
            "<bookmark mark='c'/> The question is which benchmark. Not zero, if the strategy was chosen from N tries: "
            "the benchmark is the best that N zero-skill tries would show, chapter three's formula, scaled by the "
            "spread V of the tries' own Sharpe ratios. <bookmark mark='d'/> The probabilistic Sharpe ratio against "
            "that benchmark is the deflated Sharpe ratio. It asks one honest question: is the winner better than the "
            "best of N that had no skill?"
        ) as vo:
            step(0)
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

    def neff(self, d):
        a = d["in"]
        rows = [cmath(r"N_{\text{eff}}", r"\approx", r"N\cdot\frac{1}{M}\frac{\big(\sum_k \lambda_k\big)^2}{\sum_k \lambda_k^2}",
                      font_size=38, colors={r"N_{\text{eff}}": HURDLE})]
        rows[0].to_edge(UP, buff=0.8)
        w = why(r"the participation ratio of the eigenvalues $\lambda_k$ of the trials' correlation matrix (here from "
                r"$M = 1{,}500$ sampled rules): $M$ if they were independent, 1 if they were all the same trial").next_to(
            rows[0], DOWN, buff=0.3)
        vals = VGroup(
            MathTex(rf"N = {comma(a['n'])}\ \to\ N_{{\text{{eff}}}} \approx {a['n_eff']:.0f}\ \ (1926\text{{--}}86)",
                    font_size=32, color=IS_C),
            MathTex(rf"N = {comma(d['out']['n'])}\ \to\ N_{{\text{{eff}}}} \approx {d['out']['n_eff']:.0f}\ \ "
                    rf"(1987\text{{--}}2020)", font_size=32, color=OOS_C),
            MathTex(rf"\sqrt{{V}} = {a['sd_trials_ann']:.2f}\ \ \text{{a year, against}}\ \ "
                    rf"{1 / np.sqrt(a['T'] / 252):.2f}\ \text{{for independent noise}}", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(w, DOWN, buff=0.5)
        with self.voiceover(
            "Two inputs need care. The first is N. <bookmark mark='a'/> Ten thousand rules are not ten thousand "
            "independent tries: rules that differ by a day trade almost alike. One estimate of the effective number "
            "comes from the eigenvalues of the rules' correlation matrix, their participation ratio, which is the "
            "full count if the rules are independent and one if they are all the same rule. <bookmark mark='b'/> For "
            "these rules it is under two percent of the count: about a hundred and seventy-five independent tries in "
            "the first era, a hundred and fifty-five in the second. <bookmark mark='c'/> The second input is V, the "
            "spread of the trials' Sharpe ratios. For these rules it is point one nine a year, larger than pure noise "
            "would give, because the rules really differ: some were long the market more often than others."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(w))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(vals[0]), FadeIn(vals[1]))
            vo.wait_until("c")
            self.play(FadeIn(vals[2]))
        self.wait(0.4)
        self.clear_scene()

    def picture(self, d):
        e = np.linspace(-1.5, 2.0, 71)
        c = (e[:-1] + e[1:]) / 2
        panels = VGroup()
        for era, title, col in (("in", r"1926--1986", IS_C), ("out", r"1987--2020", OOS_C)):
            a = d[era]
            h = np.asarray(a["sr_hist"], float)
            top = h.max() * 1.15
            g = axes([-1.5, 2.0], [0, top], x_length=5.6, y_length=3.3, xlabel=r"rules' Sharpe ratios", ylabel=r"rules",
                     xticks=[-1, 0, 1, 2], yticks=[], font_size=12)
            ax = g.ax
            w = ax.c2p(e[1], 0)[0] - ax.c2p(e[0], 0)[0]
            bars = VGroup(*[Rectangle(width=w * 0.9, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                      fill_color=col, fill_opacity=0.5).move_to(
                [ax.c2p(x, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for x, v in zip(c, h) if v > 0])
            sr0 = a["eff"]["sr0"]
            l0 = DashedLine(ax.c2p(sr0, 0), ax.c2p(sr0, top), color=HURDLE, stroke_width=2.5)
            lb = Line(ax.c2p(a["sr_best"], 0), ax.c2p(a["sr_best"], top * 0.8), color=BAD if a["eff"]["dsr"] < 0.95
                      else GOOD, stroke_width=3)
            cap = VGroup(label(title, font_size=20, color=col),
                         MathTex(rf"\text{{best}}\ {a['sr_best']:.2f}\ \text{{vs hurdle}}\ {sr0:.2f}", font_size=22)
                         ).arrange(RIGHT, buff=0.3)
            panels.add(VGroup(cap, VGroup(g, bars, l0, lb)).arrange(DOWN, buff=0.15))
        panels.arrange(RIGHT, buff=0.6).move_to(UP * 0.1)
        foot = wrapped_label(r"gold dashed: the expected best of $N_{\text{eff}}$ zero-skill tries with the trials' own spread; "
                             r"solid: the winner. Both annualised", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here are the two eras as the deflated Sharpe ratio sees them: the rules' Sharpe ratios, the hurdle, and "
            "the winner. <bookmark mark='a'/> Before 1987 the winner, at one point six seven, is far beyond the hurdle "
            "of about a half. <bookmark mark='b'/> After 1986, the best rule is a slow one, a two-hundred against "
            "two-hundred-and-fifty-day average with a fifty-day hold, at point five six. Its hurdle is point four four. "
            "It clears it, but not by much."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def table(self, d):
        a, b = d["in"], d["out"]
        head = VGroup(*[label(h, font_size=18, color=GREY_A) for h in (r"", r"1926--1986", r"1987--2020")])
        data = [
            (r"the winner", label(a["label"].replace("%", r"\%"), font_size=15), label(b["label"].replace("%", r"\%"),
                                                                                      font_size=15)),
            (r"its Sharpe ratio", MathTex(f"{a['sr_best']:.2f}", font_size=24), MathTex(f"{b['sr_best']:.2f}", font_size=24)),
            (r"PSR against zero", MathTex(f"{a['psr0']:.4f}", font_size=24), MathTex(f"{b['psr0']:.4f}", font_size=24)),
            (r"DSR, $N = 10{,}000$", MathTex(f"{a['raw']['dsr']:.2f}", font_size=24, color=GOOD),
             MathTex(f"{b['raw']['dsr']:.2f}", font_size=24, color=BAD)),
            (r"DSR, $N_{\text{eff}}$", MathTex(f"{a['eff']['dsr']:.2f}", font_size=24, color=GOOD),
             MathTex(f"{b['eff']['dsr']:.2f}", font_size=24, color=BAD)),
        ]
        rows = [head] + [VGroup(label(t, font_size=19, color=RULE), x, y) for t, x, y in data]
        xs = [-4.2, 0.4, 4.4]
        for j, row in enumerate(rows):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 2.3 - 0.75 * j, 0])
            row[0].align_to([xs[0] - 1.9, 0, 0], LEFT)
        tab = VGroup(*rows)
        foot = wrapped_label(r"before 1987 the winner passes every test of selection. After, its nominal $p$-value is "
                             r"0.0006 and it fails the deflated test however $N$ is counted: it is about what the best of "
                             r"that many noise rules would show", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The verdict. <bookmark mark='a'/> Before 1987 the winner passes everything: its probabilistic Sharpe ratio "
            "against zero is one, and deflated for ten thousand tries, or for the effective hundred and seventy-five, it "
            "is still one. Whatever the rules found, they did not find it by searching. <bookmark mark='b'/> After 1986 "
            "the winner's probability of beating zero is point nine nine nine four, a nominal p-value of six in ten "
            "thousand. Deflated for ten thousand tries it is point three five; for the effective number, point seven six. "
            "Neither reaches point nine five. The best rule of the modern era is about what the best of that many noise "
            "rules would look like."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_[0]) for r_ in rows[1:]], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(r_[1]) for r_ in rows[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in rows[1:]], lag_ratio=0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def curve_n(self, b):
        grid, dc = np.log10(np.asarray(b["grid"])), np.asarray(b["dsr_curve"])
        g = axes([0, 4], [0, 1.02], x_length=7.4, y_length=4.0, xlabel=r"$N$ the winner is deflated for",
                 ylabel=r"deflated Sharpe ratio of the 1987--2020 winner", xticks=[0, 1, 2, 3, 4], yticks=[0, 0.5, 0.95],
                 log_x=True, font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, grid, dc, OOS_C, stroke_width=3)
        bar = DashedLine(ax.c2p(0, 0.95), ax.c2p(4, 0.95), color=HURDLE, stroke_width=2)
        n95 = float(10 ** np.interp(-0.95, -dc, grid))
        mark = VGroup(Dot(ax.c2p(np.log10(n95), 0.95), color=BAD, radius=0.08),
                      MathTex(rf"N \approx {n95:.0f}", font_size=24, color=BAD).next_to(ax.c2p(np.log10(n95), 0.95), DR,
                                                                                    buff=0.1))
        side = wrapped_label(r"a Sharpe ratio of 0.56 over 34 years, chosen from $N$ independent tries. It is convincing "
                             r"only if fewer than about a dozen were tried", 3.4, 16, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Read it as a function of N. <bookmark mark='a'/> This rule's thirty-four-year Sharpe ratio of point five "
            "six would pass the deflated test if it had been chosen from about a dozen independent tries or fewer. Chosen "
            "from more, it is what selection would produce. The same number means different things depending on a "
            "fact that is not in the backtest at all: how many tries came before it. That is why the House writes the "
            "number down."
        ) as vo:
            self.play(FadeIn(g), Create(bar))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(mark), FadeIn(side), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"two strategies both show a Sharpe ratio of 1.5 over six years. One was the only idea its author "
                r"tested; the other was the best of 500. Their returns' skewness is $-2$ and $0$. Rank them.")
        with self.voiceover(
            "Pause and predict. Two strategies each show a Sharpe ratio of one and a half over six years. One was "
            "the only idea its author tested; the other the best of five hundred. The first has skewness of minus two, "
            "the second of zero. Rank them."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
