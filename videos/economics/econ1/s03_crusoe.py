from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403


class Crusoe(VoiceoverScene):
    def construct(self):
        card(self, 2, r"One person, two goods", r"What does anything cost, when there is nobody to buy it from?",
             "Chapter two. One person, two goods.", scale=("person",), horizon=("a day",))
        self.alone()
        self.hours()
        self.frontier()
        self.margin()
        self.best_day()

    # ------------------------------------------------------------------
    def alone(self):
        isl = island_shape(7.4, 3.6).move_to(DOWN * 0.3)
        man = islander("crusoe", 0.9, name=True).move_to(isl.get_center() + LEFT * 0.4 + DOWN * 0.1)
        trees = VGroup(*[palm(1.5).move_to(isl.get_center() + RIGHT * dx + UP * dy) for dx, dy in
                         ((1.9, 0.5), (2.6, -0.2), (1.2, -0.6))])
        fishes = VGroup(*[fish_glyph(0.45).move_to(isl.get_center() + p) for p in
                          ((-4.3, 0.9, 0), (-4.7, -0.6, 0), (-3.6, -1.7, 0), (4.4, 1.6, 0))])
        day = label(r"10 hours a day", font_size=32, color=CRUSOE).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Strip an economy down as far as it will go. One person, alone on an island. Call him Crusoe. "
            "<bookmark mark='a'/> He has ten hours of daylight to work with, and two things he can do with them: "
            "<bookmark mark='b'/> fish from the rocks, or gather coconuts from the palms. There are no prices, "
            "because there is nobody to trade with. And yet every choice he makes has a cost, and we can measure "
            "it."
        ) as vo:
            self.play(FadeIn(isl), FadeIn(man, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(day))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in fishes], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(tr) for tr in trees], lag_ratio=0.2), run_time=2)
        self.play(VGroup(isl, man, trees, fishes, day).animate.scale(0.4).to_corner(UL, buff=0.25))
        self.island_small = VGroup(isl, man, trees, fishes, day)

    def hours(self):
        d = load("crusoe")
        rows = d["hours"]
        ax = axes([0.4, 10.6], [0, 3.2], x_length=5.6, y_length=3.0, xticks=list(range(1, 11)),
                  yticks=[0, 1, 2, 3], xlabel=r"hour of fishing", font_size=18, center=[-3.3, -1.4, 0])
        ax2 = axes([0.4, 10.6], [0, 4.2], x_length=5.6, y_length=3.0, xticks=list(range(1, 11)),
                   yticks=[0, 1, 2, 3, 4], xlabel=r"hour of fishing", font_size=18, center=[3.5, -1.4, 0])
        bars_f = VGroup(*[Rectangle(width=0.36, height=ax.ax.c2p(0, r["fish"])[1] - ax.ax.c2p(0, 0)[1],
                                    stroke_width=0, fill_color=E.FISH, fill_opacity=0.9)
                          .move_to(ax.ax.c2p(r["hour"], r["fish"] / 2)) for r in rows])
        bars_c = VGroup(*[Rectangle(width=0.36, height=ax2.ax.c2p(0, r["coconuts"])[1] - ax2.ax.c2p(0, 0)[1],
                                    stroke_width=0, fill_color=E.COCONUT, fill_opacity=0.9)
                          .move_to(ax2.ax.c2p(r["hour"], r["coconuts"] / 2)) for r in rows])
        t1 = label(r"fish that the hour adds", font_size=24, color=E.FISH).next_to(ax.ax, UP, buff=0.2)
        t2 = label(r"coconuts that the hour costs", font_size=24, color=E.COCONUT).next_to(ax2.ax, UP, buff=0.2)
        p = d["params"]
        law = MathTex(r"F = 3\sqrt{h}", r"\qquad", r"C = 4\sqrt{10 - h}", font_size=40)
        law[0].set_color(E.FISH)
        law[2].set_color(E.COCONUT)
        law.to_edge(UP, buff=0.55).shift(RIGHT * 1.8)
        lab = label(r"$h$: hours spent fishing; \ the rest go to the palms", font_size=22, color=GREY_A)
        lab.next_to(law, DOWN, buff=0.15)
        tag = illustrative_tag(r"the Island's technology: illustrative numbers", font_size=17)
        first, last = rows[0], rows[-1]
        with self.voiceover(
            "Suppose his catch grows with the square root of the hours he spends at it, and so does his harvest. "
            "Three fish times the square root of the hours fishing, four coconuts times the square root of the "
            "hours left over. <bookmark mark='a'/> Then the first hour of fishing brings in "
            f"{first['fish']:.0f} fish, the second only {rows[1]['fish']:.2f} more, and the tenth "
            f"{last['fish']:.2f}. The easy fish are caught first. Economists call this diminishing returns. "
            "<bookmark mark='b'/> And every hour he fishes is an hour he doesn't spend at the palms. Moving the "
            f"first hour to fishing costs him {first['coconuts']:.2f} of a coconut. Moving the last one costs "
            f"{last['coconuts']:.0f} whole coconuts, because by then that hour is the only one he has left for "
            "climbing."
        ) as vo:
            self.play(Write(law), FadeIn(lab), FadeIn(tag))
            self.play(FadeIn(ax), FadeIn(t1))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_f], lag_ratio=0.25), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(ax2), FadeIn(t2))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_c], lag_ratio=0.25), run_time=3)
        self.play(FadeOut(VGroup(ax, ax2, bars_f, bars_c, t1, t2, lab, tag)), law.animate.scale(0.8).to_corner(UR,
                                                                                                          buff=0.4))
        self.law = law

    def frontier(self):
        d = load("crusoe")
        ax = axes([0, 10], [0, 13], x_length=6.2, y_length=5.4, xticks=[0, 2, 4, 6, 8, 10],
                  yticks=[0, 4, 8, 12], xlabel=r"fish a day", font_size=20, center=[-2.6, -0.35, 0])
        ylab = label(r"coconuts a day", font_size=22, color=GREY_A).next_to(ax.ax, UP, buff=0.15).align_to(ax.ax,
                                                                                                         LEFT)
        h = ValueTracker(0.0)
        fx = lambda x: 3 * np.sqrt(x)  # noqa: E731
        cx = lambda x: 4 * np.sqrt(10 - x)  # noqa: E731
        dot = always_redraw(lambda: Dot(ax.ax.c2p(fx(h.get_value()), cx(h.get_value())), radius=0.09, color=CRUSOE))
        trace = VMobject(stroke_color=CRUSOE, stroke_width=5)
        trace.set_points_as_corners([ax.ax.c2p(fx(0), cx(0)), ax.ax.c2p(fx(0), cx(0))])

        def grow(m):
            hs = np.linspace(0, h.get_value(), max(2, int(60 * h.get_value() / 10) + 2))
            m.set_points_smoothly([ax.ax.c2p(fx(x), cx(x)) for x in hs])

        trace.add_updater(grow)
        readout = always_redraw(lambda: label(rf"{h.get_value():.1f} hours fishing", font_size=24,
                                              color=CRUSOE).move_to([3.6, 2.4, 0]))
        frontier_name = label(r"what he can have: \ the production possibilities frontier", font_size=24,
                              color=CRUSOE).move_to([3.6, 1.7, 0])
        with self.voiceover(
            "Now put all ten hours together. Every way of splitting the day gives one pair of numbers, so many "
            "fish and so many coconuts. <bookmark mark='a'/> All coconuts and no fish is here. Move the hours "
            "across to fishing, one by one, and trace the pairs. <bookmark mark='b'/> The curve is what he can "
            "have. Anything inside it he can do, anything outside it he can't, and that line between the two is "
            "what economists mean by scarcity. It's called the production possibilities frontier. "
            "<bookmark mark='c'/> And notice its shape. It bows outward, because of diminishing returns: the more "
            "he fishes, the more coconuts each extra fish costs him."
        ) as vo:
            self.play(FadeOut(self.island_small), FadeIn(ax), FadeIn(ylab))
            vo.wait_until("a")
            self.add(trace, dot, readout)
            self.play(h.animate.set_value(10.0), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(frontier_name))
        trace.clear_updaters()
        self.remove(readout)
        self.frontier_axes, self.trace, self.dot_h = ax, trace, h
        self.ylab, self.frontier_name = ylab, frontier_name
        self.remove(dot)

    def margin(self):
        d = load("crusoe")
        ax = self.frontier_axes.ax
        marks = d["marks"]
        rows = VGroup(
            MathTex(r"\text{opportunity cost of a fish}", r"=", r"-\frac{dC}{dF}", font_size=34),
            MathTex(r"=", r"\frac{dC/dh_{\text{palms}}}{dF/dh_{\text{fish}}}", r"=",
                    r"\frac{b\,/\,2\sqrt{10-h}}{a\,/\,2\sqrt{h}}", font_size=34),
            MathTex(r"=", r"\frac{4}{3}\sqrt{\frac{h}{10-h}}", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.4, 0.0, 0])
        rows[1].shift(RIGHT * 0.25)
        rows[2].shift(RIGHT * 0.25)
        tangents = VGroup()
        vals = VGroup()
        for k, (hh, col) in enumerate(((2.0, GREY_A), (6.0, E.ACCENT), (9.0, GREY_A))):
            f, c = 3 * np.sqrt(hh), 4 * np.sqrt(10 - hh)
            s = -marks[str(hh)]["opportunity_cost"]
            dx = 1.2 / np.sqrt(1 + s * s)
            ln = Line(ax.c2p(f - dx, c - s * dx), ax.c2p(f + dx, c + s * dx), color=col, stroke_width=3)
            dt = Dot(ax.c2p(f, c), radius=0.07, color=col)
            v = label(rf"{marks[str(hh)]['opportunity_cost']:.2f}", font_size=24, color=col)
            v.next_to(dt, UR, buff=0.1)
            tangents.add(VGroup(ln, dt))
            vals.add(v)
        why_ = VGroup(label(r"the slope of the frontier", font_size=22, color=GREY_B),
                      label(r"coconuts given up for one more fish", font_size=22, color=GREY_B))
        why_.arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(rows, DOWN, buff=0.45).align_to(rows, LEFT)
        defs = definition_card(r"Opportunity cost", r"what you give up to get something: \ the best alternative "
                               r"you could have had instead", color=E.ACCENT, width=6.2, font_size=24)
        defs.move_to([3.4, -2.6, 0])
        with self.voiceover(
            "That rising cost is the slope of the frontier. <bookmark mark='a'/> The cost of one more fish, "
            "measured in coconuts, is how fast coconuts fall as fish rise. Each depends on the hours, so divide one "
            "rate by the other: the coconuts an hour at the palms would have brought, over the fish that hour "
            "brings at the rocks. <bookmark mark='b'/> With our numbers it comes to four thirds times the square "
            "root of the hours fishing over the hours left. <bookmark mark='c'/> At two hours of fishing, a fish "
            f"costs {marks['2.0']['opportunity_cost']:.2f} of a coconut. At six it costs "
            f"{marks['6.0']['opportunity_cost']:.2f}. At nine, {marks['9.0']['opportunity_cost']:.2f}. "
            "<bookmark mark='d'/> This is the first idea in economics, and the most important: the cost of "
            "anything is what you give up to get it. Economists call it opportunity cost. On an island with no "
            "money, nothing is free, and nothing has a price tag either. The cost is in the coconuts. "
            "<bookmark mark='e'/> And notice which question Crusoe actually faces. It's never fish or coconuts. "
            "It's one more hour of which? Economists call this thinking at the margin."
        ) as vo:
            self.play(FadeOut(self.frontier_name))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(why_))
            vo.wait_until("c")
            for t, v in zip(tangents, vals):
                self.play(Create(t[0]), FadeIn(t[1]), FadeIn(v), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeOut(why_), FadeIn(defs, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(Indicate(tangents[1], color=E.ACCENT))
        self.clear_scene(self.frontier_axes, self.trace, self.ylab)

    def best_day(self):
        d = load("crusoe")
        ax = self.frontier_axes.ax
        b = d["best"]
        th = d["params"]["theta"]
        u0 = b["u"]
        curves = VGroup()
        for du, op in ((-0.35, 0.45), (0.0, 1.0), (0.3, 0.45)):
            fs = np.linspace(0.4, 10, 120)
            cs = np.exp((u0 + du - th * np.log(fs)) / (1 - th))
            ok = cs <= 13.2
            curves.add(curve(ax, fs[ok], cs[ok], E.OUGHT, 3).set_stroke(opacity=op))
        pt = Dot(ax.c2p(b["fish"], b["coconuts"]), radius=0.1, color=E.ACCENT)
        eq = MathTex(r"U = 0.6\ln F + 0.4 \ln C", font_size=36, color=E.OUGHT).move_to([3.5, 2.3, 0])
        eq2 = MathTex(r"\underbrace{\frac{0.6/F}{0.4/C}}_{\text{what a fish is worth to him}}", r"=",
                      r"\underbrace{\frac{4}{3}\sqrt{\frac{h}{10-h}}}_{\text{what a fish costs him}}",
                      font_size=32).move_to([3.5, 0.5, 0])
        res = label(rf"best: \ {b['h']:.0f} hours fishing, \ {b['fish']:.2f} fish and {b['coconuts']:.1f} "
                    rf"coconuts", font_size=24, color=E.ACCENT).move_to([3.5, -1.3, 0])
        res2 = label(rf"both sides $=$ {b['mrs']:.2f} coconuts a fish", font_size=24, color=GREY_A).next_to(res, DOWN,
                                                                                                        buff=0.15)
        pay = label(r"wants are built properly in Part 5", font_size=22, color=GREY_B).move_to([3.5, -2.6, 0])
        with self.voiceover(
            "So which point does he pick? That depends on what he wants. <bookmark mark='a'/> Give him a liking for "
            "both, a little more for fish, written as a utility function. Each pink curve joins the days he likes "
            "equally well. <bookmark mark='b'/> His best day is where one of those curves just touches the "
            "frontier. There, two slopes are equal: what one more fish is worth to him, in coconuts, and what it "
            f"costs him. <bookmark mark='c'/> With these numbers it's {b['h']:.0f} hours of fishing, for "
            f"{b['fish']:.1f} fish and {b['coconuts']:.0f} coconuts, and both slopes come to {b['mrs']:.2f}. "
            "<bookmark mark='d'/> That one condition, worth equals cost at the margin, will come back again and "
            "again. In Part five we build the theory of what people want properly. For now, notice that we found "
            "Crusoe's best day without a single price. The prices come in with the second person."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(eq))
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(pt, scale=0.5), FadeIn(eq2))
            vo.wait_until("c")
            self.play(FadeIn(res), FadeIn(res2))
            vo.wait_until("d")
            self.play(FadeIn(pay))
        self.clear_scene()
