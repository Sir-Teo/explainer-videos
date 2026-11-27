from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Debt(VoiceoverScene):
    def construct(self):
        card(self, 4, "Other people's money", "Who lends against buildings, and what happens when they will not?",
             "Chapter four. Other people's money. Almost every building is bought partly with borrowed money, and the "
             "loans, not the buildings, are where property's crises begin.", lit=("dollar", "change"))
        self.dollar()
        self.cover()
        self.banks()
        self.delinq()
        self.wall()

    def dollar(self):
        D = R["debt"]["pld"]
        parts = [("running the buildings", D["rentexp"] / D["rental"], LOAN), ("net operating income", D["noi"] / D["rental"], INCOME)]
        bar = viz.bar_split(parts, 1.0, width=11.0, height=0.9).move_to([0, 0.9, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}c", 22, c, bold=True), tx(n, 15, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        w = draw.warehouse(2.4).move_to([0, 2.6, 0]).scale(0.7)
        src = source("Prologis, Inc., Form 10-K for 2025: rental revenues and expenses, real estate segment", size=12)
        beat(self,
             "Start with a dollar of rent at the largest warehouse landlord, Prologis, in 2025. <bookmark mark='a'/> About "
             f"{100 * D['rentexp'] / D['rental']:.0f} cents went on running the buildings: taxes, insurance, repairs, "
             f"management. <bookmark mark='b'/> The other {100 * D['noi'] / D['rental']:.0f} cents were net operating "
             f"income: {D['noi']:.1f} billion dollars on {D['rental']:.1f} billion of rent.",
             base=[w, src], steps=[[bar[0], labs[0]], [bar[1], labs[1]]])

    def cover(self):
        D = R["debt"]["pld"]
        off = R["run"]["office"]["at"]
        items = [("Prologis, 2025: net operating income over interest", D["noi"] / D["interest"], GOOD, f"{D['noi'] / D['interest']:.1f}x"),
                 ("the Works' office in 2026, over its old interest", off["extend"]["interest_cover"], BAD,
                  f"{off['extend']['interest_cover']:.2f}x")]
        rows = hbars(items, max_value=7, x0=0.6, top=1.0, row=1.2, length=5.4, size=17, bar_h=0.55)
        one = DashedLine([0.6 + 5.4 / 7, 1.9, 0], [0.6 + 5.4 / 7, 0.45, 0], stroke_color=GREY_B, stroke_width=2)
        onel = tx("1x: income just pays the interest", 14, GREY_B).next_to(one, UP, buff=0.1)
        src = source("Prologis, Inc., Form 10-K for 2025 (interest expense via SEC company facts); the Works", size=12)
        beat(self,
             "From that income come the lenders. <bookmark mark='a'/> Prologis paid "
             f"{D['interest']:.1f} billion dollars of interest in 2025: its income covered its interest about "
             f"{D['noi'] / D['interest']:.0f} times. <bookmark mark='b'/> The Works' office covers its old interest only "
             f"{off['extend']['interest_cover']:.2f} times: every month it does not earn its loan's interest. Lenders measure "
             "a borrower by this ratio, and by how much the building is worth against the loan, and when either fails they "
             "stop lending.",
             base=[rows.axis, one, onel, src], steps=[rows[0], rows[1]])

    def banks(self):
        D = R["debt"]
        L = {y: v / 1e3 for y, v in D["loans"].items() if y <= 2025}
        ch = line_chart({"commercial property loans at American banks": (L, LOAN)}, x=(2005, 2025), y=(0, 3.5),
                        xticks=[2005, 2010, 2015, 2020, 2025], yticks=[0, 1, 2, 3], yfmt=lambda v: f"${v:.0f}tn",
                        ylabel="commercial real estate loans held by all commercial banks (annual average)", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        m1 = marker(ch.ax, 2005, L[2005], f"2005: ${L[2005]:.2f}tn", ALL, side=RIGHT)
        m2 = marker(ch.ax, 2025, L[2025], f"2025: ${L[2025]:.2f}tn", LOAN, side=DOWN)
        src = source("Federal Reserve, H.8: real estate loans, commercial real estate, all commercial banks, via FRED", size=12)
        beat(self,
             "Who lends? Insurers, bond investors who buy pools of mortgages, private lenders, and above all the banks. "
             f"<bookmark mark='a'/> In 2005 American banks held about {L[2005]:.1f} trillion dollars of commercial property "
             f"loans. <bookmark mark='b'/> In 2025, {L[2025]:.1f} trillion, and in October 2026 "
             f"{D['loans_now'] / 1e3:.2f} trillion dollars.",
             base=[ch.frame, src], steps=[[ch.lines["commercial property loans at American banks"], m1], m2])

    def delinq(self):
        D = R["debt"]
        dq = D["delinq"]
        ch = line_chart({"delinquent": (dq, BAD)}, x=(1991, 2026.5), y=(0, 13), xticks=[1991, 1995, 2000, 2005, 2010, 2015, 2020, 2026],
                        yticks=[0, 3, 6, 9, 12], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="share of banks' commercial property loans past due 30 days or more, or not accruing interest", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        k10 = max((k for k in dq if 2009 <= k <= 2012), key=dq.get)
        k19 = max(k for k in dq if k < 2020)
        kn = max(dq)
        m1 = marker(ch.ax, min(dq), dq[min(dq)], f"1991: {D['dq_1991']:.1f}%", BAD, side=RIGHT)
        m2 = marker(ch.ax, k10, dq[k10], f"2010: {D['dq_2010']:.1f}%", BAD, side=UP)
        m3 = marker(ch.ax, k19, dq[k19], f"2019: {D['dq_2019']:.2f}%", GOOD, side=DOWN)
        m4 = marker(ch.ax, kn, dq[kn], f"2026: {D['dq_now']:.2f}%", VALUE, side=UP)
        src = source("Federal Reserve, delinquency rate on commercial real estate loans excluding farmland, all commercial "
                     "banks (quarterly, seasonally adjusted), via FRED", size=12)
        beat(self,
             "How often are these loans not paid? <bookmark mark='a'/> In 1991, after a building boom and a banking crisis, "
             f"{D['dq_1991']:.0f} per cent of banks' commercial property loans were past due. <bookmark mark='b'/> In 2010, "
             f"{D['dq_2010']:.1f} per cent. <bookmark mark='c'/> In 2019, under one per cent. <bookmark mark='d'/> By 2026, "
             f"{D['dq_now']:.1f} per cent: more than twice the level before the pandemic, but far from the earlier crises. "
             "In this series' reading, the office losses have so far been spread thin across a much larger book, or postponed.",
             base=[ch.frame, src], steps=[[ch.lines["delinquent"], m1], m2, m3, m4])

    def wall(self):
        q = quote(["'A substantial volume of non-agency commercial mortgage-backed securities (CMBS) debt is set to mature",
                   "in late 2026, and, if borrowers face difficulties in refinancing, potential forced property sales could",
                   "occur and push prices lower. To date, lenders' willingness to extend or restructure maturing loans has",
                   "helped mitigate this risk.'"], "Federal Reserve, Financial Stability Report, November 2026", size=16).move_to([0, 1.4, 0])
        why = bullets(["a loan falls due on a fixed date, whatever rates are that year",
                       "a building that cannot be refinanced must be sold, recapitalized or handed back",
                       "a lender that extends the loan postpones the loss and hopes the income returns"], size=18).move_to([0, -1.3, 0])
        tag = estimate_tag("this series' summary of how maturities turn into sales", size=12)
        beat(self,
             "Which is why the dates matter. <bookmark mark='a'/> In November 2026 the Federal Reserve warned that a large "
             "volume of commercial mortgage bonds would mature in late 2026, and that forced sales could push prices lower, "
             "but that lenders willing to extend or restructure had so far held that off. <bookmark mark='b'/> A loan falls "
             "due on a date, whatever rates happen to be that year. A building that cannot be refinanced must be sold, find "
             "new money or be handed back. And a lender that extends is betting, as in Run it, that the income will come back "
             "before the loss has to be counted.",
             base=[tag], steps=[q, why])
