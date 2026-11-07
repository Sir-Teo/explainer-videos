from __future__ import annotations

import numpy as np

from videos.stats.stats14.common import *  # noqa: F403

DEPTS = "ABCDEF"


class ThreeWay(VoiceoverScene):
    def construct(self):
        self.card()
        self.strata()
        self.mh()
        self.cmh_test()
        self.logistic()
        self.homogeneity()
        self.history()

    def card(self):
        card = chapter_card(9, r"Three-way tables", r"Comparing within strata, \ then pooling", lit=(1959,), part=PART)
        with self.voiceover("Chapter nine. Three-way tables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def strata(self):
        d = load("tables")
        ors = d["cmh"]["strata_or"]
        A = axes([-0.6, 6.6], [np.log(0.25), np.log(4)], x_length=8.4, y_length=4.0, xlabel=r"", ylabel=r"odds ratio, \ men vs women (log scale)",
                 xticks=[], yticks=[np.log(0.25), np.log(0.5), 0, np.log(2), np.log(4)], center=[-1.6, 0.4, 0],
                 yfmt=lambda v: f"{np.exp(v):.2g}")
        ax = A.ax
        one = DashedLine(ax.c2p(-0.6, 0), ax.c2p(6.6, 0), color=GREY_C, stroke_width=2)
        dots = VGroup(*[Dot(ax.c2p(k, np.log(o)), radius=0.11, color=S.ALT) for k, o in enumerate(ors)])
        names = VGroup(*[label(dep, font_size=24, color=GREY_B).move_to(ax.c2p(k, np.log(0.25)) + DOWN * 0.3) for k, dep in enumerate(DEPTS)])
        pooled = Dot(ax.c2p(6.2, np.log(d["pooled"]["or"])), radius=0.13, color=RES)
        pl = label(r"pooled", font_size=22, color=RES).move_to(ax.c2p(6.2, np.log(0.25)) + DOWN * 0.3)
        rows = fit_rows(VGroup(
            label(r"six $2\times2$ tables: \ one odds ratio per department", font_size=22),
            label(r"five near 1; \ A well below", font_size=22, color=S.ALT),
            MathTex(rf"\text{{pooled table:}}\ {d['pooled']['or']:.2f}", font_size=28, color=RES),
            label(r"we want one number for ``sex, \ within department''", font_size=22, color=OBS),
        ), 3.8, 0.36, [5.1, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Berkeley data are a three-way table: sex, by admission, by department. Slice it into six "
            "two-by-two tables and compute each department's odds ratio, men's odds of admission over women's. "
            "<bookmark mark='b'/> Five departments sit near one. Department A, where women did much better, sits well below. "
            "<bookmark mark='c'/> The pooled table's odds ratio, one point eight four, is higher than "
            "every single department's. <bookmark mark='d'/> We'd like a single summary of the association "
            "between sex and admission within departments, which pools the six tables without letting the departments' "
            "different sizes and rates distort it."
        ) as vo:
            self.play(FadeIn(A), Create(one), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.6) for d_ in dots], lag_ratio=0.15), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pooled, scale=1.6), FadeIn(pl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def mh(self):
        d = load("tables")
        rows = [
            cmath(r"\widehat{\text{OR}}_k", r"=", r"\frac{a_k d_k}{b_k c_k}", font_size=34),
            cmath(r"\widehat{\text{OR}}_{\text{MH}}", r"=", r"\frac{\sum_k a_k d_k / n_k}{\sum_k b_k c_k / n_k}", font_size=34),
            cmath(r"\widehat{\text{OR}}_{\text{MH}}", r"=", rf"{d['cmh']['or_mh']:.3f}", font_size=34),
            cmath(r"\text{women vs men}", r":", rf"1/{d['cmh']['or_mh']:.3f} = {1 / d['cmh']['or_mh']:.2f}", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"department $k$'s own odds ratio"), why(r"Mantel \& Haenszel (1959): \ weights $b_k c_k/n_k$"),
                why(r"men's odds slightly lower, \ within departments"), why(r"the 1.84 has turned into 1.11 the other way")]
        with self.voiceover(
            "<bookmark mark='a'/> Each department has its own odds ratio, a d over b c. <bookmark mark='b'/> Nathan Mantel and "
            "William Haenszel's 1959 estimator pools them: add up a d over n across the strata, add up b c over n, and divide. "
            "It's a weighted average of the departments' odds ratios, robust when some strata are small. "
            "<bookmark mark='c'/> For Berkeley it's point nine oh five: within departments, men's odds of admission were "
            "slightly lower than women's. <bookmark mark='d'/> Turned around, women's odds were about eleven percent higher. "
            "The pooled table's one point eight four against women has become one point one one in their favour."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cmh_test(self):
        d = load("tables")["cmh"]
        rows = [
            cmath(r"\mathbb E[a_k]", r"=", r"\frac{(a_k + b_k)(a_k + c_k)}{n_k}", font_size=32),
            cmath(r"\mathrm{Var}(a_k)", r"=", r"\frac{(a_k + b_k)(c_k + d_k)(a_k + c_k)(b_k + d_k)}{n_k^2(n_k - 1)}", font_size=30),
            cmath(r"X^2_{\text{CMH}}", r"=", r"\frac{\big(\sum_k (a_k - \mathbb E[a_k])\big)^2}{\sum_k \mathrm{Var}(a_k)}", font_size=32),
            cmath(r"X^2_{\text{CMH}}", r"=", rf"{d['chi2']:.2f}\ \text{{on 1 df}}:\ \ p = {d['p']:.2f}", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"each stratum's expected count, \ given its margins"), why(r"its hypergeometric variance (Part 10)"),
                why(r"pool the deviations, \ not the tables"), why(r"no evidence of a common directional association")]
        intro = label('Combine within-stratum deviations from independence', font_size=36)
        with self.voiceover(
            "And a test. <bookmark mark='a'/> In each department, condition on the margins, as in Fisher's exact test: the count "
            "of admitted men then has a known expected value <bookmark mark='b'/> and a hypergeometric variance. "
            "<bookmark mark='c'/> The Cochran–Mantel–Haenszel statistic adds up the deviations across departments before "
            "squaring, so that consistent small effects accumulate and opposite ones cancel. <bookmark mark='d'/> For Berkeley "
            "it's one point five two, p equals point two two: no clear common directional association after stratification. Opposite associations can cancel, so this does not establish independence in every department. The p of ten to the minus twenty-one has evaporated."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def logistic(self):
        d = load("tables")
        b = d["logit_women_adj"]
        se = d["logit_women_adj_se"]
        rows = [
            cmath(r"\text{logit}\,P(\text{admit})", r"=", r"\beta_0 + \beta_1\,\text{woman} + \textstyle\sum_k \gamma_k\,\text{dept}_k", font_size=32),
            cmath(r"\hat\beta_1", r"=", rf"{b:+.3f}\ \ (\mathrm{{SE}}\ {se:.3f})", font_size=32),
            cmath(r"e^{\hat\beta_1}", r"=", rf"{np.exp(b):.2f}\ \ [{np.exp(b - 1.96 * se):.2f},\ {np.exp(b + 1.96 * se):.2f}]", font_size=32),
            cmath(r"\text{without departments}", r":", rf"\hat\beta_1 = {d['logit_women_pooled']:.3f}", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"department dummies: \ a separate baseline per department"), why(r"the sign has flipped"),
                why(r"close to Mantel--Haenszel's 1.11"), why(r"adjustment changes the comparison; logistic ORs are noncollapsible")]
        with self.voiceover(
            "<bookmark mark='a'/> The same conclusion comes from logistic regression with a dummy for each department, so each "
            "department gets its own baseline log-odds. <bookmark mark='b'/> The coefficient for women is now plus point one "
            "oh. The sign has flipped. <bookmark mark='c'/> As an odds ratio, one point one oh, with an interval from about "
            "point nine four to one point three: close to Mantel and Haenszel's estimate. <bookmark mark='d'/> Without the "
            "department dummies it was minus point six one. Leaving out the department, a variable related both to sex, "
            "through where people applied, and to admission, changes the comparison. Unlike linear regression, odds ratios are also noncollapsible: marginal and conditional ORs may differ without confounding, so Part 12's linear bias identity does not transfer."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.0, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def history(self):
        hc = history_card(1959, r"Nathan Mantel \ and \ William Haenszel, \ National Cancer Institute",
                          r"``Statistical aspects of the analysis of data from retrospective studies of disease'': \ pooling "
                          r"stratified $2\times2$ tables of cases and controls, \ building on William Cochran (1954)",
                          color=S.ALT, width=10.4, font_size=22).move_to([0, 1.3, 0])
        rows = fit_rows(VGroup(
            label(r"their setting: \ patients with a disease, \ and controls without it, \ stratified by age", font_size=24),
            label(r"the odds ratio was the natural measure there: \ chapter ten shows why", font_size=24, color=OBS),
            label(r"one of the most cited papers in epidemiology", font_size=22, color=GREY_A),
        ), 12.4, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Mantel and Haenszel weren't thinking about admissions. They worked at the National Cancer "
            "Institute, and their 1959 paper was about retrospective studies of disease, building on William Cochran's work "
            "of 1954. <bookmark mark='b'/> Their setting was patients with a disease and comparable people without it, "
            "stratified by age and other factors. <bookmark mark='c'/> In that setting the odds ratio isn't just convenient. It's "
            "a disease odds ratio identifiable without knowing the case/control sampling fractions. That's the next chapter. <bookmark mark='d'/> Their paper "
            "became one of the most cited in epidemiology."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def homogeneity(self):
        d = load("tables")
        rows = [
            cmath(r"H_0", r":", r"\text{OR}_1 = \cdots = \text{OR}_6\ \text{(one common odds ratio)}", font_size=30),
            cmath(r"\text{Breslow--Day}", r":", rf"X^2 = {d['bd']:.1f}\ \text{{on 5 df}},\ \ p = {d['bd_p']:.3f}", font_size=30),
            cmath(r"\text{without A}", r":", rf"X^2 = {d['bd5']:.1f}\ \text{{on 4 df}},\ \ p = {d['bd5_p']:.2f}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{one summary fits five departments; \ A is different}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"is pooling sensible?"), why(r"Breslow \& Day (1980): \ the odds ratios differ"),
                why(r"no detected heterogeneity in the selected five"), why(r"report A separately")]
        intro = label('Does a common odds ratio summarize the strata?', font_size=36)
        with self.voiceover(
            "A pooled odds ratio summarizes well only if the strata roughly agree. <bookmark mark='a'/> Test that: do all six "
            "departments share one odds ratio? <bookmark mark='b'/> Norman Breslow and Nicholas Day's test says no: chi-squared "
            "of eighteen point eight on five degrees of freedom, p of point zero zero two. <bookmark mark='c'/> Leave out "
            "department A and the other five are entirely consistent with a common odds ratio. <bookmark mark='d'/> Removing A is exploratory, since the data suggested it. A descriptive summary has two parts: in the selected five, no clear common association between sex and admission; in department A, women "
            "were admitted at a notably higher rate than men. Neither part shows the bias the pooled table seemed to."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()
