from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


class Sub(VoiceoverScene):
    def construct(self):
        card(self, 2, "A subscriber", "What is a customer worth to a phone company?",
             "Chapter two. A subscriber. A phone company's business is a pool of accounts that pay every month, and a "
             "steady leak of them to rivals.", lit=("unit", "dollar"))
        self.bill()
        self.phones()
        self.life()
        self.lines()
        self.churn()

    def bill(self):
        S = R["sub"]
        phones = VGroup(*[draw.phone(1.0, screen=c) for c in (WIRELESS, OVER, CABLE)]).arrange(RIGHT, buff=0.3).move_to([0, 1.6, 0])
        c = stat_cards([(f"${S['arpa']:.2f}", "a month per account, Verizon, 2025", WIRELESS),
                        (f"{S['cpa']:.2f}", "lines per account", ALL),
                        (f"${S['tm_arpa']:.2f}", "a month per account, T-Mobile", CABLE)], y=-0.9, size=38, span=12)
        src = source("Forms 10-K for 2025 of Verizon (Consumer segment) and T-Mobile", size=12)
        beat(self,
             "The unit is the account: a household, usually with several phones on one bill. <bookmark mark='a'/> "
             f"Verizon's consumer accounts paid an average of {S['arpa']:.2f} dollars a month in 2025, "
             f"<bookmark mark='b'/> for {S['cpa']:.2f} lines each. <bookmark mark='c'/> T-Mobile's paid {S['tm_arpa']:.2f}. "
             "The family plan is no accident: in this series' reading, the more phones on one bill, the harder it is to move them all.",
             base=[phones, src], steps=[c[0], c[1], c[2]])

    def phones(self):
        er, ec = get("vz30.equiprev"), get("vz30.equipcost")
        items = [("phones and devices sold", er, GOOD, f"${er:.1f}bn"), ("what they cost Verizon", ec, BAD, f"${ec:.1f}bn")]
        rows = hbars(items, max_value=32, x0=0.4, top=1.2, row=1.2, length=5.6, size=18, bar_h=0.6)
        ph = draw.phone(1.6, screen=WIRELESS).move_to([-5.0, -1.8, 0])
        lab = tx("Verizon, 2025", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Verizon Communications, Form 10-K for 2025", size=12)
        beat(self,
             "Winning an account starts with a phone. <bookmark mark='a'/> In 2025 Verizon sold phones and other devices "
             f"for {er:.1f} billion dollars, <bookmark mark='b'/> which had cost it {ec:.1f} billion: it handed over "
             f"{ec - er:.1f} billion more in hardware than it was paid for. The phone is the bait, paid for in monthly "
             "instalments by a customer who must stay to finish paying it off.",
             base=[rows.axis, lab, ph, src], steps=[rows[0], rows[1]])

    def life(self):
        S = R["sub"]
        c = stat_cards([(f"{100 * S['churn']:.2f}%", "of Verizon's phones leave each month", BAD),
                        (f"{S['months'] / 12:.0f} years", "the average stay that implies", ALL),
                        (f"${S['life']:,.0f}", "an account's worth, after winning it", GOOD)], y=0.6, size=38, span=12)
        tag = estimate_tag(f"the Works: {100 * S['margin']:.0f}% of the bill left after serving it, ${S['cac']:.0f} to win an account, no discounting (assumptions); churn and ARPA are Verizon's", size=12)
        beat(self,
             f"<bookmark mark='a'/> Each month about {100 * S['churn']:.2f} per cent of Verizon's postpaid phone customers "
             f"leave. <bookmark mark='b'/> At that rate the average customer stays about {S['months'] / 12:.0f} years. "
             f"<bookmark mark='c'/> If {100 * S['margin']:.0f} cents of each dollar is left after the cost of serving the "
             f"account, and winning it cost {S['cac']:.0f} dollars in promotions, discounted phones and commissions, the "
             f"account is worth about {S['life']:,.0f} dollars over its life, by this series' arithmetic.",
             base=[tag], steps=[c[0], c[1], c[2]])

    def lines(self):
        items = [("2023", 2.84, ALL, "2.84 lines, 33.0m accounts"), ("2024", 2.90, ALL, "2.90 lines, 32.8m accounts"),
                 ("2025", 2.95, WIRELESS, "2.95 lines, 32.4m accounts")]
        rows = hbars(items, max_value=3.2, x0=-0.6, top=1.4, row=1.0, length=5.0, size=17, bar_h=0.5)
        lab = tx("Verizon Consumer: postpaid connections per account, and accounts", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Verizon Communications, Form 10-K for 2025", size=12)
        beat(self,
             "Watch the family plan at work. <bookmark mark='a'/> In 2023 Verizon's consumer accounts had 2.84 lines each, "
             "<bookmark mark='b'/> in 2024, 2.90, <bookmark mark='c'/> and in 2025, 2.95, while the number of accounts "
             "fell from 33.0 million to 32.4 million. Fewer households, more devices each: watches, tablets and the box "
             "that brings the internet home.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2]])

    def churn(self):
        S = R["sub"]
        B = S["by_churn"]
        items = [(f"{100 * c:.2f}% a month" + ("  (Verizon, 2025)" if abs(c - S["churn"]) < 1e-12 else ""), v,
                  GOOD if c <= S["churn"] + 1e-12 else BAD, f"${v:,.0f}") for c, v in B.items()]
        rows = hbars(items, max_value=11000, x0=0.6, top=2.0, row=0.6, length=5.0, size=15, bar_h=0.34)
        lab = tx("the Works: an account's lifetime worth, by the share of customers who leave each month", 16, GREY_A).to_edge(UP, buff=0.6)
        tag = estimate_tag("the Works", size=12)
        beat(self,
             "That is why the companies fight so hard over churn. <bookmark mark='a'/> At six-tenths of a per cent a month "
             f"an account is worth about {B[0.006]:,.0f} dollars; <bookmark mark='b'/> at Verizon's rate, {S['life']:,.0f}; "
             f"<bookmark mark='c'/> at two per cent, {B[0.02]:,.0f}; at three, {B[0.03]:,.0f}. Bundles, family plans, phones "
             "paid off over three years and loyalty perks are all ways of keeping that number small. AT&T's churn was "
             f"{S['att_churn']:.2f} per cent in 2025, and T-Mobile's {S['tm_churn']:.2f}: the three are almost "
             "indistinguishable.",
             base=[rows.axis, lab, tag], steps=[VGroup(*rows[:2]), VGroup(*rows[2:4]), VGroup(*rows[4:])])
