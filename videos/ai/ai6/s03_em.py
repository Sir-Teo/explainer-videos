from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import AUSTEN, DICKENS, ellipse_2sd, load, mix


class EM(VoiceoverScene):
    def construct(self):
        self.card()
        self.fit()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Hidden sources: mixtures and EM", r"Which source made each point?", part=6)
        with self.voiceover("Chapter two. Mixtures, and the EM algorithm."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def fit(self):
        g = load("gmm")
        P, y = np.asarray(g["P"]), np.asarray(g["y"])
        means, covs, ws = np.asarray(g["means"]), np.asarray(g["covs"]), np.asarray(g["w"])
        R, ll = np.asarray(g["r"]), np.asarray(g["ll"])
        flip = ((R[-1] > 0.5) == y).mean() < 0.5  # the component that ends on Dickens takes Dickens's colour
        if flip:
            R = 1 - R
            means, covs, ws = means[:, ::-1], covs[:, ::-1], ws[:, ::-1]
        lo, hi = P.min(0) - 0.4, P.max(0) + 0.4
        ax = Axes(x_range=[lo[0], hi[0], 2], y_range=[lo[1], hi[1], 2], x_length=7.6, y_length=5.6, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-2.4, -0.3, 0])
        names = VGroup(label(r"direction 1", font_size=22, color=GREY_A).next_to(ax.x_axis.get_right(), DOWN, buff=0.12)
                       .shift(LEFT * 0.6),
                       label(r"direction 2", font_size=22, color=GREY_A).next_to(ax.y_axis, UP, buff=0.08))
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.045, color=GREY_B, fill_opacity=0.85) for p in P])
        it = ValueTracker(0)

        def ells():
            k = int(round(it.get_value()))
            return VGroup(*[ellipse_2sd(ax, means[k][c], covs[k][c], col, stroke_width=4)
                            for c, col in ((0, AUSTEN), (1, DICKENS))],
                          *[Dot(ax.c2p(*means[k][c]), radius=0.08, color=col) for c, col in ((0, AUSTEN), (1, DICKENS))])

        el = always_redraw(ells)
        # the log-likelihood, climbing
        lax = Axes(x_range=[0, len(ll), 10], y_range=[float(ll[1:].min()) - 0.05, float(ll.max()) + 0.05, 0.1], x_length=4.2,
                   y_length=2.2, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([4.4, -1.9, 0])
        lcurve = always_redraw(lambda: VMobject(color=C.BITS, stroke_width=3).set_points_as_corners(
            [lax.c2p(k, ll[k]) for k in range(1, max(3, int(round(it.get_value())) + 1))]))  # from round 1: round 0 is far below
        ll_l = label(r"log-likelihood: \ never goes down", font_size=22, color=C.BITS).next_to(lax, UP, buff=0.1)
        steps = VGroup(label(r"E: \ for each point, how likely \\ is each bell to have made it?", font_size=24),
                       label(r"M: \ refit each bell to its points, \\ weighted by those chances", font_size=24))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, 1.6, 0])
        e_box = SurroundingRectangle(steps[0], color=C.BITS, buff=0.1, corner_radius=0.08)
        m_box = SurroundingRectangle(steps[1], color=C.BITS, buff=0.1, corner_radius=0.08)
        itv = Integer(0, font_size=30, color=WHITE)
        itl = VGroup(label(r"round", font_size=26, color=GREY_A), itv).arrange(RIGHT, buff=0.15).next_to(steps, UP, buff=0.35)
        res = label(rf"the two bells' points match the authors: \ ${100 * g['agree']:.0f}\%$", font_size=26,
                    color=WHITE).to_edge(DOWN, buff=0.25).set_x(-2.4)
        cite_ = cite(r"A.~P.~Dempster, N.~M.~Laird \& D.~B.~Rubin, \textit{Maximum Likelihood from Incomplete Data via the EM "
                     r"Algorithm} (1977)", corner=UR)

        def colour(k):
            return [d.animate.set_color(mix(AUSTEN, DICKENS, R[k][i])) for i, d in enumerate(dots)]

        with self.voiceover(
            "PCA finds directions. A mixture model goes further: it supposes that each point was made by one of "
            "several hidden sources, each a bell curve of its own, and tries to recover them. Here are the pages "
            "along the first two directions, with no colours: we don't know who wrote what. "
            "<bookmark mark='a'/> Start with two guessed bells, badly placed. The expectation-maximization "
            "algorithm, EM, alternates two steps. <bookmark mark='b'/> E: for each page, how likely is each bell "
            "to have made it? That gives every page a soft colour. <bookmark mark='c'/> M: refit each bell to the "
            "pages, weighted by those colours."
        ) as vo:
            self.play(Create(ax), FadeIn(names), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(el), FadeIn(cite_))
            vo.wait_until("b")
            self.play(Create(e_box), FadeIn(steps[0]))
            self.play(*colour(0), run_time=1.2)
            vo.wait_until("c")
            self.play(ReplacementTransform(e_box, m_box), FadeIn(steps[1]))
            self.play(it.animate.set_value(1), run_time=1.2)
        with self.voiceover(
            "Then again: E, M, E, M. <bookmark mark='a'/> Each round can only raise the likelihood, so the bells "
            "creep toward a fit. <bookmark mark='b'/> After forty rounds they've settled, and the pages each one "
            f"claims match the true authors {100 * g['agree']:.0f} percent of the time. Nobody told it there were "
            "authors at all. EM fits any model with hidden parts, and it's the next chapter's engine too."
        ) as vo:
            self.play(FadeIn(itl), Create(lax), FadeIn(ll_l), FadeIn(lcurve))
            for k in range(1, 8):
                self.play(*colour(k), ChangeDecimalToValue(itv, k), run_time=0.45)
                self.play(it.animate.set_value(k + 1), run_time=0.45)
            vo.wait_until("a")
            last = len(ll) - 1
            self.play(*colour(last), it.animate.set_value(last), ChangeDecimalToValue(itv, last), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(res))
        el.clear_updaters()
        lcurve.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
