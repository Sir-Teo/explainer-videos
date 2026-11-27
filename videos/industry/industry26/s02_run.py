from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: your loan comes due",
             "Your office tower's loan falls due in 2026. Pay in, hand back the keys, or ask for time?",
             "Chapter one. Run it. You own an office building in the Works. You bought it in 2019 with a seven-year loan, "
             "and in 2026 the loan falls due.", lit=("dollar", "change"))
        self.bought()
        self.now()
        self.worth()
        self.lender()
        self.choices()
        self.shed()

    def bought(self):
        U = R["run"]["office"]
        T0 = U["then"]
        tower = draw.office_tower(1.3).move_to([-5.0, -0.2, 0])
        draw.light(tower.windows, T0["occupancy"])
        lines = VGroup(tx("2019: you buy", 22, VALUE, bold=True),
                       tx(f"400,000 square feet, {100 * T0['occupancy']:.0f}% let at ${T0['rent']:.0f} a square foot", 18, WHITE),
                       tx(f"rent {m(T0['rent_roll'])} a year, less running costs {m(T0['costs'])}", 18, WHITE),
                       tx(f"= net operating income {m(T0['noi'])}", 20, INCOME, bold=True),
                       tx(f"buyers want {100 * T0['cap']:.0f}%: price {m(T0['value'], 0)}", 20, VALUE, bold=True),
                       tx(f"loan {m(U['loan'], 0)} at 4% for seven years; your money {m(U['equity'], 0)}", 18, LOAN),
                       tx(f"you keep {m(T0['noi'] - 0.04 * U['loan'])} a year: {100 * T0['cash_yield']:.1f}% on your money", 18, GOOD)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([1.4, 0.2, 0])
        est = estimate_tag("the Works: an illustrative office building", size=12)
        beat(self,
             "Here is the deal you made. <bookmark mark='a'/> In 2019 you bought a four hundred thousand square foot office "
             f"building, {100 * T0['occupancy']:.0f} per cent let at {T0['rent']:.0f} dollars a square foot a year. "
             f"<bookmark mark='b'/> The rent came to {T0['rent_roll']:.0f} million dollars a year; taxes, insurance, cleaning, "
             f"power and management took {T0['costs']:.0f} million, <bookmark mark='c'/> leaving {T0['noi']:.0f} million of "
             f"net operating income. <bookmark mark='d'/> Buyers then wanted five per cent a year, so you paid "
             f"{T0['value']:.0f} million. <bookmark mark='e'/> A bank lent you {U['loan']:.0f} million at four per cent, "
             f"interest only, for seven years, and you put in {U['equity']:.0f} million of your own. <bookmark mark='f'/> After "
             f"interest you kept about {T0['noi'] - 0.04 * U['loan']:.1f} million a year: nearly seven per cent on your money.",
             base=[tower, est], steps=[lines[0:2], lines[2], lines[3], lines[4], lines[5], lines[6]])

    def now(self):
        U = R["run"]["office"]
        T0, T1 = U["then"], U["now"]
        t0 = draw.office_tower(1.1).move_to([-5.4, -0.3, 0])
        t1 = draw.office_tower(1.1).move_to([-3.4, -0.3, 0])
        draw.light(t0.windows, T0["occupancy"])
        draw.light(t1.windows, T1["occupancy"])
        l0 = tx("2019", 16, GREY_A).next_to(t0, DOWN, buff=0.15)
        l1 = tx("2026", 16, GREY_A).next_to(t1, DOWN, buff=0.15)
        items = [("rent collected, 2019", T0["rent_roll"], ALL, m(T0["rent_roll"])),
                 ("rent collected, 2026", T1["rent_roll"], OFFICE, m(T1["rent_roll"])),
                 ("net operating income, 2019", T0["noi"], ALL, m(T0["noi"])),
                 ("net operating income, 2026", T1["noi"], BAD, m(T1["noi"]))]
        rows = hbars(items, max_value=20, x0=0.4, top=1.6, row=0.85, length=4.6, size=16, bar_h=0.45)
        drop_r = 100 * (1 - T1["rent_roll"] / T0["rent_roll"])
        drop_n = 100 * (1 - T1["noi"] / T0["noi"])
        note = tx(f"rent down {drop_r:.0f}%, income down {drop_n:.0f}%: the costs stayed", 18, BAD, bold=True).move_to([1.8, -2.1, 0])
        est = estimate_tag("the Works' office in 2026", size=12)
        beat(self,
             "Now it is 2026. <bookmark mark='a'/> People work from home two or three days a week, and a third of your "
             f"tenants have left or shrunk: the building is {100 * T1['occupancy']:.0f} per cent let, and new leases are "
             f"signed at {T1['rent']:.0f} dollars. <bookmark mark='b'/> The rent you collect falls to {T1['rent_roll']:.1f} "
             f"million. <bookmark mark='c'/> But the costs do not fall: an empty floor is still taxed, insured, heated and "
             f"guarded, and they have crept up to {T1['costs']:.1f} million. <bookmark mark='d'/> So your income falls from "
             f"{T0['noi']:.0f} million to {T1['noi']:.1f}. The rent fell {drop_r:.0f} per cent; the income fell "
             f"{drop_n:.0f}. That is the first lesson of property: costs are fixed, so income moves much more than rent.",
             base=[t0, t1, l0, l1, rows.axis, est], steps=[[rows[0]], [rows[1]], [rows[2]], [rows[3], note]])

    def worth(self):
        U = R["run"]["office"]
        T0, T1 = U["then"], U["now"]
        at = U["at"]
        items = [("price paid, 2019", T0["value"], ALL, m(T0["value"], 0)),
                 ("your loan", U["loan"], LOAN, m(U["loan"], 0)),
                 (f"value in 2026, at {100 * T1['cap']:.1f}%", T1["value"], BAD, m(T1["value"]))]
        rows = hbars(items, max_value=210, x0=-0.6, top=1.4, row=1.1, length=6.4, size=18, bar_h=0.55)
        eq = MathTex(r"\frac{%.2f}{%.3f} = %.1f" % (T1["noi"], T1["cap"], T1["value"]), font_size=44, color=RATE).move_to([0, -2.1, 0])
        est = estimate_tag("the Works' office in 2026", size=12)
        beat(self,
             "And the rate has moved too. <bookmark mark='a'/> In 2019 buyers paid "
             f"{T0['value']:.0f} million for the building. <bookmark mark='b'/> You still owe {U['loan']:.0f} million. "
             "<bookmark mark='c'/> But interest rates have risen, and buyers of half-empty offices now want "
             f"{100 * T1['cap']:.1f} per cent a year. {T1['noi']:.1f} million of income at that rate is worth about "
             f"{T1['value']:.0f} million. <bookmark mark='d'/> Your building is worth less than a third of what you owe on "
             f"it: the loan is {at['ltv_now']:.1f} times its value.",
             base=[rows.axis, est], steps=[rows[0], rows[1], rows[2], eq])

    def lender(self):
        U = R["run"]["office"]
        at = U["at"]
        t = at["tests"]
        items = [("60% of the value", t["ltv"], LOAN, m(t["ltv"])),
                 ("income covers 7% interest 1.25 times", t["dscr"], RATE, m(t["dscr"])),
                 ("income is 10% of the loan", t["debt_yield"], INCOME, m(t["debt_yield"]))]
        rows = hbars(items, max_value=140, x0=0.6, top=1.4, row=1.05, length=5.2, size=17, bar_h=0.5)
        old = DashedLine([0.6 + 5.2 * U["loan"] / 140, 2.0, 0], [0.6 + 5.2 * U["loan"] / 140, -1.0, 0], stroke_color=BAD, stroke_width=2)
        oldl = tx(f"old loan {m(U['loan'], 0)}", 15, BAD).next_to(old, UP, buff=0.1)
        gap = tx(f"the most anyone will lend: {m(at['new_loan'])}; the gap: {m(at['gap'])}", 20, BAD, bold=True).move_to([0, -1.9, 0])
        est = estimate_tag("the Works: a lender's three tests at a 7% rate", size=12)
        beat(self,
             "To repay the old loan you need a new one. <bookmark mark='a'/> A lender looks at three things. It will lend "
             f"perhaps sixty per cent of the building's value: {at['tests']['ltv']:.1f} million. <bookmark mark='b'/> It wants "
             "the income to cover the interest, now seven per cent, a quarter more than once over: that allows "
             f"{t['dscr']:.1f} million. <bookmark mark='c'/> And it wants the income to be at least a tenth of the loan: "
             f"{t['debt_yield']:.1f} million. <bookmark mark='d'/> It lends the least of the three, {at['new_loan']:.1f} "
             f"million, against the {U['loan']:.0f} million you owe. To keep the building you must find "
             f"{at['gap']:.0f} million dollars.",
             base=[rows.axis, old, oldl, est], steps=[rows[0], rows[1], rows[2], gap])

    def choices(self):
        U = R["run"]["office"]
        at = U["at"]
        opts = VGroup(
            VGroup(tx("Pay in", 24, VALUE, bold=True), tx(f"put {m(at['gap'], 0)} into a", 17, WHITE),
                   tx(f"building worth {m(at['value'], 0)}", 17, WHITE)).arrange(DOWN, buff=0.12),
            VGroup(tx("Hand back the keys", 24, BAD, bold=True), tx(f"you lose your {m(U['equity'], 0)};", 17, WHITE),
                   tx(f"the lender loses {m(at['keys']['lender_loss'], 0)}", 17, WHITE)).arrange(DOWN, buff=0.12),
            VGroup(tx("Ask for time", 24, OFFICE, bold=True), tx(f"income covers {100 * at['extend']['interest_cover']:.0f}%", 17, WHITE),
                   tx("of the old interest", 17, WHITE)).arrange(DOWN, buff=0.12)).arrange(RIGHT, buff=1.2).move_to([0, 0.9, 0])
        key = draw.house_key(1.0).next_to(opts[1], UP, buff=0.3)
        q = quote(["'To date, lenders' willingness to extend or restructure maturing loans has helped mitigate this risk'"],
                  "Federal Reserve, Financial Stability Report, November 2026", size=17).move_to([0, -1.9, 0])
        est = estimate_tag("the Works' office in 2026", size=12)
        beat(self,
             "So you have three choices. <bookmark mark='a'/> You can pay in "
             f"{at['gap']:.0f} million dollars to keep a building worth {at['value']:.0f} million: no one does. "
             "<bookmark mark='b'/> You can hand the lender the keys. You lose the "
             f"{U['equity']:.0f} million you put in, which is gone already; the lender gets a {at['value']:.0f} million "
             f"building for a {U['loan']:.0f} million loan, and loses about {at['keys']['lender_loss']:.0f} million. "
             "<bookmark mark='c'/> Or you can ask the lender to wait, though the income now covers only "
             f"{100 * at['extend']['interest_cover']:.0f} per cent of even the old interest. Many lenders wait, because "
             "waiting postpones the loss. <bookmark mark='d'/> In November 2026 the Federal Reserve wrote that lenders' "
             "willingness to extend or restructure maturing loans had held off forced sales, so far.",
             base=[est], steps=[opts[0], [opts[1], key], opts[2], q])

    def shed(self):
        U = R["run"]["warehouse"]
        T0, T1 = U["then"], U["now"]
        at = U["at"]
        w = draw.warehouse(3.0).move_to([-4.0, 1.6, 0])
        left = VGroup(tx("A warehouse bought the same year", 20, SHED, bold=True),
                      tx(f"rent ${T0['rent']:.0f} to ${T1['rent']:.1f} a square foot, as leases renew", 17, WHITE),
                      tx(f"income {m(T0['noi'])} to {m(T1['noi'])}", 17, INCOME),
                      tx(f"buyers want {100 * T0['cap']:.1f}% to {100 * T1['cap']:.1f}%", 17, RATE),
                      tx(f"value {m(T0['value'], 0)} to {m(T1['value'], 0)}", 19, VALUE, bold=True),
                      tx(f"new loan {m(at['new_loan'])} repays {m(U['loan'])}: {m(at['cash_out'])} to spare", 17, GOOD)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([2.0, -0.2, 0])
        est = estimate_tag("the Works' warehouse; Prologis renewed its leases about 50% higher in 2025", size=12)
        beat(self,
             "Now the other building you could have bought in 2019: a million square foot warehouse, for the same ten million "
             "dollars of income. <bookmark mark='a'/> Online shopping filled warehouses, and as its leases came up, rents "
             f"rose by half, from {T0['rent']:.0f} to {T1['rent']:.1f} dollars a square foot, as Prologis's did in 2025. "
             f"<bookmark mark='b'/> Its income rose to {T1['noi']:.1f} million. <bookmark mark='c'/> Buyers want more for "
             f"warehouses too, {100 * T1['cap']:.1f} per cent instead of {100 * T0['cap']:.1f}, <bookmark mark='d'/> but the "
             f"higher income more than makes up for it: it is worth {T1['value']:.0f} million, more than you paid. "
             f"<bookmark mark='e'/> A new loan repays the old with {at['cash_out']:.1f} million to spare. The same rates, the "
             "same year, opposite fates. The difference is the income, and income comes from tenants.",
             base=[w, est], steps=[left[0:2], left[2], left[3], left[4], left[5]])
