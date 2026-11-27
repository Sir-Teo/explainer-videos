from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403


class Factory(VoiceoverScene):
    def construct(self):
        card(self, 9, "The factory's side", "Who carries the risk the brands pass down the chain?",
             "Chapter nine. The factory's side. Every answer in this film, speed, off-price, scarcity, rests on factories "
             "the brands do not own, and on the people who work in them.", lit=("make", "change"))
        self.rana()
        self.codes()
        self.squeeze()
        self.tariffs()

    def rana(self):
        floors = VGroup(*[RoundedRectangle(corner_radius=0.04, width=3.2, height=0.5, stroke_color=GREY_B, stroke_width=2,
                                           fill_color="#1A2230", fill_opacity=1) for _ in range(8)]).arrange(UP, buff=0.04).move_to([-3.6, 0.2, 0])
        machines = VGroup(*[draw.sewing_machine(0.32).move_to(floors[i].get_center() + RIGHT * (0.9 * j - 0.9))
                            for i in range(3, 8) for j in range(3)])
        c = VGroup(tx("24 April 2013, Dhaka, Bangladesh", 18, GREY_A),
                   tx(f"at least {get('ilo.rana'):,.0f} killed", 34, BAD, bold=True),
                   tx(f"more than {get('ilo.rana.injured'):,.0f} injured", 24, WHITE, bold=True),
                   tx("the building housed five garment factories", 18, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.8, 0.4, 0])
        src = source("International Labour Organization, Employment injury insurance in Bangladesh: bridging social security in "
                     "cases of tragedy", size=12)
        beat(self,
             "On 24 April 2013, a building called Rana Plaza, in Dhaka in Bangladesh, collapsed. "
             "<bookmark mark='a'/> It housed five garment factories. <bookmark mark='b'/> At least "
             f"{get('ilo.rana'):,.0f} people were killed and more than {get('ilo.rana.injured'):,.0f} injured. The "
             "International Labour Organization counts it among the worst industrial accidents anywhere. The clothes "
             "sewn there carried the labels of brands that did not own the building and had not built it: the same "
             "arrangement as every contract factory in this film.",
             base=[src], steps=[[floors, machines], c])

    def codes(self):
        q1 = quote(["'We require the contractors that directly manufacture our products ... to comply with a code of",
                    "conduct and other environmental, human rights, health and safety standards for the benefit of",
                    "workers ... from time to time contractors may not comply with such standards or applicable local law'"],
                   "NIKE, Inc., Form 10-K for fiscal 2026", size=16).move_to([0, 1.6, 0])
        q2 = quote(["'We expect finished good manufacturers to undergo a social compliance audit before being",
                    "approved as a Tapestry supplier.'"], "Tapestry, Inc., Form 10-K for fiscal 2026", size=16).move_to([0, -0.6, 0])
        src = source("NIKE, Inc. and Tapestry, Inc., Forms 10-K for fiscal 2026", size=12)
        beat(self,
             "What changed? The brands' own reports now describe rules for the factories they buy from. "
             "<bookmark mark='a'/> NIKE requires its contractors to follow a code of conduct on safety, health and workers' "
             "rights, and says, in the same paragraph, that contractors sometimes do not. <bookmark mark='b'/> Tapestry "
             "expects every new factory making finished goods to pass an audit before it is approved. An audit is a "
             "visit and a checklist, and it describes the factory on the day of the visit.",
             base=[src], steps=[q1, q2])

    def squeeze(self):
        M = R["made"]
        q = quote(["'significant pricing pressure caused by many factors, including intense competition and a highly",
                   "promotional environment, fragmentation in the retail industry, pressure from retailers to reduce",
                   "the costs of products'"], "Tapestry, Inc., Form 10-K for fiscal 2026: risk factors", size=17).move_to([0, 1.8, 0])
        chain = VGroup(tx("shopper", 20, PRICE, bold=True), tx("retailer", 20, DEPT, bold=True), tx("brand", 20, LUX, bold=True),
                       tx("factory", 20, BAD, bold=True), tx("worker", 20, BAD, bold=True)).arrange(RIGHT, buff=1.0).move_to([0, -0.4, 0])
        arrows = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.12, stroke_width=3, stroke_color=GREY_B,
                                max_tip_length_to_length_ratio=0.3) for i in range(4)])
        note = tx(f"NIKE's {M['fw_makers']:.0f} shoe contractors and {M['ap_makers']:.0f} clothing contractors compete for its orders", 17, GREY_A).move_to([0, -2.0, 0])
        src = source("Tapestry, Inc. and NIKE, Inc., Forms 10-K for fiscal 2026", size=12)
        beat(self,
             "And price pressure runs down the chain. <bookmark mark='a'/> Tapestry lists among its risks 'pressure from "
             "retailers to reduce the costs of products'. <bookmark mark='b'/> The shopper wants a lower price; the "
             "retailer presses the brand; the brand presses the factory; and, in this series' reading, the factory, whose "
             "largest cost it can change is labour, presses the people at the machines. <bookmark mark='c'/> And the "
             "factories compete with each other "
             f"for the brands' orders: NIKE's shoes came from {M['fw_makers']:.0f} contractors and its clothes from "
             f"{M['ap_makers']:.0f}, and an order can move to another factory, or another country, next season.",
             base=[src], steps=[q, [chain, arrows], note])

    def tariffs(self):
        B = R["brands"]
        c = stat_cards([(f"${B['ieepa'] / 1e3:.2f}bn", "tariffs NIKE expects back after the Supreme Court's ruling", SPORT),
                        (f"-{B['lulu'][0] - B['lulu'][1]:.1f} pts", "Lululemon's gross margin in 2025, mostly tariffs and markdowns", BAD)],
                       y=0.8, size=40, span=11)
        note = tx("a tariff is paid by the importer, the brand, when the goods land", 18, GREY_A).move_to([0, -1.4, 0])
        src = source("NIKE, Inc., Form 10-K for fiscal 2026; lululemon athletica inc., Form 10-K for fiscal 2025", size=12)
        beat(self,
             "Last, the governments. In 2025 America raised its tariffs and ended the exemption for small parcels, both of "
             "which Lululemon's report names. <bookmark mark='a'/> On 20 February 2026 the Supreme Court "
             "ruled that the tariffs imposed under the emergency powers law were unauthorized, and NIKE booked "
             f"{B['ieepa'] / 1e3:.2f} billion dollars it expects to get back. <bookmark mark='b'/> Lululemon's margin fell "
             f"{B['lulu'][0] - B['lulu'][1]:.1f} points in 2025, mostly, it says, from tariffs and markdowns. "
             "<bookmark mark='c'/> The tariff is paid by the brand when its goods arrive; whether it can pass it on to "
             "shoppers, or back to its factories, is the question every one of these companies answered differently.",
             base=[src], steps=[c[0], c[1], note])
