from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 13, r"In practice: who sets prices for a living", r"Where is this chapter's toolkit used?",
             "Chapter thirteen. In practice: who sets prices for a living.", scale=("firm", "nation"),
             horizon=("a day", "a year"))
        head = heading(r"In practice")
        items = [
            (r"commodity desks", r"traders and analysts who forecast supply shocks, \ like the next frost, \ and hedge "
             r"them with futures", COFFEE),
            (r"pricing teams", r"firms estimate their own customers' elasticities, \ often by experiment, \ and set "
             r"prices on the elastic side", E.DEMAND),
            (r"tax analysts", r"treasuries and their scorekeepers decide who bears a proposed tax, \ using this "
             r"chapter's incidence", TAX),
            (r"competition authorities", r"to define a market, \ they ask whether a small price rise would send "
             r"buyers elsewhere", E.SUPPLY),
        ]
        pc = point_cards(items, width=12.8, cols=2, font_size=22).move_to(DOWN * 0.25)
        with self.voiceover(
            "Who uses this for a living? <bookmark mark='a'/> Commodity desks at trading houses and food companies: "
            "their job is to see the next frost coming, judge how far it will move the price, and hedge the risk "
            "with futures contracts. <bookmark mark='b'/> Pricing teams inside firms, who estimate how their own "
            "customers respond to a price, often by running experiments, and who know never to price where demand "
            "is inelastic. <bookmark mark='c'/> Tax analysts in treasuries and parliaments, whose tables of who "
            "pays a proposed tax rest on exactly the incidence calculation of chapter nine. "
            "<bookmark mark='d'/> And competition authorities, who decide what counts as a market by asking "
            "whether a small, lasting rise in price would send enough buyers elsewhere to make it unprofitable. "
            "Part sixty-one does that test properly."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c in zip("abcd", pc.cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
