from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403


class Florid(SoundScene):
    def construct(self):
        chapter(self, 4, r"Free and florid organum", r"How did the second voice break free?", extra=((1000, r"the Winchester Troper"),))
        self.free()
        self.florid()
        self.two_styles()

    # ------------------------------------------------------------------
    def free(self):
        items = [
            (r"about 1000: \ the Winchester Troper, \ some 170 two-voice organa", WHITE),
            (r"written in neumes without staff lines: \ we know their shapes, \ not their exact notes", GREY_A),
            (r"about 1026: \ Guido's \textit{Micrologus}: \ the organal voice may cross the chant", WHITE),
            (r"about 1100: \ \textit{Ad organum faciendum}: \ contrary motion preferred, \ the organal voice above", WHITE),
            (r"note against note, \ but now the two lines can move in opposite directions", TUNE),
        ]
        rows_scene(self, r"free organum", items,
                   "Within a century the rules loosened. <bookmark mark='b'/> Around the year 1000 the cathedral at "
                   "Winchester in England copied about a hundred and seventy organa for two voices into a book now called "
                   "the Winchester Troper, the largest early collection. <bookmark mark='c'/> They are written in neumes "
                   "without staff lines, so we know the shape of each line but not its exact notes, and every modern "
                   "performance is a reconstruction. <bookmark mark='d'/> Guido, in his Micrologus of about 1026, lets "
                   "the organal voice cross above the chant and approach the final from below. <bookmark mark='e'/> And "
                   "a treatise of about 1100, Ad organum faciendum, prefers contrary motion and puts the added voice "
                   "above the chant. <bookmark mark='f'/> Still one note against one note, but the two lines can now go "
                   "in opposite directions, which parallel organum never allowed.", marks="bcdef")

    # ------------------------------------------------------------------
    def florid(self):
        d = load("organum")["florid"]
        c = clip("organum.florid")
        up, ten = d["upper"], d["tenor"]
        g = voices_roll([up, ten], width=11.4, height=3.0, colors=[TUNE, GREY_A], bar_h=0.12).move_to(DOWN * 0.1)
        head = label(r"florid organum: \ many notes above each note of the chant \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"each melisma starts and ends on a fifth or an octave above the held note", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In the twelfth century, in the monasteries of Aquitaine in southern France and at the pilgrimage church of "
            "Santiago de Compostela, singers went further. The chant was slowed down to long held notes, and over each "
            "one the upper voice sang a whole flourish, a melisma of many notes, starting and ending on a perfect "
            "consonance. This is a short one, computed for the film: six chant notes, each under a flourish of four to "
            "eight notes."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"florid organum over six notes", detail=r"two synthetic voices", kind="synthesized", corner=UL, tag_corner=UR)
            flash_voices(snd, g, [up, ten], 0.0, d["unit"], colors=[TUNE, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_styles(self):
        left = VGroup(label(r"discant", font_size=30, color=TUNE),
                      label(r"note against note, \ or a few against one", font_size=20, color=GREY_A),
                      label(r"both voices move: \ they need a shared beat", font_size=20, color=WHITE)).arrange(DOWN, buff=0.25)
        right = VGroup(label(r"organum purum", font_size=30, color=BLUE),
                       label(r"a flourish over a held note", font_size=20, color=GREY_A),
                       label(r"only one voice moves: \ it can be free", font_size=20, color=WHITE)).arrange(DOWN, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=1.6).move_to(UP * 0.6)
        cap = VGroup(label(r"Codex Calixtinus, \ about 1160: \ \textit{Congaudeant catholici}, \ often called the first piece in three voices", font_size=21, color=GREY_A),
                     label(r"two styles, \ and a question: \ how do many voices keep together?", font_size=24, color=EAR)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"two ways to add a voice", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "So by about 1150 there were two ways to add a voice to chant. <bookmark mark='a'/> In discant, the voices move note against note, or a few notes against one, and since both move they must agree on a beat. <bookmark mark='b'/> In organum purum, pure organum, the chant holds and only the upper voice moves, allowing freer rhythm within stylistic and notational constraints. <bookmark mark='c'/> A book of music for the pilgrims at Santiago, the Codex Calixtinus, copied around 1160, contains a piece called Congaudeant catholici that is often discussed among the earliest three-voice examples, though how its voices were intended to combine is debated. <bookmark mark='d'/> Three voices moving at once is discant three times over, and it makes the question unavoidable: how do several moving voices keep together?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(FadeIn(left[1:]))
            vo.wait_until("b")
            self.play(FadeIn(right[1:]))
            vo.wait_until("c")
            self.play(FadeIn(cap[0]))
            vo.wait_until("d")
            self.play(FadeIn(cap[1]))
        self.wait(0.4)
        self.clear_scene()
