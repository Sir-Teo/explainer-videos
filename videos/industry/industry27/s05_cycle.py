from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Cycle(VoiceoverScene):
    def construct(self):
        card(self, 4, "Fortune and ruin", "What happened to freight rates after 2020, and to the lines that charge them?",
             "Chapter four. Fortune and ruin. Run it's cycle, in real companies' accounts.", lit=("change", "dollar"))
        self.rates()
        self.quarters()
        self.index()
        self.zim()
        self.maersk()
        self.supply()

    def rates(self):
        C = R["cycle"]
        r = C["rate"]
        ch = line_chart({"ZIM's average freight rate": (r, RATE)}, x=(2016, 2025), y=(0, 3600),
                        xticks=[2016, 2018, 2020, 2022, 2024, 2025], yticks=[0, 1000, 2000, 3000], yfmt=lambda v: f"${v:,.0f}",
                        ylabel="ZIM: average freight per TEU carried, each year", width=9.2, height=4.4, center=(-0.8, -0.45),
                        label_end=False)
        m1 = marker(ch.ax, 2019, r[2019], f"2019: ${r[2019]:,.0f}", ALL, side=UP)
        m2 = marker(ch.ax, 2022, r[2022], f"2022: ${r[2022]:,.0f}", BAD, side=UP)
        m3 = marker(ch.ax, 2023, r[2023], f"2023: ${r[2023]:,.0f}", GOOD, side=DOWN)
        src = source("ZIM Integrated Shipping Services, Forms 20-F for 2020, 2021, 2023 and 2025", size=12)
        beat(self,
             "ZIM, an Israeli container line, reports what it was paid on average to carry each TEU. <bookmark mark='a'/> "
             f"From 2016 to 2019, about a thousand dollars: {r[2019]:,.0f} in 2019. <bookmark mark='b'/> Then the "
             f"pandemic years, when every box seemed to be wanted at once. By 2022 ZIM's average was {r[2022]:,.0f} dollars, "
             f"more than three times as much. <bookmark mark='c'/> In 2023 it was back to {r[2023]:,.0f}.",
             base=[ch.frame, src], steps=[[ch.lines["ZIM's average freight rate"], m1], m2, m3])

    def quarters(self):
        Q = R["cycle"]["q"]
        items = [(q[2:].replace("Q", " Q"), v, BAD if v > 2000 else (RATE if v > 1500 else GOOD), f"${v:,.0f}") for q, v in Q.items()]
        cols = vbars(items, base_y=-2.0, height=3.6, width=0.9, gap=0.5, size=15, max_value=2700)
        lab = tx("ZIM: average freight per TEU, each quarter", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("ZIM, quarterly results, Forms 6-K of March, May, August and November 2026", size=12)
        beat(self,
             "And it has not stopped moving. <bookmark mark='a'/> Through 2025 and into early 2026, ZIM's average fell, to "
             f"{Q['2026Q1']:,.0f} dollars in the first quarter of 2026. <bookmark mark='b'/> In the third quarter it jumped to "
             f"{Q['2026Q3']:,.0f}, up more than half on a year before. ZIM credited 'continued strong market demand and "
             "favorable momentum in freight rates'; it was also the quarter in which, as chapter six shows, war had all but "
             "closed the Strait of Hormuz.",
             base=[lab, src], steps=[VGroup(*cols[:5]), VGroup(*cols[5:])])

    def index(self):
        P = R["cycle"]["ppi_m"]
        ch = line_chart({"deep-sea freight prices": (P, RATE)}, x=(2015, 2027), y=(0.6, 1.8), xticks=[2015, 2017, 2019, 2021, 2023, 2025, 2027],
                        yticks=[0.8, 1.0, 1.2, 1.4, 1.6], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"x{v:.1f}",
                        ylabel="producer prices for deep-sea freight, monthly, 2019 = 1", width=9.2, height=4.4, center=(-0.6, -0.45),
                        label_end=False)
        k = max(P, key=P.get)
        last = max(P)
        m1 = marker(ch.ax, k, P[k], f"peak: x{P[k]:.2f}", BAD, side=UP)
        m2 = marker(ch.ax, last, P[last], f"Oct 2026: x{P[last]:.2f}", RATE, side=LEFT)
        src = source("BLS, producer price index for deep sea freight transportation, via FRED", size=12)
        beat(self,
             "An official index tells the same story more gently. <bookmark mark='a'/> The Bureau of Labor Statistics' "
             f"producer prices for deep-sea freight peaked at {P[k]:.2f} times their 2019 level, <bookmark mark='b'/> and in "
             f"October 2026 stood at {P[last]:.2f}. It moves less than ZIM's average because it includes contracts set months "
             "ahead; the spot market, and the lines' profits, move far more.",
             base=[ch.frame, src], steps=[[ch.lines["deep-sea freight prices"], m1], m2])

    def zim(self):
        Z = R["cycle"]["zim"]
        items = [(str(y), abs(Z[y][1]), GOOD if Z[y][1] > 0 else BAD, f"{Z[y][1]:+.1f}") for y in range(2018, 2026)]
        cols = vbars(items, base_y=-1.9, height=3.4, width=0.8, gap=0.5, size=15, max_value=5)
        lab = tx("ZIM: net income, $bn a year", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("ZIM Integrated Shipping Services, Forms 20-F via SEC company facts", size=12)
        beat(self,
             "What that did to the company. <bookmark mark='a'/> ZIM lost money in 2018 and 2019. <bookmark mark='b'/> It "
             f"earned {Z[2021][1]:.1f} billion dollars in 2021 and {Z[2022][1]:.1f} billion in 2022, on revenue of "
             f"{Z[2022][0]:.1f} billion: more than a third of every dollar kept as profit. <bookmark mark='c'/> In 2023 it lost "
             f"{abs(Z[2023][1]):.1f} billion. Fortune and ruin, two years apart.",
             base=[lab, src], steps=[VGroup(*cols[:2]), VGroup(*cols[2:5]), VGroup(*cols[5:])])

    def maersk(self):
        M = R["cycle"]["maersk"]
        items = [(str(y), M[y][1], BAD if M[y][1] > 10 else RATE, f"${M[y][1]:.1f}bn") for y in range(2019, 2026)]
        cols = vbars(items, base_y=-1.9, height=3.6, width=0.9, gap=0.5, size=15, max_value=32)
        lab = tx("A.P. Moller-Maersk: operating profit (EBIT), $bn a year", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("A.P. Moller - Maersk, annual reports (ESEF filings via filings.xbrl.org)", size=12)
        beat(self,
             "The largest listed line tells the same story at greater size. <bookmark mark='a'/> Maersk made "
             f"{M[2019][1]:.1f} billion dollars of operating profit in 2019. <bookmark mark='b'/> In 2022, "
             f"{M[2022][1]:.1f} billion, on revenue of {M[2022][0]:.0f} billion. <bookmark mark='c'/> In 2025, "
             f"{M[2025][1]:.1f} billion. The two pandemic years earned it more than the other five together.",
             base=[lab, src], steps=[VGroup(*cols[:1]), VGroup(*cols[1:4]), VGroup(*cols[4:])])

    def supply(self):
        G = R["box"]["g"]
        items = [("2024", G["g24"], None), ("2025", G["g25"], G["d25"]), ("2026", G["g26"], G["d26"])]
        rows = VGroup()
        for i, (y, g, d) in enumerate(items):
            yy = 1.4 - 1.2 * i
            b1 = Rectangle(width=0.5 * g, height=0.4, stroke_width=0, fill_color=SHIP, fill_opacity=0.9).move_to([-1.0 + 0.25 * g, yy + 0.22, 0])
            l1 = tx(f"ships +{g:.1f}%", 15, SHIP, bold=True).next_to(b1, RIGHT, buff=0.12)
            grp = VGroup(tx(y + ("" if y != "2026" else " (forecast)"), 17, WHITE).move_to([-3.4, yy, 0]), b1, l1)
            if d is not None:
                b2 = Rectangle(width=0.5 * d, height=0.4, stroke_width=0, fill_color=BOX, fill_opacity=0.9).move_to([-1.0 + 0.25 * d, yy - 0.24, 0])
                grp.add(b2, tx(f"cargo +{d:.1f}%", 15, BOX, bold=True).next_to(b2, RIGHT, buff=0.12))
            rows.add(grp)
        lab = tx("growth of the world's container fleet against growth of the cargo", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Alphaliner, as quoted in ZIM's Form 20-F for 2025", size=12)
        beat(self,
             "Why the rates fell after 2022 is Run it's answer. <bookmark mark='a'/> The ships ordered in the boom arrived: "
             f"the fleet grew {G['g24']:.1f} per cent in 2024. <bookmark mark='b'/> In 2025 it grew {G['g25']:.1f} per cent "
             f"while the cargo grew {G['d25']:.1f}. <bookmark mark='c'/> For 2026 the forecast was {G['g26']:.1f} per cent more "
             f"ships for {G['d26']:.1f} per cent more cargo. In this series' reading, only the conflicts at sea, which sent "
             "ships the long way round, kept the surplus from showing.",
             base=[lab, src], steps=[rows[0], rows[1], rows[2]])
