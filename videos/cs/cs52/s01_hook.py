from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

TOP10 = [(r"1946", r"the Monte Carlo method", True), (r"1947", r"the simplex method", True),
         (r"1950", r"Krylov subspace iteration", True), (r"1951", r"matrix decompositions", True),
         (r"1957", r"the Fortran optimizing compiler", False), (r"1959--61", r"the QR algorithm", True),
         (r"1962", r"Quicksort", False), (r"1965", r"the fast Fourier transform", True),
         (r"1977", r"integer relation detection", True), (r"1987", r"the fast multipole method", True)]


class Hook(VoiceoverScene):
    def construct(self):
        self.ten()
        self.trust()
        self.plan()

    def ten(self):
        head = label(r"Ten algorithms of the twentieth century", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        for y, name, num in TOP10:
            r = VGroup(label(y, font_size=20, color=GREY_B), label(name, font_size=22, color=WHITE))
            r[1].next_to(r[0], RIGHT, buff=0.3)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        left, right = VGroup(*rows[:5]), VGroup(*rows[5:])
        left.move_to(LEFT * 3.3 + DOWN * 0.1)
        right.move_to(RIGHT * 3.3 + DOWN * 0.1)
        right.align_to(left, UP)
        src = note(r"Dongarra and Sullivan, \ \textit{Computing in Science and Engineering}, \ January 2000",
                   font_size=16).to_edge(DOWN, buff=0.3)
        marks = VGroup(*[SurroundingRectangle(rows[i], color=HEAD, buff=0.08, stroke_width=1.6)
                         for i, (_, _, num) in enumerate(TOP10) if num])
        foot = label(r"eight of the ten compute with real numbers", font_size=24, color=HEAD)
        foot.next_to(src, UP, buff=0.35)
        with self.voiceover(
            "In the year 2000 a journal asked two numerical analysts to name the ten algorithms that had done most "
            "to shape science and engineering in the twentieth century. <bookmark mark='a'/> Their list runs from "
            "the Monte Carlo method, born at Los Alamos in 1946, through the simplex method, "
            "Krylov iterations, matrix decompositions, the first optimizing compiler, the QR algorithm, Quicksort, "
            "the fast Fourier transform, integer relation detection and the fast multipole method. "
            "<bookmark mark='b'/> Eight of the ten compute with real numbers. This part is about them, and about the "
            "question that hangs over every one: when every operation rounds, which answers can we trust?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.25), run_time=5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.1), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def trust(self):
        p = {r["eps"]: r for r in load("pivot")["rows"]}[1e-20]
        head = label(r"Two equations, \ two unknowns, \ one wrong answer", font_size=36).to_edge(UP, buff=0.3)
        sys_ = MathTex(r"10^{-20}\,x_1 + x_2 = 1", r"\\", r"x_1 + x_2 = 2", font_size=44).next_to(head, DOWN,
                                                                                                buff=0.6)
        exact = label(r"exact: \ $x_1 \approx 1$, \ $x_2 \approx 1$", font_size=26, color=YES).next_to(sys_, DOWN,
                                                                                                 buff=0.5)
        naive = label(rf"elimination as taught: \ $x_1 = {p['no_pivot'][0]:g}$, \ $x_2 = {p['no_pivot'][1]:g}$",
                      font_size=26, color=NO).next_to(exact, DOWN, buff=0.35)
        piv = label(rf"swap the rows first: \ $x_1 = {p['pivot'][0]:g}$, \ $x_2 = {p['pivot'][1]:g}$", font_size=26,
                    color=YES).next_to(naive, DOWN, buff=0.35)
        foot = wrapped_label(r"the problem is not hard: \ it is well conditioned. \ The algorithm was unstable. \ "
                             r"Telling those two apart is this part's first lesson", 12.0, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is the question in miniature. <bookmark mark='a'/> Two equations in two unknowns. The answer is "
            "almost exactly one and one. <bookmark mark='b'/> Gaussian elimination, done the way it is taught in "
            "school, in double precision, answers that the first unknown is zero. Every digit is wrong. "
            "<bookmark mark='c'/> Swap the two equations before eliminating, and the same arithmetic gets it right. "
            "<bookmark mark='d'/> Nothing about the problem is difficult. A tiny change in the data changes the "
            "answer only a little. The algorithm was the problem. Separating the difficulty of a problem from the "
            "quality of an algorithm is the first idea of numerical analysis, and the rest of the part is built on it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(sys_), FadeIn(exact))
            vo.wait_until("b")
            self.play(FadeIn(naive, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(piv, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Computing with Real Numbers", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"conditioning against stability, \ and backward error",
            r"elimination, \ pivoting, \ QR and the SVD",
            r"the QR algorithm, \ conjugate gradients and multigrid",
            r"Newton's method, \ and its fractal",
            r"interpolation, \ quadrature and stiff equations",
            r"why fast code is matrix multiplication",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 52 of Computer Science, Built, and it opens where Part 4 left off, with numbers that round. "
            "<bookmark mark='a'/> We will separate a problem's conditioning from an algorithm's stability; solve "
            "linear systems by elimination, QR and the SVD; find eigenvalues by an iteration that converges "
            "cubically; solve a million equations with conjugate gradients and multigrid; follow Newton's method into "
            "its fractal; interpolate, integrate, and step through stiff equations; and see why the fastest code on "
            "every machine is matrix multiplication."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO, YES)
