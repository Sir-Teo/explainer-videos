from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Locke(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"White paper", r"Is everything in the mind first in the senses?", lit=(1689, 1688),
                            part=PART)
        with self.voiceover("Chapter five. White paper."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.paper()
        self.qualities()
        self.degrees()
        self.molyneux()

    def paper(self):
        hc = history_card(1689, r"John Locke", r"\textit{An Essay Concerning Human Understanding}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        q = quote_card(r"Let us then suppose the mind to be, as we say, white paper, void of all characters, without any "
                       r"ideas: how comes it to be furnished?", r"John Locke", r"\textit{Essay} II.i.2", width=9.6,
                       font_size=28).move_to([0, 0.9, 0])
        rows = VGroup(label(r"answer: \ from experience: \ sensation, \ and reflection on the mind's own operations",
                            font_size=24, color=SENSE),
                      label(r"against innate ideas: \ children know nothing of `whatsoever is, is'", font_size=22,
                            color=GREY_A)).arrange(DOWN, buff=0.25).move_to([0, -1.7, 0])
        with self.voiceover(
            "John Locke's Essay Concerning Human Understanding, of 1689, is the founding text of the other side. "
            "<bookmark mark='a'/>Let us then suppose the mind to be, as we say, white paper, void of all characters, "
            "without any ideas: how comes it to be furnished? <bookmark mark='b'/>His answer is one word: experience. "
            "Either sensation of the world, or reflection on the mind's own operations. <bookmark mark='c'/>Against "
            "innate ideas he pointed out that children know nothing of principles like whatsoever is, is, which an "
            "innate idea should make obvious to everyone."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def qualities(self):
        head = label(r"Primary and secondary qualities", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        left = VGroup(label(r"primary", font_size=28, color=REASON),
                      label(r"solidity, \ extension, \ shape, \ motion, \ number", font_size=22),
                      label(r"in the things themselves; \ the ideas resemble them", font_size=20, color=GREY_A)).arrange(
            DOWN, buff=0.15)
        right = VGroup(label(r"secondary", font_size=28, color=SENSE),
                       label(r"colour, \ sound, \ taste, \ warmth", font_size=22),
                       label(r"powers in things to produce ideas in us; \ nothing like them out there", font_size=20,
                             color=GREY_A)).arrange(DOWN, buff=0.15)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.6).move_to([0, 1.2, 0])
        basins = VGroup()
        for i, (c, t) in enumerate(((BAD, r"hot"), ("#8899AA", r"lukewarm"), (REASON, r"cold"))):
            bowl = VGroup(Arc(radius=0.7, start_angle=PI, angle=PI, color=GREY_B, stroke_width=3),
                          Rectangle(width=1.3, height=0.35, stroke_width=0, fill_color=c, fill_opacity=0.6).shift(
                              DOWN * 0.25))
            basins.add(VGroup(bowl, label(t, font_size=20, color=c).next_to(bowl, DOWN, buff=0.15)))
        basins.arrange(RIGHT, buff=0.9).move_to([0, -1.3, 0])
        hands = VGroup(Arrow(basins[0].get_top() + UP * 0.6, basins[1].get_top() + UP * 0.1, color=BAD,
                             stroke_width=3, buff=0.1),
                       Arrow(basins[2].get_top() + UP * 0.6, basins[1].get_top() + UP * 0.1, color=REASON,
                             stroke_width=3, buff=0.1))
        tail = label(r"one hand from the hot, \ one from the cold: \ the same water feels cold and warm at once \ "
                     r"(\textit{Essay} II.viii.21)", font_size=22, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Locke drew a line through what the senses report. <bookmark mark='a'/>Primary qualities, solidity, "
            "extension, shape, motion and number, are in the things themselves, and our ideas of them resemble them. "
            "<bookmark mark='b'/>Secondary qualities, colour, sound, taste and warmth, are only powers in things to "
            "produce ideas in us. Nothing like redness is out there. <bookmark mark='c'/>His evidence is an "
            "experiment you can do in a kitchen. Put one hand in hot water and the other in cold, then both in the "
            "same lukewarm basin. <bookmark mark='d'/>The same water feels cold to one hand and warm to the other. "
            "Warmth cannot be in the water, which cannot be both; it is in us."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(basins))
            vo.wait_until("d")
            self.play(GrowArrow(hands[0]), GrowArrow(hands[1]), FadeIn(tail))
        self.clear_scene()

    def degrees(self):
        head = label(r"Three degrees of knowledge", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = VGroup(*[VGroup(label(a, font_size=26, color=c), label(b, font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.12) for a, b, c in (
            (r"intuitive", r"seeing at once that white is not black, \ or that I exist", OK),
            (r"demonstrative", r"a chain of intuitions: \ a proof in geometry, \ or that God exists", REASON),
            (r"sensitive", r"that this particular thing exists outside me, \ now: \ less certain, \ but enough",
             SENSE))]).arrange(DOWN, buff=0.45).move_to([0, 0.1, 0])
        foot = label(r"knowledge is the perception of agreement or disagreement among ideas \ (\textit{Essay} IV.i.2)",
                     font_size=22, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "For Locke, knowledge is the perception of the agreement or disagreement of our ideas, and it comes in "
            "three degrees. <bookmark mark='a'/>Intuitive knowledge sees a connection at once: that white is not "
            "black, or that I exist. <bookmark mark='b'/>Demonstrative knowledge links intuitions in a chain, as in a "
            "proof of geometry, or, Locke thought, of God's existence. <bookmark mark='c'/>And sensitive knowledge, "
            "the lowest degree, is knowledge that a particular thing exists outside me, now. It is less certain, "
            "Locke admitted, but certain enough for all our purposes. The gap between ideas and the things outside "
            "them is where Berkeley and Hume would press."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def molyneux(self):
        hcs = VGroup(history_card(1688, r"William Molyneux", r"a letter to Locke", width=4.0, color=HIST),
                     history_card(2011, r"Richard Held \& colleagues", r"`The newly sighted fail to match seen with "
                                  r"felt', \ \textit{Nature Neuroscience}", width=6.0, color=HIST)).arrange(
            RIGHT, buff=0.4).to_edge(UP, buff=0.35)
        cube = Square(side_length=1.2, color=SENSE, stroke_width=3, fill_color=SENSE, fill_opacity=0.15)
        sphere = Circle(radius=0.65, color=REASON, stroke_width=3, fill_color=REASON, fill_opacity=0.15)
        shapes = VGroup(cube, sphere).arrange(RIGHT, buff=1.2).move_to([-3.4, -0.5, 0])
        q = VGroup(label(r"a man born blind \ knows a cube and a sphere by touch", font_size=24),
                   label(r"made to see, \ can he tell which is which \ by sight alone, \ before touching?",
                         font_size=24, color=GOAL),
                   label(r"Molyneux and Locke: \ no; \ Leibniz: \ yes, \ by reasoning about the shapes", font_size=22,
                         color=GREY_A),
                   label(r"Project Prakash, 2011: \ five newly sighted patients \ could not, \ at first;", font_size=22,
                         color=OK),
                   label(r"within days, \ they could", font_size=22, color=OK)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.25).move_to([2.6, -0.6, 0])
        with self.voiceover(
            "In 1688 William Molyneux sent Locke a question that is still alive. <bookmark mark='a'/>Suppose a man "
            "born blind has learned to tell a cube from a sphere by touch. <bookmark mark='b'/>Now suppose he is made "
            "to see. Could he tell, by sight alone, before touching, which is the cube and which the sphere? "
            "<bookmark mark='c'/>Molyneux and Locke said no: the link between how things look and how they feel must "
            "be learned. Leibniz said yes: a rational being could work it out from the geometry. "
            "<bookmark mark='d'/>For three centuries it was a thought experiment. Then in 2011 Richard Held and "
            "colleagues, working with Project Prakash in India, tested five patients just after surgery gave them "
            "sight. At first they could not match what they saw with what they had felt. <bookmark mark='e'/>But "
            "within days they could. The answer was no, and then, quickly, yes."
        ) as vo:
            self.play(FadeIn(hcs[0]))
            vo.wait_until("a")
            self.play(FadeIn(shapes), FadeIn(q[0]))
            vo.wait_until("b")
            self.play(FadeIn(q[1]))
            vo.wait_until("c")
            self.play(FadeIn(q[2]))
            vo.wait_until("d")
            self.play(FadeIn(hcs[1]), FadeIn(q[3]))
            vo.wait_until("e")
            self.play(FadeIn(q[4]))
        self.clear_scene()
