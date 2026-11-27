from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Specialty(VoiceoverScene):
    def construct(self):
        card(self, 8, "Sold by performance", "Why does a can of paint earn more than the plant that made its ingredients?",
             "Chapter eight. Sold by performance.", lit=("moat", "dollar"))
        self.can()
        self.dollar()
        self.prices()
        self.margins()

    def can(self):
        can = draw.paint_can(3.0).move_to([0.0, -0.7, 0])
        ings = [("resins and latex", PLASTIC, "the film that binds"), ("pigments", SPEC, "the colour and cover"),
                ("additives", GASES, "flow, drying, mildew"), ("solvents", OIL, "water or spirits to carry it"),
                ("the can", GREY_B, "metal or plastic")]
        tags = VGroup()
        for i, (n_, c, d) in enumerate(ings):
            side = -1 if i % 2 == 0 else 1
            y = 1.9 - 0.95 * (i // 2) - (0.45 if side > 0 else 0)
            t = VGroup(tx(n_, 18, c, bold=True), tx(d, 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT if side > 0 else RIGHT, buff=0.04)
            t.move_to([side * 3.9, y, 0])
            tags.add(VGroup(t, Arrow(t.get_right() if side < 0 else t.get_left(), can.get_center() + np.array([side * 0.6, 0.3, 0]),
                                     buff=0.15, stroke_width=2, color=c, max_tip_length_to_length_ratio=0.12)))
        quote = VGroup(tx("'A significant portion of these raw materials are derived from various", 15, WHITE),
                       tx("upstream petrochemical and related commodity feedstocks, notably propylene.'", 15, WHITE),
                       tx("Sherwin-Williams, Form 10-K 2025", 13, GREY_B)).arrange(DOWN, buff=0.05).to_edge(DOWN, buff=0.5)
        store = draw.shop(1.4).move_to([5.2, -2.0, 0]) if hasattr(draw, "shop") else VGroup()
        stl = tx(f"{get('shw.stores.2025'):,.0f} Sherwin-Williams stores", 15, PRICE, bold=True).next_to(store, UP, buff=0.1)
        with self.voiceover(
            "At the far end of the tree are the chemicals sold not by the tonne but by what they do. Take a can of "
            "paint. <bookmark mark='a'/> Inside, by Sherwin-Williams' own description: resins and latex, which form "
            "the film; pigments for colour; additives; solvents, often water; and the can. <bookmark mark='b'/> And "
            "much of it, the company says, comes from petrochemicals, notably propylene, straight from the crackers "
            "of chapter three. <bookmark mark='c'/> But you do not buy paint from a cracker. Sherwin-Williams sells "
            f"it through {get('shw.stores.2025'):,.0f} stores of its own in America, Canada and the Caribbean, to "
            "painting contractors and to people doing up their homes, tinted to order."
        ) as vo:
            self.play(FadeIn(can, scale=0.9))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t_[0], shift=RIGHT * 0.2 * (1 if i % 2 else -1)) for i, t_ in enumerate(tags)], lag_ratio=0.25),
                      LaggedStart(*[GrowArrow(t_[1]) for t_ in tags], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(quote, shift=UP * 0.1), Indicate(tags[0][0], color=PLASTIC))
            vo.wait_until("c")
            self.play(FadeOut(quote), FadeIn(store, shift=LEFT * 0.2), FadeIn(stl))
        self.clear_scene()

    def dollar(self):
        dow_gm = 1 - get("dow.cogs.2025") / get("dow.sales.2025")
        shw_gm = get("shw.gross.2025") / 100
        bars = VGroup()
        for i, (name, gm, col) in enumerate((("Dow", dow_gm, ETHYL), ("Sherwin-Williams", shw_gm, PRICE))):
            x = -3.2 + 6.4 * i
            h = 4.4
            base = -2.6
            cost = Rectangle(width=1.8, height=h * (1 - gm), stroke_width=0, fill_color=GREY_D, fill_opacity=0.95).move_to(
                [x, base, 0], aligned_edge=DOWN)
            gp = Rectangle(width=1.8, height=h * gm, stroke_width=0, fill_color=col, fill_opacity=0.9).next_to(cost, UP, buff=0)
            cl = tx(f"cost of sales: {100 * (1 - gm):.0f}¢", 16, GREY_A).next_to(cost, LEFT if i == 0 else RIGHT, buff=0.2)
            gl = tx(f"left over: {100 * gm:.0f}¢", 20, col, bold=True).next_to(gp, LEFT if i == 0 else RIGHT, buff=0.2)
            nm = tx(name, 22, col, bold=True).next_to(cost, DOWN, buff=0.2)
            bars.add(VGroup(cost, gp, cl, gl, nm))
        head = tx("A dollar of sales in 2025, and what was left after the cost of making it", 21, WHITE, bold=True).to_edge(UP, buff=0.35)
        note = tx("left over pays for selling, research, overheads, interest, tax and profit", 14, GREY_A).next_to(head, DOWN, buff=0.12)
        src = source("Dow Inc. and Sherwin-Williams, Forms 10-K 2025 (net sales, cost of sales; gross profit)", size=13)
        with self.voiceover(
            "Here is the difference that makes, in one dollar of sales. <bookmark mark='a'/> When Dow sold a dollar of "
            "chemicals and plastics in 2025, the materials, energy and running of its plants cost it about "
            f"{100 * (1 - dow_gm):.0f} cents, leaving {100 * dow_gm:.0f} cents for everything else. <bookmark mark='b'/> "
            f"When Sherwin-Williams sold a dollar of paint, about {100 * shw_gm:.0f} cents were left after the cost of "
            "making it. <bookmark mark='c'/> Out of that it pays for its stores, its salespeople and its brand. The "
            "customer is paying for colour, service and a name a painter trusts, not for tonnes of chemicals."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note), FadeIn(src))
            for m_, b_ in zip("ab", bars):
                vo.wait_until(m_)
                self.play(GrowFromEdge(b_[0], DOWN), FadeIn(b_[4]), FadeIn(b_[2]), run_time=1.0)
                self.play(GrowFromEdge(b_[1], DOWN), FadeIn(b_[3]), run_time=1.0)
            vo.wait_until("c")
            self.play(Indicate(bars[1][1], color=PRICE, scale_factor=1.05))
        self.clear_scene()

    def prices(self):
        S_ = R["specialty"]
        pt, pp = S_["ppi_paint"], S_["ppi_petro"]
        ys = sorted(y for y in pt if y in pp)
        a = {y: 100 * pt[y] / pt[ys[0]] for y in ys}
        b = {y: 100 * pp[y] / pp[ys[0]] for y in ys}
        pa = viz.plot_axes([ys[0] - 0.5, ys[-1] + 0.5], [0, 260], x_length=9.0, y_length=4.4,
                           xticks=[2005, 2010, 2015, 2020, 2025], yticks=[65, 130, 195, 260], xfmt=lambda v: f"{int(v)}",
                           yfmt=lambda v: f"{v:.0f}", ylabel=f"producer price index, {ys[0]} = 100", size=14).move_to([-1.4, -0.4, 0])
        la = VMobject(stroke_color=PRICE, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, a[y]) for y in ys])
        lb = VMobject(stroke_color=ETHYL, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, b[y]) for y in ys])
        fa = sum(1 for u, v in zip(ys, ys[1:]) if a[v] < a[u])
        fb = sum(1 for u, v in zip(ys, ys[1:]) if b[v] < b[u])
        key = VGroup(tx(f"paints and coatings: fell in {fa} of {len(ys) - 1} years", 16, PRICE, bold=True),
                     tx(f"petrochemicals: fell in {fb} of {len(ys) - 1} years", 16, ETHYL, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 1.8, 0])
        head = tx("What American makers charged: paint against petrochemicals", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("US Bureau of Labor Statistics, PPIs for paint and coating, and petrochemical, manufacturing, via FRED", size=13)
        with self.voiceover(
            "And when the price of its ingredients falls, a paint maker does not have to pass it on. "
            f"<bookmark mark='a'/> Petrochemical prices since {ys[0]}: falling in {fb} of the {len(ys) - 1} years. "
            f"<bookmark mark='b'/> Paint: falling in {fa}. When oil and propylene jump, paint prices follow them up; "
            "when they fall, paint mostly stays where it is, and the difference becomes margin."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lb), FadeIn(key[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(la), FadeIn(key[0]), run_time=2.5)
        self.clear_scene()

    def margins(self):
        land = {c["ticker"]: c for c in R["landscape"]["companies"]}
        names = {"SHW": "Sherwin-Williams", "ECL": "Ecolab", "PPG": "PPG", "IFF": "IFF", "DOW": "Dow", "LYB": "LyondellBasell"}
        order = ["SHW", "ECL", "PPG", "LYB", "DOW", "IFF"]
        rows = VGroup()
        for i, t in enumerate(order):
            c = land[t]
            m = c["margin5"]
            col = PRICE if land[t]["group"] == "specialty" else ETHYL
            y = 2.0 - 0.72 * i
            w = abs(m) * 30
            bar = Rectangle(width=max(w, 0.02), height=0.42, stroke_width=0, fill_color=col if m >= 0 else BAD, fill_opacity=0.9)
            bar.move_to([-0.4, y, 0], aligned_edge=LEFT if m >= 0 else RIGHT)
            nm = tx(names[t], 17, WHITE).move_to([-2.6, y, 0], aligned_edge=RIGHT) if m >= 0 else tx(names[t], 17, WHITE).next_to(
                bar, LEFT, buff=0.15)
            v = tx(f"{100 * m:+.0f}%", 16, col if m >= 0 else BAD, bold=True).next_to(bar, RIGHT if m >= 0 else LEFT, buff=0.12)
            if m < 0:
                nm.next_to(v, LEFT, buff=0.15)
            rows.add(VGroup(nm, bar, v))
        axis = Line([-0.4, 2.4, 0], [-0.4, -2.0, 0], stroke_color=GREY_C, stroke_width=1.5)
        head = tx("Net income as a share of sales, five-year average", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        gw = sum(get(f"iff.goodwill.{y}") for y in (2022, 2023, 2025))
        note = VGroup(tx(f"IFF wrote down ${gw:.1f}bn of goodwill", 15, BAD, bold=True),
                      tx(f"in 2022, 2023 and 2025: the premium it", 15, GREY_A), tx("had paid for businesses it bought", 15, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.4, -2.3, 0])
        src = source("Form 10-K filings via SEC XBRL (net income, revenue; IFF: GoodwillImpairmentLoss)", size=13)
        with self.voiceover(
            "Over five years, that shows. <bookmark mark='a'/> Sherwin-Williams and Ecolab, which sells cleaning and "
            f"water treatment, kept about {100 * land['SHW']['margin5']:.0f} cents of every "
            f"dollar as profit; PPG about {100 * land['PPG']['margin5']:.0f}. <bookmark mark='b'/> LyondellBasell and "
            f"Dow, about {100 * land['LYB']['margin5']:.0f} and {100 * land['DOW']['margin5']:.0f}. "
            "<bookmark mark='c'/> But specialty is not a guarantee. IFF, which makes flavours and fragrances, lost "
            f"money: it wrote down about {gw:.0f} billion dollars of goodwill in three of those years, the premium it "
            "had paid for businesses it bought. A good business bought at too high a price is a bad investment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows[:3]],
                                  lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows[3:5]],
                                  lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[5][0]), GrowFromEdge(rows[5][1], RIGHT), FadeIn(rows[5][2]), FadeIn(note))
        self.clear_scene()
