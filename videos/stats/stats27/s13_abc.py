from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats27.common import *  # noqa: F403


class ABC(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.sufficient()
        self.insufficient()
        self.abc_smc()
        self.neural()
        self.sbc_board()

    def card(self):
        card = chapter_card(12, r"Likelihood-free inference", r"When you can simulate but not evaluate", lit=(2002,), part=PART)
        with self.voiceover("Chapter twelve. Likelihood-free inference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\theta \sim p(\theta)", r",", r"\ y^* \sim p(y \mid \theta)", font_size=30),
            cmath(r"\text{keep } \theta", r"\text{ if }", r"\|S(y^*) - S(y)\| \le \epsilon", font_size=30),
            cmath(r"\epsilon \to 0", r":", r"\text{the kept } \theta \sim p(\theta \mid S(y))", font_size=30),
            cmath(r"\text{only exact if}", r":", r"S \text{ is sufficient}", font_size=30),
        ]
        rows[2][2].set_color(HIT)
        whys = [why(r"draw a parameter, \ simulate data"), why(r"summaries close enough to the real ones"),
                why(r"Pritchard et al.\ (1999); \ Beaumont et al.\ (2002)"), why(r"otherwise a different posterior")]
        with self.voiceover(
            "<bookmark mark='a'/> Some models can be simulated but their likelihood can't be written down: population "
            "genetics, epidemics, agent-based economies. Approximate Bayesian computation needs only the simulator. Draw a "
            "parameter from the prior and simulate a data set. <bookmark mark='b'/> Keep the parameter if the simulated "
            "data's summaries are within epsilon of the real ones. <bookmark mark='c'/> As epsilon shrinks, the kept "
            "parameters approach the posterior given the summaries. <bookmark mark='d'/> That is the posterior given the data "
            "only if the summaries are sufficient."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def panel(self, which):
        d = load("abc")
        e = np.asarray(d["edges"])
        res = d["res"][which]
        g = np.asarray(d["grid"])
        ymax = 1.4
        A = axes([0, 7], [0, ymax], x_length=7.2, y_length=4.2, xlabel=r"Poisson rate $\lambda$", ylabel=r"density",
                 xticks=[0, 2, 4, 6], yticks=[], center=[-2.0, 0.3, 0])
        ax = A.ax
        ex = curve(ax, g, np.minimum(d["exact_pdf"], ymax), EXACTC, 3.5)
        bars = {eps: hist_bars(ax, e, np.minimum(res[eps]["hist"], ymax), color=col, opacity=0.45)
                for eps, col in (("1.0", RES), ("0.3", PATH), ("0.05", SAMPLER))}
        return A, ex, bars, res, d

    def sufficient(self):
        A, ex, bars, res, d = self.panel("mean")
        rows = fit_rows(VGroup(
            label(rf"15 counts; \ Gamma(2, 1) prior; \ summary: \ the mean", font_size=22),
            label(rf"gold: \ the exact posterior, \ mean {d['exact_mean']:.2f}", font_size=22, color=EXACTC),
            label(rf"$\epsilon = 1$: \ mean {res['1.0']['mean']:.2f}, \ SD {res['1.0']['sd']:.2f}", font_size=22, color=RES),
            label(rf"$\epsilon = 0.05$: \ {res['0.05']['mean']:.2f}, \ SD {res['0.05']['sd']:.2f} \ (exact {d['exact_sd']:.2f})", font_size=22, color=SAMPLER),
            label(rf"but only {100 * res['0.05']['accept']:.1f}\% of simulations kept", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A test case with a known answer: fifteen Poisson counts, a gamma prior, and the sample mean "
            "as the summary, which is sufficient. <bookmark mark='b'/> The exact posterior is in gold. <bookmark mark='c'/> "
            "With a loose tolerance of one, ABC's posterior is too wide. <bookmark mark='d'/> With point oh five it matches the "
            "exact one closely, <bookmark mark='e'/> but only one simulation in eighty is kept: ABC's accuracy is bought with "
            "simulations."
        ) as vo:
            self.play(FadeIn(A), Create(ex))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars["1.0"]], lag_ratio=0.01), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeOut(bars["1.0"]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars["0.05"]], lag_ratio=0.01), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def insufficient(self):
        A, ex, bars, res, d = self.panel("median")
        rows = fit_rows(VGroup(
            label(r"the same data; \ summary: \ the median", font_size=22),
            label(rf"$\epsilon = 0.05$: \ mean {res['0.05']['mean']:.2f}, \ SD {res['0.05']['sd']:.2f}", font_size=22, color=SAMPLER),
            label(rf"exact: \ {d['exact_mean']:.2f}, \ {d['exact_sd']:.2f}", font_size=22, color=EXACTC),
            label(r"not just wider: \ shifted", font_size=22, color=RES),
            label(r"shrinking $\epsilon$ cannot fix a poor summary", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now the same data with the median as the summary, which throws information away. "
            "<bookmark mark='b'/> Even at the tightest tolerance, ABC's posterior has mean two point one and standard "
            "deviation point four nine, <bookmark mark='c'/> where the exact answer is two point five six and point four. "
            "<bookmark mark='d'/> It isn't merely wider; it is in the wrong place, because the median of Poisson counts is "
            "biased low and can only take a few values. <bookmark mark='e'/> No tolerance can fix a poor summary: choosing "
            "summaries is the heart of ABC."
        ) as vo:
            self.play(FadeIn(A), Create(ex))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars["0.05"]], lag_ratio=0.01), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def neural(self):
        rows = fit_rows(VGroup(
            label(r"regression ABC: \ adjust kept draws by regressing $\theta$ on $S$ \ (Beaumont et al.\ 2002)", font_size=24),
            label(r"synthetic likelihood: \ a normal fitted to simulated summaries \ (Wood 2010)", font_size=24),
            label(r"neural posterior estimation: \ train a network to output $p(\theta \mid y)$ from simulations", font_size=24, color=SAMPLER),
            label(r"amortized: \ train once, \ infer in milliseconds for every new data set", font_size=24, color=HIT),
            label(r"and check every one of them with SBC", font_size=24, color=PATH),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Better versions keep more of the simulations: Mark Beaumont's regression adjustment corrects "
            "each kept draw for how far its summaries missed. <bookmark mark='b'/> Simon Wood's synthetic likelihood fits a "
            "normal to simulated summaries. <bookmark mark='c'/> And neural posterior estimation trains a network to map "
            "simulated data straight to a posterior, <bookmark mark='d'/> after which inference on any new data set is a "
            "single forward pass. <bookmark mark='e'/> All of them approximate, so all of them need checking, by Part 26's "
            "simulation-based calibration: the Board."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def sbc_board(self):
        rows = [r for r in load_all(upto=27) if r.part == 27]
        b = coverage_board(rows, lit_part=27, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        r = {x.method: x for x in rows}
        with self.voiceover(
            "<bookmark mark='a'/> The Board tests computation itself. Draw the eight schools' parameters from the prior, "
            "simulate eight estimates, and compute each school's ninety percent interval; a hundred times. If the "
            "computation is right, the intervals cover ninety percent of the true effects, averaged over the prior. The exact "
            "grid draws cover ninety point five percent. <bookmark mark='b'/> NUTS on the non-centred model, ninety point "
            "nine. <bookmark mark='c'/> NUTS on the centred model, ninety-one: averaged over the prior, its trouble at "
            "small tau barely moves the schools' coverage, though chapter seven showed it distorts tau itself. "
            "<bookmark mark='d'/> Mean-field ADVI covers eighty-seven and a half percent, short, as its narrow "
            "posteriors predict, though within the Board's margin for eight hundred intervals. Calibration can pass "
            "while a particular data set's answer is still biased; it checks the computation on average, not case by "
            "case."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        self.wait(1.0)
        self.clear_scene()

    def abc_smc(self):
        rows = [
            cmath(r"\text{rejection}", r":", r"\text{most simulations wasted as } \epsilon \to 0", font_size=30),
            cmath(r"\text{ABC-MCMC}", r":", r"\text{Metropolis with simulate-and-compare}", font_size=30),
            cmath(r"\text{ABC-SMC}", r":", r"\text{particles through shrinking } \epsilon_1 > \epsilon_2 > \cdots", font_size=30),
            cmath(r"\text{all}", r":", r"\text{target } p(\theta \mid \|S(y^*) - S(y)\| \le \epsilon)", font_size=30),
        ]
        rows[2][-1].set_color(HIT)
        whys = [why(r"one in eighty kept, \ here"), why(r"Marjoram et al.\ (2003)"), why(r"Sisson, Fan \& Tanaka (2007); \ Beaumont et al.\ (2009)"), why(r"cheaper, \ not different")]
        with self.voiceover(
            "<bookmark mark='a'/> Rejection is wasteful: at small tolerances almost every simulation is thrown away. "
            "<bookmark mark='b'/> ABC-MCMC moves a Metropolis chain through parameter space, accepting a proposal only if its "
            "simulated data land close enough. <bookmark mark='c'/> ABC-SMC passes a population of particles through a "
            "sequence of shrinking tolerances, as chapter nine's tempering did with temperatures. <bookmark mark='d'/> All "
            "target the same approximate posterior; they differ in how many simulations it costs."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
