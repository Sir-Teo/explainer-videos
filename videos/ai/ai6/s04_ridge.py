from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import HIST, HL, chapter, load, plot

RIDGE = "#7FD3FF"
SIGC = C.BITS  # singular values
SIGNAL = C.TRUE_P


class Ridge(VoiceoverScene):
    def construct(self):
        chapter(self, 3, r"Ridge: shrinking the weak directions", r"How do you stop a model leaning on noise?",
                "Chapter three. Ridge regression.")
        self.derive()
        self.shrink()
        self.paths()
        self.validate()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\lambda": RIDGE, r"\frac{d_j^2}{d_j^2 + \lambda}": RIDGE}
        rows = [
            cmath(r"\min_{\mathbf{w}}", r"\;\|\mathbf{y} - Z\mathbf{w}\|^2 + \lambda\|\mathbf{w}\|^2", font_size=36,
                  colors=colors),
            cmath(r"(Z^{\top}Z + \lambda I)\,\mathbf{w}", "=", r"Z^{\top}\mathbf{y}", font_size=36, colors=colors),
            cmath(r"\mathbf{w}", "=", r"V\,(D^2 + \lambda I)^{-1} D\, U^{\top}\mathbf{y}", font_size=36, colors=colors),
            cmath(r"Z\mathbf{w}", "=", r"\sum_j \mathbf{u}_j", r"\frac{d_j^2}{d_j^2 + \lambda}", r"\,(\mathbf{u}_j^{\top}\mathbf{y})",
                  font_size=36, colors=colors),
        ]
        whys = [why(r"fit, \ plus a price on size"), why(r"gradient $= 0$; \ always invertible"),
                why(r"$Z = UDV^{\top}$ \ (Part 3)"), why(r"the fit, \\ direction by direction")]
        rows[0].shift(RIGHT * 0)
        step = ladder(self, rows, whys, keep=4, top=1.3, x=-0.9, buff=0.42, align_index=1, edge=6.8)
        hist = history_card(1970, r"Hoerl \& Kennard", r"ridge regression, \ for chemical-plant data whose "
                            r"columns nearly repeated", color=HIST, width=5.2).to_corner(UL, buff=0.3)
        ls = label(r"least squares: \ every factor is $1$", font_size=26, color=GREY_A)
        rd = label(r"ridge: \ weak directions shrink most", font_size=26, color=RIDGE)
        tail = VGroup(ls, rd).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.4)
        with self.voiceover(
            "Seventy weights can lean on accidents of the training pages. Ridge regression puts a price on their "
            "size: the squared error, plus lambda times the squared length of the weights. <bookmark mark='a'/> Set "
            "the gradient to zero. Adding lambda to the diagonal makes the matrix invertible, always: that's how Hoerl "
            "and Kennard rescued nearly repeating columns in 1970. <bookmark mark='b'/> Now use the singular value "
            "decomposition from Part 3. <bookmark mark='c'/> The fit is a sum over directions in the data: each "
            "direction's share of the target, times a factor, d squared over d squared plus lambda. "
            "<bookmark mark='d'/> Least squares keeps every direction whole. Ridge shrinks each one, and the weak "
            "directions, with small singular values, shrink the most."
        ) as vo:
            self.play(FadeIn(hist, shift=DOWN * 0.2))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeOut(hist), FadeIn(tail))
            self.play(Indicate(rows[3][3], color=RIDGE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shrink(self):
        r = load("ridge")
        d = np.asarray(r["d"])
        uy = np.abs(np.asarray(r["uy"]))
        n = len(d)
        top = plot([0, n + 1, 10], [0, float(d.max()) * 1.1, 20], x_length=9.0, y_length=1.9, yticks=[0, 20, 40, 60],
                   center=[-0.6, 2.0, 0], ylabel=r"singular value $d_j$ \ (how much the pages vary that way)")
        mid = plot([0, n + 1, 10], [0, float(uy.max()) * 1.1, 2], x_length=9.0, y_length=1.3, yticks=[0, 4, 8],
                   center=[-0.6, -0.3, 0], ylabel=r"$|\mathbf{u}_j^{\top}\mathbf{y}|$ \ (how much of the authorship lies that way)")
        bot = plot([0, n + 1, 10], [0, 1, 0.5], x_length=9.0, y_length=1.3, yticks=[0, 0.5, 1], xticks=[1, 10, 20, 30, 40, 50, 60, 70],
                   center=[-0.6, -2.6, 0], ylabel=r"the factor $d_j^2/(d_j^2 + \lambda)$")
        W = 9.0 / (n + 1) * 0.7

        def bars(ax, vals, col, op=0.85):
            g = VGroup()
            for j, v in enumerate(vals, 1):
                p0, p1 = ax.c2p(j, 0), ax.c2p(j, v)
                g.add(Rectangle(width=W, height=max(p1[1] - p0[1], 0.004), stroke_width=0, fill_color=col,
                                fill_opacity=op).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
            return g

        bd, bu = bars(top.ax, d, SIGC), bars(mid.ax, uy, SIGNAL)
        loglam = ValueTracker(0.0)
        fac = always_redraw(lambda: bars(bot.ax, d ** 2 / (d ** 2 + 10 ** loglam.get_value()), RIDGE))
        lam_r = always_redraw(lambda: VGroup(
            MathTex(rf"\lambda = {10 ** loglam.get_value():,.0f}".replace(",", "{,}"), font_size=32, color=RIDGE),
            MathTex(rf"\text{{effective weights}} = {float((d ** 2 / (d ** 2 + 10 ** loglam.get_value())).sum()):.1f}",
                    font_size=28, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.3).shift(DOWN * 0.45))
        share = float((uy[:2] ** 2).sum() / (uy ** 2).sum())
        n_tr = int((~np.asarray(load("pages")["test"], bool)).sum())
        tag = note(rf"the ${n_tr}$ training pages, \ $70$ standardized rates").to_corner(UR, buff=0.2)
        f30 = float(d[-1] ** 2 / (d[-1] ** 2 + 30))
        f1k_hi, f1k_lo = float(d[0] ** 2 / (d[0] ** 2 + 1000)), float(d[-1] ** 2 / (d[-1] ** 2 + 1000))
        with self.voiceover(
            "Here are the seventy directions of the training pages, from the widest to the thinnest. "
            "<bookmark mark='a'/> Below, how much of the authorship lies along each: "
            f"{100 * share:.0f} percent of it along the first two. <bookmark mark='b'/> Now raise lambda. At one, "
            f"nothing much shrinks. At thirty, the thinnest direction keeps {100 * f30:.0f} percent. "
            f"<bookmark mark='c'/> At a thousand, the widest keeps {100 * f1k_hi:.0f} percent and the thinnest "
            f"{100 * f1k_lo:.0f}. The sum of the factors counts how many weights are effectively still free."
        ) as vo:
            self.play(FadeIn(top), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bd], lag_ratio=0.02), FadeIn(tag),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(mid), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bu], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bot), FadeIn(fac), FadeIn(lam_r))
            self.play(loglam.animate.set_value(math.log10(30)), run_time=3.0)
            vo.wait_until("c")
            self.play(loglam.animate.set_value(3.0), run_time=3.0)
        fac.clear_updaters()
        lam_r.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paths(self):
        r = load("ridge")
        p = load("pages")
        vocab = p["vocab"]
        lams = np.asarray(r["lams"])
        coef = np.asarray(r["coef"])
        lx = np.log10(lams)
        top = float(np.abs(coef).max()) * 1.05
        g = plot([-lx[-1], -lx[0], 1], [-top, top, 0.05], x_length=6.8, y_length=4.6, xticks=[-5, -3, -1, 1],
                 xfmt=lambda v: f"10^{{{int(round(-v))}}}", center=[-2.8, -0.4, 0],
                 xlabel=r"$\lambda$, \ weaker $\longrightarrow$", ylabel=r"the $70$ weights")
        ax2 = g.ax
        big = np.argsort(-np.abs(coef[0]))[:4]
        lines = VGroup()
        for j in range(coef.shape[1]):
            hot = j in big
            lines.add(VMobject(color=RIDGE if hot else GREY_D, stroke_width=3 if hot else 1.2).set_points_as_corners(
                [ax2.c2p(-a, b) for a, b in zip(lx, coef[:, j])]))
        names = VGroup(*[data_text(vocab[j], font="DejaVu Sans Mono", font_size=20, color=RIDGE)
                         .next_to(ax2.c2p(-lx[0], coef[0, j]), RIGHT, buff=0.08) for j in big])
        zeros = int((np.abs(coef) < 1e-12).sum())
        best = int(r["best"])
        mk = DashedLine(ax2.c2p(-lx[best], -top), ax2.c2p(-lx[best], top), color=HL, stroke_width=2)
        notes = VGroup(label(r"every weight shrinks smoothly", font_size=26, color=RIDGE),
                       label(rf"weights exactly zero, \ at any $\lambda$: \ ${zeros}$", font_size=24, color=GREY_A),
                       label(r"Bayes: \ ridge is the most probable \\ weights under a bell-shaped prior \\ (Part 5); "
                             r"\ in networks, \ weight decay", font_size=22, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        notes.move_to([4.5, 0.4, 0])
        if notes.get_left()[0] < 2.0:
            notes.scale_to_fit_width(6.8 - 2.0).move_to([4.4, 0.4, 0])
        say_zero = ("Not one weight ever reaches exactly zero." if zeros == 0 else
                    f"Only {zeros} weights ever reach exactly zero.")
        with self.voiceover(
            "Here is what ridge does to the seventy weights, from a strong penalty to almost none. "
            f"<bookmark mark='a'/> Every weight grows smoothly out of zero as lambda falls. {say_zero} "
            "<bookmark mark='b'/> Ridge has a second reading: it's the most probable set of weights if, before seeing "
            "any pages, you believed they were small, with a bell-shaped prior, as in Part 5. In neural networks the "
            "same penalty is called weight decay."
        ) as vo:
            self.play(FadeIn(g))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.01), run_time=2.5)
            self.play(FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]), Create(mk))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def validate(self):
        r = load("ridge")
        lams = np.asarray(r["lams"])
        mm, se = np.asarray(r["cv_mse"]), np.asarray(r["cv_mse_se"])
        lx = np.log10(lams)
        best = int(r["best"])
        lo_, hi_ = float((mm - se).min()), float(min((mm + se).max(), 0.26))
        g = plot([lx[0], lx[-1], 1], [0.0, 0.26, 0.05], x_length=6.6, y_length=4.0, xticks=[-1, 0, 1, 2, 3, 4, 5],
                 yticks=[0, 0.1, 0.2], xfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.6, -0.3, 0],
                 xlabel=r"$\lambda$", ylabel=r"squared error on held-out folds \ (ten folds)")
        ax = g.ax
        cl = np.clip
        bnd = band(ax, lx, cl(mm - se, 0, 0.26), cl(mm + se, 0, 0.26), RIDGE, opacity=0.25)
        cv = curve(ax, lx, cl(mm, 0, 0.26), RIDGE, stroke_width=3.5)
        mk = DashedLine(ax.c2p(lx[best], 0), ax.c2p(lx[best], 0.26), color=HL, stroke_width=2)
        ta = np.asarray(r["test_acc"])
        df_best = float(np.asarray(r["df"])[best])
        right = VGroup(
            label(rf"cross-validation picks $\lambda \approx {lams[best]:.0f}$", font_size=26, color=HL),
            label(rf"about ${df_best:.0f}$ effective weights of $70$", font_size=24, color=GREY_A),
            label(rf"held-out pages there: \ ${100 * ta[best]:.1f}\%$", font_size=24, color=GREY_A),
            label(rf"with almost no penalty: \ ${100 * ta[0]:.1f}\%$", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.7, 0.6, 0])
        link = label(r"shrink every direction (ridge) \ or drop the thin ones (Part 7's PCA); \ "
                     r"why a little bias pays: \ Part 8", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.25)
        folds = VGroup(*[Rectangle(width=0.42, height=0.42, stroke_color=GREY_B, stroke_width=1.5, fill_color=RIDGE,
                                   fill_opacity=0.25) for _ in range(10)]).arrange(RIGHT, buff=0.06)
        fold_l = label(r"the training pages, \ in ten folds", font_size=22, color=GREY_A)
        held = label(r"held back: \ measure the error", font_size=20, color=C.BITS)
        cvd = VGroup(fold_l, folds).arrange(DOWN, buff=0.18).move_to([3.7, 1.4, 0])
        held.next_to(folds, DOWN, buff=0.25)
        hl = SurroundingRectangle(folds[0], color=C.BITS, buff=0.04, stroke_width=3)
        flat = ta[best] >= ta[0] - 1e-9
        say = ("which costs nothing on the held-out pages" if flat else
               f"which costs a page or so on the held-out pages, {100 * ta[best]:.1f} percent against {100 * ta[0]:.1f}")
        with self.voiceover(
            "Which lambda? Hold some pages back, fit on the rest, and measure the error on the held-back ones; "
            "do that ten times, each time with a different tenth held back: ten-fold cross-validation. "
            f"<bookmark mark='a'/> The error is lowest near lambda {lams[best]:.0f}, about {df_best:.0f} effective "
            f"weights instead of seventy, {say}. <bookmark mark='b'/> These pages are easy to tell apart, so the "
            "penalty barely matters for accuracy; it matters when there are more words than pages. Ridge keeps every "
            "word, only smaller. The next chapter's penalty throws words away."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cvd))
            self.play(Create(hl), FadeIn(held), folds[0].animate.set_fill(C.BITS, 0.7))
            for k in range(1, 10):
                self.play(hl.animate.move_to(folds[k]), folds[k - 1].animate.set_fill(RIDGE, 0.25),
                          folds[k].animate.set_fill(C.BITS, 0.7), run_time=0.35)
            self.play(FadeIn(bnd), Create(cv), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeOut(VGroup(cvd, hl, held)))
            self.play(Create(mk), LaggedStart(*[FadeIn(r_) for r_ in right], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(link))
        self.wait(0.3)
        self.clear_scene()
