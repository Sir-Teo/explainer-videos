from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403


class Subtilior(SoundScene):
    def construct(self):
        chapter(self, 12, r"The Ars subtilior", r"How complicated can written rhythm get?", extra=((1390, r"the Chantilly Codex"),))
        self.courts()
        self.proportions()
        self.pages()

    # ------------------------------------------------------------------
    def courts(self):
        items = [
            (r"1378: \ the Great Schism, \ two popes, \ one in Rome, \ one in Avignon", WHITE),
            (r"at Avignon and the courts of Foix and Aragon, \ songs for connoisseurs", WHITE),
            (r"rhythms in proportion: \ three against two, \ four against three, \ syncopation across whole bars", WHITE),
            (r"new note shapes, \ red notes, \ hollow notes, \ to write them", WHITE),
            (r"a modern name: \ \textit{ars subtilior}, \ the subtler art \ (Ursula Günther, \ 1963)", GREY_A),
        ]
        rows_scene(self, r"the subtler art", items,
                   "At the end of the century the new art went further than anyone has since, for a while. "
                   "<bookmark mark='b'/> From 1378 there were two popes, one in Rome and one in Avignon, and the court at "
                   "Avignon, <bookmark mark='c'/> with the courts of Foix and Aragon in the south, cultivated songs for "
                   "connoisseurs. <bookmark mark='d'/> Their rhythms are proportions: one voice moves three notes against "
                   "another's two, or four against three, and syncopations run across whole bars. <bookmark mark='e'/> To "
                   "write them, scribes invented new shapes: red notes, hollow notes, notes with extra flags. "
                   "<bookmark mark='f'/> The style's name is modern too: the subtler art, proposed by the musicologist "
                   "Ursula Günther in 1963.", marks="bcdef")

    # ------------------------------------------------------------------
    def proportions(self):
        d = load("subtilior")
        c = clip("subtilior.proportions")
        vs = d["voices"]
        g = voices_roll(vs, width=11.0, height=3.0, colors=[EAR, TUNE, BLUE], bar_h=0.13).move_to(DOWN * 0.1)
        span = 3.0
        grid = VGroup()
        for k in range(int(round(g.total / span)) + 1):
            x = g.frame.get_left()[0] + g.frame.width * span * k / g.total
            grid.add(DashedLine([x, g.frame.get_bottom()[1] - 0.1, 0], [x, g.frame.get_top()[1] + 0.1, 0], color=DIM, stroke_width=1))
        labs_ = VGroup(label(r"three to the span", font_size=19, color=EAR), label(r"four to the span", font_size=19, color=TUNE),
                       label(r"two to the span", font_size=19, color=BLUE)).arrange(RIGHT, buff=0.8).next_to(g, UP, buff=0.3)
        head = label(r"three voices in proportion \ (ours)", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"they agree only at the dashed lines: \ the common grid is twelve to the span", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.3)
        with self.voiceover(
            "Here is the idea in its simplest form, computed for the film: three voices dividing the same span of time "
            "into three, four and two. They agree only at the dashed lines. To place every note on one grid you need "
            "twelve divisions of the span, the least common multiple again; the real pieces use proportions like these "
            "inside a single song, and change them from bar to bar. Listen for the three speeds."
        ):
            self.play(FadeIn(head), FadeIn(g), Create(grid), FadeIn(labs_), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"three, \ four and two to the span", detail=r"three synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, g, vs, 0.0, d["unit"], colors=[EAR, TUNE, BLUE])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pages(self):
        heart = VGroup(Circle(radius=0.6, color=RED, stroke_width=3).shift(LEFT * 0.42 + UP * 0.2),
                       Circle(radius=0.6, color=RED, stroke_width=3).shift(RIGHT * 0.42 + UP * 0.2),
                       Polygon([-1.0, -0.1, 0], [1.0, -0.1, 0], [0, -1.3, 0], color=RED, stroke_width=3))
        circ = VGroup(Circle(radius=0.9, color=TUNE, stroke_width=3), Circle(radius=0.55, color=TUNE, stroke_width=1.5))
        pics = VGroup(VGroup(heart, label(r"\textit{Belle, bonne, sage}: \ written in a heart", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.3),
                      VGroup(circ, label(r"\textit{Tout par compas}: \ a canon written in a circle", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.3)).arrange(RIGHT, buff=1.6).move_to(UP * 1.0)
        rows_ = VGroup(*[label(t, font_size=22, color=c_) for t, c_ in (
            (r"Baude Cordier, \ about 1400: \ two songs added to the Chantilly Codex", WHITE),
            (r"the page itself as part of the art: \ notation as a puzzle and a picture", WHITE),
            (r"our corpus holds none of these songs: \ the counts of chapter 11 cannot speak for them", EAR),
            (r"after 1420 the style vanished: \ the next generation chose clarity \ (Part 24)", TUNE))]).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(DOWN, buff=0.45)
        rows_.scale_to_fit_width(min(rows_.width, 12.4))
        with self.voiceover(
            "The most famous pages of the style are by Baude Cordier, copied into the Chantilly Codex around 1400. <bookmark mark='a'/> A love song, Belle, bonne, sage, is written on a page shaped like a heart, with red notes for the changes of proportion; a canon, Tout par compas, is written in a circle, to be sung round and round. <bookmark mark='b'/> The notation is part of the work: a puzzle for the singer and a picture for the owner. <bookmark mark='c'/> A caution: the film's corpus contains none of these songs, so the counts of the last chapter say nothing about them. <bookmark mark='d'/> And the style did not last. After about 1420 the next generation, Dufay among them, turned to smooth lines and full triads, while later scholarship renewed interest in a repertory with a complicated history of transmission and reception."
        ) as vo:
            self.play(FadeIn(pics), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
