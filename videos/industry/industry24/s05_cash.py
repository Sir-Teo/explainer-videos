from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403


class Cash(VoiceoverScene):
    def construct(self):
        card(self, 4, "Paid first, pay later", "How can a profitable contractor run out of cash?",
             "Chapter four. Paid first, pay later. A contractor's profit is thin, but its cash can be large, and the two "
             "can move in opposite directions.", lit=("dollar", "change"))
        self.one_job()
        self.book()
        self.carillion()
        self.warnings()
        self.lesson()

    def one_job(self):
        from explainer.industry.works import contractor
        C = R["cash"]
        f = contractor.job_flows(horizon=24)
        cum = {m: v for m, v in enumerate(np.cumsum(f))}
        ch = line_chart({"cash from one job": (cum, CASH)}, x=(0, 20), y=(-5, 20), xticks=[0, 4, 8, 12, 16, 20],
                        yticks=[-5, 0, 5, 10, 15, 20], xfmt=lambda v: f"month {int(v)}", yfmt=lambda v: f"${v:.0f}m",
                        ylabel="the contractor's cash from a $100m, twelve-month job", width=9.0, height=4.2, center=(-0.6, -0.5),
                        label_end=False)
        zero = DashedLine(ch.ax.c2p(0, 0), ch.ax.c2p(20, 0), stroke_color=GREY_B, stroke_width=1.5)
        pk = max(cum, key=cum.get)
        m1 = marker(ch.ax, pk, cum[pk], f"${cum[pk]:.1f}m in hand", CASH, side=UP)
        m2 = marker(ch.ax, 20, cum[20], f"in the end: ${cum[20]:.0f}m, the profit", PROFIT, side=UP)
        m2[1].shift(LEFT * 1.0)
        est = estimate_tag(f"the Works: paid {C['receive_lag']} months after the work, pays {C['pay_lag']} months after, "
                           f"{100 * C['retention']:.0f}% held back to the end, a {100 * C['margin']:.0f}% margin", size=12)
        beat(self,
             f"Take one job: a hundred million dollars of work over twelve months, at a {100 * C['margin']:.0f} per cent "
             f"margin. Each month the contractor bills for the work done and is paid {C['receive_lag']} months later, "
             f"with {100 * C['retention']:.0f} per cent held back until the end. It pays its own subcontractors and "
             f"suppliers {C['pay_lag']} months after the work. <bookmark mark='a'/> So while the job runs, cash comes in "
             f"before it goes out: at the peak, about {cum[pk]:.0f} million dollars of other people's money is sitting in "
             f"its bank account. <bookmark mark='b'/> When the job ends, the suppliers are paid, the retention comes "
             f"back, and what is left is the profit: {cum[20]:.0f} million.",
             base=[ch.frame, zero, est], steps=[[ch.lines["cash from one job"], m1], m2])

    def book(self):
        C = R["cash"]
        cash = {m: v for m, v in enumerate(C["cash"]) if m <= 48}
        prof = {m: v for m, v in enumerate(C["profit"]) if m <= 48}
        ch = line_chart({"cash in the bank": (cash, CASH), "profit earned so far": (prof, PROFIT)}, x=(0, 48), y=(0, 110),
                        xticks=[0, 12, 24, 36, 48], yticks=[0, 25, 50, 75, 100], xfmt=lambda v: f"month {int(v)}",
                        yfmt=lambda v: f"${v:.0f}m", ylabel="a contractor winning one job a month, then none", width=9.4,
                        height=4.4, center=(-0.8, -0.45), label_end=False)
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=c, stroke_width=4), tx(n, 14, c)).arrange(RIGHT, buff=0.12)
                       for n, c in (("cash in the bank", CASH), ("profit earned so far", PROFIT))]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 1.9, 0])
        stop = DashedLine(ch.ax.c2p(C["stop"], 0), ch.ax.c2p(C["stop"], 105), stroke_color=BAD, stroke_width=2)
        sl = tx("no new wins", 14, BAD, bold=True).next_to(ch.ax.c2p(C["stop"], 105), LEFT, buff=0.1).shift(DOWN * 0.2)
        p = C["peak"]
        drop = marker(ch.ax, p + 8, cash[p + 8], f"cash ${cash[p + 8]:.0f}m, down from ${cash[p]:.0f}m", BAD, side=RIGHT)
        est = estimate_tag("the Works: the same jobs, one a month for two years", size=12)
        beat(self,
             "Now a whole order book. <bookmark mark='a'/> The contractor wins one such job a month. Its profit builds "
             f"slowly, but its cash builds fast: by month {p} it holds about {cash[p]:.0f} million dollars, against "
             f"{prof[p]:.0f} million of profit earned. The difference is money owed to suppliers that has not yet fallen "
             "due. <bookmark mark='b'/> Then it stops winning. <bookmark mark='c'/> Over the next eight months its profit "
             f"keeps rising, to {prof[p + 8]:.0f} million, while its cash falls to {cash[p + 8]:.0f} million, as the bills "
             "for the old work come in and no new work pays in advance. A growing contractor looks rich; a contractor "
             "that stops growing finds out how much of that cash was never its own.",
             base=[ch.frame, est, key], steps=[[ch.lines[k] for k in ch.lines], [stop, sl], drop])

    def carillion(self):
        K = R["carillion"]
        c = stat_cards([(f"£{K['revenue']:.1f}bn", "Carillion's revenue in 2016", BUILD),
                        (f"{K['staff']:,.0f}", "people employed, around the world", ALL),
                        (f"{K['contracts']:.0f}", "contracts with the British public sector", MAKE)], y=1.0, size=38, span=12)
        what = tx("hospitals, schools, prisons, roads, railways, the armed forces", 17, GREY_A).move_to([0, -0.6, 0])
        src = source("National Audit Office, Investigation into the government's handling of the collapse of Carillion (June 2018)", size=12)
        beat(self,
             "Something like it happened, on a vast scale, to Carillion. <bookmark mark='a'/> In 2016 this British "
             f"construction and services company had {K['revenue']:.1f} billion pounds of revenue, "
             f"<bookmark mark='b'/> about {K['staff']:,.0f} people, <bookmark mark='c'/> and about {K['contracts']:.0f} "
             "contracts with the British government and other public bodies: building and running hospitals, schools, "
             "prisons, roads and railways. Its 2016 accounts, published in March 2017, showed it profitable and solvent.",
             base=[src], steps=[c[0], c[1], [c[2], what]])

    def warnings(self):
        K = R["carillion"]
        rows = VGroup(tx(f"10 July 2017: a £{K['warn1']:.0f}m provision for losses on its contracts", 19, BAD),
                      tx(f"29 September 2017: raised to £{K['warn2'] / 1e3:.2f}bn", 19, BAD),
                      tx("17 November 2017: expects to breach the terms of its loans", 19, BAD),
                      tx("15 January 2018: insolvency; the Official Receiver takes over", 19, WHITE, bold=True),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.9, 0])
        cash = tx(f"cash lost from operations in 2017: £{K['cash']:.0f}m", 20, PRICE, bold=True).move_to([0, -1.6, 0])
        src = source("National Audit Office, Investigation into the government's handling of the collapse of Carillion (June 2018)", size=12)
        beat(self,
             f"Then it unravelled in six months. <bookmark mark='a'/> On 10 July 2017 Carillion set aside {K['warn1']:.0f} "
             "million pounds for losses on its contracts. <bookmark mark='b'/> In September it raised that to over a "
             "billion. <bookmark mark='c'/> In November it warned it would break the terms of its loans. "
             "<bookmark mark='d'/> On 15 January 2018 it was declared insolvent. <bookmark mark='e'/> In 2017 its "
             f"operations had lost {K['cash']:.0f} million pounds of cash.",
             base=[src], steps=[rows[0], rows[1], rows[2], rows[3], cash])

    def lesson(self):
        K = R["carillion"]
        q = quote(["among practices a review said 'enhanced reported financial performance above underlying",
                   "operating performance': 'securing large advance payments on new contracts at the expense of",
                   "future profitability'"], "National Audit Office, citing a draft review by FTI for Carillion's lenders", size=17).move_to([0, 1.5, 0])
        pay = tx(f"suppliers paid on average {K['paydays']:.0f} days after the invoice; almost a third more than 60 days later",
                 18, WHITE).move_to([0, -0.6, 0])
        pen = tx(f"and £{K['pension']:.1f}bn of pension liabilities", 18, GREY_A).move_to([0, -1.5, 0])
        src = source("National Audit Office, Investigation into the government's handling of the collapse of Carillion (June 2018)", size=12)
        beat(self,
             "The National Audit Office's report points to the mechanism. <bookmark mark='a'/> Among the practices a "
             "review for Carillion's lenders said made its results look better than its operations: 'securing large "
             "advance payments on new contracts at the expense of future profitability'. New work brought in cash up "
             "front. <bookmark mark='b'/> Carillion was also paying its suppliers late: on average 45 days after the "
             "invoice in early 2017, with almost a third of invoices paid more than 60 days later. "
             f"<bookmark mark='c'/> And it carried {K['pension']:.1f} billion pounds of pension liabilities. In this "
             "series' reading, it is the Works' order book in real life: cash that looked like strength was money "
             "owed to others, and when the new contracts went bad there was nothing behind it.",
             base=[src], steps=[q, pay, pen])
