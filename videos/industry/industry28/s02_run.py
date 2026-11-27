from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: sell one flight", "180 seats, two kinds of traveller, sixty days. How do you sell them?",
             "Chapter one. Run it. You run one flight in the Works: a hundred and eighty seats, a thousand miles, departing "
             "in sixty days. Every seat you do not sell is worth nothing the moment the doors close.", lit=("unit", "make"))
        self.flight()
        self.travellers()
        self.first()
        self.high()
        self.protect()
        self.result()
        self.overbook()
        self.dearer()
        self.lesson()

    def flight(self):
        U = R["run"]
        cab = draw.cabin(rows=30, seats=(3, 3), size=0.2, gap=0.04).move_to([0, 1.2, 0])
        c = stat_cards([(f"{U['seats']}", "seats", SKY), (f"{U['miles']:,.0f}", "miles", ALL),
                        (f"${U['cost']:,.0f}", "to fly it, full or empty", BAD)], y=-1.4, size=40, span=10)
        tag = estimate_tag(f"the Works: {100 * U['casm']:.0f} cents per seat-mile; Delta's 2025 cost was 19.31 cents", size=12)
        beat(self,
             "Here is the flight. <bookmark mark='a'/> A hundred and eighty seats, <bookmark mark='b'/> a thousand miles. "
             f"<bookmark mark='c'/> It costs {U['cost']:,.0f} dollars to fly: crew, fuel, the aircraft, the airport, all of "
             f"it, about {100 * U['casm']:.0f} cents for every seat carried every mile. Once the flight is on the timetable "
             "that cost hardly changes whether one passenger boards or a hundred and eighty.",
             base=[cab, tag], steps=[c[0], c[1], c[2]])

    def travellers(self):
        U = R["run"]
        left = VGroup(tx("Leisure travellers", 22, LEISURE, bold=True), tx(f"about {U['leisure']:.0f} want this flight", 17, WHITE),
                      tx("they book early", 17, WHITE), tx(f"they pay at most ${U['low']:.0f}", 17, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        right = VGroup(tx("Business travellers", 22, BIZ, bold=True), tx(f"about {U['business']:.0f} want it", 17, WHITE),
                       tx("they book in the last weeks", 17, WHITE), tx(f"they will pay ${U['high']:.0f}", 17, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        g = VGroup(left, right).arrange(RIGHT, buff=2.2).move_to([0, 0.6, 0])
        prob = tx("the problem: the cheap demand arrives first", 20, BAD, bold=True).move_to([0, -1.8, 0])
        tag = estimate_tag("the Works: demand for each fare is random around these averages", size=12)
        beat(self,
             "Two kinds of people want the seats. <bookmark mark='a'/> Holidaymakers: about "
             f"{U['leisure']:.0f} of them, who book weeks ahead and will pay at most {U['low']:.0f} dollars. "
             f"<bookmark mark='b'/> And business travellers: about {U['business']:.0f}, who book in the last weeks and will "
             f"pay {U['high']:.0f}. <bookmark mark='c'/> The difficulty is the order they arrive in. If you sell to whoever "
             "asks first, the cheap demand takes the plane before the dear demand has even looked.",
             base=[tag], steps=[left, right, prob])

    def first(self):
        U = R["run"]["first"]
        cab = draw.cabin(rows=30, seats=(3, 3), size=0.2, gap=0.04).move_to([0, 1.6, 0])
        fill(cab, int(round(U["sold_low"])), int(round(U["sold_high"])))
        c = stat_cards([(f"{U['turned_away']:.0f}", "business travellers turned away", BAD),
                        (f"${U['revenue']:,.0f}", "revenue", ALL), (usd(U['profit']), "profit on the flight", BAD)],
                       y=-1.3, size=38, span=11)
        tag = estimate_tag("the Works: average of many simulated flights", size=12)
        beat(self,
             f"So, first: sell every seat at {R['run']['low']:.0f} dollars to whoever comes first. <bookmark mark='a'/> The "
             "plane fills with holidaymakers weeks before departure. <bookmark mark='b'/> When the business travellers "
             f"arrive, about {U['turned_away']:.0f} of them find it full. <bookmark mark='c'/> Revenue: {U['revenue']:,.0f} "
             f"dollars. <bookmark mark='d'/> The flight cost {R['run']['cost']:,.0f}: a full plane, and a loss of "
             f"{abs(U['profit']):,.0f} dollars.",
             base=[tag], steps=[cab, c[0], c[1], c[2]])

    def high(self):
        U = R["run"]["high_only"]
        cab = draw.cabin(rows=30, seats=(3, 3), size=0.2, gap=0.04).move_to([0, 1.6, 0])
        fill(cab, 0, int(round(U["sold_high"])))
        c = stat_cards([(f"{U['sold']:.0f}", "seats sold", BIZ), (f"${U['revenue']:,.0f}", "revenue", ALL),
                        (usd(U['profit']), "profit on the flight", BAD)], y=-1.3, size=38, span=11)
        tag = estimate_tag("the Works", size=12)
        beat(self,
             f"Then the opposite: one fare, {R['run']['high']:.0f} dollars, for everyone. <bookmark mark='a'/> Only the "
             f"business travellers pay it: about {U['sold']:.0f} seats, the rest empty. <bookmark mark='b'/> Revenue "
             f"{U['revenue']:,.0f}, <bookmark mark='c'/> and a loss of {abs(U['profit']):,.0f}. One price is too low for "
             "half the customers and too high for the other half.",
             base=[cab, tag], steps=[c[0], c[1], c[2]])

    def protect(self):
        U = R["run"]
        sw = U["sweep"]
        ch = line_chart({"revenue per flight": ({k: v / 1e3 for k, v in sw.items()}, CASH)}, x=(0, 80), y=(15, 40),
                        xticks=[0, 20, 40, 60, 80], yticks=[15, 20, 25, 30, 35, 40], yfmt=lambda v: f"${v:.0f}k",
                        ylabel="the Works: revenue per flight, by seats held back for business travellers", width=9.2, height=4.2,
                        center=(-0.8, -0.45), label_end=False)
        cost = DashedLine(ch.ax.c2p(0, U["cost"] / 1e3), ch.ax.c2p(80, U["cost"] / 1e3), stroke_color=BAD, stroke_width=2)
        cl = tx("the flight's cost", 14, BAD).next_to(ch.ax.c2p(80, U["cost"] / 1e3), UP, buff=0.08, aligned_edge=RIGHT)
        m = marker(ch.ax, U["lw"], sw[U["lw"]] / 1e3, f"hold back {U['lw']}: ${sw[U['lw']]:,.0f}", GOOD, side=UP)
        rule = MathTex(r"\text{hold the } y\text{th seat while } P(\text{business demand} \ge y) > \frac{%d}{%d} = %.0f\%%"
                       % (U["low"], U["high"], 100 * U["ratio"]), font_size=30).to_edge(UP, buff=0.5)
        tag = estimate_tag("the Works; after Littlewood (1972)", size=12)
        beat(self,
             "The answer is to sell the same seat at two prices, and to hold some seats back. <bookmark mark='a'/> Hold back "
             "none and you get the first result; hold back too many and you fly them empty. <bookmark mark='b'/> In between "
             f"there is a best number: here, {U['lw']} seats. <bookmark mark='c'/> Ken Littlewood wrote down the rule in "
             "1972, in a paper on forecasting and controlling airline bookings: keep holding a seat back as long as the chance that a business traveller will "
             f"still want it is more than the ratio of the two fares, {U['low']:.0f} over {U['high']:.0f}, about "
             f"{100 * U['ratio']:.0f} per cent.",
             base=[ch.frame, cost, cl, tag], steps=[ch.lines["revenue per flight"], m, rule])

    def result(self):
        U = R["run"]["protect"]
        cab = draw.cabin(rows=30, seats=(3, 3), size=0.2, gap=0.04).move_to([0, 1.6, 0])
        fill(cab, int(round(U["sold_low"])), int(round(U["sold_high"])))
        c = stat_cards([(f"{U['sold_low']:.0f} + {U['sold_high']:.0f}", "leisure and business seats sold", SKY),
                        (f"${U['fare']:.0f}", "average fare", ALL), (usd(U['profit']), "profit on the flight", GOOD)],
                       y=-1.3, size=38, span=11)
        tag = estimate_tag("the Works", size=12)
        beat(self,
             f"With {R['run']['lw']} seats held back: <bookmark mark='a'/> about {U['sold_low']:.0f} holidaymakers and "
             f"{U['sold_high']:.0f} business travellers fly. <bookmark mark='b'/> The average fare is {U['fare']:.0f} dollars, "
             f"<bookmark mark='c'/> and the flight makes {U['profit']:,.0f} dollars instead of losing {abs(R['run']['first']['profit']):,.0f}. "
             "Same plane, same crew, same fuel, nearly the same number of passengers. The whole difference is which "
             "passengers got which seats, at which price.",
             base=[cab, tag], steps=[c[0], c[1], c[2]])

    def overbook(self):
        U = R["run"]
        ov = U["over"]
        ch = line_chart({"revenue less compensation": ({k: v / 1e3 for k, v in ov.items()}, CASH)}, x=(0, 24), y=(33, 37),
                        xticks=[0, 4, 8, 12, 16, 20, 24], yticks=[33, 34, 35, 36, 37], yfmt=lambda v: f"${v:.0f}k",
                        ylabel="the Works: revenue per flight less payments to bumped travellers, by seats sold beyond 180",
                        width=9.2, height=4.2, center=(-0.8, -0.45), label_end=False)
        b = U["best_over"]
        m = marker(ch.ax, b, ov[b] / 1e3, f"sell {b} extra: ${ov[b]:,.0f}", GOOD, side=UP)
        B = U["both"]
        tag = estimate_tag(f"the Works: {100 * U['noshow']:.0f}% of booked travellers do not show; each bumped traveller is paid ${U['bump']:.0f}", size=12)
        beat(self,
             f"One more lever. <bookmark mark='a'/> About {100 * U['noshow']:.0f} per cent of booked travellers do not turn "
             "up, so an empty seat is still flown. Sell more seats than the plane has, and pay anyone who cannot board to take "
             f"a later flight. <bookmark mark='b'/> The best here is to sell {b} extra seats: on an average flight, "
             f"{B['bumped']:.2f} travellers are bumped and paid, and the flight makes {B['profit']:,.0f} dollars.",
             base=[ch.frame, tag], steps=[ch.lines["revenue less compensation"], m])

    def dearer(self):
        U = R["run"]
        D = U["dear"]
        X = D["res"]
        cab = draw.cabin(rows=30, seats=(3, 3), size=0.2, gap=0.04).move_to([0, 1.6, 0])
        fill(cab, int(round(X["sold_low"])), int(round(X["sold_high"])))
        c = stat_cards([(f"hold back {D['lw']}", f"seats, at a ${D['high']:.0f} business fare", BIZ),
                        (f"${X['fare']:.0f}", "average fare", ALL), (usd(X['profit']), "profit on the flight", GOOD)],
                       y=-1.3, size=38, span=11)
        tag = estimate_tag("the Works: the same flight with a dearer business fare", size=12)
        beat(self,
             "Now change one thing. <bookmark mark='a'/> Suppose the business travellers will pay "
             f"{D['high']:.0f} dollars instead of {U['high']:.0f}. The ratio of the fares falls to about "
             f"{100 * U['low'] / D['high']:.0f} per cent, so Littlewood's rule says hold back more: {D['lw']} seats. "
             f"<bookmark mark='b'/> The average fare rises to {X['fare']:.0f} dollars, <bookmark mark='c'/> and the flight "
             f"makes {X['profit']:,.0f}. The plane, the crew and the fuel are the same again. What moved the profit is how "
             "much the last-minute travellers will pay, which is why airlines watch business travel more closely than any "
             "other number.",
             base=[cab, tag], steps=[c[0], c[1], c[2]])

    def lesson(self):
        U = R["run"]
        g = VGroup(tx("What Run it shows", 22, WHITE, bold=True),
                   tx(f"the cost is fixed: ${U['cost']:,.0f} a flight, full or empty", 18, BAD),
                   tx("the seat perishes at departure, so any fare above zero beats an empty seat", 18, SKY),
                   tx("and yet the profit is made in the last few seats, sold dear", 18, BIZ),
                   tx(f"from a ${abs(U['first']['profit']):,.0f} loss to a ${U['both']['profit']:,.0f} profit, with the same aircraft", 18, GOOD)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' summary of the Works' flight", size=12)
        beat(self,
             "So: <bookmark mark='a'/> the cost of a flight is fixed, <bookmark mark='b'/> the seat perishes at departure, so "
             "almost any fare beats an empty seat, <bookmark mark='c'/> and yet the profit is made in the last few seats, "
             "sold dear to people who book late. <bookmark mark='d'/> Get the mix right and the flight turns from a loss to a "
             "profit with nothing else changed. Get it slightly wrong, every flight, every day, and an airline loses money "
             "with full planes.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
