from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, axis_plot, load, sci


class Error(WatchScene):
    def construct(self):
        self.card()
        self.model()
        self.cancel()
        self.summation()
        self.patriot()

    def card(self):
        self.chapter(11, r"Rounding error", r"How do tiny errors become big ones?", lit=(1991, 1996), part=PART, said="Chapter eleven. Rounding error.")

    # ------------------------------------------------------------------
    def model(self):
        head = label(r"The standard model of floating point", font_size=36).to_edge(UP, buff=0.35)
        m = MathTex(r"\mathrm{fl}(x \circ y) = (x \circ y)(1 + \delta), \qquad |\delta| \le u", font_size=44,
                    color=CODE).move_to(UP * 1.6)
        us = MathTex(r"u = 2^{-24} \approx 6 \times 10^{-8} \ (\text{float32}), \qquad u = 2^{-53} \approx 1.1 \times "
                     r"10^{-16} \ (\text{float64})", font_size=30, color=GREY_A).next_to(m, DOWN, buff=0.4)
        bad = VGroup(
            label(r"no overflow or underflow: \ each operation is nearly exact", font_size=28, color=YES),
            label(r"the danger is in what the errors do next:", font_size=28, color=GREY_A),
            label(r"subtracting nearly equal numbers \ amplifies them", font_size=28, color=NO),
            label(r"adding many numbers \ accumulates them", font_size=28, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 1.4)
        with self.voiceover(
            "Away from overflow and underflow, the rounding rule gives a simple relative-error model. <bookmark mark='a'/> The computed result is "
            "the exact result times one plus delta, where delta is at most u in size: about six parts in a hundred "
            "million for single precision, about one in ten million billion for double. <bookmark mark='b'/> So every "
            "single operation is very accurate, relative to its own answer. Trouble only comes from what later "
            "operations do with those errors, and it comes in two main forms. Subtracting two nearly equal numbers "
            "turns small relative errors into huge ones. And adding up very many numbers lets errors pile up. "
            "James Wilkinson built the whole of numerical analysis on this model in the 1960s."
        ) as vo:
            self.play(FadeIn(head), FadeIn(m))
            vo.wait_until("a")
            self.play(Indicate(m, scale_factor=1.02), FadeIn(us))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bad], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cancel(self):
        self.ask(r"$(1 - \cos x) / x^2$ at $x = 10^{-8}$, \\ in double precision. \\ The true answer is $\tfrac12$. "
                 r"The computer says...", [r"$0.5$", r"$0$", r"a huge number"], 1,
                 say="One minus cos x, over x squared, at x equal to ten to the minus eight. The true answer is about one half. "
                     "What does double precision say?",
                 reveal="Zero. Cos x rounds to exactly one, and every digit cancels.")
        d = load("error")["cancel"]
        head = label(r"Catastrophic cancellation", font_size=38).to_edge(UP, buff=0.3)
        f1 = MathTex(r"f(x) = \frac{1 - \cos x}{x^2} \ \xrightarrow{\ x \to 0\ } \ \frac12", font_size=36,
                     color=CODE).move_to(LEFT * 3.4 + UP * 2.2)
        f2 = MathTex(r"= \frac{2 \sin^2(x/2)}{x^2}", font_size=36, color=YES).next_to(f1, RIGHT, buff=0.3)
        ax = Axes(x_range=[0, 7, 1], y_range=[0, 0.7, 0.1], x_length=6.4, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18},
                  y_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 1}}).move_to(
            LEFT * 3.2 + DOWN * 0.8)
        xl = VGroup(*[MathTex(rf"10^{{{k - 8}}}", font_size=20, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                      for k in range(0, 8)])
        xs = [np.log10(r["x"]) + 8 for r in d]
        naive = axis_plot(xs, [r["naive"] for r in d], ax, NO, 3)
        stable = axis_plot(xs, [r["stable"] for r in d], ax, YES, 3)
        nl = label(r"as written", font_size=24, color=NO).next_to(ax.c2p(1.2, 0.1), RIGHT, buff=0.1)
        sl = label(r"rewritten", font_size=24, color=YES).next_to(ax.c2p(5.5, 0.5), UP, buff=0.1)
        why = VGroup(
            MathTex(r"\cos x \approx 1 - \tfrac{x^2}{2}", font_size=30, color=GREY_A),
            label(r"$1 - \cos x$: \ two numbers agreeing in their first digits; \\ the difference keeps only their "
                  r"\textit{errors}", font_size=24, color=GREY_A),
            MathTex(r"\text{relative error} \approx \frac{u}{x^2/2}", font_size=30, color=NO),
            label(r"at $x = 10^{-8}$: \ $\cos x$ rounds to exactly 1, \ and $f = 0$", font_size=24, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 0.9 + DOWN * 0.6, aligned_edge=LEFT)
        with self.voiceover(
            "Here is cancellation, in a function that should be harmless. <bookmark mark='a'/> One minus cos x, over x "
            "squared, tends to one half as x goes to zero. <bookmark mark='b'/> Compute it as written, in double "
            "precision, for smaller and smaller x. Down to a ten-thousandth it is fine. Then it wobbles, and at ten to "
            "the minus eight it collapses to zero. <bookmark mark='c'/> The reason: cos x is very close to one, so one "
            "minus cos x subtracts two numbers whose leading digits agree. Those digits cancel, and what is left is "
            "mostly the rounding error in cos x, now magnified by one over x squared. At ten to the minus eight, cos x "
            "rounds to exactly one. <bookmark mark='d'/> The cure is algebra, not more bits: rewrite one minus cos x "
            "as two sine squared of x over two, which subtracts nothing, and the answer stays accurate for small nonzero x."
        ) as vo:
            self.play(FadeIn(head), Write(f1))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl))
            self.play(Create(naive), FadeIn(nl), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(w) for w in why], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(f2), Create(stable), FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def summation(self):
        d = load("error")
        sums = d["sums"]
        head = label(r"Adding a million numbers", font_size=38).to_edge(UP, buff=0.3)
        code = code_block([
            "s = c = 0.0",
            "for x in xs:",
            "    y = x - c        # correct",
            "    t = s + y        # low bits lost",
            "    c = (t - s) - y  # ...recovered",
            "    s = t",
        ], font_size=20).move_to(RIGHT * 3.7 + UP * 1.2)
        kl = label(r"Kahan's compensated summation \ (1965)", font_size=24, color=YES).next_to(code, UP, buff=0.15)
        ax = Axes(x_range=[2, 6, 1], y_range=[0, 5, 1], x_length=5.8, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(LEFT * 3.4 + DOWN * 0.6)
        xl = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                      for k in range(2, 7)])
        yl = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(2, k + 9), LEFT, buff=0.15)
                      for k in range(-9, -3)])
        t = note(r"relative error of a float32 sum of $n$ random numbers in $[0, 1)$", font_size=20).next_to(ax, UP, buff=0.1)
        xs = [np.log10(r["n"]) for r in sums]
        cn = axis_plot(xs, [np.log10(max(r["err_naive"], 1e-9)) + 9 for r in sums], ax, NO)
        ck = axis_plot(xs, [np.log10(max(r["err_kahan"], 1e-9)) + 9 for r in sums], ax, YES)
        cp = axis_plot(xs, [np.log10(max(r["err_pair"], 1e-9)) + 9 for r in sums], ax, INF)
        keys = VGroup(label(r"one at a time", font_size=22, color=NO), label(r"pairwise", font_size=22, color=INF),
                      label(r"Kahan", font_size=22, color=YES)).arrange(RIGHT, buff=0.4).next_to(ax, DOWN, buff=0.6)
        bounds = VGroup(
            MathTex(r"\text{naive: } |E| \lesssim (n - 1)\, u \sum |x_i|", font_size=28, color=NO),
            MathTex(r"\text{pairwise: } |E| \lesssim \log_2 n \; u \sum |x_i|", font_size=28, color=INF),
            MathTex(r"\text{Kahan: } |E| \lesssim 2u \sum |x_i| + O(n u^2)", font_size=28, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.4 + DOWN * 1.6)
        with self.voiceover(
            "The second danger is accumulation. <bookmark mark='a'/> Add up a million random numbers in single "
            "precision, one at a time. Once the running sum is large, each new small number loses its low bits when "
            "it is added, and the losses pile up: the relative error grows with n, and by a million terms it is "
            "around ten to the minus five, a hundred times u. <bookmark mark='b'/> Adding in pairs, then pairs of "
            "pairs, a tree like chapter four's, keeps the error growing only like log n; numpy does this by default. "
            "<bookmark mark='c'/> William Kahan's compensated summation, from 1965, does better with four lines. It "
            "keeps a second variable, c, approximating the low bits that the last addition threw away, and feeds "
            "them back into the next one. Its error bound does not grow with n at all, to first order, and the curve "
            "is flat. Python's math dot fsum tracks partial sums for very high accuracy; some platforms can still double-round the last bit."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(t))
            vo.wait_until("a")
            self.play(Create(cn), FadeIn(keys[0]), FadeIn(bounds[0]))
            vo.wait_until("b")
            self.play(Create(cp), FadeIn(keys[1]), FadeIn(bounds[1]))
            vo.wait_until("c")
            self.play(FadeIn(kl), FadeIn(code), Create(ck), FadeIn(keys[2]), FadeIn(bounds[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def patriot(self):
        p = load("error")["patriot"]
        head = label(r"Dhahran, \ 25 February 1991", font_size=38).to_edge(UP, buff=0.35)
        steps = VGroup(
            label(r"the clock counted tenths of a second, \ as an integer", font_size=26, color=GREY_A),
            label(r"times in seconds: \ the count $\times$ 0.1, \ held in a 24-bit fixed-point register", font_size=26,
                  color=GREY_A),
            MathTex(r"0.1 = 0.00011001100110011001100\,1100\ldots_2 \ \to \ 0.00011001100110011001100_2", font_size=30,
                    color=CODE),
            MathTex(rf"\text{{error per tick}} = {sci(p['per_tick'])}\ \text{{s}}", font_size=32, color=NO),
            MathTex(rf"\times\, {p['hours']}\text{{ hours}} \times 36{{,}}000 \text{{ ticks/hour}} = {p['drift']:.2f}\ "
                    r"\text{s}", font_size=32, color=NO),
            label(rf"a Scud travels {p['scud']:,} m/s: \ the radar's tracking window was off by more than half a "
                  r"kilometre", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.28).move_to(DOWN * 0.1)
        foot = note(r"the system missed the missile; \ 28 soldiers died. \ Corrected software reached Dhahran the next "
                    r"day \ (GAO report IMTEC-92-26)", font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In the Gulf War, a Patriot missile battery in Dhahran had been running for about a hundred hours. "
            "<bookmark mark='a'/> Its clock counted tenths of a second as an integer, and to get time in seconds the "
            "software multiplied by one tenth, kept in a twenty-four-bit fixed-point register. "
            "<bookmark mark='b'/> One tenth has no finite binary expansion, so the register held it chopped: too small "
            "by about ten to the minus seven seconds per tick. <bookmark mark='c'/> After a hundred hours, three point "
            "six million ticks, the clock was a third of a second slow. A Scud missile covers more than half a "
            "kilometre in a third of a second, and the radar looked in the wrong place. <bookmark mark='d'/> On the "
            "twenty-fifth of February 1991 the battery failed to intercept a Scud, and twenty-eight soldiers were "
            "killed. The corrected software, already on its way, arrived the next day."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(steps[0], steps[1])))
            vo.wait_until("a")
            self.play(Indicate(VGroup(steps[0], steps[1]), scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(steps[2]), FadeIn(steps[3]))
            vo.wait_until("c")
            self.play(FadeIn(steps[4]), FadeIn(steps[5]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

