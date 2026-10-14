from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis2.common import load, plain_axes, polyline


class LimSup(VoiceoverScene):
    def construct(self):
        self.card()
        self.tails()
        self.characterize()
        self.all_rationals()
        self.special()
        self.hump()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Upper and lower limits", r"What is left of ``the limit'' when there isn't one?",
                            lit=(1821,), part=2)
        with self.voiceover(
            "Chapter three. Most sequences don't converge, but even a divergent sequence has a largest and a smallest "
            "place where it keeps coming back. Cauchy already needed this, in 1821, for the root test."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def _axes(self, n_max=40):
        ax = plain_axes([0, n_max + 1, 5], [-2.2, 2.2, 1], 11.0, 4.2, numbers=True, font_size=20).move_to([-0.4, -1.3, 0])
        return ax

    def tails(self):
        d = load("limsup")
        a, sup_t, inf_t = d["a"], d["sup_tail"], d["inf_tail"]
        n_max = 40
        ax = self._axes(n_max)
        dots = VGroup(*[Dot(ax.c2p(k, a[k - 1]), radius=0.05, color=C.SEQ) for k in range(1, n_max + 1)])
        ex = MathTex(r"s_n = (-1)^n\big(1 + \tfrac1n\big)", font_size=34, color=C.SEQ).move_to([-4.3, 1.45, 0])
        dfn = VGroup(label(r"$E$ = the set of subsequential limits (in $[-\infty, +\infty]$)", font_size=28),
                     MathTex(r"\limsup_{n\to\infty} s_n = \sup E, \qquad \liminf_{n\to\infty} s_n = \inf E",
                             font_size=36)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        ref = note(r"Rudin 3.16").next_to(dfn, RIGHT, buff=0.3).align_to(dfn, DOWN)
        e_here = MathTex(r"E = \{-1, 1\}", font_size=34).next_to(ex, RIGHT, buff=0.6)
        dots.set_z_index(1)  # the dots stay above the water marks drawn later
        with self.voiceover(
            "Take the sequence that alternates near one and minus one, approaching each from outside. "
            "<bookmark mark='d'/> Collect every subsequential limit into a set E, allowing plus and minus infinity. "
            "The upper limit, lim sup, is the largest element of E; the lower limit, lim inf, is the smallest. "
            "<bookmark mark='e'/> Here E is just minus one and one."
        ) as vo:
            self.play(Create(ax), FadeIn(ex), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.03))
            vo.wait_until("d")
            self.play(FadeIn(dfn), FadeIn(ref))
            vo.wait_until("e")
            self.play(FadeIn(e_here))

        hi = VGroup(*[Line(ax.c2p(N - 0.5, sup_t[N - 1]), ax.c2p(N + 0.5, sup_t[N - 1]), color=C.UPPER_SUM,
                           stroke_width=4) for N in range(1, n_max + 1)])
        lo = VGroup(*[Line(ax.c2p(N - 0.5, inf_t[N - 1]), ax.c2p(N + 0.5, inf_t[N - 1]), color=C.LOWER_SUM,
                           stroke_width=4) for N in range(1, n_max + 1)])
        hi_l = MathTex(r"\sup_{n \ge N} s_n", font_size=30, color=C.UPPER_SUM).next_to(ax.c2p(n_max, 1.15), UP, buff=0.12)
        lo_l = MathTex(r"\inf_{n \ge N} s_n", font_size=30, color=C.LOWER_SUM).next_to(ax.c2p(n_max, -1.15), DOWN,
                                                                                       buff=0.12)
        hi_l.shift(LEFT * 0.4)
        lo_l.shift(LEFT * 0.4)
        eq = MathTex(r"\limsup s_n = \lim_{N \to \infty} \, \sup_{n \ge N} s_n", font_size=34).move_to([3.4, 1.45, 0])
        eq_n = note(r"(the same number: the high-water mark of the tail)").next_to(eq, DOWN, buff=0.1)
        with self.voiceover(
            "There's a more hands-on way to see it. <bookmark mark='h'/> For each N, mark the highest value in the tail "
            "from N on: the high-water mark. Dropping terms can only lower it, so it decreases, and here it comes down "
            "to one. <bookmark mark='l'/> The low-water mark rises, to minus one. <bookmark mark='q'/> The limit of the "
            "high-water mark is exactly the upper limit, and the limit of the low-water mark is the lower limit."
        ) as vo:
            vo.wait_until("h")
            self.play(LaggedStart(*[Create(x) for x in hi], lag_ratio=0.08), FadeIn(hi_l), run_time=2.4)
            vo.wait_until("l")
            self.play(LaggedStart(*[Create(x) for x in lo], lag_ratio=0.08), FadeIn(lo_l), run_time=2.0)
            vo.wait_until("q")
            self.play(FadeIn(eq), FadeIn(eq_n))
        assert np.all(np.diff(sup_t) <= 1e-15) and np.all(np.diff(inf_t) >= -1e-15)
        self.wait(0.3)
        self.ax, self.dots, self.keep = ax, dots, VGroup(ax, dots, ex, hi, lo, hi_l, lo_l)
        self.play(FadeOut(VGroup(dfn, ref, e_here, eq, eq_n)))

    # ------------------------------------------------------------------
    def characterize(self):
        n_max = 40
        a = load("limsup")["a"][:n_max]
        ax, dots = self.ax, self.dots
        xv = ValueTracker(1.2)

        def level():
            x = xv.get_value()
            return DashedLine(ax.c2p(0, x), ax.c2p(n_max + 1, x), color=C.PATHOLOGY, stroke_width=2.5)

        lev = always_redraw(level)
        x_l = always_redraw(lambda: MathTex(r"x", font_size=32, color=C.PATHOLOGY).next_to(
            ax.c2p(n_max + 1, xv.get_value()), RIGHT, buff=0.12))

        def recolor():
            x = xv.get_value()
            for k, dot in enumerate(dots, start=1):
                dot.set_color(C.PATHOLOGY if a[k - 1] > x else C.SEQ)

        self.remove(*dots)
        self.add(dots)  # the group itself must be in the scene for its updater to run
        dots.add_updater(lambda m: recolor())
        thm = VGroup(label(r"\textbf{Rudin 3.17} \ $s^* = \limsup s_n$ is the only number with:", font_size=28),
                     label(r"(a) \ some subsequence converges to $s^*$;", font_size=26, color=GREY_A),
                     label(r"(b) \ for every $x > s^*$, only finitely many $s_n$ exceed $x$.", font_size=26,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(UP, buff=0.3)

        def count(x):
            return int((a > x).sum())

        cnt = Integer(count(1.2), font_size=30, color=C.PATHOLOGY)
        cnt_l = VGroup(label(r"terms above $x$:", font_size=26, color=C.PATHOLOGY), cnt).arrange(RIGHT, buff=0.15)
        cnt_l.move_to([3.6, 0.95, 0])
        cnt.add_updater(lambda m: m.set_value(count(xv.get_value())))
        with self.voiceover(
            "Rudin pins the upper limit down with two properties. <bookmark mark='t'/> Some subsequence converges "
            "to it, and above it the sequence is eventually absent: <bookmark mark='x'/> pick any level x above one. "
            "Only finitely many terms are higher: <bookmark mark='y'/> two terms for x equal to 1.2, nine for 1.05. "
            "<bookmark mark='z'/> Push x below one and infinitely many terms are above it. So one is the dividing line, "
            "and no other number has both properties."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm))
            vo.wait_until("x")
            self.play(FadeIn(lev), FadeIn(x_l), FadeIn(cnt_l))
            vo.wait_until("y")
            self.wait(0.6)
            self.play(xv.animate.set_value(1.05), run_time=1.5)
            vo.wait_until("z")
            self.play(xv.animate.set_value(0.9), run_time=1.5)
        assert count(1.2) == 2 and count(1.05) == 9 and count(0.9) == 20
        assert sum(d_.get_color() == ManimColor(C.PATHOLOGY) for d_ in dots) == count(0.9)  # the red dots are those
        dots.clear_updaters()
        cnt.clear_updaters()
        for m in (lev, x_l):
            m.clear_updaters()
        self.play(FadeOut(VGroup(lev, x_l, cnt_l)), dots.animate.set_color(C.SEQ))
        conv = label(r"$s_n$ converges $\iff \limsup s_n = \liminf s_n$ \ (then both equal the limit)", font_size=30,
                     color=C.EPS).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='c'/> And a sequence converges exactly when its upper and lower limits agree: the "
            "high-water and low-water marks squeeze together, onto the limit."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(conv))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def all_rationals(self):
        d = load("limsup")
        r = d["rats"]
        M = len(r)
        ax = plain_axes([0, M + 10, 100], [-0.1, 1.1, 0.5], 11.6, 4.0, numbers=True, font_size=20,
                        axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([0, -1.2, 0])
        dots = VGroup(*[Dot(ax.c2p(k, v), radius=0.022, color=C.RATIONAL) for k, v in enumerate(r, start=1)])
        head = MathTex(r"0,\ 1,\ \tfrac12,\ \tfrac13,\ \tfrac23,\ \tfrac14,\ \tfrac34,\ \tfrac15,\ \ldots", font_size=38,
                       color=C.RATIONAL).to_edge(UP, buff=0.3)
        sub = label(r"every rational in $[0, 1]$, listed by denominator", font_size=26, color=GREY_A).next_to(head, DOWN,
                                                                                                           buff=0.15)
        target = 1 / math.sqrt(2)
        # the denominators of the list, block by block; from each block, the fraction nearest the target
        q_of = np.array([1, 1] + [q for q in range(2, 41) for p in range(1, q) if math.gcd(p, q) == 1])
        assert len(q_of) == M
        idx = [min(np.where(q_of == q)[0], key=lambda k: abs(r[k] - target)) for q in range(2, 41)]
        sub_dots = VGroup(*[dots[k] for k in idx])
        tline = DashedLine(ax.c2p(0, target), ax.c2p(M + 10, target), color=C.APPROX, stroke_width=2)
        t_l = MathTex(r"\tfrac{1}{\sqrt2}", font_size=30, color=C.APPROX).next_to(ax.c2p(M + 10, target), RIGHT, buff=0.1)
        res = VGroup(label(r"every point of $[0, 1]$ is a subsequential limit:", font_size=28),
                     MathTex(r"E = [0, 1], \quad \limsup = 1, \quad \liminf = 0", font_size=34)
                     ).arrange(DOWN, buff=0.15).move_to([0, 1.55, 0])
        with self.voiceover(
            "E can be much bigger than two points. <bookmark mark='a'/> List every fraction between zero and one, by "
            "denominator: zero, one, a half, a third, two thirds, and so on. <bookmark mark='b'/> Pick any point, say "
            "one over root two. From each block of the list take the fraction nearest to it: that's a subsequence "
            "converging to one over root two. <bookmark mark='c'/> The same works for every point of the interval, so E "
            "is the whole interval from zero to one. Its upper limit is one, its lower limit zero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), Create(ax))
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(tline), FadeIn(t_l))
            self.play(LaggedStart(*[x.animate.set_color(C.APPROX).scale(2.2) for x in sub_dots], lag_ratio=0.08),
                      run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(res))
        errs = np.abs(r[idx] - target)
        assert errs[-1] < 0.02 and np.all(np.diff(idx) > 0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def special(self):
        d = load("sequences")
        n, rr = d["n"], d["r"]
        head = label(r"\textbf{Rudin 3.20} \ Five limits worth knowing", font_size=34).to_edge(UP, buff=0.3)
        mains = [r"\tfrac{1}{n^p} \to 0", r"\sqrt[n]{p} \to 1", r"\sqrt[n]{n} \to 1", r"\tfrac{n^\alpha}{(1 + p)^n} \to 0",
                 r"x^n \to 0"]
        conds = [r"$p > 0$", r"$p > 0$", r"\phantom{$p$}", r"$p > 0$", r"$|x| < 1$"]
        cols = [-5.2, -2.6, 0.0, 2.6, 5.2]
        facts = VGroup(*[VGroup(MathTex(m_, font_size=32, color=C.SEQ if i == 2 else WHITE),
                                note(c_)).arrange(DOWN, buff=0.08)
                         for i, (m_, c_) in enumerate(zip(mains, conds))])
        for f_, x_ in zip(facts, cols):
            f_.move_to([x_, 2.35, 0])
        # a sparkline under each: the first 30 terms and the limit
        k = np.arange(1, 31, dtype=float)
        seqs = [([1 / k], (0, 1.05), 0.0), ([4 ** (1 / k), 0.25 ** (1 / k)], (0, 4.2), 1.0),
                ([k ** (1 / k)], (0.9, 1.5), 1.0), ([k**3 / 1.5**k], (0, 21), 0.0), ([(-0.8) ** k], (-0.85, 0.85), 0.0)]
        sparks = VGroup()
        for x_, (ys_list, yr, lim) in zip(cols, seqs):
            sa = Axes(x_range=[0, 31, 10], y_range=[yr[0], yr[1], (yr[1] - yr[0]) / 2], x_length=1.95, y_length=2.6,
                      tips=False, axis_config={"stroke_color": GREY_D, "stroke_width": 1.5, "include_ticks": False})
            sa.move_to([x_ - 0.15, -0.5, 0])
            ll = DashedLine(sa.c2p(0, lim), sa.c2p(31, lim), color=WHITE, stroke_width=1.2, stroke_opacity=0.7)
            lim_l = MathTex(f"{lim:g}", font_size=22, color=GREY_B).next_to(sa.c2p(31, lim), RIGHT, buff=0.08)
            dd = VGroup(*[Dot(sa.c2p(a, b), radius=0.03, color=c_) for ys_, c_ in zip(ys_list, (C.SEQ, C.APPROX))
                          for a, b in zip(k, ys_)])
            sparks.add(VGroup(sa, VGroup(ll, lim_l), dd))
            assert all(yr[0] <= v <= yr[1] for ys_ in ys_list for v in ys_)  # every dot inside its window
        # the two families on the second sparkline, labelled
        sp1 = sparks[1][0]
        sparks[1].add(MathTex(r"p = 4", font_size=22, color=C.SEQ).next_to(sp1.c2p(2, 4 ** 0.5), RIGHT, buff=0.15),
                      MathTex(r"p = \tfrac14", font_size=22, color=C.APPROX).next_to(sp1.c2p(2, 0.25 ** 0.5), RIGHT,
                                                                                     buff=0.15))
        assert abs((k**3 / 1.5**k).max() - 20.0) < 0.2 and np.argmax(k ** (1 / k)) == 2
        with self.voiceover(
            "Rudin collects five limits that the convergence tests will lean on: <bookmark mark='a'/> one over n to "
            "a positive power goes to zero; the n-th root of a positive number goes to one; the n-th root of n goes to "
            "one; any power of n over an exponential goes to zero; and x to the n goes to zero when x is smaller than "
            "one in size. Let's look at two of them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(f, shift=UP * 0.15), Create(sp[0]), Create(sp[1]),
                                                   LaggedStart(*[FadeIn(x) for x in sp[2]], lag_ratio=0.03),
                                                   *[FadeIn(x) for x in sp[3:]])
                                    for f, sp in zip(facts, sparks)], lag_ratio=0.4), run_time=6.0)
        self.play(FadeOut(head), FadeOut(sparks), FadeOut(VGroup(*[f_[1] for f_ in facts])),
                  VGroup(*[f_[0] for f_ in facts]).animate.scale(0.8).arrange(RIGHT, buff=0.7).to_edge(UP, buff=0.3))

        rows = [MathTex(r"n", r"=", r"(1 + x_n)^n", font_size=38),
                MathTex(r"n", r"\ge", r"\binom{n}{2} x_n^2 = \frac{n(n-1)}{2}\, x_n^2", font_size=38),
                MathTex(r"0 \le x_n", r"\le", r"\sqrt{\frac{2}{n - 1}} \to 0", font_size=38)]
        whys = [why(r"write $\sqrt[n]{n} = 1 + x_n$, \ $x_n \ge 0$"),
                why(r"binomial theorem: keep one term"),
                why(r"rearrange")]
        step = ladder(self, rows, whys, keep=3, top=2.35, buff=0.38, x=-1.2)
        lx = plain_axes([0, 6.2, 1], [0.9, 1.6, 0.1], 10.4, 2.2, numbers=False).move_to([0.2, -2.15, 0])
        ticks = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_B).next_to(lx.c2p(k, 0.9), DOWN, buff=0.12)
                         for k in range(0, 7)])
        ylab = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(lx.c2p(0, v), LEFT, buff=0.25)
                        for v in (1.0, 1.2, 1.4)])
        lg = np.log10(n)
        assert rr.max() < 1.6 and rr.min() > 0.9
        curve = polyline(lx, lg, rr, color=C.SEQ, stroke_width=3)
        m = n[n >= 9]
        assert np.all(1 + np.sqrt(2 / (m - 1)) < 1.6)
        bound = polyline(lx, np.log10(m), 1 + np.sqrt(2 / (m - 1)), color=C.UPPER_SUM, stroke_width=2.5)
        one = DashedLine(lx.c2p(0, 1), lx.c2p(6.2, 1), color=GREY_B, stroke_width=1.5)
        c_l = MathTex(r"\sqrt[n]{n}", font_size=28, color=C.SEQ).next_to(lx.c2p(0.6, 1.44), UP, buff=0.05)
        b_l = MathTex(r"1 + \sqrt{2/(n-1)}", font_size=26, color=C.UPPER_SUM).next_to(lx.c2p(2.0, 1.15), UR, buff=0.05)
        with self.voiceover(
            "The n-th root of n is the subtle one: n grows, but the root shrinks the exponent. Who wins? "
            "<bookmark mark='a'/> Write the root as one plus x n. <bookmark mark='b'/> By the binomial theorem, n is at "
            "least one term of the expansion, n times n minus one over two, times x n squared. <bookmark mark='c'/> "
            "Rearranged, x n is squeezed to zero. <bookmark mark='g'/> On a logarithmic scale, out to a million, the "
            "root peaks at n equal to 3 and then sinks toward one, under the bound."
        ) as vo:
            self.play(Create(lx), FadeIn(ticks), FadeIn(ylab), Create(one))
            self.play(Create(curve), FadeIn(c_l), run_time=1.5)
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("g")
            self.play(Create(bound), FadeIn(b_l), run_time=1.2)
        assert rr.argmax() == 2 and abs(n[2] - 3) < 1e-9
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hump(self):
        d = load("limsup")
        lgv, peak, lg_max, cross = d["lg"], int(d["peak"]), float(d["lg_max"]), int(d["cross"])
        k = np.arange(1, len(lgv) + 1)
        ax = plain_axes([0, 1000, 100], [-12, 18, 6], 10.0, 4.6, numbers=True, font_size=20).move_to([0.8, -0.9, 0])
        assert -12 < lgv.min() and lgv.max() < 18  # the whole curve lies inside the window
        ylab = MathTex(r"\log_{10} \frac{n^{10}}{1.1^n}", font_size=26).next_to(ax.c2p(0, 12), LEFT, buff=0.6)
        curve = polyline(ax, k, lgv, color=C.SEQ, stroke_width=3.5)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(1000, 0), color=GREY_B, stroke_width=1.5)
        head = label(r"$\dfrac{n^\alpha}{(1+p)^n} \to 0$: \ exponentials beat powers, eventually", font_size=34)
        head.to_edge(UP, buff=0.3)
        pk = Dot(ax.c2p(peak, lg_max), radius=0.07, color=WHITE)
        val = 10 ** lg_max
        pk_l = MathTex(rf"n = {peak}:\ \ \frac{{n^{{10}}}}{{1.1^n}} \approx {sci(val, 1)}", font_size=28).next_to(pk, UR,
                                                                                                          buff=0.1)
        cr = Dot(ax.c2p(cross, 0), radius=0.07, color=C.EPS)
        cr_l = label(rf"below 1 for good from $n = {cross}$", font_size=26, color=C.EPS).next_to(cr, UR, buff=0.12)
        with self.voiceover(
            "And powers against exponentials. <bookmark mark='a'/> n to the tenth over 1.1 to the n: the numerator "
            "starts far ahead. On a log scale, <bookmark mark='b'/> the ratio climbs to about seven quadrillion at n "
            "equal to 105. <bookmark mark='c'/> But each step multiplies the denominator by 1.1, and multiplies the "
            "numerator by less and less, so from n equal to 686 on the ratio stays below one, and it goes to zero. "
            "Any power, any exponential base above one: the exponential always wins."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(ylab), Create(zero))
            vo.wait_until("b")
            self.play(Create(curve), run_time=2.5)
            self.play(FadeIn(pk), FadeIn(pk_l))
            vo.wait_until("c")
            self.play(FadeIn(cr), FadeIn(cr_l))
        assert 7e15 < val < 8e15 and peak == 105 and cross == 686
        self.wait(0.5)
        self.clear_scene()
