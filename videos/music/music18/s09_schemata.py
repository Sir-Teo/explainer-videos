from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class Schemata(SoundScene):
    def construct(self):
        chapter(self, 8, r"Galant schemata", r"What were composers' building blocks?", extra=((2007, r"Gjerdingen's \textit{Music in the Galant Style}"),))
        self.idea()
        self.eight()

    # ------------------------------------------------------------------
    def idea(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"a schema: \ a bass and a melody, \ a few notes each, \ moving together", WHITE),
            (r"named by Gjerdingen from old treatises, \ places, \ and teachers: \ Romanesca, \ Prinner, \ Fonte, \ Monte", WHITE),
            (r"each with a place in a piece: \ openings, \ replies, \ after the double bar, \ before the end", WHITE),
            (r"learned by heart, \ like the phrases of a spoken language", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"galant schemata", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Robert Gjerdingen, reading the partimenti and the music of the galant style, the polite music of the "
            "mid-eighteenth century, found that composers built their phrases from a few dozen stock patterns. "
            "<bookmark mark='a'/> A schema is a short bass and a short melody that move together, a few notes "
            "each. <bookmark mark='b'/> Gjerdingen named them, some after old treatises and teachers: Joseph "
            "Riepel, writing in 1755, called three of them the Monte, the Fonte and the Ponte, the mountain, the "
            "fountain and the bridge. <bookmark mark='c'/> Each had its place: some open a piece, some answer an "
            "opening, some come after the double bar, some lead to the end. <bookmark mark='d'/> A composer "
            "learned them as a speaker learns the phrases of a language, and could improvise with them."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def eight(self):
        d = load("schemata")
        c = clip("schemata.eight")
        cells = VGroup()
        for k, name in enumerate(d["order"]):
            s = d["schemata"][name]
            g = chord_roll(s["chords"], width=2.6, height=1.25, lo=38, hi=82, thick=0.09)
            nm = label(name, font_size=26, color=TUNE)
            tx = label(s["text"], font_size=15, color=GREY_A)
            tx.scale_to_fit_width(min(tx.width, 3.0))
            cell = VGroup(nm, g, tx).arrange(DOWN, buff=0.15)
            cells.add(cell)
        cells.arrange_in_grid(rows=2, cols=4, buff=(0.45, 0.6)).move_to(DOWN * 0.15)
        with self.voiceover(
            "Here are eight of them, each realized in four voices in C major, the melody on top. Three that open "
            "a piece: the Do-Re-Mi, the Romanesca and the Meyer. The Prinner, which answers an opening, its melody "
            "falling six, five, four, three. The Fonte and the Monte, sequences that come after the double bar, "
            "one falling a step, one climbing. The Ponte, a bridge over a held dominant. And the Quiescenza, a "
            "settling after the end. Listen to each."
        ):
            self.play(LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.15), run_time=4.0)
        with self.listen(c) as snd:
            window(snd, r"eight schemata", detail=r"a plucked string", corner=DL, tag_corner=DR)
            names = d["order"]
            for k, name in enumerate(names):
                sing_chords(snd, cells[k][1], d["schemata"][name]["times"])
                end = d["starts"][names[k + 1]] - 0.4 if k + 1 < len(names) else c.duration
                pulse(snd, cells[k][0], d["starts"][name], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()
