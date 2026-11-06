from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Demon(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Maxwell's demon", r"Can knowledge beat the second law?", lit=(1867, 1961),
                            part=PART)
        with self.voiceover("Chapter twelve. Maxwell's demon."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.demon()
        self.szilard()
        self.landauer()
        self.exorcism()

    def demon(self):
        hc = history_card(1867, r"James Clerk Maxwell", r"letter to Peter Guthrie Tait", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        box = Rectangle(width=7.0, height=3.6, color=GREY_B, stroke_width=2).move_to([-2.2, -0.6, 0])
        wall_top = Line([-2.2, 1.2, 0], [-2.2, -0.1, 0], color=GREY_B, stroke_width=3)
        wall_bot = Line([-2.2, -1.1, 0], [-2.2, -2.4, 0], color=GREY_B, stroke_width=3)
        door = Line([-2.2, -0.1, 0], [-2.2, -1.1, 0], color=DATA, stroke_width=5)
        rng = np.random.default_rng(1867)
        n = 28
        fast = np.array([i % 2 == 0 for i in range(n)])
        left = rng.random(n) < 0.5
        pos = []
        for i in range(n):
            x = rng.uniform(-5.4, -2.6) if left[i] else rng.uniform(-1.8, 1.0)
            pos.append(np.array([x, rng.uniform(-2.2, 1.0), 0]))
        mols = VGroup(*[Dot(p, radius=0.09, color=BAD if f else LAW) for p, f in zip(pos, fast)])
        targets = []
        for i in range(n):
            if fast[i] and left[i]:
                targets.append(np.array([rng.uniform(-1.8, 1.0), rng.uniform(-2.2, 1.0), 0]))
            elif not fast[i] and not left[i]:
                targets.append(np.array([rng.uniform(-5.4, -2.6), rng.uniform(-2.2, 1.0), 0]))
            else:
                targets.append(None)
        demon = VGroup(Circle(radius=0.22, color=DATA, fill_color=DATA, fill_opacity=0.6),
                       label(r"demon", font_size=16, color=DATA)).arrange(DOWN, buff=0.06).move_to([-2.2, 1.65, 0])
        legend = VGroup(VGroup(Dot(radius=0.08, color=BAD), label(r"fast", font_size=18, color=BAD)).arrange(
            RIGHT, buff=0.1), VGroup(Dot(radius=0.08, color=LAW), label(r"slow", font_size=18, color=LAW)).arrange(
            RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([2.4, 1.0, 0])
        side = stack([(r"the demon opens the door for fast molecules going right, \ slow ones going left", DATA),
                      (r"no work done: \ yet the right side gets hot, \ the left cold", BAD),
                      (r"entropy falls: \ the second law broken, \ by knowledge", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=4.4).move_to([4.6, -1.0, 0])
        with self.voiceover(
            "In 1867 James Clerk Maxwell, in a letter to Peter Guthrie Tait, imagined a way to break the second "
            "law. <bookmark mark='a'/>A box of gas, divided by a wall with a small door. The molecules move at "
            "different speeds, fast and slow, mixed on both sides at the same temperature. "
            "<bookmark mark='b'/>A tiny being, later called Maxwell's demon, watches the door. It opens it only "
            "when a fast molecule approaches from the left or a slow one from the right. "
            "<bookmark mark='c'/>The door is light and frictionless, so no work is done. Yet the right side fills "
            "with fast molecules and grows hot, and the left grows cold. <bookmark mark='d'/>Entropy has fallen, "
            "and all it took was information about the molecules. Either the second law is false, or knowing has a "
            "physical cost. It took more than a century to find out which."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(box), Create(wall_top), Create(wall_bot), Create(door), FadeIn(mols), FadeIn(legend))
            vo.wait_until("b")
            self.play(FadeIn(demon), FadeIn(side[0]))
            vo.wait_until("c")
            movers = [(m, t) for m, t in zip(mols, targets) if t is not None]
            anims = []
            for m, t in movers:
                path = VMobject().set_points_smoothly([m.get_center(), np.array([-2.2, -0.6, 0]), t])
                anims.append(MoveAlongPath(m, path))
            self.play(LaggedStart(*anims, lag_ratio=0.25), door.animate.set_color(OK), run_time=6)
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def szilard(self):
        d = load("szilard")
        hc = history_card(1929, r"Leo Szilard", r"`On the Decrease of Entropy in a Thermodynamic System'",
                          width=6.6, color=HIST).to_corner(UL, buff=0.3)
        box = Rectangle(width=4.4, height=2.4, color=GREY_B, stroke_width=2).move_to([-3.8, 0.0, 0])
        mol = Dot([-5.0, 0.4, 0], radius=0.12, color=ENT)
        part = Line([-3.8, 1.2, 0], [-3.8, -1.2, 0], color=DATA, stroke_width=5)
        steps = stack([(r"1. \ one molecule in a box at temperature $T$", WHITE),
                       (r"2. \ slide in a partition", DATA),
                       (r"3. \ look: \ which side? \ one bit", ABS),
                       (r"4. \ let that side push the partition, \ as a piston, \ out to the wall", ENT),
                       (r"work gained: \ $W = kT \ln 2$", OK)], font_size=21, aligned_edge=LEFT, width=4.4,
                      buff=0.25).move_to([-3.8, -2.4, 0])
        steps.next_to(box, DOWN, buff=0.35)
        hd = [r"\text{partition at}", r"\text{bits learned}", r"\text{work } (kT)", r"\text{simulated}"]
        rows = [[MathTex(f"{r['x']:.2f}", font_size=22), MathTex(f"{r['bits']:.3f}", font_size=22, color=ABS),
                 MathTex(f"{r['theory_kT']:.3f}", font_size=22, color=OK),
                 MathTex(f"{r['simulated_kT']:.3f}", font_size=22, color=GREY_A)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[2.0, 1.8, 1.6, 1.7], cell_h=0.44, font_size=19).move_to([3.4, 0.6, 0])
        f = MathTex(r"\langle W \rangle = kT \, H(\text{outcome}) \le kT \ln 2", font_size=30, color=OK).next_to(
            grid, DOWN, buff=0.4)
        with self.voiceover(
            "In 1929 Leo Szilard boiled the demon down to one molecule. <bookmark mark='a'/>A single molecule in a "
            "box, at temperature T. <bookmark mark='b'/>Slide a partition into the middle. <bookmark mark='c'/>Look "
            "to see which side the molecule is on: one bit of information. <bookmark mark='d'/>Now let the "
            "molecule push the partition outward, like a piston, while heat flows in from the surroundings to keep "
            "the temperature fixed. <bookmark mark='e'/>The work gained is k T log two. Repeat, and heat turns "
            "into work forever. <bookmark mark='f'/>The Reasoner runs the engine twenty thousand times, with the "
            "partition at different places. The average work is k T times the information the measurement gives, "
            "in natural units, and it is largest, log two, when the partition is in the middle and the answer is a "
            "full bit. Information is worth work, at an exact exchange rate."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(box), FadeIn(mol), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(Create(part), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(Indicate(mol, color=DATA), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(part.animate.shift(RIGHT * 2.15), mol.animate.move_to([-3.0, -0.3, 0]), FadeIn(steps[3]),
                      run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
            vo.wait_until("f")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            self.play(Write(f))
        self.clear_scene()

    def landauer(self):
        la = load("landauer")
        hc = history_card(1961, r"Rolf Landauer", r"`Irreversibility and Heat Generation in the Computing Process'",
                          width=6.8, color=HIST).to_corner(UL, buff=0.3)
        ax = Axes(x_range=[-2, 2, 1], y_range=[-1.5, 2.5, 1], x_length=5.4, y_length=3.2, tips=False,
                  axis_config={"color": GREY_D}).move_to([-3.4, -0.9, 0])
        tilt = ValueTracker(0.0)
        barrier = ValueTracker(1.0)

        def V(x):
            return barrier.get_value() * (x ** 4 - 2 * x ** 2) + tilt.get_value() * x

        curve = always_redraw(lambda: ax.plot(V, x_range=[-1.75, 1.75], color=ABS, stroke_width=3.5))
        ball = always_redraw(lambda: Dot(ax.c2p(1.0, V(1.0)) + UP * 0.14, radius=0.12, color=DATA))
        labs = VGroup(label(r"0", font_size=22, color=GREY_A).move_to(ax.c2p(-1, -1.45)),
                      label(r"1", font_size=22, color=GREY_A).move_to(ax.c2p(1, -1.45)))
        side = stack([(r"a bit: \ a particle in one of two wells", WHITE),
                      (r"erase: \ force it into well 0, \ whatever it was", BAD),
                      (r"two states become one: \ the entropy of the memory falls by $k \ln 2$", ABS),
                      (r"so at least $kT \ln 2$ of heat must go into the world", ENT),
                      (rf"at room temperature: \ ${la['joules_per_bit'] * 1e21:.2f} \times 10^{{-21}}$ joules "
                       rf"per bit", OK),
                      (r"measured: \ Bérut et al. \ (2012), \ a bead in a laser trap", HIST)], font_size=20,
                     aligned_edge=LEFT, width=5.2, buff=0.22).move_to([3.8, -0.6, 0])
        ball_end = Dot(ax.c2p(-1.0, -1.0) + UP * 0.14, radius=0.12, color=DATA)
        with self.voiceover(
            "The answer came from computing. In 1961 Rolf Landauer, at IBM, asked what it costs to compute. "
            "<bookmark mark='a'/>Store a bit as a particle that sits in one of two wells, zero or one. "
            "<bookmark mark='b'/>To erase the bit, to reset it to zero whatever it was, lower the barrier, tilt the "
            "landscape so the particle rolls into the zero well, and raise the barrier again. "
            "<bookmark mark='c'/>Two possible states have become one. The memory's entropy has fallen by k log "
            "two, <bookmark mark='d'/>and by the second law at least k T log two of heat must flow into the "
            "surroundings. Erasing information is irreversible, and has a minimum price. "
            "<bookmark mark='e'/>At room temperature the price is about three times ten to the minus twenty-one "
            "joules per bit. <bookmark mark='f'/>In 2012 Antoine Bérut and colleagues measured it, with a glass "
            "bead held in a double-welled laser trap: when the erasure was done slowly enough, the heat released "
            "approached Landauer's bound."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(curve), FadeIn(ball), FadeIn(labs), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            self.play(barrier.animate.set_value(0.15), run_time=1.2)
            self.play(tilt.animate.set_value(1.2), run_time=1.2)
            ball.clear_updaters()
            self.play(ball.animate.move_to(ball_end), run_time=1.0)
            self.play(tilt.animate.set_value(0.0), barrier.animate.set_value(1.0), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        curve.clear_updaters()
        self.clear_scene()

    def exorcism(self):
        head = label(r"Bennett's exorcism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        T = lambda s, c=WHITE: label(s, font_size=21, color=c)  # noqa: E731
        hd = [T(r"one cycle of the engine", CONN), T(r"heat into work", CONN)]
        rows = [[T(r"measure the molecule: \ can be done reversibly"), MathTex(r"0", font_size=26)],
                [T(r"let it push the piston"), MathTex(r"+\,kT\ln 2", font_size=26, color=OK)],
                [T(r"erase the demon's memory, \ ready for the next cycle"), MathTex(r"-\,kT\ln 2", font_size=26,
                                                                                    color=BAD)],
                [T(r"net", GOAL), MathTex(r"\le 0", font_size=28, color=GOAL)]]
        grid = ValueGrid(hd, rows, col_w=[7.4, 2.6], cell_h=0.62, font_size=21).move_to([0, 0.4, 0])
        foot = stack([(r"Bennett \ (1982): \ the cost is not in knowing, \ but in forgetting", ABS),
                      (r"Landauer \ (1991): \ `information is physical'", HIST)], font_size=22,
                     buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1982 Charles Bennett put the pieces together. <bookmark mark='a'/>Measuring the molecule need cost "
            "nothing: a measurement can be done reversibly, by copying. <bookmark mark='b'/>The engine then turns "
            "k T log two of heat into work. <bookmark mark='c'/>But the demon now remembers which side the molecule "
            "was on. To run the next cycle it must clear that memory, and erasing one bit costs at least k T log two "
            "of heat. <bookmark mark='d'/>The books balance, at best. The demon cannot win. "
            "<bookmark mark='e'/>The cost was never in knowing; it is in forgetting. Information is physical, as "
            "Landauer liked to say, and the second law covers it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]])
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
