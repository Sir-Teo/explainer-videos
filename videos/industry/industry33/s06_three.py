from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Three(VoiceoverScene):
    def construct(self):
        card(self, 5, "Why three", "Why do a few distributors handle most of a market?",
             "Chapter five. Why three. America has three big drug wholesalers, a handful of national food distributors and a "
             "few national industrial suppliers. Density is the reason.", lit=("moat",))
        self.town()
        self.curve()
        self.size()
        self.customers()

    def town(self):
        import random
        rng = random.Random(4)
        pts = [(rng.uniform(-6.0, -1.0), rng.uniform(-2.2, 2.2)) for _ in range(40)]
        dots = VGroup(*[Dot([x, y, 0], radius=0.07, color=GREY_B) for x, y in pts])
        mine = VGroup(*[Dot([x, y, 0], radius=0.11, color=DRUG) for x, y in pts[:4]])
        big = VGroup(*[Dot([x + 7.0, y, 0], radius=0.11, color=DRUG) for x, y in pts[:16]])
        dots2 = VGroup(*[Dot([x + 7.0, y, 0], radius=0.07, color=GREY_B) for x, y in pts])
        path1 = VMobject(stroke_color=DRUG, stroke_width=2).set_points_as_corners([[-3.5, -2.6, 0]] + [[x, y, 0] for x, y in pts[:4]] + [[-3.5, -2.6, 0]])
        o = sorted(pts[:16], key=lambda p: (p[0] > -3.5, p[1] if p[0] <= -3.5 else -p[1]))
        path2 = VMobject(stroke_color=DRUG, stroke_width=2).set_points_as_corners([[3.5, -2.6, 0]] + [[x + 7.0, y, 0] for x, y in o] + [[3.5, -2.6, 0]])
        l1 = tx("10% of the town's pharmacies: long drives between stops", 15, GREY_A).move_to([-3.5, 2.7, 0])
        l2 = tx("40%: the same day's driving reaches far more of them", 15, GREY_A).move_to([3.5, 2.7, 0])
        tag = estimate_tag("illustration", size=12)
        beat(self,
             "Picture a town with forty pharmacies. <bookmark mark='a'/> A wholesaler that serves four of them drives a long "
             "way between stops; most of its driver's day is spent on the road. <bookmark mark='b'/> A wholesaler that serves "
             "sixteen finds its customers a few streets apart. The truck, the driver and the fuel cost about the same per "
             "day; the second wholesaler spreads them over far more deliveries.",
             base=[dots, dots2, tag], steps=[VGroup(mine, path1, l1), VGroup(big, path2, l2)])

    def curve(self):
        U = R["run"]
        Rt = U["route"]
        cps = {100 * s: v["cps"] for s, v in Rt.items()}
        ch = line_chart({"cost a stop": (cps, DRUG)}, x=(0, 60), y=(25, 50), xticks=[0, 10, 20, 30, 40, 50, 60], yticks=[25, 30, 35, 40, 45, 50],
                        xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: f"${v:.0f}",
                        ylabel="the Works: a delivery's cost, by the share of the town's pharmacies served", width=8.6, height=4.3,
                        center=(-1.0, -0.45), label_end=False)
        a, b = Rt[0.1], Rt[0.4]
        m1 = marker(ch.ax, 10, a["cps"], f"10%: ${a['cps']:.0f}, {a['stops']:.0f} stops a day", BAD, side=UP + RIGHT)
        m2 = marker(ch.ax, 40, b["cps"], f"40%: ${b['cps']:.0f}, {b['stops']:.0f} stops", GOOD, side=UP)
        tag = estimate_tag(f"the Works: a truck and driver cost ${U['route_cost']:.0f} a day; ${U['route_drop']:,.0f} of goods a stop", size=12)
        beat(self,
             f"<bookmark mark='a'/> In the Works, a truck and driver cost {U['route_cost']:.0f} dollars a day. Serving a tenth "
             f"of a town's pharmacies, a driver manages {a['stops']:.0f} stops, at {a['cps']:.0f} dollars each. "
             f"<bookmark mark='b'/> Serving two-fifths, {b['stops']:.0f} stops, at {b['cps']:.0f} dollars. On a delivery of "
             f"{U['route_drop']:,.0f} dollars of medicine the difference is {100 * (a['share'] - b['share']):.2f} cents on the "
             f"dollar: about a tenth of the whole operating margin of {100 * (U['gm'] - U['opex']):.1f} cents. In a business "
             "this thin, the biggest local player can undercut the rest and still earn more.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["cost a stop"], m1), m2])

    def size(self):
        T = R["traffic"]
        H = R["hook"]
        y = max(T["drugs"])
        items = [("the three wholesalers' revenue, latest fiscal years", H["big3_rev"], DRUG, f"${H['big3_rev']:.0f}bn"),
                 (f"all American wholesalers of drugs, {y} (Census)", T["drugs"][y] * 1e3, GOODS, f"${T['drugs'][y] * 1e3:,.0f}bn")]
        rows = hbars(items, max_value=1400, x0=-0.4, top=1.0, row=1.4, length=6.4, size=17, bar_h=0.7)
        note = tx("not like for like: the companies' revenue includes Canada and other businesses, and their fiscal years differ", 15, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("Forms 10-K via SEC company facts; Census Bureau, monthly wholesale trade, via FRED", size=12)
        tag = estimate_tag("this series' reading", size=12).next_to(note, UP, buff=0.15)
        beat(self,
             "How much of the market do the three hold? The numbers are not quite comparable, but they give the scale. "
             f"<bookmark mark='a'/> The three took in {H['big3_rev']:.0f} billion dollars in their latest years. "
             f"<bookmark mark='b'/> America's merchant wholesalers of drugs, all of them, sold about "
             f"{T['drugs'][y] * 1e3:,.0f} billion in {y}. Allowing for the parts of the three's revenue earned abroad or "
             "outside drug wholesaling, in this series' reading they handle the great majority of America's medicines.",
             base=[rows.axis, note, src, tag], steps=[rows[0], rows[1]])

    def customers(self):
        P = R["power"]
        rows = [["", "largest customer", "share of revenue"],
                ["McKesson", "CVS Health", f"{P['cvs']:.0f}%"],
                ["", "next two together", f"{P['next2']:.0f}%"],
                ["Cencora", "Walgreens", f"{P['wag']:.0f}%"],
                ["", "Evernorth Health Services", f"{P['evernorth']:.0f}%"]]
        cols = [None, [DRUG, WHITE, TRADE], [DRUG, WHITE, TRADE], [DRUG, WHITE, TRADE], [DRUG, WHITE, TRADE]]
        t = table(rows, col_x=[-5.6, -2.2, 2.6], top=1.6, row_h=0.8, size=19, colors=cols)
        src = source("McKesson and Cencora, Forms 10-K for fiscal 2026", size=12)
        beat(self,
             "And the customers are concentrated too. <bookmark mark='a'/> CVS Health alone bought "
             f"{P['cvs']:.0f} per cent of everything McKesson sold in its last year, <bookmark mark='b'/> and its next two "
             f"customers another {P['next2']:.0f}. <bookmark mark='c'/> Walgreens bought {P['wag']:.0f} per cent of "
             f"Cencora's, <bookmark mark='d'/> and Evernorth Health Services {P['evernorth']:.0f}. A few huge "
             "buyers, a few huge sellers, and three wholesalers in between, each needing the others' volume to keep its "
             "trucks full.",
             base=[t[0], src], steps=[t[1], t[2], t[3], t[4]])
