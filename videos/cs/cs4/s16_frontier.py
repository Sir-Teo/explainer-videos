from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, LIMIT, NO, PART, YES, fmt,
                                  load, say)


class Frontier(VoiceoverScene):
    """The research tier (videos/cs/SYLLABUS.md 1.1): how fast two numbers can be multiplied, and whether the
    functions of a math library can all be correctly rounded; both measured on the machine that renders the video."""

    def construct(self):
        self.card()
        self.multiply()
        self.record()
        self.rounding()
        self.dilemma()

    def card(self):
        card = chapter_card(15, r"Frontier: \ arithmetic's open questions", r"How fast can we multiply, \ and how exactly "
                            r"can we compute $e^x$?", lit=(1971, 2019, 2022), part=PART,
                            extra=((1971, r"Sch\"onhage and Strassen"), (2019, r"multiplication in $O(n \log n)$"),
                                   (2022, r"CORE-MATH")))
        with self.voiceover("Chapter fifteen. Frontier: arithmetic's open questions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def multiply(self):
        d = load("frontier")
        head = label(r"Multiplying huge numbers, \ measured on this machine", font_size=34).to_edge(UP, buff=0.3)
        sub = label(rf"{d['cpu']}; \ Python's integers and its \texttt{{decimal}} module", font_size=20,
                    color=GREY_B).next_to(head, DOWN, buff=0.15)
        mul = d["mul"]
        ax = Axes(x_range=[3, 6, 1], y_range=[-5, 0, 1], x_length=6.4, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 2.4 + DOWN * 0.5)
        xt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(k, -5), DOWN, buff=0.12)
                      for k in (3, 4, 5, 6)])
        yt = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(3, k), LEFT, buff=0.1)
                      for k, t in ((-4, r"0.1 ms"), (-2, r"10 ms"), (0, r"1 s"))])
        xl = note(r"digits in each factor", font_size=18).next_to(xt, DOWN, buff=0.08)
        lx = [np.log10(m["digits"]) for m in mul]
        ci = VMobject(color=NO, stroke_width=3).set_points_as_corners([ax.c2p(x, np.log10(m["int"])) for x, m in
                                                                      zip(lx, mul)])
        cd = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(x, np.log10(m["decimal"])) for x, m in
                                                                       zip(lx, mul)])
        dots = VGroup(*[Dot(ax.c2p(x, np.log10(m[k])), radius=0.05, color=c) for x, m in zip(lx, mul)
                        for k, c in (("int", NO), ("decimal", YES))])
        side = VGroup(
            label(rf"\texttt{{int}}: \ Karatsuba \ (Part 19), \ time $\propto n^{{{d['slope_int']:.2f}}}$", font_size=20,
                  color=NO),
            label(rf"\texttt{{decimal}}: \ a number-theoretic transform, \ time $\propto n^{{{d['slope_dec']:.2f}}}$",
                  font_size=20, color=YES),
            label(rf"a million digits: \ {d['ratio_1m']:.1f} times faster \ (the FFT of Part 19, \\ done in modular "
                  r"arithmetic, \ Part 2's clock)", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.2)
        slope_i, slope_d, ratio = f"{d['slope_int']:.1f}", f"{d['slope_dec']:.1f}", f"{d['ratio_1m']:.0f}"
        with self.voiceover(
            "Chapter six multiplied numbers the way school does, in time proportional to the square of their length. "
            "How fast can it really be done? <bookmark mark='a'/> Here are two multipliers already inside Python, timed "
            "on this machine. <bookmark mark='b'/> Python's integers switch to Karatsuba's method, which Part 19 "
            f"derives, and their time grows like the length to the power of about {slope_i}. "
            "<bookmark mark='c'/> Python's decimal module, for very long numbers, multiplies with a number-theoretic "
            "transform: a fast Fourier transform done in modular arithmetic, so that no rounding happens at all. Its "
            f"time grows almost linearly, and at a million digits it is about {ratio} times faster."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(dots))
            vo.wait_until("b")
            self.play(Create(ci), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(cd), FadeIn(side[1]))
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def record(self):
        head = label(r"The race to $n \log n$", font_size=36).to_edge(UP, buff=0.3)
        rows = [
            (r"antiquity", r"n^2", r"schoolbook", GREY_A),
            (r"1960", r"n^{1.585}", r"Karatsuba", GREY_A),
            (r"1963", r"n^{1 + \varepsilon}", r"Toom and Cook", GREY_A),
            (r"1971", r"n \log n \log\log n", r"Sch\"onhage and Strassen, \ the FFT", DATA),
            (r"2007", r"n \log n \, 2^{O(\log^* n)}", r"F\"urer", DATA),
            (r"2019", r"n \log n", r"Harvey and van der Hoeven", HEAD),
        ]
        tab = VGroup()
        for k, (yr, f, who, c) in enumerate(rows):
            y = 2.0 - 0.58 * k
            tab.add(VGroup(label(yr, font_size=22, color=HIST).move_to([-5.0, y, 0]),
                           MathTex(f, font_size=32, color=c).move_to([-3.6, y, 0], aligned_edge=LEFT),
                           label(who, font_size=22, color=GREY_A).move_to([0.2, y, 0], aligned_edge=LEFT)))
        notes = VGroup(
            label(r"Sch\"onhage and Strassen conjectured $n \log n$ in 1971; \ Harvey and van der Hoeven reached it with "
                  r"a 1729-dimensional Fourier transform", font_size=20, color=GREY_A),
            label(r"an illustrative asymptotic crossover estimate is $2^{1729^{12}}$ bits: \ a \textit{galactic} algorithm, \ "
                  r"important for what it proves", font_size=20, color=LIMIT),
            label(r"unconditional: $\Omega(n)$; \ conditional: $\Omega(n\log n)$ circuit size \ "
                  r"for constant-degree Boolean circuits \ (Afshani et al., 2019; network coding conjecture)", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The theory went further than any library. <bookmark mark='a'/> Anatoly Karatsuba broke the square in 1960, "
            "Toom and Cook pushed the exponent towards one, and in 1971 Arnold Schönhage and Volker Strassen used the "
            "fast Fourier transform to reach n log n times log log n, and conjectured that n log n was the truth. "
            "<bookmark mark='b'/> Martin Fürer improved the last factor in 2007, and in 2019 David Harvey and Joris van "
            "der Hoeven reached n log n itself, with a Fourier transform in one thousand seven hundred and twenty-nine "
            "dimensions. <bookmark mark='c'/> An illustrative asymptotic crossover estimate is two to the "
            "seventeen-twenty-nine to the twelfth bits, far beyond practical sizes. That is not a measured or "
            "exact threshold. <bookmark mark='d'/> Is n log n optimal? We have a linear unconditional lower "
            "bound. A 2019 result gives n log n circuit size for constant-degree Boolean circuits, conditional "
            "on a conjecture about network coding. It is not an unconditional runtime bound."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab[:3]))
            vo.wait_until("a")
            self.play(Indicate(tab[:3], scale_factor=1.02), FadeIn(tab[3]))
            vo.wait_until("b")
            self.play(FadeIn(tab[4]), FadeIn(tab[5]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rounding(self):
        d = load("frontier")
        head = label(r"Is $e^x$ correctly rounded?", font_size=36).to_edge(UP, buff=0.3)
        rule = VGroup(
            label(r"IEEE 754 \ (chapter 10): \ $+$, $-$, $\times$, $\div$, $\sqrt{\ }$ \ must be correctly rounded", font_size=22,
                  color=YES),
            label(r"$e^x$, \ $\log x$, \ $\sin x$: \ only \textit{recommended}", font_size=22, color=LIMIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(UP * 2.0)
        ul = d["exp_ulps"]
        ks = sorted(int(k) for k in ul)
        bars = VGroup()
        for k in ks:
            v = ul[str(k)] / d["exp_n"]
            w = 6.0 * v
            y = 0.5 - 0.7 * k
            r = Rectangle(width=max(w, 0.03), height=0.45, stroke_width=0, fill_color=YES if k == 0 else NO,
                          fill_opacity=0.75).move_to([-2.0 + w / 2, y, 0])
            bars.add(VGroup(label(rf"{k} ulp{'s' if k != 1 else ''} off", font_size=20, color=GREY_A).next_to(
                [-2.1, y, 0], LEFT, buff=0.1), r, label(rf"{100 * v:.1f}\%", font_size=20, color=GREY_A).next_to(
                r, RIGHT, buff=0.12)))
        cap = label(rf"NumPy {d['numpy']}'s \texttt{{float32}} \texttt{{exp}} \ on ${fmt(d['exp_n'])}$ random inputs, \ "
                    rf"against float64 exp rounded to float32 \\ ({d['exp_checked']} disagreements rechecked with "
                    rf"200-bit \texttt{{mpmath}}: \ {d['exp_agree']} confirm the reference)", font_size=18,
                    color=GREY_B).next_to(bars, DOWN, buff=0.35)
        why = label(r"accuracy and speed depend on the library, \ CPU and vector path", font_size=22,
                    color=HEAD).to_edge(DOWN, buff=0.35)
        pct = f"{100 * d['exp_frac']:.0f}"
        mx = d["exp_max_ulp"]
        with self.voiceover(
            "The second question is about chapter fourteen's functions. <bookmark mark='a'/> The IEEE standard requires "
            "addition, subtraction, multiplication, division and square root to be correctly rounded: the exact answer, "
            "rounded once. For the exponential, the logarithm and the sines it only recommends it. "
            "<bookmark mark='b'/> So we tested the single-precision exponential of NumPy, on this machine, on ten "
            "million random inputs, against a float64 exponential rounded to float32. We rechecked two hundred "
            "disagreements at two hundred bits; that validates those cases, not every reference value. "
            f"<bookmark mark='c'/> About {pct} percent disagree with the reference, by one unit in the last "
            f"place or, rarely, {mx}. <bookmark mark='d'/> Accuracy and speed depend on the library, CPU and "
            "vector path. These measurements show why a last-bit guarantee needs more than random testing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rule[0]))
            vo.wait_until("a")
            self.play(Indicate(rule[0], scale_factor=1.03))
            self.play(FadeIn(rule[1]))
            vo.wait_until("b")
            self.play(FadeIn(cap))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
                                    for b in bars], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dilemma(self):
        head = label(r"The table-maker's dilemma", font_size=36).to_edge(UP, buff=0.3)
        line = NumberLine(x_range=[0, 4, 1], length=9.0, include_ticks=True, color=GREY_C).move_to(UP * 1.1)
        fl = VGroup(*[label(t, font_size=20, color=DATA).next_to(line.n2p(k), DOWN, buff=0.2)
                      for k, t in ((1, r"float $a$"), (3, r"float $b$"))])
        mid = DashedLine(line.n2p(2) + UP * 0.5, line.n2p(2) + DOWN * 0.5, color=LIMIT)
        ml = label(r"halfway", font_size=20, color=LIMIT).next_to(mid, UP, buff=0.08)
        true = Dot(line.n2p(2.07), color=HEAD, radius=0.07)
        tl = label(r"$e^x$, \ just past halfway", font_size=20, color=HEAD).next_to(true, DOWN, buff=0.45)
        pts = VGroup(
            label(r"to round correctly you must know which side of halfway $e^x$ lies: \\ when it lies very close, \ "
                  r"you need many more bits than the answer has", font_size=22, color=GREY_A),
            label(r"how many? \ rigorous error bounds and worst-case searches; \ structured methods can prune huge ranges "
                  r"\\ some binary64 cases need over 106 bits to resolve the midpoint",
                  font_size=22, color=GREY_A),
            label(r"CORE-MATH: \ binary32 and many binary64 routines already exist; \ proofs for several binary64 functions "
                  r"\\ project report, Nov. 2026: seven binary64 functions integrated into glibc 2.43",
                  font_size=22, color=YES),
            label(r"research continues: \ complete certified coverage, \ fast implementations and wider adoption", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why is correct rounding hard? <bookmark mark='a'/> Rounding means deciding which of two neighbouring "
            "floats the true value is nearer to, which side of halfway it lies. When it lies extremely close to "
            "halfway, you have to compute many more digits than the answer itself has before you know. This is the "
            "table-maker's dilemma, as old as printed tables of logarithms. <bookmark mark='b'/> How many more? "
            "Rigorous error bounds and worst-case searches can answer that. Structured methods can exclude whole "
            "ranges rather than evaluate every input. Work by Vincent Lefèvre, Jean-Michel Muller and others "
            "found binary64 cases requiring more than twice its fifty-three bits to resolve. "
            "<bookmark mark='c'/> CORE-MATH already provides single-precision and many double-precision "
            "routines, with proofs for several binary64 functions. As of November 2026, the project reports "
            "seven binary64 functions integrated into GNU libc two point forty-three. "
            "<bookmark mark='d'/> Complete certified coverage, speed and wider adoption remain active work. "
            "This part's research problem explores a bounded search for hard single-precision inputs, and asks "
            "what extra evidence would make the search a certificate."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(fl))
            vo.wait_until("a")
            self.play(Create(mid), FadeIn(ml), FadeIn(true), FadeIn(tl), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
