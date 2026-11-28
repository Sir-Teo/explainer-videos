from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403


class Ai(VoiceoverScene):
    def construct(self):
        card(self, 8, "When the copy stops being free", "What happens to software's economics when every answer costs computing power?",
             "Chapter eight. When the copy stops being free. Artificial intelligence changes the oldest fact in this film: "
             "each use of an AI model costs real computing power.", lit=("make", "change"))
        self.capex()
        self.fcf()
        self.margin()
        self.oracle()
        self.seats()

    def capex(self):
        A = R["ai"]
        items = [(str(y), A["ms_capex"][y], STOCK if y < 2024 else AI, f"${A['ms_capex'][y]:.0f}bn") for y in sorted(A["ms_capex"]) if y >= 2016]
        cols = vbars(items, base_y=-2.3, height=3.8, width=0.75, gap=0.32, size=13, max_value=125)
        hd = tx("Microsoft's additions to property and equipment, fiscal years to June", 20, WHITE, bold=True).to_edge(UP, buff=0.6)
        src = source("Microsoft, Forms 10-K via SEC company facts (fiscal 2026: $115,948m)", size=12)
        beat(self,
             "Look at what Microsoft spends on buildings and machines. <bookmark mark='a'/> In 2016, about "
             f"{A['ms_capex'][2016]:.0f} billion dollars; by 2023, {A['ms_capex'][2023]:.0f} billion. <bookmark mark='b'/> Then "
             f"{A['ms_capex'][2024]:.0f} billion, {A['ms_capex'][2025]:.0f} billion, and in the year to June 2026, "
             f"{A['ms_capex'][2026]:.0f} billion: {100 * A['ms_capex_share'][2026]:.0f} cents of every dollar of revenue, much "
             "of it data centres and the computers inside them.",
             base=[hd, src], steps=[VGroup(*[cols[i] for i, it in enumerate(items) if int(it[0]) < 2024]),
                                    VGroup(*[cols[i] for i, it in enumerate(items) if int(it[0]) >= 2024])])

    def fcf(self):
        A = R["ai"]
        H = R["hook"]
        fc = {y: v for y, v in A["ms_fcf"].items() if y >= 2016}
        oi = {y: H["hist"][y][1] for y in fc}
        ch = line_chart({"operating income": (oi, PROFIT), "free cash flow": (fc, SUB)}, x=(2016, 2026), y=(0, 170),
                        xticks=[2016, 2018, 2020, 2022, 2024, 2026], yticks=[0, 50, 100, 150], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="Microsoft, fiscal years to June, $bn", width=8.6, height=4.3, center=(-1.0, -0.45))
        src = source("Microsoft, Forms 10-K via SEC company facts (operating cash flow less additions to property and equipment)", size=12)
        beat(self,
             "That spending shows up in cash. <bookmark mark='a'/> Microsoft's operating income kept climbing, to "
             f"{oi[2026]:.0f} billion dollars. <bookmark mark='b'/> Its free cash flow, the cash left after paying for the "
             f"buildings and machines, peaked at {max(fc.values()):.0f} billion in 2024 and fell to {fc[2026]:.0f} billion in "
             f"2026. Microsoft is now putting about {100 * A['ms_capex'][2026] / (A['ms_fcf'][2026] + A['ms_capex'][2026]):.0f} per "
             "cent of the cash its operations bring in back into buildings, chips and power.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["operating income"], ch.labels["operating income"]),
                                          VGroup(ch.lines["free cash flow"], ch.labels["free cash flow"])])

    def margin(self):
        A = R["ai"]
        q = quote(["'Microsoft Cloud gross margin percentage decreased to 66% driven by continued investments",
                   "in AI infrastructure and growing AI product usage'"], "Microsoft, Form 10-K for fiscal 2026", size=18).move_to([0, 1.6, 0])
        c = stat_cards([(f"{100 * A['ms_gm'][2024]:.1f}%", "Microsoft's gross margin, fiscal 2024", GA),
                        (f"{100 * A['ms_gm'][2026]:.1f}%", "fiscal 2026", AI)], y=-1.0, size=36, span=9)
        src = source("Microsoft, Form 10-K for fiscal 2026; SEC company facts", size=12)
        beat(self,
             "And the cost of each copy is no longer zero. <bookmark mark='a'/> Microsoft told its shareholders that the gross "
             "margin of its cloud business fell to 66 per cent because of its spending on AI infrastructure and the growing "
             "use of its AI products. <bookmark mark='b'/> Across the company, the gross margin slipped from "
             f"{100 * A['ms_gm'][2024]:.1f} per cent to {100 * A['ms_gm'][2026]:.1f}. Each question answered by an AI model "
             "uses chips and electricity, so the more customers use it, the more it costs, much more like a factory than like "
             "a copy.",
             base=[src], steps=[q, c])

    def oracle(self):
        A = R["ai"]
        cap = {y: v for y, v in A["or_capex"].items() if y >= 2016}
        fcf = {y: v for y, v in A["or_fcf"].items() if y >= 2016}
        ch = line_chart({"capital spending": (cap, LIC), "free cash flow": (fcf, PROFIT)}, x=(2016, 2026), y=(-30, 60),
                        xticks=[2016, 2018, 2020, 2022, 2024, 2026], yticks=[-20, 0, 20, 40, 60], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="Oracle, fiscal years to May, $bn", width=8.6, height=4.3, center=(-1.0, -0.45))
        zero = DashedLine(ch.ax.c2p(2016, 0), ch.ax.c2p(2026, 0), color=GREY_B, stroke_width=1.2)
        src = source("Oracle, Forms 10-K via SEC company facts; Form 10-K for fiscal 2026", size=12)
        beat(self,
             "Oracle, the database company, has gone furthest. <bookmark mark='a'/> For years it spent one or two billion "
             f"dollars a year on equipment. In its latest year, {cap[2026]:.0f} billion, {100 * A['or_capex_share'][2026]:.0f} "
             "cents of every dollar of revenue. <bookmark mark='b'/> Its free cash flow, steady at twelve billion or so for "
             f"years, turned negative: {fcf[2026]:.0f} billion dollars. In this series' reading, it is betting that the contracts "
             "in its backlog will pay for the data centres: a software company turning itself into a builder of computing "
             "plants.",
             base=[ch.frame, zero, src], steps=[VGroup(ch.lines["capital spending"], ch.labels["capital spending"]),
                                                VGroup(ch.lines["free cash flow"], ch.labels["free cash flow"])])

    def seats(self):
        lines = [("software has been priced by the seat: a fee for each person who uses it", GA),
                 ("AI agents do work that people did: fewer seats, or a new unit?", AI),
                 ("Salesforce sells Agentforce as 'digital labor'; prices may move toward use and outcomes", SALES),
                 ("the free copy made software rich; the costly answer may change who wins", STOCK)]
        g = VGroup(*[tx(t, 18, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.1, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "And the unit of sale is shifting. <bookmark mark='a'/> Business software has long been priced by the seat: a fee "
             "for each person who uses it. <bookmark mark='b'/> If AI agents do work that people did, the seats shrink. "
             "<bookmark mark='c'/> Salesforce now describes its Agentforce product as digital labour for employees and "
             "customers; in this series' reading, prices are moving toward charging by use or by result. <bookmark mark='d'/> In this series' "
             "reading, the free copy is what made software so profitable; the costly answer may change who wins next.",
             base=[head("Seats, agents and the unit of sale")], steps=list(g))
