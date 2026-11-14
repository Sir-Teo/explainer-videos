from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403


def melody_roll(mel, width=5.4, height=2.0, lo=58, hi=86, color=TUNE):
    ps = [p for p, _ in mel]
    bs = [d for _, d in mel]
    return roll(ps, bs, width=width, height=height, color=color, lo=lo, hi=hi, lines=())


class Phrase(SoundScene):
    def construct(self):
        chapter(self, 1, r"Phrase, \ period, \ sentence", r"What is the smallest complete thought in music?", extra=((1998, r"Caplin's \textit{Classical Form}"),))
        self.terms()
        self.quiz()
        self.why()

    # ------------------------------------------------------------------
    def terms(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"a phrase: \ a stretch of music that ends with a cadence", WHITE),
            (r"a period: \ two phrases, \ the first ending open \ (half cadence), \ the second closed", WHITE),
            (r"a sentence: \ an idea, \ the idea again, \ then a quicker run to the cadence", WHITE),
            (r"Caplin's theory of classical form: \ these two are the building blocks of themes", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"the small forms", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Form starts small. <bookmark mark='a'/> A phrase is a stretch of music that ends with a cadence, the "
            "musical equivalent of punctuation. <bookmark mark='b'/> A period is two phrases that answer each other: "
            "the first ends open, on the dominant, a question; the second ends closed, on the tonic, often beginning "
            "the same way as the first. <bookmark mark='c'/> A sentence works differently: a short idea, the idea again, and then a quicker "
            "continuation that breaks the idea into fragments and drives to the cadence. <bookmark mark='d'/> William "
            "Caplin's theory of classical form, from 1998, takes these two as the main ways a theme is built."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("phrase")
        c = clip("phrase.two")
        card = listen_card(r"Two themes on the Tune's notes. \ One is a period, \ one a sentence. \ Which is the period, \ A or B?", width=9.6)
        with self.voiceover(
            "Two themes made from the Tune's notes. One is a period, the other a sentence. Which is the period, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = melody_roll(d["A"]["melody"]).move_to(LEFT * 3.4 + DOWN * 0.2)
        gB = melody_roll(d["B"]["melody"]).move_to(RIGHT * 3.4 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for g, key in ((gA, "A"), (gB, "B")):
                on = np.concatenate([[0.0], np.cumsum([x[1] for x in d[key]["melody"]])])[:-1]
                flash(snd, g.notes, [d["starts"][key] + t * d["beat"] for t in on], hot=WHITE, base=TUNE)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ann = VGroup(label(r"idea, \ idea, \ continuation, \ cadence", font_size=22, color=GREY_A).next_to(gA, DOWN, buff=0.35),
                     label(r"question (ends on V), \ answer (ends on I)", font_size=22, color=EAR).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "B is the period: its first phrase, C C G G A A G, stops on the dominant chord, open; the second phrase "
            "answers and closes on C. That is the Tune's own opening. A is a sentence: the idea C C G G, then the same "
            "idea again, then a run down the scale, A G F E D C, to the cadence."
        ):
            self.play(FadeIn(ann))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"both are made of 2 + 2 + 4 bars, \ or 4 + 4", WHITE),
            (r"the period works by answer: \ often the second phrase starts like the first", WHITE),
            (r"the sentence works by acceleration: \ the idea, \ repeated, \ then broken up", WHITE),
            (r"Beethoven's first piano sonata opens with a textbook sentence", GREY_A),
            (r"the same two plans scale up: \ themes, \ sections, \ whole movements", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"two ways to make a theme", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Both are eight bars long in the classical style, built of two and two and four, or four and four. "
            "<bookmark mark='a'/> The period works by answer. Often its second phrase starts like the first, so the ear "
            "expects the same and gets a different ending; the Tune's opening is a contrasting period, whose answer "
            "starts elsewhere. <bookmark mark='b'/> The sentence works by acceleration: "
            "the idea, the idea again, then its pieces faster and faster. <bookmark mark='c'/> Beethoven's first piano "
            "sonata opens with a textbook sentence. <bookmark mark='d'/> And the two ideas, return and acceleration, scale "
            "up: the rest of this part is about how whole pieces return to what they began with."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("abcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
