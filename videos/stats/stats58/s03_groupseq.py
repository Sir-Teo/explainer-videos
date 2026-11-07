from __future__ import annotations

import numpy as np

from videos.stats.stats58.common import *  # noqa: F403


class GroupSequential(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter two. Group-sequential theory: a few planned looks, in the Brownian picture, and what "
                       "stopping does to an estimate.", 2, r"Group-sequential theory", r"A few planned looks", lit=(1977, 1979, 1983))
        self.brownian()
        self.bounds()
        self.spending()
        self.bias_chart()
        self.bias_why()
        self.remedies()
        self.compare()

    def brownian(self):
        heading = label('The known-variance Gaussian joint law', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Group-sequential designs inspect a trial at a sequence of information fractions. "
            "The illustrated calculation uses five equally spaced looks. <bookmark mark='b'/> For independent "
            'Gaussian observations with known variance, the scaled score has exactly the Brownian joint law at '
            'deterministic information times. Other settings often use this as an approximation. <bookmark '
            "mark='c'/> Propagate the surviving density between looks and remove probability crossing either "
            'boundary. Smooth quadrature on the continuation interval avoids a grid that rounds moving boundaries. '
            "<bookmark mark='d'/> Exactness refers to this Gaussian model and the stated timing design, not "
            'arbitrary looks chosen from the current z statistic.'
        ),
            [(r"t_k", r"=", r"\text{information at look } k \,/\, \text{planned total}", 38),
             (r"Z_k\sqrt{t_k}", r"\approx", r"B(t_k) + \theta\sqrt{I_{\max}}\,t_k", 38),
             (r"P(\text{cross at } k)", r":", r"\text{propagate the density, \ remove what crossed}", 36),
             (r"\text{exact}", r":", r"\text{for normal data, \ any looks}", 38)],
            [r"Part 35", r"the Brownian picture", r"a convolution per look", r"Armitage, \ McPherson \& Rowe (1969)"],
            colors=[(1, SPRTC)])

    def bounds(self):
        d = load("gs")
        obf = d["obf"]
        heading = label('Two-sided boundaries at five looks', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            f"<bookmark mark='a'/> Two classical boundaries for five looks at overall level five percent, two-sided. Pocock's "
            f"is flat: reject at any look where the absolute z statistic exceeds {say(d['pocock'], 3)}. <bookmark mark='b'/> O'Brien and "
            f"Fleming's starts high, {say(obf[0], 2)} at the first look, and falls to {say(obf[-1], 2)} at the last, close to the "
            f"fixed test's one point nine six. <bookmark mark='c'/> Pocock stops early more often; O'Brien–Fleming keeps almost "
            f"all the final test's power, <bookmark mark='d'/> which is why boundaries of the O'Brien–Fleming type are the "
            f"common choice in practice.",
            [(r"\text{Pocock}", r":", rf"c_k = {d['pocock']:.3f} \text{{ at every look}}", 38),
             (r"\text{O'Brien--Fleming}", r":", rf"c_k = {obf[0]:.2f}, \ {obf[1]:.2f}, \ {obf[2]:.2f}, \ {obf[3]:.2f}, \ {obf[4]:.2f}", 36),
             (r"\text{trade}", r":", r"\text{early stopping \ vs \ final power}", 38),
             (r"\text{in practice}", r":", r"\text{O'Brien--Fleming-type boundaries}", 38)],
            [r"Pocock (1977)", r"O'Brien \& Fleming (1979)", r"spend early or late", r"conservative early looks"],
            colors=[(0, FIXEDC), (1, SPRTC)])

    def spending(self):
        heading = label('Spending functions and noninformative timing', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Lan-DeMets spending allows flexibility in analysis timing through a prechosen "
            "nondecreasing cumulative error budget. <bookmark mark='b'/> At each information time, solve a boundary "
            'using the probability increment spent since the previous look. Timing must be noninformative for the '
            "score process or explicitly accounted for in its joint calibration. <bookmark mark='c'/> The displayed "
            "O'Brien-Fleming-like spending family is one valid choice, spending little early. <bookmark mark='d'/> "
            'Our algorithm illustrates finitely many looks with known information fractions. This is not a '
            'fundamental prohibition on all continuous-time spending methods. Confidence sequences offer a '
            'different construction for monitoring at every time.'
        ),
            [(r"\alpha(t)", r":", r"0 \to \alpha, \ \text{chosen in advance}", 38),
             (r"\text{look at } t_k", r":", r"\text{spend } \alpha(t_k) - \alpha(t_{k-1})", 38),
             (r"\text{O'Brien--Fleming-like}", r":", r"4 - 4\Phi\big(z_{1-\alpha/4}/\sqrt t\big)", 36),
             (r"\text{still}", r":", r"\text{shown here: finite looks; \ timing must be noninformative}", 38)],
            [r"Lan \& DeMets (1983)", r"looks need not be planned", r"almost nothing early", r"chapter 6 lifts this"],
            colors=[(1, SPRTC), (3, FIXEDC)])

    def bias_chart(self):
        d = load("gs")
        R = d["rows"]
        th = np.array([r["theta"] for r in R])
        A = axes([-0.02, 0.42], [-0.01, 0.16], x_length=7.4, y_length=4.4, xlabel=r"true effect $\theta$ \ (SD units per observation)",
                 ylabel=r"bias of the mean at stopping", xticks=[0, 0.1, 0.2, 0.3, 0.4], yticks=[0, 0.05, 0.1, 0.15], center=[-2.5, 0.2, 0])
        ax = A.ax
        allb = VGroup(polyline(ax, th, [r["bias"] for r in R], FIXEDC, 4), *[Dot(ax.c2p(a, r["bias"]), radius=0.07, color=FIXEDC) for a, r in zip(th, R)])
        er = [(a, r["bias_early_positive"]) for a, r in zip(th, R) if r["bias_early_positive"] is not None and a > 0]
        early = VGroup(polyline(ax, [a for a, _ in er], [b for _, b in er], WEALTHC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=WEALTHC) for a, b in er])
        zero = DashedLine(ax.c2p(-0.02, 0), ax.c2p(0.42, 0), color=GREY_B, stroke_width=2)
        r1 = R[1]
        side = fit_rows(VGroup(
            label(rf"five O'Brien--Fleming looks, \ {d['n_per_look']} observations each", font_size=22),
            label(rf"red: \ maximum overall bias on these five simulated effects: {max(r['bias'] for r in R):.3f}", font_size=22, color=FIXEDC),
            label(rf"gold: \ given a positive early stop; \ {r1['bias_early_positive']:.2f} at $\theta = 0.1$", font_size=22, color=WEALTHC),
            label(rf"at $\theta = 0.1$ only {100 * r1['p_early_positive']:.0f}\% stop early, \ and those were lucky", font_size=22, color=GREY_A),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> What does stopping do to the estimate? Five O'Brien–Fleming looks, {d['n_per_look']} "
            f"observations each, and the sample mean reported when the trial stops. <bookmark mark='b'/> Overall, the bias is "
            f"small on these five effect values, with a simulated maximum of {say(max(r['bias'] for r in R), 3)} standard deviations. <bookmark mark='c'/> But given that the "
            f"trial stopped early for a positive crossing, it is large: at a true effect of a tenth, {say(r1['bias_early_positive'], 2)}, more than doubling the "
            f"effect. <bookmark mark='d'/> Only {100 * r1['p_early_positive']:.0f} percent of such trials stop early, and those that do "
            f"were lucky: early stopping for benefit selects overestimates, Part fifty-six's winner's curse again."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(simulated_tag(r"simulated, \ 40{,}000 trials per $\theta$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(allb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(early), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def bias_why(self):
        heading = label('Stopping selects estimates', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Stopping selects on the estimates. In our two-sided trial, an early positive "
            "crossing selects high estimates; an early negative crossing selects low ones. <bookmark mark='b'/> The "
            'gold curve conditions specifically on a positive early crossing. Its upward bias can greatly exceed '
            "the overall bias. <bookmark mark='c'/> The overall mean also averages continuations and negative "
            'crossings, and can show partial cancellation. The five simulated effect values do not establish a '
            "uniform bound over all effects. <bookmark mark='d'/> This is why an estimate reported after a "
            'particular type of stop needs a stopping-aware analysis. Pooling selected early efficacy stops can '
            'inherit the same selection problem.'
        ),
            [(r"\text{stopping}", r":", r"\text{a selection rule on the estimates}", 38),
             (r"\text{positive early stop}", r":", r"\hat\theta \text{ beyond the boundary: \ selected high}", 38),
             (r"\text{continuers}", r":", r"\text{a selected mix; \ partial cancellation overall}", 38),
             (r"\text{so}", r":", r"\text{small bias overall, \ large given the outcome}", 38)],
            [r"Part 56's theme", r"truncation from below", r"the other side", r"how results are read"],
            colors=[(1, WEALTHC), (3, FIXEDC)])

    def remedies(self):
        heading = label('Stagewise inversion after stopping', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> The remedies come from ordering the sample space. Order outcomes by the look at "
            "which the trial stopped, then by the statistic: stagewise ordering. <bookmark mark='b'/> A p-value is "
            'the probability of an outcome at least as extreme in that order, computed with the same Brownian '
            "recursion. <bookmark mark='c'/> Inverting it in theta gives a confidence interval, and solving its "
            'stagewise one-sided p-value equation at one-half gives a median-unbiased point estimate. That estimate '
            "need not be the interval midpoint. <bookmark mark='d'/> These are the standard tools in Jennison and "
            "Turnbull's book, and they assume, again, that the looks and the stopping rule were followed exactly."
        ),
            [(r"\text{order}", r":", r"\text{by stopping look, \ then by } Z", 38),
             (r"p\text{-value}", r":", r"P_\theta(\text{at least as extreme in that order})", 38),
             (r"\text{invert}", r":", r"\text{interval; \ its } 50\% \text{ point: \ median-unbiased}", 38),
             (r"\text{assumes}", r":", r"\text{the plan was followed}", 38)],
            [r"stagewise ordering", r"the same recursion", r"Part 46's inversion", r"Jennison \& Turnbull (2000)"],
            colors=[(2, CSC), (3, FIXEDC)])

    def compare(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> Where this leaves us. <bookmark mark='b'/> Group-sequential designs are exact, "
            "efficient, and accepted by regulators. <bookmark mark='c'/> But they need the looks, or at least a "
            "spending plan, fixed in advance, and a known maximum information. <bookmark mark='d'/> Online "
            'platforms look continuously, stop for business reasons, and add data without plan. <bookmark '
            "mark='e'/> For them we need guarantees that hold at every time at once, which is the next chapter's "
            'subject.'
        ),
            [(r"where this leaves us:", GREY_A),
             (r"group-sequential designs: \ exact, \ efficient, \ accepted by regulators", CSC),
             (r"but: \ looks or a spending plan in advance, \ and a known maximum", FIXEDC),
             (r"online platforms look continuously and stop for their own reasons", WEALTHC),
             (r"needed: \ guarantees at every time at once", SPRTC)])
