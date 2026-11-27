from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403


class Rail(VoiceoverScene):
    def construct(self):
        card(self, 3, "The railway: a road you own", "Why does a railway keep forty cents of every dollar?",
             "Chapter three. The railway, a road you own. A railway builds, owns and maintains its own track, and that one "
             "fact explains both why it was failing in 1980 and why it prospers now.", lit=("make", "moat"))
        self.owns()
        self.density()
        self.prices()
        self.four()
        self.captive()

    def owns(self):
        Rl = R["rail"]
        tr = draw.train(8, 0.9, kinds=("hopper", "well", "box", "tank"),
                        colors=("#B58CFF", "#E8554E", "#7BD88F", "#C9D3E0")).move_to([0, 1.8, 0])
        track = Line([-7, tr.get_bottom()[1] - 0.04, 0], [7, tr.get_bottom()[1] - 0.04, 0], stroke_color=GREY_B, stroke_width=3)
        c = stat_cards([(f"{Rl['route']:,.0f}", "miles of route", RAIL), (f"{Rl['rtm']:.0f}bn", "ton-miles carried in 2025", ALL),
                        (f"{Rl['emp']:,.0f}", "employees, on average", SKY)], y=-0.9, size=40, span=12)
        src = source("Union Pacific, Form 10-K for 2025", size=12)
        beat(self,
             "Take Union Pacific, which connects twenty-three states in the western two-thirds of America. "
             f"<bookmark mark='a'/> It operates {Rl['route']:,.0f} miles of route and owns most of it. "
             f"<bookmark mark='b'/> In 2025 it carried {Rl['rtm']:.0f} billion ton-miles: a ton of freight moved a mile, "
             f"four hundred and twenty-seven billion times. <bookmark mark='c'/> It did it with about "
             f"{Rl['emp']:,.0f} people. A trucker shares the public road with everyone; a railway pays for every mile of its "
             "own, whether one train runs on it a day or fifty.",
             base=[tr, track, src], steps=[c[0], c[1], c[2]])

    def density(self):
        Rl = R["rail"]
        cv = {d / 1e6: 100 * v for d, v in Rl["curve"].items() if 100 * v <= 25}
        ch = line_chart({"cost a ton-mile": (cv, RAIL)}, x=(0, 30), y=(0, 25), xticks=[0, 5, 10, 15, 20, 25, 30],
                        yticks=[0, 5, 10, 15, 20, 25], xfmt=lambda v: f"{v:.0f}m", yfmt=lambda v: f"{v:.0f}c",
                        ylabel="the Works' railway: average cost of a ton-mile, by ton-miles a year on each mile of route",
                        width=9.2, height=4.4, center=(-0.6, -0.45), label_end=False)
        price = DashedLine(ch.ax.c2p(0, 100 * Rl["rate"]), ch.ax.c2p(30, 100 * Rl["rate"]), stroke_color=GOOD, stroke_width=2)
        pl = tx(f"what Union Pacific is paid: {100 * Rl['rate']:.1f}c", 14, GOOD).next_to(ch.ax.c2p(30, 100 * Rl["rate"]), UP, buff=0.08, aligned_edge=RIGHT)
        m1 = marker(ch.ax, Rl["density"] / 1e6, 100 * Rl["avg"], f"Union Pacific: {Rl['density'] / 1e6:.0f}m, {100 * Rl['avg']:.1f}c", RAIL, side=UP)
        m2 = marker(ch.ax, 1.0, 100 * Rl["at1"], f"a branch line, 1m: {100 * Rl['at1']:.0f}c", BAD, side=RIGHT)
        m3 = marker(ch.ax, Rl["be"] / 1e6, 100 * Rl["rate"], f"break-even: {Rl['be'] / 1e6:.1f}m", GOOD, side=UP)
        tag = estimate_tag("the Works, calibrated to Union Pacific's 2025 accounts; 40% of its costs taken as fixed with the track (this series' assumption)", size=12)
        beat(self,
             "Here is why that matters. <bookmark mark='a'/> Suppose two-fifths of a railway's costs come with the track "
             "itself, whatever runs on it. Then the cost of a ton-mile falls steeply as traffic grows. "
             f"<bookmark mark='b'/> On Union Pacific's network, about {Rl['density'] / 1e6:.0f} million ton-miles a year "
             f"pass over each mile of route, and a ton-mile costs about {100 * Rl['avg']:.1f} cents, against "
             f"{100 * Rl['rate']:.1f} cents of revenue. <bookmark mark='c'/> On a quiet branch line with one million, it "
             f"would cost about {100 * Rl['at1']:.0f} cents. <bookmark mark='d'/> Below about "
             f"{Rl['be'] / 1e6:.0f} million, a line loses money at today's prices. The Staggers Act of 1980 rewrote the "
             "rules for selling and abandoning such lines.",
             base=[ch.frame, price, pl, tag], steps=[ch.lines["cost a ton-mile"], m1, m2, m3])

    def prices(self):
        Rl = R["rail"]
        real = Rl["real"]
        ch = line_chart({"rail rates after inflation": (real, RAIL)}, x=(1981, 2026), y=(0.5, 1.1),
                        xticks=[1981, 1990, 2000, 2010, 2020], yticks=[0.6, 0.8, 1.0], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"x{v:.1f}", ylabel="producer prices of line-haul railroads divided by consumer prices, 1981 = 1",
                        width=9.2, height=4.4, center=(-0.6, -0.45), label_end=False)
        lo = min(real, key=real.get)
        last = max(real)
        m1 = marker(ch.ax, lo, real[lo], f"{lo}: x{real[lo]:.2f}", GOOD, side=DOWN)
        m2 = marker(ch.ax, last, real[last], f"{last}: x{real[last]:.2f}", RAIL, side=UP)
        src = source("BLS, PPI for line-haul railroads and CPI-U, annual averages, via FRED", size=12)
        beat(self,
             "What did freedom do to prices? <bookmark mark='a'/> After inflation, the prices railways charged fell for two "
             f"decades, to {100 * (1 - real[lo]):.0f} per cent below 1981's by {lo}. "
             f"<bookmark mark='b'/> Then they rose again, to about {100 * (1 - real[last]):.0f} per cent below 1981's in "
             f"{last}. The shippers got cheaper freight first, and the railways their profits later.",
             base=[ch.frame, src], steps=[ch.lines["rail rates after inflation"], VGroup(m1, m2)])

    def four(self):
        H = R["hook"]["ors"]
        items = [(k, H[k][2025], RAIL, f"{H[k][2025]:.1f}%") for k in ("Union Pacific", "Norfolk Southern", "BNSF", "CSX")]
        items += [("Knight-Swift (truckload)", H["Knight-Swift"][2025], TRUCK, f"{H['Knight-Swift'][2025]:.1f}%")]
        rows = hbars(items, max_value=100, x0=0.4, top=1.8, row=0.8, length=5.6, size=17, bar_h=0.42)
        lab = tx("operating ratio, 2025: costs per dollar of revenue", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K for 2025 via SEC company facts", size=12)
        beat(self,
             "Today's four. <bookmark mark='a'/> Union Pacific spent "
             f"{H['Union Pacific'][2025]:.0f} cents of each dollar in 2025, Norfolk Southern {H['Norfolk Southern'][2025]:.0f}, "
             f"BNSF, owned by Berkshire Hathaway, {H['BNSF'][2025]:.0f}, and CSX {H['CSX'][2025]:.0f}. "
             f"<bookmark mark='b'/> A truckload carrier, {H['Knight-Swift'][2025]:.0f}. The railway's advantage is the "
             "lesson of Run it at enormous scale: one crew moving a long train of containers on track that is already "
             "paid for.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:4]), rows[4]])

    def captive(self):
        q = quote(["'The STB has jurisdiction over rates charged on certain regulated rail traffic; common carrier service",
                   "of regulated traffic; ... abandonment of rail lines; and acquisition of control of rail common carriers'"],
                  "Union Pacific, Form 10-K for 2025, on the Surface Transportation Board", size=17).move_to([0, 1.6, 0])
        g = VGroup(tx("A coal mine or chemical plant on one railway's line has no second railway", 18, RAIL),
                   tx("so the regulator can still be asked whether its rate is reasonable", 18, SKY),
                   tx("and must approve any merger of railways", 18, BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "The catch is the shipper with no choice. <bookmark mark='a'/> The Surface Transportation Board still oversees "
             "rates on some rail traffic, the abandonment of lines and the control of railways. <bookmark mark='b'/> In this "
             "series' reading, a coal mine or a chemical plant served by only one railway is a captive customer, "
             "<bookmark mark='c'/> so the regulator can still be asked whether its rate is reasonable, "
             "<bookmark mark='d'/> and must approve any merger. Chapter ten returns to the biggest one proposed in a "
             "generation.",
             base=[tag], steps=[q, g[0], g[1], g[2]])
