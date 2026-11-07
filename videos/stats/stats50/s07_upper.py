from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class UpperBounds(VoiceoverScene):
    def construct(self):
        self.card()
        self.estimators()
        self.whyjs()
        self.chart()
        self.table()
        self.oracle()
        self.besov()

    def card(self):
        card = chapter_card(6, r"Upper bounds that match", r"Blockwise James--Stein and thresholding", part=PART)
        with self.voiceover("Chapter six. Upper bounds that match: blockwise James–Stein and thresholding."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def estimators(self):
        rows = [
            cmath(r"\text{Pinsker's rule}", r":", r"\text{needs } \alpha \text{ and } C: \ \text{the class must be known}", font_size=32),
            cmath(r"\text{blocks } B_j = \{2^j, \dots, 2^{j+1} - 1\}", r":", r"\hat\theta_{B} = \Big(1 - \frac{\varepsilon^2 |B|}{\|y_B\|^2}\Big)_+ y_B", font_size=32),
            cmath(r"\text{soft thresholding}", r":", r"\hat\theta_k = \mathrm{sign}(y_k)(|y_k| - \varepsilon\sqrt{2 \log K})_+", font_size=32),
            cmath(r"\text{both}", r":", r"\text{unknown smoothness; noise and truncation still needed}", font_size=34),
        ]
        rows[1][-1].set_color(ADAPTC)
        rows[2][-1].set_color(UPC)
        whys = [why(r"chapter 2"), why(r"Efromovich \& Pinsker (1984); \ Cai (1999)"), why(r"Donoho \& Johnstone (1994)"), why(r"adaptive estimators")]
        heading = label('Unknown smoothness still requires a noise level and an estimator design', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Pinsker's rule attains the exact linear minimax risk and the asymptotic unrestricted minimax constant, but only if we know the smoothness alpha and the radius C, which we never do. <bookmark mark='b'/> Blockwise James–Stein groups the coefficients into dyadic blocks and uses a positive-part block energy shrinker with numerator m epsilon squared. This moment-based rule differs from the classical m minus two James–Stein factor and includes small blocks where domination is not claimed, letting the data in the block decide how much to shrink. <bookmark mark='c'/> Soft thresholding, from Part twenty-nine's wavelets, kills every coefficient below a universal threshold and shrinks the rest. <bookmark mark='d'/> Neither needs to know the class, and appropriate block rules can be rate-adaptive, while universal thresholding may pay a logarithmic factor. They need the noise level and truncation dimension, even when smoothness is unknown. That property, adaptation, is the next chapter's subject."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def whyjs(self):
        rows = [
            cmath(r"\text{on a block } B \text{ of size } m", r":", r"\text{nearly constant only on narrow relative blocks}", font_size=32),
            cmath(r"\text{the best constant}", r":", r"c_B = \frac{\|\theta_B\|^2}{\|\theta_B\|^2 + m\varepsilon^2}: \ \text{an oracle shrinkage}", font_size=32),
            cmath(r"\text{James--Stein estimates it}", r":", r"1 - \frac{m \varepsilon^2}{\|y_B\|^2}, \ \ \text{error depends on signal and block size}", font_size=32),
            cmath(r"\text{blocks that grow}", r"\Rightarrow", r"\text{the oracle's risk, \ to first order: \ adaptation by averaging}", font_size=30),
        ]
        rows[1][-1].set_color(LINC)
        rows[2][-1].set_color(ADAPTC)
        whys = [why(r"a taper is flat locally"), why(r"the best constant per block"), why(r"Part 25's estimator, \ blockwise"), why(r"why it adapts")]
        heading = label('Refined blocks can approximate oracle shrinkage', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Why does blockwise James–Stein adapt? On sufficiently narrow relative blocks, Pinsker's taper can be approximated by a constant. Dyadic blocks have fixed relative width, so this is not a proof of exact first-order adaptation for the simple rule shown. <bookmark mark='b'/> The best constant for the block is the block's signal energy over its energy plus m epsilon squared, an oracle shrinkage that depends on the unknown parameter. <bookmark mark='c'/> But James–Stein estimates exactly that ratio from the block's own data, with fluctuations whose size depends on the block dimension and signal energy. A uniform relative-error claim fails when the oracle shrinkage is zero. <bookmark mark='d'/> When the blocks grow, those errors vanish, and carefully refined blocks and appropriate regularization can inherit the oracle's risk to first order. The dyadic illustration is not itself that sharp theorem. It adapts by averaging within blocks, Part twenty-five's borrowing of strength put to work in infinite dimensions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("upper")
        le = np.log10([r["eps"] for r in d["rows"]])
        A = axes([-2.6, -1.2], [-3.6, -1.0], x_length=7.4, y_length=4.4, xlabel=r"noise level $\varepsilon$ \ (log scale)", ylabel=r"$\log_{10}$ risk",
                 xticks=[np.log10(0.003), np.log10(0.008), np.log10(0.02), np.log10(0.05)], xfmt=lambda v: f"{10 ** v:.3f}", yticks=[-3.5, -3, -2.5, -2, -1.5, -1], center=[-2.5, 0.2, 0])
        ax = A.ax

        def line(key, c):
            y = np.log10([r[key] for r in d["rows"]])
            return VGroup(polyline(ax, le, y, c, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=c) for a, b in zip(le, y)])

        cb, cp, cj, cs, ct = line("bound", LOWC), line("pinsker", LINC), line("bjs", ADAPTC), line("soft", UPC), line("trunc_best", S.ALT)
        cb = VGroup(DashedVMobject(cb[0], num_dashes=30), *cb[1:])
        side = fit_rows(VGroup(
            label(r"Sobolev $\alpha = 1$, \ one $\theta$ worst for Pinsker, not necessarily other rules", font_size=22),
            label(r"red dashed: \ $R_L$; \ purple: \ Pinsker's rule", font_size=22, color=LOWC),
            label(r"teal: \ the best truncation, \ told the truth", font_size=22, color=S.ALT),
            label(r"green: \ blockwise James--Stein, \ told nothing", font_size=22, color=ADAPTC),
            label(r"blue: \ soft thresholding: \ a log factor worse here", font_size=22, color=UPC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Sobolev ball with one derivative, and one boundary parameter that is worst for Pinsker's linear rule. It need not be worst for every other estimator. <bookmark mark='b'/> In red, the exact linear minimax value as the noise shrinks, and in purple his estimator's simulated risk, on top of it. <bookmark mark='c'/> In teal, the best projection estimator, with the cut-off chosen knowing the truth: a constant factor worse than Pinsker's taper. <bookmark mark='d'/> In green, blockwise James–Stein, told nothing about the class: its simulated risk at this selected truth approaches the linear minimax benchmark across the shown noise levels. This does not measure its supremum risk over the ellipsoid. <bookmark mark='e'/> In blue, soft thresholding at the universal threshold, which pays a logarithmic factor for this kind of dense, smooth signal: it is built for sparsity, and over Sobolev balls it is not quite rate-optimal."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated: \ 300 samples; \ red exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cp), Create(cb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ct), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cj), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(cs), FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("upper")
        rows = [[r"$\varepsilon$", r"$R_L$ \ (linear minimax)", r"Pinsker's rule", r"best truncation", r"block JS", r"soft"]]
        for r in d["rows"]:
            b = r["bound"]
            rows.append([f"{r['eps']:g}", f"{b:.2e}", f"{r['pinsker'] / b:.2f}", f"{r['trunc_best'] / b:.2f}", f"{r['bjs'] / b:.2f}", f"{r['soft'] / b:.2f}"])
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.36, colors=[GREY_B] + [None] * 4)
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.8, 0])
        for i in range(1, 5):
            tab[i][4].set_color(ADAPTC)
        foot = label(r"risk at one truth divided by $R_L$; \ not a worst-case comparison", font_size=24, color=GREY_A).move_to([0, -1.5, 0])
        last = d["rows"][-1]
        foot2 = label(rf"blockwise James--Stein: \ {last['bjs'] / last['bound']:.2f} at $\varepsilon = {last['eps']}$, \ without knowing $\alpha$ or $C$", font_size=24, color=ADAPTC).move_to([0, -2.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> As ratios of selected-truth risk to the linear minimax benchmark, rather than unrestricted finite-noise minimax risks. Pinsker's rule is at one, as it should be. The best truncation, told the truth, is about one point four. Blockwise James–Stein starts at {say(d['rows'][0]['bjs'] / d['rows'][0]['bound'], 1)} at the largest noise level and falls to {say(last['bjs'] / last['bound'], 2)} at the smallest. <bookmark mark='b'/> It comes within about a fifth of the minimax risk without being told the smoothness or the radius. With slowly growing blocks instead of dyadic ones it is asymptotically exact, constant included, as Laurent Cavalier and Alexandre Tsybakov showed in 2002."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def oracle(self):
        rows = [
            cmath(r"\text{the oracle}", r":", r"\textstyle\sum_k \min(\theta_k^2, \varepsilon^2): \ \text{keep or kill each coefficient, \ knowing } \theta", font_size=30),
            cmath(r"E\|\hat\theta_{\text{soft}} - \theta\|^2", r"\le", r"(2 \log K + 1)\big(\varepsilon^2 + \textstyle\sum_k \min(\theta_k^2, \varepsilon^2)\big)", font_size=30),
            cmath(r"\text{SURE (Part 25)}", r":", r"\text{the threshold by Stein's risk estimate}", font_size=34),
            cmath(r"\text{oracle inequality}", r":", r"\text{near the best rule, \ for every } \theta", font_size=34),
        ]
        rows[1][-1].set_color(UPC)
        rows[2][-1].set_color(ADAPTC)
        whys = [why(r"an ideal, \ not an estimator"), why(r"Donoho \& Johnstone (1994)"), why(r"SureShrink (1995)"), why(r"the modern form of minimaxity")]
        heading = label('An oracle inequality compares risk uniformly over parameters', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A different way to judge an estimator is against an oracle: someone who knows theta and "
            "for each coordinate decides whether to keep it or set it to zero, paying the smaller of theta k squared and the "
            "noise variance. <bookmark mark='b'/> Donoho and Johnstone proved that soft thresholding at the universal "
            "threshold comes within a factor of two log K plus one of that oracle, for every theta at once. <bookmark "
            "mark='c'/> Choosing the threshold by minimizing Stein's unbiased risk estimate, Part twenty-five's SURE, removes "
            "the log factor for many signals. <bookmark mark='d'/> Such oracle inequalities, within a constant or a log of the "
            "best rule in a whole family for every parameter, are how modern theory states that an estimator adapts."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def besov(self):
        rows = fit_rows(VGroup(
            label(r"Sobolev balls: \ smooth everywhere: \ linear rules suffice, \ block JS adapts", font_size=26),
            label(r"Besov balls $B^s_{p,q}$ with $p < 2$: \ smooth with a few jumps, \ spikes, \ sparse wavelet coefficients", font_size=26, color=UPC),
            label(r"in suitable $L_2$-embedded regimes, linear rules are rate-suboptimal: \ Donoho \& Johnstone (1998)", font_size=26, color=LOWC),
            label(r"wavelet thresholding is near-minimax over the whole Besov scale: \ one estimator, \ many classes", font_size=26, color=ADAPTC),
            label(r"the moral: \ match the estimator to the geometry of the class", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Over the specified Sobolev ellipsoids, linear shrinkage is enough, and blockwise James–Stein adapts. <bookmark mark='b'/> Over Besov balls with p below two, functions that are smooth except for a few jumps or spikes, the wavelet coefficients are sparse. <bookmark mark='c'/> There, as David Donoho and Iain Johnstone showed in 1998, linear estimators can be rate-suboptimal in the relevant L-two-embedded Besov regimes. The precise smoothness, integrability and loss conditions matter. <bookmark mark='d'/> Wavelet thresholding is near-minimax over suitable Besov classes embedded in the specified loss space, with the theorem's wavelet and parameter restrictions. <bookmark mark='e'/> The moral: the shape of the class, round or spiky, decides which estimator can be optimal."       ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
