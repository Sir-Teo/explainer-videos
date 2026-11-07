from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class Evidence(VoiceoverScene):
    def construct(self):
        self.card()
        self.framing()
        self.table()
        self.chart()
        self.calibration()
        self.lessons()

    def card(self):
        card = chapter_card(11, r"p-values and evidence", r"How strong is $p = 0.05$?", lit=(1987,), part=PART)
        with self.voiceover("Chapter eleven. p-values and evidence: how strong is a p-value of point zero five?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def framing(self):
        rows = [
            cmath(r"x \sim N(\theta, 1)", r",", r"\ H_0: \theta = 0, \ \ z = |x|, \ \ p = 2(1 - \Phi(z))", font_size=32),
            cmath(r"\pi_0 = \tfrac12 \text{ on } H_0", r",", r"\ g \text{ on } \theta \ne 0: \ \ B = \frac{\phi(z)}{\int \phi(z - \theta)\, g(d\theta)}", font_size=30),
            cmath(r"P(H_0 \mid x)", r"=", r"\big(1 + 1/B\big)^{-1}", font_size=36),
            cmath(r"\inf_{g \in \mathcal G}", r":", r"\text{the most an advocate of } H_1 \text{ could claim}", font_size=32),
        ]
        rows[2][-1].set_color(CIC)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"a two-sided test"), why(r"the Bayes factor"), why(r"equal prior odds"), why(r"Berger \& Sellke (1987)")]
        with self.voiceover(
            "<bookmark mark='a'/> James Berger and Thomas Sellke asked in 1987 what a p-value says as evidence. Take a "
            "normal observation and the point null theta equal to zero, tested two-sided. <bookmark mark='b'/> Give the null "
            "prior probability one half, and spread the other half over the alternatives by some distribution g. The Bayes "
            "factor compares the density of the data under the null with its average under g. <bookmark mark='c'/> The "
            "posterior probability of the null follows. <bookmark mark='d'/> Now minimize it over a whole class of g's: the "
            "result is the strongest case any advocate of the alternative could make from these data."
        ) as vo:
            heading=label('Posterior null probability depends on model and prior odds',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("evidence")
        rows = [[r"$p$", r"$z$", r"all $g$", r"symmetric unimodal $g$", r"normal $g$", r"$B_{\rm calib}/(1+B_{\rm calib})$"]]
        for r in d["rows"]:
            rows.append([f"{r['p']:g}", f"{r['z']:.2f}", f"{r['all']:.3f}", f"{r['symmetric']:.3f}", f"{r['normal']:.3f}", f"{r['calibration']:.3f}"])
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.32, colors=[GREY_A, None, None, None, None, None]).move_to([0, 0.8, 0])
        if tab.width > 13:
            tab.width = 13
        note_ = fit_rows(VGroup(
            label(r"lower bounds on $P(H_0 \mid x)$, \ with $P(H_0) = \tfrac12$", font_size=24, color=GREY_A),
            label(r"$p = 0.05$: \ at least 0.13, \ and 0.29 for any symmetric unimodal prior", font_size=26, color=S.ACCENT),
        ), 12.4, 0.25, [0, -2.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The normal-model bounds, at equal prior odds, for four p-values. The last column "
            "converts the separate beta-mixture p-value Bayes-factor calibration into a posterior probability. "
            "<bookmark mark='b'/> With p equal to point one, the posterior probability of the null is at least point "
            "two one over all priors, and about point four over symmetric unimodal ones. <bookmark mark='c'/> At p "
            "equal to point zero five, the famous line: at least point one three over every proper alternative prior "
            "in this specified normal model, keeping the null prior probability fixed at one half, and point two nine"
            " over symmetric unimodal priors. <bookmark mark='d'/> It takes p near point zero zero one to bring the "
            "posterior probability of the null down to the one or two percent that p equal to point zero five is "
            "often mistaken for."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_[0]), FadeIn(exact_tag(r"exact: \ one-dimensional optimization")))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]), FadeIn(note_[1]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
        self.clear_scene()

    def chart(self):
        ps = np.logspace(-4, -0.5, 60)
        from explainer.stats.kit import testing as TK

        b = [TK.berger_sellke(float(p)) for p in ps]
        lp = np.log10(ps)
        A = axes([-4, -0.5], [0, 0.6], x_length=7.4, y_length=4.4, xlabel=r"$p$", ylabel=r"lower bound on $P(H_0 \mid x)$",
                 xticks=[-4, -3, -2, -1], yticks=[0, 0.2, 0.4, 0.6], log_x=True, center=[-2.5, 0.2, 0])
        ax = A.ax
        ca = polyline(ax, lp, [r["all"] for r in b], REJC, 4)
        cs = polyline(ax, lp, [r["symmetric"] for r in b], CIC, 4)
        cn = polyline(ax, lp, [r["normal"] for r in b], UMPC, 4)
        diag = polyline(ax, lp, ps, GREY_B, 2)
        side = fit_rows(VGroup(
            label(r"red: \ over all priors", font_size=22, color=REJC),
            label(r"gold: \ symmetric unimodal priors", font_size=22, color=CIC),
            label(r"green: \ normal priors", font_size=22, color=UMPC),
            label(r"grey: \ the p-value itself", font_size=22, color=GREY_B),
            label(r"the bounds sit far above $p$: \ $p$ is not $P(H_0 \mid x)$", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> As curves, against the p-value on a log scale. In red, the bound over all priors; "
            "<bookmark mark='b'/> in gold, over symmetric unimodal priors; <bookmark mark='c'/> in green, over normal"
            " priors. <bookmark mark='d'/> In grey, the p-value itself. <bookmark mark='e'/> In the small-p region "
            "these posterior lower bounds exceed the p-value, with the displayed equal prior odds. A p-value is not a"
            " posterior probability; a different null prior weight changes posterior odds, and the all-prior curve "
            "need not exceed p across the entire plotted range."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            for k, (m_, c) in enumerate(zip("abcd", (ca, cs, cn, diag))):
                vo.wait_until(m_)
                self.play(Create(c), FadeIn(side[k]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def calibration(self):
        rows = [
            cmath(r"\text{under } H_0", r":", r"p \sim U(0, 1); \ \ \text{under } H_1: \ p \sim \mathrm{Beta}(\xi, 1), \ \xi < 1", font_size=30),
            cmath(r"B(p)", r"=", r"\frac{1}{\xi p^{\xi - 1}} \ \ge \ \min_\xi = -e\, p \log p, \ \ p < 1/e", font_size=32),
            cmath(r"p = 0.05", r":", r"B \ge 0.41, \ \ P(H_0 \mid p) \ge 0.29", font_size=34),
            cmath(r"\text{uniform null and beta-mixture alternative}", r":", r"\text{not universal for arbitrary decreasing densities}", font_size=32),
        ]
        rows[2][-1].set_color(CIC)
        rows[3][-1].set_color(UMPC)
        whys = [why(r"alternatives that favour small $p$"), why(r"Sellke, \ Bayarri \& Berger (2001)"), why(r"close to the unimodal normal bound"), why(r"assumptions on the law of $p$ required")]
        with self.voiceover(
            "<bookmark mark='a'/> A calibration with explicit assumptions on the alternative distribution of the "
            "p-value. Under the null, p is uniform; under an alternative, suppose p has a Beta xi, one distribution "
            "with xi between zero and one, or a mixture of these beta distributions. Merely having a decreasing "
            "density is not sufficient. <bookmark mark='b'/> The Bayes factor of the null against such an alternative"
            " is at least minus e times p times the log of p, for p below one over e: the calibration of Thomas "
            "Sellke, Susie Bayarri and Berger, 2001. <bookmark mark='c'/> At point zero five it gives a Bayes factor "
            "of at least point four one and a posterior probability of at least point two nine, close to, though not "
            "identical with, the symmetric-unimodal normal-model bound, with the same equal prior odds. <bookmark "
            "mark='d'/> This derivation applies to a continuous uniform null p-value and the stated beta-mixture "
            "alternative class. Discrete p-values or a different alternative class require a separate argument; it is"
            " not a universal bound for every model."
        ) as vo:
            heading=label('The p-value bound here assumes beta-mixture alternatives',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"against a point null, \ $p = 0.05$ is weak evidence: \ equal prior odds: \ at most 6.8:1 (all $g$), \ 2.45:1 (symmetric unimodal)", font_size=26),
            label(r"the bounds are for the \emph{most favourable} alternative: \ real ones are weaker still", font_size=26, color=REJC),
            label(r"Lindley's paradox \ (Part 15): \ regular $n\to\infty$, fixed $p$, fixed proper continuous alternative: \ posterior null probability can tend to 1", font_size=26, color=GREY_A),
            label(r"the ASA's statement (2016); \ proposals to use $p < 0.005$ for discoveries \ (Benjamin et al.\ 2018)", font_size=24, color=S.ACCENT),
            label(r"p-values remain valid tests: \ what they are not is a measure of the probability of $H_0$", font_size=26, color=UMPC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lesson. In this normal model at equal prior odds, p equal to point zero five "
            "allows posterior odds of about six point eight to one against the null over all alternative priors. "
            "Restricting alternatives to symmetric unimodal priors reduces the best odds to about two point four five"
            " to one. <bookmark mark='b'/> And these bounds assume the alternative most favourable to rejection; "
            "realistic alternatives give weaker evidence still. <bookmark mark='c'/> Lindley's paradox, from Part "
            "fifteen, is the extreme: in a regular increasing-information model, with fixed positive null prior "
            "weight and a fixed proper continuous alternative prior having suitable density near the null, keeping "
            "the p-value fixed can make the posterior probability of the null tend to one. This limit depends on the "
            "prior sequence. <bookmark mark='d'/> Hence the American Statistical Association's statement of 2016, and"
            " the proposal by Daniel Benjamin and some seventy co-authors to require p below point zero zero five for"
            " claims of discovery. <bookmark mark='e'/> None of this makes p-values invalid as tests: properly "
            "calibrated p-values yield tests with their advertised size or a conservative level. They are simply not "
            "the probability that the null is true."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
