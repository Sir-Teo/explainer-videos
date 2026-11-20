from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ stress tests, \ the treasury desk, \ deposit pricing", r"How do banks and "
             r"their supervisors manage the risks in this part?", "Chapter fourteen. In practice: stress tests, the "
             "treasury desk, deposit pricing.", lit={2009: r"the first US stress test", 2022: r"the scenario"},
             scale=("firm",), horizon=("a quarter", "years"))
        self.stress()
        self.called()
        self.pricing()
        self.desk()

    def stress(self):
        r = load("rates")
        ax = plane([2021, 2025], [0, 6], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[2021, 2022, 2023, 2024, 2025], yticks=[0, 1, 2, 3, 4, 5, 6], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        sc = path(ax, r["scenario_t"], r["scenario_v"], color=GREY_B, width=4, smooth=False)
        ten = path(ax, r["ten"]["t"], r["ten"]["v"], color=BOND, width=3, smooth=False)
        ff = path(ax, r["ff"]["t"], r["ff"]["v"], color=RATE, width=3, smooth=False)
        side = VGroup(
            label(r"the Fed's 2022 severely \\ adverse scenario: \\ the 10-year yield falls \\ to "
                  rf"{r['trough']:.2f}\%; \ short rates near zero; \\ unemployment {r['unemployment_peak']:.0f}\%",
                  font_size=18, color=GREY_B),
            label(rf"what happened: \ the 10-year \\ {r['ten_2022_01']:.2f}\% to {r['ten_2022_10']:.2f}\% \\ by "
                  r"October 2022", font_size=19, color=BOND),
            label(rf"the federal funds rate: \\ {r['ff_2022_01']:.2f}\% to {r['ff_2022_12']:.1f}\% \\ in a year",
                  font_size=19, color=RATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Federal Reserve, \ 2022 Stress Test Scenarios; \ FRED: \ the federal funds rate and the "
                       r"10-year yield, \ monthly", corner=DR, font_size=12)
        with self.voiceover(
            "Since the first stress test, in 2009, America's largest banks have had to show regularly that they "
            "could survive a severe "
            "recession, described by the Federal Reserve in a scenario. <bookmark mark='a'/> The scenario "
            "published in February 2022 had the ten-year Treasury yield falling to three quarters of a percent, "
            "short-term rates near zero throughout, and unemployment rising to ten percent. That is what severe "
            "recessions had looked like before. <bookmark mark='b'/> What happened instead: the ten-year yield rose "
            f"from {r['ten_2022_01']:.1f} percent to about {r['ten_2022_10']:.0f} percent by October. "
            f"<bookmark mark='c'/> And the federal funds rate went from almost nothing to {r['ff_2022_12']:.1f} "
            "percent within the year."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(sc), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ten), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(ff), FadeIn(side[2]), run_time=1.5)
        self.clear_scene()

    def called(self):
        c = calls.CALLS["stress_2022"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=19).move_to(UP * 0.1)
        tag = published_tag(r"Federal Reserve, \ 2022 Stress Test Scenarios; \ the Federal Reserve's review of "
                            r"Silicon Valley Bank (April 2023)", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> A stress scenario is not a forecast, and the Federal Reserve says so. "
            "But it is a judgment about which dangers matter, and in 2022 the danger it tested was a recession with "
            "falling rates. <bookmark mark='b'/> The danger that arrived was rising rates. The losses that sank "
            "Silicon Valley Bank came from long bonds losing value as yields rose, a risk the scenario did not "
            "test; and Silicon Valley Bank, grown large only recently, was not yet among the banks being tested. "
            "<bookmark mark='c'/> Wrong, as a "
            "judgment of where the danger was. Since 2023 the Federal Reserve has added exploratory analyses, "
            "with other kinds of shock, beside the main test."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()

    def pricing(self):
        b = load("betas")
        ax = plane([2022, 2024.1], [0, 6], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[2022, 2023, 2024], yticks=[0, 1, 2, 3, 4, 5, 6], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        ff = path(ax, b["t"], b["ff"], color=RATE, width=3, smooth=False, xr=(2022, 2024.1))
        cd = path(ax, b["t"], b["cd"], color=BOND, width=3, smooth=False, xr=(2022, 2024.1))
        sv = path(ax, b["t"], b["sav"], color=DEPOSIT, width=4, smooth=False, xr=(2022, 2024.1))
        side = VGroup(
            label(rf"federal funds: \\ {b['ff_from']:.2f}\% to {b['ff_to']:.2f}\%", font_size=19, color=RATE),
            label(rf"12-month CDs: \\ {b['cd_from']:.2f}\% to {b['cd_to']:.2f}\%: \ beta {b['beta_cd']:.2f}",
                  font_size=19, color=BOND),
            label(rf"savings: \\ {b['sav_from']:.2f}\% to {b['sav_to']:.2f}\%: \ beta {b['beta_savings']:.2f}",
                  font_size=19, color=DEPOSIT),
            label(r"the gap is the bank's income \\ from its depositors: \\ the deposit franchise", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"FDIC national deposit rates; \ the federal funds rate; \ via FRED, \ monthly", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Deposit pricing is a bank's daily decision. <bookmark mark='a'/> From February 2022 to December 2023, "
            f"the federal funds rate rose from {b['ff_from']:.2f} to {b['ff_to']:.2f} percent. "
            "<bookmark mark='b'/> The national average rate on twelve-month certificates of deposit rose to "
            f"{b['cd_to']:.2f} percent: a beta of a third. <bookmark mark='c'/> On savings accounts, to "
            f"{b['sav_to']:.2f} percent: a beta under a tenth. <bookmark mark='d'/> The gap is what depositors pay "
            "the bank for convenience, and for not shopping around. Itamar Drechsler, Alexi Savov and Philipp "
            "Schnabl call it the deposit franchise, and showed that it works like a hedge: when rates rise, a "
            "bank's long assets lose value, but its sticky deposits become more valuable. That hedge holds only if "
            "the depositors stay."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ff), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cd), FadeIn(side[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(sv), FadeIn(side[2]), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def desk(self):
        S = load("sheet")
        rows = VGroup(
            label(r"the treasury desk: \ asset and liability management", font_size=27, color=E.ACCENT),
            label(rf"duration: \ a ten-year bond at 1.5\% has a duration of {S['duration']:.1f} years: \ "
                  rf"each point on yields costs about {S['duration']:.0f}\% of its price", font_size=21, color=BOND),
            label(r"the gap: \ long assets against deposits that may stay for years, \ or leave in a day",
                  font_size=21, color=DEPOSIT),
            label(r"liquidity: \ hold enough liquid assets for thirty days of stressed outflows \ (Basel III's "
                  r"coverage ratio)", font_size=21, color=CB),
            label(r"funding plans: \ know in advance what can be pledged at the discount window", font_size=21,
                  color=CB),
            label(r"in 2023, \ thirty days of outflows came in one", font_size=23, color=RUN),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        with self.voiceover(
            "And the treasury desk, which manages the whole balance sheet. <bookmark mark='a'/> Its first number "
            f"is duration. A ten-year bond yielding one and a half percent has a duration of {S['duration']:.1f} "
            f"years: each point on yields costs about {S['duration']:.0f} percent of its price. "
            "<bookmark mark='b'/> Against long assets it sets deposits, which may stay for years, or leave in a day. "
            "<bookmark mark='c'/> Since Basel III, large banks must hold enough liquid assets to cover thirty days "
            "of outflows in a stress. <bookmark mark='d'/> And a good desk knows in advance what it can pledge at "
            "the central bank's discount window, and has tested it. <bookmark mark='e'/> In March 2023, Silicon "
            "Valley Bank faced thirty days of stressed outflows in a single day."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
