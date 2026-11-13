from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403


class Timbre(SoundScene):
    def construct(self):
        chapter(self, 6, r"Bend the timbre", r"If the ratios come from the partials, can we move them?", lit=(1965,),
                extra=((1993, r"Sethares: \ timbre and scale"),))
        self.idea()
        self.curves()
        self.four()
        self.world()

    # ------------------------------------------------------------------
    def idea(self):
        d = load("stretched")
        wide = d["wide"]
        card = history_card(1993, r"William Sethares, \ Wisconsin",
                            r"if the valleys are where partials line up, then they depend on where the partials are. Change the partials, and the consonances must move.",
                            width=5.6).to_corner(UL, buff=0.4)
        base, unit = LEFT * 5.8 + DOWN * 1.4, 11.2 / 8.4
        axis = Line(base, base + RIGHT * 11.4, color=GREY_C, stroke_width=2)
        plain = VGroup(*[Line(base + RIGHT * unit * k, base + RIGHT * unit * k + UP * 1.3, color=AIR, stroke_width=5) for k in range(1, 8)])
        fs = np.array(d["partials_of_100"]) / 100.0
        bent = VGroup(*[Line(base + RIGHT * unit * f + DOWN * 0.0, base + RIGHT * unit * f + UP * 1.3, color=TUNE, stroke_width=5) for f in fs])
        pl = VGroup(*[MathTex(str(k), font_size=22, color=AIR).next_to(base + RIGHT * unit * k, DOWN, buff=0.1) for k in range(1, 8)])
        bl = VGroup(*[MathTex(rf"{f:.2f}", font_size=22, color=TUNE).next_to(base + RIGHT * unit * f, DOWN, buff=0.45) for f in fs])
        names = VGroup(label(r"an ordinary tone: \ partials at 1, 2, 3, 4 \ldots", font_size=26, color=AIR),
                       label(rf"a bent tone: \ every doubling stretched to {wide:g}", font_size=26, color=TUNE)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(RIGHT * 3.2 + UP * 1.9)
        with self.voiceover(
            "If that is right, it makes a prediction that no theory of numbers could make, and in 1993 an "
            "engineer named William Sethares spelled it out. <bookmark mark='a'/> The valleys are where the "
            "partials of two notes line up. So they depend on where the partials are. An ordinary tone has its "
            "partials at one, two, three, four times the fundamental. <bookmark mark='b'/> But a computer can "
            "make a tone with its partials anywhere. Take every doubling in that series and stretch it, so that "
            f"the second partial is not at two but at {wide:g}, the fourth not at four but at {wide:g} squared, "
            "and the others in proportion. It is still one tone with a clear pitch. It sounds a little like a "
            "bell. <bookmark mark='c'/> If Helmholtz and Plomp are right, this tone should have its own set of "
            "consonances, and they should not be the ratios of Pythagoras."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(axis), LaggedStart(*[GrowFromEdge(x, DOWN) for x in plain], lag_ratio=0.1), FadeIn(pl), FadeIn(names[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(plain.animate.set_stroke(opacity=0.3), LaggedStart(*[GrowFromEdge(x, DOWN) for x in bent], lag_ratio=0.1), FadeIn(bl), FadeIn(names[1]), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d, p = load("stretched"), load("curve")
        wide = d["wide"]
        g = ratio_axis(1.0, 2.25, y_hi=1.0, x_length=11.2, y_length=3.4, marks=((1, 1), (6, 5), (5, 4), (4, 3), (3, 2), (5, 3), (2, 1)))
        g.move_to(DOWN * 0.3)
        old = rcurve(g, p["r"], p["curve"], AIR).set_stroke(opacity=0.5)
        new = rcurve(g, d["r"], d["curve"], TUNE)
        leg = VGroup(label(r"the ordinary tone", font_size=24, color=AIR), label(r"the bent tone", font_size=24, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.45)
        last = d["table"][-1]
        arrow = Arrow(g.at(2.0, 0.55), g.at(wide, 0.55), color=GOOD, stroke_width=4, buff=0.0, max_tip_length_to_length_ratio=0.3)
        al = label(rf"the smoothest interval is no longer 2 : 1. \ It is {wide:g} : 1.", font_size=28, color=GOOD).move_to(g.at(1.45, 0.92))
        res = label(rf"every valley has moved to its old ratio raised to the power $\log_2 {wide:g}$: \ predicted and found agree to {max(d['worst_gap'], 0.0005):.4f}", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Monochord can check that in a second. Here again is the curve for the ordinary tone, with its "
            "valleys on the just ratios. <bookmark mark='a'/> And here is the same calculation for the bent tone. "
            "Nothing has changed except where the partials are. Every valley has moved to the right. "
            f"<bookmark mark='b'/> The deepest one, which used to be the octave, is now at {wide:g} to one: an "
            "interval that an ordinary musician would call a badly out-of-tune octave. And at two to one, where "
            "the true octave is, the curve stands on a peak. <bookmark mark='c'/> The rule is simple. Each valley "
            "has moved to its old ratio, stretched by the same amount as the partials were. Prediction and "
            "calculation agree to four decimal places."
        ) as vo:
            self.play(FadeIn(g), Create(old), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(new), FadeIn(leg[1]), run_time=3.0)
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(al))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def four(self):
        d = load("stretched")
        wide = d["wide"]
        c = clip("stretched.four")
        q = listen_card(rf"Four sounds. \ An exact octave, \ then a wide one ({wide:g} to 1), \ in the ordinary tone. \\ Then the same two intervals in the bent tone. \ "
                        r"In each pair, \ which is the smooth one?", width=10.6, font_size=26).to_edge(UP, buff=0.35)
        grid = VGroup(*[RoundedRectangle(width=3.0, height=1.25, corner_radius=0.12, stroke_color=GREY_C, stroke_width=2) for _ in range(4)]).arrange_in_grid(2, 2, buff=(0.5, 0.35)).move_to(RIGHT * 1.2 + DOWN * 1.1)
        cols = VGroup(MathTex(r"2 : 1", font_size=34, color=GREY_A).next_to(grid[0], UP, buff=0.2), MathTex(rf"{wide:g} : 1", font_size=34, color=GREY_A).next_to(grid[1], UP, buff=0.2))
        rows = VGroup(label(r"ordinary tone", font_size=26, color=AIR).next_to(grid[0], LEFT, buff=0.35), label(r"bent tone", font_size=26, color=TUNE).next_to(grid[2], LEFT, buff=0.35))
        with self.voiceover(
            "A calculation is not a sound. So here are four sounds. First, in the ordinary tone, an exact "
            "octave, and then the wide one. Then the same two intervals again, in the bent tone. In each pair, "
            "decide which is the smooth one."
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(grid), FadeIn(cols), FadeIn(rows))
        keys = ("plain_true", "plain_wide", "bent_true", "bent_wide")
        with self.listen(c) as snd:
            window(snd, r"an octave and a wide octave, \ in two tones", kind="synthesized", detail=r"sums of sines", corner=DL, tag_corner=DR)
            for key, cell in zip(keys, grid):
                t0 = snd.time_of(key)
                pulse(snd, cell, t0, t0 + 2.0, buff=0.0)
        vals = VGroup()
        for key, cell in zip(keys, grid):
            v = d["grid"][key]
            good = v < 0.1
            vals.add(VGroup(label(r"smooth" if good else r"rough", font_size=30, color=SMOOTH if good else ROUGH), label(rf"{v:.2f}", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.08).move_to(cell))
        ratio = d["grid"]["bent_true"] / d["grid"]["bent_wide"]
        with self.voiceover(
            "In the ordinary tone, the exact octave is smooth and the wide one grinds, as you would expect. "
            "<bookmark mark='a'/> In the bent tone it is the other way round. The exact octave is the rough one, "
            f"by a factor of {say(ratio)} in Monochord's sum, and the wide one is smooth. <bookmark mark='b'/> That "
            "was the sound that opened this part. Its partials had been stretched, so its octave had moved, and "
            "a true two to one put fourteen partials in each other's way. An interval is not consonant or "
            "dissonant. An interval on a particular timbre is. Pythagoras's ratios are not a law of number. "
            "They are a fact about strings, pipes and voices: things whose partials are whole multiples."
        ) as vo:
            self.play(FadeOut(q), FadeIn(vals[0]), FadeIn(vals[1]))
            vo.wait_until("a")
            self.play(FadeIn(vals[2]), FadeIn(vals[3]))
            vo.wait_until("b")
            law = label(r"consonance belongs to an interval \emph{and} a timbre, \ together", font_size=32, color=EAR).to_edge(UP, buff=0.6)
            self.play(FadeIn(law))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def world(self):
        rows = rows_card([
            (r"the piano", r"its strings are stiff, \ so its partials run sharp (Part 1). \\ Tuners stretch the octaves to match. \quad $\rightarrow$ Part 6"),
            (r"bells", r"a bell's partials are not a harmonic series at all. \\ Founders tune five of them by turning metal off the inside. \quad $\rightarrow$ Part 9"),
            (r"the gamelan", r"bronze bars and gongs with their own partials, \\ and scales that are not the West's. \quad $\rightarrow$ Part 36"),
            (r"synthesizers", r"a composer can now choose the partials first \\ and derive the scale from them. \quad $\rightarrow$ Part 52"),
        ], left=-6.3, text_left=-3.3, top=1.7, step=1.3, text_size=24)
        head = label(r"Not only in computers", font_size=38, color=GREY_A).to_edge(UP, buff=0.35)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "This is not a curiosity of computer music. <bookmark mark='a'/> A piano's strings are stiff, and in "
            "Part 1 we saw that stiffness pushes the upper partials sharp. So a piano's own octaves are slightly "
            "wider than two to one, and every tuner stretches them to match. <bookmark mark='b'/> The partials of "
            "a bell are not a harmonic series at all, and bell founders tune the lowest five of them one by one. "
            "<bookmark mark='c'/> The bronze bars and gongs of a Javanese gamelan have partials of their own, "
            "and the gamelan's scales are not the scales of the West. Sethares argued that each fits the other. "
            "<bookmark mark='d'/> And a composer with a synthesizer can now go the other way: choose the "
            "partials first, and let the scale follow from them. The instrument and the scale are made for each "
            "other. Change one, and the other has to move."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
