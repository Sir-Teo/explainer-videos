from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403

CHI_COLS = {"1": S.RESID, "2": S.POST, "3": S.ACCENT, "5": S.LIK, "9": S.EST, "15": S.PRIOR}


class ChiSq(VoiceoverScene):
    def construct(self):
        self.card()
        self.family()
        self.history()
        self.sample()
        self.cochran()
        self.interval()
        self.varcover()

    def card(self):
        card = chapter_card(4, r"Chi-squared and Cochran", r"Squared lengths of random vectors", lit=(1934,), part=PART)
        with self.voiceover("Chapter four. Chi-squared, and Cochran's theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def family(self):
        d = load("chisq")
        xs = np.asarray(d["xs"])
        A = axes([0, 25], [0, 0.55], x_length=7.6, y_length=4.4, xlabel=r"$q$", xticks=[0, 5, 10, 15, 20, 25], yticks=[0, 0.25, 0.5],
                 center=[-2.0, -0.4, 0])
        ax = A.ax
        keep = xs <= 25
        cvs = VGroup(*[pdf_curve(ax, xs[keep], np.asarray(d["pdf"][k])[keep], c, 3, ymax=0.55) for k, c in CHI_COLS.items()])
        leg = legend([(c, rf"$k = {k}$") for k, c in CHI_COLS.items()], font_size=22).move_to([4.8, 1.8, 0])
        rows = fit_rows(VGroup(
            MathTex(r"\chi^2_k = Z_1^2 + \cdots + Z_k^2", font_size=30),
            MathTex(r"f(q) = \frac{q^{k/2 - 1} e^{-q/2}}{2^{k/2}\Gamma(k/2)}", font_size=30, color=EXACT),
            MathTex(r"E = k,\quad \mathrm{Var} = 2k", font_size=28),
            label(r"= Gamma$(k/2,\ \text{rate } \tfrac12)$: \ Part 3's family tree", font_size=22, color=GREY_A),
        ), 4.8, 0.3, [4.6, -0.7, 0])
        with self.voiceover(
            "The squared length of a vector of k independent standard normals has its own distribution. "
            "<bookmark mark='a'/> Chi-squared with k degrees of freedom: for one degree, piled up near zero; for "
            "two, an exponential; for more, a skewed bump that drifts right and becomes more symmetric. "
            "<bookmark mark='b'/> Its density follows from Part 3: it's a gamma distribution with shape k over two, "
            "Karl Pearson's chi-squared of 1900. <bookmark mark='c'/> Its mean is k, one for each squared normal, "
            "and its variance two k."
        ) as vo:
            self.play(FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in cvs], lag_ratio=0.3), FadeIn(leg), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def sample(self):
        d = load("chisq")
        ed, xs = np.asarray(d["edges"]), np.asarray(d["xs"])
        panels = VGroup()
        for k, (n, df) in enumerate((("4", "3"), ("10", "9"))):
            A = axes([0, 30], [0, 0.3], x_length=5.6, y_length=3.4, xlabel=rf"$(n - 1)s^2/\sigma^2$, \ $n = {n}$", xticks=[0, 10, 20, 30],
                     yticks=[0, 0.1, 0.2], center=[-3.4 + 6.8 * k, -0.4, 0])
            h = hist_bars(A.ax, ed, np.clip(np.asarray(d[n]["hist"]), 0, 0.3), color=SIM, opacity=0.65)
            cv = pdf_curve(A.ax, xs, np.asarray(d["pdf"][df]), EXACT, 3, ymax=0.3)
            info = MathTex(rf"\text{{mean }} {d[n]['mean']:.2f}\ (\text{{exact }} {df}),\ \ \text{{var }} {d[n]['var']:.1f}\ (\text{{exact }} "
                           rf"{2 * int(df)})", font_size=22, color=GREY_A).next_to(A, DOWN, buff=0.15)
            panels.add(VGroup(A, h, cv, info))
        head = MathTex(r"\text{World heights:}\quad \frac{(n - 1)s^2}{\sigma^2} \ \text{vs}\ \chi^2_{n-1}", font_size=32).to_edge(UP, buff=0.5)
        tag = simulated_tag(r"simulated: 20,000 samples each")
        with self.voiceover(
            "Check it on the World. <bookmark mark='a'/> Samples of four heights: n minus one times the sample variance, "
            "over the true variance, follows chi-squared with three degrees of freedom. <bookmark mark='b'/> Samples of "
            "ten: chi-squared with nine. The means come out at three and nine, as they must. But the variances are "
            "smaller than six and eighteen, about five and fourteen, because the World's heights mix two normal "
            "groups, men and women, which makes their distribution flatter-topped than a normal. The chi-squared law is exact only for normal data, a point that will matter "
            "in chapter twelve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
        self.clear_scene()

    def cochran(self):
        thm = theorem_card(r"Cochran's theorem", r"if $\mathbf z \sim N(\mathbf 0, I_n)$ and $\|\mathbf z\|^2 = \mathbf z^\top P_1\mathbf z + "
                           r"\cdots + \mathbf z^\top P_k \mathbf z$ with projections $P_j$ whose ranks add to $n$, \ then the pieces are "
                           r"independent, \ $\mathbf z^\top P_j\mathbf z \sim \chi^2_{\operatorname{rank} P_j}$",
                           who=r"W. G. Cochran, 1934 (Part 4, chapter 11)", color=S.ACCENT, width=10.6, font_size=24).to_edge(UP, buff=0.5)
        rows = fit_rows(VGroup(
            MathTex(r"\|\mathbf z\|^2 = \underbrace{n\bar z^2}_{\text{rank } 1,\ \chi^2_1} + \underbrace{\textstyle\sum (z_i - \bar z)^2}_{\text{rank } n - 1,\ "
                    r"\chi^2_{n-1}}", font_size=32),
            label(r"the sample's two pieces: \ the mean, \ and the deviations", font_size=24, color=GREY_A),
            label(r"in Part 12: \ fitted values and residuals; \ in Part 13: \ treatments, blocks and error", font_size=24, color=GREY_A),
            label(r"every sum-of-squares table in statistics is this theorem", font_size=26, color=S.ACCENT),
        ), 12.6, 0.35, [0, -1.2, 0])
        with self.voiceover(
            "Part 4 proved a general version, and it's worth restating here. <bookmark mark='a'/> William Cochran's "
            "theorem of 1934: split the squared length of a standard normal vector into pieces using projections whose "
            "dimensions add up to n, and the pieces are independent chi-squareds, each with degrees of freedom equal "
            "to its dimension. <bookmark mark='b'/> For a sample, the pieces are the mean, one dimension, and the "
            "deviations, n minus one. <bookmark mark='c'/> In regression, the fitted values and the residuals; in a "
            "designed experiment, treatments, blocks and error. <bookmark mark='d'/> Every analysis of variance table "
            "in statistics is this one theorem."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[[0, 2, 3][k]] if k else VGroup(rows[0], rows[1])))
        self.clear_scene()

    def interval(self):
        rows = [
            cmath(r"P\Big(\chi^2_{n-1,\,0.025} \le \frac{(n - 1)s^2}{\sigma^2} \le \chi^2_{n-1,\,0.975}\Big)", r"=", r"0.95", font_size=30),
            cmath(r"\sigma^2", r"\in", r"\Big[\frac{(n - 1)s^2}{\chi^2_{n-1,\,0.975}},\ \frac{(n - 1)s^2}{\chi^2_{n-1,\,0.025}}\Big]", font_size=32),
            cmath(r"n = 10,\ s = 9:\quad \sigma", r"\in", r"[6.2,\ 16.4]", font_size=32),
        ]
        rows[1][2].set_color(EXACT)
        whys = [why(r"a pivot: \ its distribution involves no unknowns"), why(r"invert the inequalities"),
                why(r"lopsided: \ $s^2$'s distribution is skewed")]
        with self.voiceover(
            "Chi-squared gives our first interval for something other than a mean. <bookmark mark='a'/> The scaled "
            "variance is a pivot: its distribution doesn't depend on any unknown. So it lies between the two and a "
            "half and ninety-seven and a half percentiles of chi-squared with probability ninety-five percent. "
            "<bookmark mark='b'/> Turn the inequalities around, and you have an interval for sigma squared. "
            "<bookmark mark='c'/> With ten observations and a sample standard deviation of nine, sigma lies between "
            "six point two and sixteen point four: lopsided, and wide. Ten observations say little about spread. "
            "Part 11 builds intervals from pivots in general."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=0.6, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def varcover(self):
        d = load("extras2")
        cov, kurt = d["varcover"], d["kurt"]
        wh = d["wh"]
        rows = fit_rows(VGroup(
            label(r"the $\chi^2$ interval for $\sigma^2$, \ $n = 10$, \ nominal 95\%:", font_size=26),
            MathTex(rf"\text{{normal men }}(\kappa = {kurt['normal men']:.2f}):\ {100 * cov['normal men']:.1f}\%", font_size=28, color=S.KEPT),
            MathTex(rf"\text{{all adults }}(\kappa = {kurt['all adults']:.2f}):\ {100 * cov['all adults']:.1f}\%", font_size=28, color=S.CONS),
            MathTex(rf"\text{{log incomes }}(\kappa = {kurt['log incomes']:.2f}):\ {100 * cov['log incomes']:.1f}\%", font_size=28,
                    color=S.BROKEN),
            label(r"exact for normal data, \ and only for normal data: \ kurtosis decides (chapter 12)", font_size=24, color=S.ACCENT),
            MathTex(rf"\text{{a shortcut: }} \chi^2_{{9,\,0.975}} = {wh['9']['exact']:.2f};\ \ \text{{Wilson--Hilferty}}\ {wh['9']['wh']:.2f};"
                    rf"\ \ \text{{normal}}\ {wh['9']['normal']:.2f}", font_size=24, color=GREY_A),
        ), 12.6, 0.32, [0, 0.2, 0])
        tag = simulated_tag(r"simulated: 20,000 samples each")
        with self.voiceover(
            "How far can that interval be trusted? <bookmark mark='a'/> Try it on three populations from the World, "
            "with samples of ten. <bookmark mark='b'/> For men's heights, which are normal, it covers ninety-five point "
            "two percent: on target. <bookmark mark='c'/> For all adults, a flat-topped mixture with negative excess "
            "kurtosis, ninety-six point seven: conservative. <bookmark mark='d'/> For log incomes, with positive excess "
            "kurtosis, ninety-three: broken. <bookmark mark='e'/> The chi-squared law is exact only for normal data, and "
            "the error is set by the kurtosis, a story chapter twelve finishes. <bookmark mark='f'/> One practical note: "
            "when tables of chi-squared weren't to hand, the cube root of chi-squared over k is nearly normal, a trick "
            "of Edwin Wilson and Margaret Hilferty from 1931, accurate to two decimals even with nine degrees of freedom."
        ) as vo:
            self.play(FadeIn(tag))
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def history(self):
        rows = fit_rows(VGroup(
            label(r"1876: \ Friedrich Helmert, \ a geodesist checking survey errors, \ derives the law of $\sum(x_i - \bar x)^2$", font_size=24),
            label(r"his rotation (chapter 3) is how he did it; \ the result was forgotten", font_size=24, color=GREY_A),
            label(r"1900: \ Karl Pearson rediscovers it for his goodness-of-fit test, \ and names it $\chi^2$", font_size=24),
            label(r"1922--24: \ Fisher corrects Pearson's degrees of freedom \ \textemdash{} \ estimated parameters use up dimensions",
                  font_size=24, color=S.ACCENT),
            label(r"chapter 2's lesson, \ won in a bitter public argument; \ the test itself is Part 10", font_size=22, color=GREY_A),
        ), 12.6, 0.36, [0, 0.2, 0])
        with self.voiceover(
            "The distribution has a tangled history. <bookmark mark='a'/> In 1876 Friedrich Helmert, a German geodesist "
            "studying the errors of land surveys, derived the distribution of a sum of squared deviations, <bookmark mark='b'/> "
            "using the very rotation of chapter three. Hardly anyone noticed. <bookmark mark='c'/> In 1900 Karl Pearson "
            "found the same distribution again, for his test of whether data fit a model, and gave it the name "
            "chi-squared. <bookmark mark='d'/> But Pearson got the degrees of freedom wrong when parameters were estimated "
            "from the data, and in the early 1920s Fisher corrected him: every estimated parameter uses up a dimension. "
            "<bookmark mark='e'/> That was chapter two's lesson, established in one of statistics' most bitter public "
            "arguments. The test itself comes in Part 10."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
