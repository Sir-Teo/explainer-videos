from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: fill a hotel for a year", "You own one hotel. Every night, two hundred rooms either sell or vanish.",
             "Chapter one. Run it. You own a hotel with two hundred rooms and a famous name over the door. Every night you "
             "choose a price, and every night the rooms you do not sell are gone for ever.", lit=("unit", "dollar"))
        self.hotel()
        self.one_rate()
        self.months()
        self.dollar()
        self.owner()
        self.brand()
        self.lesson()

    def hotel(self):
        U = R["run"]
        H = U["hotel"]
        h = draw.hotel(2.4, floors=12, seed=4).move_to([-3.6, 0.2, 0])
        draw.light(h.windows, U["at180"]["occupancy"])
        c = VGroup(*[VGroup(tx(a, 30, col, bold=True), tx(b_, 14, GREY_A)).arrange(DOWN, buff=0.06) for a, b_, col in (
            (f"{H['rooms']}", "rooms", WHITE),
            (f"${H['invest'] * H['rooms'] / 1e6:.0f}m", f"to build, ${H['invest'] / 1e3:.0f}k a room; {100 * H['debt']:.0f}% borrowed", OWNER),
            (f"{100 * (H['royalty'] + H['programme']):.0f}%", "of room revenue to the brand", BRAND),
            (f"{100 * H['commission']:.0f}%", "commission on rooms sold by online agents", AGENT))]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        c.move_to([2.6, 0.2, 0])
        tag = estimate_tag("the Works: a 200-room branded hotel; demand, costs and fees are this series' assumptions "
                           "(explainer/industry/works/hotel.py)", size=12)
        beat(self,
             f"Here is your hotel. <bookmark mark='a'/> {H['rooms']} rooms. <bookmark mark='b'/> It cost "
             f"{H['invest'] * H['rooms'] / 1e6:.0f} million dollars to build, {H['invest'] / 1e3:.0f} thousand a room, and you "
             f"borrowed {100 * H['debt']:.0f} per cent of it. <bookmark mark='c'/> A brand lets you use its name, its booking "
             f"system and its loyalty programme for {100 * (H['royalty'] + H['programme']):.0f} per cent of your room revenue. "
             f"<bookmark mark='d'/> And a quarter of your rooms are sold by online agents, who keep {100 * H['commission']:.0f} "
             "per cent of each booking.",
             base=[h, tag], steps=list(c))

    def one_rate(self):
        U = R["run"]
        B = U["by_rate"]
        prof = {r: y["ebitda"] / 1e6 for r, y in B.items()}
        occ = {r: 3.2 * y["occupancy"] for r, y in B.items()}
        ch = line_chart({"profit before interest": (prof, GOOD), "rooms sold (top of chart = 100%)": (occ, OWNER)}, x=(120, 260), y=(0, 3.2),
                        xticks=[120, 150, 180, 210, 240, 260], yticks=[0, 1, 2, 3], xfmt=lambda v: f"${v:.0f}",
                        yfmt=lambda v: f"${v:.0f}m", ylabel="the hotel's year, by the rate it charges every night",
                        width=8.6, height=4.3, center=(-0.9, -0.45), nudge={"rooms sold (top of chart = 100%)": 0.2})
        lo, mid, hi = U["low"], U["flat"], U["high"]
        mk = VGroup(marker(ch.ax, 150, lo["ebitda"] / 1e6, f"$150: {100 * lo['occupancy']:.0f}% full, {m(lo['ebitda'])}", GREY_A, side=DOWN),
                    marker(ch.ax, mid["rates"][0], mid["ebitda"] / 1e6, f"${mid['rates'][0]:.0f}: {100 * mid['occupancy']:.0f}% full, {m(mid['ebitda'])}", GOOD, side=UP),
                    marker(ch.ax, 220, hi["ebitda"] / 1e6, f"$220: {100 * hi['occupancy']:.0f}% full, {m(hi['ebitda'])}", GREY_A, side=DOWN))
        tag = estimate_tag("the Works: one rate for every night of the year; profit after the brand, the agents and running costs", size=12)
        beat(self,
             "First, charge one rate every night of the year. <bookmark mark='a'/> The cheaper the room, the fuller the hotel: "
             f"the blue line. And profit, the green line, rises and then falls. <bookmark mark='b'/> At 150 dollars you are "
             f"{100 * lo['occupancy']:.0f} per cent full but make only {lo['ebitda'] / 1e6:.2f} million, because every extra room "
             f"sold costs cleaning and laundry and earns little. <bookmark mark='c'/> At {mid['rates'][0]:.0f} dollars, "
             f"{100 * mid['occupancy']:.0f} per cent full, you make the most: {mid['ebitda'] / 1e6:.2f} million. "
             f"<bookmark mark='d'/> At 220 you are barely half full, and profit falls again.",
             base=[ch.frame, tag], steps=[VGroup(*ch.lines.values(), *ch.labels.values()), mk[0], mk[1], mk[2]])

    def months(self):
        U = R["run"]
        M, F = U["monthly"], U["flat"]
        xs = list(range(12))
        rates = {i + 0.5: r for i, r in enumerate(M["rates"])}
        flat = {i + 0.5: F["rates"][0] for i in xs}
        ch = line_chart({"a rate for each month": (rates, BRAND), "one rate all year": (flat, GREY_B)}, x=(0, 12), y=(120, 220),
                        xticks=[0.5, 3.5, 6.5, 9.5, 11.5], yticks=[120, 150, 180, 210], xfmt=lambda v: ["Jan", "Apr", "Jul", "Oct", "Dec"][[0.5, 3.5, 6.5, 9.5, 11.5].index(v)],
                        yfmt=lambda v: f"${v:.0f}", ylabel="the nightly rate", width=8.4, height=4.0, center=(-1.0, -0.35),
                        nudge={"one rate all year": -0.25})
        c = stat_cards([(m(M["ebitda"]), f"profit, against {m(F['ebitda'])}", GOOD),
                        (f"{100 * M['occupancy']:.0f}%", f"full, against {100 * F['occupancy']:.0f}%", OWNER)], y=-3.05, size=24, span=9)
        tag = estimate_tag("the Works: the best rate month by month, for a seasonal demand index (an assumption)", size=12)
        beat(self,
             "But demand is not the same all year. Summer brings nearly twice the guests of a winter week. <bookmark mark='a'/> So "
             f"price each month separately: {min(M['rates']):.0f} dollars in the quiet winter months, {max(M['rates']):.0f} in "
             "July, when the hotel would otherwise sell out and turn people away. <bookmark mark='b'/> The year's profit rises "
             f"to {M['ebitda'] / 1e6:.2f} million, and the hotel is fuller too, {100 * M['occupancy']:.0f} per cent instead of "
             f"{100 * F['occupancy']:.0f}. This is revenue management, which Part 28 met at the airlines: the same room sold "
             "at different prices to fill a fixed capacity that cannot be stored.",
             base=[ch.frame, tag], steps=[VGroup(*ch.lines.values(), *ch.labels.values()), c])

    def dollar(self):
        S = R["contract"]["split"]
        rev = S["revenue"]
        parts = [("running costs: staff, cleaning, power, tax", S["costs"] / rev, STAFF), ("the brand", S["brand"] / rev, BRAND),
                 ("online agents and cards", S["agents"] / rev, AGENT), ("refurbishment reserve", S["reserve"] / rev, FIXC),
                 ("interest", S["interest"] / rev, BAD), ("the owner", S["cash"] / rev, GOOD)]
        other = 1 - sum(v for _, v, _ in parts)
        parts.insert(1, ("breakfast and the rest, cost", other, ALL))
        bar = viz.bar_split(parts, 1.0, width=12.6, height=0.9).move_to([0, 0.8, 0])
        labs = VGroup()
        for i, (n_, v, c) in enumerate(parts):
            lab = VGroup(tx(f"{100 * v:.0f}c", 18, c, bold=True), tx(n_, 11, GREY_A)).arrange(DOWN, buff=0.05)
            lab.next_to(bar[i], DOWN if i % 2 == 0 else UP, buff=0.18)
            labs.add(lab)
        hd = tx(f"a dollar of the hotel's revenue ({m(rev)} a year)", 20, WHITE, bold=True).to_edge(UP, buff=0.6)
        tag = estimate_tag("the Works: the year priced month by month", size=12)
        steps = [VGroup(bar[i], labs[i]) for i in range(len(parts))]
        beat(self,
             f"Follow a dollar of the hotel's revenue. <bookmark mark='a'/> {100 * parts[0][1]:.0f} cents go on running it: "
             "the housekeepers and the front desk, the laundry, the power and the property tax. <bookmark mark='b'/> A few "
             f"cents on the breakfast and parking it sells. <bookmark mark='c'/> {100 * parts[2][1]:.0f} cents to the brand. "
             f"<bookmark mark='d'/> {100 * parts[3][1]:.0f} to the online agents and the card companies. <bookmark mark='e'/> "
             f"{100 * parts[4][1]:.0f} into a reserve for the refurbishment every hotel needs every few years. "
             f"<bookmark mark='f'/> {100 * parts[5][1]:.0f} cents of interest to the bank. <bookmark mark='g'/> And "
             f"{100 * parts[6][1]:.0f} cents for you, the owner.",
             base=[hd, tag], steps=steps)

    def owner(self):
        U = R["run"]
        M = U["monthly"]
        lo = R["run"]["at180"]
        c = stat_cards([(m(M["cash"]), "your cash a year, after interest", GOOD),
                        (m(M["equity"], 1), "your own money in the building", OWNER),
                        (f"{100 * M['yield_']:.1f}%", "a year on it", BRAND)], y=0.4, size=36, span=11)
        note = tx("the brand's fees arrive whether or not the owner earns anything", 18, GREY_B).move_to([0, -1.8, 0])
        tag = estimate_tag("the Works: before income tax and before any change in the building's value", size=12)
        beat(self,
             f"<bookmark mark='a'/> That is about {M['cash'] / 1e6:.1f} million dollars a year. <bookmark mark='b'/> On the "
             f"{M['equity'] / 1e6:.1f} million of your own money in the building, <bookmark mark='c'/> "
             f"{100 * M['yield_']:.1f} per cent a year, before tax, and before the building rises or falls in value. "
             f"<bookmark mark='d'/> Now notice the order of payment. The brand's {M['fees'] / 1e6:.2f} million comes off the top "
             "of the room revenue, every month, in good years and bad. You get what is left after the bank. A fall in "
             "occupancy that the brand barely notices can wipe out your year.",
             base=[tag], steps=[c[0], c[1], c[2], note])

    def brand(self):
        U = R["run"]
        Mb, Mi = U["monthly"], U["indep"]
        items = [("with the brand: profit before interest", Mb["ebitda"] / 1e6, BRAND, m(Mb["ebitda"])),
                 ("on your own: profit before interest", Mi["ebitda"] / 1e6, OWNER, m(Mi["ebitda"]))]
        rows = hbars(items, max_value=3.2, x0=0.8, top=1.2, row=1.3, length=5.6, size=18, bar_h=0.65)
        hd = tx("the same hotel, branded or independent", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"independent: no fees, but {100 * U['hotel']['lift']:.0f}% less demand and {100 * U['hotel']['ota_indep']:.0f}% of rooms sold by agents",
                  16, GREY_B).move_to([0, -1.6, 0])
        tag = estimate_tag("the Works: an independent hotel's lower demand and higher agent share are assumptions, with ranges", size=12)
        beat(self,
             "Is the brand worth it? Take its name off the door. <bookmark mark='a'/> With the brand, the hotel makes "
             f"{Mb['ebitda'] / 1e6:.2f} million dollars a year before interest, after paying the brand {Mb['fees'] / 1e6:.2f} "
             f"million. <bookmark mark='b'/> On your own you pay no fees, but in this series' assumptions fewer travellers find "
             f"you, and you sell {100 * U['hotel']['ota_indep']:.0f} per cent of your rooms through online agents at their "
             f"commission instead of a quarter. To fill the hotel you cut the rate, to {Mi['adr']:.0f} dollars, and you make "
             f"{Mi['ebitda'] / 1e6:.2f} million. <bookmark mark='c'/> The brand pays for itself, just: what it sells is demand.",
             base=[rows.axis, hd, tag], steps=[rows[0], rows[1], note])

    def lesson(self):
        lines = [("a room-night cannot be stored: price it to fill, not to the last dollar", OWNER),
                 ("demand moves by season and by night; rates follow it", BRAND),
                 ("the brand is paid off the top of revenue; the owner gets what is left after the bank", GOOD),
                 ("the brand is worth its fee only if it brings guests the owner could not find alone", AGENT)]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.1, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So: <bookmark mark='a'/> a hotel sells nights that cannot be kept, so it prices to fill its rooms. "
             "<bookmark mark='b'/> Demand changes by month and by night, and the rate follows it. <bookmark mark='c'/> The "
             "brand is paid first, as a share of revenue; the owner gets what is left after the bank. <bookmark mark='d'/> And "
             "the brand is worth its fee only if it brings guests the owner could not have found alone.",
             base=[head("Run it: what the hotel taught")], steps=list(g))
