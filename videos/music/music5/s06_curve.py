from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403


class Curve(SoundScene):
    def construct(self):
        chapter(self, 5, r"A curve with no ratios in it", r"What happens when each note is a whole set of partials?", lit=(1965,),
                extra=((1965, r"Plomp and Levelt"),))
        self.partials()
        self.worked()
        self.curve()
        self.glide()

    # ------------------------------------------------------------------
    def partials(self):
        d = load("curve")
        n = d["partials"]
        base = LEFT * 5.6 + DOWN * 0.3
        unit = 10.6 / 7.6
        axis = Line(base, base + RIGHT * 10.9, color=GREY_C, stroke_width=2)
        amps = [d["rolloff"] ** k for k in range(n)]
        low = VGroup(*[Line(base + RIGHT * unit * k, base + RIGHT * unit * k + UP * 2.2 * a, color=AIR, stroke_width=6) for k, a in zip(range(1, n + 1), amps)])
        up = VGroup(*[Line(base + RIGHT * unit * 1.5 * k, base + RIGHT * unit * 1.5 * k + UP * 2.2 * a, color=TUNE, stroke_width=6)
                      for k, a in zip(range(1, n + 1), amps) if 1.5 * k < 7.7])
        ticks = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(base + RIGHT * unit * k, DOWN, buff=0.12) for k in range(1, 8)])
        xl = label(r"frequency, \ in multiples of the lower note", font_size=22, color=GREY_B).next_to(axis, DOWN, buff=0.5)
        leg = VGroup(label(r"the lower note: \ seven partials", font_size=26, color=AIR), label(r"a note a fifth above: \ seven more", font_size=26, color=TUNE)
                     ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).to_corner(UR, buff=0.5)
        count = label(rf"{n} + {n} partials: \ {2 * n * (2 * n - 1) // 2} pairs, \ each with its own roughness. \ Add them up.", font_size=30, color=EAR).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A plucked string, a voice, a pipe: every one of them sounds a fundamental and a whole row of "
            "partials above it. That was Parts 1 and 3. <bookmark mark='a'/> So when two instruments play two "
            "notes, the ear does not receive two tones. With seven partials each, it receives fourteen. "
            "<bookmark mark='b'/> And every one of those fourteen can beat against every other. That is "
            "ninety-one pairs. For each pair, Plomp and Levelt's curve gives a roughness, which depends on how "
            "far apart the two partials are, measured in bands of the ear. <bookmark mark='c'/> Helmholtz's "
            "proposal, in modern form, is one line long: add them all up."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(ticks), FadeIn(xl), LaggedStart(*[GrowFromEdge(x, DOWN) for x in low], lag_ratio=0.1), FadeIn(leg[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in up], lag_ratio=0.1), FadeIn(leg[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(count))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        d = load("worked")
        title = label(r"A worked example: \ a fifth, \ and a tritone", font_size=36).to_edge(UP, buff=0.4)
        base, unit = LEFT * 5.9, 11.4 / 7.6
        rows = VGroup()
        for name, ratio, y in ((r"a fifth, \ 3 : 2", 1.5, 1.2), (r"a tritone, \ 45 : 32", 45 / 32, -1.6)):
            b = base + UP * y
            axis = Line(b, b + RIGHT * 11.6, color=GREY_C, stroke_width=2)
            low = VGroup(*[Line(b + RIGHT * unit * k, b + RIGHT * unit * k + UP * 1.2 * 0.88 ** (k - 1), color=AIR, stroke_width=5) for k in range(1, 8)])
            up = VGroup(*[Line(b + RIGHT * unit * ratio * k, b + RIGHT * unit * ratio * k + UP * 1.2 * 0.88 ** (k - 1), color=TUNE, stroke_width=5)
                          for k in range(1, 8) if ratio * k < 7.7])
            rows.add(VGroup(axis, low, up, label(name, font_size=26, color=GREY_A).next_to(axis, UP, buff=1.35).align_to(axis, LEFT)))
        ask = pause_card(r"Lower note: \ partials 1, 2, 3 \ldots \ Upper note, \ a fifth above: \ 1.5, 3, 4.5 \ldots \\ Which partials of the two notes land in the same place?",
                         width=9.4, font_size=26).move_to(DOWN * 1.9)
        meet = VGroup(*[Circle(radius=0.2, color=GOOD, stroke_width=4).move_to(base + UP * 1.2 + RIGHT * unit * k + UP * 0.15) for k in (3, 6)])
        ml = label(r"3 = 2 $\times$ 1.5 \quad and \quad 6 = 4 $\times$ 1.5: \ they coincide, \ and cannot beat", font_size=26, color=GOOD).next_to(rows[0][0], DOWN, buff=0.2)
        tp = d["tritone"]["pairs"][:3]
        clash = VGroup(*[Ellipse(width=0.55, height=0.4, color=BAD, stroke_width=4).move_to(base + DOWN * 1.6 + RIGHT * unit * (p["lower"] + p["upper"] * 45 / 32) / 2 + UP * 0.15) for p in tp])
        cl = label(rf"partials {tp[0]['lower']} and {tp[0]['upper']}: \ {tp[0]['apart']:.0f} Hz apart. \quad {tp[1]['lower']} and {tp[1]['upper']}: \ {tp[1]['apart']:.0f} Hz. \quad "
                   rf"Inside one band, \ and rough.", font_size=26, color=BAD).next_to(rows[1][0], DOWN, buff=0.2)
        tot = label(rf"total roughness: \quad fifth {d['fifth']['total']:.2f} \qquad tritone {d['tritone']['total']:.2f}", font_size=30, color=EAR).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "A worked example will show what that sum does. Take the fifth. If the lower note's partials are at "
            "one, two, three, and so on, the upper note's are at one and a half, three, four and a half. Which "
            "partials of the two notes land in exactly the same place? Pause and find them."
        ):
            self.play(FadeIn(title), FadeIn(rows[0]), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "The third partial of the lower note and the second of the upper are both at three. The sixth and "
            "the fourth are both at six. <bookmark mark='a'/> Two partials at the same frequency cannot beat. And "
            "every other pair in a fifth is at least half the lower note's frequency apart, which is too far to "
            "be very rough. <bookmark mark='b'/> Now the tritone. Nothing coincides. Instead, partials that "
            f"would have met in a fifth miss each other narrowly. The third partial of the lower note and the "
            f"second of the upper are {say(tp[0]['apart'])} hertz apart. The fourth and the third are "
            f"{say(tp[1]['apart'])} apart. Both pairs sit inside a single band of the ear, near its roughest "
            f"spacing. <bookmark mark='c'/> Add everything up, and the tritone is more than twice as rough as "
            "the fifth. Not because of its ratio. Because of where its partials fall."
        ) as vo:
            self.play(FadeOut(ask), LaggedStart(*[Create(m) for m in meet], lag_ratio=0.5), FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            self.play(LaggedStart(*[Create(m) for m in clash], lag_ratio=0.5), FadeIn(cl), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(tot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("curve")
        g = ratio_axis(1.0, 2.2, y_hi=1.0, x_length=11.2, y_length=3.6, marks=((1, 1), (6, 5), (5, 4), (4, 3), (3, 2), (5, 3), (2, 1)))
        g.move_to(DOWN * 0.5)
        cu = rcurve(g, d["r"], d["curve"], ROUGH)
        head = label(r"the roughness of two notes, \ seven partials each, \ against the interval between them", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        drops = VGroup(*[DashedLine(g.at(m["ratio"], m["rough"]), g.at(m["ratio"], 0), color=GOOD, stroke_width=2) for m in d["minima"] if m["q"] <= 5])
        sevens = VGroup(*[VGroup(DashedLine(g.at(m["ratio"], m["rough"]), g.at(m["ratio"], m["rough"] + 0.22), color=LIMIT, stroke_width=2),
                                 MathTex(rf"{m['p']}{{:}}{m['q']}", font_size=22, color=LIMIT).move_to(g.at(m["ratio"], m["rough"] + 0.3)))
                          for m in d["minima"] if m["p"] == 7 or m["q"] == 7])
        named = [m for m in d["minima"] if m["q"] <= 5]
        worst = max(abs(m["off_cents"]) for m in d["minima"])
        res = label(rf"every valley is at a simple ratio, \ to within {max(worst, 0.5):.1f} cents", font_size=28, color=GOOD).to_edge(DOWN, buff=0.3)
        xl = label(r"the interval between the two notes", font_size=22, color=GREY_B).next_to(g, DOWN, buff=0.1)
        with self.voiceover(
            "Now do that sum for every interval, from unison to a little beyond the octave, and plot it. "
            "<bookmark mark='a'/> This is Monochord's curve. It starts low, climbs steeply as the two notes "
            "separate, and then, instead of falling smoothly as it did for pure tones, it is cut by valleys. "
            "<bookmark mark='b'/> Look at where the valleys are. Six to five. Five to four. Four to three. Three "
            "to two. Five to three. Two to one. The minor third, the major third, the fourth, the fifth, the "
            "major sixth, the octave: the consonances of Western music, with the octave and the fifth the "
            "deepest of all. <bookmark mark='c'/> Nobody put a ratio into this calculation. It contains two "
            "things only: a note with harmonic partials, and the width of the ear's filter. The ratios came out. "
            "They are the places where partials of one note fall exactly onto partials of the other. "
            "<bookmark mark='d'/> There are three more valleys, shallower, at ratios with a seven in them. "
            "Western music has no names for those. Barbershop quartets sing one of them anyway, and we will meet "
            "them in the next part. And notice what has become of chapter one's test. A fifth that is five cents "
            "wide is a point just beside the bottom of a valley: a little rougher, no more. This theory can be a "
            "little bit off."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(cu), run_time=4.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in drops], lag_ratio=0.55), run_time=9.0)
            vo.wait_until("c")
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(x) for x in sevens], lag_ratio=0.3))
        self.g, self.cu = g, cu
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def glide(self):
        d = load("curve")
        c = clip("curve.glide")
        secs = d["seconds"]
        g = ratio_axis(1.0, 2.2, y_hi=1.0, x_length=11.2, y_length=3.2, marks=((1, 1), (6, 5), (5, 4), (4, 3), (3, 2), (5, 3), (2, 1)))
        g.move_to(DOWN * 1.0)
        cu = rcurve(g, d["r"], d["curve"], ROUGH).set_stroke(opacity=0.45)
        note = listen_note(r"The lower note stays on middle C. \ The upper one climbs slowly through an octave. \\ Listen for the valleys: \ moments when the grinding clears.",
                           width=10.2, font_size=26).to_edge(UP, buff=0.35)
        dot = Dot(g.at(1.0, d["rough_t"][0]), radius=0.13, color=TUNE)
        with self.voiceover(
            "Hear the curve. The lower note stays on middle C. The upper note climbs slowly from unison to just "
            "past the octave, and the dot follows it along the curve. Listen for the valleys: the moments when "
            "the grinding clears, and the two notes lock together."
        ):
            self.play(FadeIn(note, shift=DOWN * 0.2), FadeIn(g), FadeIn(cu), FadeIn(dot))
        ratio_t, rough_t = d["ratio_t"], d["rough_t"]

        def move(m, t):
            k = int(np.clip(t / secs, 0, 1) * (len(ratio_t) - 1))
            m.move_to(g.at(ratio_t[k], rough_t[k])).set_color(interpolate_color(ManimColor(SMOOTH), ManimColor(ROUGH), min(rough_t[k] / d["max"], 1.0)))

        with self.listen(c) as snd:
            window(snd, r"one note still, \ one climbing an octave", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            snd.drive(dot, move)
        with self.voiceover(
            "The clearest moments were the fifth, about two thirds of the way through, and the octave at the "
            "end, where the upper note's partials vanish into the lower note's entirely. You have just heard "
            "Pythagoras's discovery, with the reason attached."
        ):
            self.play(Indicate(g.marks[4], color=GOOD, scale_factor=1.3), Indicate(g.marks[6], color=GOOD, scale_factor=1.3))
        self.wait(0.3)
        self.clear_scene()
