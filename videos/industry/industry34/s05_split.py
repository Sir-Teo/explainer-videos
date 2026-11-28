from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class Split(VoiceoverScene):
    def construct(self):
        card(self, 4, "Why franchise", "Why would a company let someone else run its restaurants?",
             "Chapter four. Why franchise. A company could run all its restaurants itself, as Chipotle does. Most of the big "
             "burger and chicken chains choose not to.", lit=("moat", "dollar"))
        self.margins()
        self.ops()
        self.capital()
        self.chipotle()
        self.why()

    def margins(self):
        Sp = R["split"]
        items = [("franchised restaurants: margin on what franchisees pay", 100 * Sp["fr_margin"], FR, f"{100 * Sp['fr_margin']:.0f}c"),
                 ("restaurants it runs itself: margin on their sales", 100 * Sp["co_margin"], OP, f"{100 * Sp['co_margin']:.0f}c")]
        rows = hbars(items, max_value=100, x0=1.6, top=1.0, row=1.4, length=4.6, size=17, bar_h=0.7)
        hd = tx("McDonald's in 2025: cents kept from each dollar of revenue", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"franchised margins ${Sp['frmargin']:.1f}bn against company-operated margins ${Sp['comargin']:.1f}bn: "
                  "90% of restaurant margin dollars", 16, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("McDonald's, Form 10-K for 2025", size=12)
        beat(self,
             "Look at the two kinds of McDonald's revenue. <bookmark mark='a'/> On every dollar a franchisee pays it, "
             f"McDonald's keeps {100 * Sp['fr_margin']:.0f} cents after the cost of the property it rents to them. "
             f"<bookmark mark='b'/> On every dollar of food it sells in its own restaurants, it keeps {100 * Sp['co_margin']:.0f} "
             f"cents. Franchised margins were {Sp['frmargin']:.1f} billion dollars in 2025, company-operated "
             f"{Sp['comargin']:.1f} billion: nine-tenths of all McDonald's restaurant margin came from restaurants it does not run.",
             base=[rows.axis, hd, note, src], steps=[rows[0], rows[1]])

    def ops(self):
        M = R["split"]["margins"]
        DPZ, MCD = "Domino's", "McDonald's"
        names = ["McDonald's", "Yum! Brands", "Wingstop", "Restaurant Brands", "Domino's", "Chipotle", "Darden", "Starbucks", "Texas Roadhouse"]
        items = [(n, M[n]["op"], GROUP_COL[M[n]["group"]], f"{M[n]['op']:.0f}c") for n in names]
        rows = hbars(items, max_value=50, x0=-0.4, top=2.3, row=0.56, length=6.6, size=16, bar_h=0.34)
        hd = tx("Operating income per dollar of revenue, latest year", 21, WHITE, bold=True).to_edge(UP, buff=0.4)
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 13, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in ("franchisor", "operator", "full")]).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.8)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Across the industry the pattern holds. <bookmark mark='a'/> The franchisors, McDonald's, Yum, Wingstop, "
             f"Restaurant Brands and Domino's, keep {M[DPZ]['op']:.0f} to {M[MCD]['op']:.0f} "
             "cents of each dollar of revenue as operating income. <bookmark mark='b'/> The chains that run their own "
             f"restaurants keep {M['Texas Roadhouse']['op']:.0f} to {M['Chipotle']['op']:.0f}. Part of the difference is "
             "arithmetic: a franchisor's revenue is a slice of its franchisees' sales, with the food and the wages left "
             "out. But part of it is real: the franchisor's money rides on thousands of restaurants it did not pay to build.",
             base=[rows.axis, hd, key, src], steps=[VGroup(*rows[:5]), VGroup(*rows[5:])])

    def why(self):
        g = VGroup(tx("Why franchise, in this series' reading", 22, WHITE, bold=True),
                   tx("capital: the franchisee pays for the kitchen, so the brand can grow faster", 18, OP),
                   tx("effort: an owner watching the till works harder than a salaried manager", 18, GOOD),
                   tx("local knowledge: hiring, landlords and councils are local problems", 18, MASTER),
                   tx("and the franchisor's income is a share of sales, not of profit: steadier, but in conflict", 18, FR)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading, after Lafontaine and Shaw on the economics of franchising", size=12)
        beat(self,
             "Why does it work this way? <bookmark mark='a'/> Capital: franchisees pay to build, so a brand can open "
             "thousands of restaurants without raising the money itself. <bookmark mark='b'/> Effort: an owner who keeps "
             "what is left watches the waste and the rota more closely than a salaried manager would. <bookmark mark='c'/> "
             "Local knowledge: hiring, landlords and planning permission are local problems. <bookmark mark='d'/> And one "
             "conflict built in: the franchisor earns a share of sales, the franchisee earns what is left after costs. A "
             "discount that raises sales and cuts margins pleases one and hurts the other.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])

    def capital(self):
        M = R["split"]["margins"]
        names = ["McDonald's", "Restaurant Brands", "Wendy's", "Yum! Brands", "Wingstop", "Domino's"]
        items = [(n, M[n]["turns"], FR, f"${M[n]['turns']:.2f}") for n in names]
        rows = hbars(items, max_value=3.0, x0=-0.4, top=2.0, row=0.7, length=6.2, size=17, bar_h=0.4)
        hd = tx("Dollars of revenue per dollar of assets, latest year", 21, WHITE, bold=True).to_edge(UP, buff=0.5)
        src = source("Forms 10-K via SEC company facts", size=12)
        tag = estimate_tag("this series' reading: property-heavy franchisors against asset-light ones", size=12).to_edge(DOWN, buff=0.75)
        beat(self,
             "Not every franchisor is light on assets. <bookmark mark='a'/> McDonald's, which owns or leases the land and "
             f"buildings, turns each dollar of assets into only {M[chr(77) + 'cDonald' + chr(39) + 's']['turns']:.2f} dollars of "
             "revenue a year; Restaurant Brands and Wendy's are similar. <bookmark mark='b'/> Yum and Wingstop, about one. "
             f"<bookmark mark='c'/> Domino's, {M[chr(68) + 'omino' + chr(39) + 's']['turns']:.1f}, because its revenue includes the "
             "supplies it sells. In this series' reading, McDonald's high margin is partly a property company's margin, "
             "earned on a great deal of land.",
             base=[rows.axis, hd, src, tag], steps=[VGroup(*rows[:3]), VGroup(rows[3], rows[4]), rows[5]])

    def chipotle(self):
        M = R["split"]["margins"]
        c = stat_cards([(f"{get('cm34.units'):,}", "Chipotle restaurants, all run by the company, end of 2025", OP),
                        ("334", "opened in 2025, 257 of them with a Chipotlane", OP),
                        (f"{get('cm34.goal'):,}", "its long-term goal in the U.S. and Canada", OP)], y=0.5, size=36, span=12.4)
        lane = draw.restaurant(2.4, color=OP).move_to([0, -1.9, 0])
        src = source("Chipotle Mexican Grill, Form 10-K for 2025", size=12)
        beat(self,
             "And the counter-example. <bookmark mark='a'/> Chipotle runs every one of its "
             f"{get('cm34.units'):,} restaurants itself. <bookmark mark='b'/> In 2025 it opened 334 more, most with a "
             "Chipotlane, a drive-through window for orders placed on the app, <bookmark mark='c'/> on the way to a goal of "
             f"{get('cm34.goal'):,}. It pays for every one from its own cash, and keeps every restaurant's whole margin. A chain "
             "whose restaurants earn as much as Chipotle's, about a quarter of sales, can afford to; most cannot, and those "
             "that franchise trade some of the margin for someone else's capital.",
             base=[lane, src], steps=[c[0], c[1], c[2]])
