from __future__ import annotations

import numpy as np

from videos.music.music55.common import *  # noqa: F403

W, H = 2.2, 1.5
O = np.array([-W / 2, -H / 2 - 0.3, 0])
SRC = np.array([0.55, 0.45])
LIS = np.array([1.6, 1.05])


def pt(x, y):
    return O + np.array([x, y, 0])


def image(i, j):
    x = i * W + (SRC[0] if i % 2 == 0 else W - SRC[0])
    y = j * H + (SRC[1] if j % 2 == 0 else H - SRC[1])
    return np.array([x, y])


class Simulation(SoundScene):
    def construct(self):
        chapter(self, 5, r"Simulating a room", r"How can you hear a hall before it is built?")
        self.images()
        self.count()
        self.check()
        self.rays()
        self.waves()
        self.aural()

    # ------------------------------------------------------------------
    def images(self):
        cells = VGroup()
        dots = VGroup()
        d1, d2 = VGroup(), VGroup()
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                r = Rectangle(width=W, height=H, stroke_color=GREY_B if (i, j) == (0, 0) else DIM, stroke_width=3 if (i, j) == (0, 0) else 1.5)
                r.move_to(pt(i * W + W / 2, j * H + H / 2))
                cells.add(r)
                if (i, j) != (0, 0):
                    order = abs(i) + abs(j)
                    dt = Dot(pt(*image(i, j)), radius=0.07, color=BLUE if order == 1 else EAR)
                    dots.add(dt)
                    (d1 if order == 1 else d2).add(dt)
        src = Dot(pt(*SRC), radius=0.09, color=TUNE)
        lis = Dot(pt(*LIS), radius=0.09, color=WHITE)
        im = image(1, 0)
        xw = W
        yhit = im[1] + (LIS[1] - im[1]) * (xw - im[0]) / (LIS[0] - im[0])
        ghost_line = DashedLine(pt(*im), pt(*LIS), color=BLUE, stroke_width=2)
        path = VGroup(Line(pt(*SRC), pt(xw, yhit), color=TUNE, stroke_width=3), Line(pt(xw, yhit), pt(*LIS), color=TUNE, stroke_width=3))
        im2 = image(1, 1)
        g2 = DashedLine(pt(*im2), pt(*LIS), color=EAR, stroke_width=2)
        lab = VGroup(label(r"source", font_size=15, color=TUNE).next_to(src, DOWN, buff=0.08), label(r"listener", font_size=15, color=WHITE).next_to(lis, UP, buff=0.08))
        key = VGroup(label(r"first-order images", font_size=17, color=BLUE), label(r"second-order images", font_size=17, color=EAR)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        note = label(r"Allen and Berkley \ (Bell Labs, \ 1979): \ each reflection is a straight line from a mirror image; \ its delay $r/c$, \ its strength $\beta^k/r$", font_size=17, color=WHITE).to_edge(DOWN, buff=0.3)
        head = label(r"the image method", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Part 49 met the image method; here it is in full. <bookmark mark='a'/> A reflection off a flat wall looks as if it "
            "came from a mirror image of the source behind the wall. <bookmark mark='b'/> So instead of bouncing a ray, draw a "
            "straight line from the image to the listener: where it crosses the wall is the point of reflection, and its "
            "length gives the delay. <bookmark mark='c'/> Mirror the mirrored rooms again and you get the second-order images, "
            "the sounds that hit two walls, and so on for ever, a lattice of rooms. <bookmark mark='d'/> Jont Allen and David "
            "Berkley wrote it down for a box at Bell Labs in 1979: each image contributes a click after r over c, weakened by "
            "one over r and by the wall's reflection factor beta once per bounce."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells[4]), FadeIn(src), FadeIn(lis), FadeIn(lab), FadeIn(ghost(VGroup(cells, dots), 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(d1), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(Create(ghost_line), Create(path), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(d2), FadeIn(key[1]), Create(g2))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        d = load("images")
        ks = sorted(int(k) for k in d["counts"])
        vals = [d["counts"][str(k)] for k in ks]
        top = max(vals)
        bars = VGroup()
        for i, (k, v) in enumerate(zip(ks, vals)):
            h = 3.0 * v / top
            b = Rectangle(width=0.7, height=max(h, 0.03), stroke_width=0, fill_color=TUNE, fill_opacity=0.8).move_to([-4.6 + 1.0 * i, -2.2 + h / 2, 0])
            bars.add(VGroup(b, label(f"{v}", font_size=15, color=WHITE).next_to(b, UP, buff=0.08), label(f"{k}", font_size=15, color=GREY_A).next_to([-4.6 + 1.0 * i, -2.2, 0], DOWN, buff=0.1)))
        xl = label(r"images up to this order \ (a 20 by 15 by 10 m room)", font_size=16, color=GREY_A).move_to([-1.1, -3.05, 0])
        eq = VGroup(MathTex(r"\frac{dN}{dt} = \frac{4\pi c^3 t^2}{V}", font_size=36, color=EAR),
                    label(rf"after one second, \ {d['reflections_per_s']:,.0f} reflections a second", font_size=17, color=EAR)).arrange(DOWN, buff=0.25).move_to([4.4, 1.2, 0])
        note = label(r"the cube again: \ $(4k^3 + 6k^2 + 8k + 3)/3$ images up to order $k$", font_size=17, color=WHITE).move_to([4.2, -0.6, 0])
        head = label(r"how many reflections?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How many images are there? <bookmark mark='a'/> In a box, seven up to the first order, the source and its six "
            "mirrors; twenty-five up to the second; eight hundred and thirty-three up to the eighth. <bookmark mark='b'/> The "
            "count grows as the cube of the order, the same cube as Weyl's modes. <bookmark mark='c'/> In time, the reflections "
            "arrive at a rate that grows as t squared: in a hall of three thousand cubic metres, a second after the sound, about "
            f"{say(round(d['reflections_per_s'], -3))} reflections a second. No one computes them all: the image method handles "
            "the early, sparse part, and statistics the dense tail."
        ) as vo:
            self.play(FadeIn(head), FadeIn(xl), FadeIn(ghost(bars, 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(note))
            vo.wait_until("c")
            self.play(FadeIn(eq))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("check")
        rows = VGroup(VGroup(label(r"wall absorption $\alpha$", font_size=17, color=GREY_A), label(r"image method", font_size=17, color=GREY_A),
                             label(r"Sabine", font_size=17, color=GREY_A), label(r"Eyring", font_size=17, color=GREY_A)))
        for r in d["rt"]:
            rows.add(VGroup(label(f"{r['alpha']:.2f}", font_size=19, color=WHITE), label(f"{r['image']:.2f} s", font_size=19, color=TUNE),
                            label(f"{r['sabine']:.2f} s", font_size=19, color=WHITE), label(f"{r['eyring']:.2f} s", font_size=19, color=WHITE)))
        rows.arrange(DOWN, buff=0.22)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.6 + 2.6 * i)
        rows.move_to(UP * 0.9)
        pk = VGroup(*[label(rf"{a:.1f}$\to${b:.1f}", font_size=15, color=BLUE) for a, b in d["peaks"]]).arrange(RIGHT, buff=0.3)
        pl = label(rf"peaks of the simulated response \ $\to$ \ the nearest exact mode, \ Hz: \ the worst {d['worst_hz']:.2f} Hz apart", font_size=17, color=GREY_A)
        pg = VGroup(pl, pk).arrange(DOWN, buff=0.2).move_to(DOWN * 1.5)
        note = label(r"a box with smooth walls is not diffuse: \ the paths that graze the long walls bounce least, \ and keep the tail alive", font_size=17, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"the simulator, \ checked", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Monochord's image-source room, checked two ways. <bookmark mark='a'/> Its reverberation time, measured from its "
            "own response for four wall absorptions, against Sabine and Eyring. For a live room it rings longer than either: "
            f"at alpha nought point nought eight, {say(d['rt'][1]['image'], 2)} seconds against Sabine's "
            f"{say(d['rt'][1]['sabine'], 2)}. <bookmark mark='b'/> That is not a bug. Both formulas assume a diffuse field, and "
            "a box with smooth walls is not one: the paths that graze along the long walls bounce least, and they keep the tail "
            "alive. Real rooms scatter, and land closer to the formulas. <bookmark mark='c'/> And the peaks of its response, in "
            f"the bass, sit on the exact modes, the worst {say(d['worst_hz'], 1)} hertz away: the image method and the mode sum "
            "are two descriptions of the same field."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
            vo.wait_until("c")
            self.play(FadeIn(pg))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rays(self):
        items = [
            (r"real halls are not boxes: \ images multiply and most are invisible behind other walls", WHITE),
            (r"ray tracing \ (Krokstad, \ Str{\o}m and S{\o}rsdal, \ 1968): \ fire thousands of rays, \ each carrying energy, \ and count those that cross the listener", WHITE),
            (r"rays can scatter at every bounce, \ by each surface's scattering coefficient: \ diffusion, \ simulated", WHITE),
            (r"hybrids: \ images for the first reflections, \ rays for the rest, \ a statistical tail at the end", TUNE),
            (r"what geometry cannot do: \ diffraction round edges, \ and the modes below the Schroeder frequency", GREY_A),
        ]
        rows_scene(self, r"rays", items,
                   "Real halls are not boxes. <bookmark mark='b'/> In a complicated shape the images multiply, and most of them are "
                   "invisible, hidden behind other walls, so each must be checked. <bookmark mark='c'/> Ray tracing, introduced by "
                   "Krokstad, Strøm and Sørsdal in 1968, turns the problem round: fire thousands of rays from the source, each "
                   "carrying a share of the energy, and count those that pass through the listener. <bookmark mark='d'/> Rays can "
                   "scatter at every bounce, by each surface's scattering coefficient: diffusion, simulated. "
                   "<bookmark mark='e'/> Commercial programs are hybrids: images for the first reflections, rays for the rest, a "
                   "statistical tail at the end. <bookmark mark='f'/> What geometry cannot do is the wave part: diffraction round "
                   "edges, and the modes below the Schroeder frequency.", marks="bcdef")

    # ------------------------------------------------------------------
    def waves(self):
        items = [
            (r"wave-based methods solve the wave equation itself, \ on a grid: \ Part 2's finite-difference simulator, \ in three dimensions", WHITE),
            (r"the grid must be finer than the wavelength: \ about ten points per wavelength", WHITE),
            (r"a 20,000 m$^3$ hall up to 1 kHz: \ a 3.4 cm grid, \ half a billion points, \ 17,000 steps for each second of sound", WHITE),
            (r"the cost grows as the fourth power of the top frequency: \ so waves for the bass, \ rays for the treble", TUNE),
            (r"graphics processors have made full-band wave simulation of small rooms possible; \ of halls, \ nearly", GREY_A),
        ]
        rows_scene(self, r"waves", items,
                   "The alternative is to solve the wave equation itself. <bookmark mark='b'/> On a grid, by the finite-difference "
                   "method of Part 2's simulator, in three dimensions. <bookmark mark='c'/> The grid must be finer than the "
                   "wavelength, about ten points to a wavelength. <bookmark mark='d'/> For a twenty-thousand cubic metre hall up to "
                   "one kilohertz that is a grid of three point four centimetres, half a billion points, each updated seventeen thousand times for every second of sound. "
                   "<bookmark mark='e'/> The cost grows as the fourth power of the top frequency, three dimensions of space and one "
                   "of time; so in practice it is waves for the bass and rays for the treble. <bookmark mark='f'/> Graphics "
                   "processors have made full-band wave simulation of small rooms possible, and of halls, nearly.", marks="bcdef")

    # ------------------------------------------------------------------
    def aural(self):
        items = [
            (r"auralization: \ the simulated impulse response, \ convolved with a dry recording \ (Part 49)", WHITE),
            (r"for each reflection we know its direction too, \ so it can be rendered for two ears, \ or a ring of loudspeakers", WHITE),
            (r"Kleiner, \ Dalenb{\"a}ck and Svensson named it in 1993; \ halls are now heard years before they open", WHITE),
            (r"to render direction, \ we need to know how direction is heard", TUNE),
        ]
        rows_scene(self, r"hearing a hall before it is built", items,
                   "And then the simulation can be heard. <bookmark mark='b'/> Auralization: the simulated impulse response, "
                   "convolved with a dry recording, as in Part 49. <bookmark mark='c'/> And because we know the direction each "
                   "reflection comes from, it can be rendered for two ears, or for a ring of loudspeakers. "
                   "<bookmark mark='d'/> Mendel Kleiner, Bengt-Inge Dalenbäck and Peter Svensson named it in 1993, and halls are "
                   "now heard by their architects and players years before they open. <bookmark mark='e'/> To render direction, "
                   "though, we have to know how direction is heard.", marks="bcde")
