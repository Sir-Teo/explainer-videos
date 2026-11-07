from __future__ import annotations

import numpy as np

from videos.stats.stats62.common import *  # noqa: F403


class Regimes(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter six. Dynamic treatment regimes: rules that adapt as the patient changes.", 6,
                            r"Dynamic treatment regimes", r"Decisions in sequence", lit=(2003,))
        self.problem()
        self.gformula()
        self.qlearning()
        self.gest()
        self.chart()
        self.smart()
        self.emulation()

    def problem(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The hook's question was a dynamic regime: start treatment when the CD4 count first falls "
            "below a threshold. <bookmark mark='b'/> A regime is a sequence of rules, each using the history so far. "
            "<bookmark mark='c'/> Two difficulties. The intermediate measurements are affected by earlier treatment and "
            "affect later treatment, so they are both mediators and confounders. <bookmark mark='d'/> And the best first "
            "decision depends on what will be done second: decisions must be optimized backward.",
            [(r"\text{regime}", r":", r"d = (d_1(H_1), d_2(H_2), \dots)", 40),
             (r"H_k", r":", r"\text{the history before decision } k", 40),
             (r"L_k", r":", r"\text{a confounder and a mediator at once}", 40),
             (r"\text{optimize}", r":", r"\text{backward, \ like dynamic programming}", 40)],
            [r"the hook's rule", r"sequential", r"Part 36's g-methods", r"Bellman"],
            colors=[(2, HIDC)])

    def gformula(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The longitudinal g-formula identifies a regime value under consistency, sequential exchangeability and positivity for the intervention histories of interest. <bookmark mark='b'/> It integrates conditional outcome and covariate laws with treatments set by the specified regime. <bookmark mark='c'/> Reading a treatment coefficient from a single regression that conditions on an intermediate mediator is generally different from this total-effect calculation. Regression-based sequential g-computation can implement the formula correctly; regression itself is not the problem. <bookmark mark='d'/> Regime-adherence weighting is another route under its own support and nuisance-model conditions.",
            [(r"\text{g-formula}", r":", r"E[Y^d] = \int E[Y \mid \bar l, \bar a = d(\bar l)]\prod_k dP(l_k \mid \bar l_{k-1}, \bar a_{k-1})", 32),
             (r"\text{needs}", r":", r"\text{sequential exchangeability}", 40),
             (r"\text{adjusting for } L", r":", r"\text{single-coefficient adjustment }\ne\text{ sequential g-computation}", 40),
             (r"\text{or}", r":", r"\text{IPW of regime adherence; \ clone and censor}", 40)],
            [r"Robins (1986)", r"no hidden step-wise confounding", r"Part 36", r"Cain et al. (2011)"],
            colors=[(0, IDC), (2, NAIVEC)])

    def qlearning(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Q-learning works backward through conditional outcome models. <bookmark mark='b'/> At stage two, model the outcome using the relevant full observed history and each possible final treatment. Our revised simulation includes the first-stage treatment-by-state reward that the old reduced history omitted. <bookmark mark='c'/> Regress the estimated best later outcome on earlier history and treatment to learn a first-stage rule. The linear first-stage regression remains a working approximation in this nonlinear simulation. <bookmark mark='d'/> Backward induction is optimal with correct conditional Q functions and identification assumptions; it does not make misspecified fitted regressions exactly optimal.",
            [(r"\text{stage 2}", r":", r"Q_2(h_2, a_2) = E[Y \mid H_2 = h_2, A_2 = a_2]", 40),
             (r"d_2^*(h_2)", r"=", r"\arg\max_{a_2} Q_2(h_2, a_2)", 40),
             (r"\text{stage 1}", r":", r"Q_1(h_1, a_1) = E[\max_{a_2} Q_2(H_2, a_2) \mid h_1, a_1]", 40),
             (r"\text{so}", r":", r"\text{backward induction on regressions}", 40)],
            [r"Murphy (2003); \ Robins (2004)", r"the last decision", r"the pseudo-outcome", r"dynamic programming"],
            colors=[(3, IDC)])

    def chart(self):
        d = load("dtr")
        v = d["values"]
        order = ["never treat", "always treat", "stage 2 only", "Q-learning", "oracle"]
        cols = [GREY_B, NAIVEC, TRTC, IDC, GOLDC]
        vals = [v[k] for k in order]
        A = axes([-0.5, 5.5], [-0.35, 1.05], x_length=8.4, y_length=4.4, xlabel=r"", ylabel=r"mean outcome under the regime",
                 xticks=None, yticks=[0, 0.5, 1.0], center=[-1.6, 0.3, 0])
        ax = A.ax
        bars = VGroup()
        for i, (k, val, c) in enumerate(zip(order, vals, cols)):
            h = ax.c2p(i, val)[1] - ax.c2p(i, 0)[1]
            rect = Rectangle(width=0.9, height=abs(h), stroke_width=0, fill_color=c, fill_opacity=0.75)
            rect.move_to(ax.c2p(i, 0), aligned_edge=DOWN if val >= 0 else UP)
            t = label(k if k != "oracle" else r"oracle rule", font_size=20, color=c).next_to(ax.c2p(i, -0.35), DOWN, buff=0.15)
            vl = label(rf"{val:.2f}", font_size=22, color=c).next_to(rect, UP if val >= 0 else DOWN, buff=0.08)
            bars.add(VGroup(rect, t, vl))
        zero = Line(ax.c2p(-0.5, 0), ax.c2p(5.5, 0), color=GREY_C, stroke_width=1.5)
        side = side_groups([
            [(r"a two-stage SMART, \ $n = 1{,}000$", WHITE), (r"both treatments randomized", GREY_A)],
            [(r"200,000 common fresh simulation states", GREY_A), (r"conditional-mean outcomes; \ Monte Carlo errors recorded", GREY_A)],
            [(r"oracle rule: \ the true model's", GOLDC), (r"thresholds at both stages", GOLDC)],
        ], width=3.6, pos=(5.2, 1.6, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> A two-stage simulation in which each stage's treatment helps some patients and harms others, depending on their current state. A thousand patients, with both treatments randomized, as in a sequential trial. <bookmark mark='b'/> The five policies are evaluated on the same two hundred thousand fresh simulated states, integrating out the final outcome noise. Saved Monte Carlo errors quantify numerical uncertainty conditional on this one training fit. <bookmark mark='c'/> Never treating gives {say(v['never treat'], 2)}; always treating, {say(v['always treat'], 2)}, worse; treating only at stage two, when the state is favourable, {say(v['stage 2 only'], 2)}. <bookmark mark='d'/> Q-learning's regime, estimated from the thousand patients, reaches {say(v['Q-learning'], 2)}, close to the {say(v['oracle'], 2)} of the regime that uses the true model's thresholds."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(b) for b in bars[:3]], run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(bars[3]), FadeIn(bars[4]), FadeIn(side[2]), run_time=1.5)
        self.clear_scene()

    def smart(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Sequential multiple-assignment randomized trials randomize treatments at specified decision points. <bookmark mark='b'/> Designs may re-randomize nonresponders, responders or other eligible subgroups according to their protocol. <bookmark mark='c'/> Randomization supplies sequential exchangeability for the assigned decisions; consistency, sufficient treatment support and handling of loss to follow-up still matter. <bookmark mark='d'/> Such trials study adaptive interventions in many areas. Observational emulation can complement them when waiting for a trial is impractical, but does not inherit randomization automatically.",
            [(r"\text{SMART}", r":", r"\text{randomize, \ then re-randomize non-responders}", 40),
             (r"\text{embedded regimes}", r":", r"\text{compared on randomized data}", 40),
             (r"\text{exchangeability}", r":", r"\text{exchangeability by design}", 40),
             (r"\text{uses}", r":", r"\text{depression, \ autism, \ smoking, \ addiction}", 40)],
            [r"Murphy (2005)", r"sequential randomization", r"the design does the work", r"applied widely"],
            colors=[(2, IDC)])

    def emulation(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The HIV-CAUSAL analysis is now the model for target-trial emulation, Miguel Hernán and "
            "Robins's framework. <bookmark mark='b'/> Write down the protocol of the trial one would run: eligibility, "
            "regimes, start of follow-up, outcome. <bookmark mark='c'/> Then mimic it with observational data, aligning "
            "time zero for every regime so that no one's survival is counted before they could be classified. <bookmark "
            "mark='d'/> Many famous observational failures, such as early hormone-therapy studies, were partly failures of "
            "time zero, and emulation removes that error by construction.",
            [(r"\text{target trial}", r":", r"\text{the protocol one would run}", 40),
             (r"\text{emulate}", r":", r"\text{same eligibility, \ regimes, \ time zero}", 40),
             (r"\text{time zero}", r":", r"\text{aligned for every regime}", 40),
             (r"\text{removes}", r":", r"\text{immortal-time bias}", 40)],
            [r"Hern\'an \& Robins (2016)", r"Part 36's target trials", r"cloning", r"the hormone-therapy lesson"],
            colors=[(2, IDC)])

    def gest(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Q-learning models conditional outcome levels as well as treatment contrasts. <bookmark mark='b'/> Structural nested models instead parameterize the treatment blip. Specific g-estimation procedures can be robust to some nuisance misspecification when the blip model and the required treatment or outcome nuisance are correct. <bookmark mark='c'/> A-learning similarly focuses on action advantages. <bookmark mark='d'/> Known randomization probabilities help with nuisance robustness, but do not protect a wrong blip model or an incorrectly specified treatment history.",
            [(r"\text{Q-learning}", r":", r"\text{models the outcome}", 40),
             (r"\text{g-estimation}", r":", r"\text{models only the blip } \gamma(h, a)", 40),
             (r"\text{A-learning}", r":", r"\text{the advantage of each action}", 40),
             (r"\text{robust}", r":", r"\text{known propensities, \ wrong outcome model}", 40)],
            [r"a strong demand", r"Robins (2004)", r"Murphy (2003)", r"SMARTs help"],
            colors=[(1, IDC)])
