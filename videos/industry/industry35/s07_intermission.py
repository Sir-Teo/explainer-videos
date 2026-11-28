from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.nights()
        self.prices()
        self.flying()
        self.jobs()

    def nights(self):
        N = R["traffic"]["nights"]
        items = [(str(y), v, AGENT if y != 2020 else BAD, f"{v:,}m") for y, v in N.items()]
        cols = vbars(items, base_y=-2.3, height=3.8, width=1.0, gap=0.45, size=16, max_value=1300)
        hd = tx("Intermission: on the move", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        lab = tx("room nights booked through Booking Holdings, millions a year", 18, GREY_A).to_edge(UP, buff=1.0)
        src = source("Booking Holdings, Forms 10-K for 2020, 2023 and 2025", size=12)
        beat(self,
             f"An intermission, and four pictures of travel. <bookmark mark='a'/> In 2019 travellers booked {N[2019]} million "
             f"room nights through Booking Holdings, the owner of Booking.com. <bookmark mark='b'/> In 2020, {N[2020]} million. "
             f"<bookmark mark='c'/> By 2022 it was back above 2019, and in 2025 it reached {N[2025]:,} million, nearly half "
             "as many again as before the pandemic.",
             base=[hd, lab, src], steps=[cols[0], cols[1], VGroup(*cols[2:])])

    def prices(self):
        T = R["traffic"]
        ch = line_chart({"hotel and motel rooms": (T["lodging"], BRAND), "airline fares": (T["air"], OWNER), "all consumer prices": (T["cpi"], GREY_B)},
                        x=(2015, 2027), y=(50, 140), xticks=[2015, 2018, 2021, 2024, 2027], yticks=[50, 80, 110, 140],
                        xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}", ylabel="US consumer prices, December 2019 = 100",
                        width=8.4, height=4.4, center=(-1.4, -0.45), nudge={"all consumer prices": 0.2, "hotel and motel rooms": 0.02, "airline fares": -0.32})
        src = source("BLS consumer price indexes (not seasonally adjusted), via FRED", size=12)
        a, b_, c = (round(T[k][max(T[k])] - 100) for k in ("lodging", "air", "cpi"))
        beat(self,
             "Prices. <bookmark mark='a'/> Consumer prices in general have risen about "
             f"{c} per cent since the end of 2019. <bookmark mark='b'/> Hotel rooms collapsed in 2020, then recovered, and are "
             f"up about {a} per cent. <bookmark mark='c'/> Airfares fell further, swung harder and are up about {b_}. In "
             "travel, prices move with how full the planes and hotels are, month by month.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["all consumer prices"], ch.labels["all consumer prices"]),
                                          VGroup(ch.lines["hotel and motel rooms"], ch.labels["hotel and motel rooms"]),
                                          VGroup(ch.lines["airline fares"], ch.labels["airline fares"])])

    def flying(self):
        E = R["traffic"]["enplane"]
        ys = [y for y in sorted(E) if y >= 2015]
        items = [(str(y), E[y], OWNER if y != 2020 else BAD, f"{E[y]:.0f}m") for y in ys]
        cols = vbars(items, base_y=-2.3, height=3.6, width=0.72, gap=0.3, size=13, max_value=1050)
        lab = tx("passengers boarding US airlines' flights, millions a year", 18, GREY_A).to_edge(UP, buff=1.0)
        src = source("Bureau of Transportation Statistics, enplanements (domestic and international), via FRED", size=12)
        beat(self,
             f"Flying. <bookmark mark='a'/> American airlines boarded {E[2019]:.0f} million passengers in 2019, "
             f"<bookmark mark='b'/> {E[2020]:.0f} million in 2020, <bookmark mark='c'/> and {E[max(ys)]:.0f} million in "
             f"{max(ys)}, back above the 2019 level since 2023.",
             base=[lab, src], steps=[VGroup(*[cols[i] for i, y in enumerate(ys) if y <= 2019]),
                                     VGroup(*[cols[i] for i, y in enumerate(ys) if y == 2020]),
                                     VGroup(*[cols[i] for i, y in enumerate(ys) if y > 2020])])

    def jobs(self):
        J = R["traffic"]["jobs"]
        ch = line_chart({"accommodation jobs": ({k: v / 1e3 for k, v in J.items()}, STAFF)}, x=(2000, 2027), y=(0.8, 2.2),
                        xticks=[2000, 2007, 2014, 2021, 2027], yticks=[1.0, 1.5, 2.0], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:.1f}m", ylabel="people employed by US hotels, motels and other lodging, millions",
                        width=8.6, height=4.2, center=(-1.0, -0.45))
        low = min(v for k, v in J.items() if 2020 < k < 2021)
        pre = J[max(k for k in J if k < 2020)]
        src = source("BLS, all employees in accommodation (seasonally adjusted), via FRED", size=12)
        beat(self,
             "And people. <bookmark mark='a'/> American hotels and other lodging employed about "
             f"{pre / 1e3:.1f} million people at the end of 2019. In the spring of 2020 that fell to {low / 1e3:.2f} million in a "
             f"matter of weeks, and six years later it is about {J[max(J)] / 1e3:.2f} million: the rooms came back faster than "
             "the staff. A hotel's costs are mostly people, and in 2020 they were the costs owners could cut; many have not "
             "been added back.",
             base=[ch.frame, src], steps=[VGroup(*ch.lines.values(), *ch.labels.values())])
