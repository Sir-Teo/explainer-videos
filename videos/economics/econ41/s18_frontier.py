from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ migration, \ bargaining, \ behaviour", r"What is still being worked out?",
             "Chapter sixteen. Frontier: migration, bargaining, behaviour.",
             lit={2013: r"Kleven, \ Landais and Saez", 2014: r"Piketty, \ Saez and Stantcheva"},
             scale=("person", "world"), horizon=("a decade",))
        self.open()

    def open(self):
        F = tables.FRONTIER41.data
        cards = point_cards([
            (r"migration", rf"footballers in 14 leagues: \\ foreign players' \\ elasticity about {F['foreign']:g}, \\ "
                           rf"domestic {F['domestic']:g}", WORKER),
            (r"bargaining", r"if top pay partly \\ reflects bargaining, \\ not output, \ the best \\ top rate is "
                            r"higher", TOP),
            (r"behaviour", r"salience, \ inattention, \\ tax morale: \ taxes \\ people misperceive", RATE),
        ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.2)
        head = label(r"open questions", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.FRONTIER41.tag + r"; \ " + tables.DIAMOND_SAEZ_2011.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Three frontiers. <bookmark mark='a'/> Migration. If top earners can move country, the elasticity that "
            "matters includes moving. Henrik Kleven, Camille Landais and Emmanuel Saez studied footballers in "
            "fourteen European leagues: the number of foreign players responds to a country's top tax rate with an "
            f"elasticity of about {F['foreign']:g}, domestic players with about {F['domestic']:g}. Mobility is high "
            "for some and low for most, which is why special schemes for foreign earners exist. "
            "<bookmark mark='b'/> Bargaining. Piketty, Saez and Stefanie Stantcheva separate top earners' responses "
            "into working less, avoiding tax, and bargaining for pay that comes at others' expense. Only the first "
            "is a true cost; if much of the response is bargaining, the best top rate is higher. "
            "<bookmark mark='c'/> Behaviour. If people misperceive taxes, ignore those they do not see, or pay out of "
            "a sense of duty, the formulas of this part need new terms, and the evidence for them is still coming in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
