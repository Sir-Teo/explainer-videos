from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Buy(VoiceoverScene):
    def construct(self):
        card(self, 6, "The biggest customer", "What does it mean to be every supplier's largest customer?",
             "Chapter six. The biggest customer. A retailer this large is not just a shop: for the companies that make "
             "what it sells, it is the market itself.", lit=("moat",))
        self.share()
        self.edlp()
        self.label()

    def share(self):
        items = [("Clorox", get("clx.walmart"), BAD), ("Church & Dwight", get("chd.walmart"), BAD), ("General Mills", get("gis.walmart"), BAD),
                 ("Procter & Gamble", get("pg.walmart"), DOLLAR), ("Kimberly-Clark", get("kmb.walmart"), DOLLAR), ("Colgate-Palmolive", get("cl.walmart"), DOLLAR)]
        rows = hbars([(n, v, c, f"{v:.0f}%") for n, v, c in items], max_value=30, x0=0.4, top=1.9, row=0.72, length=5.4, size=17, bar_h=0.4)
        lab = tx("Walmart's share of each supplier's sales, as each supplier reports it", 17, GREY_A).to_edge(UP, buff=0.7)
        src = source("the suppliers' latest Forms 10-K, as registered for Part 22", size=12)
        beat(self,
             "Look at Walmart from the suppliers' side. <bookmark mark='a'/> Clorox sells about "
             f"{get('clx.walmart'):.0f} per cent of everything it makes to Walmart; Church and Dwight "
             f"{get('chd.walmart'):.0f}; General Mills {get('gis.walmart'):.0f}. <bookmark mark='b'/> Even Procter and "
             f"Gamble, the world's biggest maker of household brands, sells {get('pg.walmart'):.0f} per cent of its goods "
             "through Walmart. In this series' reading, a supplier can lose any other customer and carry on; losing Walmart's "
             "shelves would change the company, and both sides know it when they sit down to agree a price.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:3]), VGroup(*rows[3:])])

    def edlp(self):
        q = quote(["'EDLP is our pricing philosophy under which we price items at a low price every day so our customers",
                   "trust that our prices will not change under frequent promotional activity'"], "Walmart, Form 10-K for fiscal 2026", size=18).move_to([0, 1.6, 0])
        g = bullets(["fewer price changes mean steadier sales, simpler stores and fewer staff",
                     "steady orders let suppliers plan their factories and lorries",
                     "and the buyer's question to the supplier is always the same: can you make it cheaper?"], size=18).move_to([0, -0.9, 0])
        tag = estimate_tag("the quotation is Walmart's; the consequences are this series' reading", size=12)
        beat(self,
             "Walmart's answer to the price war of Run it is not to have one. <bookmark mark='a'/> It calls its approach "
             "everyday low prices: few promotions, so customers trust the price on the shelf. <bookmark mark='b'/> In this "
             "series' reading, steady prices mean steady sales, which mean simpler stores, steadier orders for suppliers, "
             "and a buyer who asks every supplier, every year, to find a way to make it cheaper.",
             base=[tag], steps=[q, g])

    def label(self):
        shelf = draw.shelf(9.0, rows=3, n=12).move_to([0, 0.9, 0])
        g = VGroup(tx("Own label: the retailer's brand", 21, WHITE, bold=True),
                   tx("made by a supplier to the retailer's recipe, sold under the retailer's name", 17, GOODS),
                   tx("usually cheaper to the shopper, and more profitable to the retailer (Costco says so of Kirkland)", 17, GOOD),
                   tx("and a standing reminder to every brand on the next shelf of what it can be replaced with", 17, BAD)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([0, -1.6, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        tag = estimate_tag("this series' reading; Costco's Form 10-K for fiscal 2026 on Kirkland Signature", size=12)
        beat(self,
             "The retailer's other weapon is its own brand. <bookmark mark='a'/> A store's own label is made by a supplier "
             "to the retailer's recipe. <bookmark mark='b'/> It is usually cheaper to the shopper and earns the retailer "
             "more; Costco says exactly that of Kirkland Signature. <bookmark mark='c'/> And in this series' reading it sits "
             "beside the famous brand on the shelf as a reminder of what that brand could be replaced with, which is a "
             "strong card to hold in a negotiation. The brands answer with advertising, which Part 22 showed is their own "
             "kind of moat: a shopper who asks for the name on the box keeps the retailer honest too.",
             base=[shelf, tag], steps=[g[:2], g[2], g[3]])
