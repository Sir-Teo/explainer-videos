from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403


def clock(center, radius=1.0, neglect=True):
    """A clock face as a patient with neglect draws it: every number crowded onto the right half."""
    c = np.asarray(center, float)
    g = VGroup(Circle(radius=radius, color=VOLT, stroke_width=3).move_to(c))
    for i in range(1, 13):
        a = PI / 2 - (PI * (i - 0.5) / 12 if neglect else TAU * i / 12)
        g.add(label(rf"{i}", font_size=19, color=VOLT).move_to(c + 0.78 * radius * np.array([np.cos(a), np.sin(a), 0])))
    return g


def face(center, r=0.55, color=VOLT):
    c = np.asarray(center, float)
    return VGroup(Circle(radius=r, color=color, stroke_width=3).move_to(c),
                  Dot(c + np.array([-0.2 * r / 0.55, 0.15, 0]), radius=0.05, color=color),
                  Dot(c + np.array([0.2 * r / 0.55, 0.15, 0]), radius=0.05, color=color),
                  Arc(radius=0.25, start_angle=PI * 1.2, angle=PI * 0.6, color=color, stroke_width=3).move_arc_center_to(
                      c + UP * 0.02))


class Catalogue(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.reading()

    def card(self):
        card = chapter_card(9, r"Things that break alone", r"What else can be lost by itself?", lit=(), part=PART,
                            scale=("brain", "mind"), marr=("what", "tissue"))
        with self.voiceover(
            "Chapter nine. Things that break alone."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def four(self):
        head = heading(r"Four losses, \ each of something nobody knew was separate")
        cells = [(-3.5, 1.15), (3.5, 1.15), (-3.5, -1.95), (3.5, -1.95)]
        frames = VGroup(*[RoundedRectangle(width=6.7, height=2.85, corner_radius=0.15, color=GREY_D, stroke_width=2,
                                           fill_color="#0E131C", fill_opacity=1).move_to([x, y, 0]) for x, y in cells])

        def text(name, col, lost, kept):
            return VGroup(label(name, font_size=34, color=col), wrapped_label(lost, 4.0, 26, WHITE),
                          wrapped_label(kept, 4.0, 26, SPARED)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        pics = VGroup(
            clock([cells[0][0] - 2.2, cells[0][1], 0]),
            VGroup(Rectangle(width=1.1, height=0.55, color=VOLT, stroke_width=3).move_to([cells[1][0] - 2.4, cells[1][1] + 0.15, 0]),
                   Circle(radius=0.3, color=VOLT, stroke_width=3).move_to([cells[1][0] - 1.75, cells[1][1] + 0.15, 0]),
                   label(r"?", font_size=44, color=LESION).move_to([cells[1][0] - 2.3, cells[1][1] - 0.7, 0])),
            VGroup(face([cells[2][0] - 2.3, cells[2][1] + 0.1, 0]),
                   label(r"?", font_size=44, color=LESION).move_to([cells[2][0] - 2.3, cells[2][1] - 0.95, 0])),
            VGroup(Rectangle(width=1.9, height=1.5, color=VOLT, stroke_width=3).move_to([cells[3][0] - 2.3, cells[3][1], 0]),
                   Rectangle(width=0.95, height=1.5, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9).move_to(
                       [cells[3][0] - 2.775, cells[3][1], 0]),
                   Dot([cells[3][0] - 2.8, cells[3][1] + 0.2, 0], radius=0.09, color=THRESH)),
        )
        texts = VGroup(
            text(r"neglect", PARIETAL, r"the left half of the world is ignored: \ a clock drawn like this",
                 r"not blind: \ pointed out, the left can be seen"),
            text(r"visual agnosia", TEMPORAL, r"sees edges, colours, shapes, \ and cannot say what the thing is",
                 r"names it at once by touch"),
            text(r"prosopagnosia", OCCIPITAL, r"cannot recognize a face, \ a friend's or their own",
                 r"knows the same people by voice"),
            text(r"blindsight", LESION, r"``I see nothing there''",
                 r"asked to guess, \ points to it far better than chance"),
        )
        for t, (x, y) in zip(texts, cells):
            t.move_to([x + 1.15, y, 0])
            if t.height > 2.6:
                t.scale_to_fit_height(2.6)
        met = VGroup(*[label(t_, font_size=34, color=c_) for t_, c_ in (
            (r"speech \ (chapter 3)", FRONTAL), (r"new memories \ (chapter 7)", TEMPORAL),
            (r"a hemisphere's voice \ (chapter 8)", PARIETAL))]).arrange(DOWN, buff=0.45).move_to([0, 0.1, 0])
        met_l = label(r"lost by themselves, so far", font_size=28, color=GREY_A).next_to(met, UP, buff=0.5)
        src = historical_tag(archive.WEISKRANTZ_1974.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Speech, new memories, a hemisphere's voice. Neurologists have a long catalogue of things that "
            "can be lost by themselves, and each one was a surprise. Four of them, quickly. They all come "
            "back later in the series. <bookmark mark='a'/> Neglect. After damage to the right side of the "
            "brain, usually the parietal lobe, a patient may ignore the left half of the world. They eat "
            "the food on the right half of the plate. Asked to draw a clock, they crowd all twelve numbers "
            "into the right half. They aren't blind on the left. Point to something there, and they can "
            "see it. It just doesn't occur to them that the left exists. <bookmark mark='b'/> Visual "
            "agnosia. The patient sees edges and colours and shapes, can even copy a drawing, and can't say "
            "what the object is. Put it in their hand, and they name it at once. <bookmark mark='c'/> "
            "Prosopagnosia. The patient can't recognize faces. Not a friend's, not their own in a mirror. "
            "They know the same people immediately by voice, and they recognize objects. "
            "<bookmark mark='d'/> And blindsight. After damage to the visual cortex, a patient says of "
            "part of their field of view: I see nothing there. Ask them to guess where a light was, and "
            "they point to it, far more accurately than chance. They are responding to something they deny "
            "seeing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(met_l))
            self.play(LaggedStart(*[FadeIn(m_, shift=UP * 0.1) for m_ in met], lag_ratio=0.6), run_time=3.0)
            for k, mark_ in enumerate("abcd"):
                vo.wait_until(mark_)
                if k == 0:
                    self.play(FadeOut(met), FadeOut(met_l), run_time=0.4)
                self.play(FadeIn(frames[k]), FadeIn(pics[k]), FadeIn(texts[k], shift=RIGHT * 0.1))
        self.clear_scene()

    def reading(self):
        head = heading(r"Reading the catalogue with chapter four's rules")
        rows = VGroup(
            VGroup(label(r"what each case offers", font_size=36, color=SPARED),
                   wrapped_label(r"a candidate for a separate part: \ attending to a side, \ recognizing things, "
                                 r"\ recognizing faces, \ knowing that you see", 12.4, 31, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"what each one needs before you believe it", font_size=36, color=THRESH),
                   wrapped_label(r"the reverse patient: \ objects lost and faces spared; \ and tests of equal "
                                 r"difficulty on both sides", 12.4, 31, WHITE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.08),
            VGroup(label(r"what the blind spot already taught", font_size=36, color=P.ACCENT),
                   wrapped_label(r"a missing part of experience does not announce itself. \ Patients with neglect "
                                 r"do not feel that half the world is gone.", 12.4, 31, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.3, 0])
        with self.voiceover(
            "Read that catalogue with the rules from chapter four. <bookmark mark='a'/> Each case offers a "
            "candidate for a separate part of the mind. Attending to one side of space. Recognizing what a "
            "thing is. Recognizing faces in particular. And, strangest, knowing that you see, as distinct "
            "from seeing. <bookmark mark='b'/> And each needs the same things before you believe it. The "
            "reverse patient: someone who loses objects and keeps faces. Such patients have been described. "
            "And tests of equal difficulty, because faces may just be the hardest things we ever have to "
            "tell apart. That argument is still running, and Part 14 picks it up. <bookmark mark='c'/> One "
            "more thing, which your blind spot has already taught you. A missing piece of experience "
            "doesn't announce itself. The patient with neglect doesn't feel that half the world has gone "
            "dark. Nothing is where it was, and nothing marks the place."
        ) as vo:
            self.play(FadeIn(head))
            for k, mark_ in enumerate("abc"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()
