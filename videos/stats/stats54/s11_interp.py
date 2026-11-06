from __future__ import annotations

import numpy as np

from videos.stats.stats54.common import *  # noqa: F403


class Interpolation(VoiceoverScene):
    def construct(self):
        self.card()
        self.puzzle()
        self.double()
        self.benign_theory()
        self.benign_chart()
        self.kernels()
        self.uniform()
        self.lesson()

    def card(self):
        card = chapter_card(10, r"Interpolation", r"Double descent and benign overfitting", lit=(2020,), part=PART)
        with self.voiceover("Chapter ten. Interpolation: double descent and benign overfitting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def puzzle(self):
        rows = [
            cmath(r"\text{Zhang et al. (2017)}", r":", r"\text{networks fit random labels perfectly}", font_size=34),
            cmath(r"\text{so}", r":", r"\text{their Rademacher complexity is near its maximum}", font_size=34),
            cmath(r"\text{yet}", r":", r"\text{trained on real labels, \ they generalize}", font_size=34),
            cmath(r"\text{the classical story}", r":", r"\text{zero training error on noisy data} \Rightarrow \text{overfitting}", font_size=32),
        ]
        rows[0][-1].set_color(BADC)
        rows[2][-1].set_color(GOODC)
        whys = [why(r"``rethinking generalization''"), why(r"chapter 3, \ vacuous"), why(r"the puzzle"), why(r"which seems false")]
        with self.voiceover(
            "<bookmark mark='a'/> In 2017, Chiyuan Zhang and colleagues showed that standard image-recognition networks can "
            "fit completely random labels perfectly. <bookmark mark='b'/> So their Rademacher complexity is essentially "
            "maximal, and every bound of chapter three is vacuous. <bookmark mark='c'/> Yet the same networks, trained on the "
            "real labels, generalize well. <bookmark mark='d'/> And they fit their noisy training labels exactly, which the "
            "classical story says is the definition of overfitting."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def double(self):
        d = load("interp")
        lp = np.log10(d["ps"])
        lr = np.log10(d["risk"])
        A = axes([0.9, 3.1], [-0.2, 3.3], x_length=7.4, y_length=4.4, xlabel=rf"number of features $p$ \ (log scale), \ $n = {d['n']}$", ylabel=r"$\log_{10}$ test risk",
                 xticks=[1, np.log10(30), 2, np.log10(300), 3], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 1, 2, 3], center=[-2.5, 0.2, 0])
        ax = A.ax
        c = VGroup(polyline(ax, lp, lr, CLASSC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=CLASSC) for a, b in zip(lp, lr)])
        th = DashedLine(ax.c2p(2, -0.2), ax.c2p(2, 3.3), color=BADC, stroke_width=2.5)
        r = dict(zip(d["ps"], d["risk"]))
        side = fit_rows(VGroup(
            label(r"min-norm least squares on the first $p$ of 1,000 features", font_size=22),
            label(rf"$p < n$: \ the classical U, \ {r[10]:.2f} at $p = 10$", font_size=22, color=TESTC),
            label(rf"red: \ $p = n$: \ the interpolation threshold, \ {r[100]:,.0f}", font_size=22, color=BADC),
            label(rf"$p > n$: \ a second descent, \ to {r[1000]:.2f} at 1,000", font_size=22, color=GOODC),
            label(r"the best model interpolates", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Double descent, the phenomenon Mikhail Belkin and colleagues named in 2019. Least squares "
            f"on the first p of a thousand features, a hundred observations, and when p exceeds n the minimum-norm "
            f"interpolating solution. <bookmark mark='b'/> With few features, the classical picture: risk {say(r[10], 2)} at "
            f"ten, rising as the fit grows noisier. <bookmark mark='c'/> At p equal to n, the interpolation threshold, the "
            f"design is barely invertible and the risk explodes to about {r[100]:,.0f}. <bookmark mark='d'/> Beyond it, a "
            f"second descent: among the many interpolating solutions the minimum-norm one spreads the noise across many "
            f"directions, and the risk falls to {say(r[1000], 2)} with a thousand features. <bookmark mark='e'/> Here the "
            f"best model of all is one that fits the training data exactly."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(th), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def benign_theory(self):
        rows = [
            cmath(r"\Sigma", r"=", r"\text{a few large eigenvalues } + \text{ a long flat tail}", font_size=34),
            cmath(r"\text{min-norm interpolation}", r":", r"\text{the signal from the large directions, \ the noise absorbed by the tail}", font_size=30),
            cmath(r"\text{excess risk}", r"\lesssim", r"\text{bias} + \sigma^2\Big(\frac{k}{n} + \frac{n}{R_k(\Sigma)}\Big)", font_size=34),
            cmath(r"\text{benign}", r"\iff", r"\text{the tail's effective rank } R_k \gg n", font_size=34),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"a spiked spectrum (Part 52)"), why(r"many tiny directions"), why(r"Bartlett, \ Long, \ Lugosi \& Tsigler (2020)"), why(r"$R_k = (\sum_{j>k}\lambda_j)^2/\sum_{j>k}\lambda_j^2$")]
        with self.voiceover(
            "<bookmark mark='a'/> Why can interpolation be harmless? Suppose the features' covariance has a few large "
            "eigenvalues plus a long, flat tail of tiny ones. <bookmark mark='b'/> The minimum-norm interpolator learns the "
            "signal from the large directions and hides the noise in the tail, where many small coordinates absorb it "
            "without affecting predictions much. <bookmark mark='c'/> Peter Bartlett, Philip Long, Gábor Lugosi and Alexander "
            "Tsigler proved in 2020 that the excess risk is a bias term plus sigma squared times k over n plus n over the "
            "tail's effective rank. <bookmark mark='d'/> Overfitting is benign exactly when the tail's effective rank is "
            "much larger than n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def benign_chart(self):
        d = load("interp")
        rows = [[r"$n$"] + [str(b["n"]) for b in d["benign"]],
                [r"excess risk, \ long tail (20,000 tiny features)"] + [f"{b['excess']:.3f}" for b in d["benign"]],
                [r"noise level $\sigma^2$"] + [f"{b['noise']:.2f}" for b in d["benign"]]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.45, colors=[GREY_B, GOODC, GREY_A])
        tab.move_to([0, 1.0, 0])
        s = d["short_tail"]
        foot = label(rf"short tail (400 features, \ $n = 200$): \ excess {s['excess']:.3f}, \ as large as the noise", font_size=24, color=BADC).move_to([0, -0.8, 0])
        foot2 = label(r"same signal, \ same interpolation: \ the spectrum decides", font_size=24, color=CLASSC).move_to([0, -1.6, 0])
        b = d["benign"]
        with self.voiceover(
            f"<bookmark mark='a'/> A test. Five strong features carry the signal, plus twenty thousand tiny ones. Every fit "
            f"interpolates its training data exactly, noise and all, yet the excess risk falls from {say(b[0]['excess'], 3)} "
            f"at fifty observations to {say(b[-1]['excess'], 3)} at four hundred, far below the noise level of a quarter. "
            f"<bookmark mark='b'/> With a short tail of only four hundred features, the same interpolation at two hundred "
            f"observations has excess risk {say(s['excess'], 3)}, as large as the noise itself: harmful overfitting. "
            f"<bookmark mark='c'/> Same signal, same algorithm: the spectrum of the features decides."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def kernels(self):
        rows = [
            cmath(r"\text{ridgeless kernel regression}", r":", r"\text{interpolates, \ and can generalize in high dimension}", font_size=32),
            cmath(r"\text{nearest-neighbour schemes}", r":", r"\text{singular weights interpolate, \ still consistent}", font_size=34),
            cmath(r"\text{gradient descent}", r":", r"\text{from zero, \ converges to the min-norm interpolator}", font_size=34),
            cmath(r"\text{implicit bias}", r":", r"\text{the algorithm chooses which interpolator}", font_size=34),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Liang \& Rakhlin (2020)"), why(r"Belkin, \ Rakhlin \& Tsybakov (2019)"), why(r"for least squares"), why(r"the real regularizer")]
        with self.voiceover(
            "<bookmark mark='a'/> The phenomenon is not special to linear models. Tengyuan Liang and Alexander Rakhlin showed in 2020 that kernel regression with no ridge penalty interpolates and can still generalize in high dimension. <bookmark mark='b'/> Mikhail Belkin, Rakhlin and Alexandre Tsybakov built interpolating nearest-neighbour-style rules, with singular weights, that are statistically consistent. <bookmark mark='c'/> And gradient descent on least squares, started from zero, converges to exactly the minimum-norm interpolator of the double-descent chart. <bookmark mark='d'/> The algorithm, not an explicit penalty, decides which interpolator is found: its implicit bias is the real regularizer."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def uniform(self):
        rows = [
            cmath(r"\text{Nagarajan \& Kolter (2019)}", r":", r"\text{uniform convergence may be unable to explain it}", font_size=32),
            cmath(r"\text{the construction}", r":", r"\text{the gap over any class containing the learned rules is near 1}", font_size=30),
            cmath(r"\text{even}", r":", r"\text{the tightest algorithm-dependent uniform bound is vacuous}", font_size=32),
            cmath(r"\text{instead}", r":", r"\text{implicit bias of the algorithm, \ exact asymptotics, \ stability}", font_size=32),
        ]
        rows[0][-1].set_color(BADC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"NeurIPS outstanding paper"), why(r"overparameterized linear classifiers"), why(r"a limit of the method"), why(r"Part 59")]
        with self.voiceover(
            "<bookmark mark='a'/> Vaishnavh Nagarajan and Zico Kolter argued in 2019 that uniform convergence itself may be "
            "unable to explain these successes. <bookmark mark='b'/> They built settings, overparameterized linear "
            "classifiers trained by gradient descent, where the uniform deviation over any class containing the learned rules "
            "is close to one, though the learned rules generalize well. <bookmark mark='c'/> Even the tightest uniform bound, "
            "tailored to the algorithm, is then vacuous. <bookmark mark='d'/> What explains the successes instead is the "
            "implicit bias of the algorithm, which picks particular interpolators like the minimum-norm one, and exact "
            "high-dimensional asymptotics, the subject of Part fifty-nine."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"where learning theory stands:", font_size=28, color=GREY_A),
            label(r"for classical regimes: \ VC, \ Rademacher, \ margins, \ PAC-Bayes and stability are sharp and useful", font_size=26, color=GOODC),
            label(r"for overparameterized models: \ the algorithm and the data's geometry matter, \ not the class", font_size=26, color=CLASSC),
            label(r"the open problem: \ a theory of deep learning's generalization as clean as Vapnik's", font_size=26, color=BADC),
            label(r"and the practical rule, \ unchanged: \ estimate the risk on data you did not use", font_size=26, color=BOUNDC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Where learning theory stands. <bookmark mark='b'/> In classical regimes, VC dimension, "
            "Rademacher complexity, margins, PAC-Bayes and stability give sharp and useful guarantees. <bookmark mark='c'/> "
            "For heavily overparameterized models, what matters is the algorithm's implicit bias and the geometry of the data, "
            "not the size of the class. <bookmark mark='d'/> A theory of deep learning's generalization as clean as "
            "Vapnik's remains open. <bookmark mark='e'/> And the practical rule is unchanged by any of it: estimate the risk "
            "on data you did not use to choose, as the Board showed in chapter two."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
