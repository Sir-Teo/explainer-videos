from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import AUSTEN, DICKENS, HL, MONO, chapter, load, plot, sci_tex

WSTAR = np.array([2.2, 0.5])  # the unpenalized best weights (illustrative)
H = np.array([[1.0, 0.3], [0.3, 1.6]])
RIDGE, LASSO, ENET = "#7FD3FF", C.BITS, C.REWARD


def loss(w):
    d = w - WSTAR
    return float(d @ H @ d)


def project_l2(w, r):
    n = np.linalg.norm(w)
    return w if n <= r else w * r / n


def project_l1(w, r):
    if np.abs(w).sum() <= r:
        return w
    u = np.sort(np.abs(w))[::-1]
    cs = np.cumsum(u)
    k = np.nonzero(u * np.arange(1, len(w) + 1) > (cs - r))[0][-1]
    th = (cs[k] - r) / (k + 1)
    return np.sign(w) * np.maximum(np.abs(w) - th, 0)


def constrained(r, proj):
    w = proj(WSTAR.copy(), r)
    for _ in range(400):
        w = proj(w - 0.25 * 2 * H @ (w - WSTAR), r)
    return w


def ellipse(level, ax, color=GREY_C, sw=1.5):
    vals, vecs = np.linalg.eigh(H)
    ts = np.linspace(0, 2 * math.pi, 80)
    pts = [WSTAR + vecs @ (np.sqrt(level / vals) * np.array([math.cos(t), math.sin(t)])) for t in ts]
    return VMobject(color=color, stroke_width=sw).set_points_smoothly([ax.c2p(*p) for p in pts])


class Lasso(VoiceoverScene):
    def construct(self):
        chapter(self, 4, r"The lasso: soft thresholds and a path", r"Can a penalty choose the words?",
                "Chapter four. The lasso.")
        self.shapes()
        self.soft()
        self.path()
        self.cvcurve()
        self.twins()

    # ------------------------------------------------------------------
    def panel(self, center, proj, color, shape_fn, title):
        ax = Axes(x_range=[-1.5, 3, 1], y_range=[-1.5, 2.5, 1], x_length=5.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(center)
        conts = VGroup(*[ellipse(c, ax) for c in (0.15, 0.6, 1.4, 2.6, 4.2)])
        star = Dot(ax.c2p(*WSTAR), radius=0.07, color=WHITE)
        r = ValueTracker(1.8)
        region = always_redraw(lambda: shape_fn(ax, r.get_value(), color))

        def sol():
            w = constrained(r.get_value(), proj)
            return VGroup(ellipse(loss(w), ax, color=WHITE, sw=2.5), glow_dot(ax.c2p(*w), color=color, radius=0.09))

        touch = always_redraw(sol)
        names = VGroup(MathTex(r"w_1", font_size=28, color=GREY_A).next_to(ax.x_axis, RIGHT, buff=0.1),
                       MathTex(r"w_2", font_size=28, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1))
        t = label(title, font_size=28, color=color).next_to(ax, UP, buff=0.35)
        return ax, conts, star, r, region, touch, names, t

    def shapes(self):
        def circle(ax, r, color):
            u = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
            return Circle(radius=r * u, color=color, stroke_width=3, fill_color=color, fill_opacity=0.15).move_to(ax.c2p(0, 0))

        def diamond(ax, r, color):
            return Polygon(ax.c2p(r, 0), ax.c2p(0, r), ax.c2p(-r, 0), ax.c2p(0, -r), color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.15)

        L = self.panel([-3.4, -0.6, 0], project_l2, RIDGE, circle, r"ridge: \ $w_1^2 + w_2^2 \le t^2$")
        R = self.panel([3.4, -0.6, 0], project_l1, LASSO, diamond, r"lasso: \ $|w_1| + |w_2| \le t$")
        tag = label(r"illustrative: \ two weights, \ the loss's contour lines", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.2)
        head = label(r"Keep the weights in a budget", font_size=34).to_edge(UP, buff=0.3)
        w_end = constrained(0.9, project_l1)
        assert abs(w_end[1]) < 1e-9 < abs(w_end[0])  # the diamond's corner: w2 exactly zero
        zero = label(r"$w_2 = 0$ \ exactly", font_size=28, color=LASSO).next_to(R[0].c2p(0.9, 0), DR, buff=0.6)
        with self.voiceover(
            "A penalty is a budget. <bookmark mark='a'/> Here are two weights, and the contour lines of the loss, "
            "whose lowest point is out here. <bookmark mark='b'/> Ridge's budget on the squared length is a circle. "
            "Tibshirani's lasso, in 1996, budgets the sum of absolute values: a diamond. The answer is where the lowest "
            "contour just touches the shape. <bookmark mark='c'/> Shrink the budget. The circle's answer slides "
            "smoothly toward zero. The diamond's catches on a corner, where one weight is exactly zero."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for P in (L, R):
                ax, conts, star, r, region, touch, names, t = P
                self.play(Create(ax), FadeIn(names), Create(conts), FadeIn(star), FadeIn(tag), run_time=1.0)
            vo.wait_until("b")
            for P in (L, R):
                ax, conts, star, r, region, touch, names, t = P
                self.play(FadeIn(t), FadeIn(region), FadeIn(touch))
            vo.wait_until("c")
            self.play(L[3].animate.set_value(0.9), R[3].animate.set_value(0.9), run_time=4.0)
            self.play(FadeIn(zero), Indicate(R[5], color=LASSO))
        for P in (L, R):
            P[4].clear_updaters()
            P[5].clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def soft(self):
        colors = {r"\lambda": LASSO, r"S_\lambda(z)": LASSO}
        rows = [
            cmath(r"\min_w", r"\;\tfrac12 (z - w)^2 + \lambda |w|", font_size=36, colors=colors),
            cmath(r"0", r"\in", r"w - z + \lambda\,\partial|w|", font_size=36, colors=colors),
            cmath(r"w", "=", r"S_\lambda(z)", r"= \operatorname{sign}(z)\,\max(|z| - \lambda,\, 0)", font_size=36,
                  colors=colors),
        ]
        whys = [why(r"one weight, \\ the others held fixed"), why(r"$\partial|w| = \operatorname{sign} w$, \\ "
                                                                    r"or all of $[-1, 1]$ at $0$"),
                why(r"the soft threshold")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-3.0, buff=0.45, align_index=1, edge=6.8)
        g = plot([-3, 3, 1], [-2.2, 2.2, 1], x_length=4.6, y_length=3.4, xticks=[-2, 0, 2], yticks=[-2, 0, 2],
                 center=[3.8, -1.75, 0], xlabel=r"$z$: \ the least-squares value", ylabel=r"$w$")
        ax = g.ax
        lam = 1.0
        ident = DashedLine(ax.c2p(-2.2, -2.2), ax.c2p(2.2, 2.2), color=GREY_B, stroke_width=2)
        st = VMobject(color=LASSO, stroke_width=4).set_points_as_corners(
            [ax.c2p(-3, -2), ax.c2p(-lam, 0), ax.c2p(lam, 0), ax.c2p(3, 2)])
        zone = Rectangle(width=ax.c2p(lam, 0)[0] - ax.c2p(-lam, 0)[0], height=0.2, stroke_width=0, fill_color=LASSO,
                         fill_opacity=0.25).move_to(ax.c2p(0, 0))
        zl = label(r"$|z| \le \lambda$: \ exactly $0$", font_size=22, color=LASSO).next_to(zone, DOWN, buff=0.35)
        cd = VGroup(label(r"coordinate descent:", font_size=26, color=WHITE),
                    label(r"visit each word in turn; \ set its weight \\ to the soft threshold of what it would \\ "
                          r"explain alone; \ repeat until nothing moves", font_size=22, color=GREY_A))
        cd.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.3, -1.8, 0])
        cite_ = cite(r"Friedman, Hastie \& Tibshirani, \textit{glmnet} (2010)", corner=DL)
        with self.voiceover(
            "How is it solved? One weight at a time. <bookmark mark='a'/> Hold the others fixed, and one weight "
            "faces a parabola plus lambda times its absolute value. <bookmark mark='b'/> The absolute value has a "
            "corner at zero, where its slope can be anything between minus one and one. <bookmark mark='c'/> So the "
            "answer is the soft threshold: slide the least-squares value toward zero by lambda, and stop at zero. "
            "<bookmark mark='d'/> Any value inside the band gives exactly zero. Visit the words in turn, "
            "thresholding each, until nothing moves: coordinate descent, the way glmnet computes it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(g), Create(ident))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(Create(st))
            vo.wait_until("d")
            self.play(FadeIn(zone), FadeIn(zl))
            self.play(FadeIn(cd), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def path(self):
        d = load("lasso")
        p = load("pages")
        vocab = p["vocab"]
        path = np.asarray(d["path"])
        order = d["order"]
        k8, words8 = int(d["k8"]), d["words8"]
        n = len(path)
        top = float(np.abs(path).max()) * 1.05
        ax = Axes(x_range=[0, n - 1, 5], y_range=[-top, top, 1], x_length=8.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.0, -0.5, 0])
        xl = label(r"the penalty relaxes $\longrightarrow$", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        first8 = order[:8]
        lines, named = VGroup(), {}
        for j, w in enumerate(vocab):
            ys = path[:, j]
            if not np.any(ys):
                continue
            hot = w in first8
            col = (DICKENS if ys[-1] > 0 else AUSTEN) if hot else GREY_D
            ln = VMobject(color=col, stroke_width=3 if hot else 1.5).set_points_as_corners(
                [ax.c2p(k, v) for k, v in enumerate(ys)])
            lines.add(ln)
            if hot:
                named[w] = ln
        tags = VGroup()
        for w, ln in named.items():
            tags.add(data_text(w, font=MONO, font_size=20, color=ln.get_color()).next_to(ln.get_end(), RIGHT, buff=0.08))
        tags = VGroup(*sorted(tags, key=lambda m: m.get_y()))
        for a, b in zip(tags[:-1], tags[1:]):
            if b.get_y() - a.get_y() < 0.28:
                b.set_y(a.get_y() + 0.28)
        first = label(r"first to come alive: \ " + ", \\ ".join(rf"\texttt{{{w}}}" for w in first8), font_size=24,
                      color=C.BITS).to_edge(UP, buff=0.3)
        sign = VGroup(label(r"above zero: \ Dickens", font_size=22, color=DICKENS),
                      label(r"below zero: \ Austen", font_size=22, color=AUSTEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        sign.to_corner(UR, buff=0.4).shift(DOWN * 0.75)
        acc = np.asarray(d["test_acc"])
        nnz = np.asarray(d["nnz"])
        u = ValueTracker(0)
        cur = lambda: min(n - 1, int(u.get_value() + 1e-6))  # noqa: E731
        cursor = always_redraw(lambda: Line(ax.c2p(u.get_value(), -top), ax.c2p(u.get_value(), top), color=GREY_B,
                                            stroke_width=1.5, stroke_opacity=0.7))
        nw = Integer(int(nnz[0]), font_size=30, color=C.BITS)
        nw.add_updater(lambda m: m.set_value(int(nnz[cur()])))
        av = DecimalNumber(100 * acc[0], num_decimal_places=0, unit=r"\%", font_size=30, color=WHITE)
        av.add_updater(lambda m: m.set_value(100 * acc[cur()]))
        live = VGroup(VGroup(label(r"words in use:", font_size=24, color=C.BITS), nw).arrange(RIGHT, buff=0.15),
                      VGroup(label(r"held-out pages right:", font_size=24, color=GREY_A), av).arrange(RIGHT, buff=0.15))
        live.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(sign, DOWN, buff=0.35).align_to(sign, LEFT)
        keep_in_frame(live)
        mark = DashedLine(ax.c2p(k8, -top), ax.c2p(k8, top), color=WHITE, stroke_width=2)
        ml = label(rf"${len(words8)}$ words: \ ${100 * d['acc8']:.0f}\%$", font_size=24, color=WHITE).next_to(mark, UP, buff=0.08)
        k1 = int(d["one_se"])
        cvl = label(rf"cross-validation, \\ one-standard-error rule: \\ ${d['n_selected']}$ words, \ "
                    rf"${100 * d['acc_one_se']:.1f}\%$", font_size=22, color=GREY_A).next_to(live, DOWN, buff=0.3).align_to(live, LEFT)
        keep_in_frame(cvl)
        kkt = note(rf"KKT conditions checked at every penalty: \ worst violation ${sci_tex(d['kkt'])}$").to_corner(DR, buff=0.2)
        names_say = ", ".join(f"'{w}'" for w in first8[:-1]) + f" and '{first8[-1]}'"
        with self.voiceover(
            "Here's the whole path on the pages: all seventy weights, computed by coordinate descent at "
            f"{n} penalties, from total to gentle. <bookmark mark='a'/> The first words to come alive are {names_say}. "
            f"<bookmark mark='b'/> With just those {len(words8)}, the classifier gets {100 * d['acc8']:.0f} percent of "
            "the held-out pages right. <bookmark mark='c'/> Cross-validation, choosing the sparsest model within "
            f"one standard error of the best, keeps {d['n_selected']} words and gets {100 * d['acc_one_se']:.1f} percent."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(sign), FadeIn(live), FadeIn(kkt))
            self.add(cursor)
            self.play(*[Create(l_) for l_ in lines], u.animate.set_value(n - 1), run_time=4.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(first), LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(u.animate.set_value(k8), run_time=1.0)
            self.play(Create(mark), FadeIn(ml))
            vo.wait_until("c")
            self.play(u.animate.set_value(k1), run_time=1.0)
            self.play(FadeIn(cvl))
        for m in (cursor, nw, av):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cvcurve(self):
        d = load("lasso")
        mm, se = np.asarray(d["cv_mse"]), np.asarray(d["cv_se"])
        nnz = np.asarray(d["nnz"])
        n = len(mm)
        top = float(min(mm.max(), 0.26)) * 1.05
        g = plot([0, n - 1, 10], [0, top, 0.05], x_length=7.4, y_length=4.2, yticks=[0, 0.1, 0.2],
                 center=[-2.2, -0.4, 0], xlabel=r"the penalty relaxes $\longrightarrow$",
                 ylabel=r"squared error on held-out folds \ (ten folds, $\pm 1$ s.e.)")
        ax = g.ax
        xs = np.arange(n)
        bnd = band(ax, xs, np.clip(mm - se, 0, top), np.clip(mm + se, 0, top), LASSO, opacity=0.25)
        cv = curve(ax, xs, np.clip(mm, 0, top), LASSO, stroke_width=3.5)
        b, o = int(d["best"]), int(d["one_se"])
        thr = DashedLine(ax.c2p(0, mm[b] + se[b]), ax.c2p(n - 1, mm[b] + se[b]), color=GREY_B, stroke_width=1.5)
        mb = DashedLine(ax.c2p(b, 0), ax.c2p(b, top), color=WHITE, stroke_width=2)
        mo = DashedLine(ax.c2p(o, 0), ax.c2p(o, top), color=HL, stroke_width=2.5)
        notes = VGroup(label(rf"lowest error: \ ${int(nnz[b])}$ words", font_size=26, color=WHITE),
                       label(r"the sparsest model within \\ one standard error of it:", font_size=24, color=GREY_A),
                       label(rf"${int(nnz[o])}$ words", font_size=30, color=HL)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        notes.move_to([4.5, 0.8, 0])
        keep_in_frame(notes)
        with self.voiceover(
            "How many words to keep? Cross-validate the whole path: for every penalty, fit on nine tenths of the "
            "training pages and score the tenth, ten times over. <bookmark mark='a'/> The error is lowest with "
            f"{int(nnz[b])} words. <bookmark mark='b'/> But the curve is nearly flat there, and its wobble, one "
            "standard error, is as large as the differences. The usual rule takes the sparsest model within one "
            f"standard error of the best: {int(nnz[o])} words."
        ) as vo:
            self.play(FadeIn(g))
            self.play(FadeIn(bnd), Create(cv), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(mb), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(thr), Create(mo), FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def twins(self):
        d = load("lasso")
        tl, te = np.abs(np.asarray(d["twin_lasso"])), np.abs(np.asarray(d["twin_enet"]))
        K = 18
        top = float(max(tl[:K].max(), te[:K].max())) * 1.15
        panels = []
        for k_, (arr, title, col) in enumerate(((tl, r"lasso", LASSO), (te, r"elastic net: \ half $|w|$, half $w^2$", ENET))):
            g = plot([0, K - 1, 5], [0, top, 0.05], x_length=5.4, y_length=3.2, center=[-3.4 + 6.8 * k_, -0.6, 0],
                     xlabel=r"the penalty relaxes $\longrightarrow$", ylabel=r"size of the weight")
            a = curve(g.ax, range(K), arr[:K, 0], col, stroke_width=4)
            b = DashedLine(g.ax.c2p(0, arr[0, 1]), g.ax.c2p(0, arr[0, 1]))  # placeholder, replaced below
            b = VMobject(color=WHITE, stroke_width=3).set_points_as_corners([g.ax.c2p(k, v) for k, v in enumerate(arr[:K, 1])])
            b.set_stroke(opacity=0.85)
            t = label(title, font_size=26, color=col).next_to(g, UP, buff=0.15)
            panels.append((g, a, b, t))
        key = VGroup(label(r"coloured: \ ``not''", font_size=22, color=GREY_A), label(r"white: \ its near-copy", font_size=22,
                                                                                         color=WHITE)).arrange(RIGHT, buff=0.5)
        key.to_edge(UP, buff=0.4)
        # the strongest penalty at which the lasso already uses "not" but not yet its copy
        ks = [k for k in range(K) if tl[k, 0] > 1e-6 and tl[k, 1] < 1e-9]
        k0 = ks[-1] if ks else 3
        share_e = float(min(te[k0]) / max(te[k0].sum(), 1e-12))
        note_ = note(rf"the copy: \ ``not'' plus a little noise, \ correlation ${d['twin_corr']:.3f}$").to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "One weakness. Give the lasso two nearly identical words: 'not', and a noisy copy of it. "
            "<bookmark mark='a'/> While the penalty is strong, it uses one twin and ignores the other, an arbitrary "
            "choice. <bookmark mark='b'/> Zou and Hastie's elastic net, in 2005, mixes in a little ridge, and shares "
            f"the weight: at the same penalty, the smaller twin carries {100 * share_e:.0f} percent of the pair's weight."
        ) as vo:
            self.play(FadeIn(key), FadeIn(note_), *[FadeIn(P_[0]) for P_ in panels], *[FadeIn(P_[3]) for P_ in panels])
            vo.wait_until("a")
            g, a, b, t = panels[0]
            self.play(Create(a), Create(b), run_time=1.5)
            vo.wait_until("b")
            g, a, b, t = panels[1]
            self.play(Create(a), Create(b), run_time=1.5)
            for g, a, b, t in panels:
                self.play(Create(DashedLine(g.ax.c2p(k0, 0), g.ax.c2p(k0, top), color=HL, stroke_width=2)), run_time=0.5)
        self.wait(0.3)
        self.clear_scene()
