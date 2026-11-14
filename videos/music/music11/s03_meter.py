from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403


class Meter(SoundScene):
    def construct(self):
        chapter(self, 2, r"Meter", r"What does a time signature count?", extra=((1983, r"Lerdahl and Jackendoff's grid"),))
        self.levels()
        self.signatures()
        self.finder()

    # ------------------------------------------------------------------
    def levels(self):
        d = load("meter")
        g = dot_grid(d["four"], width=11.0, row=0.42, radius=0.09).move_to(DOWN * 0.6)
        names = [r"sixteenths", r"eighths", r"quarters: \ the beat", r"half bars", r"the bar"]
        tags = VGroup(*[label(t, font_size=24, color=GREY_A).move_to([g.get_left()[0] - 0.2, g.cols[0][k].get_y(), 0], aligned_edge=RIGHT) for k, t in enumerate(names)])
        VGroup(g, tags).shift(RIGHT * 0.9)
        counts = VGroup(*[label(str(w), font_size=24, color=TUNE if w == 5 else GREY_B).next_to(col, DOWN, buff=0.2) for w, col in zip(d["four"], g.cols)])
        head = label(r"one bar of four-four", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "A beat alone is only a pulse. Meter is several pulses at once, one inside another. Take one "
            "bar of four-four time. <bookmark mark='a'/> The fastest pulse here is sixteen to the bar. "
            "<bookmark mark='b'/> Every second one of those is an eighth. <bookmark mark='c'/> Every "
            "second eighth is a quarter, and that is the level we tap: the beat. <bookmark mark='d'/> "
            "Above it the half bar, and the bar itself. <bookmark mark='e'/> Now read down each column "
            "and count the dots. The more levels a moment belongs to, the stronger it is. The first "
            "moment of the bar belongs to all five: the downbeat. The middle of the bar has four. The "
            "moments between the eighths have one. This picture is from a book of 1983 by a composer and "
            "a linguist, Lerdahl and Jackendoff, and we will use it for the rest of this part."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(col[0]) for col in g.cols], FadeIn(tags[0]))
            for k, mark in enumerate("abcde"):
                vo.wait_until(mark)
                if k == 3:
                    self.play(*[FadeIn(col[3]) for col in g.cols if len(col) > 3], FadeIn(tags[3]), run_time=0.6)
                    self.play(*[FadeIn(col[4]) for col in g.cols if len(col) > 4], FadeIn(tags[4]), run_time=0.6)
                elif k == 4:
                    self.play(LaggedStart(*[FadeIn(x) for x in counts], lag_ratio=0.05), run_time=1.5)
                elif k == 0:
                    self.play(LaggedStart(*[Indicate(col[0], color=TUNE, scale_factor=1.6) for col in g.cols], lag_ratio=0.08), run_time=2.0)
                else:
                    self.play(*[FadeIn(col[k]) for col in g.cols if len(col) > k], FadeIn(tags[k]), run_time=0.7)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def signatures(self):
        d = load("meter")
        a = dot_grid(d["three_four"], width=4.6, row=0.42, radius=0.1)
        b = dot_grid(d["six_eight"], width=4.6, row=0.42, radius=0.1)
        ta = VGroup(MathTex(r"\tfrac{3}{4}", font_size=64), label(r"three beats, \ each of two eighths", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.4)
        tb = VGroup(MathTex(r"\tfrac{6}{8}", font_size=64), label(r"two beats, \ each of three eighths", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.4)
        left = VGroup(ta, a).arrange(DOWN, buff=0.7).move_to(LEFT * 3.4)
        right = VGroup(tb, b).arrange(DOWN, buff=0.7).move_to(RIGHT * 3.4)
        ba = group_brackets(a.xs + a.get_center()[0] * 0, (2, 2, 2), a.get_bottom()[1] - 0.3, a.pitch)
        bb = group_brackets(b.xs, (3, 3), b.get_bottom()[1] - 0.3, b.pitch)
        ba.shift(RIGHT * (a.cols[0].get_x() - a.xs[0]))
        bb.shift(RIGHT * (b.cols[0].get_x() - b.xs[0]))
        same = label(r"the same six eighth notes; \ a different metre", font_size=30, color=TUNE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "A time signature names such a nesting. Its lower number says which note value is counted, "
            "and its upper number how many. <bookmark mark='a'/> Three-four: three quarter notes to the "
            "bar, each one two eighths. <bookmark mark='b'/> Six-eight: six eighths to the bar, but "
            "grouped in threes, so that there are two beats, each a dotted quarter. "
            "<bookmark mark='c'/> Both bars hold the same six eighth notes. What differs is where the "
            "dots stack up. Hold on to this pair; in chapter six, music will switch between them."
        ) as vo:
            a.set_opacity(0.35)
            b.set_opacity(0.35)
            self.play(FadeIn(ta[0]), FadeIn(tb[0]), FadeIn(a), FadeIn(b))
            vo.wait_until("a")
            self.play(FadeIn(ta[1]), a.animate.set_opacity(1.0), FadeIn(ba))
            vo.wait_until("b")
            self.play(FadeIn(tb[1]), b.animate.set_opacity(1.0), FadeIn(bb))
            vo.wait_until("c")
            self.play(FadeIn(same))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def finder(self):
        d = load("meter")
        c = clip("meter.tap")
        g = axes([np.log10(0.2), np.log10(2.4)], [0, 1.1], x_length=10.0, y_length=2.6, xlabel=r"time between beats of the grid (seconds)", ylabel=r"score",
                 xticks=[np.log10(v) for v in (0.25, 0.5, 1.0, 2.0)], yticks=[], xfmt=lambda v: f"{10 ** v:g}", font_size=22).move_to(UP * 1.2)
        cv = curve_from(g, np.log10(np.asarray(d["periods"])), d["scores"], TUNE)
        peak = Dot(g.ax.c2p(np.log10(d["period"]), 1.0), radius=0.09, color=WHITE)
        pk = label(rf"{d['period']:.2f} s: \ {d['bpm']:.0f} to the minute", font_size=26, color=WHITE).next_to(peak, UP, buff=0.15)
        rule = label(r"score \ = \ share of the notes on the grid \ $\times$ \ share of the grid with a note \ $\times$ \ how natural that speed is", font_size=24, color=GREY_A).next_to(g, DOWN, buff=0.35)
        first = ticks(d["notes"], 0.0, max(d["notes"]) + 1.1, width=10.0, height=0.5, color=TUNE).move_to(DOWN * 2.0)
        lf = label(r"all the machine is given: \ the moments when the notes begin", font_size=24, color=GREY_A).next_to(first, DOWN, buff=0.3)
        with self.voiceover(
            "So where does a listener's beat come from? Nobody knows in full, but here is a toy that does "
            "something like it. Give Monochord the moments when the notes of a tune begin, and nothing "
            "else. It lays a steady grid over them, at every speed and every starting point, and scores "
            "each grid. <bookmark mark='a'/> A good grid catches most of the notes, has a note on most "
            "of its points, and runs at a speed near two to the second. <bookmark mark='b'/> For the first "
            f"two phrases of the Tune the best grid has {say(d['period'], 2)} seconds between beats: "
            f"{say(d['bpm'])} to the minute, which is the tempo it was played at. Here is that grid, "
            "tapped on a wood block."
        ) as vo:
            self.play(FadeIn(g), FadeIn(first), FadeIn(lf))
            vo.wait_until("a")
            self.play(FadeOut(first), FadeOut(lf), FadeIn(rule), Create(cv), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(peak), FadeIn(pk))
        self.play(FadeOut(rule))
        end = max(d["notes"]) + 1.1
        notes = ticks(d["notes"], 0.0, end, width=10.0, height=0.5, color=TUNE).move_to(DOWN * 1.5)
        taps = ticks(d["taps"], 0.0, end, width=10.0, height=0.5, color=LOW).move_to(DOWN * 2.6)
        ln = label(r"the notes", font_size=22, color=TUNE).next_to(notes, LEFT, buff=0.2)
        lt = label(r"the taps", font_size=22, color=LOW).next_to(taps, LEFT, buff=0.2)
        h1, h2 = notes.head(), taps.head()
        self.play(FadeIn(notes), FadeIn(taps), FadeIn(ln), FadeIn(lt), FadeIn(h1), FadeIn(h2))
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ and the beat a machine found in it", detail=r"Part 7's piano; \ a wood block", corner=DL, tag_corner=DR)
            snd.drive(h1, notes.run())
            snd.drive(h2, taps.run())
            flash(snd, taps.marks, d["taps"], base=LOW, hot=WHITE)
        with self.voiceover(
            "It found the beat. It did not find the bar. Whether these beats go in twos or in threes is "
            "not in the timing of this tune at all: every note but two is the same length. To hear a "
            "meter, a listener needs to be told which beats are strong. That is the job of accent."
        ):
            self.play(FadeOut(h1), FadeOut(h2))
        self.wait(0.4)
        self.clear_scene()
