from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Ports(VoiceoverScene):
    def construct(self):
        card(self, 8, "Ports, forwarders and flags", "Who else earns from the box?",
             "Chapter eight. Ports, forwarders and flags. Between the factory and the shop the box passes through ports, "
             "the hands of a freight forwarder, and sometimes a law that decides which ships may carry it.", lit=("moat", "dollar"))
        self.port()
        self.forwarders()
        self.margins()
        self.jones()

    def port(self):
        c = draw.quay_crane(3.0).move_to([-4.2, 0.2, 0])
        vessel = draw.ship(4.4).move_to([0.4, -1.6, 0])
        g = VGroup(tx("A port terminal is a concession on a piece of coast", 20, PORT, bold=True),
                   tx("a government or port authority owns the land and the water", 17, WHITE),
                   tx("an operator leases it for decades, buys the cranes, and charges for every box", 17, WHITE),
                   tx("rivals need another deep harbour, which nature and planners rarely allow", 17, GREY_A)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.6, 1.4, 0])
        tag = estimate_tag("this series' summary of how terminals are owned", size=12)
        beat(self,
             "Start at the quay. <bookmark mark='a'/> A container terminal is usually a concession: <bookmark mark='b'/> a "
             "government or port authority owns the land and the water, <bookmark mark='c'/> and an operator leases it for "
             "decades, buys the cranes and charges for every box lifted. <bookmark mark='d'/> A rival needs another deep "
             "harbour nearby, which geography and planners rarely allow. Like Part 24's toll roads, the money is in owning the "
             "narrow place.",
             base=[c, vessel, tag], steps=[g[0], g[1], g[2], g[3]])

    def forwarders(self):
        P = R["ports"]["fw"]
        series = {k: ({y: v[0] for y, v in d.items()}, col) for (k, d), col in zip(P.items(), (SEA, BOX))}
        ch = line_chart(series, x=(2019, 2025), y=(0, 26), xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025], yticks=[0, 10, 20],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="revenue, $bn a year", width=9.0, height=4.4, center=(-1.2, -0.45))
        e, c = P["Expeditors"], P["C.H. Robinson"]
        src = source("Expeditors International and C.H. Robinson, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Then the forwarders, who book space on ships, planes and lorries for companies that make or sell things, and "
             "handle the paperwork. They own few ships or none. <bookmark mark='a'/> Expeditors' revenue went from "
             f"{e[2019][0]:.1f} billion dollars in 2019 to {e[2022][0]:.1f} billion in 2022 and back to {e[2025][0]:.1f}; "
             f"<bookmark mark='b'/> C.H. Robinson's from {c[2019][0]:.1f} to {c[2022][0]:.1f} and back to {c[2025][0]:.1f}. "
             "Their revenue includes the freight they buy and resell, so it rises and falls with the rates.",
             base=[ch.frame, src], steps=[[ch.lines["Expeditors"], ch.labels["Expeditors"]], [ch.lines["C.H. Robinson"], ch.labels["C.H. Robinson"]]])

    def margins(self):
        P = R["ports"]["fw"]
        Z = R["liner"]["zim_margin"]
        items = [("Expeditors, 2021 / 2023", 100 * P["Expeditors"][2021][1], SEA, f"{100 * P['Expeditors'][2021][1]:.1f}% / {100 * P['Expeditors'][2023][1]:.1f}%"),
                 ("C.H. Robinson, 2021 / 2023", 100 * P["C.H. Robinson"][2021][1], BOX, f"{100 * P['C.H. Robinson'][2021][1]:.1f}% / {100 * P['C.H. Robinson'][2023][1]:.1f}%"),
                 ("ZIM, 2021 / 2023", 100 * Z[2021], RATE, f"{100 * Z[2021]:.0f}% / {100 * Z[2023]:.0f}%")]
        rows = hbars(items, max_value=45, x0=0.6, top=1.4, row=1.0, length=5.4, size=16, bar_h=0.5)
        lab = tx("net income per dollar of revenue, in the boom year and the bust year", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K and 20-F via SEC company facts", size=12)
        beat(self,
             "But their margins barely move. <bookmark mark='a'/> Expeditors kept "
             f"{100 * P['Expeditors'][2021][1]:.1f} cents of each dollar in 2021 and {100 * P['Expeditors'][2023][1]:.1f} in "
             f"2023. <bookmark mark='b'/> C.H. Robinson, {100 * P['C.H. Robinson'][2021][1]:.1f} and "
             f"{100 * P['C.H. Robinson'][2023][1]:.1f}. <bookmark mark='c'/> ZIM, the ship operator, swung from "
             f"{100 * Z[2021]:.0f} per cent to a loss of {abs(100 * Z[2023]):.0f}. The middleman earns a fee on whatever the "
             "freight costs; the owner of the ships owns the cycle.",
             base=[lab, src], steps=[rows[0], rows[1], rows[2]])

    def jones(self):
        P = R["ports"]
        q = quote(["'Under the Jones Act, all vessels transporting cargo between covered U.S. ports must, subject to limited",
                   "exceptions, be built in the U.S., registered under the U.S. flag, be manned predominantly by U.S. crews,",
                   "and owned and operated by U.S.-organized companies'"], "Matson, Inc., Form 10-K for 2025", size=16).move_to([0, 1.6, 0])
        c = stat_cards([(f"{P['jones']:.0f}%", "of Matson's ocean revenue, 2025, from trades the Jones Act protects", SHIP),
                        (f"{100 * P['matx'][2025][1]:.0f}%", "Matson's net margin, 2025", GOOD)], y=-0.9, size=40, span=9.6)
        src = source("Matson, Inc., Form 10-K for 2025 and SEC company facts", size=12)
        beat(self,
             "And some routes are closed by law. <bookmark mark='a'/> Since 1920 America's Jones Act has required ships "
             "carrying cargo between American ports to be American-built, American-flagged, mostly American-crewed and "
             f"American-owned. <bookmark mark='b'/> Matson, which ships to Hawaii and Alaska, earned {P['jones']:.0f} per cent "
             "of its ocean revenue in 2025 in trades the act protects, <bookmark mark='c'/> and kept "
             f"{100 * P['matx'][2025][1]:.0f} cents of each dollar of its revenue. A protected route is a moat.",
             base=[src], steps=[q, c[0], c[1]])
