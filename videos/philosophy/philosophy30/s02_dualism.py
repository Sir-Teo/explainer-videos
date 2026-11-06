from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


class Dualism(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Two substances", r"Is the mind a thing distinct from the body?", lit=(1641, 1643),
                            part=PART)
        with self.voiceover("Chapter one. Two substances."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.floating()
        self.descartes()
        self.argument()
        self.elisabeth()

    def floating(self):
        hc = history_card(r"c.\ 1020", r"Ibn S\={\i}n\=a \ (Avicenna)", r"\textit{The Book of Healing}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        man = VGroup(Circle(radius=0.3, color=MIND), Line([0, -0.3, 0], [0, -1.3, 0], color=MIND),
                     Line([-0.8, -0.6, 0], [-0.25, -0.75, 0], color=MIND), Line([0.25, -0.75, 0], [0.8, -0.6, 0],
                                                                                 color=MIND),
                     Line([-0.1, -1.3, 0], [-0.55, -2.0, 0], color=MIND), Line([0.1, -1.3, 0], [0.55, -2.0, 0],
                                                                               color=MIND)).move_to([-3.4, -0.3, 0])
        air = VGroup(*[DashedLine([-5.2, y, 0], [-1.6, y, 0], color=GREY_D, dash_length=0.15) for y in (-2.4, 1.6)])
        rows = stack([(r"created in mid-air, \ fully formed, \ eyes covered, \ limbs not touching", WHITE),
                      (r"he senses nothing, \ not even his own body", GREY_A),
                      (r"yet he affirms that he exists", MIND),
                      (r"so the self he affirms is not the body he does not know", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=6.2, buff=0.3).move_to([3.0, -0.3, 0])
        with self.voiceover(
            "The thought experiment is older than Descartes. <bookmark mark='a'/>Around 1020, Ibn Sīnā, known in Latin "
            "as Avicenna, asked us to imagine a man created all at once in mid-air, fully formed, his eyes covered, "
            "his limbs held apart so that they do not touch. <bookmark mark='b'/>He senses nothing, not even his own "
            "body. <bookmark mark='c'/>Yet, Avicenna argued, he would affirm that he exists. "
            "<bookmark mark='d'/>So the self he affirms is something other than the body he does not know: the floating "
            "man."
        ) as vo:
            self.play(FadeIn(hc), Create(air))
            vo.wait_until("a")
            self.play(FadeIn(man), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def descartes(self):
        hc = history_card(1641, r"Ren\'e Descartes", r"\textit{Meditations on First Philosophy}", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        left = VGroup(RoundedRectangle(width=4.4, height=2.4, corner_radius=0.2, color=MIND, fill_opacity=0.08),
                      VGroup(label(r"mind", font_size=26, color=MIND), label(r"thinking, \ unextended, \ indivisible",
                                                                             font_size=18, color=GREY_A),
                             label(r"known with certainty", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.15)
                      ).move_to([-3.2, -0.2, 0])
        right = VGroup(RoundedRectangle(width=4.4, height=2.4, corner_radius=0.2, color=PHYS, fill_opacity=0.08),
                       VGroup(label(r"body", font_size=26, color=PHYS), label(r"extended, \ unthinking, \ divisible",
                                                                              font_size=18, color=GREY_A),
                              label(r"known through the senses, \ doubtfully", font_size=18, color=GREY_A)).arrange(
                           DOWN, buff=0.15)).move_to([3.2, -0.2, 0])
        gland = VGroup(Dot([0, -0.2, 0], radius=0.12, color=SYM),
                       label(r"the pineal gland?", font_size=17, color=SYM).move_to([0, -1.0, 0]))
        arrows = VGroup(Arrow(left.get_right(), [-0.2, -0.2, 0], buff=0.1, color=GREY_B),
                        Arrow(right.get_left(), [0.2, -0.2, 0], buff=0.1, color=GREY_B))
        with self.voiceover(
            "René Descartes, in his Meditations of 1641, made the distinction the starting point of modern "
            "philosophy. <bookmark mark='a'/>The mind is a thinking thing: unextended, indivisible, and known with "
            "more certainty than anything else, since I can doubt everything but that I am thinking. "
            "<bookmark mark='b'/>The body is an extended thing: it takes up space, it is divisible, it does not "
            "think, and it is known only through the senses, which can deceive. <bookmark mark='c'/>Two substances, "
            "each able to exist without the other. Yet they interact: a pin pricks the hand and I feel pain; I decide "
            "to raise my arm and it rises. Descartes located the meeting point in the pineal gland, at the centre of "
            "the brain."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(gland))
        self.clear_scene()

    def argument(self):
        head = label(r"The argument from conceivability", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        steps = VGroup(
            MathTex(r"1.\quad \Diamond\,(\text{I exist} \wedge \neg\,\text{my body exists})", font_size=32),
            MathTex(r"2.\quad \text{if } a = b, \ \text{then } \Box\,(a = b)", r"\qquad\text{(Part 22)}", font_size=32),
            MathTex(r"3.\quad \text{so I} \neq \text{my body}", font_size=32, color=MIND),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([0, 1.0, 0])
        steps[1][1].set_color(GREY_B)
        rows = stack([(r"premise 1 rests on clear and distinct conception: \ what I can conceive, \ God can make", HIST),
                      (r"the reply: \ conceivable is not possible \ (`water is not H$_2$O' is conceivable, \ Part 27)",
                       BAD),
                      (r"the argument returns in Part 31, \ with zombies", GOAL)], font_size=21, aligned_edge=LEFT,
                     width=12.0, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Descartes's main argument can be put in the modal logic of Part 4. <bookmark mark='a'/>It is possible "
            "that I exist and my body does not: I can clearly and distinctly conceive it, and whatever I can so "
            "conceive, God can bring about. <bookmark mark='b'/>If a is b, then necessarily a is b: identity holds "
            "in every possible world, as Part 22 showed. <bookmark mark='c'/>So I am not my body. "
            "<bookmark mark='d'/>The premise that does the work is the first. <bookmark mark='e'/>The standard reply is "
            "that conceivability is a poor guide to possibility: that water is not H two O was once conceivable, and "
            "it is impossible, as Part 27 found. <bookmark mark='f'/>The argument, sharpened, returns in Part 31 as "
            "the argument from zombies."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abc", steps):
                vo.wait_until(mk)
                self.play(Write(s))
            vo.wait_until("d")
            self.play(Indicate(steps[0], color=SYM))
            for mk, r in zip("def", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def elisabeth(self):
        hc = history_card(1643, r"Elisabeth of Bohemia", r"letter to Descartes, \ 16 May", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        q = quote_card(r"How can the soul of a human being, \ being only a thinking substance, \ determine the bodily "
                       r"spirits to perform voluntary actions?", r"Elisabeth of Bohemia", r"1643", width=9.6,
                       font_size=25).move_to([0, 0.6, 0])
        rows = stack([(r"causing motion seemed to need contact and extension, \ and the soul has neither", PHYS),
                      (r"Descartes: \ the union of mind and body is a primitive notion, \ known by living it", MIND),
                      (r"Elisabeth: \ `it would be easier for me to concede matter and extension to the soul'", BAD)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1643 the twenty-four-year-old Princess Elisabeth of Bohemia wrote to Descartes with the objection that "
            "has followed dualism ever since. <bookmark mark='a'/>How can the soul of a human being, being only a "
            "thinking substance, determine the bodily spirits to perform voluntary actions? "
            "<bookmark mark='b'/>Every cause of motion she knew worked by contact, pushing, and so needed extension; "
            "the soul has none. <bookmark mark='c'/>Descartes answered that the union of mind and body is a primitive "
            "notion, known not by thinking about it but by living it. <bookmark mark='d'/>Elisabeth was not "
            "satisfied. It would be easier for me, she wrote, to concede matter and extension to the soul than the "
            "capacity of an immaterial being to move a body. The question of how mind and matter could interact is "
            "still the chief obstacle to dualism, and it returns, in a new form, in chapter eight."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
