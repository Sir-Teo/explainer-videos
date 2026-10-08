from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import RELEASE, label, note, schematic_tag


def box(text: str, color=WHITE, width=3.2, height=1.1, font_size=26) -> VGroup:
    r = RoundedRectangle(width=width, height=height, corner_radius=0.12, color=color, stroke_width=2).set_fill(color, opacity=0.08)
    t = label(text, font_size=font_size, color=color)
    if t.width > width - 0.3:
        t.width = width - 0.3
    return VGroup(r, t.move_to(r))


class Descent(VoiceoverScene):
    def construct(self):
        self.cubes()
        self.recursion()
        self.seven_eighths()
        self.lineage()

    # ------------------------------------------------------------------
    def cubes(self):
        head = label(r"One catch: the theta function's coefficients also sit at indices $n\,b^3$", font_size=34).to_edge(UP, buff=0.5)
        coef = MathTex(r"c_\theta(n\,b^3)", r"\;\propto\;", r"|b|", r"\cdot", r"\gamma_2(n)", font_size=44).next_to(head, DOWN, buff=0.45)
        coef[0].set_color(C.THETA)
        coef[4].set_color(C.THETA)
        T = MathTex(r"T(X)", r"=", r"\sum_{b} \frac{w(b)}{N(b)}\; P\!\Big(\frac{X}{N(b)^3}\Big)", font_size=42)
        Pm = MathTex(r"P(X)", r"=", r"\sum_{d} \frac{\mu(d)\,w(d)}{N(d)}\; T\!\Big(\frac{X}{N(d)^3}\Big)", font_size=42)
        VGroup(T, Pm).arrange(DOWN, buff=0.55).next_to(coef, DOWN, buff=0.6)
        T[0].set_color(C.THETA)
        Pm[0].set_color(C.MOBIUS)
        tl = label(r"completed sum: what the theta symmetry controls", font_size=24, color=C.THETA).next_to(T, RIGHT, buff=0.4)
        pl = label(r"the part we want (cube-free), by M\"obius inversion", font_size=24, color=C.MOBIUS).next_to(Pm, RIGHT, buff=0.4)
        VGroup(T, Pm, tl, pl).shift(LEFT * 2.6)
        with self.voiceover(
            "There's one catch. <bookmark mark='c'/> The theta function's coefficients aren't only cubic Gauss sums at squarefree "
            "indices. It also has coefficients at n times a cube. <bookmark mark='t'/> So the symmetry controls a 'completed' sum, "
            "with all the cube layers included. <bookmark mark='p'/> To isolate the part we want, the proof subtracts the cube "
            "layers back off, using Möbius inversion, the same trick Euler's sieve used."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("c")
            self.play(Write(coef))
            vo.wait_until("t")
            self.play(Write(T), FadeIn(tl))
            vo.wait_until("p")
            self.play(Write(Pm), FadeIn(pl))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recursion(self):
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1], x_length=5.4, y_length=5.4, tips=True,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 4.0 + DOWN * 0.3)
        xl = label(r"$\log$ (length of each sum)", font_size=24).next_to(ax.x_axis.get_end(), DOWN, buff=0.15).shift(LEFT * 1.2)
        yl = label(r"$\log$ (number of rows)", font_size=24).next_to(ax.y_axis.get_end(), RIGHT, buff=0.15)
        floor = Polygon(ax.c2p(0, 0), ax.c2p(10, 0), ax.c2p(10, 1.0), ax.c2p(0, 1.0), stroke_width=0, fill_color=C.ZERO_FREE,
                        fill_opacity=0.25)
        floor_l = label(r"few enough rows: just count", font_size=22, color=C.ZERO_FREE).move_to(ax.c2p(6.3, 0.5))
        pts = [(9.2, 8.6), (7.4, 6.8), (5.0, 4.4), (3.1, 2.5), (1.4, 0.8)]
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.09, color=C.MOBIUS) for p in pts])
        hops = VGroup(*[Arrow(ax.c2p(*pts[i]), ax.c2p(*pts[i + 1]), buff=0.12, color=C.MOBIUS, stroke_width=3)
                        for i in range(len(pts) - 1)])
        diag = DashedLine(ax.c2p(0.6, 0), ax.c2p(10, 9.4), color=GREY_C, stroke_width=1.5)
        diag_l = label(r"same ratio\\rows : length", font_size=22, color=GREY_B).move_to(ax.c2p(7.6, 4.6))
        tag = schematic_tag(UL)
        fl = dict(font_size=26, tex_environment="flushleft")
        steps = VGroup(
            label(r"small cubes: \ bound them directly", **fl),
            label(r"large cubes: \ two more Poisson summations turn them\\into a mean square \emph{of the same kind},\\"
                  r"with both scales shrunk by the same factor", **fl),
            MathTex(r"(H, X) \;\longrightarrow\; \Big(\frac{H}{N(b)^3}, \frac{X}{N(b)^3}\Big)", font_size=34, color=C.MOBIUS),
            label(r"each round shrinks the scales by a fixed power:\\after finitely many rounds, the sums are tiny", **fl),
            label(r"unwind $\Rightarrow$ the crucial estimate\\$\Rightarrow$ $\Real(s) > \tfrac{11}{12}$ is zero-free",
                  font_size=28, color=C.ZERO_FREE, tex_environment="flushleft"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.4 + DOWN * 0.1)
        with self.voiceover(
            "Small cubes are harmless, and are bounded directly. <bookmark mark='l'/> For the large ones, two more rounds of "
            "Poisson summation turn the leftover into a mean square of exactly the same kind, but with both of its size "
            "parameters shrunk by the same factor. <bookmark mark='s'/> So the problem reproduces itself at a smaller scale."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tag), FadeIn(steps[0]))
            vo.wait_until("l")
            self.play(FadeIn(steps[1]), FadeIn(dots[0], scale=2), Create(diag), FadeIn(diag_l))
            vo.wait_until("s")
            self.play(FadeIn(steps[2]), GrowArrow(hops[0]), FadeIn(dots[1], scale=2))
        with self.voiceover(
            "Each round shrinks the scales by a fixed power, <bookmark mark='f'/> so after finitely many rounds the sums are so "
            "short that you can simply count. <bookmark mark='u'/> Unwinding the recursion proves the crucial estimate, and with "
            "it, the zero-free half-plane at eleven twelfths."
        ) as vo:
            self.play(FadeIn(steps[3]))
            for i in range(1, len(hops)):
                self.play(GrowArrow(hops[i]), FadeIn(dots[i + 1], scale=2), run_time=0.6)
            vo.wait_until("f")
            self.play(FadeIn(floor), FadeIn(floor_l))
            vo.wait_until("u")
            self.play(FadeIn(steps[4]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def seven_eighths(self):
        head = label(rf"The {RELEASE['pages_78']}-page paper: \ from $\tfrac{{11}}{{12}}$ to $\tfrac78$", font_size=38).to_edge(UP, buff=0.5)
        start = box(r"Part I:\\$\Real(s) > \tfrac{11}{12}$ zero-free\\(a different route)", color=YELLOW, width=3.2, height=1.6)
        end = box(r"Part II:\\$\Real(s) > \tfrac78$ zero-free", color=C.ZERO_FREE, width=3.0, height=1.6)
        ingredients = VGroup(
            box(r"a ``zero detector''", width=3.6, height=0.7),
            box(r"prime compensation", width=3.6, height=0.7),
            box(r"asymmetric scales", width=3.6, height=0.7),
            box(r"two new moment estimates", width=3.6, height=0.7),
        ).arrange(DOWN, buff=0.22)
        row = VGroup(start, ingredients, end).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.2)
        a1 = Arrow(start.get_right(), ingredients.get_left(), buff=0.15, color=GREY_B)
        a2 = Arrow(ingredients.get_right(), end.get_left(), buff=0.15, color=GREY_B)
        fine = note(r"same skeleton: compare two exact representations of a completed cubic-theta sum ---\\"
                    r"the theta reflection, and Poisson summation --- with power savings uniform in the character",
                    font_size=24).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "That's the 49-page argument. The 199-page paper reaches eleven twelfths by a somewhat different route, <bookmark mark='d'/> "
            "using what it calls a zero detector, <bookmark mark='i'/> and then starts from that result and pushes further: "
            "<bookmark mark='p'/> with prime compensation, asymmetric scales, and two new moment estimates. "
            "<bookmark mark='e'/> Together, they move the line from eleven twelfths to seven eighths. The skeleton is the same: "
            "compare two exact ways of writing one sum, the theta reflection and Poisson summation, and win by a power."
        ) as vo:
            self.play(FadeIn(head), FadeIn(start))
            vo.wait_until("d")
            self.play(GrowArrow(a1), FadeIn(ingredients[0]))
            vo.wait_until("i")
            self.play(Indicate(start, color=YELLOW))
            vo.wait_until("p")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in ingredients[1:]], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(GrowArrow(a2), FadeIn(end))
            self.play(FadeIn(fine))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lineage(self):
        items = [
            ("1846", r"Kummer: cubic Gauss sums"),
            ("1969", r"Kubota: metaplectic forms"),
            ("1977", r"Patterson: the cubic theta function"),
            ("1979", r"Heath-Brown \& Patterson"),
            ("1995", r"Heath-Brown: quadratic large sieve"),
            ("2000", r"Heath-Brown: cubic Gauss sums, Kummer's conjecture"),
            ("2010s", r"Goldmakher \& Louvel; Blomer, Goldmakher \& Louvel"),
            ("2024", r"Dunn \& Radziwi\l\l: bias in cubic Gauss sums"),
            ("2026", r"OpenAI's model: the quasi-Riemann claim"),
        ]
        rows = VGroup()
        for y, t in items:
            rows.add(VGroup(label(rf"\textbf{{{y}}}", font_size=26, color=C.THETA), label(t, font_size=26)).arrange(RIGHT, buff=0.3))
        for r in rows:
            r[0].set_width(r[0].width)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(LEFT * 2.6)
        rows[-1].set_color(C.ZERO_FREE)
        line = Line(rows[0].get_left() + LEFT * 0.3 + UP * 0.1, rows[-1].get_left() + LEFT * 0.3 + DOWN * 0.1, color=GREY_C)
        side = VGroup(
            label(r"None of the ingredients is alien.", font_size=32),
            label(r"By the paper's own account, the new\\contribution is how they are fitted\\together --- with the savings"
                  r"\\uniform in every character.", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 4.3)
        with self.voiceover(
            "None of these ingredients is alien. <bookmark mark='l'/> Gauss sums, the cubic theta function, large sieves, and "
            "recursive arguments like this one go back to Kummer, Kubota, Patterson, Heath-Brown, and more recently Goldmakher, "
            "Louvel, Blomer, Dunn and Radziwiłł. <bookmark mark='n'/> By the paper's own account, what's new is the way the pieces "
            "are fitted together, with savings that hold uniformly for every character."
        ) as vo:
            self.play(FadeIn(side[0]))
            vo.wait_until("l")
            self.play(Create(line), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.15), run_time=3)
            vo.wait_until("n")
            self.play(FadeIn(side[1]))
        self.wait(0.8)
        self.clear_scene()
