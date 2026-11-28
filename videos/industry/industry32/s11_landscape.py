from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403

OFFSET = {"Amazon": UP, "JD.com": DOWN, "Alibaba": UP, "PDD (Temu)": UP, "Coupang": RIGHT, "MercadoLibre": RIGHT, "Sea (Shopee)": DOWN,
          "Carvana": UP, "Vipshop": LEFT, "DoorDash": DOWN, "Chewy": LEFT, "Wayfair": LEFT, "Shopify": UP, "eBay": UP, "Instacart": UP,
          "Etsy": DOWN, "Revolve": UP, "Global-e": UP, "Beyond (Overstock)": RIGHT, "Warby Parker": LEFT, "FIGS": DOWN, "Jumia": UP,
          "Allbirds": LEFT}
FLOOR = -0.24


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who sells online, and who keeps the most?",
             "Chapter nine. The landscape, as of November 2026: shops, marketplaces, tools, delivery platforms and brands, by "
             "size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]

        def lx(v):
            return np.log10(v)
        pa = viz.plot_axes([-1.0, 3.0], [FLOOR - 0.02, 0.30], x_length=10.0, y_length=4.9,
                           xticks=[lx(0.1), lx(1), lx(10), lx(100), lx(1000)], yticks=[-0.2, -0.1, 0, 0.1, 0.2, 0.3],
                           xfmt=lambda v: f"${10 ** v:g}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue, median of the last five years", size=13).move_to([-0.3, -0.5, 0])
        xl = tx("revenue, latest year (log scale; yuan at the filings' rates)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.02 * np.sqrt(c["rev"] / 10)
            y = max(c["margin"], FLOOR)
            d = Dot(pa.ax.c2p(lx(c["rev"]), y), radius=r, color=col, fill_opacity=0.85)
            name = c["name"] if c["margin"] >= FLOOR else f"{c['name']} ({100 * c['margin']:.0f}%)"
            lab = tx(name, 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        order = ["mixed", "market", "shop", "tools", "delivery", "brand"]
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 12, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in order if g in groups]).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.95)
        hd = tx("E-commerce: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        zero = DashedLine(pa.ax.c2p(-1.0, 0), pa.ax.c2p(3.0, 0), color=GREY_B, stroke_width=1.5)
        src = source("Forms 10-K and 20-F via SEC company facts", size=12)
        g = {c["name"]: c for c in C}
        pc = lambda n: 100 * g[n]["margin"]  # noqa: E731
        beat(self,
             "The whole industry in one picture. <bookmark mark='a'/> The giants that do everything: Amazon kept a median "
             f"{pc('Amazon'):.1f} cents of each dollar over five years, MercadoLibre {pc('MercadoLibre'):.1f}, Sea "
             f"{pc('Sea (Shopee)'):.1f}. <bookmark mark='b'/> The pure marketplaces keep the most: PDD {pc('PDD (Temu)'):.0f} "
             f"cents, eBay {pc('eBay'):.0f}, Etsy {pc('Etsy'):.0f}, Alibaba {pc('Alibaba'):.1f}. <bookmark mark='c'/> The "
             f"shops that own their stock keep the least: JD.com {pc('JD.com'):.1f}, Coupang {pc('Coupang'):.1f}, Chewy "
             f"{pc('Chewy'):.1f}, and Wayfair a loss. <bookmark mark='d'/> Shopify, the toll road, {pc('Shopify'):.0f}. "
             "<bookmark mark='e'/> The delivery platforms, and <bookmark mark='f'/> the direct brands, most of them still "
             "losing money. In this series' reading, owning nothing pays best, once the market is yours.",
             base=[pa, xl, hd, key, zero, src],
             steps=[groups["mixed"], groups["market"], groups["shop"], groups["tools"], groups["delivery"], groups["brand"]])

    def map(self):
        cols = [("Giants", CLOUD, ["Amazon", "Alibaba", "JD.com", "PDD (Pinduoduo, Temu)", "Walmart", "MercadoLibre", "Sea (Shopee)"]),
                ("Marketplaces", MARKET, ["eBay", "Etsy", "Rakuten", "Flipkart", "Meesho", "Zalando", "TikTok Shop"]),
                ("Shops online", SHOP, ["Coupang", "Wayfair", "Chewy", "Vipshop", "Shein", "Revolve"]),
                ("Tools", TOOLS, ["Shopify", "Global-e", "Stripe", "Adyen", "PayPal"]),
                ("Delivery", SUBS, ["DoorDash", "Instacart", "Meituan", "Uber Eats"]),
                ("Direct brands", BRAND, ["Warby Parker", "FIGS", "Allbirds"])]
        gr = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            gr.add(box)
        note = tx("Names only where this film has not measured them: Rakuten, Flipkart, Meesho, Zalando, TikTok Shop, Shein, Stripe, Adyen, "
                  "PayPal, Meituan and Uber Eats; Walmart's online sales are in Part 31", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The giants, each a shop, a marketplace and more. <bookmark mark='b'/> The "
             "marketplaces, from eBay to India's Flipkart and Meesho and Europe's Zalando. <bookmark mark='c'/> The shops "
             "that sell online from their own stock. <bookmark mark='d'/> The tools and payment firms behind independent "
             "shops. <bookmark mark='e'/> The delivery platforms. <bookmark mark='f'/> And the direct brands.",
             base=[head("The map of the business"), note], steps=list(gr))
