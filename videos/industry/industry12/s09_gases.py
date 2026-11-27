from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Gases(VoiceoverScene):
    def construct(self):
        card(self, 7, "The plant at the fence", "How do you sell air, and why is it one of the best businesses in chemicals?",
             "Chapter seven. The plant at the fence.", lit=("unit", "moat", "dollar"))
        self.air()
        self.delivery()
        self.contract()
        self.results()
        self.prices()

    def air(self):
        kinds = ["N2"] * 78 + ["O2"] * 21 + ["Ar"]
        grid = VGroup(*[draw.molecule(k, bond=0.16) for k in kinds])
        for k, m in enumerate(grid):
            m.move_to([-6.0 + 0.42 * (k % 10), 2.2 - 0.42 * (k // 10), 0])
        frame = SurroundingRectangle(grid, buff=0.15, corner_radius=0.1, stroke_color=GREY_C, stroke_width=1.5)
        fl = tx("a hundred molecules of air", 15, GREY_A).next_to(frame, UP, buff=0.1)
        legend = VGroup(tx("78 nitrogen", 17, NITRO, bold=True), tx("21 oxygen", 17, BAD, bold=True),
                        tx("about 1 argon", 17, EUROPE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(frame, DOWN, buff=0.25)
        col = draw.column(3.2).move_to([1.6, -0.6, 0])
        cl = VGroup(tx("air separation unit:", 15, WHITE, bold=True), tx("compress, cool below -180°C,", 14, GREY_A),
                    tx("and distil the liquid air", 14, GREY_A)).arrange(DOWN, buff=0.04).next_to(col, DOWN, buff=0.15)
        outs = VGroup()
        for i, (k, name, c, use) in enumerate((("N2", "nitrogen", NITRO, "blankets food, chips and chemical tanks"),
                                               ("O2", "oxygen", BAD, "steel furnaces, hospitals, glass"),
                                               ("Ar", "argon", EUROPE, "welding, light bulbs, chip making"))):
            m = draw.molecule(k, bond=0.35)
            row = VGroup(m, VGroup(tx(name, 18, c, bold=True), tx(use, 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)).arrange(
                RIGHT, buff=0.25)
            row.move_to([4.9, 1.6 - 1.3 * i, 0], aligned_edge=LEFT).shift(LEFT * 1.7)
            outs.add(row)
        arrs = VGroup(*[Arrow(col.cuts[5 - 2 * i].get_end(), o_.get_left(), buff=0.1, stroke_width=2.5, color=GREY_B,
                              max_tip_length_to_length_ratio=0.15) for i, o_ in enumerate(outs)])
        with self.voiceover(
            "The strangest business in chemicals sells air. <bookmark mark='a'/> Take a hundred molecules of air: "
            "seventy-eight are nitrogen, twenty-one oxygen, and about one argon. <bookmark mark='b'/> An air separation "
            "unit squeezes air, chills it until it turns liquid, colder than minus a hundred and eighty degrees, and "
            "distils it like crude oil in a refinery, because each gas boils at a different temperature. "
            "<bookmark mark='c'/> Out come nitrogen, to keep oxygen away from food, chips and chemicals; oxygen, for "
            "steelmaking, hospitals and glass; and argon, for welding and making chips. The same companies also make "
            "hydrogen, from natural gas, for refineries."
        ) as vo:
            self.play(FadeIn(frame), FadeIn(fl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in grid], lag_ratio=0.01), run_time=2.0)
            self.play(FadeIn(legend[0]), *[Indicate(m, color=NITRO, scale_factor=1.0) for m in grid[:78]], run_time=0.8)
            self.play(FadeIn(legend[1]), *[Indicate(m, color=BAD, scale_factor=1.3) for m in grid[78:99]], run_time=0.8)
            self.play(FadeIn(legend[2]), Indicate(grid[99], color=EUROPE, scale_factor=2.0), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(col), FadeIn(cl))
            g2 = grid.copy()
            self.add(g2)
            self.play(g2.animate.scale(0.5).move_to(col.tower.get_bottom() + UP * 0.6).set_opacity(0), grid.animate.set_opacity(0.35),
                      run_time=1.6)
            self.remove(g2)
            vo.wait_until("c")
            for a_, o_ in zip(arrs, outs):
                self.play(GrowArrow(a_), FadeIn(o_, shift=RIGHT * 0.2), run_time=0.8)
        self.clear_scene()

    def delivery(self):
        G = R["gases"]
        cols = VGroup()
        items = [(draw.cylinder(1.2, "#7EC8F5"), "In cylinders", "welders, labs, hospitals", "small customers, many of them"),
                 (draw.truck(1.8), "As liquid, by truck", "food plants, hospitals, factories", "contracts of 3-7 years, no minimum"),
                 (VGroup(draw.column(1.5), draw.factory(1.2)).arrange(RIGHT, buff=0.2, aligned_edge=DOWN), "On site, by pipe",
                  "steel mills, refineries, chemical and chip plants", "a plant at the customer's fence")]
        for i, (ic, h, w, n_) in enumerate(items):
            ic.scale_to_fit_height(min(ic.height, 1.4))
            g = VGroup(ic, tx(h, 20, WHITE, bold=True), tx(w, 14, GREY_A), tx(n_, 14, GREY_B)).arrange(DOWN, buff=0.12)
            g.move_to([-4.6 + 4.6 * i, 1.0, 0])
            cols.add(g)
        box = SurroundingRectangle(cols[2], buff=0.2, corner_radius=0.12, stroke_color=GOLD, stroke_width=2)
        terms = VGroup(tx(f"Linde: contracts of {G['linde_lo']}-{G['linde_hi']} years, 'with minimum purchase requirements and "
                          "price escalation provisions'", 15, WHITE),
                       tx(f"Air Products: 'long-term contracts ranging from {G['apd_lo']}- to {G['apd_hi']}-years'", 15, WHITE),
                       tx("Linde: 'generally uneconomical to transport most products distances greater than a few hundred miles'",
                          15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to([0, -2.4, 0])
        if terms.width > 13:
            terms.scale_to_fit_width(13)
        src = source("Linde plc, Form 10-K 2025; Air Products and Chemicals, Form 10-K fiscal 2026", size=13)
        with self.voiceover(
            "The gas reaches customers in three ways. <bookmark mark='a'/> In cylinders, for welders, laboratories and "
            "hospitals. <bookmark mark='b'/> As a liquid, by truck, into a tank at a food plant or a factory, on "
            "contracts of three to seven years. "
            "<bookmark mark='c'/> And for the largest customers, a steel mill, a refinery, a chemical or a chip "
            "plant, the gas company builds a plant right at the fence and pipes the gas in. <bookmark mark='d'/> Those "
            f"on-site plants come with long contracts: {G['linde_lo']} to {G['linde_hi']} years at Linde, with minimum "
            f"purchases and prices that rise with costs; {G['apd_lo']} to {G['apd_hi']} years at Air Products, their "
            "filings say. And because most of these gases are, in Linde's words, uneconomical to carry more than a few "
            "hundred miles, the plant nearest the customer has a large advantage."
        ) as vo:
            self.play(FadeIn(src))
            for m_, c_ in zip("abc", cols):
                vo.wait_until(m_)
                self.play(FadeIn(c_, shift=UP * 0.2))
            self.play(Create(box))
            vo.wait_until("d")
            self.play(FadeIn(terms, shift=UP * 0.1))
        self.clear_scene()

    def contract(self):
        P_ = R["gases"]["plant"]
        u = ValueTracker(1.0)
        mill = draw.factory(1.6).move_to([-4.6, 0.6, 0])
        ml = tx("the customer: a steel mill", 16, WHITE, bold=True).next_to(mill, DOWN, buff=0.15)
        plant = draw.column(1.8).move_to([-1.6, 0.6, 0])
        pl = tx("the gas plant at its fence", 16, GASES, bold=True).next_to(plant, DOWN, buff=0.15)
        pipe = Line(plant.get_left() + DOWN * 0.3, mill.get_right() + DOWN * 0.3, stroke_color=GASES, stroke_width=5)
        ulab = tx("share of the gas the mill takes:", 20, GREY_A).move_to([-3.6, -1.4, 0])
        use = draw.number(lambda: 100 * u.get_value(), 0, suffix="%", size=26, color=WHITE)
        use.add_updater(lambda m: m.next_to(ulab, RIGHT, buff=0.2))
        use.update()

        def cash(t):
            billed = max(t, P_["minimum"])
            return P_["fee"] + billed * 40.0 - t * 25.0

        def bar():
            v = cash(u.get_value())
            return Rectangle(width=1.2, height=v / 120 * 3.6, stroke_width=0, fill_color=GOOD, fill_opacity=0.85).move_to(
                [3.4, -2.4, 0], aligned_edge=DOWN)

        def mbar():
            v = u.get_value() * 90.0
            return Rectangle(width=1.2, height=max(v / 120 * 3.6, 0.01), stroke_width=0, fill_color=BAD, fill_opacity=0.85).move_to(
                [5.4, -2.4, 0], aligned_edge=DOWN)
        b1, b2 = always_redraw(bar), always_redraw(mbar)
        v1 = draw.number(lambda: cash(u.get_value()), 0, prefix="$", suffix="m", size=22, color=GOOD)
        v1.add_updater(lambda m: m.next_to(b1, UP, buff=0.1))
        v2 = draw.number(lambda: u.get_value() * 90.0, 0, prefix="$", suffix="m", size=22, color=BAD)
        v2.add_updater(lambda m: m.next_to(b2, UP, buff=0.1))
        l1 = VGroup(tx("under the contract", 14, GOOD, bold=True), tx("fee + minimum purchase", 12, GREY_A)).arrange(
            DOWN, buff=0.03).move_to([3.4, -2.8, 0])
        l2 = VGroup(tx("selling gas by the tonne", 14, BAD, bold=True), tx("no fee, no minimum", 12, GREY_A)).arrange(
            DOWN, buff=0.03).move_to([5.4, -2.8, 0])
        head = tx("The gas plant's cash in a year", 20, WHITE, bold=True).move_to([4.4, 2.6, 0])
        terms = VGroup(tx(f"plant: ${P_['capex']:.0f}m; contract: {P_['years']} years", 14, GREY_A),
                       tx(f"fixed fee ${P_['fee']:.0f}m a year; the mill pays for at least {100 * P_['minimum']:.0f}% of the gas",
                          14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([-3.0, 2.7, 0])
        tag = estimate_tag("the Works (cracker.py, GasPlant): an illustrative contract, not any company's terms", corner=DR, size=12)
        with self.voiceover(
            "Why do these contracts matter so much? Play it with the Works' model of a gas plant. <bookmark mark='a'/> "
            f"The gas company spends about {P_['capex']:.0f} million dollars on a plant at a steel mill's fence. The mill "
            f"signs for {P_['years']} years: a fixed fee every year, and it pays for at least "
            f"{100 * P_['minimum']:.0f} per cent of the gas, whether it uses it or not. <bookmark mark='b'/> In a good "
            f"year the mill takes everything, and the gas plant makes about {cash(1.0):.0f} million dollars of cash. "
            "<bookmark mark='c'/> Now a recession: the mill cuts back to half. A plant selling gas by the tonne would "
            "lose half its income. Under the contract, the gas company still gets its fee and its minimum, and saves "
            f"the electricity it no longer burns: about {cash(0.5):.0f} million. <bookmark mark='d'/> Even if the mill "
            "stops altogether, the cash hardly moves. The customer carries the cycle. The gas company has, in effect, "
            "rented the mill a machine."
        ) as vo:
            self.play(FadeIn(mill), FadeIn(ml), FadeIn(plant), FadeIn(pl), Create(pipe), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(terms))
            vo.wait_until("b")
            self.play(FadeIn(head), FadeIn(b1), FadeIn(b2), FadeIn(v1), FadeIn(v2), FadeIn(l1), FadeIn(l2), FadeIn(use), FadeIn(ulab))
            vo.wait_until("c")
            self.play(u.animate.set_value(0.5), run_time=2.5)
            vo.wait_until("d")
            self.play(u.animate.set_value(0.0), run_time=2.0)
            self.play(u.animate.set_value(1.0), run_time=2.0)
        for m in (use, v1, v2):
            m.clear_updaters()
        self.clear_scene()

    def results(self):
        nets = R["cycle"]["nets"]
        G = R["gases"]
        ys = list(range(2017, 2026))
        pa = viz.plot_axes([2016.5, 2025.5], [-3.5, 8], x_length=8.4, y_length=4.4, xticks=[2017, 2019, 2021, 2023, 2025],
                           yticks=[-2, 0, 2, 4, 6, 8], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn",
                           ylabel="net income", size=14).move_to([-2.0, -0.3, 0])
        zero = Line(pa.ax.c2p(2016.5, 0), pa.ax.c2p(2025.5, 0), stroke_color=GREY_B, stroke_width=1.2)
        ll = VMobject(stroke_color=GASES, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, nets["LIN"][y]) for y in ys if y in nets["LIN"]])
        ld = VMobject(stroke_color=ETHYL, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, nets["DOW"][y]) for y in ys if y in nets["DOW"]])
        lab_l = tx("Linde", 17, GASES, bold=True).next_to(pa.ax.c2p(2025, nets["LIN"][2025]), RIGHT, buff=0.1)
        lab_d = tx("Dow", 17, ETHYL, bold=True).next_to(pa.ax.c2p(2025, nets["DOW"][2025]), RIGHT, buff=0.1)
        mar = VGroup(tx("net margin, five years", 16, GREY_A),
                     tx(f"Linde  {100 * G['lin']['margin5']:.0f}%", 22, GASES, bold=True),
                     tx(f"Air Products  {100 * G['apd']['margin5']:.0f}%", 22, GASES, bold=True),
                     tx(f"Dow  {100 * G['dow']['margin5']:.0f}%", 22, ETHYL, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(
            [4.9, 1.2, 0])
        apd = VGroup(tx("Air Products' margin includes", 13, GREY_A),
                     tx(f"${get('apd.charges.2025'):.1f}bn of after-tax charges in fiscal 2025,", 13, GREY_A),
                     tx("'primarily associated with ... project exit", 13, WHITE), tx("decisions'", 13, WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.03).move_to([4.9, -1.4, 0])
        src = source("Form 10-K filings via SEC XBRL; Air Products, Form 10-K fiscal 2026", size=13)
        with self.voiceover(
            "Here is what that looks like in the accounts. <bookmark mark='a'/> Dow, the commodity maker, swings from "
            "profit to loss and back. <bookmark mark='b'/> Linde, the largest industrial gas company in the world by its own "
            "account, made more profit "
            f"every single year from 2019 to 2025, to about {nets['LIN'][2025]:.1f} billion dollars. "
            "<bookmark mark='c'/> Over five years Linde kept about "
            f"{100 * G['lin']['margin5']:.0f} cents of every dollar of sales as profit, and Air Products about "
            f"{100 * G['apd']['margin5']:.0f}, against Dow's {100 * G['dow']['margin5']:.0f}. <bookmark mark='d'/> Even "
            "Air Products' bad year proves the point: it lost money in fiscal 2025 after about "
            f"{get('apd.charges.2025'):.0f} billion dollars of charges to walk away from big new energy projects, "
            f"while its adjusted operating income, which leaves such charges out, reached about "
            f"{get('apd.adj_oi.2026'):.1f} billion the following year."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(ld), run_time=2.5)
            self.play(FadeIn(lab_d))
            vo.wait_until("b")
            self.play(Create(ll), run_time=2.5)
            self.play(FadeIn(lab_l))
            vo.wait_until("c")
            self.play(FadeIn(mar, shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(apd))
        self.clear_scene()

    def prices(self):
        G = R["gases"]
        g, p = G["ppi_gases"], G["ppi_petro"]
        ys = sorted(y for y in g if y in p)
        pa = viz.plot_axes([ys[0] - 0.5, ys[-1] + 0.5], [0, 280], x_length=9.0, y_length=4.4,
                           xticks=[2005, 2010, 2015, 2020, 2025], yticks=[70, 140, 210, 280], xfmt=lambda v: f"{int(v)}",
                           yfmt=lambda v: f"{v:.0f}", ylabel=f"producer price index, {ys[0]} = 100", size=14).move_to([-1.4, -0.4, 0])
        gg = {y: 100 * g[y] / g[ys[0]] for y in ys}
        pp = {y: 100 * p[y] / p[ys[0]] for y in ys}
        lg = VMobject(stroke_color=GASES, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, gg[y]) for y in ys])
        lp = VMobject(stroke_color=ETHYL, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, pp[y]) for y in ys])
        falls_g = sum(1 for a, b in zip(ys, ys[1:]) if gg[b] < gg[a])
        falls_p = sum(1 for a, b in zip(ys, ys[1:]) if pp[b] < pp[a])
        key = VGroup(tx(f"industrial gases: fell in {falls_g} of {len(ys) - 1} years", 16, GASES, bold=True),
                     tx(f"petrochemicals: fell in {falls_p} of {len(ys) - 1} years", 16, ETHYL, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 1.8, 0])
        head = tx("What American producers charged", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("US Bureau of Labor Statistics, PPIs for industrial gas and petrochemical manufacturing, via FRED", size=13)
        with self.voiceover(
            "And in the prices. <bookmark mark='a'/> This is what American producers charged for petrochemicals since "
            f"{ys[0]}: up, down, up, down, falling in {falls_p} of the {len(ys) - 1} years. <bookmark mark='b'/> And for "
            f"industrial gases: falling in only {falls_g}, and ending at about {gg[ys[-1]] / 100:.1f} times where it "
            "started. Contracts that pass on costs, customers that cannot easily switch, and a product too costly to "
            "carry far make one of the steadiest businesses in chemicals. It is chemistry run like a utility."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lp), FadeIn(key[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(lg), FadeIn(key[0]), run_time=2.5)
        self.clear_scene()
