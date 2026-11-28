from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class Dollar(VoiceoverScene):
    def construct(self):
        card(self, 3, "A seller's dollar", "Where does a forty-dollar order go?",
             "Chapter three. A seller's dollar. Follow one forty-dollar order from the buyer's card to the seller's bank.",
             lit=("dollar",))
        self.split()
        self.fees()
        self.ftc()
        self.amazon()

    def split(self):
        D = R["dollar"]
        b = D["basket"]
        parts = [("the goods", D["goods"], BRAND), ("referral fee", D["referral"], MARKET), ("fulfilment and other fees", D["fulfil"], TOOLS),
                 ("ads", D["ads"], ADS), ("the seller keeps", D["keep"], GOOD)]
        bar = viz.bar_split(parts, b, width=12.4, height=0.9).move_to([0, 0.9, 0])
        labs = VGroup(*[VGroup(tx(f"${v:.2f}", 20, c, bold=True), tx(n, 13, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        hd = tx(f"a ${b:.0f} order on a marketplace, as the Works prices it", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        pk = draw.parcel(0.9).move_to([-5.6, -2.2, 0])
        tag = estimate_tag(f"the Works: a {get('am32.referral'):.0f}% referral fee as on Amazon's price list; the other fees, ads and "
                           "the goods' cost are this series' assumptions", size=12)
        beat(self,
             f"<bookmark mark='a'/> Of the forty dollars, about {D['goods']:.0f} paid the factory for the goods. "
             f"<bookmark mark='b'/> A referral fee of fifteen per cent, {D['referral']:.0f} dollars, goes to the platform "
             f"for the sale. <bookmark mark='c'/> About {D['fulfil']:.0f} more pays it to store, pick, pack and deliver the "
             f"parcel. <bookmark mark='d'/> {D['ads']:.2f} went on ads to be seen in the first place. <bookmark mark='e'/> "
             f"The seller keeps {D['keep']:.2f}, from which it pays its own staff, its photographs, its returns and its "
             "unsold stock. The platform's share, fees and ads together, is close to a third of the price.",
             base=[hd, pk, tag], steps=[VGroup(bar[i], labs[i]) for i in range(5)])

    def fees(self):
        rows = [["Amazon's US price list, November 2026", "referral fee"],
                ["backpacks, handbags and luggage; footwear; eyewear", "15%"],
                ["beauty, health and personal care (above $10)", "15%"],
                ["computers; consumer electronics", "8%"],
                ["Amazon device accessories", "45%"],
                ["the minimum per item; the Professional plan", "$0.30; $39.99 a month"]]
        cols = [None, [WHITE, MARKET], [WHITE, MARKET], [WHITE, MARKET], [WHITE, ADS], [WHITE, GREY_A]]
        t = table(rows, col_x=[-6.0, 2.6], top=1.9, row_h=0.72, size=19, colors=cols)
        src = source("Amazon, 'Pricing' for selling on Amazon (US store), read 28 November 2026", size=12)
        beat(self,
             "Where does the fifteen per cent come from? <bookmark mark='a'/> Amazon publishes its fees. For many "
             "categories, from luggage to shoes, the referral fee is fifteen per cent of the price. <bookmark mark='b'/> "
             "The same for beauty products above ten dollars. <bookmark mark='c'/> For computers and electronics, where "
             "prices are high and margins thin, eight. <bookmark mark='d'/> For accessories to Amazon's own devices, forty-five. "
             "<bookmark mark='e'/> Each item pays at least thirty cents, and a professional seller pays a monthly fee on top. "
             "Storage, delivery and advertising are priced separately.",
             base=[t[0], src], steps=[t[1], t[2], t[3], t[4], t[5]])

    def ftc(self):
        D = R["dollar"]
        q = quote(["'Combined, all of these fees force many sellers to pay close to 50% of their total",
                   "revenues to Amazon.'"], "Federal Trade Commission, announcing its lawsuit, 26 September 2023", size=19).move_to([0, 1.8, 0])
        b = bullets(["the complaint: a monopoly in 'online superstores' and 'marketplace services', kept by pricing",
                     "policies, advertising practices, the structure of Prime and promoting Amazon's own products",
                     "Amazon disputes it; the case is still being fought in Seattle",
                     f"separately, Amazon recorded ${get('am32.ftc.settle'):.1f}bn in 2025 to settle another FTC lawsuit"], size=17).move_to([0, -0.9, 0])
        src = source("FTC press release, 26 September 2023; Amazon, Forms 10-K for 2023 and 2025, 10-Q for 2025 Q3", size=12)
        beat(self,
             "Not everyone thinks a third is the whole story. <bookmark mark='a'/> In September 2023 the Federal Trade "
             f"Commission sued Amazon, saying that with all its fees together many sellers pay close to "
             f"{D['ftc']:.0f} per cent of their revenue to Amazon. That is an allegation, not a finding. <bookmark mark='b'/> "
             "The complaint says Amazon holds a monopoly and keeps it through its pricing rules, its advertising, the design "
             "of Prime and the promotion of its own products. <bookmark mark='c'/> Amazon disputes it, and the case is still "
             "being fought. <bookmark mark='d'/> In 2025 Amazon paid 2.5 billion dollars to settle a different FTC lawsuit. "
             "Whatever the courts decide, the question is the one Run it asked: what can sellers do instead?",
             base=[src], steps=[q, VGroup(b[0], b[1]), b[2], b[3]])

    def amazon(self):
        D = R["dollar"]
        items = [("third-party seller services", D["amzn_3p"], MARKET, f"${D['amzn_3p']:.0f}bn"),
                 ("advertising", D["amzn_ads"], ADS, f"${D['amzn_ads']:.0f}bn"),
                 ("shipping costs", -D["amzn_ship"], BAD, f"-${D['amzn_ship']:.0f}bn"),
                 ("fulfilment costs", -D["amzn_fulfil"], BAD, f"-${D['amzn_fulfil']:.0f}bn")]
        rows = hbars(items, max_value=180, x0=0.0, top=1.5, row=0.95, length=5.4, size=17, bar_h=0.5)
        hd = tx("Amazon in 2025: what sellers pay, against what delivery costs", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx("the costs also deliver Amazon's own sales, so they cannot be set against the fees alone", 15, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("Amazon.com, Form 10-K for 2025", size=12)
        beat(self,
             "Now look from the platform's side. <bookmark mark='a'/> Amazon's sellers paid it "
             f"{D['amzn_3p']:.0f} billion dollars in 2025 in commissions and delivery fees, <bookmark mark='b'/> and "
             f"advertisers, many of them the same sellers, another {D['amzn_ads']:.0f} billion. <bookmark mark='c'/> But "
             f"moving parcels cost Amazon {D['amzn_ship']:.0f} billion in shipping <bookmark mark='d'/> and "
             f"{D['amzn_fulfil']:.0f} billion to run its warehouses, take payments and answer customers. Those costs also "
             "serve Amazon's own shop, so they cannot be matched to the fees one for one; but they show where the money "
             "goes. Much of what a seller pays is not profit for the platform. It is the cost of the van.",
             base=[rows.axis, hd, note, src], steps=[rows[0], rows[1], rows[2], rows[3]])
