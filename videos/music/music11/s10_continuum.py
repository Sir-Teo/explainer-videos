from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403


class Continuum(SoundScene):
    def construct(self):
        chapter(self, 9, r"Where rhythm becomes pitch", r"What is three against two, \ a hundred times a second?", extra=((1930, r"Cowell, \textit{New Musical Resources}"),))
        self.speed_up()
        self.fifth()
        self.chords()
        self.timbre()

    # ------------------------------------------------------------------
    def speed_up(self):
        d = load("continuum")
        c = clip("continuum.fifth")
        nk = necklace(6, onsets=[0, 2, 4], radius=1.2, color=HIGH).move_to(LEFT * 4.6 + UP * 1.6)
        low = VGroup(Line(nk.at(0), nk.at(3), color=LOW, stroke_width=3), *[Dot(nk.at(i), radius=0.14, color=LOW, fill_opacity=0.0, stroke_width=3, stroke_color=LOW) for i in (0, 3)])
        lo, hi = np.log10(d["rate0"]), np.log10(d["rate1"])
        width = 11.0
        X = lambda r: -width / 2 + width * (np.log10(r) - lo) / (hi - lo)          # noqa: E731
        y0 = -1.6
        axis = VGroup(Line([X(d["rate0"]), y0, 0], [X(d["rate1"]), y0, 0], color=GREY_C, stroke_width=2))
        for r, t in ((1, r"1 cycle a second"), (3, r"3"), (10, r"10"), (30, r"30"), (100, r"100")):
            axis.add(Line([X(r), y0 - 0.1, 0], [X(r), y0 + 0.1, 0], color=GREY_B, stroke_width=2), label(t, font_size=22, color=GREY_B).move_to([X(r), y0 - 0.4, 0]))
        two = DecimalNumber(2 * d["rate0"], num_decimal_places=1, font_size=44, color=LOW)
        three = DecimalNumber(3 * d["rate0"], num_decimal_places=1, font_size=44, color=HIGH)
        read = VGroup(VGroup(label(r"the two:", font_size=28, color=LOW), two, label(r"a second", font_size=24, color=GREY_B)).arrange(RIGHT, buff=0.25),
                      VGroup(label(r"the three:", font_size=28, color=HIGH), three, label(r"a second", font_size=24, color=GREY_B)).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 2.0 + UP * 1.6)
        for row in read:                                             # leave room for the numbers to grow to three digits
            row[2].shift(RIGHT * 1.0)
            row[1].align_to(row[0].get_right() + RIGHT * 0.25, LEFT)
        marker = Triangle(color=WHITE, fill_color=WHITE, fill_opacity=1.0).scale(0.14).rotate(PI).move_to([X(d["rate0"]), y0 + 0.35, 0])
        card = listen_card(r"Three against two, \ faster and faster. \ Notice the moment when you stop hearing a rhythm. \ What do you hear instead?", width=10.0, font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "Now the experiment this part has been heading for. Take three against two, at less than "
            "one cycle a second, and speed it up, steadily, until it is going round a hundred times a "
            "second. Notice the moment when you stop hearing a rhythm. And what do you hear instead?"
        ):
            self.play(FadeIn(nk), FadeIn(low), FadeIn(card))
        self.wait(0.8)
        self.play(FadeOut(card), FadeIn(axis), FadeIn(read), FadeIn(marker))
        g = np.log(d["rate1"] / d["rate0"]) / d["ramp"]
        rate = lambda t: d["rate0"] * np.exp(g * min(max(t, 0.0), d["ramp"]))          # noqa: E731
        phase = lambda t: d["rate0"] * (np.exp(g * min(max(t, 0.0), d["ramp"])) - 1.0) / g + d["rate1"] * max(t - d["ramp"], 0.0)   # noqa: E731

        def hand(m, t):                                              # the hand shows the cycle while the eye can follow it
            r = rate(t)
            a = np.pi / 2 - 2 * np.pi * (phase(t) if r < 6 else 0.0)
            cc = nk.ring.get_center()
            m.put_start_and_end_on(cc, cc + nk.radius * 0.92 * np.array([np.cos(a), np.sin(a), 0.0]))
            m.set_stroke(opacity=1.0 if r < 6 else 0.0)

        t2, t3 = np.asarray(d["two"]), np.asarray(d["three"])
        lamp2 = Dot(radius=0.26, color=LOW).move_to(RIGHT * 0.2 + UP * 0.0)
        lamp3 = Dot(radius=0.26, color=HIGH).move_to(RIGHT * 1.2 + UP * 0.0)
        self.add(lamp2, lamp3)
        glow = lambda ts: (lambda m, t: m.set_opacity(0.15 + 0.85 * float(np.exp(-14.0 * max(t - ts[max(np.searchsorted(ts, t, side="right") - 1, 0)], 0.0)))))   # noqa: E731
        with self.listen(c) as snd:
            window(snd, r"three against two, \ sped up", kind="synthesized", detail=r"clicks", corner=DL, tag_corner=DR)
            snd.drive(lamp2, glow(t2))
            snd.drive(lamp3, glow(t3))
            snd.drive(nk.hand, hand)
            snd.drive(marker, lambda m, t: m.set_x(X(rate(t))))
            snd.drive(two, lambda m, t: m.set_value(2 * rate(t)).align_to(read[0][0].get_right() + RIGHT * 0.25, LEFT))
            snd.drive(three, lambda m, t: m.set_value(3 * rate(t)).align_to(read[1][0].get_right() + RIGHT * 0.25, LEFT))
        self.remove(lamp2, lamp3)
        self.parts = (nk, low, axis, read, marker, X, y0)

    # ------------------------------------------------------------------
    def fifth(self):
        d = load("continuum")
        nk, low, axis, read, marker, X, y0 = self.parts
        zone = VGroup(Rectangle(width=X(20 / 3) - X(d["rate0"]), height=0.5, stroke_width=0, fill_color=GOOD, fill_opacity=0.3).move_to([(X(20 / 3) + X(d["rate0"])) / 2, y0 + 0.9, 0]),
                      Rectangle(width=X(d["rate1"]) - X(20 / 3), height=0.5, stroke_width=0, fill_color=AIR, fill_opacity=0.3).move_to([(X(d["rate1"]) + X(20 / 3)) / 2, y0 + 0.9, 0]))
        zl = VGroup(label(r"a rhythm", font_size=24, color=GOOD).move_to(zone[0]), label(r"two notes", font_size=24, color=AIR).move_to(zone[1]))
        ans = VGroup(MathTex(rf"\frac{{{d['f3']:.0f} \text{{ Hz}}}}{{{d['f2']:.0f} \text{{ Hz}}}} = \frac32", font_size=48), label(rf"{d['cents']:.0f} cents: \ a perfect fifth", font_size=34, color=TUNE)).arrange(RIGHT, buff=0.7).move_to(DOWN * 3.0)
        with self.voiceover(
            "Somewhere near twenty clicks a second, the rhythm was gone. <bookmark mark='a'/> The clicks "
            "of each part fused into a note, as the single train did in chapter one. At the end, one "
            f"part was clicking {say(d['f2'])} times a second and the other {say(d['f3'])}. Those are two "
            f"notes, and Monochord measures the distance between them: {say(d['cents'])} cents. "
            "<bookmark mark='b'/> A perfect fifth. The interval that Part 1 found by stopping a string at "
            "two thirds of its length is three against two, played too fast to count."
        ) as vo:
            self.play(FadeOut(marker))
            vo.wait_until("a")
            self.play(FadeIn(zone), FadeIn(zl))
            vo.wait_until("b")
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chords(self):
        rows = rows_card([
            (r"2 : 1", r"two against one: \ the octave"),
            (r"3 : 2", r"three against two: \ the fifth"),
            (r"4 : 3", r"four against three: \ the fourth"),
            (r"4 : 5 : 6", r"three parts at once: \ a major chord"),
        ], left=-4.6, text_left=-1.6, top=1.9, step=0.95, name_size=40, text_size=30)
        head = label(r"every interval of Part 1 is a polyrhythm", font_size=34, color=TUNE).to_edge(UP, buff=0.5)
        card = history_card(1930, r"Henry Cowell, \ \textit{New Musical Resources}", r"rhythm and interval are one scale of ratios, \ heard at two speeds", width=6.4, font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So every interval of Part 1 is a polyrhythm. <bookmark mark='a'/> The octave is two "
            "against one. The fifth, three against two. The fourth, four against three. A major chord "
            "is four, five and six at once. <bookmark mark='b'/> And the reason given in Part 5 for "
            "why those intervals sound smooth is the reason given in this part for why those rhythms "
            "are easy: the pattern the parts make together repeats soon. The composer Henry Cowell "
            "set this out in 1930, and built an instrument with Leon Theremin to play it. Below about "
            "twenty a second we count the pattern, and call it rhythm. Above, we cannot count it, and we "
            "hear its ratio as a quality: an interval. It is one phenomenon, heard at two speeds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.6), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def timbre(self):
        d = load("continuum")
        c = clip("continuum.timbre")
        cols = VGroup()
        for nm, col in (("A", LOW), ("B", HIGH)):
            pt = d["timbre_patterns"][nm]
            nk = necklace(8, onsets=[i for i, ch in enumerate(pt) if ch == "x"], radius=1.0, color=col)
            h = d["timbre_harmonics"][nm]
            bars = VGroup(*[Rectangle(width=0.2, height=max(1.3 * v, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([k * 0.3, 0, 0], aligned_edge=DOWN) for k, v in enumerate(h)])
            cap = label(r"its harmonics, \ 1 to 12", font_size=20, color=GREY_B).next_to(bars, DOWN, buff=0.15)
            cols.add(VGroup(label(nm, font_size=36, color=col), nk, VGroup(bars, cap)).arrange(DOWN, buff=0.4))
        cols.arrange(RIGHT, buff=2.2).move_to(UP * 0.2)
        for col in cols:
            col[2].set_opacity(0)
        note = listen_note(r"two patterns of clicks: \ once a second, \ and then 110 times a second", width=8.6, font_size=26).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "One step further. Those fast rhythms were even strokes. What happens to a pattern? Here "
            "are two cycles of eight pulses. A has one stroke. B has three, unevenly spaced. Slowly, "
            "they are two different rhythms. Listen to them once a second, and then a hundred and ten "
            "times a second."
        ):
            self.play(FadeIn(cols), FadeIn(note))
        self.play(FadeOut(note))
        ev = d["timbre_events"]
        with self.listen(c) as snd:
            window(snd, r"A, \ B; \ then both, \ very fast", kind="synthesized", detail=r"clicks", corner=DL, tag_corner=DR)
            for nm, col in zip("AB", cols):
                pulse(snd, col[0], ev[f"slow{nm}"], ev[f"slow{nm}"] + 2.0, buff=0.12)
                pulse(snd, col[0], ev[f"fast{nm}"], ev[f"fast{nm}"] + 1.2, buff=0.12)
                snd.drive(col[1].hand, col[1].turn(1.0, ev[f"slow{nm}"], ev[f"slow{nm}"] + 2.0))
        with self.voiceover(
            "Fast, both are the same note, because the cycle goes round at the same rate. But they do "
            "not sound alike. <bookmark mark='a'/> A has every harmonic at full strength. B has some "
            "strong and some nearly missing. Those bars are the spectrum of Part 3, and they are fixed "
            "by the pattern of strokes inside the cycle. So the rate of the cycle becomes the pitch, and "
            "the rhythm inside the cycle becomes the tone colour. Rhythm, pitch and timbre are one "
            "thing, heard at three speeds."
        ) as vo:
            vo.wait_until("a")
            self.play(*[col[2].animate.set_opacity(1) for col in cols])
        self.wait(0.4)
        self.clear_scene()
