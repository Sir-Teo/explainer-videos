from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ regulators, \ markets and charges", r"Where are the prices, \ caps and bargains "
             r"of this part \ in use today?", "Chapter fourteen. In practice: regulators, markets and charges.",
             lit={1959: r"Coase on spectrum", 1975: r"Singapore's road charge", 1991: r"Sweden's carbon tax",
                  2005: r"the EU's carbon market"}, scale=("city", "nation", "world"), horizon=("a decade",))
        self.toolkit()
        self.places()

    def toolkit(self):
        rows = point_cards([
            (r"Pigou's prices", r"carbon taxes: \ Sweden 1991, \\ British Columbia 2008", GOOD),
            (r"Dales's permits", r"sulphur 1995; \ the EU's \\ carbon market 2005", SOCIAL),
            (r"Coase's rights", r"fishing quotas you can sell; \\ spectrum licences", DEMAND),
            (r"Vickrey's tolls", r"Singapore, \ London, \\ Stockholm, \ New York", ROAD),
            (r"Ostrom's rules", r"water boards, \ forest \\ and grazing councils", FISH),
            (r"plain rules", r"standards for engines, \\ fuels and chimneys", GREY_A),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.2)
        head = label(r"the toolkit, \ in use", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Every remedy in this part is in use somewhere. <bookmark mark='a'/> Pigou's prices: carbon taxes, in "
            "Sweden since 1991 and British Columbia since 2008. Dales's permits: the sulphur market from 1995, and the "
            "European Union's carbon market from 2005, now one of the largest of its kind. Coase's property rights: fishing "
            "quotas that can be bought and sold, and licences to use the radio spectrum, which Coase proposed auctioning "
            "in 1959, decades before governments did. Vickrey's tolls: Singapore from 1975, London, "
            "Stockholm, and New York since 2025. Ostrom's rules: water boards, forest and grazing councils run by "
            "their users. <bookmark mark='b'/> And plain rules, standards for engines, fuels and chimneys, which are "
            "still the commonest tool of all, and often the costliest way to get a given cut."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(rows.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards[1:5]], lag_ratio=0.8), run_time=9)
            vo.wait_until("b")
            self.play(FadeIn(rows.cards[5], shift=UP * 0.1))
        self.clear_scene()

    def places(self):
        rows = VGroup(
            label(r"a regulator's question: \ what is a tonne of this pollutant worth not emitting?", font_size=24,
                  color=E.ACCENT),
            label(r"cost--benefit analysis: \ value the damage, \ including the value of lives saved", font_size=23),
            label(r"designing a market: \ the cap, \ how permits are handed out, \ banking, \ a price floor and "
                  r"ceiling", font_size=23, color=SOCIAL),
            label(r"designing a charge: \ where the cordon runs, \ how it varies by hour, \ who is exempt, \ where "
                  r"the money goes", font_size=23, color=ROAD),
            label(r"and politics: \ a tax is visible, \ a rule's cost is hidden in prices", font_size=23,
                  color=GREY_A),
            label(r"part fifty-eight scores a bill; \ part forty-eight prices carbon; \ part sixteen auctions spectrum",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Coase, JLE 2 (1959); \ Costello, Gaines and Lynham, Science 321 (2008)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "What does an economist do in this work? <bookmark mark='a'/> The regulator's first question is what a "
            "tonne of a pollutant is worth not emitting. <bookmark mark='b'/> Cost-benefit analysis answers it by "
            "valuing the damage, including the value of the lives that cleaner air saves, which chapter fifteen "
            "measures. <bookmark mark='c'/> Designing a market means choosing the cap, how permits are handed out, "
            "whether they can be banked, and whether the price has a floor and a ceiling. Fisheries that moved to "
            "tradable catch shares were, by one large study, much less likely to collapse. "
            "<bookmark mark='d'/> Designing a charge means choosing where the cordon runs, how the price varies by "
            "the hour, who is exempt, and where the money goes. <bookmark mark='e'/> And there is politics: a tax "
            "is visible on every bill, while a rule's cost hides in prices, which is one reason rules remain popular "
            "with politicians. <bookmark mark='f'/> Part fifty-eight scores a bill, part forty-eight prices carbon, "
            "and part sixteen auctions the spectrum."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
