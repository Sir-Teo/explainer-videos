from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis8.common import load, logn_axes, plain_axes, polyline


class Hook(VoiceoverScene):
    def construct(self):
        self.recap()
        self.kernel()
        self.counting()
        self.plan()

    # ------------------------------------------------------------------
    def recap(self):
        led = ledger(filled=7, highlight=8).scale(0.9)
        with self.voiceover(
            "Seven rows of the ledger are filled. Each part found a complete space and asked what compactness costs "
            "there. <bookmark mark='l'/> Part 8 asks those questions about every complete normed space at once."
        ) as vo:
            self.play(FadeIn(led))
            vo.wait_until("l")
            self.play(Indicate(led.rows[7], color=C.EPS, scale_factor=1.03))
        self.play(FadeOut(led))

    # ------------------------------------------------------------------
    def kernel(self):
        d = load("lebesgue")
        xs, D20 = d["xs"], d["D20"]
        ax = plain_axes([-math.pi, math.pi, math.pi / 2], [-10, 42, 10], 6.2, 3.2).move_to([-3.3, 0.8, 0])  # D20 >= -8.92
        tk = VGroup(*[MathTex(s, font_size=20).next_to(ax.c2p(v, -10), DOWN, buff=0.1)
                      for s, v in ((r"-\pi", -math.pi), ("0", 0), (r"\pi", math.pi))])
        g = polyline(ax, xs, D20, color=C.SEQ, stroke_width=2.5)
        # |D_20| where D_20 < 0: the negative lobes flipped up (where D_20 > 0, |D_20| is the blue curve itself)
        absg = runs(ax, xs, np.where(D20 < 0, -D20, np.nan), C.PATHOLOGY, 2).set_stroke(opacity=0.85)
        absg.set_z_index(1)
        neg = Polygon(*([ax.c2p(a, 0) for a in xs[::2]] + [ax.c2p(a, b) for a, b in zip(xs[::-2], np.minimum(D20, 0)[::-2])]),
                      stroke_width=0, fill_color=C.PATHOLOGY, fill_opacity=0.5)
        k_l = MathTex(r"D_{20}(t) = \textstyle\sum_{|k| \le 20} e^{ikt}", font_size=28, color=C.SEQ).next_to(ax, UP, buff=0.1)
        s_l = MathTex(r"s_n(f)(0) = \frac{1}{2\pi}\int f(t)\, D_n(t)\,dt", font_size=30).move_to([3.6, 2.3, 0])
        rows = VGroup(
            label(r"the best $f$ with $|f| \le 1$ is $\mathrm{sign}\, D_n$:", font_size=24),
            MathTex(r"\sup_{\|f\|_\infty \le 1} |s_n(f)(0)| = \|D_n\|_1", font_size=30, color=C.EPS),
            label(r"a continuous $f$ gets within $3\%$ of it:", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.6, 1.0, 0])
        near, nn = d["near"], d["near_ns"]
        from videos.analysis.analysis8.compute import lebesgue_constant
        cells = [[MathTex(r"n", font_size=24, color=GREY_A), MathTex(r"\|D_n\|_1", font_size=24, color=GREY_A),
                  MathTex(r"s_n(f_n)(0)", font_size=24, color=GREY_A)]]
        for n, v in zip(nn, near):
            cells.append([MathTex(f"{int(n)}", font_size=24), MathTex(rf"{lebesgue_constant(int(n)):.4f}", font_size=24),
                          MathTex(rf"{v:.4f}", font_size=24)])
        cw = [max(r_[j].width for r_ in cells) for j in range(3)]
        lefts = [0.0, cw[0] + 0.5, cw[0] + cw[1] + 1.0]
        tab = VGroup()
        for i, r_ in enumerate(cells):
            for j, c_ in enumerate(r_):
                c_.move_to([lefts[j] + c_.width / 2, -0.42 * i, 0])
            tab.add(VGroup(*r_))
        tab.move_to([3.6, -0.55, 0])
        L, ns, asym = d["L"], d["ns"], d["asym"]
        # ||D_n||_1 against log n: the same axes as chapter 4's plots of it (the y-axis left of the dot at n = 1)
        bx, bt = logn_axes(6.2, 1.6, center=[-3.3, -2.5, 0])
        lg = np.log10(ns)
        pts = VGroup(*[Dot(bx.c2p(a, b), radius=0.05, color=C.OPERATOR) for a, b in zip(lg, L)])
        curve = polyline(bx, np.linspace(0.5, 6, 100), 4 / math.pi**2 * np.log(10 ** np.linspace(0.5, 6, 100)) + 1.2703,
                         color=WHITE, stroke_width=1.5)
        b_l = MathTex(r"\|D_n\|_1 \approx \tfrac{4}{\pi^2}\log n + 1.27 \to \infty", font_size=24, color=C.OPERATOR).next_to(
            bx, UP, buff=0.05).align_to(bx, LEFT)
        out = MathTex(rf"n = 10^6: \ \|D_n\|_1 = {L[-1]:.4f} \ \text{{vs}} \ \tfrac{{4}}{{\pi^2}}\log n + 1.27 = {asym[-1]:.4f}",
                      font_size=24, color=GREY_A).move_to([3.6, -2.2, 0])
        assert np.all(np.abs(L[2:] - asym[2:]) / L[2:] < 0.01)
        assert b_l.get_top()[1] < tk.get_bottom()[1] - 0.05 and bt.get_bottom()[1] > -3.6
        head = label(r"Why might a Fourier series diverge? \ The Dirichlet kernel's side lobes", font_size=34).to_edge(
            UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The n-th partial sum of a Fourier series at zero is the integral of f against the "
            "Dirichlet kernel. The kernel has a tall peak and many side lobes, some negative. "
            "<bookmark mark='b'/> A function bounded by one can line up its sign with the kernel's, and then its "
            "partial sum at zero is the total area under the absolute value of the kernel. Continuous functions can "
            "come within three percent of that. <bookmark mark='c'/> And that area grows without bound: like four "
            "over pi squared times the log of n, computed here out to a million. So for each n there's a bounded "
            "continuous function whose n-th partial sum at zero is large. Does a single continuous function have "
            "partial sums that grow without bound?"
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(tk), Create(g), FadeIn(k_l), FadeIn(s_l))
            self.play(FadeIn(neg))
            vo.wait_until("b")
            self.play(Create(absg), FadeIn(rows))
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bt), FadeIn(b_l), Create(curve))
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.15), FadeIn(out), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counting(self):
        rows = VGroup(
            label(r"du Bois-Reymond (1873): \ yes, \ by an explicit and delicate construction", font_size=26),
            label(r"Banach and Steinhaus (1927): \ yes, \ by counting:", font_size=26, color=C.EPS),
            MathTex(r"\|\Lambda_n\| = \|D_n\|_1 \to \infty \ \Rightarrow \ \sup_n |s_n(f)(0)| = \infty \text{ for "
                    r"\emph{most} } f \in C(T)", font_size=30, color=C.EPS),
            label(r"``most'' \ = \ all but a countable union of nowhere dense sets \ (Baire, 1899)", font_size=24),
            label(r"a theorem about the existence of monsters, \ proved by counting", font_size=26, color=C.PATHOLOGY),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.4)
        # the construction's building block (Fejer): Q_n = 2 sin(nx) sum_{k <= n} sin(kx)/k is bounded by 2 Si(pi)
        # for every n, but its partial sums at 0 climb to the harmonic number H_n ~ log n
        n_ = 40
        xq = np.linspace(-math.pi, math.pi, 4001)
        Q = 2 * np.sin(n_ * xq) * sum(np.sin(k * xq) / k for k in range(1, n_ + 1))
        si_pi = 1.851937051982466  # Si(pi), the Gibbs constant
        assert np.abs(Q).max() <= 2 * si_pi + 1e-9
        coef = {}  # Q_n = sum_k [cos((n-k)x) - cos((n+k)x)] / k: its cosine coefficients by frequency
        for k in range(1, n_ + 1):
            coef[n_ - k] = coef.get(n_ - k, 0) + 1 / k
            coef[n_ + k] = coef.get(n_ + k, 0) - 1 / k
        sN = np.cumsum([coef.get(m, 0.0) for m in range(2 * n_ + 1)])  # s_N(Q_n)(0)
        Hn = sum(1 / k for k in range(1, n_ + 1))
        assert abs(sN.max() - Hn) < 1e-12 and abs(sN[-1]) < 1e-12
        qa = plain_axes([-math.pi, math.pi, math.pi / 2], [-4, 4, 2], 5.4, 2.2).move_to([-3.5, 1.2, 0])
        qg = polyline(qa, xq, Q, color=C.SEQ, stroke_width=2)
        bnd = VGroup(*[DashedLine(qa.c2p(-math.pi, s_ * 2 * si_pi), qa.c2p(math.pi, s_ * 2 * si_pi), color=GREY_B,
                                  stroke_width=1.5) for s_ in (1, -1)])
        ql = MathTex(rf"Q_{{{n_}}}(x) = 2\sin({n_}x)\sum_{{k \le {n_}}} \tfrac{{\sin kx}}{{k}}: \ |Q_{{{n_}}}| \le "
                     rf"2\,\mathrm{{Si}}(\pi) = {2 * si_pi:.3f}", font_size=22, color=C.SEQ).next_to(qa, UP, buff=0.08)
        sa = plain_axes([0, 2 * n_, 10], [0, 5, 1], 5.4, 2.2,
                        y_axis_config={"include_numbers": True, "font_size": 18,
                                       "decimal_number_config": {"num_decimal_places": 0}}).move_to([3.5, 1.2, 0])
        sg = VGroup(*[Line(sa.c2p(m, 0), sa.c2p(m, sN[m]), color=C.PATHOLOGY, stroke_width=3) for m in range(2 * n_ + 1)])
        sl = MathTex(rf"s_N(Q_{{{n_}}})(0): \ \text{{peak }} H_{{{n_}}} = {Hn:.3f} \approx \log {n_} + \gamma",
                     font_size=22, color=C.PATHOLOGY).next_to(sa, UP, buff=0.08)
        nl = MathTex(r"N", font_size=22, color=GREY_A).next_to(sa.c2p(2 * n_, 0), RIGHT, buff=0.1)
        cap = VGroup(label(r"the building block of such constructions (Fej\'er's polynomials): \ uniformly bounded,",
                           font_size=22, color=GREY_A),
                     label(r"yet the partial sums at $0$ reach $\log n$; \ glue infinitely many, with small weights",
                           font_size=22, color=GREY_A)).arrange(DOWN, buff=0.08).move_to([0, -0.4, 0])
        assert cap.width < 12.4 and cap.get_bottom()[1] > rows.get_top()[1] + 0.2
        head = label(r"The answer, two ways", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Du Bois-Reymond answered yes in 1873, with an explicit and delicate construction. "
            "<bookmark mark='b'/> Banach and Steinhaus answered it in three lines. The functionals that take f to its "
            "n-th partial sum at zero have norms that go to infinity. Their theorem then says the partial sums are "
            "unbounded, not just for one f, but for most continuous functions, in a precise sense due to Baire. "
            "<bookmark mark='c'/> A theorem about the existence of monsters, proved by counting. That's the spirit of "
            "this part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(qa), Create(qg), FadeIn(bnd), FadeIn(ql))
            self.play(Create(sa), FadeIn(nl), LaggedStart(*[Create(l_) for l_ in sg], lag_ratio=0.03), FadeIn(sl),
                      FadeIn(cap), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        chapters = [
            r"Banach spaces and bounded operators", r"Spaces without norms", r"Baire's theorem", r"Uniform boundedness",
            r"Open mappings and closed graphs", r"Hahn--Banach", r"Dual spaces", r"Weak convergence",
            r"Banach--Alaoglu", r"Extreme points (Krein--Milman)", r"Compact operators", r"Four applications",
        ]
        items = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=27) for i, t in enumerate(chapters)])
        colL = VGroup(*items[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([-3.2, -0.5, 0])
        colR = VGroup(*items[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([3.3, -0.5, 0]).align_to(colL, UP)
        head = label(r"Part 8: Banach spaces", font_size=42).to_edge(UP, buff=0.4)
        sub = label(r"Rudin, \textit{Real and Complex Analysis}, chapter 5, \ and \textit{Functional Analysis}, chapters 1--5",
                    font_size=24, color=GREY_B).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "Here's the plan, following chapter five of Real and Complex Analysis and the first five chapters of "
            "Rudin's Functional Analysis. <bookmark mark='a'/> First the spaces, and Baire's theorem with its three "
            "children: uniform boundedness, open mappings and closed graphs. <bookmark mark='b'/> Then Hahn-Banach "
            "and duality, weak convergence, and the compactness that comes back in the weak-star topology. "
            "<bookmark mark='c'/> Then extreme points, compact operators, and four applications."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(5)], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(5, 9)], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(9, 12)], lag_ratio=0.3))
        self.wait(0.6)
        self.clear_scene()
