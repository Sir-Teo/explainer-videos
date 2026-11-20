from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Volcker(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Volcker, \ 1979--82", r"What did it cost to bring inflation down?", "Chapter ten. Volcker, "
             "1979 to 1982.", lit={1979: r"6 October", 1994: r"Ball"}, scale=("nation",), horizon=("years",))
        self.path_()
        self.cost()

    def path_(self):
        V = load("volcker")
        ax = plane([1977, 1988], [0, 20], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1977, 1979, 1981, 1983, 1985, 1987], yticks=[0, 5, 10, 15, 20], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        ff = path(ax, V["t"], V["ff"], color=CB, width=3, smooth=False)
        pi = path(ax, V["t"], V["inflation"], color=INFL, width=3, smooth=False)
        un = path(ax, V["t"], V["unemployment"], color=UNEMP, width=3, smooth=False)
        side = VGroup(
            label(rf"inflation: \ {V['peak_inf']:.1f}\% \\ in {V['peak_inf_date'][:4]}", font_size=20, color=INFL),
            label(r"6 October 1979: \\ the Fed targets money, \\ and lets rates go", font_size=19, color=CB),
            label(rf"the federal funds rate: \\ {V['peak_ff']:.1f}\% in {V['peak_ff_date'][:4]}", font_size=20,
                  color=CB),
            label(rf"unemployment: \\ {V['peak_un']:.1f}\% in late {V['peak_un_date'][:4]}", font_size=20,
                  color=UNEMP),
            label(r"inflation below 5\% \\ by 1983", font_size=20, color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Federal Reserve and BLS: \ the federal funds rate, \ CPI inflation, \ unemployment, \ "
                       r"monthly, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "The cure came from Paul Volcker, chairman of the Federal Reserve from August 1979. "
            f"<bookmark mark='a'/> Inflation, in red, peaked at {V['peak_inf']:.1f} percent in "
            f"{V['peak_inf_date'][:4]}. <bookmark mark='b'/> On the sixth of October 1979, the Fed announced that it "
            "would target the growth of money and let interest rates go wherever that took them. "
            f"<bookmark mark='c'/> The federal funds rate, in green, reached {V['peak_ff']:.1f} percent in "
            f"{V['peak_ff_date'][:4]}. <bookmark mark='d'/> Two recessions followed, and unemployment, in blue, "
            f"reached {V['peak_un']:.1f} percent at the end of {V['peak_un_date'][:4]}, the highest since the "
            "Depression. <bookmark mark='e'/> And inflation fell below five percent by 1983, and stayed there."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(pi), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ff), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(un), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def cost(self):
        V = load("volcker")
        ax = plane([1980, 1986], [-9, 2], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=4.8,
                   xticks=[1980, 1981, 1982, 1983, 1984, 1985, 1986], yticks=[-8, -6, -4, -2, 0, 2],
                   ylabel=r"real GDP against potential, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=15)
        zero = seg(ax, 1980, 0, 1986, 0, color=GREY_D, width=2)
        bars = VGroup()
        for t, g in zip(V["gap_t"], V["gap"]):
            lo, hi = ax.ax.c2p(t + 0.125, 0), ax.ax.c2p(t + 0.125, g)
            bars.add(Rectangle(width=0.22, height=abs(hi[1] - lo[1]), fill_color=UNEMP if g < 0 else OUTPUT,
                               fill_opacity=0.8, stroke_width=0).move_to((lo + hi) / 2))
        side = VGroup(
            label(rf"output lost, \ 1980--85: \\ {V['sac_lost']:.1f} point-years", font_size=20, color=UNEMP),
            label(rf"core inflation: \\ {V['core_1980']:.1f}\% (1980) $\to$ {V['core_1985']:.1f}\% (1985)",
                  font_size=20, color=INFL),
            label(rf"sacrifice ratio: \ {V['sac_ratio']:.1f} \\ point-years per point", font_size=22,
                  color=E.ACCENT),
            label(r"Ball (1994): \ faster disinflations \\ and flexible wages \ cost less", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BEA and CBO: \ real GDP against potential; \ BLS: \ core CPI; \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "What did it cost? Here is America's output against the Congressional Budget Office's estimate of "
            "potential, quarter by quarter, from 1980 to 1985. <bookmark mark='a'/> Add up the shortfalls and you "
            f"get about {V['sac_lost']:.0f} point-years: as if output had been one percent below potential for "
            f"{V['sac_lost']:.0f} years. <bookmark mark='b'/> Over the same years, core inflation fell from "
            f"{V['core_1980']:.0f} percent to {V['core_1985']:.0f}. <bookmark mark='c'/> Divide one by the other, "
            f"and you get a sacrifice ratio of about {V['sac_ratio']:.0f}: two point-years of output for each point "
            "of inflation removed. <bookmark mark='d'/> Laurence Ball, measuring sixty-five disinflations, found "
            "that faster ones, and those in countries with more flexible wage-setting, cost less per point. If "
            "people believe the central bank, the cost should be smaller still. Whether they believed Volcker at "
            "first is doubtful: long-term interest rates stayed high for years."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), LaggedStart(*[GrowFromEdge(b, UP) for b in bars],
                                                                      lag_ratio=0.05), run_time=2)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
