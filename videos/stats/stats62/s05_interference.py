from __future__ import annotations

import numpy as np

from videos.stats.stats62.common import *  # noqa: F403


class Interference(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter four. Interference: when one person's treatment affects another's outcome.", 4,
                            r"Interference and networks", r"Spillovers", lit=(2017,))
        self.sutva()
        self.versions()
        self.exposure()
        self.vaccines()
        self.network()
        self.estimates()
        self.designs()
        self.dependence()

    def sutva(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Many individual-level analyses assume no interference, although earlier parts already considered group spillovers. <bookmark mark='b'/> Vaccines, classrooms, markets and networks can violate that assumption. <bookmark mark='c'/> With no restriction, one unit has a potential outcome for every assignment vector. A full-support randomized design can identify assignment-specific means in principle, but probabilities may be too small for useful estimation. It is wrong to say that nothing is identified. <bookmark mark='d'/> An exposure model reduces complexity by specifying which features of others' assignments matter.",
            [(r"\text{SUTVA}", r":", r"Y_i(z_1, \dots, z_n) = Y_i(z_i)", 40),
             (r"\text{broken by}", r":", r"\text{vaccines, \ classrooms, \ markets, \ networks}", 40),
             (r"\text{in general}", r":", r"2^n \text{ potential outcomes per unit}", 40),
             (r"\text{needed}", r":", r"\text{a model of who affects whom}", 40)],
            [r"Rubin (1980)", r"spillovers", r"nothing identified", r"Part 35's groups"],
            colors=[(2, NAIVEC)])

    def exposure(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Exposure mappings group assignments assumed to have the same effect on each unit. <bookmark mark='b'/> Here the mapping uses own treatment and whether any neighbor is treated, giving four labels. <bookmark mark='c'/> With independent Bernoulli treatment, probabilities are available exactly from each unit's degree. Isolated units have zero probability of neighbor-treated exposures; pseudocount smoothing cannot create that support. <bookmark mark='d'/> Each contrast must use a common population with positive probabilities for both compared exposures. Our spillover contrast uses nonisolates, while the direct-alone contrast can use all units.",
            [(r"\text{exposure}", r":", r"f(z, i) = (z_i, \ \mathbf 1\{\text{a neighbour treated}\})", 40),
             (r"\text{four conditions}", r":", r"(0, 0), \ (0, 1), \ (1, 0), \ (1, 1)", 40),
             (r"\pi_i(k)", r"=", r"P(f(Z, i) = k) \ \text{under the design}", 40),
             (r"\hat\mu(k)", r"=", r"\textstyle\sum_{i: f = k} Y_i/\pi_i(k) \big/ \sum_{i: f = k} 1/\pi_i(k)", 40)],
            [r"Aronow \& Samii (2017)", r"a modelling choice", r"exact here; \ simulation for more complex designs", r"Part 18's H\'ajek"],
            colors=[(3, IDC)])

    def network(self):
        d = load("interference")
        pos, edges, e = np.asarray(d["pos"]), np.asarray(d["edges"]), np.asarray(d["exposure"])
        A = axes([0, 1], [0, 1], x_length=5.6, y_length=5.6, xlabel=r"", ylabel=r"", center=[-3.0, -0.1, 0])
        ax = A.ax
        em = ExposureMap(ax, pos, edges)
        links, units = em.links(), em.units(e, 0.05)
        leg = em.legend(22)
        counts = [int(np.sum(e == k)) for k in range(4)]
        side = VGroup(label(rf"{d['n']} units, \ neighbours within 0.06", font_size=22),
                      label(rf"mean degree {d['deg']:.1f}; \ treated with probability {d['p']}", font_size=22, color=GREY_A),
                      leg,
                      label(rf"counts: \ {counts[0]}, \ {counts[1]}, \ {counts[2]}, \ {counts[3]}", font_size=22, color=GREY_A))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The exposure map shows four hundred units in a geometric network. <bookmark mark='b'/> Treatment is independently assigned with probability three tenths. <bookmark mark='c'/> Colors distinguish the four own-treatment and neighbor-exposure combinations. <bookmark mark='d'/> Observing all four colors somewhere does not establish positivity for every unit. Isolates cannot have a treated neighbor, and the estimand must account for them."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(Create(links), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(units, lag_ratio=0.002), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def estimates(self):
        d = load("interference")
        m, s = d["mean"], d["sd"]
        hdr = [r"estimand", r"truth", r"estimate (mean $\pm$ sd)"]
        rows = [[r"direct: \ treated alone vs control alone", r"2", rf"{m['direct']:.2f} $\pm$ {s['direct']:.2f}"],
                [r"spillover: \ control with vs without", r"1", rf"{m['spill']:.2f} $\pm$ {s['spill']:.2f}"],
                [r"total HT: \ all treated vs none", rf"{d['truth_total']:.3f}", rf"{m['total']:.2f} $\pm$ {s['total']:.2f}"],
                [r"naive difference in means", r"?", rf"{m['naive']:.2f} $\pm$ {s['naive']:.2f}"]]
        tab = table_rows([hdr] + rows, font_size=28, col_buff=0.8, row_buff=0.35, colors=[GREY_B, IDC, IDC, IDC, NAIVEC]).move_to([0, 0.5, 0])
        note_ = label(r"$Y_i = Y_i(0) + 2z_i + \mathbf 1\{\text{a neighbour treated}\} + \text{noise}$; \ 300 assignments", font_size=24, color=GREY_A).next_to(tab, DOWN, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> We repeat three hundred randomized assignments and add fresh outcome noise. The table reports means and standard deviations across those repetitions, not independent-observation confidence intervals. <bookmark mark='b'/> The direct-alone Hajek comparison has true effect two on its common support. <bookmark mark='c'/> The spillover comparison has true effect one among nonisolates. <bookmark mark='d'/> The assumed any-treated-neighbor model also permits estimation of the global all-treated-versus-none contrast: use Horvitz-Thompson weights for each unit's corresponding exposure. Its population mean is three minus the isolated fraction, because isolates receive no spillover. A globally all-treated assignment need not be observed. <bookmark mark='e'/> The naive arm difference is near two here under Bernoulli assignment. It does not estimate the spillover or that global total effect."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_), FadeIn(simulated_tag(r"simulated, \ 300 assignments")))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]))
            vo.wait_until("e")
            self.play(FadeIn(tab[4]))
        self.clear_scene()

    def designs(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The design can be chosen to target the spillovers. <bookmark mark='b'/> Cluster "
            "randomization, treating whole communities, makes the treat-everyone condition common, so the total effect "
            "becomes estimable: Johan Ugander and co-authors' graph cluster randomization, in 2013. <bookmark mark='c'/> "
            "Saturation designs randomize the fraction treated in each group, separating direct from spillover effects "
            "at several doses. <bookmark mark='d'/> In online marketplaces, where buyers and sellers interact, two-sided "
            "and switchback designs are now standard practice.",
            [(r"\text{cluster}", r":", r"\text{treat whole communities}", 40),
             (r"\text{graph clusters}", r":", r"\text{Ugander et al. (2013)}", 40),
             (r"\text{saturation}", r":", r"\text{randomize the fraction treated}", 40),
             (r"\text{marketplaces}", r":", r"\text{two-sided, \ switchback designs}", 40)],
            [r"design, \ not analysis", r"total effects", r"Baird et al. (2018)", r"Part 64's experiments"],
            colors=[(1, IDC)])

    def dependence(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Inference is harder too. <bookmark mark='b'/> Outcomes are dependent through the network, "
            "so the variance of the Hájek estimator is not the independent formula. Aronow and Samii give conservative "
            "variance bounds. <bookmark mark='c'/> And the exposure mapping might be wrong: Michael Leung showed in 2022 "
            "that with approximate neighbourhood interference, where influence decays with distance, the estimators remain "
            "consistent and asymptotically normal. <bookmark mark='d'/> For observational network data, with no design to "
            "lean on, identification needs strong assumptions about who influences whom and why: an open area.",
            [(r"\text{dependence}", r":", r"\text{outcomes linked through the network}", 40),
             (r"\text{variance}", r":", r"\text{conservative bounds}", 40),
             (r"\text{misspecified exposure}", r":", r"\text{approximate neighbourhood interference}", 38),
             (r"\text{observational}", r":", r"\text{open}", 40)],
            [r"not independent", r"Aronow \& Samii", r"Leung (2022)", r"chapter 10"],
            colors=[(2, IDC), (3, NAIVEC)])

    def vaccines(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Vaccine trials gave the vocabulary. <bookmark mark='b'/> M. Elizabeth Halloran and Claudio "
            "Struchiner distinguished, in 1991 and 1995, the direct effect of a vaccine on the vaccinated, the indirect "
            "effect on the unvaccinated around them, and the total and overall effects. <bookmark mark='c'/> Michael Hudgens "
            "and Halloran's two-stage randomization, Part thirty-five's design, randomizes communities to coverage levels, "
            "then individuals within them. <bookmark mark='d'/> Herd immunity is an indirect effect: in a cholera vaccine "
            "trial in Bangladesh, the unvaccinated in high-coverage neighbourhoods were protected too, as John Ali and "
            "co-authors reported in 2005.",
            [(r"\text{direct}", r":", r"\text{on the vaccinated}", 40),
             (r"\text{indirect}", r":", r"\text{on those around them}", 40),
             (r"\text{two-stage}", r":", r"\text{coverage, \ then individuals}", 40),
             (r"\text{herd immunity}", r":", r"\text{an indirect effect}", 40)],
            [r"Halloran \& Struchiner (1991, 1995)", r"spillover", r"Hudgens \& Halloran (2008)", r"Ali et al. (2005)"],
            colors=[(3, IDC)])

    def versions(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> SUTVA has a second half, often forgotten: no hidden versions of treatment. <bookmark "
            "mark='b'/> Treatment with a drug means one dose, one schedule; treatment with surgery means one surgeon's "
            "skill or another's. <bookmark mark='c'/> If versions differ in effect, the average effect is an average over "
            "whatever mix of versions the data contain, and changes when the mix does. <bookmark mark='d'/> Defining the "
            "intervention precisely, as a target trial would, is the remedy, and it is a modelling decision, not a "
            "statistical one.",
            [(r"\text{second half}", r":", r"\text{no hidden versions of treatment}", 40),
             (r"\text{examples}", r":", r"\text{doses, \ schedules, \ surgeons}", 40),
             (r"\text{else}", r":", r"\text{the effect of the observed mix}", 40),
             (r"\text{remedy}", r":", r"\text{define the intervention}", 40)],
            [r"Rubin (1980)", r"versions", r"mix-dependent", r"Hern\'an's well-defined interventions"],
            colors=[(2, NAIVEC)])
