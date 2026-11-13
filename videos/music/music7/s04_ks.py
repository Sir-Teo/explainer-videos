from __future__ import annotations

import numpy as np

from videos.music.music7.common import *  # noqa: F403


class Karplus(SoundScene):
    def construct(self):
        chapter(self, 3, r"A pluck in three lines", r"How little does it take to compute a plucked string?", lit=(1983,))
        self.idea()
        self.listen_ks()
        self.why()

    # ------------------------------------------------------------------
    def idea(self):
        d = load("ks")
        card = history_card(1983, r"Kevin Karplus and Alex Strong, \ Stanford",
                            r"two students with a home computer too slow for any known way of making a plucked sound.", width=5.4, font_size=20).to_corner(UL, buff=0.4)
        code = code_block([f"line = noise({d['delay']})     # one period",
                           "repeat:",
                           "    out  = line[0]",
                           "    line = line[1:] + [(line[0] + line[1]) / 2]"], font_size=20).to_corner(UR, buff=0.5)
        ring = Circle(radius=1.5, color=GREY_C, stroke_width=2).move_to(LEFT * 3.4 + DOWN * 1.5)
        cells = VGroup(*[Line(ring.point_at_angle(TAU * k / 48) * 1.0, ring.get_center() + (ring.point_at_angle(TAU * k / 48) - ring.get_center()) * (1 + 0.28 * np.sin(k * 12.9898) * np.cos(k * 4.1)),
                              color=TUNE, stroke_width=3) for k in range(48)])
        avg = VGroup(RoundedRectangle(width=1.5, height=0.6, corner_radius=0.1, stroke_color=GOOD, stroke_width=2), label(r"average", font_size=22, color=GOOD))
        avg[1].move_to(avg[0])
        avg.move_to(ring.get_center() + UP * 2.25)
        out = VGroup(Arrow(ring.get_right(), ring.get_right() + RIGHT * 1.4, buff=0.05, color=GREY_A, stroke_width=3), label(r"sound out", font_size=22, color=GREY_A))
        out[1].next_to(out[0], UP, buff=0.08)
        steps = VGroup(label(r"1. \ fill a delay line, \ one period long, \ with noise", font_size=26), label(r"2. \ play what comes out of the end", font_size=26),
                       label(r"3. \ put it back in at the start, \ averaged with its neighbour", font_size=26)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(RIGHT * 3.0 + DOWN * 1.4)
        with self.voiceover(
            "Before we go on to hammers and bows, a detour into a computer, because it shows how little a "
            "plucked string really is. In 1983 two Stanford students, Kevin Karplus and Alex Strong, wanted a "
            "plucked-string sound from a home computer that was far too slow for anything like the simulations "
            "of Part 1. What they found takes three lines. <bookmark mark='a'/> Take a strip of memory as long "
            "as one period of the note you want, and fill it with random numbers. <bookmark mark='b'/> Play the "
            "number at the end. <bookmark mark='c'/> Then put it back in at the beginning, averaged with its "
            "neighbour. And go round again, for ever. That is the whole algorithm: no multiplication, no "
            "sine, no table."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(code), FadeIn(ring), LaggedStart(*[Create(c_) for c_ in cells], lag_ratio=0.02), FadeIn(steps[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(GrowArrow(out[0]), FadeIn(out[1]), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(avg), FadeIn(steps[2]), Rotate(cells, angle=-TAU / 4, about_point=ring.get_center()), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listen_ks(self):
        d = load("ks")
        c = clip("ks.demo")
        laps, nums = d["laps"], d["lap_numbers"]
        g = axes([0, 1], [-1.15, 1.15], x_length=9.6, y_length=3.0, xlabel=r"what is in the delay line", ylabel="", xticks=None, yticks=[], font_size=20)
        g.move_to(UP * 0.4)
        x = np.linspace(0, 1, laps.shape[1])
        tr = VMobject(stroke_color=TUNE, stroke_width=2.5)
        tr.set_points_as_corners([g.ax.c2p(a, b) for a, b in zip(x, laps[0])])
        count = label(r"lap 0: \ noise", font_size=30, color=GREY_A).next_to(g, DOWN, buff=0.75)
        with self.voiceover(
            f"Here it is, on a G. The picture is what the strip of memory holds, {d['delay']} numbers, lap after "
            "lap. Then you will hear the opening of the Tune, played the same way."
        ):
            self.play(FadeIn(g), FadeIn(tr), FadeIn(count))
        hz = d["hz"]

        def draw(m, t):
            lap = max(t, 0.0) * hz
            k = int(np.searchsorted(nums, lap, side="right") - 1)
            k = min(max(k, 0), len(nums) - 1)
            m.set_points_as_corners([g.ax.c2p(a, b) for a, b in zip(x, laps[k])])

        with self.listen(c) as snd:
            window(snd, r"Karplus and Strong: \ one note, \ then the Tune", kind="synthesized", detail=r"noise in a delay line", corner=DL, tag_corner=DR)
            snd.drive(tr, draw)
            tt = snd.time_of("tune")
            snd.wait_until(0.9)
            self.remove(count)
            count = label(r"lap 170: \ smoother", font_size=30, color=GREY_A).move_to(count)
            self.add(count)
            snd.wait_until(tt)
            self.remove(count)
            count = label(r"the Tune, \ by the same three lines", font_size=30, color=TUNE).move_to(count)
            self.add(count)
            snd.drive(tr, lambda m, t: draw(m, (t - tt) % 0.55))
        with self.voiceover(
            "It starts as a burst of noise, bright and sharp, and within a few dozen laps the jagged line has "
            "been smoothed into something close to a sine wave: the brightness fades and a clear pitch is left. "
            "Which is just what a plucked string does. It was the sound of every plucked instrument in the "
            "computer music and the video games of the nineteen eighties."
        ):
            self.play(Indicate(tr, color=WHITE, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        d = load("ks")
        rows = VGroup(
            VGroup(label(r"the strip of memory", font_size=30, color=TUNE), label(r"is d'Alembert's travelling wave (Part 1): \ a shape going round the string and back", font_size=25, color=GREY_A)),
            VGroup(label(r"the noise", font_size=30, color=TUNE), label(r"is the pluck: \ energy in every partial at once", font_size=25, color=GREY_A)),
            VGroup(label(r"the average", font_size=30, color=TUNE), label(r"is the loss at the bridge: \ it takes most from the highest partials, \ every lap", font_size=25, color=GREY_A)),
        )
        for k, r in enumerate(rows):
            r[0].move_to(LEFT * 6.2 + UP * (1.9 - 0.95 * k), aligned_edge=LEFT)
            r[1].move_to(LEFT * 2.6 + UP * (1.9 - 0.95 * k), aligned_edge=LEFT)
        flaw = VGroup(label(rf"its flaw: \ the delay is a whole number of samples. \ Asked for {d['hz']:.0f} Hz, \ it plays {d['true_hz']:.1f}: \ {d['off_cents']:.0f} cents sharp", font_size=25, color=BAD),
                      label(r"the cure: \ a filter that delays by a fraction of a sample", font_size=25, color=GREY_A)).arrange(DOWN, buff=0.12).move_to(DOWN * 1.2)
        grown = label(r"grown up, \ it is the \textbf{digital waveguide}: \ two delay lines, \ a filter at each end, \ and something in the middle", font_size=27, color=GOOD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Why does it work? Because each line of it is a piece of physics we already know. "
            "<bookmark mark='a'/> The strip of memory is d'Alembert's travelling wave from Part 1: a shape going "
            "down the string and back, once in each period. <bookmark mark='b'/> The noise is the pluck, which "
            "puts energy into every partial at once. <bookmark mark='c'/> And the average is the loss at the "
            "bridge, which takes a little from every partial on every lap, and most from the highest. "
            f"<bookmark mark='d'/> It has a flaw. The strip is a whole number of samples long, so most pitches "
            f"come out slightly wrong: asked for a hundred and ninety-six hertz, it plays "
            f"{say(d['true_hz'], 1)}. Parts 5 and 6 tell you that this matters. The cure is a small filter that "
            "delays by a fraction of a sample. <bookmark mark='e'/> With that, with a better loss filter and "
            "with a second strip for the wave going the other way, the toy becomes a serious method: the "
            "digital waveguide, worked out by Julius Smith in the same building. Its strength is that you can "
            "put something in the middle of the string. A finger. A hammer. A bow. That is how the rest of "
            "this part's instruments are made."
        ) as vo:
            head = label(r"Why three lines are enough", font_size=36, color=GREY_A).to_edge(UP, buff=0.35)
            self.play(FadeIn(head), run_time=0.5)
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(flaw))
            vo.wait_until("e")
            self.play(FadeIn(grown))
        self.wait(0.3)
        self.clear_scene()
