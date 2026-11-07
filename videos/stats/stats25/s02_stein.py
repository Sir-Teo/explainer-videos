from __future__ import annotations

import numpy as np

from videos.stats.stats25.common import *  # noqa: F403


class Stein(VoiceoverScene):
    def construct(self):
        self.card()
        self.estimator()
        self.geometry()
        self.lemma()
        self.risk()
        self.curves()
        self.remarks()

    def card(self):
        card = chapter_card(1, r"James--Stein", r"Inadmissibility, \ proved", lit=(1956, 1961), part=PART)
        with self.voiceover("Chapter one. The James–Stein estimator."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def estimator(self):
        rows = [
            cmath(r"X", r"\sim", r"N_p(\theta, I), \ \ p \ge 3", font_size=30),
            cmath(r"\text{risk}", r"=", r"E\,\|\hat\theta - \theta\|^2; \ \ \text{the MLE } X: \ p", font_size=30),
            cmath(r"\hat\theta^{JS}", r"=", r"\Big(1 - \dfrac{p - 2}{\|X\|^2}\Big) X", font_size=32),
            cmath(r"\text{towards } \bar X", r":", r"(p - 3) \text{ in place of } (p - 2), \ p\ge4", font_size=30),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"$p$ means, \ one observation each"), why(r"total squared error"),
                why(r"James \& Stein (1961)"), why(r"one degree of freedom spent on the target")]
        intro = label('Known equal-variance normal observations and total squared-error risk', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The setting: p means, each measured once with normal error of variance one. "
            "<bookmark mark='b'/> Judge an estimator by its risk, the expected total squared error. The obvious "
            "estimator, X itself, which is also the maximum likelihood estimate, has risk exactly p. <bookmark "
            "mark='c'/> Willard James and Charles Stein's estimator multiplies X by one minus p minus two over the "
            "squared length of X: the farther the data from zero, the less it shrinks. <bookmark mark='d'/> Shrinking"
            " towards the grand mean instead, as Efron and Morris did, costs one degree of freedom: p minus three. "
            "Strict improvement for this estimated target requires at least four means."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lemma(self):
        rows = [
            cmath(r"\text{Stein's lemma}", r":", r"E\,(X_i - \theta_i)\, h(X) = E\, \partial_i h(X)", font_size=30),
            cmath(r"\hat\theta", r"=", r"X + g(X)", font_size=30),
            cmath(r"E\,\|\hat\theta - \theta\|^2", r"=", r"p + E\,\{\|g\|^2 + 2\nabla \cdot g\}", font_size=30),
            cmath(r"\text{SURE}", r"=", r"p + \|g(X)\|^2 + 2\nabla \cdot g(X)", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"integrate by parts against the normal density"), why(r"any correction $g$"),
                why(r"expand the square, \ apply the lemma"), why(r"Stein's unbiased risk estimate (1981)")]
        intro = label('Integration by parts provides an unbiased risk identity', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The proof rests on Stein's lemma, an integration by parts against the normal "
            "density: the covariance of an error with a smooth function of X equals the expected derivative of that "
            "function. <bookmark mark='b'/> Write an estimator as X plus a sufficiently regular correction g, with "
            "integrable derivatives and risk. <bookmark mark='c'/> Expand the squared error and apply the lemma to "
            "the cross term: the risk is p plus the expected squared correction plus twice its expected divergence. "
            "<bookmark mark='d'/> Everything inside that expectation is computable from the data, so it is an "
            "unbiased estimate of the risk, Stein's unbiased risk estimate, SURE."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def risk(self):
        rows = [
            cmath(r"g(X)", r"=", r"-\dfrac{(p - 2)}{\|X\|^2} X", font_size=30),
            cmath(r"\nabla \cdot g", r"=", r"-\dfrac{(p - 2)^2}{\|X\|^2}", font_size=30),
            cmath(r"\text{SURE}", r"=", r"p - \dfrac{(p - 2)^2}{\|X\|^2}", font_size=30),
            cmath(r"\text{risk}", r"=", r"p - (p - 2)^2\, E\,\|X\|^{-2} < p \ \ \text{for every } \theta", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"James--Stein's correction"), why(r"a short calculation"), why(r"always below $p$"),
                why(r"the MLE is dominated")]
        intro = label('James-Stein improves total expected risk for every fixed mean vector', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> For James–Stein, the correction is minus p minus two over the squared length, times X. "
            "<bookmark mark='b'/> Its divergence works out to minus p minus two squared over the squared length. "
            "<bookmark mark='c'/> So SURE is p minus p minus two squared over the squared length of X. <bookmark mark='d'/> "
            "Taking expectations, the risk is p minus a positive quantity, for every theta whatsoever. The maximum likelihood "
            "estimate is beaten everywhere: it is inadmissible. The argument needs p minus two to be positive, which is why "
            "it starts at three."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        d = load("risk")
        r = np.asarray(d["norms"])
        A = axes([0, 8], [0, 11], x_length=8.0, y_length=4.4, xlabel=r"$\|\theta\|$, \ distance of the truth from zero",
                 ylabel=r"risk", xticks=[0, 2, 4, 6, 8], yticks=[0, 2, 4, 6, 8, 10], center=[-1.6, 0.3, 0])
        ax = A.ax
        mle = DashedLine(ax.c2p(0, d["p"]), ax.c2p(8, d["p"]), color=RAW, stroke_width=3)
        js = polyline(ax, r, d["js"], SHRUNK, 3.5)
        jp = polyline(ax, r, d["js_plus"], PATH, 3.5)
        rows = fit_rows(VGroup(
            label(rf"$p = {d['p']}$, \ simulated risks", font_size=22),
            label(rf"blue: \ the MLE, \ risk {d['p']}, \ everywhere", font_size=22, color=RAW),
            label(rf"green: \ James--Stein: \ {d['js'][0]:.1f} at $\theta = 0$", font_size=22, color=SHRUNK),
            label(rf"gold: \ positive part: \ {d['js_plus'][0]:.1f}", font_size=22, color=PATH),
            label(r"the gain fades as $\|\theta\|$ grows, \ never below zero", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are the risks, simulated for ten means, against how far the true means are from the "
            "shrinkage target. <bookmark mark='b'/> The maximum likelihood estimate's risk is ten, everywhere. "
            "<bookmark mark='c'/> James–Stein's is two when the truth is at the target, an eighty percent saving, "
            "<bookmark mark='d'/> and the positive-part version, which never shrinks past zero, does better still. "
            "<bookmark mark='e'/> As the truth moves away the advantage fades, but it never turns into a loss. Choose the "
            "target well, near where the means really are, and the saving is large."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(mle), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(js), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(jp), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def remarks(self):
        rows = fit_rows(VGroup(
            label(r"the gain is in the total: \ some individual estimates get worse", font_size=24, color=RES),
            label(r"James--Stein itself is inadmissible: \ the positive part beats it", font_size=24),
            label(r"any target works; \ a good one works better", font_size=24, color=SHRUNK),
            label(r"why it works: \ the next chapter's empirical Bayes", font_size=24, color=PRIOR),
            label(r"admissibility in general: \ Part 45", font_size=24, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Three cautions. The guarantee is for the total error: some individual players, the truly "
            "exceptional ones, can be estimated worse. <bookmark mark='b'/> James–Stein is itself inadmissible, since the "
            "positive part beats it. <bookmark mark='c'/> Any fixed target works, but a good one works much better. "
            "<bookmark mark='d'/> Why it works at all is clearest from the empirical Bayes view of the next chapter, "
            "<bookmark mark='e'/> and Part 45 develops the theory of admissibility in general."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def geometry(self):
        rows = [
            cmath(r"E\,\|X\|^2", r"=", r"\|\theta\|^2 + p", font_size=32),
            cmath(r"\text{so}", r":", r"\text{squared length is too large, \ on average, \ by }p", font_size=30),
            cmath(r"\text{best shrink}", r":", r"cX, \ \ c^* = \tfrac{\|\theta\|^2}{\|\theta\|^2 + p} \approx 1 - \tfrac{p}{\|X\|^2}", font_size=30),
            cmath(r"p = 1, 2", r":", r"\text{the domination argument does not apply}", font_size=30),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"each coordinate adds one unit of noise"), why(r"in high dimensions, \ noise is length"),
                why(r"estimate $\|\theta\|^2$ by $\|X\|^2 - p$"), why(r"so the paradox needs three")]
        intro = label('Squared lengths explain a shrinkage heuristic; SURE supplies the proof', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The squared length of X has expectation theta's squared length plus p: each "
            "coordinate contributes one unit of noise. <bookmark mark='b'/> It is the squared length that is too "
            "large by p, not the length itself. <bookmark mark='c'/> The best constant multiple of X uses the ratio "
            "of theta's squared length to that squared length plus p. Plugging in an estimate suggests shrinkage, but"
            " this heuristic is not the proof for an adaptive rule. <bookmark mark='d'/> The rigorous argument next "
            "gives p minus two and requires at least three dimensions."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
