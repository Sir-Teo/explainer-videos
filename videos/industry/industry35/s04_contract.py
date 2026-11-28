from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Contract(VoiceoverScene):
    def construct(self):
        card(self, 3, "Owner, brand, operator", "A hotel is three businesses in one building. Who does what, and who is paid how?",
             "Chapter three. Owner, brand, operator. Every hotel is three businesses at once: a building, a name, and the "
             "people who run it. They can belong to three different companies.", lit=("dollar",))
        self.three()
        self.franchise()
        self.management()
        self.incentive()
        self.fees()
        self.works()
        self.reimb()

    def three(self):
        b = draw.hotel(1.8, floors=10, seed=8)
        own = VGroup(b, tx("the owner", 22, OWNER, bold=True), tx("buys the land, builds, borrows, refurbishes", 14, GREY_A)).arrange(DOWN, buff=0.15)
        sign = RoundedRectangle(corner_radius=0.1, width=2.2, height=0.8, stroke_width=0, fill_color=BRAND, fill_opacity=1)
        brand = VGroup(VGroup(sign, tx("BRAND", 22, "#1B2230", bold=True).move_to(sign)), tx("the brand", 22, BRAND, bold=True),
                       tx("name, standards, bookings, loyalty", 14, GREY_A)).arrange(DOWN, buff=0.2)
        staff = VGroup(VGroup(*[draw.person(0.5, color=STAFF) for _ in range(3)]).arrange(RIGHT, buff=0.15), tx("the operator", 22, STAFF, bold=True),
                       tx("hires the staff, runs the hotel daily", 14, GREY_A)).arrange(DOWN, buff=0.2)
        g = VGroup(own, brand, staff).arrange(RIGHT, buff=1.2, aligned_edge=DOWN).move_to([0, -0.2, 0])
        beat(self,
             "Three jobs. <bookmark mark='a'/> The owner buys the land, builds the hotel, borrows against it and pays for "
             "every refurbishment. <bookmark mark='b'/> The brand supplies the name on the sign, the standards the rooms must "
             "meet, the reservation system and the loyalty programme. <bookmark mark='c'/> The operator hires the staff and "
             "runs the place day and night. Sometimes one company does all three. Usually it does not.",
             base=[], steps=[own, brand, staff])

    def franchise(self):
        C = R["contract"]
        lines = [(f"the owner pays a royalty: typically {C['roy'][0]} to {C['roy'][1]}% of room revenue (Marriott)", BRAND),
                 ("plus, for some brands, up to 4% of food and beverage revenue", BRAND),
                 ("plus charges for the loyalty programme, reservations and marketing", FEE),
                 ("the owner runs the hotel itself, or hires a management company", OWNER)]
        g = VGroup(*[tx(t, 19, c) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.1, 0])
        hd = tx("a franchise", 24, BRAND, bold=True).to_edge(UP, buff=0.8)
        src = source("Marriott International, Form 10-K for 2025", size=12)
        beat(self,
             "The first contract is a franchise, as in Part 34's restaurants. <bookmark mark='a'/> The owner pays the brand a "
             f"royalty, which at Marriott typically runs from {C['roy'][0]} to {C['roy'][1]} per cent of room revenue, "
             "<bookmark mark='b'/> plus for some brands up to four per cent of food and beverage. <bookmark mark='c'/> On top "
             "come charges for the brand's shared programmes: the loyalty scheme, the reservation system and the marketing. "
             "<bookmark mark='d'/> The owner runs the hotel, or hires a separate management company to do it, and keeps the "
             "profit or the loss.",
             base=[hd, src], steps=list(g))

    def management(self):
        C = R["contract"]
        lines = [(f"a base fee: generally {C['fee_base'] - 0.5:.0f} to {C['fee_base'] + 0.5:.0f}% of the hotel's gross revenue", STAFF),
                 ("an incentive fee: generally 10 to 20% of operating profit", GOOD),
                 ("but only after the owner has had a priority return on its investment", OWNER),
                 ("the hotel's staff are often the manager's employees; the owner repays their wages", FIXC)]
        g = VGroup(*[tx(t, 19, c) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.1, 0])
        hd = tx("a management contract", 24, STAFF, bold=True).to_edge(UP, buff=0.8)
        src = source("Host Hotels & Resorts and Marriott International, Forms 10-K for 2025", size=12)
        beat(self,
             "The second is a management contract, the usual arrangement for big full-service hotels. Host's annual report "
             "describes its terms. <bookmark mark='a'/> The manager earns a base fee, generally two to three per cent of the "
             "hotel's gross revenue, <bookmark mark='b'/> and an incentive fee, generally ten to twenty per cent of operating "
             "profit, <bookmark mark='c'/> but often only once the owner has received a priority return on its investment. "
             "<bookmark mark='d'/> The staff are frequently the manager's employees, and the owner reimburses their wages.",
             base=[hd, src], steps=list(g))

    def incentive(self):
        C = R["contract"]
        items = [("managed hotels worldwide", C["imf"], GOOD, f"{C['imf']}%"),
                 ("in the U.S. and Canada", C["imf_us"], BAD, f"{C['imf_us']}%"),
                 ("outside them", C["imf_intl"], BRAND, f"{C['imf_intl']}%")]
        rows = hbars(items, max_value=100, x0=0.6, top=1.3, row=1.0, length=5.6, size=18, bar_h=0.55)
        hd = tx("share of Marriott's managed hotels that paid it an incentive fee in 2025", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Marriott International, Form 10-K for 2025", size=12)
        beat(self,
             "How often does the profit clear that hurdle? <bookmark mark='a'/> In 2025, "
             f"{C['imf']} per cent of Marriott's managed hotels worldwide paid it an incentive fee. <bookmark mark='b'/> In the "
             f"United States and Canada, only {C['imf_us']} per cent: most owners there did not earn enough to pass their "
             f"priority return. <bookmark mark='c'/> Elsewhere, {C['imf_intl']} per cent: Marriott says the owner's hurdle "
             "is most common in North America, Europe and Latin America. The base fee, a share of revenue, is paid either way.",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], rows[2]])

    def fees(self):
        C = R["contract"]
        mf, hf = C["mar_fees"], C["hlt_fees"]
        items = [("Marriott: franchise fees", mf["franchise fees"], BRAND, bn(mf["franchise fees"], 2)),
                 ("Marriott: base management", mf["base management"], STAFF, bn(mf["base management"], 2)),
                 ("Marriott: incentive management", mf["incentive management"], GOOD, bn(mf["incentive management"], 2)),
                 ("Hilton: franchise and licensing", hf["franchise and licensing"], BRAND, bn(hf["franchise and licensing"], 2)),
                 ("Hilton: management", hf["management"], STAFF, bn(hf["management"], 2))]
        rows = hbars(items, max_value=3.6, x0=1.0, top=1.8, row=0.82, length=5.0, size=17, bar_h=0.5)
        hd = tx("fees earned in 2025", 21, WHITE, bold=True).to_edge(UP, buff=0.6)
        src = source("Marriott International and Hilton Worldwide, Forms 10-K for 2025", size=12)
        beat(self,
             "Now the brands' bills. <bookmark mark='a'/> Marriott collected 3.3 billion dollars of franchise fees in 2025, "
             "which include what banks pay to put its name on credit cards, <bookmark mark='b'/> 1.3 billion of base "
             "management fees <bookmark mark='c'/> and 0.8 billion of incentive fees. <bookmark mark='d'/> Hilton, an even "
             f"purer franchisor, collected {hf['franchise and licensing']:.1f} billion from franchising and licensing "
             f"<bookmark mark='e'/> and only {hf['management']:.1f} billion from management. The fees on revenue dwarf the "
             "fees on profit.",
             base=[rows.axis, hd, src], steps=list(rows))

    def works(self):
        S = R["contract"]["split"]
        items = [("the brand's franchise fees, a year", S["brand"] / 1e6, BRAND, m(S["brand"])),
                 ("a manager's base fee (2.5% of revenue)", S["base_fee"] / 1e6, STAFF, m(S["base_fee"])),
                 ("a manager's incentive fee", S["inc_fee"] / 1e6, GOOD, m(S["inc_fee"])),
                 ("the owner's 10% priority return", S["prior"] / 1e6, OWNER, m(S["prior"]))]
        rows = hbars(items, max_value=3.8, x0=1.0, top=1.6, row=0.9, length=5.0, size=17, bar_h=0.5)
        hd = tx("the Works' hotel under contract", 21, WHITE, bold=True).to_edge(UP, buff=0.7)
        tag = estimate_tag("the Works: incentive fee 15% of profit after fees and a 10% priority return on the hotel's cost", size=12)
        beat(self,
             f"Put the Works' hotel under such contracts. <bookmark mark='a'/> The brand's fees are {S['brand'] / 1e6:.2f} "
             "million dollars a year. <bookmark mark='b'/> A manager's base fee would add a quarter of a million. "
             "<bookmark mark='c'/> And the incentive fee would be nothing, <bookmark mark='d'/> because after those fees the "
             f"hotel's profit, {S['ebitda'] / 1e6:.1f} million, does not clear a ten per cent return on its {S['prior'] / 0.10 / 1e6:.0f} "
             "million dollar cost. "
             "Like most American owners in Marriott's figures, this one pays the fees on revenue and never reaches the fee on "
             "profit.",
             base=[rows.axis, hd, tag], steps=list(rows))

    def reimb(self):
        C = R["contract"]
        H = R["hook"]
        items = [("Marriott: costs reimbursed by owners", C["reimb"], FIXC, bn(C["reimb"])),
                 ("Marriott: everything else", H["rev"] - C["reimb"], BRAND, bn(H["rev"] - C["reimb"])),
                 ("Hilton: costs reimbursed by owners", C["hl_reimb"], FIXC, bn(C["hl_reimb"])),
                 ("Hilton: everything else", get("hl35.rev") - C["hl_reimb"], BRAND, bn(get("hl35.rev") - C["hl_reimb"]))]
        rows = hbars(items, max_value=20, x0=1.0, top=1.6, row=0.9, length=5.0, size=17, bar_h=0.5)
        hd = tx("revenue in 2025: money passed through, and the rest", 21, WHITE, bold=True).to_edge(UP, buff=0.7)
        src = source("Marriott International and Hilton Worldwide, Forms 10-K for 2025", size=12)
        beat(self,
             "Which explains the strange shape of their accounts. <bookmark mark='a'/> When Marriott employs the staff of a "
             f"hotel it manages, it pays their wages and the owner pays it back: {C['reimb']:.1f} billion dollars in 2025, "
             f"counted as revenue. <bookmark mark='b'/> Everything else came to {H['rev'] - C['reimb']:.1f} billion. "
             f"<bookmark mark='c'/> Hilton passed through {C['hl_reimb']:.1f} billion <bookmark mark='d'/> and earned "
             f"{get('hl35.rev') - C['hl_reimb']:.1f} billion besides. To compare a hotel brand with anyone else, leave the "
             "reimbursements out: they are other people's payroll.",
             base=[rows.axis, hd, src], steps=list(rows))
