from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Loyalty(VoiceoverScene):
    def construct(self):
        card(self, 5, "The loyalty machine", "What does the owner actually buy with the brand's fee?",
             "Chapter five. The loyalty machine. What an owner buys from a brand, more than anything, is a list of travellers "
             "who come back.", lit=("moat",))
        self.share()
        self.cards()
        self.direct()
        self.discount()

    def share(self):
        L = R["loyalty"]
        c = stat_cards([(f"{L['us']}%", "of Marriott's U.S. room nights booked by loyalty members", BRAND),
                        (f"{L['world']}%", "of its room nights worldwide", BRAND),
                        (f"{L['honors']}m", "Hilton Honors members, end of 2025 (+15%)", GOOD)], y=1.6, size=40, span=12)
        people = VGroup(*[draw.person(0.42, color=BRAND if k < 75 else GREY_B) for k in range(100)]).arrange_in_grid(5, 20, buff=0.12)
        people.move_to([0, -1.4, 0])
        src = source("Marriott International and Hilton Worldwide, Forms 10-K for 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> In 2025, {L['us']} per cent of the room nights at Marriott's American hotels were booked "
             f"by members of its loyalty programme, <bookmark mark='b'/> {L['world']} per cent worldwide. <bookmark mark='c'/> "
             f"Hilton's programme had {L['honors']} million members at the end of the year, fifteen per cent more than a year "
             "before. A member who collects points with one brand stays with that brand, in whichever city, at whichever "
             "owner's hotel. That habit is the thing the owner rents.",
             base=[src], steps=[VGroup(c[0], people), c[1], c[2]])

    def cards(self):
        L = R["loyalty"]
        q = quote(["'Payments received under our co-branded credit card agreements represent", "a significant funding source for the Loyalty Program.'"],
                  "Marriott International, Form 10-K for 2025", size=22)
        note = tx(f"Marriott's co-branded card and other brand fees rose ${L['card']}m in 2025", 18, BRAND).move_to([0, -2.0, 0])
        src = source("Marriott International, Form 10-K for 2025", size=12)
        beat(self,
             "Who pays for the points? <bookmark mark='a'/> Partly the hotels, which pay into the programme on every member's "
             "stay. But also the banks. Marriott's cards are issued in eleven countries, by JPMorgan Chase and American Express "
             "in the United States, and the banks pay Marriott a fixed sum up front and then amounts that grow with cardholders' "
             "spending. In its own words, those "
             f"payments are a significant funding source for the programme. <bookmark mark='b'/> In 2025 its credit card and "
             f"other brand fees rose by {L['card']} million dollars. A hotel company is, in part, a seller of points.",
             base=[src], steps=[q, note])

    def direct(self):
        U = R["run"]
        H = U["hotel"]
        items = [("the brand's fees, branded hotel", 100 * (H["royalty"] + H["programme"]), BRAND, f"{100 * (H['royalty'] + H['programme']):.0f}% of room revenue"),
                 ("an online agent's commission", 100 * H["commission"], AGENT, f"{100 * H['commission']:.0f}% of that booking"),
                 ("a direct booking's own cost", 100 * H["direct"], GOOD, f"{100 * H['direct']:.0f}%")]
        rows = hbars(items, max_value=20, x0=0.6, top=1.2, row=1.0, length=4.2, size=17, bar_h=0.55)
        hd = tx("what each channel costs the Works' hotel", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"branded: {100 * H['ota']:.0f}% of rooms through agents; independent: {100 * H['ota_indep']:.0f}%", 17, GREY_B).move_to([0, -1.9, 0])
        tag = estimate_tag("the Works: channel costs and shares are this series' assumptions", size=12)
        beat(self,
             f"In the Works, the comparison is simple. <bookmark mark='a'/> The brand costs {100 * (H['royalty'] + H['programme']):.0f} "
             f"per cent of all room revenue. <bookmark mark='b'/> An online agent charges {100 * H['commission']:.0f} per cent, "
             f"but only on the rooms it sells. <bookmark mark='c'/> A booking on the brand's own site costs about "
             f"{100 * H['direct']:.0f} per cent, for the card payment and the booking engine. <bookmark mark='d'/> The brand "
             "earns its fee by moving bookings from the second line to the third: an independent hotel, in this series' "
             "assumptions, sells half its rooms through agents; a branded one a quarter.",
             base=[rows.axis, hd, tag], steps=[rows[0], rows[1], rows[2], note])

    def discount(self):
        L = R["loyalty"]
        d = {100 * k: v / 1e6 for k, v in L["disc"].items()}
        ch = line_chart({"the hotel's profit": (d, GOOD)}, x=(0, 15), y=(2.0, 3.0), xticks=[0, 5, 10, 15], yticks=[2.0, 2.5, 3.0],
                        xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: f"${v:.1f}m", ylabel="profit a year, by members' discount on direct bookings",
                        width=8.4, height=4.0, center=(-1.0, -0.4))
        o = L["ota_disc"]
        mk = marker(ch.ax, 10, d[10.0], f"10% off: agents' share {100 * o[0.1]:.0f}% instead of {100 * o[0.0]:.0f}%, profit {m(L['disc'][0.1])}", BAD, side=DOWN)
        mk[1].shift(DOWN * 0.4)
        tag = estimate_tag("the Works: each point of members' discount moves 4 points of agents' share to direct (an assumption)", size=12)
        beat(self,
             "So hotels offer members a lower price for booking direct. Does it pay? <bookmark mark='a'/> In the Works, every "
             "member who books direct gets the discount, but only some of the agents' customers switch. <bookmark mark='b'/> "
             f"At ten per cent off, the agents' share falls from {100 * o[0.0]:.0f} to {100 * o[0.1]:.0f} per cent of rooms, "
             f"and the hotel's profit falls from {L['disc'][0.0] / 1e6:.2f} million to {L['disc'][0.1] / 1e6:.2f}. A member "
             "discount pays only if it brings guests who would not otherwise come, or moves a great many bookings away from "
             "the agents. In this series' reading, that is the owners' gamble whenever a brand asks them to fund a member rate.",
             base=[ch.frame, tag], steps=[VGroup(*ch.lines.values(), *ch.labels.values()), mk])
