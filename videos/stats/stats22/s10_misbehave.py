from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats22.common import *  # noqa: F403


class Misbehave(VoiceoverScene):
    def construct(self):
        self.card()
        self.spike()
        self.cures()
        self.switching()
        self.boundary()
        self.bootstrap()

    def card(self):
        card = chapter_card(9, r"When likelihood misbehaves", r"Spikes, \ twins and edges", part=PART)
        with self.voiceover("Chapter nine. When likelihood misbehaves."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def spike(self):
        d = load("misbehave")
        s, ll = np.asarray(d["sigma"]), np.asarray(d["ll"])
        u = -np.log10(s)
        A = axes([1.5, 12], [1600, 3700], x_length=8.0, y_length=4.4, xlabel=r"$\sigma_1$, \ shrinking", ylabel=r"log likelihood",
                 xticks=[2, 4, 6, 8, 10, 12], yticks=[2000, 2500, 3000, 3500], center=[-1.6, 0.3, 0],
                 xfmt=lambda v: rf"10^{{-{int(v)}}}")
        ax = A.ax
        cv = polyline(ax, u, ll, RES, 3.5)
        mle = DashedLine(ax.c2p(1.5, d["ll_mle"]), ax.c2p(12, d["ll_mle"]), color=PATH, stroke_width=2.5)
        cross = float(np.interp(d["ll_mle"], ll[np.argmin(ll):], u[np.argmin(ll):]))
        dot = Dot(ax.c2p(cross, d["ll_mle"]), radius=0.08, color=PATH)
        rows = fit_rows(VGroup(
            label(rf"put $\mu_1$ on one crab interval, \ {d['mu_at']:.4f}", font_size=22),
            label(r"then let its spread $\sigma_1$ shrink", font_size=22, color=RES),
            label(rf"gold: \ the MLE's log likelihood, \ {d['ll_mle']:.1f}", font_size=22, color=PATH),
            label(rf"passed near $\sigma_1 = 10^{{-{cross:.0f}}}$, \ and still rising", font_size=22, color=RES),
            VGroup(label(r"96 crabs share that value:", font_size=22, color=GREY_A),
                   label(r"$+96 \ln 10 \approx 221$ a decade", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "The crabs' fit hides an embarrassment. <bookmark mark='a'/> Put the mean of race one exactly on one of the data "
            "values, here point six five three five, the midpoint of the busiest interval but one. <bookmark mark='b'/> Then let "
            "its spread shrink. At first the fit gets worse, since race one no longer covers the other crabs. But a normal "
            "density at its own centre is one over sigma root two pi, which grows without limit. <bookmark mark='c'/> The gold "
            "line is the log likelihood of the fit we reported. <bookmark mark='d'/> Somewhere below a spread of ten to the "
            "minus seven, the spike passes it, and it keeps rising forever. <bookmark mark='e'/> Ninety-six crabs share that "
            "recorded value, so every factor of ten in sigma adds ninety-six times the log of ten. The likelihood of a normal "
            "mixture has no maximum at all."
        ) as vo:
            self.play(FadeIn(A), Create(mle))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Indicate(mle, color=PATH), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(dot), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def cures(self):
        rows = [
            cmath(r"\text{the real data}", r":", r"\text{grouped: \ } P(\text{interval}) \le 1, \ \text{bounded}", font_size=30),
            cmath(r"\text{constrain}", r":", r"\sigma_1 / \sigma_2 \ge c > 0 \ \ \text{(Hathaway 1985)}", font_size=30),
            cmath(r"\text{the right root}", r":", r"\text{a consistent local maximum exists (Redner \& Walker 1984)}", font_size=28),
            cmath(r"\text{penalize}", r":", r"\ell(\theta) - \lambda \textstyle\sum_k \{s^2/\sigma_k^2 + \log \sigma_k^2\}", font_size=30),
        ]
        rows[0][2].set_color(HIT)
        whys = [why(r"Weldon recorded intervals, \ not exact values"), why(r"no component may collapse"),
                why(r"EM from a sensible start finds it"), why(r"Chen, \ Tan \& Zhang (2008): \ a prior in disguise")]
        with self.voiceover(
            "There are four ways out. <bookmark mark='a'/> The honest one here: Weldon recorded intervals, not exact values. "
            "The likelihood of grouped data uses each interval's probability, which can never exceed one, so the spike "
            "disappears. <bookmark mark='b'/> Or forbid the spreads from being too unequal; Richard Hathaway showed in 1985 "
            "that the constrained maximum exists and is consistent. <bookmark mark='c'/> Or take the sensible local maximum, "
            "the one EM finds from a reasonable start; theory guarantees a consistent root exists among the local maxima. "
            "<bookmark mark='d'/> Or penalize small variances, which amounts to a prior, and leads to Part 26's Bayesian view."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def switching(self):
        a, b = load("crabs")["theta"], load("misbehave")["swapped"]
        hdr = [r"\textbf{EM start}", r"$p$", r"$\mu_1$", r"$\sigma_1$", r"$\mu_2$", r"$\sigma_2$", r"\textbf{log lik}"]
        ll = load("crabs")["loglik"][-1]
        body = [[r"race 1 on the left", f"{a[0]:.3f}", f"{a[1]:.4f}", f"{a[2]:.4f}", f"{a[3]:.4f}", f"{a[4]:.4f}", f"{ll:.2f}"],
                [r"race 1 on the right", f"{b[0]:.3f}", f"{b[1]:.4f}", f"{b[2]:.4f}", f"{b[3]:.4f}", f"{b[4]:.4f}", f"{ll:.2f}"]]
        t = table_rows([hdr] + body, font_size=24, col_buff=0.5, row_buff=0.3, colors=[GREY_A, CRAB1, CRAB2])
        t.move_to([0, 1.3, 0])
        foot = fit_rows(VGroup(
            label(r"the same fit with the names swapped: \ $p \leftrightarrow 1 - p$", font_size=24),
            label(r"$K$ components: \ $K!$ identical peaks", font_size=24, color=RES),
            label(r"harmless for one fit; \ a trap for averaging (bootstrap, \ MCMC)", font_size=24, color=GREY_A),
            label(r"fix: \ an ordering constraint, \ $\mu_1 < \mu_2$", font_size=24, color=HIT),
        ), 12.0, 0.32, [0, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The second oddity. Run EM again with the starting values swapped, race one on the right. "
            "It converges to the same fit with the labels exchanged: the proportion becomes one minus itself, the means and "
            "spreads trade places, and the log likelihood is identical. <bookmark mark='b'/> A mixture of K components has K "
            "factorial identical peaks. <bookmark mark='c'/> For a single fit that's harmless. But anything that averages over "
            "fits, a bootstrap or a Markov chain sampler, can mix up labels and average race one with race two. "
            "<bookmark mark='d'/> The usual fix is an ordering constraint: call race one the one with the smaller mean."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(t[0]), FadeIn(t[1]), FadeIn(t[2]), FadeIn(foot[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k + 1]))
        self.clear_scene()

    def boundary(self):
        rows = [
            cmath(r"H_0", r":", r"\text{one normal: \ } p = 0, \ \text{or } p = 1, \ \text{or } \mu_1 = \mu_2, \sigma_1 = \sigma_2", font_size=28),
            cmath(r"\text{Wilks needs}", r":", r"\theta_0 \text{ inside the space, \ every parameter identified}", font_size=28),
            cmath(r"\text{here}", r":", r"\text{on the edge; \ under } p = 0, \ \mu_1, \sigma_1 \text{ mean nothing}", font_size=28),
            cmath(r"\text{simpler edges}", r":", r"\sigma^2_{\text{between}} = 0: \ \ \tfrac12\chi^2_0 + \tfrac12\chi^2_1", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"Weldon's real question"), why(r"chapter two's conditions"), why(r"Hartigan (1985): \ the LR is unbounded"),
                why(r"Self \& Liang (1987); \ Part 25")]
        with self.voiceover(
            "The third oddity matters most for Weldon's real question: are there two races at all? <bookmark mark='a'/> The "
            "hypothesis of a single normal can be reached in several ways: a proportion of zero, or of one, or two identical "
            "components. <bookmark mark='b'/> Wilks's theorem, which made twice the log likelihood ratio chi-squared, needs the "
            "null value inside the parameter space, with every parameter identified. <bookmark mark='c'/> Here the null sits "
            "on the edge, and when the proportion is zero the other race's mean and spread mean nothing at all. John Hartigan "
            "showed in 1985 that the statistic doesn't settle to any chi-squared. <bookmark mark='d'/> Simpler edges have "
            "simpler answers: testing whether a variance component is zero, which Part 25 needs, gives a fifty-fifty mixture of "
            "a point mass at zero and a chi-squared with one degree of freedom."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bootstrap(self):
        d = load("lrboot")
        lr = np.asarray(d["lr"])
        xmax = 16
        edges = np.linspace(0, xmax, 33)
        h, _ = np.histogram(np.clip(lr, 0, xmax - 1e-9), edges, density=True)
        A = axes([0, xmax], [0, 0.45], x_length=8.0, y_length=4.2, xlabel=r"$2 \times$ log likelihood ratio, \ two normals vs one",
                 ylabel=r"density", xticks=[0, 4, 8, 12, 16], yticks=[0, 0.2, 0.4], center=[-1.6, 0.4, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, h, color=SIM, opacity=0.6)
        gr = np.linspace(0.05, xmax, 200)
        c1 = curve(ax, gr, np.minimum(stats.chi2.pdf(gr, 1), 0.45), GREY_B, 2.5)
        c3 = curve(ax, gr, stats.chi2.pdf(gr, 3), TEAL, 2.5)
        q = DashedLine(ax.c2p(d["q95"], 0), ax.c2p(d["q95"], 0.4), color=PATH, stroke_width=2.5)
        arr = Arrow(ax.c2p(xmax - 2.5, 0.3), ax.c2p(xmax + 0.6, 0.3), buff=0, color=OBS, stroke_width=4, tip_length=0.18)
        al = label(rf"crabs: \ {d['obs']:.1f}", font_size=22, color=OBS).next_to(arr, UP, buff=0.1)
        rows = fit_rows(VGroup(
            label(rf"{d['R']} fake Weldons, \ one normal", font_size=22, color=SIM),
            VGroup(label(r"grey: \ $\chi^2_1$, \ too light-tailed", font_size=22, color=GREY_A),
                   label(r"teal: \ $\chi^2_3$, \ closer", font_size=22, color=TEAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            label(rf"gold: \ the 95th percentile, \ {d['q95']:.1f}", font_size=22, color=PATH),
            label(rf"crabs: \ {d['obs']:.1f}; \ $p \le {d['p_boot']:.3f}$", font_size=22, color=OBS),
            VGroup(label(r"two components fit better;", font_size=22),
                   label(r"two \emph{races} is biology", font_size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> When theory gives no reference distribution, simulate one. Draw two hundred fake sets of a "
            "thousand crabs from the single best normal, group them into Weldon's intervals, and fit both models to each, the "
            "parametric bootstrap of Part 16. <bookmark mark='b'/> The statistic's distribution matches neither chi-squared "
            "with one degree of freedom nor with three. <bookmark mark='c'/> Its ninety-fifth percentile is the gold line. "
            "<bookmark mark='d'/> The real crabs give fifty-three, far beyond anything the single normal produced. "
            "<bookmark mark='e'/> So two components fit much better than one. Whether they're two races is a question for "
            "biology, not likelihood: a skewed single population would pass this test too."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(c1), Create(c3), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(q), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(GrowArrow(arr), FadeIn(al), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
