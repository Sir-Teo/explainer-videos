from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, GOOD, HML, MKT, PART, SMB, ask, fit_right, illustration, load


def grid(vals, lo, hi, cell=0.78, font_size=20, fmt="{:.1f}", diverging=False):
    """A 5 x 5 grid of the size (rows, small at top) by book-to-market (columns, growth at left) portfolios, coloured
    by value."""
    v = np.asarray(vals, float).reshape(5, 5)
    g = VGroup()
    for i in range(5):
        for j in range(5):
            x = (v[i, j] - lo) / (hi - lo)
            x = min(max(x, 0.0), 1.0)
            if diverging:
                col = ManimColor(BAD) if x >= 0.5 else ManimColor(QC.SPOT)
                op = 0.15 + 0.75 * abs(2 * x - 1)
            else:
                col, op = ManimColor(QC.IMPLIED), 0.12 + 0.78 * x
            sq = Square(cell, stroke_width=1, stroke_color=GREY_D, fill_color=col, fill_opacity=op)
            sq.move_to([j * cell, -i * cell, 0])
            g.add(VGroup(sq, MathTex(fmt.format(v[i, j]), font_size=font_size).move_to(sq)))
    rows = VGroup(*[label(t, font_size=14, color=GREY_A).next_to(g[5 * i], LEFT, buff=0.12)
                    for i, t in enumerate((r"small", r"2", r"3", r"4", r"big"))])
    cols = VGroup(*[label(t, font_size=14, color=GREY_A).next_to(g[j], UP, buff=0.1)
                    for j, t in enumerate((r"growth", r"2", r"3", r"4", r"value"))])
    out = VGroup(g, rows, cols)
    out.cells = g
    return out


class Tests(VoiceoverScene):
    def construct(self):
        t = load("tests")
        self.card()
        self.portfolios(t)
        self.timeseries()
        self.grs_geometry()
        self.fm()
        self.results(t)
        self.alphas(t)
        self.scatter(t)
        self.lesson()

    def card(self):
        c = chapter_card(1, r"Testing a factor model", r"How would you know a model is wrong?", lit=(1973, 1989), part=PART)
        with self.voiceover("Chapter one. Before any factor, the tests every factor model must pass, and the "
                            "twenty-five portfolios it is tested on."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def portfolios(self, t):
        gr = grid(np.asarray(t["mean"]) * 100, 4, 13).to_edge(LEFT, buff=1.2).shift(DOWN * 0.2)
        title = label(r"average excess return, \% a year", font_size=20).next_to(gr, UP, buff=0.5)
        side = VGroup(
            wrapped_label('eligible NYSE, AMEX and Nasdaq stocks with required accounting data, sorted each June into five size groups by NYSE breakpoints and, independently, five book-to-market groups; 25 value-weighted portfolios, monthly, July 1963 to December 2020', 4.4, 17, GREY_A),
            MathTex(r"\text{small value}: 12.7\%,\quad \text{small growth}: 4.3\%", font_size=24, color=HML),
            wrapped_label(r"returns rise from growth to value in every size row, and from big to small in most value "
                          r"columns, while betas barely differ. The one cell that breaks the pattern is small growth",
                          4.4, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "Here are the test assets of half a century of research. Eligible NYSE, AMEX and Nasdaq stocks with required accounting data, sorted each June into five groups by size and, independently, five by the ratio of book equity to market value: twenty-five portfolios. <bookmark mark='a'/> Their average returns above bills, 1963 to 2020. Read across any row and returns rise from growth to value; read down most columns and they fall from small to large. Small value stocks earned almost thirteen percent a year; small growth stocks four. <bookmark mark='b'/> And their market betas are all close to one. The CAPM cannot tell these portfolios apart, and the data can. A good model must explain this grid."
        ) as vo:
            self.play(FadeIn(title), LaggedStart(*[FadeIn(c_) for c_ in gr[0]], lag_ratio=0.04), FadeIn(gr[1:]),
                      FadeIn(side[0]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), Indicate(gr.cells[4], color=HML), Indicate(gr.cells[0], color=BAD))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.add(illustration(r"Kenneth French's data library: 25 portfolios formed on size and book-to-market"))
        self.wait(0.4)
        self.clear_scene()

    def timeseries(self):
        rows = [cmath(r"R^e_{it}", r"=", r"\alpha_i + \beta_i^\top f_t + \varepsilon_{it},\qquad H_0:\ \alpha_1 = \dots = "
                      r"\alpha_N = 0", font_size=36, colors={r"R^e_{it}": MKT}),
                cmath(r"J", r"=", r"\frac{T - N - K}{N}\;\frac{\hat\alpha^\top \hat\Sigma^{-1} \hat\alpha}{1 + \bar f^\top "
                      r"\hat\Omega^{-1} \bar f}\ \sim\ F_{N,\,T-N-K}", font_size=38, colors={r"J": BAD})]
        whys = [why(r"if the factors are excess returns, the model's only prediction is that each portfolio's intercept "
                    r"is zero: the factors' premia, times the betas, explain everything"),
                why("Gibbons, Ross and Shanken (1989): the alphas weighted by the residual covariance $\\Sigma$, scaled by the factors' own squared Sharpe ratio; theory: ML covariances, iid Gaussian homoskedastic errors, full rank and $T>N+K$. Saved mixed-convention outputs below are proxies")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "First, regress test-asset excess returns on traded factors and test jointly whether their intercepts vanish. <bookmark mark='a'/> Standard GRS weights the alphas by residual precision and divides by one plus factor squared Sharpe. Its exact F calibration requires maximum-likelihood residual and factor covariances, independent Gaussian homoskedastic errors, full rank and enough observations. The preserved library instead mixes covariance denominators. Its saved F and p entries are legacy proxies, not exactly calibrated standard GRS results; no corrected market regression is substituted."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def grs_geometry(self):
        rows = [cmath(r"\hat\alpha^\top \hat\Sigma^{-1} \hat\alpha", r"=", r"SR^2(f,\,R) - SR^2(f)", font_size=42,
                      colors={r"\hat\alpha^\top \hat\Sigma^{-1} \hat\alpha": BAD})]
        whys = [why('with matching moments and unrestricted portfolios, the numerator is the gain in maximum squared Sharpe. This geometry does not establish exact payoff spanning, and statistical nonrejection does not prove efficiency')]
        step = ladder(self, rows, whys, keep=1, top=2.3, x=-0.4, buff=0.8, edge=6.9)
        cards = VGroup(
            desk_question(r"what it rewards", r"a model whose factors are mean--variance efficient among all the assets",
                          width=12.0, font_size=20),
            desk_question(r"what it punishes", r"small alphas on portfolios with tiny residual risk: they could be "
                          r"levered into a high Sharpe ratio", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "With matching moment conventions and unrestricted weights, alpha times inverse residual covariance times alpha is the gain in maximum squared Sharpe from adding test assets. <bookmark mark='a'/> The gain identity has no extra factor-Sharpe denominator; that denominator belongs in the GRS statistic. Small alphas with tiny residual variance can create a large gain. Nonrejection does not prove the factors are efficient, nor that all residual payoffs are spanned."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()

    def fm(self):
        rows = [cmath(r"R^e_{it}", r"=", r"\gamma_{0t} + \gamma_t^\top \hat\beta_i + u_{it}\quad\text{each month } t",
                      font_size=38, colors={r"R^e_{it}": MKT}),
                cmath(r"\hat\lambda", r"=", '\\frac{1}{T}\\textstyle\\sum_t \\hat\\gamma_t,\\quad \\widehat{se}_{FM,j}=\\frac{\\operatorname{sd}(\\hat\\gamma_{jt})}{\\sqrt T}\\quad\\text{(iid slope benchmark)}', font_size=34, colors={r"\hat\lambda": GOOD})]
        whys = [why(r"Fama and MacBeth (1973): the second test runs across assets. Each month, regress the cross-section "
                    r"of returns on the betas; the slope is that month's reward for each unit of beta"),
                why('fixed full-sample betas, monthly cross-sectional slopes: the iid slope benchmark is shown. Saved extra covariance inflation is a legacy proxy, not formal Shanken, HAC or multiple-test inference')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Second, regress each month's asset returns across their estimated betas, then average the slopes. Here the betas come from the full sample, not a rolling out-of-sample exercise. <bookmark mark='a'/> Slope variation gives an iid benchmark standard error. The saved library inflates that covariance and adds factor variance again; under the usual traded-factor setup, that variance is already present. Its reported adjusted t values are legacy proxies, not formal Shanken or serial-dependence-robust inference. Statistical significance alone does not identify a causal factor."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def results(self, t):
        hx = [-4.6, -2.0, 0.4, 3.2]
        heads = [r"model", 'legacy $J$', 'proxy $p$', r"average $|\alpha|$, a year"]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=GREY_A).move_to([x, 2.3, 0]) for h_, x in zip(heads, hx)]))
        names = {"CAPM": r"CAPM (market)", "FF3": r"Fama--French three", "Carhart": r"Carhart four (+ momentum)",
                 "FF5": r"Fama--French five"}
        for i, k in enumerate(("CAPM", "FF3", "Carhart", "FF5")):
            m = t["models"][k]
            y = 1.6 - 0.62 * i
            pv = r"< 10^{-5}" if m["p"] < 1e-5 else f"{m['p']:.4f}"
            tab.add(VGroup(label(names[k], font_size=19).move_to([hx[0], y, 0]),
                           MathTex(f"{m['grs']:.2f}", font_size=26).move_to([hx[1], y, 0]),
                           MathTex(pv, font_size=26, color=BAD).move_to([hx[2], y, 0]),
                           MathTex(rf"{100 * m['mean_abs_alpha']:.1f}\%", font_size=26,
                                   color=GOOD if m["mean_abs_alpha"] < 0.015 else BAD).move_to([hx[3], y, 0])))
        foot = wrapped_label('the 25 size--value portfolios, July 1963 to December 2020 (690 months). Legacy covariance conventions: proxy $J,p$, not exact GRS calibration. Size and value reduce average absolute alpha in this narrow test-asset set', 12.0, 17, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Preserve the original twenty-five-portfolio results, July 1963 through December 2020. <bookmark mark='a'/> The CAPM's mean absolute annual alpha is two point three percent; three factors reduce it to one point one, and later factors to about one percent. <bookmark mark='b'/> All saved proxy p values are small. Their mixed covariance convention prevents exact GRS interpretation. Rejection is not inevitable with a long sample; assess statistical assumptions, economic errors and the narrow size-value test assets separately."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab[1:]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def alphas(self, t):
        a1 = grid(np.asarray(t["models"]["CAPM"]["alpha"]) * 100, -6, 6, cell=0.66, font_size=17, diverging=True)
        a3 = grid(np.asarray(t["models"]["FF3"]["alpha"]) * 100, -6, 6, cell=0.66, font_size=17, diverging=True)
        a5 = grid(np.asarray(t["models"]["FF5"]["alpha"]) * 100, -6, 6, cell=0.66, font_size=17, diverging=True)
        grp = VGroup(a1, a3, a5).arrange(RIGHT, buff=0.9).shift(DOWN * 0.3)
        heads = VGroup(*[label(h_, font_size=20).next_to(g_, UP, buff=0.45) for h_, g_ in
                         zip((r"CAPM alphas", r"three-factor alphas", r"five-factor alphas"), (a1, a3, a5))])
        foot = wrapped_label(r"\% a year; red positive, blue negative. Small growth stocks earn 5.5\% a year less than "
                             r"either of the first two models predicts, and 3.3\% less than the five-factor model: the "
                             r"anomaly every model leaves behind", 12.4, 17, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where the models fail, cell by cell. <bookmark mark='a'/> Under the CAPM the alphas line up with value: "
            "red on the right, the cheap stocks earning up to five percent a year more than their betas predict. "
            "<bookmark mark='b'/> With size and value as factors, most of the grid goes pale. <bookmark mark='c'/> One "
            "corner does not. Small growth stocks earn about five and a half percent a year less than either model "
            "predicts, and still more than three percent less under five factors. Small, expensive, often unprofitable "
            "and issuing shares: the corner every model leaves behind, and chapter five returns to it."
        ) as vo:
            self.play(FadeIn(a1), FadeIn(heads[0]))
            vo.wait_until("a")
            self.play(Indicate(a1, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(a3), FadeIn(heads[1]))
            vo.wait_until("c")
            self.play(FadeIn(a5), FadeIn(heads[2]), FadeIn(foot))
            self.play(*[Indicate(g_.cells[0], color=BAD) for g_ in (a1, a3, a5)])
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, t):
        mean = np.asarray(t["mean"]) * 100
        panels = VGroup()
        for k, ttl in (("CAPM", r"CAPM"), ("FF3", r"three factors")):
            pred = np.asarray(t["models"][k]["pred"]) * 100
            g = axes([2, 14], [2, 14], x_length=4.6, y_length=4.0, xlabel=r"predicted, \% a year",
                     ylabel=r"average, \% a year", xticks=[4, 8, 12], yticks=[4, 8, 12], font_size=13)
            ax = g.ax
            diag = DashedLine(ax.c2p(2, 2), ax.c2p(14, 14), color=GREY_B, stroke_width=1.5)
            dots = VGroup(*[Dot(ax.c2p(p, m), radius=0.06, color=HML if (i % 5) == 4 else
                                (BAD if i == 0 else MKT)) for i, (p, m) in enumerate(zip(pred, mean))])
            panels.add(VGroup(g, diag, dots, label(ttl, font_size=20).next_to(g, UP, buff=0.15)))
        panels.arrange(RIGHT, buff=1.0).shift(DOWN * 0.3)
        foot = wrapped_label(r"each dot one of the 25 portfolios: on the line, the model prices it. Under the CAPM the "
                             r"predictions bunch in a narrow band while the averages spread from 4\% to 13\%",
                             12.0, 17, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Another view: each portfolio's average return against the model's prediction. <bookmark mark='a'/> Under "
            "the CAPM the predictions bunch in a narrow band, because the betas hardly differ, while the averages range "
            "from four percent to thirteen: a vertical smear. <bookmark mark='b'/> Under three factors the dots fall "
            "close to the line, value portfolios in orange at the top right, with the small growth portfolio in red "
            "well below it."
        ) as vo:
            self.play(FadeIn(panels[0]))
            vo.wait_until("a")
            self.play(Indicate(panels[0], scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lesson(self):
        cards = VGroup(
            desk_question(r"time series or cross-section?", 'with traded factors, expected alphas restrict mean returns. Exact standard GRS requires matching ML covariance and iid Gaussian assumptions; saved mixed-convention outputs are proxies', width=12.0, font_size=20),
            desk_question(r"which test assets?", r"sorting on size and value builds in the answer for the Fama--French "
                          r"model: Lewellen, Nagel and Shanken (2010) ask for industries and other sorts too", width=12.0,
                          font_size=20),
            desk_question(r"how false, not whether", 'long samples do not inevitably reject; compare economic pricing errors, opportunity sets, assumptions and new validation, with selection-aware inference', width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Three lessons for using these tests. <bookmark mark='a'/> With factors that are traded portfolios, the "
            "time-series alphas are the test; the cross-sectional regression adds a free intercept, and asks whether "
            "each premium matches the factor's own mean. <bookmark mark='b'/> Choose the test assets with care: sorting "
            "on size and value builds the answer into the question, and Jonathan Lewellen, Stefan Nagel and Jay Shanken "
            "asked for industries and other sorts as well. <bookmark mark='c'/> And ask how false a model is, not "
            "whether: compare pricing errors, or the squared Sharpe ratio each model's factors can reach."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a model's GRS test rejects with $p = 0.001$, but its average absolute alpha is 0.3\% a year. Would you use "
                r"it? What would you check?")
        with self.voiceover("A model is rejected with a p-value of one in a thousand, but its average pricing error is "
                            "three tenths of a percent a year. Would you use it, and what would you check?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
