from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403


class Two(VoiceoverScene):
    def construct(self):
        card(self, 5, "Why only two", "Why doesn't a third maker break in?",
             "Chapter five. Why only two. Airlines wait ten years for their jets. Why does nobody build a third factory?",
             lit=("moat",))
        self.icons()
        self.waits()
        self.entrant()
        self.others()

    def icons(self):
        T = R["two"]
        per = 25

        def stack(n, col, x0):
            g = VGroup()
            for i in range(round(n / per)):
                r_, c_ = divmod(i, 6)
                g.add(draw.plane(0.78, col, windows=False).move_to([x0 + 0.92 * c_, 1.5 - 0.5 * r_, 0]))
            return g
        a = stack(T["ab"], AIRBUS, -6.0)
        b = stack(T["ba"], BOEING, 1.2)
        la = tx(f"Airbus: {T['ab']} ({100 * T['share_ab']:.0f}%)", 20, AIRBUS, bold=True).next_to(a, UP, buff=0.2)
        lb = tx(f"Boeing: {T['ba']} ({100 * (1 - T['share_ab']):.0f}%)", 20, BOEING, bold=True).next_to(b, UP, buff=0.2).align_to(la, UP)
        key = tx(f"each icon: {per} airliners delivered in 2025", 15, GREY_B).to_edge(DOWN, buff=0.75)
        hist = tx(f"Boeing delivered {T['ba_hist'][2023]} in 2023 and {T['ba_hist'][2024]} in 2024; Airbus {T['ab_hist'][2024]} "
                  "in 2024", 15, GREY_A).next_to(key, UP, buff=0.15)
        src = source("Airbus SE, Annual Reports 2025; The Boeing Company, Form 10-K 2025", size=12)
        beat(self,
             "First, the size of the two. <bookmark mark='a'/> In 2025 Airbus delivered "
             f"{T['ab']} airliners, {100 * T['share_ab']:.0f} per cent of the two makers' total. <bookmark mark='b'/> Boeing "
             f"delivered {T['ba']}. <bookmark mark='c'/> Boeing is climbing back: it delivered {T['ba_hist'][2023]} in "
             f"2023 and only {T['ba_hist'][2024]} in 2024, the year of the door plug and the strike, while Airbus delivered "
             f"{T['ab_hist'][2024]}.",
             base=[key, src], steps=[[a, la], [b, lb], hist])

    def waits(self):
        T = R["two"]
        items = [("Airbus, all models", T["ab_years"], AIRBUS, f"{T['ab_backlog']:,} aircraft: {T['ab_years']:.1f} years"),
                 ("Boeing, all models", T["ba_years"], BOEING, f"{T['ba_backlog']:,} aircraft: {T['ba_years']:.1f} years"),
                 ("Boeing 787", T["y787"], BOEING, f"{T['y787']:.1f} years"),
                 ("Boeing 737", T["y737"], BOEING, f"{T['y737']:.1f} years")]
        rows = hbars(items, max_value=12, x0=-2.0, top=1.5, row=0.9, length=5.6, size=17, bar_h=0.5)
        note = tx("unfilled firm orders at the end of 2025, divided by 2025's deliveries", 15, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("Airbus SE, Annual Report 2025 (backlog); The Boeing Company, Form 10-K 2025 (undelivered units under "
                     "firm orders)", size=12)
        beat(self,
             "Now the queue. Divide each maker's unfilled orders by what it delivered in a year. <bookmark mark='a'/> "
             f"Airbus had {T['ab_backlog']:,} aircraft on order at the end of 2025: {T['ab_years']:.0f} years of work at "
             f"2025's pace. <bookmark mark='b'/> Boeing had {T['ba_backlog']:,}: about {T['ba_years']:.0f} years. "
             f"<bookmark mark='c'/> For a 787 the wait is nearly {T['y787']:.0f} years, <bookmark mark='d'/> and for a 737 "
             f"about {T['y737']:.0f}. In most industries a decade's queue invites a competitor. Here it has not.",
             base=[rows.axis, note, src], steps=[rows[0], rows[1], rows[2], rows[3]])

    def entrant(self):
        T = R["two"]
        P = R["programme"]
        e = T["entrant"]
        ch = line_chart({"entrant": (e, ENGINE)}, x=(60, 120), y=(-30, 20), xticks=[60, 70, 80, 90, 100, 110, 120],
                        yticks=[-30, -20, -10, 0, 10, 20], xfmt=lambda v: f"${int(v)}m", yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="a new maker's programme, value today (the Works)", label_end=False, width=9.4, height=4.3,
                        center=(-0.4, -0.5), xlabel="the price airlines pay for a single-aisle jet")
        ax = ch.ax
        zero = DashedLine(ax.c2p(60, 0), ax.c2p(120, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        be = next(pr for pr in sorted(e) if e[pr] >= 0)
        m110 = marker(ax, 110, e[110], f"at ${P['price']:.0f}m: {bn(e[110])}", GOOD, side=LEFT)
        m80 = marker(ax, 80, e[80], f"at $80m: {bn(e[80])}", BAD, side=RIGHT)
        inc = VGroup(tx(f"the incumbent's {T['inc_n']:,}th aircraft", 15, BOEING, bold=True),
                     tx(f"costs about ${T['inc_cost']:.0f}m to build (the Works)", 15, BOEING, bold=True)).arrange(DOWN, buff=0.06).move_to([-3.0, 1.7, 0])
        first = tx(f"the newcomer's first: ${P['first']:.0f}m", 15, BAD, bold=True).next_to(inc, DOWN, buff=0.2)
        tag = estimate_tag("the Works' programme, its price varied; illustrative", size=12)
        beat(self,
             "Why not? Go back to the learning curve. <bookmark mark='a'/> In our model, a maker that has built "
             f"{T['inc_n']:,} of a type, as Boeing had built of the 737, makes each new one for about "
             f"{T['inc_cost']:.0f} million dollars. A newcomer's first costs {P['first']:.0f} million. "
             f"<bookmark mark='b'/> If airlines go on paying {P['price']:.0f} million, the newcomer's programme is worth "
             f"{e[110]:.0f} billion. <bookmark mark='c'/> But the incumbents can cut their price far below that and still "
             "make money. At eighty million a jet, the newcomer's programme loses "
             f"{-e[80]:.0f} billion. <bookmark mark='d'/> Its value falls with every dollar off the price, and it needs about "
             f"{be} million just to break even. The incumbents' past output is the moat: a newcomer has to pay for the "
             "learning they already paid for.",
             base=[ch.frame, zero, tag], steps=[[inc, first], m110, m80, ch.lines["entrant"]])

    def others(self):
        T = R["two"]
        erj = T["erj"]
        steps = [
            VGroup(tx("Canada: Bombardier's C-Series", 20, AIRBUS, bold=True),
                   tx(f"sold to Airbus in {T['a220']}, renamed the A220; Bombardier left the partnership in 2020", 16, GREY_A)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-0.6, 1.6, 0]),
            VGroup(tx("Brazil: Embraer, regional jets", 20, SUPPLIER, bold=True),
                   tx(f"average profit margin 2015-2025: {100 * np.mean([v for y, v in erj.items() if 2015 <= y <= 2025]):.1f}%", 16, GREY_A)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-0.6, 0.0, 0]),
            tx("Two makers who have each built many thousands, and a queue that pays them to wait.", 18, PRICE, bold=True).move_to([0, -1.8, 0]),
        ]
        for s in steps[:2]:
            s.align_to(steps[0], LEFT)
        src = source("Airbus SE, Annual Report 2025 (Airbus Canada); Embraer S.A., Forms 20-F, via SEC company facts", size=12)
        beat(self,
             "Others have tried. <bookmark mark='a'/> Canada's Bombardier designed a new single-aisle jet, the C-Series. "
             f"In {T['a220']} it sold the programme to Airbus, which renamed it the A220, and in 2020 Bombardier left the "
             "partnership altogether. <bookmark mark='b'/> Brazil's Embraer builds smaller regional jets; over the decade "
             "to 2025 its profit averaged about nothing. <bookmark mark='c'/> So the industry stays at two: each has built "
             "thousands, each has a decade of orders, and a newcomer would need tens of billions and fifteen years to find "
             "out whether it could match them.",
             base=[src], steps=steps)
