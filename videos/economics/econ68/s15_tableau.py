from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403

ALL_PIPES = ("spending", "goods", "labour", "taxes", "public", "saving", "loans", "money", "trade", "capital")


class Tableau(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Tableau", r"Which pipes of the economy has the series opened, \ and which boxes are "
             r"still sealed?", "Chapter thirteen. The Tableau.", lit={1758: "Quesnay"}, scale=("world",),
             horizon=("a century",))
        self.pipes()
        self.sealed()

    def pipes(self):
        tab = tableau_map(open_pipes=ALL_PIPES, lit=("households", "firms", "government", "banks", "world"),
                          width=12.6, font_size=21).move_to(DOWN * 0.2)
        cols = {"spending": E.HOUSEHOLDS, "goods": E.FIRMS, "labour": E.HOUSEHOLDS, "taxes": E.HOUSEHOLDS,
                "public": E.GOVERNMENT, "saving": E.HOUSEHOLDS, "loans": E.BANKS, "money": E.GOVERNMENT,
                "trade": E.FIRMS, "capital": E.WORLD}
        flows = VGroup(*[flowing(tab.paths[k], c, n=5, period=3.0) for k, c in cols.items()])
        head = label(r"every pipe open", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.3)
        with self.voiceover(
            "In Part one the economy was drawn as plumbing, after Quesnay's Tableau of 1758 and Phillips's water "
            "machine: five tanks, households, firms, government, banks and the rest of the world, and ten pipes "
            "between them, each sealed until a part opened it. <bookmark mark='a'/> Spending and goods in Part two; "
            "saving in Part twenty-two; labour in twenty-four; money in twenty-five; loans in twenty-six; public "
            "spending in thirty-two; capital flows in thirty-four; trade in thirty-five; taxes in forty-one. "
            "<bookmark mark='b'/> All ten are open now, and the circulation the series built runs through every one."
        ) as vo:
            self.play(FadeIn(tab), FadeIn(head))
            vo.wait_until("b")
            self.add(flows)
            self.wait(4.0)
            for f in flows:
                for d in f:
                    d.clear_updaters()
                f.clear_updaters()
        self.clear_scene()

    def sealed(self):
        cards = point_cards([
            (r"expectations", r"how people form beliefs about the future: \ rational, \ adaptive, \ diagnostic, \ "
             r"or learned \ (Parts 28, 45, 57)", MODEL),
            (r"institutions", r"why some countries have the rules that make markets work, \ and how rules change "
             r"\ (Parts 21, 47)", STATE),
            (r"the household's inside", r"how money and time are shared within a family \ (Part 49)", ROW),
            (r"the long-run growth rate", r"what sets the speed of ideas, \ and whether it can last \ (Parts 21, "
             r"65)", TRUE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"the boxes still sealed", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "But the Tableau has boxes, not pipes, that no part could open fully. <bookmark mark='a'/> Expectations: "
            "how people form beliefs about the future, rationally, adaptively, or by learning. <bookmark mark='b'/> "
            "Institutions: why some countries have the rules that make markets work, and how rules change. "
            "<bookmark mark='c'/> The inside of the household: how money and time are shared within a family. "
            "<bookmark mark='d'/> And the long-run growth rate: what sets the speed at which ideas arrive, and "
            "whether it can last. Each part that touched them made progress; none could close the question."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
