from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403
from videos.psychology.psych44.s04_cfa import cfa_diagram


class Estimate(VoiceoverScene):
    def construct(self):
        self.card()
        self.discrepancy()
        self.result()

    def card(self):
        card = chapter_card(4, r"Estimation by maximum likelihood", r"Which numbers make the model closest to the data?",
                            lit=(), part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter four. Estimation by maximum likelihood."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def discrepancy(self):
        head = heading(r"The discrepancy function")
        eq = MathTex(r"F_{\mathrm{ML}} = \log|\Sigma(\theta)| + \operatorname{tr}\!\big(S\,\Sigma(\theta)^{-1}\big) "
                     r"- \log|S| - p", font_size=38, color=MODEL).move_to([0, 1.4, 0])
        rows = rows_of([
            (r"if the data are multivariate normal, \ minimizing $F$ is maximizing the likelihood; \ $F = 0$ exactly "
             r"when the model reproduces $S$", WHITE),
            (r"Psyche minimizes it numerically over the 21 unknowns, \ from rough starting values, \ in about half a "
             r"second", MODEL),
            (r"$T = n\,F_{\min}$ is, \ if the model is exactly right, \ a chi-square on the model's degrees of freedom", GOOD),
        ], 12.4, 22, 0.42).move_to([0, -1.2, 0])
        with self.voiceover(
            "Estimation means choosing the unknowns that bring the model closest to the data. <bookmark mark='a'/> "
            "If the data are multivariate normal, minimizing this discrepancy is maximizing the likelihood. It's zero "
            "exactly when the model reproduces the observed covariances. <bookmark mark='b'/> Psyche minimizes it "
            "numerically over the twenty-one unknowns, from rough starting values, in about half a second. "
            "<bookmark mark='c'/> And n times the minimum is, if the model is exactly right, a chi-square on the "
            "model's degrees of freedom."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def result(self):
        d = load("hs")
        head = heading(r"Holzinger and Swineford, \ fitted")
        dg = cfa_diagram(loadings=d["std"].max(1)).scale(0.8).move_to([-2.2, 0.7, 0])
        pc = d["phi_cor"]
        rows = rows_of([
            (rf"standardized loadings from {d['std'].max(1).min():.2f} to {d['std'].max(1).max():.2f}", WHITE),
            (rf"factor correlations: \ visual and verbal {pc[0, 1]:.2f}, \ visual and speed {pc[0, 2]:.2f}, \ verbal "
             rf"and speed {pc[1, 2]:.2f}", MODEL),
            (rf"$\chi^2 = {d['t3_T']:.1f}$ on {d['t3_df']:.0f} degrees of freedom", PERSON),
            (r"every number matches lavaan, \ R's reference package, \ to three decimals: \ the tests check it", GOOD),
        ], 4.6, 18, 0.38).move_to([4.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{sem.fit\_cfa}; \ checked against lavaan")
        with self.voiceover(
            "Here is the model, fitted to Holzinger and Swineford's children. <bookmark mark='a'/> The standardized "
            "loadings run from about zero point four to zero point nine. <bookmark mark='b'/> The factors correlate: "
            "visual with verbal and with speed, both a little under zero point five, and verbal with speed about zero "
            "point three. <bookmark mark='c'/> The "
            "chi-square is eighty-five on twenty-four degrees of freedom. <bookmark mark='d'/> And every number "
            "matches lavaan, the reference package in R, to three decimal places. The tests check it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(dg))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
