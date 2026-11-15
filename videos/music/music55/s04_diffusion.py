from __future__ import annotations

import numpy as np

from videos.music.music55.common import *  # noqa: F403

FCOL = {"500": GREY_A, "1000": TUNE, "2000": EAR}


class Diffusion(SoundScene):
    def construct(self):
        chapter(self, 3, r"Absorption and diffusion", r"How do you treat a room without deadening it?")
        self.absorbers()
        self.flutter()
        self.idea()
        self.residues()
        self.gauss()
        self.polar()
        self.practice()

    # ------------------------------------------------------------------
    def absorbers(self):
        items = [
            (r"porous absorbers \ (foam, \ mineral wool, \ curtains): \ air rubbing through fibres; \ they work where the air moves fastest", WHITE),
            (r"next to a wall the air cannot move: \ a porous absorber must stand a quarter wavelength out, \ 86 cm for 100 Hz", WHITE),
            (r"panel absorbers: \ a sheet on an air gap, \ a mass on a spring, \ absorbing near its resonance, \ in the bass", WHITE),
            (r"Helmholtz resonators: \ a bottle's resonance, \ or slots in a board over a cavity", WHITE),
            (r"too much absorption makes a room dead: \ quiet, \ dry, \ and tiring to play in", TUNE),
        ]
        rows_scene(self, r"three ways to absorb", items,
                   "First, absorbers, of three kinds. <bookmark mark='b'/> Porous absorbers, foam, mineral wool, curtains, work by "
                   "air rubbing through fibres, so they work where the air moves fastest. <bookmark mark='c'/> Next to a wall the "
                   "air cannot move at all, so a porous absorber must stand a quarter of a wavelength out to catch a frequency: "
                   "eighty-six centimetres for a hundred hertz. That is why thin foam only removes the treble. "
                   "<bookmark mark='d'/> Panel absorbers are a sheet over an air gap, a mass on a spring, absorbing near their "
                   "resonance, in the bass. <bookmark mark='e'/> Helmholtz resonators are a bottle's resonance, or slots in a board "
                   "over a cavity. <bookmark mark='f'/> But too much absorption makes a room dead: quiet, dry, and tiring to play "
                   "in. Musicians need the room to answer.", marks="bcdef")

    # ------------------------------------------------------------------
    def flutter(self):
        d = load("flutter")
        c = clip("flutter.two")
        gap = d["gap_ms"] / 1000.0
        ax = frame_axes(width=10.0, height=2.0, xlo=0, xhi=0.6, ylo=0, yhi=1.05, center=DOWN * 0.6)
        tr = stems([k * gap for k in range(int(0.6 / gap) + 1)], [0.82 ** k for k in range(int(0.6 / gap) + 1)], ax.to, color=EAR, r=0.05)
        xt = VGroup(*[label(f"{int(v * 1000)} ms", font_size=15, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.12) for v in (0, 0.2, 0.4, 0.6)])
        walls = VGroup(Rectangle(width=0.25, height=1.3, fill_color=GREY_B, fill_opacity=0.8, stroke_width=0).move_to(LEFT * 3 + UP * 1.75),
                       Rectangle(width=0.25, height=1.3, fill_color=GREY_B, fill_opacity=0.8, stroke_width=0).move_to(RIGHT * 3 + UP * 1.75))
        arrow = DoubleArrow(LEFT * 2.8 + UP * 1.75, RIGHT * 2.8 + UP * 1.75, color=GREY_A, buff=0, stroke_width=3)
        wl = label(r"6 m", font_size=17, color=GREY_A).next_to(arrow, UP, buff=0.08)
        boxes = choice_boxes([r"bare walls", r"scattering walls"], width=3.2, height=0.8, buff=1.2, size=20).to_edge(DOWN, buff=0.35)
        note = label(rf"a reflection every {d['gap_ms']:.0f} ms: \ a buzz at {d['rate_hz']:.1f} Hz", font_size=18, color=WHITE).next_to(ax, UP, buff=0.2)
        head = label(r"flutter echo", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Absorption is not the only cure, and sometimes it is the wrong one. <bookmark mark='a'/> Clap between two parallel "
            f"hard walls six metres apart, and the sound comes back every {say(d['gap_ms'])} milliseconds, each time a little "
            f"fainter: <bookmark mark='b'/> a train of echoes {say(d['rate_hz'], 1)} times a second, which the ear hears as a "
            "metallic buzz, a flutter echo. Hear two claps between bare walls, and then between walls that scatter each "
            "reflection instead of mirroring it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(walls), FadeIn(arrow), FadeIn(wl), FadeIn(ax), FadeIn(xt), FadeIn(ghost(tr, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(note))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in tr], lag_ratio=0.08), run_time=1.5)
            self.play(FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two claps, \ twice", kind="physical model", detail=r"two simulated walls", corner=UL, tag_corner=UR)
            pulse(snd, boxes[0], st["bare"], st["diffused"] - 0.3, buff=0.06)
            pulse(snd, boxes[1], st["diffused"], c.duration, buff=0.06)
            pulse(snd, tr, 0, c.duration, rate=5.0, color=GREY_B, buff=0.04)
        with self.voiceover(
            "The same energy, the same decay; but scattered, the reflections arrive spread out in time and direction, and the "
            "buzz turns into a smooth tail. That is diffusion."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"a flat wall is a mirror: \ all the reflected energy goes one way", WHITE),
            (r"a diffuser sends it every way, \ without absorbing it", WHITE),
            (r"the trick: \ a surface whose wells delay the reflection by different amounts, \ so that the reflected wavefront is wrinkled", WHITE),
            (r"Schroeder \ (1975): \ choose the depths by a number-theoretic sequence, \ and the energy spreads evenly into every direction the wells allow", TUNE),
            (r"his quadratic-residue diffuser \ (1979): \ depth of well $n$ proportional to $n^2 \bmod N$, \ for a prime $N$", GREY_A),
        ]
        rows_scene(self, r"scattering without absorbing", items,
                   "What does a diffuser do? <bookmark mark='b'/> A flat wall is a mirror: all the reflected energy goes one way. "
                   "<bookmark mark='c'/> A diffuser sends it every way, and absorbs almost none. <bookmark mark='d'/> The trick is a "
                   "surface of wells of different depths, each delaying its part of the reflection by a different amount, so that "
                   "the reflected wavefront comes back wrinkled. <bookmark mark='e'/> Manfred Schroeder, from 1975, found how to "
                   "choose the depths: by a sequence from number theory, which spreads the energy evenly into every direction the "
                   "wells allow. <bookmark mark='f'/> His best-known design, of 1979, is the quadratic-residue diffuser: the depth of well n is proportional to n "
                   "squared, modulo a prime N.", marks="bcdef")

    # ------------------------------------------------------------------
    def residues(self):
        d = load("diffuser")
        N = d["N"]
        res = d["residues"]
        cells = VGroup()
        for n_, r in enumerate(res):
            cells.add(VGroup(MathTex(rf"{n_}^2 = {n_ * n_}", font_size=26), MathTex(rf"\equiv {r}", font_size=28, color=TUNE)).arrange(DOWN, buff=0.15))
        cells.arrange(RIGHT, buff=0.55).to_edge(UP, buff=1.0)
        mod = label(rf"the remainders after dividing by {N}", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.2)
        W = 0.75
        scale = 0.11
        base_y = -2.4
        top_y = base_y + scale * 22
        wells = VGroup()
        for i, dep in enumerate(d["depths_cm"]):
            x = (i - (N - 1) / 2) * W
            h = scale * dep
            wells.add(Rectangle(width=W * 0.92, height=max(h, 0.02), stroke_width=0, fill_color=DIM, fill_opacity=1.0).move_to([x, top_y - h / 2, 0]))
        block = Rectangle(width=W * N + 0.2, height=scale * 22 + 0.15, stroke_width=0, fill_color=GREY_B, fill_opacity=0.6).move_to([0, top_y - (scale * 22 + 0.15) / 2, 0])
        fins = VGroup(*[Line([(i - N / 2) * W, top_y, 0], [(i - N / 2) * W, top_y - scale * 22, 0], color=GREY_A, stroke_width=2) for i in range(N + 1)])
        dl = VGroup(*[label(f"{dep:.1f}", font_size=14, color=TUNE).next_to([(i - (N - 1) / 2) * W, top_y, 0], UP, buff=0.1) for i, dep in enumerate(d["depths_cm"])])
        cap = label(rf"depths in cm for {d['f0']:.0f} Hz: \ $d_n = \frac{{n^2 \bmod N}}{{N}}\,\frac{{\lambda_0}}{{2}}$; \ wells {d['width_cm']:.0f} cm wide, \ one period {N * d['width_cm']:.0f} cm",
                    font_size=17, color=GREY_A).next_to(block, RIGHT, buff=0.3).shift(UP * 0.2)
        cap.scale_to_fit_width(min(cap.width, 3.4))
        head = label(r"a quadratic-residue diffuser", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            f"Take N equals {say(N)}. <bookmark mark='a'/> Square nought to six and keep the remainders after dividing by "
            "seven: nought, one, four, two, two, four, one. The sequence is symmetrical and repeats every seven. "
            "<bookmark mark='b'/> Make each well that many sevenths of half a wavelength deep at the design frequency, here "
            "five hundred hertz, and you have a quadratic-residue diffuser: a row of slots of depths nought, five, twenty, ten, "
            "ten, twenty and five centimetres, repeated along the wall."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(cells, 0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(cl) for cl in cells], lag_ratio=0.15), FadeIn(mod), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(block), FadeIn(wells), FadeIn(fins), FadeIn(dl), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gauss(self):
        lines = VGroup(
            MathTex(r"\text{well } n \text{ returns the wave delayed by } \frac{2d_n}{c}: \quad \text{phase } \ 2\pi\,\frac{n^2}{N}\,\frac{f}{f_0}", font_size=30),
            MathTex(r"\text{at } f_0, \text{ the far field in diffraction direction } k: \quad R_k = \frac{1}{N}\sum_{n=0}^{N-1} e^{2\pi i\,(n^2 + kn)/N}", font_size=30),
            MathTex(r"|R_k| = \frac{1}{\sqrt{N}} \ \text{ for every } k \qquad (\text{Gauss's sum, } N \text{ an odd prime})", font_size=32, color=TUNE),
            MathTex(r"\text{equal energy into every lobe:} \ \sin\theta_k = \frac{k\,\lambda}{N w}, \quad |\sin\theta_k| \le 1", font_size=30),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"why it works: \ a Gauss sum", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Why does it work? <bookmark mark='a'/> Well n sends the wave back after a round trip of twice its depth, a phase of "
            "two pi times n squared over N at the design frequency. <bookmark mark='b'/> A periodic surface reflects only into "
            "a few diffraction directions, one for each whole number k, and the strength of lobe k is this sum of N phases. "
            "<bookmark mark='c'/> Gauss proved that for an odd prime N its size is one over root N for every k: not one lobe "
            "large and the others small, but all the same. <bookmark mark='d'/> So the energy goes equally into every lobe that "
            "can exist, every direction whose sine is k lambda over the period. A two-hundred-year-old theorem about remainders "
            "hangs on the walls of recording studios."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def polar(self):
        d = load("diffuser")
        ang = np.array(d["angles"])
        panels = VGroup()
        for i, f in enumerate(("500", "1000", "2000")):
            ax = frame_axes(width=3.6, height=2.2, xlo=-90, xhi=90, ylo=-40, yhi=0, center=np.array([-4.2 + 4.2 * i, -0.2, 0]))
            fl = curve(ang, np.clip(d["pol"][f]["flat"], -40, 0), ax.to, color=GREY_B, width=2)
            q = curve(ang, np.clip(d["pol"][f]["qrd"], -40, 0), ax.to, color=FCOL[f], width=3)
            ttl = label(rf"{int(f)} Hz", font_size=19, color=FCOL[f]).next_to(ax, UP, buff=0.15)
            xt = VGroup(*[label(f"{v}$^\\circ$", font_size=13, color=GREY_A).next_to(ax.to(v, -40), DOWN, buff=0.08) for v in (-90, 0, 90)])
            cf = d["coef"][f]
            coef = label(rf"diffusion: \ {cf['qrd']:.2f} \ (flat: \ {cf['flat']:.2f})", font_size=16, color=FCOL[f]).next_to(xt, DOWN, buff=0.15)
            panels.add(VGroup(ax, fl, q, ttl, xt, coef))
        key = VGroup(label(r"flat panel of the same size", font_size=16, color=GREY_B), label(r"the diffuser", font_size=16, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)
        note = label(r"at 500 Hz the 42 cm period is shorter than a wavelength: \ only the mirror lobe exists; \ above, \ the energy spreads", font_size=17, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"scattering, \ computed", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is what Monochord computes for sound arriving head on: the level reflected in each direction, from minus "
            "ninety to ninety degrees, for a flat panel in grey and for four periods of the diffuser in colour. "
            "<bookmark mark='a'/> At a thousand and two thousand hertz the flat panel throws one sharp beam straight back; the "
            f"diffuser spreads the energy across the whole half-circle, and the diffusion coefficient rises from "
            f"{say(d['coef']['1000']['flat'], 2)} to {say(d['coef']['1000']['qrd'], 2)}. <bookmark mark='b'/> But at five "
            "hundred hertz, its design frequency, the diffuser hardly helps: the period, forty-two centimetres, is shorter than "
            "the wavelength, so the only lobe that can exist is the mirror one. The design frequency sets the depths; the "
            "period sets where diffusion begins."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), *[FadeIn(VGroup(p[0], p[1], p[3], p[4])) for p in panels], FadeIn(ghost(VGroup(*[p[2] for p in panels]), 0.25)))
            vo.wait_until("a")
            self.play(Create(panels[1][2]), Create(panels[2][2]), FadeIn(panels[1][5]), FadeIn(panels[2][5]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(panels[0][2]), FadeIn(panels[0][5]), FadeIn(note), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        items = [
            (r"recording studios: \ diffusers on the back wall, \ absorbers at the first reflection points", WHITE),
            (r"old halls diffuse by accident: \ statues, \ coffered ceilings, \ boxes and balconies", WHITE),
            (r"modern ones by design: \ shaped panels, \ two-dimensional residue and primitive-root diffusers", WHITE),
            (r"the working band: \ from where the period exceeds a wavelength, \ up to where a well's width does", TUNE),
            (r"and every surface treatment is a choice between three things: \ reflect, \ absorb, \ scatter", GREY_A),
        ]
        rows_scene(self, r"diffusers at work", items,
                   "Diffusers at work. <bookmark mark='b'/> In recording studios, they go on the back wall, while absorbers catch "
                   "the first reflections from the side walls. <bookmark mark='c'/> Old halls diffuse by accident, with statues, "
                   "coffered ceilings, boxes and balconies. <bookmark mark='d'/> Modern ones do it by design, with shaped panels and "
                   "two-dimensional residue and primitive-root diffusers. <bookmark mark='e'/> Each works over a band: from where "
                   "its period exceeds a wavelength, up to where the width of a single well does. <bookmark mark='f'/> And every "
                   "surface in a room is a choice between three things: reflect, absorb, or scatter.", marks="bcdef")
