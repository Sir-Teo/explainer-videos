from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403


class Exposition(SoundScene):
    def construct(self):
        chapter(self, 9, r"An exposition, built", r"How does a program write the countersubject?")
        self.method()
        self.hear()
        self.episode()
        self.check()

    # ------------------------------------------------------------------
    def method(self):
        d = load("exposition")
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"bars 1--2: \ the subject, \ alone, \ in the top voice", WHITE),
            (r"bars 3--4: \ the tonal answer in the middle voice; \ above it, \ the countersubject", WHITE),
            (r"the countersubject: \ a search for the smoothest line consonant with the answer, \ with no fifths", WHITE),
            (r"(a Viterbi search: \ for every note on every beat, \ the cheapest way to arrive there)", GREY_A),
            (r"bars 5--6: \ the subject in the bass; \ the countersubject, \ moved down, \ above it; \ a free voice on top", WHITE),
            (r"one countersubject note clashed when moved, \ and was altered, \ as composers did", TUNE))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"a three-voice exposition on the Tune, \ step by step", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Now build an exposition on the Tune, in three voices. <bookmark mark='a'/> Bars one and two: the subject, the Tune's first phrase, alone in the top voice. <bookmark mark='b'/> Bars three and four: the tonal answer in the middle voice, and above it the countersubject. <bookmark mark='c'/> The program writes the countersubject by searching for the smoothest line, one note a beat, that is consonant with the answer on every beat, makes no parallels, and avoids fifths, so that it could later go below. <bookmark mark='d'/> The search is Part 17's Viterbi again: for each candidate state it keeps the cheapest path into it, with the transition information this cost requires. <bookmark mark='e'/> Bars five and six: the subject enters in the bass, the countersubject moves down to the middle voice above it, and the top voice gets a free line, found the same way against both. <bookmark mark='f'/> Moved down, one note of the countersubject clashed with the subject, and the program altered it by a step, as composers did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcdef", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("exposition")
        c = clip("fugue.exposition")
        g = voices_roll(d["lines"], width=11.6, height=3.6, total=24.0).move_to(DOWN * 0.4)
        braces = VGroup()
        tags = [(0.0, 8.0, r"subject"), (8.0, 16.0, r"answer + countersubject"), (16.0, 24.0, r"subject in the bass + countersubject + free voice")]
        for a, b, t in tags:
            ln = Line([g.x(a) + 0.05, g.frame.get_top()[1] + 0.25, 0], [g.x(b) - 0.05, g.frame.get_top()[1] + 0.25, 0], color=GREY_B, stroke_width=2)
            braces.add(VGroup(ln, label(t, font_size=20, color=GREY_A).next_to(ln, UP, buff=0.1)))
        key = VGroup(*[VGroup(Dot(radius=0.07, color=VOICE_C[k]), label(n, font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.12)
                       for k, n in enumerate((r"top", r"middle", r"bass"))]).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the exposition. The gold voice begins, the pink voice answers, and the blue bass enters last."
        ):
            self.play(FadeIn(g), FadeIn(braces), FadeIn(key))
        with self.listen(c) as snd:
            window(snd, r"a fugue exposition on the Tune", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_voices(snd, g, d["lines"])
            self.add(cursor(snd, g, 0.0))
            for k, (a, b, _) in enumerate(tags):
                pulse(snd, braces[k][1], a * BEAT, b * BEAT, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def episode(self):
        d = load("episode")
        c = clip("episode.sequence")
        g = voices_roll(d["lines"], width=11.0, height=3.0, total=16.0).move_to(DOWN * 0.4)
        head = label(r"an episode: \ a fragment, \ sequenced down a step a bar, \ against its inversion", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        bars = VGroup(*[label(rf"bar {k + 1}", font_size=20, color=GREY_B).move_to([g.x(4 * k + 2), g.frame.get_bottom()[1] - 0.3, 0]) for k in range(4)])
        with self.voiceover(
            "After the exposition comes an episode, a passage without the whole subject that travels somewhere new. "
            "The usual recipe is Part 18's sequence: take a short fragment, here the first four notes of the free voice, "
            "G, A, G, B, and repeat it a step lower in each bar, while the other voice sings the fragment upside down, "
            "sequenced with it. The program chose how far below to put the lower voice so that no beat clashes."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(bars))
        with self.listen(c) as snd:
            window(snd, r"an episode by sequence", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_voices(snd, g, d["lines"])
            self.add(cursor(snd, g, 0.0))
        with self.voiceover(
            f"Sixteen beats, {say(d['faults']['dissonant'])} clashes, and the music has walked down a fourth, ready for "
            "the subject to return in a new key. Episodes are where fugues breathe, and where Bach's are most "
            "inventive."
        ):
            self.play(Indicate(bars[3], color=TUNE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("exposition")
        f = d["faults"]
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (rf"{f['beats']} beats with two or three voices: \ {f['dissonant']} dissonant, \ {f['parallels']} parallels", TUNE),
            (r"correct, \ and plain: \ one note a beat, \ no suspensions, \ no rhythm of its own", WHITE),
            (r"a real countersubject contrasts: \ it moves when the subject holds, \ and holds when it moves", WHITE),
            (r"the rules make the exposition possible; \ they do not make it good", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"what the program did, \ and did not do", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"Check it: on all {say(f['beats'])} beats where two or three voices sound, {say(f['dissonant'])} are dissonant and there are {say(f['parallels'])} parallels. <bookmark mark='a'/> It passes these limited checks, and it is deliberately plain: one note a beat, no suspensions, no rhythm of its own. <bookmark mark='b'/> A real countersubject contrasts with its subject: it moves in quick notes where the subject holds, and holds where the subject moves, so that the ear can follow two lines. <bookmark mark='c'/> As with the canons, the rules make an exposition possible; they do not make it good."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("abc", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
