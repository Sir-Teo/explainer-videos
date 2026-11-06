from __future__ import annotations

import numpy as np

from videos.stats.stats33.common import *  # noqa: F403


class Adaptive(VoiceoverScene):
    def construct(self):
        self.card()
        self.waste()
        self.storey()
        self.picture()
        self.qvalue()
        self.twostage()
        self.when()

    def card(self):
        card = chapter_card(4, r"Adaptive FDR", r"Estimating the share of nulls", lit=(1995,), part=PART)
        with self.voiceover("Chapter four. Adaptive false discovery rates."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def waste(self):
        rows = [
            cmath(r"\text{FDR(BH at } q)", r"=", r"\pi_0 q", font_size=32),
            cmath(r"\pi_0 = 0.5", r"\Rightarrow", r"\text{FDR} = q/2: \ \text{half the budget unspent}", font_size=30),
            cmath(r"\text{BH at } q/\pi_0", r"\Rightarrow", r"\text{FDR} = q \ \text{exactly}", font_size=32),
            cmath(r"\text{but}", r":", r"\pi_0 \text{ is unknown: \ estimate it}", font_size=32),
        ]
        rows[2][-1].set_color(BHC)
        whys = [why(r"chapter three"), why(r"many real effects"), why(r"use the whole budget"), why(r"Storey (2002)")]
        with self.voiceover(
            "<bookmark mark='a'/> BH's false discovery rate is pi zero times q. <bookmark mark='b'/> If half the hypotheses "
            "are false, it spends only half the error budget. <bookmark mark='c'/> Running BH at q over pi zero would spend "
            "all of it, and find more. <bookmark mark='d'/> But pi zero is unknown, so John Storey proposed in 2002 to "
            "estimate it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def storey(self):
        rows = [
            cmath(r"p > \lambda", r":", r"\text{almost all nulls}", font_size=32),
            cmath(r"E\,\#\{p_i > \lambda\}", r"\approx", r"m_0 (1 - \lambda)", font_size=32),
            cmath(r"\hat\pi_0(\lambda)", r"=", r"\dfrac{\#\{p_i > \lambda\}}{m (1 - \lambda)}", font_size=32),
            cmath(r"\text{bias}", r":", r"\text{upward, \ so conservative}", font_size=32),
        ]
        rows[2][-1].set_color(BHC)
        whys = [why(r"real effects rarely have large $p$"), why(r"nulls are uniform"), why(r"e.g. $\lambda = 0.5$"),
                why(r"a few real effects land above $\lambda$")]
        with self.voiceover(
            "<bookmark mark='a'/> The idea is the flat floor of chapter one's histogram. Above some lambda, such as a half, "
            "almost all p-values come from true nulls. <bookmark mark='b'/> Uniform null p-values put a share one minus "
            "lambda of themselves there. <bookmark mark='c'/> So count the p-values above lambda and divide by m times one "
            "minus lambda. <bookmark mark='d'/> The few real effects that land above lambda bias the estimate upwards, which "
            "errs on the safe side."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("genes")
        h = np.asarray(d["hist"], float)
        edges = np.linspace(0, 1, 21)
        dens = h / (h.sum() * 0.05)
        A = axes([0, 1], [0, 5.2], x_length=7.4, y_length=4.4, xlabel=r"$p$-value", ylabel=r"density",
                 xticks=[0, 0.5, 1], yticks=[0, 1, 2, 4], center=[-2.0, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, np.minimum(dens, 5.2), color=BHC, opacity=0.5)
        right = VGroup(*[b for b, e in zip(bars, edges[:-1]) if e >= 0.5]).copy().set_fill(NULLC, opacity=0.9)
        lam = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, 4.8), color=SIGC, stroke_width=2.5)
        flat = DashedLine(ax.c2p(0, d["pi0"]), ax.c2p(1, d["pi0"]), color=SIGC, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"$\lambda = 0.5$", font_size=22, color=SIGC),
            label(r"grey: \ the $p$-values above $\lambda$", font_size=22, color=NULLC),
            label(rf"$\hat\pi_0 = {d['pi0']:.3f}$ \ (truth 0.950)", font_size=22, color=SIGC),
            label(r"Storey at $q = 0.1$: \ the same 184 here", font_size=22, color=BHC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the genes, with lambda a half: <bookmark mark='b'/> the p-values above a half fill the "
            "grey bars, <bookmark mark='c'/> and their level gives pi zero hat of point nine six two, close to the true "
            "point nine five. <bookmark mark='d'/> Since that is so close to one, the adaptive procedure rejects the same "
            "hundred and eighty-four genes as BH. Adaptivity matters when many hypotheses are false."
        ) as vo:
            self.add(genes_tag())
            self.play(FadeIn(A), FadeIn(bars))
            vo.wait_until("a")
            self.play(Create(lam), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(flat), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def qvalue(self):
        rows = [
            cmath(r"q_i", r"=", r"\min_{t \ge p_i} \widehat{\mathrm{FDR}}(t) = \hat\pi_0 \cdot p^{\mathrm{BH}}_i", font_size=30),
            cmath(r"\text{reading}", r":", r"\text{the FDR of the list cut just below gene } i", font_size=30),
            cmath(r"\text{versus } p_i", r":", r"p \text{ is about one test; \ } q \text{ is about a list}", font_size=30),
            cmath(r"q_i \le 0.1", r":", r"\text{the standard of genomics}", font_size=32),
        ]
        rows[0][-1].set_color(BHC)
        whys = [why(r"Storey (2003): \ the $q$-value"), why(r"a gene's own FDR level"), why(r"not the same thing"),
                why(r"Storey \& Tibshirani (2003)")]
        with self.voiceover(
            "<bookmark mark='a'/> Storey's q-value attaches a number to each gene: the smallest false discovery rate at which "
            "that gene would be called significant, pi zero hat times the BH adjusted p-value. <bookmark mark='b'/> It reads "
            "as the false discovery rate of the list cut just below that gene. <bookmark mark='c'/> A p-value is about one "
            "test; a q-value is about a list. <bookmark mark='d'/> Reporting genes with q-values below ten percent, after "
            "Storey and Tibshirani's paper of 2003, became the standard of genomics."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def when(self):
        rows = fit_rows(VGroup(
            label(r"adaptive FDR helps when many hypotheses are false: \ $\pi_0 = 0.5$ doubles the budget", font_size=26, color=BHC),
            label(r"its guarantee needs independence; \ under dependence $\hat\pi_0$ is noisy", font_size=26, color=FALSEC),
            label(r"other estimators: \ Storey's bootstrap $\lambda$, \ Langaas's convex fit, \ Efron's central matching", font_size=26),
            label(r"next: \ from tail areas to the density itself", font_size=26, color=SIGC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Adaptive procedures help most when many hypotheses are false; with pi zero a half they "
            "roughly double the error budget actually used. <bookmark mark='b'/> Their guarantees lean harder on "
            "independence, since under dependence the estimate of pi zero is itself noisy. <bookmark mark='c'/> There are "
            "many estimators of pi zero: Storey's bootstrap choice of lambda, convex density fits, and Efron's central "
            "matching. <bookmark mark='d'/> Efron's approach goes further, from tail areas to densities: the next chapter."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def twostage(self):
        rows = [
            cmath(r"\text{stage 1}", r":", r"\text{BH at } q' = q/(1 + q): \ r_1 \text{ rejections}", font_size=30),
            cmath(r"\hat m_0", r"=", r"m - r_1", font_size=32),
            cmath(r"\text{stage 2}", r":", r"\text{BH at } q' m / \hat m_0", font_size=32),
            cmath(r"\text{FDR}", r"\le", r"q \ \text{(independence), \ more power than BH}", font_size=30),
        ]
        rows[2][-1].set_color(BHC)
        whys = [why(r"Benjamini, Krieger \& Yekutieli (2006)"), why(r"an estimate of the nulls"), why(r"the adaptive step"), why(r"a finite-sample guarantee")]
        with self.voiceover(
            "<bookmark mark='a'/> Benjamini, Abba Krieger and Yekutieli gave an adaptive procedure with a "
            "finite-sample guarantee. First run BH at a slightly reduced level, q over one plus q. <bookmark "
            "mark='b'/> Estimate the number of true nulls as m minus the number of first-stage rejections. <bookmark "
            "mark='c'/> Then run BH again at the reduced level inflated by m over that estimate. <bookmark mark='d'/> "
            "Under independence its false discovery rate is at most q, exactly, and it rejects more than BH whenever "
            "many hypotheses are false."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
