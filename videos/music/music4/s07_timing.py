from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403


class Timing(SoundScene):
    def construct(self):
        chapter(self, 6, r"A second clock", r"Is place the ear's only way of measuring frequency?", lit=(1863,),
                extra=((1930, r"Wever and Bray: \ the nerve follows the wave"),))
        self.volley()
        self.locking()
        self.jnd()

    # ------------------------------------------------------------------
    def volley(self):
        d = load("locking")
        w = 9.6
        x0 = LEFT * 3.7
        n = len(d["drive_250"])
        t = np.linspace(0, 1, n)

        def strip(y, top, h, col):
            pts = [x0 + RIGHT * w * a + UP * (top + h * v) for a, v in zip(t[::4], y[::4])]
            m = VMobject(stroke_color=col, stroke_width=3)
            m.set_points_as_corners(pts)
            return m

        wave = strip(d["drive_250"], 2.3, 0.55, TUNE)
        nerve = strip(d["nerve_250"], 0.55, 0.9, EAR)
        base = Line(x0 + UP * 0.55, x0 + RIGHT * w + UP * 0.55, color=GREY_D, stroke_width=1)
        ticks = VGroup(*[Line(ORIGIN, UP * 0.2, color=WHITE, stroke_width=2.5).move_to(x0 + RIGHT * w * x + DOWN * (0.45 + 0.27 * r))
                         for x, r in zip(d["raster_x_250"], d["raster_row_250"])])
        names = VGroup(label(r"the membrane's motion: \\ 250 Hz, \ four cycles", font_size=22, color=TUNE).next_to(x0 + UP * 2.3, LEFT, buff=0.3),
                       label(r"what one hair cell \\ passes on", font_size=22, color=EAR).next_to(x0 + UP * 0.95, LEFT, buff=0.3),
                       label(r"ten nerve fibres \\ from that place", font_size=22, color=WHITE).next_to(x0 + DOWN * 1.65, LEFT, buff=0.3))
        crests = VGroup(*[DashedLine(x0 + RIGHT * w * (k + 0.25) / 4 + UP * 3.0, x0 + RIGHT * w * (k + 0.25) / 4 + DOWN * 3.05, color=GREY_C, stroke_width=1.2, dash_length=0.06)
                          for k in range(4)])
        say_ = label(r"no fibre fires on every cycle. \ Together they mark every one.", font_size=28, color=GOOD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "So far the ear is a row of filters, and a frequency is a place. But the nerve carries a second "
            "message, and it was found by accident. <bookmark mark='a'/> Here is the membrane at one place, "
            "moving up and down two hundred and fifty times a second. A hair cell is not a symmetrical device. "
            "Its hairs open their channels when they are bent one way, and close them when bent the other. "
            "<bookmark mark='b'/> So the cell passes on only half of each cycle: a pulse for every crest of the "
            "wave, and nothing for the troughs. <bookmark mark='c'/> Now the nerve fibres. A single fibre cannot "
            "fire two hundred and fifty times a second for long, and it does not try. It fires on some cycles and "
            "skips others. But when it does fire, it fires near the crest. <bookmark mark='d'/> Look down any of "
            "these lines. No one fibre marks every cycle, but ten fibres together mark every one of them. The "
            "wave's period is written in the timing of the spikes. In 1930 Ernest Wever and Charles Bray put a "
            "wire on a cat's auditory nerve and connected it to a loudspeaker in another room. What came out of "
            "the loudspeaker was the speech going into the cat's ear. Much of that signal turned out to come from "
            "the hair cells themselves, but it started the search, and the nerve's volleys were found soon after."
        ) as vo:
            sofar = VGroup(label(r"the first code: \ \ which fibres are firing", font_size=34, color=GREY_A),
                           label(r"a frequency is a place", font_size=28, color=GREY_B),
                           label(r"the second code?", font_size=38, color=EAR)).arrange(DOWN, buff=0.45)
            self.play(FadeIn(sofar[0]), FadeIn(sofar[1]))
            self.play(FadeIn(sofar[2]))
            vo.wait_until("a")
            self.play(FadeOut(sofar), run_time=0.4)
            self.play(Create(wave), FadeIn(names[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(nerve), FadeIn(base), FadeIn(names[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(k) for k in ticks], lag_ratio=0.03), FadeIn(names[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(c) for c in crests], lag_ratio=0.3), FadeIn(say_), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def locking(self):
        d = load("locking")
        hs = VGroup()
        for hz, col in ((250, AIR), (1000, TUNE), (4000, BAD)):
            h = d[f"hist_{hz}"]
            h = np.roll(h, 6 - int(np.argmax(h)))
            bars = VGroup(*[Rectangle(width=0.14, height=max(1.5 * v, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.9) for v in h]).arrange(RIGHT, buff=0.03, aligned_edge=DOWN)
            base = Line(bars.get_corner(DL), bars.get_corner(DR), color=GREY_C, stroke_width=1.5)
            cyc = FunctionGraph(lambda x: 0.16 * np.sin(2 * np.pi * x / bars.width), x_range=[0, bars.width], color=GREY_B, stroke_width=1.5)
            cyc.next_to(base, DOWN, buff=0.12)
            hs.add(VGroup(bars, base, cyc, label(rf"${hz_name(hz)}$ Hz", font_size=26, color=col).next_to(bars, UP, buff=0.5)))
        hs.arrange(RIGHT, buff=0.7).move_to(LEFT * 2.9 + UP * 1.75)
        hl = label(r"where in the cycle the spikes fall", font_size=24, color=GREY_A).next_to(hs, DOWN, buff=0.25)
        rows = d["rows"]
        g = faxes(200, 10000, [0, 1], x_length=6.2, y_length=1.9, ylabel=r"how closely the spikes follow the wave", yticks=[0, 0.5, 1],
                  fticks=(250, 500, 1000, 2000, 4000, 8000), font_size=20)
        g.move_to(LEFT * 2.9 + DOWN * 2.15)
        cu = fcurve(g, [r["hz"] for r in rows], [r["synchrony"] for r in rows], EAR)
        dots = VGroup(*[Dot(g.at(r["hz"], r["synchrony"]), radius=0.07, color=EAR) for r in rows])
        notes = VGroup(label(r"a hair cell cannot change its voltage \\ much faster than about \\ a thousand times a second", font_size=24, color=GREY_A),
                       label(r"in the animals measured: \\ strong below 1 kHz, \\ gone by about 5 kHz", font_size=24, color=EAR),
                       label(r"nobody has recorded from \\ single fibres in a human", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.45).move_to(RIGHT * 4.3 + DOWN * 0.3)
        r = {int(x["hz"]): x["synchrony"] for x in rows}
        with self.voiceover(
            "Does this work at every frequency? Take every spike from many fibres and ask where in the wave's "
            "cycle it fell. <bookmark mark='a'/> At two hundred and fifty hertz the spikes pile up in one part "
            "of the cycle. At a thousand, the pile is broader. At four thousand it is almost flat: the spikes "
            "come at any moment, and their timing says nothing. <bookmark mark='b'/> The reason is electrical. A "
            "hair cell cannot change its voltage much faster than about a thousand times a second, so above "
            "that, the crests blur into one another. <bookmark mark='c'/> This is Monochord's model. On a scale "
            f"from nought to one, its timing scores {say(r[250], 2)} at two hundred and fifty hertz, "
            f"{say(r[1000], 2)} at a thousand, and {say(r[4000], 2)} at four thousand. Recordings from single "
            "fibres in cats and monkeys have the same shape: strong below a thousand hertz, fading, and gone "
            "by about five thousand. In humans it has never been measured directly, and the exact limit is "
            "still argued over. But the shape is not in doubt. The ear has a clock, and the clock stops."
        ) as vo:
            self.play(FadeIn(hl), *[FadeIn(h[1]) for h in hs], *[FadeIn(h[2]) for h in hs], *[FadeIn(h[3]) for h in hs])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h[0]) for h in hs], lag_ratio=0.6), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(g), Create(cu), FadeIn(dots), FadeIn(notes[1]), run_time=1.5)
            self.wait(max(vo.remaining() - 9.0, 0.1))
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def jnd(self):
        d = load("locking")
        c = clip("locking.jnd")
        q = listen_card(r"Two pairs of tones near 1000 Hz, \ A and B. \\ In each pair: \ does the second tone go up, \ or down?", width=9.4).to_edge(UP, buff=0.45)
        bx = boxes(buff=2.0, width=3.0, height=1.5).move_to(DOWN * 0.3)
        with self.voiceover(
            "Why would the ear need a second way to measure frequency? Try this. Two pairs of tones, both near a "
            "thousand hertz. In each pair the second tone is slightly different from the first. Does it go up, "
            "or down?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"pair A, \ then pair B", kind="synthesized", detail=r"pure tones near 1000 Hz", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 1.52)
        up = d["steps"]["A"]
        facts = VGroup(label(rf"a practised listener can tell 1000 Hz from {1000 + d['jnd_hz']:.0f} Hz", font_size=28),
                       label(rf"the ear's filter there is {d['erb_1k']:.0f} Hz wide", font_size=28, color=BAD),
                       label(rf"the ear measures {d['erb_1k'] / d['jnd_hz']:.0f} times finer than its own ruler", font_size=30, color=GOOD)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.5)
        with self.voiceover(
            "In A the second tone went up, by ten hertz. In B it went down, by three. If you caught B, think "
            "about what you just did. <bookmark mark='a'/> A practised listener can tell a thousand hertz from a "
            f"thousand and two: a thirtieth of a semitone. <bookmark mark='b'/> But the filter that those tones "
            f"pass through is {say(d['erb_1k'])} hertz wide. <bookmark mark='c'/> The ear is measuring "
            f"{say(d['erb_1k'] / d['jnd_hz'])} times more finely than its own ruler. There are two ways it could "
            "do that. It could compare how strongly neighbouring places respond: a tiny shift of a broad hump is "
            "still a shift. Or it could read the timing of the spikes, where a thousand hertz and a thousand and "
            "two differ by two millionths of a second in every cycle. The evidence says it does both, and that "
            "timing matters most. Because above four or five thousand hertz, exactly where the clock stops, our "
            "ability to tell frequencies apart gets suddenly worse. And something else goes with it, as you will "
            "hear in chapter eight."
        ) as vo:
            self.play(FadeOut(q), bx.animate.shift(UP * 1.9))
            ans = VGroup(label(rf"up: \ 1000 $\rightarrow$ {1000 * 2 ** (up / 1200):.0f} Hz", font_size=28, color=GOOD).next_to(bx[0], DOWN, buff=0.25),
                         label(rf"down: \ 1000 $\rightarrow$ {d['b_hz']:.0f} Hz", font_size=28, color=GOOD).next_to(bx[1], DOWN, buff=0.25))
            self.play(FadeIn(ans))
            vo.wait_until("a")
            self.play(FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        self.wait(0.3)
        self.clear_scene()
