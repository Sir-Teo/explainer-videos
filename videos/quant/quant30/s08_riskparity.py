from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EW_C, GOOD, HRP_C, HURDLE, PART, RP_C, SHRINK_C, fit_right, house_lab, load

RULE_C = {"1/N": EW_C, "inverse volatility": QC.OPTION, "ERC": RP_C, "GMV": SHRINK_C, "HRP": HRP_C}


class RiskParity(VoiceoverScene):
    def construct(self):
        r = load("riskparity")
        self.card()
        self.contributions(r)
        self.erc_math()
        self.dendrogram(r)
        self.hrp_steps()
        self.compare(r)
        self.question()

    def card(self):
        c = chapter_card(7, r"Risk parity and HRP", r"If expected returns cannot be estimated, can a portfolio be built "
                         r"from risk alone?", part=PART)
        with self.voiceover("Chapter seven. If expected returns are too noisy to use, perhaps a portfolio should be built "
                            "from risk alone. Not the least risk, which leans on the smallest eigenvalues, but risk "
                            "spread evenly."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def contributions(self, r):
        cols = r["columns"]
        rc_ew, rc_erc = np.asarray(r["rc"]["1/N"]), np.asarray(r["rc"]["ERC"])
        order = np.argsort(-rc_ew)
        top = float(np.ceil(rc_ew.max() * 50) / 50)
        g = axes([-0.5, 48.5], [0, top], x_length=11.0, y_length=4.2, xlabel=r"the 49 industries, by their share of "
                 r"1/N's risk", ylabel=r"share of portfolio variance", xticks=[], yticks=[0, top / 2, top],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=15).move_to(DOWN * 0.3)
        ax = g.ax

        def bars(v, col, dx):
            return VGroup(*[Rectangle(width=0.09, height=max(ax.c2p(0, float(v[i]))[1] - ax.c2p(0, 0)[1], 0.002),
                                      stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(ax.c2p(k + dx, 0),
                                                                                              aligned_edge=DOWN)
                            for k, i in enumerate(order)])
        be, br = bars(rc_ew, EW_C, -0.15), bars(rc_erc, RP_C, 0.15)
        leg = legend([(EW_C, r"1/N: equal money"), (RP_C, r"equal risk contributions")], font_size=15).to_corner(UR, buff=0.35)
        i0 = int(order[0])
        with self.voiceover(
            "Equal money is not equal risk. <bookmark mark='a'/> In the equally weighted portfolio of the forty-nine "
            f"industries, the most volatile, {cols[i0]}, contributes {100 * rc_ew[i0]:.1f} percent of the variance, and "
            f"the calmest only {100 * rc_ew.min():.1f}. <bookmark mark='b'/> A risk-parity portfolio instead chooses "
            "weights so that every industry contributes the same share: here one forty-ninth each."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in be], lag_ratio=0.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in br], lag_ratio=0.02))
        self.wait(0.4)
        self.clear_scene()

    def erc_math(self):
        rows = [cmath(r"RC_i", r"=", r"\frac{w_i(\Sigma w)_i}{w^\top\Sigma w},\qquad \textstyle\sum_i RC_i = 1", font_size=32,
                      colors={r"RC_i": RP_C}),
                cmath(r"\min_{y > 0}", r"\ ", r"\tfrac12 y^\top\Sigma y - \textstyle\sum_i b_i\log y_i", font_size=32,
                      colors={r"\min_{y > 0}": RP_C}),
                cmath(r"(\Sigma y)_i", r"=", r"b_i / y_i\ \Rightarrow\ y_i(\Sigma y)_i = b_i,\quad w = y/1^\top y", font_size=30)]
        whys = [why(r"Euler's theorem for the homogeneous function $\sigma(w)$: each asset's contribution to risk"),
                why(r"Spinu (2013): a strictly convex problem, so the risk-budgeted portfolio exists, is unique, and "
                    r"Newton's method finds it"),
                why(r"its first-order condition is exactly the budget: risk contributions proportional to $b$; "
                    r"Maillard, Roncalli and Te\"iletche (2010) on the properties")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The mathematics. <bookmark mark='a'/> Each asset's contribution to risk is its weight times its marginal "
            "risk; by Euler's theorem they add up to the total. <bookmark mark='b'/> Florin Spinu found the trick in "
            "2013: minimise one half y Sigma y minus the sum of the budgets times log y, a strictly convex problem. "
            "<bookmark mark='c'/> Its first-order condition says each y times its marginal risk equals its budget: "
            "normalise y and you have the risk-parity portfolio, unique, found in a few Newton steps."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def dendrogram(self, r):
        from scipy.cluster.hierarchy import dendrogram
        Z = np.asarray(r["linkage"], float)
        dd = dendrogram(Z, no_plot=True, labels=r["columns"])
        ic, dc = np.asarray(dd["icoord"]), np.asarray(dd["dcoord"])
        xmax, ymax = ic.max() + 5, dc.max()
        W, H = 12.0, 4.2
        X = lambda v: -W / 2 + W * v / xmax
        Y = lambda v: -1.6 + H * v / ymax
        links = VGroup()
        for xs, ys in zip(ic, dc):
            pts = [[X(x), Y(y), 0] for x, y in zip(xs, ys)]
            links.add(VMobject(stroke_color=HRP_C, stroke_width=1.6).set_points_as_corners(pts))
        labs = VGroup(*[Text(n, font_size=9, color=GREY_B).rotate(PI / 2).move_to([X(5 + 10 * k), -1.95, 0])
                        for k, n in enumerate(dd["ivl"])])
        title = label(r"single-linkage clustering of the distance $\sqrt{(1 - \rho_{ij})/2}$, 2011--2020", font_size=20,
                      color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Marcos López de Prado proposed a different route in 2016: hierarchical risk parity. <bookmark mark='a'/> "
            "First, cluster the assets by correlation, here with single linkage on the distance square root of one minus "
            "rho over two. The tree groups industries that move together: the leaves along the bottom are the "
            "industries in the tree's order. Then the covariance matrix, reordered this way, is nearly block-diagonal."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(Create(links, lag_ratio=0.02, run_time=3), FadeIn(labs))
        self.wait(0.4)
        self.clear_scene()

    def hrp_steps(self):
        from explainer.quant.house import portfolio as P
        card = house_lab(r"Recursive bisection", P.hrp, "stack = [order]", 13, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Then the allocation, as the House runs it. Split the ordered list of assets in half. Give each half the "
            "inverse-variance portfolio of its members, and split the money between the halves in inverse proportion to "
            "those portfolios' variances. Repeat inside each half, down to single assets. No matrix is ever inverted, so "
            "the smallest, noisiest eigenvalues never get the chance to dominate."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def compare(self, r):
        names = ["1/N", "inverse volatility", "ERC", "HRP", "GMV"]
        hx = [-4.0, -0.6, 2.0, 4.4]
        head = VGroup(label(r"rule", font_size=18, color=GREY_B), label(r"largest weight", font_size=18, color=GREY_B),
                      label(r"largest risk share", font_size=18, color=GREY_B),
                      label(r"volatility, in sample", font_size=18, color=GREY_B))
        tab = VGroup(head)
        for n in names:
            w = np.asarray(r["weights"][n])
            rc = np.asarray(r["rc"][n])
            tab.add(VGroup(label(n, font_size=19, color=RULE_C[n]), MathTex(rf"{100 * w.max():.1f}\%", font_size=24),
                           MathTex(rf"{100 * rc.max():.1f}\%", font_size=24), MathTex(rf"{100 * r['vol'][n]:.1f}\%", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.2 - 0.7 * j, 0])
        foot = wrapped_label(r"the 49 industries, covariance from 2011--2020 monthly excess returns; the in-sample "
                             r"volatility flatters GMV most, which the research chapter explains. Out-of-sample "
                             r"comparisons are in Chapter 2's table", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.5)
        v = r["vol"]
        with self.voiceover(
            "Side by side. <bookmark mark='a'/> The rules run from equal money, through equal risk, to minimum variance. "
            f"In sample, minimum variance has by far the lowest volatility, {100 * v['GMV']:.1f} percent against "
            f"{100 * v['HRP']:.1f} for HRP and {100 * v['ERC']:.1f} for risk parity. But it concentrates its weight and "
            "trusts every estimate; risk parity and HRP give up some in-sample risk for weights that do not depend on "
            "inverting a noisy matrix. Which trade is worth it is a question for out-of-sample data, and for the envelope."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.25))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two uncorrelated assets with volatilities 10\% and 20\%. What are the equal-risk-contribution "
                       r"weights?")
        with self.voiceover(
            "Pause and predict. Two uncorrelated assets, with volatilities of ten and twenty percent. What weights give "
            "them equal risk contributions?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
