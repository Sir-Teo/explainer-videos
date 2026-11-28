from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Night(VoiceoverScene):
    def construct(self):
        card(self, 2, "The night that perishes", "What does a hotel actually sell, and what does an empty room cost?",
             "Chapter two. The night that perishes. A hotel sells something odd: the use of a room for one night, which "
             "exists only tonight.", lit=("unit", "make"))
        self.revpar()
        self.perish()
        self.mix()
        self.costs()
        self.flow()

    def revpar(self):
        N = R["night"]
        rows = [("", "occupancy", "x", "average rate", "=", "RevPAR"),
                ("Marriott, worldwide", f"{N['mar'][0]:.1f}%", "x", f"${N['mar'][1]:.2f}", "=", f"${N['mar'][2]:.2f}"),
                ("Hilton, system-wide", f"{N['hlt'][0]:.1f}%", "x", f"${N['hlt'][1]:.2f}", "=", f"${N['hlt'][2]:.2f}"),
                ("Host's luxury hotels", "", "", "", "", f"${N['hst_revpar']:.2f}")]
        t = table(rows, col_x=[-4.6, -1.2, 0.1, 1.5, 2.9, 4.3], top=1.4, row_h=0.85, size=19,
                  colors=[None] + [[WHITE, BRAND, GREY_B, BRAND, GREY_B, GOOD]] * 3)
        hd = tx("revenue per available room, 2025", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Marriott International, Hilton and Host Hotels & Resorts, Forms 10-K for 2025 (comparable hotels)", size=12)
        beat(self,
             "The industry measures itself with one number. <bookmark mark='a'/> Occupancy is the share of rooms sold; the "
             "average daily rate is what each sold room fetched; multiply them and you get revenue per available room, or "
             f"RevPAR. <bookmark mark='b'/> Across Marriott's hotels in 2025, {N['mar'][0]:.1f} per cent of rooms were sold at "
             f"an average of {N['mar'][1]:.0f} dollars: {N['mar'][2]:.2f} dollars for every room, sold or not. "
             f"<bookmark mark='c'/> Hilton's hotels were fuller and cheaper: {N['hlt'][0]:.1f} per cent at {N['hlt'][1]:.0f} "
             f"dollars. <bookmark mark='d'/> Host's big luxury hotels made {N['hst_revpar']:.0f} dollars a room.",
             base=[hd, src], steps=[t[0], t[1], t[2], t[3]])

    def perish(self):
        U = R["run"]
        F = U["flat"]
        MS = F["months"]
        occ_f = {i + 0.5: 100 * x["occupancy"] for i, x in enumerate(MS)}
        ch = line_chart({"rooms sold, one rate all year": (occ_f, OWNER)},
                        x=(0, 12), y=(0, 100), xticks=[0.5, 3.5, 6.5, 9.5, 11.5], yticks=[0, 25, 50, 75, 100],
                        xfmt=lambda v: ["Jan", "Apr", "Jul", "Oct", "Dec"][[0.5, 3.5, 6.5, 9.5, 11.5].index(v)], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="share of the hotel's rooms sold, by month", width=8.6, height=4.2, center=(-1.0, -0.4))
        jul, dec = MS[6], MS[11]
        mk = VGroup(marker(ch.ax, 6.5, 100 * jul["occupancy"], f"July: {100 * jul['occupancy']:.0f}% sold; guests turned away on "
                           f"{100 * jul['turned'] / jul['available']:.0f}% of the month's rooms", BAD, side=UP),
                    marker(ch.ax, 11.5, 100 * dec["occupancy"], f"December: {100 * (1 - dec['occupancy']):.0f}% of rooms empty", GREY_A, side=DOWN))
        tag = estimate_tag("the Works: one rate of $180; nights scatter around each month's demand", size=12)
        beat(self,
             "And it perishes. <bookmark mark='a'/> At one rate all year, the Works' hotel is about half full in the depths of "
             f"winter and {100 * jul['occupancy']:.0f} per cent full in July. <bookmark mark='b'/> On July's busiest nights it "
             "sells out and turns guests away: enough of them to fill "
             f"{100 * jul['turned'] / jul['available']:.0f} per cent of the month's rooms. <bookmark mark='c'/> In December "
             f"{100 * (1 - dec['occupancy']):.0f} per cent of the rooms stay dark. An empty room tonight cannot be sold "
             "tomorrow, and a guest turned away tonight books somewhere else. That is why hotels change their prices daily, and "
             "why the industry counts its sales per available room rather than per room sold.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["rooms sold, one rate all year"], ch.labels["rooms sold, one rate all year"]),
                                          mk[0], mk[1]])

    def mix(self):
        N = R["night"]
        parts = [(k, v / 100, c) for (k, v), c in zip(N["mix"].items(), (OWNER, CASINO, FIXC))]
        bar = viz.bar_split(parts, 1.0, width=11.0, height=0.9).move_to([0, 0.9, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}%", 22, c, bold=True), tx(n_, 14, GREY_A)).arrange(DOWN, buff=0.05).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n_, v, c) in enumerate(parts)])
        hd = tx("Host Hotels' revenue in 2025, by what it sold", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"total revenue per available room: ${N['hst_trevpar']:.0f}, against ${N['hst_revpar']:.0f} from rooms alone", 17, GREY_B).move_to([0, -1.9, 0])
        src = source("Host Hotels & Resorts, Form 10-K for 2025", size=12)
        beat(self,
             "Rooms are not the whole of a big hotel. <bookmark mark='a'/> At Host's hotels, rooms brought in "
             f"{N['mix']['rooms']} per cent of revenue in 2025. <bookmark mark='b'/> Food and drink, mostly banquets and "
             f"conferences, {N['mix']['food and drink']} per cent. <bookmark mark='c'/> Parking, spas, golf and the rest, "
             f"{N['mix']['other']}. <bookmark mark='d'/> So each available room brought in {N['hst_trevpar']:.0f} dollars a "
             f"night in all, against {N['hst_revpar']:.0f} from the room itself. A resort with a ballroom is several businesses "
             "under one roof.",
             base=[hd, src], steps=[VGroup(bar[0], labs[0]), VGroup(bar[1], labs[1]), VGroup(bar[2], labs[2]), note])

    def costs(self):
        N = R["night"]
        cols = (STAFF, CASINO, FIXC, BRAND, OWNER, ALL)
        items = [(k, v, c, f"{v}%") for (k, v), c in zip(N["costs"].items(), cols)]
        rows = hbars(items, max_value=32, x0=0.8, top=2.0, row=0.68, length=5.4, size=16, bar_h=0.42)
        hd = tx("Host Hotels' costs in 2025, share of the total", 21, WHITE, bold=True).to_edge(UP, buff=0.5)
        note = tx(f"wages and benefits: {N['wages']}% of the rooms, kitchen and support costs; hotel profit margin {N['margin']}%",
                  16, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("Host Hotels & Resorts, Form 10-K for 2025", size=12)
        beat(self,
             "And the costs. <bookmark mark='a'/> Running the rooms took 18 per cent of Host's costs, <bookmark mark='b'/> the "
             "kitchens and banquets 24, <bookmark mark='c'/> and the support departments, sales, repairs and power, 29. "
             f"<bookmark mark='d'/> Management fees to the hotel companies, {N['costs']['management fees']} per cent. "
             f"<bookmark mark='e'/> Property tax, ground rent and insurance, {N['costs']['property tax, rent, insurance']}. "
             f"<bookmark mark='f'/> And depreciation of the buildings, {N['costs']['depreciation']}. <bookmark mark='g'/> Most "
             f"of it is people: wages and benefits are {N['wages']} per cent of the operating departments' costs. A hotel needs "
             "a night manager, a front desk and engineers whether it is full or half empty.",
             base=[rows.axis, hd, src], steps=list(rows) + [note])

    def flow(self):
        F = R["run"]["flow"]
        items = [("5% more revenue from a higher rate", 100 * F["from_rate"], GOOD, f"{100 * F['from_rate']:.0f}c of each dollar"),
                 ("5% more revenue from more rooms sold", 100 * F["from_rooms"], OWNER, f"{100 * F['from_rooms']:.0f}c of each dollar")]
        rows = hbars(items, max_value=100, x0=0.6, top=1.0, row=1.3, length=4.8, size=18, bar_h=0.65)
        hd = tx("how much of extra revenue reaches the hotel's profit", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        tag = estimate_tag("the Works: a higher rate with no guests lost, against more guests at the same rate", size=12)
        beat(self,
             "Hoteliers call it flow-through: how much of an extra dollar of revenue reaches profit. <bookmark mark='a'/> In "
             f"the Works, if revenue rises five per cent because the rate is higher, {100 * F['from_rate']:.0f} cents of each "
             "extra dollar is profit; only the brand's and agents' shares come off. <bookmark mark='b'/> If it rises because "
             f"more rooms are sold, {100 * F['from_rooms']:.0f} cents, because each extra guest needs a cleaned room, fresh "
             "linen and supplies. That is why the industry watches the average rate so closely: rate is almost pure profit, "
             "occupancy is not.",
             base=[rows.axis, hd, tag], steps=[rows[0], rows[1]])
