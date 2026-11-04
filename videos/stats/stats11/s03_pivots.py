from __future__ import annotations

import numpy as np

from videos.stats.stats11.common import *  # noqa: F403


class Pivots(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.catalogue()
        self.shortest()
        self.tanks()
        self.approximate()

    def card(self):
        card = chapter_card(2, r"Pivots", r"A quantity whose distribution does not depend on $\theta$", part=PART)
        with self.voiceover("Chapter two. Pivots."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"Q(X, \theta)", r"\sim", r"F_Q \quad\text{the same for every } \theta", font_size=34),
            cmath(r"P_\theta\big(a \le Q(X, \theta) \le b\big)", r"=", r"1 - \alpha", font_size=34),
            cmath(r"C(X)", r"=", r"\{\theta : a \le Q(X, \theta) \le b\}", font_size=34),
            cmath(r"\frac{\bar X - \mu}{s/\sqrt n} \sim t_{n-1}", r"\Rightarrow", r"\bar x \pm t_{n-1, 0.975}\,\frac{s}{\sqrt n}", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        rows[3][2].set_color(OBS)
        whys = [why(r"a \emph{pivot}: \ data and parameter together, \ a known law"), why(r"pick its $\alpha/2$ and $1 - \alpha/2$ quantiles"),
                why(r"solve for $\theta$: \ the coverage is exact, \ for every $\theta$"), why(r"Student's pivot (Part 8) gives the $t$-interval")]
        with self.voiceover(
            "The cleanest way to keep Neyman's promise is a pivot. <bookmark mark='a'/> A pivot is a function of the "
            "data and the parameter together whose distribution is the same, whatever the parameter is. "
            "<bookmark mark='b'/> Then pick two quantiles of that known distribution: the pivot lands between them with "
            "probability exactly one minus alpha. <bookmark mark='c'/> Solve the inequalities for theta, and the set of "
            "parameters satisfying them is an interval whose coverage is exactly one minus alpha, for every theta at "
            "once. <bookmark mark='d'/> Student's t statistic is the classic pivot: its distribution is t with n minus "
            "one degrees of freedom whatever mu and sigma are, and solving gives the t-interval of the last chapter."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def catalogue(self):
        d = load("pivots")
        items = [
            (r"normal mean", r"\frac{\bar X - \mu}{s/\sqrt n} \sim t_{n-1}", r"\bar x \pm t\,s/\sqrt n"),
            (r"normal variance", r"\frac{(n-1)s^2}{\sigma^2} \sim \chi^2_{n-1}", r"\Big[\frac{(n-1)s^2}{\chi^2_{0.975}},\ \frac{(n-1)s^2}{\chi^2_{0.025}}\Big]"),
            (r"variance ratio", r"\frac{s_1^2/\sigma_1^2}{s_2^2/\sigma_2^2} \sim F", r"\Big[\frac{s_1^2/s_2^2}{F_{0.975}},\ \frac{s_1^2/s_2^2}{F_{0.025}}\Big]"),
            (r"exponential rate", r"\lambda \textstyle\sum X_i \sim \mathrm{Gamma}(n, 1)", r"\Big[\frac{G_{0.025}}{\sum x_i},\ \frac{G_{0.975}}{\sum x_i}\Big]"),
            (r"uniform$(0, \theta)$", r"M/\theta \sim \mathrm{Beta}(n, 1)", r"\big[M,\ M\,\alpha^{-1/n}\big]"),
        ]
        hdr = VGroup(label(r"model", font_size=22, color=GREY_B), label(r"pivot", font_size=22, color=GREY_B),
                     label(r"95\% interval", font_size=22, color=GREY_B))
        rows = VGroup(hdr)
        for nm, pv, iv in items:
            rows.add(VGroup(label(nm, font_size=24, color=GREY_A), MathTex(pv, font_size=26), MathTex(iv, font_size=26, color=OBS)))
        rows.arrange(DOWN, buff=0.26).move_to([0, 0.5, 0])
        for r in rows:
            r[0].set_x(-5.2)
            r[1].set_x(-1.2)
            r[2].set_x(3.8)
        foot = label(rf"checked: \ rate interval {100 * d['rate']:.1f}\%, \ $F$ interval {100 * d['F']:.1f}\% \ (20,000 samples each)", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The pivots of the textbook. <bookmark mark='a'/> The normal mean, by Student's t. <bookmark mark='b'/> The "
            "normal variance, by Part 8's chi-squared, divided into the sum of squares. <bookmark mark='c'/> The ratio of "
            "two normal variances, by Snedecor's F. <bookmark mark='d'/> The exponential rate: lambda times the total "
            "waiting time is a gamma variable with shape n, whatever lambda is. <bookmark mark='e'/> And the uniform on "
            "zero to theta, the continuous tank problem: the maximum over theta has a fixed beta distribution. "
            "<bookmark mark='f'/> Simulation confirms the coverage: ninety-five point four and ninety-four point nine "
            "percent, both within Monte Carlo error. Each interval is exact, but only if its model is right: the "
            "variance interval, for example, needs normal data, as Part 8's coverage check showed."
        ) as vo:
            self.play(FadeIn(hdr))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1], shift=RIGHT * 0.2))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def tanks(self):
        m, k = 214, 6
        up = m * 0.05 ** (-1 / k)
        rows = [
            cmath(r"P_\theta\Big(\frac{M}{\theta} \le u\Big)", r"=", r"u^k", font_size=34),
            cmath(r"P_\theta\Big(\frac{M}{\theta} \ge 0.05^{1/k}\Big)", r"=", r"0.95", font_size=34),
            cmath(r"\theta", r"\in", rf"\big[M,\ M \cdot 0.05^{{-1/k}}\big] = [{m},\ {up:.0f}]", font_size=34),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"all $k$ draws below $u\theta$"), why(r"a one-sided 95\% statement"), why(r"Part 9's factory: \ $M = 214$, \ $k = 6$; \ the truth, 300, is inside")]
        foot = label(r"the interval starts at the data's maximum, \ as it must: \ the support moves with $\theta$", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Back to Part 9's tanks, treated as continuous. <bookmark mark='a'/> The chance that all k serials fall "
            "below a fraction u of N is u to the k. <bookmark mark='b'/> So the maximum over N is at least point zero "
            "five to the one over k with probability ninety-five percent. <bookmark mark='c'/> Solve: N lies between the "
            "maximum and the maximum times point zero five to the minus one over k. For the factory with six captured "
            "tanks and a largest serial of two hundred and fourteen, that's two hundred and fourteen to three hundred and "
            "fifty-three, and the truth, three hundred, is inside. <bookmark mark='d'/> The interval starts exactly at the "
            "largest serial seen, as it must."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=0.9, edge=6.9)
            for kk, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(kk, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def approximate(self):
        rows = fit_rows(VGroup(
            label(r"most problems have no exact pivot; \ the asymptotic one is", font_size=28),
            MathTex(r"\frac{\hat\theta - \theta}{\widehat{\mathrm{SE}}} \approx N(0, 1) \ \Rightarrow\ \hat\theta \pm 1.96\,\widehat{\mathrm{SE}}",
                    font_size=34, color=OBS),
            label(r"the Wald interval for any parameter, \ from Part 9's curvature", font_size=24, color=GREY_A),
            label(r"it fails when the SE is badly estimated, \ or depends on $\theta$ itself: \ $\sqrt{\hat p(1 - \hat p)/n}$ is 0 when $x = 0$",
                  font_size=24, color=MISS),
            label(r"the cure: \ invert a test that uses the null's own SE \ (next chapter), \ or transform first (log-odds, Fisher's $z$)",
                  font_size=24, color=GREY_A),
        ), 12.6, 0.4, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Most problems have no exact pivot. The universal fallback is asymptotic: <bookmark mark='b'/> "
            "the estimate minus the truth, over the estimated standard error, is approximately standard normal, so the "
            "estimate plus or minus one point nine six standard errors is an approximate ninety-five percent interval. "
            "<bookmark mark='c'/> That's the Wald interval for any parameter, with Part 9's curvature supplying the "
            "standard error. <bookmark mark='d'/> It fails when the standard error is poorly estimated, or depends on the "
            "parameter itself. For a proportion, the estimated standard error is zero whenever the count is zero, and the "
            "interval shrinks to a point. <bookmark mark='e'/> There are two cures: invert a test that uses the standard "
            "error the null hypothesis implies, which is the next chapter, or transform to a scale where the "
            "approximation is better, like the log-odds or Fisher's z."
        ) as vo:
            for kk, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[kk], shift=RIGHT * 0.2))
        self.clear_scene()

    def shortest(self):
        from scipy import optimize, stats as st
        df = 9

        def gap(a):
            b = st.chi2.ppf(st.chi2.cdf(a, df) + 0.95, df)
            return a * a * st.chi2.pdf(a, df) - b * b * st.chi2.pdf(b, df)

        a = optimize.brentq(gap, 0.5, st.chi2.ppf(0.0499, df))
        b = st.chi2.ppf(st.chi2.cdf(a, df) + 0.95, df)
        ae, be = st.chi2.ppf(0.025, df), st.chi2.ppf(0.975, df)
        xs = np.linspace(0.05, 30, 300)
        A = axes([0, 30], [0, 0.11], x_length=7.2, y_length=3.6, xlabel=r"$(n-1)s^2/\sigma^2 \sim \chi^2_9$", xticks=[0, ae, a, b, be, 30],
                 xfmt=lambda v: f"{v:.1f}", center=[-2.4, 0.6, 0], font_size=18)
        ax = A.ax
        cv = curve(ax, xs, st.chi2.pdf(xs, df), GREY_A, 3)
        eq = VGroup(DashedLine(ax.c2p(ae, 0), ax.c2p(ae, 0.11), color=S.LIK), DashedLine(ax.c2p(be, 0), ax.c2p(be, 0.11), color=S.LIK))
        sh = VGroup(DashedLine(ax.c2p(a, 0), ax.c2p(a, 0.11), color=OBS), DashedLine(ax.c2p(b, 0), ax.c2p(b, 0.11), color=OBS))
        rows = fit_rows(VGroup(
            label(r"any two quantiles 95\% apart make a 95\% interval", font_size=24),
            MathTex(rf"\text{{equal tails: }}\ \sigma^2 \in \Big[\tfrac{{ss}}{{{be:.2f}}},\ \tfrac{{ss}}{{{ae:.2f}}}\Big]", font_size=26, color=S.LIK),
            MathTex(rf"\text{{shortest: }}\ \sigma^2 \in \Big[\tfrac{{ss}}{{{b:.2f}}},\ \tfrac{{ss}}{{{a:.2f}}}\Big]", font_size=26, color=OBS),
            label(rf"{100 * (1 - (1 / a - 1 / b) / (1 / ae - 1 / be)):.0f}\% shorter, \ same coverage; \ the textbooks use equal tails anyway", font_size=22,
                  color=GREY_A),
            label(r"optimal: \ $a^2 f(a) = b^2 f(b)$ \ (Casella \& Berger, \ ch.~9)", font_size=22, color=GREY_A),
        ), 5.0, 0.3, [4.4, -0.2, 0])
        with self.voiceover(
            "A pivot doesn't fix the interval uniquely. <bookmark mark='a'/> Any two quantiles that enclose ninety-five "
            "percent of the pivot's distribution give a ninety-five percent interval. For the variance, the pivot is "
            "chi-squared, which is skewed. <bookmark mark='b'/> The usual choice cuts two and a half percent from each "
            "tail. <bookmark mark='c'/> But the shortest interval for sigma squared uses different cut points, found by "
            "solving a small equation, and with ten observations it's about sixteen percent shorter, with exactly the "
            "same coverage. <bookmark mark='d'/> Equal tails remain the convention, because they're simple and they "
            "invert a two-sided test with equal error in each direction."
        ) as vo:
            self.play(FadeIn(A), Create(cv))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(eq), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(sh), FadeIn(rows[2:4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
