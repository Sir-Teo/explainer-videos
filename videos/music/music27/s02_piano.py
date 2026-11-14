from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403

OCT = {21: "A0", 24: "C1", 29: "F1", 36: "C2", 89: "F6", 96: "C7", 101: "F7", 105: "A7", 108: "C8"}


class Piano(SoundScene):
    def construct(self):
        chapter(self, 1, r"The piano grows", r"What could the new piano do?", extra=((1825, r"Babcock's iron frame"),))
        self.iron()
        self.compass()
        self.cs()
        self.spans()
        self.parlour()

    # ------------------------------------------------------------------
    def iron(self):
        items = [
            (r"1821: \ Sébastien Érard's double escapement: \ a key can repeat before it rises", WHITE),
            (r"1825: \ Alpheus Babcock \ (Boston) \ patents a cast-iron frame", WHITE),
            (r"heavier strings at higher tension: \ louder, \ longer, \ steadier in tune", WHITE),
            (r"felt hammers in place of leather: \ a rounder tone \ (Part 7: \ a softer hammer, \ fewer high partials)", TUNE),
            (r"1859: \ Steinway's grand, \ iron frame and crossed strings: \ the modern piano", GREY_A),
        ]
        rows_scene(self, r"iron, \ felt and steel", items,
                   "Between 1800 and 1870 the piano was rebuilt. <bookmark mark='b'/> In 1821 Sébastien Érard patented the "
                   "double escapement, which lets a key strike again before it has fully risen, so that fast repeated notes "
                   "became possible. <bookmark mark='c'/> In 1825 Alpheus Babcock in Boston patented a frame cast in one piece "
                   "of iron. <bookmark mark='d'/> An iron frame can hold heavier strings at far higher tension: a louder, longer "
                   "tone that stays in tune. <bookmark mark='e'/> Hammers were covered in felt instead of leather, for a "
                   "rounder tone; in Part 7's terms, a softer hammer excites fewer high partials. <bookmark mark='f'/> By "
                   "1859 Steinway in New York was building a grand with an iron frame and crossed strings, which is "
                   "essentially the modern piano.", marks="cdef")

    # ------------------------------------------------------------------
    def compass(self):
        d = load("keyboards")
        kb = d["keyboards"]
        lo, hi = 20, 110
        x0, W = -1.4, 7.4
        y0, dy = 1.9, 0.62
        rows_ = VGroup()
        for i, k in enumerate(kb):
            y = y0 - dy * i
            bar = Rectangle(width=W * (k["high"] - k["low"] + 1) / (hi - lo), height=0.32, stroke_width=0, fill_color=TUNE if i < 2 else BLUE, fill_opacity=0.85)
            bar.move_to([x0 + W * ((k["low"] + k["high"] + 1) / 2 - lo) / (hi - lo), y, 0])
            name = label(rf"{k['year']}: \ {k['name']}", font_size=17, color=GREY_A).next_to([x0, y, 0], LEFT, buff=0.25)
            keys = label(rf"{k['keys']} keys", font_size=16, color=WHITE).next_to(bar, RIGHT, buff=0.15)
            rows_.add(VGroup(bar, name, keys))
        axis = VGroup(*[VGroup(Line([x0 + W * (m - lo) / (hi - lo), y0 - dy * len(kb) + 0.25, 0], [x0 + W * (m - lo) / (hi - lo), y0 - dy * len(kb) + 0.1, 0], color=GREY_B, stroke_width=2),
                               label(n, font_size=15, color=GREY_B).move_to([x0 + W * (m - lo) / (hi - lo), y0 - dy * len(kb) - 0.12, 0]))
                        for m, n in ((21, "A0"), (36, "C2"), (60, "C4"), (84, "C6"), (108, "C8"))])
        head = label(r"the keyboard's compass, \ lowest key to highest", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The keyboard grew too. Each bar here runs from an instrument's lowest key to its highest, from the makers' own "
            "documented compasses. <bookmark mark='a'/> Cristofori's piano of about 1720 had four and a half octaves; the "
            "Viennese fortepiano that Mozart played, five. <bookmark mark='b'/> Beethoven's Broadwood of 1817 had six; a "
            "Viennese Graf of the 1820s, six and a half. <bookmark mark='c'/> By mid-century an Érard grand had seven, "
            "and by the 1880s Steinway had settled on eighty-eight keys, from A zero to C eight, where the piano has "
            "stayed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(rows_[0]))
            for mark, sl in zip("abc", (slice(1, 2), slice(2, 4), slice(4, 6))):
                vo.wait_until(mark)
                self.play(LaggedStart(*[FadeIn(r) for r in rows_[sl]], lag_ratio=0.3), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cs(self):
        d = load("keyboards")
        c = clip("keyboards.cs")
        lo, hi = 20, 110
        x0, W = -5.2, 10.4
        kb = VGroup(*[Rectangle(width=W / (hi - lo) * 0.9, height=1.1 if (m % 12) not in (1, 3, 6, 8, 10) else 0.7, stroke_width=0.5, stroke_color=GREY_B,
                                fill_color=WHITE if (m % 12) not in (1, 3, 6, 8, 10) else "#222", fill_opacity=0.6 if 29 <= m <= 89 else 0.12)
                      .move_to([x0 + W * (m - lo) / (hi - lo), 0.3 + (0.2 if (m % 12) in (1, 3, 6, 8, 10) else 0.0), 0]) for m in range(21, 109)])
        old = VGroup(*[Dot([x0 + W * (m - lo) / (hi - lo), -0.55, 0], radius=0.09, color=TUNE) for m in d["cs_old"]])
        new = VGroup(*[Dot([x0 + W * (m - lo) / (hi - lo), -0.55, 0], radius=0.09, color=BLUE) for m in d["cs_new"]])
        lab_old = label(r"the Cs of a 1780s fortepiano \ (F1 to F6)", font_size=21, color=TUNE).move_to(DOWN * 1.4 + LEFT * 2.6)
        lab_new = label(r"the Cs added by 1880", font_size=21, color=BLUE).move_to(DOWN * 1.4 + RIGHT * 3.2)
        head = label(r"88 keys: \ the bright band is what Mozart had", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Hear what was added. First every C that a fortepiano of the 1780s could play, from C two to C six. Then the Cs "
            "the century added at either end: a deep C one, and C seven and C eight at the top, which on Part 7's piano "
            "model, as on a real one, are short, bright and almost pitchless."
        ):
            self.play(FadeIn(head), FadeIn(kb), FadeIn(lab_old), FadeIn(lab_new), FadeIn(old), FadeIn(new))
        with self.listen(c) as snd:
            window(snd, r"every C, \ then the new ones", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, old, [d["starts"]["old"] + 1.25 * i for i in range(len(old))], hot=WHITE, base=TUNE)
            flash(snd, new, [d["starts"]["new"] + 1.75 * i for i in range(len(new))], hot=WHITE, base=BLUE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spans(self):
        d = load("keyboards")
        sp = d["spans"]
        lo, hi = 28, 104
        x0, W = -2.2, 7.4
        y0, dy = 2.0, 0.5
        rows_ = VGroup()
        for i, s in enumerate(sp):
            y = y0 - dy * i
            col = EAR if s["year"] > 1900 else (TUNE if s["high"] > 89 else GREY_A)
            bar = Line([x0 + W * (s["low"] - lo) / (hi - lo), y, 0], [x0 + W * (s["high"] - lo) / (hi - lo), y, 0], color=col, stroke_width=9)
            name = label(rf"{s['year']}: \ {s['composer']}", font_size=17, color=GREY_A).next_to([x0, y, 0], LEFT, buff=0.3)
            rows_.add(VGroup(bar, name))
        f6 = x0 + W * (89 - lo) / (hi - lo)
        lim = VGroup(DashedLine([f6, y0 + 0.35, 0], [f6, y0 - dy * len(sp) + 0.15, 0], color=GREY_B, stroke_width=2),
                     label(r"F6: \ the top of Mozart's fortepiano", font_size=17, color=GREY_B).move_to([f6 + 0.2, y0 + 0.6, 0]))
        cap = label(r"the lowest and highest note each keyboard piece in the Library uses", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Did the music use the new keys? Here is every keyboard piece in the film's Library, the pieces the music21 "
            "corpus holds with a date, each as a line from its lowest note to its highest. <bookmark mark='a'/> C. P. E. "
            "Bach's sonata of 1765 stays inside the old compass. <bookmark mark='b'/> Clara Wieck's four polonaises, "
            "published in 1831 when she was eleven, climb to D seven and E seven, high above the top of Mozart's "
            "instrument, while Chopin's mazurka, a dance, needs no more than the old range. <bookmark mark='c'/> Joplin's rag of 1899 and Schoenberg's pieces "
            "of 1911 take the whole of the middle. Nine pieces prove nothing on their own, but they point the same way as "
            "the instruments: the music filled the space it was given."
        ) as vo:
            self.play(FadeIn(lim), FadeIn(cap), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(Indicate(rows_[0], color=WHITE, scale_factor=1.04))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_[1:6]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_[6:]], lag_ratio=0.2), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parlour(self):
        items = [
            (r"by mid-century, \ a piano in every middle-class parlour that could afford one", WHITE),
            (r"sheet music as an industry: \ songs, \ dances, \ operas arranged for four hands", WHITE),
            (r"playing the piano: \ an accomplishment expected of daughters", WHITE),
            (r"the amateur is the market: \ much of the century's music is written for them", TUNE),
            (r"the gramophone will take this market away after 1900 \ (Part 60)", GREY_A),
        ]
        rows_scene(self, r"a piano in the parlour", items,
                   "The piano also moved into the home. <bookmark mark='b'/> By the middle of the century it stood in the "
                   "parlour of almost every middle-class household that could afford one, <bookmark mark='c'/> and publishing "
                   "sheet music became an industry: songs, dances, and whole operas arranged for piano four hands. "
                   "<bookmark mark='d'/> Playing was an accomplishment expected of daughters, <bookmark mark='e'/> and "
                   "these amateurs were the market: much of the century's piano music was written for them. "
                   "<bookmark mark='f'/> After 1900 the gramophone would take that market away, as Part 60 will tell.", marks="cdef")
