from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403


class Madrigal(SoundScene):
    def construct(self):
        chapter(self, 8, r"The madrigal and word painting", r"Can music say what the words say?", extra=((1539, r"Arcadelt's first book"),))
        self.history()
        self.opening()
        self.painting()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"from the 1530s, \ in Italy: \ settings of serious Italian poetry, \ Petrarch above all", WHITE),
            (r"for a few voices, \ one to a part, \ sung by amateurs and professionals at court", WHITE),
            (r"Arcadelt, \ Willaert, \ Rore, \ Marenzio, \ Gesualdo, \ Monteverdi: \ eighty years of experiment", WHITE),
            (r"1588: \ \textit{Musica transalpina} brings it to England: \ Morley, \ Weelkes, \ Wilbye", WHITE),
            (r"the words first: \ the music follows each image of the poem", TUNE),
        ]
        rows_scene(self, r"the madrigal", items,
                   "While the church perfected the Mass, the courts of Italy invented a secular form. "
                   "<bookmark mark='b'/> From the 1530s composers set serious Italian poetry, Petrarch above all, as "
                   "madrigals: <bookmark mark='c'/> pieces for four, five or six voices, one singer to a part, sung by "
                   "amateurs and by professional singers at court. <bookmark mark='d'/> Jacques Arcadelt and Adrian "
                   "Willaert, Cipriano de Rore, Luca Marenzio, Carlo Gesualdo and Claudio Monteverdi made it the "
                   "laboratory of the century. <bookmark mark='e'/> In 1588 a printed anthology, Musica transalpina, "
                   "carried it to England, where Thomas Morley, Thomas Weelkes and John Wilbye wrote in English. "
                   "<bookmark mark='f'/> Its principle was the opposite of the Mass's: the words come first, and the music "
                   "follows every image of the poem.", marks="bcdef")

    # ------------------------------------------------------------------
    def opening(self):
        d = load("madrigal")
        c = clip("madrigal.opening")
        vs = d["voices"]
        g = voices_roll(vs, width=11.4, height=3.4, colors=[TUNE, BLUE, EAR, "#A3E635", GREY_A], bar_h=0.11).move_to(DOWN * 0.3)
        head = label(r"Monteverdi, \ Book 3 \ (1592), \ the first madrigal: \ the opening", font_size=24, color=GREY_A).to_edge(UP, buff=0.9)
        cap = label(r"five voices, \ one to a part: \ chamber music for singers", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.3)
        with self.voiceover(
            "This is how a madrigal begins: the opening of the first piece in Monteverdi's third book, printed in 1592, "
            "for five voices, sung here on vowels by the synthetic choir. Compare it with the Mass: the voices pair off and "
            "answer each other, the rhythm follows the stresses of the Italian words, and the texture changes with every "
            "line of the poem."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Monteverdi, \ Book 3, \ no. 1", detail=r"from the encoding, \ synthetic voices", kind="synthesized", corner=UL, tag_corner=UR)
            flash_voices(snd, g, vs, 0.0, d["quarter"], colors=[TUNE, BLUE, EAR, "#A3E635", GREY_A])
            cursor(snd, g, 0.0, d["quarter"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def painting(self):
        ex = VGroup()
        for word, how, pts in ((r"`ascend', \ `heaven'", r"a rising line", [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]),
                               (r"`descend', \ `die'", r"a falling line, \ a final low note", [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)]),
                               (r"`sigh' \ (\textit{sospiro})", r"a note, \ a rest, \ a note", [(0, 2), (2, 2), (3, 1)]),
                               (r"`alone'", r"one voice by itself", [(0, 2), (1, 2), (2, 3)]),
                               (r"`pain', \ `cruel'", r"a harsh dissonance, \ a chromatic step", [(0, 2), (1, 2.5), (2, 1.5)])):
            dots = VGroup(*[RoundedRectangle(width=0.32, height=0.1, corner_radius=0.04, stroke_width=0, fill_color=TUNE, fill_opacity=1).move_to([0.42 * x, 0.18 * y, 0]) for x, y in pts])
            cell = VGroup(label(word, font_size=21, color=WHITE), dots, label(how, font_size=18, color=GREY_A)).arrange(DOWN, buff=0.22)
            ex.add(cell)
        ex.arrange(RIGHT, buff=0.55).move_to(UP * 0.4)
        ex.scale_to_fit_width(min(ex.width, 12.6))
        cap = VGroup(label(r"`madrigalisms': \ the image of a word drawn in sound", font_size=22, color=TUNE),
                     label(r"Thomas Morley's advice \ (1597): \ fit the music to the matter of the words", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        head = label(r"word painting", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The habit is called word painting. <bookmark mark='a'/> When the poem rises to heaven, the line rises; when "
            "it falls or dies, the line falls and ends low; a sigh is a note broken by a rest; a word meaning alone is "
            "sung by one voice; and pain, cruelty or bitterness are sung on a harsh dissonance or a chromatic step. "
            "<bookmark mark='b'/> Later centuries found the devices naive and called them madrigalisms. "
            "<bookmark mark='c'/> But Thomas Morley's handbook of 1597 states the principle plainly: a composer must "
            "fit the music to the matter of the words. And the harsh dissonance for a word of pain is where the "
            "rules of the last chapters began to break."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ex[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in ex[1:]], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(cap[0]))
            vo.wait_until("c")
            self.play(FadeIn(cap[1]))
        self.wait(0.4)
        self.clear_scene()
