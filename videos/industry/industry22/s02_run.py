from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403

CH_COL = {"hold": BRAND, "cut": BAD, "promote": VOL}
CH_NAME = {"hold": "hold: keep advertising, keep the price", "cut": "cut the advertising to nothing",
           "promote": "cut the price to $8"}


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: cut the advertising?",
             "Your brand earns $1.25bn a year. Cut its $100m of advertising, or its price?",
             "Chapter one. Run it. You run a brand of detergent. Next to it on the shelf sits the supermarket's own label, at "
             "half the price. This year you could cut your advertising, or cut your price. What happens?", lit=("moat", "dollar"))
        self.market()
        self.profits()
        self.shares()
        self.store()
        self.answer()

    def market(self):
        U = R["run"]
        sh = draw.shelf(6.0, rows=2, n=10, store_share=0.5).move_to([-3.2, 0.4, 0])
        jug = draw.detergent(1.3).move_to([2.2, 1.6, 0])
        store = draw.detergent(1.3, color=STORE, label="#9AA3B2").move_to([4.6, 1.6, 0])
        l1 = tx(f"your brand: ${U['price']:.0f}", 18, BRAND, bold=True).next_to(jug, DOWN, buff=0.15)
        l2 = tx(f"store label: ${U['store']:.0f}", 18, STORE, bold=True).next_to(store, DOWN, buff=0.15)
        facts = VGroup(tx(f"{U['units'] / 1e6:.0f} million bottles a year in the category", 16, WHITE),
                       tx(f"yours cost ${U['cost']:.0f} to make and ship", 16, WHITE),
                       tx(f"you advertise ${U['ads']:.0f}m a year; your share is {100 * U['target']:.0f}%", 16, ADS),
                       tx(f"advertising wears off: {100 * U['decay']:.0f}% of its effect is gone after a year", 16, GREY_A)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, -1.2, 0])
        tag = estimate_tag("the Works: an illustrative brand and store label", size=12)
        beat(self,
             f"Here is the shelf. <bookmark mark='a'/> Your detergent sells for {U['price']:.0f} dollars; "
             f"<bookmark mark='b'/> the store's own label, beside it, for {U['store']:.0f}. "
             f"<bookmark mark='c'/> Shoppers buy {U['units'] / 1e6:.0f} million bottles of the two a year, and {100 * U['target']:.0f} "
             f"per cent of them pay double for yours. Yours costs {U['cost']:.0f} dollars to make and ship. You spend "
             f"{U['ads']:.0f} million dollars a year on advertising, and its effect wears off: a fifth of what people "
             "remember is gone after a year unless you top it up.",
             base=[sh, tag], steps=[[jug, l1], [store, l2], facts])

    def profits(self):
        U = R["run"]
        Ch = U["choices"]
        series = {CH_NAME[k]: ({r["year"]: r["profit"] for r in v["rows"]}, CH_COL[k]) for k, v in Ch.items()}
        ch = line_chart(series, x=(1, 8), y=(800, 1350), xticks=list(range(1, 9)), yticks=[800, 900, 1000, 1100, 1200, 1300],
                        xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"${v:,.0f}m", ylabel="your profit after advertising, a year",
                        width=8.4, height=4.4, center=(-1.4, -0.5), label_end=False)
        y1 = {k: v["rows"][0]["profit"] for k, v in Ch.items()}
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=CH_COL[k], stroke_width=4), tx(CH_NAME[k], 14, CH_COL[k])
                              ).arrange(RIGHT, buff=0.12) for k in ("hold", "cut", "promote")]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.6, 1.6, 0])
        note = tx(f"year one: cutting the advertising earns ${y1['cut'] - y1['hold']:.0f}m more", 16, BAD, bold=True).move_to([4.4, -0.4, 0])
        tag = estimate_tag("the Works' brand", size=12)
        beat(self,
             f"Three choices. <bookmark mark='a'/> Hold: keep advertising and keep the price, and you earn about "
             f"{y1['hold']:,.0f} million dollars a year after advertising. <bookmark mark='b'/> Cut the advertising to "
             f"nothing, and the first year looks better: {y1['cut']:,.0f} million, because the {U['ads']:.0f} million "
             "is saved and most shoppers still remember you. Then the memory fades, your share slips, and profit falls "
             f"every year after, to {Ch['cut']['rows'][-1]['profit']:,.0f} million in year eight. <bookmark mark='c'/> Cut "
             f"the price to eight dollars instead, and you win many more shoppers but earn {y1['promote']:,.0f} million: "
             "every bottle carries two dollars less.",
             base=[ch.frame, key, tag], steps=[ch.lines[CH_NAME["hold"]], [ch.lines[CH_NAME["cut"]], note], ch.lines[CH_NAME["promote"]]])

    def shares(self):
        U = R["run"]
        Ch = U["choices"]
        series = {CH_NAME[k]: ({r["year"]: 100 * r["share"] for r in v["rows"]}, CH_COL[k]) for k, v in Ch.items()}
        ch = line_chart(series, x=(1, 8), y=(20, 70), xticks=list(range(1, 9)), yticks=[20, 30, 40, 50, 60, 70],
                        xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"{v:.0f}%", ylabel="your share of the bottles sold",
                        width=8.4, height=4.4, center=(-1.4, -0.5), label_end=False)
        end = marker(ch.ax, 8, 100 * Ch["cut"]["rows"][-1]["share"], f"{100 * Ch['cut']['rows'][-1]['share']:.0f}%", BAD, side=DOWN)
        tag = estimate_tag("the Works' brand", size=12)
        beat(self,
             f"Look at the shoppers. <bookmark mark='a'/> Holding keeps your share at {100 * U['target']:.0f} per cent. "
             f"<bookmark mark='b'/> Cutting the advertising lets it slide, year after year, to "
             f"{100 * Ch['cut']['rows'][-1]['share']:.0f} per cent by year eight: shoppers drift to the cheaper bottle once "
             f"they stop being reminded why yours is worth more. <bookmark mark='c'/> The price cut wins "
             f"{100 * Ch['promote']['rows'][0]['share']:.0f} per cent of the shelf at once, and keeps it only as long as the "
             "price stays down.",
             base=[ch.frame, tag], steps=[ch.lines[CH_NAME["hold"]], [ch.lines[CH_NAME["cut"]], end], ch.lines[CH_NAME["promote"]]])

    def store(self):
        U = R["run"]
        Ch = U["choices"]
        items = [(CH_NAME[k], 1 - Ch[k]["rows"][-1]["share"], STORE, f"{100 * (1 - Ch[k]['rows'][-1]['share']):.0f}%")
                 for k in ("cut", "hold", "promote")]
        rows = hbars(items, max_value=1.0, x0=1.2, top=1.2, row=0.95, length=5.0, size=16, bar_h=0.5)
        jug = draw.detergent(1.4, color=STORE, label="#9AA3B2").move_to([-5.6, 1.6, 0])
        lab = tx("the store label's share in year eight", 16, GREY_A).to_edge(UP, buff=0.9)
        tag = estimate_tag("the Works' brand", size=12)
        beat(self,
             "Now look from the retailer's side. <bookmark mark='a'/> If you stop advertising, its own label ends up with "
             f"{100 * (1 - Ch['cut']['rows'][-1]['share']):.0f} per cent of the shelf. <bookmark mark='b'/> If you hold, "
             f"{100 * (1 - Ch['hold']['rows'][-1]['share']):.0f} per cent. <bookmark mark='c'/> If you cut your price, "
             f"{100 * (1 - Ch['promote']['rows'][-1]['share']):.0f}. Every shopper a brand stops reminding walks to the "
             "store's own bottle, which, as Costco's report says of its own label, usually earns the retailer more.",
             base=[rows.axis, jug, lab, tag], steps=[rows[0], rows[1], rows[2]])

    def answer(self):
        U = R["run"]
        Ch = U["choices"]
        c = stat_cards([(f"${Ch['hold']['npv'] / 1e3:.2f}bn", "hold, over eight years, discounted", BRAND),
                        (f"${Ch['cut']['npv'] / 1e3:.2f}bn", "cut the advertising", BAD),
                        (f"${Ch['promote']['npv'] / 1e3:.2f}bn", "cut the price", VOL)], y=0.8, size=40, span=12)
        note = tx("Advertising is a cost you pay every year to keep a premium you earn every year.", 19, WHITE, bold=True).move_to([0, -1.5, 0])
        tag = estimate_tag("the Works' brand, eight years at 8%", size=12)
        beat(self,
             "Add up eight years, discounted. <bookmark mark='a'/> Holding is worth about "
             f"{Ch['hold']['npv'] / 1e3:.1f} billion dollars. <bookmark mark='b'/> Cutting the advertising, "
             f"{Ch['cut']['npv'] / 1e3:.1f} billion: the best first year, and a billion dollars lost over eight. "
             f"<bookmark mark='c'/> Cutting the price, {Ch['promote']['npv'] / 1e3:.1f} billion. <bookmark mark='d'/> That is "
             "the brand business in one picture. The premium is not a reward the brand earned once; it is rent the brand "
             "keeps paying for, with advertising, every year.",
             base=[tag], steps=[c[0], c[1], c[2], note])
