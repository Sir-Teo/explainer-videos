from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403

SCALE = ["C", "D", "E", "F", "G", "A", "B"]


class Pattern(SoundScene):
    def construct(self):
        chapter(self, 1, r"The standard pattern", r"Why do a bell's strokes match the major scale?")
        self.steps()
        self.hear()
        self.rotations()
        self.modes()
        self.even()
        self.deep()
        self.caution()

    # ------------------------------------------------------------------
    def steps(self):
        d = load("scale")
        pat = STANDARD = "x.x.xx.x.x.x"
        row = pat_row(pat, cell=0.6).move_to(UP * 1.6)
        on = d["onsets"]
        arcs = VGroup()
        for k, st in enumerate(d["steps"]):
            a, b = on[k], (on[(k + 1) % 7] if k < 6 else 12)
            if b > 11:
                lab = label(str(st), font_size=24, color=TUNE).next_to(row.cells[a], UP, buff=0.25).shift(RIGHT * 0.3)
            else:
                mid = (row.cells[a].get_center() + row.cells[b].get_center()) / 2
                lab = label(str(st), font_size=24, color=TUNE).move_to(mid + UP * 0.6)
            arcs.add(lab)
        keys = VGroup()
        for i in range(13):
            black = i in (1, 3, 6, 8, 10)
            r = Rectangle(width=0.6, height=1.3 if not black else 0.8, stroke_color=GREY_B, stroke_width=1.2,
                          fill_color=GREY_D if black else WHITE, fill_opacity=0.25 if not black else 0.8)
            keys.add(r)
        keys.arrange(RIGHT, buff=0.0).match_x(row).move_to(DOWN * 1.1, coor_mask=np.array([0, 1, 0]))
        scale_pcs = [0, 2, 4, 5, 7, 9, 11, 12]
        dots = VGroup(*[Dot(keys[p].get_bottom() + UP * 0.25, radius=0.1, color=TUNE) for p in scale_pcs])
        names = VGroup(*[label(n, font_size=18, color=TUNE).next_to(keys[p], DOWN, buff=0.12) for n, p in zip(SCALE + ["C"], scale_pcs)])
        kl = label(r"the major scale: \ semitone steps \ 2 2 1 2 2 2 1", font_size=21, color=GREY_A).next_to(keys, DOWN, buff=0.55)
        rl = label(r"the bell: \ pulse steps \ 2 2 1 2 2 2 1", font_size=21, color=GREY_A).next_to(row, DOWN, buff=0.25)
        with self.voiceover(
            "Write the bell pattern as a row of twelve pulses, with a filled box wherever the bell strikes. "
            "<bookmark mark='a'/> Count the pulses from each stroke to the next: two, two, one, two, two, two, and one back "
            "round to the start. <bookmark mark='b'/> Now take a piano octave, twelve semitones, and mark the major scale, C D "
            "E F G A B. Count the semitones from each note to the next: two, two, one, two, two, two, one. The same seven "
            "numbers in the same order. A cycle of twelve pulses and a cycle of twelve semitones, each divided into seven "
            "steps of one and two, the ones as far apart as they can be."
        ) as vo:
            self.play(FadeIn(row))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a) for a in arcs], lag_ratio=0.3), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(keys), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.15), FadeIn(names), FadeIn(kl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("scale")
        c = clip("scale.three")
        row = pat_row("x.x.xx.x.x.x", cell=0.55, name=r"bell", size=20).move_to(UP * 1.2)
        notes = VGroup()
        for k in range(12):
            notes.add(label(SCALE[d["onsets"].index(k)] if k in d["onsets"] else "", font_size=20, color=BLUE))
        for k, n in enumerate(notes):
            n.next_to(row.cells[k], DOWN, buff=0.3)
        nl = label(r"scale", font_size=20, color=BLUE).next_to(notes, LEFT, buff=0.35).match_x(row[0])
        stage = VGroup(label(r"the bell", font_size=22, color=TUNE), label(r"the scale on its strokes", font_size=22, color=BLUE),
                       label(r"both", font_size=22, color=WHITE)).arrange(RIGHT, buff=0.9).to_edge(DOWN, buff=1.2)
        with self.voiceover(
            "Hear the correspondence. First the bell, twice round. Then the major scale on a marimba, one note on each of "
            "the bell's strokes, so the scale's steps of pitch become steps of time. Then both together."
        ):
            self.play(FadeIn(row), FadeIn(notes), FadeIn(nl), FadeIn(stage))
        with self.listen(c) as snd:
            window(snd, r"bell, \ scale, \ both", detail=r"bell and bar models", corner=DL, tag_corner=DR)
            st = d["starts"]
            flash_cells(snd, row.cells, d["onsets"], st["bell"], d["pulse"], 2, 12)
            flash_cells(snd, notes, d["onsets"], st["scale"], d["pulse"], 2, 12, color=BLUE)
            flash_cells(snd, row.cells, d["onsets"], st["both"], d["pulse"], 2, 12)
            flash_cells(snd, notes, d["onsets"], st["both"], d["pulse"], 2, 12, color=BLUE)
            ks = ["bell", "scale", "both"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, stage[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rotations(self):
        d = load("scale")
        rows_ = VGroup()
        for r in d["rotations"]:
            rr = VGroup(label(rf"from stroke {r['k'] + 1}", font_size=17, color=GREY_A),
                        grid_row(r["pattern"], cell=0.3, color=TUNE if r["k"] == 0 else BLUE),
                        label(" ".join(str(x) for x in r["steps"]), font_size=17, color=WHITE),
                        label(d["modes"][r["k"]], font_size=18, color=TUNE if r["k"] == 0 else BLUE)).arrange(RIGHT, buff=0.4)
            rows_.add(rr)
        rows_.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        for col in range(4):
            x = max(r[col].get_left()[0] for r in rows_)
            for r in rows_:
                r[col].shift(RIGHT * (x - r[col].get_left()[0]))
        rows_.move_to(DOWN * 0.15)
        head = label(r"start the pattern on each of its seven strokes", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Start the pattern on a different stroke and the steps rotate. <bookmark mark='a'/> Starting on the second stroke "
            "gives two, one, two, two, two, one, two: the steps of the Dorian mode, D to D on the white keys. On the third, "
            "Phrygian; the fourth, Lydian; and so on through all seven modes of Part 12. Each rotation of the timeline "
            "is a rotation of the scale. <bookmark mark='b'/> Several of these rotations are played as bell patterns in their "
            "own right, and musicians who share one pattern may still disagree about which stroke is the start."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_[1:]], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(rows_[1][3]), Indicate(rows_[5][3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modes(self):
        d = load("scale")
        c = clip("scale.modes")
        rots = d["rotations"]
        rows_ = VGroup(pat_row(rots[1]["pattern"], cell=0.5, color=BLUE, name=r"Dorian, \ on D", size=20),
                       pat_row(rots[5]["pattern"], cell=0.5, color=EAR, name=r"Aeolian, \ on A", size=20)).arrange(DOWN, buff=0.6, aligned_edge=RIGHT).move_to(UP * 0.2)
        head = label(r"two rotations, \ each with its mode", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Two rotations, heard. The pattern started on its second stroke, with the Dorian mode on D played on its strokes, "
            "and then started on its sixth stroke, with the Aeolian mode on A, the natural minor."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"Dorian, \ then Aeolian", detail=r"bell and bar models", corner=DL, tag_corner=DR)
            ms = d["mode_starts"]
            from explainer.music.monochord import timelines as TT
            flash_cells(snd, rows_[0].cells, TT.onsets(rots[1]["pattern"]), ms["Dorian"], d["pulse"], 2, 12, color=BLUE)
            flash_cells(snd, rows_[1].cells, TT.onsets(rots[5]["pattern"]), ms["Aeolian"], d["pulse"], 2, 12, color=EAR)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def even(self):
        items = [
            (r"both are \textit{maximally even}: \ seven points spread as evenly as twelve places allow \ (Part 33)", WHITE),
            (r"both are Euclidean: \ Bjorklund's algorithm gives E(7,12), \ a rotation of the pattern", WHITE),
            (r"Jeff Pressing \ (1983) \ and Jay Rahn \ (1996) \ traced such pitch--time likenesses across musics", WHITE),
            (r"evenness is a property shared by many of the world's favourite scales and timelines", TUNE),
            (r"chapter 2 measures it, \ and its rivals", GREY_A),
        ]
        rows_scene(self, r"why the likeness?", items,
                   "Why should a scale and a bell pattern agree? <bookmark mark='b'/> Because both solve the same problem: "
                   "spread seven points as evenly as twelve places allow, which Part 33 called maximal evenness. "
                   "<bookmark mark='c'/> Bjorklund's algorithm, run with seven and twelve, gives a rotation of this very "
                   "pattern. <bookmark mark='d'/> Jeff Pressing in 1983, and Jay Rahn in 1996, traced such likenesses between "
                   "pitch and time across many musics. <bookmark mark='e'/> Evenness is shared by many of the world's favourite "
                   "scales and timelines. <bookmark mark='f'/> Chapter two measures it, and its rivals.", marks="cdef")

    # ------------------------------------------------------------------
    def deep(self):
        d = load("scale")
        counts = [d["intervals"][str(k)] if str(k) in d["intervals"] else d["intervals"][k] for k in range(1, 7)]
        bars = VGroup()
        for k, c_ in enumerate(counts):
            b = Rectangle(width=0.7, height=0.45 * c_, stroke_width=0, fill_color=TUNE, fill_opacity=0.85)
            bars.add(VGroup(b, label(str(c_), font_size=20, color=WHITE), label(str(k + 1), font_size=20, color=GREY_A)))
        for k, g in enumerate(bars):
            g[0].move_to(RIGHT * (k * 1.05) + UP * (0.225 * counts[k]))
            g[1].next_to(g[0], UP, buff=0.1)
            g[2].move_to([g[0].get_center()[0], -0.35, 0])
        bars.move_to(DOWN * 0.2 + LEFT * 2.6)
        xl = label(r"distance between two strokes \ (pulses)", font_size=18, color=GREY_A).next_to(bars, DOWN, buff=0.3)
        side = VGroup(label(r"every distance occurs \ a different number of times", font_size=21, color=TUNE),
                      label(r"the diatonic scale's intervals: \ the same counts \ 2 5 4 3 6 1", font_size=19, color=WHITE),
                      label(r"a \textit{deep} set \ (Winograd, \ 1966): \ each distance has its own frequency", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.3)
        head = label(r"how often each distance occurs between two strokes", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is a subtler likeness. Take every pair of the bell's seven strokes, twenty-one pairs, and measure the distance between them around the cycle, from one to six pulses. <bookmark mark='a'/> Distance one occurs twice, two five times, three four times, four three times, five six times, and six once. Every distance occurs a different number of times. <bookmark mark='b'/> The major scale's intervals, counted the same way in semitones, have exactly the same counts: it has six fifths and only one tritone. A set with this property is called deep, after Terry Winograd's 1966 study of such scales. Each distance has a different count, an exact combinatorial property. These rotation-invariant counts do not by themselves locate the downbeat or demonstrate how listeners orient in the cycle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*[g[2] for g in bars])), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(g[0], DOWN) for g in bars], lag_ratio=0.2), LaggedStart(*[FadeIn(g[1]) for g in bars], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in side], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def caution(self):
        items = [
            (r"a likeness of structure is not a likeness of meaning", WHITE),
            (r"Ewe musicians learn the bell by syllables and dance, \ not as a scale", WHITE),
            (r"Kofi Agawu warns against hearing African rhythm only through European theory", WHITE),
            (r"the mathematics says what the pattern shares with others, \ not what it is for", TUNE),
            (r"chapter 3 puts the bell back in its ensemble", GREY_A),
        ]
        rows_scene(self, r"a caution", items,
                   "A caution before we go further. <bookmark mark='b'/> A likeness of structure is not a likeness of meaning. "
                   "<bookmark mark='c'/> Ewe musicians learn the bell by its syllables and by the dance, not as a scale. "
                   "<bookmark mark='d'/> The Ghanaian theorist Kofi Agawu has warned against hearing African rhythm only through "
                   "European theory, and against treating it as exotic. <bookmark mark='e'/> The mathematics says what this "
                   "pattern shares with others, not what it is for. <bookmark mark='f'/> Chapter three puts the bell back in its "
                   "ensemble.", marks="cdef")
