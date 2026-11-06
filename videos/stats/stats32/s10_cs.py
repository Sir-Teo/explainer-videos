from __future__ import annotations

import numpy as np

from videos.stats.stats32.common import *  # noqa: F403


class Compressed(VoiceoverScene):
    def construct(self):
        self.card()
        self.bp()
        self.spikes()
        self.nsp()
        self.rip()
        self.random()
        self.phase()
        self.lines()
        self.panels()
        self.noise()

    def card(self):
        card = chapter_card(9, r"Compressed sensing", r"When $\ell_1$ finds the sparsest answer exactly", lit=(2006,), part=PART)
        with self.voiceover("Chapter nine. Compressed sensing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bp(self):
        rows = [
            cmath(r"y", r"=", r"A x, \ \ A \in \mathbb R^{n \times p}, \ n < p, \ \|x\|_0 = s", font_size=32),
            cmath(r"\min \|z\|_0", r"\text{ s.t. }", r"Az = y: \ \text{finds } x \text{ if } n \ge 2s, \ \text{but intractable}", font_size=28),
            cmath(r"\min \|z\|_1", r"\text{ s.t. }", r"Az = y: \ \text{a linear program}", font_size=30),
            cmath(r"\text{question}", r":", r"\text{when are the two answers the same?}", font_size=30),
        ]
        rows[2][-1].set_color(LASSO)
        whys = [why(r"noiseless, \ underdetermined"), why(r"any $2s$ columns independent"),
                why(r"basis pursuit: \ Chen, \ Donoho \& Saunders (1998)"), why(r"the equivalence problem")]
        with self.voiceover(
            "<bookmark mark='a'/> Strip the statistics away: noiseless measurements y equal A x, with fewer measurements than "
            "unknowns and an s-sparse x. <bookmark mark='b'/> Searching for the sparsest solution finds x whenever any two s "
            "columns of A are independent, but that search is the intractable one. <bookmark mark='c'/> Minimizing the one "
            "norm subject to the equations is a linear program, basis pursuit. <bookmark mark='d'/> The question of "
            "compressed sensing is when the tractable answer equals the intractable one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def spikes(self):
        d = load("cs")
        x, bp, ln = (np.asarray(d[k]) for k in ("x", "bp", "ln"))
        p = d["p"]
        t = np.arange(p)
        A1 = axes([0, p], [-2.3, 2.3], x_length=11.0, y_length=2.0, xlabel=r"", ylabel=r"basis pursuit", xticks=[], yticks=[-2, 0, 2],
                  center=[0.3, 1.5, 0])
        A2 = axes([0, p], [-2.3, 2.3], x_length=11.0, y_length=2.0, xlabel=r"coordinate", ylabel=r"least norm", xticks=[0, 50, 100, 150, 200],
                  yticks=[-2, 0, 2], center=[0.3, -1.5, 0])

        def stems(ax, v, color, sw=2.5, tol=1e-6):
            return VGroup(*[Line(ax.c2p(i, 0), ax.c2p(i, v[i]), color=color, stroke_width=sw) for i in t if abs(v[i]) > tol])

        tr1 = VGroup(*[Dot(A1.ax.c2p(i, x[i]), radius=0.06, color=SPIKE) for i in np.flatnonzero(x)])
        tr2 = VGroup(*[Dot(A2.ax.c2p(i, x[i]), radius=0.06, color=SPIKE) for i in np.flatnonzero(x)])
        s1 = stems(A1.ax, bp, LASSO, 3)
        s2 = stems(A2.ax, ln, RES, 1.5)
        cap = label(rf"$p = {p}$ unknowns, \ $n = {d['n']}$ Gaussian measurements, \ $s = {d['s']}$ spikes \ (gold)",
                    font_size=22).to_edge(UP, buff=0.25)
        r1 = label(r"$\ell_1$: \ exact, \ to solver precision", font_size=20, color=LASSO).move_to(A1.ax.c2p(150, 2.6))
        r2 = label(rf"$\ell_2$: \ smeared everywhere, \ {100 * d['err_ln']:.0f}\% error", font_size=20, color=RES).move_to(A2.ax.c2p(150, 2.6))
        with self.voiceover(
            "<bookmark mark='a'/> A test. Two hundred unknowns, ten of them nonzero spikes in gold, and only sixty random "
            "measurements, each a Gaussian-weighted sum of all two hundred. <bookmark mark='b'/> Basis pursuit returns the "
            "ten spikes exactly, and zeros everywhere else. <bookmark mark='c'/> The least-norm solution, ridge's answer as "
            "lambda goes to zero, spreads the energy over every coordinate, with an error of about eighty-five percent of the "
            "signal's size."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(cap), FadeIn(A1), FadeIn(A2), FadeIn(tr1), FadeIn(tr2))
            vo.wait_until("b")
            self.play(Create(s1), FadeIn(r1))
            vo.wait_until("c")
            self.play(Create(s2), FadeIn(r2))
        self.clear_scene()

    def nsp(self):
        rows = [
            cmath(r"x + h", r":", r"\text{every solution, \ } h \in \mathrm{null}(A)", font_size=32),
            cmath(r"\|x + h\|_1", r"\ge", r"\|x_S\|_1 - \|h_S\|_1 + \|h_{S^c}\|_1", font_size=30),
            cmath(r"\|h_S\|_1 < \|h_{S^c}\|_1", r"\ \forall h \ne 0", r"\Rightarrow \ x \text{ is the unique } \ell_1 \text{ minimizer}", font_size=28),
            cmath(r"\text{the null space property}", r":", r"\text{necessary and sufficient, \ for every } s\text{-sparse } x", font_size=28),
        ]
        rows[2][-1].set_color(LASSO)
        whys = [why(r"the feasible set"), why(r"the triangle inequality, \ $S$ the support"),
                why(r"no null vector concentrates on $S$"), why(r"Cohen, \ Dahmen \& DeVore (2009)")]
        with self.voiceover(
            "<bookmark mark='a'/> The exact condition is short to derive. Every solution of the equations is x plus a vector "
            "h in the null space of A. <bookmark mark='b'/> By the triangle inequality, with S the support of x, the one norm "
            "of x plus h is at least the one norm of x, minus the part of h on S, plus the part of h off S. "
            "<bookmark mark='c'/> So if every nonzero null vector has less mass on S than off it, x is the unique minimizer. "
            "<bookmark mark='d'/> Requiring that for every set of size s is the null space property, and it is both necessary "
            "and sufficient for basis pursuit to recover every s-sparse vector."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rip(self):
        rows = [
            cmath(r"(1 - \delta_s)\|v\|^2", r"\le", r"\|Av\|^2 \le (1 + \delta_s)\|v\|^2 \ \ \forall\, s\text{-sparse } v", font_size=28),
            cmath(r"\delta_{2s} < \sqrt2 - 1", r"\Rightarrow", r"\text{the null space property, \ and stability}", font_size=30),
            cmath(r"\|\hat x - x\|_2", r"\le", r"C_0 \tfrac{\sigma_s(x)_1}{\sqrt s} + C_1 \epsilon", font_size=30),
            cmath(r"\text{certifying RIP}", r":", r"\text{NP-hard for a given } A", font_size=30),
        ]
        rows[1][-1].set_color(LASSO)
        whys = [why(r"the restricted isometry property"), why(r"Cand\`es \& Tao (2005); \ Cand\`es (2008)"),
                why(r"robust to near-sparsity and noise"), why(r"but random $A$ satisfy it")]
        with self.voiceover(
            "<bookmark mark='a'/> A more usable condition is the restricted isometry property of Candès and Tao: A nearly "
            "preserves the length of every sparse vector. <bookmark mark='b'/> If the isometry constant at level two s is "
            "below root two minus one, the null space property follows, and more: <bookmark mark='c'/> recovery is stable. "
            "With noise of size epsilon, or an x that is only nearly sparse, the error is bounded by the noise plus the size "
            "of x's tail. <bookmark mark='d'/> Checking the property for a given matrix is itself NP-hard. The rescue is "
            "randomness."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def random(self):
        rows = [
            cmath(r"A_{ij}", r"\sim", r"N(0, 1/n) \ \text{independent}", font_size=32),
            cmath(r"n", r"\ge", r"C\, s \log(p/s) \ \Rightarrow \ \delta_{2s} < \sqrt2 - 1 \ \text{w.h.p.}", font_size=30),
            cmath(r"\text{partial Fourier}", r":", r"n \ge C\, s \log^4 p \ \text{random frequencies}", font_size=30),
            cmath(r"\text{proof}", r":", r"\text{concentration + a union bound over supports}", font_size=30),
        ]
        rows[1][-1].set_color(LASSO)
        whys = [why(r"Gaussian measurements"), why(r"Baraniuk et al. (2008)"), why(r"Rudelson \& Vershynin (2008)"),
                why(r"Part 51")]
        with self.voiceover(
            "<bookmark mark='a'/> A matrix with independent Gaussian entries <bookmark mark='b'/> satisfies the restricted "
            "isometry property with high probability as soon as the number of measurements is a constant times s log of p "
            "over s: the count from chapter one. <bookmark mark='c'/> Randomly chosen Fourier coefficients, the MRI case, "
            "need only a few more logarithms. <bookmark mark='d'/> The proof combines concentration of measure for a single "
            "sparse vector with a union bound over all supports, and Part 51 does it in full."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def phase(self):
        d = load("cs")
        G = np.asarray(d["grid"])
        deltas, rhos = np.asarray(d["deltas"]), np.asarray(d["rhos"])
        A = axes([0.05, 0.95], [0, 1.0], x_length=6.6, y_length=5.0, xlabel=r"$\delta = n/p$ \ (measurements per unknown)",
                 ylabel=r"$\rho = s/n$ \ (sparsity per measurement)", xticks=[0.1, 0.5, 0.9], yticks=[0, 0.5, 1],
                 center=[-2.4, 0.0, 0])
        ax = A.ax
        cells = VGroup()
        dw = deltas[1] - deltas[0]
        dr = rhos[1] - rhos[0]
        for i, r in enumerate(rhos):
            for j, dl in enumerate(deltas):
                a, b = ax.c2p(dl - dw / 2, r - dr / 2), ax.c2p(dl + dw / 2, r + dr / 2)
                cells.add(Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0, fill_opacity=0.9,
                                    fill_color=interpolate_color(ManimColor(RES), ManimColor(HIT), float(G[i, j]))).move_to((a + b) / 2))
        cur = clip_curve(ax, np.asarray(d["curve_d"]), np.asarray(d["curve_r"]), WHITE, 3.5, ymax=1.0)
        rows = fit_rows(VGroup(
            label(r"basis pursuit with $p = 100$, \ 20 trials per cell", font_size=22),
            label(r"green: \ always exact; \ red: \ never", font_size=22, color=HIT),
            label(r"white: \ Donoho \& Tanner's asymptotic curve", font_size=22),
            label(rf"at $\delta = 0.5$: \ up to $s \approx {d['rho_half']:.2f}\, n$ spikes", font_size=22, color=LASSO),
            label(r"a sharp phase transition, \ not a gradual decline", font_size=22, color=SPIKE),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How sharp is it? For each combination of measurements per unknown, delta, and sparsity "
            "per measurement, rho, twenty random problems with a hundred unknowns. <bookmark mark='b'/> Green where basis "
            "pursuit always recovers the signal exactly, red where it never does. <bookmark mark='c'/> The white curve is "
            "David Donoho and Jared Tanner's asymptotic phase transition, from the combinatorial geometry of random "
            "polytopes. <bookmark mark='d'/> With half as many measurements as unknowns, signals with up to about point "
            "three nine n spikes are recovered. <bookmark mark='e'/> And the change from success to failure is abrupt: a "
            "phase transition, like water freezing."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.003), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(cur), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def lines(self):
        d = load("lines")["rows"]
        L = np.array([r["lines"] for r in d])
        em, et = np.array([r["err_me"] for r in d]), np.array([max(r["err_tv"], 1e-11) for r in d])
        A = axes([2, 32], [-11, 0.5], x_length=7.0, y_length=4.6, xlabel=r"radial lines measured", ylabel=r"$\log_{10}$ relative error",
                 xticks=[4, 8, 12, 16, 22, 30], yticks=[-10, -8, -6, -4, -2, 0], center=[-2.2, 0.2, 0])
        ax = A.ax
        l1 = VGroup(polyline(ax, L, np.log10(em), RES, 3), *[Dot(ax.c2p(a, np.log10(b)), radius=0.07, color=RES) for a, b in zip(L, em)])
        l2 = VGroup(polyline(ax, L, np.log10(et), LASSO, 3), *[Dot(ax.c2p(a, np.log10(b)), radius=0.07, color=LASSO) for a, b in zip(L, et)])
        rows = fit_rows(VGroup(
            label(r"the phantom, \ $128 \times 128$, \ against the number of lines", font_size=22),
            label(r"red: \ minimum energy improves slowly", font_size=22, color=RES),
            label(r"blue: \ minimum TV", font_size=22, color=LASSO),
            label(r"28\% at 12 lines, \ 3.7\% at 16, \ exact at 22", font_size=22, color=LASSO),
            label(r"the same phase transition, \ in an image", font_size=22, color=SPIKE),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The phantom shows the same transition. Its reconstruction error, on a log scale, against "
            "the number of radial lines measured. <bookmark mark='b'/> Minimum energy improves slowly and is still forty "
            "percent wrong at thirty lines. <bookmark mark='c'/> Minimum total variation is twenty-eight percent wrong at "
            "twelve lines, four percent at sixteen, and exact, to eight decimal places, at twenty-two. "
            "<bookmark mark='d'/> Below a threshold, failure; above it, perfection."
        ) as vo:
            self.add(phantom_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(l2), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def panels(self):
        d = load("lines")["rows"]
        recs = {r["lines"]: np.asarray(r["rec"]) for r in d if r["rec"] is not None}
        ph = load("phantom")
        p1 = PhantomPanel(recs[8], size=3.2, caption=r"8 lines: \ 58\% error", lo=0, hi=1, center=[-4.4, 0.4, 0], caption_color=RES)
        p2 = PhantomPanel(recs[12], size=3.2, caption=r"12 lines: \ 28\%", lo=0, hi=1, center=[0.0, 0.4, 0], caption_color=SPIKE)
        p3 = PhantomPanel(np.asarray(ph["tv"]), size=3.2, caption=r"22 lines: \ exact", lo=0, hi=1, center=[4.4, 0.4, 0], caption_color=HIT)
        with self.voiceover(
            "<bookmark mark='a'/> What the transition looks like. With eight lines, total variation produces a blocky cartoon "
            "with the wrong shapes. <bookmark mark='b'/> With twelve, the structure is there but the small features are "
            "wrong. <bookmark mark='c'/> With twenty-two, every ellipse is exactly right. This instrument, the phantom, is "
            "this part's build."
        ) as vo:
            self.add(phantom_tag())
            vo.wait_until("a")
            self.play(FadeIn(p1))
            vo.wait_until("b")
            self.play(FadeIn(p2))
            vo.wait_until("c")
            self.play(FadeIn(p3))
        self.wait(1.0)
        self.clear_scene()

    def noise(self):
        rows = fit_rows(VGroup(
            label(r"with noise, \ exact recovery becomes stable recovery: \ error $\propto$ noise", font_size=26),
            label(r"the lasso is basis pursuit's noisy cousin: \ $\min \tfrac12\|y - Ax\|^2 + \lambda\|x\|_1$", font_size=26, color=LASSO),
            label(r"in statistics we don't choose $X$: \ RIP becomes restricted eigenvalue conditions", font_size=26, color=GREY_A),
            label(r"Part 52 proves the lasso's oracle inequality under them", font_size=26, color=SPIKE),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Real measurements are noisy, and then exact recovery becomes stable recovery: the error is "
            "proportional to the noise. <bookmark mark='b'/> The lasso is the natural noisy version of basis pursuit. "
            "<bookmark mark='c'/> The difference for statistics is that we rarely choose the design matrix; it is given to "
            "us, correlated and unrandom. The restricted isometry property is replaced by weaker restricted eigenvalue "
            "conditions. <bookmark mark='d'/> Under them, Part 52 proves that the lasso estimates s coefficients from n "
            "observations with error of order s log p over n, the oracle inequality."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
