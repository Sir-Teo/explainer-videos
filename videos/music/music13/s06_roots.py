from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403

NAMES12 = ["C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]


class Roots(SoundScene):
    def construct(self):
        chapter(self, 5, r"Where the root comes from", r"Why should a chord have a root at all?", lit=(1701,), extra=((1988, r"Parncutt's model of the root"),))
        self.series()
        self.model()
        self.ambiguous()
        self.others()
        self.ear()

    # ------------------------------------------------------------------
    def series(self):
        d = load("roots")
        c = clip("roots.missing")
        ev = c.events
        f0 = d["f0"]
        rows = partial_rows([f0], [r"C"], n=8, width=11.0, f_lo=100.0, f_hi=1200.0, row=0.5, colors=(GREY_B,), tick=0.45, font_size=30).move_to(UP * 0.6)
        ticks = rows.rows[0].ticks
        nums = VGroup(*[label(str(h + 1), font_size=24, color=GREY_B).next_to(ticks[h], UP, buff=0.12) for h in range(8)])
        nm = VGroup(*[label(t, font_size=30, color=MAJOR_C).next_to(ticks[h], DOWN, buff=0.2) for h, t in ((3, "C"), (4, "E"), (5, "G"))])
        low = label(r"131 Hz: \ not played", font_size=24, color=EAR).next_to(ticks[0], DOWN, buff=0.2)
        head = label(r"a major triad is harmonics 4, \ 5 and 6 of a note two octaves below its root", font_size=28, color=GREY_A).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Rameau wanted a physical reason for the root, and after reading about Sauveur's harmonics "
            "he found one. A single low C already contains, as its fourth, fifth and sixth harmonics, a "
            "C, an E and a G. <bookmark mark='a'/> So a major triad is a slice of one harmonic series; "
            "and Part 4 showed what the ear does with a slice of a harmonic series. It supplies the "
            "missing fundamental. <bookmark mark='b'/> Here are three pure tones, at four, five and six "
            "times 131 hertz. Then a tone at 131 hertz itself. Then all of them together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows), FadeIn(nums))
            vo.wait_until("a")
            self.play(*[ticks[h].animate.set_color(MAJOR_C) for h in (3, 4, 5)], FadeIn(nm))
            vo.wait_until("b")
            self.play(ticks[0].animate.set_color(EAR), FadeIn(low))
        tags = VGroup(*[label(t, font_size=28, color=GREY_A) for t in (r"the three tones", r"the low tone", r"together")]).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"a chord, \ and its fundamental", kind="synthesized", detail=r"pure tones; \ then an organ tone at 131 Hz", corner=DL, tag_corner=DR)
            pulse(snd, tags[0], ev["chord"], ev["low"] - 0.3, buff=0.12)
            pulse(snd, tags[1], ev["low"], ev["both"] - 0.3, buff=0.12)
            pulse(snd, tags[2], ev["both"], c.duration, buff=0.12)
            pulse(snd, nm, ev["chord"], ev["low"] - 0.3, buff=0.15)
            pulse(snd, low, ev["low"], ev["both"] - 0.3, buff=0.1)
        cap = label(r"Rameau: \ \textit{le corps sonore}, \ the sounding body", font_size=30, color=TUNE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The low C fits under the chord as if it had been there all along. In a sense it had. Rameau "
            "called this the sounding body: the major triad is the resonance of its own root, and the "
            "root is the note of which the others are harmonics."
        ):
            self.play(FadeOut(tags), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def model(self):
        d = load("roots")
        t = d["table"]
        w = VGroup(*[VGroup(label(a, font_size=26, color=WHITE), label(b, font_size=30, color=TUNE)).arrange(DOWN, buff=0.12) for a, b in
                     ((r"itself", "10"), (r"a fifth below", "5"), (r"a major third below", "3"), (r"a minor seventh below", "2"), (r"a major second below", "1"))]).arrange(RIGHT, buff=0.55).to_edge(UP, buff=0.55)
        cap = label(r"each note of a chord votes for the roots it could be a harmonic of", font_size=26, color=GREY_A).next_to(w, DOWN, buff=0.3)
        major = note_bars(t[0]["saliences"], NAMES12, width=5.6, height=1.9, color=WEAK, hot=(0,), hot_color=MAJOR_C, top=20).move_to(LEFT * 3.3 + DOWN * 1.9)
        minor = note_bars(t[1]["saliences"], NAMES12, width=5.6, height=1.9, color=WEAK, hot=(0, 3), hot_color=MINOR_C, top=20).move_to(RIGHT * 3.3 + DOWN * 1.9)
        mh = label(r"C, \ E, \ G", font_size=28, color=MAJOR_C).next_to(major, UP, buff=0.25)
        nh = label(r"C, \ E$\flat$, \ G", font_size=28, color=MINOR_C).next_to(minor, UP, buff=0.25)
        with self.voiceover(
            "A modern version of the idea is Richard Parncutt's model of the root, from 1988, building "
            "on Ernst Terhardt. Each note of a chord votes for the roots it could be a harmonic of. "
            "<bookmark mark='a'/> Itself, most strongly. Then the note a fifth below it; then a major "
            "third below; then, weakly, a minor seventh and a major second below. Those are the places "
            "of harmonics one, three, five, seven and nine. Add up the votes for each of the twelve "
            "notes. <bookmark mark='b'/> For C, E, G, the note C collects eighteen. Nothing else comes "
            "near."
        ) as vo:
            self.play(FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in w], lag_ratio=0.5), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(major), FadeIn(mh))
        with self.voiceover(
            "For the minor triad, C, E flat, G, the root is still C, with fifteen votes. "
            "<bookmark mark='a'/> But E flat is close behind, with thirteen: the G above it is its major "
            "third, and votes for it. The minor triad has a root, a slightly less certain one. That is "
            "the asymmetry we saw in Zarlino's numbers, and it may be part of why minor sounds less "
            "settled than major."
        ) as vo:
            self.play(FadeIn(minor), FadeIn(nh))
            vo.wait_until("a")
            self.play(Indicate(minor.bars[3], color=MINOR_C), Indicate(minor.names[3], color=MINOR_C))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ambiguous(self):
        d = load("roots")
        t = d["table"]
        c = clip("roots.dim")
        row = chord_row([["B4", "D5", "F5"]], width=3.0, space=0.24, above=[r"B, \ D, \ F"], font_size=30, above_color=DIM_C).move_to(LEFT * 4.2 + UP * 1.0)
        card = pause_card(r"The triad on the seventh degree. \ Which note will the model choose as its root?", width=6.2).move_to(RIGHT * 2.2 + UP * 1.0)
        with self.voiceover(
            "Now a harder one. The triad on the seventh degree of the scale: B, D, F. Before I show you, "
            "which note do you think the model picks as the root?"
        ):
            self.play(FadeIn(row), FadeIn(card))
        self.wait(2.0)
        bars = note_bars(t[2]["saliences"], NAMES12, width=7.5, height=1.7, color=WEAK, hot=(2, 5, 7, 11), hot_color=DIM_C, top=20).move_to(RIGHT * 2.2 + DOWN * 0.2)
        with self.voiceover(
            "It cannot decide. B, D and F tie, with ten votes each. <bookmark mark='a'/> And so does G: "
            "a note that is not in the chord at all. Play it, and you may hear why. Add a G underneath, "
            "and nothing sounds added. Then let it go where it wants."
        ) as vo:
            self.play(FadeOut(card), FadeIn(bars))
            vo.wait_until("a")
            self.play(Indicate(bars.bars[7], color=TUNE, scale_factor=1.3), Indicate(bars.names[7], color=TUNE, scale_factor=1.6))
        kb = keys(41, 72, width=9.0, height=1.4).to_edge(DOWN, buff=1.25)
        self.play(FadeIn(kb))
        with self.listen(c) as snd:
            window(snd, r"B, D, F; \ with a G below; \ and on", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, [[59, 62, 65], [43, 59, 62, 65], [48, 60, 64]], d["dim_times"], end=c.duration, colors=[DIM_C, GOLD, MAJOR_C])
        kb.clear()
        cap = label(r"the diminished triad: \ a seventh chord with its root left out", font_size=28, color=TUNE).next_to(kb, DOWN, buff=0.3)
        with self.voiceover(
            "The chord turned out to be the top of a seventh chord on G all along. That is why many "
            "theorists, Rameau among them, treat the diminished triad as a dominant seventh with its "
            "root left out: a chord whose root is somewhere else."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def others(self):
        d = load("roots")
        t = {r["label"]: r for r in d["table"]}
        rows = [(r"C, \ E, \ G", r"C", t["C major"]), (r"C, \ E$\flat$, \ G", r"C; \ then E$\flat$", t["C minor"]), (r"C, \ F, \ G", r"F; \ then C", t["C suspended"]),
                (r"A, \ C, \ E, \ G", r"C; \ then A", t["A minor seventh"]), (r"C, \ E, \ G$\sharp$", r"a tie of three", t["C augmented"]),
                (r"B, \ D, \ F, \ A$\flat$", r"a tie of eight", t["diminished seventh"])]
        head = VGroup(label(r"the chord", font_size=24, color=GREY_B), label(r"the model's root", font_size=24, color=GREY_B), label(r"ambiguity", font_size=24, color=GREY_B))
        xs = (-4.2, -0.4, 3.6)
        for h, x in zip(head, xs):
            h.move_to([x, 2.6, 0])
        table = VGroup()
        for k, (notes, rt, r) in enumerate(rows):
            y = 1.85 - 0.72 * k
            bar = Rectangle(width=2.2 * (r["ambiguity"] - 1.5) / 1.5, height=0.3, stroke_width=0, fill_color=TUNE if k < 2 else EAR, fill_opacity=0.85)
            bar.move_to([xs[2] - 0.6, y, 0], aligned_edge=LEFT)
            table.add(VGroup(label(notes, font_size=30, color=WHITE).move_to([xs[0], y, 0]), label(rt, font_size=28, color=GREY_A).move_to([xs[1], y, 0]),
                             bar, label(f"{r['ambiguity']:.2f}", font_size=24, color=WHITE).next_to(bar, RIGHT, buff=0.15)))
        with self.voiceover(
            "Run the model on other chords, and it sorts the solid ones from the ambiguous. The major "
            "and minor triads at the top. <bookmark mark='a'/> The suspended chord, C, F, G: the model "
            "hears F as the root, just ahead of C. <bookmark mark='b'/> A, C, E, G, which a lead sheet "
            "calls A minor seventh: the model prefers C, by a single vote. The same four notes are a C "
            "chord with a sixth added. <bookmark mark='c'/> The augmented triad: a three-way tie, every "
            "note as good a root as the others. And the diminished seventh, four notes a minor third "
            "apart: an eight-way tie. Composers use exactly these chords when they want the listener "
            "not to know where the music is going."
        ) as vo:
            self.play(FadeIn(head), FadeIn(table[0]), FadeIn(table[1]))
            vo.wait_until("a")
            self.play(FadeIn(table[2]))
            vo.wait_until("b")
            self.play(FadeIn(table[3]))
            vo.wait_until("c")
            self.play(FadeIn(table[4]))
            self.play(FadeIn(table[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ear(self):
        d = load("roots")
        e = d["ear"]
        cols = VGroup()
        for k, r in enumerate(e):
            col = KIND_COLOR[r["kind"]]
            h = 3.0 * r["strength"] / 0.5
            bar = Rectangle(width=1.1, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9)
            bar.move_to([(k - 1.5) * 2.4, -1.6 + h / 2, 0])
            heard = (rf"C, \ {r['octaves_below']:.0f} octave{'s' if r['octaves_below'] > 1.5 else ''} below" if k < 2 else r"nothing clear")
            cols.add(VGroup(bar, label(f"{r['strength']:.2f}", font_size=26, color=WHITE).next_to(bar, UP, buff=0.12),
                            label(r["kind"], font_size=26, color=col).next_to(bar, DOWN, buff=0.18), label(heard, font_size=22, color=GREY_A).next_to(bar, DOWN, buff=0.62)))
        head = label(r"Part 4's ear model, \ given each triad as sound: \ how strongly it hears one pitch", font_size=28, color=GREY_A).to_edge(UP, buff=0.55)
        with self.voiceover(
            "Parncutt's model works on note names. Part 4's ear model works on sound, and it agrees. "
            "<bookmark mark='a'/> Give it a major triad on middle C, and the strongest pitch it finds is "
            "the C two octaves below. <bookmark mark='b'/> Give it the minor triad, and it finds a C one "
            "octave below, a little more weakly. <bookmark mark='c'/> For the diminished and augmented "
            "triads it finds nothing convincing. So a root is not a convention of notation. It is the "
            "single pitch that your hearing assigns to a chord as a whole, when it can."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(cols[2]), FadeIn(cols[3]))
        self.wait(0.4)
        self.clear_scene()
