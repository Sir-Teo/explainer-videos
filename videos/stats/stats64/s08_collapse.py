from __future__ import annotations

import math

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class Collapse(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter seven. Synthetic data, and the collapse of a model trained on itself.", 7,
                            r"Model collapse", r"A Gaussian fitted to its own samples")
        self.story()
        self.setup_()
        self.mean_()
        self.typical()
        self.chart()
        self.tails()
        self.accumulate()

    def story(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Models are now trained partly on text and images that earlier models produced. "
            "<bookmark mark='b'/> Ilia Shumailov and colleagues reported in Nature in 2024 that training generation after "
            "generation on the previous generation's output makes models forget: the tails of the distribution go first, and "
            "the output narrows towards a few typical modes. They called it model collapse. <bookmark mark='c'/> The "
            "phenomenon has a one-line statistical core, visible in the simplest model there is. <bookmark mark='d'/> Fit a "
            "normal distribution; sample from the fit; fit again.",
            [(r"\text{generations}", r":", r"\text{each trained on the last one's output}", 40),
             (r"\text{observed}", r":", r"\text{tails lost, \ variance shrinks}", 40),
             (r"\text{core}", r":", r"\text{a statistical fact}", 40),
             (r"\text{the toy}", r":", r"N(\mu, \sigma^2) \ \text{refitted to itself}", 40)],
            [r"synthetic data", r"Shumailov et al. (2024)", r"no deep network needed", r"Part 9's MLE"],
            colors=[(1, NAIVEC)])

    def setup_(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Generation zero: n draws from a standard normal. <bookmark mark='b'/> Fit the mean and "
            "variance by maximum likelihood, the sample mean and the average squared deviation. <bookmark mark='c'/> "
            "Generation t plus one: n fresh draws from the fitted normal of generation t, and fit again. <bookmark "
            "mark='d'/> By Cochran's theorem, n times the fitted variance over the true one is chi-squared with n "
            "minus one degrees of freedom, so each generation multiplies the variance by an independent factor, chi-squared "
            "over n.",
            [(r"X^{(0)}_i", r"\sim", r"N(0, 1), \ \ i = 1, \dots, n", 40),
             (r"\hat\sigma_t^2", r"=", r"\frac1n \sum_i (X_i^{(t)} - \bar X^{(t)})^2", 40),
             (r"X^{(t+1)}_i", r"\sim", r"N(\hat\mu_t, \hat\sigma_t^2)", 40),
             (r"\hat\sigma_{t+1}^2", r"=", r"\hat\sigma_t^2 \cdot \chi^2_{n-1} / n", 40)],
            [r"the start", r"Part 9", r"self-consumption", r"Cochran's theorem"],
            colors=[(3, NAIVEC)])

    def mean_(self):
        d = load("collapse")
        n = d["n"]
        self.lad_voiceover(
            f"<bookmark mark='a'/> So the variance after t generations is a product of t independent factors. <bookmark "
            f"mark='b'/> Its expectation is the product of their expectations, n minus one over n to the t. <bookmark "
            f"mark='c'/> With n of {n}, that is {(n - 1) / n} to the t: halving every {math.log(0.5) / math.log((n - 1) / n):.0f} "
            f"generations. <bookmark mark='d'/> That is the bias of the maximum-likelihood variance, Part nine's divide by "
            f"n, compounded. Dividing by n minus one would fix the mean, but not what comes next.",
            [(r"\hat\sigma_t^2", r"=", r"\prod_{s=1}^{t} \frac{\chi^2_{n-1, s}}{n}", 40),
             (r"E[\hat\sigma_t^2]", r"=", r"\left(\frac{n - 1}{n}\right)^t", 40),
             (rf"n = {n}", r":", rf"{(n - 1) / n}^t, \ \ \text{{halving every }} {math.log(0.5) / math.log((n - 1) / n):.1f}", 40),
             (r"\text{cause}", r":", r"\text{the MLE's bias, \ compounded}", 40)],
            [r"independent factors", r"exact", r"slow decay", r"Part 9"],
            colors=[(1, NAIVEC)])

    def typical(self):
        d = load("collapse")
        self.lad_voiceover(
            f"<bookmark mark='a'/> The typical path is worse than the mean. <bookmark mark='b'/> Take logs: the log "
            f"variance is a sum of t independent terms, each the log of chi-squared over n, a random walk. <bookmark "
            f"mark='c'/> Its step has a negative mean, {d['drift']:.3f} for n of {d['n']}, by Jensen's inequality: the log "
            f"of an average exceeds the average of the logs. Even with the unbiased divisor the drift stays negative. "
            f"<bookmark mark='d'/> By Part six's strong law, the log variance goes to minus infinity almost surely, and the "
            f"variance to zero. The mean decays slowly only because of rare paths that wander high.",
            [(r"\log\hat\sigma_t^2", r"=", r"\sum_{s=1}^t \log(\chi^2_{n-1, s}/n)", 40),
             (r"\text{drift}", r"=", rf"E\log(\chi^2_{{{d['n'] - 1}}}/{d['n']}) = {d['drift']:.3f}", 40),
             (r"\text{Jensen}", r":", r"E\log V < \log EV", 40),
             (r"\hat\sigma_t^2", r"\to", r"0 \ \ \text{almost surely}", 40)],
            [r"a random walk", r"negative", r"Jensen's inequality", r"Part 6's strong law"],
            colors=[(3, NAIVEC)])

    def chart(self):
        d = load("collapse")
        t = np.asarray(d["t"], float)
        L = lambda v: np.log10(np.maximum(np.asarray(v, float), 1e-30))  # noqa: E731
        A = axes([0, 300], [-17, 1], x_length=7.4, y_length=4.4, xlabel=r"generation $t$",
                 ylabel=r"fitted variance $\hat\sigma_t^2$ (log scale)", xticks=[0, 100, 200, 300], yticks=[0, -5, -10, -15],
                 yfmt=lambda v: f"10^{{{int(v)}}}" if v else "1", center=[-2.4, 0.2, 0])
        ax = A.ax
        band = band_(ax, t, L(d["q10"]), L(d["q90"]), NAIVEC, 0.22)
        med = polyline(ax, t, L(d["median"]), NAIVEC, 3.5)
        exp_ = DashedVMobject(polyline(ax, t, L(d["expected"]), WHITE, 2.5), num_dashes=40)
        ex = VGroup(*[polyline(ax, t, L(e), NAIVEC, 1.2, 0.45) for e in d["examples"]])
        acc = VGroup(band_(ax, t, L(d["acc_q10"]), L(d["acc_q90"]), HONC, 0.3), polyline(ax, t, L(d["acc_median"]), HONC, 3.5))
        side = side_groups([
            [(rf"$n = {d['n']}$ per generation", WHITE), (r"400 simulated lineages", GREY_A)],
            [(r"thin red: \ six lineages", NAIVEC), (r"band: \ 10--90\%, \ line: \ median", NAIVEC)],
            [(r"white dashes: \ the mean, \ $(19/20)^t$", WHITE)],
            [(r"green: \ accumulate all data", HONC), (r"instead of replacing it", HONC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The simulation, with {d['n']} draws per generation, on a log scale. <bookmark mark='b'/> "
            f"Six lineages, and the middle eighty percent of four hundred: the variance falls by orders of magnitude; after "
            f"three hundred generations the median is ten to the minus thirteen, and every lineage is below one percent of "
            f"where it started. <bookmark mark='c'/> The exact mean, nineteen twentieths to the t, decays far more slowly: "
            f"the mean is not the typical value. <bookmark mark='d'/> In green, a different practice: keep all earlier data, "
            f"and add each generation's samples to the pool instead of replacing it. The variance barely moves."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(ex), FadeIn(band), Create(med), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(exp_), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(acc), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def tails(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What it means for real models. <bookmark mark='b'/> Any estimator fitted to a finite "
            "sample loses the tails first: rare events are missing from most samples, so the fit puts less mass there, so "
            "the next sample has fewer still. A rich model loses its rare words, its unusual faces, its minority dialects. "
            "<bookmark mark='c'/> Errors compound multiplicatively, generation after generation, and nothing pulls the fit "
            "back towards the truth, because the truth is no longer in the data. <bookmark mark='d'/> The statistical "
            "statement: refitting to your own output is a Markov chain whose only absorbing states are degenerate.",
            [(r"\text{finite samples}", r":", r"\text{miss rare events}", 40),
             (r"\text{so}", r":", r"\text{the tails go first}", 40),
             (r"\text{no anchor}", r":", r"\text{the truth has left the data}", 40),
             (r"\text{a Markov chain}", r":", r"\text{absorbed at degeneracy}", 40)],
            [r"unsampled events", r"rare words, \ rare faces", r"compounding", r"Part 44"],
            colors=[(1, NAIVEC)])

    def accumulate(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The cure follows from the toy. <bookmark mark='b'/> Matthias Gerstgrasser and colleagues "
            "showed in 2024 that if real data are kept and synthetic data are added to it, rather than replacing it, the "
            "error stays bounded, because each new generation is a shrinking fraction of the pool, and the errors it adds "
            "form a convergent sum. <bookmark mark='c'/> Keep the real data, mark the synthetic, and weight towards the real. <bookmark "
            "mark='d'/> And measure: Part sixty's shift diagnostics, run between generations, catch a narrowing distribution "
            "early.",
            [(r"\text{replace}", r":", r"\text{collapse}", 40),
             (r"\text{accumulate}", r":", r"\text{bounded error}", 40),
             (r"\text{practice}", r":", r"\text{keep, \ mark, \ weight the real data}", 40),
             (r"\text{monitor}", r":", r"\text{shift tests between generations}", 40)],
            [r"the toy", r"Gerstgrasser et al. (2024)", r"provenance", r"Part 60"],
            colors=[(0, NAIVEC), (1, HONC)])


def band_(ax, t, lo, hi, color, opacity):
    pts = [ax.c2p(a, b) for a, b in zip(t, lo)] + [ax.c2p(a, b) for a, b in zip(t[::-1], np.asarray(hi)[::-1])]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)
