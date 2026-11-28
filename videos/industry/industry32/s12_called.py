from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "Did the fastest-growing platform keep growing, and how fast will online shopping grow now?",
             "Chapter ten. Called it? A marketplace's own description of itself in 2020, scored against what followed, and "
             "our own call on the share of shopping done online.", lit=("change",))
        self.wish()
        self.ours()
        self.watch()

    def wish(self):
        C = R["called"]
        W = C["wish"]
        q = quote(["'We have become one of the largest and fastest growing global ecommerce platforms, connecting",
                   "more than 100 million monthly active users ... in over 100 countries to over 500,000 merchants'"],
                  "ContextLogic (Wish), prospectus, 20 November 2020", size=17).move_to([0, 2.3, 0])
        items = [(str(y), W[y][0], MARKET, f"${W[y][0]:.2f}bn") for y in sorted(W)]
        cols = vbars(items, base_y=-2.3, height=3.0, width=1.0, gap=0.5, size=15, max_value=2.8)
        mk_ = VGroup(*[Rectangle(width=0.45, height=max(3.0 * W[y][1] / 2.8, 0.03), stroke_width=0, fill_color=ADS, fill_opacity=0.9)
                       .move_to(cols[i][0].get_bottom() + UP * max(3.0 * W[y][1] / 2.8, 0.03) / 2 + RIGHT * 0.32)
                       for i, y in enumerate(sorted(W))])
        lk = tx("gold: revenue; pink: sales and marketing", 14, GREY_A).move_to([4.6, -0.2, 0])
        verdict = tx(f"scored: users down {C['drop']:.0f}% in 2022 when it cut ads; sold for ${C['sale']:.0f}m in 2024", 19, BAD, bold=True).to_edge(DOWN, buff=0.7)
        src = source("ContextLogic, Form S-1 (2020) and Forms 10-K for 2020-2024", size=12)
        beat(self,
             "First, a company's own words. <bookmark mark='a'/> In November 2020 Wish, a mobile marketplace for "
             "affordable goods whose merchants were mostly in China, told investors it was one of the largest and fastest-growing e-commerce platforms in "
             "the world, with more than a hundred million monthly users. <bookmark mark='b'/> Its revenue had reached "
             f"{W[2020][0]:.1f} billion dollars. But it was buying those users: its sales and marketing cost "
             f"{C['sm']:.0f} per cent of its revenue in 2019. <bookmark mark='c'/> When it cut its advertising, its monthly "
             f"users fell {C['drop']:.0f} per cent in a year. <bookmark mark='d'/> Revenue fell to {W[2023][0]:.2f} billion "
             f"in 2023, and in 2024 it sold its business for {C['sale']:.0f} million dollars. Large, yes; but the size was "
             "rented, and the rent stopped.",
             base=[src], steps=[q, VGroup(*[VGroup(c[0], c[1], c[2]) for c in cols[:3]], lk, mk_[:3]),
                                VGroup(*[VGroup(c[0], c[1], c[2]) for c in cols[3:5]], mk_[3:5]), VGroup(cols[5], mk_[5], verdict)])

    def ours(self):
        C = R["called"]
        E = C["share"]
        last = max(E)
        prev = near(E, last - 1)
        claim = VGroup(tx("Our call, 28 November 2026", 20, MARKET, bold=True),
                       tx(f"The Census Bureau's first estimate of e-commerce's share of", 22, WHITE, bold=True),
                       tx(f"American retail sales for the fourth quarter of 2027 will be {C['line']:.1f}% or more.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, MARKET, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets([f"for: {E[prev]:.1f}% a year before the latest quarter, {E[last]:.1f}% now; the climb resumed after 2022",
                       f"against: it needs {C['line'] - E[last]:.1f} points in five quarters, a little faster than the last year's {E[last] - E[prev]:.1f}",
                       "against: dearer imports after the end of the de minimis rule, and a slower economy"], size=17).move_to([0, -0.8, 0])
        rule = tx(f"scored on the Census Bureau's first release for 2027 Q4 (FRED: ECOMPCTSA); true if {C['line']:.1f}% or more", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             f"Now ours. <bookmark mark='a'/> We say the Census Bureau's first estimate of the online share of American "
             f"retail, for the last quarter of 2027, will be {C['line']:.0f} per cent or more, and give it "
             f"{100 * C['prob']:.0f} per cent: a little worse than even. <bookmark mark='b'/> For: the share has climbed "
             f"steadily since 2022, from {E[prev]:.1f} to {E[last]:.1f} per cent in the last year alone. Against: it needs "
             f"another {C['line'] - E[last]:.1f} points in five quarters, slightly faster than that, and imports have got "
             "dearer. <bookmark mark='c'/> The Census Bureau will publish the number in February 2028, and we will score "
             "the call then, whichever way it goes.",
             base=[tag], steps=[claim, why, rule])

    def watch(self):
        g = VGroup(tx("What to watch", 22, WHITE, bold=True),
                   tx("the courts: the FTC's monopoly case and the new one over ad auctions", 18, ADS),
                   tx("China: whether Temu and its rivals rebuild around warehouses in the countries they sell to", 18, MARKET),
                   tx("AI: eBay warns that AI may change how consumers search for products", 18, CLOUD)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading; eBay, Form 10-K for 2025", size=12)
        beat(self,
             "Three things to watch. <bookmark mark='a'/> The courts, where the rules of the biggest marketplace and its ad "
             "auctions are being tested. <bookmark mark='b'/> China's platforms, now that cheap parcels pay duty. "
             "<bookmark mark='c'/> And artificial intelligence: eBay's annual report warns that AI may change how people "
             "search for products. If a shopping assistant chooses for the buyer, the results page, and the ads on it, "
             "matter less, and the toll moves to whoever owns the assistant.",
             base=[tag], steps=[g[:2], g[2], g[3]])
