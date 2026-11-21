from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403


class Paris(VoiceoverScene):
    def construct(self):
        card(self, 14, r"Who feeds Paris now, \ and the Queen's question", r"What can the series answer to the "
             r"two questions it began with?", "Chapter fourteen. Who feeds Paris now, and the Queen's question.",
             lit={1845: "Bastiat", 2009: "the British Academy"}, scale=("world",), horizon=("a century",))
        self.paris()
        self.queen()

    def paris(self):
        cards = point_cards([
            (r"prices", r"the signal and the incentive: \ every farmer, \ shipper and baker responds to the same "
             r"numbers \ (Parts 1--9)", DATA),
            (r"firms and networks", r"supply chains, \ contracts, \ market power, \ and the shocks that travel "
             r"along them \ (Parts 8--17, 43, 63)", TRUE),
            (r"money, \ banks, \ states", r"payment, \ credit, \ property, \ courts, \ safety rules, \ taxes and "
             r"insurance \ (Parts 25--33, 41, 42, 47)", STATE),
            (r"the world", r"trade that brings food from other continents, \ and the politics that can stop it \ "
             r"(Parts 34--36, 66)", ROW),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"who feeds Paris now?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Bastiat asked who feeds Paris. Sixty-eight parts later, the answer has four layers. <bookmark "
            "mark='a'/> Prices, still: the signal and the incentive that every farmer, shipper and baker responds "
            "to. <bookmark mark='b'/> Firms and networks: supply chains and contracts, with market power and shocks "
            "that travel along them. <bookmark mark='c'/> Money, banks and states: payment, credit, property, "
            "courts, safety rules, taxes and insurance, all of which Bastiat's sleeping Parisians took for granted. "
            "<bookmark mark='d'/> And the world: trade that brings food from other continents, and the politics "
            "that can cut it off. No one plans it, and it is not unplanned: it is designed, rule by rule, and "
            "coordinated by prices."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def queen(self):
        Q = tables.BRITISH_ACADEMY_2009
        hc = history_card(r"November 2008", r"the Queen's question", r"at the London School of Economics, \ about "
                          r"the financial crisis: \ why did nobody notice?", color=E.ACCENT, width=11.6,
                          font_size=22).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the British Academy's answer (2009): \ a failure of the collective imagination of many bright "
                  r"people \\ to understand the risks to the system as a whole", font_size=19, color=GREY_A),
            label(r"the series' answer: \ some did notice \ (Part 33's credit booms); \ the profession lacked the "
                  r"models, \\ the data on leverage, \ and the habit of keeping score", font_size=19, color=TOLL),
            label(r"what has changed: \ banks' balance sheets measured, \ stress tests, \ crises in the models \ "
                  r"(Parts 26, 33, 52)", font_size=19, color=TRUE),
            label(r"what has not: \ the next crisis will come from where the data are thinnest", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(hc, DOWN, buff=0.5)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        tag = published_tag(tex_safe(Q.tag), corner=DL, font_size=12)
        with self.voiceover(
            "The other question this series kept returning to was the Queen's. <bookmark mark='a'/> In November "
            "2008, opening a building at the London School of Economics, she asked why nobody had seen the crisis "
            "coming. <bookmark mark='b'/> The British Academy's economists wrote back the next summer: a failure of "
            "the collective imagination of many bright people to understand the risks to the system as a whole. "
            "<bookmark mark='c'/> The series' answer is a little sharper. Some did notice: Part thirty-three showed "
            "that credit booms predict crises. What the profession lacked were models with banks in them, data on "
            "leverage, and the habit of keeping score. <bookmark mark='d'/> Much of that has changed: balance sheets "
            "are measured, banks are stress-tested, crises are in the models. <bookmark mark='e'/> What has not "
            "changed is that the next crisis will start where the data are thinnest."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            for mk, r_ in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
