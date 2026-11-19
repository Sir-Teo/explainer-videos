from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

IND = ("fishing", "coconut grove", "boatyard", "ferry")
SHORT = {"fishing": r"fishing", "coconut grove": r"grove", "boatyard": r"boatyard", "ferry": r"ferry"}


class ThreeWays(VoiceoverScene):
    def construct(self):
        card(self, 2, r"GDP three ways", r"If every sale is also somebody's purchase, what do you add up?",
             "Chapter two. GDP, three ways.", lit=("households", "firms", "government", "world"),
             scale=("nation",), horizon=("a year",))
        self.books()
        self.output()
        self.spending()
        self.income()
        self.sankey()
        self.saving()
        self.america()
        self.shares()

    # ------------------------------------------------------------------
    def _industry_boxes(self, a, width=2.5, y=1.6):
        boxes = VGroup()
        for i, name in enumerate(IND):
            col = IND_COLOR[name]
            b = RoundedRectangle(width=width, height=1.0, corner_radius=0.15, stroke_color=col, stroke_width=2.4,
                                 fill_color=col, fill_opacity=0.12)
            t = label(IND_NAME[name], font_size=24, color=col).move_to(b.get_center() + UP * 0.2)
            v = label(dollars(a["gross"][i], 0), font_size=24).move_to(b.get_center() + DOWN * 0.22)
            g = VGroup(b, t, v)
            g.box, g.name, g.value = b, t, v
            boxes.add(g)
        boxes.arrange(RIGHT, buff=0.55).move_to(UP * y)
        return boxes

    def books(self):
        a = load("accounts")
        dara = islander("dara", 1.1, name=True).to_corner(UL, buff=0.5)
        ledger = label(r"Dara keeps the Island's books: \ a year of sales", font_size=28, color=DARA)
        ledger.next_to(dara, RIGHT, buff=0.4)
        boxes = self._industry_boxes(a, y=1.6)
        Z = np.array(a["Z"])
        arrows = VGroup()
        for i in range(4):
            for j in range(4):
                if Z[i, j] > 0:
                    s, e = boxes[i].box, boxes[j].box
                    off = 0.25 if i < j else -0.25
                    start = s.get_bottom() + RIGHT * off
                    end = e.get_bottom() + RIGHT * off + DOWN * 0.02
                    # left to right, counterclockwise, bulges below; right to left, clockwise, also below
                    ang = (0.55 + 0.15 * abs(i - j)) * (1 if i < j else -1)
                    arc = CurvedArrow(start, end, angle=ang, color=IND_COLOR[IND[i]],
                                      stroke_width=1.5 + Z[i, j] / 12, tip_length=0.15)
                    arrows.add(arc)
        inputs = label(r"sales to each other: \ coconut fibre for nets, \ repairs, \ the ferry's freight",
                       font_size=22, color=GREY_A).move_to(DOWN * 1.0)
        total = MathTex(r"380 + 300 + 185 + 110 = " + f"{sum(a['gross']):.0f}", font_size=40)
        total.move_to(DOWN * 1.9)
        twice = label(r"the coconut fibre is counted twice: \ once when sold to the fishers, \ again inside the "
                      r"fish", font_size=24, color=E.MISS).move_to(DOWN * 2.8)
        tag = island_tag(r"simulated: the Island's accounts, year 3 (dollars)", corner=DR, font_size=16)
        with self.voiceover(
            "On the Island, the books are kept by Dara. <bookmark mark='a'/> There are four businesses: the "
            "fishing company, the coconut grove, the boatyard and the ferry. In a year they sold "
            f"{a['gross'][0]:.0f} dollars' worth of fish, 300 of coconuts and coconut products, 185 of boats and "
            "repairs, and 110 of passages and freight. <bookmark mark='b'/> Some of "
            "those sales were to each other. The grove sold fibre to the fishing company for its nets, the "
            "boatyard repaired the fishing boats and the ferry, and the ferry carried everyone's goods. "
            "<bookmark mark='c'/> Add up all the sales and you get 975 dollars. <bookmark mark='d'/> But that "
            "number counts some things twice. The coconut fibre is counted once when the grove sells it, and again "
            "inside the price of the fish caught with the nets made from it. A total of sales grows every time "
            "one firm buys from another, even if nothing more is made."
        ) as vo:
            self.play(FadeIn(dara), FadeIn(ledger), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in boxes], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in arrows], lag_ratio=0.15), FadeIn(inputs), run_time=2.0)
            vo.wait_until("c")
            self.play(Write(total))
            vo.wait_until("d")
            self.play(FadeIn(twice))
        self.clear_scene()

    def output(self):
        a = load("accounts")
        gross, inputs, va = a["gross"], a["inputs"], a["va"]
        k = 0.0105
        base_y = -2.4
        cols = VGroup()
        for i, name in enumerate(IND):
            x = -4.8 + i * 2.6
            col = IND_COLOR[name]
            g = Rectangle(width=1.1, height=gross[i] * k, stroke_color=col, stroke_width=2, fill_opacity=0)
            g.move_to([x, base_y + gross[i] * k / 2, 0])
            inp = Rectangle(width=1.1, height=inputs[i] * k, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9)
            inp.move_to([x, base_y + gross[i] * k - inputs[i] * k / 2, 0])
            v = Rectangle(width=1.1, height=va[i] * k, stroke_width=0, fill_color=col, fill_opacity=0.85)
            v.move_to([x, base_y + va[i] * k / 2, 0])
            nm = label(IND_NAME[name], font_size=22, color=col).next_to(g, DOWN, buff=0.15)
            vt = label(dollars(va[i], 0), font_size=24).move_to(v)
            it = label(rf"inputs {dollars(inputs[i], 0)}", font_size=18, color=GREY_B).next_to(inp, RIGHT, buff=0.08)
            cols.add(VGroup(g, inp, v, nm, vt, it))
        eq = MathTex(r"\text{value added} = \text{sales} - \text{inputs used up}", font_size=36).to_edge(UP, buff=0.45)
        tot = MathTex("275 + 290 + 110 + 65 = 740", font_size=40, color=E.ACCENT).next_to(eq, DOWN, buff=0.3)
        tot.to_edge(RIGHT, buff=0.6)
        name = label(r"GDP by output", font_size=28, color=E.ACCENT).next_to(tot, LEFT, buff=0.4)
        tag = island_tag(r"simulated: the Island's accounts, year 3 (dollars)", corner=DR, font_size=16)
        with self.voiceover(
            "The fix is to count, for each business, only what it added. <bookmark mark='a'/> Start with each "
            "one's sales. <bookmark mark='b'/> Take away everything it bought and used up to make them: the "
            "fibre, the repairs, the freight, and the nets, nails and fuel it imported. <bookmark mark='c'/> What "
            "is left is the business's value added, the value it created itself. The fishing company sold 380 "
            "dollars of fish with 105 dollars of inputs, and so added 275. <bookmark mark='d'/> Add the four: 275, "
            "290, 110 and 65 make 740 dollars. That is the Island's gross domestic product, measured by output: "
            "the value of everything produced on the Island in the year, with each thing counted once."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Create(c[0]), FadeIn(c[3])) for c in cols], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(c[1]), FadeIn(c[5])) for c in cols], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(c[2], DOWN), FadeIn(c[4])) for c in cols],
                                  lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(name), Write(tot))
        self.clear_scene()

    def spending(self):
        a = load("accounts")
        e = a["expenditure"]
        k = 0.0085
        items = [("C", e["C"]), ("I", e["I"]), ("G", e["G"]), ("X", e["X"])]
        y0 = 1.3
        x = -5.8
        blocks = VGroup()
        for key, v in items:
            r = Rectangle(width=v * k, height=0.75, stroke_width=0, fill_color=USE_COLOR[key], fill_opacity=0.85)
            r.move_to([x + v * k / 2, y0, 0])
            t = label(rf"{USE_NAME[key]} \\ {dollars(v, 0)}", font_size=20, color=BACKGROUND if v > 100 else WHITE)
            t.move_to(r)
            if v < 100:
                t.next_to(r, UP, buff=0.12).set_color(USE_COLOR[key])
            blocks.add(VGroup(r, t))
            x += v * k + 0.04
        total_right = x
        m = e["M"]
        mbar = Rectangle(width=m * k, height=0.75, stroke_width=0, fill_color=E.WORLD, fill_opacity=0.35)
        mbar.move_to([total_right - m * k / 2, y0 - 1.0, 0])
        mt = label(rf"minus imports \ {dollars(m, 0)}: \ nets, nails, fuel, \ and cloth", font_size=20,
                   color=E.WORLD).next_to(mbar, DOWN, buff=0.15)
        gdp_w = 740 * k
        gbar = Rectangle(width=gdp_w, height=0.75, stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.85)
        gbar.move_to([-5.8 + gdp_w / 2, y0 - 2.6, 0])
        gt = label(r"GDP by spending: \ \$740", font_size=24, color=BACKGROUND).move_to(gbar)
        eq = MathTex(r"Y = C + I + G + X - M", font_size=44).to_edge(UP, buff=0.45)
        num = MathTex(r"740 = 610 + 120 + 30 + 120 - 140", font_size=40, color=E.ACCENT).to_edge(DOWN, buff=0.5)
        tag = island_tag(r"simulated: the Island's accounts, year 3 (dollars)", corner=DR, font_size=16)
        with self.voiceover(
            "Now count from the other end: who bought what was produced, for their own use and not to make "
            "something else. <bookmark mark='a'/> Households bought 610 dollars of fish, coconuts, passages and "
            "cloth. That's consumption. <bookmark mark='b'/> Crusoe's boatyard built two new boats for the "
            "fishing company: 120 dollars of investment, goods bought to produce more in later years. "
            "<bookmark mark='c'/> The island council bought 30, and <bookmark mark='d'/> visiting ships bought "
            "120 of fish and coconuts: exports. <bookmark mark='e'/> That adds up to 880, which is too much, "
            "because some of what was bought wasn't made on the Island. The cloth was imported, and so were the "
            "nets, nails and fuel used up inside the fish and the boats. Take away the imports, 140, "
            "<bookmark mark='f'/> and you're back at 740. Consumption plus investment plus government plus exports "
            "minus imports: GDP measured by spending, the most famous identity in macroeconomics."
        ) as vo:
            self.play(Write(eq), FadeIn(tag))
            for mk, b in zip("abcd", blocks):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[0], LEFT), FadeIn(b[1]))
            vo.wait_until("e")
            self.play(FadeIn(mbar, shift=DOWN * 0.2), FadeIn(mt))
            vo.wait_until("f")
            self.play(GrowFromEdge(gbar, LEFT), FadeIn(gt))
            self.play(Write(num))
        self.clear_scene()

    def income(self):
        a = load("accounts")
        inc = a["income"]
        k = 0.0085
        parts = [("wages", inc["wages"], WAGES, r"wages"), ("profits", inc["profits"], PROFITS, r"profits"),
                 ("taxes", inc["taxes"], TAXES, r"taxes on production")]
        x = -5.8
        blocks = VGroup()
        for key, v, col, nm in parts:
            r = Rectangle(width=v * k, height=0.75, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to([x + v * k / 2, 0.8, 0])
            t = label(rf"{nm} \\ {dollars(v, 0)}", font_size=22, color=BACKGROUND if v > 100 else col)
            t.move_to(r)
            if v < 100:
                t.next_to(r, UP, buff=0.12)
            blocks.add(VGroup(r, t))
            x += v * k + 0.04
        eq = MathTex(r"Y = \text{wages} + \text{profits} + \text{taxes on production}", font_size=40)
        eq.to_edge(UP, buff=0.45)
        num = MathTex(r"740 = 450 + 250 + 40", font_size=40, color=E.ACCENT).move_to(DOWN * 0.9)
        why = label(r"every dollar of value added is paid to someone", font_size=28, color=GREY_A)
        why.to_edge(DOWN, buff=0.9)
        three = VGroup(label(r"output $= 740$", font_size=28, color=E.FIRMS),
                       label(r"spending $= 740$", font_size=28, color=E.HOUSEHOLDS),
                       label(r"income $= 740$", font_size=28, color=E.ACCENT)).arrange(RIGHT, buff=0.8)
        three.to_edge(DOWN, buff=0.9)
        tag = island_tag(r"simulated: the Island's accounts, year 3 (dollars)", corner=DR, font_size=16)
        with self.voiceover(
            "The third way is Petty's: count the incomes. <bookmark mark='a'/> Every dollar a business adds has "
            "to go to somebody. Most of it, 450 dollars, went to the people who did the work, as wages. "
            "<bookmark mark='b'/> 250 was left for the owners, as profit. <bookmark mark='c'/> And 40 went to the "
            "council, as taxes on production. <bookmark mark='d'/> 450 plus 250 plus 40 is 740 again. "
            "<bookmark mark='e'/> This isn't a coincidence, and it isn't a theory. It's bookkeeping. Profit is "
            "defined as what is left after everyone else is paid, so value added and the incomes it pays must be "
            "equal. And every sale is somebody's purchase, so output and spending must be equal too. Three ways of "
            "reading the same transactions give one number."
        ) as vo:
            self.play(Write(eq), FadeIn(tag))
            for mk, b in zip("abc", blocks):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[0], LEFT), FadeIn(b[1]))
            vo.wait_until("d")
            self.play(Write(num))
            vo.wait_until("e")
            self.play(FadeIn(why))
            self.play(FadeOut(why), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in three], lag_ratio=0.3))
            self.wait(0.5)
        self.clear_scene()

    def sankey(self):
        a = load("accounts")
        va = np.array(a["va"])
        wages, profits, taxes = np.array(a["wages"]), np.array(a["profits"]), np.array(a["taxes"])
        uses = ("C", "I", "G", "X")
        vbu = np.array([a["va_by_use"][u] for u in uses])      # (use, industry)
        H = 5.6
        gap = 0.08
        top = 2.75
        k = (H - 3 * gap) / 740.0
        xs = (-4.6, 0.0, 4.6)
        w = 0.42

        def spans(values):
            out, y = [], top
            for v in values:
                out.append((y, y - v * k))
                y -= v * k + gap
            return out

        left_vals = [wages.sum(), profits.sum(), taxes.sum()]
        left = spans(left_vals)
        mid = spans(va)
        right = spans(vbu.sum(axis=1))
        lcol = (WAGES, PROFITS, TAXES)
        lname = (r"wages", r"profits", r"taxes")
        blocks = VGroup()
        names = VGroup()
        for (y0, y1), c, n, v in zip(left, lcol, lname, left_vals):
            r = Rectangle(width=w, height=y0 - y1, stroke_width=0, fill_color=c, fill_opacity=0.95)
            r.move_to([xs[0], (y0 + y1) / 2, 0])
            blocks.add(r)
            names.add(label(rf"{n} \ {dollars(v, 0)}", font_size=20, color=c).next_to(r, LEFT, buff=0.12))
        for (y0, y1), name, v in zip(mid, IND, va):
            r = Rectangle(width=w, height=y0 - y1, stroke_width=0, fill_color=IND_COLOR[name], fill_opacity=0.95)
            r.move_to([xs[1], (y0 + y1) / 2, 0])
            blocks.add(r)
            t = label(rf"{SHORT[name]} \ {dollars(v, 0)}", font_size=21, color=IND_COLOR[name])
            t.move_to(r)
            bg = BackgroundRectangle(t, fill_opacity=0.85, buff=0.05)
            names.add(VGroup(bg, t).set_z_index(6))
        for (y0, y1), u, v in zip(right, uses, vbu.sum(axis=1)):
            r = Rectangle(width=w, height=y0 - y1, stroke_width=0, fill_color=USE_COLOR[u], fill_opacity=0.95)
            r.move_to([xs[2], (y0 + y1) / 2, 0])
            blocks.add(r)
            names.add(label(rf"{USE_NAME[u]} \ {dollars(v, 0)}", font_size=20, color=USE_COLOR[u]).next_to(
                r, RIGHT, buff=0.12))
        # ribbons, income -> industry: inside each left block, by industry; inside each middle block, by part
        ribbons_l = VGroup()
        mid_cursor = [m[0] for m in mid]
        for p, vec, c in ((0, wages, WAGES), (1, profits, PROFITS), (2, taxes, TAXES)):
            yl = left[p][0]
            for j in range(4):
                h = vec[j] * k
                ym = mid_cursor[j]
                ribbons_l.add(band(xs[0] + w / 2, yl, yl - h, xs[1] - w / 2, ym, ym - h, c, opacity=0.4))
                yl -= h
                mid_cursor[j] -= h
        ribbons_r = VGroup()
        mid_cursor = [m[0] for m in mid]
        right_cursor = [r[0] for r in right]
        for j in range(4):
            for u in range(4):
                h = vbu[u, j] * k
                if h < 1e-4:
                    continue
                ym, yr = mid_cursor[j], right_cursor[u]
                ribbons_r.add(band(xs[1] + w / 2, ym, ym - h, xs[2] - w / 2, yr, yr - h, IND_COLOR[IND[j]],
                                   opacity=0.4))
                mid_cursor[j] -= h
                right_cursor[u] -= h
        blocks.set_z_index(4)
        heads = VGroup(label(r"income", font_size=26, color=E.ACCENT).move_to([xs[0], 3.25, 0]),
                       label(r"output (value added)", font_size=26, color=E.ACCENT).move_to([xs[1], 3.25, 0]),
                       label(r"spending (net of imports)", font_size=26, color=E.ACCENT).move_to([xs[2], 3.25, 0]))
        tag = island_tag(r"simulated: the Island, year 3; spending split by the value added each use embodies "
                         r"(Leontief's inverse, chapter 10)", corner=DR, font_size=15)
        with self.voiceover(
            "Here are the three ways in one picture. <bookmark mark='a'/> In the middle, the value added by each "
            "business. <bookmark mark='b'/> On the left, where it went: each business's wages, profits and taxes "
            "flow out to the three kinds of income. <bookmark mark='c'/> On the right, what it was for: the fish, "
            "coconuts, boats and passages end up in households' consumption, in investment, with the council, and "
            "on the visiting ships, once the imported parts are taken out. <bookmark mark='d'/> Every column is "
            "740 dollars tall. This is what economists mean by the circular flow: the same dollars, earned, "
            "produced and spent."
        ) as vo:
            self.play(FadeIn(heads), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in blocks[3:7]], lag_ratio=0.15), FadeIn(names[3:7]))
            vo.wait_until("b")
            self.play(FadeIn(blocks[0:3]), FadeIn(names[0:3]), LaggedStart(*[FadeIn(r) for r in ribbons_l],
                                                                         lag_ratio=0.04), run_time=2.2)
            vo.wait_until("c")
            self.play(FadeIn(blocks[7:]), FadeIn(names[7:]), LaggedStart(*[FadeIn(r) for r in ribbons_r],
                                                                        lag_ratio=0.03), run_time=2.2)
            vo.wait_until("d")
            self.play(*[Indicate(h, color=WHITE) for h in heads])
        self.clear_scene()

    def saving(self):
        a = load("accounts")
        e = a["expenditure"]
        lines = VGroup(
            MathTex(r"S = Y - C - G", font_size=42),
            MathTex(rf"= 740 - 610 - 30 = {a['saving']:.0f}", font_size=40, color=E.BANKS),
            MathTex(r"Y = C + I + G + (X - M) \;\Rightarrow\; S = I + (X - M)", font_size=40),
            MathTex(rf"{a['saving']:.0f} = {e['I']:.0f} + ({a['nx']:.0f})", font_size=44, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.5)
        lines[1].align_to(lines[0], LEFT).shift(RIGHT * 1.2)
        say = label(r"the Island saved 100, \ invested 120, \ and borrowed 20 from abroad", font_size=28,
                    color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = island_tag(r"simulated: the Island's accounts, year 3 (dollars)", corner=DR, font_size=16)
        with self.voiceover(
            "The identities have a famous consequence. <bookmark mark='a'/> Call what the Island earned but didn't "
            "spend on consumption or on the council its national saving: 740, minus 610, minus 30, is 100 dollars. "
            "<bookmark mark='b'/> Put that together with the spending identity, and saving must equal investment "
            "plus net exports. <bookmark mark='c'/> The Island saved 100 and invested 120, and the difference, "
            "20, is exactly its trade deficit. <bookmark mark='d'/> A country that invests more than it saves "
            "must borrow the difference from the rest of the world, whatever its trade policy. We'll lean on that "
            "identity when we open the trade and capital pipes, in Parts 34 to 36."
        ) as vo:
            self.play(Write(lines[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(lines[1]))
            vo.wait_until("b")
            self.play(Write(lines[2]))
            vo.wait_until("c")
            self.play(Write(lines[3]))
            vo.wait_until("d")
            self.play(FadeIn(say))
        self.clear_scene()

    def america(self):
        a = load("accounts")
        us = a["us"]
        k = 0.165           # units per trillion, halved (the bars are 2k wide per trillion)
        x = -6.2
        y0 = 1.4
        blocks = VGroup()
        for key in ("C", "I", "G", "X"):
            v = us[key] / 1000
            r = Rectangle(width=v * k * 2.0, height=0.8, stroke_width=0, fill_color=USE_COLOR[key], fill_opacity=0.85)
            r.move_to([x + v * k, y0, 0])
            t = label(rf"{USE_NAME[key]} \\ {tn(us[key])}", font_size=19,
                      color=BACKGROUND if v > 4 else USE_COLOR[key]).move_to(r)
            if v <= 4:
                t.next_to(r, UP, buff=0.12)
            blocks.add(VGroup(r, t))
            x += v * k * 2.0 + 0.04
        mw = us["M"] / 1000 * k * 2.0
        mbar = Rectangle(width=mw, height=0.8, stroke_width=0, fill_color=E.WORLD, fill_opacity=0.35)
        mbar.move_to([x - 0.04 - mw / 2, y0 - 1.0, 0])
        mt = label(rf"minus imports \ {tn(us['M'])}", font_size=20, color=E.WORLD).next_to(mbar, LEFT, buff=0.15)
        gw = us["GDP"] / 1000 * k * 2.0
        gbar = Rectangle(width=gw, height=0.8, stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.85)
        gbar.move_to([-6.2 + gw / 2, y0 - 2.5, 0])
        gt = label(rf"GDP {tn(us['GDP'])}", font_size=24, color=BACKGROUND).move_to(gbar)
        gdi = label(rf"measured by income (GDI): \ {tn(us['GDI'])}", font_size=24, color=E.HOUSEHOLDS)
        disc = label(rf"the statistical discrepancy: \ {us['discrepancy']:.0f} billion dollars", font_size=24,
                     color=E.MISS)
        VGroup(gdi, disc).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.55).to_edge(LEFT, buff=0.8)
        head = label(rf"The United States, {us['year']}", font_size=34).to_edge(UP, buff=0.4)
        tag = data_tag(rf"BEA, national income and product accounts, annual (GDPA, PCECA, GPDIA, GCEA, EXPGSA, IMPGSA, "
                       rf"GDIA), {data.fred_cite('GDPA')}", corner=DR, font_size=15)
        with self.voiceover(
            "The United States keeps exactly these books, on a larger scale. <bookmark mark='a'/> In 2025, "
            f"American households spent {say_tn(us['C'])} on consumption, <bookmark mark='b'/> businesses and "
            f"home builders invested {say_tn(us['I'])}, <bookmark mark='c'/> governments, federal, state and local, "
            f"bought {say_tn(us['G'])}, and foreigners bought {say_tn(us['X'])} of American exports. "
            f"<bookmark mark='d'/> Take away {say_tn(us['M'])} of imports, <bookmark mark='e'/> and GDP was "
            f"{say_tn(us['GDP'], 2)}. <bookmark mark='f'/> Measured by income, it was {say_tn(us['GDI'], 2)}. "
            "In real data the two sides don't quite agree, because they're built from different sources: spending "
            "from sales and surveys of businesses, income from tax records and payrolls. The gap, "
            f"{abs(us['discrepancy']):.0f} billion dollars this year, is published under its honest name: the "
            "statistical discrepancy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(blocks[0][0], LEFT), FadeIn(blocks[0][1]), run_time=0.8)
            vo.wait_until("b")
            self.play(GrowFromEdge(blocks[1][0], LEFT), FadeIn(blocks[1][1]), run_time=0.8)
            vo.wait_until("c")
            for b in blocks[2:]:
                self.play(GrowFromEdge(b[0], LEFT), FadeIn(b[1]), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(mbar, shift=DOWN * 0.2), FadeIn(mt))
            vo.wait_until("e")
            self.play(GrowFromEdge(gbar, LEFT), FadeIn(gt))
            vo.wait_until("f")
            self.play(FadeIn(gdi))
            self.play(FadeIn(disc))
        self.clear_scene()

    def shares(self):
        a = load("accounts")
        sh = a["shares"]
        years = sh["years"]
        ax = year_axis([1929, 2026], [-0.1, 0.9], x_length=10.6, y_length=4.6, xticks=list(range(1930, 2030, 10)),
                       yticks=[0, 0.2, 0.4, 0.6, 0.8], yfmt=lambda v: f"{100 * v:.0f}\\%",
                       ylabel=r"share of GDP", center=DOWN * 0.3)
        A = ax.ax
        curves = VGroup()
        names = VGroup()
        for key in ("C", "I", "G", "NX"):
            col = USE_COLOR["X" if key == "NX" else key]
            c = VMobject(stroke_color=col, stroke_width=3.5).set_points_as_corners(
                [A.c2p(y, v) for y, v in zip(years, sh[key])])
            curves.add(c)
            nm = label({"C": r"consumption", "I": r"investment", "G": r"government",
                        "NX": r"net exports"}[key], font_size=21, color=col)
            nm.next_to(A.c2p(years[-1], sh[key][-1]), RIGHT, buff=0.1)
            nm.shift({"I": UP * 0.17, "G": DOWN * 0.17}.get(key, ORIGIN))
            names.add(nm)
        zero = DashedLine(A.c2p(1929, 0), A.c2p(2026, 0), color=GREY_C, stroke_width=1.2)
        pg, py = a["peak_G"]
        war = label(rf"{py}: \ government {100 * pg:.0f}\% of GDP", font_size=22, color=E.GOVERNMENT)
        war.next_to(A.c2p(py, pg), RIGHT, buff=0.2)
        head = label(r"Where America's output went, 1929--2025", font_size=30).to_edge(UP, buff=0.35)
        tag = data_tag(rf"BEA via FRED (annual, current dollars), {data.fred_cite('GDPA')}", corner=DL, font_size=15)
        with self.voiceover(
            "Kept every year since 1929, the spending side tells the century's story. <bookmark mark='a'/> "
            "Consumption is usually about two thirds of the American economy, and investment the swingiest part, "
            "collapsing in the Depression. <bookmark mark='b'/> In 1944, at the height of the war, government "
            f"bought {100 * pg:.0f} percent of everything the country produced. That's the number Keynes, Meade "
            "and Stone needed: how much a country can turn to war, and what must give way. <bookmark mark='c'/> "
            "And since the 1970s, net exports have been mostly below zero: by the identity we just saw, America "
            "has invested more than it saved, and borrowed the rest."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(head), FadeIn(tag), Create(zero))
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2), run_time=3.0)
            self.play(FadeIn(names))
            vo.wait_until("a")
            self.play(Indicate(names[0]), Indicate(names[1]))
            vo.wait_until("b")
            self.play(FadeIn(war), Flash(A.c2p(py, pg), color=E.GOVERNMENT))
            vo.wait_until("c")
            self.play(Indicate(names[3]), curves[3].animate.set_stroke(width=6))
        self.clear_scene()
