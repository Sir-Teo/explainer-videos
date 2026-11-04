from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, bit_cells, load, sci

SIGN, EXP, FRAC = "#E5484D", "#4DABF7", "#69DB7C"


class Floats(VoiceoverScene):
    def construct(self):
        self.card()
        self.layout()
        self.ruler()
        self.spacing()
        self.specials()
        self.rounding()

    def card(self):
        card = chapter_card(10, r"Floating point", r"How do 32 bits cover 76 decades?", lit=(1985,), part=PART)
        with self.voiceover("Chapter ten. Floating point."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def layout(self):
        d = load("floats")
        f = d["f32"][0]
        head = label(r"IEEE 754: \ scientific notation, \ in binary", font_size=36).to_edge(UP, buff=0.35)
        form = MathTex(r"x = (-1)^{s} \times 1.f \times 2^{\,e - 127}", font_size=46, color=CODE).move_to(UP * 2.1)
        bits = f["bits"]
        cols = [SIGN] + [EXP] * 8 + [FRAC] * 23
        cells = bit_cells(bits, cell=0.36, font_size=22, colors=cols).move_to(UP * 0.7)
        braces = VGroup(Brace(cells[0], DOWN, color=SIGN), Brace(VGroup(*cells[1:9]), DOWN, color=EXP),
                        Brace(VGroup(*cells[9:]), DOWN, color=FRAC))
        bl = VGroup(MathTex(r"s = 0", font_size=26, color=SIGN).next_to(braces[0], DOWN, buff=0.1),
                    MathTex(rf"e = {f['e']}", font_size=26, color=EXP).next_to(braces[1], DOWN, buff=0.1),
                    MathTex(rf"f = {f['m']} / 2^{{23}}", font_size=26, color=FRAC).next_to(braces[2], DOWN, buff=0.1))
        val = MathTex(rf"0.1 \;\to\; 1.6000000238\ldots \times 2^{{-4}} = {f['exact']}", font_size=30,
                      color=YES).move_to(DOWN * 1.5)
        notes = VGroup(
            label(r"the leading 1 is never stored: \ 24 significant bits in 23", font_size=24, color=GREY_A),
            label(r"the exponent is biased by 127, \ so the bits sort like the numbers", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1985 the IEEE published a standard, led by William Kahan of Berkeley, that ended a decade of every "
            "company doing floating point its own way. <bookmark mark='a'/> A number is stored like scientific "
            "notation, in binary: a sign, an exponent and a fraction. The value is plus or minus one point f, times two "
            "to the power e minus a bias. <bookmark mark='b'/> In thirty-two bits: one bit of sign, eight of "
            "exponent, twenty-three of fraction. <bookmark mark='c'/> Here is zero point one. Its exponent field says "
            "two to the minus four; its fraction says one point six, nearly. The number actually stored is zero point "
            "one, zero zero zero, zero zero zero, one four nine and more: the closest float to a tenth, but not a "
            "tenth. <bookmark mark='d'/> Two tricks make the format efficient. The leading one of a normalized number "
            "is always one, so it is not stored, buying a free bit. And the exponent is stored with a bias, so that "
            "comparing two positive floats as integers gives the right answer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(form))
            vo.wait_until("b")
            self.play(FadeIn(cells), Create(braces))
            vo.wait_until("c")
            self.play(FadeIn(bl), FadeIn(val))
            vo.wait_until("d")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ruler(self):
        d = load("floats")["mini"]
        vals = d["values"]
        head = label(r"Every value of a 6-bit float", font_size=36).to_edge(UP, buff=0.35)
        fmt_ = label(r"1 sign bit, \ 3 exponent bits, \ 2 fraction bits: \ the same rules, \ shrunk", font_size=24,
                     color=GREY_A).next_to(head, DOWN, buff=0.2)
        ax = NumberLine(x_range=[0, 14, 1], length=12.6, color=GREY_C, include_numbers=True, font_size=20).move_to(
            DOWN * 0.2)
        ticks = VGroup()
        for v in vals:
            col = INF if v["kind"] == "sub" else FUNC
            ticks.add(Line(ax.n2p(v["v"]) + DOWN * 0.0, ax.n2p(v["v"]) + UP * 0.55, color=col, stroke_width=3))
        spacing = VGroup(*[label(t, font_size=22, color=HEAD).move_to(ax.n2p(x) + UP * 1.0)
                           for x, t in ((1.5, r"spacing $\tfrac14$"), (3.0, r"$\tfrac12$"), (6.0, r"$1$"),
                                        (11.0, r"$2$"))])
        brace_note = label(r"each power of two starts a new band, \ with twice the spacing", font_size=26,
                           color=GREY_A).to_edge(DOWN, buff=1.2)
        sub_note = label(r"near zero: \ \textit{subnormals}, \ evenly spaced, \ fill the gap", font_size=26,
                         color=INF).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "To see the shape of this ruler, shrink the format until every value fits on the screen. "
            "<bookmark mark='a'/> Six bits: a sign, three bits of exponent and two of fraction. Here are all of its "
            "positive finite values. <bookmark mark='b'/> Between one and two there are four of them, a quarter apart. "
            "Between two and four, four more, half apart; between four and eight, four more, one apart. Every power of "
            "two begins a new band, with the same number of marks and twice the spacing. The ruler is uniform in "
            "relative terms, logarithmic in absolute ones. <bookmark mark='c'/> Near zero, a special rule takes over. "
            "When the exponent field is all zeros, the hidden leading one becomes a zero, and the values continue "
            "evenly down to zero. These are the subnormal numbers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fmt_), Create(ax))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.04), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in spacing], lag_ratio=0.3), FadeIn(brace_note))
            vo.wait_until("c")
            self.play(*[t.animate.set_stroke(width=5) for t, v in zip(ticks, vals) if v["kind"] == "sub"],
                      FadeIn(sub_note))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spacing(self):
        d = load("floats")
        head = label(r"ulp and machine epsilon", font_size=38).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[-3, 4, 1], y_range=[0, 1.2, 0.5], x_length=7.0, y_length=3.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(LEFT * 3.0 + DOWN * 0.6)
        xl = VGroup(*[MathTex(rf"2^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                      for k in range(-3, 5)])
        # relative spacing ulp(x)/x, in units of 2^-23: a sawtooth between 1/2 and 1
        xs = np.linspace(-3, 3.999, 800)
        ys = 2.0 ** np.floor(xs) / 2.0 ** xs
        saw = VMobject(color=FUNC, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
        yl = MathTex(r"\frac{\mathrm{ulp}(x)}{x} \ \text{in units of } 2^{-23}", font_size=26, color=FUNC).next_to(
            ax, UP, buff=0.15)
        side = VGroup(
            MathTex(r"\mathrm{ulp}(1) = 2^{-23} \approx 1.19 \times 10^{-7}", font_size=30, color=GREY_A),
            MathTex(r"\varepsilon_{32} = 2^{-23}, \quad \varepsilon_{64} = 2^{-52} \approx 2.2 \times 10^{-16}",
                    font_size=30, color=GREY_A),
            MathTex(r"u = \tfrac12 \varepsilon: \ |\text{relative rounding error}| \le u", font_size=30, color=HEAD),
            MathTex(r"2^{24} + 1 = 16{,}777{,}217 \ \to\ 16{,}777{,}216", font_size=30, color=NO),
            label(r"the first integer a 32-bit float cannot hold", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(RIGHT * 1.2 + UP * 0.2, aligned_edge=LEFT)
        with self.voiceover(
            "The gap between a float and the next one up is called an ulp, a unit in the last place. "
            "<bookmark mark='a'/> In thirty-two-bit floats, the ulp of one is two to the minus twenty-three, about "
            "one ten-millionth; between two and four it is twice that, and so on. Divide the ulp by the number itself, "
            "and you get a sawtooth that never leaves a factor of two: every float, large or small, is stored with the "
            "same relative precision. <bookmark mark='b'/> Two to the minus twenty-three is the format's machine "
            "epsilon. Half of it, called u, bounds the relative error of rounding any real number to the nearest "
            "float. For sixty-four-bit doubles, epsilon is about two times ten to the minus sixteen: sixteen decimal "
            "digits. <bookmark mark='c'/> One consequence surprises people. Above two to the twenty-four, sixteen "
            "million, a thirty-two-bit float's ulp is two, and the odd integers are simply gone: sixteen million, seven "
            "hundred and seventy-seven thousand, two hundred and seventeen rounds to the even number below it."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(saw), run_time=2.0)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def specials(self):
        head = label(r"The edges of the ruler", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup()
        for e, f, what, col in (
            (r"00000000", r"0", r"$\pm 0$ \ (two zeros: \ $1/{-0} = -\infty$)", GREY_A),
            (r"00000000", r"\ne 0", r"subnormal: \ $0.f \times 2^{-126}$", INF),
            (r"00000001 \dots 11111110", r"\text{any}", r"normal: \ $1.f \times 2^{e - 127}$", FUNC),
            (r"11111111", r"0", r"$\pm\infty$: \ $1/0$, \ overflow", HEAD),
            (r"11111111", r"\ne 0", r"NaN: \ $0/0$, \ $\sqrt{-1}$, \ $\infty - \infty$", NO),
        ):
            rows.add(VGroup(MathTex(e, font_size=28, color=EXP), MathTex(f, font_size=28, color=FRAC),
                            label(what, font_size=26, color=col)))
        hdr = VGroup(label(r"exponent", font_size=22, color=GREY_B), label(r"fraction", font_size=22, color=GREY_B),
                     label(r"meaning", font_size=22, color=GREY_B))
        tab = VGroup(hdr, *rows)
        for i, r in enumerate(tab):
            r[0].move_to([-4.0, 2.0 - 0.62 * i, 0])
            r[1].move_to([-1.0, 2.0 - 0.62 * i, 0])
            r[2].move_to([0.2, 2.0 - 0.62 * i, 0], aligned_edge=LEFT)
        nan = MathTex(r"\mathrm{NaN} \ne \mathrm{NaN}", font_size=34, color=NO).move_to(LEFT * 3.4 + DOWN * 1.9)
        nl = note(r"the only value not equal to itself: \ \texttt{x != x} \ tests for NaN", font_size=22).next_to(
            nan, DOWN, buff=0.2)
        grad = MathTex(r"x - y = 0 \iff x = y", font_size=34, color=INF).move_to(RIGHT * 3.4 + DOWN * 1.9)
        gl = note(r"true only because subnormals \ underflow gradually", font_size=22).next_to(grad, DOWN, buff=0.2)
        with self.voiceover(
            "The two extreme exponent patterns are reserved. <bookmark mark='a'/> An exponent of all zeros, with a "
            "zero fraction, is zero, and since the sign bit is separate there are two zeros, plus and minus, which "
            "compare equal but remember which side they came from. With a non-zero fraction, it is a subnormal. "
            "<bookmark mark='b'/> An exponent of all ones with a zero fraction is infinity, the honest answer to one "
            "over zero or to a result too large to hold; with any other fraction it is NaN, not a number, the answer "
            "to zero over zero or the square root of minus one. NaNs flow through any later arithmetic, so an error is "
            "never silently replaced by a plausible number. <bookmark mark='c'/> A NaN is the only value that is not "
            "equal to itself, which is how programs test for one. And the subnormals buy a guarantee that sounds "
            "obvious but fails without them: x minus y is zero only when x equals y. Kahan fought for this gradual "
            "underflow against fierce opposition, because it cost hardware. The standard is a large part of why he "
            "received the Turing Award in 1989."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(FadeIn(nan), FadeIn(nl))
            self.play(FadeIn(grad), FadeIn(gl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rounding(self):
        head = label(r"The rule that makes floating point usable", font_size=36).to_edge(UP, buff=0.35)
        rule = MathTex(r"\mathrm{fl}(x \circ y) = \mathrm{round}(x \circ y), \qquad \circ \in \{+, -, \times, \div, "
                       r"\sqrt{\ }\}", font_size=40, color=CODE).move_to(UP * 1.9)
        cap = label(r"the exact answer, \ then rounded once: \ \textit{correctly rounded}", font_size=28,
                    color=YES).next_to(rule, DOWN, buff=0.3)
        ax = NumberLine(x_range=[0, 4, 1], length=8.0, color=GREY_C).move_to(DOWN * 0.7)
        marks = VGroup(*[Line(ax.n2p(k) + DOWN * 0.15, ax.n2p(k) + UP * 0.15, color=FUNC, stroke_width=4)
                         for k in range(5)])
        ml = VGroup(*[MathTex(t, font_size=24, color=FUNC).next_to(ax.n2p(k), DOWN, buff=0.25)
                      for k, t in enumerate([r"1.00", r"1.01", r"1.10", r"1.11", r"10.0"])])
        true_ = ValueTracker(1.3)
        dot = always_redraw(lambda: Dot(ax.n2p(true_.get_value()), radius=0.09, color=HEAD))
        arrow = always_redraw(lambda: Arrow(ax.n2p(true_.get_value()) + UP * 0.5,
                                            ax.n2p(round_even(true_.get_value())) + UP * 0.12, buff=0.02,
                                            stroke_width=3, color=HEAD, max_tip_length_to_length_ratio=0.25))
        ties = label(r"exactly halfway: \ round to the neighbour whose last bit is 0 \ (ties to even)", font_size=26,
                     color=GREY_A).to_edge(DOWN, buff=1.0)
        modes = note(r"also: \ toward $0$, \ toward $+\infty$, \ toward $-\infty$ \ (interval arithmetic, chapter 13)",
                     font_size=22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The heart of the standard is one sentence. <bookmark mark='a'/> The result of adding, subtracting, "
            "multiplying, dividing or taking a square root must be the exact mathematical answer, rounded once to the "
            "nearest float. The hardware may use any method it likes inside, extra bits, the SRT divider, Newton's "
            "iteration, but what comes out must be as if it had computed exactly. <bookmark mark='b'/> On a ruler with "
            "two fraction bits, the true result is rounded to the nearest mark. <bookmark mark='c'/> When it lands "
            "exactly halfway, it goes to the neighbour whose last bit is zero, so that ties do not drift upwards on "
            "average. <bookmark mark='d'/> This rule is what makes error analysis possible: every operation is exact, "
            "up to one rounding, with a relative error no bigger than u. The next chapter is about what happens when "
            "many such small errors meet."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rule), FadeIn(cap))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(marks), FadeIn(ml), FadeIn(dot), FadeIn(arrow))
            self.play(true_.animate.set_value(2.35), run_time=2.0)
            vo.wait_until("c")
            self.play(true_.animate.set_value(2.5), run_time=1.0)
            self.play(FadeIn(ties))
            self.play(true_.animate.set_value(1.5), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(modes))
        self.wait(0.3)
        self.clear_scene()


def round_even(x: float) -> float:
    k = np.floor(x)
    fpart = x - k
    if abs(fpart - 0.5) < 1e-9:
        return k if int(k) % 2 == 0 else k + 1
    return float(np.round(x))
