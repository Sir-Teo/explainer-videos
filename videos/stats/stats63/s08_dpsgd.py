from __future__ import annotations

import numpy as np

from videos.stats.stats63.common import *  # noqa: F403


class DPSGD(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter seven. Private learning, and the attacks that audit it.", 7,
                            r"DP-SGD and membership inference", r"Learning without memorizing", lit=(2016,))
        self.algorithm()
        self.toy()
        self.chart()
        self.memorize()
        self.membership()
        self.audit()
        self.disparate()

    def algorithm(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Martin Abadi and colleagues at Google gave the standard recipe in 2016: differentially "
            "private stochastic gradient descent. <bookmark mark='b'/> At each step, compute every example's gradient "
            "separately, and clip it to norm at most C. Now one person can move the summed gradient by at most C: bounded "
            "sensitivity. <bookmark mark='c'/> Add Gaussian noise of standard deviation sigma times C to the sum, then take "
            "the step. <bookmark mark='d'/> Every step is a Gaussian mechanism; the accountant of chapter three adds them "
            "up, with amplification from sampling the batch; and the final model, a post-processing of the noisy steps, "
            "inherits the guarantee.",
            [(r"\text{per-example}", r":", r"g_i \ \to \ g_i / \max(1, \|g_i\|/C)", 40),
             (r"\text{sensitivity}", r":", r"C", 40),
             (r"\text{step}", r":", r"w \ \leftarrow \ w - \eta \, (\textstyle\sum_i \bar g_i + N(0, \sigma^2 C^2 I)) / B", 38),
             (r"\text{guarantee}", r":", r"\text{the accountant, \ then post-processing}", 40)],
            [r"Abadi et al. (2016)", r"clipping", r"Gaussian noise", r"chapters 1 and 3"],
            colors=[(2, PRIVC)])

    def toy(self):
        d = load("dpsgd")
        self.lad_voiceover(
            f"<bookmark mark='a'/> A small test. The Museum's Wisconsin breast biopsies: thirty measurements of each "
            f"sample's cell nuclei, and whether it was malignant. <bookmark mark='b'/> Logistic regression, trained on "
            f"{d['n_train']} biopsies by sixty steps of full-batch gradient descent, each gradient clipped to norm one. "
            f"<bookmark mark='c'/> The noise is set so the whole run is rho-zCDP, for a range of rho, and converted to "
            f"epsilon at delta of one in a hundred thousand. <bookmark mark='d'/> Accuracy is measured on the remaining "
            f"{d['n_test']}, averaged over ten random splits.",
            [(r"\text{data}", r":", r"569 \text{ biopsies, \ 30 features}", 40),
             (r"\text{model}", r":", rf"\text{{logistic, \ {d['n_train']} train, \ 60 steps}}", 40),
             (r"\text{noise}", r":", r"\sigma = C\sqrt{60/2\rho}", 40),
             (r"\text{measure}", r":", rf"\text{{accuracy on {d['n_test']}, \ 10 splits}}", 40)],
            [r"the Museum", r"clipped gradients", r"zCDP over 60 steps", r"held out"],
            colors=[(2, PRIVC)])

    def chart(self):
        d = load("dpsgd")
        rows = [r for r in d["rows"] if r["eps"] is not None]
        npv = next(r for r in d["rows"] if r["eps"] is None)
        lx = np.log10([r["eps"] for r in rows])
        A = axes([-0.55, 1.0], [0.82, 1.0], x_length=7.2, y_length=4.4, xlabel=r"$\varepsilon$ at $\delta = 10^{-5}$ (log scale)",
                 ylabel=r"test accuracy, \ mean of 10 splits", xticks=list(np.log10([0.5, 1, 2, 5])), xfmt=lambda v: f"{10 ** v:g}",
                 yticks=[0.85, 0.9, 0.95, 1.0], center=[-2.4, 0.2, 0])
        ax = A.ax
        top = DashedLine(ax.c2p(-0.55, npv["acc"]), ax.c2p(1.0, npv["acc"]), color=RAWC, stroke_width=2.5)
        errs = VGroup(*[Line(ax.c2p(a, max(0.82, r["acc"] - r["sd"])), ax.c2p(a, min(1.0, r["acc"] + r["sd"])), color=PRIVC,
                             stroke_width=2, stroke_opacity=0.6) for a, r in zip(lx, rows)])
        pts = VGroup(polyline(ax, lx, [r["acc"] for r in rows], PRIVC, 3.5),
                     *[Dot(ax.c2p(a, r["acc"]), radius=0.08, color=PRIVC) for a, r in zip(lx, rows)])
        side = side_groups([
            [(rf"blue dashes: \ not private, \ {npv['acc']:.3f}", RAWC)],
            [(r"purple: \ private, \ with $\pm 1$ sd", PRIVC)],
            [(rf"$\varepsilon = {rows[0]['eps']:.2f}$: \ {rows[0]['acc']:.3f}", BADC), (rf"$\varepsilon = {rows[2]['eps']:.1f}$: \ {rows[2]['acc']:.3f}", OKC)],
            [(r"beyond $\varepsilon \approx 1$: \ within noise", GREY_A), (r"of the non-private model", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The non-private model, in blue, classifies {100 * npv['acc']:.1f} percent of held-out "
            f"biopsies correctly. <bookmark mark='b'/> The private models, in purple, with one standard deviation across "
            f"splits. <bookmark mark='c'/> At epsilon of {rows[0]['eps']:.2f}, accuracy falls to {100 * rows[0]['acc']:.1f} "
            f"percent, and varies a lot from split to split. At epsilon of {rows[2]['eps']:.1f}, it is "
            f"{100 * rows[2]['acc']:.1f} percent. <bookmark mark='d'/> Beyond epsilon of about one, the private model is "
            f"within the split-to-split noise of the non-private one. Four hundred examples and thirty-one parameters is a "
            f"small problem; the noise needed shrinks as the training set grows, as chapter four predicts."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Wisconsin biopsies (the Museum)")))
            vo.wait_until("a")
            self.play(Create(top), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(pts[0]), FadeIn(VGroup(*pts[1:])), FadeIn(errs), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(pts[1], color=BADC), Indicate(pts[3], color=OKC), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def memorize(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Why bother, for a model rather than a table? <bookmark mark='b'/> Because large models "
            "memorize. Nicholas Carlini and colleagues extracted, in 2021, hundreds of verbatim training sequences from the "
            "language model GPT-2, including names, phone numbers and addresses, by sampling from it and ranking the outputs. "
            "<bookmark mark='c'/> A model is a statistic of its training data, with millions of parameters: Dinur and "
            "Nissim's reconstruction warning applies to it. <bookmark mark='d'/> Differential privacy bounds memorization "
            "directly: whatever the model outputs, it would have output with nearly the same probability without any one "
            "training example.",
            [(r"\text{memorization}", r":", r"\text{verbatim training text extracted}", 40),
             (r"\text{a model}", r":", r"\text{a statistic with many parameters}", 40),
             (r"\text{so}", r":", r"\text{reconstruction applies}", 40),
             (r"\text{DP}", r":", r"\text{bounds every example's influence}", 40)],
            [r"Carlini et al. (2021)", r"a release", r"Dinur \& Nissim (2003)", r"the guarantee"],
            colors=[(0, BADC), (3, OKC)])

    def membership(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The basic attack on a model is membership inference: was this example in the training "
            "set? Reza Shokri and colleagues framed it in 2017, training shadow models to imitate the target. <bookmark "
            "mark='b'/> It is chapter two's hypothesis test exactly: in or out, with a false positive rate and a true "
            "positive rate. <bookmark mark='c'/> Carlini and coauthors argued in 2022 that the honest summary is the true "
            "positive rate at a very low false positive rate, such as one in a thousand: an attack that confidently "
            "identifies a few members is a real breach, even if its average accuracy is near half. Their likelihood-ratio "
            "attack is Neyman and Pearson's test, with shadow models estimating the two distributions. <bookmark mark='d'/> "
            "And epsilon-DP caps every such attack: its true positive rate is at most e to the epsilon times its false "
            "positive rate, plus delta.",
            [(r"\text{membership}", r":", r"\text{in the training set or not}", 40),
             (r"\text{a test}", r":", r"(\mathrm{FPR}, \ \mathrm{TPR}) = (\alpha, 1 - \beta)", 40),
             (r"\text{report}", r":", r"\mathrm{TPR} \text{ at } \mathrm{FPR} = 10^{-3}", 40),
             (r"\text{DP caps it}", r":", r"\mathrm{TPR} \le e^{\varepsilon}\,\mathrm{FPR} + \delta", 40)],
            [r"Shokri et al. (2017)", r"chapter 2", r"Carlini et al. (2022)", r"the trade-off curve"],
            colors=[(3, OKC)])

    def audit(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Turn the cap around and it becomes an audit. <bookmark mark='b'/> Run an attack many "
            "times, estimate its false and true positive rates with confidence intervals, and every attack that achieves "
            "a ratio r proves that epsilon is at least log r. A statistical lower bound on epsilon. <bookmark mark='c'/> "
            "Matthew Jagielski, Jonathan Ullman and Alina Oprea, and then Milad Nasr and colleagues, found implementations "
            "whose claimed epsilon was smaller than what attacks proved: bugs in the code, caught by statistics. <bookmark "
            "mark='d'/> Auditing used to need thousands of training runs. Thomas Steinke, Nasr and Jagielski showed in 2023 "
            "how to audit with a single run, by inserting many random canaries and testing them all at once.",
            [(r"\text{an attack's ratio } r", r":", r"\varepsilon \ge \log r - \text{(slack)}", 40),
             (r"\text{with CIs}", r":", r"\text{a lower bound on } \varepsilon", 40),
             (r"\text{found}", r":", r"\text{implementations weaker than claimed}", 40),
             (r"\text{one run}", r":", r"\text{many random canaries}", 40)],
            [r"Part 46's tests, reversed", r"Clopper--Pearson", r"Jagielski et al. (2020); \ Nasr et al. (2021)", r"Steinke, \ Nasr \& Jagielski (2023)"],
            colors=[(1, OKC)])

    def disparate(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A bridge to the second half. <bookmark mark='b'/> Eugene Bagdasaryan, Omid Poursaeed "
            "and Vitaly Shmatikov showed in 2019 that DP-SGD costs underrepresented groups more accuracy than others. "
            "<bookmark mark='c'/> The reason is in the mechanism: rare examples have large, unusual gradients, which are the "
            "ones clipping cuts, and their signal is the one the noise drowns. <bookmark mark='d'/> Privacy for everyone can "
            "be paid for unequally. Which raises the question of the next four chapters: what would it mean for a "
            "statistical procedure to be fair?",
            [(r"\text{DP-SGD}", r":", r"\text{larger accuracy loss for small groups}", 40),
             (r"\text{why}", r":", r"\text{clipping and noise hit rare gradients}", 40),
             (r"\text{so}", r":", r"\text{privacy paid for unequally}", 40),
             (r"\text{next}", r":", r"\text{what is fair?}", 40)],
            [r"Bagdasaryan et al. (2019)", r"the mechanism", r"a disparity", r"chapters 8--11"],
            colors=[(0, BADC)])
