from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: thirty years as a shipowner",
             "A ship ordered today arrives in three years. When do you order?",
             "Chapter one. Run it. You own ships in the Works. A ship takes three years from order to delivery and lasts "
             "twenty-five. You have thirty years and one decision, made again and again: when to order.", lit=("make", "change"))
        self.curve()
        self.market()
        self.herd()
        self.rules()
        self.prices()
        self.payoff()
        self.lesson()

    def curve(self):
        U = R["run"]
        pts = {100 * k: v for k, v in U["curve"].items()}
        ch = line_chart({"a ship's earnings a day": (pts, RATE)}, x=(70, 100), y=(0, 110), xticks=[70, 80, 90, 100],
                        yticks=[0, 25, 50, 75, 100], xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: f"${v:.0f}k",
                        ylabel="the Works: what a ship earns a day, by how much of the world's fleet is busy", width=9.0,
                        height=4.2, center=(-1.0, -0.45), label_end=False)
        be = DashedLine(ch.ax.c2p(70, U["breakeven"]), ch.ax.c2p(100, U["breakeven"]), stroke_color=GOOD, stroke_width=2)
        bel = tx(f"${U['breakeven']:.0f}k a day: running cost and the ship's capital", 14, GOOD).next_to(ch.ax.c2p(72, U["breakeven"]), UP, buff=0.1, aligned_edge=LEFT)
        m1 = marker(ch.ax, 90, R["run"]["curve"][0.9], f"90% busy: ${R['run']['curve'][0.9]:.0f}k", RATE, side=LEFT)
        m2 = marker(ch.ax, 100, U["top"], f"all busy: ${U['top']:.0f}k", BAD, side=LEFT)
        vessel = draw.ship(1.8).move_to([5.4, 1.6, 0])
        tag = estimate_tag("the Works: an illustrative freight market", size=12)
        beat(self,
             "First, how freight is priced. <bookmark mark='a'/> When there are more ships than cargo, owners compete for "
             f"every load and a ship earns barely its running costs, about {U['floor']:.0f} thousand dollars a day. "
             f"<bookmark mark='b'/> A ship needs about {U['breakeven']:.0f} thousand a day to pay for itself. "
             "<bookmark mark='c'/> As the fleet fills, earnings rise slowly, <bookmark mark='d'/> then explode: when every "
             f"ship is busy, a cargo owner will pay {U['top']:.0f} thousand dollars a day for the last one. Ships cannot be "
             "made quickly, so the price of the last one has no ceiling but what the cargo can bear.",
             base=[ch.frame, vessel, tag], steps=[ch.lines["a ship's earnings a day"], [be, bel], m1, m2])

    def market(self):
        U = R["run"]["path"]
        e = {i: v for i, v in enumerate(U["earn"])}
        ch = line_chart({"earnings a day": (e, RATE)}, x=(0, 29), y=(0, 110), xticks=[0, 5, 10, 15, 20, 25, 29],
                        yticks=[0, 25, 50, 75, 100], xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"${v:.0f}k",
                        ylabel="the Works: what a ship earns a day, thirty years", width=9.6, height=4.2, center=(-0.6, -0.45),
                        label_end=False)
        be = DashedLine(ch.ax.c2p(0, R["run"]["breakeven"]), ch.ax.c2p(29, R["run"]["breakeven"]), stroke_color=GOOD, stroke_width=2)
        booms = [i for i in range(0, 29) if U["earn"][i] >= 90 and (i == 0 or U["earn"][i - 1] < 90)]
        ms = VGroup(*[marker(ch.ax, i, U["earn"][i], f"boom, year {i}", BAD, side=RIGHT if i == 0 else LEFT) for i in booms])
        tag = estimate_tag("the Works: demand grows 3% a year with shocks; ships arrive three years after they are ordered", size=12)
        beat(self,
             "Now thirty years of it. Demand for shipping grows about three per cent a year, with good and bad years. "
             "<bookmark mark='a'/> Earnings spend most of the time near the floor, <bookmark mark='b'/> and every few years "
             f"they spike: here at the start, and in years {booms[1]} and {booms[2]}. Most of the money a shipowner "
             "ever makes is made in a few short booms.",
             base=[ch.frame, be, tag], steps=[ch.lines["earnings a day"], ms])

    def herd(self):
        U = R["run"]["path"]
        o = {i: v for i, v in enumerate(U["orders"])}
        f = {i: v for i, v in enumerate(U["fleet"])}
        d = {i: v for i, v in enumerate(U["demand"])}
        ch = line_chart({"fleet": (f, SHIP), "cargo to carry": (d, BOX)}, x=(0, 29), y=(0, 420),
                        xticks=[0, 5, 10, 15, 20, 25, 29], yticks=[0, 100, 200, 300, 400], xfmt=lambda v: f"year {int(v)}",
                        yfmt=lambda v: f"{v:.0f}", ylabel="the Works: ships, and the cargo that needs them (ship-equivalents)",
                        width=9.6, height=4.2, center=(-1.0, -0.45))
        bars = VGroup(*[Rectangle(width=0.18, height=max(0.02, 0.022 * o[i]), stroke_width=0, fill_color=BAD, fill_opacity=0.7).move_to(
            ch.ax.c2p(i, 0), aligned_edge=DOWN) for i in range(30)])
        bl = tx("ships ordered each year", 14, BAD).next_to(bars, UP, buff=0.05).align_to(bars, RIGHT)
        tag = estimate_tag("the Works: the industry orders in proportion to today's profit", size=12)
        src = source("Greenwood and Hanson, 'Waves in Ship Prices and Investment', NBER Working Paper 19246", size=12)
        beat(self,
             "Why the booms end. <bookmark mark='a'/> Every owner sees the same high rates at the same moment, and orders "
             "ships at the same moment. <bookmark mark='b'/> Three years later they all arrive together, the fleet jumps, "
             "and the cargo they were ordered for has to be shared among far more ships. The boom builds the bust. The "
             "economists Robin Greenwood and Samuel Hanson found this pattern in real ship prices: when earnings are high, "
             "ship prices and orders rise, and the returns that follow are low.",
             base=[ch.frame, tag, src], steps=[[bars, bl], [ch.lines["fleet"], ch.labels["fleet"], ch.lines["cargo to carry"], ch.labels["cargo to carry"]]])

    def rules(self):
        U = R["run"]
        e = {i: v for i, v in enumerate(U["path"]["earn"])}
        ch = line_chart({"earnings a day": (e, ALL)}, x=(0, 29), y=(0, 110), xticks=[0, 5, 10, 15, 20, 25, 29],
                        yticks=[0, 25, 50, 75, 100], xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"${v:.0f}k",
                        ylabel="the Works: when each owner ordered", width=9.6, height=4.2, center=(-0.6, -0.45), label_end=False)
        fo = VGroup(*[Triangle(fill_color=BAD, fill_opacity=1, stroke_width=0).scale(0.12).move_to(ch.ax.c2p(s["order"], e[s["order"]]))
                      for s in U["follow"]["ships"]])
        ag = VGroup(*[Triangle(fill_color=GOOD, fill_opacity=1, stroke_width=0).scale(0.12).move_to(ch.ax.c2p(s["order"], e[s["order"]]))
                      for s in U["against"]["ships"]])
        lf = tx(f"follow the market: order when earnings top $40k ({len(U['follow']['ships'])} ships)", 15, BAD, bold=True).to_edge(UP, buff=0.55)
        la = tx(f"go against it: order when they are below $18k ({len(U['against']['ships'])} ships)", 15, GOOD, bold=True).next_to(lf, DOWN, buff=0.1)
        tag = estimate_tag("the Works: at most one order every three years", size=12)
        beat(self,
             "So, two owners, two rules. <bookmark mark='a'/> The first follows the market: it orders a ship whenever "
             "earnings are high, as everyone else does. <bookmark mark='b'/> The second goes against it: it orders only when "
             "earnings are low and the yards are hungry for work. Each orders at most one ship every three years.",
             base=[ch.frame, ch.lines["earnings a day"], tag], steps=[[lf, fo], [la, ag]])

    def prices(self):
        U = R["run"]
        pr = {i: v for i, v in enumerate(U["path"]["price"])}
        ch = line_chart({"price of a new ship": (pr, SHIP)}, x=(0, 29), y=(40, 130), xticks=[0, 5, 10, 15, 20, 25, 29],
                        yticks=[50, 75, 100, 125], xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"${v:.0f}m",
                        ylabel="the Works: what a new ship costs, by year", width=9.6, height=4.2, center=(-0.6, -0.45), label_end=False)
        lo, hi = min(pr.values()), max(pr.values())
        khi = max(pr, key=pr.get)
        m = marker(ch.ax, khi, hi, f"year {khi}: ${hi:.0f}m", BAD, side=RIGHT if khi < 3 else UP)
        tag = estimate_tag("the Works: shipyards price new ships off today's earnings", size=12)
        beat(self,
             "And the price of the ship moves with the market too. <bookmark mark='a'/> Shipyards and sellers of second-hand "
             f"ships know what a ship earns today, so a new one costs about {hi:.0f} million dollars in a boom and "
             f"{lo:.0f} million in a bust. <bookmark mark='b'/> Following the market means paying the most for a ship at "
             "the very moment its future earnings are about to fall.",
             base=[ch.frame, tag], steps=[ch.lines["price of a new ship"], m])

    def payoff(self):
        U = R["run"]
        f, a = U["follow"], U["against"]
        rows = table([["", "follow the market", "go against it"],
                      ["ships ordered", f"{len(f['ships'])}", f"{len(a['ships'])}"],
                      ["average price paid", f"${f['avg_price']:.0f}m", f"${a['avg_price']:.0f}m"],
                      ["earnings a day when they arrived", f"${f['avg_earn_at_delivery']:.0f}k", f"${a['avg_earn_at_delivery']:.0f}k"],
                      ["money back over money spent", f"{100 * f['ret']:+.0f}%", f"{100 * a['ret']:+.0f}%"]],
                     col_x=[-6.0, -0.6, 3.0], top=1.8, row_h=0.7, size=19, colors=[None] + [[WHITE, BAD, GOOD]] * 4)
        tag = estimate_tag("the Works: earnings less running costs to year thirty, plus what is left of each ship at that year's price", size=12)
        beat(self,
             "Here is how they did. <bookmark mark='a'/> The owner who followed the market ordered "
             f"{len(f['ships'])} ships, <bookmark mark='b'/> at an average of {f['avg_price']:.0f} million dollars each, "
             "because a ship ordered in a boom is priced in a boom. <bookmark mark='c'/> They arrived to earnings of about "
             f"{f['avg_earn_at_delivery']:.0f} thousand dollars a day. <bookmark mark='d'/> Over the thirty years it got back "
             f"{100 * f['ret']:.0f} per cent more than it spent. The contrarian paid {a['avg_price']:.0f} million a ship, "
             f"and got back {100 * a['ret']:.0f} per cent more.",
             base=[rows[0], tag], steps=[rows[1], rows[2], rows[3], rows[4]])

    def lesson(self):
        g = VGroup(tx("Why it is hard to be the contrarian", 22, WHITE, bold=True),
                   tx("in a bust the bank will not lend, and the old ships are losing money", 18, BAD),
                   tx("in a boom every rival is ordering, and customers want ships now", 18, RATE),
                   tx("the delay hides the cause: the bust arrives three years after the orders", 18, SHIP)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.3, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "If the answer is so plain, why does anyone follow the market? In this series' reading, <bookmark mark='a'/> "
             "because in a bust the banks will not lend and the ships you already own are losing money; <bookmark mark='b'/> "
             "in a boom every rival is ordering and your customers want ships now; <bookmark mark='c'/> and the three years "
             "between order and delivery hide the cause from the effect. The rest of this film shows the real cycle, which "
             "is just as violent.",
             base=[tag], steps=[g[:2], g[2], g[3]])
