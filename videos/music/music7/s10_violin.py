from __future__ import annotations

import numpy as np

from videos.music.music7.common import *  # noqa: F403


class Violin(SoundScene):
    def construct(self):
        chapter(self, 9, r"The violin's box", r"What does the body add that the string did not have?", lit=(1863,), extra=((1973, r"an electronic violin needs resonances"),))
        self.response()
        self.vibrato()
        self.wolf()

    def graph(self, y_length=3.9, x_length=10.6, top=16):
        d = load("violin")
        g = faxes(190, 8000, [-38, top], x_length=x_length, y_length=y_length, ylabel=r"how strongly the body answers (dB)", yticks=[-30, -20, -10, 0], fticks=(200, 500, 1000, 2000, 5000), font_size=20)
        cu = fcurve(g, d["f"], d["db"], WOOD)
        return d, g, cu

    # ------------------------------------------------------------------
    def response(self):
        d, g, cu = self.graph()
        VGroup(g, cu).move_to(DOWN * 0.6)
        m = d["modes"]
        at = lambda f: float(np.interp(np.log(f), np.log(d["f"]), d["db"]))  # noqa: E731

        def tag(f, text, col, up=0.35, dx=0.0):
            p = g.at(f, at(f))
            return VGroup(Dot(p, radius=0.06, color=col), label(text, font_size=22, color=col).next_to(p, UP, buff=up).shift(RIGHT * dx))

        t_air = tag(m["A0"], r"the air in the box, \\ through the f-holes", AIR, dx=0.25)
        t_wood = VGroup(tag(m["B1-"], r"", TUNE), tag(m["B1+"], r"the whole body, \\ bending and breathing", TUNE, dx=0.5))
        t_hill = tag(m["hill"], r"a broad hill: \ the bridge \\ and the wood under it", GOOD)
        strings = VGroup(*[VGroup(Line(g.at(f, -38), g.at(f, -34.5), color=STR, stroke_width=3), label(n, font_size=20, color=STR).next_to(g.at(f, -34.5), UP, buff=0.06)) for n, f in d["strings"].items()])
        sl = label(r"the four open strings", font_size=20, color=STR).next_to(strings, RIGHT, buff=0.3)
        head = label(r"A violin's body, \ driven at the bridge", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Back to the box. In chapter two a guitar's body turned out to be a filter with two strong "
            "resonances. A violin's body is the same kind of thing with more going on, and this is its "
            "response: how strongly it answers when the bridge is pushed at each frequency. "
            "<bookmark mark='a'/> Lowest, near two hundred and seventy-five hertz, is the air in the box, "
            "moving in and out through the f-holes: the bottle again. <bookmark mark='b'/> Next, between four "
            "and six hundred hertz, a pair of resonances in which the whole wooden body bends and breathes. "
            "Violin makers call these three the signature modes, and can tell you their frequencies for an "
            "instrument on the bench. <bookmark mark='c'/> Above them the peaks crowd together into a thicket, "
            "and between two and three thousand hertz the whole thicket rises in a broad hill, shaped by the "
            "bridge and the wood beneath it. Part 4 showed that the ear is at its most sensitive just there. "
            "That hill is the violin's brilliance, its ability to be heard over an orchestra. "
            "<bookmark mark='d'/> Now look where the strings are. The lowest note of the violin, the open G, is "
            "below every resonance of the body. The box hardly radiates its fundamental at all. You hear a "
            "low G anyway, for the reason Part 4 gave: the ear rebuilds a missing fundamental from the "
            "partials above it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(cu), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(t_air))
            vo.wait_until("b")
            self.play(FadeIn(t_wood))
            vo.wait_until("c")
            self.play(FadeIn(t_hill))
            vo.wait_until("d")
            self.play(FadeIn(strings), FadeIn(sl))
            self.play(Indicate(strings[0], color=WHITE, scale_factor=1.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vibrato(self):
        d, g, cu = self.graph(y_length=2.3, x_length=10.6, top=4)
        VGroup(g, cu).move_to(UP * 1.75)
        hz = d["hz"]
        lf, db = np.log(d["f"]), d["db"]
        at = lambda f: float(np.interp(np.log(f), lf, db))  # noqa: E731
        saw = [-20 * np.log10(n) for n in range(1, 11)]
        lines = VGroup(*[Line(g.at(n * hz, -38), g.at(n * hz, at(n * hz)), color=BOWED, stroke_width=2) for n in range(1, 11)])
        base_y, unit, x0, dx, w = -2.45, 2.1 / 40.0, -5.9, 0.8, 0.46
        floor = -40.0

        def level(n, cents):
            return saw[n - 1] + at(n * hz * 2 ** (cents / 1200.0))

        top = max(level(n, 0) for n in range(1, 11))
        bars = VGroup(*[Rectangle(width=w, height=0.1, stroke_width=0, fill_color=BOWED, fill_opacity=0.9) for _ in range(10)])
        nums = VGroup(*[label(str(n), font_size=20, color=GREY_B).move_to(RIGHT * (x0 + dx * (n - 1)) + UP * (base_y - 0.22)) for n in range(1, 11)])

        def set_bars(m, cents):
            for n, b in enumerate(m, start=1):
                h = max((level(n, cents) - top - floor) * unit, 0.03)
                b.stretch_to_fit_height(h)
                b.move_to(RIGHT * (x0 + dx * (n - 1)) + UP * (base_y + h / 2))
            return m

        set_bars(bars, 0.0)
        bl = label(r"the ten partials of the note A, \ as they leave the violin", font_size=22, color=GREY_B).move_to(RIGHT * (x0 + 4.5 * dx) + UP * (base_y - 0.58))
        ext = VGroup(*[VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=WHITE, stroke_width=1.5).move_to(RIGHT * (x0 + dx * (n - 1)) + UP * (base_y + max((level(n, s * 30) - top - floor) * unit, 0.03))) for s in (-1, 1)) for n in range(1, 11)])
        note = listen_note(r"One bowed note: \\ held still, \ then with vibrato. \\ Listen to the colour \\ of the second, \ not only its pitch.", width=4.4, font_size=26).move_to(RIGHT * 4.5 + DOWN * 1.5)
        c = clip("violin.vibrato")
        with self.voiceover(
            "All those narrow peaks do something that no smooth filter could. A violinist's left hand rocks on "
            "the string, five or six times a second, and the pitch of the note slides up and down by a "
            "fraction of a semitone. That is vibrato. <bookmark mark='a'/> Here is the note A, with its ten "
            "partials standing on the body's response. Slide the pitch a little, and every partial slides "
            "along the curve. One that sits on the upward side of a peak gets louder as the pitch rises. Its "
            "neighbour, on the downward side of another peak, gets quieter at the same moment. "
            "<bookmark mark='b'/> So with every wobble of the finger the recipe of the note changes: some "
            f"partials swell while others fade, in this model by up to {say(d['largest_swing'])} decibels. Listen "
            "to the same bowed note, first held still and then with vibrato, and watch the partials."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cu))
            vo.wait_until("a")
            self.play(FadeIn(lines), FadeIn(bars), FadeIn(nums), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(ext), FadeIn(note))
        rate, depth = 5.6, 30.0
        with self.listen(c) as snd:
            window(snd, r"one bowed A: \ still, \ then with vibrato", detail=r"a model violin", corner=DL, tag_corner=UR)
            t0 = snd.time_of("vibrato")

            def wob(m, t):
                tt = t - t0
                on = float(np.clip((tt - 0.25) / 0.4, 0, 1)) if 0 <= tt <= 2.4 else 0.0
                return set_bars(m, on * depth * np.sin(2 * np.pi * rate * tt))

            snd.drive(bars, wob)
        set_bars(bars, 0.0)
        with self.voiceover(
            "The first note is in tune and lifeless. The second shimmers, and what shimmers is not the pitch: "
            "it is the tone colour, changing six times a second. In 1973 Max Mathews, the father of computer "
            "music, built an electronic violin whose body was a bank of electrical resonances, and found that "
            "without sharp peaks like these it did not sound like a violin, however good the string. The "
            "lumpiness of the box is not a defect. It is the instrument."
        ):
            self.play(FadeOut(note), FadeOut(ext))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wolf(self):
        head = label(r"The box talks back", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"the bargain", r"chapter 1: \ a body must take energy from the string to make sound, \\ but not so fast that the string cannot keep its motion."),
            (r"the wolf note", r"play the note of the strongest body resonance: \ the box drains the string \\ faster than the bow can feed it. \ The note stutters and howls, \ several times a second."),
            (r"where it lives", r"on most cellos, \ near F or F sharp on the G string. \\ The cure is a small weight on the string, \ behind the bridge."),
            (r"the maker's craft", r"plates carved and tapped until the signature modes sit where they should, \\ strong enough to sing, \ not strong enough to howl."),
        ], left=-6.5, text_left=-3.3, top=1.9, step=1.4, name_size=28, text_size=23, color=WOOD)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "One last thing about the box: it talks back to the string. <bookmark mark='a'/> Remember the "
            "bargain from the first chapter. A body has to take energy from the string, or there is no sound. "
            "But the bowed string's motion depends on waves coming back from the bridge almost undiminished. "
            "<bookmark mark='b'/> Play the very note of the body's strongest resonance, and the bridge moves so "
            "much that the box drains the string faster than the bow can feed it. The Helmholtz motion "
            "collapses, the body's motion dies down, the string recovers, and round it goes, several times a "
            "second: a stuttering howl called the wolf. In Schelleng's diagram, the minimum force has risen to "
            "meet the maximum. <bookmark mark='c'/> Most cellos have one, near F or F sharp, and cellists tame "
            "it with a small weight clamped to the string behind the bridge. <bookmark mark='d'/> So a violin "
            "maker, carving and tapping the plates, is steering between two failures: resonances too weak to "
            "sing, and resonances strong enough to howl."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
