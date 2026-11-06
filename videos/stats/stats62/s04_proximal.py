from __future__ import annotations

import numpy as np

from videos.stats.stats62.common import *  # noqa: F403


class Proximal(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter three. Proximal causal inference: two imperfect proxies for one hidden confounder.", 3,
                            r"Proximal causal inference", r"Proxies, \ not measurements", lit=(2018,))
        self.setup_()
        self.bridge()
        self.linear()
        self.negcontrols()
        self.chart()
        self.board()
        self.weak()
        self.beyond()

    def setup_(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Often the confounder is not measured, but something related to it is. A patient's "
            "frailty is hidden, but there are clues: earlier hospital visits, which predict treatment, and a blood test, "
            "which predicts the outcome. <bookmark mark='b'/> Adjusting for the clues as if they were the confounder is the "
            "usual practice, and it leaves bias, because a proxy measures the confounder with error. <bookmark mark='c'/> "
            "Wang Miao, Zhi Geng and Eric Tchetgen Tchetgen showed in 2018 that two proxies of different kinds can identify "
            "the effect exactly. <bookmark mark='d'/> A treatment proxy Z, related to the outcome only through U; and an "
            "outcome proxy W, unaffected by the treatment.",
            [(r"\text{hidden}", r":", r"U \ \text{(frailty)}", 40),
             (r"\text{naive}", r":", r"\text{adjust for proxies: \ residual bias}", 40),
             (r"\text{proximal}", r":", r"\text{two proxies identify the effect}", 40),
             (r"Z \perp Y \mid A, U", r";", r"W \perp (A, Z) \mid U", 40)],
            [r"the usual situation", r"Part 41's measurement error", r"Miao, \ Geng \& Tchetgen Tchetgen (2018)", r"the two conditions"],
            colors=[(2, IDC)])

    def bridge(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The key object is an outcome bridge function h of w and a. <bookmark mark='b'/> It must "
            "satisfy one integral equation: the expected outcome given treatment and the treatment proxy equals the "
            "expected bridge given the same. <bookmark mark='c'/> If such an h exists, averaging h of W and a over the "
            "population gives the mean potential outcome under a. <bookmark mark='d'/> The proxy Z is an instrument for the "
            "proxy W: the bridge is found by the same kind of equation as Part thirty-seven's instrumental variables, "
            "with W in place of the endogenous regressor.",
            [(r"\text{bridge}", r":", r"E[Y \mid A, Z] = E[h(W, A) \mid A, Z]", 40),
             (r"\text{then}", r":", r"E[Y(a)] = E[h(W, a)]", 40),
             (r"\text{requires}", r":", r"Z \text{ informative about } U \ \text{(completeness)}", 40),
             (r"\text{like IV}", r":", r"Z \text{ instruments } W", 40)],
            [r"an integral equation", r"identification", r"a rank condition", r"Part 37's 2SLS"],
            colors=[(1, IDC)])

    def linear(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In a linear model the bridge is a line, and the method becomes two-stage least squares. "
            "<bookmark mark='b'/> Regress Y on A and W, using A and Z as instruments. <bookmark mark='c'/> The coefficient on "
            "A is the causal effect; the coefficient on W absorbs the confounding. <bookmark mark='d'/> Eric Tchetgen "
            "Tchetgen, Andrew Ying, Yifan Cui, Xu Shi and Wang Miao's 2020 introduction gives this proximal two-stage least "
            "squares, and its doubly robust and semiparametric versions.",
            [(r"h(w, a)", r"=", r"b_0 + b_A a + b_W w", 40),
             (r"\text{2SLS}", r":", r"Y \sim A + W, \ \ \text{instruments } (A, Z)", 40),
             (r"b_A", r":", r"\text{the causal effect}", 40),
             (r"\text{references}", r":", r"\text{Tchetgen Tchetgen et al. (2020)}", 40)],
            [r"linear bridge", r"P2SLS", r"identified", r"the introduction"],
            colors=[(2, IDC)])

    def chart(self):
        d = load("proximal")
        en, ep = np.asarray(d["est_naive"]), np.asarray(d["est_prox"])
        xs = np.linspace(0.2, 2.4, 300)

        def kde(v, h):
            return np.exp(-0.5 * ((xs[:, None] - v[None]) / h) ** 2).sum(1) / (len(v) * h * np.sqrt(2 * np.pi))
        yn, yp = kde(en, 0.03), kde(ep, 0.05)
        top = float(max(yn.max(), yp.max())) * 1.1
        A = axes([0.2, 2.4], [0, top], x_length=7.4, y_length=4.4, xlabel=r"estimated effect of $A$", ylabel=r"density over 600 samples",
                 xticks=[0.5, 1, 1.5, 2], yticks=[0, 1, 2, 3, 4], center=[-2.5, 0.2, 0])
        ax = A.ax
        cn = VGroup(shade(ax, xs, yn, NAIVEC, 0.25), curve(ax, xs, yn, NAIVEC, 3.5))
        cp = VGroup(shade(ax, xs, yp, IDC, 0.25), curve(ax, xs, yp, IDC, 3.5))
        tl = DashedLine(ax.c2p(1, 0), ax.c2p(1, top * 0.98), color=GOLDC, stroke_width=2.5)
        side = side_groups([
            [(r"$U \sim N(0, 1)$; \ $Z = U + e$, \ $W = U + e'$", WHITE), (r"$Y = A + 2U + \epsilon$", GREY_A)],
            [(r"gold: \ the true effect, \ 1", GOLDC)],
            [(rf"red: \ OLS on $A$, $Z$, $W$: \ mean {d['mean_naive']:.2f}", NAIVEC), (rf"95\% CI covers {100 * d['cov_naive']:.0f}\%", NAIVEC)],
            [(rf"green: \ proximal 2SLS: \ mean {d['mean_prox']:.2f}", IDC), (rf"95\% CI covers {100 * d['cov_prox']:.1f}\%", IDC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> A simulation. A hidden normal confounder U; two noisy copies of it, Z and W; a treatment "
            f"that depends on U; and an outcome that depends on both, with a true effect of one. <bookmark mark='b'/> Six "
            f"hundred samples of a thousand units. <bookmark mark='c'/> Ordinary regression adjusting for both proxies, in "
            f"red, averages {say(d['mean_naive'], 2)}: the proxies remove only part of the confounding. Its interval never "
            f"covers the truth. <bookmark mark='d'/> Proximal two-stage least squares, in green, averages {say(d['mean_prox'], 2)}, "
            f"with a wider spread, and its interval covers {100 * d['cov_prox']:.1f} percent of the time."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated, \ 600 samples")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(tl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(cn), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(cp), FadeIn(side[3]), run_time=1.5)
        self.clear_scene()

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("both proxies", "proximal 2SLS"),
                   f"<bookmark mark='a'/> On the Board: adjusting for both proxies covers the true effect "
                   f"{100 * br[0]['achieved']:.0f} percent of the time, broken. <bookmark mark='b'/> Proximal two-stage least "
                   f"squares covers {100 * br[1]['achieved']:.1f} percent: kept.", [("a", [0]), ("b", [1])])

    def beyond(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Beyond the linear case. <bookmark mark='b'/> A treatment bridge, solving the dual integral "
            "equation, gives a weighting estimator, and combining the two bridges gives a doubly robust one, from Yifan Cui "
            "and co-authors in 2023. <bookmark mark='c'/> The bridges can be estimated by kernel or neural methods, as "
            "minimax solutions of conditional moment equations. <bookmark mark='d'/> The price: the integral equations are "
            "ill-posed, like nonparametric instrumental variables, so rates are slower and proxies must be strong.",
            [(r"\text{treatment bridge}", r":", r"\text{weights}", 40),
             (r"\text{both}", r":", r"\text{doubly robust}", 40),
             (r"\text{nonparametric}", r":", r"\text{kernel, \ neural, \ minimax}", 40),
             (r"\text{price}", r":", r"\text{ill-posed: \ strong proxies needed}", 40)],
            [r"inverse weighting", r"Cui et al. (2023)", r"conditional moments", r"like nonparametric IV"],
            colors=[(1, IDC), (3, NAIVEC)])

    def negcontrols(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The proxies have an older name in epidemiology: negative controls. <bookmark mark='b'/> A "
            "negative control outcome is one the treatment cannot affect, such as flu vaccination's effect on injuries; a "
            "negative control exposure is one that cannot affect the outcome. <bookmark mark='c'/> Marc Lipsitch, Eric "
            "Tchetgen Tchetgen and Ted Cohen argued in 2010 that an association with a negative control reveals "
            "confounding. <bookmark mark='d'/> Proximal inference goes further: with one of each, it removes the confounding "
            "instead of only detecting it.",
            [(r"\text{negative control outcome}", r":", r"\text{unaffected by } A", 40),
             (r"\text{negative control exposure}", r":", r"\text{does not affect } Y", 40),
             (r"\text{detect}", r":", r"\text{association} \Rightarrow \text{confounding}", 40),
             (r"\text{proximal}", r":", r"\text{one of each} \Rightarrow \text{correct}", 40)],
            [r"the epidemiologists' tool", r"vaccines and injuries", r"Lipsitch et al. (2010)", r"from detection to correction"],
            colors=[(3, IDC)])

    def weak(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The price shows in the chart's wider green curve. <bookmark mark='b'/> The proximal "
            "estimator is an instrumental-variables estimator, so it inherits Part thirty-seven's weak-instrument problem: "
            "if the treatment proxy Z says little about the outcome proxy W, the first stage is weak and the estimate "
            "unstable. <bookmark mark='c'/> Here each proxy is the confounder plus noise of equal size; with noisier "
            "proxies the spread grows quickly, and the usual intervals start to undercover. <bookmark mark='d'/> So report "
            "the first-stage strength, as for any instrument, and prefer weak-instrument-robust intervals such as "
            "Anderson and Rubin's when it is low.",
            [(r"\text{proximal}", r"=", r"\text{IV with } Z \text{ instrumenting } W", 40),
             (r"\text{weak } Z \to W", r":", r"\text{unstable, \ undercovering}", 40),
             (r"\text{here}", r":", r"\text{signal-to-noise one in each proxy}", 40),
             (r"\text{remedy}", r":", r"\text{report first-stage } F; \ \text{Anderson--Rubin}", 40)],
            [r"the variance", r"Part 37", r"a strong design", r"robust intervals"],
            colors=[(1, NAIVEC), (3, IDC)])
