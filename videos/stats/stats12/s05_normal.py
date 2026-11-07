from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats12.common import *  # noqa: F403


class NormalTheory(VoiceoverScene):
    def construct(self):
        self.card()
        self.distribution()
        self.tests_for_coefs()
        self.t_check()
        self.non_normal()
        self.f_test()
        self.anova_table()
        self.r2_caveats()

    def card(self):
        card = chapter_card(4, r"Normal theory", r"Standard errors, \ $t$, \ $F$ as Pythagoras", part=PART)
        with self.voiceover("Chapter four. Normal theory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def distribution(self):
        rows = [
            cmath(r"\hat\beta", r"\sim", r"N\big(\beta,\ \sigma^2(X^\top X)^{-1}\big)", font_size=34),
            cmath(r"\frac{\mathrm{RSS}}{\sigma^2}", r"\sim", r"\chi^2_{n-p},\ \ \text{independent of } \hat\beta", font_size=34),
            cmath(r"s^2", r"=", r"\frac{\mathrm{RSS}}{n - p}", font_size=34),
            cmath(r"\frac{\hat\beta_j - \beta_j}{s\sqrt{[(X^\top X)^{-1}]_{jj}}}", r"\sim", r"t_{n-p}", font_size=34),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"normal errors: \ $\hat\beta$ is linear in $y$"), why(r"Cochran's theorem (Part 8): \ the residual projection"),
                why(r"unbiased for $\sigma^2$"), why(r"Student's pivot: \ tests and intervals for each coefficient")]
        intro = label('Exact inference under the normal linear model', font_size=36)
        with self.voiceover(
            "For fixed full-column-rank X and independent mean-zero normal errors with common variance, exact inference follows. <bookmark mark='a'/> Beta-hat is linear in "
            "the normal y, so it's normal, centred at beta, with covariance sigma squared X transpose X inverse. "
            "<bookmark mark='b'/> The residual sum of squares over sigma squared is chi-squared with n minus p degrees of "
            "freedom, independent of beta-hat: Part 8's Cochran theorem, with the residual projection. "
            "<bookmark mark='c'/> So s squared, the residual sum of squares over n minus p, estimates sigma squared without "
            "bias. <bookmark mark='d'/> And each coefficient, standardized by its estimated standard error, is Student's t "
            "with n minus p degrees of freedom. This is the classical normal-model coefficient table; robust and generalized models use other approximations."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.7, x=-0.4, buff=0.55, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def t_check(self):
        d = load("normal")
        ed = np.asarray(d["t_edges"])
        xs = np.linspace(-4, 4, 200)
        A = axes([-4, 4], [0, 0.45], x_length=7.4, y_length=4.2, xlabel=r"$(\hat\beta_1 - \beta_1)/\widehat{\mathrm{SE}}$, \ samples of 30 families",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.2, 0.4], center=[-2.0, -0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, ed, np.asarray(d["t_hist"]), color=SIM, opacity=0.6)
        cv = curve(ax, xs, stats.t.pdf(xs, 28), OBS, 3)
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{true slope}} = {d['true']:.3f}", font_size=28, color=EXACT),
            MathTex(rf"\text{{SD of }}\hat\beta_1 = {d['sd']:.3f}", font_size=28),
            label(r"the curve: \ $t_{28}$", font_size=24, color=OBS),
            MathTex(rf"95\%\ \text{{intervals cover }} {100 * d['cover']:.1f}\%", font_size=28, color=HIT),
        ), 4.6, 0.36, [4.4, -0.3, 0])
        tag = simulated_tag(r"the World: \ 10,000 samples", corner=DR)
        with self.voiceover(
            "On the World's finite synthetic families, this is an empirical check of the normal approximation: <bookmark mark='a'/> the true slope, over all "
            "fifty thousand families, is point seven oh three. <bookmark mark='b'/> Take ten thousand samples of thirty, "
            "standardize each estimated slope by its own standard error, and the histogram follows Student's t with "
            "twenty-eight degrees of freedom. <bookmark mark='c'/> The ninety-five percent intervals cover ninety-five point "
            "three percent of the time. Kept."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars, lag_ratio=0.02), Create(cv), FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def f_test(self):
        d = load("normal")
        rows = [
            cmath(r"\mathrm{RSS}_{\text{small}}", r"=", r"\mathrm{RSS}_{\text{full}} + \|\hat y_{\text{full}} - \hat y_{\text{small}}\|^2", font_size=32),
            cmath(r"F", r"=", r"\frac{(\mathrm{RSS}_{\text{small}} - \mathrm{RSS}_{\text{full}})/q}{\mathrm{RSS}_{\text{full}}/(n - p)} \sim F_{q,\,n-p}",
                  font_size=32),
            cmath(r"\text{child on father, \ + mother}", r":", rf"F = {d['F']['F']:.1f},\ \ p = {d['F']['p']:.1e}".replace("e-0", r"\times 10^{-") + "}",
                  font_size=30),
            cmath(r"R^2", r":", rf"{d['r2_small']:.3f} \to {d['r2_full']:.3f}", r"\quad F = t^2 = " + f"{d['t_mother'] ** 2:.1f}", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"nested models: \ another right angle"), why(r"the extra fit per extra parameter, \ over the leftover noise"),
                why(r"100 families, \ heights in cm"), why(r"one added variable: \ the $F$-test is the $t$-test squared")]
        intro = label('Compare nested linear models', font_size=36)
        with self.voiceover(
            "Pythagoras also gives the F-test, for whether a group of variables matters. <bookmark mark='a'/> Fit a small "
            "model and a full one containing it. The small model's residual sum of squares is the full model's plus the "
            "squared distance between the two fits: another right angle. <bookmark mark='b'/> The F statistic divides the "
            "extra fit per extra parameter by the leftover noise per degree of freedom, and under the null that the extra "
            "coefficients are zero it has an F distribution, Snedecor's ratio from Part 8. <bookmark mark='c'/> A hundred "
            "families: child's height on father's, then adding mother's. F is twenty-three, p about six in a million. "
            "<bookmark mark='d'/> R squared rises from point zero three to point two one. With a single added variable, F is "
            "exactly the square of that variable's t statistic."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.6, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def r2_caveats(self):
        rows = fit_rows(VGroup(
            label(r"what $R^2$ is not", font_size=30, color=OBS),
            label(r"not a test: \ adding any variable never lowers it \ (adjusted $R^2$ penalizes)", font_size=24),
            label(r"not ``the share caused'': \ the father's 3\% here, \ the mother's 18\%, \ say nothing about mechanism", font_size=24),
            label(r"not comparable across samples: \ it depends on the spread of $x$ you happened to sample", font_size=24),
            label(r"not a check of linearity: \ Anscombe's four data sets all have $R^2 = 0.67$ (ch.~9)", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> R squared is the most quoted and most misread number in regression. "
            "<bookmark mark='b'/> It isn't a test: adding any variable, even pure noise, can only raise it. The adjusted "
            "version penalizes that. <bookmark mark='c'/> It isn't the share of the outcome caused by the predictors. "
            "<bookmark mark='d'/> It isn't comparable across samples, because it depends on how spread out the x's you "
            "happened to sample were. <bookmark mark='e'/> And it isn't a check that the model is right: chapter nine shows "
            "four datasets with identical R squared and wildly different shapes."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def anova_table(self):
        d = load("normal")
        tss, rs, rf = d["tss"], d["rss_small"], d["rss_full"]
        hdr = VGroup(*[label(t, font_size=24, color=GREY_B) for t in (r"source", r"sum of squares", r"df", r"mean square", r"$F$")])
        xs = [-4.6, -1.8, 0.6, 2.6, 4.8]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 2.0, 0])
        ms_res = rf / 97
        lines = [(r"father", tss - rs, 1, (tss - rs), (tss - rs) / ms_res), (r"mother, \ given father", rs - rf, 1, rs - rf, (rs - rf) / ms_res),
                 (r"residual", rf, 97, ms_res, None), (r"total", tss, 99, None, None)]
        cells = VGroup()
        for i, (nm, ss, df, ms, f) in enumerate(lines):
            y = 1.3 - 0.6 * i
            cells.add(VGroup(label(nm, font_size=24).move_to([xs[0], y, 0]), MathTex(f"{ss:,.0f}".replace(",", "{,}"), font_size=28).move_to([xs[1], y, 0]),
                             MathTex(str(df), font_size=28).move_to([xs[2], y, 0]),
                             MathTex("" if ms is None else f"{ms:,.1f}".replace(",", "{,}"), font_size=28).move_to([xs[3], y, 0]),
                             MathTex("" if f is None else f"{f:.1f}", font_size=28, color=OBS).move_to([xs[4], y, 0])))
        foot = fit_rows(VGroup(
            label(r"the analysis of variance: \ Pythagoras, \ one right angle per row", font_size=26, color=OBS),
            label(r"sequential sums of squares depend on the order the variables enter, \ unless the columns are orthogonal", font_size=22,
                  color=GREY_A),
            label(r"orthogonal columns are what a designed experiment builds: \ Part 13", font_size=22, color=GREY_A),
        ), 12.6, 0.3, [0, -2.2, 0])
        with self.voiceover(
            "The nested sums of squares are usually laid out in a table, the analysis of variance, Fisher's invention. "
            "<bookmark mark='a'/> The total sum of squares of the hundred children's heights splits into the part explained "
            "by fathers, the extra part explained by mothers given fathers, and the residual. Each split is one of chapter "
            "two's right angles. <bookmark mark='b'/> Divide each by its degrees of freedom to get mean squares, and each F is "
            "a mean square over the residual mean square: twenty-three for the mother, as before. "
            "<bookmark mark='c'/> One subtlety: these sequential sums of squares depend on the order in which variables "
            "enter, unless the columns are orthogonal. Making them orthogonal on purpose is exactly what a designed "
            "experiment does, in Part 13."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cells], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1:]))
        self.clear_scene()

    def non_normal(self):
        from explainer.stats.kit import ols as O
        g = np.random.Generator(np.random.PCG64(1810))
        R = 6000
        res = {}
        for n in (10, 30, 100):
            hits = 0
            for _ in range(R):
                x = g.uniform(0, 1, n)
                e = g.exponential(size=n) - 1
                y = 1 + 2 * x + e
                lo, hi = O.fit(O.design(x), y).ci()[1]
                hits += lo <= 2 <= hi
            res[n] = hits / R
        rows = [
            cmath(r"\hat\beta_1 - \beta_1", r"=", r"\sum_i w_i\,\varepsilon_i,\quad w_i = \frac{x_i - \bar x}{\sum_j (x_j - \bar x)^2}", font_size=32),
            cmath(r"\text{skewed errors (exponential)}", r":", rf"n = 10:\ {100 * res[10]:.1f}\%,\ \ 30:\ {100 * res[30]:.1f}\%,\ \ 100:\ {100 * res[100]:.1f}\%",
                  font_size=30),
        ]
        rows[1][2].set_color(HIT)
        whys = [why(r"a weighted average of the errors: \ finite error variance, \ non-dominating leverage: \ a CLT can apply"),
                why(r"6,000 samples each: \ the $t$-interval for the slope still covers")]
        foot = label(r"normality matters for small samples and for prediction intervals; \ this simulated design behaves well; \ no universal small-sample guarantee", font_size=24,
                     color=OBS).to_edge(DOWN, buff=0.8)
        intro = label('Check a well-spread design with skewed errors', font_size=36)
        with self.voiceover(
            "How much does the normality assumption matter? <bookmark mark='a'/> The slope's error is a weighted average of the "
            "errors. With finite variance and no observation dominating, a weighted central limit theorem can apply. <bookmark mark='b'/> With "
            "strongly skewed exponential errors, the ninety-five percent interval for the slope covers ninety-five percent "
            "with ten observations, and with thirty, and with a hundred. <bookmark mark='c'/> Normality matters for very "
            "small samples and, as Part 11 showed, for prediction intervals, which concern a single error. These results are specific to this well-spread design; skewness, extreme leverage or infinite moments can defeat a small-sample approximation."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=1.8, x=-0.4, buff=1.0, edge=6.9)
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def tests_for_coefs(self):
        from explainer.stats.kit import ols as O
        d = load("dummies")
        r = O.fit(O.design(np.asarray(d["mid"]), np.asarray(d["son"])), np.asarray(d["y"]))
        names = [r"\text{intercept}", r"\text{mid-parent}", r"\text{son}"]
        hdr = VGroup(*[label(t, font_size=24, color=GREY_B) for t in (r"", r"estimate", r"SE", r"$t$", r"95\% interval")])
        xs = [-4.6, -2.2, -0.4, 1.2, 3.8]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 1.8, 0])
        ci = r.ci()
        cells = VGroup()
        for i in range(3):
            y = 1.1 - 0.6 * i
            cells.add(VGroup(MathTex(names[i], font_size=28).move_to([xs[0], y, 0]), MathTex(f"{r.coef[i]:.3f}", font_size=28).move_to([xs[1], y, 0]),
                             MathTex(f"{r.se()[i]:.3f}", font_size=28).move_to([xs[2], y, 0]),
                             MathTex(f"{r.t()[i]:.1f}", font_size=28, color=OBS).move_to([xs[3], y, 0]),
                             MathTex(rf"[{ci[i, 0]:.2f},\ {ci[i, 1]:.2f}]", font_size=28).move_to([xs[4], y, 0])))
        foot = fit_rows(VGroup(
            label(r"the coefficient table every package prints: \ estimate, \ SE, \ $t$ on $n - p = 397$ df, \ interval", font_size=24),
            label(r"each $t$ tests one coefficient \emph{given all the others} (FWL)", font_size=24, color=OBS),
            label(r"the intercept's test (``mean height at parents of 0 cm'') is meaningless here", font_size=22, color=GREY_A),
        ), 12.6, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the coefficient table that every statistics package prints, for the dummy-variable "
            "model of the World's four hundred families: each estimate, its standard error, its t statistic on three hundred "
            "and ninety-seven degrees of freedom, and its interval. <bookmark mark='b'/> Read each t as a test of one "
            "coefficient given all the others in the model, in the sense of Frisch–Waugh–Lovell. <bookmark mark='c'/> And not "
            "every row is a sensible question: the intercept's test asks about children of parents zero centimetres tall."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cells], lag_ratio=0.4), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()
