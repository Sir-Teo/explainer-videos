from __future__ import annotations

import numpy as np

from videos.stats.stats53.common import *  # noqa: F403


class Bands(VoiceoverScene):
    def construct(self):
        self.card()
        self.polished()
        self.picture()
        self.board()
        self.byn()
        self.lesson()

    def card(self):
        card = chapter_card(9, r"Credible sets that cover", r"Polished tails and inconvenient truths", lit=(2015,), part=PART)
        with self.voiceover("Chapter nine. Credible sets that cover: polished tails and inconvenient truths."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def polished(self):
        rows = [
            cmath(r"\text{polished tail}", r":", r"\sum_{k \ge N} \theta_k^2 \le L \sum_{k = N}^{\rho N} \theta_k^2 \ \text{ for all sufficiently large }N", font_size=32),
            cmath(r"\text{read}", r":", r"\text{the energy at every frequency is visible a little earlier}", font_size=32),
            cmath(r"\text{Szabó, \ van der Vaart \& van Zanten (2015)}", r":", r"\text{EB balls, \ inflated by a constant, \ cover}", font_size=30),
            cmath(r"\text{an inconvenient truth}", r":", r"\text{energy hidden in sparse, \ far-apart blocks}", font_size=32),
        ]
        rows[0][-1].set_color(GOODC)
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"a tail-regularity condition, not identical to self-similarity"), why(r"no hidden roughness"), why(r"\emph{Annals}, \ with discussion"), why(r"fools $\hat\alpha$")]
        heading = label('Tail regularity can support inflated adaptive credible balls', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Botond Szabó, Aad van der Vaart and Harry van Zanten identified the condition in 2015. A truth has a polished tail if the energy beyond any frequency N is at most a constant times the energy in a fixed window just after N. <bookmark mark='b'/> In words: the roughness of the truth at high frequencies is foretold by what is visible a little earlier, so the data can see how smooth the function really is. <bookmark mark='c'/> For such truths, empirical Bayes credible balls, inflated by a fixed constant, have coverage under the theorem's specified tail constants, prior family, inflation and asymptotic regime. <bookmark mark='d'/> An inconvenient truth hides its energy in sparse, widely separated blocks of frequencies. At some sample sizes the data see only smooth parts, empirical Bayes oversmooths, and the ball misses."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        from explainer.stats.kit import bnp as BN
        from videos.stats.stats53.compute import inconvenient_truth

        K = 1024
        k = np.arange(1, K + 1)
        pol = np.abs(BN.sobolev_truth(K, 1.0))
        inc = inconvenient_truth(K, 1.0)
        A = axes([0, 3.1], [-5.2, 0.2], x_length=7.4, y_length=4.4, xlabel=r"frequency $k$ \ ($\log_{10}$)", ylabel=r"$\log_{10}|\theta_k|$",
                 xticks=[0, 1, 2, 3], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[-5, -4, -3, -2, -1, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        lk = np.log10(k)
        dp = VGroup(*[Dot(ax.c2p(a, np.log10(max(b, 1e-6))), radius=0.025, color=GOODC) for a, b in zip(lk[::3], pol[::3]) if b > 1e-5])
        di = VGroup(*[Dot(ax.c2p(a, np.log10(b)), radius=0.03, color=BADC) for a, b in zip(lk, inc) if b > 0])
        side = fit_rows(VGroup(
            label(r"two truths, \ both of smoothness $\beta = 1$", font_size=22),
            label(r"green: \ polished, \ $|\theta_k| = k^{-3/2}|\sin k|$", font_size=22, color=GOODC),
            label(r"red: \ inconvenient: \ blocks $[N_j,2N_j)$, \ $N_j=2^{j(j+1)}$", font_size=22, color=BADC),
            label(r"between blocks, \ nothing: \ the function looks smoother than it is", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two truths of the same smoothness. <bookmark mark='b'/> The polished one has coefficients decaying steadily like k to the minus three halves, modulated by the sine of k. <bookmark mark='c'/> The inconvenient one has the same decay, but only in blocks starting at two to the j times j plus one, with each block ending at twice its start; the multiplicative gaps grow without bound, <bookmark mark='d'/> with nothing in between, so that at some resolutions it looks much smoother than it is."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact coefficients")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dp), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(di), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def board(self):
        rows = board_rows("EB credible ball")
        d = load("board")
        a = [x["achieved"] for x in d["rows"]]
        show_board(self, rows,
                   f"<bookmark mark='a'/> On the Coverage Board, ten thousand observations, three hundred data sets each. The finite-coordinate empirical Bayes credible ball for the polished truth covers {100 * a[0]:.1f} percent, a little short, since without inflation the ball's size and its error are of the same order. <bookmark mark='b'/> For the inconvenient truth it covers {100 * a[1]:.1f} percent: empirical Bayes picked an average smoothness of {say(d['alpha_inc'], 2)}, in this finite-coordinate experiment. Its coverage at one sample size does not prove an asymptotic counterexample. <bookmark mark='c'/> The inflated and uninflated polished rows use the same data sets and calibrated radii. The chosen factor of one point five is a finite experiment, not a universal inflation constant. The finite-coordinate blocked experiment does not prove the infinite-dimensional impossibility theorem. The infinite continuation has growing gaps; its asymptotic behaviour needs the theorem's separate argument.",
                   [("a", [0]), ("b", [1]), ("c", [2])])

    def byn(self):
        d = load("bands")
        ln = np.log10(d["ns"])
        A = axes([2.3, 4.6], [0.4, 1.02], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"coverage, finite $K=1{,}500$ EB ball",
                 xticks=[np.log10(300), 3, np.log10(3000), 4, np.log10(30000)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0.4, 0.6, 0.8, 0.95], center=[-2.5, 0.2, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(2.3, 0.95), ax.c2p(4.6, 0.95), color=GREY_B, stroke_width=2)
        cp = VGroup(polyline(ax, ln, d["polished"], GOODC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=GOODC) for a, b in zip(ln, d["polished"])])
        ci = VGroup(polyline(ax, ln, d["inconvenient"], BADC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=BADC) for a, b in zip(ln, d["inconvenient"])])
        side = fit_rows(VGroup(
            label(r"no inflation; \ 150 data sets at each $n$", font_size=22),
            label(rf"green: \ polished, \ {100 * min(d['polished']):.0f}--{100 * max(d['polished']):.0f}\%: \ short, \ but steady", font_size=22, color=GOODC),
            label(rf"red: \ inconvenient: \ {100 * d['inconvenient'][0]:.0f}\% at $n = 300$, \ {100 * d['inconvenient'][1]:.0f}\% at 1,000", font_size=22, color=BADC),
            label(rf"at 300, \ $\hat\alpha$ averages {d['alpha_inc'][0]:.2f}: \ the hidden block is unseen", font_size=22, color=BADC),
            label(r"coverage depends on where $n$ falls between the blocks", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The same comparison across sample sizes, without inflation. <bookmark mark='b'/> For the polished truth, coverage stays between {100 * min(d['polished']):.0f} and {100 * max(d['polished']):.0f} percent in these finite experiments; an inflation guarantee requires the stated regularity and asymptotic conditions. <bookmark mark='c'/> For the inconvenient truth it swings, {100 * d['inconvenient'][0]:.0f} percent at three hundred observations and {100 * d['inconvenient'][1]:.0f} at a thousand. <bookmark mark='d'/> At three hundred the estimated smoothness averages {say(d['alpha_inc'][0], 2)}: the data have not yet reached the next block of energy, so the function looks smoother than it is. <bookmark mark='e'/> Coverage depends on where n happens to fall relative to the hidden blocks, the finite grid illustrates variation; it does not establish failure for every possible fixed inflation."
        ) as vo:
            self.play(FadeIn(A), FadeIn(nom), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cp), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ci), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"so, \ can you trust a nonparametric credible set?", font_size=28, color=GREY_A),
            label(r"for smooth functionals: \ usually yes \ (chapter 5's BvM)", font_size=26, color=GOODC),
            label(r"for the whole function: \ only with inflation, \ and a condition on the truth", font_size=26, color=BALLC),
            label(r"the condition is untestable in general: \ a frequentist must assume it too \ (Low 1997)", font_size=26, color=BADC),
            label(r"Bayes and frequentism agree: \ honest adaptive bands need an assumption", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So, can a nonparametric credible set be trusted? <bookmark mark='b'/> For smooth functionals, usually yes, by chapter five's Bernstein–von Mises theorems. <bookmark mark='c'/> For a full function, coverage depends on the norm, prior, class and possible inflation; a polished-tail assumption is one route, not the only general possibility. <bookmark mark='d'/> The condition cannot be checked from the data in general. But neither can a frequentist avoid one: Low's theorem concerns supremum-norm bands in specified classes. Adaptive L-two balls have different restrictions and can exist over some limited smoothness ranges. <bookmark mark='e'/> On this point the two schools agree completely. What differs is only where the assumption is written down: in the prior, or in the class of functions over which a frequentist demands coverage, and a careful analysis states it in either case."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
