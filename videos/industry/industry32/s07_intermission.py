from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.share()
        self.sales()
        self.still()

    def share(self):
        T = R["traffic"]
        E = T["share"]
        ch = line_chart({"online share": (E, SHOP)}, x=(1999, 2027), y=(0, 20), xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[0, 5, 10, 15, 20], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}%",
                        ylabel="e-commerce as a share of American retail sales, quarterly (seasonally adjusted)", width=9.2, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        k20 = near(E, 2020.25)
        last = max(E)
        m1 = marker(ch.ax, k20, E[k20], f"spring 2020: {E[k20]:.1f}%", BAD, side=LEFT)
        m2 = marker(ch.ax, last, E[last], f"2026: {E[last]:.1f}%", SHOP, side=UP)
        hd = tx("Intermission: the screen, the shed and the van", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Census Bureau, quarterly e-commerce retail sales as a percent of total sales, via FRED", size=12)
        beat(self,
             "An intermission, and three pictures from the Census Bureau, which has measured online shopping since the "
             f"end of 1999. <bookmark mark='a'/> Then it was {E[min(E)]:.1f} per cent of American retail sales. It climbed "
             "steadily, about half a point a year. <bookmark mark='b'/> In the spring of 2020, with shops shut, it jumped to "
             f"{E[k20]:.0f} per cent, then fell back as they reopened. <bookmark mark='c'/> It passed that peak again only in "
             f"2024, and in 2026 stands at {E[last]:.1f} per cent: the pandemic pulled the future forward a few years, and "
             "the old slow climb resumed.",
             base=[hd, ch.frame, src], steps=[ch.lines["online share"], m1, m2])

    def sales(self):
        S = R["traffic"]["sales"]
        items = [(str(y), S[y], SHOP if y != 2020 else BAD, f"${S[y]:,.0f}bn") for y in (2000, 2010, 2019, 2020, 2025)]
        cols = vbars(items, base_y=-2.2, height=3.8, width=1.3, gap=0.6, size=16, max_value=1300)
        lab = tx("American e-commerce retail sales, $bn a year (not adjusted for prices)", 18, GREY_A).to_edge(UP, buff=0.9)
        src = source("Census Bureau, quarterly e-commerce retail sales (not seasonally adjusted), via FRED", size=12)
        beat(self,
             "In dollars: <bookmark mark='a'/> about "
             f"{S[2000]:.0f} billion dollars in 2000, {S[2010]:.0f} billion in 2010 and {S[2019]:.0f} billion in 2019. "
             f"<bookmark mark='b'/> {S[2020]:.0f} billion in 2020. <bookmark mark='c'/> And {S[2025] / 1e3:.2f} trillion "
             "in 2025: more than Amazon's whole revenue, because much of it is other shops' websites, cars, groceries and "
             "everything sold through marketplaces by others.",
             base=[lab, src], steps=[VGroup(*cols[:3]), cols[3], cols[4]])

    def still(self):
        T = R["traffic"]
        s = T["last_share"]
        bar = viz.bar_split([("online", s, SHOP), ("in shops, at pumps and showrooms", 100 - s, ALL)], 100, width=12.0, height=1.0).move_to([0, 0.6, 0])
        l1 = tx(f"online: {s:.1f}%", 22, SHOP, bold=True).next_to(bar[0], DOWN, buff=0.25)
        l2 = tx(f"everything else: {100 - s:.1f}%", 22, ALL, bold=True).next_to(bar[1], DOWN, buff=0.25)
        crowd = draw.crowd(16, h=0.4, cols=8).move_to([0, -2.2, 0])
        src = source("Census Bureau, via FRED", size=12)
        beat(self,
             "And the picture that surprises people most. <bookmark mark='a'/> After a quarter of a century of growth, "
             f"online shopping is {s:.0f} per cent of American retail. <bookmark mark='b'/> The other "
             f"{100 - s:.0f} per cent is still bought in person: in supermarkets, at petrol pumps, in car showrooms and "
             "chemists. The giants of the last chapters were built on the first sliver.",
             base=[crowd, src], steps=[VGroup(bar[0], l1), VGroup(bar[1], l2)])
