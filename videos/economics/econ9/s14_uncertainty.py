from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403

CALM = "#7EC8F5"
STORM = "#C9A0FF"


class Uncertainty(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Time and uncertainty: \ Arrow's securities", r"Can markets share risks the way they share "
             r"goods?", "Chapter twelve. Time and uncertainty: Arrow's securities.",
             lit={1953: r"Arrow's securities"}, horizon=("a year",))
        self.states()
        self.securities()
        self.bond()

    def harvest_bars(self, E, names, center, h=0.035):
        g = VGroup()
        for i, (row, nm, col) in enumerate(zip(E, names, (ANA, CHIDI))):
            bars = VGroup()
            for s, (v, sc) in enumerate(zip(row, (CALM, STORM))):
                bars.add(VGroup(Rectangle(width=0.6, height=v * h, stroke_width=0, fill_color=sc, fill_opacity=0.85),
                                label(f"{v:.0f}", font_size=19, color=sc)))
            for b_ in bars:
                b_[1].next_to(b_[0], UP, buff=0.06)
            bars.arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
            g.add(VGroup(bars, label(nm, font_size=21, color=col).next_to(bars, DOWN, buff=0.15)))
        g.arrange(RIGHT, buff=1.0, aligned_edge=DOWN).move_to(center)
        return g

    def states(self):
        r = load("risk")
        bars = self.harvest_bars(r["E"], (r"Ana (fish)", r"Chidi (coconuts)"), LEFT * 3.2 + DOWN * 0.6)
        key = VGroup(label(r"calm", font_size=20, color=CALM), label(r"storm", font_size=20, color=STORM)
                     ).arrange(RIGHT, buff=0.6).next_to(bars, UP, buff=0.6)
        side = VGroup(
            label(r"next year's harvest depends on the weather: \\ calm or storm, \ even odds", font_size=22),
            label(r"Ana's fishing fails in a storm; \\ storms bring Chidi's coconuts down", font_size=22),
            label(r"each eats 50 today; \ both dislike risk \ ($\gamma = 2$)", font_size=22, color=GREY_A),
            label(r"a good is what it is, \ when, \ and in which state of the world: \\ a coconut \emph{in a storm "
                  r"next year} is a good of its own", font_size=21, color=E.ACCENT),
            label(r"Arrow (1953), \ Debreu (1959): \ with markets for all of them, \\ every theorem so far still "
                  r"holds", font_size=21, color=CC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Everything so far happened in one period, with no uncertainty. Real economies have both. "
            "<bookmark mark='a'/> Next year's harvest depends on the weather, calm or stormy, with even odds. "
            "<bookmark mark='b'/> Ana's fishing fails in a storm: eighty baskets of food if it's calm, twenty if "
            "it storms. Chidi's coconuts are the other way round, because storms bring them down. "
            "<bookmark mark='c'/> Today each of them has fifty, and both dislike risk. <bookmark mark='d'/> Kenneth "
            "Arrow's idea, in 1953, was to treat a good in a particular future state as a different good: a coconut "
            "next year if there's a storm is not the same thing as a coconut next year if it's calm. "
            "<bookmark mark='e'/> Debreu built it into his Theory of Value in 1959. If there is a market for every "
            "such good, everything in this part goes through unchanged: existence, and both welfare theorems."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(side[0]), FadeIn(key))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g_, shift=UP * 0.2) for g_ in bars], lag_ratio=0.4), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def securities(self):
        r = load("risk")
        ad = r["ad"]
        before = self.harvest_bars(r["E"], (r"Ana", r"Chidi"), LEFT * 3.4 + UP * 0.9, h=0.022)
        after = self.harvest_bars(ad["c"], (r"Ana", r"Chidi"), LEFT * 3.4 + DOWN * 2.0, h=0.022)
        lb = label(r"harvests", font_size=21, color=GREY_A).next_to(before, LEFT, buff=0.4)
        la = label(r"after trading \\ securities", font_size=21, color=CC).next_to(after, LEFT, buff=0.4)
        q = ad["q"][0]
        sec = ad["securities"]
        side = VGroup(
            label(r"an Arrow security: \ pays one basket \\ in one state, \ nothing in the other", font_size=22),
            label(rf"two securities, \ each priced {q:.3f} baskets today", font_size=22, color=E.ACCENT),
            label(rf"Ana sells {abs(sec[0][0]):.0f} calm-weather claims \\ and buys {sec[0][1]:.0f} storm claims; "
                  r"\ Chidi the reverse", font_size=21),
            label(r"both eat 50 in either weather: \ the risk is shared away", font_size=22, color=CC),
            label(rf"as good as {ad['ce'][0]:.0f} a year for sure, \\ against {ad['ce_autarky'][0]:.2f} "
                  r"without trade", font_size=21, color=CC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "You don't need a market for every good in every state. Arrow showed that a simpler set of markets "
            "will do. <bookmark mark='a'/> An Arrow security pays one basket of food in one state of the world and "
            "nothing in the other. <bookmark mark='b'/> With two states you need two of them, one for calm and one "
            "for storm. On the island each costs nought point four seven five baskets today. "
            "<bookmark mark='c'/> Ana sells thirty claims on food in calm weather, when she'll have plenty, and "
            "buys thirty claims on food in a storm. Chidi does the opposite. <bookmark mark='d'/> Next year, "
            "whatever the weather, each of them eats fifty. The risk has been traded away. "
            "<bookmark mark='e'/> That's as good, for each of them, as fifty a year for certain. Without trade, "
            "their risky harvests would be worth, to someone who dislikes risk as much as they do, only "
            "thirty-nine point two five a year for certain."
        ) as vo:
            self.play(FadeIn(before), FadeIn(lb), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(TransformFromCopy(before, after), FadeIn(la), FadeIn(side[3]), run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def bond(self):
        r = load("risk")
        bo = r["bond"]
        rows = VGroup(
            label(r"now suppose the only asset is a bond: \ it pays the same whatever the weather", font_size=25),
            label(r"it can move food from today to next year, \ but not from calm years to stormy ones", font_size=25),
            label(rf"Ana and Chidi stand the same way today, \ so neither lends: \ each keeps "
                  rf"{bo['ce'][0]:.2f} for sure", font_size=25, color=HOLD),
            label(r"incomplete markets: \ the equilibrium is not efficient, \ and the welfare theorems fail",
                  font_size=25, color=HOLD),
            label(r"real economies have insurance, \ futures, \ options \\ and almost no market for the biggest "
                  r"risk most people face: \ their own earnings", font_size=24, color=GREY_A),
            label(r"Parts 23 and 33: \ asset prices, \ and crises", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.36)
        with self.voiceover(
            "Now take one market away. <bookmark mark='a'/> Suppose the only thing they can trade is a bond, "
            "which pays the same next year whatever the weather. <bookmark mark='b'/> A bond can move food "
            "between today and next year, but it can't move food from calm years to stormy ones, and that's the "
            "move they need. <bookmark mark='c'/> Here Ana and Chidi are in the same position today, so neither "
            "wants to lend to the other: the bond isn't traded at all, and each bears their own weather. "
            "<bookmark mark='d'/> With markets missing, the equilibrium is generally not efficient, and the "
            "welfare theorems no longer apply. <bookmark mark='e'/> Real economies have insurance, futures and "
            "options, but almost no market for the largest risk most people face, the risk to their own future "
            "earnings. <bookmark mark='f'/> Prices of risk come back in Part twenty-three, and what happens when "
            "the markets for it break, in Part thirty-three."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
