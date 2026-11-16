from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403


class Ssm(SoundScene):
    def construct(self):
        chapter(self, 3, r"Seeing repetition", r"Can a picture show the form of a piece?", extra=((1999, r"Foote's self-similarity matrix"),))
        self.build()
        self.read()
        self.lag()
        self.from_sound()

    # ------------------------------------------------------------------
    def build(self):
        d = load("tune")
        S = np.array(d["ssm_melody"])
        n = S.shape[0]
        img = ssm_image(S, size=4.6).move_to(LEFT * 3.6 + DOWN * 0.3)
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"one column for each beat: \ how much of each of the twelve notes sounds", WHITE),
            (r"compare every beat with every other: \ 1 if alike, \ 0 if they share nothing", WHITE),
            (rf"{n} beats: \ a {n} by {n} picture, \ time running down and across", WHITE),
            (r"the bright diagonal: \ every beat is like itself", GREY_A))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.4))
        rows_.move_to(RIGHT * 3.3 + DOWN * 0.1)
        with self.voiceover(
            "In 1999 Jonathan Foote proposed a picture in which repetition can be seen. Start with the Tune's melody. "
            "<bookmark mark='a'/> For every beat, list how much of each of the twelve notes is sounding, a "
            "column of twelve numbers. <bookmark mark='b'/> Then compare every beat with every other beat: the two "
            "columns' cosine similarity, one if they contain the same notes in the same proportions, zero if they share "
            f"none. <bookmark mark='c'/> The Tune has {say(n)} beats, so the picture is {say(n)} by {say(n)}, with time "
            "running down and across from the top left. <bookmark mark='d'/> The bright diagonal is every beat compared "
            "with itself."
        ) as vo:
            self.play(FadeIn(img), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def read(self):
        d = load("tune")
        S = np.array(d["ssm_melody"])
        n = S.shape[0]
        size = 4.8
        img = ssm_image(S, size=size).move_to(LEFT * 3.4 + DOWN * 0.3)
        letters = d["labels"]
        st = [0] + d["truth"]
        lab_top = VGroup(*[label(l, font_size=20, color=SEC_C.get(l.rstrip("'"), GREY_B)).move_to([img.get_left()[0] + size * (st[k] + 4) / n, img.get_top()[1] + 0.22, 0]) for k, l in enumerate(letters)])
        # the off-diagonal stripes where A returns: phrase 1 against phrase 5
        a0, a1 = st[0], st[4]
        box = Rectangle(width=size * 16 / n, height=size * 16 / n, stroke_color=EAR, stroke_width=3).move_to(
            [img.get_left()[0] + size * (a1 + 8) / n, img.get_top()[1] - size * (a0 + 8) / n, 0])
        box2 = Rectangle(width=size * 8 / n, height=size * 8 / n, stroke_color=BLUE, stroke_width=3).move_to(
            [img.get_left()[0] + size * (st[3] + 4) / n, img.get_top()[1] - size * (st[2] + 4) / n, 0])
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"the Tune's phrases: \ A \ B \ C \ C \ A \ B", WHITE),
            (r"a stripe parallel to the diagonal: \ a passage that comes back", EAR),
            (r"the pink box: \ the opening A B, \ heard again at the end", WHITE),
            (r"the blue box: \ C followed straight away by C", BLUE),
            (r"a form is a pattern of stripes and blocks", TUNE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.0))
        rows_.move_to(RIGHT * 3.6 + DOWN * 0.1)
        with self.voiceover(
            "Now read it. <bookmark mark='a'/> The Tune has six phrases: A, B, C, C, A, B, with C the middle phrase G G F "
            "F E E D, sung twice. <bookmark mark='b'/> Wherever a passage comes back, there is a bright stripe parallel "
            "to the diagonal, offset by the time between the two appearances. <bookmark mark='c'/> The pink box is the "
            "opening sixteen beats compared with the closing sixteen: a clean stripe, because the end repeats the "
            "beginning exactly. <bookmark mark='d'/> The blue box is C against the C straight after it. "
            "<bookmark mark='e'/> Once you can read stripes and blocks, the form of a piece can be seen at a glance, "
            "and so can every one of the forms in this part."
        ) as vo:
            self.play(FadeIn(img), FadeIn(lab_top), FadeIn(rows_[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(Create(box), FadeIn(rows_[2]))
            vo.wait_until("d")
            self.play(Create(box2), FadeIn(rows_[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows_[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lag(self):
        d = load("tune")
        S = np.array(d["ssm_melody"])
        n = S.shape[0]
        Lg = np.zeros((n, n))
        for t in range(n):
            for l in range(n):
                if t - l >= 0:
                    Lg[l, t] = S[t, t - l]
        img = ssm_image(S, size=3.8).move_to(LEFT * 3.6 + DOWN * 0.2)
        lag = ssm_image(Lg, size=3.8).move_to(RIGHT * 2.2 + DOWN * 0.2)
        t1 = label(r"time against time", font_size=22, color=GREY_A).next_to(img, UP, buff=0.25)
        t2 = label(r"time across, \ lag down", font_size=22, color=GREY_A).next_to(lag, UP, buff=0.25)
        arrow = Arrow(img.get_right(), lag.get_left(), buff=0.2, color=GREY_B)
        y32 = lag.get_top()[1] - lag.height * 32 / n
        mark = DashedLine([lag.get_left()[0], y32, 0], [lag.get_right()[0], y32, 0], color=EAR, stroke_width=2)
        side = VGroup(label(r"a repeat 32 beats later: \\ a line at lag 32", font_size=20, color=EAR),
                      label(r"stripes become horizontal lines", font_size=20, color=WHITE)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(lag, DOWN, buff=0.3)
        with self.voiceover(
            "There is a second way to draw the same numbers. <bookmark mark='a'/> Instead of time against time, plot "
            "time across and the lag, how far back you are comparing, down. <bookmark mark='b'/> Now every repeat "
            "becomes a horizontal line at its lag: the Tune's return of its opening, thirty-two beats later, is a line "
            "at lag thirty-two, starting when the return starts. <bookmark mark='c'/> Lines are easier for a program to "
            "find than diagonal stripes, and this time-lag picture is how repetition-based segmenters find the seams "
            "that novelty misses: problem four asks you to build one."
        ) as vo:
            self.play(FadeIn(img), FadeIn(t1))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(lag), FadeIn(t2))
            vo.wait_until("b")
            self.play(Create(mark), FadeIn(side))
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def from_sound(self):
        d = load("tune")
        c = clip("tune.harmony")
        A = ssm_image(d["ssm_notes"], size=3.8).move_to(LEFT * 3.4 + DOWN * 0.3)
        B = ssm_image(d["ssm_audio"], size=3.8).move_to(RIGHT * 3.4 + DOWN * 0.3)
        ta = label(r"from the notes", font_size=24, color=GREY_A).next_to(A, UP, buff=0.3)
        tb = label(r"from the sound", font_size=24, color=TUNE).next_to(B, UP, buff=0.3)
        n = len(d["ssm_notes"])
        cur = Line(ORIGIN, ORIGIN, color=WHITE, stroke_width=3)
        with self.voiceover(
            "The same picture can be made from a recording, with no score at all: cut the sound into frames, measure "
            "the energy near each of the twelve notes in every octave, and compare. Here is the Tune with its harmony, "
            "on the piano of Part 7, with the picture of its written notes, melody and chords, beside the picture of "
            "its sound. The chords make both busier than the melody's alone, and the piano's overtones blur the second, "
            "but the same pattern is there."
        ):
            self.play(FadeIn(A), FadeIn(B), FadeIn(ta), FadeIn(tb))
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ with its harmony", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            size = B.height

            def upd(m, t):
                b = min(max(t / d["beat"], 0.0), n)
                x = B.get_left()[0] + size * b / n
                m.put_start_and_end_on([x, B.get_top()[1], 0], [x, B.get_bottom()[1], 0])

            snd.drive(cur, upd)
            self.add(cur)
        self.wait(0.3)
        self.clear_scene()
