from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403


class Supply(VoiceoverScene):
    def construct(self):
        card(self, 4, "Why prices outran costs", "If a house costs no more to build, why does it cost more to buy?",
             "Chapter four. Why prices outran costs. Builders explain margins; they do not explain why a house costs "
             "four or five years of a household's income.", lit=("moat", "change"))
        self.starts()
        self.months()
        self.sales()
        self.costs()
        self.income()
        self.land()

    def starts(self):
        S = R["supply"]
        ch = line_chart({"housing starts": ({y: v / 1e3 for y, v in S["starts"].items()}, HOUSE)}, x=(1959, 2025), y=(0, 2.6),
                        xticks=[1960, 1970, 1980, 1990, 2000, 2010, 2020, 2025], yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5],
                        yfmt=lambda v: f"{v:.1f}m", ylabel="new homes started in America a year", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        pk, lo = S["peak"], S["low"]
        m1 = marker(ch.ax, pk, S["starts"][pk] / 1e3, f"{pk}: {S['starts'][pk] / 1e3:.2f}m", PRICE, side=UP)
        m2 = marker(ch.ax, lo, S["starts"][lo] / 1e3, f"{lo}: {S['starts'][lo] / 1e3:.2f}m", BAD, side=DOWN)
        m3 = marker(ch.ax, 2025, S["starts"][2025] / 1e3, f"2025: {S['starts'][2025] / 1e3:.2f}m", HOUSE, side=UP)
        src = source("Census Bureau, housing starts (annual averages of SAAR), via FRED", size=12)
        beat(self,
             "Start with how many homes America builds. <bookmark mark='a'/> In "
             f"{pk} builders started {S['starts'][pk] / 1e6:.2f} million homes, with a far smaller population than today. "
             f"<bookmark mark='b'/> After the 2008 crash, starts fell to {S['starts'][lo] / 1e3:.0f} thousand in {lo}, the "
             f"lowest on this chart. <bookmark mark='c'/> In 2025, {S['starts'][2025] / 1e6:.2f} million: a recovery, but "
             "below the levels of the 1970s and the 2000s.",
             base=[ch.frame, src], steps=[[ch.lines["housing starts"], m1], m2, m3])

    def costs(self):
        P = R["prices"]
        ch = line_chart({"house prices": (P["cs"], HOUSE), "building materials": (P["ppi"], LAND), "all consumer prices": (P["cpi"], ALL)},
                        x=(2000, 2025), y=(0.8, 3.4), xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[1.0, 1.5, 2.0, 2.5, 3.0],
                        yfmt=lambda v: f"x{v:.1f}", ylabel="prices, 2000 = 1", width=9.4, height=4.4, center=(-1.0, -0.45))
        src = source("Case-Shiller national index; BLS PPI for inputs to residential construction (goods) and CPI-U; via FRED", size=12)
        beat(self,
             "Now prices. Since 2000, <bookmark mark='a'/> consumer prices in general have risen "
             f"{P['cpi'][2025]:.1f} times, <bookmark mark='b'/> the materials that go into a house {P['ppi'][2025]:.1f} times, "
             f"<bookmark mark='c'/> and house prices {P['cs'][2025]:.1f} times. Materials explain part of the rise. The rest "
             "of the gap is in what the materials stand on: the land, and the right to build on it.",
             base=[ch.frame, src], steps=[[ch.lines["all consumer prices"], ch.labels["all consumer prices"]],
                                          [ch.lines["building materials"], ch.labels["building materials"]],
                                          [ch.lines["house prices"], ch.labels["house prices"]]])

    def income(self):
        P = R["prices"]["ratio"]
        ch = line_chart({"price over income": (P, PRICE)}, x=(1984, 2025), y=(3, 6.5), xticks=[1984, 1990, 2000, 2006, 2012, 2020, 2025],
                        yticks=[3, 4, 5, 6], yfmt=lambda v: f"{v:.0f}x", ylabel="median house price over median household income",
                        width=9.4, height=4.4, center=(-0.6, -0.45), label_end=False)
        pk = max(P, key=P.get)
        m1 = marker(ch.ax, 1984, P[1984], f"1984: {P[1984]:.1f}x", ALL, side=RIGHT)
        m2 = marker(ch.ax, pk, P[pk], f"{pk}: {P[pk]:.1f}x", BAD, side=UP)
        m3 = marker(ch.ax, 2025, P[2025], f"2025: {P[2025]:.1f}x", PRICE, side=DOWN)
        src = source("Census and HUD, median sales price of houses sold; Census, median household income; via FRED", size=12)
        beat(self,
             "Against what households earn. <bookmark mark='a'/> In 1984 the median house sold for "
             f"{P[1984]:.1f} times the median household's annual income. <bookmark mark='b'/> In {pk} it reached "
             f"{P[pk]:.1f} times. <bookmark mark='c'/> In 2025, {P[2025]:.1f}. A house that took three and a half years of "
             "income now takes nearly five.",
             base=[ch.frame, src], steps=[[ch.lines["price over income"], m1], m2, m3])

    def land(self):
        g = VGroup(tx("Why is land the scarce thing?", 22, WHITE, bold=True),
                   tx("land near jobs is fixed; you cannot make more of it near the city centre", 18, LAND),
                   tx("towns decide what may be built on it: zoning, minimum lot sizes, height limits", 18, PRICE),
                   tx("approvals take years, and each year is the builder's money tied up", 18, HOUSE),
                   tx("so where building is easy, prices track costs; where it is hard, they run ahead", 18, GREY_A)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.3, 0])
        lot = draw.plot_lot(1.6).move_to([5.0, -2.3, 0])
        tag = estimate_tag("this series' summary of the economics of land and housing supply", size=12)
        beat(self,
             "Why is the land the scarce thing? <bookmark mark='a'/> Because land near jobs is fixed: the city centre "
             "cannot be moved closer to more people. <bookmark mark='b'/> Because towns decide what may be built on it, "
             "how large each lot must be, how tall the building, whether flats are allowed at all. <bookmark mark='c'/> "
             "Because approvals take years, and the builder carries the land while it waits, as Run it showed. "
             "<bookmark mark='d'/> So where building is easy, house prices stay close to what it costs to build; where it "
             "is hard, they run ahead, and the difference is the price of the permission.",
             base=[lot, tag], steps=[g[:2], g[2], g[3], g[4]])

    def months(self):
        E = R["extra"]["months"]
        ch = line_chart({"months' supply": ({y: v for y, v in E.items() if 1990 <= y <= 2025}, PRICE)}, x=(1990, 2025), y=(2, 11),
                        xticks=[1990, 2000, 2006, 2009, 2015, 2020, 2025], yticks=[2, 4, 6, 8, 10], yfmt=lambda v: f"{v:.0f}",
                        ylabel="new houses for sale, in months of sales at the current pace", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        m1 = marker(ch.ax, 2009, E[2009], f"2009: {E[2009]:.1f}", BAD, side=UP)
        m2 = marker(ch.ax, 2020, E[2020], f"2020: {E[2020]:.1f}", GOOD, side=DOWN)
        m3 = marker(ch.ax, 2025, E[2025], f"2025: {E[2025]:.1f}", PRICE, side=UP)
        src = source("Census Bureau, monthly supply of new houses (annual averages), via FRED", size=12)
        beat(self,
             "The builders' own stock tells the other half. <bookmark mark='a'/> In 2009 the new houses for sale would "
             f"have taken {E[2009]:.0f} months to sell at the pace of the time. <bookmark mark='b'/> In 2020, "
             f"{E[2020]:.1f} months: buyers took everything. <bookmark mark='c'/> In 2025, {E[2025]:.1f} months again, "
             "close to the level of the crash. Builders have finished homes to sell, and too few buyers who can borrow "
             "enough to buy them at today's prices and rates.",
             base=[ch.frame, src], steps=[[ch.lines["months' supply"], m1], m2, m3])

    def sales(self):
        S = R["supply"]["sales"]
        ch = line_chart({"new homes sold": ({y: v / 1e3 for y, v in S.items() if 1990 <= y <= 2025}, HOUSE)}, x=(1990, 2025),
                        y=(0, 1.4), xticks=[1990, 2000, 2005, 2011, 2015, 2020, 2025], yticks=[0, 0.4, 0.8, 1.2],
                        yfmt=lambda v: f"{v:.1f}m", ylabel="new single-family houses sold a year", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        pk = max((y for y in S if y <= 2010), key=S.get)
        lo = min((y for y in S if 2008 <= y <= 2015), key=S.get)
        m1 = marker(ch.ax, pk, S[pk] / 1e3, f"{pk}: {S[pk] / 1e3:.2f}m", PRICE, side=UP)
        m2 = marker(ch.ax, lo, S[lo] / 1e3, f"{lo}: {S[lo] / 1e3:.2f}m", BAD, side=DOWN)
        m3 = marker(ch.ax, 2025, S[2025] / 1e3, f"2025: {S[2025] / 1e3:.2f}m", HOUSE, side=UP)
        src = source("Census Bureau, new one-family houses sold (annual averages of SAAR), via FRED", size=12)
        beat(self,
             "And sales of new houses. <bookmark mark='a'/> At the top of the boom, in "
             f"{pk}, builders sold {S[pk] / 1e3:.2f} million new single-family houses. <bookmark mark='b'/> In {lo}, "
             f"{S[lo] / 1e3:.2f} million, a quarter of that. <bookmark mark='c'/> In 2025, {S[2025] / 1e3:.2f} million: "
             "the market has come back to the middle, not to the boom.",
             base=[ch.frame, src], steps=[[ch.lines["new homes sold"], m1], m2, m3])
