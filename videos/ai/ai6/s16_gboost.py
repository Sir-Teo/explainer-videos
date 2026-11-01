from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import (BAD, GOOD, HIST, HL, chapter, load, page_dots, page_plane, plot, regions)

SECOND, FIRST = C.REWARD, C.MODEL_Q


def _run_time_before(vo, mark, frame_rate, preferred=1.2):
    """Leave two frames before a cue; zero requests a crisp snapshot instead.

    An already-passed cue cannot be recovered by this scheduling fallback.
    """
    if not (math.isfinite(frame_rate) and frame_rate > 0 and math.isfinite(preferred) and preferred > 0):
        raise ValueError("Positive finite frame rate and duration required")
    available = vo.mark_time(mark) - vo.elapsed()
    if not math.isfinite(available):
        raise ValueError("Finite relative bookmark budget required")
    budget = min(preferred, available - 2 / frame_rate)
    return budget if budget >= 1 / frame_rate else 0.0


class GradientBoosting(VoiceoverScene):
    def construct(self):
        chapter(self, 15, r"Gradient boosting, second order", r"How does XGBoost choose a split?",
                "Chapter fifteen. Gradient boosting.", lit=(2001,))
        self.derive()
        self.check()
        self.plane()
        self.curves()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"g_i": FIRST, r"h_i": SECOND, r"G_j": FIRST, r"H_j": SECOND, r"G_L": FIRST, r"G_R": FIRST,
                  r"H_L": SECOND, r"H_R": SECOND, r"\lambda": HL}
        rows = [
            cmath(r"\sum_i \ell(y_i, F_i + f_i) + \Omega(f)", r"\;\approx\;",
                  r"\sum_i \big[\ell_i + g_i f_i + \tfrac12 h_i f_i^2\big] + \gamma T + \tfrac12\lambda\sum_j w_j^2",
                  font_size=30, colors=colors),
            cmath(r"\text{obj}", "=", r"\sum_j \big[G_j w_j + \tfrac12 (H_j + \lambda)\, w_j^2\big] + \gamma T",
                  font_size=30, colors=colors),
            cmath(r"w_j^*", "=", r"-\frac{G_j}{H_j + \lambda}, \qquad \text{obj}^* = -\tfrac12\sum_j \frac{G_j^2}{H_j + \lambda} + \gamma T",
                  font_size=30, colors=colors),
            cmath(r"\text{gain}", "=", r"\tfrac12\Big[\frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - "
                  r"\frac{(G_L + G_R)^2}{H_L + H_R + \lambda}\Big] - \gamma", font_size=30, colors=colors),
        ]
        whys = [why(r"Taylor, to second order; \\ $g_i = p_i - y_i$, \ $h_i = p_i(1 - p_i)$", font_size=20),
                why(r"a tree: \ one weight $w_j$ per leaf", font_size=20),
                why(r"each leaf: \ a parabola's bottom", font_size=20),
                why(r"split one leaf in two", font_size=20)]
        step = ladder(self, rows, whys, keep=4, top=2.3, x=-1.6, buff=0.4, edge=6.8)
        head = cmath(r"F_{m+1}(\mathbf{x})", "=", r"F_m(\mathbf{x}) + \eta\, f_m(\mathbf{x})", font_size=34).to_edge(UP, buff=0.3)
        hn = label(r"$f_m$: \ a small tree that walks downhill on the loss", font_size=22, color=GREY_A).next_to(head, DOWN, buff=0.1)
        cite_ = note(r"J.~Friedman (2001); \ T.~Chen \& C.~Guestrin, \textit{XGBoost} (2016)").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Friedman saw, in 2001, that boosting is gradient descent, taken in the space of functions: each new tree "
            "is a small step downhill on the loss. XGBoost, in 2016, took the step to second order. "
            "<bookmark mark='a'/> Expand the loss around the current model: each page contributes its gradient g, "
            "prediction minus truth, and its curvature h, p times one minus p, plus a price on leaves and their weights. "
            "<bookmark mark='b'/> A tree gives every page in a leaf the same weight, so the sums collect leaf by leaf. "
            "<bookmark mark='c'/> Each leaf is a parabola in its weight: its best weight is minus G over H plus "
            "lambda, a Newton step. <bookmark mark='d'/> And a split's gain is how much those parabolas' bottoms "
            "drop when one leaf becomes two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hn), FadeIn(cite_))
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=HL, scale_factor=1.04))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        x = load("xgb")
        GL, GR = x["check_G"]
        HLs, HRs = x["check_H"]
        lam = float(x["lam"])
        gain, direct, true = x["check_gain"], x["check_direct"], x["check_true"]
        w = x["check_word"]
        tree = VGroup()
        root = VGroup(RoundedRectangle(width=3.4, height=0.7, corner_radius=0.12, stroke_color=GREY_B, fill_color="#121722",
                                       fill_opacity=1),
                      label(rf"``{w}'' $\le {x['check_thr']:g}$?", font_size=26)).move_to([-3.4, 2.0, 0])
        root[1].move_to(root[0])
        leafs = VGroup()
        for k, (G, H, side) in enumerate(((GL, HLs, r"yes"), (GR, HRs, r"no"))):
            b = VGroup(RoundedRectangle(width=3.0, height=1.3, corner_radius=0.12, stroke_color=HL, fill_color="#121722",
                                        fill_opacity=1),
                       VGroup(MathTex(rf"G = {G:.1f}", font_size=30, color=FIRST), MathTex(rf"H = {H:.1f}", font_size=30,
                                                                                          color=SECOND)).arrange(DOWN, buff=0.12))
            b[1].move_to(b[0])
            b.move_to([-5.1 + 3.4 * k, -0.2, 0])
            e = Line(root.get_bottom(), b.get_top(), color=GREY_C, stroke_width=2)
            leafs.add(VGroup(e, b, label(side, font_size=20, color=GREY_B).next_to(e.get_center(), LEFT if k == 0 else RIGHT, buff=0.1)))
        tree.add(root, leafs)
        start = label(r"round one: \ every page at $p = \tfrac12$, \ so $g = \pm\tfrac12$, \ $h = \tfrac14$", font_size=22,
                      color=GREY_A).to_edge(UP, buff=0.3)
        res = VGroup(
            label(rf"the gain formula: \ ${gain:.3f}$", font_size=28, color=HL),
            label(rf"the objective, evaluated leaf by leaf: \ ${direct:.3f}$", font_size=28, color=GOOD),
            label(rf"the true drop in log loss: \ ${true:.2f}$ \ (nats, summed)", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, 0.6, 0])
        same = abs(gain - direct) < 1e-6 * max(1.0, abs(gain))
        under = true > gain
        agree_s = "the same, to every digit shown." if same else f"{direct:.3f}."
        under_s = ("the second-order picture is a cautious approximation here, and the real loss falls further."
                   if under else "the second-order picture slightly overestimates it.")
        with self.voiceover(
            "Check the formula on the pages. In round one every page sits at probability a half. The best first "
            f"question is: does the page use '{w}' at most {x['check_thr']:g} times? <bookmark mark='a'/> Sum the "
            "gradients and curvatures on each side. <bookmark mark='b'/> The gain formula gives "
            f"{gain:.3f}; evaluating the second-order objective leaf by leaf gives {agree_s} <bookmark mark='c'/> "
            f"The true drop in the loss is {true:.1f}: {under_s}"
        ) as vo:
            self.play(FadeIn(start), FadeIn(root))
            self.play(LaggedStart(*[FadeIn(l_[0]) for l_ in leafs], *[FadeIn(l_[2]) for l_ in leafs], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_[1]) for l_ in leafs], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plane(self):
        x = load("xgb")
        p = load("pages")
        X2, y, test = np.asarray(p["X2"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
        snaps = [int(k) for k in x["snaps"]]
        acc, tl = np.asarray(x["test_acc_2"]), np.asarray(x["train_loss_2"])
        n = len(acc)
        plane = page_plane(x_length=6.6, y_length=4.6, center=[-3.4, -0.4, 0])
        ax = plane[0]
        tr = np.nonzero(~test)[0]
        dots = page_dots(ax, X2, y, idx=tr, jitter=0.35, radius=0.04, opacity=0.9)
        dots.set_z_index(2)
        imgs = {k: regions(ax, x[f"region{k}"], x["xs"], x["ys"], lo=0.2, hi=0.8, opacity=0.5) for k in snaps}
        r = ValueTracker(1)
        cur = lambda: min(n, max(1, int(round(r.get_value()))))  # noqa: E731
        cnt = always_redraw(lambda: MathTex(rf"\text{{round }} {cur()}", font_size=36, color=HL).move_to([3.6, 2.2, 0]))
        tv = DecimalNumber(tl[0], num_decimal_places=3, font_size=28, color=GREY_A)
        av = DecimalNumber(100 * acc[0], num_decimal_places=1, unit=r"\%", font_size=28, color=HL)
        tv.add_updater(lambda m: m.set_value(tl[cur() - 1]))
        av.add_updater(lambda m: m.set_value(100 * acc[cur() - 1]))
        reads = VGroup(VGroup(label(r"training loss, \ bits:", font_size=24, color=GREY_A), tv).arrange(RIGHT, buff=0.15),
                       VGroup(label(r"held-out pages right:", font_size=24, color=HL), av).arrange(RIGHT, buff=0.15))
        reads.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(cnt, DOWN, buff=0.3)
        keep_in_frame(reads)
        mini = plot([0, math.log10(n), 1], [0.74, 0.86, 0.04], x_length=3.8, y_length=1.9, xticks=[0, 1, 2],
                    yticks=[0.74, 0.78, 0.82, 0.86], xfmt=lambda v: {0: "1", 1: "10", 2: "100"}[int(v)],
                    yfmt=lambda v: rf"{100 * v:.0f}\%", center=[4.0, -1.6, 0], xlabel=r"rounds", font_size=18)
        rr = np.arange(1, n + 1)

        def upto():
            m_ = cur()
            if m_ < 2:
                return VGroup()
            return VMobject(color=HL, stroke_width=3).set_points_as_corners(
                [mini.ax.c2p(math.log10(k), float(np.clip(v, 0.74, 0.86))) for k, v in zip(rr[:m_], acc[:m_])])

        mc = always_redraw(upto)
        best = int(np.argmax(acc)) + 1
        slips = acc[-1] < acc[best - 1] - 1e-9
        end = (f"By round {n} they've slipped to {100 * acc[-1]:.1f}: with only two numbers per page, the extra detail "
               "fits the training pages, not the authors. Stopping early is part of the method."
               if slips else "After that they stay there.")
        tag = note(rf"depth-${x['depth']}$ trees, \ $\eta = {x['eta']:g}$, \ $\lambda = {x['lam']:g}$").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Watch it learn on the two plotted rates. <bookmark mark='a'/> One tree: a few boxes. "
            "<bookmark mark='b'/> Ten, <bookmark mark='thirty'/>thirty: the boundary sharpens where the authors meet. <bookmark mark='c'/> "
            f"The training loss keeps falling, but the held-out pages are best after {best} rounds, at "
            f"{100 * acc[best - 1]:.1f} percent. <bookmark mark='d'/> {end}"
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), FadeIn(dots), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(imgs[1]), FadeIn(cnt), FadeIn(reads), FadeIn(mini))
            self.add(mc)
            self.bring_to_front(dots)
            shown = imgs[1]

            def show_round(k, run_time=0.0):
                nonlocal shown
                if run_time:
                    self.play(r.animate.set_value(k), FadeOut(shown), FadeIn(imgs[k]), run_time=run_time, rate_func=linear)
                else:
                    # A named snapshot arrives as one coherent state, without
                    # squeezing a boundary tween between two adjacent words.
                    r.set_value(k)
                    self.remove(shown)
                    self.add(imgs[k])
                    for m in (cnt, tv, av, mc):
                        m.update(0)
                self.bring_to_front(dots)
                shown = imgs[k]

            show_round(10, _run_time_before(vo, "b", float(config.frame_rate)))
            vo.wait_until("b")
            vo.wait_until("thirty")
            show_round(30)
            vo.wait_until("c")
            show_round(100, 1.2)
            vo.wait_until("d")
            show_round(n)
        for m in (cnt, tv, av, mc):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        x = load("xgb")
        s2, s1 = np.asarray(x["train_loss_70"]), np.asarray(x["first_loss_70"])
        a2, a1 = np.asarray(x["test_acc_70"]), np.asarray(x["first_acc_70"])
        n = len(s2)
        r = np.log10(np.arange(1, n + 1))
        g1 = plot([0, r[-1], 1], [-2.5, 0.1, 1], x_length=5.6, y_length=3.6, xticks=[0, 1, 2], yticks=[0, -1, -2],
                  xfmt=lambda v: {0: "1", 1: "10", 2: "100"}[int(v)], yfmt=lambda v: {0: "1", -1: "0.1", -2: "0.01"}[int(v)],
                  center=[-3.4, -0.4, 0], xlabel=r"rounds \ (all $70$ rates)", ylabel=r"training loss, \ bits per page")
        c2 = curve(g1.ax, r, np.log10(np.maximum(s2, 10 ** -2.5)), SECOND, stroke_width=4)
        c1 = curve(g1.ax, r, np.log10(np.maximum(s1, 10 ** -2.5)), FIRST, stroke_width=4)
        g2 = plot([0, r[-1], 1], [0.85, 1.0, 0.05], x_length=5.0, y_length=3.6, xticks=[0, 1, 2], yticks=[0.85, 0.9, 0.95, 1.0],
                  xfmt=lambda v: {0: "1", 1: "10", 2: "100"}[int(v)], yfmt=lambda v: rf"{100 * v:.0f}\%",
                  center=[3.5, -0.4, 0], xlabel=r"rounds", ylabel=r"held-out pages right")
        d2 = curve(g2.ax, r, np.clip(a2, 0.85, 1), SECOND, stroke_width=4)
        d1 = curve(g2.ax, r, np.clip(a1, 0.85, 1), FIRST, stroke_width=4)
        key = VGroup(label(r"second order: \ leaf $= -G/(H + \lambda)$", font_size=22, color=SECOND),
                     label(r"first order: \ leaf $=$ mean of $-g$", font_size=22, color=FIRST)).arrange(RIGHT, buff=0.6)
        key.to_edge(UP, buff=0.35)
        ahead = s2[-1] < s1[-1]
        first = (f"The Newton leaves drive the training loss down much faster: {s2[-1]:.4f} bits after {n} rounds, "
                 f"against {s1[-1]:.4f} for the plain gradient." if ahead else
                 f"Here the plain gradient keeps up: {s1[-1]:.4f} bits against {s2[-1]:.4f}.")
        with self.voiceover(
            "On all seventy rates, compare the two kinds of step with the same trees and the same learning rate. "
            f"<bookmark mark='a'/> {first} <bookmark mark='b'/> On the held-out pages, the second-order booster reaches {100 * a2[-1]:.1f} percent, "
            f"the first-order one {100 * a1[-1]:.1f}."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(d1), Create(d2), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
