from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Cruise(VoiceoverScene):
    def construct(self):
        card(self, 7, "A hotel that moves", "What happens when the hotel owns the ships, the staff and the island?",
             "Chapter seven. A hotel that moves. A cruise line is the one travel business that still owns everything: the "
             "ships, the crew's jobs, the restaurants on board, even private islands.", lit=("make", "dollar"))
        self.ship()
        self.dollar()
        self.costs()
        self.cash()
        self.pandemic()
        self.share()

    def ship(self):
        Cr = R["cruise"]
        s = draw.cruise_ship(6.0, decks=6).move_to([0, 1.2, 0])
        draw.light(s.windows, 0.95)
        c = stat_cards([(f"{Cr['pax']:.1f}m", "passengers carried, year to November 2025", CRUISE),
                        (f"{Cr['occ']}%", "occupancy: more guests than two to a cabin", GOOD),
                        (f"{Cr['crew'] / 1e3:.0f}k", "crew on board, on average", STAFF)], y=-1.8, size=34, span=12)
        src = source("Carnival Corporation & plc, Form 10-K for 2025", size=12)
        beat(self,
             "Carnival is the largest cruise company, owner of Carnival Cruise Line, Princess, Holland America, AIDA, Costa "
             f"and P&O Cruises. <bookmark mark='a'/> In its year to November 2025 it carried {Cr['pax']:.1f} million "
             f"passengers. <bookmark mark='b'/> Its occupancy was {Cr['occ']} per cent: the industry counts two people to a "
             "cabin, and families squeeze in a third and a fourth. <bookmark mark='c'/> And on an average day "
             f"{Cr['crew'] / 1e3:.0f} thousand crew were at work on its ships, sourced from about 150 countries.",
             base=[s, src], steps=list(c))

    def dollar(self):
        Cr = R["cruise"]
        items = [("tickets", Cr["ticket"], CRUISE, bn(Cr["ticket"])), ("on board: drinks, excursions, casino, spa, shops", Cr["onboard"], BRAND, bn(Cr["onboard"]))]
        rows = hbars(items, max_value=20, x0=1.2, top=1.0, row=1.3, length=5.0, size=17, bar_h=0.65)
        hd = tx(f"Carnival's revenue, year to November 2025: {bn(Cr['rev'])}", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"Royal Caribbean: tickets {bn(Cr['rcl']['ticket'])}, on board {bn(Cr['rcl']['onboard'])}", 17, GREY_B).to_edge(DOWN, buff=0.8)
        src = source("Carnival Corporation & plc and Royal Caribbean Group, Forms 10-K for 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> Tickets brought Carnival {Cr['ticket']:.1f} billion dollars. <bookmark mark='b'/> What "
             f"passengers spent once aboard, on drinks, shore excursions, the casino, the spa and the shops, brought "
             f"{Cr['onboard']:.1f} billion: {100 * Cr['onboard'] / Cr['rev']:.0f} cents of every dollar. A cruise is priced like "
             "a cheap flight and earns like a resort: the fare fills the cabin, the spending on board pays the bills. "
             "<bookmark mark='c'/> Royal Caribbean's split is much the same.",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], note])

    def costs(self):
        Cr = R["cruise"]
        cols = (AGENT, BRAND, STAFF, BAD, CASINO, FIXC, OWNER, ALL)
        parts = [(k, v / Cr["rev"], c) for (k, v), c in zip(Cr["costs"].items(), cols)]
        parts.append(("operating income", Cr["op"] / Cr["rev"], GOOD))
        bar = viz.bar_split(parts, 1.0, width=12.6, height=0.9).move_to([0, 0.8, 0])
        labs = VGroup()
        for i, (n_, v, c) in enumerate(parts):
            lab = VGroup(tx(f"{100 * v:.0f}c", 17, c, bold=True), tx(n_, 10, GREY_A)).arrange(DOWN, buff=0.05)
            lab.next_to(bar[i], DOWN if i % 2 == 0 else UP, buff=0.18)
            labs.add(lab)
        hd = tx("a dollar of Carnival's revenue, 2025", 20, WHITE, bold=True).to_edge(UP, buff=0.6)
        src = source("Carnival Corporation & plc, Form 10-K for 2025", size=12)
        steps = [VGroup(*[VGroup(bar[i], labs[i]) for i in range(0, 2)]), VGroup(*[VGroup(bar[i], labs[i]) for i in range(2, 5)]),
                 VGroup(*[VGroup(bar[i], labs[i]) for i in range(5, 8)]), VGroup(bar[8], labs[8])]
        beat(self,
             "Where the dollar goes. <bookmark mark='a'/> Travel agents' commissions, flights and port charges take "
             f"{100 * parts[0][1]:.0f} cents, and the cost of what is sold on board {100 * parts[1][1]:.0f}. "
             f"<bookmark mark='b'/> The crew's pay {100 * parts[2][1]:.0f} cents, fuel {100 * parts[3][1]:.0f}, food "
             f"{100 * parts[4][1]:.0f}. <bookmark mark='c'/> Maintenance, insurance and the rest of running the ships "
             f"{100 * parts[5][1]:.0f}, selling and the head office {100 * parts[6][1]:.0f}, and the wear on the ships "
             f"themselves {100 * parts[7][1]:.0f}. <bookmark mark='d'/> About {100 * parts[8][1]:.0f} cents is operating income.",
             base=[hd, src], steps=steps)

    def cash(self):
        Cr = R["cruise"]
        c = stat_cards([(bn(Cr["deposits"]), "customer deposits: fares paid before sailing", GOOD),
                        (bn(Cr["debt"]), "debt, mostly for ships", BAD),
                        (bn(Cr["interest"], 2), "interest a year", BAD)], y=1.3, size=36, span=12)
        boat = draw.cruise_ship(4.4, decks=5, seed=8).move_to([0, -1.7, 0])
        draw.light(boat.windows, 0.9)
        src = source("Carnival Corporation & plc, Form 10-K for 2025 (30 November 2025)", size=12)
        beat(self,
             "Two numbers on the balance sheet tell how the business is financed. <bookmark mark='a'/> Passengers pay months "
             f"before they sail: at the end of November 2025 Carnival held {Cr['deposits']:.1f} billion dollars of their "
             "money. <bookmark mark='b'/> And the ships are bought with debt: "
             f"{Cr['debt']:.1f} billion dollars of it, <bookmark mark='c'/> costing {Cr['interest']:.2f} billion a year in "
             "interest, nearly a third of operating income. The guests lend the working capital; the banks lend the ships.",
             base=[boat, src], steps=list(c))

    def pandemic(self):
        Hh = R["cruise"]["ccl_hist"]
        rev = {y: v[0] for y, v in Hh.items()}
        ni = {y: v[1] for y, v in Hh.items()}
        ch = line_chart({"revenue": (rev, CRUISE), "net income": (ni, GOOD)}, x=(2015, 2025), y=(-11, 28),
                        xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[-10, 0, 10, 20], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="Carnival, years to November, $bn", width=8.6, height=4.3, center=(-1.0, -0.45))
        mk = marker(ch.ax, 2020, ni[2020], f"2020: a loss of {bn(-ni[2020])}", BAD, side=RIGHT)
        mk[1].shift(UP * 0.3)
        src = source("Carnival, Forms 10-K, via SEC company facts; Form 10-K for 2020", size=12)
        beat(self,
             "And the fixed costs make it fragile. <bookmark mark='a'/> Carnival's revenue was about "
             f"{rev[2019]:.0f} billion dollars in 2019. In mid-March 2020 it paused its cruises; by January 2021 not one of its "
             f"ships was carrying guests. <bookmark mark='b'/> It lost {-ni[2020]:.1f} billion dollars in 2020 and lost money "
             "every year through 2023, because a ship at anchor still needs a crew, insurance and interest. By 2025 revenue "
             "was a record, and Carnival says it has cut its debt by more than ten billion dollars since the peak in January "
             "2023.",
             base=[ch.frame, src], steps=[VGroup(*ch.lines.values(), *ch.labels.values()), mk])

    def share(self):
        Cr = R["cruise"]
        sh = Cr["berths"] / Cr["industry"]
        parts = [("Carnival", sh, CRUISE), ("Royal Caribbean, Norwegian and MSC", 0.80 - sh, OWNER), ("everyone else", 0.20, FIXC)]
        bar = viz.bar_split(parts, 1.0, width=11.0, height=0.9).move_to([0, 0.6, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}%", 22, c, bold=True), tx(n_, 14, GREY_A)).arrange(DOWN, buff=0.05).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n_, v, c) in enumerate(parts)])
        hd = tx(f"the world's cruise berths, end of 2025: {Cr['industry']:,}", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Carnival, Form 10-K for 2025, citing Cruise Industry News (the four together: 'approximately 80%')", size=12)
        beat(self,
             f"<bookmark mark='a'/> Carnival's ships held {Cr['berths']:,} of the world's {Cr['industry']:,} cruise berths at "
             f"the end of 2025, about {100 * sh:.0f} per cent. <bookmark mark='b'/> With Royal Caribbean, Norwegian and MSC, "
             "the four companies had about eighty per cent. <bookmark mark='c'/> Carnival has seven more ships on order, the "
             "last due in 2033: a cruise line grows a ship at a time, years ahead, which keeps the industry to a few large "
             "companies.",
             base=[hd, src], steps=[VGroup(bar[0], labs[0]), VGroup(bar[1], labs[1]), VGroup(bar[2], labs[2])])
