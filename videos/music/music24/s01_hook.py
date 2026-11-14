from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.forster()
        self.kyrie()
        self.plan()

    # ------------------------------------------------------------------
    def forster(self):
        card = history_card(1540, r"Nuremberg: \ Georg Forster, \ a publisher, \ in a preface", r"`now that Josquin is dead, \ he is putting out more works than when he was alive'",
                            width=11.4, font_size=25).to_edge(UP, buff=0.5)
        rows_ = text_rows([
            (r"Josquin des Prez, \ about 1450--1521: \ the first composer made famous by printed music", WHITE),
            (r"printers sold music under his name, \ whether he wrote it or not", WHITE),
            (r"scholars have since doubted a large share of what once carried his name", EAR),
            (r"so: \ can the style itself say who wrote a piece?", TUNE),
        ], font_size=25).move_to(DOWN * 1.0)
        with self.voiceover(
            "Nuremberg, 1540. A music publisher, Georg Forster, writes in a preface that he remembers a distinguished "
            "man saying that Josquin, now that he is dead, is putting out more works than when he was alive. "
            "<bookmark mark='a'/> Josquin des Prez, who died in 1521, was the first composer whose fame was made by the "
            "printing press. <bookmark mark='b'/> Printers knew his name sold copies, and put it on music he had not "
            "written. <bookmark mark='c'/> Modern scholars have doubted a large share of the works that once carried his "
            "name. <bookmark mark='d'/> Which raises the question this part ends on: can the style of a piece, measured, "
            "say who wrote it?"
        ) as vo:
            self.play(FadeIn(card))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kyrie(self):
        d = load("hook")
        c = clip("hook.kyrie")
        vs = d["voices"]
        g = voices_roll(vs, width=11.6, height=3.8, colors=[TUNE, EAR, BLUE, "#A3E635", GREY_A, GREY_B], bar_h=0.1).move_to(DOWN * 0.35)
        head = label(rf"Palestrina, \ \textit{{{d['work']}}}, \ {d['title']}: \ the opening", font_size=24, color=GREY_A).to_edge(UP, buff=0.9)
        cap = label(rf"{d['n_voices']} voices, \ each entering with the same idea; \ sung by synthetic voices from a modern encoding", font_size=20, color=GREY_B).next_to(g, DOWN, buff=0.3)
        with self.voiceover(
            "First, the sound of the century. This is the opening of the Kyrie of Palestrina's most famous Mass, the "
            f"Missa Papae Marcelli, in {say(d['n_voices'])} voices, sung by the film's synthetic choir from a modern "
            "encoding. Listen to how every voice is equal: each takes up the same idea in turn, one note sung three "
            "times and then a leap up a fourth, and the sound is "
            "full of thirds and sixths, smooth and continuous, with almost every dissonance slipped in on a weak beat and "
            "taken away by step."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Palestrina, \ \textit{Missa Papae Marcelli}", detail=r"from the encoding, \ synthetic voices", kind="synthesized", corner=UL, tag_corner=UR)
            flash_voices(snd, g, vs, 0.0, d["quarter"], colors=[TUNE, EAR, BLUE, "#A3E635", GREY_A, GREY_B])
            cursor(snd, g, 0.0, d["quarter"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        head = label(r"Part 24: \ The Renaissance", font_size=36, color=TUNE).to_edge(UP, buff=0.5)
        steps = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"thirds and sixths become consonant; \ imitation becomes structure", WHITE),
            (r"the Mass three ways; \ Palestrina's style as rules, \ measured on 1,318 movements", WHITE),
            (r"printing, \ Josquin's name, \ and a statistical test of who wrote what", EAR),
            (r"the madrigal; \ Monteverdi's second practice, \ counted", WHITE),
            (r"Zarlino's triad, \ Vicentino's thirty-one tones, \ Gesualdo", WHITE),
            (r"attribution and \textit{musica ficta} by machine", TUNE))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "This part covers the fifteenth and sixteenth centuries. <bookmark mark='a'/> How thirds and sixths became "
            "consonant, and imitation became the way a piece is built. <bookmark mark='b'/> The Mass in three kinds, and "
            "Palestrina's style written as rules and measured on more than thirteen hundred of his Mass movements. "
            "<bookmark mark='c'/> Printing, Josquin's name, and a statistical test of who wrote what. "
            "<bookmark mark='d'/> The madrigal, and Monteverdi's second practice, which a critic attacked and the numbers "
            "confirm. <bookmark mark='e'/> Tuning and chromaticism at the edge of the system. <bookmark mark='f'/> And "
            "what machines can now say about authorship and about the accidentals no one wrote down."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            for mark, s in zip("bcdef", steps[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()
