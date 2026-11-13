from __future__ import annotations

import numpy as np
from scipy.special import jv

from videos.music.music9.common import *  # noqa: F403


class Skin(SoundScene):
    def construct(self):
        chapter(self, 1, r"A skin", r"What are the notes of a drumhead?", lit=(1877,), extra=((1764, r"Euler's vibrating membrane"),))
        self.modes()
        self.worked()
        self.where()

    # ------------------------------------------------------------------
    def modes(self):
        d = load("skin")
        ms = d["modes"][:6]
        cells = VGroup()
        for r in ms:
            dg = mode_diagram(r["m"], r["n"], radius=0.78)
            cells.add(VGroup(dg, label(rf"{r['ratio']:.2f}", font_size=30, color=TUNE).next_to(dg, DOWN, buff=0.15)))
        cells.arrange_in_grid(rows=2, cols=3, buff=(1.0, 0.45)).move_to(RIGHT * 2.6 + DOWN * 0.4)
        notes = VGroup(label(r"a string's modes: \\ half waves along a line", font_size=26, color=STR),
                       label(r"a skin has two directions: \\ round the rim, \ and out from the centre", font_size=26, color=SKIN),
                       label(r"so its still lines are \\ diameters and circles", font_size=26, color=GREY_A),
                       label(r"blue rises while red falls", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(LEFT * 4.2 + DOWN * 0.3)
        with self.voiceover(
            "Part 1 found the modes of a string: one half wave, two, three, each with still points, the nodes, "
            "between its moving parts. A skin does the same in two directions at once. <bookmark mark='a'/> "
            "Its simplest mode is the whole skin rising and falling together. <bookmark mark='b'/> In the next, "
            "one half rises while the other falls, and the line between them, a diameter, stays still. "
            "<bookmark mark='c'/> Then two diameters, and four quarters. Then a mode with no diameter but a "
            "still circle, the centre moving against the rim. And so on: every mode of a round skin is some "
            "number of still diameters and some number of still circles. <bookmark mark='d'/> Under each is "
            "its frequency, as a multiple of the lowest. One, one point five nine, two point one four, two "
            "point three. The numbers come from the mathematics of round things, the Bessel functions, and "
            "they are what they are."
        ) as vo:
            self.play(FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(cells[0][0]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(cells[1][0]), FadeIn(notes[2]), FadeIn(notes[3]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(cells[k][0]) for k in (2, 3, 4, 5)], lag_ratio=0.5), run_time=6.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c[1]) for c in cells], lag_ratio=0.3), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        d = load("skin")
        z0, z1 = d["zeros"]["j01"], d["zeros"]["j11"]
        title = label(r"A worked example: \ the first interval of a drum", font_size=36).to_edge(UP, buff=0.4)
        g = axes([0, 8], [-0.5, 1.1], x_length=6.4, y_length=3.0, xlabel=r"distance from the centre (scaled)", ylabel=r"height of the skin", xticks=[0, 2, 4, 6, 8], yticks=[0], font_size=20)
        g.move_to(LEFT * 3.4 + DOWN * 0.2)
        x = np.linspace(0, 8, 300)
        c0, c1 = curve_from(g, x, jv(0, x), AIR), curve_from(g, x, jv(1, x), TUNE)
        d0 = VGroup(Dot(g.ax.c2p(z0, 0), radius=0.08, color=AIR), label(rf"{z0:.3f}", font_size=22, color=AIR).next_to(g.ax.c2p(z0, 0), DOWN, buff=0.12))
        d1 = VGroup(Dot(g.ax.c2p(z1, 0), radius=0.08, color=TUNE), label(rf"{z1:.3f}", font_size=22, color=TUNE).next_to(g.ax.c2p(z1, 0), UP, buff=0.12))
        ask = pause_card(r"The rim must be still, \\ so each mode ends where its curve \\ first crosses zero, \ and its frequency \\ is proportional to that number. \\ What interval lies between \\ a drum's two lowest modes?", width=5.0, font_size=26).move_to(RIGHT * 3.8 + UP * 0.2)
        ratio = z1 / z0
        cts = 1200 * np.log2(ratio)
        work = VGroup(MathTex(rf"\frac{{{z1:.3f}}}{{{z0:.3f}}} = {ratio:.3f}", font_size=40), label(rf"{cts:.0f} cents: \ wider than a fifth (702),", font_size=26, color=GREY_A),
                      label(rf"{abs(d['minor_sixth_cents']):.0f} cents short of a minor sixth", font_size=26, color=GREY_A), label(r"not an octave, \ not a fifth, \ not anything", font_size=28, color=BAD)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.6 + DOWN * 0.3)
        with self.voiceover(
            "A worked example, to see where one of those numbers comes from. Along a radius, the height of "
            "the skin in its lowest mode follows the blue curve, and in its next mode the gold one. The rim "
            "of a drum is held still. So each mode must end exactly where its curve first comes down to zero, "
            "and the frequency of the mode is proportional to that distance. The zeros are marked. What is "
            "the interval between a drum's two lowest notes? Pause, and work it out."
        ):
            self.play(FadeIn(title), FadeIn(g), Create(c0), Create(c1), FadeIn(d0), FadeIn(d1), FadeIn(ask, shift=UP * 0.2), run_time=2.0)
        self.wait(1.5)
        with self.voiceover(
            f"Three point eight three two over two point four oh five is {say(ratio, 3)}. <bookmark mark='a'/> In "
            f"cents, {say(cts)}: wider than a fifth, and a little short of a minor sixth. The first overtone of "
            "a string is an octave above its fundamental. The first overtone of a drum is nowhere. And the "
            "zeros of these curves never settle into even spacing, so neither do the overtones above."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(work[0]))
            vo.wait_until("a")
            self.play(FadeIn(work[1]), FadeIn(work[2]))
            self.play(FadeIn(work[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def where(self):
        d = load("skin")
        c = clip("skin.where")
        ms = d["modes"][:8]
        q = listen_card(r"One drum, \ struck twice: \ once at the very centre, \ once between the centre and the rim. \\ Which blow was at the centre?", width=9.6, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes(buff=2.6, width=3.0, height=1.3).move_to(UP * 0.4)
        with self.voiceover(
            "A drummer cannot change these numbers. But a drummer can choose which of them to sound, and the "
            "choice is made with the stick. Here is one drum, struck twice: once at the very centre, once "
            "about halfway out. Which blow was at the centre?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"one drum, \ two blows", detail=r"a model of a round skin", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 1.6)

        def bars(amounts, col):
            g = VGroup()
            for k, a in enumerate(amounts[:8]):
                r = Rectangle(width=0.3, height=max(1.3 * float(a), 0.03), stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(RIGHT * 0.42 * k, aligned_edge=DOWN)
                g.add(r)
            return g

        b_off, b_c = bars(d["off"], SKIN).next_to(bx[0], DOWN, buff=0.55), bars(d["centre"], BAD).next_to(bx[1], DOWN, buff=0.55)
        la = label(r"off centre: \ every mode joins in", font_size=24, color=SKIN).next_to(b_off, DOWN, buff=0.2)
        lb = label(r"dead centre: \ only the circles", font_size=24, color=BAD).next_to(b_c, DOWN, buff=0.2)
        with self.voiceover(
            "B was the centre: short and dead. <bookmark mark='a'/> A blow at the centre can only start the "
            "modes that move at the centre, and those are the ones with no still diameter: the whole skin "
            "going up and down, with or without circles. Those modes push the air above the drum in and out "
            "as a whole. They are good at making sound, so they give their energy away in a fraction of a "
            "second, and the drum goes thud. <bookmark mark='b'/> Strike off centre and the modes with "
            "diameters join in. Half the skin pushes air while the other half pulls, so they radiate poorly "
            "and ring on. That ring is the drum's tone. A timpanist strikes about a quarter of the way in "
            "from the rim, and now you know why."
        ) as vo:
            self.play(FadeOut(q))
            vo.wait_until("a")
            self.play(FadeIn(b_c), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeIn(b_off), FadeIn(la))
        self.wait(0.3)
        self.clear_scene()
