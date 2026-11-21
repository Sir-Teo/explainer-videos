from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403

MONTHS = ("J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D")


class Seasonal(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Seasonal adjustment", r"What does seasonal adjustment remove, \ and what can it invent?",
             "Chapter two. Seasonal adjustment.", lit={1965: r"Shiskin's X-11", 2020: r"the pandemic"},
             scale=("nation",), horizon=("a year",))
        self.raw()
        self.method()
        self.invent()

    def raw(self):
        S = load("seasonal")
        m = S["months"]
        idx = [k for k, x in enumerate(m) if "2015-01" <= x <= "2019-12"]
        ch_n = [S["ch_nsa"][k - 1] / 1000 for k in idx]
        ch_o = [S["ch_official"][k - 1] / 1000 for k in idx]
        ax = plane([-0.5, len(idx) - 0.5], [-3.4, 1.6], center=LEFT * 1.4 + DOWN * 0.3, x_length=10.0, y_length=5.0,
                   xticks=[6, 18, 30, 42, 54], yticks=[-3, -2, -1, 0, 1], xlabel=r"", ylabel=r"change in payrolls "
                   r"from the month before, \ millions", xfmt=lambda v: str(2015 + int(v) // 12),
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        bars = VGroup()
        for k, v in enumerate(ch_n):
            p0, p1 = ax.ax.c2p(k - 0.35, 0), ax.ax.c2p(k + 0.35, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=GREY_B,
                               fill_opacity=0.6).move_to((p0 + p1) / 2))
        off = path(ax, np.arange(len(idx)), ch_o, FIRST, 3.0, smooth=False)
        side = VGroup(label(r"grey: \ not adjusted", font_size=19, color=GREY_B),
                      label(r"orange: \ adjusted \ (BLS)", font_size=19, color=FIRST)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 1.5)
        tag = data_tag(r"BLS via FRED: \ PAYNSA, \ PAYEMS", corner=DR, font_size=12)
        with self.voiceover(
            "Every January, America loses millions of jobs. <bookmark mark='a'/> These are monthly changes in "
            "payrolls before adjustment, 2015 to 2019: every January a fall of two to three million, as Christmas "
            "jobs end, then a rise through the spring, a dip in July, a rise in the autumn. <bookmark mark='b'/> "
            f"The swings have a standard deviation of {S['sd_nsa_change'] / 1000:.1f} million a month. The "
            "adjusted series, in orange, which the news reports, removes the pattern that repeats every year and "
            f"moves by about {S['sd_off_change']:.0f} thousand. Nearly everything a viewer hears about jobs has "
            "been through this filter."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, UP if v < 0 else DOWN) for b_, v in zip(bars, ch_n)],
                                  lag_ratio=0.03), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(off), FadeIn(side[1]), run_time=1.5)
        self.clear_scene()

    def method(self):
        S = load("seasonal")
        chain = flow_chain([(r"$\log$ of the level", GREY_B), (r"trend: \ centred 12-month average", LATEST),
                            (r"level minus trend: \ season plus noise", FIRST),
                            (r"average each calendar month over neighbouring years", SPF),
                            (r"subtract: \ the adjusted series", NOW)], direction=RIGHT, box_w=2.3, box_h=1.2,
                           buff=0.35, font_size=17)
        chain.to_edge(UP, buff=0.9)
        eff = np.array(S["month_effect"])
        ax = plane([-0.6, 11.6], [-1.8, 1.4], center=DOWN * 1.9 + LEFT * 0.8, x_length=8.0, y_length=2.6,
                   xticks=list(range(12)), yticks=[-1, 0, 1], xlabel=r"", ylabel=r"seasonal factor, \ \%",
                   xfmt=lambda v: MONTHS[int(v)], yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0",
                   font_size=13)
        bars = VGroup()
        for k, v in enumerate(eff):
            p0, p1 = ax.ax.c2p(k - 0.32, 0), ax.ax.c2p(k + 0.32, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), stroke_width=0,
                               fill_color=SPF if v >= 0 else FIRST, fill_opacity=0.8).move_to((p0 + p1) / 2))
        fit = label(rf"this simplified X-11 against the BLS, \\ 1948--2019: \ monthly changes differ by "
                    rf"{S['rms_robust_pre']:.0f} thousand \\ (root mean square)", font_size=17,
                    color=GREY_A).next_to(ax, RIGHT, buff=0.3)
        with self.voiceover(
            "How is it done? Julius Shiskin's X-11 method, developed at the Census Bureau in the 1960s, still sits "
            "inside the programmes statistical agencies use. <bookmark mark='a'/> Take logs. <bookmark mark='b'/> "
            "Estimate the trend with a centred twelve-month average, which cancels any pattern that repeats every "
            "year. <bookmark mark='c'/> What is left is the season plus noise. <bookmark mark='d'/> Average each "
            "calendar month's value over neighbouring years, so Januaries are compared with Januaries. <bookmark "
            "mark='e'/> Subtract that seasonal factor. <bookmark mark='f'/> Run on unadjusted payrolls, this "
            f"simplified version finds January's factor {abs(eff[0]):.1f} percent below the year's average, and "
            f"December's {eff[11]:.1f} percent above; its monthly changes differ from the official ones by "
            f"{S['rms_robust_pre']:.0f} thousand, on average, before 2020."
        ) as vo:
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                anims = [FadeIn(chain.boxes[k], shift=UP * 0.1)]
                if k:
                    anims.append(GrowArrow(chain.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("f")
            self.play(FadeIn(ax), LaggedStart(*[GrowFromEdge(b_, DOWN if v >= 0 else UP) for b_, v in zip(bars, eff)],
                                              lag_ratio=0.1), FadeIn(fit), run_time=2.0)
        self.clear_scene()

    def invent(self):
        S = load("seasonal")
        yrs = np.array([int(y) for y in S["apr_years"]])
        raw, rob = np.array(S["apr_raw"]), np.array(S["apr_robust"])
        sel = yrs >= 2012
        ax = plane([2011.5, 2026.5], [-4, 1], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[2012, 2016, 2020, 2024], yticks=[-3, -2, -1, 0], xlabel=r"",
                   ylabel=r"April's seasonal factor, \ \%", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        l_raw = path(ax, yrs[sel], raw[sel], ERR, 3.0, smooth=False)
        l_rob = path(ax, yrs[sel], rob[sel], LATEST, 3.0, smooth=False)
        d_raw = VGroup(*[dot(ax, a, b, ERR, 0.05) for a, b in zip(yrs[sel], raw[sel])])
        m = S["months"]
        i21 = m.index("2021-04")
        extra = (S["adj_raw"][i21] - S["adj_robust"][i21]) / 1000
        drop = -S["ch_official"][m.index("2020-04") - 1] / 1000
        side = VGroup(
            label(r"red: \ the filter as described", font_size=19, color=ERR),
            label(r"green: \ with extreme values left out", font_size=19, color=LATEST),
            label(rf"April 2021, \ adjusted: \\ {extra:.1f} million jobs apart", font_size=19, color=E.ACCENT),
            label(rf"after 2020, \ against the BLS: \\ {S['rms_raw_post']:.0f} thousand off, \ or "
                  rf"{S['rms_robust_post']:.0f}", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            f"What can it invent? <bookmark mark='a'/> In April 2020 payrolls fell by {drop:.1f} million. The "
            "filter "
            "as described averages each April with its neighbours, so that one collapse leaks into the seasonal "
            f"factor for April in every year around it: by 2020 it is {say_num(raw[yrs == 2020][0], 1)} percent, "
            "an April slump that never recurs. <bookmark mark='b'/> X-11 guards against this by leaving extreme "
            "values out of the seasonal averages; done here, April's factor barely moves. <bookmark mark='c'/> The "
            f"difference is not small: in April 2021 the two adjustments differ by {extra:.1f} million jobs. "
            "<bookmark mark='d'/> After 2020 the version without the outlier step misses the official monthly "
            f"changes by {S['rms_raw_post']:.0f} thousand on average; with it, by {S['rms_robust_post']:.0f}. The "
            "statistical agencies spent 2020 and 2021 deciding, month by month, which movements were seasons and "
            "which were history."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(l_raw), FadeIn(d_raw), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(l_rob), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
