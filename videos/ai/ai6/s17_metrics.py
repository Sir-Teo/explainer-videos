from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import AUSTEN, BAD, DICKENS, GOOD, HL, chapter, load, plot

ROCC, PRC = C.MODEL_Q, C.REWARD


class Metrics(VoiceoverScene):
    def construct(self):
        chapter(self, 16, r"Keeping score honestly", r"What does ``83\% right'' really tell you?",
                "Chapter sixteen. Keeping score.")
        self.roc()
        self.rare()
        self.wobble()

    # ------------------------------------------------------------------
    def roc(self):
        cal = load("calibration")
        m = load("metrics")
        p = load("pages")
        y = np.asarray(p["y"])
        s = np.asarray(cal["p_lr2"])
        g = plot([0, 1, 0.5], [0, 1, 0.5], x_length=4.6, y_length=4.6, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 center=[-3.6, -0.3, 0], xlabel=r"false-alarm rate \ (Austen pages called Dickens)",
                 ylabel=r"hit rate \ (Dickens pages found)")
        ax = g.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_B, stroke_width=1.5)
        order = np.sort(np.unique(s))[::-1]
        P, N = int(y.sum()), int((1 - y).sum())
        thr = ValueTracker(1.0)

        def counts(t):
            pred = s >= t
            return int((pred & (y == 1)).sum()), int((pred & (y == 0)).sum())

        def trace():
            t = thr.get_value()
            pts = [ax.c2p(0, 0)]
            for th in order:
                if th < t:
                    break
                tp, fp = counts(th)
                pts.append(ax.c2p(fp / N, tp / P))
            path = VMobject(color=ROCC, stroke_width=4)
            if len(pts) > 1:
                path.set_points_as_corners(pts)
            tp, fp = counts(t)
            return VGroup(path, Dot(ax.c2p(fp / N, tp / P), radius=0.08, color=WHITE))

        tr = always_redraw(trace)

        nums = [Integer(0, font_size=32, color=c_) for c_ in (GOOD, BAD, BAD, GOOD)]
        cells = VGroup(
            VectorizedPoint(), label(r"called Dickens", font_size=20, color=GREY_A), label(r"called Austen", font_size=20, color=GREY_A),
            label(r"Dickens", font_size=22, color=DICKENS), nums[0], nums[1],
            label(r"Austen", font_size=22, color=AUSTEN), nums[2], nums[3])
        for i, c_ in enumerate(cells):
            c_.move_to([2.0 + 1.9 * (i % 3), 1.9 - 0.7 * (i // 3), 0])

        def upd(i):
            def f(m):
                tp, fp = counts(thr.get_value())
                m.set_value([tp, P - tp, fp, N - fp][i])
            return f

        for i, n_ in enumerate(nums):
            n_.add_updater(upd(i))
        tv = DecimalNumber(1.0, num_decimal_places=2, font_size=30, color=WHITE)
        tv.add_updater(lambda m: m.set_value(thr.get_value()))
        tb = VGroup(VGroup(label(r"threshold", font_size=26, color=WHITE), tv).arrange(RIGHT, buff=0.2).move_to([3.9, 2.8, 0]),
                    cells)
        auc, mw = m["lr2"]["auc"], m["lr2"]["mw"]
        res = VGroup(label(rf"area under the curve: \ ${auc:.4f}$", font_size=26, color=ROCC),
                     label(rf"share of (Dickens, Austen) pairs ranked the right way: \ ${mw:.4f}$", font_size=22, color=HL),
                     label(rf"all $70$ rates: \ ${m['lr70']['auc']:.4f}$", font_size=22, color=GREY_A))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, -1.9, 0])
        tag = note(r"logistic regression on two rates, \ each page predicted once by ten-fold cross-validation").to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "A classifier gives a score; we chose to cut at a half. Every cut is a trade. <bookmark mark='a'/> Start "
            "strict, calling nothing Dickens. Lower the threshold: you find more of Dickens's pages, the hits, but "
            "start calling Austen's pages Dickens, the false alarms. <bookmark mark='b'/> The path traced out is the "
            "ROC curve, from radar operators in the Second World War. <bookmark mark='c'/> Its area has a beautiful "
            "meaning: the chance that a random Dickens page scores higher than a random Austen page. Count all "
            f"{P * N:,} pairs: {mw:.4f}, the area exactly."
        ) as vo:
            self.play(FadeIn(g), Create(diag), FadeIn(tag))
            self.add(tr, tb)
            vo.wait_until("a")
            self.play(thr.animate.set_value(0.75), run_time=2.5, rate_func=linear)
            vo.wait_until("b")
            self.play(thr.animate.set_value(0.0), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]), FadeIn(res[2]))
        tr.clear_updaters()
        for m_ in (*nums, tv):
            m_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rare(self):
        m = load("metrics")
        rr = m["rare"]
        roc_r, pr_r = np.asarray(m["roc_rare"]), np.asarray(m["pr_rare"])
        pr_b = np.asarray(m["pr_lr2"])
        g1 = plot([0, 1, 0.5], [0, 1, 0.5], x_length=4.2, y_length=3.6, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                  center=[-4.5, -0.6, 0], xlabel=r"false-alarm rate", ylabel=r"hit rate")
        g2 = plot([0, 1, 0.5], [0, 1, 0.5], x_length=4.2, y_length=3.6, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                  center=[0.2, -0.6, 0], xlabel=r"recall \ (Dickens pages found)", ylabel=r"precision \ (calls that are right)")
        c1 = VMobject(color=ROCC, stroke_width=4).set_points_as_corners([g1.ax.c2p(a, b) for a, b in roc_r])
        c2 = VMobject(color=PRC, stroke_width=4).set_points_as_corners([g2.ax.c2p(a, b) for a, b in pr_r])
        cb = VMobject(color=GREY_B, stroke_width=2.5).set_points_as_corners([g2.ax.c2p(a, b) for a, b in pr_b])
        t1 = label(r"ROC", font_size=26, color=ROCC).next_to(g1, UP, buff=0.1)
        t2 = label(r"precision--recall", font_size=26, color=PRC).next_to(g2, UP, buff=0.1)
        base = m["lr2"]["ap"]
        res = VGroup(
            label(rf"${rr['n_austen']}$ Austen pages, \ ${rr['n_dickens']}$ Dickens", font_size=24, color=WHITE),
            label(rf"``always Austen'': \ ${100 * rr['always_austen']:.0f}\%$ right", font_size=24, color=BAD),
            label(rf"ROC area: \ ${rr['auc']:.2f}$ \ (${rr['auc_lo']:.2f}$--${rr['auc_hi']:.2f}$)", font_size=22, color=ROCC),
            label(rf"average precision: \ ${rr['ap']:.2f}$ \ (${rr['ap_lo']:.2f}$--${rr['ap_hi']:.2f}$)", font_size=22, color=PRC),
            label(rf"balanced pages: \ ${base:.2f}$ \ (grey)", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        if res.width > 4.2:
            res.scale_to_fit_width(4.2)
        res.move_to([4.6, 0.4, 0])
        keep_in_frame(res)
        tag = note(r"$200$ random draws of the rare pages; \ ranges: \ $10$th--$90$th percentile").to_edge(DOWN, buff=0.12)
        drops = rr["ap"] < base - 0.1
        ap_s = (f"Average precision falls from {base:.2f} to {rr['ap']:.2f}: most alarms are now false."
                if drops else f"Average precision moves from {base:.2f} to {rr['ap']:.2f}.")
        with self.voiceover(
            "Now make Dickens rare, as fraud or disease usually is. Keep all of Austen's pages, and only "
            f"{rr['n_dickens']} of Dickens's. <bookmark mark='a'/> A rule that always says Austen is now "
            f"{100 * rr['always_austen']:.0f} percent accurate, and useless. <bookmark mark='b'/> The ROC curve "
            f"barely notices: its area is still about {rr['auc']:.2f}, because it measures each author's pages "
            "separately. <bookmark mark='c'/> Precision and recall ask what you care about: of the pages you call "
            f"Dickens, how many are? {ap_s}"
        ) as vo:
            self.play(FadeIn(res[0]), FadeIn(tag), FadeIn(g1), FadeIn(t1), FadeIn(g2), FadeIn(t2))
            vo.wait_until("a")
            self.play(FadeIn(res[1]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(res[2]))
            vo.wait_until("c")
            self.play(Create(cb), FadeIn(res[4]))
            self.play(Create(c2), FadeIn(res[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wobble(self):
        m = load("metrics")
        sa, ca, fa = np.asarray(m["split_acc"]), np.asarray(m["cv_acc"]), np.asarray(m["fold_acc"])
        lo, hi = 0.66, 1.12
        g = plot([lo, hi, 0.05], [0, 1, 1], x_length=12.4, y_length=4.2, xticks=[0.7, 0.75, 0.8, 0.85, 0.9],
                 xfmt=lambda v: rf"{100 * v:.0f}\%", center=[0, -0.6, 0], xlabel=r"accuracy of logistic regression "
                 r"on two rates, \ as measured")
        ax = g.ax
        bins = np.linspace(lo, 0.96, 61)

        def hist(v, col, y0, h):
            c_, _ = np.histogram(v, bins=bins)
            c_ = c_ / max(c_.max(), 1)
            out = VGroup()
            for a, b, k in zip(bins[:-1], bins[1:], c_):
                if k <= 0:
                    continue
                p0, p1 = ax.c2p(a, y0), ax.c2p(b, y0 + h * k)
                out.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                  fill_opacity=0.75).move_to((p0 + p1) / 2))
            return out

        h1 = hist(sa, ROCC, 0.0, 0.3)
        h2 = hist(fa, GREY_B, 0.35, 0.28)
        h3 = hist(ca, HL, 0.7, 0.28)
        l1 = label(rf"$100$ different 70/30 splits: \ ${100 * sa.min():.1f}$ to ${100 * sa.max():.1f}\%$", font_size=22,
                   color=ROCC).next_to(ax.c2p(0.905, 0.15), RIGHT, buff=0.1)
        l2 = label(rf"single folds of ten-fold cross-validation: \ s.d. ${100 * fa.std():.1f}$ points", font_size=22,
                   color=GREY_B).next_to(ax.c2p(0.905, 0.5), RIGHT, buff=0.1)
        l3 = label(rf"ten-fold cross-validation, \ $20$ shuffles: \ ${100 * ca.min():.1f}$ to ${100 * ca.max():.1f}\%$",
                   font_size=22, color=HL).next_to(ax.c2p(0.905, 0.85), RIGHT, buff=0.1)
        rule = label(r"choose on the training pages; \ test once, \ at the end", font_size=28, color=WHITE).to_edge(UP, buff=0.35)
        with self.voiceover(
            "And how sure is any single number? Logistic regression on two rates, scored again and again. "
            f"<bookmark mark='a'/> On a hundred different random splits into training and test pages, its accuracy "
            f"ranges from {100 * sa.min():.0f} to {100 * sa.max():.0f} percent: the luck of the split. "
            "<bookmark mark='b'/> Ten-fold cross-validation uses every page for testing once. Each fold alone "
            f"wobbles by about {100 * fa.std():.0f} points, <bookmark mark='c'/> but their average is steady: twenty "
            f"different shuffles all land between {100 * ca.min():.1f} and {100 * ca.max():.1f}. "
            "<bookmark mark='d'/> The rule that keeps the whole contest honest: make every choice on the training "
            "pages, and look at the test pages once, at the end."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(h1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(h2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(h3), FadeIn(l3))
            vo.wait_until("d")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()
