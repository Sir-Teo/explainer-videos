from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class Models(VoiceoverScene):
    def construct(self):
        card(self, 2, "Shop or marketplace", "Who owns the stock, and what counts as revenue?",
             "Chapter two. Shop or marketplace. The same order on the same website can be two different businesses, and "
             "the accounts show it.", lit=("unit", "dollar"))
        self.two()
        self.amazon()
        self.ladder()
        self.china()
        self.reading()

    def two(self):
        M = R["models"]
        b = M["basket"]
        fee = M["take_works"] * b
        left = VGroup(tx("as a shop", 22, SHOP, bold=True), draw.parcel(1.0), draw.price_tag(f"${b:.0f}", 1.0, color=SHOP),
                      tx(f"revenue: ${b:.0f}", 22, SHOP, bold=True), tx("it bought the goods, holds the stock,", 15, GREY_A),
                      tx("sets the price and takes the risk", 15, GREY_A)).arrange(DOWN, buff=0.18).move_to([-3.6, 0.2, 0])
        right = VGroup(tx("as a marketplace", 22, MARKET, bold=True), draw.parcel(1.0), draw.price_tag(f"${b:.0f}", 1.0, color=MARKET),
                       tx(f"revenue: ${fee:.0f} of fees", 22, MARKET, bold=True), tx("a seller owns the goods and sets the price;", 15, GREY_A),
                       tx("the site counts only what it charges", 15, GREY_A)).arrange(DOWN, buff=0.18).move_to([3.6, 0.2, 0])
        line = DashedLine([0, 2.6, 0], [0, -2.4, 0], color=GREY_B)
        tag = estimate_tag(f"illustration: a ${b:.0f} order with the Works' {100 * M['take_works']:.0f}% take rate", size=12)
        beat(self,
             f"Take one order: a forty-dollar item, delivered tomorrow. <bookmark mark='a'/> If the website bought it from "
             "the maker, it owns the stock, sets the price and takes the risk of not selling it. The whole forty dollars "
             "is its revenue, and most of it goes out again to pay for the goods. <bookmark mark='b'/> If a separate "
             "seller listed it, the website never owns it. Its revenue is only its fees, say twelve dollars, and the rest "
             "belongs to the seller. Same parcel, same doorstep; a third of the revenue, and a far higher share of it kept.",
             base=[line, tag], steps=[left, right])

    def amazon(self):
        H = R["hook"]["mix"]
        ch = line_chart({"online stores (its own stock)": (H["online"], SHOP), "third-party seller services (fees)": (H["3p"], MARKET)},
                        x=(2015, 2025), y=(0, 300), xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[0, 100, 200, 300],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="Amazon's net sales, $bn a year", width=7.6, height=4.2,
                        center=(-2.2, -0.45), nudge={"third-party seller services (fees)": -0.2})
        q = quote(["'We are not the seller of record in these", "transactions.'"], "Amazon, Form 10-K for 2025, on third-party sellers",
                  size=15).move_to([4.6, 2.2, 0])
        src = source("Amazon.com, Forms 10-K for 2017-2025", size=12)
        o, t = H["online"], H["3p"]
        beat(self,
             "Amazon is both. <bookmark mark='a'/> Its own shop sold "
             f"{o[2015]:.0f} billion dollars of goods in 2015 and {o[2025]:.0f} billion in 2025. <bookmark mark='b'/> Its fees "
             f"from other sellers rose from {t[2015]:.0f} billion to {t[2025]:.0f} billion, more than ten times over, and "
             "those fees stand for a much larger value of goods, because each dollar of fees is only a slice of a sale. "
             "<bookmark mark='c'/> Amazon does not publish what third-party sellers sell in total, so neither chart shows "
             "how big the marketplace really is.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["online stores (its own stock)"], ch.labels["online stores (its own stock)"]),
                                          VGroup(ch.lines["third-party seller services (fees)"], ch.labels["third-party seller services (fees)"]), q])

    def ladder(self):
        T = R["models"]["take"]
        items = [("Shopify (software and payments)", T["Shopify"], TOOLS, f"{T['Shopify']:.1f}%"),
                 ("Shopee (Sea)", T["Shopee"], MARKET, f"{T['Shopee']:.1f}%"),
                 ("eBay", T["eBay"], MARKET, f"{T['eBay']:.1f}%"),
                 ("Etsy", T["Etsy"], MARKET, f"{T['Etsy']:.1f}%")]
        rows = hbars(items, max_value=26, x0=-0.6, top=1.4, row=1.0, length=6.2, size=18, bar_h=0.55)
        hd = tx("The take rate: revenue as a share of what buyers spent, 2025", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Forms 10-K for 2025 of Shopify (revenue over GMV), eBay and Etsy; Sea, Form 20-F for 2025", size=12)
        beat(self,
             "For a marketplace the key number is the take rate: what it keeps of each dollar buyers spend. "
             f"<bookmark mark='a'/> Shopify, which sells shops their software and payments and leaves the selling to them, "
             f"takes about {T['Shopify']:.0f} cents. <bookmark mark='b'/> Shopee, which Sea calls the largest e-commerce platform in Southeast Asia, "
             f"{T['Shopee']:.1f}. <bookmark mark='c'/> eBay, {T['eBay']:.1f}. <bookmark mark='d'/> Etsy, where many of the "
             f"goods are handmade or one of a kind, {T['Etsy']:.1f}. In this series' reading, the more a seller depends on "
             "the platform for its buyers, the more the platform can charge.",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], rows[2], rows[3]])

    def china(self):
        M = R["models"]
        W = R["world"]
        jd_p = 100 * M["jd_product"] / M["jd_total"]
        c = stat_cards([(f"{jd_p:.0f}%", "of JD.com's revenue is goods it sold itself", SHOP),
                        (f"RMB{W['baba_cmr']:.0f}bn", "Alibaba's fees and ads from Taobao and Tmall", MARKET),
                        (f"${M['shop_gmv']:.0f}bn", "spent through Shopify's merchants", TOOLS),
                        (f"${M['shop_rev']:.1f}bn", "Shopify's revenue from it", TOOLS)], y=0.3, size=32, span=12.8)
        src = source("JD.com and Alibaba, Forms 20-F; Shopify, Form 10-K for 2025", size=12)
        beat(self,
             "The same split runs through the industry. <bookmark mark='a'/> In China, JD.com is mostly a shop: "
             f"{jd_p:.0f} per cent of its revenue is goods it bought and resold. <bookmark mark='b'/> Alibaba's Taobao and "
             "Tmall are mostly a market: their main revenue is what merchants pay for placement and commissions, "
             f"{W['baba_cmr']:.0f} billion yuan in the year to March 2026. <bookmark mark='c'/> And Shopify is neither. Its "
             f"merchants sold {M['shop_gmv']:.0f} billion dollars of goods in 2025, <bookmark mark='d'/> and Shopify's "
             f"revenue was {M['shop_rev']:.1f} billion: it is the toll road that runs to thousands of independent shops.",
             base=[src], steps=[c[0], c[1], c[2], c[3]])

    def reading(self):
        g = VGroup(tx("Three businesses under one word", 22, WHITE, bold=True),
                   tx("the shop: owns the stock, earns a retail margin, carries the risk", 18, SHOP),
                   tx("the marketplace: owns nothing, earns a take rate, needs both sides", 18, MARKET),
                   tx("the toll road: sells the tools, takes a few cents of every sale", 18, TOOLS)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "In this series' reading, e-commerce is three businesses under one word. <bookmark mark='a'/> The shop, which "
             "earns a retail margin and carries the stock. <bookmark mark='b'/> The marketplace, which owns nothing and "
             "earns a take rate. <bookmark mark='c'/> And the toll road, which sells the tools. The biggest companies "
             "combine them, and the next chapter follows a seller's dollar through the combination.",
             base=[tag], steps=[g[:2], g[2], g[3]])
