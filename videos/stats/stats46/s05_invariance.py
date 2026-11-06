from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class Invariance(VoiceoverScene):
    def construct(self):
        self.card()
        self.groups()
        self.ttest()
        self.power()
        self.huntstein()
        self.ftest()

    def card(self):
        card = chapter_card(4, r"Invariance", r"Tests that respect the symmetry of the problem", part=PART)
        with self.voiceover("Chapter four. Invariance: tests that respect the symmetry of the problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def groups(self):
        rows = [
            cmath(r"g \in G", r":", r"\text{acts on the data and the parameter, \ preserving } H_0 \text{ and } H_1", font_size=30),
            cmath(r"\phi \text{ invariant}", r":", r"\phi(gx) = \phi(x) \ \ \forall g", font_size=34),
            cmath(r"M \text{ maximal invariant}", r":", r"M(x) = M(y) \iff y = gx \text{ for some } g", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\phi = \psi(M), \ \ \text{and the law of } M \text{ depends on } \theta \text{ only through } \gamma(\theta)", font_size=28),
        ]
        rows[3][-1].set_color(UMPC)
        whys = [why(r"e.g.\ change of units"), why(r"the conclusion should not change"), why(r"what is left after the symmetry"), why(r"a smaller problem")]
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-five's equivariance, for tests. A group of transformations, such as changes of "
            "units, acts on the data and the parameter and maps the null and the alternative to themselves. <bookmark "
            "mark='b'/> A test is invariant if it gives the same answer for transformed data. <bookmark mark='c'/> A "
            "maximal invariant is a statistic that is constant on each orbit of the group and different on different "
            "orbits: everything the symmetry leaves. <bookmark mark='d'/> Invariant tests are exactly the functions of the "
            "maximal invariant, and its distribution depends on theta only through the parameter's own maximal invariant. "
            "The problem shrinks, often to one dimension, where chapter two's theory may apply."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ttest(self):
        rows = [
            cmath(r"x_i \sim N(\mu, \sigma^2)", r",", r"\ H_0: \mu \le 0 \ \text{vs} \ \mu > 0", font_size=32),
            cmath(r"G", r"=", r"\{x \mapsto c x, \ c > 0\}: \ \text{change of scale}", font_size=34),
            cmath(r"\text{maximal invariant}", r":", r"t = \sqrt n\, \bar x / s, \ \ \text{law } t_{n-1}(\delta), \ \delta = \sqrt n\, \mu/\sigma", font_size=30),
            cmath(r"t_{n-1}(\delta) \text{ has MLR in } t", r"\Rightarrow", r"\text{the one-sided } t \text{ test is UMP invariant}", font_size=30),
        ]
        rows[3][-1].set_color(UMPC)
        whys = [why(r"sufficient: \ $(\bar x, s)$"), why(r"the units of measurement"), why(r"the noncentral $t$"), why(r"Karlin--Rubin, \ again")]
        with self.voiceover(
            "<bookmark mark='a'/> The t test again. Normal data, testing whether the mean is positive. <bookmark mark='b'/> "
            "Changing the units multiplies every observation by a positive constant and leaves the hypotheses alone. "
            "<bookmark mark='c'/> After reducing to the sufficient statistics, the maximal invariant is Student's t, whose "
            "distribution is the noncentral t with noncentrality root n mu over sigma. <bookmark mark='d'/> That family has "
            "a monotone likelihood ratio, so by Karlin and Rubin the one-sided t test is uniformly most powerful among "
            "scale-invariant tests. Unbiasedness and invariance arrive at the same answer."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def power(self):
        d = load("invariance")
        dl = np.asarray(d["delta"])
        A = axes([0, 1.5], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"$\mu/\sigma$", ylabel=rf"power, \ $n = {d['n']}$, \ 5\%",
                 xticks=[0, 0.5, 1, 1.5], yticks=[0, 0.05, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cz = polyline(ax, dl, d["z"], GREY_B, 3)
        ct = polyline(ax, dl, d["t"], UMPC, 4)
        cs = polyline(ax, dl, d["sign"], S.PRIOR, 4)
        z, t, s = d["at05"]
        side = fit_rows(VGroup(
            label(r"grey: \ the $z$ test, \ $\sigma$ known: \ an upper bound", font_size=22, color=GREY_B),
            label(r"green: \ the $t$ test, \ UMP among invariant tests", font_size=22, color=UMPC),
            label(r"purple: \ the sign test: \ invariant, \ wasteful", font_size=22, color=S.PRIOR),
            label(rf"at $\mu/\sigma = 0.5$: \ {z:.2f}, \ {t:.2f}, \ {s:.2f}", font_size=22, color=S.ACCENT),
            label(r"the gap $z$--$t$: \ the price of not knowing $\sigma$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Exact power curves for ten normal observations. In grey, the z test that knows sigma: no "
            f"test that does not know sigma can beat it. <bookmark mark='b'/> In green, the t test, the best among tests "
            f"invariant to the units. <bookmark mark='c'/> In purple, the sign test, also invariant, but throwing away the "
            f"sizes of the observations. <bookmark mark='d'/> At a mean of half a standard deviation the powers are "
            f"{say(z, 2)}, {say(t, 2)} and {say(s, 2)}. <bookmark mark='e'/> The gap between grey and green is what ignorance "
            f"of sigma costs; the gap below green is waste."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ noncentral $t$, \ binomial")))
            vo.wait_until("a")
            self.play(Create(cz), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ct), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def huntstein(self):
        rows = fit_rows(VGroup(
            label(r"why should we restrict to invariant tests at all?", font_size=28),
            label(r"Hunt--Stein (1946): \ if the group is amenable \ (it has invariant means),", font_size=26, color=GREY_A),
            label(r"the best invariant test is minimax among \emph{all} tests", font_size=28, color=UMPC),
            label(r"amenable: \ translations, \ scalings, \ the affine group, \ compact groups", font_size=26, color=GREY_A),
            label(r"not amenable: \ $GL(p)$: \ Stein's example, \ where an invariant test is beaten by a non-invariant one", font_size=24, color=REJC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> But why should a statistician restrict attention to invariant tests? <bookmark mark='b'/> "
            "Gilbert Hunt and Charles Stein answered in 1946, in a famous unpublished paper: if the group is amenable, "
            "meaning roughly that it admits averages that are themselves invariant, <bookmark mark='c'/> then the best "
            "invariant test is minimax among all tests, invariant or not. Nothing is lost in the worst case by respecting "
            "the symmetry. <bookmark mark='d'/> Translations, scalings, the affine group and compact groups are all "
            "amenable. <bookmark mark='e'/> The general linear group is not, and Stein constructed a covariance testing "
            "problem in which the best invariant test is beaten by a non-invariant one: symmetry can be a trap."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ftest(self):
        rows = [
            cmath(r"y = X\beta + \varepsilon", r",", r"\ H_0: \beta_2 = 0, \ \ \sigma \text{ unknown}", font_size=32),
            cmath(r"G", r":", r"\text{rotations in the error space, \ shifts in } X_1\text{'s span, \ scalings}", font_size=30),
            cmath(r"\text{maximal invariant}", r":", r"F = \tfrac{(\mathrm{RSS}_0 - \mathrm{RSS}_1)/q}{\mathrm{RSS}_1/(n - p)} \sim F_{q, n-p}(\lambda)", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"\text{the } F \text{ test is UMP invariant; \ also most stringent}", font_size=32),
        ]
        rows[3][-1].set_color(UMPC)
        whys = [why(r"Part 23's linear hypothesis"), why(r"the problem's symmetries"), why(r"noncentral $F$ has MLR in $\lambda$"), why(r"Wald (1942); \ Hsu (1941)")]
        with self.voiceover(
            "<bookmark mark='a'/> The same idea settles Part twenty-three's general linear hypothesis. Test that a block of "
            "regression coefficients is zero, with the error variance unknown. <bookmark mark='b'/> The problem is "
            "unchanged by rotations of the residual space, shifts within the span of the nuisance columns, and changes of "
            "scale. <bookmark mark='c'/> The maximal invariant is the F statistic, with a noncentral F distribution that "
            "has a monotone likelihood ratio in its noncentrality. <bookmark mark='d'/> So the F test is uniformly most "
            "powerful among invariant tests, as P. L. Hsu showed in 1941, and Wald showed it is most stringent: its "
            "largest shortfall from the best possible power is the smallest."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
