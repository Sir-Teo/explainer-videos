from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.prices()
        self.jobs()
        self.stack()
        self.copper()

    def prices(self):
        T = R["traffic"]
        ch = line_chart({"telephone services": (T["tel"], WIRELESS), "all consumer prices": (T["cpi"], GREY_B)}, x=(1998, 2027),
                        y=(50, 210), xticks=[1998, 2004, 2010, 2016, 2022], yticks=[50, 100, 150, 200], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:.0f}", ylabel="consumer price indexes, December 1997 = 100", width=8.8, height=4.4,
                        center=(-1.2, -0.45))
        hd = tx("Intermission: cheaper calls, fewer people", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        last = max(T["tel"])
        src = source("BLS, CPI-U for telephone services and all items, via FRED", size=12)
        beat(self,
             "An intermission, and three pictures. <bookmark mark='a'/> Since the end of 1997, prices in general have "
             f"roughly doubled. <bookmark mark='b'/> The price of telephone service, by the government's index, stood at "
             f"{T['tel'][last]:.0f} in late 2026, against 100 then. It is one of the few things Americans buy that costs less "
             "in dollars than it did a generation ago.",
             base=[hd, ch.frame, src], steps=[VGroup(ch.lines["all consumer prices"], ch.labels["all consumer prices"]),
                                              VGroup(ch.lines["telephone services"], ch.labels["telephone services"])])

    def jobs(self):
        T = R["traffic"]
        J = T["jobs"]
        ch = line_chart({"telecommunications jobs": (J, CABLE)}, x=(1990, 2027), y=(0, 1600), xticks=[1990, 2000, 2010, 2020],
                        yticks=[0, 400, 800, 1200, 1600], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:,.0f}k",
                        ylabel="Americans employed in telecommunications (thousands, seasonally adjusted)", width=9.2, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        pk, last = T["jobs_peak"], max(J)
        m1 = marker(ch.ax, pk, J[pk], f"{int(pk)}: {J[pk]:,.0f}k", ALL, side=UP)
        m2 = marker(ch.ax, last, J[last], f"2026: {J[last]:,.0f}k", CABLE, side=UP)
        src = source("BLS, all employees in telecommunications, via FRED", size=12)
        beat(self,
             f"<bookmark mark='a'/> In {int(pk)}, about {J[pk] / 1e3:.2f} million Americans worked in telecommunications. "
             f"<bookmark mark='b'/> By 2026, {J[last]:,.0f} thousand: fewer than two in five of them, carrying vastly more "
             "traffic over networks that need fewer hands.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["telecommunications jobs"], m1), m2])

    def copper(self):
        L = R["traffic"]["lumen"]
        items = [(str(y), L[y], WIRE, f"${L[y]:.1f}bn") for y in (2015, 2019, 2022, 2025)]
        cols = vbars(items, base_y=-2.0, height=3.6, width=1.3, gap=0.6, size=16, max_value=24)
        lab = tx("Lumen Technologies: revenue, $bn", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Lumen Technologies, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "And a fourth picture, of the old wires. <bookmark mark='a'/> Lumen, one of the old local telephone companies, "
             f"took in {L[2015]:.1f} billion dollars in 2015 and {L[2019]:.1f} billion in 2019. <bookmark mark='b'/> By 2025, "
             f"{L[2025]:.1f} billion, and a loss, and AT&T had agreed to buy its mass-market fibre business. In this series' "
             "reading, copper telephone lines are the one part of this industry shrinking for good.",
             base=[lab, src], steps=[VGroup(*cols[:2]), VGroup(*cols[2:])])

    def stack(self):
        Rv = R["traffic"]["rev"]
        cols = {"Verizon": WIRELESS, "AT&T": "#4F8FE6", "Comcast": CABLE, "T-Mobile": "#F2A7B5", "Charter": "#9FE0D0"}
        ch = line_chart({k: (Rv[k], c) for k, c in cols.items()}, x=(2015, 2025), y=(0, 200), xticks=[2015, 2017, 2019, 2021, 2023, 2025],
                        yticks=[0, 50, 100, 150, 200], yfmt=lambda v: f"${v:.0f}bn", ylabel="revenue, $bn a year", width=8.8,
                        height=4.4, center=(-1.3, -0.45))
        src = source("Forms 10-K via SEC company facts; AT&T, Form 10-K for 2021; T-Mobile, Form 10-K for 2025 (the Sprint merger of 1 April 2020)", size=12)
        beat(self,
             "And the five biggest American carriers' revenue over ten years. <bookmark mark='a'/> Verizon, flat. AT&T, "
             f"down from {Rv['AT&T'][2019]:.0f} billion in 2019 to {Rv['AT&T'][2025]:.0f}, after it separated its "
             f"television business, DIRECTV, in 2021 and agreed to combine WarnerMedia with Discovery. Comcast and Charter, slowly rising. <bookmark mark='b'/> T-Mobile, nearly tripled, from "
             f"{Rv['T-Mobile'][2015]:.0f} billion to {Rv['T-Mobile'][2025]:.0f}, largely by buying Sprint in 2020.",
             base=[ch.frame, src], steps=[VGroup(*[VGroup(ch.lines[k], ch.labels[k]) for k in ("Verizon", "AT&T", "Comcast", "Charter")]),
                                         VGroup(ch.lines["T-Mobile"], ch.labels["T-Mobile"])])
