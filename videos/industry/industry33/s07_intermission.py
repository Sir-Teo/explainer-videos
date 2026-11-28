from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.sales()
        self.ratio()
        self.jobs()
        self.margins()

    def sales(self):
        S = R["traffic"]["sales"]
        ys = [1992, 2000, 2010, 2019, 2022, 2025]
        items = [(str(y), S[y], GOODS, f"${S[y]:.1f}trn") for y in ys]
        cols = vbars(items, base_y=-2.2, height=3.8, width=1.1, gap=0.5, size=16, max_value=9)
        hd = tx("Intermission: the hidden trillions", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        lab = tx("sales of American merchant wholesalers, $ trillion a year", 18, GREY_A).to_edge(UP, buff=1.0)
        src = source("Census Bureau, monthly wholesale trade (seasonally adjusted), via FRED", size=12)
        beat(self,
             "An intermission, and four pictures of the part of the economy nobody sees. <bookmark mark='a'/> American "
             f"merchant wholesalers sold about {S[1992]:.1f} trillion dollars of goods in 1992, <bookmark mark='b'/> "
             f"{S[2010]:.1f} trillion in 2010, <bookmark mark='c'/> and {S[2025]:.1f} trillion in 2025: more than all American "
             "shops sold, because much of what wholesalers sell goes to factories, builders, hospitals and restaurants, not "
             "only to shops.",
             base=[hd, lab, src], steps=[VGroup(*cols[:2]), VGroup(*cols[2:4]), VGroup(*cols[4:])])

    def ratio(self):
        Rt = R["traffic"]["ratio"]
        ch = line_chart({"months of stock": (Rt, IND)}, x=(1992, 2027), y=(1.0, 1.8), xticks=[1995, 2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[1.0, 1.2, 1.4, 1.6, 1.8], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.1f}",
                        ylabel="merchant wholesalers' inventories over a month's sales (seasonally adjusted)", width=9.2, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        f, l = min(Rt), max(Rt)
        m1 = marker(ch.ax, f, Rt[f], f"1992: {Rt[f]:.2f}", IND, side=UP + RIGHT)
        m2 = marker(ch.ax, l, Rt[l], f"2026: {Rt[l]:.2f}", IND, side=DOWN + LEFT)
        src = source("Census Bureau, wholesale inventories to sales ratio, via FRED", size=12)
        beat(self,
             "Second, the stock. <bookmark mark='a'/> In 1992 wholesalers held "
             f"{Rt[f]:.2f} months of sales on their shelves. <bookmark mark='b'/> In 2026, {Rt[l]:.2f}. Better forecasting, "
             "faster trucks and daily orders have let them carry less for each dollar they sell, though the ratio jumped "
             "when demand collapsed in 2009, for a few weeks in the spring of 2020, and again in 2022 and 2023 as firms "
             "rebuilt their stocks after the shortages.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["months of stock"], m1), m2])

    def jobs(self):
        J = R["traffic"]["jobs"]
        ch = line_chart({"wholesale trade": (J, DRUG)}, x=(1990, 2027), y=(4500, 6500), xticks=[1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[4500, 5000, 5500, 6000, 6500], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v / 1e3:.1f}m",
                        ylabel="Americans employed in wholesale trade (seasonally adjusted)", width=9.2, height=4.4, center=(-0.6, -0.45),
                        label_end=False)
        last = max(J)
        k00 = near(J, 2000.0)
        m1 = marker(ch.ax, k00, J[k00], f"2000: {J[k00] / 1e3:.2f}m", DRUG, side=UP)
        m2 = marker(ch.ax, last, J[last], f"2026: {J[last] / 1e3:.2f}m", DRUG, side=DOWN + LEFT)
        src = source("BLS, all employees in wholesale trade, via FRED", size=12)
        beat(self,
             "Third, the people. <bookmark mark='a'/> In 2000, at the height of the forecasts that the internet would cut "
             f"out the middleman, {J[k00] / 1e3:.1f} million Americans worked in wholesale trade. <bookmark mark='b'/> In "
             f"2026, {J[last] / 1e3:.2f} million: about the same, with the economy far larger. The jobs changed, from order "
             "clerks to warehouse and software work, but the middlemen did not go away.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["wholesale trade"], m1), m2])

    def margins(self):
        T = R["traffic"]
        base = near(T["cpi"], 2005.5)
        cpi = {k: 100 * v / T["cpi"][base] for k, v in T["cpi"].items()}
        bd = near(T["ppi_d"], 2005.5)
        bn_ = near(T["ppi_n"], 2005.5)
        d = {k: 100 * v / T["ppi_d"][bd] for k, v in T["ppi_d"].items() if k >= 2005}
        n = {k: 100 * v / T["ppi_n"][bn_] for k, v in T["ppi_n"].items() if k >= 2005}
        ch = line_chart({"durable goods wholesalers' margins": (d, IND), "nondurable goods wholesalers' margins": (n, FOOD),
                         "all consumer prices": ({k: v for k, v in cpi.items() if k >= 2005}, GREY_B)},
                        x=(2005, 2027), y=(80, 260), xticks=[2005, 2010, 2015, 2020, 2025], yticks=[100, 150, 200, 250],
                        xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}", ylabel="price indexes, mid-2005 = 100",
                        width=8.4, height=4.4, center=(-1.6, -0.45), nudge={"all consumer prices": -0.2, "nondurable goods wholesalers' margins": 0.18,
                                                                    "durable goods wholesalers' margins": -0.18})
        src = source("BLS, producer price indexes for merchant wholesalers (margins) and the CPI, via FRED", size=12)
        dl, nl, cl = d[max(d)], n[max(n)], cpi[max(cpi)]
        beat(self,
             "And fourth, the price of the service itself. The Bureau of Labor Statistics measures what wholesalers charge "
             "for what they do: the margin between what they pay and what they sell for. <bookmark mark='a'/> Since 2005 "
             f"consumer prices have risen to {cl:.0f} on this scale. <bookmark mark='b'/> Wholesalers' margins on durable "
             f"goods to {dl:.0f}, <bookmark mark='c'/> and on everything else to {nl:.0f}, with a jump during the shortages "
             "of 2021 and 2022. Whatever the internet did, it did not make the middleman's service cheap.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["all consumer prices"], ch.labels["all consumer prices"]),
                                         VGroup(ch.lines["durable goods wholesalers' margins"], ch.labels["durable goods wholesalers' margins"]),
                                         VGroup(ch.lines["nondurable goods wholesalers' margins"], ch.labels["nondurable goods wholesalers' margins"])])
