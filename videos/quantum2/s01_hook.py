from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (chain_end, corner_wheel, hue, label, load, mtex, note, phasor_chain)
from videos.quantum2.compute import HOOK


class Hook(VoiceoverScene):
    def construct(self):
        self.one_screen()
        self.paths()
        self.three_roads()
        self.roadmap()

    # ------------------------------------------------------------------
    def one_screen(self):
        se = MathTex(r"i\hbar\,\frac{d}{dt}\ket{\psi}", r"=", r"\hat H\ket{\psi}", font_size=46)
        se[0].set_color(C.ENERGY)
        se[2].set_color(C.ENERGY)
        born = MathTex(r"P(a) = |\braket{a}{\psi}|^2", font_size=44, color=C.BORN)
        cr = MathTex(r"[\hat x, \hat p] = i\hbar", font_size=46, color=C.HBAR)
        top = VGroup(se, born, cr).arrange(RIGHT, buff=1.1).move_to(UP * 1.2)
        cap = label(r"Part 1, the whole theory on one screen", font_size=30, color=GREY_A).next_to(top, UP, buff=0.7)
        how = [r"guessed:\\ made to fit plane waves", r"postulated", r"computed from a\\ guessed $\hat p = -i\hbar\,\partial_x$"]
        tags = VGroup(*[label(h, font_size=26, color=C.ACTION).next_to(m, DOWN, buff=0.55) for h, m in zip(how, top)])
        qs = VGroup(*[MathTex("?", font_size=60, color=C.ACTION).next_to(t, DOWN, buff=0.25) for t in tags])
        goal = label(r"This video: \emph{derive} them", font_size=40).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "At the end of Part 1, the whole theory fit on one screen: <bookmark mark='a'/> the Schrödinger equation, "
            "the Born rule, and the commutator of position and momentum. <bookmark mark='b'/> But look at how we got "
            "them. We guessed the equation by making it work for plane waves. <bookmark mark='c'/> We took the Born rule "
            "as a postulate. <bookmark mark='d'/> And we computed the commutator from a formula for momentum that we "
            "had also guessed. <bookmark mark='e'/> In this video, we derive them, and then we put them to work."
        ) as vo:
            self.play(FadeIn(cap))
            vo.wait_until("a")
            self.play(Write(se), FadeIn(born), Write(cr), run_time=2.2)
            for m, i in zip("bcd", range(3)):
                vo.wait_until(m)
                self.play(FadeIn(tags[i], shift=DOWN * 0.15), FadeIn(qs[i]))
            vo.wait_until("e")
            self.play(FadeIn(goal))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paths(self):
        h = load("hook")
        P = HOOK
        ys, arrows = h["ys"], h["arrows"]
        s_pts = np.concatenate([h["s_top"], h["s_bot"]])
        sx, sy = 0.125, 0.115
        S = np.array([-6.6, 0.25, 0])

        def geo(x, y):
            return S + np.array([x * sx, y * sy, 0])

        x_plate, x_scr = P["L1"], P["L1"] + P["L2"]
        # the plate: three solid pieces around two slits
        a, w = P["d"] / 2, P["w"] / 2
        ymax = P["ymax"] + 2
        plate = VGroup()
        for y0, y1 in ((-ymax, -a - w), (-a + w, a - w), (a + w, ymax)):
            p0, p1 = geo(x_plate - 0.6, y0), geo(x_plate + 0.6, y1)
            plate.add(Rectangle(width=abs(p1[0] - p0[0]), height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=C.WALL,
                                fill_opacity=1).move_to((p0 + p1) / 2))
        screen = Line(geo(x_scr, -ymax), geo(x_scr, ymax), color=GREY_A, stroke_width=3)
        src = Dot(S, radius=0.07, color=WHITE)
        src_l = label(r"source", font_size=24, color=GREY_B).next_to(src, DOWN, buff=0.15)
        scr_l = label(r"screen", font_size=24, color=GREY_B).next_to(screen, UP, buff=0.12)
        yi = ValueTracker(float(np.argmin(np.abs(ys - 6.2))))
        # global phase: rotate every arrow so the first one points right (only angles between arrows matter)
        ref = np.exp(-1j * np.angle(arrows[:, 0]))
        rot = arrows * ref[:, None]
        unit = 3.4
        O = np.array([2.75, -0.45, 0])

        def idx():
            return int(round(yi.get_value()))

        def path_lines():
            i = idx()
            yP = ys[i]
            g = VGroup()
            for j, s in enumerate(s_pts):
                col = hue(np.angle(rot[i, j]))
                g.add(VMobject(stroke_color=col, stroke_width=2.2).set_points_as_corners([S, geo(x_plate, s), geo(x_scr, yP)]))
            g.add(Dot(geo(x_scr, yP), radius=0.07, color=C.BORN))
            return g

        def chain():
            i = idx()
            ch = phasor_chain(rot[i], origin=O, unit=unit, stroke_width=4, tip_length=0.08)
            end = chain_end(rot[i], O, unit)
            tot = Arrow(O, end, buff=0, color=WHITE, stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.3)
            tot.set_opacity(0.9 if np.linalg.norm(end - O) > 0.05 else 0)
            return VGroup(ch, tot)

        prof_x0 = geo(x_scr, 0)[0] + 0.12
        prof_s = 1.25

        def profile():
            i = idx()
            pts = [[prof_x0 + prof_s * np.abs(rot[k].sum()) ** 2, geo(0, ys[k])[1], 0] for k in range(0, i + 1)]
            m = VMobject(stroke_color=C.BORN, stroke_width=3.5)
            if len(pts) > 1:
                m.set_points_as_corners(pts)
            return m

        pl, chn = always_redraw(path_lines), always_redraw(chain)
        prof = always_redraw(profile)
        frame = Square(side_length=4.2, stroke_color=GREY_D, stroke_width=1.5).move_to(O + RIGHT * 1.85 + UP * 0.2)
        f_l = label(r"the arrows, tip to tail", font_size=26, color=GREY_A).next_to(frame, UP, buff=0.12)
        tot_l = MathTex(r"\Big|\sum_{\text{paths}} e^{i k L}\Big|^2", r"=", r"\text{brightness}", font_size=30)
        tot_l[0].set_color(WHITE)
        tot_l[2].set_color(C.BORN)
        tot_l.next_to(frame, DOWN, buff=0.2)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.28)
        gtag = note(r"computed: 14 paths through each slit; color = direction of each path's arrow; "
                    r"the picture is turned so the first arrow points right").to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Start with the double slit again, seen Richard Feynman's way. A source on the left, two slits, a screen. "
            "<bookmark mark='p'/> Pick one point on the screen, and consider every way to get there: through any point "
            "of either slit. <bookmark mark='c'/> Each path contributes an arrow, and the arrow turns one full "
            "revolution for every wavelength of path length, so the color of each path shows which way its arrow "
            "points. <bookmark mark='s'/> Now add all the arrows, tip to tail. The paths through each slit give a gently "
            "curving string of arrows; the two strings join; and the length of the total, squared, is the brightness "
            "at that point."
        ) as vo:
            self.play(FadeIn(plate), Create(screen), FadeIn(src), FadeIn(src_l), FadeIn(scr_l))
            vo.wait_until("p")
            self.add(pl)
            self.play(FadeIn(pl), FadeIn(wheel))
            vo.wait_until("c")
            self.play(FadeIn(gtag))
            vo.wait_until("s")
            self.add(chn)
            self.play(Create(frame), FadeIn(f_l), FadeIn(chn), run_time=1.5)
            self.play(Write(tot_l))
        with self.voiceover(
            "Now move the point. <bookmark mark='m'/> As it moves, the path lengths change, the arrows swing around, "
            "and the total grows and shrinks. Tracing its length squared along the screen draws the interference "
            "fringes. <bookmark mark='f'/> In Part 1 we had two arrows; here every point of each slit has its own, and "
            "the fringes come out with the slits' finite width built in."
        ) as vo:
            self.play(yi.animate.set_value(0), run_time=1.5)
            self.add(prof)
            vo.wait_until("m")
            self.play(yi.animate.set_value(len(ys) - 1), run_time=max(6.0, vo.mark_time("f") - vo.elapsed()), rate_func=linear)
            self.play(yi.animate.set_value(float(np.argmin(np.abs(ys - 10.0)))), run_time=1.5)
        # every path at all: a few wiggly ones
        rng = np.random.default_rng(4)
        iP = idx()
        PP = geo(x_scr, ys[iP])
        wig = VGroup()
        for k in range(7):
            ts = np.linspace(0, 1, 120)
            base = S[None, :] * (1 - ts[:, None]) + PP[None, :] * ts[:, None]
            off = sum(rng.normal() * 0.9 / (m + 1) * np.sin((m + 1) * np.pi * ts) for m in range(5))
            offx = sum(rng.normal() * 0.6 / (m + 1) * np.sin((m + 1) * np.pi * ts) for m in range(4))
            pts = base + np.stack([offx, off, 0 * ts], 1)
            wig.add(VMobject(stroke_color=hue(rng.uniform(0, 2 * np.pi)), stroke_width=2.5).set_points_smoothly(pts))
        wtag = label(r"every path, however wild,", font_size=30, color=C.ACTION)
        act = MathTex(r"\text{turns its arrow by }", r"S[\text{path}]", r"/\hbar", font_size=32)
        VGroup(wtag, act).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.3).shift(LEFT * 1.0)
        act[1].set_color(C.ACTION)
        with self.voiceover(
            "Feynman's real claim is far stronger: <bookmark mark='w'/> not just straight paths through the slits, but "
            "every path at all, however wild, contributes an arrow, <bookmark mark='a'/> turning at a rate set by a "
            "quantity from classical mechanics, the action. That single idea contains the Schrödinger equation, and it "
            "explains why a thrown ball follows just one path."
        ) as vo:
            vo.wait_until("w")
            pl.clear_updaters()
            self.play(FadeOut(gtag), FadeOut(plate), LaggedStart(*[Create(m) for m in wig], lag_ratio=0.25), FadeIn(wtag), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(act))
        for m in (chn, prof):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three_roads(self):
        heads = [r"1.\ Symmetry", r"2.\ Sum over paths", r"3.\ The classical limit"]
        bodies = [
            [r"U(t) = e^{-i\hat H t/\hbar}", r"T(a) = e^{-ia\hat p/\hbar}", r"\Rightarrow\ i\hbar\,\partial_t\psi = \hat H\psi,\ \ [\hat x, \hat p] = i\hbar"],
            [r"K(b, a) = \int \mathcal{D}x\; e^{\,iS[x]/\hbar}", r"\Rightarrow\ i\hbar\,\partial_t\psi = \hat H\psi"],
            [r"\hbar \to 0:\ \ \delta S = 0", r"\Rightarrow\ m\ddot x = -V'(x)", r"\oint p\,dx = (n + \tfrac12)\,h"],
        ]
        cols = VGroup()
        colors = [C.QTIME, C.ACTION, C.CLASSICAL]
        for hd, bd, col in zip(heads, bodies, colors):
            g = VGroup(label(hd, font_size=34, color=col), *[MathTex(b, font_size=30) for b in bd]).arrange(DOWN, buff=0.28)
            cols.add(g)
        cols.arrange(RIGHT, buff=0.7, aligned_edge=UP).to_edge(UP, buff=0.6)
        if cols.width > 13.4:
            cols.width = 13.4
        same = label(r"one theory", font_size=38).move_to(DOWN * 1.6)
        box = SurroundingRectangle(same, color=WHITE, buff=0.25, corner_radius=0.12)
        arrs = VGroup(*[Arrow(c.get_bottom(), box.get_top(), buff=0.2, color=GREY_B, stroke_width=3) for c in cols])
        with self.voiceover(
            "It's one of three roads we'll take. <bookmark mark='a'/> The first is symmetry: the laws don't change from "
            "moment to moment, or from place to place, and those two facts alone force the Schrödinger equation and the "
            "commutator. <bookmark mark='b'/> The second is Feynman's sum over paths. <bookmark mark='c'/> The third "
            "runs backward from classical mechanics, and explains the old quantum rules of Bohr and Sommerfeld. "
            "<bookmark mark='d'/> All three arrive at the same theory."
        ) as vo:
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=DOWN * 0.15), run_time=1.2)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2), FadeIn(same), Create(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roadmap(self):
        items = [
            (r"Part 1.\ Symmetry", r"time, space, rotations and local phase: $\hat H$, $\hat p$, $\hat J$ and electromagnetism"),
            (r"Part 2.\ Sums over paths", r"the path integral, the classical limit, WKB, alpha decay"),
            (r"Part 3.\ Approximations", r"perturbation theory (and why its series diverge), Fermi's golden rule"),
            (r"Part 4.\ Many particles", r"bosons and fermions, helium, the periodic table, bands in solids"),
            (r"Part 5.\ Open systems", r"density matrices, Gleason's theorem, decoherence"),
            (r"Part 6.\ Relativity", r"the Dirac equation: spin, antimatter, fine structure"),
        ]
        rows = VGroup(*[VGroup(label(a, font_size=32), label(b, font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
                        for a, b in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(LEFT, buff=0.9).shift(DOWN * 0.25)
        plan = label(r"The plan", font_size=42, color=GREY_A).to_edge(UP, buff=0.4)
        pre = note(r"assumes Part 1: wavefunctions, operators, $[\hat x, \hat p] = i\hbar$, the oscillator, hydrogen, spin. "
                   r"Every derivation is on screen; every picture is computed.").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Then we'll use the theory. <bookmark mark='a'/> Approximation methods for real atoms, "
            "<bookmark mark='b'/> what identical particles do, from helium to the periodic table and solids, "
            "<bookmark mark='c'/> what happens to interference when a system touches its environment, "
            "<bookmark mark='d'/> and finally Dirac's equation, where relativity brings in antimatter. "
            "<bookmark mark='e'/> This is Part 2, and it's more mathematical than Part 1; it assumes the wavefunction, "
            "operators, commutators and the hydrogen atom from there. Every derivation is on screen, and every picture "
            "is computed."
        ) as vo:
            self.play(FadeIn(plan), FadeIn(rows[0]), FadeIn(rows[1]))
            for m, r in zip("abcd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(pre))
        self.wait(0.5)
        self.clear_scene()
