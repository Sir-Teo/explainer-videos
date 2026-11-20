from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403

CC = {"DE": ("#BBBBBB", r"Germany"), "IT": ("#7FD1B9", r"Italy"), "ES": ("#F2C14E", r"Spain"),
      "GR": ("#7EC8F5", r"Greece")}


class Euro(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Currency areas and the euro", r"When should countries share a currency?",
             "Chapter ten. Currency areas and the euro.", lit={1961: r"Mundell", 1999: r"the euro", 2012: r"Draghi"},
             scale=("nation", "world"), horizon=("a decade",))
        self.oca()
        self.spreads()

    def oca(self):
        cards = point_cards([
            (r"the gain", r"no exchange-rate risk, \\ cheaper trade, \\ one market", CALM),
            (r"the cost", r"no exchange rate \\ to absorb a shock \\ that hits one region", CRISIS),
            (r"what makes it work", r"workers who move, \\ a shared budget, \\ similar shocks, \\ flexible wages", DEM),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.1)
        head = label(r"Mundell (1961): \ an optimum currency area", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                          buff=0.5)
        foot = label(r"America has all four; \ the euro area, \ in 1999, \ had the first", font_size=22,
                     color=WHITE).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Mundell, \ ``A Theory of Optimum Currency Areas'', \ \emph{AER} 51(4) (1961)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "The trilemma says a fixed exchange rate costs a country its monetary policy. When is that worth it? "
            "<bookmark mark='a'/> Robert Mundell asked in 1961 what makes a region an optimum currency area. The "
            "gain from sharing a currency is no exchange-rate risk and cheaper trade. <bookmark mark='b'/> The cost "
            "is losing the exchange rate as a shock absorber when trouble hits one region and not another. "
            "<bookmark mark='c'/> The cost is small if workers move to where the jobs are, if a shared budget sends "
            "money to the region in trouble, if shocks hit everyone alike, and if wages adjust. "
            "<bookmark mark='d'/> The United States has all four. The euro's members, in 1999, had mainly the first "
            "of these: open borders, with languages that keep most workers at home, and almost no common budget."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def spreads(self):
        E_ = load("euro")
        ax = plane([1995, 2020], [0, 32], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.8, y_length=4.6,
                   xticks=[1995, 2000, 2005, 2010, 2015, 2020], yticks=[0, 10, 20, 30],
                   ylabel=r"ten-year government bond yields, \ \%", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        lines = {c: path(ax, E_[c]["t"], E_[c]["v"], col, 3.0, smooth=False) for c, (col, _) in CC.items()}
        euro99 = vline(ax, 1999.0, 0, 32, GREY_B, 1.5)
        dr = vline(ax, 2012.57, 0, 32, USD, 1.5)
        key = VGroup(*[label(n, font_size=16, color=col) for c, (col, n) in CC.items()]).arrange(RIGHT, buff=0.4)
        key.next_to(ax, UP, buff=0.12)
        side = VGroup(
            label(r"1999: \ the euro: \\ yields converge, \\ capital flows south", font_size=18, color=WHITE),
            label(r"2010--12: \ no exchange rate \\ to fall, \ no central bank \\ of one's own: \ spreads soar",
                  font_size=18, color=CRISIS),
            label(r"July 2012: \ `whatever it takes' \\ (Part 31): \ a backstop", font_size=18, color=USD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"OECD Main Economic Indicators, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Here is the euro's record in one chart. <bookmark mark='a'/> As the currency approached, the yields "
            "on Italian, Spanish and Greek government bonds fell to Germany's: markets treated them as nearly the "
            "same risk, and capital flowed south into housing and government debt. <bookmark mark='b'/> When the "
            "flows stopped after 2008, the southern economies had no exchange rate to fall and no central bank of "
            "their own to stand behind their debts, and in 2010 to 2012 the spreads soared, Greece's furthest. "
            "<bookmark mark='c'/> They fell when the European Central Bank promised, in July 2012, to do whatever "
            "it takes: the backstop of Part thirty-one, and of Part thirty-two's sovereign default. The euro "
            "survived, by building some of what Mundell's list required."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[Create(ln) for ln in lines.values()], FadeIn(euro99), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(lines["GR"], color=WHITE, scale_factor=1.0))
            vo.wait_until("c")
            self.play(FadeIn(dr), FadeIn(side[2]))
        self.clear_scene()
