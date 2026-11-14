from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403

SHORT = {"standard pattern (12)": r"standard \ (12)", "son clave (16)": r"son clave", "rumba clave (16)": r"rumba clave",
         "bossa nova (16)": r"bossa nova", "gahu (16)": r"gahu", "soli (12)": r"soli \ (12)", "tresillo (8)": r"tresillo \ (8)",
         "cinquillo (8)": r"cinquillo \ (8)", "soukous (16)": r"soukous", "shiko (16)": r"shiko"}


def yes(b):
    return r"yes" if b else r"--"


class Metrics(SoundScene):
    def construct(self):
        chapter(self, 2, r"Measuring timelines", r"Can a rhythm's quality be measured?")
        self.measures()
        self.table()
        self.offbeat()
        self.claves()
        self.central()
        self.limits()

    # ------------------------------------------------------------------
    def measures(self):
        items = [
            (r"\textbf{evenness}: \ how far the strokes lie from perfectly even spacing \ (0 = perfectly even)", WHITE),
            (r"\textbf{Euclidean}: \ whether Bjorklund's algorithm \ (Part 33) \ produces it, \ up to rotation", WHITE),
            (r"\textbf{oddity}: \ no two strokes cut the cycle into equal halves \ (Simha Arom, \ Central African music)", WHITE),
            (r"\textbf{off-beatness}: \ strokes on pulses that no regular polygon through the start can reach \ (Godfried Toussaint)", TUNE),
            (r"\textbf{centrality}: \ how close a rhythm lies, \ on average, \ to its relatives", GREY_A),
        ]
        rows_scene(self, r"five ways to measure a timeline", items,
                   "How might one measure a timeline? Here are five measures from the mathematical study of rhythm. "
                   "<bookmark mark='b'/> Evenness: how far the strokes lie from perfectly even spacing, zero meaning perfectly even. "
                   "<bookmark mark='c'/> Whether the rhythm is Euclidean: whether Bjorklund's algorithm from Part 33 produces it, "
                   "up to rotation. <bookmark mark='d'/> Oddity, a property the ethnomusicologist Simha Arom found throughout "
                   "Central African music: no two strokes cut the cycle into two equal halves. <bookmark mark='e'/> Off-beatness, "
                   "from the computer scientist Godfried Toussaint, counting strokes that fall on pulses no regular polygon "
                   "through the starting pulse can reach. <bookmark mark='f'/> And centrality: how close a rhythm lies, on "
                   "average, to its relatives.", marks="cdef")

    # ------------------------------------------------------------------
    def table(self):
        d = load("metrics")
        hdr = [r"timeline", r"pattern", r"from even", r"Euclidean", r"odd", r"off-beat"]
        rows_ = VGroup()
        for r in d["rows"]:
            rr = VGroup(label(SHORT[r["name"]], font_size=16, color=TUNE), grid_row(r["pattern"], cell=0.2, color=TUNE),
                        label(f"{r['uneven']:.2f}", font_size=16, color=WHITE), label(yes(r["euclidean"]), font_size=16, color=WHITE),
                        label(yes(r["oddity"]), font_size=16, color=WHITE), label(str(r["offbeat"]), font_size=16, color=EAR))
            rows_.add(rr)
        hrow = VGroup(*[label(h, font_size=17, color=GREY_A) for h in hdr])
        allrows = VGroup(hrow, *rows_)
        xs = [-6.0, -3.6, 0.4, 2.0, 3.6, 4.9]
        for k, r in enumerate(allrows):
            for j, cell in enumerate(r):
                if j in (0, 1):
                    cell.move_to([xs[j], 0, 0], aligned_edge=LEFT)
                else:
                    cell.move_to([xs[j] + 0.5, 0, 0])
                cell.set_y(2.55 - 0.5 * k)
        head = label(r"ten timelines, \ measured", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        allrows.shift(DOWN * 0.2)
        with self.voiceover(
            "Here are ten well-known timelines, measured by Monochord. <bookmark mark='a'/> The standard pattern and the soli "
            "pattern from Guinea in twelve pulses; six five-stroke patterns in sixteen: son clave and rumba clave from Cuba, "
            "the bossa nova from Brazil, gahu from Ghana, soukous from Congo, and shiko from Nigeria; and the tresillo and "
            "cinquillo in eight. <bookmark mark='b'/> Bossa nova is the most even of the sixteen-pulse patterns and is "
            "Euclidean; soukous is the least even. <bookmark mark='c'/> Son clave, rumba clave and bossa nova have the oddity "
            "property; the standard pattern does not, since its strokes on the sixth and twelfth pulses face each other across the cycle. "
            "<bookmark mark='d'/> And the standard pattern has the most off-beat strokes, three, as Toussaint observed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hrow))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.12), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(rows_[3][2]), Indicate(rows_[8][2]))
            vo.wait_until("c")
            self.play(*[Indicate(rows_[i][4]) for i in (0, 1, 2, 3)])
            vo.wait_until("d")
            self.play(Indicate(rows_[0][5], color=EAR))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def offbeat(self):
        d = load("metrics")
        r = 1.9
        circ = Circle(radius=r, color=DIM, stroke_width=1.5)
        pts = [r * np.array([np.cos(PI / 2 - k * TAU / 12), np.sin(PI / 2 - k * TAU / 12), 0]) for k in range(12)]
        ticks = VGroup(*[Dot(p, radius=0.06, color=GREY_B) for p in pts])
        nums = VGroup(*[label(str(k + 1), font_size=16, color=GREY_A).move_to(p * 1.17) for k, p in enumerate(pts)])
        polys = VGroup(Polygon(*[pts[k] for k in (0, 6)] + [pts[6]], color=GREY_B, stroke_width=1.5),
                       Polygon(*[pts[k] for k in (0, 4, 8)], color=BLUE, stroke_width=2),
                       Polygon(*[pts[k] for k in (0, 3, 6, 9)], color="#A3E635", stroke_width=2),
                       Polygon(*[pts[k] for k in (0, 2, 4, 6, 8, 10)], color=GREY_A, stroke_width=1.5))
        off = VGroup(*[Circle(radius=0.2, color=EAR, stroke_width=3).move_to(pts[k]) for k in d["offbeat12"]])
        on = [0, 2, 4, 5, 7, 9, 11]
        bell = VGroup(*[Dot(pts[k], radius=0.13, color=TUNE) for k in on])
        g = VGroup(circ, ticks, nums, polys, off, bell).move_to(LEFT * 3.0 + DOWN * 0.2)
        side = VGroup(label(r"regular polygons through pulse 1 \ reach every pulse except 2, \ 6, \ 8 and 12", font_size=19, color=WHITE),
                      label(r"those four are the \textit{off-beat} pulses: \ k with gcd(k, \ 12) = 1", font_size=19, color=EAR),
                      label(r"the standard pattern strikes three of them", font_size=19, color=TUNE),
                      label(r"a stroke there belongs to no beat grid \ in two, \ three, \ four or six", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.0)
        with self.voiceover(
            "Off-beatness deserves a picture. Place twelve pulses on a circle and draw every regular polygon that passes "
            "through the first pulse: <bookmark mark='a'/> the diameter, the triangle, the square, the hexagon. Those are the "
            "grids of two, three, four and six beats a cycle. <bookmark mark='b'/> They reach every pulse except four: the "
            "second, sixth, eighth and twelfth, which lie one, five, seven and eleven pulses after the start, numbers that "
            "share no factor with twelve. <bookmark mark='c'/> A "
            "stroke on one of those pulses belongs to none of the beat grids. The standard pattern strikes three of the four, "
            "which is part of why it feels as though it is always leaning against the beat, whichever beat you choose."
        ) as vo:
            self.play(FadeIn(circ), FadeIn(ticks), FadeIn(nums))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p) for p in polys], lag_ratio=0.4), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(off), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bell), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def claves(self):
        d = load("metrics")
        c = clip("metrics.claves")
        names = ["son clave (16)", "rumba clave (16)", "bossa nova (16)", "gahu (16)"]
        from explainer.music.monochord import timelines as TT
        rows_ = VGroup(*[pat_row(TT.TIMELINES[n], cell=0.4, color=VOICE_C[i], name=SHORT[n], size=20) for i, n in enumerate(names)]).arrange(DOWN, buff=0.35, aligned_edge=RIGHT).move_to(UP * 0.2)
        head = label(r"four five-stroke timelines in sixteen pulses", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Four of the sixteen-pulse patterns, heard on claves over a soft beat, two cycles each: son clave, rumba clave, "
            "which delays its third stroke by one pulse, bossa nova, which delays its last, and gahu, which pushes its last "
            "stroke later still. Listen to how much one moved stroke changes the feel."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"four timelines", detail=r"bar and membrane models", corner=DL, tag_corner=DR)
            for i, n in enumerate(names):
                flash_cells(snd, rows_[i].cells, TT.onsets(TT.TIMELINES[n]), d["starts"][n], d["pulse"], 2, 16, color=VOICE_C[i])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def central(self):
        d = load("metrics")
        from explainer.music.monochord import timelines as TT
        names = TT.CLAVES
        cent = d["centrality"]
        mx = max(cent.values())
        bars = VGroup()
        for i, n in enumerate(names):
            v = cent[n]
            b = Rectangle(width=5.0 * v / mx, height=0.38, stroke_width=0, fill_color=TUNE if n == d["most_central"] else BLUE, fill_opacity=0.85)
            row = VGroup(label(SHORT[n], font_size=19, color=WHITE), b, label(str(v), font_size=19, color=WHITE))
            bars.add(row)
        for i, row in enumerate(bars):
            row[0].move_to([-3.6, 1.6 - 0.62 * i, 0], aligned_edge=RIGHT)
            row[1].move_to([-3.3, 1.6 - 0.62 * i, 0], aligned_edge=LEFT)
            row[2].next_to(row[1], RIGHT, buff=0.15)
        pair = VGroup(pat_row(TT.TIMELINES["son clave (16)"], cell=0.32, name=r"son", size=17),
                      pat_row(TT.TIMELINES["rumba clave (16)"], cell=0.32, color=BLUE, name=r"rumba", size=17)).arrange(DOWN, buff=0.15, aligned_edge=RIGHT)
        pair.to_edge(DOWN, buff=1.0)
        pl = label(r"swap distance 1: \ one stroke moves one pulse", font_size=18, color=GREY_A).next_to(pair, DOWN, buff=0.2)
        head = label(r"total swap distance to the other five", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Now centrality. Toussaint asked why son clave, of all the five-stroke patterns, spread around the world. "
            "<bookmark mark='a'/> He measured the distance between two rhythms by the swap distance: the fewest swaps of a stroke "
            "with a neighbouring empty pulse that turn one into the other. Son and rumba clave are one swap apart. "
            "<bookmark mark='b'/> Add up each pattern's distances to the other five. Son clave's total is six, the smallest; "
            "bossa nova's is eight; the rest are ten or twelve. Son clave sits at the centre of its family, the pattern from "
            "which the others are fewest steps away. Toussaint called it the rhythm that conquered the world, and his "
            "suggestion is that a central rhythm is the easiest to vary."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pair), FadeIn(pl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in bars], lag_ratio=0.2), run_time=2.0)
            self.play(Indicate(bars[0]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"no single measure predicts which rhythms people choose", WHITE),
            (r"the measures were built by looking at rhythms already loved: \ a danger of circular reasoning", WHITE),
            (r"history, \ dance, \ language and instruments shape timelines at least as much as geometry", WHITE),
            (r"what the measures do well: \ give exact, \ testable descriptions to compare across musics", TUNE),
            (r"chapter 10 asks how rhythm is actually played and heard", GREY_A),
        ]
        rows_scene(self, r"what the measures cannot say", items,
                   "What can such measures not say? <bookmark mark='b'/> No single measure predicts which rhythms people choose. "
                   "<bookmark mark='c'/> And the measures were designed by looking at rhythms already loved, which risks circular "
                   "reasoning. <bookmark mark='d'/> History, dance, language and the instruments themselves shape timelines at "
                   "least as much as geometry does. <bookmark mark='e'/> What the measures do well is give exact, testable "
                   "descriptions that can be compared across musics. <bookmark mark='f'/> Chapter ten asks how rhythm is "
                   "actually played and heard.", marks="cdef")
