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
        self.functions()
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
            "Form starts small. <bookmark mark='a'/> In this classical teaching model, a phrase is a musical unit typically articulated by a cadence, the "
            "musical equivalent of punctuation. <bookmark mark='b'/> A period is two phrases that answer each other: "
            "the first has a weaker close, often on the dominant, a question; the second ends closed, on the tonic, often beginning "
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
    def functions(self):
        d = load("phrase")
        g = melody_roll(d["A"]["melody"], width=10.0, height=2.0).move_to(UP * 0.6)
        T = sum(x[1] for x in d["A"]["melody"])
        spans = [(0, 4, r"basic idea", TUNE), (4, 8, r"basic idea again", TUNE), (8, 12, r"continuation: \ fragments", BLUE), (12, 16, r"cadence", EAR)]
        marks = VGroup()
        for a, b, t, c_ in spans:
            x0 = g.frame.get_left()[0] + g.frame.width * a / T
            x1 = g.frame.get_left()[0] + g.frame.width * b / T
            ln = Line([x0 + 0.05, g.frame.get_bottom()[1] - 0.25, 0], [x1 - 0.05, g.frame.get_bottom()[1] - 0.25, 0], color=c_, stroke_width=4)
            marks.add(VGroup(ln, label(t, font_size=20, color=c_).next_to(ln, DOWN, buff=0.12)))
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"Caplin names each part of a theme by its job: \ its formal function", WHITE),
            (r"presentation: \ an idea, \ then the idea again; \ continuation: \ fragments, \ faster harmony; \ cadential: \ the close", WHITE),
            (r"the same idea in another place does another job", TUNE))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        with self.voiceover(
            "Caplin's theory goes further than names: it says what each part of a theme does, its formal function. "
            "<bookmark mark='a'/> In the sentence, the first four bars present: an idea, then the idea again, so the "
            "listener learns it. <bookmark mark='b'/> The next bars continue: they break the idea into fragments and "
            "speed up the harmony, which signals that something is about to happen. <bookmark mark='c'/> The last bars "
            "are cadential: they close. <bookmark mark='d'/> The point is that function is not content. The same four "
            "notes could begin a piece or end one; what they do depends on where they are, and listeners hear the "
            "difference."
        ) as vo:
            self.play(FadeIn(g), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(marks[0]), FadeIn(marks[1]))
            vo.wait_until("b")
            self.play(FadeIn(marks[2]), FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(marks[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[2]))
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
            "These are schematic eight-bar classical examples; actual themes can be shorter, longer or irregular, built of two and two and four, or four and four. "
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
