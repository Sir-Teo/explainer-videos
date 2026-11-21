from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


class Evidence(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Industrial policy, \ the new evidence", r"Has protecting or subsidizing an industry ever "
             r"worked, \ and how would we know?", "Chapter nine. Industrial policy, the new evidence.",
             lit={2018: r"Juh\'asz", 2025: "Lane"}, scale=("nation",), horizon=("a decade", "a century"))
        self.old()
        self.new()
        self.ships()

    def old(self):
        rows = VGroup(
            label(r"the old evidence: \ regress industries' growth on their protection", font_size=24, color=GREY_A),
            label(r"protected industries grew no faster \ (Krueger and Tuncer, \ Turkey, \ 1982)", font_size=21,
                  color=TARIFF),
            label(r"the problem: \ governments protect industries that are failing", font_size=21, color=GREY_A),
            label(r"the new evidence: \ find protection that fell by accident", font_size=24, color=FREE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.2)
        tag = published_tag(r"Krueger and Tuncer, \ AER 72(5) (1982); \ Juh\'asz, \ Lane and Rodrik, \ Annual "
                            r"Review of Economics (2024)", corner=DL, font_size=12)
        with self.voiceover(
            "For decades the evidence on industrial policy was discouraging. <bookmark mark='a'/> Economists "
            "regressed industries' growth on how much protection they had. <bookmark mark='b'/> Anne Krueger and "
            "Baran Tuncer found that in Turkey the protected industries grew no faster than the rest. <bookmark "
            "mark='c'/> But that design has Part four's problem: governments protect the industries that are "
            "struggling, so protection and weak growth go together whatever protection does. <bookmark mark='d'/> "
            "Réka Juhász, Nathan Lane and Dani Rodrik survey a new generation of studies that look instead for "
            "protection that fell by accident, or by a rule the industries could not influence."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def new(self):
        cards = VGroup(
            history_card(r"1806--13", r"Napoleon's blockade", r"cut France off from British goods, \ but more in "
                         r"some regions than others, \ by the routes smugglers could use; \ the more shielded regions "
                         r"took up mechanized cotton spinning, \ and kept it after the war \ (Juh\'asz)",
                         color=STATE, width=11.6, font_size=20),
            history_card(r"1973--79", r"South Korea's heavy and chemical industry drive", r"steel, \ ships, \ "
                         r"chemicals, \ machinery: \ the targeted industries grew faster in output, \ productivity "
                         r"and exports, \ and stayed ahead after the drive ended \ (Lane)", color=US, width=11.6,
                         font_size=20),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        caveat = label(r"temporary, \ disciplined by export markets, \ and aimed at industries with learning to do",
                       font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Juh\'asz, \ AER 108(11) (2018); \ Lane, \ QJE (2025)", corner=DL, font_size=12)
        with self.voiceover(
            "Two studies stand out. <bookmark mark='a'/> Réka Juhász used Napoleon's blockade of British trade, "
            "from 1806 to 1813. It shielded some French regions more than others, depending on how easily smuggled "
            "British goods could reach them. The more shielded regions took up mechanized cotton spinning faster, "
            "and kept their lead after the war, when British goods returned. A temporary shield, and a lasting "
            "industry: the infant-industry case, in history's own experiment. <bookmark mark='b'/> Nathan Lane "
            "studied South Korea's heavy and chemical industry drive of the nineteen-seventies: steel, ships, "
            "chemicals, machinery. The targeted industries grew faster in output, productivity and exports than "
            "comparable ones, and stayed ahead after the drive ended. <bookmark mark='c'/> What the successes share: "
            "the support was temporary, it was disciplined by having to sell abroad, and it went to industries "
            "with real learning to do."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(caveat))
        self.clear_scene()

    def ships(self):
        cards = point_cards([
            (r"the policy", r"from 2006, \ China made shipbuilding a strategic industry: \ subsidies for "
             r"production, \ investment and entry", STATE),
            (r"the size", r"production subsidies worth about 13--20\% of a ship's price", TARIFF),
            (r"the result", r"China's share of world shipbuilding soared; \ ship prices fell, \ so much of the "
             r"benefit went to the world's shipowners", ROW),
            (r"the waste", r"entry subsidies created yards with little to do; \ combined, \ the subsidies "
             r"returned far less than each alone", PRICE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"Chinese shipbuilding: \ a subsidy measured", font_size=30, color=E.ACCENT).to_edge(UP,
                                                                                                         buff=0.5)
        tag = published_tag(r"Kalouptsidi, \ REStud 85(2) (2018); \ Barwick, \ Kalouptsidi and Zahur, \ REStud "
                            r"(2025)", corner=DL, font_size=12)
        with self.voiceover(
            "And a case of industrial policy at enormous scale. <bookmark mark='a'/> From 2006 China made "
            "shipbuilding a strategic industry, with subsidies for production, investment and the entry of new "
            "yards. <bookmark mark='b'/> Myrto Kalouptsidi detected the subsidies in the costs Chinese yards "
            "revealed by their prices; with Panle Jia Barwick and Nahim Bin Zahur she put the production subsidies "
            "at thirteen to twenty percent of a ship's price. <bookmark mark='c'/> China's share of world "
            "shipbuilding soared. But ship prices fell, so much of the benefit went to the shipowners of the "
            "world, not to China. <bookmark mark='d'/> And the entry subsidies created yards with little to do. "
            "Combined, the policies returned far less than each would have alone. Industrial policy can build an "
            "industry; whether it pays the country that pays for it is a separate question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
