from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403


class Loyalty(VoiceoverScene):
    def construct(self):
        card(self, 5, "The bank in the airline", "Where do airlines really make their money?",
             "Chapter five. The bank in the airline. The most reliable business inside an American airline is not flying. "
             "It is selling miles to banks.", lit=("dollar", "moat"))
        self.delta()
        self.american()
        self.owed()
        self.how()

    def delta(self):
        L = R["loyalty"]
        items = [("American Express paid Delta, 2025", L["amex"], CARD, f"${L['amex']:.1f}bn"),
                 ("Delta's net income, 2025", L["dal_profit"], GOOD, f"${L['dal_profit']:.1f}bn")]
        rows = hbars(items, max_value=10, x0=0.4, top=1.2, row=1.2, length=6.0, size=18, bar_h=0.6)
        q = tx("'which we expect to grow to $10 billion over the next few years'", 17, WHITE).move_to([0, -1.6, 0])
        src = source("Delta Air Lines, Form 10-K for 2025; SEC company facts", size=12)
        beat(self,
             "Delta's SkyMiles programme has a partner: American Express, which issues Delta credit cards and buys miles "
             f"to give their holders. <bookmark mark='a'/> In 2025 it paid Delta {L['amex']:.1f} billion dollars. "
             f"<bookmark mark='b'/> Delta's entire net income that year was {L['dal_profit']:.1f} billion. "
             "<bookmark mark='c'/> And Delta expects the card money to grow to ten billion a year. A bank pays the airline "
             "more than the airline earns.",
             base=[rows.axis, src], steps=[rows[0], rows[1], q])

    def american(self):
        L = R["loyalty"]
        items = [("card and partner payments to American, 2025", L["aal"], CARD, f"${L['aal']:.1f}bn"),
                 ("American's net income, 2025", L["aal_profit"], GOOD, f"${L['aal_profit']:.2f}bn")]
        rows = hbars(items, max_value=10, x0=0.4, top=1.2, row=1.2, length=6.0, size=18, bar_h=0.6)
        src = source("American Airlines Group, Form 10-K for 2025; SEC company facts", size=12)
        beat(self,
             "At American the gap is wider. <bookmark mark='a'/> Its co-branded credit card and other partners paid it "
             f"{L['aal']:.1f} billion dollars in cash in 2025. <bookmark mark='b'/> Its net income was "
             f"{1e3 * L['aal_profit']:.0f} million: the card money was more than fifty times the profit.",
             base=[rows.axis, src], steps=[rows[0], rows[1]])

    def owed(self):
        L = R["loyalty"]
        cab = draw.cabin(rows=20, seats=(3, 3), size=0.16, gap=0.03).move_to([-3.2, 0.4, 0])
        fill(cab, 0, 0, empty_col=CARD)
        c = VGroup(tx(f"${L['skymiles']:.1f}bn", 48, CARD, bold=True),
                   tx("of SkyMiles revenue Delta had been paid for", 17, GREY_A),
                   tx("but not yet earned, at the end of 2025", 17, GREY_A)).arrange(DOWN, buff=0.1).move_to([3.0, 0.8, 0])
        note = tx("earned only when members spend the miles on flights", 18, WHITE).move_to([3.0, -1.0, 0])
        src = source("Delta Air Lines, Form 10-K for 2025: loyalty program deferred revenue", size=12)
        beat(self,
             "A mile sold is a promise. <bookmark mark='a'/> At the end of 2025 Delta carried "
             f"{L['skymiles']:.1f} billion dollars of SkyMiles revenue on its books that it had been paid for but not yet "
             "earned: seats it owes its members. <bookmark mark='b'/> It counts that money as revenue only when the miles are "
             "spent on a flight. So the bank's cash arrives first, and the cost, a seat, comes later, often on a flight "
             "with seats to spare.",
             base=[src], steps=[VGroup(cab, c), note])

    def how(self):
        g = VGroup(tx("How the bank in the airline works", 22, WHITE, bold=True),
                   tx("the bank buys miles in bulk and gives them to cardholders for spending", 18, CARD),
                   tx("the airline delivers the miles as seats, often seats that would have flown empty", 18, SKY),
                   tx("the miles cost the airline little; the cash arrives every month, in good years and bad", 18, GOOD),
                   tx(f"Delta's loyalty revenue grew {R['loyalty']['q3']:.0f}% in the third quarter of 2026, a year of dear fuel", 18, BIZ)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        tag = estimate_tag("this series' summary of a co-branded card programme", size=12)
        src = source("Delta Air Lines, results release of 9 October 2026", size=12)
        beat(self,
             "How does it work? In this series' reading, <bookmark mark='a'/> a bank buys miles in bulk and hands them to "
             "people who spend on its card. <bookmark mark='b'/> The airline pays the miles back as seats, often seats that "
             "would otherwise have flown empty, which, as Run it showed, cost it almost nothing. <bookmark mark='c'/> And the "
             "bank's cash comes in every month. <bookmark mark='d'/> In the third quarter of 2026, a quarter of costly fuel, "
             f"Delta's loyalty revenue still grew {R['loyalty']['q3']:.0f} per cent.",
             base=[tag, src], steps=[g[:2], g[2], g[3], g[4]])
