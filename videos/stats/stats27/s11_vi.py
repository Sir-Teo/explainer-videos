from __future__ import annotations

import numpy as np

from videos.stats.stats27.common import *  # noqa: F403


class VI(VoiceoverScene):
    def construct(self):
        self.card()
        self.elbo()
        self.mean_field()
        self.cavi()
        self.schools()
        self.richer()
        self.check()

    def card(self):
        card = chapter_card(10, r"Variational inference", r"Replace integration by optimization", lit=(1999,), part=PART)
        with self.voiceover("Chapter ten. Variational inference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def elbo(self):
        rows = [
            cmath(r"q^*", r"=", r"\arg\min_{q \in \mathcal Q} \mathrm{KL}(q \,\|\, p(\theta \mid y))", font_size=30),
            cmath(r"\log p(y)", r"=", r"\underbrace{E_q \log p(y, \theta) - E_q \log q}_{\text{ELBO}} + \mathrm{KL}(q \,\|\, p)", font_size=28),
            cmath(r"\text{maximize}", r":", r"\text{the ELBO: \ no normalizing constant needed}", font_size=30),
            cmath(r"\text{reverse KL}", r":", r"q \text{ avoids low } p; \ \text{restricted families often under-disperse}", font_size=30),
        ]
        rows[1][2].set_color(VIC)
        whys = [why(r"the nearest member of a simple family"), why(r"the evidence lower bound"),
                why(r"Jordan et al.\ (1999); \ Blei et al.\ (2017)"), why(r"`zero-forcing'")]
        with self.voiceover(
            "<bookmark mark='a'/> Variational inference trades sampling for optimization: find, within a simple "
            "family of distributions, the one closest to the posterior in Kullback–Leibler divergence. <bookmark "
            "mark='b'/> The log evidence splits into a lower bound plus that divergence, <bookmark mark='c'/> so "
            "maximizing the evidence lower bound, the ELBO, minimizes the divergence without ever computing the "
            "normalizing constant. <bookmark mark='d'/> But note the direction: the divergence from q to the "
            "posterior punishes q for putting mass where the posterior has little, and not the reverse. A restricted "
            "family and this divergence often favour concentrated approximations, but under-dispersion is not a "
            "universal theorem."
        ) as vo:
            intro = label('A restricted approximation maximizes an evidence lower bound', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mean_field(self):
        d = load("vi")
        rho = d["rho"]
        A = axes([-3, 3], [-3, 3], x_length=4.8, y_length=4.8, xlabel=r"$x_1$", ylabel=r"$x_2$", xticks=[-2, 0, 2], yticks=[-2, 0, 2],
                 center=[-3.0, 0.1, 0])
        ax = A.ax
        L = Landscape(ax, lambda X, Y: np.exp(-0.5 * (X ** 2 - 2 * rho * X * Y + Y ** 2) / (1 - rho ** 2)), (-3, 3), (-3, 3),
                      levels=[0.135], color=EXACTC, stroke_width=3)
        sd = np.asarray(d["mf_sd"])
        ell = ParametricFunction(lambda t: ax.c2p(d["mf_mean"][0]+2 * sd[0] * np.cos(t), d["mf_mean"][1]+2 * sd[1] * np.sin(t)), t_range=[0, TAU], color=VIC, stroke_width=3)
        rows = fit_rows(VGroup(
            label(rf"gold: \ the posterior's 2-SD contour, \ correlation {rho}", font_size=22, color=EXACTC),
            label(r"purple: \ finite stochastic ADVI fit, \ not the exact optimum", font_size=22, color=VIC),
            label(rf"its SDs: \ {sd[0]:.2f}, \ {sd[1]:.2f}; \ the true marginal SDs are 1", font_size=22, color=RES),
            label(r"$\sqrt{1 - \rho^2} = 0.44$: \ the conditional SD, \ not the marginal", font_size=22, color=GREY_A),
        ), 5.8, 0.42, [3.6, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The classic failure. The posterior is a correlated normal, its "
            "two-standard-deviation contour in gold. <bookmark mark='b'/> The purple ellipse is a stochastic ADVI fit"
            " with independent normal coordinates. The exact optimum in this family has SD root one minus rho "
            "squared, about point four four; the finite optimization has additional error. <bookmark mark='c'/> Its "
            "standard deviations are about point four, where the true ones are one: <bookmark mark='d'/> mean field "
            "recovers the conditional spread, the square root of one minus rho squared, and reports far too much "
            "certainty about each coordinate."
        ) as vo:
            self.play(FadeIn(A), FadeIn(L.levels))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ell), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def cavi(self):
        d = load("vi")
        rows = [
            cmath(r"q(\mu, \lambda)", r"=", r"q(\mu)\, q(\lambda)", font_size=32),
            cmath(r"\log q^*(\mu)", r"=", r"E_{q(\lambda)} \log p(x, \mu, \lambda) + c", font_size=30),
            cmath(r"\text{iterate}", r":", r"q(\mu) \text{ normal}, \ q(\lambda) \text{ gamma: \ closed-form updates}", font_size=28),
            cmath(r"\text{SD of } \mu", r":", rf"\text{{CAVI }} {d['cavi_sd_mu']:.3f} \ \text{{vs exact }} {d['exact_sd_mu']:.3f}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"a normal sample, \ mean and precision unknown"), why(r"each factor given the other's moments"),
                why(r"coordinate ascent: \ Bishop (2006), \ section 10.1.3"), why(r"under-dispersed in this example")]
        with self.voiceover(
            "<bookmark mark='a'/> For conditionally conjugate models the optimization has closed-form steps. A normal"
            " sample with unknown mean and precision, approximated by independent factors. <bookmark mark='b'/> The "
            "best factor for the mean, holding the other fixed, is the expected log joint under it, <bookmark "
            "mark='c'/> which is again normal, and the precision's is a gamma; alternate until they stop changing: "
            "coordinate ascent variational inference. <bookmark mark='d'/> It converges in a few iterations, and its "
            "standard deviation for the mean, point two seven six, is below the exact posterior's point two eight "
            "nine: under-dispersed in this example."
        ) as vo:
            intro = label('Coordinate updates optimize each factor against the others', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def schools(self):
        d = load("vi")
        lv, ln = np.asarray(d["logtau_vi"]), np.asarray(d["logtau_nuts"])
        edges = np.linspace(-5, 4, 46)
        hv, _ = np.histogram(lv, edges)
        hn, _ = np.histogram(ln, edges)
        hv=hv/len(lv)/np.diff(edges);hn=hn/len(ln)/np.diff(edges)
        A = axes([-5, 4], [0, float(max(hv.max(), hn.max())) * 1.1], x_length=7.2, y_length=4.2, xlabel=r"$\log\tau$",
                 ylabel=r"density", xticks=[-4, -2, 0, 2, 4], yticks=[], center=[-2.0, 0.3, 0])
        ax = A.ax
        bn = hist_bars(ax, edges, hn, color=SAMPLER, opacity=0.5)
        bv = hist_bars(ax, edges, hv, color=VIC, opacity=0.55)
        tv, tn = d["tau_vi"], d["tau_nuts"]
        rows = fit_rows(VGroup(
            label(r"the eight schools, \ non-centred", font_size=22),
            label(rf"blue: \ NUTS: \ $\tau$ 90\% [{tn[0]:.1f}, {tn[2]:.1f}]", font_size=22, color=SAMPLER),
            label(rf"purple: \ ADVI: \ [{tv[0]:.1f}, {tv[2]:.1f}]", font_size=22, color=VIC),
            label(r"too narrow, \ especially towards $\tau = 0$", font_size=22, color=RES),
            label(rf"PSIS $\hat k$ of $q$: \ {d['khat']:.2f}", font_size=22, color=PATH),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the eight schools, mean-field ADVI against NUTS. <bookmark mark='b'/> NUTS puts tau's "
            "ninety percent interval between point two six and ten point three. <bookmark mark='c'/> ADVI says point six five "
            "to six point seven: <bookmark mark='d'/> far too narrow, cutting off both the small values near the funnel's neck "
            "and the large ones. <bookmark mark='e'/> Chapter one's Pareto k-hat, using the approximation as a proposal for "
            "the posterior, comes out at point six two: below the alarm level, but not by much. Variational inference is fast "
            "and often good for means; for uncertainty, check it."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bn], lag_ratio=0.01), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bv], lag_ratio=0.01), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def check(self):
        rows = fit_rows(VGroup(
            label(r"VI wins: \ millions of parameters, \ data streams, \ topic models, \ deep nets", font_size=24, color=VIC),
            label(r"ADVI: \ transform to $\mathbb R^d$, \ Gaussian $q$, \ stochastic gradients \ (Kucukelbir et al.\ 2017)", font_size=24),
            label(r"VI loses: \ uncertainty, \ funnels, \ multiple modes", font_size=24, color=RES),
            label(r"check it: \ PSIS $\hat k$ \ (Yao et al.\ 2018), \ or SBC", font_size=24, color=HIT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Variational inference wins on scale: millions of parameters, streaming data, topic "
            "models and neural networks, where sampling is out of reach. <bookmark mark='b'/> Automatic "
            "differentiation variational inference, ADVI, is the generic version built here: transform every "
            "parameter to the real line, fit a Gaussian by stochastic gradients. <bookmark mark='c'/> It loses on "
            "uncertainty, on funnels and on multiple modes. <bookmark mark='d'/> So check it, with Yuling Yao and "
            "colleagues' Pareto k-hat, or with Part 26's simulation-based calibration, remembering that a passing "
            "diagnostic is not proof of accuracy."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def richer(self):
        rows = [
            cmath(r"\text{full-rank Gaussian}", r":", r"\text{correlations, \ } d^2 \text{ parameters}", font_size=30),
            cmath(r"\text{normalizing flows}", r":", r"q = \text{a learned invertible map of a normal}", font_size=30),
            cmath(r"\text{EP}", r":", r"\text{local moment-matching projections; \ not global forward KL}", font_size=30),
            cmath(r"\text{still}", r":", r"\text{an approximation: \ check it}", font_size=30),
        ]
        rows[3][-1].set_color(PATH)
        whys = [why(r"fixes the ellipse, \ not the funnel"), why(r"Rezende \& Mohamed (2015)"), why(r"Minka (2001)"), why(r"PSIS $\hat k$, \ SBC")]
        with self.voiceover(
            "<bookmark mark='a'/> Richer families help. A full-rank Gaussian captures correlations, at the cost of d "
            "squared parameters. <bookmark mark='b'/> Normalizing flows learn an invertible transformation of a "
            "normal, flexible enough for curved posteriors. <bookmark mark='c'/> Forward KL often favours covering "
            "mass. Expectation propagation uses local moment matching and tilted-distribution projections; it does "
            "not generally minimize one global forward KL. <bookmark mark='d'/> Each remains an approximation whose "
            "error has to be checked rather than assumed."
        ) as vo:
            intro = label('Richer approximations still need accuracy checks', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
