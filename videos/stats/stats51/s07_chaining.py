from __future__ import annotations

import numpy as np

from videos.stats.stats51.common import *  # noqa: F403


class Chaining(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.dudley()
        self.chart()
        self.sudakov()
        self.ellipsoid()
        self.generic()

    def card(self):
        card = chapter_card(6, r"Chaining revisited", r"The supremum of a Gaussian process, \ scale by scale", part=PART)
        with self.voiceover("Chapter six. Chaining revisited: the supremum of a Gaussian process, scale by scale."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"(X_t)_{t \in T} \text{ centred Gaussian}", r":", r"d(s, t) = \sqrt{E(X_s - X_t)^2}: \ \text{the canonical metric}", font_size=30),
            cmath(r"E\sup_{t \in T} X_t", r"=", r"?: \ \text{a geometric property of } (T, d)", font_size=34),
            cmath(r"|T| = N, \ \mathrm{SD} \le \sigma", r":", r"E\max \le \sigma\sqrt{2\log N}: \ \text{the union bound}", font_size=32),
            cmath(r"\text{correlated } X_t", r":", r"\text{the union bound counts nearly equal variables as different}", font_size=30),
        ]
        rows[2][-1].set_color(BNDC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"Part 48's chaining, \ now Gaussian"), why(r"Sudakov; \ Dudley (1967)"), why(r"one scale only"), why(r"wasteful when points cluster")]
        heading = label('Canonical distances describe a Gaussian supremum', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A centred Gaussian process indexed by a set T, with its canonical metric: the distance "
            "between two indices is the standard deviation of the difference of their variables. <bookmark mark='b'/> The "
            "expected supremum turns out to be a purely geometric property of T in this metric. <bookmark mark='c'/> For N "
            "variables of standard deviation at most sigma, the union bound gives sigma times the root of two log N. "
            "<bookmark mark='d'/> But when the variables are strongly correlated, as at neighbouring times of a continuous "
            "process, the union bound counts nearly identical variables as if they were independent, and badly overestimates."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def dudley(self):
        rows = [
            cmath(r"\pi_k(t)", r":", r"\text{the nearest point to } t \text{ in a } 2^{-k}\text{-net } T_k", font_size=34),
            cmath(r"X_t - X_{t_0}", r"=", r"\textstyle\sum_k \big(X_{\pi_k(t)} - X_{\pi_{k-1}(t)}\big): \ \text{a chain of links}", font_size=32),
            cmath(r"\text{level } k", r":", r"\le |T_k|^2 \text{ links, \ each of SD } \lesssim 2^{-k}: \ \text{union bound per level}", font_size=30),
            cmath(r"E\sup X_t", r"\le", r"C\int_0^{\mathrm{diam}} \sqrt{\log N(T, d, \varepsilon)}\, d\varepsilon", font_size=34),
        ]
        rows[3][-1].set_color(BNDC)
        whys = [why(r"approximations at every scale"), why(r"a telescoping sum"), why(r"coarse: \ few links, \ long"), why(r"Dudley's entropy integral (1967)")]
        heading = label('Successive nets turn proximity into a bound on increments', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Chaining, as in Part forty-eight. Approximate each index t by its nearest point in a net at "
            "scale two to the minus k, for every k. <bookmark mark='b'/> Then the variable at t is a telescoping sum of links "
            "between successive approximations. <bookmark mark='c'/> At level k there are at most the square of the net's size "
            "of distinct links, each with standard deviation of order two to the minus k, so a union bound at each level costs "
            "two to the minus k times the root of the log of the net's size. Coarse levels have few long links; fine levels "
            "many short ones. <bookmark mark='d'/> Adding the levels gives Richard Dudley's entropy integral of 1967: the "
            "expected supremum is at most a constant times the integral of the root log covering number."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("chaining")
        lN = np.log10(d["Ns"])
        A = axes([0.9, 4.1], [0, 4.6], x_length=7.4, y_length=4.4, xlabel=r"grid steps $N$ ($N+1$ points) \ (log scale)", ylabel=r"$E\max_{j \le N} B(j/N)$ \ and bounds",
                 xticks=[1, 2, 3, 4], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[0, 1, 2, 3, 4], center=[-2.5, 0.2, 0])
        ax = A.ax
        cu = VGroup(polyline(ax, lN, d["union"], BADC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=BADC) for a, b in zip(lN, d["union"])])
        cd = VGroup(polyline(ax, lN, d["dudley"], BNDC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=BNDC) for a, b in zip(lN, d["dudley"])])
        cw = VGroup(*[Dot(ax.c2p(a, b), radius=0.1, color=GAUSSC) for a, b in zip(lN, d["walk"])])
        lim = DashedLine(ax.c2p(0.9, d["limit"]), ax.c2p(4.1, d["limit"]), color=EXACTC, stroke_width=2.5)
        dinf = DashedLine(ax.c2p(0.9, d["dudley_inf"]), ax.c2p(4.1, d["dudley_inf"]), color=BNDC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"Brownian motion on a grid of $N$ points; \ $d(s,t) = \sqrt{|s-t|}$", font_size=22),
            label(rf"red: \ the union bound $\sqrt{{2\log(N+1)}}$, \ {d['union'][-1]:.2f} at $10^4$", font_size=22, color=BADC),
            label(rf"blue: \ simulated, \ {d['walk'][-1]:.2f}; \ white: \ $\sqrt{{2/\pi}} = {d['limit']:.3f}$", font_size=22, color=GAUSSC),
            label(rf"purple: \ entropy-rate integral, \ to $\sqrt{{\pi/2}} = {d['dudley_inf']:.3f}$", font_size=22, color=BNDC),
            label(r"chaining stays bounded; \ the union bound does not", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> An example: Brownian motion observed at N equally spaced times on the unit interval. Its canonical distance is the root of the time difference, so an epsilon-net needs about one over epsilon squared points. <bookmark mark='b'/> The union bound, in red, grows without limit: {say(d['union'][-1], 1)} at ten thousand points. <bookmark mark='c'/> The simulated expected maximum, in blue, levels off at the root of two over pi, {say(d['limit'], 2)}, the exact answer from the reflection principle. <bookmark mark='d'/> The entropy-rate integral, in purple, computed down to the grid's resolution, also levels off, at the root of pi over two, {say(d['dudley_inf'], 2)}, before a theorem constant and covering-number discretization corrections. This truncated rate integral alone is not a certified finite-grid upper bound. <bookmark mark='e'/> Chaining sees that the maximum of a continuous process is finite; a single-scale union bound cannot."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ union bound; \ entropy-rate illustration")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cu), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(cw), Create(lim), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cd), Create(dinf), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def sudakov(self):
        d = load("compare")
        rows = [
            cmath(r"\text{a lower bound}", r":", r"\text{if } T \text{ holds } N \text{ points pairwise } \ge \varepsilon \text{ apart}", font_size=32),
            cmath(r"E\sup_T X_t", r"\ge", r"c\,\varepsilon\sqrt{\log N}: \ \text{Sudakov's minoration (1969)}", font_size=34),
            cmath(r"\text{proof}", r":", r"\text{compare with independent } N(0, \varepsilon^2/2) \text{ by Sudakov--Fernique}", font_size=30),
            cmath(r"N = 1{,}000, \ \varepsilon = 1", r":", rf"E\sup \ge \tfrac{{1}}{{\sqrt2}}\, E\max_{{1000}} Z = {d['sudakov']:.2f}", font_size=32),
        ]
        rows[1][-1].set_color(BNDC)
        rows[3][-1].set_color(GAUSSC)
        whys = [why(r"an $\varepsilon$-separated set"), why(r"Dudley's integrand, \ at one scale"), why(r"separated $\Rightarrow$ less correlated"), why(r"exact constant")]
        heading = label('Sudakov--Fernique gives a lower bound from separated points', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> A lower bound in the other direction. Suppose T contains N points that are pairwise at least epsilon apart in the canonical metric. <bookmark mark='b'/> Vladimir Sudakov proved in 1969 that the expected supremum is then at least a constant times epsilon times the root of log N: Epsilon times the entropy integrand is a lower bound at each scale. <bookmark mark='c'/> The proof compares the process with independent normals of variance epsilon squared over two, using the Sudakov–Fernique expectation comparison from the next chapter: separated variables are less correlated, and less correlated variables have a larger maximum. <bookmark mark='d'/> For a thousand points one unit apart, the expected supremum is at least {say(d['sudakov'], 2)}. So Dudley's integral is an upper bound and the largest epsilon times its integrand a lower bound; how far apart they can be is the next question."       ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ellipsoid(self):
        d = load("chaining")
        rows = [[r"dimension $p$"] + [f"{r['p']:,}" for r in d["ell"]],
                [r"$E\sup_{t \in \mathcal E} \langle g, t\rangle$, \ simulated"] + [f"{r['sup']:.2f}" for r in d["ell"]],
                [r"Jensen upper bound $\big(\sum_k a_k^2\big)^{1/2}\asymp\sqrt{\log p}$"] + [f"{r['sqrt_log']:.2f}" for r in d["ell"]],
                [r"Dudley growth proxy $\log p$ (not a computed integral)"] + [f"{r['log']:.2f}" for r in d["ell"]]]
        tab = table_rows(rows, font_size=28, col_buff=0.6, row_buff=0.4, colors=[GREY_B, GAUSSC, EXACTC, BADC])
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.9, 0])
        foot = label(r"the ellipsoid $\mathcal E = \{t: \sum_k k\, t_k^2 \le 1\}$, \ axes $a_k = 1/\sqrt k$", font_size=24, color=GREY_A).move_to([0, -1.2, 0])
        foot2 = label(r"Dudley's integral is off by a factor $\sqrt{\log p}$, \ which grows without bound", font_size=24, color=BADC).move_to([0, -2.0, 0])
        e = d["ell"]
        with self.voiceover(
            f"<bookmark mark='a'/> Dudley's integral is not always sharp. The standard counterexample is an ellipsoid with axes "
            f"one over root k. The supremum of the Gaussian process over it is the length of a weighted Gaussian vector, about "
            f"the root of the sum of the squared axes, which grows like the root of log p: {say(e[0]['sup'], 2)} at ten "
            f"dimensions, {say(e[-1]['sup'], 2)} at ten thousand. <bookmark mark='b'/> But the covering numbers of this "
            f"ellipsoid make Dudley's integral grow like log p itself. <bookmark mark='c'/> So the ratio between the bound and "
            f"the truth grows without limit. The integral treats every scale as if it were spread over all of T, when the set "
            f"is thin in most directions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def generic(self):
        rows = [
            cmath(r"\gamma_2(T, d)", r"=", r"\inf_{(T_k)} \sup_{t} \textstyle\sum_k 2^{k/2}\, d(t, T_k), \ \ |T_0|=1,\ |T_k| \le 2^{2^k}", font_size=32),
            cmath(r"\text{Fernique--Talagrand}", r":", r"c\,\gamma_2(T, d) \le E\sup_T X_t \le C\,\gamma_2(T, d)", font_size=34),
            cmath(r"\text{the difference from Dudley}", r":", r"\text{the nets may adapt to each point } t", font_size=32),
            cmath(r"\text{the moral}", r":", r"\text{the Gaussian supremum is geometry, \ exactly, \ up to constants}", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(SPHC)
        whys = [why(r"Talagrand's functional"), why(r"majorizing measures, \ 1975 and 1987"), why(r"one sum per $t$, \ then a sup"), why(r"Talagrand, \ \emph{Upper and Lower Bounds} (2021)")]
        heading = label('Admissible nets can adapt to different parts of the index set', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The fix, in a glimpse: generic chaining. Instead of integrating covering numbers, choose a sequence of sets, the k-th with at most two to the two to the k points, and measure each point's distances to them. The first net has exactly one point. Talagrand's gamma-two functional is the best possible worst-case sum for a separable process with the required metric regularity. <bookmark mark='b'/> Xavier Fernique proved the upper bound in 1975, and Michel Talagrand proved in 1987 that it is also a lower bound: the expected supremum of a Gaussian process equals gamma two up to universal constants. <bookmark mark='c'/> The only change from Dudley is that the sum over scales is taken for each point separately before the supremum, so the sets can be fine where the set is large and coarse where it is thin. <bookmark mark='d'/> The moral: the size of a Gaussian supremum is a purely geometric quantity, known exactly up to constants. Talagrand received the Abel Prize in 2024, in part for this theorem."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
