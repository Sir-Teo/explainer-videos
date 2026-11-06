from __future__ import annotations

import numpy as np
from scipy import stats as st

from videos.stats.stats7.common import *  # noqa: F403


class VarRed(VoiceoverScene):
    def construct(self):
        self.card()
        self.antithetic()
        self.control()
        self.stratified()
        self.compare()
        self.importance()
        self.warning()

    def card(self):
        card = chapter_card(7, r"Variance reduction", r"The same accuracy, \ for less computing", part=PART)
        with self.voiceover("Chapter seven. Variance reduction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def antithetic(self):
        A = axes([0, 1], [0.8, 2.9], x_length=5.0, y_length=4.0, xlabel=r"$u$", ylabel=r"$e^u$", xticks=[0, 0.5, 1],
                 yticks=[1, 2], center=[-3.8, -0.6, 0])
        ax = A.ax
        xs = np.linspace(0, 1, 100)
        cv = curve(ax, xs, np.exp(xs), EXACT, 3)
        pairs = VGroup()
        for u in (0.15, 0.35, 0.7):
            pairs.add(VGroup(Dot(ax.c2p(u, np.exp(u)), radius=0.08, color=GOOD), Dot(ax.c2p(1 - u, np.exp(1 - u)), radius=0.08, color=S.POST),
                             DashedLine(ax.c2p(u, np.exp(u)), ax.c2p(1 - u, np.exp(1 - u)), color=GREY_B, stroke_width=1.5)))
        rows = [
            cmath(r"I = \int_0^1 e^u\,du", r"=", r"e - 1", font_size=32),
            cmath(r"\hat I_{\text{anti}}", r"=", r"\frac{1}{n}\sum_{i=1}^{n/2}\big(e^{U_i} + e^{1 - U_i}\big)", font_size=30),
            cmath(r"\mathrm{Var}", r"=", r"\frac{\sigma^2}{n}(1 + \rho)", r",\quad", r"\rho = \operatorname{corr}(e^U, e^{1-U}) = -0.97",
                  font_size=28),
        ]
        rows[2][4].set_color(S.ACCENT)
        whys = [why(r"a test case with a known answer"), why(r"pair each $U$ with $1 - U$: \ same budget of $n$ evaluations"),
                why(r"a high value is paired with a low one: \ the errors cancel")]
        with self.voiceover(
            "Monte Carlo's error falls like one over root n, so halving it costs four times the computing. Variance "
            "reduction makes each draw count for more. <bookmark mark='a'/> Take a test case with a known answer: the "
            "integral of e to the u from zero to one, which is e minus one. <bookmark mark='b'/> The antithetic trick: "
            "for each uniform U, also use one minus U. Same number of evaluations, but they come in pairs. "
            "<bookmark mark='c'/> When U is small, e to the U is low and e to the one minus U is high: the errors in "
            "each pair cancel. The variance is multiplied by one plus their correlation, which here is minus point "
            "nine seven."
        ) as vo:
            self.play(FadeIn(A), Create(cv))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=2.6, buff=1.0, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            self.play(LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=0.4))
            vo.wait_until("c")
            step(2, transform=False)
        self.clear_scene()

    def control(self):
        rows = [
            cmath(r"\hat I_{\text{cv}}", r"=", r"\overline{e^{U}} - b\,(\bar U - \tfrac12)", font_size=34),
            cmath(r"b^*", r"=", r"\frac{\mathrm{Cov}(e^U, U)}{\mathrm{Var}\,U}", font_size=32),
            cmath(r"\mathrm{Var}(\hat I_{\text{cv}})", r"=", r"\frac{\sigma^2}{n}\big(1 - \rho^2\big)", r",\quad",
                  r"\rho = \operatorname{corr}(e^U, U) = 0.99", font_size=28),
        ]
        rows[2][2].set_color(S.ACCENT)
        whys = [why(r"$U$ has known mean $\tfrac12$: \ subtract its error"), why(r"fixed population slope here: $b^*=6(3-e)$"),
                why(r"the variance that $U$ cannot explain (Part 5's $1 - \rho^2$)")]
        intro = label('Cancel noise with a known expectation', font_size=36)
        with self.voiceover(
            "A second trick uses something you already know. <bookmark mark='a'/> The uniforms themselves have a known "
            "mean, a half. If the sample of U's happens to be high, e to the U is probably high too, so subtract a "
            "multiple of the U's error. <bookmark mark='b'/> The best multiple is the regression slope of e to the U on "
            "U, here known analytically as six times three minus e. With an unknown slope, a separate pilot or cross-fitting can preserve unbiasedness; a same-sample fitted slope need not. <bookmark mark='c'/> What remains is the variance that "
            "U can't explain, one minus rho squared, and since e to the u is nearly a straight line on the unit "
            "interval, rho is point nine nine. Control variates are regression, used to cancel noise."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=1.0, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def compare(self):
        d = load("varred")
        items = [("plain", d["sd_plain"], BAD), ("antithetic", d["sd_anti"], S.POST), ("control variate", d["sd_ctrl"], GOOD)]
        A = axes([0, 0.018], [0, 3.6], x_length=7.4, y_length=3.6, xlabel=r"standard deviation of the estimate, \ $n = 1{,}000$",
                 xticks=[0, 0.005, 0.01, 0.015], center=[0.6, -0.6, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        g = VGroup()
        for i, (nm, v, c) in enumerate(items):
            y = 3.0 - 1.05 * i
            lo, hi = ax.c2p(0, y - 0.3), ax.c2p(v, y + 0.3)
            r = Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=0, fill_color=c, fill_opacity=0.85)
            r.move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0])
            g.add(VGroup(r, label(nm, font_size=24, color=c).next_to(ax.c2p(0, y), LEFT, buff=0.2),
                         MathTex(f"{v:.4f}", font_size=24, color=c).next_to(r, RIGHT, buff=0.12)))
        f1 = (d["sd_plain"] / d["sd_anti"]) ** 2
        f2 = (d["sd_plain"] / d["sd_ctrl"]) ** 2
        rows = fit_rows(VGroup(label(rf"antithetic: \ variance {f1:.0f} times smaller", font_size=26, color=S.POST),
                               label(rf"control variate: \ {f2:.0f} times smaller", font_size=26, color=GOOD),
                               label(r"the same as running the plain method 30 or 60 times longer", font_size=22, color=GREY_A)),
                        12.6, 0.2, [0, 2.6, 0])
        tag = note(r"simulated: 4,000 repetitions of each estimator").to_corner(DR, buff=0.3)
        with self.voiceover(
            "How much does it help? <bookmark mark='a'/> Four thousand repetitions of each estimator, each using a "
            "thousand evaluations. The plain average has a standard deviation of about point oh one six. "
            f"<bookmark mark='b'/> The antithetic estimator: point oh oh two eight, a variance {f1:.0f} times smaller. "
            f"<bookmark mark='c'/> The control variate: point oh oh two, about {f2:.0f} times smaller. For free, the "
            "same accuracy as running the plain simulation thirty or sixty times as long."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(GrowFromEdge(g[k][0], LEFT), FadeIn(g[k][1:]))
            self.play(FadeIn(rows))
        self.clear_scene()

    def importance(self):
        d = load("varred")
        A = axes([-3.5, 7.5], [0, 0.45], x_length=7.0, y_length=3.4, xlabel=r"$z$", xticks=[-2, 0, 2, 4, 6], center=[-2.6, 0.6, 0])
        ax = A.ax
        xs = np.linspace(-3.5, 7.5, 300)
        f = curve(ax, xs, st.norm.pdf(xs), EXACT, 3)
        gq = curve(ax, xs, st.norm.pdf(xs, 4), S.POST, 3)
        cut = DashedLine(ax.c2p(4, 0), ax.c2p(4, 0.45), color=BAD, stroke_width=2)
        cl = MathTex(r"z = 4", font_size=24, color=BAD).next_to(ax.c2p(4, 0.45), UP, buff=0.05)
        leg = legend([(EXACT, r"$\phi$: \ the target"), (S.POST, r"$N(4, 1)$: \ the proposal")], font_size=22).move_to([4.4, 2.2, 0])
        rows = [
            cmath(r"P(Z > 4)", r"=", r"E_\phi \mathbf 1\{Z > 4\}", r"=", r"E_g\Big[\mathbf 1\{Y > 4\}\frac{\phi(Y)}{g(Y)}\Big]", font_size=28),
        ]
        rows[0][4].set_color(S.POST)
        whys = [why(r"reweight draws from $g$ by $\phi/g$: \ here $e^{-4y + 8}$")]
        res = fit_rows(VGroup(
            MathTex(rf"\text{{truth: }} {d['p_true']:.3e}".replace("e-05", r"\times 10^{-5}"), font_size=28, color=EXACT),
            MathTex(rf"\text{{plain, }} 10^5 \text{{ draws: sd }} {d['sd_plain_is']:.1e}".replace("e-05", r"\times 10^{-5}") +
                    rf"\ \ ({100 * d['zero_share']:.1f}\%" + r"\text{ of runs see none})", font_size=26, color=BAD),
            MathTex(rf"\text{{importance: sd }} {d['sd_imp']:.1e}".replace("e-07", r"\times 10^{-7}"), font_size=26, color=GOOD),
            label(rf"a variance {(d['sd_plain_is'] / d['sd_imp']) ** 2:,.0f} times smaller".replace(",", "{,}"), font_size=26,
                  color=S.ACCENT),
        ), 5.4, 0.25, [4.1, 0.3, 0])
        with self.voiceover(
            "The most powerful trick changes where you sample. <bookmark mark='a'/> Suppose we want the chance that a "
            "standard normal exceeds four: about three in a hundred thousand. With a hundred thousand plain draws, "
            "you'd see about three exceedances, and in about one run in twenty-four, none at all. The estimate is "
            "mostly noise. <bookmark mark='b'/> Instead, draw from a normal centred at four, where half the draws "
            "exceed four, and reweight each by the ratio of the densities. <bookmark mark='c'/> The expectation is "
            "unchanged, by a one-line change of measure. <bookmark mark='d'/> But the variance falls by a factor of "
            "several thousand. This is importance sampling, and it's how rare events, from bank failures to "
            "particle collisions, are computed."
        ) as vo:
            self.play(FadeIn(A), Create(f), Create(cut), FadeIn(cl), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("b")
            self.play(Create(gq), FadeIn(leg[1]))
            vo.wait_until("c")
            step = ladder(self, rows, whys, keep=1, top=-2.1, x=-2.6, buff=0.8, edge=6.9)
            step(0, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(res[2:]))
        self.clear_scene()

    def warning(self):
        rows = fit_rows(VGroup(
            label(r"importance sampling can also fail, \ silently", font_size=30),
            MathTex(r"\mathrm{Var} = \int \frac{h(y)^2 \phi(y)^2}{g(y)}\,dy - I^2", font_size=32),
            label(r"require $g>0$ wherever $h\phi\ne0$; \ lighter tails can cause \ rare huge weights, \ possibly infinite variance", font_size=24,
                  color=BAD),
            label(r"the estimate looks stable for a long time, \ then jumps", font_size=24, color=BAD),
            label(r"check support and finite $\int h^2\phi^2/g$; \ heavier tails can help (Part 27: PSIS)",
                  font_size=24, color=S.ACCENT),
        ), 12.6, 0.35, [0, 0.2, 0])
        intro = label('Check importance weights and their moments', font_size=36)
        with self.voiceover(
            "<bookmark mark='a'/> Importance sampling can also fail, and silently. <bookmark mark='b'/> Its variance "
            "involves the target density squared over the proposal. <bookmark mark='c'/> If the proposal has lighter "
            "tails than the target, then far out the ratio explodes: a rare draw gets an enormous weight, and the "
            "variance can be infinite, Part 6's heavy tails all over again. <bookmark mark='d'/> Worse, the estimate "
            "can look perfectly stable for a long time before one draw moves it. <bookmark mark='e'/> The rule: "
            "cover the integrand's support, check the second moment of the weights, and inspect them. Heavier tails can help but are not a universal guarantee. Part 27 turns that "
            "advice into a diagnostic."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def stratified(self):
        g = np.random.Generator(np.random.PCG64(8))
        n, reps = 1000, 2000
        plain = np.exp(g.random((reps, n))).mean(1)
        strat = np.exp((np.arange(n) + g.random((reps, n))) / n).mean(1)
        f = float(f"{(plain.std() / strat.std()) ** 2:.2g}")
        x0, x1, y = -5.6, 5.6, 1.6
        line = Line([x0, y, 0], [x1, y, 0], color=GREY_B, stroke_width=2)
        ticks = VGroup(*[Line([x0 + k * (x1 - x0) / 10, y - 0.15, 0], [x0 + k * (x1 - x0) / 10, y + 0.15, 0], color=GREY_C,
                              stroke_width=1.5) for k in range(11)])
        rnd = VGroup(*[Dot([x0 + u * (x1 - x0), y + 0.45, 0], radius=0.07, color=BAD) for u in g.random(10)])
        st_d = VGroup(*[Dot([x0 + (k + u) / 10 * (x1 - x0), y - 0.45, 0], radius=0.07, color=GOOD) for k, u in enumerate(g.random(10))])
        lab1 = label(r"10 plain uniforms: \ clumps by chance", font_size=22, color=BAD).next_to(line, UP, buff=0.75)
        lab2 = label(r"one uniform in each tenth: \ stratified", font_size=22, color=GOOD).next_to(line, DOWN, buff=0.75)
        rows = fit_rows(VGroup(
            MathTex(r"\hat I_{\text{strat}} = \frac1n \sum_{k=0}^{n-1} g\Big(\frac{k + U_k}{n}\Big)", font_size=30),
            label(r"the variance \emph{between} strata is removed: \ only the variance \emph{within} them remains (Part 5's Eve)",
                  font_size=22, color=GREY_A),
            MathTex(rf"e^U,\ n = 1000:\ \ \text{{variance }} {f:,.0f} \text{{ times smaller}}".replace(",", "{,}"), font_size=28,
                    color=S.ACCENT),
            label(r"the survey statistician's stratification (Part 18), \ applied to uniforms", font_size=22, color=GREY_A),
        ), 12.6, 0.28, [0, -1.9, 0])
        with self.voiceover(
            "A third trick comes from survey sampling. <bookmark mark='a'/> Plain uniforms clump by chance, leaving "
            "parts of the interval unvisited. <bookmark mark='b'/> Instead, cut the interval into n equal pieces and "
            "draw exactly one uniform inside each: stratified sampling. <bookmark mark='c'/> By Part 5's law of total "
            "variance, the error now comes only from variation within each piece; the variation between pieces is "
            f"gone. For our test integral with a thousand draws, the variance falls by a factor of about {f:,.0f}. "
            "Survey statisticians call this stratification, and Part 18 uses it on people instead of numbers."
        ) as vo:
            self.play(Create(line), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(rnd, lag_ratio=0.1), FadeIn(lab1))
            vo.wait_until("b")
            self.play(FadeIn(st_d, lag_ratio=0.1), FadeIn(lab2), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:]))
        self.clear_scene()
