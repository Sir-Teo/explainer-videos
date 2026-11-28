from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.sales()
        self.versus()
        self.prices()
        self.jobs()

    def sales(self):
        S = R["traffic"]["sales"]
        ys = [1992, 2000, 2010, 2019, 2020, 2025]
        items = [(str(y), S[y], OP if y != 2020 else BAD, f"${S[y]:,.0f}bn") for y in ys]
        cols = vbars(items, base_y=-2.2, height=3.8, width=1.1, gap=0.5, size=16, max_value=1100)
        hd = tx("Intermission: eating out", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        lab = tx("Americans' spending at restaurants and bars, $bn a year", 18, GREY_A).to_edge(UP, buff=1.0)
        src = source("Census Bureau, retail sales of food services and drinking places (seasonally adjusted), via FRED", size=12)
        beat(self,
             f"An intermission, and three pictures. <bookmark mark='a'/> Americans spent about {S[1992]:.0f} billion dollars at "
             f"restaurants and bars in 1992 and {S[2010]:.0f} billion in 2010. <bookmark mark='b'/> {S[2019]:.0f} billion in 2019, "
             f"then {S[2020]:.0f} billion in 2020, when dining rooms closed. <bookmark mark='c'/> In 2025, "
             f"{S[2025] / 1e3:.2f} trillion: more than they spent at grocery stores, which Part 31 put at about nine hundred "
             "billion.",
             base=[hd, lab, src], steps=[VGroup(*cols[:3]), VGroup(*cols[3:5]), cols[5]])

    def prices(self):
        T = R["traffic"]
        ch = line_chart({"food away from home": (T["fafh"], OP), "food at home": (T["fah"], FOODC), "all consumer prices": (T["cpi"], GREY_B)},
                        x=(2015, 2027), y=(80, 145), xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[80, 100, 120, 140],
                        xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}", ylabel="consumer price indexes, December 2019 = 100",
                        width=8.4, height=4.4, center=(-1.4, -0.45), nudge={"food at home": -0.05, "all consumer prices": -0.25})
        f_, h_, c_ = T["fafh"][max(T["fafh"])], T["fah"][max(T["fah"])], T["cpi"][max(T["cpi"])]
        src = source("BLS, CPI-U for food away from home, food at home and all items, via FRED", size=12)
        beat(self,
             f"<bookmark mark='a'/> Prices in general rose about {c_ - 100:.0f} per cent from the end of 2019 to late 2026. "
             f"<bookmark mark='b'/> Food bought for home rose {h_ - 100:.0f} per cent. <bookmark mark='c'/> Food bought ready "
             f"to eat, at restaurants and from takeaways, rose {f_ - 100:.0f} per cent, the most of the three. A restaurant's "
             "price carries its wages as well as its ingredients.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["all consumer prices"], ch.labels["all consumer prices"]),
                                         VGroup(ch.lines["food at home"], ch.labels["food at home"]),
                                         VGroup(ch.lines["food away from home"], ch.labels["food away from home"])])

    def jobs(self):
        J = R["traffic"]["jobs"]
        ch = line_chart({"restaurants and bars": (J, LABC)}, x=(1990, 2027), y=(6000, 13000), xticks=[1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[6000, 8000, 10000, 12000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v / 1e3:.0f}m",
                        ylabel="Americans employed in food services and drinking places (seasonally adjusted)", width=9.2, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        last = max(J)
        k20 = min((k for k in J if 2020.2 < k < 2020.5), key=lambda k: J[k])
        m1 = marker(ch.ax, k20, J[k20], f"April 2020: {J[k20] / 1e3:.1f}m", BAD, side=RIGHT)
        m2 = marker(ch.ax, last, J[last], f"2026: {J[last] / 1e3:.1f}m", LABC, side=DOWN + LEFT)
        src = source("BLS, all employees in food services and drinking places, via FRED", size=12)
        beat(self,
             f"<bookmark mark='a'/> In April 2020 restaurant employment fell to {J[k20] / 1e3:.1f} million. "
             f"<bookmark mark='b'/> In 2026 about {J[last] / 1e3:.1f} million Americans work in restaurants and bars, one of the "
             "largest groups of workers in the country.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["restaurants and bars"], m1), m2])

    def versus(self):
        T = R["traffic"]
        ys = [y for y in T["sales"] if y in T["grocery"]]
        ch = line_chart({"restaurants and bars": ({y: T["sales"][y] for y in ys}, OP), "grocery stores": ({y: T["grocery"][y] for y in ys}, FOODC)},
                        x=(1992, 2025), y=(0, 1100), xticks=[1995, 2000, 2005, 2010, 2015, 2020, 2025], yticks=[0, 250, 500, 750, 1000],
                        xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn", ylabel="Americans' spending, $bn a year (not adjusted for prices)",
                        width=8.6, height=4.4, center=(-1.2, -0.45))
        cross = min((y for y in ys if T["sales"][y] > T["grocery"][y]), default=None)
        src = source("Census Bureau, retail sales of food services and drinking places and of grocery stores, via FRED", size=12)
        beat(self,
             f"<bookmark mark='a'/> Set restaurants beside grocery stores. In 1992 Americans spent {T['grocery'][1992]:.0f} billion "
             f"dollars at grocery stores and {T['sales'][1992]:.0f} billion eating out. <bookmark mark='b'/> Restaurants "
             f"overtook the grocers in {cross}, fell back when the pandemic closed dining rooms, and have pulled ahead again since. "
             "Americans now spend more at restaurants and bars than at grocery stores.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["grocery stores"], ch.labels["grocery stores"]),
                                         VGroup(ch.lines["restaurants and bars"], ch.labels["restaurants and bars"])])
