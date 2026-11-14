from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403


class Phrases(SoundScene):
    def construct(self):
        chapter(self, 2, r"Periodic phrasing", r"How long is a Classical phrase?", extra=((1793, r"Koch's \textit{Versuch}"),))
        self.quiz()
        self.period()
        self.forms()
        self.counted()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("phrases")
        c = clip("phrases.quiz")
        card = listen_card(r"Two four-bar phrases on the Tune. \ One sounds finished; \ one sounds like a question waiting for an answer. \ "
                           r"Which one is finished, \ A or B?", width=10.4)
        with self.voiceover(
            "A question for your ears. Two four-bar phrases on the Tune's opening. One sounds finished; the other sounds "
            "like a question, waiting for an answer. Which is finished, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll([d["A"], d["A_acc"]], width=5.2, height=2.6, colors=[TUNE, GREY_A], lo=40, hi=84, bar_h=0.13).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = voices_roll([d["B"], d["B_acc"]], width=5.2, height=2.6, colors=[TUNE, GREY_A], lo=40, hi=84, bar_h=0.13).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.35)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.35)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, [d["A"], d["A_acc"]], d["starts"]["A"], d["unit"], colors=[TUNE, GREY_A])
            flash_voices(snd, gB, [d["B"], d["B_acc"]], d["starts"]["B"], d["unit"], colors=[TUNE, GREY_A])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"ends on V: \ a half cadence, \ a question", font_size=22, color=EAR).next_to(gA, DOWN, buff=0.35),
                     label(r"ends on I: \ an authentic cadence, \ an answer", font_size=22, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "B is finished: it falls to C over the tonic chord, an authentic cadence. A stops on G over the dominant, a "
            "half cadence, and asks to go on. Put A first and B second and you have the basic unit of Classical phrasing."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def period(self):
        items = [
            (r"the period: \ an antecedent ending on a half cadence, \ a consequent ending on a full one", WHITE),
            (r"four bars and four: \ eight bars, \ a question and its answer", WHITE),
            (r"the sentence: \ an idea, \ its repetition, \ then a quicker continuation to the cadence \ (Part 21)", WHITE),
            (r"Heinrich Christoph Koch \ (1782--1793): \ phrases built from two-bar units, \ like clauses", TUNE),
            (r"William Caplin \ (1998): \ the modern theory of these `formal functions'", GREY_A),
        ]
        rows_scene(self, r"the period and the sentence", items,
                   "The answer to a half cadence is a full one. <bookmark mark='b'/> A period is an antecedent ending on "
                   "a half cadence and a consequent, usually beginning the same way, ending on an authentic cadence: "
                   "<bookmark mark='c'/> four bars and four, a question and its answer. <bookmark mark='d'/> The other "
                   "common theme-type, which Part 21 heard, is the sentence: an idea, its repetition, and a faster "
                   "continuation driving to the cadence. <bookmark mark='e'/> The theorist Heinrich Christoph Koch "
                   "described this phrasing at the time, building melodies from two-bar units the way sentences are built "
                   "from clauses. <bookmark mark='f'/> William Caplin's modern theory of formal functions makes it exact.", marks="cdef")

    # ------------------------------------------------------------------
    def forms(self):
        d = load("forms")
        c = clip("forms.two")
        gP = voices_roll([d["period"], d["period_acc"]], width=5.4, height=2.6, colors=[TUNE, GREY_A], lo=40, hi=86, bar_h=0.12).move_to(LEFT * 3.3 + DOWN * 0.3)
        gS = voices_roll([d["sentence"], d["sentence_acc"]], width=5.4, height=2.6, colors=[EAR, GREY_A], lo=40, hi=86, bar_h=0.12).move_to(RIGHT * 3.3 + DOWN * 0.3)
        lP = label(r"a period: \ question, \ answer", font_size=22, color=TUNE).next_to(gP, UP, buff=0.3)
        lS = label(r"a sentence: \ idea, \ idea again, \ drive to the cadence", font_size=22, color=EAR).next_to(gS, UP, buff=0.3)
        head = label(r"two eight-bar themes on the Tune \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear the two shapes on the Tune's own material. First a period: the antecedent to the half cadence, the "
            "consequent to the full one. Then a sentence: the idea, the idea again a step higher, and a quicker "
            "continuation in running notes, driving to the cadence."
        ):
            self.play(FadeIn(head), FadeIn(gP), FadeIn(gS), FadeIn(lP), FadeIn(lS))
        with self.listen(c) as snd:
            window(snd, r"a period, \ then a sentence", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash_voices(snd, gP, [d["period"], d["period_acc"]], d["starts"]["period"], d["unit"], colors=[TUNE, GREY_A])
            flash_voices(snd, gS, [d["sentence"], d["sentence_acc"]], d["starts"]["sentence"], d["unit"], colors=[EAR, GREY_A])
            pulse(snd, lP, d["starts"]["period"], d["starts"]["sentence"] - 0.5, buff=0.08)
            pulse(snd, lS, d["starts"]["sentence"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counted(self):
        d = load("phrases")
        g = {int(k): v for k, v in d["gaps"].items()}
        ks = list(range(2, 17))
        bars = columns([g.get(k, 0) for k in ks], [str(k) for k in ks], width=7.8, height=2.6, color=TUNE, fmt="{:.0f}", font_size=17)
        bars.move_to(LEFT * 2.4 + DOWN * 0.4)
        t = label(rf"bars between authentic cadences, \ {d['cadences']} cadences in 33 quartet movements", font_size=20, color=GREY_A).next_to(bars, UP, buff=0.35)
        per = d["periodic"]
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (r"the peaks: \ 4 and 8 bars", TUNE),
            (rf"exactly 4 or 8, \ in 100: \ Haydn {100 * per['haydn']:.0f}, \ Mozart {100 * per['mozart']:.0f}, \ Beethoven {100 * per['beethoven']:.0f}", WHITE),
            (r"most gaps are elsewhere", EAR),
            (r"a strict detector: \ bass down a fifth", GREY_A))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.2))
        side.move_to(RIGHT * 4.5 + DOWN * 0.2)
        with self.voiceover(
            "How periodic is the real music? A program finds every authentic cadence in the thirty-three quartet "
            f"movements, {say(d['cadences'])} of them, where the bass falls a fifth onto a downbeat and the top voice "
            "lands on the tonic or its third, and measures the bars between them. <bookmark mark='a'/> The peaks are at "
            "four and eight bars. <bookmark mark='b'/> But gaps of exactly four or eight are a minority: Mozart's are "
            f"{say(round(100 * per['mozart']))} in a hundred, Haydn's {say(round(100 * per['haydn']))}. "
            "<bookmark mark='c'/> Real phrases stretch, overlap and elide; the four-bar norm is the background against "
            "which those departures are heard. <bookmark mark='d'/> The detector is also strict, and misses cadences "
            "where the bass does not move by a fifth."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
