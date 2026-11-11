from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import zoo as Z
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.byparts()
        self.sheet(load("noise"), load("zoo"), load("mtest"), load("shrink"), load("kns"), load("fgx"))
        self.lab()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(12, r"Rule 25: the SDF model", r"How does the House decide a factor is real?", part=PART)
        with self.voiceover("Chapter twelve. The House's twenty-fifth rule, and the discount-factor model the research "
                            "desk now keeps."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, n, z, m, s, k, f):
        rows = [(r"best $t$ among 200 noise strategies", rf"\approx {n['rows'][6]['mean']:.1f}", NOISE),
                (r"Bonferroni hurdle for the zoo, 2016", rf"|t| \ge {z['hurdle'][-1]:.2f}", HURDLE),
                (r"significant after publication: raw, BH, Bonferroni", rf"{m['post']['raw']},\ {m['post']['bh']},\ "
                                                                        rf"{m['post']['bonferroni']}\ \text{{of}}\ {m['post']['n']}", BAD),
                ('distinct diagnostics: EB slope; mean-return ratio', rf"{100 * s['eb']['shrink']:.0f}\%,\ {100 * s['ratio']:.0f}\%",
                 SDF),
                ('heuristic DS loading t above 1.96', rf"{f['sig_ds']}\ \text{{of}}\ {f['n_new']}", TRUE),
                (r"sealed experiment in this review", r"\text{not opened or scored}", SDF)]
        hx = [-2.2, 3.8]
        tab = VGroup()
        for j, (a, b, col) in enumerate(rows):
            y = 2.1 - 0.62 * j
            tab.add(VGroup(label(a, font_size=19, color=col).move_to([hx[0], y, 0]), MathTex(b, font_size=26).move_to(
                [hx[1], y, 0])))
        title = label(r"The SDF model's first sheet", font_size=28).to_edge(UP, buff=0.4)
        foot = wrapped_label('saved public-data diagnostics and fixed simulations; research returns before realistic costs, not a forecast or advice', 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The sheet separates saved diagnostics from certified discoveries. <bookmark mark='a'/> The noise maximum is simulated. Bonferroni and BH counts use approximate mean t p-values; their formal guarantees require valid null calibration and appropriate dependence conditions. The empirical-Bayes slope and observed return-retention ratio are different quantities. Five simplified double-selection loadings cross the nominal threshold, without formal inference certification. The sealed experiment remains unopened and unscored in this review."
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
        g = axes([-0.6, len(ps) - 0.4], [0, 2.6], x_length=9.0, y_length=4.0, xlabel=r"", ylabel='$\\log_{10}(1+\\mathrm{trials})$', xticks=[], yticks=[0, 1, 2], font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
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
            f"The bars show the existing registered trials by part, using log ten of one plus the count. <bookmark mark='a'/> The total through Part twenty-five is {sum(parts.values())}. This review adds zero registrations or market trials. The historical ledger records its own declared configurations; it does not enumerate every unpublished search or every inherited choice in the public predictors. A local count is useful accounting, not proof that selection or information leakage has been eliminated."
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
        rule = wrapped_label('Rule 25: disclose the search family and inherited selection; calibrate error rates under explicit assumptions; compare candidate exposure conditionally; shrink with stated priors and validation limits; distinguish gross research returns, sensitivity scenarios and feasible net implementation.', 12.4, 19, QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The desk's tools include maxima, familywise corrections, BH, conditional empirical Bayes, ridge, latent factors and simplified selection. <bookmark mark='a'/> A tool's name does not certify valid p-values, independence, identification or implementation. <bookmark mark='b'/> Rule twenty-five is to disclose the search and inherited selection, state the calibration assumptions, compare exposures conditionally, and report prior and validation choices. Distinguish gross research returns from cost scenarios and feasible net performance. A local count or a one-third retention scenario cannot replace a genuinely separated evaluation."
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
            desk_question(r"the best of 200", 'independent normal-reference selected p near 0.3; actual calibration requires the declared search and dependence model', width=12.0, font_size=19),
            desk_question(r"the new factor with $t = 5$", 'nonrejection of a simplified loading does not establish exact spanning or no incremental investor value', width=12.0, font_size=19),
            desk_question(r"the published anomaly at 0.8\% a month", '0.3--0.4\\% before costs is a sensitivity scenario, not a calibrated universal forecast', width=12.0, font_size=19),
            desk_question(r"the equal-weighted microcap effect", 'compare construction, uncertainty, liquidity, costs and capacity; a different weighting estimates a different portfolio', width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "Apply the qualified rule. <bookmark mark='a'/> A best t of two point nine among two hundred has a selected normal-reference p-value near three tenths only under the stated independent normal search model. <bookmark mark='b'/> An insignificant simplified loading does not prove exact spanning or no incremental utility. <bookmark mark='c'/> A one-third to one-half return-retention assumption is a sensitivity scenario, not a universal forecast. <bookmark mark='d'/> Comparing equal and value weights asks about different portfolios; assess uncertainty, costs and feasibility. Counting is necessary documentation, but it does not replace these assumptions."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
