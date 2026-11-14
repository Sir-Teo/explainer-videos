from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.bell()
        self.answer()
        self.where()
        self.plan()

    # ------------------------------------------------------------------
    def bell(self):
        d = load("hook")
        c = clip("hook.bell")
        card = listen_card(r"An iron bell plays one short pattern, \ over and over. \ Clap or tap along. \ "
                           r"How many beats do you feel in each turn of the pattern?", width=10.4)
        with self.voiceover(
            "A question for your ears. An iron bell plays one short pattern, over and over. Clap or tap along with it, "
            "however feels natural. How many beats do you feel in each turn of the pattern?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        neck = necklace(d["pattern"], radius=1.6).move_to(LEFT * 3.2 + UP * 0.2)
        row = pat_row(d["pattern"], cell=0.42).move_to(RIGHT * 2.6 + UP * 0.2)
        cap = label(r"twelve pulses a turn; \ the bell strikes on seven", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        self.play(FadeOut(card), FadeIn(neck), FadeIn(row), FadeIn(cap))
        cyc = 12 * d["pulse"]
        with self.listen(c) as snd:
            window(snd, r"the bell, \ four turns", detail=r"an iron bell model", corner=DL, tag_corner=DR)
            hand(snd, neck, 0.0, cyc)
            flash_cells(snd, row.cells, d["onsets"], 0.0, d["pulse"], d["cycles"], 12)
        self.wait(0.3)
        self.play(FadeOut(cap))
        self.neck, self.row = neck, row

    # ------------------------------------------------------------------
    def answer(self):
        d = load("hook")
        neck, row = self.neck, self.row
        four = pat_row(["x" if i in d["four"] else "." for i in range(12)], cell=0.42, color=BLUE).next_to(row, DOWN, buff=0.35)
        six = pat_row(["x" if i in d["six"] else "." for i in range(12)], cell=0.42, color=EAR).next_to(row, DOWN, buff=0.35)
        lf = label(r"four beats", font_size=20, color=BLUE).next_to(four, LEFT, buff=0.3)
        ls = label(r"six beats", font_size=20, color=EAR).next_to(six, LEFT, buff=0.3)
        with self.voiceover(
            "There is no single right answer, and that is the point. Many listeners feel four beats in each turn, three "
            "pulses to a beat. Here is the bell with a drum on those four."
        ):
            self.play(FadeIn(four), FadeIn(lf))
        with self.listen(clip("hook.four")) as snd:
            window(snd, r"the bell, \ with four beats", detail=r"bell and membrane models", corner=DL, tag_corner=DR)
            hand(snd, neck, 0.0, 12 * d["pulse"])
            flash_cells(snd, row.cells, d["onsets"], 0.0, d["pulse"], d["cycles"], 12)
            flash_cells(snd, four.cells, d["four"], 0.0, d["pulse"], d["cycles"], 12, color=BLUE)
        with self.voiceover(
            "Others feel six beats, two pulses to a beat. Here is the same bell with a clap on those six. Listen to how the "
            "bell's strokes seem to change their meaning, though not one of them has moved."
        ):
            self.play(FadeOut(four), FadeOut(lf), FadeIn(six), FadeIn(ls))
        with self.listen(clip("hook.six")) as snd:
            window(snd, r"the bell, \ with six beats", detail=r"bell and noise models", corner=DL, tag_corner=DR)
            hand(snd, neck, 0.0, 12 * d["pulse"])
            flash_cells(snd, row.cells, d["onsets"], 0.0, d["pulse"], d["cycles"], 12)
            flash_cells(snd, six.cells, d["six"], 0.0, d["pulse"], d["cycles"], 12, color=EAR)
        ans = label(r"one pattern, \ felt in four or in six: \ in the music it comes from, \ both at once", font_size=22, color=TUNE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "In four, the bell seems to pull against the beat; in six, it seems to sit on it for a while and then slip "
            "away. In the music this pattern comes from, dancers' feet usually mark the four, while other parts of the "
            "ensemble stress the six, and the pattern lives in the tension between them."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def where(self):
        items = [
            (r"this bell pattern is heard in Ewe music of Ghana and Togo, \ in Yoruba music of Nigeria, \ and far beyond", WHITE),
            (r"it crossed the Atlantic with enslaved Africans: \ Cuban \textit{bemb\'e}, \ Brazilian \textit{candombl\'e}", WHITE),
            (r"musicologists call it the \textit{standard pattern}; \ Nketia called such patterns \textit{time lines}", WHITE),
            (r"written as steps of pulses it reads \ 2 2 1 2 2 2 1: \ the steps of the major scale", TUNE),
            (r"a scale turned into time, \ which chapter 1 explains", GREY_A),
        ]
        rows_scene(self, r"seven strokes in twelve pulses", items,
                   "This pattern of seven strokes in twelve pulses is one of the most widespread rhythms in the world. "
                   "<bookmark mark='b'/> It is heard in the music of the Ewe of Ghana and Togo, of the Yoruba of Nigeria, and "
                   "far beyond. <bookmark mark='c'/> It crossed the Atlantic with enslaved Africans, and is heard in Cuban "
                   "bembé and in Brazilian candomblé. <bookmark mark='d'/> Musicologists call it the standard "
                   "pattern; the Ghanaian scholar Kwabena Nketia called such patterns time lines. <bookmark mark='e'/> Written as "
                   "steps between strokes, it reads two, two, one, two, two, two, one. Those are the steps of the major scale. "
                   "<bookmark mark='f'/> A scale turned into time, which chapter one explains.", marks="cdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"the standard pattern, \ and why it is the major scale in time",
            r"measuring timelines: \ evenness, \ oddity, \ off-beatness, \ centrality",
            r"an Ewe ensemble, \ and three against two",
            r"hocket: \ one melody, \ many players",
            r"the mbira, \ and melodies nobody plays",
            r"the clave, \ samba, \ and call and response",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. The standard pattern, and why it is the major scale in time. <bookmark mark='b'/> How to "
            "measure a timeline: its evenness, its oddity, its off-beatness, and how central it sits among its relatives. "
            "<bookmark mark='c'/> An ensemble in the manner of the Ewe, and the idea of three against two. "
            "<bookmark mark='d'/> Hocket, one melody shared among many players. <bookmark mark='e'/> The mbira, and "
            "melodies that nobody plays but everybody hears. <bookmark mark='f'/> And the clave, samba, and call and "
            "response. Every part played is ours; the timelines are the well-known ones, as they are usually written down."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
