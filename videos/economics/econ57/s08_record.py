from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403


class Record(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The record", r"Who forecasts best, \ and did anyone see the recessions coming?",
             "Chapter seven. The record.", lit={2000: r"Romer and Romer", 2018: r"An, \ Jalles and Loungani"},
             scale=("nation", "world"), horizon=("a year",))
        self.greenbook()
        self.recessions()

    def greenbook(self):
        G = load("greenbook")
        rows = G["rows"]
        h = np.array([r["h"] for r in rows])
        ax = plane([-0.3, 4.3], [0, 2.2], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=5.0,
                   xticks=[0, 1, 2, 3, 4], yticks=[0, 0.5, 1.0, 1.5, 2.0], xlabel=r"quarters ahead",
                   ylabel=r"inflation forecast error, \ points \ (root mean square)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        gb = path(ax, h, [r["rmse_gb"] for r in rows], GB, 3.2, smooth=False)
        sp = path(ax, h, [r["rmse_spf"] for r in rows], SPF, 3.2, smooth=False)
        stars = VGroup(*[label(r"$\ast$", font_size=30, color=GB).next_to(ax.ax.c2p(r["h"], r["rmse_gb"]), DOWN,
                                                                           buff=0.08)
                         for r in rows if r["dm_p"] < 0.05])
        side = VGroup(
            label(rf"gold: \ the Federal Reserve staff's \\ Greenbook, \ {G['first_year']}--{G['last_year']}",
                  font_size=18, color=GB),
            label(r"blue: \ the professional forecasters, \\ the same quarters", font_size=18, color=SPF),
            label(r"$\ast$: \ the staff better, \ Diebold--Mariano, \ 5\%", font_size=18, color=GB),
            label(r"the GDP deflator, \ today's data", font_size=16, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Philadelphia Fed: \ Greenbook data set; \ SPF; \ FRED GDPDEF", corner=DR, font_size=12)
        better = sum(r["rmse_gb"] < r["rmse_spf"] for r in rows)
        romers = history_card(2000, r"Christina and David Romer", r"the Federal Reserve staff's Greenbook against "
                              r"commercial forecasters: \ the staff's inflation forecasts are better", color=GB,
                              width=5.2, font_size=19).move_to(ax.get_center() + UP * 0.6)
        h_sig = min([r["h"] for r in rows if r["dm_p"] < 0.05], default=None)
        with self.voiceover(
            "Who forecasts best? In 2000 Christina and David Romer compared the Federal Reserve staff's "
            "forecasts, in the Greenbook prepared for each policy meeting and published five years later, with "
            "commercial forecasters', and found the staff's inflation forecasts better. <bookmark mark='a'/> Here "
            f"is that comparison redone for {G['first_year']} to {G['last_year']}: forecasts of GDP-price inflation "
            "made in the same quarter. <bookmark mark='b'/> The staff's errors are smaller at "
            f"{'every' if better == len(rows) else 'most'} horizon{'' if better == len(rows) else 's'}, <bookmark "
            + (f"mark='c'/> significantly so from {h_sig} quarters ahead. " if h_sig is not None else
               "mark='c'/> though no difference is significant on its own. ") +
            "The Romers' reading was that the "
            "Federal Reserve knows things the market does not, which is why markets watch what it does so closely."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[3]), FadeIn(romers, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(romers), run_time=0.5)
            self.play(Create(sp), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(gb), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(stars), FadeIn(side[2]))
        self.clear_scene()

    def recessions(self):
        A, R = load("anxious"), load("record")
        st = A["starts"]
        rows = VGroup()
        for s_ in st:
            rows.add(VGroup(label(s_["start"], font_size=20, color=WHITE),
                            label(rf"{s_['p_before']:.0f}\%", font_size=20, color=SPF),
                            label(rf"{s_['p_peak']:.0f}\%", font_size=20, color=ERR)))
        head = VGroup(label(r"recession began", font_size=18, color=GREY_A),
                      label(r"the quarter before", font_size=18, color=SPF),
                      label(r"highest, \ once in it", font_size=18, color=ERR))
        tab = VGroup(head, *rows)
        for r_ in tab:
            r_[0].move_to([-5.2, 0, 0], aligned_edge=LEFT)
            r_[1].move_to([-2.4, 0, 0])
            r_[2].move_to([-0.6, 0, 0])
        tab.arrange(DOWN, buff=0.22)
        for r_ in tab:
            r_[0].set_x(-5.2 + r_[0].width / 2)
            r_[1].set_x(-2.4)
            r_[2].set_x(-0.4)
        tab.move_to(LEFT * 2.8 + DOWN * 0.4)
        title = label(r"the professional forecasters' chance of a fall next quarter", font_size=24,
                      color=E.ACCENT).to_edge(UP, buff=0.5)
        recs = VGroup(
            history_card(2008, r"August: \ the professional forecasters", rf"2009's growth: \ "
                         rf"${R['g_forecast']:+.1f}\%$ forecast, \ ${R['g_actual']:+.1f}\%$ actual \ (Part 1)",
                         color=SPF, width=5.6, font_size=19),
            history_card(2021, r"June: \ the Federal Reserve", rf"2022's inflation: \ {R['pi_forecast']:.1f}\% "
                         rf"projected, \ {R['pi_actual']:.1f}\% actual \ (Part 28)", color=GB, width=5.6,
                         font_size=19),
        ).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)
        with self.voiceover(
            "Did anyone see the recessions coming? <bookmark mark='a'/> Each quarter the professional forecasters "
            "give the chance that output falls the next quarter. Here it is in the quarter before each American "
            "recession since 1970, and at its highest once the recession had begun. <bookmark mark='b'/> Before, "
            "mostly between ten and forty percent; only once, in 1980, above a half. Once inside, they recognized "
            "it. <bookmark mark='c'/> The famous misses are the same story: in August 2008 the median forecaster "
            f"expected growth of {R['g_forecast']:.1f} percent in 2009, which shrank by {abs(R['g_actual']):.1f}; "
            f"<bookmark mark='d'/> in June 2021 the Federal Reserve projected inflation of {R['pi_forecast']:.1f} "
            f"percent for 2022, which came in at {R['pi_actual']:.1f}. Across 63 countries, as the opening showed, "
            "it is the same: recessions are recognized, not forecast."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("b")
            hi = [r_[1] for r_, s_ in zip(rows, st) if s_["p_before"] > 50]
            if hi:
                self.play(*[Indicate(m_, color=E.ACCENT, scale_factor=1.3) for m_ in hi], run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(recs[0], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(recs[1], shift=UP * 0.1))
        self.clear_scene()
