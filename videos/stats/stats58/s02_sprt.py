from __future__ import annotations

import numpy as np

from videos.stats.stats58.common import *  # noqa: F403


class SPRT(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter one. The sequential probability ratio test: how it works, what it costs, and why "
                       "nothing does better.", 1, r"The SPRT", r"Stop when the evidence suffices", lit=(1945, 1948))
        self.walk()
        self.paths()
        self.errors()
        self.identity()
        self.oc_chart()
        self.tail()
        self.optimal()
        self.overshoot()

    def walk(self):
        d = load("hook")
        heading = label('The Bernoulli likelihood-ratio walk', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            f"<bookmark mark='a'/> For Bernoulli data the log likelihood ratio is a random walk. Each defective adds the log "
            f"of p one over p nought, here {say(d['a'], 3)}. <bookmark mark='b'/> Each good shell adds the log of one minus "
            f"p one over one minus p nought, here minus {say(-d['b'], 3)}. <bookmark mark='c'/> The walk stops when it "
            f"leaves the band between log B, minus {say(-math.log(d['B']), 2)}, and log A, {say(math.log(d['A']), 2)}. "
            f"<bookmark mark='d'/> Because the steps take only two values, the walk lives on a lattice: after n shells with "
            f"s defectives it sits at s a plus n minus s times b. So the probability of every way to stop can be computed "
            f"to controlled numerical precision with a bounded remainder, by pushing the probabilities of the states still inside the band forward one shell at a time.",
            [(r"\text{a defective}", r":", rf"+\log\tfrac{{p_1}}{{p_0}} = +{d['a']:.3f}", 38),
             (r"\text{a good shell}", r":", rf"+\log\tfrac{{1 - p_1}}{{1 - p_0}} = -{-d['b']:.3f}", 38),
             (r"\text{stop}", r":", rf"\log\Lambda_n \notin (\log B, \log A) = (-{-math.log(d['B']):.2f}, \ {math.log(d['A']):.2f})", 36),
             (r"\text{exactly}", r":", r"\log\Lambda_n = s\,a + (n - s)\,b: \ \text{a lattice walk}", 36)],
            [r"a step up", r"a small step down", r"Wald's band", r"push the states forward"],
            colors=[(0, FIXEDC), (1, CSC), (3, SPRTC)])

    def paths(self):
        d = load("paths")
        lA, lB = d["logA"], d["logB"]
        nmax = max(max(p["n"] for p in d["h0"]), max(p["n"] for p in d["h1"]))
        nmax = int(max(120, nmax))
        A = axes([0, nmax], [lB - 0.3, lA + 0.85], x_length=8.2, y_length=4.6, xlabel=r"shells tested", ylabel=r"log likelihood ratio",
                 xticks=[0, 50, 100, 150, 200, 250][: 1 + nmax // 50], yticks=[round(lB, 2), 0, round(lA, 2)], center=[-2.1, 0.1, 0])
        ax = A.ax
        up = DashedLine(ax.c2p(0, lA), ax.c2p(nmax, lA), color=FIXEDC, stroke_width=3)
        dn = DashedLine(ax.c2p(0, lB), ax.c2p(nmax, lB), color=CSC, stroke_width=3)

        def path(p, col):
            y = np.r_[0.0, np.asarray(p["llr"])]
            x = np.arange(len(y))
            k = x <= nmax
            return polyline(ax, x[k], y[k], col, 2.2, 0.85)
        g0 = VGroup(*[path(p, SPRTC) for p in d["h0"]])
        g1 = VGroup(*[path(p, WEALTHC) for p in d["h1"]])
        n0 = np.mean([p["n"] for p in d["h0"]])
        n1 = np.mean([p["n"] for p in d["h1"]])
        acc0 = sum(p["decision"] == 0 for p in d["h0"])
        rej1 = sum(p["decision"] == 1 for p in d["h1"])
        side = fit_rows(VGroup(
            label(r"red line: \ reject $H_0$ \ ($\log A$); \ green: \ accept", font_size=22),
            label(rf"blue: \ 12 lots at $p = 0.1$; \ {acc0} accepted, \ mean {n0:.0f} shells", font_size=22, color=SPRTC),
            label(rf"gold: \ 12 lots at $p = 0.2$; \ {rej1} rejected, \ mean {n1:.0f} shells", font_size=22, color=WEALTHC),
            label(r"each path stops the moment it leaves the band", font_size=22, color=GREY_A),
        ), 4.2, 0.4, [4.6, 0.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here are twelve lots at each rate. The band runs from log B up to log A. <bookmark "
            f"mark='b'/> At a defective rate of ten percent, the walks drift down, because good shells dominate; {acc0} of the "
            f"twelve are accepted, after {n0:.0f} shells on average. <bookmark mark='c'/> At twenty percent, the walks drift "
            f"up; {rej1} of the twelve are rejected, after {n1:.0f} shells on average. <bookmark mark='d'/> Each walk stops the "
            f"moment it leaves the band: no shell is tested after the evidence is in."
        ) as vo:
            self.play(FadeIn(A), Create(up), Create(dn), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(p) for p in g0], lag_ratio=0.15), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(p) for p in g1], lag_ratio=0.15), FadeIn(side[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def errors(self):
        heading = label('Wald thresholds: relaxed error guarantees', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> On the event that the SPRT rejects, its likelihood ratio at stopping is at least "
            "A. <bookmark mark='b'/> Changing measure shows that the alternative rejection probability is at least "
            "A times the null rejection probability. <bookmark mark='c'/> Therefore the size is at most one over A, "
            "or alpha divided by one minus beta for Wald's approximate thresholds. <bookmark mark='d'/> Similarly, "
            'the other error is at most beta divided by one minus alpha. The stricter nominal targets are not '
            'automatically guaranteed. For this Bernoulli example we compute the actual errors by lattice '
            'propagation, including overshoot.'
        ),
            [(r"\{\text{reject}\}", r":", r"\Lambda_N \ge A \text{ there}", 38),
             (r"P_1(\text{reject})", r"=", r"E_0[\Lambda_N; \text{reject}] \ge A\,P_0(\text{reject})", 36),
             (r"\Rightarrow", r"\;", r"P_0(\text{reject}) \le \frac{1 - \beta'}{A} \le \frac{\alpha}{1 - \beta}", 36),
             (r"\text{likewise}", r":", r"P_1(\text{accept}) \le \frac{\beta}{1 - \alpha}", 38)],
            [r"by definition of stopping", r"a change of measure", r"Wald's bound", r"nominal targets require calibration"],
            colors=[(2, CSC), (3, CSC)])

    def identity(self):
        heading = label("Wald's identity: IID integrable increments", font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Wald's identity assumes IID integrable increments and a stopping time with finite "
            'expected length. Then the expected stopped sum equals the mean increment times expected length. '
            "<bookmark mark='b'/> At an SPRT stop the sum is near one of the boundaries, with an overshoot. "
            "<bookmark mark='c'/> Ignoring that overshoot approximates expected length by expected boundary "
            "position divided by the drift, except at zero drift where a limit is needed. <bookmark mark='d'/> "
            'Under the two specified hypotheses the drift is respectively a negative and a positive '
            'Kullback-Leibler divergence. At an intermediate true rate it is simply the expected log likelihood '
            'increment.'
        ),
            [(r"\text{Wald's identity}", r":", r"E\Big[\textstyle\sum_{i \le N} Z_i\Big] = E[N]\,E[Z_1]", 38),
             (r"\text{at the stop}", r":", r"S_N \approx \log A \text{ or } \log B", 38),
             (r"\Rightarrow", r"\;", r"E N \approx \frac{P(\text{reject})\log A + P(\text{accept})\log B}{E Z_1}", 36),
             (r"\text{under } H_0", r":", r"E_0 Z_1 = -\mathrm{KL}(f_0 \,\|\, f_1)", 38)],
            [r"optional stopping, \ for sums", r"ignoring overshoot", r"Wald's approximation", r"Part 22's divergence, \ as a clock"],
            colors=[(2, SPRTC), (3, WEALTHC)])

    def oc_chart(self):
        d = load("oc")
        R = d["rows"]
        ps = np.array([r["p"] for r in R])
        A = axes([0.04, 0.32], [0, 1.0], x_length=5.4, y_length=3.6, xlabel=r"true defective rate $p$", ylabel=r"P(reject the lot)",
                 xticks=[0.1, 0.2, 0.3], yticks=[0, 0.5, 1], center=[-3.4, 0.4, 0])
        B = axes([0.04, 0.32], [0, 120], x_length=5.4, y_length=3.6, xlabel=r"true defective rate $p$", ylabel=r"expected number of shells",
                 xticks=[0.1, 0.2, 0.3], yticks=[0, 50, 100], center=[3.4, 0.4, 0])
        ex1 = polyline(A.ax, ps, [r["accept_h1"] for r in R], SPRTC, 4)
        wa1 = polyline(A.ax, ps, [r["wald_accept_h1"] for r in R], GREY_B, 2.5)
        ex2 = polyline(B.ax, ps, [r["asn"] for r in R], SPRTC, 4)
        wa2 = polyline(B.ax, ps, [r["wald_asn"] for r in R], GREY_B, 2.5)
        fixed = DashedLine(B.ax.c2p(0.04, d["fixed_n"]), B.ax.c2p(0.32, d["fixed_n"]), color=FIXEDC, stroke_width=3)
        peak = max(R, key=lambda r: r["asn"])
        foot = fit_rows(VGroup(
            label(r"blue: \ exact, \ by the lattice; \ grey: \ Wald's approximations, \ which ignore overshoot", font_size=24, color=GREY_A),
            label(rf"red: \ the fixed test's {d['fixed_n']} shells; \ the SPRT's average peaks at {peak['asn']:.0f}, \ near $p = {peak['p']:.2f}$", font_size=24, color=FIXEDC),
        ), 12.4, 0.2, [0, -2.85, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The whole operating characteristic, exactly. On the left, the probability of rejecting the "
            f"lot as the true rate varies; on the right, the average number of shells. <bookmark mark='b'/> In blue, the exact "
            f"values; in grey, Wald's approximations, which ignore the overshoot and are close. <bookmark mark='c'/> The "
            f"average sample size is largest between the two hypotheses, about {peak['asn']:.0f} near a rate of "
            f"{say(peak['p'], 2)}, where the data cannot make up their mind; it is still below the fixed test's "
            f"{d['fixed_n']}, shown in red."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(exact_tag(r"exact arithmetic")))
            vo.wait_until("a")
            self.play(Create(ex1), Create(ex2), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(wa1), Create(wa2), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(Create(fixed), FadeIn(foot[1]))
        self.clear_scene()

    def tail(self):
        d = load("hook")
        heading = label('Truncation requires new calibration', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            f"<bookmark mark='a'/> The saving is on average. The number of shells is random, and sometimes large: <bookmark mark='b'/> at a rate of ten percent, the sequential test runs past the fixed test's {d['fixed']['n']} shells {100 * d['beyond_fixed0']:.0f} percent of the time, and at twenty percent, {100 * d['beyond_fixed1']:.0f} percent. <bookmark mark='c'/> In practice the test is truncated: decide at a maximum sample size if the walk is still inside. <bookmark mark='d'/> A terminal rule must be calibrated jointly with the boundaries: truncating and deciding by sign can change error rates substantially. A guaranteed budget requires a new error calculation.",
            [(r"N", r":", r"\text{random, \ with a long right tail}", 38),
             (r"P(N > {})".format(d["fixed"]["n"]), r":", rf"{100 * d['beyond_fixed0']:.1f}\% \ (p_0), \ \ {100 * d['beyond_fixed1']:.1f}\% \ (p_1)", 38),
             (r"\text{truncate}", r":", r"\text{decide at } n_{\max} \text{ by the sign of } \log\Lambda", 38),
             (r"\text{the price}", r":", r"\text{recalibrate errors for the terminal rule}", 38)],
            [r"saving on average", r"exact", r"the practical SPRT", r"trials need budgets"],
            colors=[(1, FIXEDC), (2, SPRTC)])

    def optimal(self):
        heading = label('Optimality at two simple hypotheses', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> And nothing does better. Abraham Wald and Jacob Wolfowitz proved in 1948 that for "
            'IID observations from two simple hypotheses, among tests with finite expected lengths, sequential or '
            "not, whose two error probabilities are no larger than the SPRT's, <bookmark mark='b'/> none has a "
            "smaller expected sample size under the null, <bookmark mark='c'/> or under the alternative: the SPRT "
            "minimizes both at once. <bookmark mark='d'/> The proof is Bayesian: the SPRT is the Bayes rule for a "
            "prior on the two hypotheses and a cost per observation, an argument Part forty-five's decision theory "
            'makes natural. Between the two hypotheses, though, other tests can do better, which is why later work '
            'truncates and adapts.'
        ),
            [(r"\text{among tests with}", r":", r"P_0(\text{reject}) \le \alpha', \ P_1(\text{accept}) \le \beta'", 36),
             (r"\text{the SPRT minimizes}", r":", r"E_0 N", 38),
             (r"\text{and simultaneously}", r":", r"E_1 N", 38),
             (r"\text{proof}", r":", r"\text{it is a Bayes rule with a cost per observation}", 36)],
            [r"Wald \& Wolfowitz (1948)", r"at the null", r"and the alternative", r"Part 45's decision theory"],
            colors=[(1, SPRTC), (2, SPRTC)])

    def overshoot(self):
        d = load("hook")
        heading = label('Actual errors include overshoot', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            f"<bookmark mark='a'/> A worked check on overshoot. The target errors were five and ten percent; Wald's bounds "
            f"allow up to {100 * 0.05 / 0.9:.1f} and {100 * 0.1 / 0.95:.1f} percent. <bookmark mark='b'/> The exact errors are "
            f"{100 * d['size']:.2f} and {100 * (1 - d['power']):.2f} percent. <bookmark mark='c'/> The size is below five percent "
            f"because a defective is a big step, log two, so the walk usually jumps well past log A when it crosses. "
            f"<bookmark mark='d'/> Siegmund's renewal theory corrects the thresholds for the expected overshoot, and recovers "
            f"the targets almost exactly.",
            [(r"\text{Wald's bounds}", r":", rf"\alpha' \le {100 * 0.05 / 0.9:.1f}\%, \ \beta' \le {100 * 0.1 / 0.95:.1f}\%", 38),
             (r"\text{exact}", r":", rf"\alpha' = {100 * d['size']:.2f}\%, \ \beta' = {100 * (1 - d['power']):.2f}\%", 38),
             (r"\text{why below}", r":", r"\text{a defective is a step of } \log 2: \ \text{overshoot}", 38),
             (r"\text{correction}", r":", r"\text{shift } \log A, \log B \text{ by the expected overshoot}", 36)],
            [r"$\alpha/(1-\beta)$, \ $\beta/(1-\alpha)$", r"the lattice", r"conservative", r"Siegmund (1985)"],
            colors=[(1, CSC)])
