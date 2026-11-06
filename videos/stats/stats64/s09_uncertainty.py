from __future__ import annotations

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class Uncertainty(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eight. Uncertainty for language models: calibration, and conformal guarantees.", 8,
                            r"Uncertainty for language models", r"Knowing what it knows")
        self.calibration()
        self.posttraining()
        self.factuality()
        self.chart()
        self.sets()
        self.limits()

    def calibration(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Does a language model know when it is likely to be wrong? <bookmark mark='b'/> Saurav "
            "Kadavath and colleagues at Anthropic asked in 2022, and found that large models' probabilities on "
            "multiple-choice answers were well calibrated, in Part thirty-four's sense: among answers given seventy percent, "
            "about seventy percent were right. <bookmark mark='c'/> Models could also be trained to estimate the probability "
            "that their own free-form answer was correct. <bookmark mark='d'/> Calibration is measurable, with reliability "
            "diagrams and expected calibration error, and repairable, with Part thirty-four's temperature scaling.",
            [(r"\text{question}", r":", r"\text{does it know when it is wrong?}", 40),
             (r"\text{multiple choice}", r":", r"\text{well calibrated}", 40),
             (r"\text{free form}", r":", r"P(\text{my answer is right})", 40),
             (r"\text{tools}", r":", r"\text{reliability diagrams, \ temperature}", 40)],
            [r"Kadavath et al. (2022)", r"Part 34", r"self-evaluation", r"Part 34"],
            colors=[(1, HONC)])

    def posttraining(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Calibration can be lost. <bookmark mark='b'/> OpenAI's GPT-4 report showed the pretrained "
            "model well calibrated on a multiple-choice benchmark, and the model after training on human preferences less so. "
            "<bookmark mark='c'/> A model trained to please is trained towards confident answers. <bookmark mark='d'/> So "
            "calibration must be checked on the deployed model, not inherited from the base model, and checked within "
            "subgroups of questions, Part sixty-three's multicalibration.",
            [(r"\text{pretrained}", r":", r"\text{calibrated}", 40),
             (r"\text{after preference training}", r":", r"\text{less so}", 40),
             (r"\text{reason}", r":", r"\text{rewarded confidence}", 40),
             (r"\text{check}", r":", r"\text{the deployed model, \ by subgroup}", 40)],
            [r"OpenAI (2023)", r"a reported plot", r"an incentive", r"Part 63"],
            colors=[(1, NAIVEC)])

    def factuality(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A guarantee, rather than an estimate, comes from Part fifty-seven. <bookmark mark='b'/> "
            "Christopher Mohri and Tatsunori Hashimoto's conformal factuality, in 2024, splits each answer into claims, and "
            "scores each claim's confidence. <bookmark mark='c'/> On calibration answers whose claims have been checked, find "
            "for each answer the smallest threshold above which every kept claim is true: the score of its most confident "
            "false claim. <bookmark mark='d'/> Take Part fifty-seven's conformal quantile of those thresholds. Filtering a "
            "new answer to the claims above it gives an answer that is entirely true with probability at least one minus "
            "alpha, for exchangeable questions, whatever the model.",
            [(r"\text{an answer}", r":", r"\text{claims, \ each with a score}", 40),
             (r"t_i", r"=", r"\max\{\text{score of a false claim in answer } i\}", 40),
             (r"\hat t", r"=", r"\lceil (n + 1)(1 - \alpha) \rceil\text{-th smallest } t_i", 40),
             (r"P(\text{all kept claims true})", r"\ge", r"1 - \alpha", 40)],
            [r"Part 57", r"Mohri \& Hashimoto (2024)", r"the needed threshold", r"distribution-free"],
            colors=[(3, HONC)])

    def chart(self):
        d = load("factual")
        rows = d["rows"]
        al = [r["alpha"] for r in rows]
        A = axes([0, 0.35], [0, 1], x_length=7.2, y_length=4.4, xlabel=r"$\alpha$", ylabel=r"fraction of answers, \ and of claims",
                 xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.4, 0.2, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0, 1), ax.c2p(0.35, 0.65), color=GREY_B, stroke_width=2)
        safe = VGroup(polyline(ax, al, [r["safe"] for r in rows], HONC, 3.5), *[Dot(ax.c2p(a, r["safe"]), radius=0.08, color=HONC) for a, r in zip(al, rows)])
        kept = VGroup(polyline(ax, al, [r["kept"] for r in rows], MODB, 3.5), *[Dot(ax.c2p(a, r["kept"]), radius=0.08, color=MODB) for a, r in zip(al, rows)])
        raw = DashedLine(ax.c2p(0, d["unfiltered_safe"]), ax.c2p(0.35, d["unfiltered_safe"]), color=NAIVEC, stroke_width=2.5)
        r10 = next(r for r in rows if r["alpha"] == 0.1)
        side = side_groups([
            [(rf"answers of {d['claims']} claims, \ each true", WHITE), (rf"with probability {d['p_true']}", WHITE)],
            [(rf"red dashes: \ unfiltered, \ {100 * d['unfiltered_safe']:.0f}\% all true", NAIVEC)],
            [(r"green: \ filtered answers all true", HONC), (rf"{100 * r10['safe']:.1f}\% at $\alpha = 0.1$; \ grey: $1 - \alpha$", HONC)],
            [(r"gold: \ the fraction of claims kept", MODB), (rf"{100 * r10['kept']:.0f}\% at $\alpha = 0.1$", MODB)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> A simulation: answers of {d['claims']} claims, each true with probability {d['p_true']}, "
            f"with confidence scores that are informative but noisy. <bookmark mark='b'/> Unfiltered, only "
            f"{100 * d['unfiltered_safe']:.0f} percent of answers are entirely true. <bookmark mark='c'/> After conformal "
            f"filtering, the fraction of entirely true answers tracks one minus alpha, the grey line: "
            f"{100 * r10['safe']:.1f} percent at alpha of a tenth. <bookmark mark='d'/> The price is in the gold line: at "
            f"alpha of a tenth, only {100 * r10['kept']:.0f} percent of claims survive. Factuality is bought with "
            f"informativeness, and a better confidence score buys more of both."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(raw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(safe[0]), FadeIn(VGroup(*safe[1:])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(kept[0]), FadeIn(VGroup(*kept[1:])), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def sets(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Other conformal guarantees for generation. <bookmark mark='b'/> Victor Quach and "
            "colleagues' conformal language modeling, in 2024, keeps sampling answers until the set of samples contains an "
            "acceptable one with guaranteed probability, and prunes redundant ones. <bookmark mark='c'/> For multiple-choice "
            "questions, ordinary prediction sets from Part fifty-seven apply directly, and the set's size is a measure of "
            "the model's uncertainty. <bookmark mark='d'/> All of them inherit Part fifty-seven's fine print: the guarantee "
            "is marginal, over exchangeable questions, and must be recalibrated when the questions shift.",
            [(r"\text{conformal LM}", r":", r"\text{sample until acceptable}", 40),
             (r"\text{multiple choice}", r":", r"\text{prediction sets}", 40),
             (r"\text{set size}", r":", r"\text{an uncertainty measure}", 40),
             (r"\text{fine print}", r":", r"\text{marginal, \ exchangeable}", 40)],
            [r"Quach et al. (2024)", r"Part 57", r"informative", r"Part 60's shift"],
            colors=[(3, NAIVEC)])

    def limits(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What remains hard. <bookmark mark='b'/> Checking claims is itself expensive, so the "
            "calibration set is small, and chapter six's judges are tempting; their errors then enter the guarantee. "
            "<bookmark mark='c'/> Claims are not independent, and splitting an answer into claims is itself done by a "
            "model. <bookmark mark='d'/> And a guarantee over typical questions says little about the rare question that "
            "matters most, Part fifty-seven's conditional coverage problem, unsolved in general.",
            [(r"\text{checking}", r":", r"\text{expensive, \ or a judge}", 40),
             (r"\text{claims}", r":", r"\text{dependent, \ model-made}", 40),
             (r"\text{rare questions}", r":", r"\text{marginal is not conditional}", 40),
             (r"\text{open}", r":", r"\text{conditional guarantees}", 40)],
            [r"chapter 6", r"the decomposition", r"Part 57", r"chapter 13"],
            colors=[(3, NAIVEC)])
