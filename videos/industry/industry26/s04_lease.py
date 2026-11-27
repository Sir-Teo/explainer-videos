from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Lease(VoiceoverScene):
    def construct(self):
        card(self, 3, "The lease is the asset", "What exactly does a landlord own?",
             "Chapter three. The lease is the asset. A landlord owns bricks, but what it sells to investors and lenders is a "
             "set of promises: who will pay, how much, and for how long.", lit=("unit", "moat"))
        self.net()
        self.towers()
        self.mismatch()
        self.losses()
        self.lesson()

    def net(self):
        L = R["lease"]
        doc = draw.lease(1.4).move_to([-4.6, 0.6, 0])
        shop = draw.shop(1.4).move_to([-4.6, -1.6, 0])
        q = quote(["'A net lease typically requires the client to be responsible for monthly rent and certain property",
                   "operating expenses including property taxes, insurance, and maintenance'"],
                  "Realty Income Corporation, Form 10-K for 2025", size=16).move_to([1.6, 1.8, 0])
        c = stat_cards([(f"{L['props']:,.0f}", "properties, at the end of 2025", INCOME),
                        (f"{L['occ']:.1f}%", "of them let", GOOD),
                        (f"{L['term']:.1f} years", "average lease on what it bought in 2025", VALUE)], y=-0.6, size=34, span=8.4)
        c.shift(RIGHT * 1.6)
        src = source("Realty Income Corporation, Form 10-K for 2025", size=12)
        beat(self,
             "Start with the simplest landlord. <bookmark mark='a'/> Realty Income owns pharmacies, grocery stores, gyms, "
             "warehouses and the like, each let to one tenant on a net lease: the tenant pays the rent and also the property "
             f"taxes, the insurance and the repairs. <bookmark mark='b'/> At the end of 2025 it owned {L['props']:,.0f} "
             f"properties, <bookmark mark='c'/> {L['occ']:.1f} per cent of them let, <bookmark mark='d'/> and the buildings "
             f"it bought in 2025 came with leases averaging {L['term']:.1f} years. Its income is close to a bond's coupon, "
             "with the tenant's business standing behind it, which is why it is priced like one.",
             base=[doc, shop, src], steps=[q, c[0], c[1], c[2]])

    def towers(self):
        L = R["lease"]
        t = draw.cell_tower(2.6).move_to([-4.4, -0.4, 0])
        ants = t.antennas
        c = stat_cards([(f"{L['sites']:,.0f}", "communications sites owned by American Tower, end of 2025", OFFICE),
                        ("5-10 years", "non-cancellable leases, with rent rising, typically every year", VALUE)],
                       y=0.4, size=36, span=7.8)
        c.shift(RIGHT * 2.0)
        src = source("American Tower Corporation, Form 10-K for 2025", size=12)
        tag = estimate_tag("this series' reading: a second tenant on a mast adds rent but little cost", size=12)
        beat(self,
             "A phone mast is the same idea with different tenants. <bookmark mark='a'/> American Tower owned "
             f"{L['sites']:,.0f} communications sites at the end of 2025, renting space on each to the mobile networks. "
             "<bookmark mark='b'/> Its leases run five to ten years and cannot be cancelled, with rent that rises, usually "
             "every year. Each extra network that hangs its antennas on a mast pays rent for space the owner has already "
             "built, which is the reason, in this series' reading, that towers keep a large share of each dollar.",
             base=[t, src, tag], steps=[c[0], [c[1]]])

    def mismatch(self):
        L = R["lease"]
        pa = viz.plot_axes([0, 15], [0, 2], x_length=10.0, y_length=2.4, xticks=[0, 2, 4, 6, 8, 10, 12, 14],
                           xfmt=lambda v: f"{v:.0f}y", grid=False, size=13).move_to([0.4, -0.4, 0])
        ax = pa.ax
        owe = Rectangle(width=ax.c2p(L["we_term"], 0)[0] - ax.c2p(0, 0)[0], height=0.5, stroke_width=0, fill_color=BAD,
                        fill_opacity=0.85).move_to(ax.c2p(L["we_term"] / 2, 1.5))
        get_ = Rectangle(width=ax.c2p(L["we_member"] / 12, 0)[0] - ax.c2p(0, 0)[0], height=0.5, stroke_width=0, fill_color=GOOD,
                         fill_opacity=0.85).move_to(ax.c2p(L["we_member"] / 24, 0.5))
        lo = tx(f"what WeWork owed its landlords: ${L['we_lease']:.1f}bn, over about {L['we_term']:.0f} years", 16, BAD,
                bold=True).next_to(owe, UP, buff=0.12)
        lg = tx(f"what its members had promised: a little over {L['we_member']:.0f} months, on average", 16, GOOD,
                bold=True).next_to(get_, DOWN, buff=0.12).align_to(get_, LEFT)
        src = source("The We Company, Form S-1 of 14 August 2019 (figures at 30 June 2019)", size=12)
        beat(self,
             "Now a company that got the promises backwards. <bookmark mark='a'/> WeWork leased whole floors from landlords "
             "and rented desks and offices to members. When it filed to go public in August 2019, it owed its landlords "
             f"{L['we_lease']:.1f} billion dollars of future rent, on leases with about {L['we_term']:.0f} years left. "
             "<bookmark mark='b'/> Its members had committed to stay, on average, a little over "
             f"{L['we_member']:.0f} months. It had promised to pay for fourteen years and been promised payment for one.",
             base=[pa, src], steps=[[owe, lo], [get_, lg]])

    def losses(self):
        W = R["lease"]["we"]
        items = [(str(y), -W[y][1], BAD, f"-${-W[y][1]:.1f}bn") for y in sorted(W)]
        cols = vbars(items, base_y=-2.0, height=3.4, width=1.0, gap=0.7, size=16, max_value=5.0)
        cols.shift(LEFT * 2.2)
        lab = tx("WeWork's net loss each year", 17, GREY_A).to_edge(UP, buff=0.8).shift(LEFT * 2.2)
        rev = tx(f"on revenue of about ${W[2019][0]:.1f}bn, ${W[2020][0]:.1f}bn, ${W[2021][0]:.1f}bn and ${W[2022][0]:.1f}bn", 15,
                 GREY_A).next_to(cols, DOWN, buff=0.6)
        end = VGroup(tx("6 November 2023", 22, BAD, bold=True), tx("WeWork files for Chapter 11", 18, WHITE),
                     tx("bankruptcy protection", 18, WHITE)).arrange(DOWN, buff=0.12).move_to([4.4, 0.6, 0])
        src = source("WeWork Inc., Forms 10-K via SEC company facts; Form 8-K of 7 November 2023", size=12)
        beat(self,
             f"<bookmark mark='a'/> It lost {abs(W[2019][1]):.1f} billion dollars in 2019, {abs(W[2020][1]):.1f} billion in "
             f"2020, {abs(W[2021][1]):.1f} billion in 2021 and {abs(W[2022][1]):.1f} billion in 2022, on revenue of about "
             "three billion a year. When members left in the pandemic, the rent to the landlords did not stop. "
             "<bookmark mark='b'/> On 6 November 2023 WeWork filed for bankruptcy protection. The leases were long; the "
             "promises from its members were short; the gap was its losses.",
             base=[lab, rev, src], steps=[cols, end])

    def lesson(self):
        rows = VGroup(
            VGroup(draw.lease(0.8), tx("a lease is a promise to pay", 20, WHITE, bold=True)).arrange(RIGHT, buff=0.4),
            VGroup(tx("its value: who promises, how much and for how long", 18, INCOME)),
            VGroup(tx("a landlord with long leases to strong tenants owns something like a bond", 18, VALUE)),
            VGroup(tx("a landlord with short leases owns an operating business, and its risk", 18, BAD))
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' summary", size=12)
        beat(self,
             "So the asset is the lease. <bookmark mark='a'/> A lease is a promise to pay, <bookmark mark='b'/> and it is "
             "worth what the promiser is worth, times how much and how long. <bookmark mark='c'/> A landlord with long leases "
             "to strong tenants owns something close to a bond with a roof. <bookmark mark='d'/> A landlord with short "
             "leases, a hotel, a co-working floor, a senior home, owns an operating business inside a building, and its income "
             "moves with the economy.",
             base=[tag], steps=[rows[0], rows[1], rows[2], rows[3]])
