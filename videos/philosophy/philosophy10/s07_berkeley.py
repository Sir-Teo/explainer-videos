from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Berkeley(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"To be is to be perceived", r"Is there anything beyond our ideas?", lit=(1710,),
                            part=PART)
        with self.voiceover("Chapter six. To be is to be perceived."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.esse()
        self.master()
        self.abstract()
        self.analyst()
        self.stone()

    def esse(self):
        hc = history_card(1710, r"George Berkeley", r"\textit{A Treatise Concerning the Principles of Human "
                          r"Knowledge}", width=6.0, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"Locke's argument against colour \ (it varies with the observer) \ works just as well for shape and "
                  r"size", font_size=24),
            label(r"a tower is round from afar and square up close; \ a mite sees a foot as huge", font_size=22,
                  color=GREY_A),
            label(r"so primary qualities are ideas too: \ there is no matter behind them", font_size=24, color=GOAL),
            label(r"\textit{esse est percipi}: \ for unthinking things, \ to be is to be perceived", font_size=28,
                  color=SENSE),
            label(r"what keeps the tree in being when no one is looking? \ God, \ who perceives everything",
                  font_size=22, color=REASON)).arrange(DOWN, buff=0.35).move_to([0, -0.5, 0])
        with self.voiceover(
            "George Berkeley, an Irish bishop, took empiricism one step further than Locke. <bookmark mark='a'/>"
            "Locke had argued that colour is not in things, because it varies with the observer. But shape and size "
            "vary too. <bookmark mark='b'/>A tower looks round from afar and square up close; to a mite, a human foot "
            "is enormous. <bookmark mark='c'/>So primary qualities are ideas as well, and there is no matter behind "
            "the ideas, holding them up. <bookmark mark='d'/>For unthinking things, Berkeley wrote in 1710, to be is "
            "to be perceived: esse est percipi. <bookmark mark='e'/>What, then, keeps a tree in being when no one is "
            "looking at it? God, who perceives everything."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def master(self):
        head = label(r"The master argument", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        steps = VGroup(
            label(r"1. \ try to conceive a tree \ that no one perceives or conceives", font_size=26),
            label(r"2. \ in doing so, \ you are conceiving it", font_size=26, color=GOAL),
            label(r"3. \ so you have not conceived an unconceived tree", font_size=26, color=BAD),
            label(r"4. \ so nothing can exist unconceived", font_size=26)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.4).move_to([0, 0.6, 0])
        reply = VGroup(label(r"the slip: \ conceiving \textit{of} a tree unconceived \ is not conceiving \textit{it} "
                             r"as conceived", font_size=23, color=OK),
                       label(r"I can think of a book no one will ever read, \ without that thought being a reading",
                             font_size=21, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Berkeley rested a great deal on one short argument, now called the master argument. "
            "<bookmark mark='a'/>Try to conceive of a tree that exists without anyone perceiving or conceiving it. "
            "<bookmark mark='b'/>But in trying, you are conceiving it. <bookmark mark='c'/>So you have not conceived "
            "an unconceived tree. <bookmark mark='d'/>So nothing can exist unconceived. <bookmark mark='e'/>Most "
            "readers find a slip here. To conceive of a tree that is unconceived is not to conceive of it as being "
            "conceived. I can think about a book that no one will ever read, without my thought being a reading of "
            "it. The content of a thought and the act of thinking it come apart."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s_ in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(reply))
        self.clear_scene()

    def abstract(self):
        q = quote_card(r"It must be neither oblique, nor rectangle, neither equilateral, equicrural, nor scalenon; but all "
                       r"and none of these at once.", r"John Locke, \ on the general idea of a triangle",
                       r"\textit{Essay} IV.vii.9", width=9.6, font_size=26).move_to([0, 1.6, 0])
        tris = VGroup(Polygon([0, 0, 0], [1.4, 0, 0], [0.7, 1.2, 0], color=SENSE),
                      Polygon([0, 0, 0], [1.4, 0, 0], [0, 1.1, 0], color=SENSE),
                      Polygon([0, 0, 0], [1.8, 0, 0], [1.3, 0.8, 0], color=SENSE)).arrange(RIGHT, buff=0.8).move_to(
            [0, -0.4, 0])
        rows = VGroup(label(r"Berkeley: \ no one can frame such an idea; \ every triangle I picture has some shape",
                            font_size=23, color=GOAL),
                      label(r"a general word works by standing for any particular, \ indifferently", font_size=23,
                            color=OK)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Berkeley's empiricism also attacked abstraction. <bookmark mark='a'/>Locke had described the general "
            "idea of a triangle: it must be neither oblique nor rectangle, neither equilateral, equicrural nor "
            "scalenon, but all and none of these at once. <bookmark mark='b'/>Berkeley replied that no one can frame "
            "such an idea. Every triangle you picture has some particular shape. <bookmark mark='c'/>A general word, "
            "he proposed, works by standing for any particular of its kind, indifferently. A geometer proves a theorem "
            "about one triangle, using nothing special to it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(t) for t in tris], lag_ratio=0.4), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def analyst(self):
        hc = history_card(1734, r"George Berkeley", r"\textit{The Analyst}: \ a discourse addressed to an infidel "
                          r"mathematician", width=5.8, color=HIST).to_corner(UL, buff=0.35)
        steps = VGroup(
            MathTex(r"\frac{(x + o)^2 - x^2}{o} = \frac{2xo + o^2}{o}", font_size=34),
            MathTex(r"= 2x + o \quad (\text{divide by } o:\ o \neq 0)", font_size=34, color=REASON),
            MathTex(r"\to 2x \quad (\text{now let } o = 0)", font_size=34, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.6, 0.4, 0])
        q = quote_card(r"And what are these fluxions? \dots May we not call them the ghosts of departed quantities?",
                       r"George Berkeley", r"\textit{The Analyst} \S 35", width=6.0, font_size=24).move_to(
            [3.6, 0.6, 0])
        nums = VGroup(*[MathTex(rf"o = 10^{{-{k}}}:\ \ {2 * 3 + 10 ** -k:.{k}f}", font_size=26,
                                color=GREY_A) for k in (1, 2, 3, 4)]).arrange(DOWN, aligned_edge=LEFT,
                                                                             buff=0.12).move_to([-2.6, -2.0, 0])
        lab = label(r"at $x = 3$: \ the quotient approaches 6", font_size=20, color=GREY_B).next_to(nums, UP, buff=0.15)
        fix = VGroup(label(r"the cure took over a century:", font_size=22, color=OK),
                     label(r"Cauchy (1821) and Weierstrass:", font_size=22, color=OK),
                     label(r"limits with $\varepsilon$ and $\delta$, \ no `$o = 0$' at all", font_size=22,
                           color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.6, -1.9, 0])
        with self.voiceover(
            "Berkeley's sharpest argument was about mathematics. <bookmark mark='a'/>In The Analyst of 1734 he "
            "examined Newton's method of fluxions, the calculus. To find how fast x squared grows, increase x by a "
            "small quantity o, subtract, and divide by o: two x plus o. <bookmark mark='b'/>Dividing by o requires "
            "that o is not zero. Then Newton lets o vanish, leaving two x. <bookmark mark='c'/>So o is assumed to be "
            "something, and then nothing. And what are these fluxions? Berkeley asked. May we not call them the "
            "ghosts of departed quantities? <bookmark mark='d'/>The Reasoner computes the quotient for smaller and "
            "smaller o at x equals three: six point one, six point zero one, and so on, approaching six and never "
            "needing o to be zero. <bookmark mark='e'/>The cure took more than a century. Cauchy and Weierstrass "
            "defined the limit with epsilon and delta, so that o never has to vanish. Berkeley's objection was "
            "right, and it improved mathematics."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            self.play(FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(lab), LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(FadeIn(fix))
        self.clear_scene()

    def stone(self):
        hc = history_card(1763, r"Samuel Johnson, \ in Boswell's \textit{Life}", r"`I refute it \textit{thus}'",
                          width=5.4, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"Johnson kicked a large stone, \ and felt it push back", font_size=24),
            label(r"but Berkeley never denied the stone: \ only that it is more than ideas, \ hardness included",
                  font_size=24, color=GOAL),
            label(r"the kick is one more idea, \ arriving in the right order", font_size=24, color=SENSE),
            label(r"what Berkeley leaves open, \ Hume will press: \ why expect the ideas to keep their order?",
                  font_size=24, color=REASON)).arrange(DOWN, buff=0.4).move_to([0, -0.5, 0])
        with self.voiceover(
            "Berkeley's view invites a famous reply. <bookmark mark='a'/>In 1763, according to James Boswell, Samuel "
            "Johnson kicked a large stone so hard that he rebounded from it, and said: I refute it thus. "
            "<bookmark mark='b'/>But Berkeley never denied that the stone exists, or that it is hard. He denied only "
            "that it is anything more than ideas. <bookmark mark='c'/>The kick and the pain in Johnson's foot are "
            "more ideas, arriving in the regular order God gives them. <bookmark mark='d'/>The deeper question is why "
            "we expect that order to continue. That question belongs to David Hume."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
