from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, ask, fit_right, illustration, load


class Weak(VoiceoverScene):
    def construct(self):
        w = load("weak")
        self.card()
        self.problem()
        self.sim(w)
        self.omitted()
        self.threepass()
        self.lesson()

    def card(self):
        c = chapter_card(8, r"Weak factors", r"What if a factor barely moves the assets it is meant to price?", lit=(2021,),
                         part=PART)
        with self.voiceover("Chapter eight. A statistical trap hidden inside the two-pass regressions of Part six: weak "
                            "factors."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def problem(self):
        rows = [cmath(r"\bar R_i", r"=", r"\gamma_0 + \hat\beta_i\,\lambda + e_i,\quad \hat\beta_i = \beta_i + \text{noise}",
                      font_size=40, colors={r"\bar R_i": SDF}),
                cmath(r"\beta_i \approx 0\ \forall i", r"\Rightarrow", r"\hat\lambda \approx \frac{\text{cov}(\bar R, \text{noise})}"
                      r"{\text{var}(\text{noise})}\ \text{: anything}", font_size=36, colors={r"\beta_i \approx 0\ \forall i": BAD})]
        whys = [why(r"the second pass regresses average returns on estimated betas. If the factor really moves the assets, "
                    r"the betas are spread out and the slope is well identified"),
                why(r"if the factor is weak, its true betas are all near zero and the estimated ones are mostly noise: the "
                    r"slope is a ratio of noises, with no reason to be near the true premium, and standard errors that "
                    r"understate the uncertainty (Kan and Zhang 1999; Kleibergen 2009)")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "The second pass of a Fama-MacBeth test regresses assets' average returns on their estimated betas. If the "
            "factor really moves the assets, the betas are spread out and the slope, the premium, is well identified. "
            "<bookmark mark='a'/> But if the factor is weak, its true betas are all close to zero, and the estimated "
            "betas are mostly noise. The slope becomes a ratio of noises, with no reason to be near the true premium, "
            "and the usual standard errors badly understate the uncertainty. Raymond Kan and Chu Zhang showed that a "
            "useless factor can look priced this way."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def sim(self, w):
        lam = w["true"] * 100
        panels = VGroup()
        for nm, col, ttl in (("strong", TRUE, r"strong factor: betas near 1"), ("weak", BAD, r"weak factor: betas near 0.05")):
            est = np.asarray(w[nm]["est"]) * 100
            edges = np.linspace(-1.5, 2.0, 36)
            h = np.histogram(np.clip(est, -1.49, 1.99), edges)[0]
            g = axes([-1.5, 2.0], [0, max(h) * 1.15], x_length=5.4, y_length=3.6, xlabel=r"estimated premium, \% a month",
                     ylabel=r"simulations", xticks=[-1, 0, 0.5, 1, 2], yticks=[], font_size=12)
            ax = g.ax
            bars = VGroup(*[Rectangle(width=ax.c2p(edges[i + 1], 0)[0] - ax.c2p(edges[i], 0)[0],
                                      height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0, fill_color=col,
                                      fill_opacity=0.8).move_to([(ax.c2p(edges[i], 0)[0] + ax.c2p(edges[i + 1], 0)[0]) / 2,
                                                                 (ax.c2p(0, 0)[1] + ax.c2p(0, v)[1]) / 2, 0])
                            for i, v in enumerate(h)])
            tl = DashedLine(ax.c2p(lam, 0), ax.c2p(lam, max(h) * 1.1), color=WHITE, stroke_width=2)
            cap = MathTex(rf"\text{{median}}\ {100 * w[nm]['median']:.2f}\%,\ \text{{10--90\%}}:\ [{100 * w[nm]['p10']:.2f},\ "
                          rf"{100 * w[nm]['p90']:.2f}]", font_size=18).next_to(g, DOWN, buff=0.15)
            panels.add(VGroup(g, bars, tl, label(ttl, font_size=18, color=col).next_to(g, UP, buff=0.1), cap))
        panels.arrange(RIGHT, buff=0.8).shift(DOWN * 0.1)
        foot = label(r"400 simulations, 50 assets, 40 years; true premium 0.5\% a month (white line)", font_size=15,
                     color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "A simulation. Fifty assets, forty years, a factor with a true premium of half a percent a month. "
            "<bookmark mark='a'/> When the factor is strong, with betas around one, the two-pass estimates cluster "
            "around the truth. <bookmark mark='b'/> Make the same factor weak, betas around one twentieth, and the "
            "estimates spread from minus six tenths to plus three quarters, centred near zero. The truth is the same "
            "half percent in both. The weak factor's premium is simply not identified by these test assets."
        ) as vo:
            self.play(FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
        self.add(illustration(r"simulated: the House's \texttt{econ.two\_pass}", corner=UR))
        self.wait(0.4)
        self.clear_scene()

    def omitted(self):
        rows = [cmath(r"R_t", r"=", r"\beta\,g_t + \underbrace{\eta\,v_t}_{\text{omitted}} + \varepsilon_t", font_size=42,
                      colors={r"R_t": SDF}),
                cmath(r"\hat\lambda_g", r"\to", r"\lambda_g + \text{bias}(\text{cov}(\beta, \eta),\ \lambda_v)", font_size=40,
                      colors={r"\hat\lambda_g": BAD})]
        whys = [why(r"a second problem: the factors in the model are rarely all the factors that price the assets. An "
                    r"omitted factor $v$ whose betas are correlated with $g$'s leaks its premium into $\hat\lambda_g$"),
                why(r"Giglio and Xiu (2021): the bias does not vanish with more data, and choosing different test assets "
                    r"gives different answers for the same factor")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "And a second problem. A model rarely contains every factor that prices the assets. If an omitted factor's "
            "betas are correlated with the included factor's, its premium leaks into the estimate. "
            "<bookmark mark='a'/> Stefano Giglio and Dacheng Xiu showed that the bias does not go away with more data, "
            "and that the same factor gets different premia from different sets of test assets."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def threepass(self):
        cards = VGroup(
            desk_question(r"1. find the latent factors", r"PCA on many test assets: the components span every factor that "
                          r"moves them, observed or not", width=12.0, font_size=20),
            desk_question(r"2. price the components", r"a cross-sectional regression of mean returns on the components' "
                          r"betas: their premia are well identified, because the components are strong by construction",
                          width=12.0, font_size=20),
            desk_question(r"3. map the factor of interest", r"regress $g$ on the components; its premium is the "
                          r"components' premia weighted by that regression: valid even with omitted factors", width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Their remedy has three passes. <bookmark mark='a'/> First, principal components of a large set of test "
            "assets: the components span every factor that moves them, whether anyone named it or not. "
            "<bookmark mark='b'/> Second, price the components, whose premia are well identified because they are "
            "strong by construction. <bookmark mark='c'/> Third, express the factor of interest in terms of the "
            "components; its premium follows. Omitted factors are no longer omitted. Later work by Giglio, Xiu and "
            "Dake Zhang selects test assets so that even weak factors are measured well."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lesson(self):
        cards = VGroup(
            desk_question(r"check strength first", r"before estimating a premium, ask whether the factor moves the test "
                          r"assets at all: the spread of its betas, and their $t$'s", width=12.0, font_size=20),
            desk_question(r"macro factors especially", r"consumption, inflation and other non-traded factors are often "
                          r"weak: their estimated premia from portfolio sorts deserve the most suspicion", width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Two habits follow. <bookmark mark='a'/> Before estimating any premium, check that the factor moves the "
            "test assets at all: the spread of its betas and their t-statistics. <bookmark mark='b'/> And be most "
            "suspicious of non-traded factors, consumption or inflation: they are often weak, and the premia "
            "estimated for them from portfolio sorts can be almost anything."
        ) as vo:
            for i, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a macro factor's estimated premium is 0.8\% a month with $t = 2.5$, but its betas on the 25 portfolios have "
                r"$t$'s below 1. What do you conclude?")
        with self.voiceover("A macro factor's estimated premium is zero point eight percent a month, with a t of two and a "
                            "half, but its betas on the test portfolios all have t-statistics below one. What do you "
                            "conclude?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
