from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class Sensitivity(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Too sensitive, \ and too smooth", r"How much of income goes to households who simply spend "
             r"it, \ and why is spending smoother than the theory says?", "Chapter five. Too sensitive, and too "
             "smooth.", lit={1981: r"Flavin", 1989: r"Campbell and Mankiw", 1992: r"Deaton"},
             scale=("household", "nation"), horizon=("a quarter", "a year"))
        self.rule()
        self.island()
        self.us()
        self.smooth()
        self.fact()

    def rule(self):
        rows = VGroup(
            label(r"Marjorie Flavin, \ 1981: \ consumption responds to income changes that were predictable", font_size=23,
                  color=GREY_A),
            label(r"excess sensitivity", font_size=30, color=HOLD),
            label(r"John Campbell and Gregory Mankiw, \ 1989: \ two kinds of household", font_size=23, color=GREY_A),
            MathTex(r"\Delta c_t \;=\; \lambda\,\Delta y_t \;+\; (1-\lambda)\,\varepsilon_t", font_size=46,
                    color=SPEND),
            label(r"a share $\lambda$ of income goes to rule-of-thumb households who spend what they get; \ the rest "
                  r"to Hall's", font_size=22, color=GREY_A),
            label(r"OLS is biased: \ news $\varepsilon_t$ moves income too; \ instrument $\Delta y_t$ with what was "
                  r"known two quarters before", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Flavin, JPE 89(5) (1981); \ Campbell and Mankiw, NBER Macroeconomics Annual 4 (1989)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Hall's test failed in the direction Marjorie Flavin had already found in 1981: consumption responds to "
            "changes in income that could have been predicted. <bookmark mark='a'/> Economists call it excess "
            "sensitivity. <bookmark mark='b'/> In 1989 John Campbell and Gregory Mankiw gave it a size. Suppose "
            "there are two kinds of household. <bookmark mark='c'/> A share lambda of income goes to households who "
            "follow a rule of thumb: they spend what they get, when they get it. <bookmark mark='d'/> The rest goes "
            "to Hall's households, whose consumption moves only with news. <bookmark mark='e'/> You cannot estimate "
            "lambda by regressing consumption growth on income growth, because the news that moves Hall's "
            "households also moves income. Use instead the part of income growth that was predictable two quarters "
            "earlier: an instrument, in the sense of Part four."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def island(self):
        r = load("rot")
        bins = np.linspace(-0.2, 1.0, 49)
        ax = plane([-0.2, 1.0], [0, 140], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.4, y_length=4.8,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[0, 40, 80, 120],
                   xlabel=r"estimated $\lambda$ \ (200 island economies, \ 240 quarters each)",
                   ylabel=r"economies", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=15)

        def hist(vals, col):
            h, e = np.histogram(np.clip(vals, -0.2, 0.999), bins=bins)
            g = VGroup()
            for k, v in enumerate(h):
                if v == 0:
                    continue
                x0, x1 = e[k], e[k + 1]
                w = ax.ax.c2p(x1, 0)[0] - ax.ax.c2p(x0, 0)[0]
                hh_ = ax.ax.c2p(0, v)[1] - ax.ax.c2p(0, 0)[1]
                g.add(Rectangle(width=w, height=hh_, stroke_width=0, fill_color=col, fill_opacity=0.7).move_to(
                    [(ax.ax.c2p(x0, 0)[0] + ax.ax.c2p(x1, 0)[0]) / 2, ax.ax.c2p(0, 0)[1], 0], aligned_edge=DOWN))
            return g
        h_ols = hist(r["ols_reps"], GREY_B)
        h_iv = hist(r["iv_reps"], SPEND)
        truth = seg(ax, r["lam"], 0, r["lam"], 140, color=TRUTH_C, width=3, dashed=True)
        side = VGroup(
            label(rf"planted: \ $\lambda = {r['lam']}$", font_size=22, color=TRUTH_C),
            label(rf"OLS: \ average {r['ols_mean']:.2f}", font_size=22, color=GREY_B),
            label(rf"IV: \ median {r['iv_median']:.2f}", font_size=22, color=SPEND),
            label(r"centred on the truth, \\ but wide: \ a short sample \\ and a modest first stage \\ (a few far "
                  r"below zero, \\ piled at the left edge)", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "First on the Island, where we know the answer. <bookmark mark='a'/> We plant lambda at "
            f"{r['lam']}: four tenths of income goes to households who spend what they get. Then we run two hundred "
            "island economies for sixty years of quarters each. <bookmark mark='b'/> Ordinary least squares, "
            f"economy by economy, averages {r['ols_mean']:.2f}. The news contaminates it. "
            "<bookmark mark='c'/> Instrumenting with income growth two quarters earlier, the estimates centre on the "
            f"truth, a median of {r['iv_median']:.2f}. <bookmark mark='d'/> But they are wide. Sixty years of "
            "quarters is not much data, and the instrument predicts income growth only modestly."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in h_ols], lag_ratio=0.03), FadeIn(side[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in h_iv], lag_ratio=0.03), FadeIn(side[2]),
                      run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def us(self):
        h = load("hall")
        rows = VGroup(
            label(r"the same estimate on American data, \ 1960--2019", font_size=27, color=E.ACCENT),
            label(rf"OLS: \ {h['ols']:.2f}", font_size=25, color=GREY_B),
            label(rf"IV, \ instruments at lags two to four: \ $\hat\lambda = {h['iv']:.2f}$ \ (s.e. {h['iv_se']:.2f})",
                  font_size=25, color=SPEND),
            label(rf"but the first-stage $F$ is only {h['first_F']:.1f}: \ weak instruments, \ so read it loosely",
                  font_size=23, color=HOLD),
            label(r"Campbell and Mankiw's own estimates, \ on data to 1985: \ about one half", font_size=23,
                  color=GREY_A),
            label(r"a large share of income, \ not a rounding error, \ goes to households who spend it", font_size=24,
                  color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = data_tag(r"BEA via FRED; \ Campbell and Mankiw (1989)", corner=DR, font_size=12)
        with self.voiceover(
            "Now on the real thing. <bookmark mark='a'/> On American quarters from 1960 to 2019, least squares gives "
            f"{h['ols']:.2f}. <bookmark mark='b'/> Instrumenting with income and consumption growth two to four "
            f"quarters earlier gives {h['iv']:.2f}, with a standard error of {h['iv_se']:.2f}. "
            "<bookmark mark='c'/> But the first stage is weak, an F of "
            f"{h['first_F']:.1f}, far below the rule of thumb of ten, and Part four showed what weak instruments do: "
            "they pull the estimate toward least squares and make its standard error too small. Read the number "
            "loosely. <bookmark mark='d'/> Campbell and Mankiw's own estimates, on data to the mid-1980s, were about "
            "one half. <bookmark mark='e'/> Whatever the exact number, a large share of income, not a rounding "
            "error, goes to households who spend it when it comes."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def smooth(self):
        s = load("smooth")
        vals = [(r"income growth", s["sd_dy_a"], INCOME), (r"consumption, \\ permanent income's \\ prediction",
                                                            s["pih_sd"], SPEND),
                (r"consumption, \\ actual", s["sd_dc_a"], SAVE)]
        ax = plane([0.4, 3.6], [0, 2.4], center=LEFT * 2.4 + DOWN * 0.45, x_length=6.4, y_length=4.6,
                   xticks=[], yticks=[0, 0.5, 1.0, 1.5, 2.0], ylabel=r"standard deviation of annual growth, \ \%",
                   yfmt=lambda v: f"{v:g}", font_size=16)
        bars = VGroup()
        for k, (name, v, col) in enumerate(vals):
            x = k + 1
            bar = Rectangle(width=ax.ax.c2p(x + 0.3, 0)[0] - ax.ax.c2p(x - 0.3, 0)[0],
                            height=ax.ax.c2p(0, 100 * v)[1] - ax.ax.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                            fill_opacity=0.85).move_to(ax.ax.c2p(x, 50 * v))
            nm = label(name, font_size=16, color=col).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.15)
            val = label(f"{100 * v:.2f}", font_size=19, color=col).next_to(bar, UP, buff=0.08)
            bars.add(VGroup(bar, nm, val))
        side = VGroup(
            label(r"Angus Deaton's paradox", font_size=24, color=E.ACCENT),
            label(rf"income growth is persistent: \\ a good year predicts another \\ (autocorrelation "
                  rf"{s['phi']:.2f})", font_size=19, color=GREY_A),
            label(r"so a surprise raises permanent \\ income by more than this \\ year's income", font_size=19,
                  color=GREY_A),
            label(r"consumption should be \\ more volatile than income; \\ it is less", font_size=20, color=HOLD),
            label(r"excess smoothness and \\ excess sensitivity: \ one \\ failure seen two ways", font_size=19,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BEA via FRED, \ annual averages, \ 1960--2019; \ Deaton, \emph{Understanding Consumption} "
                       r"(1992)", corner=DR, font_size=12)
        with self.voiceover(
            "Then the opposite failure. <bookmark mark='a'/> In American data, income growth is persistent: a good "
            f"year tends to be followed by another, an autocorrelation of about {s['phi']:.2f} in annual growth. "
            "<bookmark mark='b'/> If so, a surprise in income raises permanent income by more than it raises this "
            "year's income, and a permanent-income household should change its consumption by more than its income "
            "changed. <bookmark mark='c'/> Income growth has a standard deviation of "
            f"{100 * s['sd_dy_a']:.1f} percent a year. The theory predicts consumption growth with a standard "
            f"deviation of {100 * s['pih_sd']:.1f}. Actual spending on nondurables and services: "
            f"{100 * s['sd_dc_a']:.1f}. Consumption is too smooth. <bookmark mark='d'/> Angus Deaton called it a "
            "paradox in 1987. John Campbell and Deaton then showed that excess smoothness and excess sensitivity are "
            "the same failure seen two ways: consumption responds too little to news when it arrives and catches up "
            "later, when the news has become predictable."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]))
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1:]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def fact(self):
        s = load("smooth")
        m = load("mpc")
        f = next(x for x in facts.FACTS if x.key == "smooth_consumption")
        data_m = label(rf"quarterly growth, \ 1960--2019: \\ spending {100 * s['sd_dc_q']:.2f}\%, \\ income "
                       rf"{100 * s['sd_dy_q']:.2f}\%: \ half as volatile", font_size=19, color=WHITE)
        theory_m = label(r"permanent income: \\ spend the annuity value \\ of a windfall, \ a few \\ cents a year",
                         font_size=19, color=INCOME)
        agora_m = label(rf"buffer-stock households: \\ {100 * m['mean_mpc']:.0f}\% of a month's \\ windfall within "
                        r"the year \\ (chapter 6)", font_size=19, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, INCOME, None)).move_to(UP * 0.1)
        with self.voiceover(
            "So consumption is smoother than income, though not as smooth as the theory first said. It goes on the "
            "series' list of facts. <bookmark mark='a'/> Quarter by quarter from 1960 to 2019, American spending on "
            f"nondurables and services grew with a standard deviation of {100 * s['sd_dc_q']:.2f} percent, income "
            f"with {100 * s['sd_dy_q']:.2f}. <bookmark mark='b'/> Agora's column is filled by the households of the "
            "next chapter, who smooth, but not completely."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), FadeIn(fc.cols[0][:2]), FadeIn(fc.cols[1][:2]),
                      FadeIn(fc.cols[2][:2]))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]), FadeIn(fc.cols[1][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[2][2:]))
        self.clear_scene()
