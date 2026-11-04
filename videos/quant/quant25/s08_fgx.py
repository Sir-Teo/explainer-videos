from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, ask, fit_right, illustration, load


class FGX(VoiceoverScene):
    def construct(self):
        f = load("fgx")
        self.card()
        self.question()
        self.lasso()
        self.three(f)
        self.results(f)
        self.funnel(f)
        self.reading()

    def card(self):
        c = chapter_card(7, r"Taming the zoo", r"Does a new factor add anything to the hundreds we already have?",
                         lit=(2020,), part=PART)
        with self.voiceover("Chapter seven. A test for the question every new factor should face: what does it add?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def question(self):
        rows = [cmath(r"m_t", r"=", r"1 - \lambda_g\,g_t - \textstyle\sum_{h \in \mathcal H} \lambda_h\,h_t", font_size=40,
                      colors={r"m_t": SDF}),
                cmath(r"\mathbb{E}[R_i]", r"=", r"\text{cov}(R_i, g)\,\lambda_g + \textstyle\sum_h \text{cov}(R_i, h)\,\lambda_h",
                      font_size=38)]
        whys = [why(r"the right question about a new factor $g$ is not whether its own premium is positive, but whether the "
                    r"SDF needs it, given everything else: is its loading $\lambda_g$ non-zero?"),
                why(r"across test assets, mean returns are a regression on covariances with the factors. But with hundreds "
                    r"of candidate controls $h$ and only as many test assets, ordinary regression is impossible, and "
                    r"choosing the controls by hand invites the search problem again")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "The right question about a new factor is not whether its own average return is positive. Many are, "
            "because they overlap with old ones. It is whether the discount factor needs it, given everything we "
            "already have. <bookmark mark='a'/> Across test assets, mean returns are a regression on their covariances "
            "with all the factors. But with hundreds of candidate controls, ordinary regression breaks down, and "
            "choosing the controls by hand brings the search problem straight back."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def lasso(self):
        rows = [cmath(r"\hat\beta", r"=", r"\arg\min_\beta\ \tfrac{1}{2n}\,\|y - X\beta\|^2 + \lambda\,\|\beta\|_1",
                      font_size=40, colors={r"\hat\beta": GOOD})]
        whys = [why(r"the lasso (Tibshirani 1996): an L1 penalty sets most coefficients exactly to zero, so it selects. "
                    r"But a single lasso also drops controls that matter only because they are correlated with $g$, and "
                    r"then the estimate of $\lambda_g$ absorbs their effect: omitted-variable bias")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "The lasso selects variables automatically: an absolute-value penalty sets most coefficients exactly to "
            "zero. But one lasso is not enough. It can drop a control that matters only through its correlation with "
            "the new factor, and then the new factor's coefficient silently absorbs the missing control's effect. "
            "That is omitted-variable bias, chosen by an algorithm."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def three(self, f):
        cards = VGroup(
            desk_question(r"1. which factors price the assets?", r"lasso the test assets' mean returns on their "
                          r"covariances with the zoo: keep the selected controls", width=12.0, font_size=20),
            desk_question(r"2. which factors look like $g$?", r"lasso the assets' covariances with $g$ on their "
                          r"covariances with the zoo: keep those too, the would-be omitted variables", width=12.0,
                          font_size=20),
            desk_question(r"3. the test", r"regress mean returns on cov$(R, g)$ and the union of both selections; "
                          r"$\lambda_g$'s $t$ is valid despite the selection (Belloni, Chernozhukov and Hansen 2014)",
                          width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Guanhao Feng, Stefano Giglio and Dacheng Xiu used double selection. <bookmark mark='a'/> First, a lasso "
            "of the assets' mean returns on their covariances with the zoo: which old factors price these assets? "
            "<bookmark mark='b'/> Second, a lasso of the assets' covariances with the new factor on their covariances "
            "with the zoo: which old factors look like the new one? <bookmark mark='c'/> Third, an ordinary regression "
            "of mean returns on the new factor's covariance and everything either lasso kept. The t-statistic on the "
            "new factor is then valid despite the selection."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def results(self, f):
        rows = sorted(f["rows"], key=lambda r_: -r_["t_mean"])[:12]
        hx = [-4.2, -2.2, 0.0, 2.2, 4.4]
        heads = [r"new factor (year)", r"its own mean, $t$", r"naive SDF $t$", r"double selection $t$", r"controls kept"]
        tab = VGroup(VGroup(*[label(h_, font_size=15, color=GREY_A).move_to([x, 2.85, 0]) for h_, x in zip(heads, hx)]))
        for i, r_ in enumerate(rows):
            y = 2.35 - 0.42 * i
            tab.add(VGroup(label(rf"{r_['name']} ({r_['year']})", font_size=14).move_to([hx[0], y, 0]),
                           MathTex(f"{r_['t_mean']:.1f}", font_size=20, color=TRUE if r_["t_mean"] > 1.96 else NOISE).move_to([hx[1], y, 0]),
                           MathTex(f"{r_['t_naive']:.1f}", font_size=20, color=TRUE if abs(r_["t_naive"]) > 1.96 else NOISE).move_to([hx[2], y, 0]),
                           MathTex(f"{r_['t_ds']:.1f}", font_size=20, color=TRUE if abs(r_["t_ds"]) > 1.96 else NOISE).move_to([hx[3], y, 0]),
                           MathTex(str(r_["selected"]), font_size=20, color=GREY_B).move_to([hx[4], y, 0])))
        with self.voiceover(
            "On the open-source zoo: twenty-five predictors published from 2011 on, each tested against the fifty-three "
            "published by 2003, using the remaining predictors as test assets, 1973 to 2020. Here are the twelve with "
            "the largest average returns. <bookmark mark='a'/> Most have strong t-statistics on their own. "
            "<bookmark mark='b'/> Asked whether the discount factor needs them without any controls, fewer pass. "
            "<bookmark mark='c'/> With double selection, only a handful remain significant."
        ) as vo:
            self.play(FadeIn(tab[0]), *[FadeIn(r_[0]) for r_ in tab[1:]])
            vo.wait_until("a")
            self.play(*[FadeIn(r_[1]) for r_ in tab[1:]])
            vo.wait_until("b")
            self.play(*[FadeIn(r_[2]) for r_ in tab[1:]])
            vo.wait_until("c")
            self.play(*[FadeIn(r_[3:]) for r_ in tab[1:]])
        self.wait(0.8)
        self.clear_scene()

    def funnel(self, f):
        n = f["n_new"]
        stages = [(r"published since 2011", n, NOISE), (r"own mean, $t > 1.96$", f["sig_mean"], HURDLE),
                  (r"SDF loading, no controls", f["sig_naive"], SDF), (r"SDF loading, double selection", f["sig_ds"], TRUE)]
        grp = VGroup()
        for i, (nm, v, col) in enumerate(stages):
            w = 9.0 * v / n
            grp.add(VGroup(Rectangle(width=max(w, 0.3), height=0.7, stroke_width=0, fill_color=col, fill_opacity=0.85),
                           MathTex(str(v), font_size=30)).arrange(ORIGIN))
            grp[-1].add(label(nm, font_size=18, color=GREY_A).next_to(grp[-1][0], LEFT, buff=0.3))
        grp.arrange(DOWN, buff=0.35).shift(RIGHT * 1.5 + DOWN * 0.2)
        title = label(r"Twenty-five new factors, against fifty-three older ones", font_size=26).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"the House's \texttt{zoo.double\_selection}, penalties set by a standard rule, not tuned. A "
                             r"simplified version of Feng, Giglio and Xiu (2020), who found most recently proposed "
                             r"factors redundant against the zoo, with a few exceptions", 12.0, 17,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "As a funnel. <bookmark mark='a'/> Of twenty-five new predictors, twenty-one have significant average "
            "returns of their own. Fourteen look like they add to the discount factor if nothing is controlled for. "
            "After double selection, five. <bookmark mark='b'/> Feng, Giglio and Xiu found the same on their own "
            "data: most factors proposed after 2012 are redundant given the zoo, with a few genuine additions. A "
            "factor can be real, in the sense of earning a premium, and still add nothing."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g_, shift=RIGHT * 0.2) for g_ in grp], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def reading(self):
        cards = VGroup(
            desk_question(r"real is not new", r"a factor with a positive premium that is spanned by older ones gives an "
                          r"investor nothing that older factors do not already provide", width=12.0, font_size=20),
            desk_question(r"order matters", r"the test asks whether $g$ adds to the zoo as it stood; testing the old "
                          r"factors against the new would give different answers", width=12.0, font_size=20),
            desk_question(r"for the research desk", r"a candidate factor is tested against the House's library, with "
                          r"selected controls, before it gets a row", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "What it means. <bookmark mark='a'/> Real is not the same as new: a factor with a genuine premium that is "
            "spanned by older ones adds nothing to an investor who already holds them. <bookmark mark='b'/> Order "
            "matters: the test asks whether a factor adds to the zoo as it stood when the factor arrived. "
            "<bookmark mark='c'/> And for the research desk, every candidate is tested against the House's library, "
            "with selected controls, before it gets a row of its own."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a new factor has $t = 5$ on its own but its SDF loading is insignificant after double selection. What "
                r"has the test told you, and would you still hold it?")
        with self.voiceover("A new factor has a t-statistic of five on its own, but its discount-factor loading is "
                            "insignificant after double selection. What has the test told you, and would you still hold "
                            "it?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
