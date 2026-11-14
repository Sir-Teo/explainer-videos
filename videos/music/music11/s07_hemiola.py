from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403


class Hemiola(SoundScene):
    def construct(self):
        chapter(self, 6, r"Three against two", r"What if two metres are right at once?")
        self.six()
        self.together()
        self.four_three()
        self.canon()

    # ------------------------------------------------------------------
    def six(self):
        d = load("hemiola")
        c = clip("hemiola.bars")
        dots = VGroup(*[Dot(radius=0.16, color=WEAK) for _ in range(6)]).arrange(RIGHT, buff=0.9).move_to(UP * 0.6)
        xs = [x.get_x() for x in dots]
        pitch = xs[1] - xs[0]
        up = group_brackets(xs, (3, 3), dots.get_y() + 0.75, pitch, color=LOW)
        for b in up:
            b.rotate(PI, axis=RIGHT)
        down = group_brackets(xs, (2, 2, 2), dots.get_y() - 0.75, pitch, color=HIGH)
        lu = label(r"two beats of three: \ six-eight", font_size=28, color=LOW).next_to(up, UP, buff=0.3)
        ld = label(r"three beats of two: \ three-four", font_size=28, color=HIGH).next_to(down, DOWN, buff=0.3)
        with self.voiceover(
            "Go back to the six eighth notes of chapter two. <bookmark mark='a'/> Grouped in threes they "
            "make two beats: six-eight. <bookmark mark='b'/> Grouped in twos they make three beats: "
            "three-four. Nothing stops a composer from changing the grouping from one bar to the next. "
            "The eighth notes go on evenly; only the accents move. Listen: the bass drum marks the "
            "groups, and they change every bar."
        ) as vo:
            self.play(FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(up), FadeIn(lu))
            vo.wait_until("b")
            self.play(FadeIn(down), FadeIn(ld))
        with self.listen(c) as snd:
            window(snd, r"threes, \ twos, \ threes, \ twos", detail=r"bass drum and wood block, \ modelled", corner=DL, tag_corner=DR)
            for bar in range(8):
                t0 = snd.time_of(f"bar{bar}")
                pulse(snd, lu if bar % 2 == 0 else ld, t0, t0 + 1.18, buff=0.12)
            ts = [snd.time_of(f"bar{bar}") + i * d["pulse"] for bar in range(8) for i in range(6)]
            flash(snd, [dots[i] for _ in range(8) for i in range(6)], ts, base=WEAK, hot=WHITE, fade=0.12)
        with self.voiceover(
            "That device has a Greek name, hemiola, which means one and a half: three in the place of "
            "two. Baroque dances use it to broaden before a cadence, and it is the engine of a great deal "
            "of music from Spain and Latin America. The six notes never change. The listener's grid is "
            "pulled from one shape to the other and back."
        ):
            self.play(Indicate(up, color=LOW), Indicate(down, color=HIGH))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def together(self):
        d = load("hemiola")
        c = clip("hemiola.poly")
        p = d["p32"]
        nk = necklace(6, onsets=p["a"], radius=1.7, color=HIGH).move_to(LEFT * 3.4 + UP * 0.3)
        low = VGroup(Line(nk.at(p["b"][0]), nk.at(p["b"][1]), color=LOW, stroke_width=3), *[Dot(nk.at(i), radius=0.16, color=LOW, fill_opacity=0.0, stroke_width=3, stroke_color=LOW) for i in p["b"]])
        row = VGroup(*[Square(side_length=0.5, stroke_color=GREY_D, stroke_width=1.5) for _ in range(6)]).arrange(RIGHT, buff=0.08)
        hi_row = VGroup(*[Dot(row[i].get_center() + UP * 0.6, radius=0.13, color=HIGH) for i in p["a"]])
        lo_row = VGroup(*[Dot(row[i].get_center() + DOWN * 0.6, radius=0.13, color=LOW) for i in p["b"]])
        comp = VGroup(*[row[i].copy().set_fill(WHITE, opacity=0.85) for i in p["composite"]])
        grid = VGroup(row, hi_row, lo_row, comp).move_to(RIGHT * 3.2 + UP * 0.6)
        gaps = label(r"together: \ long, \ short, \ short, \ long \ ($2, 1, 1, 2$)", font_size=26, color=GREY_A).next_to(grid, DOWN, buff=0.5)
        lcm = label(r"the two meet once in every $2 \times 3 = 6$ pulses", font_size=26, color=GREY_A).next_to(gaps, DOWN, buff=0.25)
        both = label(r"both groupings at once: \ a cycle of six pulses", font_size=32, color=TUNE).to_edge(UP, buff=0.5)
        with self.voiceover(
            "A bolder idea: do not take turns. Play both groupings at once. Draw the cycle as a circle of "
            "six pulses, with a hand that goes round once a cycle. <bookmark mark='a'/> One player "
            "strikes three times a cycle, evenly: the triangle. <bookmark mark='b'/> The other strikes "
            "twice: the line across. <bookmark mark='c'/> Together they make a pattern neither plays: "
            "long, short, short, long. Musicians learn it as one rhythm, shared between two hands. You "
            "will hear the two alone, the three alone, and then both."
        ) as vo:
            self.play(FadeIn(nk.ring), FadeIn(nk.ticks), FadeIn(nk.hand), FadeIn(row), FadeIn(both))
            vo.wait_until("a")
            self.play(FadeIn(nk.poly), FadeIn(nk.dots), FadeIn(hi_row))
            vo.wait_until("b")
            self.play(FadeIn(low), FadeIn(lo_row))
            vo.wait_until("c")
            self.play(FadeIn(comp), FadeIn(gaps), FadeIn(lcm))
        with self.listen(c) as snd:
            window(snd, r"two; \ three; \ three against two", detail=r"a drum and a clave, \ modelled", corner=DL, tag_corner=DR)
            snd.drive(nk.hand, nk.turn(d["cycle"], 0.0, snd.time_of("four_three") - 0.6))
            pulse(snd, lo_row, snd.time_of("two"), snd.time_of("three"), buff=0.12)
            pulse(snd, hi_row, snd.time_of("three"), snd.time_of("both"), buff=0.12)
            pulse(snd, comp, snd.time_of("both"), snd.time_of("four_three") - 0.6, buff=0.12)
            snd.wait_until(snd.time_of("four_three") - 0.5)
            self.four_three_picture(snd)
        self.wait(0.3)
        self.clear_scene()

    def four_three_picture(self, snd):
        d = load("hemiola")
        q = d["p43"]
        self.clear()
        self.add(*snd._owned)
        nk = necklace(12, onsets=q["a"], radius=1.9, color=HIGH).move_to(LEFT * 3.2 + UP * 0.3)
        tri = VGroup(Polygon(*[nk.at(i) for i in q["b"]], color=LOW, stroke_width=3), *[Dot(nk.at(i), radius=0.16, color=LOW, fill_opacity=0.0, stroke_width=3, stroke_color=LOW) for i in q["b"]])
        text = VGroup(label(r"four against three", font_size=34, color=TUNE), label(r"a cycle of $3 \times 4 = 12$ pulses", font_size=28, color=GREY_A),
                      label(r"together: \ $3, 1, 2, 2, 1, 3$", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.2 + UP * 0.3)
        self.add(nk, tri, text)
        t0 = snd.time_of("four_three")
        snd.drive(nk.hand, nk.turn(d["cycle2"], t0))

    def four_three(self):
        with self.voiceover(
            "The second one was four against three, on a cycle of twelve. Any two whole numbers will do, "
            "and the two parts meet once in every cycle, at the start. The smaller the numbers, the "
            "sooner they meet, and the easier the pattern is to hear as one thing. Keep that in mind. "
            "Three against two is going to come back at the end of this part, in a different disguise."
        ):
            head = VGroup(label(r"$a$ against $b$", font_size=40, color=TUNE), label(r"they meet once in every cycle; \ small numbers meet soonest", font_size=30, color=GREY_A),
                          MathTex(r"2:1 \qquad 3:2 \qquad 4:3 \qquad 5:4", font_size=48)).arrange(DOWN, buff=0.5)
            self.play(FadeIn(head))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def canon(self):
        d = load("hemiola")
        c = clip("hemiola.canon")
        base = d["canon_base"]
        g = dot_grid([1] * 16, width=9.0, row=0.0, radius=0.0)
        top = pattern_row(base, g.xs, y=0.5, size=0.34, color=HIGH)
        rows = [pattern_row(cp, g.xs, y=-0.1, size=0.34, color=LOW) for cp in d["canon_copies"]]
        VGroup(top, *rows).move_to(UP * 1.9)
        lt = label(r"a rhythm", font_size=24, color=HIGH).next_to(top, LEFT, buff=0.3)
        lb = label(r"its copy", font_size=24, color=LOW).next_to(rows[0], LEFT, buff=0.3)
        ax = axes([-0.7, 15.7], [0, 5.6], x_length=8.0, y_length=2.0, xlabel=r"the copy starts this many pulses late", ylabel=r"strokes together", xticks=[0, 2, 4, 6, 8, 10, 12, 14], yticks=[0, 5], font_size=20).move_to(DOWN * 1.4)
        bars = VGroup(*[Rectangle(width=0.32, height=max(ax.ax.c2p(0, m)[1] - ax.ax.c2p(0, 0)[1], 0.03), stroke_width=0, fill_color=WEAK, fill_opacity=0.9).move_to(ax.ax.c2p(k, 0), aligned_edge=DOWN)
                        for k, m in enumerate(d["canon_meets"])])
        with self.voiceover(
            "There is one more thing to set a rhythm against: itself. Take the clave, and a copy of it "
            "on another sound, and start the copy late. <bookmark mark='a'/> For each delay, count how "
            "many strokes of the two still fall together. With no delay, all five. Two pulses late, "
            "one. Eight pulses late, none: the two interlock, and ten strokes come out where there were "
            "five. Listen to those three."
        ) as vo:
            self.play(FadeIn(top), FadeIn(rows[0]), FadeIn(lt), FadeIn(lb))
            vo.wait_until("a")
            self.play(FadeIn(ax), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.06), run_time=2.5)
        shown = rows[0]
        with self.listen(c) as snd:
            window(snd, r"a rhythm against itself: \ 0, \ 2 and 8 pulses late", detail=r"clave and rim, \ modelled", corner=DL, tag_corner=DR)
            for j, k in enumerate(d["canon_shifts"]):
                snd.wait_until(d["canon_starts"][j])
                self.remove(shown)
                shown = rows[j]
                self.add(shown)
                t0 = d["canon_starts"][j]
                snd.drive(bars[k], lambda m, t, t0=t0: m.set_fill(TUNE if t0 <= t < t0 + 4.0 else WEAK))
                on = [i for i, ch in enumerate(base) if ch == "x"]
                flash(snd, [top.cells[i] for rep in range(2) for i in on], [t0 + (rep * 16 + i) * d["canon_pulse"] for rep in range(2) for i in on], base=HIGH, hot=WHITE, fade=0.12)
        with self.voiceover(
            "The composer Steve Reich made whole pieces out of this, a pattern drifting slowly against "
            "itself, and called it phasing. It is the cheapest composing there is: one rhythm, and a "
            "decision about when to start."
        ):
            self.play(Indicate(bars[8], color=TUNE), Indicate(bars[2], color=TUNE))
        self.wait(0.4)
        self.clear_scene()
