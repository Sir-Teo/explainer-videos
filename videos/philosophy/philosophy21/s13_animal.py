from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Animal(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Animalism", r"Are you an animal?", lit=(1997, 2007), part=PART)
        with self.voiceover("Chapter twelve. Animalism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.thesis()
        self.thinking()
        self.brain()
        self.brownson()

    def thesis(self):
        hc = history_card(1997, r"Eric Olson", r"\textit{The Human Animal: Personal Identity without Psychology}",
                          width=7.6, color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"the thesis", r"each of us is a human animal, \ an organism \ (Part 19); \ we persist as animals do", OK),
            (r"its criterion", r"biological continuity: \ the same life, \ in van Inwagen's sense \ (Part 20)", UNIV),
            (r"so", r"you were once a foetus, \ and could survive in a persistent vegetative state", WHOLE),
            (r"and", r"psychology is not what makes you persist, \ though it may be what matters", GREY_A),
            (r"transplant", r"move your cerebrum to another head: \ animalism says you stay behind, \ as the animal "
                            r"with the empty skull", BAD),
        ]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Psychological views say you go where your psychology goes. Animalism disagrees. "
            "<bookmark mark='a'/>Eric Olson and Paul Snowdon hold that each of us is a human animal, an organism of "
            "the kind Part 19 studied, and persists as animals do. <bookmark mark='b'/>The criterion is biological: "
            "the same life, in van Inwagen's sense from Part 20. <bookmark mark='c'/>So you were once a foetus, which "
            "had no psychology at all, and you could survive in a persistent vegetative state. "
            "<bookmark mark='d'/>Psychology is not what makes you persist, though it may be what matters to you. "
            "<bookmark mark='e'/>The hard case is the transplant. Move your cerebrum into another skull: animalism "
            "says you remain behind, as the animal whose skull is empty, and the person who wakes with your memories "
            "is someone else. Most people's intuitions disagree."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def thinking(self):
        head = label(r"The thinking-animal problem", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        steps = stack([(r"1. \ there is a human animal sitting in your chair", WHITE),
                       (r"2. \ the animal is thinking your thoughts", WHITE),
                       (r"3. \ you are the thing thinking your thoughts", WHITE),
                       (r"4. \ so you are the animal \ (unless two thinkers share every thought)", OK)], font_size=21,
                      aligned_edge=LEFT, width=8.4).move_to([1.9, 1.15, 0])
        chair = VGroup(Line([-5.7, 0.55, 0], [-4.5, 0.55, 0]), Line([-5.7, 0.55, 0], [-5.7, 1.9, 0]),
                       Line([-5.6, 0.55, 0], [-5.6, -0.1, 0]), Line([-4.6, 0.55, 0], [-4.6, -0.1, 0])).set_stroke(
            GREY_B, 3)
        sitter = VGroup(Circle(radius=0.24, color=NOM, fill_opacity=0.25).move_to([-5.05, 2.05, 0]),
                        Line([-5.05, 1.8, 0], [-5.2, 0.75, 0]), Line([-5.2, 0.75, 0], [-4.4, 0.75, 0]),
                        Line([-4.4, 0.75, 0], [-4.35, 0.0, 0]), Line([-5.1, 1.5, 0], [-4.55, 1.15, 0])).set_stroke(
            NOM, 3)
        la = label(r"the animal", font_size=20, color=PARTC).move_to([-6.1, 2.95, 0])
        lp = label(r"the person", font_size=20, color=NOM).move_to([-3.9, 2.95, 0])
        aa = Arrow(la.get_bottom(), [-5.2, 2.2, 0], buff=0.08, color=PARTC, stroke_width=2.5)
        ap = Arrow(lp.get_bottom(), [-4.9, 2.2, 0], buff=0.08, color=NOM, stroke_width=2.5)
        q = MathTex(r"=\,?", font_size=34, color=GOAL).move_to([-5.0, 3.0, 0])
        rows = stack([(r"the psychological theorist must deny 1, \ or 2, \ or accept two thinkers in one chair", BAD),
                      (r"and then: \ how do you know you are the person, \ not the animal?", GOAL),
                      (r"replies: \ the animal thinks derivatively, \ by constituting you \ (Baker); \ or there is "
                       r"no animal \ (van Inwagen's simples, \ no)", UNIV),
                      (r"the debate mirrors the statue and the lump \ (chapter 3)", GREY_A)], font_size=19,
                     aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Olson's main argument. <bookmark mark='a'/>There is a human animal sitting in your chair. "
            "<bookmark mark='b'/>It is thinking your thoughts: it has a working brain. <bookmark mark='c'/>You are the "
            "thing thinking your thoughts. <bookmark mark='d'/>So you are the animal, unless there are two thinkers "
            "in your chair, sharing every thought. <bookmark mark='e'/>A psychological theorist must deny that there "
            "is an animal, or that it thinks, or accept two thinkers. And then how could you tell which one you are? "
            "<bookmark mark='f'/>Lynne Rudder Baker replies that the animal thinks only derivatively, by constituting "
            "you; the structure is the statue and the lump again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(chair), FadeIn(sitter), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(la), GrowArrow(aa), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(lp), GrowArrow(ap), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(q), FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("f")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.clear_scene()

    def brain(self):
        head = label(r"Between the animal and the psychology", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the brain view", r"Nagel; \ McMahan's embodied mind \ (2002): \ you are the part of the organism that "
                                r"supports consciousness", NOM),
            (r"remnant persons", r"Johnston \ (2007): \ a living head without its body: \ the animal is gone, \ you "
                                 r"are not", BAD),
            (r"constitution", r"Baker: \ a person is constituted by an animal, \ as the statue by the lump", WHOLE),
            (r"narrative", r"Schechtman \ (1996): \ persons are constituted by the stories they live and tell", UNIV),
            (r"the pattern", r"each view picks a different relation \ (life, \ brain, \ psychology, \ story) \ to be "
                             r"the one that counts", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Between animalism and psychological views lie others. <bookmark mark='a'/>The brain view, suggested by "
            "Thomas Nagel and developed by Jeff McMahan as the embodied mind account: you are the part of the "
            "organism that supports your consciousness. <bookmark mark='b'/>Mark Johnston's remnant persons: imagine "
            "your head kept alive without your body. The animal, arguably, is gone; you are not. "
            "<bookmark mark='c'/>Lynne Rudder Baker's constitution view: a person is constituted by an animal, as the "
            "statue is by the lump. <bookmark mark='d'/>Marya Schechtman's narrative view: persons are constituted "
            "by the stories they live and tell. <bookmark mark='e'/>Each picks a different relation, a life, a "
            "brain, a psychology or a story, to be the one that counts."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def brownson(self):
        hc = history_card(1963, r"Sydney Shoemaker", r"\textit{Self-Knowledge and Self-Identity}", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        brown = VGroup(Circle(radius=0.3, color=NOM).move_to([-5.2, 0.5, 0]),
                       label(r"Brown", font_size=16, color=NOM).move_to([-5.2, -0.1, 0]))
        robin = VGroup(Circle(radius=0.3, color=PARTC).move_to([-2.6, 0.5, 0]),
                       label(r"Robinson", font_size=16, color=PARTC).move_to([-2.6, -0.1, 0]))
        brain = Ellipse(width=0.4, height=0.28, color=GOAL, fill_opacity=0.6).move_to([-5.2, 0.5, 0])
        ar = CurvedArrow([-5.0, 0.9, 0], [-2.8, 0.9, 0], angle=-PI / 3, color=GOAL)
        res = label(r"Brownson: \ Robinson's body, \ Brown's brain", font_size=17, color=GOAL).move_to([-3.9, -1.0, 0])
        rows = stack([(r"Brown's brain is put into Robinson's skull", WHITE),
                      (r"the man who wakes has Brown's memories and character", NOM),
                      (r"he recognises Brown's wife, \ not Robinson's", GREY_A),
                      (r"most judge: \ he is Brown, \ in a new body", OK),
                      (r"the animalist must say he is Robinson, \ with a new brain", BAD)], font_size=20,
                     aligned_edge=LEFT, width=6.0).move_to([3.5, -0.4, 0])
        with self.voiceover(
            "Sydney Shoemaker's case is the classic test for animalism. <bookmark mark='a'/>Brown's brain is put into "
            "Robinson's skull, and the result is called Brownson. <bookmark mark='b'/>Brownson has Brown's memories "
            "and Brown's character. <bookmark mark='c'/>He recognises Brown's wife and children, not Robinson's. "
            "<bookmark mark='d'/>Most people judge that Brownson is Brown, in a new body. <bookmark mark='e'/>If the "
            "brain is a proper part of the animal, as Olson thinks, the animalist must say Brownson is Robinson, with "
            "a new brain; or, on Olson's own view, that Brown's animal has been pared down to a brain and moved. "
            "Either way, intuition strains."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(brown), FadeIn(robin), FadeIn(brain))
            vo.wait_until("a")
            self.play(Create(ar), brain.animate.move_to([-2.6, 0.5, 0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(res), FadeIn(rows[1]))
            for mk, r in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
