from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403


class Fugue(SoundScene):
    def construct(self):
        chapter(self, 8, r"Subject and answer", r"Why does a fugue answer at the fifth, \ and why bend the answer?")
        self.parts()
        self.quiz()
        self.why()

    # ------------------------------------------------------------------
    def parts(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"subject: \ the theme, \ alone, \ in the home key", WHITE),
            (r"answer: \ the theme again in a second voice, \ a fifth higher, \ in the dominant", WHITE),
            (r"countersubject: \ the line the first voice sings against the answer, \ kept for later", WHITE),
            (r"exposition: \ every voice enters with subject or answer in turn", TUNE),
            (r"then episodes \ (sequences on fragments), \ entries in other keys, \ stretto, \ a pedal, \ the end", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"a fugue's parts", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A fugue is not a form so much as a procedure built from canon. <bookmark mark='a'/> One voice states the "
            "subject, the theme, alone. <bookmark mark='b'/> A second voice enters with the answer, the subject again "
            "but a fifth higher, in the key of the dominant. <bookmark mark='c'/> Meanwhile the first voice goes on with "
            "a counter-line, and if it is kept and reused, it is called the countersubject. <bookmark mark='d'/> Each "
            "voice enters in turn, subject, answer, subject, and when all have entered, the exposition is over. "
            "<bookmark mark='e'/> After that come episodes, sequences built from fragments, entries in other keys, "
            "perhaps a stretto, where entries overlap, and often a held bass note, a pedal, before the end."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("answers")
        c = clip("answers.two")
        card = listen_card(r"The Tune's first phrase as a fugue subject, \ answered twice at the fifth. \ "
                           r"One answer copies it exactly; \ one bends a note. \ Which answer stays closer to home, \ A or B?", width=10.4)
        with self.voiceover(
            "Take the Tune's first phrase as a fugue subject, and answer it twice at the fifth. One answer copies it "
            "exactly, a fifth higher; the other bends one interval. Which answer stays closer to the home key, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll([d["subject"], d["real"]], width=5.4, height=2.6, lo=70, hi=90, total=15.0).move_to(LEFT * 3.4 + DOWN * 0.2)
        gB = voices_roll([d["subject"], d["tonal"]], width=5.4, height=2.6, lo=70, hi=90, total=15.0).move_to(RIGHT * 3.4 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_voices(snd, gA, [d["subject"], d["real"]], start=d["starts"]["A"])
            sing_voices(snd, gB, [d["subject"], d["tonal"]], start=d["starts"]["B"])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        names = VGroup(label(r"real: \ G G \textbf{D} D E E D", font_size=24, color=GREY_A).next_to(gA, DOWN, buff=0.35),
                       label(r"tonal: \ G G \textbf{C} C E E D", font_size=24, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "B. The subject opens with a leap from C up to G, home to dominant. Answer A, the real answer, copies it "
            "exactly: G up to D, dominant to the dominant's dominant, which pulls the music toward G major at once. "
            "Answer B, the tonal answer, bends the leap: G up to C, a fourth instead of a fifth, dominant back to home, "
            "and only then continues a fifth higher. The opening is answered as a mirror, and the home key survives "
            "the answer's first notes."
        ):
            self.play(FadeIn(names))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"the rule: \ where the subject's head moves between tonic and dominant, \ swap them", WHITE),
            (r"tonic $\to$ dominant, \ dominant $\to$ tonic: \ a fifth becomes a fourth", WHITE),
            (r"the rest of the subject: \ a fifth higher, \ in the scale", WHITE),
            (r"the answer at the fifth itself: \ the canon at the fifth of chapter 2", TUNE),
            (r"why the fifth: \ the dominant is the nearest key \ (Parts 15 and 18)", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"the tonal answer, \ as an algorithm", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The rule fits in a line of code. <bookmark mark='a'/> In the subject's head, its opening notes, wherever "
            "it moves between the tonic and the dominant, swap them: <bookmark mark='b'/> tonic answered by dominant, "
            "dominant by tonic, so a fifth becomes a fourth. <bookmark mark='c'/> After the head, move everything up a "
            "fifth within the scale. <bookmark mark='d'/> Answering at the fifth is the canon at the fifth of chapter "
            "two, with the follower delayed until the leader has finished. <bookmark mark='e'/> And the fifth because "
            "the dominant is the nearest key, the first stop on every journey Parts 15 and 18 measured: the answer "
            "leaves home only as far as the next room. A subject that never touches the dominant near its start gets a "
            "real answer; one that opens on the dominant, or leaps from tonic to dominant, gets a tonal one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
