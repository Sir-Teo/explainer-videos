from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403

MAC, KOH = "Macy's", "Kohl's"
IDX_COL = {"TJX": OFF, "Ross": "#D7B8FF", "Burlington": "#8E6BD8", "Macy's": DEPT, "Kohl's": "#C9D3E0"}


class OffPrice(VoiceoverScene):
    def construct(self):
        card(self, 5, "Selling other people's mistakes", "Where do the clothes nobody bought go?",
             "Chapter five. Selling other people's mistakes. The second answer to the buyer's problem is not to guess "
             "better at all, but to buy what other people guessed wrong.", lit=("moat", "change"))
        self.leftovers()
        self.model()
        self.growth()
        self.size()
        self.margin()

    def leftovers(self):
        U = R["run"]["choices"]
        rail = draw.rail(4.6, n=6).move_to([-3.2, 1.2, 0])
        lab = tx(f"the early buyer's leftovers: about {U['far']['cleared'] / 1e3:.0f},000 shirts a season", 17, FAR, bold=True).move_to([-3.2, -1.6, 0])
        shop = draw.shop(2.0) if hasattr(draw, "shop") else Square(1.5)
        shop.move_to([3.6, 1.0, 0])
        sl = tx("an off-price shop", 17, OFF, bold=True).next_to(shop, DOWN, buff=0.2)
        arrow = Arrow([-0.6, 1.0, 0], [2.2, 1.0, 0], buff=0, stroke_color=OFF, stroke_width=5)
        est = estimate_tag("the Works' season", size=12)
        beat(self,
             "Go back to the Works' season. <bookmark mark='a'/> The buyer who ordered everything early ends an average "
             f"season with about {U['far']['cleared'] / 1e3:.0f} thousand shirts nobody bought at full price. The Works "
             "put them in its own sale. <bookmark mark='b'/> Not every brand or shop wants to clear its mistakes in its own "
             "windows, and the space is needed for next season. <bookmark mark='c'/> So there is a "
             "business that buys those clothes, and others like them, and sells them on, cheaply, in shops of its own.",
             base=[est], steps=[[rail, lab], arrow, [shop, sl]])

    def model(self):
        O = R["offprice"]
        c = stat_cards([(f"{O['vendors']:,.0f}", "vendors it buys from", OFF),
                        (f"{O['lo']:.0f}-{O['hi']:.0f}%", "below full-price shops' regular prices", PRICE),
                        (f"{O['stores']:,.0f}", f"stores; it sees room for {O['potential']:,.0f}", OFF)], y=1.3, size=38, span=12)
        q = quote(["'Our practice is to not engage in promotional pricing activity such as sales or coupons.'",
                   "'They typically buy throughout the year, with much of our merchandise purchased for the",
                   "current or immediately upcoming season.'"], "The TJX Companies, Inc., Form 10-K for fiscal 2026",
                  size=17).move_to([0, -1.3, 0])
        src = source("The TJX Companies, Inc., Form 10-K for fiscal 2026", size=12)
        beat(self,
             "The largest is TJX, owner of TJ Maxx, Marshalls, HomeGoods and, in Europe, TK Maxx. <bookmark mark='a'/> It "
             f"says it buys from about {O['vendors']:,.0f} vendors, thousands of them new each year: makers, brands and "
             f"other retailers. <bookmark mark='b'/> It sells at prices it says are generally {O['lo']:.0f} to "
             f"{O['hi']:.0f} per cent below what full-price shops charge for the same things, <bookmark mark='c'/> from "
             f"{O['stores']:,.0f} stores, and thinks it has room for about {O['potential']:,.0f}. <bookmark mark='d'/> And it "
             "never holds a sale. Its buyers buy through the year, much of it for the season that is already under way: "
             "they are buying after the guess has been made, from whoever guessed wrong.",
             base=[src], steps=[c[0], c[1], c[2], q])

    def growth(self):
        O = R["offprice"]["index"]
        series = {k: ({y: v for y, v in O[k].items() if y != 2021}, IDX_COL[k]) for k in ("Burlington", "TJX", "Ross", "Macy's", "Kohl's")}
        ch = line_chart(series, x=(2015, 2026), y=(0.5, 2.5), xticks=[2015, 2017, 2019, 2021, 2023, 2026],
                        yticks=[0.5, 1.0, 1.5, 2.0, 2.5], yfmt=lambda v: f"x{v:.1f}",
                        ylabel="sales against the fiscal year ending early 2015 (= 1)", width=9.4, height=4.4,
                        center=(-0.8, -0.45), nudge={"TJX": 0.06, "Ross": -0.08, MAC: 0.14, KOH: -0.14})
        one = DashedLine(ch.ax.c2p(2015, 1), ch.ax.c2p(2026, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        src = source("Forms 10-K via SEC company facts: net sales, fiscal years ending in January or early February of each "
                     "year shown; the pandemic year ending early 2021 left out", size=12)
        beat(self,
             "And it has grown while the shops whose mistakes it sells have not. <bookmark mark='a'/> Since the year "
             f"ending early 2015, TJX's sales have grown {O['TJX'][2026]:.1f} times, Ross's {O['Ross'][2026]:.1f} times, "
             f"Burlington's {O['Burlington'][2026]:.1f} times. <bookmark mark='b'/> Over the same years Macy's sales fell to "
             f"{O[MAC][2026]:.2f} of what they were and Kohl's to {O[KOH][2026]:.2f}. Two things in this film "
             "press on the department store from either side: brands selling more in their own shops and on their own "
             "websites, and off-price shops selling the same brands for less.",
             base=[ch.frame, one, src], steps=[[ch.lines[k] for k in ("TJX", "Ross", "Burlington")] + [ch.labels[k] for k in ("TJX", "Ross", "Burlington")],
                                               [ch.lines[k] for k in ("Macy's", "Kohl's")] + [ch.labels[k] for k in ("Macy's", "Kohl's")]])

    def size(self):
        O = R["offprice"]["rev"]
        items = [(f"{k}, {'2015' if i == 0 else '2026'}", O[k][i], IDX_COL[k], f"${O[k][i]:.1f}bn") for k in ("TJX", "Macy's", "Kohl's")
                 for i in (0, 1)]
        rows = hbars(items, max_value=62, x0=-0.4, top=2.0, row=0.62, length=6.6, size=16, bar_h=0.36)
        lab = tx("net sales, fiscal years ending early in each year", 15, GREY_A).to_edge(UP, buff=0.5)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "In dollars. <bookmark mark='a'/> In the year ending early 2015, TJX sold "
             f"{O['TJX'][0]:.0f} billion dollars of goods; in the year ending January 2026, {O['TJX'][1]:.0f} billion. "
             f"<bookmark mark='b'/> Macy's went from {O[MAC][0]:.0f} billion to {O[MAC][1]:.0f}. "
             f"<bookmark mark='c'/> Kohl's from {O[KOH][0]:.0f} to {O[KOH][1]:.0f}. TJX now sells more than "
             "Macy's and Kohl's together.",
             base=[rows.axis, lab, src], steps=[rows[:2], rows[2:4], rows[4:]])

    def margin(self):
        O = R["offprice"]
        comp = {c["name"]: c for c in R["landscape"]["companies"]}
        items = [("TJX", comp["TJX"]["margin"], OFF, f"{100 * comp['TJX']['margin']:.1f}%"),
                 ("Ross", comp["Ross"]["margin"], OFF, f"{100 * comp['Ross']['margin']:.1f}%"),
                 ("Burlington", comp["Burlington"]["margin"], OFF, f"{100 * comp['Burlington']['margin']:.1f}%"),
                 ("Macy's", comp["Macy's"]["margin"], DEPT, f"{100 * comp[MAC]['margin']:.1f}%"),
                 ("Kohl's", comp["Kohl's"]["margin"], DEPT, f"{100 * comp[KOH]['margin']:.1f}%")]
        rows = hbars(items, max_value=0.1, x0=-0.4, top=1.8, row=0.7, length=6.0, size=17, bar_h=0.4)
        lab = tx("net income per dollar of sales, median of the last five fiscal years", 15, GREY_A).to_edge(UP, buff=0.7)
        note = tx(f"TJX keeps only {100 - O['cost']:.0f}c of each dollar after the goods and the shops, and still earns {O['pretax']}c before tax",
                  16, WHITE).move_to([0, -2.1, 0])
        src = source("Forms 10-K via SEC company facts; The TJX Companies, Inc., Form 10-K for fiscal 2026", size=12)
        beat(self,
             "The off-price shops do not make fat margins on each item. <bookmark mark='a'/> TJX has kept about "
             f"{100 * comp['TJX']['margin']:.0f} cents of each dollar as net income, Ross about "
             f"{100 * comp['Ross']['margin']:.0f}, Burlington less. <bookmark mark='b'/> Macy's and Kohl's, about "
             f"{100 * comp[MAC]['margin']:.0f} and {100 * comp[KOH]['margin']:.0f}. <bookmark mark='c'/> After "
             f"paying for its goods, its buyers and its shops, TJX has {100 - O['cost']:.0f} cents of each dollar left, and "
             f"still earns {O['pretax']} cents before tax: a thin margin, turned fast, on a very large and growing pile of "
             "other people's mistakes.",
             base=[rows.axis, lab, src], steps=[rows[:3], rows[3:], note])
