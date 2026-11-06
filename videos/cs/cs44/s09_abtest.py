from __future__ import annotations

import math
import random

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, tag_box

Z_A, Z_B = 1.959964, 0.841621          # standard normal quantiles at 0.975 and 0.8, as in the instrument


def _phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def _pdf(x, mu=0.0):
    return math.exp(-0.5 * (x - mu) ** 2) / math.sqrt(2 * math.pi)


def _two_hump(shift, x_length=7.6, y_length=2.6, font=17):
    """Sampling distributions of the estimated difference, in units of its standard error: under no difference
    (centred at 0) and under a true difference ``shift``; the critical value; alpha and beta shaded."""
    ax = Axes(x_range=[-3.5, 6.5, 1], y_range=[0, 0.45, 0.1], x_length=x_length, y_length=y_length,
              axis_config={"color": GREY_D, "include_ticks": False}, y_axis_config={"stroke_opacity": 0})
    h0 = ax.plot(lambda x: _pdf(x), x_range=[-3.5, 6.5], color=DATA, stroke_width=3)
    h1 = ax.plot(lambda x: _pdf(x, shift), x_range=[-3.5, 6.5], color=LAM, stroke_width=3)
    alpha = VGroup(ax.get_area(h0, x_range=(Z_A, 6.5), color=NO, opacity=0.6),
                   ax.get_area(h0, x_range=(-3.5, -Z_A), color=NO, opacity=0.6))
    beta = ax.get_area(h1, x_range=(-3.5, Z_A), color=KERN, opacity=0.45)
    crit = DashedLine(ax.c2p(Z_A, 0), ax.c2p(Z_A, 0.44), color=HEAD, stroke_width=2)
    ticks = VGroup(*[label(t, font_size=font, color=c).next_to(ax.c2p(x, 0), DOWN, buff=0.12) for x, t, c in (
        (0, r"$0$", DATA), (Z_A, r"$1.96$", HEAD))])
    ticks.add(label(rf"$\delta = {shift:.2f}$", font_size=font, color=LAM).next_to(ax.c2p(shift, _pdf(0)), UP,
                                                                                  buff=0.1))
    g = VGroup(ax, beta, alpha, h0, h1, crit, ticks)
    g.ax, g.h0, g.h1, g.alpha, g.beta, g.crit, g.ticks = ax, h0, h1, alpha, beta, crit, ticks
    return g


class Abtest(VoiceoverScene):
    def construct(self):
        self.card()
        self.rct()
        self.ztest()
        self.errors()
        self.size()
        self.power()

    def card(self):
        card = chapter_card(8, r"The A/B test", r"Did the change cause the difference?", lit=(1935, 2009),
                            extra=((1935, r"Fisher: \ \textit{The Design of Experiments}"),
                                   (2009, r"Kohavi et al.: \ experiments on the web")), part=PART)
        with self.voiceover("Chapter eight. The A/B test."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rct(self):
        head = label(r"A randomized controlled trial", font_size=36).to_edge(UP, buff=0.3)
        rng = random.Random(9)
        n = 40
        loyal = [rng.random() < 0.35 for _ in range(n)]
        arm = [rng.random() < 0.5 for _ in range(n)]
        queue = VGroup(*[Dot(radius=0.09, color=KERN if loyal[k] else GREY_B) for k in range(n)]).arrange_in_grid(
            rows=5, cols=8, buff=0.14).move_to([-5.0, 0.6, 0])
        coin = tag_box(r"coin", color=HEAD, size=20, w=1.2, h=0.6).move_to([-2.4, 0.6, 0])
        boxes = VGroup(
            RoundedRectangle(width=3.2, height=1.6, corner_radius=0.1, stroke_color=DATA).move_to([1.0, 1.6, 0]),
            RoundedRectangle(width=3.2, height=1.6, corner_radius=0.1, stroke_color=YES).move_to([1.0, -0.4, 0]))
        names = VGroup(label(r"A: \ the current page", font_size=19, color=DATA).next_to(boxes[0], UP, buff=0.08),
                       label(r"B: \ the new page", font_size=19, color=YES).next_to(boxes[1], DOWN, buff=0.08))
        slots = {True: [], False: []}
        for k in range(n):
            slots[arm[k]].append(k)
        targets = {}
        for side, box in ((False, boxes[0]), (True, boxes[1])):
            for i, k in enumerate(slots[side]):
                targets[k] = box.get_corner(UL) + np.array([0.25 + (i % 10) * 0.28, -0.3 - (i // 10) * 0.32, 0])
        counts = VGroup(*[label(rf"{sum(loyal[k] for k in slots[s])} of {len(slots[s])} returning", font_size=18,
                                color=KERN).next_to(box, RIGHT, buff=0.25)
                          for s, box in ((False, boxes[0]), (True, boxes[1]))])
        key = wrapped_label(r"orange: \ returning customers, \ a trait nobody measured", 3.4, font_size=17,
                            color=KERN).next_to(queue, DOWN, buff=0.3)
        ill = note(r"illustrative", font_size=16).next_to(key, DOWN, buff=0.1).align_to(key, LEFT)
        lines = VGroup(
            wrapped_label(r"a coin, \ not a person, \ decides who sees B: \ so the two groups differ only by chance, "
                          r"\ in every trait, \ measured or not", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"large random groups have nearly equal averages \ (Part 20's concentration), \ so a "
                          r"difference in outcomes is caused by the change, \ or by chance; \ the test measures "
                          r"chance", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where intuition runs out, run an experiment. <bookmark mark='a'/> Each arriving user is assigned by a "
            "coin: heads, the current page; tails, the new one. <bookmark mark='b'/> Because a coin decides and not "
            "a person, the two groups differ only by chance, in every trait, even ones nobody measured, such as how "
            "many are returning customers. <bookmark mark='c'/> With large groups, Part 20's concentration makes "
            "their averages nearly equal. So if the groups then behave differently, the cause is the change, or "
            "chance. This is Ronald Fisher's randomized experiment, and a statistical test measures the chance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(queue), FadeIn(key), FadeIn(ill), FadeIn(coin), Create(boxes),
                      FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[queue[k].animate.move_to(targets[k]) for k in range(n)], lag_ratio=0.08),
                      Indicate(coin, color=HEAD), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(counts), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def ztest(self):
        head = label(r"The two-proportion z-test", font_size=36).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"\hat p_A = \frac{x_A}{n_A},\quad \hat p_B = \frac{x_B}{n_B},\quad \hat d = \hat p_B - \hat p_A",
                    font_size=30),
            MathTex(r"\text{if no difference: } \hat p = \frac{x_A + x_B}{n_A + n_B}", font_size=30),
            MathTex(r"\mathrm{SE} = \sqrt{\hat p(1 - \hat p)\left(\frac{1}{n_A} + \frac{1}{n_B}\right)}",
                    font_size=30),
            MathTex(r"z = \frac{\hat d}{\mathrm{SE}},\qquad p = 2\,\bigl(1 - \Phi(|z|)\bigr)", font_size=32,
                    color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-2.9, 0.55, 0])
        whys = VGroup(
            note(r"conversion rates in each arm", font_size=17),
            note(r"pool both arms: \ one rate $p$ under the null", font_size=17),
            note(r"variance of a rate is $p(1-p)/n$; \ variances of independent arms add", font_size=17),
            note(r"for large $n$, \ $z$ is close to standard normal \ (central limit theorem)", font_size=17),
        )
        for w, e in zip(whys, eqs):
            w.next_to(e, DOWN, buff=0.06).align_to(e, LEFT)
        nA = nB = 10_000
        xA, xB = 500, 560
        pp = (xA + xB) / (nA + nB)
        se = math.sqrt(pp * (1 - pp) * (1 / nA + 1 / nB))
        z = (xB / nB - xA / nA) / se
        pv = 2 * (1 - _phi(abs(z)))
        ex = VGroup(
            label(r"an example", font_size=20, color=HEAD),
            label(rf"A: \ {xA} of {nA:,} \ ({100 * xA / nA:.1f}\%)", font_size=19, color=DATA),
            label(rf"B: \ {xB} of {nB:,} \ ({100 * xB / nB:.1f}\%)", font_size=19, color=YES),
            label(rf"pooled {100 * pp:.2f}\%, \ SE {100 * se:.3f} points", font_size=19, color=WHITE),
            label(rf"$z = {z:.2f}$, \ $p = {pv:.3f}$", font_size=21, color=NO),
            wrapped_label(rf"a {100 * (xB / xA - 1):.0f}\% lift, \ and still not significant at 0.05", 3.8,
                          font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        box = SurroundingRectangle(ex, color=GREY_D, buff=0.25, corner_radius=0.1)
        VGroup(box, ex).move_to([4.6, 0.4, 0])
        ill = note(r"illustrative numbers", font_size=16).next_to(box, DOWN, buff=0.12)
        with self.voiceover(
            "Here is the standard test. <bookmark mark='a'/> Each arm converts a share of its users, and the "
            "observed difference is B's rate minus A's. <bookmark mark='b'/> Suppose the change did nothing: then "
            "both arms share one rate, estimated by pooling them. <bookmark mark='c'/> A rate's variance is p times "
            "one minus p over n, and the two arms' variances add. <bookmark mark='d'/> Divide the difference by the "
            "resulting standard error. For large samples z is nearly standard normal, and the p-value is the chance "
            "of a z this far from zero if nothing changed. <bookmark mark='e'/> Five hundred conversions against "
            "five hundred and sixty, out of ten thousand each, is a twelve per cent "
            f"lift, yet z is only {z:.2f} and the p-value {pv:.3f}: not significant at five per cent."
        ) as vo:
            self.play(FadeIn(head))
            for mk, e, w in zip("abcd", eqs, whys):
                vo.wait_until(mk)
                self.play(Write(e), FadeIn(w))
            vo.wait_until("e")
            self.play(Create(box), FadeIn(ex[0]), FadeIn(ill))
            self.play(LaggedStart(*[FadeIn(t) for t in ex[1:]], lag_ratio=0.4), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def errors(self):
        head = label(r"Two hypotheses, \ two errors", font_size=36).to_edge(UP, buff=0.3)
        shift = Z_A + Z_B
        g = _two_hump(shift).move_to([-2.0, 0.6, 0])
        xl = label(r"estimated difference, \ in standard errors", font_size=17, color=GREY_A).next_to(
            g.ax, DOWN, buff=0.55)
        h0l = label(r"no difference", font_size=19, color=DATA).next_to(g.ax.c2p(-1.1, 0.33), LEFT, buff=0.1)
        h1l = label(r"true difference $\delta$", font_size=19, color=LAM).next_to(g.ax.c2p(shift + 0.9, 0.33),
                                                                                 RIGHT, buff=0.05)
        al = label(r"$\alpha/2 = 2.5\%$", font_size=19, color=NO).next_to(g.ax.c2p(2.6, 0.06), UR, buff=0.05)
        bl = label(rf"$\beta = {100 * _phi(Z_A - shift):.0f}\%$", font_size=19, color=KERN).next_to(
            g.ax.c2p(0.9, 0.05), UP, buff=0.02)
        rej = label(r"reject the null $\to$", font_size=18, color=HEAD).next_to(g.ticks[1], RIGHT, buff=0.35)
        notes = VGroup(
            wrapped_label(r"\textbf{false positive}: \ no real change, \ but the estimate lands beyond $\pm 1.96$: "
                          r"\ probability $\alpha = 5\%$", 4.4, font_size=19, color=NO),
            wrapped_label(r"\textbf{false negative}: \ a real change, \ but the estimate falls short of 1.96: \ "
                          r"probability $\beta$; \ \textbf{power} $= 1 - \beta$", 4.4, font_size=19, color=KERN),
            wrapped_label(r"for power 80\%, \ $\delta$ must sit $0.84$ standard errors beyond the line: \ "
                          r"$\delta = (1.96 + 0.84)\,\mathrm{SE}$", 4.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.6, 0.3, 0])
        with self.voiceover(
            "A test can be wrong in two ways. <bookmark mark='a'/> If the change did nothing, the estimated "
            "difference scatters around zero, with a spread of one standard error. We declare a winner beyond one "
            "point nine six of them, so we are fooled five per cent of the time: that is alpha. "
            "<bookmark mark='b'/> If the change really helps by delta, the estimate scatters around delta instead, "
            "and whenever it falls short of the line we miss a real effect: that is beta, and one minus beta is the "
            "power. <bookmark mark='c'/> For eighty per cent power, delta must sit nought point eight four standard "
            "errors beyond the line."
        ) as vo:
            self.play(FadeIn(head), Create(g.ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(g.h0), FadeIn(h0l), FadeIn(g.ticks[0]))
            self.play(Create(g.crit), FadeIn(g.ticks[1]), FadeIn(rej))
            self.play(FadeIn(g.alpha), FadeIn(al), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(g.h1), FadeIn(h1l), FadeIn(g.ticks[2]))
            self.play(FadeIn(g.beta), FadeIn(bl), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def size(self):
        s = load("size")
        rows_ = s["rows"]
        p = rows_[0]["p"]
        head = label(r"How many users?", font_size=36).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"\delta = (z_{1-\alpha/2} + z_{\text{power}})\,\mathrm{SE},\qquad "
                    r"\mathrm{SE} = \sigma\sqrt{2/n},\quad \sigma^2 = p(1-p)", font_size=30),
            MathTex(r"n = \frac{(z_{1-\alpha/2} + z_{\text{power}})^2 \cdot 2\sigma^2}{\delta^2}", font_size=32),
            MathTex(r"(1.96 + 0.84)^2 \cdot 2 = 15.7 \;\Rightarrow\; n \approx \frac{16\,\sigma^2}{\delta^2}",
                    font_size=32, color=YES),
        ).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.35)
        why = note(r"per arm, \ two arms of $n$ users; \ $\alpha = 0.05$, \ power 0.8", font_size=17).next_to(
            eqs[0], DOWN, buff=0.06)
        eqs[1:].shift(DOWN * 0.2)
        rows = [[rf"{100 * r['lift']:.0f}\%", rf"{100 * r['delta']:.2f}", f"{r['n_per_arm']:,.0f}",
                 f"{r['rule_16']:,.0f}"] for r in rows_]
        tab = grid_table([r"relative lift", r"$\delta$ \ (points)", r"$n$ per arm", r"$16\sigma^2/\delta^2$"], rows,
                         widths=[2.2, 2.0, 2.6, 2.6], row_h=0.4, font_size=19, mono_cols=())
        tab.next_to(eqs, DOWN, buff=0.35).set_x(-1.6)
        k5 = next(i for i, r in enumerate(rows_) if abs(r["lift"] - 0.05) < 1e-9) + 1
        for c in tab.cells[k5]:
            c.set_color(HEAD)
        side = wrapped_label(rf"base rate {100 * p:.0f}\%; \ halve the lift and you need four times the users",
                             3.2, font_size=19, color=NO).next_to(tab, RIGHT, buff=0.45)
        r5 = rows_[k5 - 1]
        with self.voiceover(
            "That picture is a recipe for the sample size. <bookmark mark='a'/> Delta must be one point nine six "
            "plus nought point eight four standard errors, and the standard error is sigma times the root of two "
            "over n. <bookmark mark='b'/> Solve for n. <bookmark mark='c'/> The constant comes to fifteen point "
            "seven, so n is about sixteen sigma squared over delta squared: every experimenter's rule of thumb. "
            "<bookmark mark='d'/> On a five per cent conversion rate, a five per cent relative lift needs about "
            f"{r5['n_per_arm'] / 1000:.0f} thousand users in each arm; the rule says "
            f"{r5['rule_16'] / 1000:.1f} thousand. Halve the lift and you need four times as many: a one per cent "
            f"lift needs about {rows_[0]['n_per_arm'] / 1e6:.0f} million per arm."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(why))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(1, len(rows) + 1)],
                                  lag_ratio=0.3), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def power(self):
        pw = load("power")
        full, half = pw["at_n"], pw["half_n"]
        head = label(r"Checking by simulation", font_size=36).to_edge(UP, buff=0.3)
        shift = Z_A + Z_B
        g = _two_hump(shift, x_length=6.6, y_length=2.4).move_to([-3.0, 0.9, 0])
        theory_half = _phi(shift / math.sqrt(2) - Z_A)
        g2 = _two_hump(shift / math.sqrt(2), x_length=6.6, y_length=2.4)
        g2.shift(g.ax.get_center() - g2.ax.get_center())
        cap = label(r"at the computed $n$", font_size=19, color=YES).next_to(g, DOWN, buff=0.25)
        cap2 = label(r"at half the $n$: \ SE grows by $\sqrt{2}$", font_size=19, color=NO).move_to(cap)
        vals = [(r, c, rf"$n = {r['n']:,}$".replace(",", "{,}")) for r, c in ((full, YES), (half, NO))]
        bars = VGroup()
        for k, (r, c, t) in enumerate(vals):
            b = Rectangle(width=1.0, height=3.2 * r["power"], stroke_width=0, fill_color=c, fill_opacity=0.8)
            b.move_to([k * 1.9, 1.6 * r["power"], 0])
            v = label(f"{r['power']:.2f}", font_size=21, color=BLACK).move_to(b.get_top() + DOWN * 0.25)
            nm = label(t, font_size=17, color=GREY_A).next_to([k * 1.9, 0, 0], DOWN, buff=0.12)
            bars.add(VGroup(b, v, nm))
        base = Line([-0.7, 0, 0], [2.6, 0, 0], color=GREY_C)
        target = DashedLine([-0.7, 3.2 * 0.8, 0], [2.6, 3.2 * 0.8, 0], color=HEAD, stroke_width=2)
        tl = label(r"target 0.8", font_size=17, color=HEAD).next_to(target, RIGHT, buff=0.1)
        chart = VGroup(base, target, tl, bars).move_to([4.3, 0.6, 0])
        ct = label(r"simulated power, \ 2{,}000 experiments each", font_size=18, color=GREY_A).next_to(chart, UP,
                                                                                                   buff=0.2)
        lines = VGroup(
            wrapped_label(rf"in theory, \ at half the $n$: \ $\Phi(2.80/\sqrt{{2}} - 1.96) = {theory_half:.2f}$; \ "
                          r"a coin flip for a real effect", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"an underpowered test that does reach significance overstates the effect: \ only the "
                          r"lucky overestimates cross the line \ (Gelman and Carlin, \ 2014)", 12.4, font_size=20,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Formulas built on approximations deserve a check. <bookmark mark='a'/> We simulated two thousand "
            f"experiments with a true five per cent lift and {full['n']:,} users per arm. "
            f"<bookmark mark='b'/> The test found the lift in {100 * full['power']:.1f} per cent of them, the eighty "
            "per cent we designed for, to within the simulation's noise. <bookmark mark='c'/> With half the users, "
            "the standard error grows by the square root of two, and delta now sits barely past the line. Power falls "
            f"to {100 * half['power']:.0f} per cent: a real improvement missed half the time. "
            "<bookmark mark='d'/> Worse, when such a test does come out significant, it overstates the effect, "
            "because only the lucky overestimates cross the line."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(base), FadeIn(target), FadeIn(tl), FadeIn(ct))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]))
            vo.wait_until("c")
            self.play(ReplacementTransform(g, g2), ReplacementTransform(cap, cap2))
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, YES)
