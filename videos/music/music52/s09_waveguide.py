from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403


class Waveguide(SoundScene):
    def construct(self):
        chapter(self, 8, r"Digital waveguides", r"Can a string be computed with two delay lines?")
        self.rails()
        self.exact()
        self.winds()
        self.threshold()
        self.heard()
        self.industry()

    # ------------------------------------------------------------------
    def rails(self):
        d = load("waveguide")
        sh = np.array(d["shape"])
        M = len(sh)
        w = 10.0
        xs = np.linspace(-w / 2, w / 2, M)
        top = VMobject(stroke_color=TUNE, stroke_width=3).set_points_as_corners([[x, 1.2 + 0.9 * y / 2, 0] for x, y in zip(xs, sh)])
        bot = VMobject(stroke_color=BLUE, stroke_width=3).set_points_as_corners([[x, -0.6 + 0.9 * y / 2, 0] for x, y in zip(xs, sh)])
        tl = label(r"right-going rail: \ half the shape, \ moving right one point a sample", font_size=17, color=TUNE).next_to(top, UP, buff=0.2)
        bl = label(r"left-going rail: \ the other half, \ moving left", font_size=17, color=BLUE).next_to(bot, DOWN, buff=0.2)
        ends = VGroup(*[Line([s * w / 2, -1.2, 0], [s * w / 2, 2.0, 0], color=GREY_B, stroke_width=4) for s in (-1, 1)])
        el = label(r"at each fixed end the wave comes back inverted", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.4)
        eq = MathTex(r"u(x, t) = r(x - ct) + l(x + ct)", font_size=34).to_edge(UP, buff=1.0)
        head = label(r"d'Alembert's solution, \ on a computer", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Part 1 met d'Alembert's solution of the string: any motion is two waves of fixed shape, one travelling right and "
            "one left. <bookmark mark='a'/> Store each as a row of numbers, a rail. Split the plucked shape in half between "
            "them. <bookmark mark='b'/> Every sample, move the right-going rail one place right and the left-going rail one "
            "place left; at each fixed end, the arriving wave goes back inverted. The string is the sum of the two rails. "
            "Julius Smith called this a digital waveguide, in the 1980s, and it is Karplus-Strong's loop made exact."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq), FadeIn(ends), FadeIn(ghost(VGroup(top, bot), 0.3)))
            vo.wait_until("a")
            self.play(Create(top), Create(bot), FadeIn(tl), FadeIn(bl))
            vo.wait_until("b")
            self.play(top.animate.shift(RIGHT * 0.6), bot.animate.shift(LEFT * 0.6), FadeIn(el), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exact(self):
        d = load("waveguide")
        y = np.array(d["out"])
        ax = frame_axes(width=10.0, height=2.6, xlo=0, xhi=len(y), ylo=-1.05, yhi=1.05, center=DOWN * 0.1)
        a = curve(np.arange(len(y)), y, ax.to, color=GREY_A, width=6)
        b = curve(np.arange(len(y)), y, ax.to, color=TUNE, width=2)
        key = VGroup(label(r"finite differences \ (Part 1's beads)", font_size=17, color=GREY_A), label(r"the waveguide", font_size=17, color=TUNE)).arrange(RIGHT, buff=0.8).next_to(ax, UP, buff=0.3)
        res = label(rf"largest difference over half a second: \ ${d['max_err']:.1e}$", font_size=20, color=WHITE).to_edge(DOWN, buff=1.0)
        why = label(rf"an ideal string on {d['N']} intervals at its exact rate, \ {d['sr'] / 1000:.0f} kHz: \ both are exact, \ so they agree to rounding", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"two routes, \ one string", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Check it against Part 1's finite-difference string, the beads pulling on their neighbours. <bookmark mark='a'/> The "
            "same ideal string, plucked at a fifth, read at the same pickup: the bead simulation in grey, <bookmark mark='b'/> "
            "the waveguide in colour on top. <bookmark mark='c'/> Over half a second they differ by at most "
            f"{say(d['max_err'] * 1e14, 1)} times ten to the minus fourteen: rounding. At its exact rate the finite-difference "
            "scheme is exact for the ideal string, and so is the waveguide; they are the same mathematics. But the waveguide "
            "does it with two moving rails, which a computer does by moving a pointer, not the data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ghost(a, 0.25)))
            vo.wait_until("a")
            self.play(Create(a), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(b), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(res), FadeIn(why))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def winds(self):
        blocks = VGroup()
        for t, s, col in ((r"mouth", r"pressure $p_m$", GREY_A), (r"reed", r"a valve: \ $r = 0.7 - 0.3\,\Delta p$", EAR),
                          (r"bore", r"a delay line: \ the tube", TUNE), (r"bell", r"inverts, \ loses highs", BLUE)):
            blocks.add(VGroup(RoundedRectangle(width=2.6, height=1.2, corner_radius=0.15, stroke_color=col), VGroup(label(t, font_size=22, color=col), label(s, font_size=14, color=GREY_A)).arrange(DOWN, buff=0.1)).arrange(ORIGIN))
        blocks.arrange(RIGHT, buff=0.5).move_to(UP * 0.7)
        arr = VGroup(*[DoubleArrow(blocks[i].get_right(), blocks[i + 1].get_left(), buff=0.05, color=GREY_B, stroke_width=2, tip_length=0.15) for i in range(1, 3)])
        a0 = Arrow(blocks[0].get_right(), blocks[1].get_left(), buff=0.05, color=GREY_B, stroke_width=2)
        notes = VGroup(label(r"the reed is Part 8's valve: \ the pressure across it decides how much of the returning wave it lets back", font_size=17, color=WHITE),
                       label(r"Michael McIntyre, \ Robert Schumacher and Jim Woodhouse \ (1983): \ a nonlinear junction plus a linear delay is a wind instrument", font_size=17, color=GREY_A),
                       label(r"the closed reed and open bell make the bore a quarter-wave pipe: \ odd harmonics, \ as Part 8 found", font_size=17, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        head = label(r"a clarinet as a waveguide", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Waveguides model air columns too. <bookmark mark='a'/> A clarinet: the player's mouth pressure, the reed, the bore, "
            "the bell. The bore is a delay line; the bell sends the wave back inverted and a little duller. "
            "<bookmark mark='b'/> The reed is Part 8's valve: the pressure across it decides how much of the returning wave it "
            "lets back. Michael McIntyre, Robert Schumacher and Jim Woodhouse showed in 1983 that a nonlinear junction like this, "
            "on a linear delay, is all a wind instrument needs to oscillate. <bookmark mark='c'/> Closed at the reed and open at "
            "the bell, the bore is a quarter-wave pipe, so only odd harmonics survive, as Part 8 found."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(blocks, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(blocks), FadeIn(arr), FadeIn(a0))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def threshold(self):
        d = load("clarinet")
        ps, rms = np.array(d["pressures"]), np.array(d["rms"])
        ax = frame_axes(width=5.6, height=3.0, xlo=0.1, xhi=1.3, ylo=0, yhi=0.7, center=LEFT * 3.0 + DOWN * 0.3)
        cv = curve(ps, rms, ax.to, color=TUNE, width=3)
        dots = VGroup(*[Dot(ax.to(p, r), radius=0.04, color=TUNE) for p, r in zip(ps, rms)])
        xt = VGroup(*[label(f"{v:g}", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (0.2, 0.6, 1.0)])
        xl = label(r"mouth pressure \ (1 = closes the reed)", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"sound level \ (RMS)", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        on = ps[np.argmax(rms > 0.1)]
        off = ps[len(rms) - 1 - np.argmax(rms[::-1] > 0.1)]
        h = d["harmonics"]
        hb = harm_bars(h, width=0.22, gap=0.36, floor=-60.0, height=2.4, color=EAR, x0=2.0, y0=-1.4)
        hl = label(r"its harmonics \ (dB re the first): \ the odd ones only", font_size=15, color=EAR).next_to(hb, UP, buff=0.3)
        head = label(r"a threshold, \ and odd harmonics", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The model behaves like a clarinet in two ways nobody put in. <bookmark mark='a'/> Blow gently and nothing sounds; the "
            f"tone starts only above a threshold, here between {say(on - 0.05, 2)} and {say(on, 2)} of the pressure that "
            f"closes the reed. Blow too hard, above about {say(off, 2)}, and the reed is pushed shut and the sound stops, as a "
            "beginner discovers. <bookmark mark='b'/> And the spectrum: the second, fourth and sixth harmonics more than sixty "
            f"decibels down, the third at {say(h[2])} and the fifth at {say(h[4])}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(dots), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(hb), FadeIn(hl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("clarinet")
        c = clip("clarinet.two")
        cells = choice_boxes([r"a slow crescendo", r"the Tune"], width=3.6, buff=1.0, colors=[GREY_A, TUNE]).move_to(UP * 0.4)
        cap = label(rf"in the crescendo the pressure rises from 0.4 to 0.95; \ the tone begins after {d['onset_s']:.1f} s, \ at about {d['onset_p']:.2f}", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"the waveguide clarinet, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear it: first a slow crescendo, the mouth pressure rising from well below the threshold to near the top; then the "
            "Tune's first phrase."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a waveguide clarinet", kind="physical model", detail=r"bore, \ reed, \ bell", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["crescendo"], st["tune"] - 0.3, buff=0.08)
            pulse(snd, cells[1], st["tune"], c.duration, buff=0.08)
        with self.voiceover(
            "Silence, a breathy hiss, and then the note blooms out of nothing as the pressure crosses the threshold, later than "
            "the steady threshold because the oscillation needs time to grow. A sampler cannot do that: it has a soft "
            "recording and a loud one, but no threshold between them."
        ):
            self.play(Indicate(cells[0], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def industry(self):
        items = [
            (r"Stanford licensed waveguides to Yamaha too: \ the VL1 \ (1994) \ played breath-controlled winds", WHITE),
            (r"waveguides also model horns, \ flutes, \ bowed strings and rooms \ (Part 49's delay networks are cousins)", WHITE),
            (r"they are exact only for waves that keep their shape: \ stiffness and frequency-dependent loss need filters in the loop", WHITE),
            (r"a stiff piano string needs many all-passes to disperse its waves correctly", WHITE),
            (r"for objects that are not tubes or strings, \ another route is better: \ their modes", TUNE),
        ]
        rows_scene(self, r"waveguides at work", items,
                   "Waveguides went to market. <bookmark mark='b'/> Stanford licensed them to Yamaha too, and the VL1 of 1994 played "
                   "breath-controlled winds. <bookmark mark='c'/> They also model horns, flutes, bowed strings and rooms; Part 49's "
                   "feedback delay networks are cousins. <bookmark mark='d'/> But they are exact only for waves that keep their "
                   "shape: stiffness and frequency-dependent loss need filters in the loop, <bookmark mark='e'/> and a stiff piano "
                   "string needs many all-passes to spread its waves correctly. <bookmark mark='f'/> For objects that are not tubes "
                   "or strings, another route is better: their modes.", marks="bcdef")
