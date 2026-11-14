from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403

TEXT = {
    "parallel": (r"no parallel fifths or octaves, \ between any two of the six pairs of voices",
                 "The first rule is Part 16's, now for six pairs of voices instead of one. From C major to D "
                 "minor, the easy way moves every voice up a step. The soprano and tenor go up in parallel "
                 "fifths, so do soprano and bass, and tenor and bass in octaves. The better way moves the "
                 "upper voices down, against the bass."),
    "leading": (r"the leading note rises to the tonic, \ above all in the outer voices",
                "Second, the leading note. In a dominant chord the third, here B, is the leading note of "
                "Part 14, a semitone below home. In the soprano it should rise to C. Let it fall instead and "
                "the cadence loses its pull."),
    "seventh": (r"a chord's seventh falls by step",
                "Third, a seventh. In the dominant seventh chord G, B, D, F, the F is a dissonance against "
                "the G, and it must resolve by falling a step, to E. Let it rise and the clash is left "
                "hanging."),
    "spacing": (r"the upper three voices within an octave of each other",
                "And fourth, spacing, from chapter two. Spread the upper voices wide apart and leave the "
                "middle empty, and the chord stops sounding like one sound and starts sounding like two "
                "groups."),
}


class Rules(SoundScene):
    def construct(self):
        chapter(self, 4, r"The rules for four", r"What must four voices avoid?")
        self.intro()
        for name in ("parallel", "leading", "seventh", "spacing"):
            self.rule(name)
        self.summary()

    # ------------------------------------------------------------------
    def intro(self):
        rows_ = VGroup(*[label(t, font_size=26, color=WHITE) for t in (
            r"from Part 16: \ no parallel perfect intervals; \ no unisons; \ approach perfect intervals with care",
            r"new with four voices: \ six pairs to watch at every move",
            r"new with chords: \ tendency notes must go where they lean",
            r"and the chord must stay one sound: \ spacing and doubling")]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.2)
        head = label(r"the rules of four-part writing, \ in four families", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The rules of four-part harmony, as every textbook gives them, come in four families. "
            "<bookmark mark='a'/> Those of Part 16, to keep voices apart. <bookmark mark='b'/> More of "
            "them, because four voices make six pairs to watch at every move. <bookmark mark='c'/> Rules "
            "for the notes that lean, from Part 14 and Part 15: the leading note and the seventh. "
            "<bookmark mark='d'/> And rules that keep the chord a single sound. Here are four of them, "
            "each heard twice: done wrong, then right."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self, name):
        d = load("rules")
        demo = d["demos"][name]
        c = clip(f"rules.{name}")
        title, speech = TEXT[name]
        head = label(title, font_size=30, color=TUNE).to_edge(UP, buff=0.5)
        sw = block_staff(demo["wrong"], width=4.6, beats=2).move_to(LEFT * 3.4 + DOWN * 0.1)
        sr = block_staff(demo["right"], width=4.6, beats=2).move_to(RIGHT * 3.4 + DOWN * 0.1)
        lw = label(r"wrong", font_size=30, color=RED).next_to(sw, UP, buff=0.3)
        lr = label(r"right", font_size=30, color=TUNE).next_to(sr, UP, buff=0.3)
        notes = {"parallel": (r"S--T and S--B fifths, \ T--B octaves", r"contrary motion: \ none"),
                 "leading": (r"B falls to G", r"B rises to C"),
                 "seventh": (r"F rises to G", r"F falls to E"),
                 "spacing": (r"soprano an octave and more above the alto", r"three upper voices within an octave")}[name]
        nw = label(notes[0], font_size=22, color=GREY_A).next_to(sw, DOWN, buff=0.35)
        nr = label(notes[1], font_size=22, color=GREY_A).next_to(sr, DOWN, buff=0.35)
        with self.voiceover(speech):
            self.play(FadeIn(head), FadeIn(sw), FadeIn(sr), FadeIn(lw), FadeIn(lr))
        with self.listen(c) as snd:
            window(snd, r"wrong, \ then right", kind="synthesized", detail=r"organ tones", corner=DL, tag_corner=DR)
            st = d["starts"][name]
            pulse(snd, lw, st["wrong"], st["right"] - 0.3, buff=0.1)
            pulse(snd, lr, st["right"], c.duration, buff=0.1)
        self.play(FadeIn(nw), FadeIn(nr))
        self.wait(1.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def summary(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"each rule protects something heard: \ independence, \ direction, \ one sound", WHITE),
            (r"but they are stated as prohibitions, \ and a textbook marks every one wrong", WHITE),
            (r"so: \ how often does Bach do what they forbid?", EAR))]).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        with self.voiceover(
            "Each of these rules protects something you can hear: the independence of the voices, the "
            "direction of a leaning note, the unity of the chord. <bookmark mark='a'/> But textbooks state "
            "them as prohibitions, and students lose marks for every one. <bookmark mark='b'/> So the "
            "obvious question is how often the master breaks them. With three hundred and sixty-four "
            "chorales as data, it can be counted."
        ) as vo:
            self.play(FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[2]))
        self.wait(0.4)
        self.clear_scene()
