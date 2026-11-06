from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Empiricism(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Constructive empiricism", r"Must we believe in what we cannot see?",
                            lit=(1962, 1983), part=PART)
        with self.voiceover("Chapter ten. Constructive empiricism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.vanfraassen()
        self.continuum()
        self.hacking()
        self.badlot()

    def vanfraassen(self):
        hc = history_card(1980, r"Bas van Fraassen", r"\textit{The Scientific Image}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = [
            (r"the aim", r"science aims at theories that are \textit{empirically adequate}: \ true about what is "
                         r"observable", ANTI),
            (r"acceptance", r"to accept a theory is to believe it empirically adequate, \ not true", ANTI),
            (r"literalism", r"theories are read literally: \ not instruments, \ not translations into observation "
                            r"talk", THEORY),
            (r"the virtue", r"less belief, \ less risk: \ success is explained by selection, \ like a species' fit "
                            r"to its niche", OK),
            (r"the cost", r"why should the line between observable and unobservable carry epistemic weight?", BAD),
        ]
        g = rows_table(rows, top=1.4, gap=0.45, width=8.6, x_text=-2.8)
        with self.voiceover(
            "Bas van Fraassen gave anti-realism its modern form. <bookmark mark='a'/>Science aims at theories that "
            "are empirically adequate: true about what is observable, whatever they say about the rest. "
            "<bookmark mark='b'/>To accept a theory is to believe that it is empirically adequate, not that it is "
            "true. <bookmark mark='c'/>Unlike the logical empiricists, he reads theories literally: electron talk "
            "is about electrons, and is true or false, but we need not believe it. <bookmark mark='d'/>The virtue "
            "is epistemic caution, and success needs no miracle: theories survive because they were selected for "
            "fitting the phenomena, as species fit their niches. <bookmark mark='e'/>The cost: why should a line "
            "drawn by human eyesight carry so much epistemic weight?"
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def continuum(self):
        hc = history_card(1962, r"Grover Maxwell", r"`The Ontological Status of Theoretical Entities'", width=6.6,
                          color=HIST).to_corner(UL, buff=0.35)
        steps = [r"naked eye", r"window", r"spectacles", r"binoculars", r"light microscope", r"electron microscope",
                 r"bubble chamber"]
        xs = np.linspace(-5.8, 5.8, len(steps))
        line = Arrow([-6.4, 0.2, 0], [6.4, 0.2, 0], buff=0, color=GREY_B, stroke_width=3)
        dots = VGroup(*[Dot([x, 0.2, 0], color=ANTI if i < 4 else REAL, radius=0.1) for i, x in enumerate(xs)])
        names = VGroup(*[label(s, font_size=17, color=ANTI if i < 4 else REAL).next_to(d, UP if i % 2 == 0 else DOWN,
                                                                                         buff=0.2)
                         for i, (s, d) in enumerate(zip(steps, dots))])
        cut = DashedLine([(xs[3] + xs[4]) / 2, 1.3, 0], [(xs[3] + xs[4]) / 2, -0.9, 0], color=BAD)
        cl = label(r"van Fraassen's line", font_size=17, color=BAD).next_to(cut, UP, buff=0.1)
        rows = stack([(r"Maxwell: \ seeing shades into detecting without a break; \ any cut is arbitrary", WHITE),
                      (r"van Fraassen: \ vague, \ but not empty: \ the moons of Jupiter could be seen by an astronaut, "
                       r"\ an electron never", ANTI),
                      (r"`observable' means observable by \textit{us}: \ the line is fixed by human physiology", GREY_A),
                      (r"Churchland \ (1985): \ a creature with electron-microscope eyes would then believe more", BAD)],
                     font_size=20, aligned_edge=LEFT, width=12.4).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Grover Maxwell had already attacked the line in 1962. <bookmark mark='a'/>We look at things with the "
            "naked eye, through a window, through spectacles, through binoculars, a light microscope, an electron "
            "microscope, and at tracks in a bubble chamber. <bookmark mark='b'/>Where does seeing end and inferring "
            "begin? Maxwell said there is no principled place, and any cut is arbitrary. "
            "<bookmark mark='c'/>Van Fraassen replied that a vague line is still a line. The moons of Jupiter are "
            "observable, because an astronaut could fly there and look; an electron never is. "
            "<bookmark mark='d'/>Observable means observable by us, a fact about human physiology. "
            "<bookmark mark='e'/>Paul Churchland pressed the consequence: a species with electron microscopes for "
            "eyes would then be entitled to believe more of the same theory."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(GrowArrow(line), LaggedStart(*[AnimationGroup(FadeIn(d), FadeIn(n)) for d, n in
                                                     zip(dots, names)], lag_ratio=0.25), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(cut), FadeIn(cl), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def hacking(self):
        hc = history_card(1983, r"Ian Hacking", r"\textit{Representing and Intervening}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        grid = VGroup(*[Dot([x * 0.32, y * 0.32, 0], radius=0.05, color=THEORY) for x in range(-3, 4)
                        for y in range(-3, 4)]).move_to([-3.6, -0.6, 0])
        frame = Square(side_length=2.6, color=GREY_B).move_to(grid)
        gl = label(r"a grid, \ seen through microscopes using different physics", font_size=17, color=GREY_A).next_to(
            frame, DOWN, buff=0.2)
        rows = stack([(r"entity realism: \ believe in the entities we manipulate, \ not necessarily the theories", REAL),
                      (r"`so far as I'm concerned, \ if you can spray them then they are real'", GOAL),
                      (r"the argument from coincidence: \ light, \ fluorescence and electron microscopes show the same "
                       r"grid", OK),
                      (r"experiment has a life of its own: \ its knowledge outlives theories", THEORY)],
                     font_size=20, aligned_edge=LEFT, width=6.4).move_to([3.0, -0.4, 0])
        with self.voiceover(
            "Ian Hacking moved the debate from theory to practice. <bookmark mark='a'/>Entity realism: believe in "
            "the entities we can manipulate, even if our theories of them are false. "
            "<bookmark mark='b'/>Of an experiment that sprayed electrons onto a niobium ball to change its charge, "
            "he wrote: so far as I'm concerned, if you can spray them, then they are real. "
            "<bookmark mark='c'/>He also gave an argument from coincidence. A tiny grid seen through a light "
            "microscope, a fluorescence microscope and an electron microscope looks the same, though the three use "
            "entirely different physical processes. It would be a miracle if the grid were an artefact of each. "
            "<bookmark mark='d'/>Experiment, Hacking said, has a life of its own, and its knowledge outlives the "
            "theories of its day."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(frame), FadeIn(grid), FadeIn(gl))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def badlot(self):
        head = label(r"The best of a bad lot \ (van Fraassen, \ 1989)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cands = VGroup(*[VGroup(RoundedRectangle(width=1.6, height=0.6, corner_radius=0.12, color=c, stroke_width=2),
                                label(t, font_size=17, color=c)) for t, c in
                         ((r"$H_1$", GREY_A), (r"$H_2$", GREY_A), (r"$H_3$", OK), (r"$H_4$", GREY_A))])
        for c in cands:
            c[1].move_to(c[0])
        cands.arrange(RIGHT, buff=0.35).move_to([-2.6, 1.0, 0])
        box = SurroundingRectangle(cands, color=GREY_B, buff=0.25)
        bl = label(r"the hypotheses anyone has thought of", font_size=17, color=GREY_A).next_to(box, UP, buff=0.1)
        truth = VGroup(Star(n=5, outer_radius=0.3, color=GOAL, fill_opacity=0.7),
                       label(r"the truth?", font_size=17, color=GOAL)).arrange(DOWN, buff=0.1).move_to([2.6, 1.0, 0])
        best = label(r"best explanation", font_size=17, color=OK).next_to(box, DOWN, buff=0.12).set_x(
            cands[2].get_x())
        rows = stack([(r"IBE ranks the candidates we have; \ it cannot tell us the truth is among them", BAD),
                      (r"$P(\text{best is true}) \le P(\text{the truth is among the candidates})$", THEORY),
                      (r"the realist needs a privilege: \ that scientists' candidate lists tend to contain the truth", REAL),
                      (r"Stanford's unconceived alternatives \ (Chapter 6) \ say history refutes that privilege", BAD),
                      (r"Lipton \ (2004): \ the same comparative skill that ranks them also generates good candidates",
                       OK)], font_size=19, aligned_edge=LEFT, width=12.4).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Van Fraassen had a second argument, against the inference that powers the no-miracles argument. "
            "<bookmark mark='a'/>Inference to the best explanation ranks the hypotheses that someone has thought of, "
            "and picks the best. <bookmark mark='b'/>But it cannot tell us that the truth is among them. The best "
            "of a bad lot is still bad. <bookmark mark='c'/>The probability that the best candidate is true can be "
            "no higher than the probability that the truth was a candidate. <bookmark mark='d'/>So the realist "
            "needs a privilege: that scientists tend to think of the truth. <bookmark mark='e'/>Stanford's history of "
            "unconceived alternatives argues that the privilege fails. <bookmark mark='f'/>Peter Lipton replied that "
            "the comparative skill that ranks hypotheses is the same skill that generates good ones, so the two "
            "cannot be separated."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(box), FadeIn(bl), LaggedStart(*[FadeIn(c) for c in cands], lag_ratio=0.2))
            self.play(FadeIn(best), Indicate(cands[2], color=OK))
            vo.wait_until("b")
            self.play(FadeIn(truth), FadeIn(rows[0]))
            for mk, r in zip("cdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
