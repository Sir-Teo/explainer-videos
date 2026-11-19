from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403


class Budget(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The budget and the best bundle", r"Of everything someone can afford, which do they choose?",
             "Chapter five. The budget and the best bundle.", lit=("households", "firms"))
        self.budget()
        self.tangency()
        self.lagrange()

    def _axes(self):
        return goods_axes(center=LEFT * 2.9 + DOWN * 0.2, top=21, ticks=(0, 5, 10, 15, 20), x_length=5.4,
                          y_length=5.4)

    def budget(self):
        t = load("tangency")
        ax = self._axes()
        a = ax.ax
        A, B = t["m"] / t["px"], t["m"] / t["py"]
        tri = Polygon(a.c2p(0, 0), a.c2p(A, 0), a.c2p(0, B), stroke_width=0, fill_color=BUDGET, fill_opacity=0.15)
        ln = budget_line(ax, A, B)
        cheaper = DashedLine(a.c2p(A * 1.5, 0), a.c2p(0, B), color=BUDGET, stroke_width=2.5)
        top_y = 21.0                      # the richer line leaves the frame at the top: stop it there
        richer = DashedLine(a.c2p(A * 1.25, 0), a.c2p(A * 1.25 * (1 - top_y / (B * 1.25)), top_y), color=GREY_B,
                            stroke_width=2.5)
        rows = VGroup(
            MathTex(rf"p_x x + p_y y \le m:\quad {t['px']:.0f}x + {t['py']:.0f}y \le {t['m']:.0f}", font_size=34),
            label(rf"Bo's \${t['m']:.0f}: \ fish \${t['px']:.0f}, \ coconuts \${t['py']:.0f}", font_size=24,
                  color=WHO["bo"]),
            label(rf"the slope: \ $-p_x/p_y = -{t['px'] / t['py']:.2f}$: \\ the market's rate of exchange",
                  font_size=24, color=BUDGET),
            label(r"cheaper fish: \ the line swings out along the fish axis", font_size=22, color=BUDGET),
            label(r"more money: \ it moves out, parallel", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            f"Tastes are half of a choice. The other half is what a person can afford. <bookmark mark='a'/> Bo has "
            f"{t['m']:.0f} dollars; fish cost {t['px']:.0f} dollars and coconuts {t['py']:.0f}. Everything he can "
            "afford is this triangle, and the bundles that use all his money lie on its edge, the budget line. "
            "<bookmark mark='b'/> Its slope is the price of fish in coconuts: the rate at which the market lets him "
            "trade one for the other. <bookmark mark='c'/> If fish gets cheaper, the line swings out along the fish "
            "axis. <bookmark mark='d'/> If Bo gets more money, it moves out without turning."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(tri), Create(ln))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), Indicate(ln, color=BUDGET))
            vo.wait_until("c")
            self.play(Create(cheaper), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeOut(cheaper), Create(richer), FadeIn(rows[4]))
        self.clear_scene()

    def tangency(self):
        t = load("tangency")
        ax = self._axes()
        a = ax.ax
        A, B = t["m"] / t["px"], t["m"] / t["py"]
        ln = budget_line(ax, A, B)
        xs = np.array(t["xs"])
        ics = VGroup(*[curve(ax, xs, np.array(t[k]), color=IC, width=w, top=21)
                       for k, w in (("ic_low", 2), ("ic", 4), ("ic_high", 2))])
        pref = cs.Preference("cobb-douglas", a=0.6)
        xv = ValueTracker(2.0)
        dot = always_redraw(lambda: Dot(a.c2p(xv.get_value(), B - B / A * xv.get_value()), radius=0.1, color=WHITE))
        uval = always_redraw(lambda: VGroup(
            label(r"utility here:", font_size=22, color=GREY_A),
            DecimalNumber(float(pref.u(xv.get_value(), B - B / A * xv.get_value())), num_decimal_places=2,
                          font_size=30, color=IC)).arrange(RIGHT, buff=0.2).move_to(RIGHT * 3.6 + UP * 2.6))
        rows = VGroup(
            label(rf"best: \ {t['x']:.0f} fish and {t['y']:.0f} coconuts", font_size=26, color=WHITE),
            MathTex(r"\text{MRS} = \frac{p_x}{p_y}", font_size=40, color=E.ACCENT),
            label(rf"Bo's rate of trade, \ {t['mrs']:.2f} coconuts per fish, \\ equals the market's, \ "
                  rf"\${t['px']:.0f}/\${t['py']:.0f}", font_size=23),
            label(r"if they differed, \ trading along the line \\ would make him better off", font_size=23,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(uval, DOWN, buff=0.5).align_to(uval, LEFT)
        rows.to_edge(RIGHT, buff=0.45)
        tag = island_tag(r"simulated: Bo's tastes, Cobb--Douglas, 60\% of spending on fish", corner=DR, font_size=14)
        with self.voiceover(
            "Now put the two halves together. <bookmark mark='a'/> Here are three of Bo's indifference curves. "
            "<bookmark mark='b'/> Slide along his budget line. Near the coconut end, each step toward fish raises "
            "his utility. <bookmark mark='c'/> Past a certain point it starts to fall. <bookmark mark='d'/> The best "
            f"bundle is where the budget line just touches the highest curve it can reach: {t['x']:.0f} fish and "
            f"{t['y']:.0f} coconuts. <bookmark mark='e'/> There the curve and the line have the same slope: Bo's "
            "rate of trade equals the market's. If they differed, say Bo valued a fish at two coconuts while the "
            "market charged one and a third, he'd gain by buying another fish and fewer coconuts, and he'd keep "
            "going until the two rates met."
        ) as vo:
            self.play(FadeIn(ax), Create(ln), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in ics], lag_ratio=0.3))
            vo.wait_until("b")
            self.add(dot, uval)
            self.play(xv.animate.set_value(t["x"]), run_time=3.0)
            vo.wait_until("c")
            self.play(xv.animate.set_value(13.5), run_time=2.0)
            vo.wait_until("d")
            self.play(xv.animate.set_value(t["x"]), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("e")
            self.play(Write(rows[1]), FadeIn(rows[2]))
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lagrange(self):
        t = load("tangency")
        eqs = VGroup(
            MathTex(r"\mathcal{L} = u(x, y) + \lambda\,(m - p_x x - p_y y)", font_size=42),
            MathTex(r"\frac{\partial u}{\partial x} = \lambda p_x, \qquad \frac{\partial u}{\partial y} = \lambda p_y",
                    font_size=40),
            MathTex(r"\lambda = \frac{\partial u/\partial x}{p_x} = \frac{\partial u/\partial y}{p_y}", font_size=40,
                    color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 1.2)
        rows = VGroup(
            label(r"each good's last dollar buys the same extra utility: \ $\lambda$", font_size=26),
            label(rf"Bo's $\lambda$: \ {t['lam']:.3f}; \ one more dollar raises his utility by {t['du_one_dollar']:.3f}",
                  font_size=26, color=E.ACCENT),
            label(r"the multiplier is the value of relaxing the constraint: \ a shadow price, \ here of money",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The same answer comes out of algebra, by a method of Joseph-Louis Lagrange. <bookmark mark='a'/> Add "
            "the budget to the utility with a multiplier, lambda, and set the derivatives to zero. "
            "<bookmark mark='b'/> The conditions say the last dollar spent on fish buys the same extra utility as "
            "the last dollar spent on coconuts, and that common amount is lambda. <bookmark mark='c'/> Lambda has a "
            f"meaning of its own. Give Bo one more dollar, and his utility rises by {t['du_one_dollar']:.3f}, "
            "exactly lambda. <bookmark mark='d'/> It is the value of loosening the constraint, a shadow price. "
            "Shadow prices will come back whenever something scarce has no market price: a firm's capacity, a "
            "country's pollution permits, your time."
        ) as vo:
            self.play(Write(eqs[0]))
            vo.wait_until("a")
            self.play(Write(eqs[1]))
            vo.wait_until("b")
            self.play(Write(eqs[2]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
