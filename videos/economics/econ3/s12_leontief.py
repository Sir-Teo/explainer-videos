from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

IND = ("fishing", "coconut grove", "boatyard", "ferry")
SHORT = (r"fishing", r"grove", r"boatyard", r"ferry")


class Leontief(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Input and output", r"If the world wants more fish, how much more of everything must the "
             r"Island make?", "Chapter ten. Input and output.", lit=("firms", "world"), scale=("firm", "nation"),
             horizon=("a year",))
        self.table()
        self.ripple()
        self.inverse()
        self.trade()

    # ------------------------------------------------------------------
    def _matrix(self, M, fmt, cell=1.25, font_size=26, colors=True, row_head=True):
        g = VGroup()
        cells = VGroup()
        n = len(M)
        for i in range(n):
            for j in range(n):
                v = M[i][j]
                t = label(fmt(v), font_size=font_size, color=WHITE if v else GREY_D)
                t.move_to([j * cell, -i * 0.7, 0])
                cells.add(t)
        heads_c = VGroup(*[label(SHORT[j], font_size=20, color=IND_COLOR[IND[j]]).move_to([j * cell, 0.65, 0])
                           for j in range(n)])
        heads_r = VGroup(*[label(SHORT[i], font_size=20, color=IND_COLOR[IND[i]]).move_to([-1.2, -i * 0.7, 0])
                           for i in range(n)])
        g.add(cells, heads_c, heads_r)
        g.cells, g.heads_c, g.heads_r = cells, heads_c, heads_r
        return g

    def table(self):
        a = load("leontief")
        acc_ = load("accounts")
        Z = acc_["Z"]
        who = history_card(r"1936", r"Wassily Leontief, Harvard",
                           r"a table of the American economy of 1919: what every industry bought from every other",
                           color=E.FIRMS, width=6.0, font_size=23).to_corner(UL, buff=0.45)
        zm = self._matrix(Z, lambda v: f"{v:.0f}").move_to(RIGHT * 2.6 + UP * 0.9)
        zl = label(r"Dara's table: \ row sells to column, \ dollars", font_size=22, color=GREY_A)
        zl.next_to(zm, UP, buff=0.3)
        gross = VGroup(*[label(rf"\${v:.0f}", font_size=22, color=IND_COLOR[IND[j]]) for j, v in
                         enumerate(acc_["gross"])])
        for j, t in enumerate(gross):
            t.move_to(zm.heads_c[j].get_center() + DOWN * (0.65 + 4 * 0.7))
        gl = label(r"each one's sales", font_size=20, color=GREY_B).next_to(gross, LEFT, buff=0.4)
        am = self._matrix(a["A"], lambda v: f"{v:.3f}" if v else "0", font_size=26)
        am.shift(zm.cells.get_center() - am.cells.get_center())
        al = MathTex(r"A = \frac{\text{what } j \text{ buys from } i}{\text{what } j \text{ sells}}", font_size=34)
        al.next_to(who, DOWN, buff=0.8).align_to(who, LEFT)
        al2 = label(r"Leontief's coefficients: \ inputs per dollar of sales", font_size=22, color=GREY_A)
        al2.move_to(zl)
        tag = island_tag(r"simulated: the Island's input-output table, year 3", corner=DR, font_size=16)
        with self.voiceover(
            "Dara's books hold one more table, and it has its own history. <bookmark mark='a'/> In 1936 Wassily "
            "Leontief, an economist at Harvard who had left the Soviet Union in 1925, published a table of the "
            "American economy of 1919, "
            "showing what every industry bought from every other. <bookmark mark='b'/> Here is the Island's "
            "version. Each row is a seller, each column a buyer: the grove sold 20 dollars of fibre to the fishing "
            "company and 30 of coconut wood to the boatyard; the boatyard did 40 dollars of repairs for the "
            "fishers and 25 for the ferry. <bookmark mark='c'/> Divide each column by that business's total sales, "
            "and you get Leontief's coefficients: how much of each input it needs for every dollar it sells. "
            "Each dollar of fish needs about five cents of fibre, ten cents of repairs and four cents of "
            "freight. Leontief's bet was that these recipes stay roughly fixed, at least for a while."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(who, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(who, color=E.FIRMS, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(zl), FadeIn(zm.heads_c), FadeIn(zm.heads_r), LaggedStart(
                *[FadeIn(c) for c in zm.cells], lag_ratio=0.05), run_time=2.0)
            self.play(FadeIn(gross), FadeIn(gl))
            vo.wait_until("c")
            self.play(FadeOut(zm.cells), FadeOut(gross), FadeOut(gl), FadeTransform(zl, al2), Write(al))
            self.play(LaggedStart(*[FadeIn(c) for c in am.cells], lag_ratio=0.04), run_time=1.6)
        self.clear_scene()

    def ripple(self):
        a = load("leontief")
        rounds = np.array(a["rounds"])
        cum = np.array(a["cumulative"])
        k = 0.42
        base = -2.3
        xs = [-4.6, -2.0, 0.6, 3.2]
        frames = VGroup()
        bars = []
        vals = []
        for j in range(4):
            col = IND_COLOR[IND[j]]
            frames.add(label(SHORT[j], font_size=24, color=col).move_to([xs[j], base - 0.35, 0]))
            bars.append(Rectangle(width=1.4, height=0.01, stroke_width=0, fill_color=col, fill_opacity=0.85)
                        .move_to([xs[j], base + 0.005, 0]))
            vals.append(label(r"\$0", font_size=24).move_to([xs[j], base + 0.35, 0]))
        floor = Line([-5.6, base, 0], [4.3, base, 0], color=GREY_C, stroke_width=2)
        head = label(r"\$10 more fish for the visiting ships: \ the extra output, \ round by round", font_size=28)
        head.to_edge(UP, buff=0.4)
        rlabel = label(r"round 0", font_size=28, color=E.ACCENT).to_corner(UR, buff=0.6).shift(DOWN * 0.8)
        expl = [r"the fish itself", r"the fibre, repairs and freight for that fish",
                r"the inputs for those inputs", r"and so on, smaller each time"]
        notes = VGroup(*[label(t, font_size=24, color=GREY_A) for t in expl])
        for nt in notes:
            nt.next_to(rlabel, DOWN, buff=0.3).align_to(rlabel, RIGHT)
        tag = island_tag(r"simulated: the Island, year 3; Leontief's coefficients", corner=DR, font_size=16)

        def state(r):
            out = []
            for j in range(4):
                h = cum[r][j] * k
                nb = Rectangle(width=1.4, height=max(h, 0.01), stroke_width=0, fill_color=IND_COLOR[IND[j]],
                               fill_opacity=0.85).move_to([xs[j], base + max(h, 0.01) / 2, 0])
                nv = label(rf"\${cum[r][j]:.2f}", font_size=24).move_to([xs[j], base + max(h, 0.01) + 0.3, 0])
                out.append((nb, nv))
            return out

        with self.voiceover(
            "Now ask the question Leontief built the table to answer. Suppose the visiting ships want ten "
            "dollars more fish. How much more must every business on the Island produce? <bookmark mark='a'/> "
            "First, ten dollars of fish. <bookmark mark='b'/> But catching it uses up fibre, repairs and freight, so "
            "the grove, the boatyard and the ferry must make about two dollars more between them. "
            "<bookmark mark='c'/> And those inputs need inputs of their own: the boatyard needs coconut wood, the "
            "ferry needs repairs. That's the second round, about thirty cents. <bookmark mark='d'/> Each round is "
            "smaller than the one before, and they add up. In all, the Island must produce "
            f"{sum(a['total']):.2f} dollars more to deliver ten dollars of fish."
        ) as vo:
            self.play(FadeIn(head), Create(floor), FadeIn(frames), FadeIn(tag), *[FadeIn(b) for b in bars],
                      *[FadeIn(v) for v in vals], FadeIn(rlabel))
            for r, mk in enumerate("abcd"):
                vo.wait_until(mk)
                st = state(r if r < 3 else len(cum) - 1)
                new_r = label(rf"round {r}" if r < 3 else r"all rounds", font_size=28, color=E.ACCENT).move_to(rlabel)
                anims = [Transform(rlabel, new_r)]
                for j in range(4):
                    anims += [Transform(bars[j], st[j][0]), Transform(vals[j], st[j][1])]
                if r:
                    anims.append(FadeOut(notes[r - 1]))
                anims.append(FadeIn(notes[r]))
                self.play(*anims, run_time=1.2)
        self.clear_scene()

    def inverse(self):
        a = load("leontief")
        eq = MathTex(r"x = f + A f + A^2 f + A^3 f + \cdots", r"= (I - A)^{-1} f", font_size=44)
        eq.to_edge(UP, buff=0.5)
        lm = self._matrix(a["L"], lambda v: f"{v:.3f}" if abs(v) > 5e-4 else "0", font_size=26)
        lm.move_to(LEFT * 1.0 + UP * 0.2)
        ll = label(r"Leontief's inverse: \ column $j$ is everything needed for \$1 more of $j$", font_size=24,
                   color=GREY_A).next_to(lm, UP, buff=0.3)
        mults = VGroup(*[label(f"{v:.2f}", font_size=28, color=IND_COLOR[IND[j]]) for j, v in
                         enumerate(a["multipliers"])])
        for j, t in enumerate(mults):
            t.move_to(lm.heads_c[j].get_center() + DOWN * (0.65 + 4 * 0.7 + 0.1))
        rule = Line(lm.cells[12].get_left() + DOWN * 0.38 + LEFT * 0.3, lm.cells[15].get_right() + DOWN * 0.38 +
                    RIGHT * 0.3, color=GREY_C)
        ml = label(r"output multipliers", font_size=22, color=E.ACCENT).next_to(mults, LEFT, buff=0.5)
        uses = VGroup(
            label(r"wartime planning: \ how much steel for so many ships", font_size=23, color=GREY_A),
            label(r"the Nobel prize, \ 1973", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        tag = island_tag(r"simulated: the Island, year 3", corner=DR, font_size=16)
        with self.voiceover(
            "All the rounds at once is a matrix sum: the order, plus what the order needs, plus what that needs, "
            "and so on. <bookmark mark='a'/> Because each round shrinks, the sum converges, to a single matrix "
            "Leontief could compute directly: the inverse of the identity minus the coefficients. "
            "<bookmark mark='b'/> Each column says what every business must produce to deliver one more dollar of "
            "one product. <bookmark mark='c'/> Add up a column and you get that product's output multiplier: a "
            f"dollar of fish needs {a['multipliers'][0]:.2f} dollars of output in all, a dollar of passages on the "
            f"ferry {a['multipliers'][3]:.2f}. <bookmark mark='d'/> The same arithmetic answered how much steel and "
            "rubber a fleet of ships would need in the Second World War, and won Leontief the Nobel prize in "
            "1973."
        ) as vo:
            self.play(Write(eq[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq[1]))
            vo.wait_until("b")
            self.play(FadeIn(ll), FadeIn(lm.heads_c), FadeIn(lm.heads_r),
                      LaggedStart(*[FadeIn(c) for c in lm.cells], lag_ratio=0.04), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(rule), FadeIn(ml), LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in mults],
                                                              lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(uses))
        self.clear_scene()

    def trade(self):
        a = load("leontief")
        k = 0.075
        x0 = -5.8
        gross = Rectangle(width=a["exports"] * k, height=0.9, stroke_color=E.WORLD, stroke_width=2, fill_opacity=0)
        gross.move_to([x0 + a["exports"] * k / 2, 1.2, 0])
        gl = label(rf"the Island's exports: \ \${a['exports']:.0f}", font_size=26, color=E.WORLD)
        gl.next_to(gross, UP, buff=0.2).align_to(gross, LEFT)
        va = Rectangle(width=a["va_exports"] * k, height=0.9, stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.85)
        va.move_to([x0 + a["va_exports"] * k / 2, 1.2, 0])
        vl = label(rf"value added on the Island: \ \${a['va_exports']:.0f} \ ({pct(a['va_share_exports'], 0)})",
                   font_size=24, color=BACKGROUND).move_to(va)
        imp = label(r"the rest: \\ imported nets, \\ nails, fuel", font_size=21, color=E.WORLD)
        imp.next_to(gross, RIGHT, buff=0.2)
        lesson = VGroup(
            label(r"a phone assembled in one country is that country's export, \\ though its parts were made in "
                  r"many others", font_size=25),
            label(r"Leontief's inverse, \ run on world tables, \ re-measures trade by value added \\ (the OECD "
                  r"and WTO's database, since 2013)", font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 1.6)
        tag = island_tag(r"simulated: the Island, year 3; $v^\top (I-A)^{-1} f_X$", corner=DR, font_size=16)
        with self.voiceover(
            "The inverse also answers a question about trade. <bookmark mark='a'/> The Island exports 120 dollars "
            "of fish and coconuts. But how much of that was made on the Island? <bookmark mark='b'/> Trace every "
            "export back through all its rounds of inputs, and keep only the value added at home along the way: "
            f"{a['va_exports']:.0f} dollars, {say_pct(a['va_share_exports'], 0)}. The rest is the imported nets, "
            "nails and fuel buried inside the fish. <bookmark mark='c'/> For the world this matters a great deal. "
            "A phone assembled in one country counts in the trade statistics as that country's export, though "
            "its parts were made in many others. <bookmark mark='d'/> Since 2013 the OECD and the World Trade "
            "Organization have published trade measured by value added, using Leontief's method on tables of the "
            "whole world. We'll use them in Part 36."
        ) as vo:
            self.play(FadeIn(tag), Create(gross), FadeIn(gl))
            vo.wait_until("a")
            self.play(Indicate(gl, color=E.WORLD))
            vo.wait_until("b")
            self.play(GrowFromEdge(va, LEFT), FadeIn(vl), run_time=1.5)
            self.play(FadeIn(imp))
            vo.wait_until("c")
            self.play(FadeIn(lesson[0]))
            vo.wait_until("d")
            self.play(FadeIn(lesson[1]))
        self.clear_scene()
