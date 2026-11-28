from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.who()
        self.rooms()
        self.revenue()
        self.split()
        self.today()
        self.title()

    def who(self):
        H = R["hook"]
        towers = VGroup(*[draw.hotel(1.5, floors=12 + 2 * i, seed=3 + i) for i in range(4)]).arrange(RIGHT, buff=0.45, aligned_edge=DOWN)
        towers.move_to([0, 1.0, 0])
        for t in towers:
            draw.light(t.windows, 0.69)
        c = stat_cards([(f"{H['rooms']:,}", "rooms in Marriott's system, end of 2025", BRAND),
                        (f"{H['own_props']}", f"hotels it owns or leases: {100 * H['own_share']:.1f}% of its rooms", OWNER)],
                       y=-2.1, size=38, span=11)
        src = source("Marriott International, Form 10-K for 2025", size=12)
        beat(self,
             f"Marriott had {H['rooms']:,} rooms in its hotels at the end of 2025, in {H['props']:,} properties across 145 "
             f"countries and territories. <bookmark mark='a'/> That is more than Hilton's {get('hl35.rooms') / 1e6:.2f} million, "
             f"and yet <bookmark mark='b'/> it owned or leased only {H['own_props']} of those properties: less than one room in a "
             "hundred. Somebody else owns almost every hotel with Marriott's name on it. So why do the biggest hotel "
             "companies own almost no hotels?",
             base=[towers, src], steps=[c[0], c[1]])

    def rooms(self):
        H = R["hook"]
        b = H["by"]
        tot = sum(b.values())
        parts = [("franchised", b["franchised"] / tot, BRAND), ("managed for owners", b["managed"] / tot, STAFF),
                 ("owned or leased", b["owned or leased"] / tot, OWNER), ("residences", b["residences"] / tot, PARK)]
        bar = viz.bar_split(parts, 1.0, width=12.4, height=0.9).move_to([0, 0.6, 0])
        labs = VGroup()
        for i, (n_, v, c) in enumerate(parts):
            lab = VGroup(tx(f"{100 * v:.0f}%" if v >= 0.05 else f"{100 * v:.1f}%", 20, c, bold=True), tx(n_, 13, GREY_A)).arrange(DOWN, buff=0.05)
            lab.next_to(bar[i], DOWN if i % 2 == 0 else UP, buff=0.2)
            labs.add(lab)
        hd = tx("Marriott's rooms at the end of 2025, by who owns and runs the hotel", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Marriott International, Form 10-K for 2025", size=12)
        beat(self,
             f"Split its rooms by contract. <bookmark mark='a'/> Two-thirds, {b['franchised']:,} rooms, are in franchised "
             "hotels: an owner pays to use the name and the booking system and runs the hotel itself. "
             f"<bookmark mark='b'/> Almost a third, {b['managed']:,}, are in hotels Marriott manages for their owners: its "
             "staff run them, the owner pays the bills and takes the profit or the loss. <bookmark mark='c'/> Then the sliver "
             f"it owns or leases, {b['owned or leased']:,} rooms, <bookmark mark='d'/> and branded residences.",
             base=[hd, src], steps=[VGroup(bar[i], labs[i]) for i in range(4)])

    def revenue(self):
        H = R["hook"]
        items = [("costs reimbursed by hotel owners", H["reimb"], FIXC, bn(H["reimb"])),
                 ("fees: franchise, base and incentive", H["fees"], BRAND, bn(H["fees"])),
                 ("its own and leased hotels, other", H["owned"], OWNER, bn(H["owned"]))]
        rows = hbars(items, max_value=21, x0=0.4, top=1.3, row=1.0, length=6.0, size=18, bar_h=0.55)
        hd = tx(f"Marriott's revenue in 2025: {bn(H['rev'])}", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        q = tx(f"operating income {bn(H['op'])}: about three-quarters of the fees", 19, GOOD, bold=True).move_to([0, -1.9, 0])
        src = source("Marriott International, Form 10-K for 2025; operating income via SEC company facts", size=12)
        beat(self,
             f"Its revenue looks enormous: {H['rev']:.1f} billion dollars in 2025. <bookmark mark='a'/> But "
             f"{H['reimb']:.1f} billion of it is money Marriott spends on the owners' behalf, mostly the wages of the staff at "
             "the hotels it manages, and gets back from them with no mark-up. <bookmark mark='b'/> The real business is the "
             f"fees: {H['fees']:.1f} billion dollars for the name, the booking system and the management. "
             f"<bookmark mark='c'/> Its own hotels and other revenue add {H['owned']:.1f} billion. <bookmark mark='d'/> And "
             f"its operating income was {H['op']:.1f} billion: roughly three-quarters of what it earns in fees.",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], rows[2], q])

    def split(self):
        left = VGroup(draw.hotel(1.4, floors=10, seed=21), tx("Host Marriott", 20, OWNER, bold=True),
                      tx("the hotels and the debt", 15, GREY_A)).arrange(DOWN, buff=0.15).move_to([-3.4, -0.3, 0])
        right = VGroup(draw.bed(1.5, color=BRAND), tx("Marriott International", 20, BRAND, bold=True),
                       tx("the name and the management contracts", 15, GREY_A)).arrange(DOWN, buff=0.15).move_to([3.4, -0.3, 0])
        top = VGroup(tx("Marriott Corporation", 24, WHITE, bold=True), tx("until 8 October 1993", 15, GREY_A)).arrange(DOWN, buff=0.08)
        top.move_to([0, 2.5, 0])
        arrows = VGroup(Arrow(top.get_bottom(), left.get_top(), buff=0.15, color=GREY_B, stroke_width=3),
                        Arrow(top.get_bottom(), right.get_top(), buff=0.15, color=GREY_B, stroke_width=3))
        src = source("Host Marriott Corporation, Form 10-K for 1993", size=12)
        beat(self,
             "It was not always so. <bookmark mark='a'/> Until October 1993 there was one company, Marriott Corporation, "
             "which built hotels, owned them, borrowed against them and ran them. <bookmark mark='b'/> Then it split in two. "
             "The old company kept the buildings and most of the debt, and was renamed Host Marriott. <bookmark mark='c'/> "
             "A new one, Marriott International, took the business of managing hotels and the brands. Its own filing said the "
             "split was meant to separate two kinds of business with different financial and operating characteristics.",
             base=[src], steps=[top, VGroup(arrows[0], left), VGroup(arrows[1], right)])

    def today(self):
        H = R["hook"]
        items = [("Marriott: operating income on assets", 100 * H["op"] / H["mar_assets"], BRAND, f"{100 * H['op'] / H['mar_assets']:.0f}%"),
                 ("Host Hotels: operating income on assets", 100 * H["hst_op"] / H["hst_assets"], OWNER, f"{100 * H['hst_op'] / H['hst_assets']:.1f}%")]
        rows = hbars(items, max_value=18, x0=0.8, top=0.9, row=1.3, length=5.6, size=18, bar_h=0.65)
        hd = tx("the two halves in 2025", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"Host owns {H['hst_hotels']} hotels; {H['hst_marriott']}% of them, by revenue, are run or franchised by Marriott",
                  16, GREY_B).to_edge(DOWN, buff=0.8)
        src = source("Host Hotels & Resorts and Marriott International, Forms 10-K for 2025; SEC company facts", size=12)
        beat(self,
             f"Thirty-two years on, Host Hotels owns {H['hst_hotels']} large hotels, and {H['hst_marriott']} per cent of them, "
             "measured by revenue, are still run or franchised by Marriott. <bookmark mark='a'/> In 2025 Marriott's operating "
             f"income was {100 * H['op'] / H['mar_assets']:.0f} cents for every dollar of assets on its books. "
             f"<bookmark mark='b'/> Host's was about {100 * H['hst_op'] / H['hst_assets']:.0f}. The same hotels, cut two ways: the "
             "half that kept the name earns far more on what it owns, because what it owns is so little.",
             base=[rows.axis, hd, note, src], steps=[rows[0], rows[1]])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part thirty-five: travel and hotels. Why do the biggest hotel companies own "
                            "almost no hotels?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
