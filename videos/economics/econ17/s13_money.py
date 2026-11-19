from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403

BUYERS = ("ana", "bo")
SELLERS = ("crusoe", "friday")


class Money(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Matching with money: \ the assignment game", r"When partners can pay each other, \ how is "
             r"the surplus split?", "Chapter eleven. Matching with money: the assignment game.",
             lit={1971: r"Shapley and Shubik", 1982: r"Kelso and Crawford", 1986: r"Demange, Gale and Sotomayor"},
             scale=("person", "market"), horizon=("a year",))
        self.table()
        self.core()

    def table(self):
        g = load("assignment")
        v = g["values"]
        head = label(r"two boats for sale, \ two buyers: \ what each pair creates together", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        xs, ys = [-0.8, 2.2], [1.3, 0.1]
        hdr = VGroup(*[who_chip(s, 0.55, 18).move_to([x, 2.4, 0]) for s, x in zip(SELLERS, xs)])
        rws = VGroup(*[who_chip(b, 0.55, 18).move_to([-3.6, y, 0]) for b, y in zip(BUYERS, ys)])
        cells = VGroup()
        for i in range(2):
            for j in range(2):
                cells.add(label(rf"{v[i][j]:.0f}", font_size=34, color=WHITE).move_to([xs[j], ys[i], 0]))
        best = VGroup(*[SurroundingRectangle(cells[i * 2 + g["assign"][i]], color=STABLE, buff=0.18)
                        for i in range(2)])
        side = VGroup(
            label(r"a number is the buyer's value for that boat, \ less what its owner could get elsewhere",
                  font_size=21, color=GREY_A),
            label(rf"the best pairing: \ Ana with Friday's boat, \ Bo with Crusoe's: \ {g['total']:.0f} in all",
                  font_size=23, color=STABLE),
            label(r"Lloyd Shapley and Martin Shubik, \ 1971: \ the assignment game", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Shapley and Shubik, Int.\ J.\ Game Theory 1(1) (1971)", corner=DR, font_size=13)
        with self.voiceover(
            "Everything so far has had no money changing hands. When partners can pay each other, matching meets "
            "prices again. <bookmark mark='a'/> Crusoe and Friday each have a boat to sell, and Ana and Bo each want "
            "one. The table shows what each pair would create together: the buyer's value for that boat, less "
            "what its owner could get elsewhere. <bookmark mark='b'/> The best pairing puts Ana with Friday's boat "
            "and Bo with Crusoe's, for fifteen in all. <bookmark mark='c'/> Lloyd Shapley and Martin Shubik called "
            "this the assignment game, in 1971. The question is how the fifteen is split, by the prices the boats "
            "sell for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(rws), FadeIn(cells), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(best), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def core(self):
        g = load("assignment")
        so, bo = g["seller_optimal"], g["buyer_optimal"]
        nl = NumberLine(x_range=[0, 8, 1], length=8.0, include_numbers=True, font_size=22, color=GREY_B).move_to(
            DOWN * 0.1)
        lo, hi = bo["sellers"][1], so["sellers"][1]
        band = Line(nl.n2p(lo), nl.n2p(hi), color=STABLE, stroke_width=12)
        ends = VGroup(label(r"best for the buyers", font_size=19, color=PROPOSE).next_to(nl.n2p(lo), UP, buff=0.4),
                      label(r"best for the sellers", font_size=19, color=MONEY).next_to(nl.n2p(hi), UP, buff=0.4))
        cap = label(r"what Friday gets from selling to Ana, \ above Friday's alternative", font_size=21,
                    color=GREY_A).next_to(nl, DOWN, buff=0.6)
        head = label(r"the core: \ every split no pair could beat by dealing on its own", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"the splits form an interval: \ a lattice again, \ with each side's best at one end",
                  font_size=22),
            label(r"they are exactly the competitive prices: \ supply equals demand for each boat", font_size=22,
                  color=STABLE),
            label(r"an English auction for many items ends at the buyers' end \ (Demange, \ Gale and Sotomayor, \ 1986)",
                  font_size=21, color=PROPOSE),
            label(r"with wages for prices, \ the same model matches workers to firms: \ parts thirty-nine and forty-nine",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.8)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Agora finds every split that no pair could beat by dealing on its own: the core. "
            "<bookmark mark='a'/> It is an interval. Here is Friday's share: at the buyers' end, Friday gets two "
            "shells above what the boat would fetch elsewhere; at the sellers' end, eight. "
            "<bookmark mark='b'/> It is a lattice again, with the buyers' best at one end and the sellers' best at "
            "the other, as in Gale and Shapley's marriages. <bookmark mark='c'/> Shapley and Shubik showed these "
            "splits are exactly the competitive equilibrium prices, at which each boat has one buyer who wants it. "
            "<bookmark mark='d'/> And an English auction for many items, run as in part sixteen, ends at the "
            "buyers' end of the interval. <bookmark mark='e'/> Put wages in place of prices, and the same model "
            "matches workers to firms, which parts thirty-nine and forty-nine take up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nl), FadeIn(cap), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(band), FadeIn(ends))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
