from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class Ads(VoiceoverScene):
    def construct(self):
        card(self, 5, "The shop that sells ads", "Why do the results fill with sponsored products?",
             "Chapter five. The shop that sells ads. Search for anything on a big marketplace and look at what comes first.",
             lit=("dollar", "moat"))
        self.page()
        self.growth()
        self.store()
        self.others()
        self.rules()

    def page(self):
        pg = draw.web_page(6.4, cols=4, rows=2, sponsored=(0, 1, 4, 6), accent=ADS).move_to([0, 0.5, 0])
        lab = tx("sponsored", 15, ADS, bold=True).next_to(pg.flags[0], UP, buff=0.08)
        steps_ = [VGroup(pg.tiles[0], pg.tiles[1], lab), VGroup(pg.tiles[4], pg.tiles[6])]
        organic = VGroup(*[pg.tiles[i] for i in (2, 3, 5, 7)])
        tag = estimate_tag("illustration: a results page", size=12)
        beat(self,
             "Here is a results page. <bookmark mark='a'/> The places that matter most are the first ones, and on the big "
             "marketplaces many of them are sold: sellers bid, in an auction run for each search, to put their product "
             "there, and pay when someone clicks. <bookmark mark='b'/> More are sold further down. <bookmark mark='c'/> "
             "The rest are what the site's own ranking chose. For the platform this is close to perfect revenue: no "
             "warehouse, no van, just a slot on a page that buyers were going to look at anyway.",
             base=[VGroup(pg[0], pg[1], pg[2], pg[3]), tag], steps=steps_ + [organic])

    def growth(self):
        A = R["ads"]["amzn"]
        items = [(str(y), v, ADS, f"${v:.0f}bn") for y, v in A.items()]
        cols = vbars(items, base_y=-2.2, height=3.8, width=1.1, gap=0.45, size=16, max_value=75)
        hd = tx("Amazon's advertising revenue, $bn a year", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        q3, q3p = R["ads"]["q3"], R["ads"]["q3_prev"]
        note = tx(f"nine months of 2026: ${q3:.1f}bn, up {100 * (q3 / q3p - 1):.0f}%", 17, ADS, bold=True).to_edge(UP, buff=1.45)
        src = source("Amazon.com, Forms 10-K for 2021-2025 and 10-Q for 2026 Q3", size=12)
        beat(self,
             f"<bookmark mark='a'/> Amazon first reported its advertising separately for 2019: {A[2019]:.1f} billion "
             f"dollars. <bookmark mark='b'/> By 2022, {A[2022]:.0f} billion. <bookmark mark='c'/> In 2025, "
             f"{A[2025]:.0f} billion, and in the first nine months of 2026 it grew another {100 * (q3 / q3p - 1):.0f} per "
             "cent: sponsored products, display and video ads, sold to its sellers, the brands that supply it, publishers "
             "and others.",
             base=[hd, src], steps=[VGroup(*cols[:3]), VGroup(*cols[3:5]), VGroup(*cols[5:], note)])

    def store(self):
        A, S = R["ads"]["amzn"], R["ads"]["store_op"]
        ch = line_chart({"advertising revenue": (A, ADS), "the shops' operating income": ({y: v for y, v in S.items() if y >= 2019}, SHOP)},
                        x=(2019, 2025), y=(-15, 75), xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025], yticks=[-15, 0, 15, 30, 45, 60, 75],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="Amazon, $bn a year (the shops: North America and International segments)",
                        width=8.2, height=4.3, center=(-1.4, -0.45), nudge={"the shops' operating income": -0.3})
        m = marker(ch.ax, 2022, S[2022], f"2022: -${abs(S[2022]):.1f}bn", BAD, side=RIGHT)
        tag = estimate_tag("this series' reading: Amazon does not report what its advertising earns", size=12)
        beat(self,
             "Now set that beside the shops' profit. <bookmark mark='a'/> The advertising revenue: "
             f"{A[2019]:.0f} billion dollars in 2019, {A[2025]:.0f} billion in 2025. <bookmark mark='b'/> The operating income "
             f"of all Amazon's shops, at home and abroad, from {S[2019]:.0f} billion to {S[2025]:.0f} billion, "
             f"<bookmark mark='c'/> with a loss of {abs(S[2022]):.1f} billion in 2022. In every year the advertising revenue "
             "is larger than the shops' entire profit. Amazon does not say what its ads earn after costs; but an ad costs "
             "little to serve, so in this series' reading the ads may be most of the profit and the selling of goods, on "
             "its own, close to break-even.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["advertising revenue"], ch.labels["advertising revenue"]),
                                         VGroup(ch.lines["the shops' operating income"], ch.labels["the shops' operating income"]), m])

    def others(self):
        A = R["ads"]
        c = stat_cards([(f"${A['ebay']:.1f}bn", "eBay's advertising, 2025, up 22%", ADS),
                        (f"${A['etsy']:.2f}bn", "Etsy's services: mostly on-site ads", ADS),
                        (f"{A['pdd_share']:.0f}%", "of PDD's revenue is 'online marketing services'", ADS)], y=0.4, size=36, span=12.4)
        src = source("eBay and Etsy, Forms 10-K for 2025; PDD Holdings, Form 20-F for 2025", size=12)
        beat(self,
             "It is the same everywhere. <bookmark mark='a'/> eBay's advertising, mostly sellers promoting their own "
             f"listings, brought in {A['ebay']:.1f} billion dollars in 2025, up twenty-two per cent while the rest grew five. "
             "<bookmark mark='b'/> Etsy's services, mostly its on-site ads, grew eleven per cent in a year when what buyers "
             f"spent fell. <bookmark mark='c'/> And PDD, the Chinese company behind Pinduoduo and Temu, earns "
             f"{A['pdd_share']:.0f} per cent of its revenue from what it calls online marketing services: merchants paying "
             "to be seen.",
             base=[src], steps=[c[0], c[1], c[2]])

    def rules(self):
        q = quote(["'... harmed advertisers through, among other things, misrepresentations, omissions, and unfair business",
                   "practices involving the use of reserve prices in Amazon's sponsored ad auctions'"],
                  "Amazon's 10-Q for 2026 Q3, describing a complaint by the FTC and 22 states filed in August 2026", size=17).move_to([0, 1.4, 0])
        b = bullets(["a reserve price is the lowest bid the auction will accept: raise it and every winner pays more",
                     "Amazon disputes the allegations; nothing has been decided",
                     "Run it's warning: past a point, more ads cost a marketplace its buyers"], size=18).move_to([0, -1.2, 0])
        src = source("Amazon.com, Form 10-Q for the third quarter of 2026", size=12)
        beat(self,
             "And the auctions themselves are now in court. <bookmark mark='a'/> In August 2026 the FTC and twenty-two "
             "states sued Amazon, claiming it harmed advertisers through the reserve prices in its sponsored-ad auctions. "
             "<bookmark mark='b'/> A reserve price is the lowest bid an auction will accept; set it higher and winners "
             "pay more. <bookmark mark='c'/> Amazon disputes the claim, and nothing has been decided. <bookmark mark='d'/> "
             "But Run it showed the deeper limit: advertising is nearly free money for a marketplace until the ads crowd "
             "out what buyers came for.",
             base=[src], steps=[q, b[0], b[1], b[2]])
