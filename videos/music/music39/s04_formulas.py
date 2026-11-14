from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403
from explainer.music.monochord import blues as BL


class Formulas(SoundScene):
    def construct(self):
        chapter(self, 3, r"Enclosures and formulas", r"How does a line arrive exactly on time?")
        self.targets()
        self.diagram()
        self.hear()
        self.formulas()
        self.keys()
        self.vocabulary()

    # ------------------------------------------------------------------
    def targets(self):
        items = [
            (r"improvisers think in \textit{targets}: \ a strong note of the next chord, \ on its first beat", WHITE),
            (r"usually a guide tone \ (Part 38): \ the third or seventh, \ which names the new chord", WHITE),
            (r"the notes before it are the approach: \ by step, \ by arpeggio, \ or by surrounding it", WHITE),
            (r"an \textit{enclosure} surrounds the target: \ a note above, \ a note below, \ then the target", TUNE),
            (r"the ear hears the target coming, \ and its arrival lands harder", GREY_A),
        ]
        rows_scene(self, r"aiming at targets", items,
                   "Improvisers think in targets: a strong note of the next chord, placed on its first beat. "
                   "<bookmark mark='b'/> Usually it is a guide tone from Part 38, the third or the seventh, which names the new "
                   "chord. <bookmark mark='c'/> The notes before it are the approach: by step, by arpeggio, or by surrounding "
                   "it. <bookmark mark='d'/> An enclosure surrounds the target: a note above, a note below, then the target. "
                   "<bookmark mark='e'/> The ear hears the target coming, and its arrival lands harder.", marks="bcde")

    # ------------------------------------------------------------------
    def diagram(self):
        d = load("enclose")
        rows_ = VGroup()
        names = {"plain": r"plain: \ a step into the target", "enclosed": r"enclosure: \ above, \ below, \ target", "double": r"double chromatic: \ two above, \ one below, \ target"}
        cols = {"plain": GREY_A, "enclosed": TUNE, "double": EAR}
        for k, L in d["ways"].items():
            tail = L[-4:]
            pts = VGroup()
            for j, (m, e) in enumerate(tail):
                pts.add(Dot([j * 0.9, (m - 76) * 0.22, 0], radius=0.1 if j < len(tail) - 1 else 0.15, color=cols[k] if j < len(tail) - 1 else WHITE))
            path = VMobject(color=cols[k], stroke_width=2).set_points_as_corners([p.get_center() for p in pts])
            tgt = DashedLine([-0.4, 0, 0], [3.2, 0, 0], color=GREY_D, stroke_width=1)
            rows_.add(VGroup(label(names[k], font_size=19, color=cols[k]), VGroup(tgt, path, pts)).arrange(RIGHT, buff=0.6))
        rows_.arrange(DOWN, buff=0.6, aligned_edge=RIGHT).move_to(DOWN * 0.1)
        head = label(r"three ways to reach E, \ the third of Cmaj7 \ (dashed line: \ the target)", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here are the last few notes before a target, three ways, aiming at E, the third of C major seven. "
            "<bookmark mark='a'/> Plainly, by a step. <bookmark mark='b'/> By an enclosure: F above, E flat below, then E. "
            "<bookmark mark='c'/> And by a double chromatic enclosure: F sharp and F above, then D and E flat below, closing in "
            "on the target from both sides."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.2)))   # a ghost of what is coming: never a bare title
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("enclose")
        c = clip("enclose.three")
        ch = [["Dm7"], ["G7"], ["Cmaj7"]]
        gs = VGroup()
        for k, col in (("plain", GREY_A), ("enclosed", TUNE), ("double", EAR)):
            L = [tuple(x) for x in d["ways"][k]]
            gs.add(line_over(L, ch, width=11.0, height=1.1, color=col, lo=68, hi=84, size=14))
        gs.arrange(DOWN, buff=0.55).move_to(DOWN * 0.1)
        with self.voiceover(
            "Hear the three, each over D minor seven, G seven, C major seven, on an additive saxophone with piano, bass and "
            "cymbal. In each, listen for the moment the E arrives."
        ):
            self.play(FadeIn(gs))
        with self.listen(c) as snd:
            window(snd, r"plain, \ enclosed, \ double", kind="synthesized", detail=r"an additive saxophone over piano, \ string and cymbal", corner=DL, tag_corner=DR)
            for g, k in zip(gs, ("plain", "enclosed", "double")):
                L = d["ways"][k]
                flash(snd, g.roll.notes, list(BL.swing_times([e for _, e in L], d["bpm"]) + d["starts"][k]), hot=WHITE, base=GREY_D)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def formulas(self):
        items = [
            (r"Thomas Owens \ (1974) \ catalogued about a hundred melodic formulas in Charlie Parker's recorded solos", WHITE),
            (r"Parker used them in different keys, \ at different points in the bar, \ combined in new ways", WHITE),
            (r"Martin Norgaard \ (2014): \ much of Parker's improvising is built from recurring patterns, \ often transposed", WHITE),
            (r"formulas are not cheating: \ they are words in a language spoken fast", TUNE),
            (r"the open question: \ how much is recalled, \ and how much invented in the moment?", GREY_A),
        ]
        rows_scene(self, r"formulas", items,
                   "Lines are also built from formulas. <bookmark mark='b'/> In 1974 Thomas Owens catalogued about a hundred "
                   "melodic formulas in Charlie Parker's recorded solos. <bookmark mark='c'/> Parker used them in different keys, "
                   "at different points in the bar, combined in new ways. <bookmark mark='d'/> In 2014 Martin Norgaard showed by "
                   "computer that much of Parker's improvising is built from recurring patterns, often transposed. "
                   "<bookmark mark='e'/> Formulas are not cheating: they are words in a language spoken fast. "
                   "<bookmark mark='f'/> The open question is how much is recalled and how much invented in the moment.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def keys(self):
        d = load("formula")
        c = clip("formula.keys")
        rows_ = VGroup()
        for name, k, col in zip(d["keys"], d["shifts"], (TUNE, BLUE, EAR)):
            L = [(m + k, e) for m, e in d["formula"]]
            ch = [[BL.transpose("Dm7", k % 12), BL.transpose("G7", k % 12)], [BL.transpose("Cmaj7", k % 12)]]
            g = line_over(L, ch, width=6.4, height=1.0, color=col, lo=66, hi=88, size=13)
            rows_.add(VGroup(label(rf"in {sym(name)}", font_size=20, color=col), g).arrange(RIGHT, buff=0.5))
        rows_.arrange(DOWN, buff=0.5, aligned_edge=RIGHT).move_to(DOWN * 0.1)
        head = label(r"one figure of ours, \ three keys", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Players practise formulas in every key, so the fingers know them anywhere. Here is a two-five-one figure of our "
            "own, a guide tone on each chord change, played in C, then F, then B flat, round the circle of fifths as the "
            "standards move. Same shape, three places."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"a figure in three keys", kind="synthesized", detail=r"an additive saxophone over piano, \ string and cymbal", corner=DL, tag_corner=DR)
            for g, name in zip(rows_, d["keys"]):
                flash(snd, g[1].roll.notes, list(BL.swing_times([e for _, e in d["formula"]], d["bpm"]) + d["starts"][name]), hot=WHITE, base=GREY_D)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vocabulary(self):
        items = [
            (r"Paul Berliner's \textit{Thinking in Jazz} \ (1994): \ how players learn, \ from more than fifty musicians' accounts", WHITE),
            (r"transcribing solos from records, \ by ear, \ is the traditional apprenticeship", WHITE),
            (r"players speak of `vocabulary', \ `saying something', \ `telling a story'", WHITE),
            (r"the model is language: \ learned phrases, \ recombined, \ to say something new", TUNE),
            (r"chapter 4 asks what notes are available at all", GREY_A),
        ]
        rows_scene(self, r"vocabulary", items,
                   "How are formulas learned? <bookmark mark='b'/> Paul Berliner's Thinking in Jazz, from 1994, draws on the "
                   "accounts of more than fifty musicians. <bookmark mark='c'/> The traditional apprenticeship is transcribing solos "
                   "from records, by ear. <bookmark mark='d'/> Players speak of vocabulary, of saying something, of telling a "
                   "story. <bookmark mark='e'/> The model is language: learned phrases, recombined, to say something new. "
                   "<bookmark mark='f'/> Chapter four asks which notes are available at all.", marks="cdef")
