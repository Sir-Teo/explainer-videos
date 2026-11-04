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
        self.oos(p)
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
                why(r"Lettau and Pelger (2020): add the means back with weight $\gamma$. The components now explain both "
                    r"co-movement and average returns; $\gamma = -1$ is ordinary PCA")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "But PCA only looks at variance. It never sees average returns, so it can miss a direction that moves "
            "little and pays a lot, which is exactly what a discount factor needs. <bookmark mark='a'/> Martin Lettau "
            "and Markus Pelger's fix, risk-premium PCA: before taking eigenvectors, add the outer product of the mean "
            "returns, weighted by gamma. The components must now explain both how the portfolios move together and "
            "what they earn on average."
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
                 ylabel=r"out-of-sample Sharpe, 2001--2020", xticks=[1, 2, 4, 6, 8, 10], yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5],
                 font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        la = curve(ax, K, a, PCA_C, stroke_width=3)
        lb = curve(ax, K, b, RP_C, stroke_width=3)
        da = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=PCA_C) for x, y in zip(K, a)])
        db = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=RP_C) for x, y in zip(K, b)])
        side = VGroup(
            legend([(PCA_C, r"PCA"), (RP_C, r"RP-PCA, $\gamma = 10$")], font_size=17),
            MathTex(rf"K = 5:\ {a[4]:.2f}\ \text{{vs}}\ {b[4]:.2f}", font_size=24),
            wrapped_label(r"components estimated on 1973--2000; their tangency combination fitted then, held through "
                          r"2001--2020, annualised, before costs. With the means in the objective, a few components "
                          r"capture far more of what the zoo pays", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Test it out of sample. Estimate the components on 1973 to 2000, combine them into their tangency portfolio "
            "then, and hold it through 2020. <bookmark mark='a'/> With ordinary PCA, the out-of-sample Sharpe ratio "
            "stays below one even with ten components: the big-variance directions are not the ones that pay. "
            "<bookmark mark='b'/> With risk-premium PCA, four components already pass one and a half, and five reach "
            "two. A few well-chosen directions capture most of what the zoo earns."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(la), FadeIn(da), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(db), FadeIn(side[1]), FadeIn(side[2]), run_time=1.5)
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
        foot = wrapped_label(r"the root-mean-square alpha of the 154 portfolios on the $K$ components, a year, in 2001--2020. "
                             r"Even ten components leave most of the zoo's out-of-sample pricing errors: the zoo is not "
                             r"explained by a few factors, only its best combination is", 12.0, 17, GREY_A).to_edge(DOWN,
                                                                                                         buff=0.5)
        with self.voiceover(
            "But pricing the whole zoo is harder than earning its best combination. <bookmark mark='a'/> The "
            "root-mean-square alpha of the hundred and fifty-four portfolios, out of sample: about five percent a year "
            "with no factors; with ten components, still about four, by either method. A few components capture the "
            "zoo's best portfolio, not every portfolio's average return."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def ipca(self):
        rows = [cmath(r"r_{i,t+1}", r"=", r"\alpha_{i,t} + \beta_{i,t}^\top f_{t+1} + \varepsilon_{i,t+1},\quad "
                      r"\beta_{i,t} = z_{i,t}^\top \Gamma_\beta", font_size=38, colors={r"r_{i,t+1}": SDF}),
                cmath(r"H_0:\ \Gamma_\alpha = 0", r"\iff", r"\text{characteristics matter only through risk}", font_size=36)]
        whys = [why(r"Kelly, Pruitt and Su (2019), instrumented PCA: each stock's betas are linear in its characteristics "
                    r"$z$ (size, value, momentum, ...), estimated jointly with the latent factors $f$. Betas change as a "
                    r"firm's characteristics change"),
                why(r"if characteristics also enter the alpha, they predict returns beyond risk. On individual US stocks, "
                    r"with five factors, the alpha test passes: 'characteristics are covariances'. It needs stock-level "
                    r"data this series does not have; Part 27 returns to it with machine learning")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "The third method works with individual stocks. Bryan Kelly, Seth Pruitt and Yinan Su's instrumented PCA "
            "lets each stock's betas be a linear function of its characteristics, its size, value, momentum and so "
            "on, estimated together with the latent factors. As a firm's characteristics change, so do its betas. "
            "<bookmark mark='a'/> Then test whether characteristics also enter the alpha, predicting returns beyond "
            "risk. With five factors they found they do not: characteristics are covariances. It needs stock-level "
            "data that this series does not have; Part twenty-seven returns to the idea with machine learning."
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
            desk_question(r"few factors, many errors", r"a handful of components capture the zoo's best combination; they "
                          r"do not price every portfolio, which is why the anomaly literature never ends", width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Two lessons. <bookmark mark='a'/> What the statistics optimise is the model: variance alone, variance and "
            "means together, or pricing errors with betas that move with characteristics. <bookmark mark='b'/> And a "
            "few components capture the zoo's best combination without pricing every portfolio, which is why new "
            "anomalies keep being found."
        ) as vo:
            for i, mk in enumerate(("a", "b")):
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
