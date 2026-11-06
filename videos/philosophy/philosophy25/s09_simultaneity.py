from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Simultaneity(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Is simultaneity a convention?", r"Even for one observer, \ when is `now' over "
                            r"there?", lit=(1928, 1977), part=PART)
        with self.voiceover("Chapter eight. Is simultaneity a convention?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.signal()
        self.transport()
        self.malament()
        self.debate()

    def signal(self):
        d = load("eps")
        head = label(r"Reichenbach's $\varepsilon$", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        o = np.array([-3.4, -2.4, 0])
        s = 2.0
        P = lambda t, x: o + s * np.array([x, t, 0])  # noqa: E731
        me = Line(P(0, 0), P(2.3, 0), color=MATTER, stroke_width=4)
        mirror = Line(P(0, 1.0), P(2.3, 1.0), color=SPACE, stroke_width=4)
        ml = label(r"me", font_size=19, color=MATTER).next_to(P(0, 0), DOWN, buff=0.15)
        mrl = label(r"mirror", font_size=19, color=SPACE).next_to(P(0, 1.0), DOWN, buff=0.15)
        eps = ValueTracker(0.5)

        def light():
            e = eps.get_value()
            t2 = 2.0 * e
            return VGroup(Line(P(0, 0), P(t2, 1.0), color=LIGHT, stroke_width=3),
                          Line(P(t2, 1.0), P(2.0, 0), color=LIGHT, stroke_width=3),
                          DashedLine(P(t2, 0), P(t2, 1.0), color=TIME), Dot(P(t2, 1.0), radius=0.08, color=LIGHT))

        lt = always_redraw(light)
        labs = VGroup(MathTex(r"t_1", font_size=26, color=MATTER).next_to(P(0, 0), LEFT, buff=0.12),
                      MathTex(r"t_3", font_size=26, color=MATTER).next_to(P(2.0, 0), LEFT, buff=0.12))
        elab = always_redraw(lambda: MathTex(rf"\varepsilon = {eps.get_value():.2f}", font_size=30, color=TIME
                                             ).move_to(P(2.6, 0.5)))
        f = MathTex(r"t_2 = t_1 + \varepsilon\,(t_3 - t_1), \qquad 0 < \varepsilon < 1", font_size=32,
                    color=ABS).move_to([3.2, 1.6, 0])
        side = stack([(r"send light to a distant mirror at $t_1$; \ it returns at $t_3$", LIGHT),
                      (r"when did it reach the mirror? \ only a round trip can be timed", WHITE),
                      (r"Einstein: \ by definition, \ halfway: \ $\varepsilon = \tfrac12$", OK),
                      (r"Reichenbach \ (1928): \ any $\varepsilon$ fits every observation", BAD),
                      (r"so `now, over there' is fixed by a choice", GOAL)], font_size=21, aligned_edge=LEFT,
                     width=5.6, buff=0.28).move_to([3.4, -0.9, 0])
        assert [r["t2"] for r in d["rows"]] == [0.5, 1.0, 1.5]
        with self.voiceover(
            "Relativity says that different observers disagree about simultaneity. Hans Reichenbach argued that "
            "even a single observer has to choose it. <bookmark mark='a'/>I send a light signal at time t one to a "
            "distant mirror, and it comes back at t three. <bookmark mark='b'/>When did it reach the mirror? I can "
            "only time the round trip; to time the outward leg I would need a clock at the mirror already "
            "synchronized with mine, which is the very thing in question. <bookmark mark='c'/>Einstein's definition: "
            "halfway, epsilon equal to one half. <bookmark mark='d'/>Reichenbach: any epsilon between zero and one "
            "is consistent with every observation, so long as we use it consistently. <bookmark mark='e'/>If so, "
            "which distant events are happening now is fixed by a convention, not by the world."
        ) as vo:
            self.play(FadeIn(head), Create(me), Create(mirror), FadeIn(ml), FadeIn(mrl), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(lt), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(elab), FadeIn(side[2]), Write(f))
            vo.wait_until("d")
            self.play(eps.animate.set_value(0.25), FadeIn(side[3]), run_time=1.5)
            self.play(eps.animate.set_value(0.75), run_time=2)
            self.play(eps.animate.set_value(0.5), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        lt.clear_updaters()
        elab.clear_updaters()
        self.clear_scene()

    def transport(self):
        d = load("transport")
        head = label(r"Carry a clock", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"\Delta\tau = \frac{L}{v}\left(1 - \sqrt{1 - v^2}\right) \approx \frac{L v}{2}",
                    font_size=36, color=ABS).next_to(head, DOWN, buff=0.35)
        hd = [r"\text{transport speed } v", r"\text{clock's lag}", r"\text{the }\varepsilon\text{ it gives}"]
        rows = []
        for r in d["rows"]:
            m, e = f"{r['lag']:.1e}".split("e")
            rows.append([MathTex(f"{r['v']:g}", font_size=24), MathTex(rf"{m} \times 10^{{{int(e)}}}", font_size=24),
                         MathTex(f"{r['eps']:.4f}", font_size=24, color=OK)])
        grid = ValueGrid(hd, rows, col_w=[3.0, 2.8, 2.6], cell_h=0.5, font_size=22).move_to([-2.5, -1.0, 0])
        side = stack([(r"synchronize two clocks, \ then carry one slowly to the distant mirror", WHITE),
                      (r"time dilation makes it lag, \ by an amount that vanishes as $v \to 0$", ABS),
                      (r"infinitely slow transport gives $\varepsilon = \tfrac12$: \ Einstein's synchrony", OK),
                      (r"the conventionalist: \ `slow' already assumes the answer", BAD)], font_size=20,
                     aligned_edge=LEFT, width=4.4, buff=0.3).move_to([4.6, -0.9, 0])
        with self.voiceover(
            "Is there an independent way to synchronize distant clocks? <bookmark mark='a'/>Set two clocks side by "
            "side, then carry one of them to the distant mirror. <bookmark mark='b'/>Moving clocks run slow, so the "
            "carried clock falls behind, by this amount, which for slow transport is about L v over two. The Reasoner "
            "tabulates it for speeds from half the speed of light down to a thousandth. <bookmark mark='c'/>The lag "
            "vanishes as the speed goes to zero, and the synchrony it gives approaches epsilon equal to one half, "
            "Einstein's choice, as Arthur Eddington and later Brian Ellis and Peter Bowman pointed out. "
            "<bookmark mark='d'/>The conventionalist's reply is that the formula for time dilation was itself "
            "derived using Einstein's synchrony, so slow transport cannot independently confirm it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(side[1]), FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def malament(self):
        hc = history_card(1977, r"David Malament", r"`Causal Theories of Time and the Conventionality of "
                          r"Simultaneity'", width=6.8, color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"start from the causal structure: \ which events can signal to which", LIGHT),
                      (r"add an inertial observer's worldline", MATTER),
                      (r"ask which simultaneity relations can be defined from these alone, \ and respect their "
                       r"symmetries", ABS),
                      (r"theorem: \ exactly one, \ apart from trivial ones: \ $\varepsilon = \tfrac12$", OK),
                      (r"so standard simultaneity is not a choice: \ the causal structure fixes it", GOAL)],
                     font_size=22, aligned_edge=LEFT, width=11.6, buff=0.32).move_to([0, -0.4, 0])
        with self.voiceover(
            "In 1977 David Malament proved a theorem that most physicists and many philosophers took to settle the "
            "matter. <bookmark mark='a'/>Start only from the causal structure of Minkowski spacetime: which events "
            "can send a signal to which. <bookmark mark='b'/>Add the worldline of one inertial observer. "
            "<bookmark mark='c'/>Now ask which simultaneity relations can be defined from those alone, in a way that "
            "respects their symmetries. <bookmark mark='d'/>Malament showed there is exactly one, apart from trivial "
            "relations that make everything or nothing simultaneous, and it is Einstein's, epsilon equal to one half. "
            "<bookmark mark='e'/>So standard simultaneity is not a convention after all: the causal structure "
            "already determines it."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def debate(self):
        head = label(r"Settled?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the objection", r"Malament assumes time-reflection symmetry; \ drop it, \ and other $\varepsilon$ are "
                               r"definable \ (Sarkar and Stachel, \ 1999)", BAD),
            (r"the reply", r"but any $\varepsilon \neq \tfrac12$ singles out a direction in space for no physical "
                           r"reason", OK),
            (r"what is not at issue", r"for each observer there is a natural simultaneity; \ across observers, \ "
                                      r"none is privileged", SPACE),
            (r"what is at issue next", r"if `now' depends on the observer, \ what becomes of the present \ (chapters "
                                       r"9 and 10)?", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.8, label_size=22, text_size=21)
        with self.voiceover(
            "Is it settled? Mostly. <bookmark mark='a'/>Critics, among them Sahotra Sarkar and John Stachel in 1999, "
            "pointed out that Malament assumes the simultaneity relation is unchanged by reflecting time; drop that, "
            "and other choices become definable. <bookmark mark='b'/>The reply is that any epsilon other than one "
            "half picks out a direction in space for no physical reason. <bookmark mark='c'/>What is not in dispute: "
            "for each observer there is a natural simultaneity, and across observers none is privileged. "
            "<bookmark mark='d'/>That raises the question of the next two chapters. If now depends on who is asking, "
            "what becomes of the present, and of the idea that only the present is real?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
