from __future__ import annotations

import numpy as np

from videos.stats.stats43.common import *  # noqa: F403


class RandomVariables(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.digits()
        self.everything()
        self.quantile()
        self.information()

    def card(self):
        card = chapter_card(2, r"Random variables as measurable maps", r"What is $X$, \ really?", lit=(1909,), part=PART)
        with self.voiceover("Chapter two. What is a random variable, really?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"X", r":", r"\Omega \to \mathbb R \ \text{ with } \ X^{-1}(B) = \{\omega : X(\omega) \in B\} \in \mathcal F \ \ \forall B \in \mathcal B", font_size=30),
            cmath(r"\text{enough}", r":", r"\{X \le x\} \in \mathcal F \ \ \forall x \ \ (\pi\text{--}\lambda \text{ again})", font_size=30),
            cmath(r"\mu_X(B)", r"=", r"P(X^{-1}(B)) = P \circ X^{-1}: \ \text{the law, a push-forward}", font_size=32),
            cmath(r"E\, g(X)", r"=", r"\textstyle\int_\Omega g(X(\omega))\, dP(\omega) = \int_{\mathbb R} g(x)\, d\mu_X(x)", font_size=32),
        ]
        rows[2][-1].set_color(LAWC)
        whys = [why(r"measurable"), why(r"a generating class suffices"), why(r"the distribution"), why(r"change of variables")]
        with self.voiceover(
            "<bookmark mark='a'/> A random variable is neither random nor a variable. It is a function from outcomes "
            "to numbers, with one requirement: for every Borel set B, the outcomes it sends into B form an event. "
            "That is what measurable means. <bookmark mark='b'/> By the pi–lambda theorem it is enough to check the "
            "half-lines. <bookmark mark='c'/> Its law is the measure it pushes forward onto the line: the probability"
            " of B is the probability of the outcomes landing in B. <bookmark mark='d'/> And every expectation can be"
            " computed either on the outcome space or on the line, against the law. This is why statistics can forget"
            " about omega: expectations of measurable functions of X are determined by its law. Dependence between "
            "observations requires their joint law, not just their marginal distributions."
        ) as vo:
            heading=label('A real random variable is a measurable map',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def digits(self):
        d = load("digits")
        L, x0 = 9.0, -5.6
        rows = VGroup()
        for j in range(4):
            y = 2.0 - 0.75 * j
            segs = VGroup()
            for i in range(2 ** (j + 1)):
                a, b = i / 2 ** (j + 1), (i + 1) / 2 ** (j + 1)
                on = i % 2 == 1
                segs.add(Rectangle(width=(b - a) * L * 0.98, height=0.36, stroke_width=0, fill_color=LAWC if on else GREY_E,
                                   fill_opacity=0.9 if on else 0.6).move_to([x0 + (a + b) / 2 * L, y, 0]))
            tag = label(rf"digit {j + 1}", font_size=22, color=GREY_A).next_to(segs, LEFT, buff=0.25)
            rows.add(VGroup(segs, tag))
        ax0 = VGroup(label(r"$0$", font_size=22, color=GREY_B).move_to([x0, -1.0, 0]),
                     label(r"$1$", font_size=22, color=GREY_B).move_to([x0 + L, -1.0, 0]),
                     label(r"$\omega$ \ uniform on $[0, 1)$", font_size=22, color=GREY_A).move_to([x0 + L / 2, -1.0, 0]))
        side = fit_rows(VGroup(
            label(rf"20,000 uniforms: \ digit shares {min(d['share']):.3f}--{max(d['share']):.3f}", font_size=22, color=LAWC),
            label(rf"correlation of digits 1 and 2: \ ${d['corr01']:.3f}$", font_size=22, color=GREY_A),
            label(rf"three 1s in a row: \ {d['three_heads']:.3f} \ (1/8 = 0.125)", font_size=22, color=GREY_A),
        ), 12.4, 0.3, [0, -2.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is the most useful probability space of all: the unit interval with length as "
            f"probability. Write a point omega in binary. Its first digit is one on the right half, <bookmark mark='b'/> its "
            f"second on the right half of each half, <bookmark mark='c'/> and so on: each digit is one on exactly half the "
            f"interval, and the digits are independent, because each pattern of the first k digits picks out an interval of "
            f"length two to the minus k. Émile Borel noticed in 1909 that the binary digits of a uniform number are "
            f"independent fair coins. <bookmark mark='d'/> Twenty thousand uniforms bear it out: each digit is one about half "
            f"the time, neighbouring digits are uncorrelated, and three ones in a row turn up "
            f"{100 * d['three_heads']:.1f} percent of the time, against an eighth."
        ) as vo:
            self.play(FadeIn(ax0))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(side))
        self.clear_scene()

    def everything(self):
        rows = fit_rows(VGroup(
            label(r"one uniform $\omega$ \ $\to$ \ infinitely many fair coins \ (its digits)", font_size=26, color=LAWC),
            label(r"deal the coins into infinitely many columns \ $\to$ \ infinitely many independent uniforms", font_size=26),
            label(r"apply $F^{-1}$ to each \ $\to$ \ an i.i.d.\ sequence from any law $F$", font_size=26),
            label(r"so every limit theorem for i.i.d.\ sequences is a theorem about $([0, 1), \mathcal B, \lambda)$", font_size=26, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> An ideal real uniform number supplies infinitely many fair binary digits, up to the"
            " null set with ambiguous expansions. A finite-precision computer draw has only finitely many random "
            "bits. <bookmark mark='b'/> Deal its digits into infinitely many columns, the first digit to column one, "
            "the second to column two, the third back to column one, in a diagonal pattern, and each column's digits "
            "form a new uniform number, all of them independent. <bookmark mark='c'/> Apply the quantile function F "
            "inverse to each, and you have an independent sequence from any law you like. <bookmark mark='d'/> So the"
            " strong law, the central limit theorem and everything else in this part are theorems about the unit "
            "interval and its length. Infinite sequences of independent variables exist; chapter four gives the "
            "general reason."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def quantile(self):
        d = load("digits")
        A = axes([0, 1], [0, 1.3], x_length=3.6, y_length=3.0, xlabel=r"$U$", ylabel=r"density", xticks=[0, 1], yticks=[0, 1],
                 center=[-4.6, 0.0, 0])
        B = axes([0, 6], [0, 1.0], x_length=4.6, y_length=3.0, xlabel=r"$X = F^{-1}(U) = -\log(1 - U)$", ylabel=r"density",
                 xticks=[0, 2, 4, 6], yticks=[0, 0.5, 1], center=[2.8, 0.0, 0])
        a, b = A.ax, B.ax
        flat = Rectangle(width=a.c2p(1, 0)[0] - a.c2p(0, 0)[0], height=a.c2p(0, 1)[1] - a.c2p(0, 0)[1], stroke_width=0,
                         fill_color=LAWC, fill_opacity=0.6).move_to(a.c2p(0.5, 0.5))
        h, e = np.asarray(d["exp_hist"]), np.asarray(d["exp_edges"])
        bars = bars_at(b, (e[:-1] + e[1:]) / 2, h, e[1] - e[0], LAWC, opacity=0.7)
        xs = np.linspace(0, 6, 200)
        lim = curve(b, xs, np.exp(-xs), LIMC, 3)
        arrow = Arrow([-2.4, 0.3, 0], [-0.4, 0.3, 0], color=S.ACCENT, stroke_width=4)
        side = fit_rows(VGroup(
            label(r"$P(F^{-1}(U) \le x) = P(U \le F(x)) = F(x)$", font_size=26, color=S.ACCENT),
            label(r"the law of $X$ is Lebesgue measure pushed through $F^{-1}$: \ Part 7's inverse-CDF sampler", font_size=22, color=GREY_A),
        ), 12.4, 0.3, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The last step is the quantile transform. Start with uniform probability on the interval. "
            "<bookmark mark='b'/> Push it through F inverse, here minus the log of one minus u, <bookmark mark='c'/> and "
            "what arrives is the exponential law. <bookmark mark='d'/> The proof is one line: F inverse of U is at most x "
            "exactly when U is at most F of x, which has probability F of x. It is Part seven's inverse-CDF sampler, seen "
            "as a push-forward of measure, and chapter seven will use it again to turn convergence of laws into convergence "
            "of random variables."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(flat))
            vo.wait_until("b")
            self.play(GrowArrow(arrow))
            vo.wait_until("c")
            self.play(FadeIn(bars), Create(lim))
            vo.wait_until("d")
            self.play(FadeIn(side))
        self.clear_scene()

    def information(self):
        rows = [
            cmath(r"\sigma(X)", r"=", r"\{X^{-1}(B) : B \in \mathcal B\}: \ \text{the events that } X \text{ decides}", font_size=32),
            cmath(r"\text{Doob--Dynkin}", r":", r"Y \text{ is } \sigma(X)\text{-measurable} \iff Y = g(X) \text{ for a Borel } g", font_size=30),
            cmath(r"\mathcal F_n", r"=", r"\sigma(X_1, \ldots, X_n) \subseteq \mathcal F_{n+1}: \ \text{information growing}", font_size=32),
            cmath(r"T(X_1, \ldots, X_n)", r":", r"\text{a statistic; \ sufficient: \ } \sigma(T) \text{ keeps all about } \theta", font_size=30),
        ]
        rows[0][-1].set_color(LAWC)
        whys = [why(r"generated $\sigma$-algebra"), why(r"functions of $X$"), why(r"a filtration: \ Part 44"), why(r"Part 45")]
        with self.voiceover(
            "<bookmark mark='a'/> Sigma-algebras also measure information. The sigma-algebra generated by X is the set of "
            "events whose occurrence you can decide by looking at X. <bookmark mark='b'/> The Doob–Dynkin lemma makes it "
            "exact: a random variable is determined by that information precisely when it is a function of X. <bookmark "
            "mark='c'/> Watching a sequence, the information grows: each sigma-algebra contains the last, a filtration, the "
            "setting of martingales in Part forty-four. <bookmark mark='d'/> And a statistic is just a measurable function "
            "of the data; sufficiency, in Part forty-five, will be the statement that its sigma-algebra keeps everything "
            "the data say about the parameter."
        ) as vo:
            heading=label('Generated sigma-algebras record observable information',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
