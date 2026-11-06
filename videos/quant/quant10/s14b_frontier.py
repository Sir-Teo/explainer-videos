from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import FullRangeReplay, GAIN, IMP, LOSS, OPT, PART, QQ, SPOT, computed, load


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.race()
        self.replay(load("neural_iv"))
        self.papers()

    def card(self):
        c = chapter_card(19, r"Frontier: 2023 to 2026", r"What is still new about a fifty-year-old formula?",
                         lit=(2024, 2025), part=PART)
        with self.voiceover("Chapter nineteen. Frontier: 2023 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def race(self):
        cards = VGroup(*[VGroup(label(a, font_size=24, color=c), wrapped_label(b, 5.6, 20, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08) for a, b, c in (
            (r"Schadner (arXiv 2604.24480, 2026)", r"implied volatility in closed form, as a quantile of the "
             r"inverse-Gaussian distribution; reported faster than a standard solver on one benchmark", IMP),
            (r"Le Floc'h and Healy (arXiv 2605.29102, 2026)", r"``Implying volatility: how fast can we go?'': "
             r"a fast solver, FlashIV", IMP),
            (r"Saqur, Limmer, Kratsios, Horvath, Buehler (arXiv 2606.17065)", r"PIVOT: J\"ackel's solver as a "
             r"differentiable layer; 1.79 billion inversions a second on one GPU, at machine precision "
             r"(the authors' figures)", OPT),
            (r"Amiriyan and Boutaib (arXiv 2609.05491, 2026)", r"a gated neural network gives the first guess; two "
             r"Householder steps finish to near machine precision", QQ),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.6)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6).to_edge(LEFT, buff=0.6)
        pre = note(r"arXiv preprints: not yet peer reviewed", font_size=20, color=LOSS).to_corner(DR, buff=0.3)
        lean = VGroup(label(r"Ushakov and Berdinsky (arXiv 2608.19223, 2026)", font_size=22, color=GAIN),
                      wrapped_label(r"the call price derived from the Gaussian kernel, chapter 3's road, and checked "
                                    r"by machine in Lean 4 and Mathlib", 4.8, 20, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        with self.voiceover(
            "Fifty years on, chapter eleven's problem is still a race. In 2026 alone: Schadner wrote "
            "implied volatility in closed form, as a quantile of the inverse-Gaussian distribution. Fabien Le "
            "Floc'h and Jherek Healy asked how fast it can go. <bookmark mark='a'/> A team including Blanka "
            "Horvath and Hans Buehler wrapped Peter Jaeckel's solver as a differentiable layer that inverts, by "
            "their count, one point seven nine billion quotes a second on one graphics card. And Samira Amiriyan "
            "and Youness Boutaib trained a gated neural network to give the first guess, finished by two "
            "Householder steps. <bookmark mark='b'/> Even the derivation is new again: chapter three's road, from "
            "the Gaussian kernel to the call price, has now been checked line by line by a computer proof "
            "assistant. All of these are preprints: read them as claims, not settled results."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.2) for c_ in cards[:2]], lag_ratio=0.5, run_time=3),
                      FadeIn(pre))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.2) for c_ in cards[2:]], lag_ratio=0.5, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(lean, shift=LEFT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self, nv):
        ep = np.asarray(nv["epochs"], float)
        loss = np.asarray(nv["loss"], float)
        iv = np.asarray(nv["iv"], float)
        snaps = nv["snaps"]
        keys = sorted(snaps, key=lambda s_: int(s_))
        ck = [max(int(k_), int(ep[0])) for k_ in keys]

        def frame(i):
            g = axes(np.log10([0.3, 1.2]), np.log10([0.2, 22]), x_length=4.2, y_length=3.6,
                     xlabel=r"input quote IV (log scale)", ylabel=r"seed 0 guess (log scale)",
                     xticks=np.log10([0.4, 0.8, 1.2]), yticks=np.log10([0.2, 1, 5, 20]),
                     xfmt=lambda v: f"{100 * 10**v:.0f}\\%", yfmt=lambda v: f"{100 * 10**v:.0f}\\%", font_size=15)
            p = np.asarray(snaps[keys[i]], float)
            diag = DashedLine(g.ax.c2p(np.log10(0.3), np.log10(0.3)),
                              g.ax.c2p(np.log10(1.2), np.log10(1.2)), color=GREY_B, stroke_width=1.2)
            pts = VGroup(*[Dot(g.ax.c2p(np.log10(a), np.log10(b)), radius=0.025, color=QQ, fill_opacity=0.8)
                          for a, b in zip(iv, p)])
            return VGroup(g, diag, pts)

        rp = FullRangeReplay(ep, loss, frame, ck, ylabel=r"training loss (log)", xlabel=r"epoch", log_y=True)
        rp.scale(0.88).shift(UP * 0.25)  # the bottom strip holds the results
        fin = nv["final"]

        def sci(v):  # 1.2e-05 as 1.2 x 10^{-5}
            m, e = f"{v:.1e}".split("e")
            return rf"{m}\times 10^{{{int(e)}}}"
        g0 = np.median([f["guess_med"] for f in fin])
        g1 = np.median([f["one_med"] for f in fin])
        g2max = max(f["two_max"] for f in fin)
        title = label(r"Lab: a learned first guess for implied volatility, 5 seeds", font_size=26, color=QC.HOUSE)
        title.to_edge(UP, buff=0.3)
        res = VGroup(
            MathTex(rf"\text{{guess: median error}}\ {100 * g0:.2f}\ \text{{vol pts}}", font_size=26, color=QQ),
            MathTex(rf"\text{{Corrado--Miller: median}}\ {100 * nv['cm_med']:.2f}", font_size=26, color=GREY_A),
            MathTex(rf"\text{{after 1 Newton step: median}}\ {100 * g1:.3f}", font_size=26, color=GAIN),
            MathTex(rf"\text{{after 2: median}}\ {sci(100 * np.median([f['two_med'] for f in fin]))},\ \text{{worst}}\ "
                    rf"{100 * g2max:.1f}", font_size=26, color=GAIN),
        ).arrange_in_grid(rows=2, cols=2, col_alignments="ll", buff=(0.6, 0.12)).to_edge(DOWN, buff=0.25)
        better = g0 < nv["cm_med"]
        cmp_word = "smaller than" if better else "no better than"
        g2med = np.median([f["two_med"] for f in fin])
        two_txt = "rounding level" if g2med < 1e-9 else f"{100 * g2med:.4f} points"
        worst_line = ("and even the worst quote of the Surface is at rounding level." if g2max < 1e-6 else
                      f"but the worst quote is still {100 * g2max:.0f} points off: deep out of the money, where chapter "
                      "eleven's flat sheet throws Newton around. That is why the papers gate the network by region and "
                      "finish with a third-order step, and why the House keeps its bracket.")
        with self.voiceover(
            f"""A small two-input network learns total volatility from {nv['n_train']:,} synthetic quotes, with five seeds. This is a teaching implementation, not a replication of the gated Householder method. Right: every logged training loss, with the full seed range. Left: seed zero's checkpoint predictions against the input quote IVs, on logarithmic axes. The untrained guess reaches {100 * max(nv['snaps'][keys[0]]):.0f} percent and remains visible. <bookmark mark='a'/> Across seeds, the median quote error's median is {100 * g0:.2f} points, {cmp_word} Corrado-Miller's {100 * nv['cm_med']:.2f}. One Newton step gives a median of {100 * g1:.2f} points; two give {two_txt}. {worst_line} Median accuracy cannot certify the worst case, and we did not benchmark runtime against the papers."""
        ) as vo:
            self.play(FadeIn(title), FadeIn(rp))
            rp.play(self, run_time=max(vo.until("a") - 1.5, 5.0))
            self.play(FadeIn(res), FadeIn(computed(corner=UR)))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def papers(self):
        rows = VGroup(*[VGroup(label(a, font_size=23, color=c), wrapped_label(b, 11.6, 20, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06) for a, b, c in (
            (r"Alexander, Chen and Imeraj (2023), \textit{Mathematical Finance}",
             r"crypto quanto and inverse options: pricing and hedging what Deribit lists, in a Black--Scholes world",
             SPOT),
            (r"Matic, Packham and H\"ardle (2023), \textit{Review of Derivatives Research}",
             r"hedging Bitcoin options: calibrations point to stochastic volatility and jumps; delta hedging is "
             r"not enough for the tails", SPOT),
            (r"Hull and White (2017), \textit{JBF}; Ruf and Wang (2022), \textit{JBES}",
             r"the minimum-variance delta: correct Black--Scholes' hedge for how volatility moves with the price; a "
             r"linear regression does about as well as a neural hedger. On Bitcoin: Part 13", IMP),
            (r"Pointers", r"deep hedging and learned no-trade bands (Part 17); rough volatility (Part 14); "
             r"zero-day options (Part 12)", GREY_B),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "Three more lines of work carry this part forward. Carol Alexander and her coauthors priced "
            "the inverse options Deribit actually lists. Matic, Packham and Hardle "
            "showed what hedging Bitcoin options really takes: stochastic volatility and jumps, more than delta. "
            "<bookmark mark='a'/> And John Hull and Alan White corrected Black-Scholes' delta for the way implied "
            "volatility moves with the price, the minimum-variance delta; Johannes Ruf and Weiguan Wang found that "
            "a simple regression of this kind does about as well as a neural network. Part thirteen fits it on "
            "Bitcoin. Deep hedging, rough volatility and zero-day options have their own parts."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:2]], lag_ratio=0.5, run_time=3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[2:]], lag_ratio=0.5, run_time=3))
        self.wait(0.4)
        self.clear_scene()
