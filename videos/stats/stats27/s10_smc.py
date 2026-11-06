from __future__ import annotations

import numpy as np

from videos.stats.stats27.common import *  # noqa: F403


class SMC(VoiceoverScene):
    def construct(self):
        self.card()
        self.filter_idea()
        self.filter_picture()
        self.noise()
        self.degeneracy()
        self.tempering()
        self.evidence()

    def card(self):
        card = chapter_card(9, r"Sequential Monte Carlo", r"A population of particles, \ reweighted and resampled", lit=(1993,), part=PART)
        with self.voiceover("Chapter nine. Sequential Monte Carlo."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def filter_idea(self):
        rows = [
            cmath(r"x_t", r"=", r"x_{t-1} + w_t, \ \ y_t = x_t + v_t", font_size=30),
            cmath(r"\text{propagate}", r":", r"x_t^{(i)} \sim p(x_t \mid x_{t-1}^{(i)})", font_size=30),
            cmath(r"\text{weight}", r":", r"w^{(i)} \propto p(y_t \mid x_t^{(i)})", font_size=30),
            cmath(r"\text{resample}", r":", r"\text{copy heavy particles, \ drop light ones}", font_size=30),
        ]
        rows[2][2].set_color(SAMPLER)
        whys = [why(r"a hidden state, \ seen with noise: \ Part 17"), why(r"move each particle by the dynamics"),
                why(r"importance sampling, \ chapter one"), why(r"Gordon, Salmond \& Smith (1993)")]
        with self.voiceover(
            "<bookmark mark='a'/> When data arrive one at a time, posteriors must be updated one at a time. Take Part 17's "
            "local-level model: a hidden level that wanders, observed with noise. <bookmark mark='b'/> A particle filter "
            "keeps a cloud of guesses for the level. Move each by the model's dynamics. <bookmark mark='c'/> Weight each by "
            "how well it predicts the new observation: chapter one's importance sampling. <bookmark mark='d'/> Then resample: "
            "copy the heavily weighted particles and drop the light ones, so the cloud doesn't degenerate. This bootstrap "
            "filter is Neil Gordon, David Salmond and Adrian Smith's, from 1993."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def filter_picture(self):
        d = load("smc")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        km, ks, pf = np.asarray(d["kalman"]), np.asarray(d["kalman_sd"]), np.asarray(d["pf"])
        T = len(y)
        lo, hi = float(min(y.min(), x.min())) - 1, float(max(y.max(), x.max())) + 1
        A = axes([0, T], [lo, hi], x_length=8.0, y_length=4.4, xlabel=r"time", ylabel=r"level", xticks=[0, 20, 40, 60],
                 yticks=[], center=[-1.8, 0.3, 0])
        ax = A.ax
        obs = VGroup(*[Dot(ax.c2p(t, v), radius=0.045, color=GREY_B) for t, v in enumerate(y)])
        truth = polyline(ax, np.arange(T), x, EXACTC, 2.0)
        band = Polygon(*([ax.c2p(t, m + 2 * s) for t, (m, s) in enumerate(zip(km, ks))] +
                         [ax.c2p(t, m - 2 * s) for t, (m, s) in reversed(list(enumerate(zip(km, ks))))]),
                       stroke_width=0, fill_color=SAMPLER, fill_opacity=0.18)
        kal = polyline(ax, np.arange(T), km, SAMPLER, 3)
        par = DashedVMobject(polyline(ax, np.arange(T), pf, HIT, 3), num_dashes=60)
        rows = fit_rows(VGroup(
            label(r"grey: \ 60 noisy observations", font_size=22, color=GREY_B),
            label(r"gold: \ the hidden level", font_size=22, color=EXACTC),
            label(r"blue: \ the exact Kalman filter, \ $\pm 2$ SD", font_size=22, color=SAMPLER),
            label(r"green dashed: \ 1,000 particles", font_size=22, color=HIT),
            label(r"the particles track the exact answer", font_size=22, color=HIT),
        ), 3.6, 0.42, [5.0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Sixty noisy observations of a wandering level, <bookmark mark='b'/> whose true path is in "
            "gold. <bookmark mark='c'/> For this linear Gaussian model the exact answer is Part 38's Kalman filter, in blue "
            "with its two-standard-deviation band. <bookmark mark='d'/> The particle filter, a thousand particles, dashed "
            "green, <bookmark mark='e'/> lies on top of it. The particle filter needs no linearity or normality, so it carries "
            "over unchanged to models where no exact filter exists."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(o) for o in obs], lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(band), Create(kal), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(par), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def noise(self):
        d = load("smc")
        sp = d["spread"]
        hdr = [r"\textbf{particles}", r"\textbf{log likelihood, \ mean of 40 runs}", r"\textbf{SD across runs}"]
        body = [[f"{int(k):,}", f"{sp[k]['mean']:.2f}", f"{sp[k]['sd']:.2f}"] for k in ("50", "200", "1000")]
        tb = table_rows([hdr] + body + [[r"exact (Kalman)", f"{d['ll_kalman']:.2f}", r"---"]], font_size=26, col_buff=0.9,
                        row_buff=0.3, colors=[GREY_A, RES, SAMPLER, HIT, EXACTC])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"the likelihood estimate is unbiased; \ its log is slightly low", font_size=22),
            label(r"its noise shrinks like $1/\sqrt N$: \ pseudo-marginal MCMC runs Metropolis on it", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The filter also estimates the likelihood of the whole series, as a product of each "
            "observation's average weight. <bookmark mark='b'/> With fifty particles the estimate's log varies by one point "
            "two from run to run; with two hundred, by point six six; with a thousand, by point two. <bookmark mark='c'/> The "
            "estimate itself is unbiased, so its log is slightly low on average, and it converges on the Kalman filter's "
            "exact value. <bookmark mark='d'/> Christophe Andrieu and Gareth Roberts showed that Metropolis–Hastings run with "
            "such a noisy but unbiased likelihood still targets the exact posterior: pseudo-marginal MCMC, for models whose "
            "likelihood can only be simulated."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[4]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[1:4]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def tempering(self):
        rows = [
            cmath(r"\pi_\phi(\theta)", r"\propto", r"p(\theta)\, p(y \mid \theta)^\phi, \ \ 0 = \phi_0 < \phi_1 < \dots < \phi_K = 1", font_size=28),
            cmath(r"\text{reweight}", r":", r"w \propto p(y \mid \theta)^{\phi_{k+1} - \phi_k}", font_size=30),
            cmath(r"\text{choose } \phi_{k+1}", r":", r"\text{so the ESS falls to half}", font_size=30),
            cmath(r"\log p(y)", r"=", r"\textstyle\sum_k \log \overline{w}_k", font_size=32),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"a bridge from prior to posterior"), why(r"importance sampling, \ one rung at a time"),
                why(r"adaptive; \ then resample and move by MCMC"), why(r"the evidence, \ for free: \ Part 26's chapter eight")]
        with self.voiceover(
            "<bookmark mark='a'/> The same machinery reaches static posteriors by tempering. Build a ladder of distributions "
            "from the prior, at temperature zero, to the posterior, at one, raising the likelihood to a power that climbs "
            "step by step. <bookmark mark='b'/> Particles drawn from the prior are reweighted from one rung to the next, "
            "<bookmark mark='c'/> with each new temperature chosen so the effective sample size falls to half; then they are "
            "resampled and moved by a few Metropolis steps. <bookmark mark='d'/> And the average weights along the way "
            "multiply up to the evidence, the hard integral behind Part 26's Bayes factors."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def evidence(self):
        d = load("smc")
        hdr = [r"\textbf{polynomial degree}", r"\textbf{exact log evidence}", r"\textbf{SMC, \ 2,000 particles}", r"\textbf{rungs}"]
        body = [[f"{e['deg']}", f"{e['exact']:.2f}", f"{e['smc']:.2f}", f"{len(e['phi']) - 1}"] for e in d["evidence"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.3, colors=[GREY_A] + [None] * 4)
        for r in tb[1:]:
            r[1].set_color(EXACTC)
            r[2].set_color(HIT)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"Part 26's twenty points from a cubic", font_size=22),
            label(r"SMC finds the evidence within about 0.15, \ and the same winner, \ degree 3", font_size=22, color=HIT),
        ), 12.0, 0.22, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 26's twenty points from a cubic, whose evidence we could compute exactly. "
            "<bookmark mark='b'/> Tempered SMC with two thousand particles, five to seven rungs, finds each log evidence "
            "within about point one five of the truth, and picks the same winner, degree three. With no closed form, it "
            "would be the way to compute a Bayes factor."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), FadeIn(foot[1]))
        self.wait(1.0)
        self.clear_scene()

    def degeneracy(self):
        rows = [
            cmath(r"\text{without resampling}", r":", r"\text{one particle gets all the weight}", font_size=30),
            cmath(r"\text{with it}", r":", r"\text{paths coalesce: \ the distant past is one ancestor}", font_size=30),
            cmath(r"\text{unknown parameters}", r":", r"\text{particle MCMC wraps the filter in Metropolis}", font_size=30),
            cmath(r"\text{dimension}", r":", r"\text{particle counts grow fast with the state's size}", font_size=30),
        ]
        rows[3][-1].set_color(RES)
        whys = [why(r"weight degeneracy"), why(r"path degeneracy"), why(r"Andrieu, Doucet \& Holenstein (2010)"), why(r"Bengtsson, Bickel \& Li (2008)")]
        with self.voiceover(
            "<bookmark mark='a'/> Particle methods have their own pathologies. Without resampling, after a few steps one "
            "particle carries nearly all the weight. <bookmark mark='b'/> With resampling, the particles' histories "
            "coalesce, so the distant past is represented by a single ancestor. <bookmark mark='c'/> To learn the model's "
            "fixed parameters too, particle MCMC wraps the filter inside Metropolis–Hastings. <bookmark mark='d'/> And in high "
            "dimensions the number of particles needed grows very quickly: particle filters suit small hidden states, not "
            "large ones."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
