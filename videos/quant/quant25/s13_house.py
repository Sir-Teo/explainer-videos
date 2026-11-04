from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import zoo as Z
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.byparts()
        self.sheet(load("noise"), load("zoo"), load("mtest"), load("shrink"), load("kns"), load("fgx"), load("envelope"))
        self.lab()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(12, r"Rule 25: the SDF model", r"How does the House decide a factor is real?", part=PART)
        with self.voiceover("Chapter twelve. The House's twenty-fifth rule, and the discount-factor model the research "
                            "desk now keeps."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, n, z, m, s, k, f, e):
        rows = [(r"best $t$ among 200 noise strategies", rf"\approx {n['rows'][6]['mean']:.1f}", NOISE),
                (r"Bonferroni hurdle for the zoo, 2016", rf"|t| \ge {z['hurdle'][-1]:.2f}", HURDLE),
                (r"significant after publication: raw, BH, Bonferroni", rf"{m['post']['raw']},\ {m['post']['bh']},\ "
                                                                        rf"{m['post']['bonferroni']}\ \text{{of}}\ {m['post']['n']}", BAD),
                (r"share of a premium kept: noise alone, observed", rf"{100 * s['eb']['shrink']:.0f}\%,\ {100 * s['ratio']:.0f}\%",
                 SDF),
                (r"new factors that add to the zoo (double selection)", rf"{f['sig_ds']}\ \text{{of}}\ {f['n_new']}", TRUE),
                (r"shrinkage SDF: Sharpe, research to 2021--23", rf"{e['rows']['kns_sdf_part25']['research']['sharpe']:.1f}\ "
                                                                rf"\to\ {e['rows']['kns_sdf_part25']['holdout']['sharpe']:.1f}", SDF)]
        hx = [-2.2, 3.8]
        tab = VGroup()
        for j, (a, b, col) in enumerate(rows):
            y = 2.1 - 0.62 * j
            tab.add(VGroup(label(a, font_size=19, color=col).move_to([hx[0], y, 0]), MathTex(b, font_size=26).move_to(
                [hx[1], y, 0])))
        title = label(r"The SDF model's first sheet", font_size=28).to_edge(UP, buff=0.4)
        foot = wrapped_label(r"every number computed in this part from public data, paper returns before realistic costs; "
                             r"none is a forecast, and none is advice", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> Two hundred noise strategies produce a best t near three. The zoo's "
            "own Bonferroni hurdle is three point seven. After publication, fifty-nine predictors are significant one "
            "by one, twenty-four under the false discovery rate, seven under Bonferroni. Noise alone would cost a "
            "predictor a sixth of its strength; publication cost it three fifths. Five of twenty-five new factors add "
            "anything to the zoo. And the shrinkage discount factor's paper Sharpe ratio fell from four and a half to "
            "three on unseen years, before costs."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.35), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def byparts(self):
        from explainer.quant.house import pit
        reg = pit._read()["registered"]
        parts = {}
        for k, r_ in reg.items():
            p = pit.PARTS[k][0]
            if p <= PART:  # the count as this part shows it: later parts' registrations are not yet made
                parts[p] = parts.get(p, 0) + r_["trials"]
        ps = sorted(parts)
        g = axes([-0.6, len(ps) - 0.4], [0, 2.6], x_length=9.0, y_length=4.0, xlabel=r"", ylabel=r"$\log_{10}$ trials "
                 r"registered", xticks=[], yticks=[0, 1, 2], font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        grp = VGroup()
        for i, p in enumerate(ps):
            v = np.log10(parts[p] + 1)
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            grp.add(VGroup(Rectangle(width=0.5, height=max(y1 - y0, 0.01), stroke_width=0,
                                     fill_color=SDF if p == PART else QC.HOUSE, fill_opacity=0.85).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]), MathTex(str(parts[p]), font_size=16).next_to(ax.c2p(i, v), UP, buff=0.05),
                label(rf"{p}", font_size=13, color=GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.1)))
        side = VGroup(MathTex(rf"\text{{total}}:\ {sum(parts.values())}", font_size=28, color=QC.HOUSE),
                      wrapped_label(r"configurations tried, by the part that registered them (bars labelled by part). "
                                    r"Part 3's 208 published predictors and Part 6's 49 industries dominate so far",
                                    3.2, 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Where the count comes from, part by part. <bookmark mark='a'/> Part three registered two hundred and "
            "twenty-two configurations, most of them published predictors; Part six fifty-nine, most of them "
            "industries; Part seven eleven volatility models; Part twenty-four ten factors; and this part twenty-one. Three hundred and forty-six configurations so far, every one a line of code that "
            "registered it. The research desk's claims are only as honest as this number, and it can only go up."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in grp], lag_ratio=0.1), FadeIn(side), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"The zoo, in the House", Z.kns_b, "S = np.asarray(S", 2,
                         extra=((Z.rp_pca, "mu = F.mean(0)", 3), (Z.double_selection, "s1 = np.flatnonzero", 3)), width=9.4)
        card.to_edge(UP, buff=0.6)
        with self.voiceover(
            "Three excerpts. The shrinkage discount factor: the covariance plus gamma times the identity, solved "
            "against the means; one line, one parameter. Risk-premium PCA: the second moment plus gamma times the "
            "outer product of the means, before the eigenvectors. And double selection: two lassos, and the union of "
            "what they keep. Each replaces a researcher's discretion with a rule whose choices can be counted: the "
            "shrinkage by cross-validation, the components by their number, the controls by a penalty set in advance."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("research",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{noise\_max\_t}, \texttt{bonferroni\_t}", r"the best of many, and the hurdle"),
            (r"\texttt{econ.holm}, \texttt{econ.benjamini\_hochberg}", r"step-down and false discovery"),
            (r"\texttt{eb\_shrink}", r"how much of a $t$ is noise"),
            (r"\texttt{kns\_b}, \texttt{kns\_cv}", r"the shrinkage SDF"),
            (r"\texttt{pca}, \texttt{rp\_pca}, \texttt{max\_sh2}", r"latent factors; comparing models"),
            (r"\texttt{lasso}, \texttt{double\_selection}", r"does a new factor add?"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=16, color=QC.HOUSE), label(b_, font_size=16, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.4)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 25: every claim that a factor is real states the number of tests behind it and clears "
                             r"the hurdle that number implies; every new factor is tested against the House's library, "
                             r"with selected controls, before it gets a row; expected returns come from a shrunk SDF over the "
                             r"whole library, not from the best single backtest; and every published premium is planned at a "
                             r"third to a half of its reported size, before costs.", 12.4, 19, QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The research desk's new tools. <bookmark mark='a'/> The best of many and the hurdle it implies; the "
            "step-down and false-discovery procedures; empirical-Bayes shrinkage; the shrinkage discount factor; "
            "latent factors and model comparison; and double selection. <bookmark mark='b'/> And the twenty-fifth "
            "rule. Every claim that a factor is real states the number of tests behind it, and clears the hurdle that "
            "number implies. Every new factor is tested against the House's library, with selected controls, before it "
            "gets a row. Expected returns come from a shrunk discount factor over the whole library, not from the best "
            "single backtest. And every published premium is planned at a third to a half of its reported size, "
            "before costs."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the best of 200", r"a $t$ of 2.9 found among 200 tries has an honest $p$-value near 0.3: the "
                          r"rule asks for the 200 before the 2.9", width=12.0, font_size=19),
            desk_question(r"the new factor with $t = 5$", r"spanned by the library after double selection: no new row, "
                          r"whatever its own $t$", width=12.0, font_size=19),
            desk_question(r"the published anomaly at 0.8\% a month", r"planned at 0.3--0.4\% before costs: what history "
                          r"says publication leaves", width=12.0, font_size=19),
            desk_question(r"the equal-weighted microcap effect", r"rebuilt value-weighted with NYSE breakpoints before it "
                          r"is believed; sized for its capacity if it survives", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "Hold the rule against this part's cases. <bookmark mark='a'/> The best of two hundred tries, with a t of "
            "two point nine, has an honest p-value near three tenths: the rule asks for the two hundred before the two "
            "point nine. <bookmark mark='b'/> A new factor with a t of five, spanned by the library, gets no row. "
            "<bookmark mark='c'/> A published anomaly at eight tenths of a percent a month is planned at a third to a "
            "half of that. <bookmark mark='d'/> And an equal-weighted microcap effect is rebuilt with value weights "
            "before anyone believes it. None of this needs genius. It needs the count."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
