from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class FmIndex(VoiceoverScene):
    def construct(self):
        self.card()
        self.backward()
        self.measured()

    def card(self):
        card = chapter_card(9, r"Searching compressed text: \ the FM-index", r"Can we search a text we never "
                            r"decompress?", lit=(2000,), extra=((2000, r"Ferragina--Manzini"),), part=PART)
        with self.voiceover("Chapter nine. Searching compressed text: the FM-index."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def backward(self):
        d = load("fm")
        b = load("bwt")
        head = label(r"Backward search for \texttt{ana}", font_size=34).to_edge(UP, buff=0.3)
        rots = b["rotations"]
        rows = VGroup()
        for k, r in enumerate(rots):
            rows.add(VGroup(mono(str(k), 18, GREY_B), mono(r[0], 24, DATA), mono(r[1:-1], 24, GREY_D),
                            mono(r[-1], 24, YES)).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(LEFT * 3.8 + DOWN * 0.3)
        formula = MathTex(r"[lo, hi) \;\to\; [\,C[c] + \mathrm{rank}_c(L, lo),\ \ C[c] + \mathrm{rank}_c(L, hi)\,)",
                          font_size=30, color=LAM).next_to(head, DOWN, buff=0.35).shift(RIGHT * 1.6)
        notes = VGroup(
            label(r"$C[c]$: \ how many characters of the text are smaller than $c$", font_size=20, color=GREY_A),
            label(r"$\mathrm{rank}_c(L, i)$: \ how many $c$'s are in $L$ before row $i$", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(formula, DOWN, buff=0.3)
        trace = d["banana_trace"]
        steps = VGroup()
        for k, (c, lo, hi) in enumerate(trace):
            steps.add(label(rf"read \texttt{{{c}}} \ (pattern {'a' if k == 0 else 'na' if k == 1 else 'ana'}): \ rows "
                            rf"$[{lo}, {hi})$", font_size=21, color=HEAD))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(notes, DOWN, buff=0.4).align_to(notes, LEFT)
        res = label(r"two rows: \ \texttt{ana} occurs twice; \ two rank queries per character", font_size=22,
                    color=YES).next_to(steps, DOWN, buff=0.35).align_to(steps, LEFT)
        box = None
        with self.voiceover(
            "Paolo Ferragina and Giovanni Manzini saw in 2000 that the transform is itself an index. <bookmark "
            "mark='a'/> The sorted rows are the sorted suffixes of chapter seven, so all occurrences of a pattern "
            "are a block of consecutive rows. Find the block by reading the pattern backwards. <bookmark mark='b'/> "
            "Start with the last character, a: rows one to three begin with a. <bookmark mark='c'/> Which rows "
            "begin with n a? They are where the LF mapping sends those a rows whose last character is n, and two "
            "counts of n in the last column, before row one and before row four, say where they land: rows five and "
            "six. <bookmark mark='d'/> Once more for a n a: rows two and three. <bookmark mark='e'/> Two "
            "rows, two occurrences. Each character of the pattern costs two rank queries, whatever the length of "
            "the text."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows))
            vo.wait_until("a")
            self.play(FadeIn(formula), FadeIn(notes))
            for mk, (st, (c, lo, hi)) in zip("bcd", zip(steps, trace)):
                vo.wait_until(mk)
                nb = SurroundingRectangle(VGroup(*rows[lo:hi]), color=HEAD, buff=0.06)
                if box is None:
                    self.play(Create(nb), FadeIn(st))
                else:
                    self.play(Transform(box, nb), FadeIn(st))
                box = box or nb
            vo.wait_until("e")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("fm")
        head = label(r"The FM-index of the novels", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r["pattern"], words(r["count"]), f"{r['t_count'] * 1000:.2f} ms", f"{r['t_locate'] * 1000:.2f} ms"]
                for r in d["rows"]]
        tab = grid_table([r"pattern", r"count", r"counting", r"locating one"], rows, widths=[5.0, 1.8, 2.2, 2.4],
                         row_h=0.4, font_size=20, mono_cols=(0,), colors=[[DATA, YES, HEAD, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        notes = VGroup(
            label(r"locate: \ walk back with LF until a sampled suffix-array position \ (every 32nd)", font_size=20,
                  color=WHITE),
            label(rf"our teaching version keeps $L$ as plain bytes and rank counts every 64 rows: \ larger than the "
                  rf"text", font_size=20, color=NO),
            label(rf"real FM-indexes code $L$ with wavelet trees and entropy coding: \ near the compressed size \ "
                  rf"(here, \ bzip2 of $L$: \ {d['bz2_bwt'] / 1e6:.1f} MB of {d['n'] / 1e6:.0f} MB)", font_size=20,
                  color=YES),
            label(r"in practice: \ BWA and Bowtie align billions of DNA reads to the 3-gigabase human genome",
                  font_size=20, color=LAM),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here it is on the whole corpus. <bookmark mark='a'/> Counting any pattern takes a fraction of a "
            "millisecond, a couple of rank queries per character, whether the pattern occurs once or two hundred "
            "thousand times. To find where an occurrence is, walk back with the LF mapping until reaching a row "
            "whose suffix-array entry was kept; we kept every thirty-second. <bookmark mark='b'/> Our teaching "
            "version stores the transform as plain bytes with rank counts every sixty-four rows, which is larger "
            "than the text. <bookmark mark='c'/> Real FM-indexes store the transform compressed, with wavelet trees, "
            "close to the size of the compressed text: the transform of the novels compresses to seven megabytes. "
            "So the index is smaller than the book it searches. <bookmark mark='d'/> This is how DNA aligners like "
            "BWA and Bowtie map billions of short reads against the human genome."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
