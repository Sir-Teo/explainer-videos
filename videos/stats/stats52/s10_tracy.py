from __future__ import annotations

import numpy as np

from videos.stats.stats52.common import *  # noqa: F403


class TracyWidom(VoiceoverScene):
    def construct(self):
        self.card()
        self.law()
        self.chart()
        self.roy()
        self.factors()
        self.board()
        self.beyond()

    def card(self):
        card = chapter_card(9, r"Tracy--Widom fluctuations", r"The largest eigenvalue, \ to the next order", lit=(2001,), part=PART)
        with self.voiceover("Chapter nine. Tracy–Widom fluctuations: the largest eigenvalue, to the next order."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def law(self):
        rows = [
            cmath(r"\ell_1 = \lambda_{\max}(X^\top X)", r":", r"\text{under } \Sigma = I, \ \text{near } (\sqrt n + \sqrt p)^2", font_size=32),
            cmath(r"\frac{\ell_1 - \mu_{np}}{\sigma_{np}}", r"\Rightarrow", r"TW_1: \ \text{not normal; \ scale } n^{1/3}\text{, \ not } n^{1/2}", font_size=34),
            cmath(r"\mu_{np}", r"=", r"(\sqrt{n - 1} + \sqrt p)^2, \ \ \sigma_{np} = (\sqrt{n-1} + \sqrt p)\big(\tfrac{1}{\sqrt{n-1}} + \tfrac{1}{\sqrt p}\big)^{1/3}", font_size=28),
            cmath(r"F_1(s)", r"=", r"\det(I - K_1)_{L^2(s, \infty)}, \ \ K_1(x, y) = \tfrac12\mathrm{Ai}\big(\tfrac{x + y}{2}\big)", font_size=30),
        ]
        rows[1][-1].set_color(SPIKEC)
        rows[3][-1].set_color(TRUEC)
        whys = [why(r"the null: \ no spike"), why(r"Tracy \& Widom (1994, 1996)"), why(r"Johnstone (2001)"), why(r"Ferrari--Spohn; \ Bornemann (2010)")]
        heading = label('The top covariance eigenvalue has Tracy--Widom edge fluctuations', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Under the null of no spike, where does the largest eigenvalue fall, beyond its limit? <bookmark mark='b'/> Craig Tracy and Harold Widom found in 1994 and 1996, for physicists' random matrices, that the centred and scaled largest eigenvalue converges to a new law, not a normal one, and on a scale of n to the one third rather than the root of n. <bookmark mark='c'/> Iain Johnstone proved in 2001 that the same law governs the largest eigenvalue of a sample covariance, with these explicit centring and scaling constants, useful at moderate n and p, with finite-sample approximation error. <bookmark mark='d'/> The distribution function is a Fredholm determinant of a kernel built from the Airy function, which Folkmar Bornemann showed in 2010 can be computed accurately by converged quadrature. This implementation uses a finite cutoff and quadrature order, so convergence checks are needed before claiming numerical precision."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("tw")
        A = axes([-5, 4], [0, 0.45], x_length=7.4, y_length=4.4, xlabel=r"$(\ell_1 - \mu_{np})/\sigma_{np}$", ylabel=r"density",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.1, 0.2, 0.3, 0.4], center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = hist_bars(ax, d["edges"], d["hist"], color=BULKC, opacity=0.55)
        s = np.asarray(d["s"])
        tw1 = polyline(ax, s, d["pdf1"], TRUEC, 4)
        tw2 = polyline(ax, s, d["pdf2"], GREY_B, 2.5)
        nrm = polyline(ax, s, np.exp(-0.5 * ((s - d["tw_mean"]) / d["tw_sd"]) ** 2) / (d["tw_sd"] * np.sqrt(2 * np.pi)), BADC, 2.5)
        q = DashedLine(ax.c2p(d["q95"], 0), ax.c2p(d["q95"], 0.45), color=SPIKEC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(rf"$n = {d['n']}$, \ $p = {d['p']}$, \ 1,500 null samples", font_size=22),
            label(rf"teal: \ simulated, \ mean {d['z_mean']:.2f}, \ SD {d['z_sd']:.2f}", font_size=22, color=BULKC),
            label(rf"white: \ $TW_1$, \ mean {d['tw_mean']:.3f}, \ SD {d['tw_sd']:.3f}", font_size=22, color=TRUEC),
            label(r"red: \ a normal with the same moments; \ grey: \ $TW_2$", font_size=22, color=BADC),
            label(rf"gold: \ the 95\% point, \ {d['q95']:.3f}", font_size=22, color=SPIKEC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Fifteen hundred null samples of four hundred observations on two hundred variables. "
            f"<bookmark mark='b'/> The centred and scaled largest eigenvalues have mean {say(d['z_mean'], 2)} and standard "
            f"deviation {say(d['z_sd'], 2)}. <bookmark mark='c'/> The Tracy–Widom law, computed from the Fredholm "
            f"determinant, has mean {say(d['tw_mean'], 3)} and standard deviation {say(d['tw_sd'], 3)}, and its density "
            f"traces the histogram. <bookmark mark='d'/> It is skewed: a normal with the same mean and variance, in red, puts "
            f"too little mass in the right tail. The grey curve is the complex-matrix version, beta equal to two, narrower and "
            f"further left. <bookmark mark='e'/> The law's ninety-fifth percentile is {say(d['q95'], 3)}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ the law exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(tw1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(nrm), Create(tw2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(q), FadeIn(side[4]))
        self.clear_scene()

    def roy(self):
        d = load("tw")
        rows = [
            cmath(r"H_0: \Sigma = I", r"\text{ vs }", r"H_1: \text{ a spike}", font_size=36),
            cmath(r"\text{Roy's largest root (1953)}", r":", rf"\text{{reject if }} (\ell_1 - \mu_{{np}})/\sigma_{{np}} > {d['q95']:.3f}", font_size=32),
            cmath(r"\text{simulated size}", r":", rf"{100 * d['size']:.1f}\% \text{{ at nominal 5\%}}", font_size=34),
            cmath(r"\text{power}", r":", r"\to 1 \text{ above BBP; \ } \to \alpha \text{ below: \ detection fails too}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"known identity covariance; \ unknown scale needs another calibration"), why(r"Johnstone's calibration"), why(r"$n = 400$, \ $p = 200$"), why(r"Onatski, \ Moreira \& Hallin (2013)")]
        heading = label('A known-identity null admits an asymptotic largest-root calibration', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> The use: testing whether there is any spike at all. <bookmark mark='b'/> Samarendra Roy's "
            f"largest-root test of 1953 rejects when the largest eigenvalue is too big, and Johnstone's result calibrates it: "
            f"reject when the scaled statistic exceeds {say(d['q95'], 2)}. <bookmark mark='c'/> On the null samples, it "
            f"rejects {100 * d['size']:.1f} percent of the time, at a nominal five. <bookmark mark='d'/> Above the BBP "
            f"threshold its power tends to one. Below it, Alexei Onatski, Marcelo Moreira and Marc Hallin showed in 2013, no "
            f"test based on the top eigenvalue can do much better than chance, though tests using the whole spectrum retain a "
            f"little power."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def factors(self):
        rows = [
            cmath(r"\text{how many factors?}", r":", r"\text{test } H_0^{(k)}: k \text{ spikes, \ for } k = 0, 1, 2, \dots", font_size=32),
            cmath(r"\text{step } k", r":", r"\text{compare } \hat\lambda_{k+1} \text{ with the edge, \ on the Tracy--Widom scale}", font_size=32),
            cmath(r"\text{stop}", r":", r"\text{at the first } k \text{ not rejected}", font_size=34),
            cmath(r"\text{Harman caveat}", r":", r"\text{edge counting alone is not a calibrated sequential factor test}", font_size=30),
        ]
        rows[3][-1].set_color(SPIKEC)
        whys = [why(r"Kritchman \& Nadler (2008)"), why(r"the remaining spectrum"), why(r"a sequential test"), why(r"chapter 8's data")]
        heading = label('Sequential factor tests require a noise model and error calibration', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Choosing the number of factors becomes a sequence of tests, as Shira Kritchman and Boaz Nadler proposed in 2008: test zero spikes, then one, then two. <bookmark mark='b'/> At step k, compare the next eigenvalue with the bulk's edge, on the Tracy–Widom scale. <bookmark mark='c'/> Stop at the first k that is not rejected. <bookmark mark='d'/> For Harman's tests, simply counting two eigenvalues above an isotropic MP reference is not an implemented calibrated sequential procedure. A factor-count test needs an appropriate fitted noise model, finite-sample centering, thresholds and sequential error control."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = board_rows("test")
        d = load("board")
        a = [x["achieved"] for x in d["rows"]]
        show_board(self, rows,
                   f"<bookmark mark='a'/> On the Board, with two hundred observations of a hundred variables. A naive single-variance normal cutoff, incorrectly applied to a maximum eigenvalue, rejecting when the top eigenvalue exceeds one by more than one point six four five times root two over n, rejects pure noise {100 * a[2]:.0f} percent of the time: under the null the top eigenvalue sits near two point nine, not one. <bookmark mark='b'/> Roy's test with the Tracy–Widom calibration has size {100 * a[3]:.1f} percent.",
                   [("a", [0]), ("b", [1])])

    def beyond(self):
        rows = fit_rows(VGroup(
            label(r"Tracy--Widom is everywhere:", font_size=28, color=GREY_A),
            label(r"the longest increasing subsequence of a random permutation (Baik, \ Deift \& Johansson 1999)", font_size=26, color=BULKC),
            label(r"growing interfaces, \ queues in tandem, \ the KPZ universality class", font_size=26, color=BULKC),
            label(r"in statistics: \ how many factors? \ signals in arrays, \ finance, \ genetics", font_size=26, color=SPIKEC),
            label(r"the edge is universal too, \ for light-tailed entries", font_size=26, color=GOODC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Tracy–Widom law turned out to be everywhere. <bookmark mark='b'/> Jinho Baik, Percy "
            "Deift and Kurt Johansson showed in 1999 that it is the law of the longest increasing subsequence of a random "
            "permutation. <bookmark mark='c'/> It describes the fluctuations of growing interfaces and queues in tandem, the "
            "KPZ universality class. <bookmark mark='d'/> In statistics it calibrates tests for the number of factors and for "
            "signals in sensor arrays, finance and population genetics, where Patterson, Price and Reich used it in 2006 to "
            "count the axes of human genetic variation. <bookmark mark='e'/> And like the bulk, the edge is universal for "
            "light-tailed entries."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
