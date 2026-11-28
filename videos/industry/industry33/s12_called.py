from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "Did the online marketplace replace the distributor, and will the trading house hit its forecast?",
             "Chapter ten. Called it? A dot-com prospectus that promised to cut out the distributors, scored against what "
             "followed; and our own call on a trading house.", lit=("change",))
        self.chemdex()
        self.ours()
        self.watch()

    def chemdex(self):
        C = R["called"]
        q1 = quote(["'The life sciences research products industry is particularly well suited for business-to-business",
                    "e-commerce because of its high degree of fragmentation and because of the inefficiencies inherent in its",
                    "traditional paper-based purchasing process.'"], "Chemdex, prospectus, July 1999", size=17).move_to([0, 2.1, 0])
        q2 = quote(["'Our gross margins on sales of life sciences research products are small relative to the margins earned",
                    "by traditional distributors.'"], "the same prospectus", size=17).move_to([0, 0.5, 0])
        q3 = quote(["'In December 2000 the Board of Directors concluded that the Chemdex Marketplace would be discontinued ...",
                    "revenue and gross margin growth below expectations'"], "Ventro (formerly Chemdex), Form 10-K for 2000", size=17).move_to([0, -1.1, 0])
        verdict = tx(f"scored: closure decided within eighteen months of the listing; a ${C['loss']:.1f}m loss in 2000", 19, BAD, bold=True).to_edge(DOWN, buff=0.75)
        src = source("Chemdex, Form 424B4 (1999); Ventro, Form 10-K for 2000", size=12)
        beat(self,
             "First, a company's own forecast. <bookmark mark='a'/> In July 1999 Chemdex listed its shares, promising to sell "
             "laboratory supplies online and cut through a fragmented, paper-based trade. <bookmark mark='b'/> It admitted "
             "its margins were small beside those of the traditional distributors, and counted on volume to fix that. "
             f"In the three months to June 1999 its revenue was {C['q2rev']:.1f} million dollars. <bookmark mark='c'/> In "
             "December 2000 the board, now of a company renamed Ventro, decided to close the marketplace, because revenue "
             "and margins had grown more slowly than expected and it needed more cash. <bookmark mark='d'/> The distributors "
             "it meant to replace kept their trucks and their customers. A website could take the order; it could not hold "
             "the stock or make the delivery for less.",
             base=[src], steps=[q1, q2, q3, verdict])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 28 November 2026", 20, TRADE, bold=True),
                       tx(f"Mitsui & Co. will report profit attributable to owners of at least ¥{C['fc']:,.0f}bn", 22, WHITE, bold=True),
                       tx("for its year to 31 March 2027, meeting its raised forecast.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, TRADE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets([f"for: ¥{C['h1']:.0f}bn in the first half; it needs ¥{C['fc'] - C['h1']:.0f}bn more, less than it earned in the first half",
                       f"for: the forecast was already raised once, from ¥{C['fc_may']:.0f}bn in May",
                       "against: more than half its cash comes from mines and energy; a fall in iron ore, coal or oil prices would cut it"], size=17).move_to([0, -0.8, 0])
        rule = tx(f"scored on Mitsui's results for the year to March 2027 (May 2027): true if ¥{C['fc']:,.0f}bn or more", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             f"Now ours. <bookmark mark='a'/> We say Mitsui will report at least {C['fc']:,.0f} billion yen of profit for its "
             f"year to March 2027, the forecast it raised in November, and give it {100 * C['prob']:.0f} per cent. "
             f"<bookmark mark='b'/> For: it earned {C['h1']:.0f} billion in the first half, so it needs "
             f"{C['fc'] - C['h1']:.0f} billion in the second, less than in the first; and it has already raised the forecast "
             f"once, from {C['fc_may']:.0f} billion. Against: more than half its cash comes from mines and energy, and a fall in "
             "commodity prices over the winter would cut the second half. <bookmark mark='c'/> Mitsui will publish the year's "
             "results in May 2027, and we will score the call then.",
             base=[tag], steps=[claim, why, rule])

    def watch(self):
        g = VGroup(tx("What to watch", 22, WHITE, bold=True),
                   tx("drug prices: costlier medicines raise wholesalers' revenue more than their profit", 18, DRUG),
                   tx("the customers: one pharmacy chain buys about a quarter of what McKesson or Cencora sells", 18, BAD),
                   tx("commodities: the trading houses now rise and fall with iron ore, coal and gas", 18, TRADE)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Three things to watch. <bookmark mark='a'/> Drug prices: expensive new medicines swell a wholesaler's revenue "
             "far more than its profit. <bookmark mark='b'/> The customers: a single pharmacy chain buys about a quarter of "
             "what McKesson or Cencora sells, so a chain that closes stores or switches wholesaler moves the whole company. "
             "<bookmark mark='c'/> And commodities: the trading houses that became owners now share the owners' cycle. "
             "None of these threatens the middleman's basic job; each changes how much it keeps for doing it.",
             base=[tag], steps=[g[:2], g[2], g[3]])
