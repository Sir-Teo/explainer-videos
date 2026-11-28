from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.sales()
        self.prices()
        self.jobs()
        self.retail()
        self.ecom()

    def sales(self):
        G = R["traffic"]["grocery"]
        items = [(str(y), G[y], GROCER if y != 2020 else MASS, f"${G[y]:.0f}bn") for y in (2000, 2010, 2019, 2020, 2025)]
        cols = vbars(items, base_y=-2.0, height=3.6, width=1.3, gap=0.6, size=16, max_value=1000)
        hd = tx("Intermission: food, prices and people", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        lab = tx("sales of American grocery stores, $bn a year", 17, GREY_A).to_edge(UP, buff=1.0)
        src = source("Census Bureau, monthly retail sales of grocery stores (seasonally adjusted), via FRED", size=12)
        beat(self,
             "An intermission, and four pictures. <bookmark mark='a'/> Americans spent about "
             f"{G[2000]:.0f} billion dollars at grocery stores in 2000 and {G[2019]:.0f} billion in 2019. "
             f"<bookmark mark='b'/> In 2020, with restaurants shut, {G[2020]:.0f} billion. <bookmark mark='c'/> In 2025, "
             f"{G[2025]:.0f} billion: a little more than in 2020, mostly because prices rose.",
             base=[hd, lab, src], steps=[VGroup(*cols[:3]), cols[3], cols[4]])

    def prices(self):
        T = R["traffic"]
        ch = line_chart({"food at home": (T["food"], GROCER), "all consumer prices": (T["cpi"], GREY_B)}, x=(2015, 2027), y=(85, 140),
                        xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[90, 100, 110, 120, 130, 140], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:.0f}", ylabel="consumer price indexes, December 2019 = 100", width=8.8, height=4.4, center=(-1.2, -0.45))
        f, c = T["food_a"], T["cpi_a"]
        src = source("BLS, CPI-U for food at home and all items, via FRED", size=12)
        beat(self,
             "Second, prices. <bookmark mark='a'/> Prices in general rose about "
             f"{100 * (c[2025] / c[2019] - 1):.0f} per cent from 2019 to 2025. <bookmark mark='b'/> Food bought to eat at "
             f"home rose {100 * (f[2025] / f[2019] - 1):.0f} per cent, most of it in 2022 and 2023. Shoppers noticed, and "
             "grocers took much of the blame, though their margins, as chapter two showed, stayed thin.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["all consumer prices"], ch.labels["all consumer prices"]),
                                         VGroup(ch.lines["food at home"], ch.labels["food at home"])])

    def jobs(self):
        J = R["traffic"]["jobs"]
        ch = line_chart({"food and beverage stores": (J, MASS)}, x=(2000, 2027), y=(2600, 3400), xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[2600, 2800, 3000, 3200, 3400], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v / 1e3:.1f}m",
                        ylabel="Americans employed by food and beverage stores (seasonally adjusted)", width=9.2, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        last = max(J)
        m = marker(ch.ax, last, J[last], f"2026: {J[last] / 1e3:.2f}m", MASS, side=DOWN)
        src = source("BLS, all employees in food and beverage stores, via FRED", size=12)
        beat(self,
             "Third, the people. <bookmark mark='a'/> Grocery and drink stores employ about "
             f"{J[last] / 1e6 * 1e3:.1f} million Americans, <bookmark mark='b'/> close to the most on this record. "
             "Self-checkouts have spread, but stores still need people to stock, cut, pick online orders and keep the "
             "shelves full.",
             base=[ch.frame, src], steps=[ch.lines["food and beverage stores"], m])

    def retail(self):
        J = R["traffic"]["retail"]
        ch = line_chart({"retail trade": (J, MASS)}, x=(2000, 2027), y=(13000, 17000), xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[13000, 14000, 15000, 16000, 17000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v / 1e3:.0f}m",
                        ylabel="Americans employed in retail trade (seasonally adjusted)", width=9.2, height=4.4, center=(-0.6, -0.45),
                        label_end=False)
        last = max(J)
        m = marker(ch.ax, last, J[last], f"2026: {J[last] / 1e3:.1f}m", MASS, side=DOWN)
        src = source("BLS, all employees in retail trade, via FRED", size=12)
        beat(self,
             "And all of retail together. <bookmark mark='a'/> Between thirteen and sixteen million Americans have worked in "
             f"shops of every kind through this century, <bookmark mark='b'/> {J[last] / 1e3:.1f} million in 2026. In this "
             "series' reading, retail is one of the country's largest employers, which is why its wages and its automation are "
             "political questions as well as business ones.",
             base=[ch.frame, src], steps=[ch.lines["retail trade"], m])

    def ecom(self):
        E = R["traffic"]["ecom"]
        ch = line_chart({"online share": (E, ONLINE)}, x=(2000, 2027), y=(0, 20), xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[0, 5, 10, 15, 20], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}%",
                        ylabel="e-commerce as a share of American retail sales (seasonally adjusted)", width=9.2, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        last = max(E)
        m = marker(ch.ax, last, E[last], f"2026: {E[last]:.1f}%", ONLINE, side=LEFT)
        src = source("Census Bureau, quarterly e-commerce retail sales as a percent of total, via FRED", size=12)
        beat(self,
             "And fourth, the screen. <bookmark mark='a'/> Online sales were about one per cent of American retail in "
             f"2000. <bookmark mark='b'/> By 2026, {E[last]:.0f} per cent. Groceries are the hardest thing to sell online, "
             "chilled, heavy and wanted within hours, and chapter eight shows what that costs.",
             base=[ch.frame, src], steps=[ch.lines["online share"], m])
