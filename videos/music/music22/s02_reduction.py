from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Reduction(SoundScene):
    def construct(self):
        chapter(self, 1, r"Reduction and prolongation", r"Which notes are the skeleton, \ and which the flesh?")
        self.kinds()
        self.quiz()
        self.prolong()

    # ------------------------------------------------------------------
    def kinds(self):
        cells = VGroup()
        demos = [(r"passing", [(72, 0, 1), (74, 1, 1), (76, 2, 2)], "C D E: \\ D passes between"),
                 (r"neighbour", [(72, 0, 1), (74, 1, 1), (72, 2, 2)], "C D C: \\ D steps away and back"),
                 (r"arpeggiation", [(72, 0, 1), (76, 1, 1), (79, 2, 2)], "C E G: \\ the chord, \\ unfolded"),
                 (r"repetition", [(72, 0, 1), (72, 1, 1), (72, 2, 2)], "C C C: \\ one note, \\ restruck")]
        for name, notes, cap in demos:
            g = mroll(notes, width=2.6, height=1.3, lo=70, hi=81, total=4.0)
            cells.add(VGroup(label(name, font_size=24, color=TUNE), g, label(cap, font_size=18, color=GREY_A)).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=0.55).move_to(UP * 0.4)
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"in each, \ one note is structural; \ the others serve it", WHITE),
            (r"the structural note is \textit{prolonged}: \ it lasts, \ in the mind, \ through the others", TUNE))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Reduction rests on a few ways one note can serve another. <bookmark mark='a'/> A passing note fills the "
            "gap between two notes a third apart. A neighbour note steps away and comes back. An arpeggiation unfolds a "
            "chord in time. A repetition strikes the same note again. <bookmark mark='b'/> In each, one note is "
            "structural and the others serve it, and the structural note is said to be prolonged: it lasts, in the "
            "listener's mind, through the notes that decorate it."
        ) as vo:
            self.play(FadeIn(cells[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows_))
        d = load("kinds")
        c = clip("reduction.kinds")
        with self.voiceover("Hear the four, in order. In each, the first note is the one that lasts in the mind."):
            pass
        with self.listen(c) as snd:
            window(snd, r"passing, \ neighbour, \ arpeggiation, \ repetition", detail=r"Part 7's piano", corner=UL, tag_corner=UR)
            for cell, k in zip(cells, d["demos"]):
                s0 = d["starts"][k]
                flash(snd, cell[1].notes, [s0 + n[1] * d["beat"] for n in d["demos"][k]], hot=WHITE, base=TUNE)
                pulse(snd, cell[0], s0, s0 + 4 * d["beat"], buff=0.08)
        with self.voiceover("Reduction is the reverse of decoration: remove the servants, and see what they served."):
            self.play(Indicate(rows_[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("skeleton")
        c = clip("skeleton.three")
        card = listen_card(r"The Tune's first strain, \ then two candidate skeletons, \ a note every four beats, \ "
                           r"over the same chords. \ Which skeleton is the strain's, \ A or B?", width=10.4)
        with self.voiceover(
            "Your turn. You will hear the Tune's first strain, then two candidate skeletons, one note every four beats, "
            "over the same chords. Which skeleton belongs to the strain, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        g0 = mroll(d["surface"], width=10.0, height=1.2, lo=70, hi=84, total=16.0).move_to(UP * 1.6)
        gA = mroll(d["A"], width=4.6, height=1.2, lo=70, hi=84, total=16.0, color=BLUE).move_to(LEFT * 3.0 + DOWN * 1.0)
        gB = mroll(d["B"], width=4.6, height=1.2, lo=70, hi=84, total=16.0, color=BLUE).move_to(RIGHT * 3.0 + DOWN * 1.0)
        la = label(r"A", font_size=36, color=GREY_A).next_to(gA, UP, buff=0.25)
        lb = label(r"B", font_size=36, color=GREY_A).next_to(gB, UP, buff=0.25)
        self.play(FadeOut(card), FadeIn(g0), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"the strain, \ then A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g0.notes, [d["starts"]["surface"] + n[1] * d["beat"] for n in d["surface"]], hot=WHITE, base=TUNE)
            flash(snd, gA.notes, [d["starts"]["A"] + n[1] * d["beat"] for n in d["A"]], hot=WHITE, base=BLUE)
            flash(snd, gB.notes, [d["starts"]["B"] + n[1] * d["beat"] for n in d["B"]], hot=WHITE, base=BLUE)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        names = lambda ns: r" \ ".join(NAMES[n[0] % 12] for n in ns)  # noqa: E731
        ans = VGroup(label(names(d["A"]), font_size=26, color=GREY_A).next_to(gA, DOWN, buff=0.3),
                     label(names(d["B"]), font_size=26, color=TUNE).next_to(gB, DOWN, buff=0.3))
        with self.voiceover(
            "B: C, G, E, C. Each of its notes is a note of the chord sounding at that moment, on the strongest beat of "
            "its span, and a stable degree of the scale. A replaced two of them by their neighbours, A and F, and they "
            "rub against the chords. A skeleton is not any set of notes that fits the rhythm: it is the set the harmony "
            "supports."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prolong(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"a prolongation can last a bar, \ a phrase, \ a whole movement", WHITE),
            (r"a whole section can prolong one chord: \ the tonic, \ the dominant", WHITE),
            (r"so a piece is a tree: \ each event elaborates a deeper one", WHITE),
            (r"the claim of reduction: \ listeners hear the deeper events through the surface", TUNE),
            (r"the question for this part: \ is that true, \ and can it be computed?", EAR))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"prolongation at every scale", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The idea scales up. <bookmark mark='a'/> A note can be prolonged for a bar, a phrase, or longer. "
            "<bookmark mark='b'/> A whole section can prolong a single chord: the development of a sonata, Part 21's "
            "drama, can be heard as one long dominant. <bookmark mark='c'/> So a piece becomes a tree, every event "
            "elaborating a deeper one. <bookmark mark='d'/> The claim behind reduction is that listeners hear the deep "
            "events through the surface, as a reader hears a sentence's structure through its words. "
            "<bookmark mark='e'/> This part asks whether that is true, and whether it can be computed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
