from __future__ import annotations

import math

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class Watermark(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter nine. Watermarks: hiding a hypothesis test in the text.", 9,
                            r"Watermarks as tests", r"A signal in the word choices")
        self.scheme()
        self.test()
        self.chart()
        self.entropy()
        self.attacks()
        self.deployed()

    def scheme(self):
        d = load("watermark")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Can text say which model wrote it? <bookmark mark='b'/> John Kirchenbauer and "
            f"colleagues' watermark, in 2023: before generating each token, hash the previous token to split the vocabulary "
            f"into a green list, a fraction gamma of it, and a red list. <bookmark mark='c'/> Add a bias delta to the green "
            f"tokens' logits. When the model is uncertain, it now picks a green token more often than chance: with gamma of a "
            f"quarter and delta of two, about {100 * d['green']:.0f} percent of the time instead of twenty-five. <bookmark "
            f"mark='d'/> When the model is certain, the bias barely matters, so the text's quality is nearly unchanged. "
            f"Anyone with the hash key can count the green tokens.",
            [(r"\text{green list}", r":", r"\text{hash of the previous token}, \ \text{fraction } \gamma", 40),
             (r"\text{bias}", r":", r"\text{logit}_g \ \mathrel{+}= \ \delta", 40),
             (r"P(\text{green})", r"=", rf"\frac{{\gamma e^\delta}}{{\gamma e^\delta + 1 - \gamma}} = {d['green']:.2f}", 40),
             (r"\text{detect}", r":", r"\text{count green tokens}", 40)],
            [r"Kirchenbauer et al. (2023)", r"a soft watermark", r"high-entropy tokens", r"a keyed test"],
            colors=[(2, MODB)])

    def test(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Detection is Part ten's test of a proportion. <bookmark mark='b'/> Under the null, text "
            "written without the key, each token is green with probability gamma, independently, because the hash looks "
            "random. <bookmark mark='c'/> So with T tokens and G green ones, the z statistic, G minus gamma T over the square "
            "root of T gamma one minus gamma, is approximately standard normal. <bookmark mark='d'/> Declare text "
            "watermarked when z exceeds four: a false-positive rate of three in a hundred thousand, small enough to accuse "
            "no one lightly. The null is exact by design: the test needs no model of human writing.",
            [(r"H_0", r":", r"G \sim \mathrm{Bin}(T, \gamma)", 40),
             (r"z", r"=", r"\frac{G - \gamma T}{\sqrt{T\gamma(1 - \gamma)}}", 40),
             (r"\text{reject}", r":", r"z > 4", 40),
             (r"\text{false positives}", r"\approx", r"3 \times 10^{-5}", 40)],
            [r"Part 10", r"a known null", r"Part 6's normal limit", r"no model of people needed"],
            colors=[(0, HONC)])

    def chart(self):
        d = load("watermark")
        T = np.log10(d["T"])
        A = axes([0.6, 2.6], [0, 1], x_length=7.2, y_length=4.4, xlabel=r"tokens $T$ (log scale)",
                 ylabel=r"power to detect at $z > 4$", xticks=list(np.log10([5, 20, 80, 320])), xfmt=lambda v: f"{10 ** v:.0f}",
                 yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.4, 0.2, 0])
        ax = A.ax

        def line(key, color):
            return VGroup(polyline(ax, T, d[key], color, 3.5), *[Dot(ax.c2p(a, b), radius=0.07, color=color) for a, b in zip(T, d[key])])
        full, low, ed = line("full", HONC), line("low_entropy", MODA), line("edited", NAIVEC)
        k40 = list(d["T"]).index(40)
        k160 = list(d["T"]).index(160)
        side = side_groups([
            [(r"$\gamma = 0.25$, \ $\delta = 2$; \ exact binomial power", WHITE)],
            [(rf"green: \ every token uncertain", HONC), (rf"{100 * d['full'][k40]:.1f}\% at 40 tokens", HONC)],
            [(rf"blue: \ 40\% of tokens uncertain", MODA), (rf"{100 * d['low_entropy'][k160]:.0f}\% at 160 tokens", MODA)],
            [(rf"red: \ half the tokens rewritten", NAIVEC), (rf"{100 * d['edited'][k40]:.0f}\% at 40, \ {100 * d['edited'][k160]:.0f}\% at 160", NAIVEC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The power of the test, computed exactly from the binomial, against the length of the "
            f"text. <bookmark mark='b'/> If every token is one where the model was uncertain, forty tokens are detected "
            f"{100 * d['full'][k40]:.1f} percent of the time. <bookmark mark='c'/> Real text has many nearly forced tokens, "
            f"where the watermark cannot act: with only forty percent uncertain, it takes about a hundred and sixty tokens "
            f"to reach {100 * d['low_entropy'][k160]:.0f} percent. <bookmark mark='d'/> And if someone rewrites half the "
            f"tokens, the signal halves: {100 * d['edited'][k40]:.0f} percent at forty tokens. Power, as always, is about "
            f"the effect size and the sample size, here the green excess per token and the number of tokens."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(full[0]), FadeIn(VGroup(*full[1:])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(low[0]), FadeIn(VGroup(*low[1:])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ed[0]), FadeIn(VGroup(*ed[1:])), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def entropy(self):
        d = load("watermark")
        k10 = list(d["T"]).index(10)
        self.lad_voiceover(
            f"<bookmark mark='a'/> Two statistical details. <bookmark mark='b'/> For short texts the normal approximation "
            f"is poor: at ten tokens, the exact false-positive rate of the z greater than four rule is "
            f"{d['exact_fpr'][k10]:.4f}, more than ten times the nominal three in a hundred thousand. Use the exact binomial "
            f"tail, Part fourteen's lesson. <bookmark mark='c'/> And repeated phrases break independence: the same pair of "
            f"tokens gives the same green list every time, so only distinct token pairs should be counted. <bookmark "
            f"mark='d'/> Scott Aaronson's scheme, and the distortion-free schemes that followed, use the key to drive the "
            f"sampling itself, so the watermarked model's output has exactly the original distribution for each token.",
            [(r"\text{short texts}", r":", rf"\text{{exact FPR at }} T = 10: \ {d['exact_fpr'][k10]:.4f}", 40),
             (r"\text{use}", r":", r"\text{the exact binomial tail}", 40),
             (r"\text{repeats}", r":", r"\text{count distinct pairs}", 40),
             (r"\text{distortion-free}", r":", r"\text{keyed sampling}", 40)],
            [r"Part 14", r"exact tests", r"independence", r"Aaronson; \ Kuditipudi et al. (2023)"],
            colors=[(0, NAIVEC)])

    def attacks(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The adversary. <bookmark mark='b'/> Paraphrasing with another model rewrites most tokens "
            "and destroys most of the signal, as the red curve showed. <bookmark mark='c'/> Inserting the watermarked text "
            "into a longer human one dilutes it; a windowed test that scans for the most watermarked stretch recovers some "
            "power, at the price of multiple testing, Part thirty-three. <bookmark mark='d'/> No watermark survives an "
            "adversary who rewrites everything. The test is strong evidence when it fires and weak evidence when it does "
            "not: absence of a watermark proves nothing.",
            [(r"\text{paraphrase}", r":", r"\text{signal destroyed}", 40),
             (r"\text{dilute}", r":", r"\text{scan windows, \ correct for multiplicity}", 40),
             (r"\text{rewrite all}", r":", r"\text{nothing survives}", 40),
             (r"\text{asymmetry}", r":", r"\text{firing is evidence; \ silence is not}", 40)],
            [r"edits", r"Part 33", r"limits", r"Part 10's power"],
            colors=[(0, NAIVEC), (3, MODB)])

    def deployed(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Watermarks are deployed. <bookmark mark='b'/> Sumanth Dathathri and colleagues at Google "
            "DeepMind described SynthID-Text in Nature in 2024: a tournament-sampling watermark running on Gemini's "
            "responses. <bookmark mark='c'/> In a live comparison over about twenty million responses, users' ratings of "
            "watermarked and unwatermarked answers were indistinguishable: an A/B test of Part thirteen, used to show that "
            "nothing happened. <bookmark mark='d'/> The authors note the same limit: rewriting the text weakens detection.",
            [(r"\text{SynthID-Text}", r":", r"\text{tournament sampling}", 40),
             (r"\text{deployed}", r":", r"\text{Gemini's responses}", 40),
             (r"\text{live test}", r":", r"\text{about 20 million responses}", 40),
             (r"\text{limit}", r":", r"\text{paraphrasing}", 40)],
            [r"Dathathri et al. (2024)", r"in production", r"Part 13's A/B test", r"the same asymmetry"],
            colors=[(1, HONC)])
