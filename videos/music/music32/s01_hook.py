from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403


def glide_lines(width=4.2, height=2.0, cross=True):
    """Two pitch paths in a small frame: crossing (an X) or meeting and turning back (a pair of chevrons)."""
    fr = Rectangle(width=width, height=height, stroke_color=GREY_B, stroke_width=1.5)
    l, r, b, t = fr.get_left()[0], fr.get_right()[0], fr.get_bottom()[1], fr.get_top()[1]
    lo, hi, mid = b + 0.25 * height, t - 0.25 * height, (b + t) / 2
    if cross:
        p1 = Line([l + 0.2, lo, 0], [r - 0.2, hi, 0], color=TUNE, stroke_width=5)
        p2 = Line([l + 0.2, hi, 0], [r - 0.2, lo, 0], color=BLUE, stroke_width=5)
    else:
        cx = (l + r) / 2
        p1 = VMobject(color=TUNE, stroke_width=5).set_points_as_corners([[l + 0.2, lo, 0], [cx, mid - 0.04, 0], [r - 0.2, lo, 0]])
        p2 = VMobject(color=BLUE, stroke_width=5).set_points_as_corners([[l + 0.2, hi, 0], [cx, mid + 0.04, 0], [r - 0.2, hi, 0]])
    return VGroup(fr, p1, p2)


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.science()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.quiz")
        card = listen_card(r"Two voices start on C and E and glide. \ In one sound they cross over each other; \ "
                           r"in the other they meet in the middle and turn back. \ Which one crosses, \ A or B?", width=10.4)
        with self.voiceover(
            "Start with a puzzle for the ears. Two voices begin on C and E and glide smoothly. In one of the next two "
            "sounds they pass through each other and swap places, the lower ending on top. In the other they meet in the "
            "middle and turn back, each returning to where it began. Listen to both: in which do the voices cross, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ga = glide_lines(cross=True).move_to(LEFT * 3.2 + DOWN * 0.1)
        gb = glide_lines(cross=False).move_to(RIGHT * 3.2 + DOWN * 0.1)
        la = label(r"A", font_size=40, color=GREY_A).next_to(ga, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gb, UP, buff=0.3)
        hide = VGroup(*[Rectangle(width=4.25, height=2.05, stroke_width=0, fill_color=BLACK, fill_opacity=1).move_to(g) for g in (ga, gb)])
        qs = VGroup(label(r"?", font_size=60, color=GREY_A).move_to(ga), label(r"?", font_size=60, color=GREY_A).move_to(gb))
        self.play(FadeOut(card), FadeIn(ga), FadeIn(gb), FadeIn(hide), FadeIn(qs), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", kind="synthesized", detail=r"two gliding voices", corner=DL, tag_corner=DR)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.6, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        cap = label(r"at every instant both sounds hold the same two pitches: \ no one can tell", font_size=23, color=EAR).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "The honest answer is that no one can tell. In A the voices really do cross; in B they bounce. But at every "
            "instant both sounds contain exactly the same two pitches, and a chord does not remember which voice is which. "
            "That one fact, that a chord is an unordered set of notes, bends the space of all chords into a strange shape. "
            "This part draws that shape."
        ):
            self.play(FadeOut(hide), FadeOut(qs), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def science(self):
        items = [
            (r"\textit{Science}, \ 2006: \ Dmitri Tymoczko, \ `The geometry of musical chords'", WHITE),
            (r"every chord a point; \ every voice leading a path; \ its size a length", WHITE),
            (r"the space of two-note chords is a M\"obius strip", TUNE),
            (r"Callender, \ Quinn and Tymoczko \ (2008): \ five symmetries, \ one family of spaces", WHITE),
            (r"the claim: \ the chords of Western music sit where short paths join them to their own transpositions", GREY_A),
        ]
        rows_scene(self, r"music theory in a science journal", items,
                   "In 2006 the journal Science published a paper on music theory. <bookmark mark='b'/> Its author, the composer "
                   "Dmitri Tymoczko, treated every chord as a point in a space, every voice leading as a path, and the size of "
                   "a voice leading as a length. <bookmark mark='c'/> One of its pictures was startling: the space of all "
                   "two-note chords is a Möbius strip. <bookmark mark='d'/> Two years later, with Clifton Callender and Ian "
                   "Quinn, he described a whole family of such spaces, built from five symmetries. <bookmark mark='e'/> And "
                   "he made a claim this part will test: the familiar chords of Western music sit exactly where short paths "
                   "join them to their own transpositions, which is why harmony and smooth voice leading can work together.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"chords as points, \ and why the space folds",
            r"two notes: \ a M\"obius strip; \ three: \ a triangle in a twisted prism",
            r"the size of a voice leading, \ in three norms",
            r"nearly even chords, \ and scales as chords",
            r"OPTIC: \ five symmetries that name music theory's objects",
            r"Fourier magnitudes; \ and how close Bach comes to the shortest paths",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Chords as points, and why the space folds. <bookmark mark='b'/> Two-note chords on a Möbius "
            "strip, and three-note chords in a triangle inside a twisted prism. <bookmark mark='c'/> How to measure a voice "
            "leading. <bookmark mark='d'/> Why nearly even chords matter, and how a scale is a chord too. "
            "<bookmark mark='e'/> Five symmetries that name the objects of music theory. <bookmark mark='f'/> Fourier "
            "magnitudes, and a measurement: how close does Bach come to the shortest paths?"
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
