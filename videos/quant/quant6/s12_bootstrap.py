from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import (ALT, BAD, DATA_C, EST, GOOD, PART, hist_bars, load, predict, real_data,
                                        show_card, tbar)

BOOT_CODE = [
    "def stationary_bootstrap(x, stat, mean_block=12, B=2000, seed=0):",
    "    rng = np.random.default_rng(seed)",
    "    n = len(x)",
    "    p = 1 / mean_block",
    "    out = np.empty(B)",
    "    for b in range(B):",
    "        idx = np.empty(n, int)",
    "        i = rng.integers(n)",
    "        for k in range(n):        # a new block with probability p",
    "            idx[k] = i",
    "            i = rng.integers(n) if rng.random() < p else (i + 1) % n",
    "        out[b] = stat(x[idx])",
]


class Bootstrap(VoiceoverScene):
    def construct(self):
        d = load("boot_demo")
        b = load("bootstrap")
        c = load("boot_coverage")
        self.card()
        self.ribbon(d)
        self.derive()
        self.lab(b, d)
        self.coverage(c)

    def card(self):
        c = chapter_card(11, r"The bootstrap for dependent data", r"How do you resample a history?", part=PART)
        with self.voiceover("Chapter eleven. The bootstrap for dependent data."):
            show_card(self, c)
        self.play(FadeOut(c))

    def ribbon(self, d):
        x = np.asarray(d["x"])
        n = len(x)
        W = 12.4
        w = W / n
        scale = 1.0 / np.abs(x).max()

        def ribbon_of(vals, y0, opacity=0.9):
            return VGroup(*[Line([-W / 2 + (i + 0.5) * w, y0, 0], [-W / 2 + (i + 0.5) * w, y0 + 1.1 * abs(v) * scale, 0],
                                 stroke_width=1.2, color=GOOD if v > 0 else BAD, stroke_opacity=opacity)
                            for i, v in enumerate(vals)])
        top = ribbon_of(x, 1.2)
        tl = label(r"the US market, 1926--2020: 1{,}134 months, bar height $|r_t|$", font_size=20, color=GREY_A).next_to(
            top, UP, buff=0.15).align_to(top, LEFT)
        idx = np.asarray(d["idx"])[0]
        brk = np.flatnonzero(np.diff(idx) != 1) + 1
        starts = np.concatenate([[0], brk])
        ends = np.concatenate([brk, [n]])
        iid_idx = np.random.default_rng(5).integers(0, n, n)
        shred = ribbon_of(x[iid_idx], -1.6)
        sl = label(r"iid bootstrap: months shredded, the calm and stormy seasons lost", font_size=20, color=BAD).next_to(
            shred, DOWN, buff=0.15).align_to(shred, LEFT)
        sr = lambda z: z.mean() / z.std(ddof=1) * np.sqrt(12)  # noqa: E731
        res = MathTex(rf"\widehat{{SR}}^* = {sr(x[idx]):.2f}\quad (\text{{data: }} {d['sr']:.2f})", font_size=28,
                      color=EST).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Bradley Efron's bootstrap, from 1979, lets the sample stand in for the population: resample the one "
            "history you have, many times, and recompute. <bookmark mark='a'/> Here is the market as a ribbon, one bar "
            "per month, height the size of the move. Volatility clusters: 1929, 1974, 1987, 2008. <bookmark mark='b'/> "
            "The ordinary bootstrap draws single months with replacement: the right months, the wrong seasons, storms "
            "shredded into confetti. <bookmark mark='c'/> Hans Künsch's block bootstrap, 1989, resamples whole blocks. "
            "Politis and Romano's stationary bootstrap, 1994, uses blocks of random geometric length, a year on "
            "average, wrapping around, so the resample is stationary. Watch blocks cut and laid end to end. "
            "<bookmark mark='d'/> Its Sharpe ratio is one draw. Do it eight hundred times."
        ) as vo:
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(l_) for l_ in top], lag_ratio=0.001, run_time=2))
            vo.wait_until("b")
            self.play(FadeIn(shred, shift=DOWN * 0.2), FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeOut(shred), FadeOut(sl))
            new = VGroup()
            pos = 0
            anims = []
            for bi, (a, b) in enumerate(zip(starts, ends)):
                seg = idx[a:b]
                blk = VGroup(*[top[j].copy() for j in seg])
                tgt = VGroup(*[Line([-W / 2 + (pos + k + 0.5) * w, -1.6, 0],
                                    [-W / 2 + (pos + k + 0.5) * w, -1.6 + 1.1 * abs(x[j]) * scale, 0],
                                    stroke_width=1.2, color=GOOD if x[j] > 0 else BAD) for k, j in enumerate(seg)])
                pos += len(seg)
                new.add(tgt)
                anims.append(ReplacementTransform(blk, tgt))
            first = anims[:8]
            rest = anims[8:]
            for an in first:
                self.play(an, run_time=0.5)
            self.play(LaggedStart(*rest, lag_ratio=0.02, run_time=max(vo.until("d") - 0.3, 1.5)))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        C_ = {r"\hat\Gamma_0": BAD, r"S": GOOD}
        rows = [cmath(r"\mathrm{Law}(\hat\theta^* - \hat\theta \mid \hat F_n)", r"\approx",
                      r"\mathrm{Law}(\hat\theta - \theta \mid F)", font_size=36, colors=C_),
                cmath(r"\mathrm{Var}^*\big(\sqrt n\,\bar x^*_{iid}\big)", r"=", r"\hat\Gamma_0 \;\neq\; S",
                      font_size=36, colors=C_),
                cmath(r"\mathrm{Var}^*\big(\sqrt n\,\bar x^*_{block}\big)", r"\approx",
                      r"\hat\Gamma_0 + 2\textstyle\sum_{k<\ell}(1 - k/\ell)\,\hat\Gamma_k", font_size=36, colors=C_)]
        whys = [why(r"the plug-in principle: the sample's distribution stands in for the population's"),
                why(r"resampling single months keeps only lag zero of chapter two's long-run variance"),
                why(r"blocks of length $\ell$ keep the autocovariances inside them: a Bartlett-weighted $S$, chapter "
                    r"two again; the block length plays the bandwidth")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.4, buff=1.0, edge=6.8)
        with self.voiceover(
            "Why blocks? The plug-in principle: resampled estimates vary around the sample's estimate as the sample's "
            "estimate varies around the truth, as long as the resampling mimics how the data were generated. "
            "<bookmark mark='a'/> Resample single months and every pair of months in the new series is independent, so "
            "the variance of a mean is only lag zero: chapter two's long-run variance with every autocovariance thrown "
            "away. For a Sharpe ratio, whose noise also depends on how volatility clusters, the same loss applies. "
            "<bookmark mark='b'/> Blocks of length ell keep every autocovariance inside a block. A lag-k pair falls "
            "inside the same block ell minus k times out of ell, so lag k is kept with weight one minus k over ell: "
            "Bartlett's triangle again. The block length is the bandwidth, with the same trade-off: too short loses the "
            "dependence, too long leaves too few blocks to vary."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def lab(self, b, d):
        card = lab_card(r"the stationary bootstrap in the House", BOOT_CODE, source="explainer/quant/house/econ.py",
                        width=7.0, font_size=17).to_corner(UL, buff=0.3)
        outs = [f"stationary_bootstrap(mkt, sharpe, 12, B=800)",
                f"se = {b['se_stationary']:.3f}   (iid {b['se_iid_boot']:.3f}, Lo {b['se_iid']:.3f})"]
        g = axes([0.0, 0.9], [0, 4.2], x_length=5.0, y_length=3.0, xlabel=r"bootstrap Sharpe ratios, annual",
                 xticks=[0, 0.4, 0.8], yticks=[], font_size=15).to_corner(DR, buff=0.4)
        ax = g.ax
        st, iid = np.asarray(d["stationary"]), np.asarray(d["iid"])
        edges = np.linspace(0, 0.9, 37)
        n = ValueTracker(2)
        hs = always_redraw(lambda: hist_bars(ax, st[:int(n.get_value())], edges, EST, opacity=0.65, cap=4.2))
        hi = hist_bars(ax, iid, edges, BAD, opacity=0.35, cap=4.2)
        leg = legend([(EST, rf"stationary, se {d['se_st']:.3f}"), (BAD, rf"iid, se {d['se_iid']:.3f}")],
                     font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        with self.voiceover(
            "The House's stationary bootstrap: start anywhere; each step, with probability one over the mean block "
            "length, jump to a random month, else take the next one, wrapping around the end. Recompute the statistic "
            "on the new history, and repeat. <bookmark mark='a'/> On the market's Sharpe ratio, eight hundred times: a "
            f"standard error of {b['se_stationary']:.3f}, against {b['se_iid_boot']:.3f} for the iid bootstrap and "
            f"{b['se_iid']:.3f} from Lo's formula. The clustering of volatility makes the Sharpe ratio a fifth less "
            "certain than independent months suggest. <bookmark mark='b'/> After ninety-four years, the market's "
            "Sharpe ratio is known only to within about a quarter either way."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(leg))
            self.add(hs)
            self.play(n.animate.set_value(len(st)), run_time=3, rate_func=rate_functions.ease_in_quad)
            self.play(FadeIn(hi))
            lab_run(self, card, outs, run_time=1.6, direction=DOWN)
            vo.wait_until("b")
        hs.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def coverage(self, c):
        cov = c["cover"]
        g = axes([0, 3], [0.8, 1.0], x_length=6.0, y_length=4.0, ylabel=r"how often the 95\% interval covers the truth",
                 xticks=[], yticks=[0.8, 0.85, 0.9, 0.95, 1.0], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        names = [("iid", r"iid"), ("block", r"moving block (12)"), ("stationary", r"stationary (12)")]
        cols = [BAD, ALT, EST]
        bars = VGroup(*[tbar(ax, i + 0.5, cov[k], col, width=0.55, lo=0.8) for i, ((k, _), col) in
                        enumerate(zip(names, cols))])
        vals = VGroup(*[MathTex(f"{100 * cov[k]:.1f}\\%", font_size=24, color=col).next_to(b, UP, buff=0.06)
                        for (k, _), col, b in zip(names, cols, bars)])
        labs = VGroup(*[label(t, font_size=18, color=GREY_B).next_to(ax.c2p(i + 0.5, 0.8), DOWN, buff=0.12)
                        for i, (_, t) in enumerate(names)])
        nominal = DashedLine(ax.c2p(0, 0.95), ax.c2p(3, 0.95), color=GOOD, stroke_width=2)
        side = VGroup(
            label(rf"{c['paths']:,} simulated markets of {c['n']:,} months".replace(",", "{,}"), font_size=21,
                  color=GREY_A),
            label(r"AR(1) returns ($\phi = 0.1$) with GARCH(1,1) shocks", font_size=21, color=GREY_A),
            MathTex(rf"\text{{true monthly Sharpe }} {c['sr_true']}", font_size=26),
            MathTex(rf"\text{{true sd of }} \widehat{{SR}}: {c['true_sd']:.4f}", font_size=26, color=GOOD),
            MathTex(rf"\text{{mean bootstrap se: iid }} {c['se_mean']['iid']:.4f},\ \text{{stationary }} "
                    rf"{c['se_mean']['stationary']:.4f}", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        gap_iid = 0.95 - cov["iid"]
        gap_st = 0.95 - cov["stationary"]
        closes = gap_iid - gap_st
        verdict = (f"Blocks help, closing about {100 * closes / gap_iid:.0f} percent of the gap, but neither reaches "
                   "ninety-five: year-long blocks are too short for volatility this persistent."
                   if 0 < closes < gap_iid else "Here the blocks do not help.")
        q = predict(r"Block length equal to the whole sample: what is the bootstrap standard error?").to_edge(DOWN,
                                                                                                      buff=0.15)
        with self.voiceover(
            "Does it work? A thousand simulated markets as long as ours, slightly autocorrelated, volatility "
            "clustering, true monthly Sharpe of an eighth; build each bootstrap's nominal ninety-five percent interval. "
            f"<bookmark mark='a'/> The iid bootstrap covers the truth {100 * cov['iid']:.1f} percent of the time, the "
            f"moving block {100 * cov['block']:.1f}, the stationary {100 * cov['stationary']:.1f}. {verdict} "
            "<bookmark mark='b'/> Pause and predict: a block the length of the sample? Every resample is the sample "
            "rotated: a standard error of zero."
        ) as vo:
            self.play(FadeIn(g), Create(nominal), FadeIn(labs), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(v)) for b, v in zip(bars, vals)],
                                  lag_ratio=0.5, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
