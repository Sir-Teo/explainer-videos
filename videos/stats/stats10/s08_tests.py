from __future__ import annotations

import numpy as np

from explainer.stats.kit import tests as T
from videos.stats.stats10.common import *  # noqa: F403


class Tests(VoiceoverScene):
    def construct(self):
        self.card()
        self.catalogue()
        self.paired()
        self.behrens()
        self.sizes()
        self.advice()

    def card(self):
        card = chapter_card(7, r"The everyday tests", r"$z$, \ $t$, \ paired, \ pooled, \ Welch", part=PART)
        with self.voiceover("Chapter seven. The everyday tests."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def catalogue(self):
        items = [
            (r"$z$, \ $\sigma$ known", r"\frac{\bar x - \mu_0}{\sigma/\sqrt n}", r"N(0, 1)"),
            (r"one-sample $t$", r"\frac{\bar x - \mu_0}{s/\sqrt n}", r"t_{n-1}"),
            (r"paired $t$", r"\frac{\bar d}{s_d/\sqrt n},\ \ d_i = x_i - y_i", r"t_{n-1}"),
            (r"two-sample $t$ (pooled)", r"\frac{\bar x - \bar y}{s_p\sqrt{1/n_1 + 1/n_2}}", r"t_{n_1 + n_2 - 2}"),
            (r"Welch", r"\frac{\bar x - \bar y}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}", r"\approx t_{\nu}"),
        ]
        hdr = VGroup(label(r"test", font_size=24, color=GREY_B), label(r"statistic", font_size=24, color=GREY_B),
                     label(r"null distribution", font_size=24, color=GREY_B))
        rows = VGroup(hdr)
        for nm, st, nd in items:
            rows.add(VGroup(label(nm, font_size=26, color=GREY_A), MathTex(st, font_size=30), MathTex(nd, font_size=30, color=OBS)))
        rows.arrange(DOWN, buff=0.3).move_to([0, 0.2, 0])
        for r in rows:
            r[0].set_x(-4.4)
            r[1].set_x(0.4)
            r[2].set_x(4.6)
        foot = label(r"every one: \ (estimate $-$ null value) $\div$ its standard error; \ Part 8 supplied the distributions", font_size=24,
                     color=OBS).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The tests used every day are all built the same way. <bookmark mark='a'/> The z-test, when sigma is known: "
            "the distance from x-bar to the null value, in standard errors, compared with a standard normal. "
            "<bookmark mark='b'/> With sigma estimated, Student's t, with n minus one degrees of freedom. "
            "<bookmark mark='c'/> For paired data, the same test on the differences. <bookmark mark='d'/> For two "
            "independent groups, the pooled two-sample t, which assumes the groups share a variance. "
            "<bookmark mark='e'/> And Welch's version, which doesn't. <bookmark mark='f'/> Each is an estimate minus its "
            "null value, divided by its standard error, and Part 8 derived every one of the reference distributions. "
            "statkit's tests module writes each in a few lines."
        ) as vo:
            self.play(FadeIn(hdr))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1], shift=RIGHT * 0.2))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def paired(self):
        a, b = np.asarray(museum.SLEEP_DRUG1), np.asarray(museum.SLEEP_DRUG2)
        pr, up = T.t_test(b, a, paired=True), T.t_test(b, a)
        A = axes([0.5, 10.5], [-2, 6], x_length=6.0, y_length=4.0, ylabel=r"extra hours of sleep", xticks=list(range(1, 11)),
                 yticks=[-2, 0, 2, 4, 6], center=[-3.0, -0.2, 0])
        ax = A.ax
        segs = VGroup(*[Line(ax.c2p(i + 1, a[i]), ax.c2p(i + 1, b[i]), color=GREY_C, stroke_width=2) for i in range(10)])
        da = VGroup(*[Dot(ax.c2p(i + 1, a[i]), radius=0.08, color=S.CTRL) for i in range(10)])
        db = VGroup(*[Dot(ax.c2p(i + 1, b[i]), radius=0.08, color=S.TREAT) for i in range(10)])
        leg = legend([(S.CTRL, r"drug 1"), (S.TREAT, r"drug 2")], font_size=22).next_to(A, UP, buff=0.1).align_to(A, RIGHT)
        rows = fit_rows(VGroup(
            label(r"Student's sleep data (1908): \ 10 patients, \ both drugs", font_size=24, color=GREY_A),
            MathTex(rf"\text{{paired:}}\ t_9 = {pr['t']:.2f},\ \ p = {pr['p']:.4f}", font_size=30, color=OBS),
            MathTex(rf"\text{{as if unpaired:}}\ t_{{18}} = {up['t']:.2f},\ \ p = {up['p']:.3f}", font_size=30),
            label(r"the same difference of means, \ 1.58 hours;", font_size=24),
            label(r"pairing removes the patient-to-patient spread", font_size=24),
            label(r"analyse the design you ran", font_size=26, color=OBS),
        ), 5.6, 0.34, [3.6, -0.2, 0])
        src = historical_tag(r"Cushny \& Peebles (1905), \ via Student", corner=DR)
        with self.voiceover(
            "The choice of test has to follow the design. <bookmark mark='a'/> Part 8's sleep data: ten patients, each "
            "given both drugs. Each line joins one patient's two results. <bookmark mark='b'/> Analysed as pairs, the "
            "differences give t equals four point oh six on nine degrees of freedom, and a p-value of point zero zero "
            "three. <bookmark mark='c'/> Analysed, wrongly, as two independent groups, the very same numbers give t of "
            "one point eight six and p of point zero eight. <bookmark mark='d'/> The difference of means is the same, "
            "one point five eight hours, but the patients differ a lot from each other, and pairing cancels that "
            "variation. <bookmark mark='e'/> Analyse the design you actually ran."
        ) as vo:
            self.play(FadeIn(A), FadeIn(leg), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(segs), FadeIn(da), FadeIn(db), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1] if k < 2 else (rows[3:5] if k == 2 else rows[5])))
        self.clear_scene()

    def behrens(self):
        h1 = history_card(1929, r"W.-U. Behrens; \ then Fisher (1935)", r"two normal means, \ unequal unknown variances: \ no exact "
                          r"$t$ reference law free of the variance ratio, \ the Behrens--Fisher problem", color=ALTC, width=6.0, font_size=22).move_to([-3.3, 1.0, 0])
        h2 = history_card(1947, r"B. L. Welch, \ \emph{Biometrika} 34", r"use each group's own variance, \ and approximate the null by $t$ "
                          r"with fractional degrees of freedom", color=ALTC, width=6.0, font_size=22).move_to([3.3, 1.0, 0])
        df = MathTex(r"\nu = \frac{\big(s_1^2/n_1 + s_2^2/n_2\big)^2}{\frac{(s_1^2/n_1)^2}{n_1 - 1} + \frac{(s_2^2/n_2)^2}{n_2 - 1}}",
                     font_size=34, color=OBS).move_to([0, -1.5, 0])
        lab = label(r"the Welch--Satterthwaite degrees of freedom (Satterthwaite, 1946)", font_size=22, color=GREY_A).next_to(df, DOWN, buff=0.25)
        intro = label('Two normal means with unequal unknown variances', font_size=36)
        with self.voiceover(
            "The pooled two-sample test assumes both groups have the same variance. What if they don't? "
            "<bookmark mark='a'/> That's the Behrens–Fisher problem, posed by Walter-Ulrich Behrens in 1929 and taken "
            "up by Fisher: for two normal means with unequal, unknown variances, the usual statistic has no exact t distribution independent of the unknown variance ratio. This is the classical Behrens–Fisher difficulty, not a claim that no valid exact or conservative procedure exists. <bookmark mark='b'/> Bernard "
            "Welch's practical answer, in 1947: use each group's own variance in the standard error, and approximate "
            "the null distribution by a t with fractional degrees of freedom, <bookmark mark='c'/> given by this "
            "formula, which Franklin Satterthwaite also found."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(h2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(df), FadeIn(lab))
        self.clear_scene()

    def sizes(self):
        d = load("welch")["rows"]
        hdr = VGroup(*[label(t, font_size=24, color=GREY_B) for t in (r"$n_1,\ n_2$", r"$\sigma_1/\sigma_2$", r"Student", r"Welch")])
        xs = [-4.4, -1.8, 1.0, 3.8]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 2.7, 0])
        cells = VGroup()
        for i, r in enumerate(d):
            y = 2.15 - 0.5 * i

            def col(v):
                return S.KEPT if abs(v - 0.05) <= 3 * np.sqrt(0.05 * 0.95 / 20000) else (S.BROKEN if v > 0.05 else S.CONS)

            cells.add(VGroup(MathTex(rf"{r['n1']},\ {r['n2']}", font_size=28).move_to([xs[0], y, 0]),
                             MathTex(rf"{r['ratio']:g}", font_size=28).move_to([xs[1], y, 0]),
                             MathTex(rf"{100 * r['student']:.1f}\%", font_size=28, color=col(r["student"])).move_to([xs[2], y, 0]),
                             MathTex(rf"{100 * r['welch']:.1f}\%", font_size=28, color=col(r["welch"])).move_to([xs[3], y, 0])))
        foot = fit_rows(VGroup(
            label(r"the size of a nominal 5\% test, \ normal data, \ 20,000 replications per row", font_size=22, color=GREY_A),
            label(r"Student fails when the \emph{smaller} group has the \emph{larger} variance; \ Welch is close to nominal in these simulated settings", font_size=24,
                  color=OBS),
        ), 12.6, 0.26, [0, -2.65, 0])
        tag = simulated_tag(r"simulated", corner=UR)
        with self.voiceover(
            "How much does it matter? <bookmark mark='a'/> Each row is twenty thousand pairs of normal samples with "
            "equal means, so every rejection is a false alarm, and a five percent test should reject five percent of "
            "the time. With equal sample sizes, the pooled test is only slightly off, six percent at worst. "
            "<bookmark mark='b'/> But give the first group ten observations and the second forty, and make the first "
            "group twice as spread out: the pooled test rejects eighteen percent of the time; four times as spread, "
            "twenty-nine percent. <bookmark mark='c'/> Reverse it, the large group being the variable one, and the "
            "pooled test almost never rejects, so the test is conservative here and can lose power against alternatives. <bookmark mark='d'/> Welch's test "
            "stays close to five percent in these rows. The pooled variance borrows the wrong group's spread whenever sizes "
            "and variances are unbalanced together."
        ) as vo:
            self.play(FadeIn(hdr), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells[3:6]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in cells[6:]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"in practice", font_size=32, color=OBS),
            label(r"use Welch's test by default: \ it costs almost nothing when the variances are equal \ (Delacre, Lakens \& Leys, 2017)",
                  font_size=24),
            label(r"a permutation test does not rescue unequal variances: \ under $H_0$ it assumes the groups are exchangeable", font_size=24),
            label(r"paired designs: \ test the differences; \ heavy tails: \ ranks (Part 16); \ many groups: \ ANOVA (Part 13)", font_size=24,
                  color=GREY_A),
            label(r"the Coverage Board gets Student vs Welch at the end of chapter 10", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The practical advice. <bookmark mark='b'/> Use Welch's test by default; when the "
            "variances really are equal, it loses almost nothing. <bookmark mark='c'/> Don't expect a permutation test to "
            "rescue you either: shuffling labels assumes the two groups are exchangeable under the null, which unequal "
            "variances violate. <bookmark mark='d'/> For paired designs, test the differences; for heavy tails, the rank "
            "tests of Part 16; for many groups, the analysis of variance of Part 13. <bookmark mark='e'/> And the "
            "Coverage Board will record Student against Welch at the end of chapter ten."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
