from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class Formalism(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"The formalism in one chapter", r"What does the theory say?", lit=(1926, 1932),
                            part=PART)
        with self.voiceover("Chapter one. The formalism in one chapter."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.states()
        self.born()
        self.interference()
        self.which_path()
        self.uncertainty()
        self.entangled()

    def states(self):
        head = label(r"States are vectors", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        c = np.array([-3.2, -0.6, 0])
        R = 2.3
        circle = Circle(radius=R, color=GREY_D, stroke_width=2).move_to(c)
        up = Arrow(c, c + UP * R, buff=0, color=CLASS, stroke_width=4)
        rt = Arrow(c, c + RIGHT * R, buff=0, color=CLASS, stroke_width=4)
        l0 = MathTex(r"|0\rangle", font_size=32, color=CLASS).next_to(up, UP, buff=0.1)
        l1 = MathTex(r"|1\rangle", font_size=32, color=CLASS).next_to(rt, RIGHT, buff=0.1)
        th = ValueTracker(PI / 3)
        psi = always_redraw(lambda: Arrow(c, c + R * np.array([math.sin(th.get_value() / 2),
                                                               math.cos(th.get_value() / 2), 0]),
                                          buff=0, color=WAVE, stroke_width=6))
        pl = always_redraw(lambda: MathTex(r"|\psi\rangle", font_size=32, color=WAVE).next_to(
            psi.get_end(), UR, buff=0.05))
        f = MathTex(r"|\psi\rangle = \cos\tfrac{\theta}{2}\,|0\rangle + \sin\tfrac{\theta}{2}\,|1\rangle",
                    font_size=34, color=WAVE).move_to([3.4, 1.6, 0])
        rows = stack([(r"a system's state: \ a unit vector in a complex vector space", WHITE),
                      (r"superposition: \ any combination of states is a state", WAVE),
                      (r"dynamics: \ Schrödinger's equation, \ $i\hbar\,\partial_t|\psi\rangle = H|\psi\rangle$, \ "
                       r"linear and deterministic", ABS),
                      (r"a qubit: \ the simplest case, \ two basis states", CLASS)], font_size=21, aligned_edge=LEFT,
                     width=5.6, buff=0.3).move_to([3.4, -0.6, 0])
        with self.voiceover(
            "The formalism fits in one chapter. <bookmark mark='a'/>A system's state is a unit vector in a complex "
            "vector space. <bookmark mark='b'/>Any combination of states is again a state: that is superposition. "
            "Here is the simplest system, a qubit, with two basis states, zero and one, and a state psi that is a "
            "combination of both, at an angle theta. <bookmark mark='c'/>Between measurements, states change by "
            "Schrödinger's equation, which is linear and deterministic: given the state now, the state at every later "
            "time is fixed. <bookmark mark='d'/>So far, nothing strange."
        ) as vo:
            self.play(FadeIn(head), Create(circle), GrowArrow(up), GrowArrow(rt), FadeIn(l0), FadeIn(l1))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(psi), FadeIn(pl), Write(f), FadeIn(rows[1]))
            self.play(th.animate.set_value(2 * PI / 3), run_time=1.5)
            self.play(th.animate.set_value(PI / 3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        psi.clear_updaters()
        pl.clear_updaters()
        self.clear_scene()

    def born(self):
        d = load("born")
        head = label(r"The Born rule", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"P(0) = |\langle 0 | \psi \rangle|^2 = \cos^2\tfrac{\theta}{2}", font_size=40,
                    color=ALICE).next_to(head, DOWN, buff=0.35)
        hd = [r"\theta", r"P(0)\ \text{predicted}", r"\text{frequency in }" + f"{d['shots']:,}".replace(",", r"\,")
              + r"\text{ runs}"]
        rows = [[MathTex(rf"{r['theta_deg']}^\circ", font_size=24), MathTex(f"{r['p0']:.3f}", font_size=24,
                                                                           color=ALICE),
                 MathTex(f"{r['freq0']:.3f}", font_size=24, color=PART_C)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[1.4, 2.6, 3.4], cell_h=0.5, font_size=22).move_to([-3.0, -0.9, 0])
        side = stack([(r"measurement: \ the outcome is random, \ with probability $|\text{amplitude}|^2$", ALICE),
                      (r"and afterwards the state \textit{is} the outcome: \ collapse", BAD),
                      (r"two rules: \ smooth Schrödinger evolution, \ and sudden collapse", ABS),
                      (r"when does which apply? \ the textbooks say: \ `on measurement'", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=4.8, buff=0.3).move_to([4.3, -0.8, 0])
        with self.voiceover(
            "The strangeness enters with measurement. <bookmark mark='a'/>Max Born's rule of 1926: measure the "
            "qubit, and you get zero with probability equal to the squared size of its amplitude, here cos squared "
            "of theta over two. <bookmark mark='b'/>The Reasoner samples two thousand measurements at each of five "
            "angles; the frequencies follow the rule. <bookmark mark='c'/>And after the measurement, the state is "
            "whatever was found: it has jumped, or collapsed. <bookmark mark='d'/>So the textbook theory has two "
            "rules for change, smooth Schrödinger evolution and sudden collapse, as John von Neumann set out in 1932. "
            "<bookmark mark='e'/>Which applies when? The textbooks say: collapse happens on measurement. They do not "
            "say what a measurement is."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def interference(self):
        d = load("mzi")
        head = label(r"Two paths, \ one photon", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        src, bs1, m1, m2, bs2 = (np.array(p) for p in ([-6.6, -2.0, 0], [-5.4, -2.0, 0], [-5.4, 1.0, 0],
                                                        [-1.8, -2.0, 0], [-1.8, 1.0, 0]))
        d0, d1 = np.array([-0.5, 1.0, 0]), np.array([-1.8, 2.3, 0])

        def splitter(c, col):
            return Line(c + np.array([-0.35, -0.35, 0]), c + np.array([0.35, 0.35, 0]), color=col, stroke_width=5)

        parts = VGroup(splitter(bs1, WAVE), splitter(bs2, WAVE), splitter(m1, GREY_B), splitter(m2, GREY_B))
        tags = VGroup(label(r"beam splitter", font_size=16, color=WAVE).next_to(bs1, DOWN, buff=0.5),
                      label(r"beam splitter", font_size=16, color=WAVE).next_to(bs2, RIGHT, buff=0.2).shift(
                          DOWN * 0.4))
        beams = VGroup(Line(src, bs1, color=PART_C, stroke_width=3), Line(bs1, m1, color=PART_C, stroke_width=3),
                       Line(m1, bs2, color=PART_C, stroke_width=3), Line(bs1, m2, color=PART_C, stroke_width=3),
                       Line(m2, bs2, color=PART_C, stroke_width=3))
        out = VGroup(Line(bs2, d0, color=PART_C, stroke_width=3), Line(bs2, d1, color=PART_C, stroke_width=3))
        D0 = VGroup(Square(0.45, color=OK, fill_opacity=0.25).move_to(d0),
                    label(r"$D_0$", font_size=20, color=OK).next_to(d0, RIGHT, buff=0.3))
        D1 = VGroup(Square(0.45, color=BAD, fill_opacity=0.25).move_to(d1),
                    label(r"$D_1$", font_size=20, color=BAD).next_to(d1, LEFT, buff=0.3))
        shifter = VGroup(Rectangle(width=0.5, height=0.5, color=ABS, fill_opacity=0.3).move_to([-3.6, -2.0, 0]),
                         MathTex(r"\varphi", font_size=26, color=ABS).move_to([-3.6, -2.6, 0]))
        amps = VGroup(MathTex(r"\tfrac{1}{\sqrt2}", font_size=24, color=WAVE).next_to(Line(bs1, m1), LEFT, buff=0.15),
                      MathTex(r"\tfrac{1}{\sqrt2}", font_size=24, color=WAVE).move_to([-4.5, -1.55, 0]))
        A = d["amplitudes"]
        assert A == {"D0": [0.5, 0.5], "D1": [0.5, -0.5]}
        sums = VGroup(MathTex(r"D_0:\ \tfrac12 + \tfrac12 = 1", font_size=30, color=OK),
                      MathTex(r"D_1:\ \tfrac12 - \tfrac12 = 0", font_size=30, color=BAD)).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.6, 1.6, 0])
        b = d["blocked"]
        assert b == {"D0": 0.25, "D1": 0.25, "absorbed": 0.5}
        side = stack([(r"block either arm: \ $D_0$ and $D_1$ each fire $\tfrac14$ of the time", BAD),
                      (r"a phase $\varphi$ in one arm: \ $P(D_0) = \left|\tfrac{1 + e^{i\varphi}}{2}\right|^2 "
                       r"= \cos^2\tfrac{\varphi}{2}$", ABS)], font_size=21, aligned_edge=LEFT, width=6.0,
                     buff=0.35).move_to([3.6, -0.2, 0])
        hd = [r"\varphi", r"P(D_0)", r"\text{freq. in } %d" % d["shots"]]
        rows = [[MathTex(rf"{r['phi_deg']}^\circ", font_size=24), MathTex(f"{r['p0']:.3f}", font_size=24, color=ABS),
                 MathTex(f"{r['freq0']:.3f}", font_size=24, color=PART_C)] for r in d["samples"]]
        grid = ValueGrid(hd, rows, col_w=[1.4, 1.8, 2.2], cell_h=0.45, font_size=20).move_to([3.6, -2.3, 0])
        with self.voiceover(
            "Here is the formalism at work, in the simplest experiment that shows what is strange about it. "
            "<bookmark mark='a'/>A single photon meets a half-silvered mirror, a beam splitter. Its state becomes a "
            "superposition of the two arms, with amplitude one over root two in each. <bookmark mark='b'/>Mirrors "
            "bring the arms together at a second beam splitter, and two detectors wait beyond it. "
            "<bookmark mark='c'/>Follow the amplitudes. Toward the first detector, the two paths each contribute "
            "one half, and they add: amplitude one. Toward the second, they contribute plus a half and minus a half, "
            "and cancel. So every photon arrives at the first detector. <bookmark mark='d'/>Block either arm, and "
            "each detector fires a quarter of the time: removing a path makes the second detector fire. "
            "<bookmark mark='e'/>Put a phase shift phi in one arm, and the probability at the first detector "
            "becomes cos squared of phi over two. <bookmark mark='f'/>The Reasoner sends two thousand photons at "
            "each of three settings."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(parts[0]), FadeIn(tags[0]), Create(beams[0]))
            self.play(Create(beams[1]), Create(beams[3]), FadeIn(amps))
            vo.wait_until("b")
            self.play(FadeIn(parts[2:]), FadeIn(parts[1]), FadeIn(tags[1]), Create(beams[2]), Create(beams[4]))
            self.play(Create(out), FadeIn(D0), FadeIn(D1))
            vo.wait_until("c")
            self.play(Write(sums[0]))
            self.play(Write(sums[1]), D0[0].animate.set_fill(opacity=0.8))
            vo.wait_until("d")
            self.play(FadeIn(side[0]))
            vo.wait_until("e")
            self.play(FadeIn(shifter), FadeIn(side[1]))
            vo.wait_until("f")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
        self.clear_scene()

    def which_path(self):
        d = load("mzi")
        head = label(r"Which way did it go?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 360, 90], y_range=[0, 1, 0.25], x_length=7.0, y_length=4.2,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([-2.4, -0.6, 0])
        xl = label(r"phase $\varphi$ (degrees)", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"$P(D_0)$", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1).align_to(ax, LEFT)
        xs = [math.degrees(p) for p in d["phi"]]
        cols = {"1.0": WAVE, "0.5": ABS, "0.0": BAD}
        curves = {k: series_plot(ax, d["curves"][k], cols[k], xs=xs, width=4) for k in ("1.0", "0.5", "0.0")}
        v = d["visibility"]
        assert v == {"1.0": 1.0, "0.5": 0.5, "0.0": 0.0}
        side = stack([(r"each arm leaves a marker: \ $|m_0\rangle$ or $|m_1\rangle$", WHITE),
                      (r"no record: \ visibility 1", WAVE),
                      (r"markers overlapping by $\langle m_0 | m_1 \rangle = \tfrac12$: \ visibility 0.5", ABS),
                      (r"a perfect record: \ visibility 0, \ $P(D_0) = \tfrac12$ always", BAD),
                      (r"$P(D_0) = \tfrac12\,(1 + \langle m_0 | m_1 \rangle \cos\varphi)$: \ nobody needs to "
                       r"read the record", GOAL)], font_size=20, aligned_edge=LEFT, width=4.6,
                     buff=0.32).move_to([4.4, -0.4, 0])
        with self.voiceover(
            "Now ask which way the photon went. <bookmark mark='a'/>Let each arm leave a record: a marker, in one "
            "state if the photon took the upper arm and another if it took the lower. <bookmark mark='b'/>The "
            "Reasoner computes the probability at the first detector as the phase varies. With no record, the "
            "fringes swing all the way from one to zero. <bookmark mark='c'/>With markers whose states overlap by "
            "one half, the swing is halved. <bookmark mark='d'/>With a perfect record, orthogonal markers, the "
            "fringes vanish: one half, whatever the phase. <bookmark mark='e'/>The visibility of the fringes equals "
            "the overlap of the records, exactly. Nobody has to read the marker. That a record exists, somewhere, is "
            "enough. This is the seed of decoherence, which returns in chapter ten."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curves["1.0"]), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(curves["0.5"]), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(Create(curves["0.0"]), FadeIn(side[3]), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def uncertainty(self):
        d = load("uncert")
        head = label(r"Questions that cannot both be sharp", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        eqs = VGroup(MathTex(r"XZ - ZX = -2iY \neq 0", font_size=32, color=ABS),
                     MathTex(r"\Delta X\,\Delta Z \;\ge\; \tfrac12\,|\langle [X, Z] \rangle| = |\langle Y "
                             r"\rangle|", font_size=32, color=WAVE),
                     MathTex(r"\Delta X^2 + \Delta Z^2 = 2 - \langle X\rangle^2 - \langle Z\rangle^2 \;\ge\; 1",
                             font_size=32, color=GOAL)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(
            [2.9, 1.3, 0])
        assert d["commutator_is_minus_2iY"]
        c, R = np.array([-4.0, -1.0, 0]), 2.2
        disk = Circle(radius=R, color=GREY_B, stroke_width=2).move_to(c)
        axx = Arrow(c + LEFT * (R + 0.3), c + RIGHT * (R + 0.5), buff=0, color=GREY_C, stroke_width=2,
                    max_tip_length_to_length_ratio=0.04)
        axz = Arrow(c + DOWN * (R + 0.3), c + UP * (R + 0.5), buff=0, color=GREY_C, stroke_width=2,
                    max_tip_length_to_length_ratio=0.04)
        lx = MathTex(r"\langle X \rangle", font_size=22, color=GREY_A).next_to(axx, RIGHT, buff=0.1)
        lz = MathTex(r"\langle Z \rangle", font_size=22, color=GREY_A).next_to(axz, UP, buff=0.1)
        pts = VGroup(*[Dot(c + R * np.array([x, z, 0]), radius=0.025, color=WAVE) for x, z in d["points"]])
        corners = VGroup(*[Cross(scale_factor=0.12, stroke_color=BAD, stroke_width=4).move_to(c + R * np.array([sx, sz, 0]))
                           for sx in (-1, 1) for sz in (-1, 1)])
        ctag = label(r"both sharp: \ outside", font_size=17, color=BAD).next_to(corners[3], UP, buff=0.1)
        assert d["robertson_slack_min"] >= 0 and d["sum_sq_min"] >= 1
        side = stack([(r"%d random states: \ Robertson's bound never fails" % d["n_random"], OK),
                      (rf"least $\Delta X^2 + \Delta Z^2$: \ {d['sum_sq_min']:.3f} \ (never below 1)", OK)],
                     font_size=21, aligned_edge=LEFT, width=6.2, buff=0.3).move_to([2.9, -1.6, 0])
        with self.voiceover(
            "Some questions cannot both have sharp answers. <bookmark mark='a'/>Spin along x and spin along z are "
            "represented by matrices that do not commute: X Z minus Z X is minus two i Y, not zero. "
            "<bookmark mark='b'/>Howard Robertson's inequality of 1929 turns that into a bound: the spread in x "
            "times the spread in z is at least half the size of the commutator's expected value. Heisenberg's "
            "relation for position and momentum is the same theorem. <bookmark mark='c'/>For a qubit there is a "
            "sharper way to see it. Plot each state by its expected x spin and its expected z spin: every state "
            "lies inside the unit disk. <bookmark mark='d'/>The corners, where both spins would be definite, lie "
            "outside it. The sum of the two variances is two minus the squared distance from the centre, so it is "
            "never less than one. <bookmark mark='e'/>The Reasoner tries five thousand random states: Robertson's "
            "bound always holds, and the sum of the variances never drops below one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(Create(disk), Create(axx), Create(axz), FadeIn(lx), FadeIn(lz))
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.005), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(corners), FadeIn(ctag), Write(eqs[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def entangled(self):
        head = label(r"Entanglement", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"|\Psi^-\rangle = \tfrac{1}{\sqrt2}\big(|0\rangle_A|1\rangle_B - |1\rangle_A|0\rangle_B\big)",
                    font_size=40, color=WAVE).move_to([0, 1.5, 0])
        rows = stack([(r"two particles, \ one state: \ not a product of a state for each", WAVE),
                      (r"measure either: \ 0 or 1, \ each half the time", WHITE),
                      (r"measure both along the same axis: \ always opposite", ALICE),
                      (r"`the characteristic trait of quantum mechanics' \ (Schrödinger, \ 1935)", HIST),
                      (r"the stage for EPR, \ Bell, \ and everything after", GOAL)], font_size=22, aligned_edge=LEFT,
                     width=11.0, buff=0.32).move_to([0, -1.0, 0])
        with self.voiceover(
            "One more piece. <bookmark mark='a'/>Two particles can share a single state that is not the product of "
            "a state for each: the singlet, written here. <bookmark mark='b'/>Measure either particle alone and you "
            "get zero or one, each half the time. <bookmark mark='c'/>Measure both along the same axis and the "
            "results are always opposite. <bookmark mark='d'/>Schrödinger named this entanglement in 1935, and "
            "called it not one but the characteristic trait of quantum mechanics. <bookmark mark='e'/>It is the "
            "stage for everything that follows."
        ) as vo:
            self.play(FadeIn(head), Write(f))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
