from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


class Touch(VoiceoverScene):
    def construct(self):
        self.card()
        self.receptors()
        self.twopoint()
        self.position()
        self.rubber()

    def card(self):
        card = chapter_card(9, r"Touch and the body", r"How does the skin know what it touches, \ and where the hand is?",
                            lit={1972: r"Goodwin", 1998: r"Botvinick \& Cohen"}, part=PART, scale=("circuit", "mind"),
                            marr=("what", "how"))
        with self.voiceover("Chapter nine. Touch, and the body."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def receptors(self):
        head = heading(r"Four kinds of touch fibre")
        cells = [
            (r"Meissner", r"small fields, \ fast: \ flutter, \ slip", TOUCH),
            (r"Merkel", r"small fields, \ slow: \ pressure, \ edges, \ Braille", PLACE),
            (r"Pacinian", r"large fields, \ fast: \ vibration near 250 Hz", SOUND),
            (r"Ruffini", r"large fields, \ slow: \ stretch of the skin", TIMING),
        ]
        cards = VGroup()
        for name, what, col in cells:
            b = RoundedRectangle(width=2.9, height=1.9, corner_radius=0.15, stroke_color=col, stroke_width=3)
            t = label(name, font_size=28, color=col)
            w_ = wrapped_label(what, 2.6, 21, GREY_A)
            VGroup(t, w_).arrange(DOWN, buff=0.2).move_to(b)
            cards.add(VGroup(b, t, w_))
        cards.arrange(RIGHT, buff=0.3).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"two sizes of receptive field, \ times two speeds of adaptation: \ four channels", WHITE),
            (r"about 17{,}000 touch fibres from each hand \ (Johansson and Vallbo, \ 1979)", GREY_A),
            (r"like the eye's channels in Part 13, \ each fibre answers a different question about the surface", PRIOR),
        ], 12.4, 27, 0.28).to_edge(DOWN, buff=0.75)
        tag = note(r"drawn; \ the glabrous skin of the hand").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Touch starts with four kinds of nerve ending in the skin of the hand, each with its own fibre. "
            "<bookmark mark='a'/> Meissner endings have small receptive fields and adapt fast: they signal flutter, "
            "and an object starting to slip from your grip. Merkel endings have small fields and adapt slowly: "
            "sustained pressure, edges, the dots of Braille. Pacinian endings, deep in the skin, have large fields "
            "and are exquisitely sensitive to vibration, best at around two hundred and fifty hertz. Ruffini endings "
            "signal the skin stretching as the fingers move. <bookmark mark='b'/> Roland Johansson and Åke Vallbo "
            "estimated in 1979 that about seventeen thousand such fibres leave each hand. <bookmark mark='c'/> As with "
            "the eye's channels in Part 13, each kind answers a different question about the surface, and perception "
            "combines them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def twopoint(self):
        head = heading(r"On you: \ one point, \ or two?")
        sites = [(r"fingertip", 2.5, TOUCH), (r"back", 39.0, PLACE), (r"calf", 45.0, SOUND)]
        A = axes([0, 3.6], [0, 50], x_length=5.0, y_length=4.2, xticks=[], yticks=[0, 10, 20, 30, 40, 50],
                 ylabel=r"two-point threshold (mm)", center=[-3.2, -0.3, 0])
        ax = A.ax
        bars = VGroup()
        for k, (n, v, col) in enumerate(sites):
            x = 0.7 + 1.1 * k
            bars.add(VGroup(Rectangle(width=0.7, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                      fill_color=col, fill_opacity=0.85).move_to(ax.c2p(x, v / 2)),
                            label(n, font_size=22, color=col).next_to(ax.c2p(x, 0), DOWN, buff=0.15)))
        rows = rows_of([
            (r"touch two points at once: \ how far apart before they feel like two?", WHITE),
            (r"on a fingertip, \ 2 to 3 mm; \ on the back, \ around 40 mm", TOUCH),
            (r"try it with two pen tips on a friend's finger, \ then their back", YOU),
            (r"small fields packed densely, \ and a large patch of cortex: \ the homunculus of Part 7", PRIOR),
        ], 5.2, 26, 0.32).move_to([3.8, -0.2, 0])
        keep_in_frame(rows)
        tag = note(r"as usually tabulated from Weinstein (1968); \ approximate").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here's a test you can try with a friend and two pen tips. <bookmark mark='a'/> Touch two points on the "
            "skin at once, and ask: one point, or two? <bookmark mark='b'/> On a fingertip, two points about two or "
            "three millimetres apart already feel like two. On the back, they have to be about four centimetres apart. "
            "<bookmark mark='c'/> Try the fingertip and then the back; the difference is startling. "
            "<bookmark mark='d'/> The fingertip has small receptive fields packed densely, and a disproportionately "
            "large patch of cortex: the distorted little person, the homunculus, of Part 7. The resolution of touch, "
            "like that of the eye, is set by sampling."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.4),
                      FadeIn(VGroup(*[b[1] for b in bars])), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def position(self):
        head = heading(r"The sense you never notice")
        rows = rows_of([
            (r"proprioception: \ where your limbs are, \ from stretch receptors in the muscles and tendons", WHITE),
            (r"close your eyes and touch your nose: \ no other sense tells you where your hand is", YOU),
            (r"1972: \ vibrate the tendon of the biceps and the arm feels straighter than it is", SOUND),
            (r"vibration mimics stretch: \ the brain believes its receptors, \ as with any illusion", PRIOR),
            (r"lose it, \ as a few people have after nerve damage, \ and every movement must be watched", BAD),
        ], 12.6, 28, 0.4).move_to([0, -0.1, 0])
        with self.voiceover(
            "There's a sense most people have never heard of, and use every second. <bookmark mark='a'/> "
            "Proprioception: the sense of where your limbs are, from stretch receptors in the muscles, tendons and "
            "joints. <bookmark mark='b'/> Close your eyes and touch your nose. Nothing you see or feel on the skin "
            "tells you where your hand is; proprioception does. <bookmark mark='c'/> In 1972, Guy Goodwin, Ian "
            "McCloskey and Peter Matthews vibrated the tendon of a blindfolded person's biceps, and the arm felt "
            "straighter than it really was. <bookmark mark='d'/> The vibration mimics the stretch of a lengthening "
            "muscle, and the brain believes its receptors. <bookmark mark='e'/> A few people have lost this sense "
            "entirely, after damage to their large sensory nerves. They can still move, but only by watching every "
            "movement, and in the dark they can barely move at all."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def rubber(self):
        head = heading(r"A rubber hand that feels like yours")
        table = Rectangle(width=6.0, height=2.6, color=GREY_D, fill_color=GREY_E, fill_opacity=0.5).move_to([-3.2, 0.2, 0])
        screen = Line([-3.2, 1.5, 0], [-3.2, -1.1, 0], color=GREY_B, stroke_width=6)
        real = RoundedRectangle(width=1.0, height=1.6, corner_radius=0.3, color=TOUCH, fill_opacity=0.3).move_to([-5.0, 0.2, 0])
        fake = RoundedRectangle(width=1.0, height=1.6, corner_radius=0.3, color=PLACE, fill_opacity=0.3).move_to([-1.4, 0.2, 0])
        rl = label(r"your hand, \ hidden", font_size=20, color=TOUCH).next_to(real, DOWN, buff=0.7)
        fl = label(r"a rubber hand, \ in view", font_size=20, color=PLACE).next_to(fake, DOWN, buff=0.7)
        brush1 = Line(real.get_top() + DOWN * 0.3 + LEFT * 0.4, real.get_top() + DOWN * 0.3 + RIGHT * 0.4, color=WHITE, stroke_width=5)
        brush2 = Line(fake.get_top() + DOWN * 0.3 + LEFT * 0.4, fake.get_top() + DOWN * 0.3 + RIGHT * 0.4, color=WHITE, stroke_width=5)
        rows = rows_of([
            (r"1998: \ Botvinick and Cohen stroke both hands with brushes, \ in time", WHITE),
            (r"within minutes many people feel the touch on the rubber hand, \ and call it theirs", PLACE),
            (r"the felt position of the real hand drifts toward the rubber one", TOUCH),
            (r"cue combination again: \ vision says the touch is there, \ and vision usually knows best where", PRIOR),
            (r"2020: \ Lush and colleagues: \ the reports track suggestibility; \ how much is expectation?", BAD),
        ], 5.8, 25, 0.3).move_to([3.5, -0.1, 0])
        keep_in_frame(rows)
        tag = published_tag(rf"{archive.BOTVINICK_COHEN_1998.cite}; \ {archive.LUSH_2020.cite}", corner=DL)
        with self.voiceover(
            "The sense of what is your body can be moved. <bookmark mark='a'/> In 1998, Matthew Botvinick and "
            "Jonathan Cohen hid a person's hand behind a screen, put a rubber hand in view, and stroked both with "
            "brushes, in time. <bookmark mark='b'/> Within minutes, many people felt the strokes on the rubber hand, "
            "and said it felt like their own. <bookmark mark='c'/> Asked to point to their hidden hand, they pointed "
            "toward the rubber one. <bookmark mark='d'/> It's Part 14's rule again. Vision says the touch is happening "
            "over there, and vision is usually the more precise sense about where things are, so the felt location "
            "moves. <bookmark mark='e'/> But in 2020, Peter Lush and colleagues found, in three hundred and fifty-three "
            "people, that the strength of the illusion tracked how responsive each person was to hypnotic suggestion. "
            "How much of the illusion is a change in bodily experience, and how much is people experiencing what they "
            "expect the experiment to produce, is now argued, and the Ledger records it as contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(table), FadeIn(screen), FadeIn(real), FadeIn(fake), FadeIn(rl), FadeIn(fl),
                      FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(brush1), FadeIn(brush2))
            self.play(brush1.animate.shift(DOWN * 0.8), brush2.animate.shift(DOWN * 0.8), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), brush1.animate.shift(UP * 0.8), brush2.animate.shift(UP * 0.8), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
