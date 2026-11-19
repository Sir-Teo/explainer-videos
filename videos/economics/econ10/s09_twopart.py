from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403


class TwoPart(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Two-part tariffs: \ Oi's Disneyland", r"Why charge a fee to get in and a price per ride?",
             "Chapter seven. Two-part tariffs: Oi's Disneyland.", lit={1971: r"Oi's Disneyland"},
             horizon=("a day",))
        self.one()
        self.two()

    def one(self):
        r = load("rides")
        ax = plane([0, 12], [0, 12], center=LEFT * 3.0 + DOWN * 0.3, x_length=5.6, y_length=5.0,
                   xticks=[0, 4, 8, 12], yticks=[0, 4, 8, 12], xlabel=r"rides a day", ylabel=r"\$ a ride", font_size=17)
        a = ax.ax
        qs = np.linspace(0, 10, 50)
        dem = path(ax, qs, 10 - qs, color=DEM, width=3.5, smooth=False)
        c = r["c"]
        mc = DashedLine(a.c2p(0, c), a.c2p(12, c), color=MC, stroke_width=2)
        m = r["mono"]
        mono_prof = region(ax, [(0, c), (m["q"], c), (m["q"], m["p"]), (0, m["p"])], PROFIT, 0.3)
        fee = region(ax, [(0, c), (10 - c, c), (0, 10)], CS, 0.4)
        side = VGroup(
            label(r"the Island's pleasure park: \ a visitor wants $10 - p$ rides a day; \ a ride costs \$2",
                  font_size=21),
            label(rf"one price per ride: \ \${m['p']:.0f} a ride, \ {m['q']:.0f} rides, \ profit \${m['profit']:.0f}",
                  font_size=22, color=PROFIT),
            label(r"two parts: \ rides at cost, \ \$2, \\ and an entry fee equal to the visitor's whole surplus",
                  font_size=22, color=CS),
            label(rf"fee \${r['one']['fee']:.0f}: \ profit \${r['one']['profit']:.0f}, \ twice as much, \ and no "
                  rf"waste", font_size=22, color=CS),
            label(r"with identical buyers, \ a two-part tariff is perfect discrimination", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "In 1971 Walter Oi asked how Disneyland should price: a fee at the gate, a price for each ride, or both? "
            "<bookmark mark='a'/> Take the Island's pleasure park. A visitor wants ten minus p rides a day at a price "
            "of p, and each ride costs the park two dollars. <bookmark mark='b'/> With one price per ride, the best is "
            "six dollars: four rides, and sixteen dollars of profit per visitor. <bookmark mark='c'/> Now use two "
            "parts. Price the rides at cost, two dollars, so the visitor takes all eight that are worth their cost, "
            "and charge an entry fee equal to the visitor's whole surplus. <bookmark mark='d'/> The fee is thirty-"
            "two dollars, and profit doubles to thirty-two. <bookmark mark='e'/> With identical visitors, a "
            "two-part tariff achieves perfect discrimination: nothing is wasted, and the park takes it all. Razors "
            "and blades, printers and ink, clubs with a joining fee: all variations on this."
        ) as vo:
            self.play(FadeIn(ax), Create(dem), Create(mc), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(mono_prof), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeOut(mono_prof), FadeIn(fee), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def two(self):
        r = load("rides")
        t = r["two"]
        rows = VGroup(
            label(r"now two kinds of visitor: \ two in three want $10 - p$ rides, \ the keen third $16 - p$",
                  font_size=26),
            label(r"one fee for all, \ so it can be no more than the smaller visitor's surplus", font_size=25,
                  color=GREY_A),
            label(rf"rides at cost: \ fee \${t['fee_at_cost']:.0f}, \ profit \${t['profit_at_cost']:.0f} from three "
                  r"visitors", font_size=25),
            label(rf"rides at \${t['p']:.0f}: \ fee \${t['fee']:.0f}, \ profit \${t['profit']:.0f}; \ the keen "
                  rf"visitor alone: \${t['profit_without_smallest']:.0f}", font_size=25, color=PROFIT),
            label(r"the price per ride rises above cost: \ it charges the keen visitors more, \ in proportion to "
                  r"use", font_size=24, color=E.ACCENT),
            label(r"the ride price does the sorting; \ the fee collects from everyone", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.36)
        tag = published_tag(r"Oi, Quarterly Journal of Economics 85(1) (1971)", corner=DR, font_size=14)
        with self.voiceover(
            "Real visitors differ. <bookmark mark='a'/> Suppose two visitors in three want ten minus p rides, and "
            "the third, a keen one, wants sixteen minus p. <bookmark mark='b'/> If everyone pays the same fee, it "
            "can be no more than the smaller visitor's surplus, or they won't come. <bookmark mark='c'/> With rides at cost, the fee is thirty-two "
            "dollars, and three visitors bring in ninety-six. <bookmark mark='d'/> But raising the ride price to "
            "four dollars, and cutting the fee to eighteen, brings in a hundred and two. Shutting the ordinary "
            "visitors out, and charging the keen one their whole surplus of ninety-eight, would bring in less, so the "
            "park keeps them all. <bookmark mark='e'/> The price per ride goes above cost because it charges the keen visitors more, in proportion to how much they "
            "ride. <bookmark mark='f'/> The ride price does the sorting, and the fee collects from everyone. This "
            "is Oi's answer to his Disneyland dilemma."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
