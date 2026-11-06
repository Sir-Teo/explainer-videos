from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Entropy(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Counting microstates", r"What is entropy?", lit=(1872, 1877), part=PART)
        with self.voiceover("Chapter eight. Counting microstates."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.clausius()
        self.box()
        self.counts()
        self.cells()

    def clausius(self):
        q = quote_card(r"The energy of the world is constant. \ The entropy of the world tends to a maximum.",
                       r"Rudolf Clausius", r"1865", width=9.6, font_size=28).to_edge(UP, buff=0.6)
        rows = stack([(r"the second law of thermodynamics: \ in an isolated system, \ entropy never decreases",
                       ENT),
                      (r"heat flows from hot to cold; \ gases spread; \ eggs break and stay broken", WHITE),
                      (r"but molecules obey time-symmetric laws: \ where does a one-way law come from?", GOAL)],
                     font_size=23, aligned_edge=LEFT, width=11.4, buff=0.35).move_to([0, -1.3, 0])
        with self.voiceover(
            "Return to the film of the gas. <bookmark mark='a'/>In 1865 Rudolf Clausius summed up "
            "thermodynamics in two sentences: the energy of the world is constant; the entropy of the world tends "
            "to a maximum. <bookmark mark='b'/>The second is the second law: in an isolated system, entropy never "
            "decreases. <bookmark mark='c'/>It is why heat flows from hot to cold, why gases spread, why eggs break "
            "and stay broken. <bookmark mark='d'/>But the gas is made of molecules obeying laws that run equally "
            "well in both directions. How can a one-way law come out of two-way laws? Ludwig Boltzmann spent his "
            "life on that question."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def box(self):
        head = label(r"Microstates and macrostates", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        box = (-3.0, 3.0, -2.0, 2.0)
        frame = Rectangle(width=6.0, height=4.0, color=GREY_B, stroke_width=2).move_to([-3.2, -0.4, 0])
        mid = DashedLine([-3.2, 1.6, 0], [-3.2, -2.4, 0], color=GREY_C)
        rng = np.random.default_rng(1877)
        n = 100
        p0 = np.column_stack([-3.0 + 3.0 * rng.random(n), -2.0 + 4.0 * rng.random(n)])
        a = rng.random(n) * 2 * np.pi
        v0 = np.column_stack([np.cos(a), np.sin(a)]) * (0.5 + rng.random(n))[:, None]
        t = ValueTracker(0.0)

        def pts():
            return gas_at(p0, v0, t.get_value(), box)

        dots = always_redraw(lambda: VGroup(*[Dot([x - 3.2, y - 0.4, 0], radius=0.055, color=ENT)
                                              for x, y in pts()]))
        count = always_redraw(lambda: label(rf"on the left: \ {int((pts()[:, 0] < 0).sum())}", font_size=22,
                                            color=CHANCE).next_to(frame, DOWN, buff=0.2))
        side = stack([(r"microstate: \ exactly where every molecule is \ (and how it moves)", WHITE),
                      (r"macrostate: \ what we can measure: \ here, \ how many are on the left", CHANCE),
                      (r"$W$: \ the number of microstates in a macrostate", ABS)], font_size=21,
                     aligned_edge=LEFT, width=5.4).move_to([3.8, 0.4, 0])
        f = MathTex(r"S = k_B \log W", font_size=46, color=ENT).move_to([3.8, -1.7, 0])
        tomb = label(r"on Boltzmann's grave in Vienna \ (in Planck's notation)", font_size=18,
                     color=GREY_A).next_to(f, DOWN, buff=0.2)
        with self.voiceover(
            "Boltzmann's answer begins with a distinction. <bookmark mark='a'/>A hundred molecules in a box, all "
            "starting in the left half. <bookmark mark='b'/>The microstate is everything: exactly where each "
            "molecule is and how it moves. <bookmark mark='c'/>The macrostate is what we can measure, here just how "
            "many molecules are on the left. Let them move. <bookmark mark='d'/>Many microstates share each "
            "macrostate, and W counts them. <bookmark mark='e'/>Boltzmann's entropy is the logarithm of W, times a "
            "constant: S equals k log W, the formula on his grave in Vienna, written in Max Planck's notation. A "
            "macrostate has high entropy when a great many microstates look like it."
        ) as vo:
            self.play(FadeIn(head), Create(frame), Create(mid))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(count))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            self.play(t.animate.set_value(9.0), run_time=6, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(Write(f), FadeIn(tomb))
        dots.clear_updaters()
        count.clear_updaters()
        self.clear_scene()

    def counts(self):
        d = load("boltzmann")
        head = label(r"Counting a hundred molecules", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 100, 10], y_range=[0, 30, 5], x_length=7.6, y_length=4.0,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([-2.2, -0.7, 0])
        xl = label(r"molecules on the left", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"$\log_{10} W$", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1).align_to(ax, LEFT)
        logW = [s / np.log(10) for s in d["S"]]
        bars = VGroup(*[Line(ax.c2p(k, 0), ax.c2p(k, logW[k]), color=ENT, stroke_width=3.5) for k in range(101)])
        band = Rectangle(width=ax.c2p(60, 0)[0] - ax.c2p(40, 0)[0], height=4.0, stroke_width=0, fill_color=OK,
                         fill_opacity=0.12).move_to([(ax.c2p(40, 0)[0] + ax.c2p(60, 0)[0]) / 2, ax.c2p(0, 15)[1], 0])
        side = stack([(rf"half and half: \ $W \approx 10^{{{d['W_half_log10']:.0f}}}$", ENT),
                      (r"all on the left: \ $W = 1$, \ probability $2^{-100} \approx 10^{-30}$", BAD),
                      (rf"between 40 and 60 on the left: \ {100 * d['fraction_within_10pct']:.1f}\% of all "
                       r"microstates", OK),
                      (r"for $10^{23}$ molecules, \ the middle is everything", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=4.6).move_to([4.6, -0.4, 0])
        with self.voiceover(
            "Count. <bookmark mark='a'/>With a hundred molecules, each on the left or the right, there are two to "
            "the hundred microstates. The number with exactly k on the left is a binomial coefficient, plotted here "
            "on a logarithmic scale. <bookmark mark='b'/>Half and half: about ten to the twenty-nine microstates. "
            "<bookmark mark='c'/>All on the left: exactly one, a probability of one in ten to the thirty. "
            "<bookmark mark='d'/>Between forty and sixty on the left: ninety-six and a half per cent of all "
            "microstates. <bookmark mark='e'/>And a real gas has something like ten to the twenty-three molecules. "
            "Then the macrostates near equilibrium contain all but a vanishing fraction of the microstates."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), Indicate(bars[50], color=GOAL))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(band), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def cells(self):
        head = label(r"Phase space, \ cut into macrostates", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        big = Rectangle(width=7.2, height=4.6, color=GREY_B, stroke_width=2, fill_color=ENT,
                        fill_opacity=0.10).move_to([-2.6, -0.6, 0])
        c3 = Rectangle(width=2.6, height=1.8, color=CHANCE, stroke_width=2, fill_color=CHANCE,
                       fill_opacity=0.12).move_to(big.get_corner(UL) + np.array([1.3, -0.9, 0]))
        c2 = Rectangle(width=1.1, height=0.8, color=LAW, stroke_width=2, fill_color=LAW,
                       fill_opacity=0.15).move_to(big.get_corner(UL) + np.array([0.55, -0.4, 0]))
        c1 = Rectangle(width=0.32, height=0.26, color=GOAL, stroke_width=2, fill_color=GOAL,
                       fill_opacity=0.4).move_to(big.get_corner(UL) + np.array([0.16, -0.13, 0]))
        tags = VGroup(label(r"equilibrium", font_size=18, color=ENT).move_to(big.get_corner(DR) + np.array([-1.2, 0.3, 0])),
                      label(r"low entropy", font_size=16, color=GOAL).next_to(c1, RIGHT, buff=0.08).shift(UP * 0.02))
        rng = np.random.default_rng(1872)
        p = c1.get_center().copy()
        walk = [p.copy()]
        lo, hi = big.get_corner(DL), big.get_corner(UR)
        for _ in range(150):
            p = p + np.array([rng.normal(0.028, 0.13), rng.normal(-0.012, 0.13), 0])
            for ax_i in (0, 1):  # reflect off the walls of phase space
                a, b = lo[ax_i] + 0.15, hi[ax_i] - 0.15
                if p[ax_i] < a:
                    p[ax_i] = 2 * a - p[ax_i]
                if p[ax_i] > b:
                    p[ax_i] = 2 * b - p[ax_i]
            walk.append(p.copy())
        path = VMobject(stroke_color=WHITE, stroke_width=1.6).set_points_smoothly(walk)
        dot = Dot(walk[0], radius=0.08, color=WHITE)
        side = stack([(r"each point: \ one microstate of the whole gas", WHITE),
                      (r"each cell: \ one macrostate; \ its size is $W$", ABS),
                      (r"not to scale: \ the real ratios have $10^{23}$ in the exponent", BAD),
                      (r"a typical microstate wanders into ever bigger cells: \ entropy rises", ENT),
                      (r"Boltzmann: \ the second law is not certain, \ only overwhelmingly probable", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=4.6).move_to([4.6, -0.5, 0])
        with self.voiceover(
            "Now the picture Boltzmann had in mind. <bookmark mark='a'/>Phase space: every point is one microstate "
            "of the whole gas, every position and velocity at once. <bookmark mark='b'/>The macrostates cut it into "
            "cells, and a cell's size is W. <bookmark mark='c'/>A tiny cell for the gas crowded in its corner, "
            "larger cells as it spreads, and one cell, equilibrium, that fills almost everything. The drawing is not "
            "to scale: the real ratios have ten to the twenty-three in the exponent. "
            "<bookmark mark='d'/>As the microstate moves under the laws of motion, it wanders, and it is "
            "overwhelmingly likely to wander into bigger cells, simply because there is so much more of them. "
            "Entropy rises. <bookmark mark='e'/>So Boltzmann's second law is not a certainty but an overwhelming "
            "probability. And there is a catch, which the next chapter makes precise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(big), FadeIn(tags[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(c3), FadeIn(c2), FadeIn(c1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(tags[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(dot), FadeIn(side[3]))
            self.play(Create(path), MoveAlongPath(dot, path), run_time=5, rate_func=linear)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
