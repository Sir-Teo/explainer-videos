from __future__ import annotations

import numpy as np

from videos.stats.stats52.common import *  # noqa: F403


class Spikes(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.eigen_chart()
        self.overlap_chart()
        self.harman()
        self.harman_table()
        self.board()

    def card(self):
        card = chapter_card(8, r"Spiked models and the BBP transition", r"Ordinary PCA overlap vanishes below the asymptotic threshold", lit=(2005,), part=PART)
        with self.voiceover('Chapter eight. Spiked models and the BBP transition: below a threshold, ordinary PCA loses directional overlap below a model-dependent asymptotic threshold.'):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model(self):
        rows = [
            cmath(r"\Sigma", r"=", r"I + \ell\, v v^\top: \ \text{one signal direction, \ strength } \ell", font_size=34),
            cmath(r"\ell > \sqrt\gamma", r":", r"\hat\lambda_1 \to (1 + \ell)(1 + \gamma/\ell): \ \text{it pops out of the bulk, \ biased up}", font_size=30),
            cmath(r"\ell \le \sqrt\gamma", r":", r"\hat\lambda_1 \to (1 + \sqrt\gamma)^2: \ \text{stuck at the edge; \ invisible}", font_size=30),
            cmath(r"\langle\hat v, v\rangle^2", r"\to", r"\frac{1 - \gamma/\ell^2}{1 + \gamma/\ell} \ \text{above, \ } 0 \text{ below}", font_size=34),
        ]
        rows[1][-1].set_color(SPIKEC)
        rows[2][-1].set_color(BADC)
        rows[3][-1].set_color(LASSOC)
        whys = [why(r"Johnstone's spiked model (2001)"), why(r"Baik, \ Ben Arous \& Péché (2005)"), why(r"a phase transition"), why(r"Paul (2007)")]
        heading = label('BBP describes a proportional isotropic finite-rank spike model', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Iain Johnstone's spiked model: noise, plus one signal direction v with strength ell. <bookmark mark='b'/> Jinho Baik, Gérard Ben Arous and Sandrine Péché proved in 2005 that if the spike exceeds the root of gamma, the top sample eigenvalue separates from the bulk, converging to one plus ell, times one plus gamma over ell: an overestimate of the true one plus ell. <bookmark mark='c'/> But if the spike is below the root of gamma, the top eigenvalue sticks at the bulk's edge, exactly where it would be with no signal at all. <bookmark mark='d'/> Debashis Paul found in 2007 what happens to the eigenvector: in the isotropic finite-rank proportional model, its squared overlap has the displayed limit above the threshold and tends to zero below it. A real signal, weaker than root gamma, leaves no trace in the leading principal component."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def eigen_chart(self):
        d = load("bbp")
        A = axes([0, 3.1], [0.8, 5.0], x_length=7.4, y_length=4.4, xlabel=rf"spike $\ell$, \ $n = {d['n']:,}$, \ $p = {d['p']}$", ylabel=r"top eigenvalue",
                 xticks=[0, 0.5, 1, 1.5, 2, 2.5, 3], yticks=[1, 2, 3, 4, 5], center=[-2.5, 0.2, 0])
        ax = A.ax
        u = np.asarray(d["u"])
        theory = polyline(ax, u, d["top_curve"], TRUEC, 4)
        pop = polyline(ax, u, 1 + u, BNDC2, 3)
        edge = DashedLine(ax.c2p(0, d["edge"]), ax.c2p(3.1, d["edge"]), color=BULKC, stroke_width=2.5)
        thr = DashedLine(ax.c2p(d["threshold"], 0.8), ax.c2p(d["threshold"], 5.0), color=SPIKEC, stroke_width=2.5)
        sim = VGroup(*[Dot(ax.c2p(r["ell"], r["top"]), radius=0.09, color=SPIKEC) for r in d["rows"]])
        r3 = d["rows"][-1]
        side = fit_rows(VGroup(
            label(r"$\gamma = 1/2$: \ the threshold $\sqrt\gamma = 0.707$ \ (gold, dashed)", font_size=22, color=SPIKEC),
            label(rf"teal: \ the bulk's edge, \ {d['edge']:.3f}", font_size=22, color=BULKC),
            label(r"purple: \ the true top eigenvalue, \ $1 + \ell$", font_size=22, color=BNDC2),
            label(r"white: \ the BBP limit; \ gold dots: \ simulated", font_size=22, color=TRUEC),
            label(rf"$\ell = 3$: \ truth 4, \ sample {r3['top']:.2f}, \ limit {r3['top_theory']:.2f}", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test with a thousand observations of five hundred variables, so gamma is a half and the threshold is {say(d['threshold'], 3)}. <bookmark mark='b'/> The teal line is the bulk's edge, {say(d['edge'], 2)}. <bookmark mark='c'/> The purple line is the true top eigenvalue, one plus ell. <bookmark mark='d'/> The white curve is the BBP limit, flat at the edge until the threshold and then rising; the simulated top eigenvalues, in gold, follow it, with the blur near the threshold that finite samples always have. <bookmark mark='e'/> At a spike of three, the true top eigenvalue is four, the sample's is {say(r3['top'], 2)}, and the limit predicts {say(r3['top_theory'], 2)}: inverting the limiting map corrects the leading asymptotic bias, with finite-sample error remaining."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ curves exact")))
            vo.wait_until("a")
            self.play(Create(thr), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(edge), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(pop), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(theory), FadeIn(sim), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def overlap_chart(self):
        d = load("bbp")
        A = axes([0, 3.1], [0, 1.0], x_length=7.4, y_length=4.4, xlabel=r"spike $\ell$", ylabel=r"$\langle\hat v_1, v\rangle^2$",
                 xticks=[0, 0.5, 1, 1.5, 2, 2.5, 3], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        u = np.asarray(d["u"])
        theory = polyline(ax, u, d["ov_curve"], TRUEC, 4)
        thr = DashedLine(ax.c2p(d["threshold"], 0), ax.c2p(d["threshold"], 1.0), color=SPIKEC, stroke_width=2.5)
        sim = VGroup(*[Dot(ax.c2p(r["ell"], r["overlap"]), radius=0.09, color=LASSOC) for r in d["rows"]])
        r = {x["ell"]: x for x in d["rows"]}
        side = fit_rows(VGroup(
            label(r"the squared overlap of the top eigenvector with $v$", font_size=22),
            label(r"white: \ Paul's limit; \ blue: \ simulated", font_size=22, color=TRUEC),
            label(rf"$\ell = 0.5$: \ {r[0.5]['overlap']:.3f}, \ no better than a random direction", font_size=22, color=BADC),
            label(rf"$\ell = 1$: \ {r[1.0]['overlap']:.2f}; \ $\ell = 3$: \ {r[3.0]['overlap']:.2f}", font_size=22, color=LASSOC),
            label(r"even a visible spike's direction is only partly known", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The eigenvector, on the same problems. <bookmark mark='b'/> Paul's limit in white, the simulation in blue. <bookmark mark='c'/> Below the threshold, at a spike of a half, the squared overlap is {say(r[0.5]['overlap'], 3)}: its overlap is small but need not equal the finite-sample random-direction value one over p, though the signal is real and one and a half times the noise in its direction. <bookmark mark='d'/> At a spike of one it is {say(r[1.0]['overlap'], 2)}, and at three, {say(r[3.0]['overlap'], 2)}. <bookmark mark='e'/> Even a strong spike's direction is estimated only partly: the angle between them stays well away from zero."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ curve exact")))
            vo.wait_until("a")
            self.play(Create(thr), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(theory), FadeIn(sim), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def harman(self):
        d = load("harman")
        k = np.arange(1, d["p"] + 1)
        A = axes([0, 25], [0, 8.8], x_length=7.4, y_length=4.4, xlabel=r"eigenvalue rank", ylabel=r"eigenvalue of the correlation matrix",
                 xticks=[1, 5, 10, 15, 20, 24], yticks=[0, 2, 4, 6, 8], center=[-2.5, 0.2, 0])
        ax = A.ax
        band = Rectangle(width=ax.c2p(25, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, d["mp_hi"])[1] - ax.c2p(0, d["mp_lo"])[1],
                         fill_color=BULKC, fill_opacity=0.2, stroke_width=0).move_to(ax.c2p(12.5, (d["mp_hi"] + d["mp_lo"]) / 2))
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=SPIKEC if b > d["mp_hi"] else GREY_B) for a, b in zip(k, d["ev"])])
        kaiser = DashedLine(ax.c2p(0, 1), ax.c2p(25, 1), color=BADC, stroke_width=2.5)
        n_kaiser = int(np.sum(np.asarray(d["ev"]) > 1))
        side = fit_rows(VGroup(
            label(rf"Harman's 24 psychological tests, \ $n = {d['n']}$ children", font_size=22),
            label(rf"teal: \ isotropic-noise asymptotic MP reference, \ $[{d['mp_lo']:.2f}, {d['mp_hi']:.2f}]$", font_size=22, color=BULKC),
            label(rf"gold: \ {d['above']} eigenvalues above it: \ {d['ev'][0]:.2f} and {d['ev'][1]:.2f}", font_size=22, color=SPIKEC),
            label(rf"red: \ Kaiser's rule, \ eigenvalue $> 1$: \ {n_kaiser} factors", font_size=22, color=BADC),
            label(r"the third, \ 1.69, \ is inside the noise band", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Real data: the twenty-four psychological tests of Holzinger and Swineford, from Harman's factor analysis of 1967, on {d['n']} schoolchildren, last seen in Part thirty-one. <bookmark mark='b'/> An isotropic independent-noise MP reference, which is not a calibrated band for these tests, has limiting edges {say(d['mp_lo'], 2)} to {say(d['mp_hi'], 2)}. <bookmark mark='c'/> Two stand above it: {say(d['ev'][0], 2)}, a dominant covariance component often interpreted as general ability, and {say(d['ev'][1], 2)}. <bookmark mark='d'/> Kaiser's popular rule, keep every eigenvalue above one, keeps {n_kaiser}. <bookmark mark='e'/> The third eigenvalue, one point six nine, is inside the band: the edge comparison alone neither proves noise nor establishes a factor count, though the classical four-factor solution keeps it, on substantive grounds."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Holzinger \& Swineford (1939); \ Harman (1967)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(band), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(dots), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(kaiser), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def harman_table(self):
        d = load("harman")
        rows = [[r"component", r"sample eigenvalue", r"assumed-model spike $1+\hat\ell$", r"assumed-model overlap$^2$"]]
        for i in range(d["above"]):
            rows.append([str(i + 1), f"{d['ev'][i]:.2f}", f"{d['spikes'][i]:.2f}", f"{d['overlaps'][i]:.2f}"])
        tab = table_rows(rows, font_size=28, col_buff=0.8, row_buff=0.45, colors=[GREY_B, SPIKEC, SPIKEC])
        tab.move_to([0, 1.0, 0])
        for i in range(1, len(rows)):
            tab[i][2].set_color(GOODC)
            tab[i][3].set_color(LASSOC)
        foot = label(r"invert the BBP map: \ $\hat\lambda = (1 + \ell)(1 + \gamma/\ell)$ \ solved for $\ell$", font_size=24, color=GREY_A).move_to([0, -0.8, 0])
        foot2 = label(rf"assumed-model squared overlaps; \ not validated real-data alignments", font_size=24, color=BADC).move_to([0, -1.6, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> What the theory adds. Inverting the BBP map turns each sample eigenvalue into an estimate of the population spike: {say(d['ev'][0], 2)} becomes {say(d['spikes'][0], 2)}, and {say(d['ev'][1], 2)} becomes {say(d['spikes'][1], 2)}. And Paul's formula predicts how well each estimated direction matches the truth: a squared overlap of {say(d['overlaps'][0], 2)} for the general factor, but only {say(d['overlaps'][1], 2)} for the second. <bookmark mark='b'/> These are model-based illustrations, not validated spike or overlap estimates for Harman's matrix. Its varying noise eigenvalues and sample standardization do not match identity noise plus a few positive spikes. <bookmark mark='c'/> A squared overlap is not a percentage of angle alignment, and the assumed-model prediction cannot certify these real loadings. A fitted noise model and further checks are needed."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(museum_tag(r"Harman (1967)")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def board(self):
        rows = board_rows("interval")
        d = load("board")
        a = [x["achieved"] for x in d["rows"]]
        show_board(self, rows,
                   f"<bookmark mark='a'/> On the Coverage Board: an interval for a spike of four, with two hundred observations "
                   f"of a hundred variables. Theodore Anderson's classical interval, built for fixed p, covers "
                   f"{100 * a[0]:.1f} percent: it is centred on the biased sample eigenvalue, which converges to "
                   f"{say(d['psi'], 2)}, not four. <bookmark mark='b'/> The BBP-corrected interval, which inverts the map and "
                   f"uses the spiked model's standard error, covers {100 * a[1]:.1f} percent.",
                   [("a", [0]), ("b", [1])])
