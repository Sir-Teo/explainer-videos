from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403


class Numbers(VoiceoverScene):
    def construct(self):
        card(self, 1, r"How a number is made", r"How much does a first estimate of GDP change later?",
             "Chapter one. How a number is made.", lit={1934: r"Kuznets", 1990: r"Mankiw and Shapiro"},
             scale=("nation",), horizon=("a year", "a decade"))
        self.pipeline()
        self.scatter()
        self.vintages()

    def pipeline(self):
        gdp = flow_chain([(r"advance estimate, \ a month after the quarter", FIRST), (r"second and third", FIRST),
                          (r"annual revisions", LATEST), (r"comprehensive revisions", LATEST)], direction=RIGHT,
                         box_w=2.9, box_h=1.0, buff=0.45, font_size=19)
        jobs = flow_chain([(r"a survey of employers, \ a week after the month", FIRST),
                           (r"two monthly revisions", FIRST), (r"benchmark to tax records, \ once a year", LATEST)],
                          direction=RIGHT, box_w=3.4, box_h=1.0, buff=0.5, font_size=19)
        gl = label(r"GDP \ (BEA)", font_size=24, color=WHITE)
        jl = label(r"payrolls \ (BLS)", font_size=24, color=WHITE)
        VGroup(VGroup(gl, gdp).arrange(DOWN, buff=0.25), VGroup(jl, jobs).arrange(DOWN, buff=0.25)).arrange(
            DOWN, buff=0.7).move_to(UP * 0.4)
        bench = VGroup(
            label(r"benchmark revisions to payrolls, \ year to March:", font_size=20, color=GREY_A),
            label(r"2024: \ $-818{,}000$ first announced, \ $-598{,}000$ final", font_size=20, color=LATEST),
            label(r"2025: \ $-911{,}000$ first announced \qquad 2026: \ $-79{,}000$", font_size=20, color=LATEST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"BLS, \ preliminary benchmark releases of August 2024, \ September 2025 and August "
                            r"2026", corner=DR, font_size=11)
        with self.voiceover(
            "A statistic is not observed; it is made, and remade. <bookmark mark='a'/> America's first estimate of "
            "a quarter's GDP comes about a month after the quarter ends, built partly from complete data and "
            "partly from assumptions where the data are not in yet. A second and a third estimate follow, then "
            "annual revisions as tax and census data arrive, then comprehensive revisions that can rewrite "
            "decades. <bookmark mark='b'/> Payrolls come from a survey of more than a hundred thousand employers, "
            "a week after the month ends, with a model of businesses born and dying that the survey cannot yet "
            "see. Each month's number is revised twice, and once a year the whole series is benchmarked to the "
            "unemployment-insurance tax records. <bookmark mark='c'/> Those benchmarks can be large. In August "
            "2024 the Bureau of Labor Statistics announced that the year to March had about 818 thousand fewer "
            "jobs than reported, later settled at 598 thousand; in 2025 the first announcement was 911 thousand; "
            "in 2026, 79 thousand."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(gl), LaggedStart(*[FadeIn(b_) for b_ in gdp.boxes], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a_) for a_ in gdp.arrows], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(jl), LaggedStart(*[FadeIn(b_) for b_ in jobs.boxes], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a_) for a_ in jobs.arrows], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bench], lag_ratio=0.4), run_time=2.0)
        self.clear_scene()

    def scatter(self):
        R = load("revisions")
        f, l_ = np.array(R["first"]), np.array(R["latest"])
        ax = plane([-12, 18], [-12, 18], center=LEFT * 2.0 + DOWN * 0.3, x_length=5.6, y_length=5.6,
                   xticks=[-10, -5, 0, 5, 10, 15], yticks=[-10, -5, 0, 5, 10, 15],
                   xlabel=r"first estimate, \ \% a year", ylabel=r"latest estimate", xfmt=lambda x: f"{x:+.0f}".replace(
                       "-", "{-}") if x else "0", yfmt=lambda y: f"{y:+.0f}".replace("-", "{-}") if y else "0",
                   font_size=13)
        diag = seg(ax, -12, -12, 18, 18, GREY_C, 1.6, dashed=True)
        keep = (np.abs(f) < 12) & (np.abs(l_) < 18) & (f < 18)
        flips = (np.sign(f) != np.sign(l_))
        dots = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.04, color=ERR if fl else FIRST, fill_opacity=0.8)
                        for a, b, fl, k in zip(f, l_, flips, keep) if k])
        bq = R["biggest"]
        side = VGroup(
            label(rf"{R['n']} quarters, \ {R['quarters'][0][:4]}--{R['quarters'][-1][:4]}", font_size=19,
                  color=WHITE),
            label(rf"average revision: \ ${R['mean_rev']:+.2f}$ points", font_size=19, color=FIRST),
            label(rf"average size: \ {R['mae']:.2f} points", font_size=19, color=FIRST),
            label(rf"red: \ {R['sign_flips']} quarters \\ that changed sign", font_size=19, color=ERR),
            label(rf"largest: \ {bq['quarter'].replace(':', ' ')}, \\ {bq['first']:.1f} then {bq['latest']:.1f}",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Philadelphia Fed, \ Real-Time Data Set for Macroeconomists", corner=DR, font_size=12)
        with self.voiceover(
            "How much do the numbers move? <bookmark mark='a'/> Here is every quarter since the mid-1960s: its "
            "annualized growth as first published, against what today's data say. If nothing were ever revised, "
            "every dot would sit on the dashed line. <bookmark mark='b'/> They cluster around it, with a "
            f"correlation of {R['corr']:.2f}, <bookmark mark='c'/> but the average revision is "
            f"{R['mae']:.2f} points either way, and on average growth has been revised up by "
            f"{R['mean_rev']:.2f}. <bookmark mark='d'/> In {R['sign_flips']} quarters, in red, the first estimate "
            "had the wrong sign: growth became a fall, or a fall growth. Gregory Mankiw and Matthew Shapiro asked "
            "in 1986 whether such revisions are news or noise; for American GDP they found mostly news, which "
            "means the first number is the best guess at the time, but a guess."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(diag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.005), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def vintages(self):
        R = load("revisions")
        p = R["path_2008q4"]
        x = np.array([int(v["vintage"][:4]) + (int(v["vintage"][-1]) - 1) / 4 for v in p])
        y = np.array([v["growth"] for v in p])
        ax = plane([2008.8, 2027], [-10, -2], center=LEFT * 1.0 + DOWN * 0.3, x_length=9.6, y_length=5.0,
                   xticks=[2010, 2014, 2018, 2022, 2026], yticks=[-10, -8, -6, -4, -2], xlabel=r"vintage",
                   ylabel=r"growth in 2008Q4, \ \% a year, \ as each vintage had it", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        line = path(ax, x, y, FIRST, 3.0, smooth=False)
        d0 = dot(ax, x[0], y[0], FIRST, 0.09)
        d1 = dot(ax, x[-1], y[-1], LATEST, 0.09)
        l0 = label(rf"January 2009: \ ${y[0]:.1f}$", font_size=20, color=FIRST).next_to(d0, UP, buff=0.15).shift(
            RIGHT * 1.2)
        l1 = label(rf"today: \ ${y[-1]:.1f}$", font_size=20, color=LATEST).next_to(d1, DOWN, buff=0.2)
        tag = data_tag(r"Philadelphia Fed, \ Real-Time Data Set: \ every vintage since 2009", corner=DR,
                       font_size=12)
        with self.voiceover(
            "The quarter that mattered most shows why. <bookmark mark='a'/> The first estimate of the last quarter "
            f"of 2008, published in January 2009 while Congress debated a stimulus, was {say_num(y[0], 1)} percent "
            "a year: bad, but not catastrophic. <bookmark mark='b'/> Vintage by vintage it got worse. <bookmark "
            f"mark='c'/> Today it is {say_num(y[-1], 1)}: more than twice as bad. Policy was made with the first "
            "number."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(d0), FadeIn(l0))
            vo.wait_until("b")
            self.play(Create(line), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(d1), FadeIn(l1))
        self.clear_scene()
