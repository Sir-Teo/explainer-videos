from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


def eye(color=WHITE):
    white = Ellipse(width=0.62, height=0.3, color=color, stroke_width=3)
    pupil = Dot(radius=0.08, color=color).shift(DOWN * 0.03)
    brow = Arc(radius=0.4, start_angle=PI / 4, angle=PI / 2, color=color, stroke_width=4).move_to(UP * 0.32)
    return VGroup(white, pupil, brow)


def mouth(color=WHITE):
    lip = Arc(radius=0.55, start_angle=-PI / 2 - 0.75, angle=1.5, color=color, stroke_width=5)
    return VGroup(lip).move_to(ORIGIN)


def face(thatcher=False, color=WHITE):
    head = Ellipse(width=2.2, height=2.9, color=GREY_B, stroke_width=3)
    le, re_ = eye(color).move_to([-0.48, 0.38, 0]), eye(color).move_to([0.48, 0.38, 0])
    nose = VMobject(color=color, stroke_width=3).set_points_as_corners([[0, 0.25, 0], [-0.14, -0.3, 0], [0.08, -0.32, 0]])
    m = mouth(color).move_to([0, -0.78, 0])
    if thatcher:
        for part in (le, re_, m):
            part.rotate(PI)
    return VGroup(head, le, re_, nose, m)


class Faces(VoiceoverScene):
    def construct(self):
        self.card()
        self.inversion()
        self.thatcher()
        self.brain()
        self.expertise()

    def card(self):
        card = chapter_card(10, r"Faces", r"Is there a special system for faces?",
                            lit={1969: r"Yin", 1980: r"Thompson", 1997: r"Kanwisher"}, part=PART, scale=("mind", "circuit"),
                            marr=("what", "hardware"))
        with self.voiceover("Chapter ten. Faces."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def inversion(self):
        head = heading(r"Upside down, \ faces suffer most")
        rows = rows_of([
            (r"1969: \ Yin: \ remember pictures of faces, \ houses, \ aeroplanes and other things", WHITE),
            (r"turned upside down, \ all got harder to remember; \ faces much the hardest", LIKE),
            (r"the composite face: \ the top of one face on the bottom of another makes a new face", PRIOR),
            (r"faces seem to be seen as wholes, \ the spacing of eyes, \ nose and mouth together; \ inversion breaks that", POST),
        ], 12.6, 28, 0.38).move_to([0, -0.1, 0])
        tag = published_tag(archive.YIN_1969.cite)
        with self.voiceover(
            "Faces are the objects people are most expert at. Two findings suggest they're also processed "
            "differently. <bookmark mark='a'/> In 1969, Robert Yin asked people to remember photographs of faces, "
            "houses, aeroplanes and other things, upright or upside down. <bookmark mark='b'/> Turning them upside "
            "down made every kind of picture harder to remember. But it hurt faces far more than anything else. "
            "<bookmark mark='c'/> In 1987, Andrew Young and colleagues joined the top half of one famous face to the "
            "bottom half of another. The halves fused into a new face, and naming the person in the top half became "
            "hard; slide the halves apart sideways, and it became easy again. <bookmark mark='d'/> Both findings "
            "suggest faces are seen as wholes: the arrangement and spacing of the eyes, nose and mouth together, "
            "rather than each feature on its own. And turning a face upside down seems to break that whole."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def thatcher(self):
        head = heading(r"On you: \ the Thatcher illusion")
        f1 = face(False).rotate(PI).move_to([-4.6, 0.3, 0])
        f2 = face(True).rotate(PI).move_to([-1.6, 0.3, 0])
        cap = label(r"two faces, \ upside down", font_size=24, color=GREY_B).next_to(VGroup(f1, f2), DOWN, buff=0.3)
        rows = rows_of([
            (r"upside down: \ much the same face, \ one with an odd expression", WHITE),
            (r"turned upright: \ one is grotesque; \ its eyes and mouth were flipped", BAD),
            (r"inverted, \ the features are checked one by one, \ each looks fine; \ upright, \ the whole is wrong", POST),
            (r"Thompson, \ 1980, \ with a photograph of Margaret Thatcher; \ drawn here with a schematic face", GREY_A),
        ], 5.6, 26, 0.34).move_to([3.8, 0.0, 0])
        keep_in_frame(rows)
        tag = note(r"drawn after Thompson (1980)").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here's a demonstration you can try on yourself. <bookmark mark='a'/> Two faces, upside down. They look "
            "much the same. Perhaps one has a slightly odd expression. <bookmark mark='b'/> Now turn them upright. "
            "One of them is grotesque. Its eyes and mouth had been turned upside down within the face, and upside "
            "down you barely noticed. With a real photograph the effect is far stronger than with this drawing. "
            "<bookmark mark='c'/> The usual explanation follows from the last slide: upside down, the face isn't "
            "seen as a whole, so each feature is checked on its own, and each feature, a pair of eyes, a mouth, is "
            "fine. Upright, the whole is seen, and the whole is wrong. <bookmark mark='d'/> Peter Thompson, the same "
            "Thompson as the slow gratings, published it in 1980, with a photograph of the British prime minister, "
            "and it's been called the Thatcher illusion ever since."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f1), FadeIn(f2), FadeIn(cap), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Rotate(f1, PI), Rotate(f2, PI), run_time=2.0)
            self.play(FadeIn(rows[1]), FadeOut(cap))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def brain(self):
        head = heading(r"Face-selective cortex")
        brain = VGroup(Ellipse(width=4.8, height=2.4, color=GREY_B, stroke_width=3),
                       Line([-2.0, -0.2, 0], [2.0, -0.2, 0], color=GREY_D, stroke_width=2))
        ffa = Ellipse(width=0.9, height=0.45, color=POST, fill_color=POST, fill_opacity=0.5).move_to([0.6, -0.65, 0])
        fl = label(r"fusiform face area", font_size=22, color=POST).next_to(brain, DOWN, buff=0.15)
        bl = label(r"the brain from below", font_size=20, color=GREY_B).next_to(brain, UP, buff=0.15)
        fig = VGroup(brain, ffa, fl, bl).move_to([-3.8, 0.4, 0])
        rows = rows_of([
            (r"1997: \ Kanwisher, \ McDermott and Chun: \ a fusiform region more active to faces than objects, \ in 12 of 15 people", WHITE),
            (r"2006: \ Tsao and colleagues: \ in monkeys' face patches, \ 97\% of the visually responsive cells prefer faces", LIKE),
            (r"prosopagnosia: \ faces not recognized, \ after damage or from birth, \ about 2 in 100 by one estimate", BAD),
            (r"super-recognizers, \ at the other end, \ remember faces seen once, \ years before", WORLD),
        ], 6.2, 25, 0.34).move_to([3.3, 0.0, 0])
        keep_in_frame(rows)
        tag = published_tag(archive.KANWISHER_1997.cite)
        with self.voiceover(
            "If faces are special, is there special hardware? <bookmark mark='a'/> In 1997, Nancy Kanwisher, Josh "
            "McDermott and Marvin Chun found a region on the underside of the brain, in the fusiform gyrus, that "
            "responded much more to faces than to other objects, in twelve of the fifteen people they scanned. They "
            "called it the fusiform face area, and Part 8 used it as an example of a brain map. "
            "<bookmark mark='b'/> In 2006, Doris Tsao and colleagues used scans to find similar face patches in "
            "monkeys, then recorded from single cells inside one: ninety-seven percent of its visually responsive "
            "cells preferred faces. <bookmark mark='c'/> And there are people who can't recognize faces, a condition "
            "called prosopagnosia. It can follow damage to this part of the brain, or be present from birth, with no "
            "damage at all: by one estimate in about two people in a hundred. <bookmark mark='d'/> At the other end "
            "are super-recognizers, who can pick out a face seen once, years before. Some police forces now employ "
            "them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(brain), FadeIn(bl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ffa), FadeIn(fl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def expertise(self):
        head = heading(r"Faces, \ or expertise?")
        rows = rows_of([
            (r"1999: \ Gauthier and colleagues: \ train people for hours on invented creatures, \ greebles", WHITE),
            (r"as they became experts, \ the face area responded more to greebles", PRIOR),
            (r"bird and car experts show some of the same, \ for birds and cars", PRIOR),
            (r"the reply: \ the effects for experts are smaller, \ and patients can lose faces alone", LIKE),
            (r"selectivity is settled; \ what it is selective for is argued: \ the Ledger's row", POST),
        ], 12.6, 28, 0.38).move_to([0, -0.1, 0])
        tag = published_tag(archive.GAUTHIER_1999.cite)
        with self.voiceover(
            "Is the region for faces as such, or for whatever a person is expert at? <bookmark mark='a'/> In 1999, "
            "Isabel Gauthier and colleagues trained people for many hours to tell apart invented creatures they "
            "called greebles, which share a structure the way faces do. <bookmark mark='b'/> As the observers became "
            "experts, the face area's response to greebles rose. <bookmark mark='c'/> Bird watchers and car "
            "enthusiasts show some of the same for birds and cars. <bookmark mark='d'/> Kanwisher and others reply "
            "that the effects of expertise are much smaller than the response to faces, and that some patients lose "
            "the ability to recognize faces while keeping their expertise with other things. "
            "<bookmark mark='e'/> That the region is selective for faces has been found in study after study. What "
            "it's selective for is still argued, and the Ledger's row will say so."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
