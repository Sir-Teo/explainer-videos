from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Ursatz(SoundScene):
    def construct(self):
        chapter(self, 2, r"The \textit{Ursatz}", r"Is every tonal piece one descent to the tonic?")
        self.structure()
        self.quiz()
        self.census()
        self.critique()

    # ------------------------------------------------------------------
    def structure(self):
        top = VGroup(*[label(t, font_size=40, color=TUNE) for t in (r"$\hat 5$", r"$\hat 4$", r"$\hat 3$", r"$\hat 2$", r"$\hat 1$")])
        for k, t in enumerate(top):
            t.move_to([-4.0 + 2.0 * k, 1.6 - 0.45 * k, 0])
        arrows = VGroup(*[Arrow(top[k].get_right(), top[k + 1].get_left(), buff=0.1, color=TUNE, stroke_width=3) for k in range(4)])
        bass = VGroup(label(r"I", font_size=40, color=BLUE).move_to([-4.0, -1.4, 0]), label(r"V", font_size=40, color=BLUE).move_to([2.0, -1.4, 0]),
                      label(r"I", font_size=40, color=BLUE).move_to([4.0, -1.4, 0]))
        bl = VGroup(Line(bass[0].get_right(), bass[1].get_left(), color=BLUE, stroke_width=2), Line(bass[1].get_right(), bass[2].get_left(), color=BLUE, stroke_width=2))
        t1 = label(r"\textit{Urlinie}: \ the fundamental line", font_size=24, color=TUNE).to_edge(UP, buff=0.4)
        t2 = label(r"\textit{Bassbrechung}: \ the bass arpeggiation", font_size=24, color=BLUE).next_to(bass, DOWN, buff=0.4)
        tune = label(r"the Tune: \ G \ (end of phrase 1) \ F \ E \ D \ C \ (phrase 2), \ over I \ ... \ V \ I", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Schenker's fundamental structure, the Ursatz, has two parts. <bookmark mark='a'/> On top, the "
            "fundamental line, falling by step from the third, fifth or octave of the scale to the tonic: here, from "
            "five. <bookmark mark='b'/> Below it, the bass arpeggiation: tonic, dominant, tonic, the dominant arriving "
            "under the second degree, so that the last step, two to one, is a cadence. <bookmark mark='c'/> The Tune "
            "lays this out on its surface: its first phrase ends on G, the fifth; the second walks down F, E, D, C over "
            "the dominant and the tonic."
        ) as vo:
            self.play(FadeIn(t1), FadeIn(top[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(arrows[k]), FadeIn(top[k + 1])) for k in range(4)], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(bass), Create(bl), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(tune))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("cadence")
        c = clip("cadence.two")
        card = listen_card(r"The Tune's second phrase, \ F F E E D D C, \ twice, \ over two different basses. \ In which does the last step, \ D to C, \ sound like an ending, \ A or B?", width=10.4)
        with self.voiceover(
            "Is the bass really part of the structure? Hear the Tune's second phrase, F F E E D D C, twice over two "
            "different basses. In which does the last step, D to C, sound like an ending, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        cells = VGroup()
        for key in "AB":
            g = mroll(d["melody"], width=4.6, height=1.4, lo=70, hi=80, total=8.0)
            ch = VGroup(*[label(tex({"C": "I", "F": "IV", "G": "V"}[x]), font_size=28, color=BLUE) for x in d[key]]).arrange(RIGHT, buff=0.75).next_to(g, DOWN, buff=0.3)
            cells.add(VGroup(label(key, font_size=40, color=GREY_A), g, ch).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=1.4).move_to(DOWN * 0.1)
        self.play(FadeOut(card), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, key in enumerate("AB"):
                flash(snd, cells[k][1].notes, [d["starts"][key] + n[1] * d["beat"] for n in d["melody"]], hot=WHITE, base=TUNE)
                end = d["starts"]["B"] - 0.5 if key == "A" else c.duration
                pulse(snd, cells[k][0], d["starts"][key], end, buff=0.1)
        ans = label(r"B: \ D over V, \ then C over I: \ the cadence the \textit{Ursatz} is made of", font_size=24, color=TUNE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "B. Over a held tonic, A's descent is a scale that stops; nothing pulls D to C. Over the Tune's own bass, the "
            "D sits on the dominant and the C arrives with the tonic, and the step is a cadence. That is why Schenker "
            "joined the two lines: the falling melody and the bass's motion to the dominant together make the close."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def census(self):
        d = load("urlinie")
        real = d["real"]
        shuf = d["shuffled"]
        vals = [real.get("5-4-3-2-1", 0), real.get("3-2-1", 0), shuf.get("5-4-3-2-1", 0), shuf.get("3-2-1", 0)]
        ch = columns(vals, [r"5--4--3--2--1", r"3--2--1", r"5--4--3--2--1", r"3--2--1"], width=7.0, height=2.6, color=WEAK, hot=(0, 1), hot_color=TUNE, fmt="{:.1f}", font_size=20).move_to(LEFT * 2.6 + DOWN * 0.5)
        tags = VGroup(label(r"the tunes", font_size=22, color=TUNE), label(r"their notes shuffled", font_size=22, color=GREY_A)).arrange(RIGHT, buff=1.6).next_to(ch, UP, buff=0.35)
        tot = real.get("5-4-3-2-1", 0) + real.get("3-2-1", 0)
        side = VGroup(label(rf"{tot} of {d['n']} major tunes end on a descent to the tonic", font_size=24, color=TUNE),
                      label(rf"shuffled: \ about {shuf.get('5-4-3-2-1', 0) + shuf.get('3-2-1', 0):.0f}", font_size=24, color=WHITE),
                      label(r"the surface ending, \ the easiest place to find it", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 4.0 + DOWN * 0.3)
        with self.voiceover(
            "How common is the fundamental line on the surface? Take Part 14's major-key tunes and ask whether each one "
            "ends with a stepwise descent to the tonic, five-four-three-two-one or three-two-one, with repeated notes "
            f"merged. <bookmark mark='a'/> {say(tot)} of the {say(d['n'])} do, {say(real.get('5-4-3-2-1', 0))} of them "
            "from the fifth, the Tune among them. <bookmark mark='b'/> Shuffle each tune's notes, keeping its last note, "
            f"and about {say(round(shuf.get('5-4-3-2-1', 0) + shuf.get('3-2-1', 0)))} would by chance. The descent is real, "
            "and it is everywhere at the ends of tunes: a cadence is usually a melody stepping down to home."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def critique(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"strength: \ it explains why tunes end as they do, \ and why some notes feel structural", WHITE),
            (r"problem: \ the theory decides in advance what it will find", EAR),
            (r"problem: \ two analysts can reduce the same piece differently", EAR),
            (r"problem: \ it applies to one repertoire, \ and ranks music by it", EAR),
            (r"to test it, \ the rules of reduction must be written down: \ the next three chapters", TUNE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"what the claim explains, \ and what it costs", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "What does the Ursatz buy? <bookmark mark='a'/> It explains why tunes end as they do, and why some notes "
            "feel more important than others. <bookmark mark='b'/> But it is a theory that decides in advance what it "
            "will find: the analyst looks for a descent, and finds one. <bookmark mark='c'/> Two analysts can reduce "
            "the same piece in different ways, both following the method. <bookmark mark='d'/> And it was built for "
            "one repertoire, German instrumental music from Bach to Brahms, and Schenker used it to rank music: what "
            "did not fit was lesser. <bookmark mark='e'/> To test a theory like this, its rules have to be written "
            "down precisely enough for someone else, or a program, to follow them. That was the aim of the next book."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
