from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BOUND, HIST, MEAS, TEST, TRAIN, chapter, curve, load, log_axes


class DoubleDescent(VoiceoverScene):
    def construct(self):
        chapter(self, 12, r"Double descent", r"What happens past the point of fitting everything?",
                "Chapter twelve. Double descent.", lit=(2019,))
        self.curve()
        self.spectrum()
        self.ridge()

    def curve(self):
        d = load("double")
        ps, te, tr = (np.asarray(d[k]) for k in ("ps", "test", "train"))
        n = int(d["n"])
        lx = np.log10(ps)
        ylo, yhi = -1.0, 2.0
        ax = Axes(x_range=[1, 3.8, 1], y_range=[0, yhi - ylo, 1], x_length=9.0, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.0, -0.6, 0])
        xl = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for t, v in (("10", 1), ("100", 2), ("1{,}000", 3))])
        yl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=22, color=GREY_B).next_to(ax.c2p(1, v - ylo), LEFT, buff=0.1)
                      for v in range(int(ylo), int(yhi) + 1)])
        xn = label(r"$p$: \ random features per page", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.5)
        yn = label(r"squared error on new pages", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        k_n = int(np.argmin(np.abs(ps - n)))
        k_min1 = int(np.argmin(te[:k_n]))

        def seg(a, b):
            return curve(ax, lx[a:b], np.clip(np.log10(te[a:b]), ylo, yhi) - ylo, TEST, 5)

        part1, part2, part3 = seg(0, k_n - 2), seg(k_n - 3, k_n + 3), seg(k_n + 2, len(ps))
        nline = DashedLine(ax.c2p(math.log10(n), 0), ax.c2p(math.log10(n), yhi - ylo), color=WHITE, stroke_width=2)
        nl = label(rf"$p = n = {n}$: \\ as many features as pages", font_size=24, color=WHITE)
        nl.next_to(nline.get_top(), RIGHT, buff=0.15).shift(DOWN * 0.3)
        trc = curve(ax, lx, np.clip(np.log10(np.maximum(tr, 10 ** ylo)), ylo, yhi) - ylo, TRAIN, 3)
        trl = label(r"training pages: \ fitted exactly past $n$", font_size=22, color=TRAIN)
        trl = VGroup(Line(ORIGIN, RIGHT * 0.5, color=TRAIN, stroke_width=3), trl).arrange(RIGHT, buff=0.15)
        trl.next_to(ax.c2p(1.1, 2.55), RIGHT, buff=0)  # a key in the empty top left, off the curves
        low = Dot(ax.c2p(lx[k_min1], math.log10(te[k_min1]) - ylo), radius=0.08, color=TEST)
        final = Dot(ax.c2p(lx[-1], math.log10(te[-1]) - ylo), radius=0.08, color=TEST)
        floor = DashedLine(ax.c2p(1, math.log10(te[k_min1]) - ylo), ax.c2p(3.8, math.log10(te[k_min1]) - ylo), color=TEST,
                           stroke_width=1.5).set_stroke(opacity=0.5)
        classic = label(r"the classical U", font_size=26, color=TEST).next_to(low, UP, buff=0.35)
        modern = label(r"and down again", font_size=26, color=TEST).next_to(final, UP, buff=0.3).shift(LEFT * 0.4)
        colors = {r"\boldsymbol{\beta}": C.MODEL_Q}
        mn = cmath(r"\min", r"\|", r"\boldsymbol{\beta}", r"\|", r"\;\text{ among all exact fits}", colors=colors,
                   font_size=32).to_corner(UR, buff=0.4)
        cite_ = cite(r"M.~Belkin, D.~Hsu, S.~Ma \& S.~Mandal (2019); \ P.~Nakkiran et al.\ (2020)", corner=UL)
        below = te[-1] < te[k_min1]
        feats, fits = self.features_picture(), self.min_norm_picture()
        with self.voiceover(
            "Here's the curve that came back. Turn each page into p random features: each feature is a fixed random "
            "mix of the seventy word rates, passed through a bend that zeroes anything negative. Only the weights on "
            "the features are learned, by least squares. <bookmark mark='m'/> When there are more features than "
            "pages, many fits match every training page exactly, so take the one with the smallest weights: of all "
            "the curves through the points, the calmest. <bookmark mark='a'/> With few features, the error on new "
            "pages falls, then "
            "rises again as p approaches the number of pages: the classical U. <bookmark mark='b'/> At exactly "
            f"{n} features, as many as there are pages, the fit is forced through every point, and the error "
            "explodes. <bookmark mark='c'/> And then, past it, the error comes back down"
            + (", lower than the bottom of the U." if below else ", though not quite to the bottom of the U.")
        ) as vo:
            self.play(FadeIn(feats[0]), FadeIn(feats[2]), FadeIn(cite_))
            self.play(Create(feats[1]), FadeIn(feats[3]), run_time=1.5)
            self.play(Create(feats[4]), FadeIn(feats[5]))
            vo.wait_until("m")
            self.play(FadeIn(fits[0]), FadeIn(mn))
            self.play(Create(fits[1]), FadeIn(fits[3]))
            self.play(Create(fits[2]), FadeIn(fits[4]))
            vo.wait_until("a")
            self.play(FadeOut(feats), FadeOut(fits))
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xn), FadeIn(yn))
            self.play(Create(part1), run_time=2.0)
            self.play(FadeIn(low), FadeIn(classic))
            vo.wait_until("b")
            self.play(Create(nline), FadeIn(nl), Create(part2), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(part3), run_time=2.0)
            self.play(Create(floor), FadeIn(final), FadeIn(modern))
        # the size of the fitted weights against p (computed with the curve): it peaks where the fit is forced
        nm = np.asarray(d["norms"])
        ny0, ny1 = math.floor(np.log10(nm.min()) * 2) / 2, math.ceil(np.log10(nm.max()) * 2) / 2
        nax = CornerAxes(x_range=[1, 3.8, 1], y_range=[ny0, ny1, 0.5], x_length=2.9, y_length=1.9, tips=False,
                         axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ncap = label(r"the size of the fitted weights \\ (log scale)", font_size=20, color=C.MODEL_Q)
        ninset = VGroup(ncap, nax).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([5.3, 0.3, 0])
        keep_in_frame(ninset, margin=0.2)
        ncurve = curve(nax, lx, np.log10(nm), C.MODEL_Q, 3)
        nn_ = DashedLine(nax.c2p(math.log10(n), ny0), nax.c2p(math.log10(n), ny1), color=WHITE, stroke_width=1.5)
        peak_at_n = abs(int(np.argmax(nm)) - k_n) <= 1
        below_u = nm[-1] < nm[k_min1]
        with self.voiceover(
            ("More parameters than data, and better on new data. " if below else
             "More parameters than data, and still good on new data. ")
            + "Belkin and colleagues named it double descent in "
            "2019, and Nakkiran and colleagues found it in deep networks the same year. <bookmark mark='a'/> The training error is zero all along "
            "the second descent, so it can't be what decides. What decides is which of the many exact fits you "
            "get, and the smallest one is the simplest. "
            + ("<bookmark mark='n'/> Its size tells the story: the weights blow up at the peak, where the fit is "
               "forced, then shrink as features are added"
               + (", ending smaller than at the bottom of the U. " if below_u else ". ")
               if peak_at_n else
               "<bookmark mark='n'/> Past the peak, the smallest fit's weights shrink as features are added. ")
            + "And from chapter ten: gradient descent from zero finds exactly that smallest fit."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(trc), FadeIn(trl))
            vo.wait_until("n")
            self.play(FadeIn(ncap), Create(nax), Create(nn_))
            self.play(Create(ncurve), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectrum(self):
        d = load("double")
        n = int(d["n"])
        ps = np.asarray(d["ps"])
        sm = np.asarray(d["smin"])
        show = [int(s) for s in d["show"]]
        rows = [
            cmath(r"\hat\beta = F^{+} t", r"=", r"\sum_i \frac{u_i^\top t}{\sigma_i}\, v_i", font_size=32),
            cmath(r"\hat\beta_{\text{noise}}", r"=", r"\sum_i \frac{u_i^\top \varepsilon}{\sigma_i}\, v_i", font_size=32),
            cmath(r"\mathbb{E}\,|\hat\beta_{\text{noise}}|^2", r"=", r"s^2 \sum_i \frac{1}{\sigma_i^2}", font_size=32,
                  colors={r"s^2 \sum_i \frac{1}{\sigma_i^2}": C.SURPRISE}),
        ]
        whys = [why(r"the SVD of the $n \times p$ feature matrix $F$"),
                why(r"the part of the labels no feature explains: \ noise $\varepsilon$"),
                why(r"$u_i^\top \varepsilon$ has variance $s^2$: \ the smallest $\sigma_i$ dominates")]
        step = ladder(self, rows, whys, keep=3, top=3.4, x=-3.0, buff=0.3, edge=6.9)
        # the singular values for one p, sorted, on a log scale
        G = axes([0, n], [-4, 1], x_length=6.0, y_length=3.2, xticks=[0, n], yticks=[-4, -3, -2, -1, 0, 1],
                 yfmt=lambda v: "1" if v == 0 else (f"10" if v == 1 else f"10^{{{int(v)}}}"),
                 xlabel=r"singular values, \ largest to smallest", center=(-3.3, -1.8, 0), font_size=18)
        ax = G.ax
        k = ValueTracker(0)

        def spec():
            i = int(np.clip(round(k.get_value()), 0, len(show) - 1))
            S = np.sort(np.asarray(d[f"spec{show[i]}"]))[::-1]
            xs = np.linspace(0, n, len(S))
            ys = np.clip(np.log10(np.maximum(S, 1e-4)), -4, 1)
            g = VGroup(*[Line(ax.c2p(x, -4), ax.c2p(x, y), color=C.TRUE_P, stroke_width=1.2).set_stroke(opacity=0.8)
                         for x, y in zip(xs[::3], ys[::3])])
            g.add(Dot(ax.c2p(xs[-1], ys[-1]), radius=0.08, color=C.SURPRISE))
            g.add(label(rf"$p = {show[i]}$", font_size=26, color=WHITE).next_to(ax.c2p(n, 1), DL, buff=0.1))
            return g

        sp = always_redraw(spec)
        H = log_axes((1, 3.8), (-4, 1), x_length=5.4, y_length=3.2, xticks=[1, 2, 3], yticks=[-4, -2, 0],
                     xlabel=r"$p$ features", ylabel=r"smallest singular value $\sigma_{\min}/\sqrt p$",
                     center=(3.6, -1.8, 0), font_size=18)
        hx = H.ax
        cs = curve(hx, np.log10(ps), np.clip(np.log10(np.maximum(sm, 1e-4)), -4, 1), C.SURPRISE, 3.5)
        nl = DashedLine(hx.c2p(math.log10(n), -4), hx.c2p(math.log10(n), 1), color=WHITE, stroke_width=1.5)
        kn = int(np.argmin(np.abs(ps - n)))
        with self.voiceover(
            "Why the peak, exactly at p equals n? Write the minimum-norm fit with the singular value decomposition "
            "of the feature matrix. <bookmark mark='a'/> It's a sum over directions, each label component divided "
            "by its singular value sigma i. <bookmark mark='b'/> Part of the labels is noise no feature explains. "
            "<bookmark mark='c'/> That part gets amplified by one over sigma, and its expected size is the noise "
            "variance times the sum of one over sigma squared. So everything hangs on the smallest singular value. "
            "<bookmark mark='d'/> Here are the feature matrix's singular values as p grows. With few features they "
            "stay well away from zero. <bookmark mark='e'/> As p approaches n, the smallest slides toward zero, and "
            f"at p equals n it's {sm[kn]:.0e}: a square random matrix is nearly singular. "
            "<bookmark mark='f'/> Past it, with more features than pages, the smallest singular value climbs back "
            "up, and the noise is spread over directions that barely affect new pages."
        ) as vo:
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(i)
            vo.wait_until("d")
            self.play(FadeIn(G), FadeIn(H), Create(nl))
            self.add(sp)
            k1 = show.index(n) if n in show else len(show) // 2
            vo.wait_until("e")
            self.play(k.animate.set_value(k1), run_time=3.0, rate_func=linear)
            self.play(Create(cs), run_time=1.5)
            vo.wait_until("f")
            self.play(k.animate.set_value(len(show) - 1), run_time=3.0, rate_func=linear)
        sp.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ridge(self):
        d = load("double")
        ps, te = np.asarray(d["ps"]), np.asarray(d["test"])
        rd = np.asarray(d["ridge"])
        lams = list(d["lams"])
        n = int(d["n"])
        ylo, yhi = -1.0, 2.0
        G = log_axes((1, 3.8), (ylo, yhi), x_length=8.0, y_length=4.4, xticks=[1, 2, 3], yticks=[-1, 0, 1, 2],
                     xlabel=r"$p$: \ random features per page", ylabel=r"squared error on new pages",
                     center=(-1.6, -0.6, 0))
        ax = G.ax
        lx = np.log10(ps)
        c0 = curve(ax, lx, np.clip(np.log10(te), ylo, yhi), TEST, 4)
        cols = [C.MODEL_Q, C.INTERVAL, GREY_B]
        cr = VGroup(*[curve(ax, lx, np.clip(np.log10(rd[:, j]), ylo, yhi), cols[j], 3) for j in range(len(lams))])
        key = legend([(TEST, r"no ridge: \ the minimum-norm fit")] +
                     [(cols[j], rf"ridge $\lambda = {lams[j]:g}\,p$") for j in range(len(lams))], font_size=20)
        key.to_corner(UR, buff=0.4)
        kn = int(np.argmin(np.abs(ps - n)))
        best = int(np.argmin([rd[:, j].max() for j in range(len(lams))]))
        hist = history_card(2020, r"P.~Nakkiran, P.~Venkat, S.~Kakade \& T.~Ma", r"\textit{Optimal Regularization Can "
                            r"Mitigate Double Descent}", width=5.6, font_size=18, color=HIST).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The cure follows: don't divide by tiny numbers. Ridge regression adds lambda to each sigma squared, so "
            f"the smallest directions are damped instead of amplified. <bookmark mark='a'/> With lambda {lams[best]:g} "
            f"times p, the peak at {n} features is gone: the error there is {rd[kn, best]:.2f}, against "
            f"{te[kn]:.1f} without it. <bookmark mark='b'/> Too little ridge leaves a bump; too much, and the fit is "
            "too timid everywhere. Nakkiran and colleagues showed in 2020 that well-tuned regularization removes the "
            "peak in such models. The peak was never a law of nature: it's an artifact of fitting noise exactly "
            "with barely enough features to do it."
        ) as vo:
            self.play(FadeIn(G), Create(c0), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(Create(cr[best]), FadeIn(key[best + 1]))
            vo.wait_until("b")
            others = [j for j in range(len(lams)) if j != best]
            self.play(*[Create(cr[j]) for j in others], *[FadeIn(key[j + 1]) for j in others])
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    @staticmethod
    def features_picture() -> VGroup:
        """What a random feature is: the 70 word rates, mixed by fixed random weights and bent (ReLU) into p features;
        only the weights from the features to the prediction are learned. Parts: inputs, fixed lines, features,
        their labels, learned lines, their label."""
        def column(n, x, color, r=0.11):
            dots = VGroup(*[Circle(radius=r, color=color, stroke_width=2.5) for _ in range(n)])
            dots.arrange(DOWN, buff=0.16)
            dots.insert(n // 2, MathTex(r"\vdots", font_size=26, color=color))
            return dots.arrange(DOWN, buff=0.12).move_to([x, 0.1, 0])

        ins, fs = column(6, -6.0, GREY_B), column(8, -3.6, C.BITS)
        out = Circle(radius=0.16, color=C.MODEL_Q, stroke_width=3).move_to([-1.5, 0.1, 0])
        ci = [m for m in ins if isinstance(m, Circle)]
        cf = [m for m in fs if isinstance(m, Circle)]
        fixed = VGroup(*[Line(a.get_right(), b.get_left(), color=GREY_D, stroke_width=1.2) for a in ci for b in cf])
        learned = VGroup(*[Line(b.get_right(), out.get_left(), color=C.MODEL_Q, stroke_width=2.5) for b in cf])
        li = label(r"$70$ word rates", font_size=22, color=GREY_B).next_to(ins, DOWN, buff=0.25)
        lf = label(r"$p$ random features", font_size=22, color=C.BITS).next_to(fs, DOWN, buff=0.25)
        lm = label(r"fixed random mix, \\ then a bend", font_size=20, color=GREY_B).next_to(fixed, UP, buff=0.2)
        ll = label(r"learned weights", font_size=20, color=C.MODEL_Q).next_to(learned, UP, buff=0.2)
        return VGroup(ins, fixed, fs, VGroup(li, lf, lm), VGroup(learned, out), ll)

    @staticmethod
    def min_norm_picture() -> VGroup:
        """Two curves through the same four points: one with big weights, wild; the smallest-weight one, calm.
        Parts: axes and points, the wild fit, the calm fit, their two labels."""
        xs_, ys_ = np.array([-1.5, -0.5, 0.5, 1.5]), np.array([0.3, -0.25, 0.35, 0.05])
        calm_c = np.polyfit(xs_, ys_, 3)
        ax = Axes(x_range=[-1.8, 1.8, 1], y_range=[-1.3, 1.3, 1], x_length=4.6, y_length=2.8, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([3.7, 0.1, 0])
        calm = ax.plot(lambda t: np.polyval(calm_c, t), x_range=[-1.8, 1.8], color=C.MODEL_Q, stroke_width=4)
        wild = ax.plot(lambda t: np.polyval(calm_c, t) + 0.9 * math.sin(2 * math.pi * (t + 1.5)), x_range=[-1.8, 1.8],
                       color=C.SURPRISE, stroke_width=2.5)
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=WHITE) for a, b in zip(xs_, ys_)])
        lw = label(r"exact fit, \ big weights", font_size=22, color=C.SURPRISE)
        lc = label(r"exact fit, \ smallest weights", font_size=22, color=C.MODEL_Q)
        VGroup(lw, lc).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax, DOWN, buff=0.2)
        return VGroup(VGroup(ax, pts), wild, calm, lw, lc)
