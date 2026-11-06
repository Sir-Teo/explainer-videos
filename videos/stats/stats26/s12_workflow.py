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
        with self.voiceover(
            "<bookmark mark='a'/> Step three has a sharp form: simulation-based calibration. Draw a true parameter from the "
            "prior and fake data from the model. <bookmark mark='b'/> Run your posterior code on the fake data and take L "
            "draws. <bookmark mark='c'/> Record where the true value ranks among them. <bookmark mark='d'/> If the code is "
            "right, the truth is just another draw from the posterior, averaged over the prior, so its rank is uniform. "
            "Repeat thousands of times and look at the histogram."
        ) as vo:
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
            "<bookmark mark='a'/> Three versions of the posterior code for a normal mean with two observations, four thousand "
            "simulations each. <bookmark mark='b'/> The correct code gives a flat histogram. <bookmark mark='c'/> Code whose "
            "posterior variance is half what it should be gives a U: the truth too often falls outside all the draws, so "
            "its intervals would be too narrow. <bookmark mark='d'/> Code with a slip in the prior mean gives a slope: the "
            "posterior is systematically off-centre. <bookmark mark='e'/> Both bugs would produce plausible-looking "
            "posteriors on real data. Only the simulation exposes them."
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
        rows = [r for r in load_all(upto=26) if r.part == 26]
        b = coverage_board(rows, lit_part=26, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        w = load("board")["width"]
        with self.voiceover(
            "<bookmark mark='a'/> The Board, on the World's schools: draw eight schools, ten pupils from each, and estimate "
            "each school's true mean score; a thousand times. Each school's own interval covers ninety-four point eight "
            "percent: kept. <bookmark mark='b'/> Complete pooling, one mean for all, covers thirty-two percent: broken. "
            "<bookmark mark='c'/> The hierarchical model's ninety-five percent credible intervals cover ninety-three point "
            "nine percent, just short, and so broken by the Board's strict rule, while being eleven percent narrower than "
            "no pooling's. A credible interval is calibrated on average over its prior; the World's schools are close to "
            "that normal population, not exactly it."
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
            cmath(r"\hat R", r"<", r"1.01: \ \text{chains started apart now agree}", font_size=30),
            cmath(r"\text{ESS}", r">", r"400: \ \text{enough independent information}", font_size=30),
            cmath(r"\text{divergences}", r"=", r"0: \ \text{the sampler saw the whole posterior}", font_size=30),
            cmath(r"\text{exact here}", r":", r"\text{the grid needs none of these, \ Part 27's do}", font_size=30),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"Gelman \& Rubin (1992); \ Vehtari et al.\ (2021)"), why(r"Part 15's effective sample size"),
                why(r"Hamiltonian Monte Carlo's alarm"), why(r"step four of the workflow")]
        with self.voiceover(
            "<bookmark mark='a'/> Step four checks the computation. When the posterior comes from Markov chains, run several "
            "from scattered starting points and check that they agree: the R-hat statistic should be within one percent of "
            "one. <bookmark mark='b'/> Check the effective sample size, Part 15's measure of how many independent draws the "
            "correlated chain is worth. <bookmark mark='c'/> And with Hamiltonian Monte Carlo, check for divergences, "
            "warnings that the sampler couldn't follow the posterior's curvature. <bookmark mark='d'/> Our grid was exact and "
            "needed none of this; Part 27 will need all of it, and the eight schools will set off the alarm."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
