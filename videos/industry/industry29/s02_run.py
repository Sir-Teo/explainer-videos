from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403

CHI, ATL = np.array([-3.6, 1.4, 0]), np.array([2.8, -0.9, 0])
_D = (ATL - CHI) / np.linalg.norm(ATL - CHI)
BELOW = -0.5 * np.array([-_D[1], _D[0], 0])


def home_arrow(color):
    return Arrow(ATL + BELOW, CHI + BELOW, buff=0.3, color=color, stroke_width=4)


def cities():
    a = VGroup(Dot(CHI, radius=0.12, color=WHITE), tx("Chicago", 18, WHITE, bold=True).next_to(CHI, UP, buff=0.12))
    b = VGroup(Dot(ATL, radius=0.12, color=WHITE), tx("Atlanta", 18, WHITE, bold=True).next_to(ATL, DOWN, buff=0.12))
    return a, b


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: price a lane", "One truck, one load from Chicago to Atlanta. What should you charge?",
             "Chapter one. Run it. You own one truck in Chicago, and a shipper offers you a load to Atlanta, seven hundred "
             "and twenty miles. What should you charge?", lit=("unit", "make"))
        self.truck()
        self.offer()
        self.home()
        self.backhaul()
        self.network()
        self.lesson()

    def truck(self):
        U = R["run"]
        s = draw.semi(5.0, cab_color=TRUCK).move_to([0, 1.6, 0])
        c = stat_cards([(f"${U['nonfuel']:.2f}", "a mile: driver, truck, insurance, upkeep", ALL),
                        (f"${U['fuel_mile']:.2f}", f"a mile of diesel at ${U['diesel']:.2f} a gallon", FUEL),
                        (f"${U['per_mile']:.2f}", "a mile driven, loaded or empty", TRUCK)], y=-1.0, size=38, span=12)
        tag = estimate_tag("the Works; diesel is the EIA's 2025 average retail price", size=12)
        beat(self,
             "First, what the truck costs. <bookmark mark='a'/> The driver, the tractor and trailer, insurance, repairs and "
             f"the office come to about {U['nonfuel']:.2f} dollars for every mile driven, this series' assumption, set "
             "against Knight-Swift's accounts. <bookmark mark='b'/> Diesel cost "
             f"{U['diesel']:.2f} a gallon on average in 2025; at six and a half miles a gallon that is "
             f"{100 * U['fuel_mile']:.0f} cents a mile. <bookmark mark='c'/> In all, {U['per_mile']:.2f} dollars a mile, "
             "and the important words are 'a mile driven': the truck costs the same whether the trailer is full or empty. "
             f"Driven as far as one of Knight-Swift's trucks went in 2025, {get('kx29.miles'):,.0f} miles, that is about "
             f"{get('kx29.miles') * U['per_mile'] / 1e3:,.0f} thousand dollars a year. And in 2026, with the Strait of "
             f"Hormuz all but shut, diesel averaged about {U['diesel26']:.2f} a gallon, adding "
             f"{100 * (U['diesel26'] - U['diesel']) / 6.5:.0f} cents to every mile.",
             base=[s, tag], steps=[c[0], c[1], c[2]])

    def offer(self):
        U = R["run"]
        a, b = cities()
        arr = Arrow(CHI, ATL, buff=0.25, color=TRUCK, stroke_width=6)
        s = draw.semi(1.4, cab_color=TRUCK).move_to(CHI + np.array([0.9, -0.2, 0]))
        c = stat_cards([(f"${U['out_rev']:,.0f}", f"{U['miles']:.0f} miles at ${U['head']:.2f} a loaded mile", GOOD),
                        (f"${U['one_way']:,.0f}", "what the trip costs", BAD),
                        (usd(U['out_rev'] - U['one_way']), "it looks like a profit", GOOD)], y=-2.5, size=32, span=12)
        tag = estimate_tag(f"the Works; ${U['head']:.2f} is J.B. Hunt's 2025 truckload revenue per loaded mile", size=12)
        beat(self,
             f"The shipper offers {U['head']:.2f} dollars a mile, which is what J.B. Hunt's truckload business averaged in "
             f"2025. <bookmark mark='a'/> {U['miles']:.0f} miles to Atlanta. <bookmark mark='b'/> That pays "
             f"{U['out_rev']:,.0f} dollars. <bookmark mark='c'/> The trip costs {U['one_way']:,.0f}. "
             f"<bookmark mark='d'/> A profit of {U['out_rev'] - U['one_way']:,.0f} dollars. You take the load.",
             base=[a, b, tag], steps=[VGroup(arr, s), c[0], c[1], c[2]])

    def home(self):
        U = R["run"]
        E = U["empty"]
        a, b = cities()
        out = Arrow(CHI, ATL, buff=0.25, color=TRUCK, stroke_width=6)
        back = DashedVMobject(home_arrow(GREY_B), num_dashes=24)
        bl = tx("home, empty", 16, GREY_B).next_to(back.get_center(), DOWN + LEFT, buff=0.3)
        c = stat_cards([(f"${E['cost']:,.0f}", "the round trip costs", BAD), (usd(E['profit']), "the trip's result", BAD),
                        (f"${U['be_empty']:.2f}", "a loaded mile needed to pay", TRUCK)], y=-2.5, size=32, span=12)
        tag = estimate_tag("the Works", size=12)
        beat(self,
             "Then you are in Atlanta, and your truck lives in Chicago. <bookmark mark='a'/> Suppose, as in the Works, "
             "that Atlanta receives more freight than it sends out, so on this lane there is no load home, and you drive "
             "back empty. "
             f"<bookmark mark='b'/> The round trip costs {E['cost']:,.0f} dollars <bookmark mark='c'/> against "
             f"{U['out_rev']:,.0f} of revenue: a loss of {abs(E['profit']):,.0f}. <bookmark mark='d'/> To pay for the "
             f"truck, the load out would have to pay {U['be_empty']:.2f} a mile, nearly twice the market rate. The price "
             "of a lane is set by the trip home.",
             base=[a, b, out, tag], steps=[VGroup(back, bl), c[0], c[1], c[2]])

    def backhaul(self):
        U = R["run"]
        B = U["back"]
        a, b = cities()
        out = Arrow(CHI, ATL, buff=0.25, color=TRUCK, stroke_width=6)
        back = home_arrow(GOOD)
        bl = tx(f"a load home at ${U['back_rate']:.2f} a mile, {100 * U['p_back']:.0f}% of the time", 16, GOOD).next_to(
            back.get_center(), DOWN + LEFT, buff=0.3)
        c = stat_cards([(f"${B['back_rev']:,.0f}", "expected revenue home", GOOD),
                        (f"${B['wait']:,.0f}", "a day spent waiting for it", BAD),
                        (usd(B['profit']), f"against {usd(U['empty']['profit'])} empty", ALL)], y=-2.5, size=32, span=12)
        tag = estimate_tag("the Works: the rate, the odds and the wait home are this series' assumptions", size=12)
        beat(self,
             f"Now a broker offers a load back toward Chicago at {U['back_rate']:.2f} a mile. <bookmark mark='a'/> That is "
             f"below your cost of {U['per_mile']:.2f}. Do you take it? Yes: you are driving home anyway, so almost all of "
             "the money is extra. Say you find one six times in ten, after a day's wait. <bookmark mark='b'/> It adds "
             f"about {B['back_rev']:,.0f} dollars <bookmark mark='c'/> for a day's wait of {B['wait']:,.0f}, "
             f"<bookmark mark='d'/> and the loss falls from {abs(U['empty']['profit']):,.0f} to {abs(B['profit']):,.0f}. "
             "Like the airline's last seat in Part 28, a load home sells below its full cost and is still worth selling.",
             base=[a, b, out, tag], steps=[VGroup(back, bl), c[0], c[1], c[2]])

    def network(self):
        U = R["run"]
        N = U["needed"]
        items = [(("half the miles empty: one lane" if s == 0.5 else f"{100 * s:.0f}% empty" + ("  (Knight-Swift, 2025)" if abs(s - U['knx_empty'] / 100) < 1e-9 else "")),
                  v, GOOD if v <= U["head"] * 1.08 else (TRUCK if s < 0.5 else BAD), f"${v:.2f}") for s, v in N.items()]
        rows = hbars(items, max_value=5.6, x0=0.6, top=1.9, row=0.62, length=5.6, size=16, bar_h=0.36)
        mkt = DashedLine(rows.axis.get_bottom() + RIGHT * 5.6 * U["head"] / 5.6 + DOWN * 0.1,
                         rows.axis.get_top() + RIGHT * 5.6 * U["head"] / 5.6 + UP * 0.1, stroke_color=SKY, stroke_width=2)
        ml = tx(f"the market's ${U['head']:.2f}", 14, SKY).next_to(mkt, DOWN, buff=0.1)
        lab = tx("the rate a loaded mile needed to pay the truck, by the share of miles driven empty", 17, GREY_A).to_edge(UP, buff=0.6)
        tag = estimate_tag(f"the Works; Knight-Swift's truckload segment drove {U['knx_empty']:.1f}% of its miles empty in 2025", size=12)
        beat(self,
             "So the real answer is not a price at all, it is a network. <bookmark mark='a'/> With one truck on one lane, "
             f"half your miles are empty, and you need {N[0.5]:.2f} a loaded mile. <bookmark mark='b'/> Find loads for more "
             "of the trips home, through triangles of cities, a broker's app, or customers of your own, and the price "
             f"you need falls. <bookmark mark='c'/> Knight-Swift ran {U['knx_empty']:.1f} per cent of its miles empty in "
             f"2025, so it needs about {N[U['knx_empty'] / 100]:.2f}, close to the market rate. <bookmark mark='d'/> That "
             "is why the large carriers and the brokers exist: a one-truck firm wins a load out, and the large network "
             f"wins the trip home. J.B. Hunt's brokerage alone works with about {get('jb29.carriers'):,.0f} other "
             "trucking firms, finding them loads they could not find themselves.",
             base=[rows.axis, lab, tag], steps=[VGroup(*rows[:1]), VGroup(*rows[1:4]), VGroup(*rows[4:5], mkt, ml), VGroup(*rows[5:])])

    def lesson(self):
        U = R["run"]
        g = VGroup(tx("What Run it shows", 22, WHITE, bold=True),
                   tx(f"a truck costs about ${U['per_mile']:.2f} a mile driven, loaded or empty", 18, TRUCK),
                   tx("the price of a lane is set by the trip home", 18, SKY),
                   tx("a load home below cost still beats an empty trailer", 18, GOOD),
                   tx("the firm with the most freight in the most places runs the fewest empty miles", 18, RAIL)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' summary of the Works' lane", size=12)
        beat(self,
             "So: <bookmark mark='a'/> a truck costs the same full or empty; <bookmark mark='b'/> the price of a lane is "
             "set by the trip home, which is why shippers in a city that sends more than it receives pay more; "
             "<bookmark mark='c'/> a load home is worth taking at almost any price; <bookmark mark='d'/> and the carrier "
             "with the most freight in the most places drives the fewest empty miles. Hold on to that idea. It explains "
             "the railways, the parcel networks and the half a million trucking firms alike.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
