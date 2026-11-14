from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403


class Forms(SoundScene):
    def construct(self):
        chapter(self, 2, r"Binary and ternary", r"What are the two oldest plans for a whole piece?")
        self.binary()
        self.ternary()

    # ------------------------------------------------------------------
    def binary(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"binary: \ two halves, \ each repeated: \ $\|$: A :$\|$: B :$\|$", WHITE),
            (r"A goes from home to the dominant; \ B comes back", WHITE),
            (r"the dance movements of the Baroque suite: \ allemande, \ courante, \ sarabande, \ gigue", WHITE),
            (r"rounded binary: \ the end of B brings back the start of A", TUNE),
            (r"the seed of sonata form \ (chapter 6)", GREY_A))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 7.2))
        rows_.move_to(RIGHT * 2.8 + DOWN * 0.1)
        d = load("forms")["binary"]
        img = ssm_image(d["ssm"], size=4.2).move_to(LEFT * 4.2 + DOWN * 0.2)
        cap = label(r"A A B B: \ the notes, \ beat by beat, \ compared with every other beat", font_size=18, color=GREY_B).next_to(img, DOWN, buff=0.25)
        with self.voiceover(
            "The oldest plan for a whole piece has two halves, each played twice. <bookmark mark='a'/> Binary form: "
            "repeat the first half, repeat the second. <bookmark mark='b'/> Typically the first half travels from the "
            "home key to the dominant, and the second half finds its way back. <bookmark mark='c'/> Nearly every dance "
            "in a Baroque suite is built this way. <bookmark mark='d'/> When the second half ends by bringing back the "
            "opening, the form is called rounded binary, <bookmark mark='e'/> and it is the seed from which sonata form "
            "grew. On the left, a picture of a binary piece on the Tune, which the next chapters will explain: for now, "
            "notice the four squares, and how the first two match."
        ) as vo:
            self.play(FadeIn(rows_[0]), FadeIn(img), FadeIn(cap))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        c = clip("forms.binary")
        with self.listen(c) as snd:
            window(snd, r"a binary piece on the Tune: \ A A B B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            self.add(diag_cursor(snd, img, d["beats"], d["beat"]))
            pulse(snd, cap, 0.0, c.duration, buff=0.08)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ternary(self):
        d = load("forms")["ternary"]
        img = ssm_image(d["ssm"], size=4.2).move_to(LEFT * 4.2 + DOWN * 0.2)
        cap = label(r"A B A", font_size=20, color=GREY_B).next_to(img, DOWN, buff=0.25)
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"ternary: \ A B A, \ statement, \ contrast, \ return", WHITE),
            (r"the B section in another key, \ often with another character", WHITE),
            (r"the da capo aria: \ the singer ornaments the returning A", WHITE),
            (r"the minuet and trio: \ minuet, \ trio, \ minuet again", WHITE),
            (r"the return is the point: \ A after B is not A before it", TUNE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 7.2))
        rows_.move_to(RIGHT * 2.8 + DOWN * 0.1)
        with self.voiceover(
            "The second plan has three parts. <bookmark mark='a'/> Ternary form: a statement, a contrast, a return. "
            "<bookmark mark='b'/> The middle section is usually in another key, often with another character, faster or "
            "slower, louder or softer. <bookmark mark='c'/> The da capo aria of Baroque opera is ternary: the singer "
            "returns to the first section and ornaments it, to show that it is not the same as before. "
            "<bookmark mark='d'/> So is the minuet and trio of the classical symphony. <bookmark mark='e'/> The return is "
            "the point. Heard after the contrast, the opening means something it could not mean the first time: it is "
            "now a homecoming."
        ) as vo:
            self.play(FadeIn(rows_[0]), FadeIn(img), FadeIn(cap))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        c = clip("forms.ternary")
        with self.listen(c) as snd:
            window(snd, r"a ternary piece on the Tune: \ A B A", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            self.add(diag_cursor(snd, img, d["beats"], d["beat"]))
            pulse(snd, cap, 0.0, c.duration, buff=0.08)
        self.wait(0.4)
        self.clear_scene()
