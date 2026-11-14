from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403

IV_NAME = {"0": r"unison or octave", "5": r"fourth", "7": r"fifth"}


class Imitation(SoundScene):
    def construct(self):
        chapter(self, 2, r"Imitation as structure", r"How do equal voices make a form?", extra=((1500, r"Josquin's generation"),))
        self.idea()
        self.point()
        self.counted()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"in the fourteenth century: \ a tenor from chant, \ voices above it with their own rhythms", WHITE),
            (r"about 1500: \ all voices equal, \ each entering with the same short idea", WHITE),
            (r"a `point of imitation': \ a phrase of text, \ a motive, \ entries in turn, \ then a cadence", WHITE),
            (r"a piece is a chain of points, \ one for each phrase of the words", TUNE),
            (r"Part 20's fugue grew out of this", GREY_A),
        ]
        rows_scene(self, r"equal voices", items,
                   "The second change was in how voices relate. <bookmark mark='b'/> In Machaut's time a piece was built "
                   "on a tenor, usually borrowed from chant, with voices above it moving in their own rhythms. "
                   "<bookmark mark='c'/> By about 1500, in Josquin's generation, all the voices are equal, and each enters "
                   "in turn with the same short idea. <bookmark mark='d'/> That unit is called a point of imitation: a "
                   "phrase of the text gets a motive, the voices take it up one after another, and the passage closes with "
                   "a cadence. <bookmark mark='e'/> A whole piece is a chain of points, one for each phrase of the words, "
                   "overlapping at the joins. <bookmark mark='f'/> The fugue of Part 20 grew out of this habit, two "
                   "centuries later.", marks="bcdef")

    # ------------------------------------------------------------------
    def point(self):
        d = load("imitation")["piece"]
        c = clip("imitation.point")
        vs = d["voices"]
        g = voices_roll(vs, width=11.4, height=3.4, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.12).move_to(DOWN * 0.3)
        tags = VGroup()
        for k, (j, t) in enumerate(zip(d["entry_order"], d["entry_times"])):
            first = g.parts[j].notes[0]
            tags.add(label(rf"{k + 1}", font_size=22, color=WHITE).next_to(first, UP, buff=0.12))
        head = label(rf"Palestrina, \ \textit{{{d['work']}}}, \ {d['title']}: \ four entries", font_size=24, color=GREY_A).to_edge(UP, buff=0.9)
        with self.voiceover(
            "Here is a point of imitation found by a program in Palestrina's Masses: a movement in four voices where all "
            "four enter with exactly the same intervals. The numbers mark the order of the entries. Listen to the idea "
            "pass from voice to voice, each entry starting while the others continue."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"a point of imitation", detail=r"from the encoding, \ synthetic voices", kind="synthesized", corner=UL, tag_corner=UR)
            flash_voices(snd, g, vs, 0.0, d["quarter"], colors=[TUNE, BLUE, EAR, GREY_A])
            flash(snd, list(tags), [t * d["quarter"] for t in d["entry_times"]], hot=TUNE, base=WHITE, fade=0.8)
            cursor(snd, g, 0.0, d["quarter"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counted(self):
        d = load("imitation")
        iv = d["intervals"]
        top = sorted(iv.items(), key=lambda x: -x[1])[:3]
        bars = columns([v for _, v in top], [IV_NAME.get(k, k) for k, _ in top], width=5.6, height=2.6, color=TUNE, fmt="{:.0f}", font_size=20)
        bars.move_to(LEFT * 3.3 + DOWN * 0.4)
        t = label(r"the interval between the first entry and each later one", font_size=19, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=23, color=c_) for s, c_ in (
            (rf"{100 * d['share']:.0f} in 100 of Palestrina's movements open with imitation", WHITE),
            (rf"{d['exact']:,} of {d['followers']:,} later entries copy the intervals exactly".replace(",", "{,}"), WHITE),
            (r"at the octave, \ the fourth or the fifth: \ the steps of the mode stay in place", TUNE),
            (rf"Monteverdi's madrigals: \ {100 * d['share_monteverdi']:.0f} in 100 \ (the words come first)", EAR))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 6.4))
        side.move_to(RIGHT * 3.3 + DOWN * 0.2)
        with self.voiceover(
            "How common is it? The program reads the first four melodic intervals of every voice and asks whether later "
            f"voices begin with the same ones. <bookmark mark='a'/> {say(round(100 * d['share']))} in a hundred of "
            "Palestrina's Mass movements open with imitation, <bookmark mark='b'/> and of the later entries, "
            f"{say(d['exact'])} out of {say(d['followers'])} copy the intervals exactly; the rest adjust a step, as a "
            "tonal answer does in Part 20. <bookmark mark='c'/> They enter at the octave, the fourth or the fifth, the "
            "intervals that keep the mode's half steps in the same places: a motive that steps E to F in one voice steps "
            "B to C a fifth higher, and the half step is still a half step. At the second it would not be, which is "
            "one of this part's problems. <bookmark mark='d'/> Monteverdi's madrigals "
            f"open imitatively only {say(round(100 * d['share_monteverdi']))} times in a hundred: in his music the words "
            "come first."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
