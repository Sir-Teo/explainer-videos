from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Premia(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Risk premia and the consumption CAPM", r"How much risk aversion does the stock market's "
             r"premium imply?", "Chapter seven. Risk premia and the consumption CAPM.",
             lit={1979: r"Breeden", 1978: r"Lucas"}, scale=("market", "nation"), horizon=("a year", "a century"))
        self.ccapm()
        self.data()

    def ccapm(self):
        rows = VGroup(
            label(r"with power utility, \ $u'(c) = c^{-\gamma}$, \ and small changes:", font_size=24, color=GREY_A),
            MathTex(r"m_{t+1} \;\approx\; \beta\,\big(1 - \gamma\,\Delta \ln c_{t+1}\big)", font_size=44, color=SDF),
            MathTex(r"\mathbb{E}[R] - R_f \;\approx\; \gamma\;\operatorname{cov}\big(\Delta \ln c,\; R\big)",
                    font_size=48, color=STOCK),
            label(r"the consumption CAPM: \ an asset's premium is risk aversion times its covariance with consumption "
                  r"growth", font_size=22, color=WHITE),
            label(r"Douglas Breeden, \ 1979; \ tested by Hansen and Singleton, \ 1982", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Breeden, JFE 7(3) (1979); \ Hansen and Singleton, Econometrica 50(5) (1982)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Now put a number on it. <bookmark mark='a'/> With power utility, marginal utility is consumption to the "
            "minus gamma, and for small changes the discount factor falls one for one with gamma times consumption "
            "growth. <bookmark mark='b'/> So the premium on any asset is approximately gamma, the coefficient of "
            "relative risk aversion, times the covariance of the asset's return with consumption growth. "
            "<bookmark mark='c'/> This is the consumption capital asset pricing model. <bookmark mark='d'/> Douglas "
            "Breeden derived it in 1979, and Lars Peter Hansen and Kenneth Singleton built the econometrics to "
            "test it."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(tag))
            for mk, r_ in zip("bcd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def data(self):
        c = load("ccapm")
        mo = c["mp_window"]
        lg = c["long"]
        rows = VGroup(
            label(r"Shiller's data: \ the S\&P composite, \ one-year bonds, \ consumption per head", font_size=23,
                  color=GREY_A),
            VGroup(label(r"", font_size=20), label(r"1889--1978", font_size=22, color=STOCK),
                   label(r"1889--2009", font_size=22, color=STOCK)).arrange(RIGHT, buff=1.2),
        )
        lines = [
            (r"stocks, \ real return a year", "stock", pc),
            (r"one-year bonds", "bill", pc),
            (r"the premium", "premium", pc),
            (r"consumption growth \ (s.d.)", "sd_growth", pc),
            (r"correlation of returns with growth", "corr", lambda v: f"{v:.2f}"),
            (r"covariance", "cov", lambda v: f"{v:.4f}"),
            (r"implied $\gamma$ = premium $\div$ covariance", "implied_gamma", lambda v: f"{v:.0f}"),
        ]
        grid = VGroup()
        for k, (name, key, f) in enumerate(lines):
            hot = key == "implied_gamma"
            col = HOLD if hot else WHITE
            row = VGroup(label(name, font_size=20, color=col if hot else GREY_A),
                         label(f(mo[key]), font_size=22, color=col), label(f(lg[key]), font_size=22, color=col))
            grid.add(row)
        for k, row in enumerate(grid):
            row[0].move_to([-3.4, 1.15 - 0.55 * k, 0], aligned_edge=RIGHT)
            row[1].move_to([0.3, 1.15 - 0.55 * k, 0])
            row[2].move_to([2.9, 1.15 - 0.55 * k, 0])
        rows[0].move_to(UP * 2.9)
        rows[1][1].move_to([0.3, 1.8, 0])
        rows[1][2].move_to([2.9, 1.8, 0])
        verdict = label(r"economists think $\gamma$ between 1 and 10 is plausible: \ the stock market asks for more",
                        font_size=23, color=E.ACCENT).to_edge(DOWN, buff=0.7)
        tag = data_tag(r"Shiller, \emph{Market Volatility} ch.\ 26 data, \ updated; \ annual, \ real", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Here is the formula on a century of American data, from Robert Shiller's series: real returns on the "
            "S and P composite and on one-year bonds, and real consumption per head. <bookmark mark='a'/> From 1889 "
            f"to 1978, Mehra and Prescott's window, stocks returned {100 * mo['stock']:.1f} percent a year after "
            f"inflation, bonds {100 * mo['bill']:.1f}: a premium of {100 * mo['premium']:.1f} points. "
            "<bookmark mark='b'/> Consumption growth was smooth, a standard deviation of about "
            f"{100 * mo['sd_growth']:.0f} percent, and its correlation with stock returns about "
            f"{mo['corr']:.2f}, so the covariance is tiny: {mo['cov']:.4f}. <bookmark mark='c'/> The premium divided "
            f"by the covariance gives the risk aversion the model needs: about {mo['implied_gamma']:.0f}, and over "
            f"the longer span about {lg['implied_gamma']:.0f}. <bookmark mark='d'/> Most economists think a gamma "
            "between one and ten describes how people actually trade off risk. The stock market seems to ask for "
            "more, and Mehra and Prescott's calculation, next, shows the trouble runs deeper than one number."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1][1:]), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in grid[:3]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in grid[3:6]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(grid[6]))
            vo.wait_until("d")
            self.play(FadeIn(verdict))
        self.clear_scene()
