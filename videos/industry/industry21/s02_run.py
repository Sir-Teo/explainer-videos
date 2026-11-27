from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: sell the robot, or place it?",
             "Sell your robot for $2 million, or place it free and charge $1,000 an operation?",
             "Chapter one. Run it. You make a surgical robot. Do you sell it to hospitals for two million dollars, or put it "
             "in their operating rooms for free and charge them for every operation?", lit=("dollar", "moat"))
        self.market()
        self.sell()
        self.place()
        self.answer()
        self.real()

    def strip(self):
        U = R["run"]
        vols = U["volumes"]
        x0, w = -5.6, 11.2
        bw = w / len(vols)
        bars = VGroup(*[Rectangle(width=bw * 0.8, height=0.006 * v, stroke_width=0, fill_color=GREY_B, fill_opacity=0.8)
                        .move_to([x0 + bw * (i + 0.5), -2.2 + 0.003 * v, 0]) for i, v in enumerate(vols)])
        axis = Line([x0, -2.2, 0], [x0 + w, -2.2, 0], stroke_color=GREY_B, stroke_width=2)
        lab = VGroup(tx(f"{vols[0]:.0f} operations a year", 13, GREY_A).next_to(axis.get_start(), DOWN, buff=0.12),
                     tx(f"{vols[-1]:.0f}", 13, GREY_A).next_to(axis.get_end(), DOWN, buff=0.12),
                     tx(f"{len(vols)} hospitals, by the robotic operations each would do", 15, GREY_A).next_to(axis, DOWN, buff=0.45))
        return bars, VGroup(axis, lab), x0, bw

    def market(self):
        U = R["run"]
        bars, frame, *_ = self.strip()
        bot = draw.surgical_robot(1.6).move_to([-4.6, 1.9, 0])
        offer = VGroup(tx(f"each operation: the hospital gains ${U['value']:,.0f} and uses ${U['instrument']:,.0f} of your instruments",
                          16, WHITE),
                       tx(f"sell: ${U['price'] / 1e6:.1f}m a robot, with a service contract", 17, DEVICE, bold=True),
                       tx(f"or place it free and charge ${U['fee']:,.0f} an operation on top", 17, PRICE, bold=True)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([1.4, 1.9, 0])
        tag = estimate_tag("the Works: illustrative hospitals and costs, Intuitive's price ranges", size=12)
        beat(self,
             f"Here is the market. <bookmark mark='a'/> A hundred and one hospitals could use your robot, and they differ "
             f"in how many robotic operations they would do: from {U['volumes'][0]:.0f} a year to {U['volumes'][-1]:.0f}. "
             f"<bookmark mark='b'/> In our model each operation is worth {U['value']:,.0f} dollars more to a hospital than "
             f"the open or keyhole alternative, and uses {U['instrument']:,.0f} dollars of your instruments. "
             f"<bookmark mark='c'/> You can sell each robot for {U['price'] / 1e6:.0f} million dollars, with a service "
             f"contract, <bookmark mark='d'/> or place it free, service included, and charge {U['fee']:,.0f} dollars an "
             "operation on top of the instruments.",
             base=[frame, bot, tag], steps=[bars, offer[0], offer[1], offer[2]])

    def sell(self):
        U = R["run"]
        S = U["sell"]
        bars, frame, x0, bw = self.strip()
        buy = VGroup(*[b for b, v in zip(bars, U["volumes"]) if v >= S["threshold"]])
        thr = DashedLine([x0 + bw * (S["threshold"] - 50) / 5, -2.3, 0], [x0 + bw * (S["threshold"] - 50) / 5, 1.2, 0],
                         stroke_color=DEVICE, stroke_width=2, dash_length=0.08)
        tl = tx(f"buys if it does {S['threshold']:.0f} or more a year", 15, DEVICE, bold=True).next_to(thr, UP, buff=0.1)
        c = stat_cards([(f"{S['buyers']}", "hospitals buy", DEVICE), (f"${S['value'] / 1e6:.0f}m", "your robots are worth", GOOD),
                        (f"{S['ops']:,.0f}", "operations a year", WHITE)], y=2.4, size=34, span=11)
        tag = estimate_tag("the Works: seven years at 8%", size=12)
        beat(self,
             "Sell first. <bookmark mark='a'/> A hospital buys only if what it gains over the robot's life covers the price "
             f"and the service, which here means doing at least {S['threshold']:.0f} operations a year. <bookmark mark='b'/> "
             f"{S['buyers']} hospitals buy. <bookmark mark='c'/> Counting the price, the service and the instruments, your "
             f"robots are worth about {S['value'] / 1e6:.0f} million dollars to you, <bookmark mark='d'/> and they do "
             f"{S['ops']:,.0f} operations a year. The small hospitals go without.",
             base=[frame, bars, tag], steps=[[thr, tl], [buy.animate.set_fill(DEVICE, 0.95).build(), c[0]], c[1], c[2]])

    def place(self):
        U = R["run"]
        P = U["place"]
        bars, frame, x0, bw = self.strip()
        lose = VGroup(*[b for b, v in zip(bars, U["volumes"]) if v < P["breakeven"]])
        win = VGroup(*[b for b, v in zip(bars, U["volumes"]) if v >= P["breakeven"]])
        be = DashedLine([x0 + bw * (P["breakeven"] - 50) / 5, -2.3, 0], [x0 + bw * (P["breakeven"] - 50) / 5, 1.2, 0],
                        stroke_color=BAD, stroke_width=2, dash_length=0.08)
        bl = tx(f"below {P['breakeven']:.0f} a year, you lose money", 15, BAD, bold=True).next_to(be, UP, buff=0.1).shift(RIGHT * 1.2)
        c = stat_cards([(f"{P['takers']}", "hospitals take one", PRICE), (f"${P['value'] / 1e6:.0f}m", "your robots are worth", GOOD),
                        (f"{P['ops']:,.0f}", "operations a year", WHITE)], y=2.4, size=34, span=11)
        tag = estimate_tag("the Works: seven years at 8%", size=12)
        beat(self,
             f"Now place them. <bookmark mark='a'/> With no price to pay, every hospital takes a robot: all {P['takers']}. "
             f"<bookmark mark='b'/> Together they do {P['ops']:,.0f} operations a year, many more patients. "
             "<bookmark mark='c'/> But you carry the risk of an idle machine: below about "
             f"{P['breakeven']:.0f} operations a year a placed robot never earns back its cost, and {P['losers']} hospitals are "
             f"that small. <bookmark mark='d'/> In all, your robots are worth about {P['value'] / 1e6:.0f} million dollars.",
             base=[frame, bars, tag], steps=[[win.animate.set_fill(PRICE, 0.95).build(), lose.animate.set_fill(PRICE, 0.95).build(), c[0]],
                                             c[2], [lose.animate.set_fill(BAD, 0.95).build(), be, bl], c[1]])

    def answer(self):
        U = R["run"]
        S, P = U["sell"], U["place"]
        c = stat_cards([(f"${S['value'] / 1e6:.0f}m", f"sell: {S['buyers']} hospitals", DEVICE),
                        (f"${P['value'] / 1e6:.0f}m", f"place: {P['takers']} hospitals", PRICE),
                        (f"${U['match']:,.0f}", "the fee an operation that pays as well as selling", GOOD)], y=0.9, size=40, span=12)
        note = tx("A fee per operation charges each hospital by how much it uses the machine.", 19, WHITE, bold=True).move_to([0, -1.4, 0])
        tag = estimate_tag("the Works' robot market", size=12)
        beat(self,
             f"So which? <bookmark mark='a'/> Selling earns you more here: {S['value'] / 1e6:.0f} million against "
             f"{P['value'] / 1e6:.0f}. <bookmark mark='b'/> Placing reaches {P['takers'] - S['buyers']} more hospitals and "
             f"{P['ops'] - S['ops']:,.0f} more operations a year. <bookmark mark='c'/> And at a fee of about "
             f"{U['match']:,.0f} dollars an operation, placing would pay you as well as selling. <bookmark mark='d'/> A fee "
             "per use is a price that grows with use: the hospitals that operate most pay most, and the small ones can "
             "start without the capital. The maker, in return, carries the risk that its machine sits idle.",
             base=[tag], steps=[c[0], c[1], c[2], note])

    def real(self):
        U = R["run"]
        lr = U["lease_rev"]
        items = [(str(y), lr[y], PRICE, f"${lr[y]:,.0f}m") for y in sorted(lr)]
        bars_ = vbars(items, base_y=-2.3, height=3.0, width=1.1, gap=0.6, x0=2.0)
        c = VGroup(tx(f"{U['leased']:,} of {R['hook']['base']:,} da Vinci robots on operating leases", 18, WHITE, bold=True),
                   tx(f"{U['usage']:,} paid for by use, up from {U['usage23']:,} two years before", 18, PRICE, bold=True)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.0, 1.6, 0])
        lab = tx("operating lease revenue", 15, GREY_A).next_to(bars_, UP, buff=0.5)
        src = source("Intuitive Surgical, Inc., Form 10-K 2025: installed base under operating leases; operating lease revenue",
                     size=12)
        beat(self,
             f"Intuitive does both. <bookmark mark='a'/> At the end of 2025, {U['leased']:,} of its "
             f"{R['hook']['base']:,} robots were leased rather than sold, <bookmark mark='b'/> and {U['usage']:,} of those "
             f"were paid for by use, up from {U['usage23']:,} two years before. <bookmark mark='c'/> Its lease revenue rose "
             f"from {lr[2023]:,.0f} million dollars in 2023 to {lr[2025]:,.0f} million in 2025. The machine is increasingly "
             "priced like the operations it does.",
             base=[src, lab], steps=[c[0], c[1], bars_])
