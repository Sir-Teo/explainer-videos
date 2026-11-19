from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403


class Demand(VoiceoverScene):
    def construct(self):
        card(self, 2, r"The demand function", r"How does the best bundle move when a price or an income moves?",
             "Chapter two. The demand function.")
        self.price_path()
        self.income_path()
        self.homogeneity()
        self.elasticities()

    def price_path(self):
        b = load("bo")
        a_, m, py = b["a"], b["m"], b["py"]
        ax = goods_axes(center=LEFT * 3.4 + DOWN * 0.35, top=13, x_length=5.0, y_length=5.0)
        a = ax.ax
        from explainer.ai.viz import axes

        dax = axes([0, 13], [0, 16], x_length=5.0, y_length=5.0, xticks=[0, 4, 8, 12], yticks=[0, 4, 8, 12, 16],
                   xlabel=r"fish bought", ylabel=r"price of fish (\$)", font_size=18,
                   center=RIGHT * 3.3 + DOWN * 0.35)
        d = dax.ax
        p = ValueTracker(15.0)

        def bundle(pp):
            return a_ * m / pp, (1 - a_) * m / py

        line = always_redraw(lambda: Line(a.c2p(min(m / p.get_value(), 13), 0 if m / p.get_value() <= 13 else
                                                (m - 13 * p.get_value()) / py), a.c2p(0, m / py), color=BUDGET,
                                          stroke_width=3))
        u_of = lambda pp: bundle(pp)[0] ** a_ * bundle(pp)[1] ** (1 - a_)  # noqa: E731
        xs = np.linspace(0.6, 13, 160)

        def ic():
            u = u_of(p.get_value())
            ys = (u / xs ** a_) ** (1 / (1 - a_))
            return curve(ax, xs, ys, color=IC, width=2.5)

        icv = always_redraw(ic)
        dot = always_redraw(lambda: Dot(a.c2p(*bundle(p.get_value())), radius=0.09, color=CHOICE))
        trail = TracedPath(lambda: a.c2p(*bundle(p.get_value())), stroke_color=E.ACCENT, stroke_width=3)
        ddot = always_redraw(lambda: Dot(d.c2p(bundle(p.get_value())[0], p.get_value()), radius=0.09,
                                         color=E.ACCENT))
        dtrail = TracedPath(lambda: d.c2p(bundle(p.get_value())[0], p.get_value()), stroke_color=E.ACCENT,
                            stroke_width=4)
        plab = always_redraw(lambda: label(rf"fish \${p.get_value():.2f}", font_size=22, color=BUDGET).move_to(
            a.c2p(9.5, 12.0)))
        heads = VGroup(label(r"Bo's choices", font_size=24, color=WHO["bo"]).next_to(ax, UP, buff=0.15),
                       label(r"his demand curve for fish", font_size=24, color=E.ACCENT).next_to(dax, UP, buff=0.15))
        pcc = label(r"the price-consumption curve", font_size=19, color=E.ACCENT).move_to(a.c2p(7.5, 2.9))
        formula = MathTex(r"x(p) = \frac{0.6 \times 60}{p} = \frac{36}{p}", font_size=34,
                          color=E.ACCENT).move_to(d.c2p(8.5, 12.5))
        tag = island_tag(r"Bo: 60\% of \$60 on fish (Part 5)", corner=DR, font_size=15)
        with self.voiceover(
            "Part five ended with one choice: the best bundle on one budget. A demand function says how that "
            "choice moves. <bookmark mark='a'/> Here is Bo again, who always spends sixty percent of his sixty "
            "dollars on fish. Coconuts cost six dollars; the price of fish will slide from fifteen dollars down to "
            "two fifty. <bookmark mark='b'/> As fish get cheaper, the budget line swings out along the fish axis, "
            "and Bo's best bundle moves with it. Its path is the price-consumption curve. "
            "<bookmark mark='c'/> Now plot each price against the fish Bo buys at it, on a second picture with "
            "the price going up the side, as Marshall drew it. That is Bo's demand curve for fish. "
            "<bookmark mark='d'/> For Bo it has a formula: thirty-six dollars divided by the price. He spends the "
            "same thirty-six dollars on fish whatever they cost."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(dax), FadeIn(heads), FadeIn(tag))
            vo.wait_until("a")
            self.add(line, icv, dot, plab)
            self.play(FadeIn(line), FadeIn(dot))
            vo.wait_until("b")
            self.add(trail)
            self.play(p.animate.set_value(6.0), run_time=5.0, rate_func=smooth)
            self.play(FadeIn(pcc))
            vo.wait_until("c")
            p.set_value(15.0)
            self.remove(trail)
            trail2 = TracedPath(lambda: a.c2p(*bundle(p.get_value())), stroke_color=E.ACCENT, stroke_width=3)
            self.add(trail2, dtrail, ddot)
            self.play(p.animate.set_value(2.8), run_time=6.0, rate_func=smooth)
            vo.wait_until("d")
            self.play(FadeIn(formula))
        self.clear_scene()

    def income_path(self):
        b = load("bo")
        a_, py, px = b["a"], b["py"], 10.0
        ax = goods_axes(center=LEFT * 3.4 + UP * 0.3, top=13, x_length=4.5, y_length=4.5)
        a = ax.ax
        from explainer.ai.viz import axes

        eax = axes([0, 80], [0, 5], x_length=4.5, y_length=4.5, xticks=[0, 20, 40, 60, 80], yticks=[0, 1, 2, 3, 4, 5],
                   xlabel=r"income (\$)", ylabel=r"fish bought", font_size=18, center=RIGHT * 3.3 + UP * 0.3)
        e = eax.ax
        m = ValueTracker(20.0)

        def bundle(mm):
            return a_ * mm / px, (1 - a_) * mm / py

        line = always_redraw(lambda: Line(a.c2p(m.get_value() / px, 0), a.c2p(0, m.get_value() / py), color=BUDGET,
                                          stroke_width=3))
        dot = always_redraw(lambda: Dot(a.c2p(*bundle(m.get_value())), radius=0.09, color=CHOICE))
        trail = TracedPath(lambda: a.c2p(*bundle(m.get_value())), stroke_color=HICKS, stroke_width=3)
        edot = always_redraw(lambda: Dot(e.c2p(m.get_value(), bundle(m.get_value())[0]), radius=0.09, color=HICKS))
        etrail = TracedPath(lambda: e.c2p(m.get_value(), bundle(m.get_value())[0]), stroke_color=HICKS,
                            stroke_width=4)
        heads = VGroup(label(r"fish \$10, \ coconuts \$6; \ income grows", font_size=22, color=WHO["bo"]).next_to(
            ax, UP, buff=0.15), label(r"his Engel curve for fish", font_size=24, color=HICKS).next_to(eax, UP,
                                                                                                    buff=0.15))
        icc = label(r"income-consumption \\ curve: \ a ray", font_size=19, color=HICKS).move_to(a.c2p(9.5, 9.5))
        kinds = VGroup(
            label(r"a ray, \ for Bo: \ shares don't change with income", font_size=23, color=HICKS),
            label(r"bends toward a good: \ a luxury", font_size=23, color=GREY_A),
            label(r"bends back: \ an inferior good \ (Play it's coconuts)", font_size=23, color=GIFF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Hold the prices still and let income grow instead. <bookmark mark='a'/> The budget line moves out "
            "without turning, and the best bundle moves along the income-consumption curve. For Bo it's a straight "
            "ray from the origin, because he spends the same shares whatever his income. "
            "<bookmark mark='b'/> Plot income against the fish he buys, and you have an Engel curve, named after "
            "Ernst Engel, whom we'll meet in chapter seven. <bookmark mark='c'/> Most people's curves are not rays. "
            "When the curve bends toward a good, the good is a luxury: its share of spending rises with income. "
            "When it bends back, so that a richer household buys less of the good, the good is inferior. Play it's "
            "coconuts were one: with more money you'd have bought fewer coconuts and more fish."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(eax), FadeIn(heads))
            self.add(line, dot)
            vo.wait_until("a")
            self.add(trail, etrail, edot)
            self.play(m.animate.set_value(76.0), run_time=6.0, rate_func=smooth)
            self.play(FadeIn(icc))
            vo.wait_until("b")
            self.play(Indicate(heads[1], color=HICKS))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.1) for k in kinds], lag_ratio=0.5), run_time=2.5)
        self.clear_scene()

    def homogeneity(self):
        b = load("bo")
        ax = goods_axes(center=LEFT * 3.4 + DOWN * 0.3, top=13, x_length=5.0, y_length=5.0)
        a = ax.ax
        l1 = budget_line(ax, 6.0, 10.0)
        dot = Dot(a.c2p(*b["A"]), radius=0.1, color=CHOICE)
        rows = VGroup(
            MathTex(r"p_x = 10,\; p_y = 6,\; m = 60 \;\;\Rightarrow\;\; (3.6,\ 4)", font_size=34),
            MathTex(r"p_x = 20,\; p_y = 12,\; m = 120 \;\;\Rightarrow\;\; (3.6,\ 4)", font_size=34, color=E.ACCENT),
            MathTex(r"x(t\,p,\ t\,m) = x(p,\ m)", font_size=42, color=HICKS),
            label(r"demand is homogeneous of degree zero: \\ no money illusion", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=0.6)
        rows[2:].shift(DOWN * 0.25)
        lab = label(r"the same line, \ twice over", font_size=21, color=BUDGET).next_to(a.c2p(4.5, 8.5), RIGHT,
                                                                                       buff=0.1)
        with self.voiceover(
            "One property every demand function has. <bookmark mark='a'/> At fish ten dollars, coconuts six, and "
            "sixty dollars of income, Bo buys three point six fish and four coconuts. <bookmark mark='b'/> Double "
            "every price and his income too. The budget line doesn't move at all: twelve dollars a coconut and a "
            "hundred and twenty dollars still buy ten coconuts. So his choice can't move either. "
            "<bookmark mark='c'/> Demand depends only on prices relative to income: it is homogeneous of degree "
            "zero. If the Island counted its money in cents instead of dollars, nobody's shopping would change. "
            "A consumer who behaved otherwise would suffer from what Irving Fisher called money illusion."
        ) as vo:
            self.play(FadeIn(ax), Create(l1), FadeIn(dot))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(l1, color=E.ACCENT), FadeIn(lab))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.clear_scene()

    def elasticities(self):
        b = load("bo")
        defs = VGroup(
            MathTex(r"\varepsilon_{xx} = \frac{\partial x}{\partial p_x}\frac{p_x}{x}", font_size=38),
            MathTex(r"\varepsilon_{xy} = \frac{\partial x}{\partial p_y}\frac{p_y}{x}", font_size=38),
            MathTex(r"\eta_{x} = \frac{\partial x}{\partial m}\frac{m}{x}", font_size=38),
        ).arrange(RIGHT, buff=0.9).to_edge(UP, buff=0.7)
        names = VGroup(label(r"own price", font_size=22, color=E.ACCENT), label(r"cross price", font_size=22,
                                                                                color=GREY_A),
                       label(r"income", font_size=22, color=HICKS))
        for n_, d_ in zip(names, defs):
            n_.next_to(d_, DOWN, buff=0.2)
        bo = label(rf"Bo: \ own ${b['own']:+.0f}$, \ cross ${abs(b['cross']):.0f}$, \ income ${b['income_el']:+.0f}$:"
                   r" \ 1\% dearer fish, \ 1\% fewer fish", font_size=27, color=WHO["bo"]).next_to(names, DOWN,
                                                                                               buff=0.55)
        rules = VGroup(
            VGroup(MathTex(r"\textstyle\sum_j \varepsilon_{ij} + \eta_i = 0", font_size=40),
                   label(r"homogeneity: \ raise every price and income 1\%, \ nothing moves", font_size=24,
                         color=GREY_A)).arrange(RIGHT, buff=0.4),
            VGroup(MathTex(r"\textstyle\sum_i w_i\,\eta_i = 1", font_size=40),
                   label(r"Engel aggregation: \ not everything can be a luxury", font_size=24,
                         color=GREY_A)).arrange(RIGHT, buff=0.4),
            VGroup(MathTex(r"\textstyle\sum_i w_i\,\varepsilon_{ij} = -w_j", font_size=40),
                   label(r"Cournot aggregation: \ the budget still adds up after a price change", font_size=24,
                         color=GREY_A)).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(bo, DOWN, buff=0.55)
        note_ = label(r"$w_i$: \ the share of the budget spent on good $i$", font_size=22, color=GREY_B).to_edge(
            DOWN, buff=0.4)
        head = VGroup(label(r"elasticities", font_size=44, color=E.ACCENT),
                      label(r"percent change per percent change: \ the units drop out", font_size=28,
                            color=GREY_A)).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Economists summarize demand with elasticities: percent changes per percent change, so the units drop "
            "out. <bookmark mark='a'/> The own-price elasticity: how much the quantity moves when the good's own "
            "price moves. The cross-price elasticity: when another good's price moves. The income elasticity: when "
            "income moves. <bookmark mark='b'/> Bo's are minus one, zero and one: fish one percent dearer means one "
            "percent fewer fish, the price of coconuts doesn't touch his fish, and one percent more income buys one "
            "percent more. <bookmark mark='c'/> And three rules hold for everyone. Homogeneity again: the "
            "elasticities with respect to all prices and income add to zero. <bookmark mark='d'/> Weighted by "
            "budget shares, income elasticities average exactly one: a household can't spend more than all of an "
            "extra dollar, so not everything can be a luxury. <bookmark mark='e'/> And when one price changes, the "
            "budget still has to add up, which ties the price elasticities together too."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeOut(head), LaggedStart(*[FadeIn(VGroup(d_, n_)) for d_, n_ in zip(defs, names)],
                                                 lag_ratio=0.5), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(bo))
            vo.wait_until("c")
            self.play(FadeIn(rules[0]), FadeIn(note_))
            vo.wait_until("d")
            self.play(FadeIn(rules[1]))
            vo.wait_until("e")
            self.play(FadeIn(rules[2]))
        self.clear_scene()
