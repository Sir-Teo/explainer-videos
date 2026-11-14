from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403

NAMES = {"authentic": (r"authentic", r"V to I: \ a full stop"), "half": (r"half", r"stops on V: \ a comma, \ or a question"), "plagal": (r"plagal", r"IV to I: \ the ``Amen''"),
         "deceptive": (r"deceptive", r"V to vi: \ the stop that does not come")}


class Cadences(SoundScene):
    def construct(self):
        chapter(self, 4, r"Four endings", r"How does a phrase stop?")
        self.four()
        self.soprano()
        self.quiz()

    # ------------------------------------------------------------------
    def four(self):
        d = load("cadences")
        c = clip("cadences.four")
        kb = keys(41, 77, width=10.0, height=1.3).to_edge(DOWN, buff=1.25)
        rows = VGroup()
        for k, key in enumerate(d["cadences"]):
            nm, what = NAMES[key]
            r = VGroup(label(nm, font_size=30, color=TUNE), chips(d["cadences"][key]["names"], font_size=30, buff=0.45), label(what, font_size=24, color=GREY_A))
            r[0].move_to([-5.6, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-3.2, 0, 0], aligned_edge=LEFT)
            r[2].move_to([1.2, 0, 0], aligned_edge=LEFT)
            rows.add(r)
        rows.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(UP * 1.4)
        with self.voiceover(
            "The three jobs come to a point at the end of a phrase. The last two chords of a phrase are "
            "called a cadence, and there are four that matter. <bookmark mark='a'/> Dominant to tonic: "
            "the authentic cadence, a full stop. <bookmark mark='b'/> A phrase that stops on the "
            "dominant: a half cadence, a comma, or a question. <bookmark mark='c'/> Four to one: the "
            "plagal cadence, the Amen at the end of a hymn. <bookmark mark='d'/> And the dominant going "
            "not to one but to six: the deceptive cadence. Everything promises the tonic, and the bass "
            "steps up instead of falling home. Listen to the four."
        ) as vo:
            self.play(FadeIn(kb))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        keysl = list(d["cadences"])
        allch = [ch for k in keysl for ch in d["cadences"][k]["chords"]]
        allt = [t for k in keysl for t in d["times"][k]]
        with self.listen(c) as snd:
            window(snd, r"four cadences", detail=r"in C major: \ Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, allch, allt, end=c.duration)
            for i, k in enumerate(keysl):
                pulse(snd, rows[i][0], d["starts"][k], d["starts"][keysl[i + 1]] - 0.3 if i < 3 else c.duration, buff=0.1)
        kb.clear()
        with self.voiceover(
            "These are the punctuation of tonal music. In Part 14, phrases ended as questions until the "
            "last one answered: now those have names. The question is a half cadence. The answer is an "
            "authentic one. And the deceptive cadence is how a composer says: not yet."
        ):
            self.play(Indicate(rows[1][0], color=EAR), Indicate(rows[0][0], color=TUNE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("cadences")["quiz"]
        c = clip("cadences.quiz")
        card = listen_card(r"Three endings, \ in a new key. \ One of them is the deceptive cadence. \ Which: \ A, \ B or C?", width=9.2)
        with self.voiceover("Try your ear. Three endings, in a new key. One of them is the deceptive cadence. Which: A, B or C?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B", "C"), buff=0.9, width=2.2, height=1.2, font_size=48).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", detail=r"in D major: \ Part 7's piano", corner=DL, tag_corner=DR)
            for k, key in enumerate("ABC"):
                pulse(snd, bx[k], d["starts"][key], d["starts"]["ABC"[k + 1]] - 0.4 if k < 2 else c.duration, buff=0.1)
        ans = VGroup(*[label(t, font_size=28, color=TUNE if k == 1 else GREY_A).next_to(bx[k], DOWN, buff=0.3) for k, t in enumerate((r"half", r"deceptive", r"authentic"))])
        with self.voiceover(
            "B. A stopped on the dominant, in mid air: a half cadence. C came home: authentic. B did "
            "everything C did until the last chord, and then turned aside. Notice that you could hear "
            "all that in a key you were not told, on first hearing. You found the home note within a "
            "chord or two. How? That is the next chapter."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def soprano(self):
        d = load("more")["soprano"]
        c = clip("cadences.soprano")
        kb = keys(41, 84, width=10.0, height=1.3).move_to(UP * 0.3)
        tags = VGroup(VGroup(label(r"melody ends on the first degree", font_size=28, color=TUNE), label(r"a perfect authentic cadence", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12),
                      VGroup(label(r"melody ends on the third degree", font_size=28, color=BLUE), label(r"an imperfect one", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12)).arrange(RIGHT, buff=1.2).move_to(UP * 2.3)
        note = listen_note(r"The same chords twice. \ Only the top note differs. \ Which is the firmer ending?", width=8.0).to_edge(DOWN, buff=1.05)
        with self.voiceover(
            "Even the full stop comes in two strengths. The chords of an authentic cadence can be the "
            "same while the melody ends on different notes of the tonic chord. Listen to the same three "
            "chords twice: first with the tune ending on the first degree, then on the third."
        ):
            self.play(FadeIn(kb), FadeIn(tags), FadeIn(note))
        keys2 = ("perfect", "imperfect")
        with self.listen(c) as snd:
            window(snd, r"one cadence, \ two top notes", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, [ch[:-1] for k in keys2 for ch in d["chords"][k]], [t for k in keys2 for t in d["times"][k]], end=c.duration, color=BLUE,
                         melody=[ch[-1] for k in keys2 for ch in d["chords"][k]], melody_times=[t for k in keys2 for t in d["times"][k]], melody_color=GOLD)
            pulse(snd, tags[0], d["starts"]["perfect"], d["starts"]["imperfect"] - 0.4, buff=0.12)
            pulse(snd, tags[1], d["starts"]["imperfect"], c.duration, buff=0.12)
        kb.clear()
        with self.voiceover(
            "The first closes the door. The second leaves it ajar. This is the profile of chapter one "
            "at work in the melody: the tonic is at the top of the ranking, the third a level below, "
            "and you hear exactly that difference in how finished the ending feels. Composers save the "
            "first kind for the end of a section."
        ):
            self.play(FadeOut(note), Indicate(tags[0], color=TUNE, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()
