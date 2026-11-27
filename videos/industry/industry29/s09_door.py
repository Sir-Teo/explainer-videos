from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403


class Door(VoiceoverScene):
    def construct(self):
        card(self, 7, "The last mile", "Why is the last mile the dearest?",
             "Chapter seven. The last mile. A parcel can cross a continent in a full trailer for a dollar or two, then cost "
             "as much again to carry to one door.", lit=("make", "dollar"))
        self.route()
        self.curve()
        self.post()

    def route(self):
        D = R["door"]
        v = draw.van(1.8, color=PARCEL).move_to([-4.8, 1.6, 0])
        houses = VGroup(*[draw.house(0.6).move_to([-2.6 + 1.1 * k, 1.5, 0]) for k in range(7)])
        c = stat_cards([(f"${D['hour']:.0f}", "an hour for the driver and van", PARCEL), (f"{D['dwell']:.1f} min", "at each stop", ALL),
                        (f"{D['speed']:.0f} mph", "between stops", SKY), (f"{D['pps']:.1f}", "parcels a stop", GOOD)],
                       y=-1.0, size=34, span=12.4)
        tag = estimate_tag("the Works: every figure here is this series' assumption", size=12)
        beat(self,
             "The Works has a delivery route. <bookmark mark='a'/> A driver and van cost about "
             f"{D['hour']:.0f} dollars an hour, all in, for an {D['hours']:.0f}-hour day. <bookmark mark='b'/> Each stop "
             f"takes {D['dwell']:.1f} minutes, <bookmark mark='c'/> the van drives between stops at {D['speed']:.0f} miles an "
             f"hour, <bookmark mark='d'/> and each stop takes {D['pps']:.1f} parcels. The only thing left to choose is how "
             "far apart the doors are.",
             base=[v, houses, tag], steps=[c[0], c[1], c[2], c[3]])

    def curve(self):
        D = R["door"]
        cv, st = D["curve"], D["stops"]
        kinds = [(0.05, "city blocks", GOOD), (0.3, "suburb", SKY), (0.75, "small town", PARCEL), (2.0, "countryside", BAD),
                 (5.0, "remote", BAD)]
        items = [(f"{n}: {s:g} miles apart, {st[s]:.0f} stops a day", cv[s], c, f"${cv[s]:.2f}") for s, n, c in kinds]
        rows = hbars(items, max_value=14, x0=1.2, top=1.8, row=0.8, length=5.0, size=16, bar_h=0.42)
        lab = tx("the Works' route: cost of delivering one parcel", 17, GREY_A).to_edge(UP, buff=0.7)
        tag = estimate_tag("the Works", size=12)
        beat(self,
             "Now spread the doors out. <bookmark mark='a'/> In a dense city, with a stop every twentieth of a mile, the "
             f"driver makes about {st[0.05]:.0f} stops a day and a parcel costs about {D['city']:.2f} dollars to deliver. "
             f"<bookmark mark='b'/> In a suburb, three-tenths of a mile apart, {st[0.3]:.0f} stops and {D['suburb']:.2f}. "
             f"<bookmark mark='c'/> In the countryside, two miles apart, {st[2.0]:.0f} stops and {D['rural']:.2f}. The "
             "last mile is Run it's empty trip home in another form: most of the driver's day is spent between doors.",
             base=[rows.axis, lab, tag], steps=[rows[0], rows[1], VGroup(*rows[2:])])

    def post(self):
        D = R["door"]
        items = [("2007", D["ppd"][0], ALL, f"{D['ppd'][0]:.1f}"), ("2025", D["ppd"][1], BAD, f"{D['ppd'][1]:.1f}")]
        rows = hbars(items, max_value=6, x0=-1.0, top=2.0, row=0.9, length=5.6, size=18, bar_h=0.5)
        lab = tx("the Postal Service: pieces delivered to each address each day", 17, GREY_A).to_edge(UP, buff=0.6)
        c = stat_cards([(f"+{D['dp']:.1f}m", "new addresses to serve in 2025", SKY), (f"${D['usps_rev']:.1f}bn", "revenue, fiscal 2025", ALL),
                        (f"-${D['usps_loss']:.1f}bn", "net loss", BAD)], y=-1.6, size=34, span=11)
        src = source("United States Postal Service, report on Form 10-K for fiscal 2025", size=12)
        beat(self,
             "The Postal Service lives at the far end of that curve. 'We serve the American people in all areas of our "
             "nation,' its annual report says, 'and through the universal service mission, bind our nation together.' It "
             "visits every address, the remote ones included. "
             f"<bookmark mark='a'/> In 2007 it delivered {D['ppd'][0]:.1f} pieces to each address each day; "
             f"<bookmark mark='b'/> by 2025, {D['ppd'][1]:.1f}, as the mail shrank. <bookmark mark='c'/> Yet the "
             f"addresses keep growing, {D['dp']:.1f} million more in 2025 alone. <bookmark mark='d'/> It took in "
             f"{D['usps_rev']:.1f} billion dollars that year, <bookmark mark='e'/> and lost {D['usps_loss']:.1f} billion. "
             f"Shipping and packages, {D['usps_pkgrev']:.1f} billion, are now its largest business; the cost is a route "
             "walked every day for fewer letters.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], c[0], c[1], c[2]])
