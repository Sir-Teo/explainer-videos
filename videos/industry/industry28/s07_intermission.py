from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.load()
        self.seats()
        self.passengers()
        self.jobs()

    def load(self):
        T = R["traffic"]
        ch = line_chart({"load factor": (T["lf"], SKY)}, x=(2000, 2027), y=(0, 100), xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[0, 20, 40, 60, 80, 100], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}%",
                        ylabel="American airlines' load factor (monthly)", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        a = T["lf_annual"]
        m1 = marker(ch.ax, 2000.5, a[2000], f"2000: {a[2000]:.0f}%", ALL, side=UP)
        m2 = marker(ch.ax, 2019.5, a[2019], f"2019: {a[2019]:.0f}%", GOOD, side=UP)
        hd = tx("Intermission: seats, passengers and jobs", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Bureau of Transportation Statistics, load factor, US air carriers, via FRED", size=12)
        beat(self,
             "An intermission, and three pictures of the whole American industry. <bookmark mark='a'/> In 2000, airlines "
             f"filled {a[2000]:.0f} per cent of their seats. <bookmark mark='b'/> By 2019, {a[2019]:.0f}: two decades of "
             "better forecasting, pricing and scheduling, Run it's tools at scale. Then the pandemic emptied the planes for a "
             "year.",
             base=[hd, ch.frame, src], steps=[[ch.lines["load factor"], m1], m2])

    def seats(self):
        T = R["traffic"]
        ch = line_chart({"seat-miles flown": (T["asm_m"], ALL), "seat-miles sold": (T["rpm_m"], SKY)}, x=(2000, 2027), y=(0, 140),
                        xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[0, 40, 80, 120], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:.0f}bn", ylabel="American airlines, seat-miles a month",
                        width=9.0, height=4.4, center=(-1.0, -0.45))
        a, p = T["asm"], T["rpm"]
        src = source("Bureau of Transportation Statistics, available seat-miles and revenue passenger-miles, via FRED", size=12)
        beat(self,
             "The same story in seat-miles. <bookmark mark='a'/> The grey line is the seats airlines flew, "
             f"{12 * a[2025] / 1e6 / 1e3:.2f} trillion seat-miles in 2025, against {12 * a[2000] / 1e6:,.0f} billion in 2000. "
             "<bookmark mark='b'/> The blue line is the seats they sold. The gap between them is the empty seats, and it has "
             "narrowed: the industry grew, and filled what it grew.",
             base=[ch.frame, src], steps=[[ch.lines["seat-miles flown"], ch.labels["seat-miles flown"]],
                                          [ch.lines["seat-miles sold"], ch.labels["seat-miles sold"]]])

    def passengers(self):
        E = R["traffic"]["enplane"]
        items = [(str(y), E[y], BAD if y == 2020 else SKY, f"{E[y]:.0f}m") for y in (2000, 2019, 2020, 2021, 2024, 2025)]
        cols = vbars(items, base_y=-2.0, height=3.6, width=1.1, gap=0.6, size=16, max_value=1050)
        lab = tx("passengers boarded on American airlines' scheduled flights, a year", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Bureau of Transportation Statistics, enplanements (monthly totals summed), via FRED", size=12)
        beat(self,
             f"Second, passengers. <bookmark mark='a'/> About {E[2000]:.0f} million boardings in 2000, "
             f"{E[2019]:.0f} million in 2019, <bookmark mark='b'/> {E[2020]:.0f} million in 2020, <bookmark mark='c'/> and "
             f"{E[2025]:.0f} million in 2025, just below 2024's {E[2024]:.0f} million, the most since this record began in 2000.",
             base=[lab, src], steps=[VGroup(*cols[:2]), VGroup(*cols[2:3]), VGroup(*cols[3:])])

    def jobs(self):
        J = R["traffic"]["jobs"]
        E = R["traffic"]["enplane"]
        ch = line_chart({"air transportation jobs": (J, CASH)}, x=(2000, 2027), y=(300, 700), xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[300, 400, 500, 600, 700], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}k",
                        ylabel="Americans employed in air transportation (thousands, monthly)", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        pk = max(J, key=J.get)
        lo = min((k for k in J if 2005 <= k <= 2015), key=J.get)
        last = max(J)
        j00 = float(np.mean([v for k, v in J.items() if 2000 <= k < 2001]))
        j25 = float(np.mean([v for k, v in J.items() if 2025 <= k < 2026]))
        m1 = marker(ch.ax, pk, J[pk], f"{int(pk)}: {J[pk]:.0f}k", ALL, side=UP)
        m2 = marker(ch.ax, lo, J[lo], f"{int(lo)}: {J[lo]:.0f}k", BAD, side=DOWN)
        m3 = marker(ch.ax, last, J[last], f"2026: {J[last]:.0f}k", CASH, side=DOWN)
        src = source("BLS, all employees in air transportation; BTS enplanements; via FRED", size=12)
        beat(self,
             "And third, the people. <bookmark mark='a'/> Air transport employed about "
             f"{J[pk]:.0f} thousand Americans in {int(pk)}. <bookmark mark='b'/> By {int(lo)}, {J[lo]:.0f} thousand. "
             f"<bookmark mark='c'/> In 2026, {J[last]:.0f} thousand: fewer people than in {int(pk)}, carrying "
             f"{E[2025]:.0f} million passengers a year instead of {E[2000]:.0f} million. By this series' arithmetic, each "
             f"job carried about {1e3 * E[2000] / j00:,.0f} passengers in 2000 and about {1e3 * E[2025] / j25:,.0f} in 2025: "
             "bigger planes, fuller flights, machines at check-in and the booking done by the passengers themselves.",
             base=[ch.frame, src], steps=[[ch.lines["air transportation jobs"], m1], m2, m3])
