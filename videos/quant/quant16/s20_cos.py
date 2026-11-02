from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import (BAD, GOOD, METHOD_COL, OPT, PART, illustration, load, loglog, polyline,
                                         predict, sci)

ORDER = ["Monte Carlo (QE, 50 steps)", "Monte Carlo, control variate", "ADI (Craig-Sneyd)", "Carr-Madan FFT", "COS"]


class COS(VoiceoverScene):
    def construct(self):
        cd = load("cos_density")
        f = load("fourier")
        r = load("race")
        rc = load("race_cv")
        self.card()
        self.rebuild(cd)
        self.derive()
        self.truncate(cd, f)
        self.race(r, rc)

    def card(self):
        c = chapter_card(16, r"Fourier II: the COS method, and the race", r"Which method should price this option?",
                         lit=(2008,), part=PART)
        with self.voiceover("Chapter sixteen. Fourier methods, part two: the cosine method, and the race."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rebuild(self, cd):
        y = np.asarray(cd["y"])
        tru = np.asarray(cd["true"])
        top = float(tru.max()) * 1.15
        g = axes([y[0], y[-1]], [-0.3, top], x_length=7.0, y_length=4.2, xlabel=r"log-return $\log(S_T/S_0)$",
                 ylabel=r"density", xticks=[-0.8, -0.4, 0, 0.4], yticks=[0, 1, 2], font_size=15)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        truth = curve(ax, y, tru, GREY_B, stroke_width=5)
        Ns = ["2", "4", "8", "16", "32", "64", "128"]
        recs = [curve(ax, y, np.clip(np.asarray(cd["rec"][n]), -0.3, top), QC.DELTA, stroke_width=3) for n in Ns]
        errs = {n: float(np.max(np.abs(np.asarray(cd["rec"][n]) - tru))) for n in Ns}
        tag = MathTex(r"N = 2", font_size=32, color=QC.DELTA).next_to(g, UP, buff=0.05).align_to(g, RIGHT)
        A = np.asarray(cd["A"])
        h = axes([0, len(A)], [-12, 1], x_length=4.2, y_length=3.0, xlabel=r"$k$",
                 ylabel=r"$|A_k|$ ($\log_{10}$)", xticks=[0, 100, 200], yticks=[-10, -5, 0], font_size=14)
        h.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
        dots = VGroup(*[Dot(h.ax.c2p(k, np.clip(np.log10(max(a_, 1e-12)), -12, 1)), radius=0.025, color=QC.DELTA)
                        for k, a_ in enumerate(A)])
        src = illustration(rf"Heston, one year: $v_0 = \theta = 0.04$, $\kappa = 1.5$, $\xi = 0.5$, $\rho = -0.7$; range "
                           rf"$[{cd['a']:.2f}, {cd['b']:.2f}]$")
        with self.voiceover(
            "Fang Fang and Kees Oosterlee's cosine method of 2008 asks a simpler question: what is the density of "
            "the log-return? In grey, Heston's. Rebuild it from cosines, one term after another. "
            "<bookmark mark='a'/> Two terms: a rough hump. Four, eight: the skew appears. Sixteen: the left tail. By "
            f"sixty-four the largest error is {errs['64']:.1e}, and at a hundred and twenty-eight it is gone. "
            "<bookmark mark='b'/> On the right, the size of each cosine's coefficient on a log scale: a straight "
            "line down. The coefficients fall exponentially, and so does the error. That is the method's whole "
            "advantage."
        ) as vo:
            self.play(FadeIn(g), Create(truth), FadeIn(src))
            self.play(Create(recs[0]), FadeIn(tag))
            vo.wait_until("a")
            cur = recs[0]
            for k in range(1, len(Ns)):
                self.play(ReplacementTransform(cur, recs[k]),
                          Transform(tag, MathTex(rf"N = {Ns[k]}", font_size=32, color=QC.DELTA).move_to(tag)), run_time=1.0)
                cur = recs[k]
                self.wait(0.3)
            vo.wait_until("b")
            self.play(FadeIn(h), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01, run_time=2.5))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"V", r"=", r"e^{-rT}\int_{\mathbb{R}} v(y)f(y)\,dy\ \approx\ e^{-rT}\int_a^b v(y)f(y)\,dy", font_size=32,
                  colors={r"V": OPT}),
            cmath(r"f(y)", r"=", r"{\sum_{k \ge 0}}' A_k\cos\Big(k\pi\frac{y - a}{b - a}\Big),\quad A_k = \frac{2}{b - a}"
                  r"\int_a^b f(y)\cos\Big(k\pi\frac{y - a}{b - a}\Big)dy", font_size=28),
            cmath(r"A_k", r"\approx", r"\frac{2}{b - a}\,\mathrm{Re}\Big[\varphi\Big(\frac{k\pi}{b - a}\Big)e^{-ik\pi\frac{a}{b - a}}\Big]",
                  font_size=32, colors={r"A_k": QC.DELTA}),
            cmath(r"V", r"\approx", r"e^{-rT}{\sum_{k < N}}'\,\mathrm{Re}\Big[\varphi\Big(\frac{k\pi}{b - a}\Big)"
                  r"e^{ik\pi\frac{x - a}{b - a}}\Big]V_k", font_size=32, colors={r"V": GOOD}),
            cmath(r"\text{error}", r"=", r"\text{truncation} + O(e^{-\nu N})", font_size=34, colors={r"\text{error}": BAD}),
        ]
        whys = [why(r"truncate to $[a, b] = c_1 \pm L\sqrt{c_2}$ from the cumulants; the tails are tiny"),
                why(r"any function on $[a, b]$ is a cosine series (the prime halves the first term)"),
                why(r"extend the integral back to the whole line: that is the characteristic function's definition"),
                why(r"the payoff's cosine coefficients $V_k$ are in closed form (the code's \texttt{chi} and \texttt{psi})"),
                why(r"exponential for densities analytic in a strip; Junike (2024) gives the $N$ for a target error "
                    r"(chapter 19)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Four steps. A price is the payoff integrated against the density; cut the integral to a finite range, "
            "set by the distribution's cumulants. <bookmark mark='a'/> On that range the density is a cosine series. "
            "<bookmark mark='b'/> Each coefficient is an integral of the density against a cosine, and extending it "
            "to the whole line turns it into the characteristic function at one frequency: known in closed form. "
            "<bookmark mark='c'/> The payoff's own cosine coefficients are elementary integrals, so the price is one "
            "short sum. <bookmark mark='d'/> Its error is the truncation, plus a term that falls exponentially in the "
            "number of terms."
        ) as vo:
            for i, mk in enumerate("abcd"):
                step(i)
                vo.wait_until(mk)
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def truncate(self, cd, f):
        L = np.asarray(cd["L"], float)
        e = np.asarray(cd["errL"])
        g = axes([2, 42], [-15, 0], x_length=5.6, y_length=3.8, xlabel=r"range half-width $L$ (in standard deviations)",
                 ylabel=r"price error, $N = 4{,}096$ ($\log_{10}$)", xticks=[10, 20, 30, 40], yticks=[-15, -10, -5, 0],
                 font_size=14).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ok = e > 0
        line = polyline(g.ax, L[ok], np.clip(np.log10(e[ok]), -15, 0), BAD, radius=0.05)
        mark = DashedLine(g.ax.c2p(16, -15), g.ax.c2p(16, 0), stroke_color=GREY_B, stroke_width=1.5)
        cos = [x for x in f["rows"] if x["method"] == "COS"]
        card = lab_card(r"the COS sum", [
            "k = np.arange(N)",
            "w = k * np.pi / (b - a)",
            "chi = (np.cos(w * (0 - a)) * 1.0 - np.cos(0.0) * np.exp(a)",
            "       + w * np.sin(w * (0 - a)) * 1.0) / (1 + w * w)",
            "psi = np.where(k == 0, -a, np.sin(w * (0 - a)) / np.where(k == 0, 1, w))",
            "Vk = 2.0 / (b - a) * (psi - chi)",
            "phi = cf(w, T)",
            "terms = (phi[None, :] * np.exp(1j * w[None, :] * (x[:, None] - a))).real * Vk[None, :]",
            "terms[:, 0] *= 0.5",
            "put = K * terms.sum(axis=1)",
        ], source="explainer/quant/house/stochvol.py  cos_price", width=6.6, font_size=16).to_edge(RIGHT, buff=0.3)
        card.shift(UP * 1.2)
        out = [f"N = {x['N']:>3}: error {x['err']:.1e}" for x in cos if x["N"] in (32, 64, 128, 256)]
        e16 = float(e[list(L).index(16.0)])
        with self.voiceover(
            "The other knob is the range. Too narrow, and the left tail of a strongly skewed density is cut off: with "
            f"a half-width of four standard deviations the error is {e[0]:.2f}. Widen it, and the truncation error "
            f"falls fast; at sixteen, the House's choice for this correlation, it is about {e16 * 1e8:.0f} in a hundred "
            "million. "
            "<bookmark mark='a'/> The House's COS code is ten lines: the put's coefficients in closed form, the "
            "characteristic function at each frequency, one sum, and the call by put–call parity. "
            f"<bookmark mark='b'/> Run it: with {cos[-2]['N']} terms the error is about {cos[-2]['err'] * 1e8:.0f} in a "
            "hundred million."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(mark))
            vo.wait_until("a")
            self.play(FadeIn(card))
            vo.wait_until("b")
            lab_run(self, card, out, font_size=17)
        self.wait(0.5)
        self.clear_scene()

    def race(self, r, rc):
        pts = r["points"] + rc["points"]
        g = loglog(-4.2, 1.5, -8, 0, r"wall-clock time (seconds, one core)", r"error in the price", x_length=7.4,
                   y_length=4.6, xt=[-4, -2, 0], yt=[-8, -6, -4, -2, 0])
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        clock = ValueTracker(-4.2)
        by = {m: sorted([q for q in pts if q["method"] == m], key=lambda q: q["time"]) for m in ORDER}

        def draw(m):
            def make():
                rr = [q for q in by[m] if np.log10(q["time"]) <= clock.get_value()]
                grp = VGroup()
                pp = [ax.c2p(np.clip(np.log10(q["time"]), -4.2, 1.5), np.clip(np.log10(max(q["err"], 1e-9)), -8, 0)) for q in rr]
                if len(pp) > 1:
                    grp.add(VMobject(stroke_color=METHOD_COL[m], stroke_width=3).set_points_as_corners(pp))
                grp.add(*[Dot(q_, radius=0.06, color=METHOD_COL[m]) for q_ in pp])
                return grp
            return always_redraw(make)

        lines = [draw(m) for m in ORDER]
        leg = legend([(METHOD_COL[m], m) for m in ORDER], font_size=15).next_to(g, RIGHT, buff=0.25).align_to(g, UP)
        cv = rc["points"][-1]
        mc = by[ORDER[0]][-1]
        cos_best = min(by["COS"], key=lambda q: q["err"])
        side = VGroup(
            wrapped_label(rf"the stock as control buys a variance ratio of {cv['ratio']:.1f}: the line shifts down by "
                          rf"$\sqrt{{{cv['ratio']:.1f}}}$ and keeps its slope", 4.0, 17, GREY_A),
            wrapped_label(r"Fourier for vanillas when the model has a characteristic function (Bermudans too: Fang and "
                          r"Oosterlee 2009); grids for low-dimensional early exercise and barriers; simulation for "
                          r"everything else", 4.0, 17, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        q = predict(r"Why can COS not price a barrier directly?", width=4.0, font_size=19).to_corner(DR, buff=0.25)
        src = illustration(r"Monte Carlo's plotted error is its standard error; reference: COS, 4{,}096 terms, $L = 40$",
                           corner=DL)
        with self.voiceover(
            "Now the race of the opening, run again with everything we know, including Monte Carlo with a control "
            "variate. The clock runs from a tenth of a millisecond to ten seconds. <bookmark mark='a'/> COS finishes "
            f"first, with an error of {cos_best['err'] * 1e8:.0f} in a hundred million in under a millisecond. "
            "Carr–Madan follows, then the ADI grid. <bookmark mark='b'/> Monte Carlo crawls down its square-root "
            f"line; the control variate shifts it down by a factor of {np.sqrt(cv['ratio']):.1f}, but cannot change "
            "the slope. Its plotted error is the standard error, the honest expected size. "
            "<bookmark mark='c'/> So the rule: Fourier when the model allows it and the product is a vanilla; grids "
            "for low-dimensional products with early exercise or barriers; simulation for everything else. Pause and "
            "predict: why can the cosine method not price a barrier? It needs only the terminal density, and a "
            "barrier needs the path."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src), *[FadeIn(x) for x in lines])
            vo.wait_until("a")
            self.play(clock.animate.set_value(-1.5), run_time=4, rate_func=linear)
            vo.wait_until("b")
            self.play(clock.animate.set_value(1.5), run_time=4, rate_func=linear)
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(q))
        for x in lines:
            x.clear_updaters()
        self.wait(0.5)
        self.clear_scene()
