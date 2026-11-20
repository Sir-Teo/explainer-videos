from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Calibrate(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Calibration", r"Where do a model's numbers come from?", "Chapter seven. Calibration.",
             lit={1982: r"Kydland and Prescott", 1996: r"Hansen and Heckman"}, scale=("nation",),
             horizon=("a quarter", "a century"))
        self.targets()
        self.steady()
        self.argument()

    def targets(self):
        C = load("calibrate")
        M = C["model"]
        y0, y1 = C["years"]
        heads = (r"parameter", r"pinned down by", rf"US data, \ {y0}--{y1}", r"the Island")
        xs = [-5.2, -1.8, 2.0, 5.0]
        hrow = VGroup(*[label(h, font_size=20, color=GREY_B).move_to(RIGHT * x + UP * 2.35) for h, x in zip(heads, xs)])
        data_rows = [
            (r"$\alpha$, \ capital's share", r"labour's share of income", rf"{C['labsh']:.2f} $\Rightarrow$ "
             rf"$\alpha$ = {C['alpha_data']:.2f}", rf"{M['alpha']:.2f}", INVEST),
            (r"$\beta$, \ patience", r"the real interest rate", r"about 4\% a year",
             rf"{M['beta']} a quarter \ ({100 * M['r_annual']:.1f}\%)", VALUE),
            (r"$\delta$, \ depreciation", r"investment and the capital stock", rf"{100 * C['delta']:.1f}\% a year",
             rf"{100 * M['delta']:.1f}\% a quarter", HOLD),
            (r"$\bar n$, \ hours", r"time spent at work", rf"{C['hours']:,.0f} hours a year: \ "
             rf"{C['hours_share']:.2f} of waking time".replace(",", "{,}"), r"one third", HOURS),
            (r"$\rho$, \ $\sigma$, \ technology", r"the Solow residual's persistence \\ and size", r"chapter ten",
             rf"{M['rho']}, \ {100 * M['sigma']:.1f}\%", TECH),
        ]
        rows = VGroup()
        for n, (a, b, c, d, col) in enumerate(data_rows):
            y = 1.45 - 0.85 * n
            rows.add(VGroup(label(a, font_size=20, color=col).move_to(RIGHT * xs[0] + UP * y),
                            label(b, font_size=18, color=GREY_A).move_to(RIGHT * xs[1] + UP * y),
                            label(c, font_size=18).move_to(RIGHT * xs[2] + UP * y),
                            label(d, font_size=19, color=col).move_to(RIGHT * xs[3] + UP * y)))
        rule = Line(LEFT * 6.6, RIGHT * 6.6, stroke_color=GREY_D, stroke_width=1.5).move_to(UP * 1.98)
        foot = label(r"the data's depreciation counts houses and buildings that last a century; \ the Island's "
                     r"capital is shorter-lived machinery", font_size=16, color=GREY_B).to_edge(DOWN, buff=0.55)
        tag = data_tag(r"Penn World Table 11.0, \ United States; \ the Island's truths", corner=DR, font_size=12)
        with self.voiceover(
            "The model has a handful of numbers to choose. Kydland and Prescott's rule was to take them from facts "
            "that have nothing to do with the cycle, and only then ask the model about the cycle. "
            f"<bookmark mark='a'/> Capital's share alpha comes from the share of income paid to labour: in the Penn "
            f"World Table it averaged {C['labsh']:.2f} for America from {y0} to {y1}, so alpha is about "
            f"{C['alpha_data']:.2f}. The Island uses the classic {M['alpha']:.2f}. <bookmark mark='b'/> Patience comes "
            "from the real interest rate. At about four percent a year, beta is 0.99 a quarter. "
            "<bookmark mark='c'/> Depreciation is a choice about what counts as capital. The table's rate, "
            f"{100 * C['delta']:.1f} percent a year, includes houses and buildings that last a century; the Island "
            "takes the textbook two and a half percent a quarter, for machinery. <bookmark mark='d'/> Hours: "
            f"Americans worked about {C['hours']:,.0f} hours a year, roughly a third of their waking time. "
            "<bookmark mark='e'/> And technology's persistence and the size of its shocks come from the measured "
            "Solow residual, which chapter ten examines."
        ) as vo:
            self.play(FadeIn(hrow), FadeIn(rule), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            self.play(FadeIn(foot))
        self.clear_scene()

    def steady(self):
        R = load("rbc")["ss"]
        C = load("calibrate")
        eqs = VGroup(
            MathTex(r"\text{Euler: }\ 1 = \beta\Big(\alpha \frac{\bar y}{\bar k} + 1 - \delta\Big)"
                    r"\ \Rightarrow\ \frac{\bar k}{\bar y} = \frac{\alpha}{1/\beta - 1 + \delta}", font_size=32),
            MathTex(r"\text{investment: }\ \frac{\bar\imath}{\bar y} = \delta\, \frac{\bar k}{\bar y}", font_size=32),
            MathTex(r"\text{hours: }\ A\, \bar c = (1-\alpha)\frac{\bar y}{\bar n}\ \Rightarrow\ A", font_size=32),
        ).arrange(DOWN, buff=0.45).move_to(UP * 1.4)
        nums = VGroup(
            label(rf"capital: \ {R['ky']:.1f} quarters of output \ ({R['ky'] / 4:.1f} years; \ the table: "
                  rf"{C['ky']:.1f})", font_size=22, color=INVEST),
            label(rf"investment: \ {100 * R['iy']:.1f}\% of output \ (the table: {100 * C['iy']:.0f}\%)",
                  font_size=22, color=INVEST),
            label(rf"consumption: \ {100 * R['cy']:.1f}\%; \ $A = {R['A']:.2f}$ \ gives hours of one third",
                  font_size=22, color=CONS),
        ).arrange(DOWN, buff=0.35).next_to(eqs, DOWN, buff=0.5)
        tag = data_tag(r"the Island's truths; \ Penn World Table 11.0", corner=DR, font_size=12)
        with self.voiceover(
            "With the numbers chosen, the model's long-run state follows from three equations. "
            "<bookmark mark='a'/> In the steady state the Euler equation says the return on capital must just repay "
            "impatience and wear, which fixes the ratio of capital to output. <bookmark mark='b'/> Investment must "
            "replace what wears out. <bookmark mark='c'/> And the hours condition sets the weight on leisure, A, so "
            f"that people work a third of their time. <bookmark mark='d'/> The Island holds {R['ky']:.1f} quarters "
            f"of output as capital, {R['ky'] / 4:.1f} years, less than the table's {C['ky']:.1f} because its capital "
            f"wears out faster. It invests {100 * R['iy']:.0f} percent of output, close to the data's "
            f"{100 * C['iy']:.0f}, and consumes the rest. The long-run facts are matched by construction. The test "
            "is whether the short-run facts, which were never targeted, come out right."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, e in zip("abc", eqs):
                vo.wait_until(mk)
                self.play(Write(e), run_time=1.2)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in nums], lag_ratio=0.5), run_time=2)
        self.clear_scene()

    def argument(self):
        left = VGroup(
            label(r"calibrate", font_size=28, color=VALUE),
            label(r"every model is false by design", font_size=20, color=GREY_A),
            label(r"match long-run facts; \\ judge on facts not used", font_size=20, color=GREY_A),
            label(r"borrow numbers from \\ micro studies and growth", font_size=20, color=GREY_A),
            label(r"Kydland and Prescott, \ 1996: \\ ``the computational experiment''", font_size=18,
                  color=VALUE),
        ).arrange(DOWN, buff=0.35)
        right = VGroup(
            label(r"estimate", font_size=28, color=TECH),
            label(r"without standard errors, \\ a good fit may be luck", font_size=20, color=GREY_A),
            label(r"a micro number need not \\ fit a macro model \\ (the Frisch elasticity!)", font_size=20,
                  color=GREY_A),
            label(r"choose all the numbers \\ to fit all the data", font_size=20, color=GREY_A),
            label(r"Hansen and Heckman, \ 1996: \\ ``the empirical foundations of calibration''", font_size=18,
                  color=TECH),
        ).arrange(DOWN, buff=0.35)
        VGroup(left, right).arrange(RIGHT, buff=2.0).move_to(UP * 0.4)
        bar = Line(UP * 2.6, DOWN * 1.6, stroke_color=GREY_D).move_to((left.get_right() + right.get_left()) / 2)
        end = label(r"today: \ estimate the whole model by likelihood, \ with priors that carry the calibrator's "
                    r"knowledge \ (Part 55)", font_size=21, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"\emph{Journal of Economic Perspectives} 10(1) (1996): \ Kydland and Prescott; \ "
                            r"Hansen and Heckman", corner=DR, font_size=12)
        with self.voiceover(
            "Calibration started a long argument. <bookmark mark='a'/> On one side, Kydland and Prescott, writing "
            "in 1996: every model is deliberately false, so it should not be judged by a statistical test it is "
            "bound to fail. Match the long-run facts, borrow numbers from studies of growth and of individuals, and "
            "judge the model on facts it was not built to match. <bookmark mark='b'/> On the other, Lars Peter "
            "Hansen and James Heckman, in the same issue of the same journal: without standard errors, a good fit "
            "may be luck; a number measured on individuals need not apply to a whole economy, as the Frisch "
            "elasticity shows; and the honest procedure is to choose all the numbers to fit all the data. "
            "<bookmark mark='c'/> The argument ended in a compromise. Modern models are estimated as a whole, by "
            "likelihood, with prior beliefs about the parameters that carry the calibrator's knowledge. Part "
            "fifty-five does it."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(bar))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in left], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in right], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
