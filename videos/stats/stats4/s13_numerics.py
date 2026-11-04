from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


class Numerics(VoiceoverScene):
    def construct(self):
        self.card()
        self.float_()
        self.condition()
        self.experiment()
        self.centring()
        self.cancellation()
        self.practice()

    def card(self):
        card = chapter_card(12, r"Conditioning and numerics", r"Why you should never invert $X^\top X$", lit=(1947,), part=PART)
        with self.voiceover("Chapter twelve. Conditioning and numerics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def float_(self):
        d = load("numerics")
        rows = VGroup(
            MathTex(r"0.1 + 0.2", r"=", r"0.30000000000000004", font_size=38),
            MathTex(rf"\epsilon_{{\text{{machine}}}} = 2^{{-52}} \approx {d['machine_eps']:.2e}", font_size=34, color=EIG),
            label(r"every operation can lose a relative error of about $\epsilon$", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to([0, 0.8, 0])
        rows[0][2].set_color(RES)
        hc = note(r"floating point: \ IEEE 754 (1985); \ J. von Neumann \& H. Goldstine (1947), \ J. H. Wilkinson (1963)")
        hc.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Everything so far has been exact algebra. Computers don't do exact algebra. <bookmark mark='a'/> In "
            "double precision, nought point one plus nought point two is not quite nought point three. "
            "<bookmark mark='b'/> Numbers carry about sixteen significant digits, and each operation can lose a "
            "relative error of about two to the minus fifty-two. <bookmark mark='c'/> Usually that's harmless. The "
            "question is when it gets amplified."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(hc))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def condition(self):
        rows = [
            cmath(r"\kappa(X)", r"=", r"\frac{\sigma_{\max}(X)}{\sigma_{\min}(X)}", font_size=38),
            cmath(r"\frac{\|\delta\boldsymbol\beta\|}{\|\boldsymbol\beta\|}", r"\lesssim", r"\kappa \cdot \frac{\|\delta \mathbf y\|}{\|\mathbf y\|}",
                  font_size=34),
            cmath(r"\kappa(X^\top X)", r"=", r"\kappa(X)^2", font_size=38),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"the condition number: \ the ellipse's stretch, \ chapter 6"), why(r"relative errors are amplified by $\kappa$"),
                why(r"squaring the singular values squares the stretch")]
        take = label(r"solving the normal equations squares the condition number; \ QR works with $X$ itself", font_size=26,
                     color=S.ACCENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The amplification factor is the condition number. <bookmark mark='a'/> It's the ratio of the largest "
            "to the smallest singular value: how much the matrix stretches its most-stretched direction compared "
            "with its least. <bookmark mark='b'/> Relative errors in the data can be amplified by that factor in the "
            "solution. <bookmark mark='c'/> And here's the trap: X transpose X has the squared singular values of X, "
            "so its condition number is the square of X's. <bookmark mark='d'/> Forming X transpose X and inverting "
            "it squares the damage. A QR decomposition works with X directly and doesn't."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.6, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

    def experiment(self):
        d = load("numerics")
        rws = d["rows"]
        A = axes([-0.5, 3.5], [-16, 1], x_length=7.0, y_length=4.4, ylabel=r"error in $\hat{\boldsymbol\beta}$ (log scale)",
                 yticks=[-15, -10, -5, 0], yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.4, -0.4, 0])
        ax = A.ax
        labs = VGroup()
        bars = VGroup()
        for k, r in enumerate(rws):
            for dx, val, col in ((-0.17, r["err_ne"], RES), (0.17, r["err_qr"], FIT)):
                lv = max(np.log10(max(val, 1e-16)), -16)
                bars.add(Rectangle(width=0.3, height=ax.c2p(0, lv)[1] - ax.c2p(0, -16)[1], stroke_width=0, fill_color=col,
                                   fill_opacity=0.85).move_to(ax.c2p(k + dx, (lv - 16) / 2)))
            labs.add(MathTex(rf"\kappa \approx 10^{{{np.log10(r['condX']):.0f}}}", font_size=22, color=GREY_A)
                     .next_to(ax.c2p(k, -16), DOWN, buff=0.15))
        leg = legend([(RES, r"normal equations: \ invert $X^\top X$"), (FIT, r"QR")], font_size=22).move_to([4.2, 2.2, 0])
        setup = label(r"two almost identical columns: \ $x_2 = x_1 + \epsilon\, \cdot$ noise; \ exact answer $(1, 2, 3)$",
                      font_size=22, color=GREY_B).to_edge(UP, buff=0.3)
        res = VGroup(*[MathTex(rf"\kappa = {r['condX']:.0e}:\ \ {r['err_ne']:.0e}\ \text{{vs}}\ {r['err_qr']:.0e}",
                               font_size=22) for r in rws]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, 0.2, 0])
        take = label(r"statistical software uses QR (or the SVD), \ never $(X^\top X)^{-1}$", font_size=24, color=S.ACCENT)
        take.move_to([4.0, -1.8, 0])
        if take.width > 5.8:
            take.width = 5.8
        with self.voiceover(
            "Here's the difference, measured. <bookmark mark='a'/> A regression with two nearly identical columns, "
            "whose exact coefficients are one, two and three, with no noise at all. As the columns get closer, the "
            "condition number grows from twenty to twenty million. <bookmark mark='b'/> Solving the normal "
            "equations, red, loses accuracy fast: at the end the coefficients are wrong in the first decimal. "
            "<bookmark mark='c'/> QR, blue, stays accurate to nine or ten digits. <bookmark mark='d'/> That's why "
            "every serious statistical package solves least squares with QR or the SVD, and why you should never "
            "write the inverse of X transpose X in code, however often it appears in formulas."
        ) as vo:
            self.play(FadeIn(setup), FadeIn(A), FadeIn(labs), FadeIn(leg))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[0::2]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[1::2]], lag_ratio=0.2), FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

    def centring(self):
        e = load("extras")["centre"]
        rows = VGroup(
            label(r"a quadratic in height: \ columns $1,\ h,\ h^2$ \ with $h \approx 170$", font_size=28),
            MathTex(rf"\operatorname{{corr}}(h, h^2) = {e['corr_raw']:.4f}", r"\qquad", rf"\kappa(X) = {e['raw']:.1e}",
                    font_size=32, color=RES),
            label(r"centre first: \ columns $1,\ h - \bar h,\ (h - \bar h)^2$", font_size=28),
            MathTex(rf"\operatorname{{corr}} = {e['corr_cen']:.3f}", r"\qquad", rf"\kappa(X) = {e['cen']:.0f}", font_size=32,
                    color=FIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.5, 0])
        take = label(r"the same model, \ the same fitted values, \ thirty thousand times better conditioned", font_size=26,
                     color=S.ACCENT).to_edge(DOWN, buff=0.7)
        tag = simulated_tag(r"simulated: 200 of the World's adults")
        with self.voiceover(
            "Bad conditioning usually comes from the way variables are coded, and the cure is often trivial. "
            "<bookmark mark='a'/> Fit a quadratic in height, with columns one, h and h squared. Heights are all "
            "near a hundred and seventy, so h and h squared are almost perfectly correlated, <bookmark mark='b'/> "
            "and the condition number is in the millions. <bookmark mark='c'/> Centre the heights first. "
            "<bookmark mark='d'/> The correlation drops to a sixth, and the condition number to about two hundred. "
            "It's exactly the same model, with the same fitted values; only the coordinates changed. Centring and "
            "scaling before fitting cost nothing and buy several digits."
        ) as vo:
            self.play(FadeIn(tag))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            self.play(FadeIn(take))
        self.clear_scene()

    def cancellation(self):
        e = load("extras2")["cancel"]
        rows = [
            cmath(r"s^2", r"=", r"\frac{1}{n-1}\Big(\sum_i x_i^2 - n\bar x^2\Big)", font_size=34),
            cmath(r"s^2", r"=", r"\frac{1}{n-1}\sum_i (x_i - \bar x)^2", font_size=34),
        ]
        rows[0][2].set_color(RES)
        rows[1][2].set_color(FIT)
        whys = [why(r"one pass: \ subtract two huge, nearly equal numbers"), why(r"two passes: \ centre first")]
        tbl = VGroup(*[MathTex(rf"\text{{offset }} 10^{{{int(np.log10(r['off'])) if r['off'] > 0 else 0}}}:\ \ "
                               rf"{r['naive']:.6f}\ \ \text{{vs}}\ \ {r['two']:.6f}", font_size=26)
                       for r in e["rows"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        tbl.move_to([0, -1.4, 0])
        hdr = label(r"1,000 of the World's heights, \ measured from further and further away", font_size=22, color=GREY_B)
        hdr.next_to(tbl, UP, buff=0.2)
        take = label(r"algebraically equal, \ numerically not: \ Welford's one-pass update (1962) is both", font_size=24,
                     color=S.ACCENT).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The same lesson appears in the humblest formula in statistics. <bookmark mark='a'/> The variance can be "
            "computed in one pass, as the sum of squares minus n times the squared mean. <bookmark mark='b'/> Or in "
            "two passes, centring first. Algebraically they're identical. <bookmark mark='c'/> Take a thousand of "
            "the World's heights and add a constant, as if measuring from further away; the variance shouldn't "
            "change at all. With an offset of a hundred million, the one-pass formula loses the third significant "
            "figure: it subtracts two enormous, nearly equal numbers, and the digits that mattered cancel away. The "
            "two-pass formula doesn't notice. <bookmark mark='d'/> Statistical software uses two passes, or "
            "Welford's clever one-pass update."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.8, x=-0.8, buff=0.6, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in tbl], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

    def practice(self):
        steps = VGroup(
            label(r"1. \ centre and scale the columns", font_size=28),
            label(r"2. \ factor $X = QR$ \ (Householder reflections, \ Golub 1965)", font_size=28),
            label(r"3. \ solve the triangular system $R\hat{\boldsymbol\beta} = Q^\top\mathbf y$ \ by back-substitution", font_size=28),
            label(r"4. \ for standard errors, \ use $(X^\top X)^{-1} = R^{-1}R^{-\top}$, \ never the product itself", font_size=28),
            label(r"5. \ if $R$ has tiny diagonal entries, \ the design is nearly rank-deficient: \ pivot, \ or use the SVD", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.2, 0])
        for s_ in steps:
            if s_.width > 12.8:
                s_.width = 12.8
        head = label(r"How regression software actually solves least squares", font_size=34, color=S.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "So here, in five steps, is how good regression software solves least squares, and how this part's "
            "toolkit fits together. <bookmark mark='a'/> Centre and scale the columns, to keep the conditioning down. "
            "<bookmark mark='b'/> Factor X as Q R, using Householder's reflections, as Gene Golub showed in 1965, "
            "which is more stable still than Gram–Schmidt. <bookmark mark='c'/> Solve the triangular system by "
            "back-substitution. <bookmark mark='d'/> When standard errors need X transpose X inverse, get it from R, "
            "never by forming the product. <bookmark mark='e'/> And if R has a tiny diagonal entry, the design is "
            "nearly rank-deficient: pivot the columns, or fall back on the SVD and the pseudoinverse. Every formula "
            "in Part 12 will be written with inverses; every computation should be done like this."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(steps[k], shift=RIGHT * 0.2))
        self.clear_scene()
