from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403

F_COLS = {"2,10": S.RESID, "5,10": S.POST, "10,10": S.LIK, "30,30": SIM}


class FDist(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.shapes()
        self.world()
        self.anova()
        self.relations()

    def card(self):
        card = chapter_card(6, r"The $F$ distribution", r"Comparing two variances", part=PART)
        with self.voiceover("Chapter six. The F distribution."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"F", r"=", r"\frac{U/a}{V/b}", r",\quad U \sim \chi^2_a \perp V \sim \chi^2_b", font_size=34),
            cmath(r"\frac{s_1^2/\sigma_1^2}{s_2^2/\sigma_2^2}", r"\sim", r"F_{n_1 - 1,\ n_2 - 1}", font_size=34),
            cmath(r"\sigma_1 = \sigma_2:\quad \frac{s_1^2}{s_2^2}", r"\sim", r"F_{n_1 - 1,\ n_2 - 1}", font_size=34),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"a ratio of two independent mean squares"), why(r"two independent normal samples (chapter 4)"),
                why(r"so the ratio tests equal variances; \ and, in Part 13, \ equal means")]
        hc = note(r"named by George Snedecor (1934) for R. A. Fisher, \ who had worked with $\tfrac12 \log F$ (1924)").to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "If chi-squared measures one variance, a ratio of two measures how they compare. <bookmark mark='a'/> The F "
            "distribution is a ratio of two independent chi-squareds, each divided by its degrees of freedom. "
            "<bookmark mark='b'/> For two independent normal samples, the ratio of sample variances, each scaled by its "
            "true variance, has this distribution. <bookmark mark='c'/> So if the two true variances are equal, the "
            "ratio of sample variances is F, whatever the common variance is. George Snedecor named it in 1934 after "
            "Fisher, who had used half its logarithm ten years earlier. In Part 13 the same ratio compares the "
            "variation between groups to the variation within them."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
            self.play(FadeIn(hc))
        self.clear_scene()

    def shapes(self):
        d = load("fdist")
        xs = np.asarray(d["xs"])
        A = axes([0, 5], [0, 1.6], x_length=7.4, y_length=4.4, xlabel=r"$f$", xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 0.5, 1, 1.5],
                 center=[-2.0, -0.4, 0])
        ax = A.ax
        cvs = VGroup(*[pdf_curve(ax, xs, np.asarray(d["shapes"][k]), c, 3, ymax=1.6) for k, c in F_COLS.items()])
        leg = legend([(c, rf"$F_{{{k}}}$") for k, c in F_COLS.items()], font_size=24).move_to([4.6, 1.6, 0])
        rows = fit_rows(VGroup(label(r"centred near 1: \ the two variances agree", font_size=24),
                               label(r"skewed right; \ concentrates at 1 as both $df$ grow", font_size=24, color=GREY_A),
                               MathTex(r"F_{a,b} = 1/F_{b,a}", font_size=28)), 4.8, 0.3, [4.6, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are a few F distributions. They're all centred near one, where the two variances "
            "agree, and skewed to the right, since a ratio can be large but not negative. <bookmark mark='b'/> With "
            "thirty degrees of freedom on each side, the curve tightens around one: more data, a sharper comparison. "
            "And turning the ratio upside down just swaps the two degrees of freedom."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in cvs[:3]], lag_ratio=0.3), FadeIn(leg[:3]), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(Create(cvs[3]), FadeIn(leg[3]), FadeIn(rows[2]))
        self.clear_scene()

    def world(self):
        d = load("fdist")
        ed, xs = np.asarray(d["edges"]), np.asarray(d["xs"])
        A = axes([0, 6], [0, 0.8], x_length=7.4, y_length=4.2, xlabel=r"$s_1^2/s_2^2$: \ 5 men vs 10 men", xticks=[0, 1, 2, 3, 4, 5, 6],
                 yticks=[0, 0.4, 0.8], center=[-2.0, -0.4, 0])
        ax = A.ax
        h = hist_bars(ax, ed, np.clip(np.asarray(d["hist"]), 0, 0.8), color=SIM, opacity=0.65)
        cv = pdf_curve(ax, xs, np.asarray(d["pdf"]), EXACT, 3, ymax=0.8)
        qs = VGroup(DashedLine(ax.c2p(d["q"], 0), ax.c2p(d["q"], 0.8), color=S.RESID, stroke_width=2),
                    DashedLine(ax.c2p(d["q_lo"], 0), ax.c2p(d["q_lo"], 0.8), color=S.RESID, stroke_width=2))
        rows = fit_rows(VGroup(
            MathTex(r"F_{4,9}", font_size=32, color=EXACT),
            MathTex(rf"2.5\%,\ 97.5\%:\ \ {d['q_lo']:.2f},\ \ {d['q']:.2f}", font_size=28, color=S.RESID),
            label(r"a ratio below 4.7 is unremarkable \ \ldots{} \ variances are hard to compare with small samples", font_size=22,
                  color=GREY_A),
        ), 4.8, 0.3, [4.6, 0.4, 0])
        tag = simulated_tag(r"simulated: 20,000 pairs of samples of the World's men")
        with self.voiceover(
            "Check it on the World. <bookmark mark='a'/> Take five men and ten men, and divide their sample variances. "
            "Twenty thousand times. <bookmark mark='b'/> The histogram follows F with four and nine degrees of freedom. "
            "<bookmark mark='c'/> Its middle ninety-five percent runs from about point one one to four point seven: the "
            "first group's sample variance can be more than four times the second's by chance alone, when the true "
            "variances are equal. Variances are hard to compare with small samples."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(h, lag_ratio=0.02))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(qs), FadeIn(rows[1:]))
        self.clear_scene()

    def relations(self):
        rows = fit_rows(VGroup(
            MathTex(r"t_k^2 = F_{1,k}", r"\quad \text{a squared } t \text{ is an } F \text{ with one numerator df}", font_size=30),
            MathTex(r"a\,F_{a,b} \to \chi^2_a \ \ (b \to \infty)", r"\quad \text{the denominator becomes exact}", font_size=30),
            MathTex(r"\frac{a F_{a,b}}{b + a F_{a,b}} \sim \mathrm{Beta}\big(\tfrac a2, \tfrac b2\big)", r"\quad \text{Part 3's family tree}", font_size=30),
            label(r"normal, \ $\chi^2$, \ $t$, \ $F$, \ beta, \ gamma: \ one family, \ all from squared normal coordinates", font_size=26,
                  color=S.ACCENT),
        ), 12.6, 0.42, [0, 0.2, 0])
        for r in rows[:3]:
            r[1].set_color(GREY_B)
        with self.voiceover(
            "The four distributions of normal theory are one family. <bookmark mark='a'/> A squared t is an F with one "
            "degree of freedom on top. <bookmark mark='b'/> As the denominator's degrees of freedom grow, a times F "
            "becomes chi-squared with a degrees of freedom. <bookmark mark='c'/> And a simple transformation of F is a "
            "beta, which puts all of them on Part 3's family tree. <bookmark mark='d'/> Normal, chi-squared, t, F, "
            "beta, gamma: all of them are lengths and ratios of normal coordinates in Fisher's round cloud."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def anova(self):
        rows = [
            cmath(r"\text{total SS}", r"=", r"\underbrace{\sum_g n_g(\bar x_g - \bar x)^2}_{\text{between groups}} + \underbrace{\sum_g \sum_i (x_{gi} - \bar x_g)^2}_{\text{within}}",
                  font_size=30),
            cmath(r"F", r"=", r"\frac{\text{between SS}/(k - 1)}{\text{within SS}/(n - k)}", r"\ \sim\ F_{k - 1,\ n - k}\ \text{if all means are equal}",
                  font_size=30),
        ]
        rows[1][2].set_color(EXACT)
        whys = [why(r"Cochran: \ two orthogonal projections, \ $k - 1$ and $n - k$ dimensions"),
                why(r"Fisher's analysis of variance (1918--1925): \ Part 13")]
        foot = label(r"the same $F$, \ now comparing \emph{means} through variances", font_size=26, color=S.ACCENT).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The F distribution's most important use isn't comparing two variances at all. <bookmark mark='a'/> With "
            "several groups, the total sum of squares splits into a between-group part, how far the group means are "
            "from the overall mean, and a within-group part: two orthogonal projections, by Cochran's theorem. "
            "<bookmark mark='b'/> If all the group means are equal, the ratio of the two mean squares has an F "
            "distribution. Fisher's analysis of variance, developed at Rothamsted in the early 1920s, compares means by "
            "comparing variances, and it's the subject of Part 13."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.2, x=-1.6, buff=1.3, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            self.play(FadeIn(foot))
        self.clear_scene()
