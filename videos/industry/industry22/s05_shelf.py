from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403


class Shelf(VoiceoverScene):
    def construct(self):
        card(self, 4, "The shelf and the buyer", "Who is the brand's real customer?",
             "Chapter four. The shelf and the buyer. A brand is chosen by shoppers, but it is bought by a handful of "
             "retailers, and the largest of them sells its own brands too. The brand fights for the shopper's "
             "memory; it fights the retailer for the shelf and the margin.", lit=("dollar", "moat"))
        self.walmart()
        self.mclane()
        self.trade()
        self.own()

    def walmart(self):
        W = R["retailer"]["walmart"]
        items = [(k, v, PRICE, f"{v}%") for k, v in sorted(W.items(), key=lambda kv: -kv[1])]
        rows = hbars(items, max_value=30, x0=-0.4, top=1.8, row=0.72, length=6.2, size=18, bar_h=0.42)
        crt = draw.cart(1.3).move_to([-5.6, 2.4, 0])
        lab = tx("Walmart's share of each maker's sales, latest fiscal year", 16, GREY_A).to_edge(UP, buff=0.9)
        src = source("Forms 10-K: Clorox (fiscal 2026), Church & Dwight (2025), General Mills (fiscal 2026), P&G (fiscal 2026), "
                     "Kimberly-Clark (2025), Colgate-Palmolive (2025)", size=12)
        beat(self,
             "Here is the customer every maker names in its annual report. <bookmark mark='a'/> Walmart bought "
             f"{W['Clorox']} per cent of everything Clorox sold, <bookmark mark='b'/> {W['Church & Dwight']} per cent of Church "
             f"and Dwight's and {W['General Mills']} per cent of General Mills', <bookmark mark='c'/> {W['Procter & Gamble']} "
             f"per cent of P&G's and Kimberly-Clark's, <bookmark mark='d'/> and {W['Colgate-Palmolive']} per cent of "
             "Colgate's, which sells two-thirds of its products outside America. One buyer with a quarter of your sales can "
             "ask for a lower price, a better promotion, a delivery on its terms. And it cannot easily be replaced: a maker "
             "that walked away from Walmart would lose a fifth of its business overnight, while Walmart would lose one "
             "supplier among many, and could fill the gap on its shelf with its own label.",
             base=[rows.axis, crt, lab, src], steps=[rows[0], VGroup(rows[1], rows[2]), VGroup(rows[3], rows[4]), rows[5]])

    def mclane(self):
        Rt = R["retailer"]
        c = stat_cards([(f"{Rt['mclane']}%", "of Hershey's sales went to one distributor, McLane, which also supplies Walmart", FOOD),
                        (f"{Rt['top10']}%", "of P&G's sales went to its ten largest customers", BRAND),
                        (f"{R['extra']['chd_top4']}%", "of Church & Dwight's to its four largest", BRAND)], y=0.8, size=44, span=12)
        q = quote(["'With the growing trend towards retailer consolidation ... the Company is increasingly dependent on",
                   "certain retailers.'"], "The Clorox Company, Form 10-K for fiscal 2026", size=15, width=11.0).move_to([0, -1.6, 0])
        src = source("The Hershey Company, Form 10-K 2025; The Procter & Gamble Company and The Clorox Company, Forms 10-K for "
                     "fiscal 2026", size=12)
        beat(self,
             "The pattern repeats. <bookmark mark='a'/> Hershey sold "
             f"{Rt['mclane']} per cent of its chocolate to one wholesaler, McLane, which distributes to convenience stores, "
             "drug stores and clubs, and is the main route of Hershey's products into Walmart. <bookmark mark='b'/> P&G's ten "
             f"largest customers took {Rt['top10']} per cent of its sales; "
             f"Church and Dwight's four largest, {R['extra']['chd_top4']} per cent. <bookmark mark='c'/> Clorox's report says it "
             "plainly: as retailers consolidate, the company depends more and more on a few of them.",
             base=[src], steps=[c[0], VGroup(c[1], c[2]), q])

    def trade(self):
        E = R["extra"]
        box = draw.cereal_box(1.6).move_to([-4.6, 0.4, 0])
        q = quote(["'Our revenues are reported net of variable consideration and consideration payable to our customers,",
                   "including trade promotion, consumer coupon redemption, and other reductions to the transaction price'"],
                  "General Mills, Form 10-K for fiscal 2026", size=15, width=8.4).move_to([2.0, 1.2, 0])
        c = tx(f"trade and coupon promotions owed but not yet paid, 31 May 2026: ${E['gis_trade']}m", 18, PRICE, bold=True).move_to([1.6, -1.0, 0])
        src = source("General Mills, Inc., Form 10-K for fiscal 2026", size=12)
        beat(self,
             "Shelf space is paid for too. <bookmark mark='a'/> When General Mills sells cereal to a grocer, part of the price "
             "flows back to the grocer as trade promotion, and to shoppers as coupons. Its report counts its revenue only after taking all that off. <bookmark mark='b'/> At the end of May "
             f"2026 it owed {E['gis_trade']} million dollars of such promotions that it had promised but not yet paid. The "
             "list price is what the maker asks; what it keeps is decided at the shelf.",
             base=[box, src], steps=[q, c])

    def own(self):
        sh = draw.shelf(7.0, rows=3, n=10, store_share=0.3).move_to([-2.6, -0.4, 0])
        q = quote(["'[Kirkland Signature] products also generally carry higher",
                   "margins than national brand products and represent",
                   "a growing portion of our overall sales.'"], "Costco Wholesale, Form 10-K for fiscal 2026", size=15, width=5.6).move_to([4.2, 1.2, 0])
        q2 = quote(["'The Company's products compete with other nationally",
                    "advertised brands and with “private label” brands",
                    "within each category.'"], "The Clorox Company, Form 10-K for fiscal 2026", size=15, width=5.6).move_to([4.2, -1.2, 0])
        src = source("Costco Wholesale Corporation and The Clorox Company, Forms 10-K for fiscal 2026", size=12)

        def glow(vo):
            self.play(sh.store.animate.set_fill(PRICE, 0.95), run_time=1.2)
        beat(self,
             "And the retailer has its own brand. <bookmark mark='a'/> The grey packs on this shelf are the store's: "
             "Costco's report says its own label, Kirkland Signature, generally earns it higher margins than national "
             "brands, and is a growing part of its sales. <bookmark mark='b'/> Clorox lists them as competitors in every "
             "category. The retailer chooses where your product sits, sets the price of the bottle beside it, and sells its own version under "
             "its own name. It is your largest customer and your nearest rival at once.",
             base=[sh, src], steps=[q, q2], after=glow)
