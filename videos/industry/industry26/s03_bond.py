from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Bond(VoiceoverScene):
    def construct(self):
        card(self, 2, "A bond with a roof", "Why does a building's price move when the building does not?",
             "Chapter two. A bond with a roof. A building with tenants on long leases pays its owner a stream of money, "
             "much as a bond pays its holder interest, and it is priced the same way.", lit=("unit", "change"))
        self.point()
        self.curve()
        self.yields()
        self.spread()
        self.leverage()

    def point(self):
        P = R["run"]["one_point"]
        c = stat_cards([(f"{100 * P[0.04]:.0f}%", "a one-point rise from 4% to 5%", BAD),
                        (f"{100 * P[0.05]:.0f}%", "from 5% to 6%", BAD),
                        (f"{100 * P[0.075]:.0f}%", "from 7.5% to 8.5%", VALUE)], y=-0.4, size=40, span=12)
        eq = MathTex(r"V = \frac{\text{NOI}}{r} \qquad \frac{V_{\text{new}}}{V} = \frac{r}{r + 0.01}", font_size=50).move_to([0, 2.0, 0])
        lab = tx("the change in value when the rate rises one point and the income does not", 16, GREY_A).move_to([0, 0.9, 0])
        tag = estimate_tag("this series' arithmetic", size=12)
        beat(self,
             "Start with the arithmetic. <bookmark mark='a'/> If value is income divided by a rate, then when the rate rises "
             "and the income does not, the value falls by the ratio of the old rate to the new. <bookmark mark='b'/> A rise "
             f"from four per cent to five takes {abs(100 * P[0.04]):.0f} per cent off the value. <bookmark mark='c'/> From five "
             f"to six, {abs(100 * P[0.05]):.0f}. <bookmark mark='d'/> From seven and a half to eight and a half, "
             f"{abs(100 * P[0.075]):.0f}. The lower the rate, the more each point matters, which is why the buildings bought "
             "at the lowest rates, in 2021, fell furthest when rates rose.",
             base=[lab, tag], steps=[eq, c[0], c[1], c[2]])

    def curve(self):
        S = R["run"]["sweep_cap"]
        pts = {100 * k: v for k, v in S.items()}
        ch = line_chart({"value of $10m a year": (pts, VALUE)}, x=(3.5, 9.5), y=(0, 300), xticks=[4, 5, 6, 7, 8, 9],
                        yticks=[0, 100, 200, 300], xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: f"${v:.0f}m",
                        ylabel="what $10 million of income a year is worth, by the rate buyers demand", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        m1 = marker(ch.ax, 4, 250, "4%: $250m", VALUE, side=RIGHT)
        m2 = marker(ch.ax, 5, 200, "5%: $200m", VALUE, side=UP)
        m3 = marker(ch.ax, 7.5, 1000 / 7.5, "7.5%: $133m", BAD, side=UP)
        tag = estimate_tag("this series' arithmetic", size=12)
        beat(self,
             "Drawn as a curve, <bookmark mark='a'/> ten million dollars a year is worth two hundred and fifty million at four "
             "per cent, <bookmark mark='b'/> two hundred million at five, <bookmark mark='c'/> and a hundred and thirty-three "
             "million at seven and a half. The curve is steepest at the left: when money is cheap, small changes in the rate "
             "make and destroy fortunes.",
             base=[ch.frame, tag], steps=[[ch.lines["value of $10m a year"], m1], m2, m3])

    def yields(self):
        B = R["bond"]
        ch = line_chart({"what Realty Income earned on what it bought": (B["o_yield"], INCOME),
                         "10-year Treasury yield": ({y: B["gs10"][y] for y in range(2015, 2026)}, RATE)},
                        x=(2015, 2025), y=(0, 8), xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[0, 2, 4, 6, 8],
                        yfmt=lambda v: f"{v:.0f}%", ylabel="per cent a year", width=9.2, height=4.4, center=(-1.2, -0.45),
                        nudge={"10-year Treasury yield": -0.25})
        o = B["o_yield"]
        m1 = marker(ch.ax, 2021, o[2021], f"2021: {o[2021]:.1f}%", INCOME, side=DOWN)
        m2 = marker(ch.ax, 2024, o[2024], f"2024: {o[2024]:.1f}%", INCOME, side=UP)
        shop = draw.shop(0.9).move_to([5.8, 2.4, 0])
        src = source("Realty Income, Forms 10-K 2015-2025 (initial cash yield on its investments each year); Federal Reserve "
                     "H.15, 10-year Treasury (annual average), via FRED", size=12)
        beat(self,
             "Now the real thing. Realty Income buys shops, warehouses and other buildings let to single tenants on long "
             "leases, and every year it reports what it paid for them as a yield: the first year's rent over the price. "
             "<bookmark mark='a'/> From 2015 to 2019 it paid prices that yielded six and a half per cent or so, while a "
             f"ten-year American government bond paid two or three. <bookmark mark='b'/> In 2021, with the bond at "
             f"{B['gs10'][2021]:.1f}, it paid prices that yielded only {o[2021]:.1f} per cent: buildings were dear. "
             f"<bookmark mark='c'/> By 2024 the bond paid {B['gs10'][2024]:.1f} and it bought at {o[2024]:.1f}: buildings "
             "had got cheaper, for the same rent.",
             base=[ch.frame, shop, src], steps=[[ch.lines["what Realty Income earned on what it bought"],
                                                 ch.labels["what Realty Income earned on what it bought"],
                                                 ch.lines["10-year Treasury yield"], ch.labels["10-year Treasury yield"]], m1, m2])

    def spread(self):
        B = R["bond"]
        sp = B["spread"]
        items = [(str(y), sp[y], INCOME if sp[y] > 3.5 else VALUE, f"{sp[y]:.1f} pts") for y in range(2015, 2026)]
        cols = vbars(items, base_y=-2.0, height=3.4, width=0.7, gap=0.35, size=14, max_value=5.5)
        lab = tx("Realty Income's buying yield minus the 10-year Treasury yield", 17, GREY_A).to_edge(UP, buff=0.8)
        q = tx(f"the Federal Reserve's average capitalization rate since 2001: {B['cap_avg']:.2f}%", 17, RATE, bold=True).move_to([0, 2.2, 0])
        src = source("Realty Income, Forms 10-K; FRED; Federal Reserve, Financial Stability Report, November 2026", size=12)
        beat(self,
             "The gap between the two is what a buyer is paid for owning a building rather than a bond. "
             f"<bookmark mark='a'/> It was about {sp[2015]:.1f} percentage points in 2015 and {sp[2020]:.1f} in 2020, when "
             f"bond yields collapsed. <bookmark mark='b'/> Since 2022 it has been about {sp[2025]:.0f}: buildings have "
             "repriced, but by less than bonds. The gap pays for the risks a bond does not have: tenants who leave, roofs "
             "that wear out, buildings that cannot be sold in a hurry. <bookmark mark='c'/> The Federal Reserve tracks the "
             f"same yield across all commercial sales: it has averaged {B['cap_avg']:.2f} per cent since 2001, and in its "
             "words has 'increased sizably from historical lows in 2022'.",
             base=[lab, src], steps=[VGroup(*cols[:6]), VGroup(*cols[6:]), q])

    def leverage(self):
        S = R["run"]["sweep_occ"]
        pts = {100 * k: v for k, v in S.items()}
        ch = line_chart({"net operating income": (pts, INCOME)}, x=(40, 100), y=(-2, 12), xticks=[40, 50, 60, 70, 80, 90, 100],
                        yticks=[0, 4, 8, 12], xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: f"${v:.0f}m",
                        ylabel="the Works' office: income a year at $50 a square foot, by the share let", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        zero = DashedLine(ch.ax.c2p(40, 0), ch.ax.c2p(100, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        be = 100 * R["run"]["breakeven_occ"]
        m1 = marker(ch.ax, 95, S[0.95], f"95% let: ${S[0.95]:.0f}m", INCOME, side=UP)
        m2 = marker(ch.ax, 65, S[0.65], f"65% let: ${S[0.65]:.0f}m", BAD, side=UP)
        m3 = marker(ch.ax, be, 0, f"{be:.0f}% let: nothing", BAD, side=DOWN)
        tag = estimate_tag("the Works' office: $9m of costs a year whether let or not", size=12)
        beat(self,
             "And the income is a lever. <bookmark mark='a'/> The Works' office earns ten million dollars when it is "
             "ninety-five per cent let. <bookmark mark='b'/> Sixty-five per cent let, at the same rent, it earns only four "
             f"million. <bookmark mark='c'/> Below about {be:.0f} per cent it earns nothing at all, because the costs of "
             "running it are the same whether a floor is let or empty. A building is a fixed-cost business, like the "
             "factories of Part 4, and its price is that leveraged income divided by a rate that moves on its own.",
             base=[ch.frame, zero, tag], steps=[[ch.lines["net operating income"], m1], m2, m3])
