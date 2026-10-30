from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import AUSTEN, BOUND, DICKENS, HIDDEN, LIKE, PART, ellipse_2sd, load, mix

COL = {r"q(z)": HIDDEN, r"\mathcal{B}(q, \theta)": BOUND, r"\log p(x; \theta)": LIKE, r"\ge": BOUND}


class EM(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Mixtures and EM", r"Which source made each point?", lit=(1977,), part=PART)
        with self.voiceover("Chapter four. Mixtures, and the EM algorithm."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.fit()
        self.derive()
        self.bound()
        self.kmeans()

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
        lax = Axes(x_range=[0, len(ll), 10], y_range=[float(ll[1:].min()) - 0.05, float(ll.max()) + 0.05, 0.1], x_length=4.2,
                   y_length=2.2, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([4.4, -1.9, 0])
        lcurve = always_redraw(lambda: VMobject(color=C.BITS, stroke_width=3).set_points_as_corners(
            [lax.c2p(k, ll[k]) for k in range(1, max(3, int(round(it.get_value())) + 1))]))
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
        mixdef = definition_card(r"a mixture of Gaussians",
                                 cmath(r"p(x)", r"=", r"\sum_{k} \pi_k\, \mathcal{N}(x \mid \mu_k, \Sigma_k)", font_size=34),
                                 width=5.6, color=HIDDEN).move_to([4.0, 1.2, 0])

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
            self.play(Create(ax), FadeIn(names), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), FadeIn(mixdef),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeOut(mixdef), FadeIn(el), FadeIn(cite_))
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

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\log p(x; \theta)", r"=", r"\log \sum_z p(x, z; \theta)", colors=COL, font_size=38),
            cmath(r"\log p(x; \theta)", r"=", r"\log \sum_z", r"q(z)", r"\frac{p(x, z; \theta)}{q(z)}", colors=COL,
                  font_size=38),
            cmath(r"\log p(x; \theta)", r"\ge", r"\sum_z", r"q(z)", r"\log \frac{p(x, z; \theta)}{q(z)}", r"=",
                  r"\mathcal{B}(q, \theta)", colors=COL, font_size=38),
            cmath(r"\log p(x; \theta)", r"-", r"\mathcal{B}(q, \theta)", r"=",
                  r"\mathrm{KL}\big(q(z) \,\|\, p(z \mid x; \theta)\big)", colors=COL, font_size=38),
            cmath(r"\log p(x; \theta_{\mathrm{new}})", r"\ge", r"\mathcal{B}(q, \theta_{\mathrm{new}})", r"\ge",
                  r"\mathcal{B}(q, \theta_{\mathrm{old}})", r"=", r"\log p(x; \theta_{\mathrm{old}})", font_size=36),
        ]
        rows[4][0].set_color(LIKE)
        rows[4][6].set_color(LIKE)
        rows[4][2].set_color(BOUND)
        rows[4][4].set_color(BOUND)
        whys = [why(r"$z$: \ which bell made $x$, \ hidden"),
                why(r"multiply and divide \\ by any $q(z) > 0$"),
                why(r"Jensen: \ $\log$ is concave, \\ $\log$ of an average $\ge$ average of $\log$s"),
                why(r"the gap is a KL: \ zero when \\ $q$ is the posterior \ (the E step)"),
                why(r"bound below; \ M step; \\ E step made it touch")]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-2.6, buff=0.55, edge=6.8)
        head = label(r"Why EM never goes downhill", font_size=34).to_edge(UP, buff=0.25)
        box_ = None
        with self.voiceover(
            "Why can't EM ever go downhill? Write the log-likelihood as a sum over the hidden choice z: which bell "
            "made this point. <bookmark mark='a'/> Multiply and divide by any distribution q over z. "
            "<bookmark mark='b'/> The log of an average is at least the average of the logs: that's Jensen's "
            "inequality, because the log curves downward. So we get a lower bound, B, that we can compute. "
            "<bookmark mark='c'/> How far below? The gap is exactly a KL divergence, between q and the posterior over "
            "z. It vanishes when q is the posterior, and that is the E step: it makes the bound touch. "
            "<bookmark mark='d'/> The M step then maximizes the bound over the parameters. Chain the three facts: the "
            "new likelihood is above the bound, the bound went up, and it started touching. The likelihood can never "
            "fall. That's Dempster, Laird and Rubin's theorem, from 1977."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            box_ = SurroundingRectangle(rows[4], color=LIKE, buff=0.12, corner_radius=0.1)
            self.play(Create(box_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bound(self):
        e = load("embound")
        ts, ll, bd = np.asarray(e["ts"]), np.asarray(e["ll"]), np.asarray(e["bound"])
        rounds = list(e["rounds"])
        i0, i1 = int(e["i0"]), int(e["i1"])
        panels = VGroup()
        anims = []
        for j, k in enumerate((0, 1, 4)):
            r = rounds.index(k)
            ok = np.isfinite(ll[r])
            yl, yb = ll[r][ok], bd[r][ok]
            top = float(yl.max())
            lo_ = float(ll[r][i0]) if k == 0 else float(min(yl.min(), yb.min()))
            lo_ = lo_ - 0.15 * (top - lo_)
            hi_ = top + 0.12 * (top - lo_)
            ax = Axes(x_range=[-0.5, 1.6, 0.5], y_range=[lo_, hi_, (hi_ - lo_) / 4], x_length=3.8, y_length=3.6, tips=False,
                      axis_config={"stroke_color": GREY_D, "include_ticks": False})
            keep = ok & (ll[r] >= lo_)
            c_l = curve(ax, ts[keep], ll[r][keep], LIKE, 4)
            kb = ok & (bd[r] >= lo_)
            c_b = curve(ax, ts[kb], bd[r][kb], BOUND, 3)
            p0 = Dot(ax.c2p(0, ll[r][i0]), radius=0.07, color=WHITE)
            p1 = Dot(ax.c2p(1, bd[r][i1]), radius=0.07, color=BOUND)
            p2 = Dot(ax.c2p(1, ll[r][i1]), radius=0.07, color=LIKE)
            up = Arrow(ax.c2p(1, bd[r][i1]), ax.c2p(1, ll[r][i1]), buff=0.05, color=GREY_A, stroke_width=2,
                       max_tip_length_to_length_ratio=0.3) if ll[r][i1] - bd[r][i1] > 0.05 * (hi_ - lo_) else VGroup()
            ticks = VGroup(label(rf"round ${k}$", font_size=20, color=GREY_A).next_to(ax.c2p(0, lo_), DOWN, buff=0.1),
                           label(rf"round ${k + 1}$", font_size=20, color=GREY_A).next_to(ax.c2p(1, lo_), DOWN, buff=0.1))
            vlines = VGroup(DashedLine(ax.c2p(0, lo_), ax.c2p(0, hi_), color=GREY_D, stroke_width=1),
                            DashedLine(ax.c2p(1, lo_), ax.c2p(1, hi_), color=GREY_D, stroke_width=1))
            pan = VGroup(ax, vlines, ticks, c_l, c_b, p0, p1, p2, up)
            panels.add(pan)
            anims.append((c_b, p0, p1, p2, up))
        panels.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.3)
        heads = VGroup(*[label(rf"from round ${k}$ to round ${k + 1}$", font_size=24).next_to(p, UP, buff=0.15)
                         for k, p in zip((0, 1, 4), panels)])
        lg = legend([(LIKE, r"the log-likelihood"), (BOUND, r"the bound the E step built")], font_size=22)
        lg.arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.3)
        xn = label(r"along the straight line in parameter space from one round's parameters to the next "
                   r"\ (computed on the pages)", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Here's that bound for real, on the pages. Each panel follows a straight line through the parameters, "
            "from one round's bells to the next round's. The yellow curve is the log-likelihood. "
            "<bookmark mark='a'/> The green curve is the bound that round's E step built: always below, touching at "
            "the start. <bookmark mark='b'/> The M step jumps to the top of the green curve, and the yellow curve, "
            "above it, can only be higher there. <bookmark mark='c'/> The first step, from a poor start, is a leap; "
            "later steps are small, and the curves flatten as EM settles. It never overshoots, and it never needs a "
            "learning rate."
        ) as vo:
            self.play(FadeIn(lg), FadeIn(xn), *[FadeIn(VGroup(p[0], p[1], p[2], p[3])) for p in panels], FadeIn(heads))
            vo.wait_until("a")
            self.play(*[Create(a[0]) for a in anims], *[FadeIn(a[1]) for a in anims], run_time=1.5)
            vo.wait_until("b")
            self.play(*[FadeIn(a[2], scale=1.5) for a in anims])
            self.play(*[FadeIn(a[3]) for a in anims], *[GrowArrow(a[4]) for a in anims if isinstance(a[4], Arrow)])
            vo.wait_until("c")
            self.play(Indicate(panels[0], scale_factor=1.03, color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kmeans(self):
        g, km = load("gmm"), load("kmeans")
        P, y = np.asarray(g["P"]), np.asarray(g["y"])
        cs, zs, J = np.asarray(km["centres"]), np.asarray(km["z"]), np.asarray(km["J"])
        zl = zs[-1]
        dick = int(round(np.mean(zl[y == 1])))  # the cluster that ends on Dickens takes his colour
        cmap = {dick: DICKENS, 1 - dick: AUSTEN}
        lo, hi = P.min(0) - 0.4, P.max(0) + 0.4
        ax = Axes(x_range=[lo[0], hi[0], 2], y_range=[lo[1], hi[1], 2], x_length=6.4, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-3.2, -0.5, 0])
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.04, color=GREY_B, fill_opacity=0.85) for p in P])
        it = ValueTracker(0)

        def cents():
            k = min(int(round(it.get_value())), len(cs) - 1)
            return VGroup(*[Star(n=5, outer_radius=0.17, color=cmap[c], fill_opacity=1).move_to(ax.c2p(*cs[k][c]))
                            for c in (0, 1)])

        def border():
            k = min(int(round(it.get_value())), len(cs) - 1)
            a, b = cs[k]
            mid, d = (a + b) / 2, b - a
            n_ = np.array([-d[1], d[0]]) / np.linalg.norm(d)
            return DashedLine(ax.c2p(*(mid - 2.6 * n_)), ax.c2p(*(mid + 2.6 * n_)), color=WHITE, stroke_width=2)

        st = always_redraw(cents)
        bl_ = always_redraw(border)
        jv = DecimalNumber(J[0], num_decimal_places=2, font_size=30, color=C.BITS)
        jl = VGroup(label(r"mean squared distance to the nearest centre:", font_size=22, color=GREY_A), jv)
        jl.arrange(RIGHT, buff=0.15).to_edge(UP, buff=0.35).shift(LEFT * 1.5)
        rule = VGroup(label(r"E, made hard: \ each point joins its nearest centre", font_size=24),
                      label(r"M: \ each centre moves to the mean of its points", font_size=24)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                    buff=0.2)
        rule.move_to([3.8, 1.9, 0])
        sig, hard = np.asarray(km["sigma"]), np.asarray(km["hard"])
        g2 = axes([0, len(sig) - 1, 1], [0, 1, 0.5], x_length=4.2, y_length=2.0, xlabel=r"bells of width $\sigma$, shrinking",
                  ylabel=r"pages $99\%$ sure of their bell", yticks=[0, 1], center=[3.8, -1.2, 0])
        hc = curve(g2.ax, np.arange(len(sig)), hard, HIDDEN, 3)
        res = label(rf"$k$-means: \ ${100 * km['agree']:.0f}\%$ match the authors \ (EM: \ ${100 * km['agree_em']:.0f}\%$)",
                    font_size=26).to_edge(DOWN, buff=0.3).set_x(-3.2)
        hist = cite(r"S.~Lloyd (1957, published 1982); \ J.~MacQueen (1967)", corner=DR)
        softer = km["agree_em"] > km["agree"]
        verdict = (f"It matches the authors {100 * km['agree']:.0f} percent of the time, a little below EM's "
                   f"{100 * km['agree_em']:.0f}: hard choices throw away the doubt about pages near the border."
                   if softer else
                   f"It matches the authors {100 * km['agree']:.0f} percent of the time, as well as EM's "
                   f"{100 * km['agree_em']:.0f}.")
        with self.voiceover(
            "Now make EM's choices hard. Instead of soft colours, each page joins whichever centre is nearest; then "
            "each centre moves to the mean of its pages. That's k-means, Stuart Lloyd's algorithm from Bell Labs in "
            f"1957. <bookmark mark='a'/> From the same poor start, it settles in {km['iters']} rounds, and the "
            "average squared distance falls every time. <bookmark mark='b'/> It really is EM: take bells that are "
            "round and equal, and shrink their width. The soft colours harden, until every page is ninety-nine "
            "percent sure. <bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(Create(ax), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), FadeIn(rule), FadeIn(hist),
                      run_time=1.5)
            self.play(FadeIn(st), Create(bl_), FadeIn(jl))
            vo.wait_until("a")
            for k in range(len(cs)):
                z = zs[k]
                self.play(*[d.animate.set_color(cmap[int(z[i])]) for i, d in enumerate(dots)],
                          it.animate.set_value(k), ChangeDecimalToValue(jv, J[k]), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(hc), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(res))
        st.clear_updaters()
        bl_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
