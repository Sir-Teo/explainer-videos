from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403

GCOL = {"Food services": "#F28B82", "Food processing": "#B58CFF", "Food retail": "#7EC8F5", "Food wholesale": "#5DA9E9",
        "Finance and insurance": "#8B95A7", "Transportation and storage": "#C9D3E0", "Livestock": MEAT,
        "Agribusiness": "#A47A4C", "Energy": "#F2A65A", "Advertising": "#E879F9", "Crops": CORN,
        "Legal and accounting": "#6F7A8C", "Forestry, fishing, and agricultural services": FARM}
GNAME = {"Food services": "restaurants and cafes", "Food processing": "food processing", "Food retail": "food shops",
         "Food wholesale": "wholesale", "Finance and insurance": "finance and insurance",
         "Transportation and storage": "transport and storage", "Livestock": "livestock farms",
         "Agribusiness": "agribusiness (seed, fertilizer...)", "Energy": "energy", "Advertising": "advertising",
         "Crops": "crop farms", "Legal and accounting": "legal and accounting",
         "Forestry, fishing, and agricultural services": "fishing and farm services"}


class Dollar(VoiceoverScene):
    def construct(self):
        card(self, 3, "Where the food dollar goes", "Of each dollar spent on food, who gets what?",
             "Chapter three. Where the food dollar goes.", lit=("dollar",))
        self.cents()
        self.channels()
        self.loaf()

    def cents(self):
        D = R["dollar"]
        g = D["groups"]
        # 100 cents, filled group by group (rounded to whole cents, largest remainders)
        raw = {k: v for k, v in g.items()}
        whole = {k: int(v) for k, v in raw.items()}
        rem = sorted(raw, key=lambda k: raw[k] - int(raw[k]), reverse=True)
        for k in rem[:100 - sum(whole.values())]:
            whole[k] += 1
        coins = VGroup(*[Circle(0.17, stroke_color="#2B2B2B", stroke_width=1, fill_color="#3A4558", fill_opacity=1)
                         for _ in range(100)]).arrange_in_grid(rows=10, cols=10, buff=0.06).move_to([-3.6, -0.3, 0])
        bill = draw.note_bill(2.4).move_to(coins)
        order = list(whole)
        idx = 0
        groups = []
        for k in order:
            groups.append((k, list(range(idx, idx + whole[k]))))
            idx += whole[k]
        legend = VGroup()
        for k, ids in groups:
            legend.add(VGroup(Square(0.2, stroke_width=0, fill_color=GCOL[k], fill_opacity=1),
                              tx(f"{GNAME[k]}: {raw[k]:.1f}", 15, WHITE)).arrange(RIGHT, buff=0.1))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.1, -0.3, 0])
        farmers = SurroundingRectangle(VGroup(legend[order.index("Livestock")], legend[order.index("Crops")]), color=FARM,
                                       buff=0.06)
        head = tx(f"A US food dollar, {D['year']}: cents, by who adds the value", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source(f"USDA ERS, Food Dollar Series (Ag-FEDS model, November 2026), {D['year']}, industry groups", size=13)
        with self.voiceover(
            f"Americans spent about {D['spend'] / 1000:.1f} trillion dollars on food in {D['year']}. "
            "<bookmark mark='a'/> Take one of those dollars and break it into a hundred cents. The Department of "
            "Agriculture's economists trace each cent back through the economy, to the industry whose work it pays "
            "for. <bookmark mark='b'/> The biggest slice by far, about a third, pays restaurants and cafes: the cooks, "
            "the waiters, the rent on the dining room. <bookmark mark='c'/> Then the food processors: millers, bakers, "
            "packers, canners. <bookmark mark='d'/> Then the shops that sell food, and the wholesalers behind them. "
            "<bookmark mark='e'/> Then a long tail: finance and insurance, trucks and warehouses, energy, advertising, "
            "lawyers and accountants. <bookmark mark='f'/> And the farms themselves? The work done on crop and "
            f"livestock farms accounts for about {g['Crops'] + g['Livestock']:.0f} cents of the dollar. Less than "
            "advertising and energy put together, plus finance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(bill, scale=0.8))
            vo.wait_until("a")
            self.play(FadeOut(bill), LaggedStart(*[FadeIn(c_, scale=0.5) for c_ in coins], lag_ratio=0.01), run_time=2.0)
            marks = "bcdeef"
            groups_by_mark = {"b": ["Food services"], "c": ["Food processing"], "d": ["Food retail", "Food wholesale"],
                              "e": ["Finance and insurance", "Transportation and storage", "Energy", "Advertising",
                                    "Legal and accounting", "Agribusiness", "Forestry, fishing, and agricultural services"],
                              "f": ["Livestock", "Crops"]}
            for m in "bcdef":
                vo.wait_until(m)
                anims = []
                for k in groups_by_mark[m]:
                    ids = dict(groups)[k]
                    anims += [coins[i].animate.set_fill(GCOL[k]) for i in ids]
                    anims.append(FadeIn(legend[order.index(k)], shift=LEFT * 0.1))
                self.play(*anims, run_time=1.2)
            self.play(Create(farmers))
            self.play(*[Indicate(coins[i], color=WHITE, scale_factor=1.3) for k in ("Livestock", "Crops")
                        for i in dict(groups)[k]])
        self.clear_scene()

    def channels(self):
        D = R["dollar"]
        S = D["series"]
        bag = VGroup(RoundedRectangle(corner_radius=0.08, width=1.4, height=1.6, stroke_width=0, fill_color="#C9A57A",
                                      fill_opacity=1),
                     Arc(radius=0.35, start_angle=0, angle=PI, stroke_color="#8A6E52", stroke_width=5).shift(UP * 0.85),
                     draw.loaf(0.8).shift(UP * 0.75 + LEFT * 0.2), draw.corn_plant(0.6).shift(UP * 0.55 + RIGHT * 0.35))
        plate = VGroup(Circle(0.8, stroke_color="#C9D3E0", stroke_width=4, fill_color="#E8EAED", fill_opacity=1),
                       Circle(0.55, stroke_color="#C9D3E0", stroke_width=2, fill_opacity=0),
                       Ellipse(width=0.7, height=0.35, stroke_width=0, fill_color=MEAT, fill_opacity=1).shift(LEFT * 0.1),
                       Ellipse(width=0.35, height=0.2, stroke_width=0, fill_color=FARM, fill_opacity=1).shift(RIGHT * 0.3 + UP * 0.15))
        bag.move_to([-4.6, 1.6, 0])
        plate.move_to([-4.6, -1.3, 0])
        lb = VGroup(tx("food from a shop", 18, WHITE, bold=True),
                    tx(f"farm share: {D['home']:.1f} cents", 22, FARM, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.05
                                                                                         ).next_to(bag, RIGHT, buff=0.35)
        lp = VGroup(tx("food at a restaurant", 18, WHITE, bold=True),
                    tx(f"farm share: {D['away']:.1f} cents", 22, FARM, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.05
                                                                                         ).next_to(plate, RIGHT, buff=0.35)
        ys = sorted(S["All"])
        pa = viz.plot_axes([2006.5, 2025.5], [0, 22], x_length=5.2, y_length=3.4, xticks=[2007, 2013, 2019, 2025],
                           yticks=[5, 10, 15, 20], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}c", size=13).move_to(
            [3.9, -0.2, 0])
        cols = {"All": PRICE, "Food-at-home": FARM, "Food-away-from-home": BRAND}
        lines = VGroup(*[VMobject(stroke_color=c, stroke_width=3).set_points_as_corners(
            [pa.ax.c2p(y, S[ch][y]) for y in ys if S[ch].get(y) is not None]) for ch, c in cols.items()])
        lk = VGroup(*[tx(n, 13, c) for n, c in (("all food", PRICE), ("at home", FARM), ("away from home", BRAND))]
                    ).arrange(RIGHT, buff=0.3).next_to(pa, UP, buff=0.12)
        pt = tx("the farm share, cents per food dollar", 15, GREY_A).next_to(lk, UP, buff=0.08)
        src = source("USDA ERS, Food Dollar Series (Ag-FEDS model), 2007-2025", size=13)
        with self.voiceover(
            "There is another way to count the farm's part: not the work done on farms, but the price farms are "
            f"paid for the food we eat. By that measure, the farm share was {D['farm']:.1f} cents of the dollar in "
            f"{D['year']}. <bookmark mark='a'/> It depends a great deal on where you eat. Of a dollar spent in a "
            f"grocery store, about {D['home']:.0f} cents reached farms. <bookmark mark='b'/> Of a dollar spent in a "
            f"restaurant, about {D['away']:.1f}: the rest pays for the kitchen and the service. <bookmark mark='c'/> "
            "Over time, the farm share moves with the price of crops. It rose in the price spikes of 2011 to 2014 and "
            "of 2022, and fell when prices fell. And as Americans spend more of their food money in restaurants, the "
            "overall share drifts down even if nothing else changes."
        ) as vo:
            self.play(FadeIn(src), FadeIn(bag), FadeIn(plate))
            vo.wait_until("a")
            self.play(FadeIn(lb, shift=LEFT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(lp, shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(pa), FadeIn(pt), FadeIn(lk))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), run_time=3.0)
        self.clear_scene()

    def loaf(self):
        B = R["bread"]
        bread = draw.loaf(3.6).move_to([-3.6, 0.3, 0])
        wheat_cut = draw.loaf(3.6).move_to(bread)
        frac = B["wheat_loaf"] / B["bread"]
        full = Rectangle(width=4.2, height=0.45, stroke_color=GREY_B, stroke_width=1.5, fill_color="#3A4558",
                         fill_opacity=1).next_to(bread, DOWN, buff=0.5)
        part = Rectangle(width=4.2 * frac, height=0.45, stroke_width=0, fill_color=WHEATC, fill_opacity=1).align_to(
            full, LEFT).align_to(full, DOWN)
        bar_l = VGroup(tx(f"the loaf's price, ${B['bread']:.2f}", 15, GREY_A).next_to(full, DOWN, buff=0.1),
                       tx("the wheat", 15, WHEATC, bold=True).next_to(part, UP, buff=0.08).align_to(full, LEFT))
        slice_ = VGroup(full, part, bar_l)
        del wheat_cut
        sheaf = VGroup(*[draw.wheat(1.4, dwarf=True) for _ in range(5)]).arrange(RIGHT, buff=0.05).move_to([-3.6, 2.4, 0])
        nums = VGroup(tx("a 60-pound bushel of wheat", 18, WHITE), tx(f"→ {B['flour']:.0f} pounds of white flour", 18, WHITE),
                      tx(f"→ about {B['loaves']:.0f} one-pound loaves", 18, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08
                                                                                          ).move_to([3.4, 2.2, 0])
        math_ = VGroup(tx(f"wheat, {mlabel(B['month'])}: ${B['wheat_bu']:.2f} a bushel", 18, WHEATC),
                       tx(f"wheat in one loaf: {100 * B['wheat_loaf']:.1f} cents", 22, WHEATC, bold=True),
                       tx(f"the loaf, average US price: ${B['bread']:.2f}", 22, WHITE, bold=True),
                       tx(f"the wheat is {100 * B['share']:.0f}% of the price", 22, PRICE, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, -0.6, 0])
        note = tx("(world wheat price; the farmer gets less, after freight and handling)", 13, GREY_B).next_to(math_, DOWN,
                                                                                                         buff=0.15)
        src = source("Kansas Wheat (flour and loaves per bushel); IMF wheat price and BLS average price of white bread "
                     "via FRED", size=13)
        with self.voiceover(
            "Here is the same arithmetic for one familiar thing: a loaf of white bread. <bookmark mark='a'/> According "
            f"to Kansas's wheat commission, a sixty-pound bushel of wheat makes about {B['flour']:.0f} pounds of white "
            f"flour, enough for about {B['loaves']:.0f} one-pound loaves. <bookmark mark='b'/> In {mlabel(B['month'])}, "
            f"wheat sold for about {say_money(B['wheat_bu'])} a bushel on the world market, so the wheat in one loaf "
            f"cost about {100 * B['wheat_loaf']:.0f} cents. <bookmark mark='c'/> The average loaf of white bread in an "
            f"American shop cost {say_money(B['bread'])}. The wheat is about {100 * B['share']:.0f} percent of the "
            "price. Even when wheat spiked in 2022, after the invasion of Ukraine, it never reached "
            f"{100 * B['peak_share'] + 1:.0f} percent. The rest is milling, baking, packaging, trucking, the shop, and "
            "the brand on the bag. Double the price of wheat, and a loaf would cost you about ten cents more."
        ) as vo:
            self.play(FadeIn(src), FadeIn(sheaf, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(bread, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(math_[0]), FadeIn(math_[1]))
            self.play(FadeIn(full), FadeIn(bar_l[0]))
            self.play(GrowFromEdge(part, LEFT), FadeIn(bar_l[1]), Flash(part, color=WHEATC))
            vo.wait_until("c")
            self.play(FadeIn(math_[2:]), FadeIn(note))
        self.clear_scene()
