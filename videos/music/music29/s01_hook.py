from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.planet()
        self.op19()
        self.plan()

    # ------------------------------------------------------------------
    def planet(self):
        card = history_card(1908, r"Vienna: \ Arnold Schoenberg's Second String Quartet, \ Op. 10", r"a soprano enters the last two movements: \ `I feel the air of another planet'",
                            width=11.4, font_size=25).to_edge(UP, buff=0.5)
        rows_ = text_rows([
            (r"the words are Stefan George's; \ the music leaves its key behind as she sings them", WHITE),
            (r"the first performance, \ December 1908, \ was met with laughter and catcalls", WHITE),
            (r"for fifteen years Schoenberg wrote without keys, \ and then looked for a law to replace them", TUNE),
            (r"the law, \ and the mathematics later found under it, \ are this part", EAR),
        ], font_size=25).move_to(DOWN * 0.9)
        with self.voiceover(
            "Vienna, 1908. In the last two movements of Arnold Schoenberg's Second String Quartet a soprano joins the four "
            "strings, singing a poem by Stefan George that begins: I feel the air of another planet. <bookmark mark='a'/> As "
            "she sings it, the music leaves its key behind. <bookmark mark='b'/> At the first performance, that December, "
            "parts of the audience laughed and jeered. <bookmark mark='c'/> For more than a decade Schoenberg wrote without "
            "keys, and then looked for a rule to take their place. <bookmark mark='d'/> That rule, and the mathematics that "
            "theorists later found underneath it, are this part."
        ) as vo:
            self.play(FadeIn(card))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def op19(self):
        d = load("hook")
        c = clip("hook.op19no6")
        g = mroll(d["notes"], width=11.4, height=3.6, lo=min(n[0] for n in d["notes"]) - 1, hi=max(n[0] for n in d["notes"]) + 1, color=TUNE, bar_h=0.1).move_to(DOWN * 0.2)
        head = label(r"Schoenberg, \ Six Little Piano Pieces, \ Op. 19 No. 6 \ (1911), \ whole", font_size=25, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"nine bars, \ very slow: \ two chords, \ like bells, \ and a few quiet notes", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.35)
        with self.voiceover(
            "Here is what music without a key sounded like three years later. The last of Schoenberg's Six Little Piano "
            "Pieces, written in 1911, whole: nine very slow bars, read from the encoding and played on Part 7's piano. "
            "Two soft chords sound like distant bells, and a few quiet notes move above and below them. There is no tonic "
            "to arrive at, and nothing resolves; the piece simply stops."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Op. 19 No. 6", detail=r"from the encoding, \ Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in d["notes"]], hot=WHITE, base=TUNE)
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"free atonality: \ what Schoenberg's piano pieces are made of",
            r"pitch-class sets: \ prime forms, \ interval vectors, \ 224 classes counted two ways",
            r"Z-related sets and the hexachord theorem, \ proved",
            r"the row: \ forty-eight forms; \ Webern's canon in inversion, \ heard",
            r"all-interval rows, \ combinatoriality, \ total serialism",
            r"can anyone hear it? \ the evidence, \ and a question for your ears",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. First, what free atonality is made of. <bookmark mark='b'/> Then the theory built to "
            "describe it: sets of pitch classes, their names and interval vectors, and all two hundred and twenty-four of "
            "them, counted two ways. <bookmark mark='c'/> A theorem about hexachords, proved. <bookmark mark='d'/> "
            "Schoenberg's row and its forty-eight forms, and a canon by Webern in which one line is the other upside down. "
            "<bookmark mark='e'/> All-interval rows, combinatoriality and total serialism. <bookmark mark='f'/> And the "
            "question that hangs over all of it: can anyone hear it?"
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
