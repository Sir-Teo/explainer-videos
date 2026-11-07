from __future__ import annotations

import numpy as np

from videos.stats.stats48.common import *  # noqa: F403


class Chaining(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.tree()
        self.path()
        self.chart()
        self.dudley()

    def card(self):
        card = chapter_card(4, r"Chaining", r"Dudley's refining nets", lit=(1967,), part=PART)
        with self.voiceover("Chapter four. Chaining: Dudley's refining nets."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"Z_1, \dots, Z_N \sim N(0, \sigma^2)", r":", r"E \max_j Z_j \le \sigma \sqrt{2 \log N}", font_size=34),
            cmath(r"\text{Brownian motion on } 2^K \text{ grid points}", r":", r"E \max \le \sqrt{2 K \log 2} \to \infty", font_size=32),
            cmath(r"\text{but}", r":", r"E \sup_{[0,1]} B_t = \sqrt{2/\pi} = 0.798", font_size=34),
            cmath(r"\text{the waste}", r":", r"\text{neighbours are nearly equal; \ the union bound treats them as strangers}", font_size=28),
        ]
        rows[1][-1].set_color(BADC)
        rows[2][-1].set_color(GOODC)
        whys = [why(r"the union bound for Gaussians"), why(r"each point has variance $\le 1$"), why(r"the reflection principle, \ Part 44"), why(r"correlation ignored")]
        heading = label('A single union bound wastes the proximity of neighbouring points', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The basic tool for a maximum of N Gaussians with standard deviation sigma is the union "
            "bound: the expected maximum is at most sigma times the root of two log N. <bookmark mark='b'/> Apply it to "
            "Brownian motion on a grid of two to the K points. Each value has variance at most one, so the bound is the root "
            "of two K log two, which grows without limit as the grid is refined. <bookmark mark='c'/> Yet the true expected "
            "supremum over the whole interval is finite: root two over pi, about point eight, by Part forty-four's "
            "reflection principle. <bookmark mark='d'/> The union bound wastes its strength because neighbouring values are "
            "nearly equal, and it treats them as if they were independent."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tree(self):
        g = ChainingNet.tree(levels=5, width=10.4, height=4.2)
        rows, edges = g
        g.move_to([0, 0.4, 0])
        labs = VGroup(*[label(rf"level {k}: \ $2^{{{k}}}$ cells", font_size=20, color=GREY_B).next_to(rows[k], LEFT, buff=0.35).set_x(-6.2) for k in range(6)])
        foot = label(r"each new point is tied to its parent, \ $2^{-k}$ away: \ the link has s.d. $2^{-k/2}$", font_size=24, color=CLASSC).move_to([0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Richard Dudley's chaining, from 1967, uses the correlation. Build nets that refine: at "
            "level zero, the two endpoints; <bookmark mark='b'/> at each later level, add the midpoints of the previous "
            "cells, so that level k has two to the k cells. <bookmark mark='c'/> Tie every new point to its parent, the "
            "nearest point of the coarser net, which is two to the minus k away. Then the value at any point is the value at "
            "the coarsest level plus a chain of links down the tree, and the link at level k is a Brownian increment over a "
            "distance two to the minus k, with standard deviation two to the minus k over two."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(labs[0]))
            vo.wait_until("b")
            for k in range(1, 6):
                self.play(FadeIn(rows[k]), FadeIn(labs[k]), run_time=0.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(edges[k]) for k in range(1, 6)], lag_ratio=0.4), FadeIn(foot), run_time=3)
        self.clear_scene()

    def path(self):
        d = load("chain")
        A = axes([0, 1], [-1.8, 1.6], x_length=7.4, y_length=4.4, xlabel=r"$t$", ylabel=r"$B_t$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[-1, 0, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        net = ChainingNet(ax, d["t"], d["w"])
        full = polyline(ax, d["t"], d["w"], GREY_D, 2)
        cols = [S.TRUTH, S.EST, S.ALT, S.KEPT, S.PRIOR, S.RESID]
        ap = [net.approx(k, cols[k % len(cols)], 3) for k in range(0, 7)]
        lk = [net.links(k, CLASSC, 3) for k in range(1, 7)]
        side = fit_rows(VGroup(
            label(r"grey: \ one Brownian path", font_size=22, color=GREY_B),
            label(r"level $k$: \ the path seen on $\{j/2^k\}$, \ joined up", font_size=22, color=S.EST),
            label(r"gold: \ midpoint minus the two-parent chord", font_size=22, color=CLASSC),
            label(r"midpoint s.d. $2^{-(k+1)/2}$; \ $2^{k-1}$ new points", font_size=22, color=GOODC),
            label(r"$\sup B \le \max_0 + \sum_k \max(0,\text{level-}k\text{ corrections})$", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is a Brownian path. <bookmark mark='b'/> Seen at level zero it is a single chord from zero to its endpoint. At level one, add the midpoint; at level two, the quarter points; and so on: each picture refines the last. <bookmark mark='c'/> The gold segments are midpoint corrections relative to the chord joining both neighbouring parents. This interpolation version has slightly smaller variances than the single-parent tree. <bookmark mark='d'/> At level k there are two to the k minus one of them, each of size about two to the minus k plus one over two in standard deviation. The number grows but the sizes shrink faster. <bookmark mark='e'/> So the supremum of the path is at most the maximum at the coarsest level plus, for each level, the positive part of the largest midpoint correction. Including zero matters: keeping the old grid points must never lower a maximum. Apply the union bound level by level, where it is cheap, and add up."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(Create(full), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ap[0]), FadeIn(side[1]))
            cur = ap[0]
            for k in range(1, 4):
                self.play(Transform(cur, ap[k]), run_time=0.8)
            vo.wait_until("c")
            for k in range(4, 7):
                self.play(Create(lk[k - 1]), Transform(cur, ap[k]), run_time=0.8)
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def chart(self):
        d = load("chain")
        ks = np.asarray(d["ks"], float)
        kk = np.arange(0, 41, dtype=float)
        A = axes([0, 40], [0, 7.6], x_length=7.4, y_length=4.4, xlabel=r"net level $K$ \ ($2^K + 1$ points)", ylabel=r"$E \max$ over the net",
                 xticks=[0, 10, 20, 30, 40], yticks=[0, 0.8, 2, 4, 6], center=[-2.5, 0.2, 0])
        ax = A.ax
        union = np.sqrt(2 * np.log(2.0 ** kk + 1))
        cu = polyline(ax, kk, union, BADC, 4)
        cs = VGroup(polyline(ax, ks, d["emax"], EMPC, 4), *[Dot(ax.c2p(a, b), radius=0.06, color=EMPC) for a, b in zip(ks, d["emax"])])
        part = np.asarray(d["partial"])[: len(kk)]
        cc = polyline(ax, kk, part, BOUNDC, 4)
        ex = DashedLine(ax.c2p(0, d["exact"]), ax.c2p(40, d["exact"]), color=BRIDGEC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"red: \ the one-step union bound: \ $\sqrt{2K\log 2} \to \infty$", font_size=22, color=BADC),
            label(rf"blue: \ simulated, \ $K \le 10$: \ {d['emax'][-1]:.3f}", font_size=22, color=EMPC),
            label(rf"white: \ $\sqrt{{2/\pi}}$ = {d['exact']:.3f}", font_size=22, color=BRIDGEC),
            label(rf"purple: \ positive-part sum + bounded tail: {d['bound']:.2f}", font_size=22, color=BOUNDC),
            label(r"finite, \ within a constant: \ that is the point", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Compare. In red, the union bound applied in one step to the whole net: it climbs without limit as the net refines. <bookmark mark='b'/> In blue, the expected maximum over the net, simulated: it rises to {say(d['emax'][-1], 3)} at a thousand and twenty-five points <bookmark mark='c'/> and is closing on root two over pi. <bookmark mark='d'/> In purple, the chaining bound, summed level by level: it converges, to {say(d['bound'], 2)}. <bookmark mark='e'/> It is loose, but it is finite, and it stays finite as the net becomes the whole interval. Chaining trades the right answer for the right order, and in empirical-process theory the order is what matters."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"blue simulated: \ 4,000 paths; \ bounds exact")))
            vo.wait_until("a")
            self.play(Create(cu), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ex), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cc), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def dudley(self):
        rows = [
            cmath(r"\text{level } k", r":", r"N(2^{-k}) \text{ links, \ each of size } \le 2 \cdot 2^{-k}", font_size=32),
            cmath(r"E \sup_{s, t} |X_s - X_t|", r"\lesssim", r"\textstyle\sum_k 2^{-k}\sqrt{\log N(2^{-k})}", font_size=34),
            cmath(r"\phantom{E \sup}", r"\lesssim", r"\int_0^{\mathrm{diam}} \sqrt{\log N(\varepsilon, T, d)}\, d\varepsilon", font_size=36),
            cmath(r"\text{Brownian motion}, \ d(s,t) = \sqrt{|s - t|}", r":", r"N(\varepsilon) \approx \varepsilon^{-2}, \ \int_0^1 \sqrt{2\log(1/\varepsilon)}\,d\varepsilon = \sqrt{\pi/2}", font_size=28),
        ]
        rows[2][-1].set_color(CLASSC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"any sub-Gaussian process"), why(r"the union bound, \ level by level"), why(r"Dudley's entropy integral (1967)"), why(r"finite: \ continuous paths")]
        heading = label('Chaining sums complexity at progressively finer scales', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The same argument works for any process whose increments are sub-Gaussian in some metric: at level k, the net is an epsilon net with epsilon two to the minus k, and each link is at most twice that in the metric. <bookmark mark='b'/> The union bound at each level gives a sum, over levels, of the link size times the root of the log of the number of links. <bookmark mark='c'/> And that sum is, up to constants, an integral: Dudley's entropy integral, the area under the root of the metric entropy. <bookmark mark='d'/> For Brownian motion the natural metric is the root of the distance in time, N of epsilon is about one over epsilon squared, and the integral is finite: root pi over two. For a separable sub-Gaussian process, the entropy condition gives a bounded uniformly continuous version in the increment metric. For the empirical process, the same integral, with the class's entropy, is the condition of the next chapter."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
