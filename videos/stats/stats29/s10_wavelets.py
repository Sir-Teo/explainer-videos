from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class Wavelets(VoiceoverScene):
    def construct(self):
        self.card()
        self.haar()
        self.signals()
        self.coefficients()
        self.threshold()
        self.maxima()
        self.denoise()
        self.scores()

    def card(self):
        card = chapter_card(9, r"Wavelets", r"Sparse in the right basis", lit=(1994,), part=PART)
        with self.voiceover("Chapter nine. Wavelets."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def haar(self):
        rows = [
            cmath(r"\psi_{jk}(t)", r"=", r"2^{j/2} \psi(2^j t - k)", font_size=32),
            cmath(r"\text{Haar}", r":", r"\psi = +1 \text{ then } -1 \text{ on } [0, 1)", font_size=30),
            cmath(r"y", r"=", r"\textstyle\sum_k s_k \phi_{Jk} + \sum_{j, k} d_{jk} \psi_{jk}", font_size=30),
            cmath(r"\text{orthonormal}", r":", r"\text{white noise stays white}, \ \ O(n) \text{ to compute}", font_size=28),
        ]
        rows[2][2].set_color(WAVC)
        whys = [why(r"dilate by $2^j$, \ shift by $k$"), why(r"Haar (1910); \ smoother: \ Daubechies (1988)"),
                why(r"a coarse picture plus details at every scale"), why(r"Mallat's pyramid")]
        with self.voiceover(
            "<bookmark mark='a'/> Basic fixed-bandwidth kernels and fixed-penalty splines use global tuning. Wavelet "
            "thresholding offers another way to adapt locally. A wavelet basis is one small wave, dilated by powers "
            "of two and shifted along. <bookmark mark='b'/> The simplest is Alfréd Haar's of 1910, a step up then "
            "down; Ingrid Daubechies built smooth ones in 1988, and statkit uses her four-tap filter. <bookmark "
            "mark='c'/> Any signal is a coarse picture plus detail coefficients at every scale and location. "
            "<bookmark mark='d'/> the periodic basis is orthonormal, so iid Gaussian noise maps to iid Gaussian noise"
            " with the same variance, and Stéphane Mallat's pyramid computes it in order n."        ) as vo:
            intro=label('An orthonormal basis separates a coarse signal from local details',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def signals(self):
        d = load("wavelets")["signals"]
        n = 1024
        t = np.arange(n) / n
        panels = VGroup()
        for k, name in enumerate(("blocks", "bumps", "heavisine", "doppler")):
            f = np.asarray(d[name]["f"])
            y = np.asarray(d[name]["y"])
            lo, hi = float(min(y.min(), f.min())), float(max(y.max(), f.max()))
            A = axes([0, 1], [lo, hi], x_length=5.6, y_length=2.2, xlabel=r"", ylabel=r"", xticks=[], yticks=[],
                     center=[-3.2 + 6.4 * (k % 2), 1.7 - 3.2 * (k // 2), 0])
            ax = A.ax
            noisy = polyline(ax, t[::2], y[::2], GREY_B, 1, 0.6)
            truth = polyline(ax, t, f, TRUE, 2.5)
            tl = label(name, font_size=22, color=TRUE).next_to(A, UP, buff=0.05)
            panels.add(VGroup(A, noisy, truth, tl))
        with self.voiceover(
            "<bookmark mark='a'/> David Donoho and Iain Johnstone's four test signals, each sampled at a thousand and "
            "twenty-four points and scaled to signal-to-noise ratio seven: blocks, with jumps; <bookmark mark='b'/> bumps, "
            "with sharp spikes; <bookmark mark='c'/> heavisine, a sine wave with two breaks; <bookmark mark='d'/> and the "
            "Doppler, oscillating faster and faster towards the left. Grey is the signal plus unit noise. No single bandwidth "
            "suits any of them."
        ) as vo:
            self.add(seeded_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(panels[k][0]), FadeIn(panels[k][3]), Create(panels[k][1]), Create(panels[k][2]))
        self.clear_scene()

    def coefficients(self):
        d = load("wavelets")["signals"]["blocks"]
        cy = [np.asarray(c) for c in d["coefs_y"]]
        cf = [np.asarray(c) for c in d["coefs_f"]]
        levels = len(cy)
        A = axes([0, 1], [0, levels + 0.5], x_length=9.0, y_length=4.8, xlabel=r"location", ylabel=r"scale (fine at the top)",
                 xticks=[], yticks=[], center=[-1.4, 0.2, 0])
        ax = A.ax
        sticks_f, sticks_y = VGroup(), VGroup()
        for j, (a, b) in enumerate(zip(cf, cy)):
            m = len(a)
            base = j + 0.5
            for k in range(m):
                xk = (k + 0.5) / m
                for v, grp, col, sw in ((b[k], sticks_y, GREY_B, 1.2), (a[k], sticks_f, WAVC, 2.0)):
                    hgt = float(np.clip(v / 12.0, -0.45, 0.45))
                    if abs(hgt) > 0.004:
                        grp.add(Line(ax.c2p(xk, base), ax.c2p(xk, base + hgt), color=col, stroke_width=sw))
        rows = fit_rows(VGroup(
            label(r"blocks: \ detail coefficients; sticks vertically clipped", font_size=22),
            label(rf"purple: \ the signal's: \ {d['big_coefs']} of 1,016 large", font_size=22, color=WAVC),
            label(r"grey: \ the noisy data's: \ noise everywhere", font_size=22, color=GREY_B),
            label(r"sparse signal, \ dense noise", font_size=22, color=PATH),
        ), 3.4, 0.42, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why wavelets work: look at the blocks signal's detail coefficients, coarse scales "
            "at the bottom, fine at the top. <bookmark mark='b'/> The signal's own coefficients are sparse: only "
            "seventy-six of about a thousand exceed the unit-noise universal threshold, clustered at the jumps. The "
            "sticks are vertically clipped for display; the count uses the original coefficients. <bookmark "
            "mark='c'/> The noise spreads evenly over every coefficient, because the basis is orthonormal. <bookmark "
            "mark='d'/> So keep the big coefficients and kill the small ones."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(sticks_f), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(sticks_y), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeOut(sticks_y), FadeIn(rows[3]))
        self.clear_scene()

    def threshold(self):
        rows = [
            cmath(r"\eta_t(d)", r"=", r"\mathrm{sign}(d)\, (|d| - t)_+", font_size=32),
            cmath(r"\hat\sigma", r"=", r"\mathrm{median}|d_{\text{finest}}| / 0.6745", font_size=30),
            cmath(r"t_{\text{universal}}", r"=", r"\hat\sigma \sqrt{2 \log n}", font_size=32),
            cmath(r"\text{SureShrink}", r":", r"t_j = \arg\min_t \mathrm{SURE}(t) \text{ at each scale}", font_size=30),
        ]
        rows[2][2].set_color(WAVC)
        whys = [why(r"soft thresholding: \ shrink, \ or kill"), why(r"requires little signal in the finest details"),
                why(r"VisuShrink: \ Donoho \& Johnstone (1994)"), why(r"Part 25's Stein estimate: \ Donoho \& Johnstone (1995)")]
        with self.voiceover(
            "<bookmark mark='a'/> Soft thresholding: coefficients below t are set to zero, the rest pulled towards "
            "zero by t. <bookmark mark='b'/> If the finest detail scale is mostly Gaussian noise, its median absolute"
            " coefficient divided by point six seven four five estimates sigma. Fine-scale signal can contaminate "
            "this estimate. <bookmark mark='c'/> VisuShrink uses one universal threshold, sigma times root two log n."
            " <bookmark mark='d'/> SureShrink chooses a threshold at each scale by minimizing Stein's unbiased risk "
            "estimate, Part 25's SURE, falling back to the universal one where the coefficients look sparse."
        ) as vo:
            intro=label('Thresholding trades coefficient noise against shrinkage bias',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def maxima(self):
        d = load("wavelets")["max_normals"]
        hdr = [r"\textbf{$n$ independent $N(0, 1)$}", r"\textbf{median of the largest $|z|$}", r"\textbf{90\% point}",
               r"\textbf{$\sqrt{2 \log n}$}"]
        body = [[f"{int(k):,}", f"{v['median']:.2f}", f"{v['q90']:.2f}", f"{v['bound']:.2f}"] for k, v in d.items()]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.3, colors=[GREY_A] + [None] * 5)
        for r in tb[1:]:
            r[3].set_color(WAVC)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"$P(\max_i |z_i| > \sqrt{2 \log n}) \to 0$: \ known $\sigma$: noise killed with probability tending to one", font_size=22),
            label(r"finite-sample exceedances remain possible; \ retained coefficients are also shrunk", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Where root two log n comes from: it is the size of the largest of n independent "
            "standard normals. <bookmark mark='b'/> In two hundred simulations at each n, the largest absolute value "
            "sits just below it, and the chance of exceeding it shrinks to zero. So the universal threshold kills "
            "pure noise with high probability, a known-noise asymptotic statement, not a literal guarantee of "
            "smoothness or of zero false retained coefficients at every finite sample size. At n of a thousand and "
            "twenty-four, a unit-noise threshold is about three point seven."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), FadeIn(foot[1]), run_time=3.0)
        self.wait(1.0)
        self.clear_scene()

    def denoise(self):
        d = load("wavelets")["signals"]["blocks"]
        n = 1024
        t = np.arange(n) / n
        f, y = np.asarray(d["f"]), np.asarray(d["y"])
        A = axes([0, 1], [-10, 22], x_length=9.0, y_length=4.4, xlabel=r"$t$", ylabel=r"", xticks=[0, 0.5, 1], yticks=[],
                 center=[-1.4, 0.3, 0])
        ax = A.ax
        noisy = polyline(ax, t[::2], y[::2], GREY_D, 1)
        truth = polyline(ax, t, f, TRUE, 2)
        sp = polyline(ax, t, np.asarray(d["spline"]), SPLC, 2.5)
        su = polyline(ax, t, np.asarray(d["sure"]), WAVC, 2.5)
        rows = fit_rows(VGroup(
            label(r"blocks, \ noisy", font_size=22, color=GREY_B),
            label(rf"green: \ GCV spline, \ df {d['spline_df']:.0f}: \ ringing at the jumps", font_size=22, color=SPLC),
            label(r"purple: \ SureShrink: \ sharp jumps, \ flat steps", font_size=22, color=WAVC),
        ), 3.4, 0.42, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the blocks. <bookmark mark='b'/> The best spline, chosen by GCV, needs three hundred and "
            "fifty degrees of freedom to follow the jumps, and so it rings with noise along every flat step. "
            "<bookmark mark='c'/> SureShrink keeps the jumps sharp and the steps flat, because it spends its coefficients "
            "only where the signal changes."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(noisy), Create(truth))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(sp), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeOut(sp), Create(su), FadeIn(rows[2]))
        self.clear_scene()

    def scores(self):
        d = load("wavelets")["signals"]
        hdr = [r"\textbf{signal}", r"\textbf{noisy}", r"\textbf{VisuShrink}", r"\textbf{SureShrink}", r"\textbf{GCV spline}"]
        body = [[k, f"{v['mse']['noisy']:.2f}", f"{v['mse']['visu']:.2f}", f"{v['mse']['sure']:.2f}", f"{v['mse']['spline']:.2f}"]
                for k, v in d.items()]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.32, colors=[GREY_A] + [None] * 4)
        for r in tb[1:]:
            r[2].set_color(GREY_B)
            r[3].set_color(WAVC)
            r[4].set_color(SPLC)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"one noise realization per signal; \ $n = 1{,}024$, \ noise SD 1, \ SNR 7", font_size=22),
            label(r"wavelets win where the signal jumps; \ the spline holds its own where it is smooth", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The scores, as mean squared error per point; the noise alone scores one. <bookmark "
            "mark='b'/> VisuShrink is too conservative at this high signal-to-noise ratio: shrinking every large "
            "coefficient by three point seven costs it more than it saves on blocks, bumps and Doppler. <bookmark "
            "mark='c'/> SureShrink is best on blocks and bumps, which jump and spike. <bookmark mark='d'/> On the "
            "piecewise smooth heavisine its error is close to the spline's, and on the Doppler, smooth but with "
            "changing frequency, the spline edges it. Appropriately chosen wavelet procedures achieve adaptive "
            "near-minimax bounds over specified Besov smoothness classes. This single noise realization illustrates "
            "behavior, rather than proving a universal ranking."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(VGroup(r[0], r[1])) for r in tb[1:]], lag_ratio=0.2), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[2]) for r in tb[1:]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r[3]) for r in tb[1:]], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r[4]) for r in tb[1:]], lag_ratio=0.2), FadeIn(foot[1]))
        self.clear_scene()
