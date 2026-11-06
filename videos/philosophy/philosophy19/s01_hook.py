from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"Nothing in biology makes sense except in the light of evolution.", r"Theodosius Dobzhansky",
                       r"\textit{The American Biology Teacher} \ (1973)", width=9.6, font_size=26).next_to(
            t, DOWN, buff=0.5)
        with self.voiceover(
            "Part 18 asked what our theories tell us about reality, mostly through physics. This part turns to the "
            "science of living things, which raises its own philosophical questions. <bookmark mark='a'/>Theodosius "
            "Dobzhansky put the organizing idea in one line: nothing in biology makes sense except in the light of "
            "evolution. <bookmark mark='b'/>We will build that light, piece by piece, and test what it can and cannot "
            "explain."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=GOAL, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Purpose without a purposer?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        # an eye, schematically
        eye = VGroup(Ellipse(width=3.2, height=2.0, color=GREY_B, stroke_width=3),
                     Circle(radius=0.6, color=GENE, fill_opacity=0.4),
                     Circle(radius=0.25, color=BLACK, fill_opacity=1, stroke_width=0)).move_to([-4.0, 0.8, 0])
        el = label(r"the eye: \ lens, \ iris, \ retina", font_size=18, color=GREY_A).next_to(eye, DOWN, buff=0.2)
        rows = stack([
            (r"organs look made \textit{for} something: \ the eye is for seeing", WHITE),
            (r"Paley \ (1802): \ so they were made, \ by a designer", ORG),
            (r"Darwin \ (1859): \ variation and selection produce the appearance of design", GENE),
            (r"then: \ what is fitness? \ at what level does selection act? \ what is a function, \ a species, \ "
             r"a gene's `information'?", GOAL),
            (r"and: \ what is life itself, \ and can we build it?", ALT),
        ], font_size=21, aligned_edge=LEFT, width=7.4).move_to([2.6, -0.4, 0])
        with self.voiceover(
            "Living things pose a puzzle that physics does not. <bookmark mark='a'/>Their parts seem made for "
            "something. The eye has a lens to focus, an iris to regulate light, and a retina to detect it: it is "
            "for seeing. <bookmark mark='b'/>William Paley concluded in 1802 that organisms, like watches, were made "
            "by a designer. <bookmark mark='c'/>Charles Darwin showed in 1859 how variation and natural selection "
            "could produce the appearance of design without a designer. <bookmark mark='d'/>But his answer raised "
            "new questions, which this part works through with the mathematics of evolution: what fitness is, at "
            "what level selection acts, what a biological function is, what a species is, and whether genes carry "
            "information. <bookmark mark='e'/>And finally: what is life, and can we build it?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eye), FadeIn(el), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Paley's watch and Darwin's argument, \ as likelihoods",
            r"Lewontin's recipe \ (selection with and without heredity); \ fitness and the Price equation",
            r"replicator dynamics on the simplex; \ hawks and doves; \ the ESS",
            r"Hamilton's rule, \ derived and simulated; \ levels of selection \ (the Wall)",
            r"genes and organisms; \ function and teleology; \ species and trees",
            r"information in the genetic code; \ the evolution of cooperation",
            r"what is life? \ and a creature grown in Lenia",
        ], font_size=24)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Paley against Darwin, as a comparison of likelihoods. "
            "<bookmark mark='b'/>The recipe for natural selection, and the Price equation, which captures all of "
            "it in one line. <bookmark mark='c'/>Evolutionary game theory: replicator dynamics, hawks and doves, and "
            "evolutionarily stable strategies. <bookmark mark='d'/>Kin selection and the levels-of-selection debate: "
            "this part's brick in the Wall. <bookmark mark='e'/>Genes and organisms, function, and species. "
            "<bookmark mark='f'/>Information and cooperation. <bookmark mark='g'/>And what life is, with an "
            "artificial creature grown on screen."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
