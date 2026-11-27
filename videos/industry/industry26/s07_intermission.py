from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.rents()
        self.cranes()
        self.real()

    def rents(self):
        E = R["extra"]
        ch = line_chart({"rents of commercial buildings": (E["ppi"], INCOME), "all consumer prices": (E["cpi"], ALL)},
                        x=(2005, 2025), y=(0.9, 1.8), xticks=[2005, 2010, 2015, 2020, 2025], yticks=[1.0, 1.2, 1.4, 1.6, 1.8],
                        yfmt=lambda v: f"x{v:.1f}", ylabel="2005 = 1", width=9.2, height=4.4, center=(-1.2, -0.45))
        hd = tx("Intermission: rents, cranes and prices", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("BLS producer price index for lessors of nonresidential buildings; CPI-U; annual averages via FRED", size=12)
        beat(self,
             "An intermission, and three pictures. <bookmark mark='a'/> First, rents. The Bureau of Labor Statistics measures "
             "the rents that owners of commercial buildings charge. Since 2005 they have risen "
             f"{E['ppi'][2025]:.2f} times, <bookmark mark='b'/> while consumer prices rose {E['cpi'][2025]:.2f} times. In real "
             "terms, the average commercial rent has fallen: a building's income has had to come from filling it, not from "
             "raising the price of its space.",
             base=[hd, ch.frame, src], steps=[[ch.lines["rents of commercial buildings"], ch.labels["rents of commercial buildings"]],
                                              [ch.lines["all consumer prices"], ch.labels["all consumer prices"]]])

    def cranes(self):
        E = R["extra"]
        ch = line_chart({"offices, including data centres": (E["office"], OFFICE), "shops and warehouses": (E["comm"], SHED)},
                        x=(2002, 2025), y=(0, 175), xticks=[2002, 2006, 2010, 2015, 2019, 2022, 2025], yticks=[0, 50, 100, 150],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="construction spending a year (annual average of SAAR)", width=9.2,
                        height=4.4, center=(-1.2, -0.45), nudge={"shops and warehouses": 0.2})
        crane = draw.tower_crane(1.6).move_to([5.4, -1.5, 0])
        src = source("Census Bureau, construction spending: office and commercial, via FRED, and its definitions; BXP, Inc., Form 10-K for 2025", size=12)
        pk = max(E["comm"], key=E["comm"].get)
        beat(self,
             "Second, the cranes. <bookmark mark='a'/> Spending on new shops and warehouses rose from "
             f"{E['comm'][2019]:.0f} billion dollars in 2019 to a peak of {E['comm'][pk]:.0f} billion in {pk}, as online "
             f"shopping filled the sheds, and was {E['comm'][2025]:.0f} billion in 2025. <bookmark mark='b'/> Spending on offices rose "
             f"too, to {E['office'][2025]:.0f} billion. But the Census Bureau counts data centres as offices, and BXP wrote in "
             "its 2025 annual report that 'new office construction has effectively halted'. The cranes are building server "
             "halls, not desks.",
             base=[ch.frame, crane, src], steps=[[ch.lines["shops and warehouses"], ch.labels["shops and warehouses"]],
                                                 [ch.lines["offices, including data centres"], ch.labels["offices, including data centres"]]])

    def real(self):
        H = R["hook"]
        rl = H["real"]
        ch = line_chart({"commercial property prices after inflation": (rl, VALUE)}, x=(1990, 2026.5), y=(60, 140),
                        xticks=[1990, 1995, 2000, 2007, 2010, 2016, 2022, 2026], yticks=[60, 80, 100, 120, 140],
                        yfmt=lambda v: f"{v:.0f}", ylabel="the Federal Reserve's price index divided by consumer prices, 2001 = 100",
                        width=9.4, height=4.4, center=(-0.6, -0.45), label_end=False)
        k1 = max((k for k in rl if 2005 <= k <= 2009), key=rl.get)
        k2 = max((k for k in rl if 2018 <= k <= 2024), key=rl.get)
        kn = max(rl)
        k0 = min((k for k in rl if k <= 1996), key=rl.get)
        m0 = marker(ch.ax, k0, rl[k0], f"{int(k0)}: {rl[k0]:.0f}", BAD, side=DOWN)
        m1 = marker(ch.ax, k1, rl[k1], f"{int(k1)}: {rl[k1]:.0f}", VALUE, side=UP)
        m2 = marker(ch.ax, k2, rl[k2], f"{int(k2)}: {rl[k2]:.0f}", VALUE, side=UP)
        m3 = marker(ch.ax, kn, rl[kn], f"{int(kn)}: {rl[kn]:.0f}", BAD, side=DOWN)
        src = source("Federal Reserve Z.1 commercial real estate price index; BLS CPI-U; via FRED", size=12)
        tag = estimate_tag("this series' arithmetic: the index over the CPI", size=12)
        beat(self,
             "Third, prices after inflation, since 1990. <bookmark mark='a'/> The early 1990s were a commercial property "
             f"crash: real prices bottomed in {int(k0)}. <bookmark mark='b'/> They peaked in {int(k1)}, <bookmark mark='c'/> "
             f"and again in {int(k2)}, <bookmark mark='d'/> and by mid-2026 they were back about where they stood in the "
             f"mid-2010s, at {rl[kn]:.0f}. Over thirty-five years the price of a commercial building, after inflation, has "
             "gone up and down far more than it has gone up.",
             base=[ch.frame, src, tag], steps=[[ch.lines["commercial property prices after inflation"], m0], m1, m2, m3])
