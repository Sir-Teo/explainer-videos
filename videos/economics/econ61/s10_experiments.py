from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403


class Experiments(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Experiments at scale", r"Thousands of A/B tests a year: \ how many of their winners are "
             r"real?", "Chapter eight. Experiments at scale.",
             lit={2013: r"CUPED", 2020: r"Kohavi, Tang and Xu"}, scale=("firm",), horizon=("a day", "a year"))
        self.peeking()
        self.cuped()
        self.habits()

    def peeking(self):
        P = load("peeking")
        days = P["days"]
        ax = plane([1, days], [-3.6, 3.6], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.6, y_length=4.8,
                   xticks=[1, 10, 20, 30], yticks=[-3, -2, -1, 0, 1, 2, 3], xlabel=r"day of the test",
                   ylabel=r"z statistic, \ B against A", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        band_ = Rectangle(width=ax.ax.c2p(days, 0)[0] - ax.ax.c2p(1, 0)[0],
                          height=ax.ax.c2p(1, 1.96)[1] - ax.ax.c2p(1, -1.96)[1], stroke_width=0, fill_color=GREY_D,
                          fill_opacity=0.5).move_to(ax.ax.c2p((1 + days) / 2, 0))
        x = np.arange(1, days + 1)
        lines = VGroup(*[path(ax, x, z, SURGE if max(abs(np.array(z))) > 1.96 else GREY_B, 2.0, smooth=False)
                         for z in P["paths"]])
        reds = [m for z, m in zip(P["paths"], lines) if max(abs(np.array(z))) > 1.96]
        side = VGroup(
            label(r"A/A tests: \ both arms identical, \ 2,000 users a day each".replace(",", "{,}"), font_size=19,
                  color=WHITE),
            label(r"grey band: \ not significant at 5\%", font_size=19, color=GREY_A),
            label(rf"read once, \ at the end: \ {100 * P['last']:.0f}\% `significant'", font_size=21, color=GAIN),
            label(rf"read every day, \ stop at the first star: \ {100 * P['ever']:.0f}\%", font_size=21,
                  color=SURGE),
            label(r"the fix: \ fix the length in advance, \\ or use tests valid at every look \ (sequential tests, \ "
                  r"\emph{Statistics, Built})", font_size=18, color=TEST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        if side.width > 5.8:
            side.width = 5.8
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ 2,000 A/A tests of a 5\% conversion rate; \ agora.platform.peeking"
                         .replace(",", "{,}"), corner=DL, font_size=12)
        with self.voiceover(
            "Large platforms run thousands of experiments a year, and the first thing that goes wrong is "
            "impatience. <bookmark mark='a'/> Here are A/A tests on the Island: both arms see exactly the same "
            "page, two thousand users a day each, so there is nothing to find. <bookmark mark='b'/> The grey band "
            "is where the difference is not significant at five percent. <bookmark mark='c'/> Read each test once, "
            f"at the end of thirty days, and {100 * P['last']:.0f} percent cross the line, as they should. "
            "<bookmark mark='d'/> But a dashboard that updates every morning invites a peek, and a test stopped "
            f"at the first significant day declares a winner {100 * P['ever']:.0f} percent of the time. Red lines "
            "are the tests that would have shipped a change that does nothing. <bookmark mark='e'/> The fixes are "
            "old: decide the length in advance, or use tests whose error rate holds at every look, the sequential "
            "methods of Statistics, Built."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(band_), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(m) for m in lines], lag_ratio=0.15), FadeIn(side[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), *[Indicate(m, color=SURGE, scale_factor=1.0) for m in reds])
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def cuped(self):
        C = load("cuped")
        s0, s1 = C["sd_plain"], C["sd_cuped"]
        xs = np.linspace(-0.035, 0.075, 220)
        eff = 0.02

        def pdf(x, s):
            return np.exp(-0.5 * ((x - eff) / s) ** 2) / (s * np.sqrt(2 * np.pi))

        top = pdf(eff, s1) * 1.15
        ax = plane([-0.035, 0.075], [0, top], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.6, y_length=4.4,
                   xticks=[-0.02, 0, 0.02, 0.04, 0.06], yticks=[], xlabel=r"the estimated effect",
                   xfmt=lambda v: f"{v:+.2f}".replace("-", "{-}") if v else "0", font_size=14)
        p0 = path(ax, xs, pdf(xs, s0), GREY_B, 3.0)
        p1 = path(ax, xs, pdf(xs, s1), TEST, 3.0)
        z = vline(ax, 0, 0, top, GREY_C, 1.2)
        side = VGroup(
            MathTex(r"\hat\tau_{\text{CUPED}} = \hat\tau - \theta\,(\bar X_B - \bar X_A),\quad "
                    r"\theta = \frac{\mathrm{Cov}(X, Y)}{\mathrm{Var}(X)}", font_size=26, color=WHITE),
            label(r"$X$: \ the same user's spending before the test", font_size=19, color=GREY_A),
            label(r"grey: \ the plain difference in means", font_size=19, color=GREY_B),
            label(r"pink: \ adjusted for the pre-period", font_size=19, color=TEST),
            label(rf"variance cut to {C['ratio']:.2f} of the plain estimator's; \ theory: \ $1 - \rho^2$ = "
                  rf"{C['predicted']:.2f}", font_size=19, color=WHITE),
            label(r"the same precision with about half the users", font_size=21, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ 1,000 tests of 20,000 users, \ pre-period correlation 0.7; \ "
                         r"agora.platform.cuped".replace(",", "{,}"), corner=DL, font_size=12)
        with self.voiceover(
            "The second problem is noise, and the cheapest fix is information the platform already has. "
            "<bookmark mark='a'/> What a user spends during a test is predictable from what the same user spent "
            "before it. Subtract the part of the difference that the pre-period predicts, and the estimate keeps "
            "its centre but loses much of its noise. <bookmark mark='b'/> Microsoft's experimenters called this "
            "CUPED; it is the regression adjustment of Part four and of Statistics, Built, applied at scale. "
            "<bookmark mark='c'/> Across a thousand Island tests of twenty thousand users, the plain difference "
            "in means spreads like the grey curve; <bookmark mark='d'/> adjusted, like the pink one. <bookmark "
            f"mark='e'/> The variance falls to {C['ratio']:.2f} of the plain estimator's; theory says one minus "
            f"the squared correlation, {C['predicted']:.2f}. <bookmark mark='f'/> The same precision with about "
            "half the users: for a platform, that means twice as many experiments a year."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(z), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(p0), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(p1), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def habits(self):
        cards = point_cards([
            (r"check the split", r"if the arms are not the sizes the design promised, \ something broke: \ the "
             r"sample ratio check", TEST),
            (r"guardrails", r"every test also watches the metrics it must not hurt: \ speed, \ complaints, \ "
             r"cancellations", SURGE),
            (r"novelty and learning", r"a new design gets clicks because it is new; \ effects can fade, \ or "
             r"grow, \ over weeks", RIDER),
            (r"too good to be true", r"a big surprising win is more often a bug than a breakthrough: \ check it "
             r"before celebrating", GREY_A),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"the habits of an experimentation platform", font_size=30, color=E.ACCENT).to_edge(UP,
                                                                                                    buff=0.5)
        tag = published_tag(r"Kohavi, \ Tang and Xu, \ \emph{Trustworthy Online Controlled Experiments} (2020); \ "
                            r"Deng, \ Xu, \ Kohavi and Walker (2013)", corner=DL, font_size=12)
        with self.voiceover(
            "Experimentation platforms grow habits. <bookmark mark='a'/> Check the split: if the arms are not the "
            "sizes the design promised, something in the pipeline broke, and every number from the test is "
            "suspect. <bookmark mark='b'/> Watch the guardrails: every test also tracks what it must not hurt, "
            "like page speed, complaints and cancellations. <bookmark mark='c'/> Expect novelty: a new design "
            "draws clicks because it is new, and an effect measured in a week can fade, or grow, over months, "
            "which is chapter ten's problem. <bookmark mark='d'/> And distrust the spectacular: a large, "
            "surprising win is more often a bug than a breakthrough. Ron Kohavi, who led experimentation at "
            "Microsoft, made that a rule, under the name of Twyman's law."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
