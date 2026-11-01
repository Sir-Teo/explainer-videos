from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import (AUSTEN, BAD, DICKENS, GOOD, HIST, HL, chapter, load, page_dots, page_plane, plot,
                                  regions, sci_tex, side_ladder)
from videos.ai.ai6.compute import toy_clusters

GOLD = C.BITS


class SVM(VoiceoverScene):
    def construct(self):
        chapter(self, 11, r"The widest street", r"Which line, of all the lines that work?",
                "Chapter eleven. Support vector machines.", lit=(1995,))
        self.street()
        self.hinge()
        self.dual()
        self.pages()
        self.grid()

    # ------------------------------------------------------------------
    def street(self):
        s = load("svm")
        P, y = toy_clusters()
        w, b = np.asarray(s["toy_w"]), float(s["toy_b"])
        sv = [int(i) for i in s["toy_sv"]]
        U = 0.95
        C0 = np.array([-3.6, -0.4, 0])

        def S(z):
            return C0 + U * np.array([z[0], z[1], 0])

        dots = VGroup(*[Dot(S(p), radius=0.08, color=AUSTEN if l_ == 0 else DICKENS) for p, l_ in zip(P, y)])
        wn = w / np.linalg.norm(w)
        perp = np.array([-wn[1], wn[0]])
        c0 = -b / np.linalg.norm(w) * wn
        m = 1 / np.linalg.norm(w)
        L = 2.6

        def edge(off, color, dashed=False, sw=4):
            p0, p1 = S(c0 + off * wn - L * perp), S(c0 + off * wn + L * perp)
            return (DashedLine if dashed else Line)(p0, p1, color=color, stroke_width=sw)

        mid = edge(0, GOLD)
        edges = VGroup(edge(m, GREY_A, True, 2.5), edge(-m, GREY_A, True, 2.5))
        street = Polygon(S(c0 + m * wn - L * perp), S(c0 + m * wn + L * perp), S(c0 - m * wn + L * perp),
                         S(c0 - m * wn - L * perp), stroke_width=0, fill_color=GOLD, fill_opacity=0.12)
        rings = VGroup(*[Circle(radius=0.16, color=WHITE, stroke_width=3).move_to(S(P[i])) for i in sv])
        others = VGroup()
        for ang, sh in ((0.35, 0.1), (-0.3, -0.15), (0.6, 0.0)):
            u = rotate_vector(np.array([*perp, 0]), ang)[:2]
            others.add(Line(S(c0 + sh * wn - L * u), S(c0 + sh * wn + L * u), color=GREY_B, stroke_width=2))
        colors = {r"\|\mathbf{w}\|": GOLD}
        rows = [
            cmath(r"\text{dist}(\mathbf{x})", "=", r"\frac{|\mathbf{w}\cdot\mathbf{x} + b|}{\|\mathbf{w}\|}", font_size=32,
                  colors=colors),
            cmath(r"\min_i\, y_i(\mathbf{w}\cdot\mathbf{x}_i + b)", "=", r"1", font_size=32, colors=colors),
            cmath(r"\text{width}", "=", r"\frac{2}{\|\mathbf{w}\|}", font_size=32, colors=colors),
            cmath(r"\min\ \tfrac12\|\mathbf{w}\|^2", r"\ \ \text{s.t.}\ \ ", r"y_i(\mathbf{w}\cdot\mathbf{x}_i + b) \ge 1",
                  font_size=32, colors=colors),
        ]
        whys = [why(r"project onto the unit normal", font_size=20), why(r"choose the scale of $\mathbf{w}$", font_size=20),
                why(r"one $1/\|\mathbf{w}\|$ each side", font_size=20), why(r"widest street", font_size=20)]
        step = side_ladder(self, rows, whys, 3.4, 3.3, keep=4, top=3.0, buff=0.42)
        tag = note(r"illustrative points").to_corner(DL, buff=0.25)
        res = label(rf"${len(sv)}$ support vectors hold up the street", font_size=24, color=WHITE).to_edge(DOWN, buff=0.35)
        res.shift(RIGHT * 3.2)
        with self.voiceover(
            "Many lines separate these two groups. Vapnik's question: which is best? <bookmark mark='a'/> His answer: "
            "the one with the widest empty street on both sides. <bookmark mark='b'/> A point's distance to the line "
            "is the score over the length of w. <bookmark mark='c'/> Rescale w so the nearest points score exactly "
            "one; <bookmark mark='d'/> then the street is two over the length of w wide, <bookmark mark='e'/> and the "
            "widest street is the shortest w that keeps every point on its side. <bookmark mark='f'/> The street's "
            f"edges rest on just {len(sv)} points, the support vectors. Moving another point leaves this solution unchanged "
            "as long as that point stays outside the same margin."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03), FadeIn(tag))
            self.play(LaggedStart(*[Create(o) for o in others], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(others), FadeIn(street), Create(mid), Create(edges))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            step(3)
            vo.wait_until("f")
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hinge(self):
        g = plot([-2.5, 2.5, 1], [0, 4, 1], x_length=6.0, y_length=4.0, xticks=[-2, -1, 0, 1, 2], yticks=[0, 1, 2, 3, 4],
                 center=[-2.6, -0.5, 0], xlabel=r"the margin of a page, \ $y\,f(\mathbf{x})$", ylabel=r"loss")
        ax = g.ax
        m = np.linspace(-2.5, 2.5, 201)
        zero_one = VMobject(color=GREY_A, stroke_width=4).set_points_as_corners(
            [ax.c2p(-2.5, 1), ax.c2p(0, 1), ax.c2p(0, 0), ax.c2p(2.5, 0)])
        hingec = curve(ax, m, np.maximum(0, 1 - m), GOLD, stroke_width=5)
        logc = curve(ax, m, np.log2(1 + np.exp(-m)), C.TRUE_P, stroke_width=3, smooth=True)
        exp_m = np.r_[-math.log(4), m[m > -math.log(4)]]
        expc = curve(ax, exp_m, np.exp(-exp_m), "#B48EF0", stroke_width=3, smooth=True)
        key = VGroup(label(r"right or wrong \ ($0$--$1$)", font_size=22, color=GREY_A),
                     label(r"hinge: \ $\max(0,\ 1 - yf)$ \ (SVM)", font_size=22, color=GOLD),
                     label(r"logistic: \ $\log_2(1 + e^{-yf})$", font_size=22, color=C.TRUE_P),
                     label(r"exponential: \ $e^{-yf}$ \ (Chapter 14)", font_size=22, color="#B48EF0"))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.9, 1.6, 0])
        f = cmath(r"\min\ \tfrac12\|\mathbf{w}\|^2", "+", r"C\sum_i \max\big(0,\ 1 - y_i f(\mathbf{x}_i)\big)",
                  font_size=32, colors={"C": GOLD}).move_to([3.4, -0.8, 0])
        fn = label(r"$C$: \ the price of standing in the street", font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.2)
        cite_ = cite(r"C.~Cortes \& V.~Vapnik, \textit{Support-Vector Networks} (1995)", corner=DR)
        with self.voiceover(
            "Real authors overlap, so no street is empty. In 1995 Cortes and Vapnik let points stand in the street, "
            "or on the wrong side, at a price. <bookmark mark='a'/> The price is the hinge loss: zero for a page "
            "safely on its side, growing in a straight line as it crosses. <bookmark mark='b'/> Compare it with "
            "being right or wrong, which is difficult to optimize by gradients, and with logistic regression's loss. "
            "Both are convex substitutes for counting mistakes; logistic loss is smooth, while hinge loss has a corner "
            "at margin one. <bookmark mark='c'/> The constant C sets the price: large C, a "
            "narrow street that fights for every page; small C, a wide, forgiving one."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(hingec), FadeIn(key[1]))
            vo.wait_until("b")
            self.play(Create(zero_one), FadeIn(key[0]), Create(logc), FadeIn(key[2]), Create(expc), FadeIn(key[3]))
            vo.wait_until("c")
            self.play(Write(f), FadeIn(fn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dual(self):
        colors = {r"\alpha_i": GOLD, r"\alpha_j": GOLD, r"K(\mathbf{x}_i, \mathbf{x}_j)": C.REWARD}
        rows = [
            cmath(r"\mathcal{L}", "=", r"\tfrac12\|\mathbf{w}\|^2 + C\sum_i\xi_i - \sum_i \alpha_i\big[y_i(\mathbf{w}"
                  r"\cdot\mathbf{x}_i + b) - 1 + \xi_i\big] - \sum_i \mu_i\xi_i", font_size=30, colors=colors),
            cmath(r"\mathbf{w}", "=", r"\sum_i \alpha_i y_i \mathbf{x}_i, \quad \sum_i \alpha_i y_i = 0, \quad "
                  r"0 \le \alpha_i \le C", font_size=30, colors=colors),
            cmath(r"\max_{\boldsymbol\alpha}", r"\;\sum_i \alpha_i - \tfrac12\sum_{i,j}\alpha_i\alpha_j y_iy_j\,",
                  r"K(\mathbf{x}_i, \mathbf{x}_j)", font_size=30, colors=colors),
            cmath(r"\alpha_i\big[y_i f(\mathbf{x}_i) - 1 + \xi_i\big]", "=", r"0", font_size=30, colors=colors),
        ]
        whys = [why(r"Lagrange multipliers \\ (Part 4)", font_size=20),
                why(r"$\partial/\partial\mathbf{w},\ \partial/\partial b,\ \partial/\partial\xi_i = 0$", font_size=20),
                why(r"substitute: \ only dot products, \\ so any kernel fits", font_size=20),
                why(r"complementary slackness: \\ $\alpha_i > 0$ only at the street", font_size=20)]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.2, buff=0.45, edge=6.8)
        smo = label(r"solved two $\alpha$'s at a time: \ SMO \ (Platt, 1998)", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "This is a constrained problem, and Part 4's Lagrange multipliers turn it inside out. "
            "<bookmark mark='a'/> Give each page's constraint a multiplier alpha. <bookmark mark='b'/> Setting the "
            "derivatives to zero says the weights are a mix of the training pages themselves, and each alpha lies "
            "between zero and C. <bookmark mark='c'/> Substitute back, and the problem is about the alphas alone, "
            "and the pages appear only through dot products: swap in a kernel, and the street becomes curved. "
            "<bookmark mark='d'/> The KKT conditions finish it: alpha is zero for every page safely off the "
            "street. Only the support vectors count. <bookmark mark='e'/> Platt's SMO solves it two alphas at a time, "
            "and that's what we'll run."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=GOLD, scale_factor=1.05))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(smo))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pages(self):
        p = load("pages")
        s = load("svm")
        X2, y, test = np.asarray(p["X2"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
        tr = np.nonzero(~test)[0]
        plane = page_plane(x_length=6.8, y_length=4.6, center=[-3.1, -0.3, 0])
        ax = plane[0]
        dots = page_dots(ax, X2, y, idx=tr, jitter=0.3, radius=0.035, opacity=0.85)
        Cs = [float(c) for c in s["Cs"]]
        imgs, rings = {}, {}
        for C_ in Cs:
            key = f"C{C_:g}"
            imgs[C_] = regions(ax, (np.asarray(s[f"region_{key}"]) > 0).astype(float), s["xs"], s["ys"], opacity=0.42)
            svs = set(int(i) for i in s[f"sv_{key}"])
            rings[C_] = VGroup(*[Circle(radius=0.06, color=WHITE, stroke_width=1.2).move_to(d.get_center())
                                 for k_, d in enumerate(dots) if tr.tolist().index(d.page) in svs])
        ci = ValueTracker(0)

        def readout():
            C_ = Cs[int(round(ci.get_value()))]
            r = s[f"C{C_:g}"]
            return VGroup(MathTex(rf"C = {C_:g}", font_size=34, color=GOLD),
                          label(rf"support vectors: \ ${r['n_sv']}$ of ${s['n_train']}$", font_size=24, color=WHITE),
                          label(rf"held-out pages: \ ${100 * r['test']:.1f}\%$", font_size=24, color=GREY_A),
                          label(rf"primal $-$ dual: \ ${sci_tex(max(r['gap'], 1e-16))}$ \ (relative)", font_size=22,
                                color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.2, 1.3, 0])

        rd = always_redraw(readout)
        kk = s["kkt"]
        kkt = label(rf"KKT at $C = 1$, \ page by page: \ ${kk['outside'] + kk['bound_out']}$ violations",
                    font_size=22, color=GOOD).move_to([4.2, -0.6, 0])
        hist = history_card(1995, r"Cortes \& Vapnik", r"after Vapnik \& Chervonenkis (1963) and Boser, Guyon \& "
                            r"Vapnik's kernels (1992): \ for a decade, the method to beat", color=HIST, width=5.4)
        hist.move_to([4.0, -2.2, 0])
        c0, cb = s["C0.01"], s[f"C{Cs[-1]:g}"]
        cvC, cvg = float(s["C_cv"]), float(s["g_cv"])
        with self.voiceover(
            "Now the pages, with a Gaussian kernel, solved by SMO. <bookmark mark='a'/> At C equals "
            f"{Cs[0]:g}, standing in the street is cheap: {c0['n_sv']} of the {s['n_train']} pages are support "
            f"vectors, and the boundary barely bends. <bookmark mark='b'/> Raise C, and the street narrows: at "
            f"{Cs[-1]:g}, {cb['n_sv']} support vectors, and the boundary bends around the pages. Every solution is "
            "checked: the dual and the primal agree, and every page obeys its KKT condition. <bookmark mark='c'/> "
            f"Ten-fold cross-validation picks C equals {cvC:g} and a kernel width of {cvg:g}, and gets "
            f"{100 * s['acc_cv2']:.0f} percent of the held-out pages right; with all seventy rates, "
            f"{100 * s['acc70_rbf']:.1f}. <bookmark mark='d'/> From 1995 until deep networks took over around 2012, "
            "this was the method to beat."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(imgs[Cs[0]]), FadeIn(rings[Cs[0]]), FadeIn(rd))
            self.bring_to_front(dots)
            vo.wait_until("b")
            for i in range(1, len(Cs)):
                self.play(FadeOut(imgs[Cs[i - 1]]), FadeIn(imgs[Cs[i]]), FadeOut(rings[Cs[i - 1]]), FadeIn(rings[Cs[i]]),
                          ci.animate.set_value(i), run_time=1.1)
                self.bring_to_front(dots, rings[Cs[i]])
            self.play(FadeIn(kkt))
            vo.wait_until("c")
            rd.clear_updaters()
            self.play(FadeOut(rd), FadeOut(kkt))
            cvl = VGroup(label(rf"cross-validated: \ $C = {cvC:g}$, \ $\gamma = {cvg:g}$", font_size=24, color=GOLD),
                         label(rf"held-out pages: \ ${100 * s['acc_cv2']:.0f}\%$ \ ($2$ rates)", font_size=24, color=WHITE),
                         label(rf"all $70$ rates: \ ${100 * s['acc70_rbf']:.1f}\%$", font_size=24, color=HL)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.2, 1.2, 0])
            self.play(FadeIn(cvl))
            vo.wait_until("d")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grid(self):
        s = load("svm")
        cv = np.asarray(s["cv"])
        Cs, gs = [float(c) for c in s["Cs"]], [float(g) for g in s["gammas"]]
        lo, hi = 0.75, float(cv.max())
        cells = VGroup()
        W = 1.15
        for i, C_ in enumerate(Cs):
            for j, g_ in enumerate(gs):
                v = float(cv[i, j])
                t = float(np.clip((v - lo) / (hi - lo), 0, 1))
                sq = Square(W, stroke_color=GREY_D, stroke_width=1.5, fill_color=GOLD, fill_opacity=0.08 + 0.8 * t)
                sq.move_to([-3.6 + j * W, 1.7 - i * W, 0])
                txt = MathTex(rf"{100 * v:.1f}", font_size=24, color=WHITE if t < 0.6 else BLACK).move_to(sq)
                cells.add(VGroup(sq, txt))
        bi, bj = np.unravel_index(int(np.argmax(cv)), cv.shape)
        box = SurroundingRectangle(cells[bi * len(gs) + bj], color=WHITE, buff=0.0, stroke_width=4)
        rows = VGroup(*[MathTex(rf"C = {c:g}", font_size=24, color=GREY_A).next_to(cells[i * len(gs)], LEFT, buff=0.2)
                        for i, c in enumerate(Cs)])
        cols = VGroup(*[MathTex(rf"\gamma = {g:g}", font_size=24, color=GREY_A).next_to(cells[j], UP, buff=0.15)
                        for j, g in enumerate(gs)])
        head = label(r"Ten-fold cross-validation over $C$ and the kernel width $\gamma$: \ accuracy, \%", font_size=28).to_edge(UP, buff=0.3)
        near = int((cv >= cv.max() - 0.01).sum())
        worst = float(cv.min())
        notes = VGroup(label(rf"best: \ ${100 * cv.max():.1f}\%$", font_size=26, color=GOLD),
                       label(rf"${near}$ of ${cv.size}$ settings within a point of it", font_size=24, color=WHITE),
                       label(rf"worst: \ ${100 * worst:.1f}\%$ \ (tiny $C$)", font_size=24, color=BAD)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, 0.6, 0])
        keep_in_frame(notes)
        with self.voiceover(
            f"Where did C and gamma come from? A grid: {len(Cs)} prices times {len(gs)} kernel widths, each pair "
            "scored by "
            f"ten-fold cross-validation on the training pages. <bookmark mark='a'/> The best pair averages "
            f"{100 * cv.max():.1f} percent, but {near} of the {cv.size} settings are within a point of it. "
            f"<bookmark mark='b'/> Only a tiny C, a street so cheap to stand in that the boundary barely bends, "
            f"falls to {100 * worst:.0f} percent. On two numbers per page, the method matters less than the data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows), FadeIn(cols))
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(box), FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
