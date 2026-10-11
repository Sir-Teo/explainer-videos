from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (label, ladder, load, mtex, note, why)


class FineStructure(VoiceoverScene):
    def construct(self):
        self.g_factor()
        self.g_minus_2()
        self.hydrogen()
        self.layers()

    # ------------------------------------------------------------------
    def g_factor(self):
        rows = [
            MathTex(r"(\boldsymbol\sigma\cdot\mathbf a)(\boldsymbol\sigma\cdot\mathbf b)", r"=", r"\mathbf a\cdot\mathbf b + i\,\boldsymbol\sigma\cdot(\mathbf a\times\mathbf b)", font_size=38),
            MathTex(r"\boldsymbol\pi = \hat{\mathbf p} - q\mathbf A:\quad \boldsymbol\pi\times\boldsymbol\pi", r"=", r"iq\hbar\,\mathbf B", font_size=38),
            MathTex(r"\frac{(\boldsymbol\sigma\cdot\boldsymbol\pi)^2}{2m}", r"=", r"\frac{\boldsymbol\pi^2}{2m} - \frac{q\hbar}{2m}\,\boldsymbol\sigma\cdot\mathbf B", font_size=40),
            MathTex(r"-\frac{q\hbar}{2m}\,\boldsymbol\sigma\cdot\mathbf B", r"=", r"-\,g\,\frac{q}{2m}\,\mathbf S\cdot\mathbf B\quad\text{with}\quad g = 2", font_size=40),
        ]
        rows[3][2].set_color(C.DIRAC_POS)
        whys = [why(rows[0], r"the Pauli matrices' identity (checked numerically)"), why(rows[1], r"the components of $\boldsymbol\pi$ don't commute"),
                why(rows[2], r"Dirac's equation at low speed: the Pauli equation"), why(rows[3], r"with $\mathbf S = \tfrac{\hbar}{2}\boldsymbol\sigma$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.4, buff=0.6)
        orb = label(r"an orbit gives $g = 1$; the electron's spin is twice as magnetic", font_size=28, color=C.DIRAC_POS).to_edge(DOWN, buff=0.7)
        intro = MathTex(r"\hat H_{\text{low speed}}", r"=", r"\frac{(\boldsymbol\sigma\cdot\boldsymbol\pi)^2}{2m} + qV,\qquad \boldsymbol\pi = \hat{\mathbf p} - q\mathbf A", font_size=44)
        intro_n = note(r"the upper two components of Dirac's equation, when $v \ll c$").next_to(intro, DOWN, buff=0.3)
        with self.voiceover(
            "Dirac's equation predicts more than antimatter. At low speeds, its upper two components obey a "
            "Schrödinger equation with a twist: the kinetic energy appears as sigma dot pi, squared, over 2m, where pi is "
            "p minus q A. <bookmark mark='a'/> The Pauli matrices obey this identity: sigma dot a times sigma dot b is a "
            "dot b plus i sigma dot a cross b. <bookmark mark='b'/> And because the components of pi don't commute in a "
            "magnetic field, pi cross pi isn't zero: it's i q h-bar B. <bookmark mark='c'/> So the kinetic energy "
            "contains a magnetic term, <bookmark mark='d'/> and it says the electron's spin is a magnet with g equal to "
            "two: twice as strong, for its angular momentum, as an orbiting charge."
        ) as vo:
            self.play(Write(intro), run_time=2.5)
            self.play(FadeIn(intro_n))
            for m, i in zip("abcd", range(4)):
                vo.wait_until(m)
                if i == 0:
                    self.play(FadeOut(VGroup(intro, intro_n), shift=UP * 0.3), run_time=0.6)
                step(i)
            self.play(FadeIn(orb))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def g_minus_2(self):
        n = load("numbers")
        a_s, a_m = float(n["a_schwinger"]), float(n["a_meas"])
        assert abs(a_s - 0.0011614) < 1e-7
        l1 = MathTex(r"\frac g2", r"=", r"1.001\,159\,652\,180\,59\,(13)", font_size=46).move_to(UP * 1.6)
        l1[2].set_color(WHITE)
        src = note(r"Fan, Myers, Sukra \& Gabrielse, PRL 130, 071801 (2023): one electron in a trap").next_to(l1, DOWN, buff=0.2)
        l2 = MathTex(r"a = \frac{g - 2}{2}", r"\approx", r"\frac{\alpha}{2\pi} = " + f"{a_s:.7f}", font_size=40).next_to(src, DOWN, buff=0.6)
        l2[2].set_color(C.APPROX)
        sch = note(r"Schwinger (1948): the first correction from quantum electrodynamics").next_to(l2, DOWN, buff=0.15)
        l3 = label(r"with higher orders of QED: agreement to about one part in a trillion", font_size=28).next_to(sch, DOWN, buff=0.5)
        with self.voiceover(
            "Measured, g is not exactly two. <bookmark mark='a'/> The best value, from a single electron held in a trap, "
            "is 2.00231930436, to thirteen digits. <bookmark mark='b'/> The small excess comes from the next layer of the "
            "theory, quantum electrodynamics: its first term, computed by Julian Schwinger in 1948, is the fine-structure "
            "constant over two pi. <bookmark mark='c'/> With the higher terms included, theory and experiment agree to "
            "about one part in a trillion."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(l1), FadeIn(src))
            vo.wait_until("b")
            self.play(Write(l2), FadeIn(sch))
            vo.wait_until("c")
            self.play(FadeIn(l3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hydrogen(self):
        n = load("numbers")
        fs, fsm, lamb = float(n["fs_dirac_GHz"]), float(n["fs_meas_GHz"]), float(n["lamb_MHz"])
        E2 = float(n["E2_bohr_eV"])
        assert abs(fs - 10.94) < 0.01 and abs(fsm - 10.969) < 0.001 and abs(lamb - 1057.85) < 0.01
        import scipy.constants as sc
        assert abs(fs * 1e9 * sc.h / sc.e * 1e6 - 45) < 1  # micro-eV
        assert 0.0015 < abs((fsm - fs) / fsm) < 0.0025  # "within a quarter of a percent"
        form = MathTex(r"E_{nj} = mc^2\Big[1 + \Big(\frac{\alpha}{n - (j + \frac12) + \sqrt{(j + \frac12)^2 - \alpha^2}}\Big)^2\Big]^{-1/2}", font_size=34).to_edge(UP, buff=0.3)
        fn = note(r"Dirac's hydrogen, solved exactly by Darwin and by Gordon (1928): the energy depends on $n$ and $j$ only").next_to(form, DOWN, buff=0.12)

        def col(x0, title, levels, scale_note):
            g = VGroup(label(title, font_size=26, color=GREY_A).move_to(RIGHT * x0 + UP * 1.75))
            for y, txt, c in levels:
                ln = Line(RIGHT * (x0 - 0.9) + UP * y, RIGHT * (x0 + 0.9) + UP * y, color=c, stroke_width=4)
                g.add(ln, MathTex(txt, font_size=26, color=c).next_to(ln, RIGHT, buff=0.12))
            g.add(note(scale_note).move_to(RIGHT * x0 + DOWN * 2.85))
            return g

        bohr = col(-5.2, r"Bohr / Schr\"odinger", [(-0.6, r"n = 2", C.ENERGY)], f"{E2:.2f} eV, all states")
        dirac = col(-0.9, r"Dirac", [(0.9, r"2P_{3/2}", C.DIRAC_POS), (-1.6, r"2S_{1/2}, 2P_{1/2}", C.DIRAC_POS)],
                    r"splitting " + f"{fs:.2f}" + r" GHz (measured " + f"{fsm:.3f}" + r")")
        qed = col(3.6, r"+ QED", [(0.7, r"2S_{1/2}", C.APPROX), (-1.2, r"2P_{1/2}", C.DIRAC_POS)], r"Lamb shift: " + f"{lamb:.1f}" + r" MHz")
        z1 = DashedLine(bohr[2].get_right() + RIGHT * 0.15, RIGHT * -2.0 + UP * -0.35, color=GREY_D)
        z2 = DashedLine(dirac[4].get_corner(UR) + RIGHT * 0.1, RIGHT * 2.6 + UP * -0.25, color=GREY_D)
        zl1 = label(r"zoom $\times 10^{5}$", font_size=20, color=GREY_B).next_to(z1, UP, buff=0.05)
        zl2 = label(r"zoom $\times 10$", font_size=20, color=GREY_B).next_to(z2, UP, buff=0.05)
        lr = note(r"Lamb \& Retherford (1947): ``about 1000 Mc/sec''").to_edge(DOWN, buff=0.15).shift(RIGHT * 3.0)
        with self.voiceover(
            "Dirac's equation can be solved exactly for hydrogen, <bookmark mark='a'/> and the energies depend not just "
            "on n but on j, the total angular momentum including spin. <bookmark mark='b'/> Zoom in on the second level. "
            "In Schrödinger's theory it's a single energy, minus 3.4 electron volts. <bookmark mark='c'/> In Dirac's, it "
            "splits: the 2 P three-halves states sit higher by 10.94 gigahertz, about forty-five millionths of an "
            "electron volt, within a quarter of a percent of the measured splitting. <bookmark mark='d'/> But Dirac's theory "
            "leaves 2 S one-half and 2 P one-half exactly together. In 1947 Willis Lamb and Robert Retherford found them "
            "apart by about a thousand megahertz, now measured as 1057.8. <bookmark mark='e'/> Explaining that shift, "
            "the electron interacting with fluctuations of the field itself, launched quantum electrodynamics."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(form), FadeIn(fn))
            vo.wait_until("b")
            self.play(FadeIn(bohr))
            vo.wait_until("c")
            self.play(Create(z1), FadeIn(zl1), FadeIn(dirac))
            vo.wait_until("d")
            self.play(Create(z2), FadeIn(zl2), FadeIn(qed), FadeIn(lr))
            vo.wait_until("e")
            self.play(Indicate(qed[3], color=C.APPROX))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layers(self):
        items = [
            (r"Schr\"odinger", r"$-13.6\,\text{eV}/n^2$", C.ENERGY),
            (r"Dirac", r"spin, $g = 2$, fine structure, antimatter", C.DIRAC_POS),
            (r"quantum electrodynamics", r"the Lamb shift, $g - 2$: agreement to 12 digits", C.APPROX),
        ]
        sizes = [(6.0, 1.2, -1.6), (9.0, 3.4, -0.75), (12.0, 5.8, -0.05)]  # width, height, center y
        boxes, heads = VGroup(), VGroup()
        for (a, b, c), (w, hgt, y) in zip(items, sizes):
            bx = RoundedRectangle(corner_radius=0.2, width=w, height=hgt, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.06).move_to(UP * y + DOWN * 0.2)
            hd = VGroup(label(a, font_size=34, color=c), label(b, font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
            hd.next_to(bx.get_corner(UL), DR, buff=0.22)
            boxes.add(bx)
            heads.add(hd)
        with self.voiceover(
            "Each layer of the theory contains the one before it, and each new decimal place has been checked: "
            "<bookmark mark='a'/> Schrödinger's equation, <bookmark mark='b'/> Dirac's, <bookmark mark='c'/> and quantum "
            "electrodynamics, the most precisely tested theory in science."
        ) as vo:
            vo.wait_until("a")
            self.play(DrawBorderThenFill(boxes[0]), FadeIn(heads[0]))
            vo.wait_until("b")
            self.play(DrawBorderThenFill(boxes[1]), FadeIn(heads[1]))
            vo.wait_until("c")
            self.play(DrawBorderThenFill(boxes[2]), FadeIn(heads[2]))
        self.wait(0.5)
        self.clear_scene()
