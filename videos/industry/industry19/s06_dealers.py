from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403


class Dealers(VoiceoverScene):
    def construct(self):
        card(self, 5, "Dealers, lenders and the rental yard", "Who stands between the maker and the machine's owner?",
             "Chapter five. Between the maker and the machine's owner stand three businesses: the dealer, the lender and "
             "the rental yard.", lit=("dollar", "moat"))
        self.dealers()
        self.lenders()
        self.rental()

    def dealers(self):
        D = R["dealers"]
        maker = VGroup(draw.factory(1.6, MACHINE), tx("the maker", 16, MACHINE, bold=True)).arrange(DOWN, buff=0.1).move_to([-5.0, 0.9, 0])
        dealer = VGroup(draw.shop(1.4) if hasattr(draw, "shop") else Square(1.0), tx("the dealer", 16, PRICE, bold=True)).arrange(DOWN, buff=0.1).move_to([0, 0.9, 0])
        owner = VGroup(draw.excavator(1.8, MACHINE), tx("the owner", 16, WHITE, bold=True)).arrange(DOWN, buff=0.1).move_to([5.0, 0.9, 0])
        a1 = Arrow([-3.9, 1.0, 0], [-1.0, 1.0, 0], buff=0.1, stroke_width=4, color=MACHINE)
        a2 = Arrow([1.0, 1.0, 0], [3.9, 1.0, 0], buff=0.1, stroke_width=4, color=PRICE)
        jobs = bullets(["sells and delivers the machine", "stocks the parts", "sends the mechanics",
                        "rents, and buys back the old one"], size=15).next_to(dealer, DOWN, buff=0.35)
        c = stat_cards([(f"{D['cat']}", "Caterpillar dealers, serving 190 countries", MACHINE),
                        (f"{D['de']:,}", "Deere dealer locations in the US and Canada", "#A3D977")], y=-2.2, size=34, span=9)
        src = source("Caterpillar Inc., Form 10-K 2025; Deere & Company, Form 10-K fiscal 2025", size=12)
        beat(self,
             "The makers do not sell most machines themselves. <bookmark mark='a'/> They sell to dealers, <bookmark mark='b'/> "
             "independent companies that sell the machine to its owner, <bookmark mark='c'/> and then stock the parts, "
             "send the mechanics, rent machines out and take old ones in trade. <bookmark mark='d'/> Caterpillar sells "
             f"through {D['cat']} dealers, most of them independently owned, serving 190 countries; Deere through about "
             f"{D['de']:,} dealer locations in America and Canada alone, about sixteen hundred selling farm equipment and "
             "four hundred and fifty construction and forestry machines. Each Caterpillar dealer has the right to sell and "
             "service the company's products in its own territory, so the dealer, not the factory, is who the owner "
             "knows.",
             base=[maker, dealer, owner, src], steps=[a1, a2, jobs, c])

    def lenders(self):
        D = R["dealers"]
        items = [("Deere: financial products", 100 * D["de_fin"] / D["de_rev"], SERVICE, f"${D['de_fin']:.1f}bn, "
                  f"{100 * D['de_fin'] / D['de_rev']:.1f}% of revenue"),
                 ("Caterpillar: Financial Products", 100 * D["cat_fp"] / D["cat_rev"], SERVICE, f"${D['cat_fp']:.1f}bn, "
                  f"{100 * D['cat_fp'] / D['cat_rev']:.1f}% of revenue")]
        rows = hbars(items, max_value=16, x0=-0.6, top=1.0, row=1.1, length=5.4, size=17, bar_h=0.55)
        coin = draw.coin_stack(6, 0.3).move_to([-5.4, -1.6, 0])
        note = tx(f"Caterpillar's dealers added about ${D['dealer_inv']:.1f}bn of inventory in 2025", 16, GREY_A).to_edge(DOWN, buff=0.75)
        src = source("Deere & Company, Form 10-K fiscal 2025; Caterpillar Inc., Form 10-K 2025", size=12)
        beat(self,
             "Machines are expensive, and many buyers borrow to pay for them. So both companies run their own banks. "
             f"<bookmark mark='a'/> Deere's financing brought in {D['de_fin']:.1f} billion dollars in 2025, "
             f"{100 * D['de_fin'] / D['de_rev']:.0f} per cent of its revenue; <bookmark mark='b'/> Caterpillar's "
             f"{D['cat_fp']:.1f} billion, lending both to the owners and to the dealers. Caterpillar's report notes that its "
             "loans to dealers have not historically seen large swings in losses, thanks to its close working "
             "relationships with them: the dealer network and the bank support each other. <bookmark mark='c'/> The dealers' own stocks matter too: when they "
             "build inventory the maker's sales run ahead of what owners buy, and when they cut it, behind.",
             base=[rows.axis, coin, head("The makers' banks"), src], steps=[rows[0], rows[1], note])

    def rental(self):
        D = R["dealers"]
        U = D["uri"]
        m = {y: 100 * v for y, v in U["margin"].items() if y <= 2025}
        ch = line_chart({"United Rentals": (m, PRICE)}, x=(2015, 2025), y=(0, 25), xticks=[2015, 2017, 2019, 2021, 2023, 2025],
                        yticks=[0, 5, 10, 15, 20, 25], yfmt=lambda v: f"{v:.0f}%", ylabel="United Rentals' net income, % of revenue",
                        width=6.4, height=3.8, center=(-3.0, -0.6), label_end=False)
        c = VGroup(tx(f"{U['units'] / 1e6:.1f} million machines and tools", 18, WHITE, bold=True),
                   tx(f"which cost ${U['oec']:.1f}bn new", 17, GREY_A),
                   tx(f"{U['loc']:,} rental locations", 17, GREY_A),
                   tx(f"${U['rev']:.1f}bn of revenue in 2025", 17, PRICE, bold=True),
                   tx(f"about {U['share']}% of North American rental", 17, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.6, 0.3, 0])
        src = source("United Rentals, Inc., Form 10-K 2025 and Forms 10-K via SEC company facts", size=12)
        beat(self,
             "And many machines are never bought by the people who use them. <bookmark mark='a'/> United Rentals, which "
             f"calls itself the world's largest equipment rental company, owns about {U['units'] / 1e6:.1f} million "
             f"machines and tools that cost {U['oec']:.0f} billion dollars new, and rents them from {U['loc']:,} "
             f"locations. <bookmark mark='b'/> It has kept between ten and twenty cents of each dollar of revenue as "
             "profit every year since 2015. A builder who needs a lift for six weeks rents one; the rental company buys machines by the "
             f"thousand, keeps them busy, and sells the old ones on, so its fleet is only about {U['age'] / 12:.0f} years "
             "old on average. Every machine it buys still needs parts and service, and the rental company, not the "
             "builder, is the customer the maker must keep.",
             base=[src], steps=[c, [ch.frame, ch.lines["United Rentals"]]])
