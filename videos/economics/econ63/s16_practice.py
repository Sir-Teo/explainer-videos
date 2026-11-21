from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ supply-chain and systemic risk", r"Who maps these networks, \ and what do "
             r"they do with the map?", "Chapter fourteen. In practice: supply-chain and systemic risk.",
             scale=("firm", "nation"), horizon=("a year",))
        self.jobs()
        self.cautions()

    def jobs(self):
        cards = point_cards([
            (r"supply-chain risk", r"mapping suppliers beyond the first tier; \ a second source or a stock of the "
             r"specific parts, \ chapter six's lesson", SEED),
            (r"systemic risk", r"central banks and supervisors: \ who owes whom, \ stress tests that let losses "
             r"travel, \ the clearing houses of chapter eight", BANK),
            (r"seeding and targeting", r"public-health campaigns, \ marketing and microfinance: \ whom to tell "
             r"first, \ chapter ten", PEOPLE),
            (r"planning and policy", r"input-output tables for disasters, \ sanctions and choke points: \ which "
             r"input nobody can replace", LINK),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"where network economics is used", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Where is this used? <bookmark mark='a'/> In supply-chain risk. After 2011, manufacturers that had "
            "known only their direct suppliers began mapping the suppliers behind them, and for specific parts "
            "they keep a second source or a stock, which is chapter six's lesson. <bookmark mark='b'/> In systemic "
            "risk: central banks and supervisors collect who owes whom, run stress tests in which losses travel "
            "between banks, and oversee the clearing houses at the centre of the derivatives network. <bookmark "
            "mark='c'/> In seeding: public-health campaigns, marketing and microfinance choose whom to tell first. "
            "<bookmark mark='d'/> And in policy: governments use input-output tables to plan for disasters, and, "
            "as Part sixty-six will show, to find the inputs their rivals cannot replace."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def cautions(self):
        head = label(r"three cautions from this part", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"1. \ Sales first", font_size=26, color=GDP),
                   label(r"to a first approximation a sector matters by its sales, \ however central it looks: \ "
                         r"Hulten before the picture", font_size=19, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"2. \ Then ask what cannot be replaced", font_size=26, color=SHOCK),
                   label(r"large shocks to essential inputs cost more than their sales, \ and more the longer the "
                         r"chain cannot adjust", font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.1),
            VGroup(label(r"3. \ Linked is not contagious", font_size=26, color=PEOPLE),
                   label(r"friends and trading partners resemble each other for many reasons: \ contagion needs a "
                         r"design, \ as in chapters six, \ nine and eleven", font_size=19, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "And three cautions this part teaches. <bookmark mark='a'/> Sales first: to a first approximation, a "
            "sector matters by its sales, however central it looks in a picture of the network. <bookmark "
            "mark='b'/> Then ask what cannot be replaced: a large shock to an essential input costs more than its "
            "sales, and more the longer the chain cannot adjust. <bookmark mark='c'/> And linked is not "
            "contagious. Friends, banks and trading partners resemble each other for many reasons; showing that "
            "something travels along the links takes a design: a disaster, a randomized suggestion, a natural "
            "experiment."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()
