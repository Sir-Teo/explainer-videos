from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403


class Art(SoundScene):
    def construct(self):
        chapter(self, 11, r"\textit{The Art of Fugue}", r"What did Bach do with one subject?", extra=((1751, r"\textit{Die Kunst der Fuge} printed"),))
        self.one_subject()
        self.bach()
        self.unfinished()

    # ------------------------------------------------------------------
    def one_subject(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"one subject in D minor, \ and about twenty pieces on it", WHITE),
            (r"simple fugues; \ fugues against the subject's inversion", WHITE),
            (r"stretto fugues against its augmentation and diminution", WHITE),
            (r"double and triple fugues; \ mirror fugues, \ playable upside down; \ four canons", WHITE),
            (r"a catalogue of everything in this part, \ on a single line", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"\textit{The Art of Fugue}", font_size=32, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "In his last decade Bach worked on a collection that does to one subject everything this part has done. "
            "<bookmark mark='a'/> The Art of Fugue takes a plain subject in D minor, D, A, F, D, C sharp, D, E, F, and "
            "builds about twenty pieces on it. <bookmark mark='b'/> Simple fugues first, then fugues in which the "
            "subject meets its own inversion. <bookmark mark='c'/> Stretto fugues, with the subject against itself "
            "slowed down and sped up. <bookmark mark='d'/> Double and triple fugues, with new subjects combined with the "
            "first; mirror fugues that can be played entirely upside down, every voice inverted; and four canons. "
            "<bookmark mark='e'/> It is a catalogue of everything in this part, on a single line of eight notes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bach(self):
        d = load("bach")
        c = clip("bach.motif")
        g = voices_roll([d["motif"]], width=6.0, height=2.0, lo=67, hi=74, total=8.0).move_to(LEFT * 2.8 + DOWN * 0.2)
        nm = VGroup(*[VGroup(label(n, font_size=40, color=TUNE), label(s.replace("♭", r"$\flat$").replace("♮", r"$\natural$"), font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12) for n, s in zip(d["names"], d["spelled"])])
        for k, x in enumerate(nm):
            x.move_to([g.x(2 * k + 1), g.frame.get_top()[1] + 0.7, 0])
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"in German, \ B is B$\flat$ \ and H is B$\natural$", WHITE),
            (r"so Bach's name is a melody: \ four notes within a tone", WHITE),
            (r"a chromatic cell, \ like the king's slide, \ in miniature", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 5.4))
        rows_.move_to(RIGHT * 3.9 + DOWN * 0.1)
        with self.voiceover(
            "The last fugue of the collection introduces a third subject that spells a name. In German note names, B "
            "means B flat and H means B natural, so B, A, C, H is a melody: B flat, A, C, B natural."
        ):
            self.play(FadeIn(g), FadeIn(nm), FadeIn(rows_[0]))
        with self.listen(c) as snd:
            window(snd, r"B--A--C--H", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_voices(snd, g, [d["motif"]], beat=0.5)
            flash(snd, list(nm), [0.0, 1.0, 2.0, 3.0], hot=WHITE, base=TUNE)
        with self.voiceover(
            "Four notes spanning a minor third: a chromatic cell, the king's slide in miniature, and a signature "
            "that composers from Schumann and Liszt to Schoenberg and Webern have borrowed."
        ):
            self.play(FadeIn(rows_[1]), FadeIn(rows_[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unfinished(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"the last fugue stops in the middle of a bar, \ just after B--A--C--H has joined the other subjects", WHITE),
            (r"a note in the manuscript, \ by his son: \ the composer died over this fugue", WHITE),
            (r"scholars now think the ending was lost or left for later, \ not interrupted by death", GREY_A),
            (r"it was planned to combine with the main subject: \ a quadruple fugue", WHITE),
            (r"Bach died in July 1750; \ the collection was printed in 1751", TUNE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"the fugue that stops", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The story attached to it is famous. <bookmark mark='a'/> The final fugue breaks off in the middle of a bar, soon after B, A, C, H has been combined with the other subjects. <bookmark mark='b'/> In the manuscript, his son Carl Philipp Emanuel wrote that the composer died over this fugue. <bookmark mark='c'/> Scholars now doubt it: the handwriting is earlier, and a lost continuation and an unfinished plan are competing possibilities; the precise reason remains uncertain. <bookmark mark='d'/> One influential reconstruction proposes to bring the main subject in as a fourth, making a quadruple fugue, and the four subjects do fit together, as later musicians who completed it have shown. <bookmark mark='e'/> Bach died in July 1750, and the collection was printed the next year, unfinished."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
