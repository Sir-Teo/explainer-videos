from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403


class Backlog(VoiceoverScene):
    def construct(self):
        card(self, 5, "Paid in advance", "Why does a software company's cash run ahead of its profit?",
             "Chapter five. Paid in advance. Subscription customers usually pay for the year before they use it, and often "
             "sign for several years at once.", lit=("dollar",))
        self.billing()
        self.cash()
        self.rpo()
        self.giants()

    def billing(self):
        months = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.75, height=0.5, stroke_width=0, fill_color=SUB if i < 1 else GA,
                                           fill_opacity=0.9) for i in range(12)]).arrange(RIGHT, buff=0.1).move_to([0, 0.6, 0])
        labs = VGroup(*[tx(m_, 12, GREY_A).next_to(months[i], DOWN, buff=0.1) for i, m_ in enumerate("JFMAMJJASOND")])
        inv = VGroup(tx("invoice: the whole year, paid in January", 17, PROFIT, bold=True), Arrow(UP * 0.4, DOWN * 0.1, color=PROFIT)).arrange(DOWN, buff=0.1)
        inv.next_to(months[0], UP, buff=0.15).shift(RIGHT * 2.0)
        rev = tx("revenue: one twelfth a month, as the service is delivered", 17, SUB, bold=True).move_to([0, -1.2, 0])
        q = quote(["'We generally invoice our customers in advance, in annual installments'"], "Salesforce, Form 10-K for fiscal 2026",
                  size=17).move_to([0, -2.4, 0])
        beat(self,
             "Here is how a typical contract is paid. <bookmark mark='a'/> The customer is invoiced for the whole year at the "
             "start and pays within a month. <bookmark mark='b'/> But the company counts the revenue a twelfth at a time, as "
             "it delivers the service. Until then the money sits on the balance sheet as deferred revenue: cash received for "
             "work still owed. <bookmark mark='c'/> Salesforce says so plainly in its annual report.",
             base=[months, labs], steps=[inv, rev, q])

    def cash(self):
        Cc = R["cohorts"]
        items = [("operating income", Cc["crm_op"], PROFIT, bn(Cc["crm_op"])),
                 ("cash from operations", Cc["crm_ocf"], SUB, bn(Cc["crm_ocf"])),
                 ("deferred revenue, end of January 2026", Cc["crm_def"], STOCK, bn(Cc["crm_def"]))]
        rows = hbars(items, max_value=26, x0=1.0, top=1.2, row=1.0, length=4.8, size=17, bar_h=0.55)
        hd = tx("Salesforce, year to January 2026", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Salesforce, Form 10-K for fiscal 2026; deferred revenue via SEC company facts", size=12)
        beat(self,
             f"<bookmark mark='a'/> So Salesforce's operating income was {Cc['crm_op']:.1f} billion dollars last year, "
             f"<bookmark mark='b'/> but its operating cash flow was {Cc['crm_ocf']:.1f} billion: customers paid ahead, and the "
             "stock it pays employees costs no cash. <bookmark mark='c'/> At the year's end it held "
             f"{Cc['crm_def']:.0f} billion dollars of customers' money for service it had not yet delivered. A growing "
             "subscription company is financed in part by its own customers.",
             base=[rows.axis, hd, src], steps=list(rows))

    def rpo(self):
        Cc = R["cohorts"]
        items = [("next twelve months' revenue already contracted", Cc["crm_crpo"], SUB, bn(Cc["crm_crpo"])),
                 ("all revenue under contract, not yet recognized", Cc["crm_rpo"], STOCK, bn(Cc["crm_rpo"])),
                 ("revenue in the year just ended", Cc["crm_rev"], GA, bn(Cc["crm_rev"]))]
        rows = hbars(items, max_value=80, x0=1.2, top=1.2, row=1.0, length=4.8, size=17, bar_h=0.55)
        hd = tx("Salesforce's remaining performance obligation, 31 January 2026", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Salesforce, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "And contracts often run for several years. <bookmark mark='a'/> At the start of 2026 Salesforce already had "
             f"{Cc['crm_crpo']:.1f} billion dollars of revenue contracted for the next twelve months, <bookmark mark='b'/> and "
             f"{Cc['crm_rpo']:.1f} billion in all: <bookmark mark='c'/> nearly twice the revenue of the year just ended. "
             "Accountants call it the remaining performance obligation. Investors read it as the year ahead, half written.",
             base=[rows.axis, hd, src], steps=list(rows))

    def giants(self):
        Cc = R["cohorts"]
        items = [("Microsoft: commercial, 30 June 2026", Cc["ms_rpo"], STOCK, f"{bn(Cc['ms_rpo'], 0)} (+84%)"),
                 ("Oracle: 31 May 2026", Cc["or_rpo"], LIC, f"{bn(Cc['or_rpo'], 0)}, from $138bn"),
                 ("Oracle's revenue that year", Cc["or_rev"], GA, bn(Cc["or_rev"], 0))]
        rows = hbars(items, max_value=700, x0=0.4, top=1.2, row=1.0, length=4.4, size=17, bar_h=0.55)
        hd = tx("the largest backlogs in software", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx("Oracle: 'primarily attributable to certain significant cloud contracts'", 16, GREY_B).to_edge(DOWN, buff=0.8)
        src = source("Microsoft, Form 10-K for fiscal 2026; Oracle, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "Lately the backlogs have exploded. <bookmark mark='a'/> Microsoft's commercial backlog was "
             f"{Cc['ms_rpo']:.0f} billion dollars at the end of June 2026, up 84 per cent in a year. <bookmark mark='b'/> "
             f"Oracle's was {Cc['or_rpo']:.0f} billion, up from 138 billion, <bookmark mark='c'/> almost ten times its revenue "
             "for the year. Oracle says the jump came primarily from certain significant cloud contracts. In this series' "
             "reading, most of it is not software at all but computing power for artificial intelligence, contracted years "
             "ahead. Chapter eight, and Part 37, come back to it.",
             base=[rows.axis, hd, note, src], steps=list(rows))
