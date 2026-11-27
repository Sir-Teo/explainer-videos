from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Shops(VoiceoverScene):
    def construct(self):
        card(self, 7, "Shops, sheds and the internet", "Who won when shopping moved online?",
             "Chapter seven. Shops, sheds and the internet. Online shopping was supposed to empty the malls. It filled the "
             "warehouses, and the best malls are full too.", lit=("change", "moat"))
        self.ecom()
        self.simon()
        self.macerich()
        self.prologis()
        self.develop()

    def ecom(self):
        T = R["retail"]
        e = T["ecom"]
        ch = line_chart({"online share of retail sales": (e, SHED)}, x=(1999.75, 2026.75), y=(0, 20), xticks=[2000, 2005, 2010, 2015, 2020, 2026],
                        yticks=[0, 5, 10, 15, 20], yfmt=lambda v: f"{v:.0f}%", ylabel="e-commerce as a share of American retail sales (quarterly)",
                        width=9.4, height=4.4, center=(-0.6, -0.45), label_end=False)
        k19 = max(k for k in e if k < 2020)
        k20 = max((k for k in e if 2020 <= k < 2021), key=e.get)
        kn = max(e)
        m1 = marker(ch.ax, k19, e[k19], f"end of 2019: {T['ecom_2019']:.1f}%", ALL, side=LEFT)
        m2 = marker(ch.ax, k20, e[k20], f"2020: {T['ecom_2020']:.1f}%", SHED, side=UP)
        m3 = marker(ch.ax, kn, e[kn], f"2026: {T['ecom_now']:.1f}%", SHED, side=DOWN)
        src = source("Census Bureau, quarterly e-commerce retail sales as a percent of total sales (seasonally adjusted), via FRED", size=12)
        beat(self,
             "In 1999 Americans bought well under one per cent of their retail goods online. <bookmark mark='a'/> By the end "
             f"of 2019, {T['ecom_2019']:.1f} per cent. <bookmark mark='b'/> In the spring of 2020, with shops shut, it jumped "
             f"to {T['ecom_2020']:.0f}. <bookmark mark='c'/> And by the third quarter of 2026, {T['ecom_now']:.1f} per cent. "
             "Every online order is picked from a shelf in a warehouse, not a shop.",
             base=[ch.frame, src], steps=[[ch.lines["online share of retail sales"], m1], m2, m3])

    def simon(self):
        S = R["retail"]["spg"]
        mall = draw.mall(3.2).move_to([-3.8, 0.6, 0])
        c = VGroup(*[VGroup(tx(a, 38, col, bold=True), tx(b, 17, GREY_A)).arrange(DOWN, buff=0.1)
                     for a, b, col in ((f"{S['props']:.0f}", "American malls, outlets and other centres", SHOP),
                                       (f"{S['occ']:.1f}%", "let, end of 2025", GOOD),
                                       (f"${S['rent']:.2f}", "average base rent a square foot, up 4.7%", VALUE))]
                   ).arrange(DOWN, buff=0.4).move_to([3.0, 0.4, 0])
        src = source("Simon Property Group, Form 10-K for 2025", size=12)
        beat(self,
             "Yet the largest mall owner is doing well. <bookmark mark='a'/> Simon owned or held interests in "
             f"{S['props']:.0f} American malls, outlet centres and other shopping centres at the end of 2025. "
             f"<bookmark mark='b'/> They were {S['occ']:.1f} per cent let, <bookmark mark='c'/> and the average base rent rose "
             f"{4.7:.1f} per cent, to {S['rent']:.2f} dollars a square foot. Shoppers still go to the best malls; it is the rest "
             "that have suffered.",
             base=[mall, src], steps=[c[0], c[1], c[2]])

    def macerich(self):
        M = R["retail"]["mac"]
        items = [(str(y), abs(M[y][1]), GOOD if M[y][1] > 0 else BAD, f"{M[y][1]:+.2f}") for y in range(2016, 2026)]
        cols = vbars(items, base_y=-1.8, height=3.0, width=0.7, gap=0.35, size=13, max_value=0.6)
        lab = tx("Macerich, another mall owner: net income, $bn a year", 16, GREY_A).to_edge(UP, buff=0.8)
        mall = draw.mall(1.8).move_to([5.4, 1.8, 0])
        for k in (1, 3, 4):
            mall.stores[k][1].set_fill("#4A5263")
        src = source("Macerich Company, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Further down, <bookmark mark='a'/> Macerich, which owns malls across America, earned "
             f"{M[2016][1]:.2f} billion dollars in 2016, then lost money in 2020 and in each year from 2022 to 2025, about "
             f"{abs(M[2025][1]):.1f} billion in 2025 on {M[2025][0]:.1f} billion of revenue. Same internet, same shoppers; "
             "different malls.",
             base=[lab, mall, src], steps=[cols])

    def prologis(self):
        P = R["retail"]["pld"]
        w = draw.warehouse(3.0, trucks=3).move_to([-3.8, 1.4, 0])
        c = stat_cards([(f"{P['sqft']:.1f}bn sq ft", "owned and managed, 6,500 customers", SHED),
                        (f"{P['amazon']:.1f}%", "of its rent from Amazon, the largest", VALUE),
                        (f"+{P['change']:.0f}%", "rents on leases renewed in 2025", GOOD),
                        (f"{P['mtm']:.0f}%", "by which market rents still beat what tenants pay", INCOME)], y=-0.9, size=30, span=12.4)
        src = source("Prologis, Inc., Form 10-K for 2025", size=12)
        beat(self,
             "Now the sheds. <bookmark mark='a'/> Prologis, in its own words 'the global leader in logistics real estate', owns and manages "
             f"{P['sqft']:.1f} billion square feet for about 6,500 customers. <bookmark mark='b'/> Its largest is Amazon, "
             f"{P['amazon']:.1f} per cent of its rent. <bookmark mark='c'/> Its leases run for years, so rents in force lag "
             f"the market: in 2025, leases that came up for renewal were re-let at about {P['change']:.0f} per cent more. "
             f"<bookmark mark='d'/> And even after that, it reckons the market rent is still {P['mtm']:.0f} per cent above "
             "what its tenants pay, a rise already earned and waiting in the leases.",
             base=[w, src], steps=list(c))

    def develop(self):
        P = R["retail"]["pld"]
        eq = MathTex(r"\text{margin} = \frac{\text{yield on cost}}{\text{cap rate}} - 1 = \frac{%.1f\%%}{%.2f\%%} - 1 = %.1f\%%"
                     % (P["yld"], 100 * P["cap"], P["margin"]), font_size=40, color=WHITE).move_to([0, 1.6, 0])
        g = VGroup(draw.blueprint(1.2), Arrow(LEFT, RIGHT, stroke_color=GREY_B), draw.warehouse(2.2)).arrange(RIGHT, buff=0.4).move_to([0, -0.9, 0])
        cost = tx("cost: $100", 18, LOAN, bold=True).next_to(g[0], DOWN, buff=0.2)
        val = tx(f"worth: ${100 * (1 + P['margin'] / 100):.0f}", 18, VALUE, bold=True).next_to(g[2], DOWN, buff=0.2)
        src = source("Prologis, Inc., Form 10-K for 2025: development stabilizations; this series' arithmetic", size=12)
        beat(self,
             "And Prologis builds. <bookmark mark='a'/> The buildings it finished and filled in 2025 earn "
             f"{P['yld']:.1f} per cent a year on what they cost, and it reckons they are worth {P['margin']:.1f} per cent more "
             f"than they cost. <bookmark mark='b'/> Those two numbers imply that buyers would pay a price yielding "
             f"{100 * P['cap']:.1f} per cent. Development is the gap between the yield on cost and the cap rate: build at "
             "6.7, sell at 5.3, and a hundred dollars of steel and concrete becomes a hundred and twenty-five dollars of "
             "building.",
             base=[src], steps=[eq, [g, cost, val]])
