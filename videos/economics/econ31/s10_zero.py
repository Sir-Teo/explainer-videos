from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Zero(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The zero bound in practice", r"What happened when real central banks ran out of room?",
             "Chapter eight. The zero bound in practice.",
             lit={1999: r"Japan at zero", 2008: r"the Fed at zero"}, scale=("nation", "world"),
             horizon=("a year", "decades"))
        self.rates()

    def rates(self):
        Z = load("zlb")
        ax = plane([1990, 2027], [-1, 9], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 2, 4, 6, 8], ylabel=r"policy rate, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        zero = seg(ax, 1990, 0, 2027, 0, GREY_C, 1.5)
        jp = path(ax, Z["jp_t"], Z["jp"], COUNTRY["JP"], 3, smooth=False)
        us = path(ax, Z["us_t"], Z["us"], COUNTRY["US"], 3, smooth=False)
        ea = path(ax, Z["ecb_t"], Z["ecb"], COUNTRY["EA"], 3, smooth=False)
        side = VGroup(
            label(r"red: \ Japan's overnight call rate", font_size=18, color=COUNTRY["JP"]),
            label(rf"at or below 0.1\% for {Z['jp_low_months'] // 12} years \\ of the last {2026 - 1999}", font_size=18,
                  color=COUNTRY["JP"]),
            label(r"pink: \ the Fed's target \\ (the top of its range from 2008)", font_size=18, color=COUNTRY["US"]),
            label(rf"at zero for {Z['us_zero_months']} months: \\ 2008--15 and 2020--22", font_size=18,
                  color=COUNTRY["US"]),
            label(rf"purple: \ the ECB's deposit rate, \\ below zero for {Z['ecb_negative_months']} months",
                  font_size=18,
                  color=COUNTRY["EA"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"OECD (Japan's call rate), \ Federal Reserve Board, \ ECB, \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Part 30's model treated the zero bound as a thought experiment. It became the main problem of "
            "central banking for two decades. <bookmark mark='a'/> Japan got there first. After its bubble burst, "
            "the Bank of Japan cut its rate to near zero by 1999, <bookmark mark='b'/> and it stayed at or below a "
            f"tenth of a percent for about {Z['jp_low_months'] // 12} of the next {2026 - 1999} years. In 2001 the "
            "bank began buying assets to expand its balance sheet, the first quantitative easing. "
            "<bookmark mark='c'/> The Federal Reserve reached zero in December 2008, <bookmark mark='d'/> stayed "
            "there seven years, and returned in March 2020 for two more. <bookmark mark='e'/> The European Central "
            "Bank went further, and in June 2014 set its deposit rate below zero, where it stayed for eight years, "
            f"reaching {Z['ecb_min']:.1f} percent. When the rate cannot fall, a central bank still has its balance "
            "sheet and its words. The next two chapters are about what those achieved."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(jp), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(us), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(ea), FadeIn(side[4]), run_time=2)
        self.clear_scene()
