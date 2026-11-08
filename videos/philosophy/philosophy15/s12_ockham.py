from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403


class Ockham(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Ockham's razor, \ justified", r"Why prefer the simpler theory?", lit=(1320, 2007),
                            part=PART)
        with self.voiceover("Chapter eleven. Ockham's razor, justified."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.razor()
        self.game()
        self.theorem()
        self.automatic()

    def razor(self):
        hc = history_card(1323, r"William of Ockham", r"\textit{Summa Logicae}", width=5.0,
                          color=HIST).to_corner(UL, buff=0.35)
        q = quote_card(r"Plurality is never to be posited without necessity.", r"William of Ockham",
                       r"\textit{Commentary on the Sentences}", width=8.4, font_size=26).next_to(hc, DOWN, buff=0.4).set_x(0)
        puzzle = stack([(r"scientists prefer simpler theories: \ Copernicus, \ Newton, \ Einstein", WHITE),
                        (r"but why would the world be simple?", BAD),
                        (r"if the razor is a bias toward simplicity, \ how can it lead to \textit{truth}?", GOAL)],
                       font_size=23).next_to(q, DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "Every learner needs a bias, and the favourite bias of science is simplicity. "
            "<bookmark mark='a'/>William of Ockham, in the fourteenth century: plurality is never to be posited "
            "without necessity. <bookmark mark='b'/>Copernicus, Newton and Einstein all argued that their theories "
            "were simpler than the rivals. <bookmark mark='c'/>But why would the world be simple? "
            "<bookmark mark='d'/>If the razor is only a bias, a taste for simplicity, how could it lead us to the "
            "truth, rather than to the theories we find convenient?"
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcd", puzzle):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def game(self):
        d = load("ockham")
        head = label(r"Kelly's game: \ how many particles are there?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rule = stack([(r"Nature reveals particles one at a time, \ and may hold the next one back as long as it likes",
                       WHITE),
                      (r"a learner must \textit{converge} on the true count", GREY_A)], font_size=21).next_to(
            head, DOWN, buff=0.25)
        H = len(d["ockham"])
        ax = Axes(x_range=[0, H, 4], y_range=[0, 4, 1], x_length=10.0, y_length=3.1, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 18}).move_to([-0.4, -0.95, 0])
        xl = label(r"time", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
        yl = label(r"conjectured count", font_size=18, color=GREY_B).next_to(ax.y_axis, UP, buff=0.1)

        def steps(ys, col, dy=0.0):
            pts = []
            for t, y in enumerate(ys):
                pts += [ax.c2p(t, y + dy), ax.c2p(t + 1, y + dy)]
            return VMobject(stroke_color=col, stroke_width=4).set_points_as_corners(pts)
        stars = VGroup(*[Star(n=5, outer_radius=0.14, color=PAST, fill_opacity=1).move_to(ax.c2p(t + 0.5, 4.2))
                         for t in d["effects"]])
        sl = label(r"a particle appears", font_size=17, color=PAST).next_to(stars[0], LEFT, buff=0.2)
        ock = steps(d["ockham"], OK, 0.04)
        bold = steps(d["bold"], BAD, -0.04)
        retr = VGroup()
        for t in range(1, H):
            if d["bold"][t] < d["bold"][t - 1]:
                retr.add(Circle(radius=0.17, color=BAD, stroke_width=3).move_to(ax.c2p(t, (d["bold"][t] +
                                                                                       d["bold"][t - 1]) / 2)))
        leg = stack([(r"Ockham: \ conjecture exactly the particles seen \ \ (retractions: \ " +
                      str(d["ockham_retractions"]) + r")", OK),
                     (r"bold: \ after a quiet spell, \ anticipate one more \ \ (retractions: \ " +
                      str(d["bold_retractions"]) + r")", BAD)], font_size=20, aligned_edge=LEFT).to_edge(DOWN,
                                                                                                    buff=0.15)
        with self.voiceover(
            "Kevin Kelly found a precise sense in which the razor helps. Here is his game. "
            "<bookmark mark='a'/>Nature reveals particles, or effects, one at a time, and may hold the next one "
            "back as long as it likes. A learner must eventually settle on the true number. "
            "<bookmark mark='b'/>Particles appear at three moments. <bookmark mark='c'/>The Ockham learner "
            "conjectures exactly as many particles as it has seen. It never takes anything back: when a particle "
            "appears, it adds one. <bookmark mark='d'/>A bold learner gets impatient, and after a quiet spell it "
            "anticipates one more particle. Nature simply withholds it. The bold learner eventually gives up its "
            "guess, and the moment it does, Nature reveals the particle. <bookmark mark='e'/>Each time, the bold "
            "learner is forced to retract: three retractions, against Ockham's none."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rule), FadeIn(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s, scale=1.5) for s in stars], lag_ratio=0.3), FadeIn(sl))
            vo.wait_until("c")
            self.play(Create(ock), FadeIn(leg[0]), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(bold), FadeIn(leg[1]), run_time=3)
            vo.wait_until("e")
            self.play(LaggedStart(*[Create(c) for c in retr], lag_ratio=0.3))
        self.clear_scene()

    def theorem(self):
        hc = history_card(2007, r"Kevin Kelly", r"`Ockham's Razor, \ Empirical Complexity, \ and Truth-finding "
                          r"Efficiency'", width=7.4, color=HIST).to_corner(UL, buff=0.35)
        thm = stack([
            (r"\textbf{Theorem.} \ Among methods that converge to the truth,", WHITE),
            (r"Ockham's method has the fewest retractions in the worst case;", OK),
            (r"every method that violates Ockham's razor \ can be forced into at least one more", BAD),
        ], font_size=24, aligned_edge=LEFT).next_to(hc, DOWN, buff=0.45).set_x(0)
        meta = stack([
            (r"it does \textit{not} say that simple theories are more likely true", GREY_A),
            (r"it says the Ockham path to the truth is the most direct", FUT),
            (r"like the best route home \ when you don't know where home is", PAST),
        ], font_size=23).next_to(thm, DOWN, buff=0.55)
        with self.voiceover(
            "Kelly proved that this is no accident. <bookmark mark='a'/>Among all methods that are guaranteed to "
            "converge to the truth, <bookmark mark='b'/>Ockham's method has the fewest retractions in the worst "
            "case, <bookmark mark='c'/>and any method that ever violates the razor can be forced by Nature into "
            "at least one retraction more. <bookmark mark='d'/>Notice what the theorem does not say. It does not "
            "say that simpler theories are more likely to be true. <bookmark mark='e'/>It says that preferring the "
            "simplest theory compatible with the data is the most direct route to the truth, whatever the truth "
            "is. <bookmark mark='f'/>It is like the best route home when you do not know where home is: not a "
            "guarantee of arriving soon, but the fewest U-turns."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", thm):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            for mk, r in zip("def", meta):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def automatic(self):
        head = label(r"The Bayesian razor: \ simplicity from the evidence itself", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        eq = MathTex(r"P(D \mid M) = \int P(D \mid \theta, M)\, p(\theta \mid M)\, d\theta", font_size=34,
                     color=FUT).next_to(head, DOWN, buff=0.3)
        ax = Axes(x_range=[-5, 5, 1], y_range=[0, 0.45, 0.1], x_length=9.0, y_length=3.2, tips=False,
                  axis_config={"color": GREY_C, "include_ticks": False}).move_to([0, -1.2, 0])
        xl = label(r"all possible data sets", font_size=19, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.2)
        simple = ax.plot(lambda x: 0.4 * np.exp(-x ** 2 / 1.0), x_range=[-5, 5], color=OK, stroke_width=4)
        complex_ = ax.plot(lambda x: 0.13 * np.exp(-x ** 2 / 12.0), x_range=[-5, 5], color=BAD, stroke_width=4)
        sl = label(r"simple $M_1$: \ few data sets, \ each likely", font_size=19, color=OK).move_to(
            ax.c2p(3.1, 0.36))
        cl = label(r"flexible $M_2$: \ fits almost anything, \ each thinly", font_size=19, color=BAD).move_to(
            ax.c2p(-3.4, 0.27))
        obs = DashedLine(ax.c2p(0.4, 0), ax.c2p(0.4, 0.43), color=GOAL, stroke_width=3)
        ol = label(r"the data we got", font_size=18, color=GOAL).next_to(obs, UP, buff=0.05)
        foot = label(r"both fit; \ the simple model predicted it more sharply, \ and wins the Bayes factor \ "
                     r"(Jefferys and Berger, \ 1992; \ MacKay)", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Bayesians have a razor of their own, which needs no prior preference for simplicity. "
            "<bookmark mark='a'/>The evidence for a model is the probability it gave the data, averaged over its "
            "parameters. <bookmark mark='b'/>A simple model can produce only a few data sets, so it gives each of "
            "them high probability. <bookmark mark='c'/>A flexible model can fit almost anything, so it must spread "
            "its probability thinly. <bookmark mark='d'/>When the data fall where both can fit them, the simple "
            "model predicted them more sharply, and wins. William Jefferys and James Berger called this Ockham's "
            "razor at work, and David MacKay made it a standard tool of machine learning."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(xl), Create(simple), FadeIn(sl))
            vo.wait_until("c")
            self.play(Create(complex_), FadeIn(cl))
            vo.wait_until("d")
            self.play(Create(obs), FadeIn(ol))
            self.play(FadeIn(foot))
        self.clear_scene()
