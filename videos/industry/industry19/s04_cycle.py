from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403


class Cycle(VoiceoverScene):
    def construct(self):
        card(self, 3, "Capital goods: the cycle", "Why do machine orders swing so much harder than the economy?",
             "Chapter three. Capital goods. A machine is bought by a business that expects to need it for years, so it is "
             "bought when the business is confident, and put off when it is not.", lit=("change",))
        self.share()
        self.orders()
        self.core()
        self.cat()
        self.deere()

    def deere(self):
        d = {y: v for y, v in R["deere"].items() if 2009 <= y <= 2025}
        ch = line_chart({"Deere": (d, "#A3D977"), "Caterpillar": ({y: v for y, v in R["cycle"]["cat_rev"].items() if 2009 <= y <= 2025}, MACHINE)},
                        x=(2009, 2025), y=(0, 75), xticks=[2009, 2013, 2017, 2021, 2025], yticks=[0, 25, 50, 75],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="sales and revenues, $bn, by fiscal year", width=9.0, height=4.4,
                        center=(-1.0, -0.45))
        ax = ch.ax
        m1 = marker(ax, 2016, d[2016], f"2013 to 2016: {100 * (d[2016] / d[2013] - 1):.0f}%", BAD, side=DOWN)
        m2 = marker(ax, 2025, d[2025], f"2023 to 2025: {100 * (d[2025] / d[2023] - 1):.0f}%", BAD, side=DOWN)
        src = source("Deere & Company and Caterpillar Inc., Forms 10-K, via SEC company facts", size=12)
        beat(self,
             "And not every machine follows the same cycle. <bookmark mark='a'/> Deere sells mostly to farmers. Its sales "
             "fell "
             f"{-100 * (d[2016] / d[2013] - 1):.0f} per cent from 2013 to 2016, <bookmark mark='b'/> then rose to "
             f"{d[2023]:.0f} billion dollars in 2023 <bookmark mark='c'/> and fell "
             f"{-100 * (d[2025] / d[2023] - 1):.0f} per cent in the two years after, <bookmark mark='d'/> while "
             "Caterpillar's sales, driven by builders, miners and now data centres, held up. A farm-machine maker and a "
             "construction-machine maker can be in different seasons at the same time.",
             base=[ch.frame, src], steps=[[ch.lines["Deere"], ch.labels["Deere"], m1], [], m2,
                                         [ch.lines["Caterpillar"], ch.labels["Caterpillar"]]])

    def core(self):
        C = R["cycle"]
        o = {y: v for y, v in C["core"].items() if y <= 2025}
        ch = line_chart({"core orders": (o, PRICE)}, x=(1993, 2025), y=(300, 900), xticks=[1995, 2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[300, 500, 700, 900], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="US orders for capital goods, excluding defence and aircraft, $bn a year", width=9.6, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        ax = ch.ax
        m09 = marker(ax, 2009, o[2009], f"2009: {100 * C['core_fall']:.0f}%", BAD, side=DOWN)
        m25 = marker(ax, 2025, o[2025], f"2025: ${o[2025]:.0f}bn", GOOD, side=LEFT)
        src = source("US Census Bureau, M3 survey: new orders for nondefense capital goods excluding aircraft (via FRED, "
                     "NEWORDER), sums of seasonally adjusted months", size=12)
        beat(self,
             "Economists watch one series in particular: orders for capital goods, leaving out defence and aircraft, whose "
             "big orders make the numbers jump. <bookmark mark='a'/> It is a monthly reading of how much businesses are "
             "willing to invest. <bookmark mark='b'/> In 2009 it fell "
             f"{-100 * C['core_fall']:.0f} per cent. <bookmark mark='c'/> In 2025 American businesses ordered "
             f"{o[2025]:.0f} billion dollars of such equipment. It rises and falls with the machine makers' own orders, "
             "because it is largely the same orders, seen from the buyers' side.",
             base=[ch.frame, src], steps=[ch.lines["core orders"], m09, m25])

    def share(self):
        C = R["cycle"]
        s = {y: 100 * v for y, v in C["eq_share"].items() if y <= 2025}
        ch = line_chart({"equipment": (s, MACHINE)}, x=(1947, 2025), y=(3, 9), xticks=[1950, 1970, 1990, 2010, 2025],
                        yticks=[3, 5, 7, 9], yfmt=lambda v: f"{v:.0f}%", ylabel="US business investment in equipment, % of GDP",
                        width=9.8, height=4.4, center=(-0.4, -0.45), label_end=False)
        ax = ch.ax
        lows = VGroup(*[marker(ax, y, s[y], f"{y}", BAD, side=DOWN, size=13) for y in (1961, 1983, 1992, 2003) if y in s],
                      marker(ax, 2009, s[2009], f"2009: {s[2009]:.1f}%", BAD, side=DOWN, size=13))
        peak = max(s, key=s.get)
        m_pk = marker(ax, peak, s[peak], f"{peak}: {s[peak]:.1f}%", GOOD, side=UP, size=13)
        m25 = marker(ax, 2025, s[2025], f"2025: {s[2025]:.1f}%", PRICE, side=LEFT)
        src = source("US Bureau of Economic Analysis, private fixed investment in equipment, and GDP (via FRED: Y033RC1Q027SBEA, "
                     "GDP), annual averages of quarterly rates", size=12)
        beat(self,
             "Here is what American businesses spend on equipment each year, as a share of everything the economy "
             f"produces, since 1947. <bookmark mark='a'/> It peaked at {s[peak]:.1f} per cent in {peak}, and it moves "
             "with the business cycle: <bookmark mark='b'/> each downturn leaves a dip, and the deepest came in 2009, at "
             f"{s[2009]:.1f} per cent. <bookmark mark='c'/> In 2025 it was {s[2025]:.1f} per cent: about "
             f"{C['eq_level'][2025] / 1e3:.1f} trillion dollars of computers, vehicles, machines and other equipment. A "
             "machine maker's whole market breathes with these swings, and a swing of one point of GDP is hundreds of "
             "billions of dollars of orders won or lost.",
             base=[ch.frame, src], steps=[[ch.lines["equipment"], m_pk], lows, m25])

    def orders(self):
        C = R["cycle"]
        o = {y: v for y, v in C["orders"].items() if y <= 2025}
        s = {y: v for y, v in C["ships"].items() if 1993 <= y <= 2025}
        ch = line_chart({"orders": (o, PRICE), "shipments": (s, BLUE)}, x=(1993, 2025), y=(200, 500),
                        xticks=[1995, 2000, 2005, 2010, 2015, 2020, 2025], yticks=[200, 300, 400, 500],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="US machinery makers, $bn a year (not adjusted for inflation)",
                        width=9.4, height=4.4, center=(-0.8, -0.45), nudge={"orders": 0.15, "shipments": -0.15})
        ax = ch.ax
        m09 = marker(ax, 2009, o[2009], f"2009: orders {100 * C['orders_fall']:.0f}%", BAD, side=DOWN)
        src = source("US Census Bureau, Manufacturers' Shipments, Inventories and Orders: machinery, new orders and "
                     "shipments, seasonally adjusted (via FRED: A33SNO, A33SVS)", size=12)
        beat(self,
             "Now the machinery makers' own orders and shipments since 1993. <bookmark mark='a'/> New orders lead. "
             f"<bookmark mark='b'/> In 2009 they fell {-100 * C['orders_fall']:.0f} per cent in a single year; "
             f"<bookmark mark='c'/> shipments followed, down {-100 * C['ships_fall']:.0f} per cent, as the factories "
             "worked through orders already on their books. The gap between the two lines is the backlog, filling and "
             "emptying.",
             base=[ch.frame, src], steps=[[ch.lines["orders"], ch.labels["orders"]], m09,
                                          [ch.lines["shipments"], ch.labels["shipments"]]])

    def cat(self):
        C = R["cycle"]
        rev = {y: v for y, v in C["cat_rev"].items() if 2009 <= y <= 2025}
        items = [(str(y), v, MACHINE if y not in (2016, 2020, 2009) else BAD, f"{v:.0f}") for y, v in sorted(rev.items())]
        bars_ = vbars(items, base_y=-2.4, height=4.0, width=0.5, gap=0.18, size=12)
        note = VGroup(tx(f"2012 to 2016: {100 * C['cat_fall']:.0f}%", 17, BAD, bold=True),
                      tx(f"2019 to 2020, the pandemic: {100 * C['cat_fall20']:.0f}%", 17, BAD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([2.6, 2.4, 0])
        src = source("Caterpillar Inc., Forms 10-K, via SEC company facts: sales and revenues, $bn", size=12)
        beat(self,
             "And one company through it. Here are Caterpillar's sales and revenues each year since 2009, in billions of "
             "dollars. <bookmark mark='a'/> They doubled from the trough of 2009 to 2012. <bookmark mark='b'/> Then "
             f"they fell {-100 * C['cat_fall']:.0f} per cent in four years. <bookmark mark='c'/> They fell again in the pandemic, by {-100 * C['cat_fall20']:.0f} "
             "per cent, and recovered to new records. A business that can lose two fifths of its sales in four years must "
             "find something steadier to live on.",
             base=[head("Caterpillar's sales and revenues, $bn"), src],
             steps=[VGroup(*bars_[:4]), VGroup(*bars_[4:8]), [VGroup(*bars_[8:]), note]])
