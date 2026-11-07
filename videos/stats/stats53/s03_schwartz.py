from __future__ import annotations

import numpy as np

from videos.stats.stats53.common import *  # noqa: F403


class Schwartz(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.kl()
        self.chart()
        self.sieves()
        self.tests()

    def card(self):
        card = chapter_card(2, r"Schwartz's theorem", r"Which truths can a prior learn?", lit=(1965,), part=PART)
        with self.voiceover("Chapter two. Schwartz's theorem: which truths can a prior learn?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\text{KL support}", r":", r"\Pi\big(p: \mathrm{KL}(p_0, p) < \varepsilon\big) > 0 \ \text{ for every } \varepsilon > 0", font_size=32),
            cmath(r"\text{tests}", r":", r"\phi_n \text{ for } p_0 \text{ against } U^c \text{ with errors } \to 0 \text{ exponentially}", font_size=30),
            cmath(r"\text{Schwartz (1965)}", r":", r"\Pi(U \mid X_{1:n}) \to 1 \ \ p_0\text{-a.s.}", font_size=34),
            cmath(r"\text{read}", r":", r"\text{prior mass near the truth, \ and separability}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"prior mass near the truth"), why(r"identifiability, \ uniformly"), why(r"for the fixed truth $p_0$"), why(r"two ingredients")]
        heading = label('Posterior convergence requires both local and global model conditions', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Lorraine Schwartz's theorem of 1965 is about a fixed truth p zero. The first condition: the prior puts positive mass on every Kullback–Leibler neighbourhood of the truth, however small. <bookmark mark='b'/> In an i.i.d. dominated model, a sufficient testing condition is: for each chosen neighbourhood U of the truth, there are tests that distinguish the truth from everything outside U, with errors that vanish exponentially fast. <bookmark mark='c'/> Then the posterior mass of U tends to one, almost surely under the truth. <bookmark mark='d'/> Two ingredients, then: enough prior mass near the truth, and a model in which the truth can be told apart from the alternatives. Every consistency and rate theorem since is built from these two."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def kl(self):
        rows = [
            cmath(r"\Pi(U^c \mid X)", r"=", r"\frac{\int_{U^c} \prod_i \frac{p}{p_0}(X_i)\, d\Pi(p)}{\int \prod_i \frac{p}{p_0}(X_i)\, d\Pi(p)}", font_size=32),
            cmath(r"\text{denominator}", r"\ge", r"e^{-n(\varepsilon + o(1))}: \ \text{from KL support}", font_size=34),
            cmath(r"(1-\phi_n)\times\text{numerator}", r"\;", r"\text{has exponentially small expectation; type-I error controlled}", font_size=34),
            cmath(r"\text{ratio}", r"\to", r"0, \ \text{exponentially}", font_size=36),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Bayes' formula, \ as likelihood ratios"), why(r"the law of large numbers"), why(r"Markov's inequality"), why(r"the proof")]
        heading = label('Tests control a weighted numerator, while prior mass controls the denominator', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Why it works. Write the posterior mass outside U as a ratio of integrals of likelihood ratios against the truth. <bookmark mark='b'/> The denominator cannot be too small: the prior has mass near the truth, where the likelihood ratio decays at most like e to the minus n epsilon, by the law of large numbers applied to the log ratio. <bookmark mark='c'/> Multiply the numerator by one minus the test. Uniform type-two error controls the expectation of this test-weighted integral; small type-one error controls the event where the test rejects. The raw numerator need not itself have exponentially small expectation. <bookmark mark='d'/> Choose epsilon below c and the ratio vanishes exponentially."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("schwartz")
        th = np.asarray(d["theta"])
        top = np.log10(1 + max(max(v["good"]) for v in d["post"].values()) + max(max(v["bad"]) for v in d["post"].values())) + .08
        A = axes([-1.5, 3.2], [0, top], x_length=7.4, y_length=4.4, xlabel=r"$\theta$ \ (the truth is $\theta_0 = 0$)", ylabel=r"$\log_{10}(1+\mathrm{density})$",
                 xticks=[-1, 0, 1, 2, 3], yticks=[0, 1, 2, 3], center=[-2.5, 0.2, 0])
        ax = A.ax
        g = {k: clip_curve(ax, th, np.log10(1+np.asarray(v["good"])), POSTC, 3 + i, ymin=0, ymax=top) for i, (k, v) in enumerate(d["post"].items())}
        b = {k: clip_curve(ax, th, np.log10(1+np.asarray(v["bad"])), BADC, 3 + i, ymin=0, ymax=top) for i, (k, v) in enumerate(d["post"].items())}
        supp = Rectangle(width=ax.c2p(3, 0)[0] - ax.c2p(1, 0)[0], height=0.18, fill_color=PRIORC, fill_opacity=0.5, stroke_width=0).move_to(ax.c2p(2, 0.3))
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, top), color=TRUTHC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"$X_i \sim N(\theta_0, 1)$, \ $\theta_0 = 0$; \ $n = 10, \ 100, \ 1{,}000$", font_size=22),
            label(r"blue: \ prior $N(0, 10)$: \ KL support everywhere", font_size=22, color=POSTC),
            label(r"purple bar: \ a second prior, \ Uniform$[1, 3]$", font_size=22, color=PRIORC),
            label(rf"red: \ its posterior piles up at 1: \ mean {d['post']['1000']['bad_mean']:.3f} at $n = 1{{,}}000$", font_size=22, color=BADC),
            label(r"no prior mass near the truth, \ no consistency", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The simplest illustration. Normal observations with true mean zero, at ten, a hundred and "
            f"a thousand observations. <bookmark mark='b'/> With a wide normal prior, which puts mass in every neighbourhood "
            f"of zero, the posteriors in blue concentrate at zero. <bookmark mark='c'/> Now a second prior, uniform on one to "
            f"three, which excludes the truth. <bookmark mark='d'/> Its posteriors, in red, pile up against the boundary at "
            f"one, the point of the support closest to the truth in Kullback–Leibler divergence, with posterior mean "
            f"{say(d['post']['1000']['bad_mean'], 3)} at a thousand observations. <bookmark mark='e'/> They become ever more "
            f"confident in the wrong answer. Schwartz's first condition is not a technicality."
        ) as vo:
            self.play(FadeIn(A), FadeIn(zero), FadeIn(exact_tag(r"exact posteriors")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[Create(v) for v in g.values()], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(supp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(*[Create(v) for v in b.values()], FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def sieves(self):
        rows = [
            cmath(r"\text{when tests are hard to build}", r":", r"\text{split the model into a sieve } \mathcal P_n \text{ and the rest}", font_size=32),
            cmath(r"\log N(\varepsilon, \mathcal P_n)", r"\le", r"c\, n\varepsilon^2: \ \text{small enough to test}", font_size=34),
            cmath(r"\Pi(\mathcal P_n^c)", r"\le", r"e^{-\beta n}: \ \text{the rest has exponentially small prior mass}", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\text{consistency in Hellinger distance}", font_size=34),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Barron, \ Schervish \& Wasserman (1999)"), why(r"Part 48's entropy"), why(r"the prior's tails"), why(r"for densities")]
        heading = label('A sieve balances testing complexity against prior mass outside it', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> For densities, tests against everything outside a neighbourhood can be hard to build directly. Andrew Barron, Mark Schervish and Larry Wasserman's way around it, in 1999, splits the model into a sieve and the rest. <bookmark mark='b'/> On the sieve, the covering numbers must grow at most exponentially in n, slowly enough that tests exist, by the entropy arguments of Part forty-eight. <bookmark mark='c'/> Off it, the prior's mass must be exponentially small, so the posterior can ignore it. <bookmark mark='d'/> Then the posterior is consistent in Hellinger distance. The same split, made quantitative, is the next chapter's theorem."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tests(self):
        rows = fit_rows(VGroup(
            label(r"where the conditions come from in practice:", font_size=28, color=GREY_A),
            label(r"KL support: \ a Dirichlet-process mixture of normals has it for most smooth densities", font_size=26, color=POSTC),
            label(r"tests: \ exist when the model is not too large, \ measured by entropy (Part 48)", font_size=26, color=FREQC),
            label(r"a direct DP lacks KL support at densities; \ weak consistency can still hold", font_size=26, color=BADC),
            label(r"next: \ the same two ingredients, \ quantified, \ give rates", font_size=26, color=GOODC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Where the conditions come from in practice. <bookmark mark='b'/> Kullback–Leibler support holds for Dirichlet-process mixtures of normals at most smooth densities, as Subhashis Ghosal, Jayanta Ghosh and R. V. Ramamoorthi showed in 1999. <bookmark mark='c'/> Tests exist when the model is not too large, measured by the entropy of Part forty-eight. <bookmark mark='d'/> And A Dirichlet process draws discrete distributions, so a continuous truth is not in its KL support as a prior directly on sampling distributions. KL support is sufficient, not necessary for every mode of consistency: DP posterior CDFs can still be weakly consistent. The location counterexample needs its own model-specific argument. <bookmark mark='e'/> Next, the same two ingredients, quantified, give rates."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
