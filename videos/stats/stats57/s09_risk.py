from __future__ import annotations

import numpy as np

from videos.stats.stats57.common import *  # noqa: F403


class Risk(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.proof()
        self.crc_worked()
        self.ltt()
        self.chart()
        self.llm()

    def card(self):
        card = chapter_card(8, r"Risk control", r"Beyond coverage: \ any monotone loss", lit=(2024,), part=PART)
        with self.voiceover("Chapter eight. Risk control: beyond coverage, to any monotone loss."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\text{a family of sets } C_\lambda", r":", r"\text{growing in } \lambda; \ \text{a loss } L_i(\lambda) \in [0, B] \text{ shrinking in } \lambda", font_size=32),
            cmath(r"\text{coverage}", r":", r"L_i(\lambda) = 1\{Y_i \notin C_\lambda(X_i)\}", font_size=36),
            cmath(r"\text{or}", r":", r"\text{the share of true labels missed \ (FNR)}", font_size=36),
            cmath(r"\hat\lambda", r"=", r"\inf\Big\{\lambda: \ \frac{n}{n+1}\hat R_n(\lambda) + \frac{B}{n+1} \le \alpha\Big\}", font_size=36),
        ]
        rows[3][-1].set_color(COVC)
        whys = [why(r"Angelopoulos, \ Bates, \ Fisch, \ Lei \& Schuster"), why(r"the special case"), why(r"multilabel, \ segmentation"), why(r"conformal risk control (2024)")]
        with self.voiceover(
            "<bookmark mark='a'/> Anastasios Angelopoulos, Stephen Bates, Adam Fisch, Lihua Lei and Tal Schuster generalized "
            "the lemma from coverage to any bounded loss that shrinks as the prediction set grows. <bookmark mark='b'/> Coverage "
            "is the special case where the loss is the miss indicator. <bookmark mark='c'/> But the loss could be the fraction of "
            "an image's tumour pixels missed by a segmentation, or of a document's correct labels missed by a tagger: a false "
            "negative rate. <bookmark mark='d'/> Choose lambda as the smallest value whose empirical risk, slightly inflated, is "
            "at most alpha."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\lambda'", r"=", r"\inf\{\lambda: \hat R_{n+1}(\lambda) \le \alpha\}: \ \text{the oracle with all } n + 1 \text{ losses}", font_size=32),
            cmath(r"\hat\lambda \ge \lambda'", r":", r"\text{since } L_{n+1} \le B \text{ was assumed in the inflation}", font_size=34),
            cmath(r"\lambda' \text{ symmetric in the } n + 1", r"\Rightarrow", r"E\,L_{n+1}(\lambda') = E\,\hat R_{n+1}(\lambda') \le \alpha", font_size=32),
            cmath(r"\text{monotone}", r"\Rightarrow", r"E\,L_{n+1}(\hat\lambda) \le E\,L_{n+1}(\lambda') \le \alpha \qquad \blacksquare", font_size=34),
        ]
        rows[3][-1].set_color(COVC)
        whys = [why(r"exchangeability's trick"), why(r"the worst case for the unseen loss"), why(r"the test loss is a typical one"), why(r"larger $\lambda$, \ smaller loss")]
        with self.voiceover(
            "<bookmark mark='a'/> The proof copies the lemma's. Define an oracle lambda prime using all n plus one losses, "
            "including the test point's. <bookmark mark='b'/> The real lambda hat is at least as large, because its inflation "
            "assumed the worst value for the unseen loss. <bookmark mark='c'/> The oracle is a symmetric function of the n plus "
            "one points, so the test point's expected loss at it equals the average loss, at most alpha. <bookmark mark='d'/> "
            "And since the loss shrinks as lambda grows, the expected loss at lambda hat is no larger."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def crc_worked(self):
        rows = [
            cmath(r"n = 100, \ B = 1, \ \alpha = 0.1", r":", r"\text{need } \frac{100\,\hat R_n(\lambda) + 1}{101} \le 0.1", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\hat R_n(\lambda) \le 0.091", font_size=38),
            cmath(r"\text{the } +B \text{ term}", r":", r"\text{one worst-case point added: \ a finite-sample margin}", font_size=34),
            cmath(r"\text{as } n \to \infty", r":", r"\hat\lambda \to \text{the level where the risk is exactly } \alpha", font_size=34),
        ]
        rows[1][-1].set_color(COVC)
        whys = [why(r"the rule"), why(r"9.1\%, \ not 10\%"), why(r"like the $+1$ in the lemma"), why(r"no waste in the limit")]
        with self.voiceover(
            "<bookmark mark='a'/> In numbers: with a hundred calibration examples, losses bounded by one, and alpha a "
            "tenth, the rule needs a hundred times the empirical risk, plus one, over a hundred and one, to be at most "
            "a tenth. <bookmark mark='b'/> That is an empirical risk of at most nine point one percent, not ten. "
            "<bookmark mark='c'/> The extra B is a worst-case loss for the unseen test point, exactly as the plus one "
            "is in the quantile lemma. <bookmark mark='d'/> As n grows the margin vanishes, and the chosen lambda "
            "tends to the level where the true risk is exactly alpha."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ltt(self):
        rows = [
            cmath(r"\text{non-monotone losses}", r":", r"\text{the argument fails}", font_size=36),
            cmath(r"\text{learn then test}", r":", r"\text{test } H_\lambda: R(\lambda) > \alpha \text{ for each } \lambda \text{ on a grid}", font_size=34),
            cmath(r"\text{fixed-sequence or FWER control}", r":", r"P\big(R(\hat\lambda) \le \alpha\big) \ge 1 - \delta", font_size=32),
            cmath(r"\text{so}", r":", r"\text{any loss, \ many parameters, \ w.h.p.}", font_size=36),
        ]
        rows[2][-1].set_color(COVC)
        whys = [why(r"e.g. precision"), why(r"Angelopoulos et al. (2021)"), why(r"Part 33's tools"), why(r"more general, \ more conservative")]
        with self.voiceover(
            "<bookmark mark='a'/> For losses that are not monotone in lambda, such as precision, the proof fails. "
            "<bookmark mark='b'/> Learn then test, from Angelopoulos and colleagues, turns risk control into multiple "
            "testing: for each lambda on a grid, test the hypothesis that its risk exceeds alpha. <bookmark mark='c'/> "
            "Controlling the family-wise error over the grid, with Part thirty-three's tools, guarantees that with "
            "probability one minus delta, the chosen lambda's risk is at most alpha. <bookmark mark='d'/> It works for "
            "any loss and any number of tuning parameters, at the price of being more conservative."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def llm(self):
        rows = [
            cmath(r"\text{language models}", r":", r"\text{keep only the claims whose confidence exceeds } 1 - \lambda", font_size=34),
            cmath(r"\text{loss}", r":", r"1\{\text{any kept claim is false}\}", font_size=36),
            cmath(r"\text{calibrate } \lambda", r":", r"\text{on documents with checked claims}", font_size=36),
            cmath(r"\Rightarrow", r"\;", r"P(\text{the filtered output contains an error}) \le \alpha", font_size=36),
        ]
        rows[3][-1].set_color(COVC)
        whys = [why(r"conformal factuality"), why(r"a monotone loss"), why(r"exchangeable prompts"), why(r"Part 64's subject")]
        with self.voiceover(
            "<bookmark mark='a'/> The same tool reaches language models. Split a model's answer into claims, and keep "
            "only those whose confidence exceeds one minus lambda. <bookmark mark='b'/> Let the loss be whether any "
            "kept claim is false: it shrinks as fewer claims are kept. <bookmark mark='c'/> Calibrate lambda on "
            "documents whose claims were checked by hand. <bookmark mark='d'/> Then, for an exchangeable new prompt, "
            "the chance that the filtered answer contains an error is at most alpha: a guarantee about a black box, "
            "which is Part sixty-four's subject."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("risk")
        lam = np.asarray(d["curve_lam"])
        A = axes([0, 1], [0, 1.02], x_length=7.4, y_length=4.4, xlabel=r"$\lambda$: \ include label $k$ if its score $\ge 1 - \lambda$", ylabel=r"false negative rate",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.1, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        c = polyline(ax, lam, d["curve_risk"], CALC, 4)
        a = DashedLine(ax.c2p(0, 0.1), ax.c2p(1, 0.1), color=GREY_B, stroke_width=2)
        v = DashedLine(ax.c2p(d["lam"], 0), ax.c2p(d["lam"], 1.02), color=TESTPT, stroke_width=3)
        side = fit_rows(VGroup(
            label(r"20 candidate labels per unit, \ 15\% true; \ a noisy scorer", font_size=22),
            label(r"teal: \ the calibration set's FNR by $\lambda$ \ ($n = 500$)", font_size=22, color=CALC),
            label(rf"gold: \ $\hat\lambda = {d['lam']:.3f}$, \ the first under $\alpha = 0.1$ after inflation", font_size=22, color=TESTPT),
            label(rf"20,000 new units: \ FNR {d['test_fnr']:.3f}; \ {d['set_size']:.1f} labels per set", font_size=22, color=COVC),
            label(rf"over 200 calibration sets: \ mean FNR {d['mean_fnr']:.3f} $\le 0.1$", font_size=22, color=COVC),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A multilabel screen: twenty candidate labels per unit, about fifteen percent of them true, "
            f"and a noisy scorer. <bookmark mark='b'/> In teal, the calibration set's false negative rate as lambda grows and "
            f"the sets include more labels. <bookmark mark='c'/> Lambda hat is {say(d['lam'], 3)}, the first value under a "
            f"tenth after the inflation. <bookmark mark='d'/> On twenty thousand new units the false negative rate is "
            f"{say(d['test_fnr'], 3)}, with sets of about {say(d['set_size'], 1)} labels. <bookmark mark='e'/> Averaged over two "
            f"hundred calibration sets, {say(d['mean_fnr'], 3)}: the guarantee is in expectation, and it holds."
        ) as vo:
            self.play(FadeIn(A), FadeIn(a), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(v), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
