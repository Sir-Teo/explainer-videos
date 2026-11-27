from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class Inputs(VoiceoverScene):
    def construct(self):
        card(self, 5, "Seed, fertilizer and machines", "Who sells to the farmer, and how do they fare?",
             "Chapter five. Seed, fertilizer and machines.", lit=("moat", "dollar"))
        self.squeeze()
        self.costs()
        self.margins()

    def squeeze(self):
        farms = VGroup(*[draw.house(0.22, color=FARM) for _ in range(60)]).arrange_in_grid(rows=6, cols=10, buff=0.07)
        farms.move_to([0, -0.1, 0])
        fl = VGroup(tx(f"{R['treadmill']['farms_2025']:.2f} million farms", 20, FARM, bold=True),
                    tx("each one a price taker", 15, GREY_A)).arrange(DOWN, buff=0.04).next_to(farms, DOWN, buff=0.25)
        sellers = [("seed and chemicals", "Corteva, Bayer, Syngenta", COST), ("fertilizer", "Nutrien, CF, Mosaic, Yara", "#5DA9E9"),
                   ("machinery", "Deere, CNH, AGCO, Kubota", "#3FA34D")]
        buyers = [("grain", "ADM, Bunge, Cargill, Louis Dreyfus", TRADE), ("meat", "Tyson, JBS, Cargill, National Beef", MEAT),
                  ("food makers", "PepsiCo, General Mills, Kraft Heinz", BRAND)]

        def column(items, x):
            g = VGroup()
            for k, (what, who, col) in enumerate(items):
                c = draw.castle(1.1, color=col).scale(0.75)
                t = VGroup(tx(what, 16, col, bold=True), tx(who, 12, GREY_A)).arrange(DOWN, buff=0.03)
                g.add(VGroup(c, t).arrange(DOWN, buff=0.08))
            g.arrange(DOWN, buff=0.35).move_to([x, -0.1, 0])
            return g
        left = column(sellers, -5.2)
        right = column(buyers, 5.2)
        lh = tx("they sell to farmers", 17, WHITE, bold=True).next_to(left, UP, buff=0.2)
        rh = tx("they buy from farmers", 17, WHITE, bold=True).next_to(right, UP, buff=0.2)
        arrows = VGroup(*[Arrow(c.get_right(), farms.get_left() + UP * (0.7 - 0.7 * k), buff=0.15, stroke_width=2.5,
                                color=GREY_B, tip_length=0.14) for k, c in enumerate(left)],
                        *[Arrow(farms.get_right() + UP * (0.7 - 0.7 * k), c.get_left(), buff=0.15, stroke_width=2.5,
                                color=GREY_B, tip_length=0.14) for k, c in enumerate(right)])
        src = source("company names: the companies' own filings and reports; farm count: USDA NASS (2025)", size=13)
        with self.voiceover(
            "Here is the shape of the business that surrounds the farm. <bookmark mark='a'/> In the middle, almost "
            f"{R['treadmill']['farms_2025']:.1f} million American farms. None of them can change the price of corn by "
            "growing more or less: each is far too small. Economists call that a price taker. "
            "<bookmark mark='b'/> On one side, the companies that sell to farmers. Seed and crop chemicals: Corteva, "
            "Bayer, which bought Monsanto, and Syngenta, owned by a Chinese state company. Fertilizer: Nutrien, CF "
            "Industries, Mosaic, Yara. Machinery: Deere, CNH, AGCO and Kubota. A handful of names in each. "
            "<bookmark mark='c'/> On the other side, the companies that buy from farmers: the grain traders, the meat "
            "packers, the food manufacturers. Again, a handful of names. The farmer buys from a few, and sells to a few, "
            "and is one of very many. That is the second clue."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(f, scale=0.6) for f in farms], lag_ratio=0.01), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(lh), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in left], lag_ratio=0.4), run_time=2.0)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows[:3]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(rh), LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in right], lag_ratio=0.4), run_time=2.0)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows[3:]], lag_ratio=0.2))
        self.clear_scene()

    def costs(self):
        I = R["inputs"]
        ys = sorted(I["fert"])
        pa = viz.plot_axes([1995.5, 2025.5], [0, 250], x_length=5.6, y_length=3.6, xticks=[1996, 2005, 2015, 2025],
                           yticks=[50, 100, 150, 200, 250], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=13
                           ).move_to([-3.4, -0.3, 0])
        fl = VMobject(stroke_color="#5DA9E9", stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, I["fert"][y]) for y in ys])
        sl = VMobject(stroke_color=COST, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, I["seed"][y]) for y in ys])
        lk = VGroup(tx(f"fertilizer: ${I['fert'][1996]:.0f} → ${I['fert'][2025]:.0f}", 15, "#5DA9E9"),
                    tx(f"seed: ${I['seed'][1996]:.0f} → ${I['seed'][2025]:.0f}", 15, COST)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                   buff=0.05)
        lk.next_to(pa, UP, buff=0.12).align_to(pa, LEFT)
        pt = tx("per acre of US corn, dollars", 14, GREY_A).next_to(lk, UP, buff=0.06).align_to(pa, LEFT)
        cf = I["cf"]
        cy = sorted(cf)
        pb = viz.plot_axes([2014.4, 2025.6], [-1, 12], x_length=5.4, y_length=3.6, xticks=[2015, 2018, 2022, 2025],
                           yticks=[0, 4, 8, 12], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=13).move_to(
            [3.6, -0.3, 0])
        rb = VGroup()
        nb = VGroup()
        for y in cy:
            rv, ni = cf[y]
            p0, p1 = pb.ax.c2p(y - 0.18, 0), pb.ax.c2p(y - 0.18, rv)
            rb.add(Rectangle(width=0.32, height=p1[1] - p0[1], stroke_width=0, fill_color="#5DA9E9", fill_opacity=0.8).move_to(
                [p0[0], (p0[1] + p1[1]) / 2, 0]))
            q0, q1 = pb.ax.c2p(y + 0.18, 0), pb.ax.c2p(y + 0.18, ni)
            nb.add(Rectangle(width=0.32, height=max(abs(q1[1] - q0[1]), 0.01), stroke_width=0,
                             fill_color=GREEN_C if ni >= 0 else STATE, fill_opacity=0.9).move_to([q0[0], (q0[1] + q1[1]) / 2, 0]))
        ck = VGroup(tx("CF Industries, the largest US nitrogen maker", 15, WHITE, bold=True),
                    tx("revenue (blue) and profit (green)", 13, GREY_A)).arrange(DOWN, buff=0.03).next_to(pb, UP, buff=0.12)
        spike = VGroup(tx(f"2022: ${cf[2022][0]:.1f}bn revenue,", 14, WHITE), tx(f"${cf[2022][1]:.2f}bn profit", 14, GREEN_C)
                       ).arrange(DOWN, buff=0.02).next_to(pb.ax.c2p(2022, cf[2022][0]), LEFT, buff=0.15)
        src = source("USDA ERS costs and returns (corn); SEC EDGAR, CF Industries Forms 10-K", size=13)
        with self.voiceover(
            "Watch what the sellers have done with their side. <bookmark mark='a'/> In 1996, the seed for an acre of "
            f"American corn cost about {I['seed'][1996]:.0f} dollars. In 2025, about {I['seed'][2025]:.0f}: more than "
            "four times as much, as companies sold hybrids with patented genetic traits that resist insects and weed "
            "killers. Farmers paid it because the seed yields more. <bookmark mark='b'/> Fertilizer cost about "
            f"{I['fert'][1996]:.0f} dollars an acre in 1996. In 2022 it reached {I['fert'][2022]:.0f}, as the price "
            "of natural gas, from which nitrogen fertilizer is made, soared and the invasion of Ukraine disrupted "
            "supplies. "
            "<bookmark mark='c'/> Here is the other side of that bill. CF Industries, America's largest maker of "
            f"nitrogen fertilizer, had revenue of about {cf[2020][0]:.0f} billion dollars and a profit of "
            f"{1000 * cf[2020][1]:.0f} million in 2020. <bookmark mark='d'/> In 2022: revenue of "
            f"{cf[2022][0]:.0f} billion, and a profit of {cf[2022][1]:.1f} billion, ten times as much. The farmer's "
            "worst year for costs was the fertilizer maker's best year ever."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(pt), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(sl), FadeIn(lk[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(fl), FadeIn(lk[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(pb), FadeIn(ck))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(a, DOWN), GrowFromEdge(b, DOWN if cf[y][1] >= 0 else UP))
                                    for a, b, y in zip(rb[:6], nb[:6], cy[:6])], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(a, DOWN), GrowFromEdge(b, DOWN if cf[y][1] >= 0 else UP))
                                    for a, b, y in zip(rb[6:], nb[6:], cy[6:])], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(spike))
        self.clear_scene()

    def margins(self):
        C = R["chain"]
        sel = [c for c in C["companies"] if c["ticker"] in ("CF", "DE", "MOS", "CTVA")]
        rows = [("growing corn (USDA's accounts)", C["corn5"], CORN)] + [(f"{c['name']} ({c['what']})", c["margin5"], COST)
                                                                          for c in sorted(sel, key=lambda q: q["margin5"])]
        bars = VGroup()
        for i, (n, m, col) in enumerate(rows):
            w = 7.0 * m / 0.22
            b = Rectangle(width=max(w, 0.02), height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                [-1.4, 1.5 - 0.8 * i, 0], aligned_edge=LEFT)
            bars.add(VGroup(b, tx(n, 17, WHITE).next_to(b, LEFT, buff=0.2).align_to([-1.6, 0, 0], RIGHT),
                            tx(f"{100 * m:.1f}%", 18, WHITE, bold=True).next_to(b, RIGHT, buff=0.12)))
        for b in bars:
            b[1].next_to([-1.55, b[0].get_center()[1], 0], LEFT, buff=0)
        head = tx("Profit as a share of sales, average 2021-2025", 22, WHITE, bold=True).to_edge(UP, buff=0.45)
        note = VGroup(tx("Not quite like for like: USDA charges the farm for the family's land and work at market rates,", 14,
                         GREY_B),
                      tx("so its 'profit' is what is left after paying the owners a normal return.", 14, GREY_B)
                      ).arrange(DOWN, buff=0.04).to_edge(DOWN, buff=0.75)
        src = source("SEC EDGAR, Forms 10-K (net income over revenue); USDA ERS costs and returns, corn, 2021-2025", size=13)
        with self.voiceover(
            "Put the five years from 2021 to 2025 side by side, as profit kept from each dollar of sales. "
            "<bookmark mark='a'/> Growing corn, by the Department of Agriculture's accounts, kept about "
            f"{100 * C['corn5']:.0f} cents on the dollar over those five years, and that includes the boom years of "
            f"2021 and 2022. <bookmark mark='b'/> The seed and chemical maker, Corteva, about "
            f"{100 * [c for c in sel if c['ticker'] == 'CTVA'][0]['margin5']:.0f}. Mosaic, about "
            f"{100 * [c for c in sel if c['ticker'] == 'MOS'][0]['margin5']:.0f}. Deere, about "
            f"{100 * [c for c in sel if c['ticker'] == 'DE'][0]['margin5']:.0f}, and CF Industries, about "
            f"{100 * [c for c in sel if c['ticker'] == 'CF'][0]['margin5']:.0f}. <bookmark mark='c'/> The comparison is "
            "not perfectly fair, because the farm's accounts pay its owners a normal return on their land and labour "
            "before counting profit. But the pattern is the treadmill's: the farmer's gains are competed away, while "
            "the companies with patents, brands and scale keep theirs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1:]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], LEFT), FadeIn(b[1:])) for b in bars[1:]],
                                  lag_ratio=0.5), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.clear_scene()
