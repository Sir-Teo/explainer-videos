from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Realtime(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Rules with the data of the day", r"What would a rule have said, \ with only what was known "
             r"then?", "Chapter seven. Rules with the data of the day.",
             lit={2001: r"Orphanides"}, scale=("nation",), horizon=("a quarter", "decades"))
        self.gaps()
        self.rules()

    def gaps(self):
        R = load("realtime")
        rows = R["rows"]
        yr = np.array([r["year"] for r in rows]) - 1 + 0.75
        ax = plane([1965, 2008], [-12, 6], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[1970, 1980, 1990, 2000], yticks=[-12, -8, -4, 0, 4], xlabel=r"",
                   ylabel=r"output gap at the end of each year, \ \%", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        zero = seg(ax, 1965, 0, 2008, 0, GREY_C, 1.5)
        rt = path(ax, yr, [r["gap_rt"] for r in rows], OUTPUT, 3.2, smooth=False)
        td = path(ax, yr, [r["gap_today"] for r in rows], CB, 3.2, smooth=False)
        dots_rt = VGroup(*[dot(ax, x, r["gap_rt"], OUTPUT, 0.045) for x, r in zip(yr, rows)])
        side = VGroup(
            label(r"green: \ the gap from the data of the day \\ (a trend fitted to each year's release)",
                  font_size=17, color=OUTPUT),
            label(r"teal: \ today's estimate \\ (the CBO's potential, \ today's data)", font_size=17, color=CB),
            label(rf"the 1970s: \ the green line {abs(R['mean_error_70s']):.1f} points \\ lower, \ on average",
                  font_size=17, color=E.ACCENT),
            label(r"the old trend kept promising \\ growth that had stopped", font_size=18, color=HOLD),
            label(r"and again in the 2000s", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Philadelphia Fed, \ Real-Time Data Set (first-quarter vintages, \ 1966--2008); \ CBO's "
                       r"potential via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Your Play it was one year. Here are all of them. <bookmark mark='a'/> In green, the output gap at the "
            "end of each year as it looked the following winter: a trend fitted to everything that winter's figures "
            "contained, and output's distance from it. <bookmark mark='b'/> In teal, today's estimate of the same "
            "gap, from the Congressional Budget Office's potential output and today's revised figures. "
            "<bookmark mark='c'/> Through the 1970s, the data of the day put output on average "
            f"{abs(R['mean_error_70s']):.1f} points further below potential than we now think it was. "
            "<bookmark mark='d'/> The trend extended the fast growth of the fifties and sixties, after productivity "
            "growth had slowed. <bookmark mark='e'/> And a mechanical trend makes the same mistake after the "
            "slowdown of the 2000s. Real forecasters did better than this simple line, but the point stands: the "
            "gap a rule needs cannot be seen, only estimated, and the estimates were worst exactly when they "
            "mattered most."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(rt), FadeIn(dots_rt), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(td), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def rules(self):
        R = load("realtime")
        rows = [r for r in R["rows"] if r["year"] <= 1990]
        yr = np.array([r["year"] for r in rows]) + 0.1
        ax = plane([1965, 1991], [0, 22], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[1965, 1970, 1975, 1980, 1985, 1990], yticks=[0, 5, 10, 15, 20],
                   ylabel=r"percent, \ each year's first quarter", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        ff = path(ax, yr, [r["ff"] for r in rows], RATE, 3.5, smooth=False)
        rrt = path(ax, yr, [r["rule_rt"] for r in rows], OUTPUT, 2.8, smooth=False)
        rtd = DashedVMobject(path(ax, yr, [r["rule_today"] for r in rows], CB, 2.8, smooth=False), num_dashes=60)
        side = VGroup(
            label(r"pink: \ the federal funds rate", font_size=18, color=RATE),
            label(r"green: \ Taylor's rule, \ data of the day", font_size=18, color=OUTPUT),
            label(r"teal, \ dashed: \ the rule, \ today's gap", font_size=18, color=CB),
            label(rf"the 1970s: \ the actual rate \\ {abs(R['ff_minus_rule_rt_70s']):.1f} points below the rule \\ "
                  rf"of the day; \ {abs(R['ff_minus_rule_today_70s']):.1f} below today's", font_size=18,
                  color=E.ACCENT),
            label(r"respond to inflation; \\ be humble about the gap", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Orphanides, \ \emph{AER} 91(4) (2001), \ \emph{JMCB} 36(2) (2004); \ Taylor, \ "
                            r"Carnegie-Rochester 39 (1993); \ "
                            r"this film", corner=DR, font_size=12)
        with self.voiceover(
            "What would Taylor's rule have said? <bookmark mark='a'/> The federal funds rate, in pink. "
            "<bookmark mark='b'/> The rule with the gap of the day, in green, <bookmark mark='c'/> and with today's "
            "gap, dashed. <bookmark mark='d'/> In the 1970s the actual rate was on average "
            f"{abs(R['ff_minus_rule_rt_70s']):.1f} points below what the rule would have said with the data of the "
            f"day, and {abs(R['ff_minus_rule_today_70s']):.1f} points below what it says with today's. "
            "<bookmark mark='e'/> On this simple measure, misreading the gap explains about a point of the "
            "shortfall. Orphanides went further, with the forecasts and gap estimates the committee actually had in "
            "front of it. He found that before 1979, as after, the Federal Reserve responded strongly to its "
            "forecasts of inflation; the difference was that it also responded strongly to gaps that later proved "
            "far too optimistic. The lessons: respond firmly to inflation, and be humble about the gap."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(ff), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(rrt), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(rtd), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
