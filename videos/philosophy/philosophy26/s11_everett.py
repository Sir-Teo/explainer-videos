from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class Everett(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Many worlds", r"What if the wavefunction is all there is?", lit=(1957, 2012),
                            part=PART)
        with self.voiceover("Chapter ten. Many worlds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.decoherence()
        self.counting()
        self.probability()

    def idea(self):
        hc = history_card(1957, r"Hugh Everett III", r"`Relative State Formulation of Quantum Mechanics'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        trunk = Line([-5.0, -0.6, 0], [-2.4, -0.6, 0], color=WAVE, stroke_width=6)
        b1 = Line([-2.4, -0.6, 0], [1.2, 0.8, 0], color=ALICE, stroke_width=5)
        b2 = Line([-2.4, -0.6, 0], [1.2, -2.0, 0], color=BOB, stroke_width=5)
        l1 = label(r"a branch where the pointer reads 0, \ and so do you", font_size=19, color=ALICE).next_to(
            b1.get_end(), RIGHT, buff=0.15)
        l2 = label(r"a branch where it reads 1", font_size=19, color=BOB).next_to(b2.get_end(), RIGHT, buff=0.15)
        rows = stack([(r"keep the linear equation; \ drop collapse; \ apply it to everything", WAVE),
                      (r"the cat superposition is not a problem: \ it describes two cats, \ in two branches", ALICE),
                      (r"each observer sees one outcome, \ because each observer is in one branch", GOAL)],
                     font_size=21, aligned_edge=LEFT, width=11.0, buff=0.26).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1957 Hugh Everett, a graduate student of John Wheeler's at Princeton, proposed taking the "
            "equation seriously. <bookmark mark='a'/>Keep Schrödinger's linear equation, drop collapse, and apply "
            "the theory to everything, observers included. <bookmark mark='b'/>Then the superposition at the end of a "
            "measurement is not a problem to be removed. It describes the world splitting into branches: one in which "
            "the pointer reads zero and the observer sees zero, and one in which it reads one. "
            "<bookmark mark='c'/>Each observer sees a single outcome, because each version of the observer is in "
            "one branch. The definite-outcomes claim of the measurement problem is what goes."
        ) as vo:
            self.play(FadeIn(hc), Create(trunk))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(b1), Create(b2), FadeIn(l1), FadeIn(l2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def decoherence(self):
        d = load("decohere")
        head = label(r"Decoherence, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 12, 2], y_range=[0, 0.5, 0.1], x_length=7.0, y_length=3.8,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([-2.4, -0.6, 0])
        xl = label(r"environment qubits that have recorded the system", font_size=18, color=GREY_A).next_to(
            ax.x_axis, DOWN, buff=0.4)
        yl = label(r"coherence $|\rho_{01}|$", font_size=18, color=GREY_A).next_to(ax.y_axis, UP,
                                                                                  buff=0.1).align_to(ax, LEFT)
        pts = VGroup(*[Dot(ax.c2p(r["env"], r["coherence"]), radius=0.07, color=WAVE) for r in d["rows"]])
        curve = series_plot(ax, [r["coherence"] for r in d["rows"]], WAVE, xs=[r["env"] for r in d["rows"]])
        f = MathTex(r"|\rho_{01}| = \tfrac12 \cos^n\theta", font_size=34, color=WAVE).move_to([4.6, 1.5, 0])
        side = stack([(rf"each environment qubit records the system imperfectly: \ overlap $\cos\theta = "
                       rf"{d['overlap']:.2f}$", WHITE),
                      (r"the system's interference terms fall exponentially", WAVE),
                      (r"for a real pointer, \ $n \sim 10^{23}$: \ the branches stop interfering at once", GOAL),
                      (r"decoherence explains why branches behave classically; \ it does not choose one", BAD)],
                     font_size=20, aligned_edge=LEFT, width=4.6, buff=0.3).move_to([4.6, -0.8, 0])
        with self.voiceover(
            "What makes the branches separate? Decoherence. <bookmark mark='a'/>A qubit in a superposition interacts "
            "with its environment, and each environment qubit keeps an imperfect record of which state the system "
            "is in. <bookmark mark='b'/>The Reasoner builds the joint state and traces out the environment. The "
            "system's coherence, the part of its state that allows interference, falls as cos theta to the power of "
            "the number of records: exponentially. <bookmark mark='c'/>A real pointer is recorded by something like "
            "ten to the twenty-three air molecules and photons, so its branches stop interfering almost instantly, "
            "and each behaves like a classical world. <bookmark mark='d'/>But notice what decoherence does not do: "
            "it does not choose one branch. It explains why we never see interference between pointer readings; for "
            "Everett, that is all that needs explaining."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(f), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1), Create(curve), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def counting(self):
        d = load("branches")
        head = label(r"Counting branches, \ or weighing them", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        n = d["plot_n"]
        assert n == 50 and d["p"] == 0.9 and d["tol"] == 0.1
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 0.2, 0.05], x_length=6.6, y_length=3.6,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([-3.0, 0.2, 0])
        xl = label(r"frequency of outcome 0 in the branch", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"share", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1).align_to(ax, LEFT)
        w = 6.6 / (n + 1) * 0.9

        def bars(dist, col):
            g = VGroup()
            for k, v in enumerate(dist):
                if v < 1e-4:
                    continue
                h = 3.6 * v / 0.2
                g.add(Rectangle(width=w, height=h, stroke_width=0, fill_color=col, fill_opacity=0.75).move_to(
                    ax.c2p(k / n, 0) + UP * h / 2))
            return g

        cb, wb = bars(d["count_dist"], CLASS), bars(d["weight_dist"], WAVE)
        band = Rectangle(width=ax.c2p(1.0, 0)[0] - ax.c2p(0.8, 0)[0], height=3.6, stroke_width=0, fill_color=GOAL,
                         fill_opacity=0.12).move_to((ax.c2p(0.8, 0) + ax.c2p(1.0, 0.2)) / 2)
        lab = stack([(r"teal: \ branches counted, \ each alike", CLASS),
                     (r"blue: \ branches weighed by $|\text{amplitude}|^2$", WAVE),
                     (r"gold band: \ frequency within 0.1 of 0.9", GOAL)], font_size=19, aligned_edge=LEFT,
                    width=4.6, buff=0.22).move_to([4.2, 1.6, 0])
        rows_d = d["rows"]
        assert [r["n"] for r in rows_d] == [10, 50, 200]
        assert rows_d[0]["count_fraction"] > 0.05 and rows_d[1]["count_fraction"] < 2e-5
        assert rows_d[2]["count_fraction"] < 2e-18 and rows_d[0]["born_weight"] > 0.92 and rows_d[1]["born_weight"] > 0.99

        def sci(x):
            if x >= 0.01:
                return f"{x:.3f}"
            m, e = f"{x:.1e}".split("e")
            return rf"{m} \times 10^{{{int(e)}}}"

        hd = [r"n", r"\text{share of branches}", r"\text{their Born weight}"]
        rows = [[MathTex(str(r["n"]), font_size=24), MathTex(sci(r["count_fraction"]), font_size=24, color=CLASS),
                 MathTex(f"{r['born_weight']:.4f}" if r["born_weight"] < 1 else "1 - " + sci(r["born_shortfall"]), font_size=24,
                         color=WAVE)] for r in rows_d]
        grid = ValueGrid(hd, rows, col_w=[0.9, 2.6, 2.4], cell_h=0.45, font_size=19).move_to([4.0, -1.0, 0])
        foot = label(r"the probability problem: \ why weigh the branches, \ rather than count them?", font_size=22,
                     color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the problem in numbers. <bookmark mark='a'/>Measure a qubit whose Born weights are nine tenths "
            "and one tenth, fifty times over. The world splits into two to the fifty branches, each with its own "
            "record of results. <bookmark mark='b'/>Count the branches by their frequency of zeros: most have about "
            "half zeros, as fair coin flips would. <bookmark mark='c'/>Now weigh each branch by the Born rule, the "
            "squared size of its amplitude: the weight piles up near nine tenths. <bookmark mark='d'/>The Reasoner "
            "counts. The share of branches whose frequency is within a tenth of nine tenths falls from about five "
            "percent at ten trials, to about one in a hundred thousand at fifty, to about ten to the minus eighteen "
            "at two hundred. Their Born weight rises from ninety-three percent to ninety-nine, and then to all but "
            "certainty. <bookmark mark='e'/>So the theory needs a reason to weigh branches by squared amplitude, and "
            "not to count them. That is the probability problem."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(band), FadeIn(lab[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in cb], lag_ratio=0.03), FadeIn(lab[0]), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in wb], lag_ratio=0.03), FadeIn(lab[1]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def probability(self):
        head = label(r"The probability problem", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the problem", r"if every outcome happens, \ what does `probability 0.9' mean? \ and why should we "
                             r"expect Born frequencies?", BAD),
            (r"Deutsch \ (1999), \ Wallace \ (2012)", r"a rational agent who knows she will branch must weight her "
                                                     r"successors by $|\text{amplitude}|^2$: \ a decision-theoretic "
                                                     r"derivation", OK),
            (r"self-location", r"Vaidman; \ Sebens and Carroll: \ before you look, \ you are uncertain which branch "
                               r"you are in", ABS),
            (r"the critics", r"Albert, \ Kent, \ Price: \ the axioms beg the question; \ why not count branches "
                             r"equally?", BAD),
            (r"next", r"Part 33's decision theory meets Everett's branching", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.45, width=8.4, x_text=-2.0, label_size=21, text_size=20)
        with self.voiceover(
            "The hardest problem for many worlds is probability. <bookmark mark='a'/>If every outcome happens, what "
            "does it mean to say one outcome has probability nine tenths? And why should we expect to see Born-rule "
            "frequencies rather than any others? <bookmark mark='b'/>David Deutsch in 1999, and David Wallace in his "
            "book of 2012, gave a decision-theoretic answer: an agent who knows she is about to branch, and who "
            "satisfies some plausible axioms of rationality, must care about her successors in proportion to their "
            "squared amplitudes. <bookmark mark='c'/>Others, such as Lev Vaidman, Charles Sebens and Sean Carroll, "
            "appeal to self-locating uncertainty: after branching but before looking, you do not know which branch "
            "you are in. <bookmark mark='d'/>Critics, among them David Albert, Adrian Kent and Huw Price, reply "
            "that the axioms smuggle in the answer, and ask why one should not simply count branches equally. "
            "<bookmark mark='e'/>Part 33's decision theory will return to this."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
