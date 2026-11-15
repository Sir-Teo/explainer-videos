from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403


class Room(SoundScene):
    def construct(self):
        chapter(self, 6, r"The room's response", r"What happens to a sound in a room?")
        self.images()
        self.response()
        self.precedence()
        self.hear()
        self.decay()
        self.sabine_()
        self.modes()

    # ------------------------------------------------------------------
    def images(self):
        W, H = 2.6, 2.1
        sc = 1.15
        room = Rectangle(width=W * sc, height=H * sc, stroke_color=WHITE, stroke_width=3)
        grid = VGroup()
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    continue
                grid.add(Rectangle(width=W * sc, height=H * sc, stroke_color=GREY_B, stroke_width=1, stroke_opacity=0.5).shift(RIGHT * i * W * sc + UP * j * H * sc))
        src = np.array([0.6, 0.7])
        mic = np.array([1.9, 1.4])
        def P(x, y):
            return np.array([(x - W / 2) * sc, (y - H / 2) * sc, 0])
        imgs = VGroup()
        for i in range(-2, 3):
            for j in range(-2, 3):
                x = (src[0] if i % 2 == 0 else W - src[0]) + i * W
                y = (src[1] if j % 2 == 0 else H - src[1]) + j * H
                imgs.add(Dot(P(x, y), radius=0.06 if (i, j) != (0, 0) else 0.09, color=TUNE if (i, j) != (0, 0) else WHITE))
        m = Dot(P(*mic), radius=0.09, color=BLUE)
        rays = VGroup(*[Line(d.get_center(), m.get_center(), color=TUNE, stroke_width=1, stroke_opacity=0.5) for d in imgs])
        lab = VGroup(label(r"source", font_size=16, color=WHITE).next_to(imgs[12], DOWN, buff=0.08), label(r"microphone", font_size=16, color=BLUE).next_to(m, UP, buff=0.08))
        head = label(r"the image-source method, \ seen from above", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "How does a room respond to a click? Jont Allen and David Berkley gave a beautiful answer in 1979 for a "
            "rectangular room. <bookmark mark='a'/> A wall is a mirror: sound reflected from it seems to come from an image of "
            "the source behind the wall. <bookmark mark='b'/> Reflect the room in every wall, and those rooms in theirs, and "
            "you get a lattice of images. <bookmark mark='c'/> Each image's sound arrives at the microphone straight, after "
            "its distance divided by the speed of sound, weakened by distance and by every wall it passed through. The "
            "impulse response is the sum of all of them: thousands, then millions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(room), FadeIn(imgs[12]), FadeIn(m), FadeIn(lab))
            vo.wait_until("a")
            self.play(FadeIn(grid[:8]), FadeIn(VGroup(*[d for i, d in enumerate(imgs) if i in (7, 11, 13, 17)])))
            vo.wait_until("b")
            self.play(FadeIn(grid), FadeIn(imgs))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.05), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def response(self):
        d = load("room")
        ir = np.array(d["ir"])
        t = np.arange(len(ir)) * 24 / 48000 * 1000
        ax = frame_axes(width=11.0, height=3.0, xlo=0, xhi=250, ylo=-1, yhi=1, center=DOWN * 0.5)
        cv = curve(t, ir, ax.to, color=TUNE, width=1.2)
        ticks = VGroup(*[label(f"{v} ms", font_size=15, color=GREY_A).next_to(ax.to(v, -1), DOWN, buff=0.1) for v in (0, 50, 100, 150, 200, 250)])
        direct = VGroup(Arrow(ax.to(d["direct_ms"] + 15, 1.2), ax.to(d["direct_ms"], 0.85), buff=0, color=WHITE, stroke_width=3),
                        label(rf"the direct sound, \ {d['direct_ms']:.1f} ms", font_size=16, color=WHITE).next_to(ax.to(d["direct_ms"] + 15, 1.2), RIGHT, buff=0.1))
        early = label(r"early reflections: \ separate, \ countable", font_size=16, color=EAR).move_to(ax.to(40, 1.25))
        late = label(r"the late tail: \ dense as noise, \ dying away", font_size=16, color=BLUE).move_to(ax.to(170, 0.8))
        head = label(rf"a tiled room, \ {d['dims'][0]} by {d['dims'][1]} by {d['dims'][2]} m, \ its walls absorbing {100 * d['alpha']:.0f}\%", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the first quarter second of our tiled room's impulse response: a room two point six by two point one by "
            "two point five metres, every wall absorbing five per cent of the sound that strikes it. <bookmark mark='a'/> The "
            f"direct sound arrives after {say(d['direct_ms'], 1)} milliseconds. <bookmark mark='b'/> Then the early "
            "reflections, from the nearest walls, each one separate. <bookmark mark='c'/> Soon they arrive so thick that they "
            "blur into a tail, dense as noise, dying away."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), Create(cv), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(direct))
            vo.wait_until("b")
            self.play(FadeIn(early))
            vo.wait_until("c")
            self.play(FadeIn(late))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("room")
        c = clip("room.two")
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.4, height=1.3, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(ORIGIN)
                         for t in (r"dry", r"in the tiled room")]).arrange(RIGHT, buff=1.4).move_to(UP * 0.3)
        cap = label(r"the dry phrase convolved with the room's impulse response", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"the room, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Convolve the dry Tune with that response, and you are in the room. Dry, then in the tiled room."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"dry, \ then the room", kind="synthesized", detail=r"Part 7's piano, \ image sources", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["dry"], st["room"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["room"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decay(self):
        d = load("room")
        e = np.array(d["edc"])
        t = np.arange(len(e)) * 240 / 48000
        ax = frame_axes(width=9.0, height=3.4, xlo=0, xhi=1.6, ylo=-80, yhi=0, center=DOWN * 0.4)
        cv = curve(t, np.clip(e, -80, 0), ax.to, color=TUNE, width=3)
        ticks = VGroup(*[label(f"{v:g} s", font_size=15, color=GREY_A).next_to(ax.to(v, -80), DOWN, buff=0.1) for v in (0, 0.4, 0.8, 1.2, 1.6)],
                       *[label(f"{v} dB", font_size=15, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (0, -20, -40, -60)])
        rt = d["rt60"]
        line = DashedLine(ax.to(0, 0), ax.to(rt, -60), color=WHITE, stroke_width=2)
        mark = VGroup(DashedLine(ax.to(rt, -60), ax.to(rt, -80), color=EAR, stroke_width=2), label(rf"60 dB down at {rt:.2f} s", font_size=17, color=EAR).next_to(ax.to(rt, -60), RIGHT, buff=0.2))
        eq = MathTex(r"E(t) = \int_t^{\infty} h^2(\tau)\,d\tau", font_size=34).to_corner(UR, buff=0.6).shift(DOWN * 0.6)
        head = label(r"Schroeder's backward integration", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How long does the room ring? Schroeder showed in 1965 how to read it cleanly from the impulse response: "
            "<bookmark mark='a'/> add up the energy still to come, from each moment to the end. In decibels, it falls along "
            "a nearly straight line. <bookmark mark='b'/> The time it takes to fall sixty decibels is the reverberation time, "
            f"RT sixty: here {say(rt, 2)} seconds, measured on the stretch from minus five to minus twenty-five decibels and "
            "extended."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(eq))
            vo.wait_until("a")
            self.play(Create(cv), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(mark))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modes(self):
        d = load("bands")
        items = [
            (r"at low frequencies a small room is a set of resonances, \ its modes, \ spaced far apart", WHITE),
            (r"Schroeder's frequency marks where the modes overlap into a smooth response: \ $2000\sqrt{T_{60}/V}$", WHITE),
            (rf"for our tiled room: \ $2000\sqrt{{{d['rt60']:.2f}/{d['V']:.1f}}} \approx {d['schroeder_freq']:.0f}$ Hz", TUNE),
            (r"below it, \ some bass notes boom and others vanish, \ depending where you stand", WHITE),
            (r"a cathedral's Schroeder frequency is a few tens of hertz; \ a bathroom's is in the middle of a singer's range", GREY_A),
        ]
        rows_scene(self, r"the room's colour: \ its modes", items,
                   "One more feature of small rooms. <bookmark mark='b'/> At low frequencies a room is a set of resonances, its "
                   "modes, spaced far apart. <bookmark mark='c'/> Schroeder's frequency marks where the modes overlap into a smooth "
                   "response: two thousand times the square root of the reverberation time over the volume. "
                   f"<bookmark mark='d'/> For our tiled room that is about {say(d['schroeder_freq'])} hertz. "
                   "<bookmark mark='e'/> Below it, some bass notes boom and others vanish, depending where you stand. "
                   "<bookmark mark='f'/> A cathedral's Schroeder frequency is a few tens of hertz; a bathroom's is in the middle of "
                   "a singer's range, which is why people like singing there.", marks="bcdef")

    # ------------------------------------------------------------------
    def sabine_(self):
        d = load("room")
        rows_ = text_rows([
            (r"Wallace Sabine \ (1900): \ RT60 $= 0.161\,V / (S\,\alpha)$, \ from timing organ pipes in Harvard's lecture halls", WHITE),
            (rf"our room: \ $V = {d['V']:.1f}$ m$^3$, \ $S = {d['S']:.1f}$ m$^2$, \ $\alpha = {d['alpha']}$: \ Sabine predicts {d['sabine']:.2f} s", WHITE),
            (rf"Carl Eyring \ (1930), \ for rooms that absorb more: \ $0.161\,V / (-S \ln(1 - \alpha))$, \ {d['eyring']:.2f} s", WHITE),
            (rf"the simulated room measured {d['rt60']:.2f} s: \ within {100 * abs(d['rt60'] / d['eyring'] - 1):.0f}\% of Eyring", TUNE),
            (r"both formulas assume sound arrives from every direction equally; \ real rooms with awkward shapes stray from them", GREY_A),
        ], font_size=21)
        head = label(r"Sabine's law, \ checked", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "There is a classical prediction to check it against. <bookmark mark='a'/> Wallace Sabine, timing organ pipes in "
            "Harvard's lecture halls in 1900, found that the reverberation time is point one six one times the volume, over "
            "the total absorbing area. <bookmark mark='b'/> For our room that predicts "
            f"{say(d['sabine'], 2)} seconds. <bookmark mark='c'/> Carl Eyring's 1930 correction, better when walls absorb "
            f"more, predicts {say(d['eyring'], 2)}. <bookmark mark='d'/> The simulated room measured {say(d['rt60'], 2)}: "
            "within a few per cent. <bookmark mark='e'/> Both formulas assume sound arrives from every direction equally, "
            "and real rooms with awkward shapes or uneven absorption stray from them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def precedence(self):
        items = [
            (r"we hear the direct sound and dozens of reflections, \ yet hear one source, \ in one place", WHITE),
            (r"the precedence effect \ (Wallach and colleagues, \ 1949; \ Haas, \ 1951): \ the first arrival fixes where a sound is", WHITE),
            (r"reflections within a few tens of milliseconds fuse with it, \ adding loudness and colour, \ not a second place", WHITE),
            (r"later ones are heard as the room: \ its size from the early gaps, \ its material from the tail", TUNE),
            (r"Part 45's auditory scene, \ applied to walls", GREY_A),
        ]
        rows_scene(self, r"how we hear a room", items,
                   "How do we hear all this? <bookmark mark='b'/> We receive the direct sound and dozens of reflections, yet we "
                   "hear one source in one place. <bookmark mark='c'/> The precedence effect, described by Hans Wallach and "
                   "colleagues in 1949 and by Helmut Haas in 1951: the first arrival fixes where a sound is. "
                   "<bookmark mark='d'/> Reflections arriving within a few tens of milliseconds fuse with it, adding loudness and "
                   "colour, not a second place. <bookmark mark='e'/> Later ones are heard as the room: its size from the early "
                   "gaps, its material from the tail. <bookmark mark='f'/> It is Part 45's auditory scene, applied to walls.",
                   marks="bcdef")
