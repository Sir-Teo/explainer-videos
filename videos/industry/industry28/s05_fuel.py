from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403


class Fuel(VoiceoverScene):
    def construct(self):
        card(self, 4, "Fuel and the war", "What happens to an airline when oil jumps?",
             "Chapter four. Fuel and the war. An airline's second-largest cost is set in oil markets it cannot control, and in "
             "2026 that market was upended.", lit=("change", "make"))
        self.history()
        self.spike()
        self.year()
        self.hit()
        self.passon()
        self.efficiency()

    def history(self):
        F = R["fuel"]
        ch = line_chart({"jet fuel": (F["monthly"], FUEL)}, x=(2000, 2027), y=(0, 5), xticks=[2000, 2005, 2008, 2012, 2016, 2020, 2022, 2026],
                        yticks=[0, 1, 2, 3, 4, 5], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}",
                        ylabel="jet fuel, US Gulf Coast, dollars a gallon (monthly)", width=9.4, height=4.4, center=(-0.6, -0.45),
                        label_end=False)
        a = F["annual"]
        m1 = marker(ch.ax, 2020.5, a[2020], f"2020: ${a[2020]:.2f}", GOOD, side=DOWN)
        m2 = marker(ch.ax, 2022.5, a[2022], f"2022: ${a[2022]:.2f}", BAD, side=UP)
        m3 = marker(ch.ax, 2025.5, a[2025], f"2025: ${a[2025]:.2f}", ALL, side=DOWN)
        src = source("EIA, kerosene-type jet fuel, US Gulf Coast (monthly), via FRED", size=12)
        beat(self,
             "Jet fuel's price, a gallon at a time. <bookmark mark='a'/> In 2020, with the planes grounded, it averaged "
             f"{a[2020]:.2f} dollars. <bookmark mark='b'/> In 2022, after Russia invaded Ukraine, {a[2022]:.2f}. "
             f"<bookmark mark='c'/> In 2025, {a[2025]:.2f}. Delta burned {R['fuel']['gallons'] / 1e3:.1f} billion gallons in "
             "2025: every ten cents is more than four hundred million dollars.",
             base=[ch.frame, src], steps=[[ch.lines["jet fuel"], m1], m2, m3])

    def spike(self):
        M = R["fuel"]["m26"]
        mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        items = [(mon[int(m[5:7]) - 1] + ("\n" + m[:4] if m[5:7] in ("07", "01") else ""), v, BAD if v > 3 else FUEL, f"{v:.2f}")
                 for m, v in M.items()]
        cols = vbars(items, base_y=-2.2, height=3.8, width=0.62, gap=0.24, size=12, max_value=4.2)
        lab = tx("jet fuel, US Gulf Coast, dollars a gallon, month by month", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("EIA, kerosene-type jet fuel, US Gulf Coast (monthly), via FRED", size=12)
        k = list(M).index("2026-03")
        beat(self,
             "Now zoom in on the last year. <bookmark mark='a'/> Through the second half of 2025 and into February 2026, a "
             f"gallon cost a little over two dollars. <bookmark mark='b'/> In March 2026, with the Strait of Hormuz all but "
             f"closed, it jumped to {M['2026-03']:.2f}, and by May to {M['2026-05']:.2f}: in two months, almost double. "
             f"<bookmark mark='c'/> In August it was still {M['2026-08']:.2f}.",
             base=[lab, src], steps=[VGroup(*cols[:k]), VGroup(*cols[k:k + 3]), VGroup(*cols[k + 3:])])

    def year(self):
        F = R["fuel"]
        items = [("2025, the year", F["dal25"], ALL, f"${F['dal25']:.2f}"), ("Q2 2026, expected", F["q2"], BAD, f"${F['q2']:.2f}"),
                 ("Q3 2026, expected", F["q3"], FUEL, f"${F['q3']:.2f}"), ("Q4 2026, expected", F["q4"], BAD, f"${F['q4']:.2f}")]
        rows = hbars(items, max_value=4.6, x0=-0.4, top=1.6, row=0.85, length=6.2, size=17, bar_h=0.45)
        lab = tx("Delta: all-in price of a gallon of fuel", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Delta Air Lines, Form 10-K for 2025 and results releases of April, July and October 2026", size=12)
        beat(self,
             f"Now Delta's own fuel. <bookmark mark='a'/> In 2025 it paid {F['dal25']:.2f} dollars a gallon, all in. "
             f"<bookmark mark='b'/> In April 2026, with war in the Gulf, it expected about {F['q2']:.2f} for the second "
             f"quarter. <bookmark mark='c'/> By July, {F['q3']:.2f} for the third. <bookmark mark='d'/> In October, "
             f"{F['q4']:.2f} again for the fourth.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2], rows[3]])

    def hit(self):
        C = R["called"]
        q = quote(["'For the full year, we expect to generate a pre-tax profit of roughly $4.5 billion, absorbing a $6 billion",
                   "increase in fuel costs.'"], "Delta Air Lines, results release of 9 October 2026", size=18).move_to([0, 1.4, 0])
        c = stat_cards([(f"${C['hit']:.0f}bn", "more for fuel in 2026", BAD), (f"${C['pretax']:.1f}bn", "pre-tax profit left", GOOD)],
                       y=-0.9, size=44, span=8)
        src = source("Delta Air Lines, results release of 9 October 2026 (Form 8-K)", size=12)
        beat(self,
             "What that does to a year. <bookmark mark='a'/> In October, Delta said it expected a pre-tax profit of roughly "
             f"{C['pretax']:.1f} billion dollars for 2026, 'absorbing a {C['hit']:.0f} billion dollar increase in fuel costs'. "
             f"<bookmark mark='b'/> Six billion dollars of extra fuel, more than the whole profit it expected to keep. "
             "<bookmark mark='c'/> And Delta is partly hedged by owning a refinery: its outlook for the last quarter counted a "
             "refinery benefit of about forty cents a gallon.",
             base=[src], steps=[q, c[0], c[1]])

    def passon(self):
        F = R["fuel"]["fares26"]
        mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        items = [(mon[int(m[5:7]) - 1], v, BAD if v > 15 else FUEL, f"+{v:.0f}%") for m, v in F.items()]
        cols = vbars(items, base_y=-2.0, height=3.4, width=0.8, gap=0.35, size=13, max_value=30)
        lab = tx("American airline fares in 2026, change from the same month of 2025 (consumer price index)", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("BLS, CPI-U for airline fares, not seasonally adjusted, via FRED", size=12)
        beat(self,
             "Did the airlines pass it on? <bookmark mark='a'/> In January and February 2026, fares were a few per cent "
             f"above a year before. <bookmark mark='b'/> From March they climbed, and by May they were {F['2026-05']:.0f} per "
             f"cent higher than in May 2025. <bookmark mark='c'/> Through the summer they stayed more than a fifth higher. "
             "When every airline's main variable cost rises at once, they can all raise fares at once; what none of them can "
             "do is raise fares on seats already sold, which is why the profits fell first.",
             base=[lab, src], steps=[VGroup(*cols[:2]), VGroup(*cols[2:5]), VGroup(*cols[5:])])

    def efficiency(self):
        F = R["fuel"]
        a, b = F["mpg"]
        items = [("2022", a, ALL, f"{a:.1f}"), ("2025", b, GOOD, f"{b:.1f}")]
        rows = hbars(items, max_value=90, x0=-0.4, top=1.0, row=1.2, length=6.4, size=18, bar_h=0.6)
        lab = tx("Southwest: seat-miles flown per gallon of fuel", 17, GREY_A).to_edge(UP, buff=0.8)
        plane = draw.plane(2.4).move_to([0, -2.0, 0])
        src = source("Southwest Airlines, Form 10-K for 2025", size=12)
        beat(self,
             "The one defence an airline controls is the aircraft. <bookmark mark='a'/> Southwest flew "
             f"{a:.1f} seat-miles on a gallon of fuel in 2022 <bookmark mark='b'/> and {b:.1f} in 2025, as newer, more "
             f"efficient planes replaced old ones: {100 * (b / a - 1):.0f} per cent more for the same gallon. It takes years "
             "and billions of dollars, and it still leaves the airline exposed to the price.",
             base=[lab, plane, src], steps=[rows[0], rows[1]])
