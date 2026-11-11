from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, PCA_C, RP_C, SDF, TRUE, ask, fit_right, load


class PCA(VoiceoverScene):
    def construct(self):
        p = load("pca")
        self.card()
        self.scree(p)
        self.rp()
        self.pc1(p)
        self.oos(p)
        self.gamma()
        self.rms(p)
        self.ipca()
        self.lesson()

    def card(self):
        c = chapter_card(9, r"PCA, RP-PCA and IPCA", r"Can the data find the factors themselves?", lit=(2020,), part=PART)
        with self.voiceover("Chapter nine. Let the data find the factors: three ways, and what each one optimises."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def scree(self, p):
        sh = np.asarray(p["share"])[:15]
        g = axes([0.4, 15.6], [0, 0.4], x_length=7.6, y_length=4.2, xlabel=r"principal component", ylabel=r"share of "
                 r"variance", xticks=[1, 5, 10, 15], yticks=[0, 0.1, 0.2, 0.3, 0.4], font_size=13).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.4, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.005), stroke_width=0,
                                  fill_color=PCA_C, fill_opacity=0.85).move_to([ax.c2p(i + 1, 0)[0],
                                                                               (ax.c2p(0, 0)[1] + ax.c2p(0, v)[1]) / 2, 0])
                        for i, v in enumerate(sh)])
        cum = np.asarray(p["cum"])
        side = VGroup(
            MathTex(rf"\text{{first}}:\ {100 * sh[0]:.0f}\%;\ \text{{five}}:\ {100 * cum[4]:.0f}\%;\ \text{{ten}}:\ "
                    rf"{100 * cum[9]:.0f}\%", font_size=22),
            wrapped_label(rf"the covariance of {p['N']} long--short predictors, 1973--2020. A handful of directions explain "
                          r"most of how the zoo moves together; the rest is a long tail", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Start with the zoo's covariance. A hundred and fifty-four long-short portfolios, but how many independent "
            "directions? <bookmark mark='a'/> The first principal component explains a third of their variance, five "
            "explain two thirds, ten three quarters. The zoo moves as a few themes and a long tail, as Part "
            "twenty-four's thirteen themes suggested."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.05), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def rp(self):
        rows = [cmath(r"\text{PCA}:", r"\ ", r"\text{eig}\Big(\tfrac{1}{T}F^\top F - \bar\mu\bar\mu^\top\Big)", font_size=38,
                      colors={r"\text{PCA}:": PCA_C}),
                cmath(r"\text{RP-PCA}:", r"\ ", r"\text{eig}\Big(\tfrac{1}{T}F^\top F + \gamma\,\bar\mu\bar\mu^\top\Big),\ \ "
                      r"\gamma = 10", font_size=38, colors={r"\text{RP-PCA}:": RP_C})]
        whys = [why(r"PCA finds the directions of greatest variance. It never looks at average returns, so it can miss a "
                    r"direction that moves little but pays a lot: exactly the kind an SDF needs"),
                why('Lettau and Pelger (2020): add the means back with weight $\\gamma$. The components now explain both co-movement and average returns; $\\gamma=-1$ gives ML-centered covariance: same PCA eigenvectors, rescaled eigenvalues')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Ordinary PCA uses the centered covariance, so directions are ranked by variance rather than mean-return efficiency. <bookmark mark='a'/> Risk-premium PCA adds a weighted mean outer product to the second moment. Here gamma is fixed at ten in the original computation. At minus one the matrix is the centered covariance with denominator T: it has the same eigenvectors as the usual T minus one covariance, but not the same eigenvalues. Means can reveal low-variance directions, yet remain noisy and sensitive to published-universe selection."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def pc1(self, p):
        a, b = p["pca"][0], p["rp"][0]
        rows = [cmath(r"\text{PC}_1", r":", f"\\text{{a third of the variance}},\\ \\text{{later-window Sharpe}}\\ {a['sr_out']:.2f}",
                      font_size=36, colors={r"\text{PC}_1": QC.SPOT}),
                cmath(r"\text{RP-PC}_1", r":", f"\\text{{later-window Sharpe}}\\ {b['sr_out']:.2f}", font_size=36,
                      colors={r"\text{RP-PC}_1": QC.IMPLIED})]
        whys = [why('the first variance direction has a small saved later-window mean-variance score; this does not identify a unique economic risk or its population reward'),
                why('the first RP component has a higher saved later-window score; selected histories and uncertain means prevent a universal ranking of methods')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Compare the first components in the preserved split calculation. Ordinary PCA ranks variance, and its first component has little subsequent mean-variance performance in this sample. <bookmark mark='a'/> The risk-premium component has a higher saved later-window Sharpe ratio. That is a descriptive contrast, not proof that the first component is unrewarded risk or that RP-PCA discovers the true discount factor. Both inherit the complete-history and published-universe selection."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def oos(self, p):
        K = np.asarray(p["K"])
        a = np.array([r_["sr_out"] for r_ in p["pca"]])
        b = np.array([r_["sr_out"] for r_ in p["rp"]])
        g = axes([0.5, 10.5], [-0.2, 2.6], x_length=7.4, y_length=4.4, xlabel=r"number of components $K$",
                 ylabel='fixed-weight split Sharpe, 2001--2020', xticks=[1, 2, 4, 6, 8, 10], yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5],
                 font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        la = curve(ax, K, a, PCA_C, stroke_width=3)
        lb = curve(ax, K, b, RP_C, stroke_width=3)
        da = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=PCA_C) for x, y in zip(K, a)])
        db = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=RP_C) for x, y in zip(K, b)])
        side = VGroup(
            legend([(PCA_C, r"PCA"), (RP_C, r"RP-PCA, $\gamma = 10$")], font_size=17),
            MathTex(rf"K = 5:\ {a[4]:.2f}\ \text{{vs}}\ {b[4]:.2f}", font_size=24),
            wrapped_label('components estimated on 1973--2000; their tangency combination fitted then, held through 2001--2020, annualised, before costs. Complete-history universe through 2023; ten K values displayed, before implementation costs', 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The original fit uses 1973 through 2000 to estimate component weights and their tangency combination, then evaluates fixed weights in 2001 through 2020. The asset universe was selected for complete observations through 2023, so this is a retrospective split on a selected panel. <bookmark mark='a'/> The chart retains all ten component counts for ordinary PCA. <bookmark mark='b'/> It also retains all ten for gamma-ten RP-PCA. Reading the best point from these curves is another selection. Reported Sharpe ratios omit financing, borrow, trading costs and feasible capital constraints; none certifies an independent implementable winner."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(la), FadeIn(da), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(db), FadeIn(side[1]), FadeIn(side[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def gamma(self):
        cards = VGroup(
            desk_question(r"$\gamma$ is a dial", 'at $-1$, PCA; at large $\\gamma$, the first component points toward the mean vector in the chosen units; not an equal-risk portfolio. Lettau and Pelger use about 10',
                          width=12.0, font_size=20),
            desk_question('fixed in the original code', 'the original computation fixes $\\gamma=10$; this does not certify a historically blind design', width=12.0, font_size=20),
            desk_question(r"why it helps", 'the means are noisy, but averaged over many portfolios their direction is only better measured under suitable dependence and model assumptions: weak factors with large premia become visible',
                          width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Gamma controls a mean-variance trade-off. <bookmark mark='a'/> At minus one the matrix has ordinary PCA directions. For very large positive gamma the leading direction approaches the mean vector in the chosen factor units; it is not automatically equal risk. <bookmark mark='b'/> This original calculation fixes gamma at ten and does not tune it, but a fixed literal does not establish that a historical decision preceded all knowledge of the test period. <bookmark mark='c'/> Means and asset selection still use noisy published histories. Their precision depends on dependence and model structure, not simply on having many columns."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def rms(self, p):
        hx = [-3.6, -0.6, 2.2]
        heads = [r"factors", r"RMS alpha, PCA", r"RMS alpha, RP-PCA"]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=GREY_A).move_to([x, 2.0, 0]) for h_, x in zip(heads, hx)]))
        tab.add(VGroup(label(r"none (raw means)", font_size=19).move_to([hx[0], 1.4, 0]),
                       MathTex(rf"{p['rms_none']:.1f}\%", font_size=26).move_to([hx[1], 1.4, 0]),
                       MathTex(rf"{p['rms_none']:.1f}\%", font_size=26).move_to([hx[2], 1.4, 0])))
        for i, k in enumerate((1, 3, 5, 10)):
            y = 0.8 - 0.6 * i
            tab.add(VGroup(label(rf"$K = {k}$", font_size=19).move_to([hx[0], y, 0]),
                           MathTex(rf"{p['pca'][k - 1]['rms_alpha']:.1f}\%", font_size=26, color=PCA_C).move_to([hx[1], y, 0]),
                           MathTex(rf"{p['rp'][k - 1]['rms_alpha']:.1f}\%", font_size=26, color=RP_C).move_to([hx[2], y, 0])))
        foot = wrapped_label('the root-mean-square alpha of the 154 portfolios on the $K$ components, a year, in 2001--2020. Intercepts fitted on this later window; selected universe, no exact-spanning or fresh-forecast certification', 12.0, 17, GREY_A).to_edge(DOWN,
                                                                                                         buff=0.5)
        with self.voiceover(
            "The alpha table asks a different question. <bookmark mark='a'/> Component directions are trained in the earlier window, but the displayed intercepts are fitted on the later 2001 through 2020 returns themselves. These are retrospective later-window RMS intercepts, with no joint uncertainty test, rather than fully frozen out-of-sample forecasts. Smaller RMS alpha is not exact payoff spanning. The saved residual means remain material, and the universe was selected using complete observations through 2023."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def ipca(self):
        rows = [cmath(r"r_{i,t+1}", r"=", r"\alpha_{i,t} + \beta_{i,t}^\top f_{t+1} + \varepsilon_{i,t+1},\quad "
                      r"\beta_{i,t} = z_{i,t}^\top \Gamma_\beta", font_size=38, colors={r"r_{i,t+1}": SDF}),
                cmath(r"H_0:\ \Gamma_\alpha = 0", r"\iff", '\\text{no characteristic-driven alpha}', font_size=36)]
        whys = [why(r"Kelly, Pruitt and Su (2019), instrumented PCA: each stock's betas are linear in its characteristics "
                    r"$z$ (size, value, momentum, ...), estimated jointly with the latent factors $f$. Betas change as a "
                    r"firm's characteristics change"),
                why('compare characteristic-driven alpha conditionally under the model; nonrejection does not prove exact pricing, causal risk, or that characteristics literally equal covariances. No stock-level IPCA estimated here')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Instrumented PCA lets individual-stock betas be functions of observable characteristics, jointly fitted with latent factors. This is a conditional factor-model restriction, not a statement that characteristics literally equal covariances. <bookmark mark='a'/> Comparing specifications with and without characteristic-driven alpha asks a conditional empirical question under the model and inference assumptions. Nonrejection of alpha is not proof of exact pricing or a unique causal risk channel. This lecture presents the method conceptually; it does not estimate stock-level IPCA or create another market test."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def lesson(self):
        cards = VGroup(
            desk_question(r"what to optimise", r"variance (PCA), variance and means (RP-PCA), or pricing errors with "
                          r"characteristic betas (IPCA): the choice is the model", width=12.0, font_size=20),
            desk_question(r"few factors, many errors", 'higher scores for selected low-dimensional combinations do not imply exact joint pricing, a true latent model or a causal explanation of new anomaly discovery', width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Two conditional lessons. <bookmark mark='a'/> Variance, mean-return fit and characteristic-driven factor exposures define different objectives and restrictions. <bookmark mark='b'/> A low-dimensional combination can have a higher saved later-window score while leaving material intercepts. Those intercepts are fitted on the later data, and the universe is selected. The comparison does not prove a true discount factor, exact payoff spanning or a universal future winner."
        ) as vo:
            for i, mk in enumerate(("a", "b")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"why can the first principal component of the zoo, which explains a third of its variance, have almost no "
                r"average return? What does that say about using PCA to build an SDF?")
        with self.voiceover("Why can the first principal component of the zoo, which explains a third of its variance, "
                            "have almost no average return, and what does that say about using PCA to build a discount "
                            "factor?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
