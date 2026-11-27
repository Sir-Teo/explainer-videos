from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403


class After(VoiceoverScene):
    def construct(self):
        card(self, 7, "After the sale", "Who earns from houses once they are built?",
             "Chapter seven. After the sale. A house is built once and lived in for decades, and paid for again and again "
             "in repairs, kitchens and roofs.", lit=("dollar", "unit"))
        self.stores()
        self.supplier()
        self.hdrev()
        self.factory()

    def stores(self):
        T = R["trade"]
        hd, lw = T["Home Depot"], T["Lowe's"]
        y = max(hd)
        items = [("Home Depot", hd[y][0], "#F2A65A", f"${hd[y][0]:.0f}bn"), ("Lowe's", lw[y][0], LOAN, f"${lw[y][0]:.0f}bn"),
                 ("D.R. Horton", R["builder"]["dhi"]["rev"], GREY_B, f"${R['builder']['dhi']['rev']:.0f}bn")]
        rows = hbars(items, max_value=180, x0=-0.2, top=1.2, row=1.0, length=6.2, size=18, bar_h=0.5)
        lab = tx("revenue, latest fiscal year", 16, GREY_A).move_to([0, 2.2, 0])
        m = tx(f"net margins: Home Depot {100 * hd[y][1]:.1f}%, Lowe's {100 * lw[y][1]:.1f}%", 18, GOOD, bold=True).move_to([0, -1.7, 0])
        src = source("Home Depot and Lowe's, Forms 10-K via SEC company facts (fiscal years ending January 2026)", size=12)
        beat(self,
             "The biggest businesses in American housing are not builders at all. <bookmark mark='a'/> Home Depot sold "
             f"{hd[y][0]:.0f} billion dollars of tools, timber, paint and appliances in the year to January 2026, "
             f"<bookmark mark='b'/> and Lowe's {lw[y][0]:.0f} billion. <bookmark mark='c'/> The largest homebuilder, "
             f"D.R. Horton, {R['builder']['dhi']['rev']:.0f} billion. <bookmark mark='d'/> And they keep more of it: "
             f"{100 * hd[y][1]:.1f} and {100 * lw[y][1]:.1f} cents of each dollar. Repairs and renovations do not wait for "
             "a buyer's mortgage approval in the way a new house does.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2], m])

    def factory(self):
        T = R["trade"]
        cv, sk = T["Cavco"], T["Champion Homes"]
        y = max(cv)
        frame = draw.factory(1.8) if hasattr(draw, "factory") else Square(1.2)
        frame.move_to([-4.6, 1.0, 0])
        house = draw.house(1.2, color="#F2A7B5").move_to([-2.2, 0.8, 0])
        c = stat_cards([(f"${cv[y][0]:.2f}bn", "Cavco's revenue, latest year", "#F2A7B5"),
                        (f"${sk[y][0]:.2f}bn", "Champion Homes'", "#F2A7B5"),
                        (f"{100 * cv[y][1]:.1f}%", "Cavco's net margin", GOOD)], y=-1.0, size=36, span=12)
        src = source("Cavco Industries and Champion Homes, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "And one part of the industry already builds houses the way Part 24 wished all buildings were built: in "
             "factories. <bookmark mark='a'/> Manufactured homes are built on assembly lines, in sections, and trucked to "
             f"the site. Cavco, a large maker, sold {cv[y][0]:.2f} billion dollars of them in its latest year, "
             f"<bookmark mark='b'/> and Champion Homes {sk[y][0]:.2f} billion. <bookmark mark='c'/> Cavco kept "
             f"{100 * cv[y][1]:.1f} cents of each dollar. It is a small corner of the market; in this series' reading it is "
             "held back less by the factory than by the land and the local rules about where such homes may stand.",
             base=[frame, house, src], steps=[c[0], c[1], c[2]])

    def supplier(self):
        B = R["extra"]["bfs"]
        ch = line_chart({"revenue": ({y: v[0] for y, v in B.items()}, LAND)}, x=(2019, 2025), y=(0, 25), xticks=list(range(2019, 2026)),
                        yticks=[0, 5, 10, 15, 20, 25], yfmt=lambda v: f"${v:.0f}bn", ylabel="Builders FirstSource's revenue",
                        width=9.0, height=4.2, center=(-0.6, -0.45), label_end=False)
        pk = max(B, key=lambda y: B[y][0])
        m1 = marker(ch.ax, pk, B[pk][0], f"{pk}: ${B[pk][0]:.1f}bn, {100 * B[pk][1]:.0f}% kept", PRICE, side=UP)
        m2 = marker(ch.ax, 2025, B[2025][0], f"2025: ${B[2025][0]:.1f}bn, {100 * B[2025][1]:.1f}% kept", LAND, side=RIGHT)
        src = source("Builders FirstSource, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Between the timber mill and the building site sits a distributor. <bookmark mark='a'/> Builders "
             "FirstSource sells lumber and building materials to builders. Its revenue roughly tripled from 2019 "
             f"to {B[pk][0]:.1f} billion dollars in {pk}, through the lumber boom of Part 24, and it kept {100 * B[pk][1]:.0f} cents "
             f"of each dollar. <bookmark mark='b'/> By 2025, {B[2025][0]:.1f} billion and {100 * B[2025][1]:.1f} cents: a "
             "supplier to builders rides the same cycle as the builders, with a lag.",
             base=[ch.frame, src], steps=[[ch.lines["revenue"], m1], m2])

    def hdrev(self):
        H = R["trade"]["Home Depot"]
        ch = line_chart({"Home Depot": ({y: v[0] for y, v in H.items()}, "#F2A65A")}, x=(2018, 2026), y=(100, 180),
                        xticks=list(range(2018, 2027, 2)), yticks=[100, 120, 140, 160, 180], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="Home Depot's revenue, fiscal years ending in each year", width=9.0, height=4.2,
                        center=(-0.6, -0.45), label_end=False)
        y0 = min(H)
        m1 = marker(ch.ax, y0, H[y0][0], f"{y0}: ${H[y0][0]:.0f}bn", GREY_B, side=UP)
        m2 = marker(ch.ax, 2022, H[2022][0], f"2022: ${H[2022][0]:.0f}bn", PRICE, side=UP)
        m3 = marker(ch.ax, 2026, H[2026][0], f"2026: ${H[2026][0]:.0f}bn", "#F2A65A", side=DOWN)
        src = source("Home Depot, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "The stores have their own cycle. <bookmark mark='a'/> Home Depot's revenue was "
             f"{H[y0][0]:.0f} billion dollars in the year ending early {y0}. <bookmark mark='b'/> It jumped to "
             f"{H[2022][0]:.0f} billion in the year ending early 2022, in the pandemic years, <bookmark mark='c'/> and has "
             f"crept up since, to {H[2026][0]:.0f} billion. In this series' reading, when fewer houses change hands, fewer "
             "kitchens are refitted for new owners, so the stores feel a frozen market too, more gently.",
             base=[ch.frame, src], steps=[[ch.lines["Home Depot"], m1], m2, m3])
