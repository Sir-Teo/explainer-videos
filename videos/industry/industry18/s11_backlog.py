from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403


class Backlog(VoiceoverScene):
    def construct(self):
        card(self, 9, "The order book and the lessors", "Who is waiting in the queue, and what is a place in it worth?",
             "Chapter nine. The order book, and the companies that own a large part of the world's airliners without "
             "flying any of them.", lit=("unit", "dollar"))
        self.book()
        self.lessor()
        self.scarce()

    def book(self):
        L = R["lessors"]
        tot = L["ab_orders"]
        W = 11.0
        x0 = -5.5
        d = Rectangle(width=W * L["ab_deliv"] / tot, height=0.8, stroke_width=0, fill_color=AIRBUS, fill_opacity=0.95)
        d.move_to([x0 + d.width / 2, 0.6, 0])
        d.grow = LEFT
        b = Rectangle(width=W * L["ab_backlog"] / tot, height=0.8, stroke_width=0, fill_color=PRICE, fill_opacity=0.9)
        b.move_to([x0 + d.width + b.width / 2, 0.6, 0])
        b.grow = LEFT
        frame = Rectangle(width=W, height=0.8, stroke_color=GREY_B, stroke_width=1.5, fill_opacity=0).move_to([0, 0.6, 0])
        ld = tx(f"delivered: {L['ab_deliv']:,}", 17, AIRBUS, bold=True).next_to(d, DOWN, buff=0.15)
        lb = tx(f"still to build: {L['ab_backlog']:,}", 17, PRICE, bold=True).next_to(b, DOWN, buff=0.15)
        top = tx(f"every Airbus airliner ever ordered: {tot:,}, from 455 customers", 18, WHITE, bold=True).next_to(frame, UP, buff=0.25)
        share = tx(f"{100 * L['ab_backlog'] / tot:.0f}% of every Airbus ever ordered has not yet been built", 18, PRICE, bold=True).move_to([0, -1.5, 0])
        src = source("Airbus SE, Annual Report 2025: orders and deliveries since the start, backlog at 31 December 2025", size=12)
        beat(self,
             f"Since its first airliner, Airbus has taken orders for {tot:,} aircraft from four hundred and fifty-five "
             f"customers. <bookmark mark='a'/> It has delivered {L['ab_deliv']:,} of them. <bookmark mark='b'/> The other "
             f"{L['ab_backlog']:,} are still to be built. <bookmark mark='c'/> A third of everything Airbus has ever sold is "
             "still in the queue. Who is in it? Airlines, and a kind of company most passengers never hear of.",
             base=[frame, top, src], steps=[[d, ld], [b, lb], share])

    def lessor(self):
        L = R["lessors"]
        maker = VGroup(draw.factory(1.6, AIRBUS), tx("the maker", 16, AIRBUS, bold=True)).arrange(DOWN, buff=0.1).move_to([-5.0, 0.6, 0])
        lessor = VGroup(draw.coin_stack(7, 0.3), tx("the lessor", 16, PRICE, bold=True)).arrange(DOWN, buff=0.1).move_to([0, 0.6, 0])
        airline = VGroup(draw.plane(1.8, WHITE), tx("the airline", 16, WHITE, bold=True)).arrange(DOWN, buff=0.1).move_to([5.0, 0.6, 0])
        a1 = Arrow([-3.9, 1.0, 0], [-1.0, 1.0, 0], buff=0.1, stroke_width=4, color=AIRBUS)
        a1l = tx("sells the jet", 14, AIRBUS).next_to(a1, UP, buff=0.05)
        a2 = Arrow([1.0, 1.0, 0], [3.8, 1.0, 0], buff=0.1, stroke_width=4, color=WHITE)
        a2l = tx("rents it out for years", 14, WHITE).next_to(a2, UP, buff=0.05)
        a3 = Arrow([3.8, 0.0, 0], [1.0, 0.0, 0], buff=0.1, stroke_width=4, color=PRICE)
        a3l = tx("monthly rent", 14, PRICE).next_to(a3, DOWN, buff=0.05)
        stats = stat_cards([(f"{L['owned']:,}", "aircraft AerCap owned, end of 2025", PRICE),
                            (f"{L['order']}", "new aircraft it had on order", AIRBUS),
                            (f"{L['em']}%", "of its lease revenue from emerging-market airlines", GREY_A)], y=-1.9, size=34, span=12)
        src = source("AerCap Holdings, Form 20-F 2025", size=12)
        beat(self,
             "The lessors. <bookmark mark='a'/> A lessor buys airliners from the makers, often straight from the order "
             "book, <bookmark mark='b'/> and rents them to airlines for years at a time, collecting rent each month. The "
             "airline gets a new jet without finding a hundred million dollars, and can hand it back. "
             f"<bookmark mark='c'/> AerCap, which calls itself the global leader in aircraft leasing, owned "
             f"{L['owned']:,} aircraft at the end of 2025, with {L['order']} more on order, and earned {L['em']} per cent "
             "of its lease revenue from airlines in emerging markets.",
             base=[maker, lessor, airline, src], steps=[[a1, a1l], [a2, a2l, a3, a3l], stats])

    def scarce(self):
        L = R["lessors"]
        m = {y: 100 * v for y, v in L["margins"].items()}
        ch = line_chart({"AerCap": (m, PRICE)}, x=(2015, 2025), y=(-15, 50), xticks=[2015, 2017, 2019, 2021, 2023, 2025],
                        yticks=[-10, 0, 10, 20, 30, 40, 50], yfmt=lambda v: f"{v:.0f}%", ylabel="AerCap's net income as a share of revenue",
                        width=7.0, height=4.2, center=(-2.6, -0.4), label_end=False)
        ax = ch.ax
        r22 = marker(ax, 2022, m[2022], "2022: jets stranded in Russia written off", BAD, side=DOWN)
        r25 = marker(ax, 2025, m[2025], f"2025: ${L['russia']:.1f}bn recovered from insurers", GOOD, side=LEFT)
        sale = VGroup(tx(f"in 2025 AerCap sold {L['sold']} older jets", 16, WHITE, bold=True),
                      tx("average age: 15 years", 15, GREY_A),
                      tx(f"for ${L['proceeds']:.1f}bn", 16, WHITE, bold=True),
                      tx(f"${L['gain']:,}m more than their book value", 17, GOOD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.2, 0.6, 0])
        src = source("AerCap Holdings, Forms 20-F, via SEC company facts; Form 20-F 2025", size=12)
        beat(self,
             "Leasing is usually a steady business: AerCap earned around a fifth of its revenue as profit for years. "
             "<bookmark mark='a'/> The swings come from outside. In 2022 it wrote off the jets it could not get back from "
             f"Russian airlines; <bookmark mark='b'/> in 2025 it recovered {L['russia']:.1f} billion dollars from its "
             "insurers, after a London court ruled in its favour. <bookmark mark='c'/> But look at what a decade's queue "
             f"does to the value of an old jet. In 2025 AerCap sold {L['sold']} aircraft averaging fifteen years old, for "
             f"{L['proceeds']:.1f} billion dollars, {L['gain']:,} million more than its own books said they were worth. "
             "When new jets are years away, a used one that can fly tomorrow is worth more.",
             base=[ch.frame, ch.lines["AerCap"], src], steps=[r22, r25, sale])
