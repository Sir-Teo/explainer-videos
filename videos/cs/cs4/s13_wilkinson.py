from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, load, sci


class Wilkinson(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_questions()
        self.polynomial()
        self.why()
        self.lesson()

    def card(self):
        card = chapter_card(12, r"Conditioning and stability", r"Is it the problem or the algorithm?", lit=(1959, 1963),
                            part=PART)
        with self.voiceover("Chapter twelve. Conditioning and stability."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def two_questions(self):
        head = label(r"Two different questions", font_size=38).to_edge(UP, buff=0.35)
        cond = VGroup(label(r"conditioning: \ a property of the \textit{problem}", font_size=30, color=HEAD),
                      MathTex(r"\kappa = \frac{|\Delta f| / |f|}{|\Delta x| / |x|}", font_size=40, color=CODE),
                      label(r"how much a small change in the input \\ can change the exact answer", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.25).move_to(LEFT * 3.4 + UP * 0.6)
        stab = VGroup(label(r"stability: \ a property of the \textit{algorithm}", font_size=30, color=YES),
                      MathTex(r"\hat f(x) = f(x + \Delta x), \ \ |\Delta x| \lesssim u\,|x|", font_size=34, color=CODE),
                      label(r"backward stable: \ the exact answer \\ to a slightly different question", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.4 + UP * 0.6)
        rule = MathTex(r"\text{error} \;\lesssim\; \kappa \times u", font_size=46, color=NO).move_to(DOWN * 2.0)
        ex = note(r"chapter 11's $(1 - \cos x)/x^2$ is well conditioned ($\kappa \approx 1$): \ the formula was the "
                  r"unstable part", font_size=22).next_to(rule, DOWN, buff=0.3)
        with self.voiceover(
            "When a computed answer is wrong, there are two different suspects. <bookmark mark='a'/> The first is the "
            "problem itself. Its condition number measures how much a small relative change in the input can change "
            "the exact answer. Subtracting two nearly equal numbers is badly conditioned: a tiny change in either "
            "changes the difference enormously. <bookmark mark='b'/> The second is the algorithm. A backward-stable "
            "algorithm returns the exact answer to a slightly perturbed question, perturbed by about u. "
            "<bookmark mark='c'/> Put together, the error of a stable algorithm is about the condition number times u. "
            "Chapter eleven's function was perfectly well conditioned; the formula was unstable, and rewriting it "
            "fixed everything. But if the problem itself is ill conditioned, no algorithm and no rewriting can save "
            "you. James Wilkinson found that out, painfully, in 1959."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cond, lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(stab, lag_ratio=0.2))
            vo.wait_until("c")
            self.play(Write(rule), FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def polynomial(self):
        d = load("wilkinson")
        frames = d["frames"]
        head = label(r"Wilkinson's polynomial", font_size=38).to_edge(UP, buff=0.3)
        p = MathTex(r"p(x) = (x - 1)(x - 2) \cdots (x - 20) = x^{20} - 210\, x^{19} + \cdots + 20!", font_size=34,
                    color=CODE).next_to(head, DOWN, buff=0.25)
        plane = ComplexPlane(x_range=[0, 22, 2], y_range=[-3.5, 3.5, 1], x_length=12.0, y_length=4.4,
                             background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.5},
                             axis_config={"color": GREY_C}).move_to(DOWN * 1.1)
        nums = VGroup(*[MathTex(str(k), font_size=20, color=GREY_B).next_to(plane.n2p(k), DOWN, buff=0.12)
                        for k in range(2, 22, 2)])
        im = MathTex(r"\mathrm{Im}", font_size=22, color=GREY_B).next_to(plane.c2p(0, 3.5), RIGHT, buff=0.1)
        t = ValueTracker(0)

        def roots():
            k = t.get_value() * (len(frames) - 1)
            i = int(np.floor(k))
            j = min(i + 1, len(frames) - 1)
            a = k - i
            pts = [(1 - a) * np.array(frames[i][r]) + a * np.array(frames[j][r]) for r in range(20)]
            return VGroup(*[Dot(plane.c2p(x, y), radius=0.08, color=NO if abs(y) > 1e-3 else YES) for x, y in pts])

        dots = always_redraw(roots)
        pert = MathTex(r"-210 \;\to\; -210 - 2^{-23}", font_size=34, color=NO).to_corner(UR, buff=0.4).shift(DOWN * 0.9)
        pl = note(r"a change of $1.2 \times 10^{-7}$ \ in one coefficient", font_size=22).next_to(pert, DOWN, buff=0.1)
        res = label(r"roots $16.73 \pm 2.81\,i$, \ $19.50 \pm 1.94\,i$, \ ... \ (computed with 60 digits)",
                    font_size=24, color=NO).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Wilkinson was testing a root-finding program on the Pilot ACE computer in London, and chose an easy "
            "polynomial: the one whose roots are one, two, three, up to twenty. <bookmark mark='a'/> Multiplied out, "
            "its coefficients are huge integers, from minus two hundred and ten down to twenty factorial. "
            "<bookmark mark='b'/> Here are its roots, the integers on the real line. <bookmark mark='c'/> Now change "
            "one coefficient, the minus two hundred and ten in front of x to the nineteen, by two to the minus "
            "twenty-three, about one part in two billion of it, and watch the roots, computed here with sixty-digit "
            "arithmetic so that no rounding interferes. <bookmark mark='d'/> The small roots barely move. The large "
            "ones collide in pairs and leave the real line: ten of them become complex, with imaginary parts as large "
            "as two point eight. This is not rounding error. It is the exact answer to the slightly different "
            "question. Wilkinson later called it the most traumatic experience of his career as a numerical analyst."
        ) as vo:
            self.play(FadeIn(head), Write(p))
            vo.wait_until("b")
            self.play(Create(plane), FadeIn(nums), FadeIn(im), FadeIn(dots))
            vo.wait_until("c")
            self.play(FadeIn(pert), FadeIn(pl))
            vo.wait_until("d")
            self.play(t.animate.set_value(1.0), run_time=6.0, rate_func=smooth)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        d = load("wilkinson")
        cond = d["cond"]
        head = label(r"How sensitive is each root?", font_size=38).to_edge(UP, buff=0.35)
        f = MathTex(r"\left|\frac{\partial r_k}{\partial a_{19}}\right| = \frac{k^{19}}{\prod_{j \ne k} |k - j|}",
                    font_size=42, color=CODE).move_to(LEFT * 3.6 + UP * 1.4)
        how = note(r"differentiate $p(r_k) = 0$ \ with respect to the coefficient", font_size=22).next_to(f, DOWN,
                                                                                                         buff=0.25)
        ax = Axes(x_range=[0, 21, 5], y_range=[-2, 10, 2], x_length=6.2, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(RIGHT * 3.2 + DOWN * 0.5)
        yl = note(r"$\log_{10}$ of the sensitivity", font_size=20).next_to(ax, UP, buff=0.1)
        bars = VGroup(*[Rectangle(width=0.2, height=max(ax.c2p(0, np.log10(c))[1] - ax.c2p(0, -2)[1], 0.01),
                                  stroke_width=0, fill_color=NO if np.log10(c) > 6 else INF, fill_opacity=0.85).move_to(
            ax.c2p(k, -2), aligned_edge=DOWN) for k, c in enumerate(cond, start=1)])
        big = label(rf"root 16: \ ${sci(cond[15])}$ \\ times a change of $10^{{-7}}$: \ a shift of hundreds", font_size=26,
                    color=NO).move_to(LEFT * 3.6 + DOWN * 1.4)
        with self.voiceover(
            "Why are the large roots so fragile? <bookmark mark='a'/> Differentiate the equation p of r equals zero "
            "with respect to that coefficient, and the sensitivity of root k comes out as k to the nineteen, over the "
            "product of its distances to all the other roots. <bookmark mark='b'/> For the small roots that is "
            "modest. For roots in the middle teens, k to the nineteen is astronomical, and the product below it is "
            "not: root sixteen has a sensitivity of about two billion. <bookmark mark='c'/> Two billion times a change "
            "of a ten-millionth is a change of hundreds, far beyond the linear estimate's range, which is why the "
            "roots do not just shift but leave the line. The problem of finding roots from coefficients is ill "
            "conditioned, and nothing about the algorithm can fix that."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(how))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(big))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lesson(self):
        head = label(r"What numerical software learned", font_size=38).to_edge(UP, buff=0.4)
        lines = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"never find eigenvalues through the characteristic polynomial", GREY_A),
            (r"backward-stable algorithms everywhere: \ QR, \ LU with pivoting, \ the FFT", YES),
            (r"report the condition number, \ not just the answer", HEAD),
            (r"LAPACK, \ numpy, \ MATLAB, \ and every ML framework rest on this theory", GREY_A),
            (r"more in Part 52, \ \textit{Computing with Real Numbers}", GREY_B),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Wilkinson turned that shock into a discipline. <bookmark mark='a'/> Never compute eigenvalues by forming "
            "a characteristic polynomial and finding its roots: the coefficients destroy the information. "
            "<bookmark mark='b'/> Use algorithms that are backward stable, like the QR algorithm, Gaussian elimination "
            "with pivoting and the fast Fourier transform. <bookmark mark='c'/> And report how well conditioned a "
            "problem is along with its answer. <bookmark mark='d'/> Every numerical library we use, LAPACK under "
            "numpy and MATLAB, and the linear algebra inside every machine learning framework, is built on his "
            "theory, and Part 52 of this series returns to it in depth."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines[:4]):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=RIGHT * 0.1))
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()
