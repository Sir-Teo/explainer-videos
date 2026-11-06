from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class BestSystem(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The best system", r"Are the laws the best summary of the facts?",
                            lit=(1928, 1994), part=PART)
        with self.voiceover("Chapter two. The best system."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.definition()
        self.toy()
        self.bits()
        self.objections()
        self.mentaculus()

    def definition(self):
        hc = history_card(1973, r"David Lewis", r"\textit{Counterfactuals}, \ after Ramsey \ (1928)", width=5.8,
                          color=HIST).to_corner(UL, buff=0.3)
        f = MathTex(r"\text{a law} \;=\; \text{a theorem of every true system with the best balance of }",
                    r"\text{simplicity}", r"\text{ and }", r"\text{strength}", font_size=30).move_to([0, 0.8, 0])
        f[1].set_color(LAW)
        f[3].set_color(CHANCE)
        rows = stack([(r"consider every true deductive system that describes the mosaic", WHITE),
                      (r"simplicity: \ few, \ short axioms", LAW),
                      (r"strength: \ says a lot about what happens", CHANCE),
                      (r"they pull against each other: \ the list of all facts is strongest, \ `something "
                       r"happens' is simplest", ABS)], font_size=22, aligned_edge=LEFT, width=11.0,
                     buff=0.3).move_to([0, -1.4, 0])
        with self.voiceover(
            "Lewis's account goes back to Frank Ramsey in 1928, and Lewis gave it its classic form in 1973. "
            "<bookmark mark='a'/>Consider every true deductive system that describes the mosaic: sets of axioms, "
            "all true, with their consequences. <bookmark mark='b'/>Some are simple: a few short axioms. "
            "<bookmark mark='c'/>Some are strong: they say a great deal about what happens. "
            "<bookmark mark='d'/>The two pull against each other. The list of every fact is as strong as can be and "
            "hopelessly complicated; the single axiom, something happens, is as simple as can be and says nothing. "
            "<bookmark mark='e'/>A law, Lewis said, is a theorem of every true system that strikes the best balance "
            "of simplicity and strength. The laws are the mosaic's best summary."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(Write(f))
        self.clear_scene()

    def toy(self):
        d = load("best")
        head = label(r"A best system, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 2, 0.5], y_range=[0, 22, 5], x_length=6.4, y_length=4.2,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([-3.0, -0.5, 0])
        xl = label(r"time $t$ (s)", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"height (m)", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1).align_to(ax, LEFT)
        pts = VGroup(*[Dot(ax.c2p(t, y), radius=0.045, color=WHITE) for t, y in d["data"]])
        grid_t = np.linspace(0, 2, 81)
        cols = {0: ABS, 1: CHANCE, 2: OK, 7: BAD}
        curves = {k: series_plot(ax, d["rows"][k]["curve"], cols[k], xs=grid_t, width=3) for k in cols}
        c2 = d["rows"][2]["coef"]
        side = stack([(r"40 measurements of a falling ball, \ with noise", WHITE),
                      (r"degree 0: \ `the height is constant'", ABS),
                      (r"degree 1: \ a straight line", CHANCE),
                      (rf"degree 2: \ $h = {c2[0]:.1f} {c2[1]:+.1f}\,t {c2[2]:+.1f}\,t^2$", OK),
                      (r"degree 7: \ eight parameters, \ hugging the noise", BAD)], font_size=21, aligned_edge=LEFT,
                     width=5.6).move_to([3.9, -0.3, 0])
        with self.voiceover(
            "Here is a best system, built. <bookmark mark='a'/>The mosaic is forty measurements of the height of a "
            "falling ball, with some noise. The candidate systems are polynomial laws of rising degree. "
            "<bookmark mark='b'/>Degree zero says the height is constant: very simple, and very weak. "
            "<bookmark mark='c'/>Degree one, a straight line, does better. <bookmark mark='d'/>Degree two, a "
            "parabola, captures the fall: twenty metres, a small linear term, and minus about four point six "
            "times t squared, close to Galileo's law, with g over two equal to four point nine. <bookmark mark='e'/>Degree seven has eight "
            "parameters and hugs the noise. It is the strongest of all, and the least simple. Which is best depends "
            "on how strength trades against simplicity."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.03), FadeIn(side[0]))
            for mk, k, i in zip("bcde", (0, 1, 2, 7), range(1, 5)):
                vo.wait_until(mk)
                self.play(Create(curves[k]), FadeIn(side[i]))
        self.clear_scene()

    def bits(self):
        d = load("best")
        head = label(r"Simplicity and strength, \ in bits", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"L(\text{law}) + L(\text{data} \mid \text{law})", font_size=34).next_to(head, DOWN, buff=0.3)
        ax = Axes(x_range=[0, 8.6, 1], y_range=[0, 200, 50], x_length=7.4, y_length=3.8,
                  axis_config={"color": GREY_B, "font_size": 18}, x_axis_config={"include_ticks": False},
                  y_axis_config={"include_numbers": True}).move_to([-2.2, -1.2, 0])
        nums = VGroup(*[MathTex(str(k), font_size=20, color=GREY_A).next_to(ax.c2p(k + 0.8, 0), DOWN, buff=0.12)
                        for k in range(8)])
        xl = label(r"degree", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.5)
        yl = label(r"bits", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1).align_to(ax, LEFT)
        bars = VGroup()
        for r in d["rows"]:
            x = r["degree"] + 0.8
            b1 = Polygon(ax.c2p(x - 0.3, 0), ax.c2p(x + 0.3, 0), ax.c2p(x + 0.3, r["data_bits"]),
                         ax.c2p(x - 0.3, r["data_bits"]), stroke_width=0, fill_color=CHANCE, fill_opacity=0.75)
            top = r["data_bits"] + r["model_bits"]
            b2 = Polygon(ax.c2p(x - 0.3, r["data_bits"]), ax.c2p(x + 0.3, r["data_bits"]), ax.c2p(x + 0.3, top),
                         ax.c2p(x - 0.3, top), stroke_width=0, fill_color=LAW, fill_opacity=0.9)
            bars.add(VGroup(b1, b2))
        best = d["best_degree"]
        star = MathTex(r"\bigstar", font_size=30, color=GOAL).next_to(bars[best], UP, buff=0.1)
        rb = d["rows"][best]
        assert best == 2 and 60 <= rb["total"] < 61
        side = stack([(r"blue: \ the law's own length, \ $\tfrac{k}{2}\log_2 n$ for $k$ parameters", LAW),
                      (r"orange: \ the data's length, \ given the law", CHANCE),
                      (rf"best: \ degree {best}, \ {rb['total']:.1f} bits", GOAL),
                      (r"Part 15's minimum description length is a best-system account", ABS)], font_size=20,
                     aligned_edge=LEFT, width=4.6).move_to([4.6, -1.0, 0])
        with self.voiceover(
            "Part 15 gave us an exchange rate between simplicity and strength: description length. "
            "<bookmark mark='a'/>Write down the law, then write down the data with the law's help, and count the "
            "bits. <bookmark mark='b'/>The law's own length grows with its parameters, about half the logarithm of "
            "the number of data points for each one. <bookmark mark='c'/>The data's length shrinks as the law fits "
            "better: a strong law leaves little to say. <bookmark mark='d'/>Add them up. The constant and the line "
            "leave too much unexplained. Beyond degree two each extra parameter costs more bits than it saves. "
            "The best system is degree two, at about sixty bits. <bookmark mark='e'/>So minimum "
            "description length is a precise best-system account. The machine-learning idea and Lewis's metaphysics "
            "of law are the same idea."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(nums))
            vo.wait_until("b")
            self.play(*[FadeIn(b[1]) for b in bars], FadeIn(side[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(b[0]) for b in bars], FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(star), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def objections(self):
        head = label(r"Three objections", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the language", r"let $F$ be true of exactly the things in our world: \ then `$\forall x\, Fx$' is "
                              r"simple and says everything. \ Lewis (1983): \ only natural properties count", BAD),
            (r"the balance", r"who sets the exchange rate? \ Lewis: \ if nature is kind, \ one system wins on any "
                             r"reasonable rate", ABS),
            (r"explanation", r"if the laws summarize the facts, \ can they explain the facts? \ the summary seems to "
                             r"depend on what it summarizes", CHANCE),
        ]
        g = rows_table(rows, top=1.7, gap=0.55, width=9.4, x_text=-3.6, label_size=22, text_size=21)
        with self.voiceover(
            "Three objections. <bookmark mark='a'/>The language. Simplicity depends on the words. Let F be a "
            "predicate true of exactly the things in our world, each doing just what it does. Then the single axiom, "
            "everything is F, is perfectly simple and perfectly strong. Lewis replied in 1983 that the axioms must "
            "be stated in terms of natural properties, the ones that carve nature at its joints. "
            "<bookmark mark='b'/>The balance. Who decides how much strength is worth how much simplicity? Lewis "
            "hoped that nature is kind: that one system wins under any reasonable exchange rate, as degree two won "
            "here. <bookmark mark='c'/>And explanation. We explain why the ball fell by citing the law. But if the "
            "law is just a summary of facts like the ball's fall, the explanation seems to run in a circle. "
            "Humeans answer that scientific explanation unifies facts; it need not produce them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def mentaculus(self):
        head = label(r"The Mentaculus", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        parts = [(r"the dynamical laws", r"how states evolve: \ Newton, \ or the Schrödinger equation", LAW),
                 (r"the Past Hypothesis", r"the universe began in a state of very low entropy \ (chapter 11)",
                  TIME),
                 (r"the statistical postulate", r"a uniform probability over the states that fit the Past "
                                                r"Hypothesis", CHANCE)]
        g = rows_table(parts, top=1.5, gap=0.55, width=8.0, x_text=-2.2, label_size=22, text_size=21)
        plus = label(r"= \ a probability for every macroscopic history: \ Albert and Loewer's best system",
                     font_size=22, color=GOAL).next_to(g, DOWN, buff=0.8)
        with self.voiceover(
            "David Albert and Barry Loewer push the best-system account as far as it goes. They borrowed a name "
            "from a Coen brothers film: the Mentaculus, a probability map of the world. <bookmark mark='a'/>Its "
            "axioms are the dynamical laws, <bookmark mark='b'/>a statement that the universe began in a state of "
            "very low entropy, which we will meet in chapter eleven, <bookmark mark='c'/>and a uniform probability "
            "over the states compatible with that beginning. <bookmark mark='d'/>Together, they claim, these three "
            "assign a probability to every macroscopic history, which is to say they would put chance and the arrow "
            "of time inside the best system. Hold on to all three ingredients: this part builds each of them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(plus))
        self.clear_scene()
