from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 14, r"Frontier: \ fragmentation and climate clubs", r"What would a world split into blocs cost, "
             r"\ and can trade policy serve the climate?", "Chapter fourteen. Frontier: fragmentation and climate "
             "clubs.", lit={2015: "Nordhaus"}, scale=("world",), horizon=("a decade",))
        self.blocs()
        self.clubs()

    def blocs(self):
        S = load("scenarios")
        cards = point_cards([
            (r"fragmentation scenarios", r"split the world model into blocs that tax each other's goods, \ and "
             r"measure the loss: \ larger for small, \ open economies than for continents", STATE),
            (r"what the losses depend on", rf"the trade elasticity \ (this part's model: \ US "
             rf"{100 * [r for r in S['rows'] if r['theta'] == 8.0 and r['retaliation']][0]['us']:+.2f}\% at "
             r"$\theta = 8$ with retaliation), \ supply chains, \ and technology's diffusion".replace("-", "{-}"),
             US),
            (r"the hard part", r"ideas cross borders too: \ splitting technology may cost more than splitting "
             r"trade \ (Parts 21 and 65)", FREE),
            (r"the measurement", r"firms' own data on where inputs come from, \ customs records, \ shipping: \ "
             r"geoeconomics as it happens", PRICE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"a world in blocs", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "At the frontier, economists are pricing a divided world. <bookmark mark='a'/> Fragmentation "
            "scenarios split the quantitative trade model into blocs that tax each other's goods, and measure the "
            "loss. Small, open economies lose most; continental ones least. <bookmark mark='b'/> The losses depend "
            "on the trade elasticity, as chapter four showed, and on supply chains, which carry a tariff from one "
            "border to the next. <bookmark mark='c'/> The hardest part is ideas. If blocs stop sharing technology, "
            "the cost may dwarf the cost of tariffs, because, as Parts twenty-one and sixty-five showed, growth "
            "comes from ideas. <bookmark mark='d'/> And the measurement is moving to firms' own records: where each "
            "input comes from, customs declarations, ships' positions. Geoeconomics, measured as it happens."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def clubs(self):
        cards = VGroup(
            history_card(r"2015", r"Nordhaus's climate club", r"countries that agree to cut emissions put a uniform "
                         r"tariff on the goods of those that do not: \ staying out costs more than joining",
                         color=FREE, width=11.4, font_size=21),
            history_card(r"2026", r"a border carbon adjustment", r"the European Union charges importers of steel, "
                         r"\ cement and other goods for the carbon in them, \ as its own producers pay",
                         color=STATE, width=11.4, font_size=21),
            history_card(r"the question", r"a weapon for a public good", r"trade policy used to solve a free-rider "
                         r"problem \ (Parts 15 and 48), \ with the risk that it becomes protection by another name",
                         color=E.ACCENT, width=11.4, font_size=21),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        tag = published_tag(r"Nordhaus, \ AER 105(4) (2015); \ Part 48", corner=DL, font_size=12)
        with self.voiceover(
            "The other frontier turns the weapon to a common good. <bookmark mark='a'/> In 2015 William Nordhaus "
            "proposed a climate club: countries that agree to cut emissions put a modest uniform tariff on the "
            "goods of countries that do not, so that staying out costs more than joining. Part forty-eight met it. "
            "<bookmark mark='b'/> From 2026 the European Union charges importers of steel, cement and some other "
            "goods for the carbon emitted in making them, as its own producers pay for theirs. <bookmark mark='c'/> "
            "Trade policy as the answer to a free-rider problem, the problem of Part fifteen, with the old risk "
            "attached: that it becomes protection by another name."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
