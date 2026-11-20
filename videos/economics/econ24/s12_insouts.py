from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403


class InsOuts(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Ins against outs", r"In a recession, \ do more people lose jobs, \ or do fewer find them?",
             "Chapter ten. Ins against outs.", lit={2009: r"Elsby, Michaels and Solon", 2012: r"Shimer"},
             scale=("market",), horizon=("a month", "decades"))
        self.measure()
        self.rates()
        self.decompose()

    def measure(self):
        rows = VGroup(
            label(r"the survey counts the unemployed, \ and how many have been looking for less than five weeks",
                  font_size=23, color=GREY_A),
            MathTex(r"u_{t+1} \;=\; (1 - F_t)\,u_t \;+\; u^{<5\,\text{wk}}_{t+1} \quad\Longrightarrow\quad F_t = 1 - "
                    r"\frac{u_{t+1} - u^{<5\,\text{wk}}_{t+1}}{u_t}", font_size=38, color=WORKER),
            label(r"those still unemployed next month are last month's, \ less those who found work, \ plus the "
                  r"newly unemployed", font_size=21, color=GREY_B),
            MathTex(r"f_t = -\ln(1 - F_t) \qquad \text{and } s_t \text{ from the stock's change, with flows within "
                    r"the month}", font_size=34, color=SEP),
            label(r"Shimer's method, \ 2005 and 2012; \ the 1994 survey redesign needs a correction \ (here, \ 1.1 on "
                  r"the short-term count)", font_size=20, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Shimer, RED 15(2) (2012): \ 127--148", corner=DR, font_size=12)
        with self.voiceover(
            "Chapter one's tub has two pipes. When unemployment rises, which one changed? To answer, you need the "
            "flows, and before JOLTS there were none. Robert Shimer found them in a number the Current Population "
            "Survey has published since 1948: <bookmark mark='a'/> how many of the unemployed have been looking for "
            "less than five weeks. <bookmark mark='b'/> Next month's unemployed are this month's, less those who "
            "found work, plus those who just became unemployed. So the share who found work, F, can be read off. "
            "<bookmark mark='c'/> Convert it to a rate, f, allowing for people who find and lose jobs within the "
            "same month, and back out the separation rate from the change in the stock. "
            "<bookmark mark='d'/> One wrinkle: the survey was redesigned in 1994 and now counts fewer people as "
            "newly unemployed; Agora scales the short-term count by 1.1 from then on, a correction in the spirit of "
            "Shimer's."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def rates(self):
        f = load("flows")
        a1 = plane([1948, 2026], [0, 1.0], center=UP * 1.4 + LEFT * 1.5, x_length=9.0, y_length=2.4,
                   xticks=[1950, 1970, 1990, 2010], yticks=[0, 0.5, 1.0], ylabel=r"job finding $f$, \ a month",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        a2 = plane([1948, 2026], [0, 0.06], center=DOWN * 1.9 + LEFT * 1.5, x_length=9.0, y_length=2.4,
                   xticks=[1950, 1970, 1990, 2010], yticks=[0, 0.03, 0.06], ylabel=r"separation $s$, \ a month",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        fl = path(a1, f["t"], f["f"], color=MATCH, width=3, smooth=False)
        sl = path(a2, f["t"], f["s"], color=SEP, width=3, smooth=False)
        side = VGroup(
            label(rf"job finding: \ average {100 * f['mean_f']:.0f}\% \\ a month; \ it collapses \\ in every "
                  r"recession", font_size=20, color=MATCH),
            label(rf"separation: \ average {100 * f['mean_s']:.1f}\%; \\ it jumps at the start \\ of recessions, "
                  r"\ briefly", font_size=20, color=SEP),
            label(r"2020: \ a month of \\ separations like no other", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BLS, \ CPS: \ unemployed, \ unemployed under 5 weeks, \ labour force, \ via FRED; \ "
                       r"quarterly averages", corner=DR, font_size=12)
        with self.voiceover(
            "Here are the two rates, quarter by quarter, since 1948. <bookmark mark='a'/> Job finding averages "
            f"about {100 * f['mean_f']:.0f} percent a month, and it collapses in every recession: in 2010 it "
            "fell below a quarter. <bookmark mark='b'/> Separation averages about "
            f"{100 * f['mean_s']:.1f} percent a month. It jumps at the start of recessions, but briefly, and "
            "with much smaller swings in proportion. <bookmark mark='c'/> The spring of 2020 is the exception: "
            "more than twenty million payroll jobs lost in April alone, most of them temporary layoffs: a burst of "
            "separations unlike anything before."
        ) as vo:
            self.play(FadeIn(a1), FadeIn(a2), FadeIn(tag), Create(fl), Create(sl), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def decompose(self):
        f = load("flows")
        ax = plane([1948, 2026], [0, 0.2], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.6, y_length=5.0,
                   xticks=[1950, 1970, 1990, 2010], yticks=[0, 0.05, 0.10, 0.15, 0.20],
                   ylabel=r"steady-state unemployment $s/(s+f)$", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        actual = path(ax, f["t"], f["steady"], color=WHITE, width=3, smooth=False, yr=(0, 0.2))
        only_f = path(ax, f["t"], f["only_f"], color=MATCH, width=3, smooth=False, yr=(0, 0.2))
        only_s = path(ax, f["t"], f["only_s"], color=SEP, width=3, smooth=False, yr=(0, 0.2))
        side = VGroup(
            label(r"from both rates", font_size=21, color=WHITE),
            label(r"only job finding moves \\ (separation at its average)", font_size=20, color=MATCH),
            label(r"only separation moves", font_size=20, color=SEP),
            label(rf"job finding: \ {100 * f['share_f']:.0f}\% \ of the variance; \\ separation: \ "
                  rf"{100 * f['share_s']:.0f}\%", font_size=23, color=E.ACCENT),
            label(rf"since 1987: \ {100 * f['share_f_87']:.0f}\% \ and {100 * f['share_s_87']:.0f}\%", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Shimer, RED 15(2) (2012); \ Elsby, Michaels and Solon, AEJ: Macro 1(1) (2009): "
                            r"84--110", corner=DR, font_size=12)
        with self.voiceover(
            "Now split unemployment's swings between the two. <bookmark mark='a'/> In white, the steady-state rate "
            "the two flows imply each quarter, which tracks actual unemployment closely. <bookmark mark='b'/> In "
            "green, what it would have been if only job finding had moved, with separation held at its average. "
            "<bookmark mark='c'/> In red, if only separation had moved. <bookmark mark='d'/> Green follows white "
            f"far more closely. Measured by the covariances, job finding accounts for about "
            f"{100 * f['share_f']:.0f} percent of the variation in unemployment since 1948, and separation for about "
            f"{100 * f['share_s']:.0f}. Shimer found three-quarters and one quarter. <bookmark mark='e'/> Michael "
            "Elsby, Ryan Michaels and Gary Solon answered that the inflow still matters, especially at the start of "
            "recessions, when layoffs surge before hiring dries up. Both are right about something: recessions "
            "begin with job losses and last because hiring stops. That is why the DMP model's focus on job "
            "creation is a good place to start, and why its weak amplification is a real problem."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(actual), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(only_f), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(only_s), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()
