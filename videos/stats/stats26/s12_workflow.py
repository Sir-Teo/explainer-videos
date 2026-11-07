from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats26.common import *  # noqa: F403


class Workflow(VoiceoverScene):
    def construct(self):
        self.card()
        self.steps()
        self.sbc_idea()
        self.sbc_pictures()
        self.computation()
        self.board()
        self.sensitivity()

    def card(self):
        card = chapter_card(11, r"Workflow", r"Building a model you can defend", lit=(2020,), part=PART)
        with self.voiceover("Chapter eleven. The Bayesian workflow."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def steps(self):
        items = [
            (r"1. \ write the model: \ what generated the data?", WHITE),
            (r"2. \ prior predictive checks: \ are the priors believable?", PRIOR),
            (r"3. \ fit on fake data with known parameters: \ does it recover them?", PATH),
            (r"4. \ fit the real data; \ check the computation", POST),
            (r"5. \ posterior predictive checks: \ what does the model miss?", SHRUNK),
            (r"6. \ expand or change the model; \ compare; \ report all of it", HIT),
        ]
        rows = fit_rows(VGroup(*[label(t, font_size=24, color=c) for t, c in items]), 12.4, 0.45, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Andrew Gelman and colleagues set out a Bayesian workflow in 2020, the habits that turn a "
            "posterior into an analysis. First, write down a model of how the data arose. <bookmark mark='b'/> Check that "
            "the priors predict believable data. <bookmark mark='c'/> Fit the model to fake data simulated with known "
            "parameters, and see whether it recovers them. <bookmark mark='d'/> Only then fit the real data, and check that "
            "the computation worked. <bookmark mark='e'/> Check what the fitted model fails to reproduce. "
            "<bookmark mark='f'/> Then improve the model, compare the versions, and report the whole path, not just the last "
            "model standing."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def sbc_idea(self):
        rows = [
            cmath(r"\tilde\theta \sim p(\theta)", r",", r"\ \tilde y \sim p(y \mid \tilde\theta)", font_size=30),
            cmath(r"\theta^{(1)}, \dots, \theta^{(L)}", r"\sim", r"\text{your posterior given } \tilde y", font_size=30),
            cmath(r"r", r"=", r"\#\{\ell : \theta^{(\ell)} < \tilde\theta\} \in \{0, \dots, L\}", font_size=30),
            cmath(r"\text{if correct}", r":", r"r \text{ is uniform: \ the truth is just another draw}", font_size=30),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"draw a truth from the prior, \ then data"), why(r"run the code you want to test"),
                why(r"where the truth ranks among the draws"), why(r"Talts et al.\ (2018); \ Cook, Gelman \& Rubin (2006)")]
        intro = label('Correct independent posterior draws imply prior-averaged rank uniformity', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Step three has a sharp form: simulation-based calibration. Draw a true parameter "
            "from the prior and fake data from the model. <bookmark mark='b'/> Run your posterior code on the fake "
            "data and take L draws. <bookmark mark='c'/> Record where the true value ranks among them. <bookmark "
            "mark='d'/> With a proper generative prior, a continuous parameter and independent correct posterior "
            "draws, prior-averaged ranks are uniform. Dependent draws or ties need separate treatment. Repeat "
            "thousands of times and look at the histogram."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sbc_pictures(self):
        d = load("sbc")
        L = d["L"]
        panels = VGroup()
        anims = []
        info = (("good", r"correct posterior", SHRUNK), ("overconfident", r"variance halved", RES), ("biased", r"wrong prior mean", POST))
        for k, (key, name, col) in enumerate(info):
            c = np.asarray(d[key]["counts"], float)
            A = axes([-0.5, L + 0.5], [0, 560], x_length=3.8, y_length=2.8, xlabel=rf"rank, \ {name}", ylabel=r"", xticks=[0, L],
                     yticks=[], center=[-4.5 + 4.5 * k, 0.7, 0])
            bars = bars_at(A.ax, list(range(L + 1)), c, 0.8, col, 0.8)
            exp = DashedLine(A.ax.c2p(-0.5, c.mean()), A.ax.c2p(L + 0.5, c.mean()), color=GREY_A, stroke_width=1.5)
            pl = label(rf"$\chi^2$ $p = {d[key]['p']:.2g}$", font_size=22, color=col).next_to(A, DOWN, buff=0.25)
            panels.add(A)
            anims.append((bars, exp, pl))
        foot = fit_rows(VGroup(
            label(r"4,000 simulations each; \ a normal mean with a normal prior and 2 observations", font_size=22),
            label(r"$\cup$: \ intervals too narrow; \ slope: \ a biased centre", font_size=22, color=PATH),
        ), 12.0, 0.2, [0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Three versions of the posterior code for a normal mean with two observations, four "
            "thousand simulations each. <bookmark mark='b'/> The correct code gives a flat histogram. <bookmark "
            "mark='c'/> Code whose posterior variance is half what it should be gives a U: the truth too often falls "
            "outside all the draws, so its intervals would be too narrow. <bookmark mark='d'/> Code with a slip in "
            "the prior mean gives a slope: the posterior is systematically off-centre. <bookmark mark='e'/> Both bugs"
            " would produce plausible-looking posteriors on real data. These simulations expose the two bugs. A flat "
            "histogram can still miss other bugs; it is a necessary diagnostic, not a proof that all posterior "
            "calculations are correct."
        ) as vo:
            self.play(FadeIn(panels), FadeIn(foot[0]))
            vo.wait_until("a")
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                bars, exp, pl = anims[k]
                self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), Create(exp), FadeIn(pl))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def board(self):
        rows = [r for r in coverage_rows() if r.part == 26]
        b = coverage_board(rows, lit_part=26, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        w = load("board")["width"]
        with self.voiceover(
            "<bookmark mark='a'/> The Board samples eight schools and ten pupils per school, repeating the complete "
            "experiment a thousand times. We estimate each finite school's mean score. No pooling covers about "
            "ninety-five percent. <bookmark mark='b'/> Complete pooling covers about thirty-two percent. <bookmark "
            "mark='c'/> Hierarchical numerical intervals cover about ninety-four percent and are narrower, but fall "
            "below the nominal level. The eight intervals within each experiment share a fitted model: the displayed "
            "Monte Carlo bands use variation across the thousand experiment-level coverage averages. Prior-average "
            "calibration is a theorem for a proper prior under its joint model, not a guarantee for our "
            "improper-hyperprior fit to the finite World."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        self.wait(1.0)
        self.clear_scene()

    def sensitivity(self):
        rows = fit_rows(VGroup(
            label(r"report the prior, \ and what changes when it does", font_size=24, color=PRIOR),
            label(r"the eight schools: \ uniform vs half-Cauchy, \ medians 5.2 and 4.8", font_size=24, color=SHRUNK),
            label(r"if the conclusion flips with a reasonable prior, \ the data have not settled it", font_size=24, color=RES),
            label(r"that is a finding, \ not a failure", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Finally, sensitivity. Report the prior you used, and show what moves when you change it "
            "within reason. <bookmark mark='b'/> For the eight schools, the uniform and half-Cauchy priors on tau agree "
            "closely, as chapter three showed. <bookmark mark='c'/> When a conclusion flips between reasonable priors, the "
            "data simply haven't settled the question, <bookmark mark='d'/> and saying so is a finding, not a failure."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def computation(self):
        rows = [
            cmath(r"\hat R", r"<", r"1.01: \ \text{a convergence screen, not a proof}", font_size=30),
            cmath(r"\text{ESS}", r">", r"400: \ \text{a guideline; check estimand-specific MC error}", font_size=30),
            cmath(r"\text{divergences}", r"=", r"0: \ \text{no detected divergence; mode coverage not guaranteed}", font_size=30),
            cmath(r"\text{grid here}", r":", r"\text{mesh and tail checks replace chain diagnostics}", font_size=30),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"Gelman \& Rubin (1992); \ Vehtari et al.\ (2021)"), why(r"Part 15's effective sample size"),
                why(r"Hamiltonian Monte Carlo's alarm"), why(r"step four of the workflow")]
        intro = label('Numerical diagnostics can detect problems without proving convergence', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> With Markov chains, use multiple dispersed starts and modern rank-normalized R-hat;"
            " values below one point oh one are a useful screen, not proof of convergence. <bookmark mark='b'/> Check"
            " bulk and tail effective sample sizes and Monte Carlo errors for the quantities you report. Four hundred"
            " is a guideline, not universal adequacy. <bookmark mark='c'/> Hamiltonian divergences flag integration "
            "problems, but zero divergences do not establish that every mode was explored. <bookmark mark='d'/> Our "
            "numerical grid needs mesh and tail checks instead of chain diagnostics. Computation still requires "
            "verification."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
