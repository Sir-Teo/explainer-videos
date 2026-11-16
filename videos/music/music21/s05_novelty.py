from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403


class Novelty(SoundScene):
    def construct(self):
        chapter(self, 4, r"Finding the seams", r"Where does one section end and the next begin?", extra=((2000, r"Foote's novelty curve"),))
        self.kernel()
        self.curve_()
        self.scale()

    # ------------------------------------------------------------------
    def kernel(self):
        L = 4
        cell = 0.42
        g = VGroup()
        for i in range(2 * L):
            for j in range(2 * L):
                same = (i < L) == (j < L)
                sq = Square(side_length=cell - 0.04, stroke_width=0, fill_color=TUNE if same else BLUE, fill_opacity=0.8)
                sq.move_to([(j - L + 0.5) * cell, (L - 0.5 - i) * cell, 0])
                g.add(sq)
        g.move_to(LEFT * 3.6 + DOWN * 0.2)
        tags = VGroup(label(r"$+$", font_size=34, color=BLACK).move_to(g[0].get_center() + (g[L * 2 * L - 1].get_center() - g[0].get_center()) * 0.0 + RIGHT * cell * 1.5 + DOWN * cell * 1.5),
                      label(r"$-$", font_size=34, color=WHITE).move_to(g[2 * L - 1].get_center() + LEFT * cell * 1.5 + DOWN * cell * 1.5))
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"slide a checkerboard along the diagonal", WHITE),
            (r"gold squares: \ past like past, \ future like future", TUNE),
            (r"blue squares: \ past against future", BLUE),
            (r"sum the matching: \ high where the music before is unlike the music after", WHITE),
            (r"the peaks of this novelty curve: \ the seams", EAR))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.6))
        rows_.move_to(RIGHT * 3.2 + DOWN * 0.1)
        with self.voiceover(
            "In 2000 Foote turned the picture into a program for finding the seams of a piece. <bookmark mark='a'/> "
            "Take a small checkerboard and slide it along the bright diagonal. <bookmark mark='b'/> Two of its squares "
            "count when the music just before a moment is like itself, and the music just after is like itself. "
            "<bookmark mark='c'/> The other two count against, when before and after are alike. <bookmark mark='d'/> "
            "Add it up at every moment, and the total can peak where one homogeneous stretch gives way to a "
            "different one. <bookmark mark='e'/> The peaks of this novelty curve are the candidate boundaries."
        ) as vo:
            self.play(FadeIn(g), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve_(self):
        d = load("tune")
        c = clip("tune.harmony")
        n = len(d["novelty"])
        img = ssm_image(d["ssm_audio"], size=3.4).move_to(LEFT * 4.3 + UP * 0.2)
        cv = curve(d["novelty"], width=7.0, height=1.6, color=TUNE).move_to(RIGHT * 2.0 + UP * 0.4)
        truth = VGroup(*[tick(cv, b, n, color=GREY_B, height=1.8) for b in d["truth"]])
        found = VGroup(*[Dot([cv[0].get_left()[0] + cv[0].width * b / (n - 1), cv[0].get_y() + 1.75, 0], radius=0.08, color=EAR) for b in d["found"]])
        key = VGroup(VGroup(Line(ORIGIN, UP * 0.3, color=GREY_B, stroke_width=2.5), label(r"the Tune's phrase ends", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15),
                     VGroup(Dot(radius=0.07, color=EAR), label(r"peaks the program picks", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.6).next_to(cv, DOWN, buff=0.45)
        sc = d["score"]
        cap = label(rf"{sc['hits']} of {len(d['truth'])} phrase ends found within two beats; \ {len(d['found']) - sc['hits']} extra peaks, \ at chord changes", font_size=22, color=TUNE).to_edge(DOWN, buff=0.6)
        cur = Line(ORIGIN, ORIGIN, color=WHITE, stroke_width=2.5)
        with self.voiceover(
            "Here is the novelty curve of the Tune, computed from its sound, with a checkerboard four beats on a side. The "
            "grey lines are where the Tune's phrases really end; the pink dots are the peaks the program picks."
        ):
            self.play(FadeIn(img), FadeIn(cv), FadeIn(truth), FadeIn(key))
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ and its novelty", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, list(found), [b * d["beat"] for b in d["found"]], hot=WHITE, base=EAR, hold=0.6)

            def upd(m, t):
                b = min(max(t / d["beat"], 0.0), n - 1)
                x = cv[0].get_left()[0] + cv[0].width * b / (n - 1)
                m.put_start_and_end_on([x, cv[0].get_y(), 0], [x, cv[0].get_y() + 1.9, 0])

            snd.drive(cur, upd)
            self.add(cur, found)
        with self.voiceover(
            f"It finds {say(sc['hits'])} of the {say(len(d['truth']))} phrase ends within two beats, and adds {say(len(d['found']) - sc['hits'])} more, "
            "in the middle of phrases where the harmony changes. A checkerboard four beats wide sees the harmony move, "
            "not only the phrases end."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scale(self):
        d = load("tune")
        n = len(d["novelty"])
        c1 = curve(d["novelty"], width=10.0, height=1.2, color=TUNE).move_to(UP * 1.0)
        c2 = curve(d["novelty_wide"], width=10.0, height=1.2, color=BLUE).move_to(DOWN * 1.4)
        t1 = label(r"checkerboard 4 beats wide: \ chords and phrases", font_size=22, color=TUNE).next_to(c1, UP, buff=0.2)
        t2 = label(r"12 beats wide: \ only the largest changes", font_size=22, color=BLUE).next_to(c2, UP, buff=0.2)
        cap = label(r"the width of the checkerboard sets the scale of form the program can see", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The checkerboard width changes which contrasts this detector emphasizes. <bookmark mark='a'/> Narrow, it reports every "
            "change of chord. <bookmark mark='b'/> Wide, it smooths those away and responds only to changes that last, "
            "the boundaries between larger sections, and on a piece as short as the Tune it finds almost nothing. "
            "<bookmark mark='c'/> Form has levels, chord, phrase, section, movement, and a listener, like the program, "
            "hears the level they attend to."
        ) as vo:
            self.play(FadeIn(c1), FadeIn(t1))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(c2), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
