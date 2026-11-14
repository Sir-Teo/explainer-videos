from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403


class Neapolitan(SoundScene):
    def construct(self):
        chapter(self, 3, r"The Neapolitan", r"Why does a chord a semitone above home sound so dark?")
        self.quiz()
        self.why()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("neapolitan")
        c = clip("neapolitan.pair")
        card = listen_card(r"Two cadences in C minor. \ They differ in one chord only. \ In which is that chord further from home: \ A or B?", width=9.6)
        with self.voiceover(
            "Hear two cadences in C minor that differ in one chord. In which one is that chord further from home, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        sA = block_staff(d["plain"], width=4.6, key=-3).move_to(LEFT * 3.3 + DOWN * 0.1)
        sB = block_staff(d["neapolitan"], width=4.6, key=-3).move_to(RIGHT * 3.3 + DOWN * 0.1)
        la = label(r"A", font_size=40, color=GREY_A).next_to(sA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(sB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(sA), FadeIn(sB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, la, d["starts"]["iv"], d["starts"]["N"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["N"], c.duration, buff=0.1)
        ans = VGroup(label(r"i \ iv6 \ V7 \ i", font_size=26, color=GREY_A).next_to(sA, DOWN, buff=0.35),
                     label(tex(r"i \ N6 (D♭ major) \ V7 \ i"), font_size=26, color=EAR).next_to(sB, DOWN, buff=0.35))
        with self.voiceover(
            "B. In A the second chord is the plain minor four. In B it is a D flat major chord, with its third in the "
            "bass: the Neapolitan sixth. Its D flat is a semitone above home, and from it the bass and upper voices "
            "fall onto the dominant by the smallest possible steps, D flat to C, D flat to B. The ear hears a chord from "
            "the far side of the key, and then the strongest pull back."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (tex(r"the Neapolitan: \ ♭II, \ the major triad on the lowered second degree"), WHITE),
            (r"named for the Neapolitan opera composers who used it in laments, \ though older", WHITE),
            (tex(r"it does the subdominant's job \ (iv with D♭ for D): \ a predominant"), WHITE),
            (tex(r"its D♭ falls to B through C: \ a diminished third, \ the most tense melodic step in the key"), WHITE),
            (r"Beethoven, \ \textit{Moonlight} sonata, \ first movement: \ the same chord at its darkest point", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"the chord a semitone above home", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The chord is named after the opera composers of Naples, who used it in laments, though it is older than "
            "them. <bookmark mark='a'/> It is the major triad on the lowered second degree. <bookmark mark='b'/> It "
            "does the subdominant's job: in C minor, it is the minor four with D flat in place of D. "
            "<bookmark mark='c'/> And its D flat must find its way down to B, the leading note, which means passing "
            "through C: a diminished third, the most strained step in the key. <bookmark mark='d'/> Beethoven, in the "
            "first movement of the Moonlight sonata, puts it at the point where the music is darkest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]), FadeIn(rows_[1]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows_[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[4]))
        self.wait(0.4)
        self.clear_scene()
