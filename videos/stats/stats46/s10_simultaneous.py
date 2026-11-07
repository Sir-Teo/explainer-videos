from __future__ import annotations

import itertools

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class Simultaneous(VoiceoverScene):
    def construct(self):
        self.card()
        self.scheffe()
        self.multipliers()
        self.closed()
        self.lattice()
        self.beyond()

    def card(self):
        card = chapter_card(9, r"Simultaneous inference", r"Many intervals, \ one promise", lit=(1953, 1976), part=PART)
        with self.voiceover("Chapter nine. Simultaneous inference: many intervals, one promise."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def scheffe(self):
        rows = [
            cmath(r"\hat\theta \sim N_k(\theta, \Sigma)", r":", r"\text{intervals for every } c^\top\theta \text{ at once}", font_size=32),
            cmath(r"\sup_c \frac{(c^\top(\hat\theta - \theta))^2}{c^\top \Sigma c}", r"=", r"(\hat\theta - \theta)^\top \Sigma^{-1} (\hat\theta - \theta) \sim \chi^2_k", font_size=30),
            cmath(r"c^\top\hat\theta", r"\pm", r"\sqrt{\chi^2_{k, 1-\alpha}}\, \sqrt{c^\top \Sigma c} \ \ \text{for all } c, \ \text{jointly}", font_size=32),
            cmath(r"\text{independent residual }\chi^2_\nu\text{ scale estimate}", r":", r"\sqrt{k F_{k, \nu}} \ \text{in place of } \sqrt{\chi^2_k}", font_size=32),
        ]
        rows[2][-1].set_color(UMPC)
        whys = [why(r"infinitely many contrasts"), why(r"Cauchy--Schwarz"), why(r"Scheff\'e (1953)"), why(r"the ANOVA version")]
        with self.voiceover(
            "<bookmark mark='a'/> Henry Scheffé asked for intervals for every linear combination of k parameters at "
            "once, infinitely many, with one joint guarantee. <bookmark mark='b'/> The worst combination, by "
            "Cauchy–Schwarz, turns the supremum into the quadratic form of the estimation error, which is chi-square "
            "with k degrees of freedom. <bookmark mark='c'/> So the intervals estimate plus or minus the root of the "
            "chi-square quantile times each combination's standard error hold simultaneously with probability one "
            "minus alpha. <bookmark mark='d'/> For the normal linear model with an independent chi-square residual "
            "estimate of a common variance, the multiplier becomes the root of k times the appropriate F quantile. An"
            " arbitrary covariance estimate does not give this exact law. The intervals are the projections of the "
            "confidence ellipsoid for theta onto every direction."
        ) as vo:
            heading=label('A normal confidence ellipsoid covers all linear contrasts',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def multipliers(self):
        d = load("simul")
        rows = [[r"$k$"] + [str(k) for k in d["ks"]],
                [r"Scheff\'e, \ every contrast"] + [f"{v:.2f}" for v in d["scheffe"]],
                [r"Bonferroni, \ $k$ intervals"] + [f"{v:.2f}" for v in d["bonf"]]]
        tab = table_rows(rows, font_size=30, col_buff=0.8, row_buff=0.35, colors=[GREY_A, UMPC, CIC]).move_to([0, 0.8, 0])
        note_ = fit_rows(VGroup(
            label(r"multipliers of the standard error, \ 95\% jointly, \ $\sigma$ known", font_size=24, color=GREY_A),
            label(r"for $k$ pre-chosen intervals, \ Bonferroni is shorter; \ for contrasts chosen after looking, \ Scheff\'e", font_size=24, color=S.ACCENT),
        ), 12.4, 0.25, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The price, as a multiplier of the standard error. <bookmark mark='b'/> Scheffé's grows like "
            "the root of k: two point four five for two parameters, five point six for twenty. <bookmark mark='c'/> "
            "Bonferroni's, for exactly k intervals chosen in advance, grows only like the root of the log of k: three point "
            "zero two for twenty. <bookmark mark='d'/> So for a fixed list of comparisons Bonferroni wins; Scheffé's "
            "advantage is that it covers every contrast, including the ones you only thought of after looking at the data."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(note_[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(note_[1]))
        self.clear_scene()

    def closed(self):
        rows = [
            cmath(r"H_S = \textstyle\bigcap_{i \in S} H_i", r":", r"\text{every intersection, \ with a level-}\alpha \text{ local test}", font_size=30),
            cmath(r"\text{reject } H_i", r"\iff", r"\text{every } H_S \text{ with } i \in S \text{ is rejected locally}", font_size=32),
            cmath(r"\text{FWER}", r"\le", r"\alpha: \ \text{a false rejection needs } H_{T} \text{ rejected, } T = \text{the true nulls}", font_size=30),
            cmath(r"\text{local Bonferroni}", r"\Rightarrow", r"\text{Holm (1979); \ \ local Simes} \Rightarrow \text{Hommel, with valid intersection dependence}", font_size=30),
        ]
        rows[2][-1].set_color(UMPC)
        whys = [why(r"all $2^m - 1$ of them"), why(r"Marcus, \ Peritz \& Gabriel (1976)"), why(r"one test guards them all"), why(r"Part 33's procedures, \ explained")]
        with self.voiceover(
            "<bookmark mark='a'/> For a finite family of hypotheses there is a general principle. Form every "
            "intersection of them, and give each a level-alpha test of its own. <bookmark mark='b'/> Reject an "
            "individual hypothesis only if every intersection containing it is rejected: the closed testing principle"
            " of Ruth Marcus, Eric Peritz and Ruben Gabriel, 1976. <bookmark mark='c'/> The proof is one line. A "
            "false rejection requires rejecting the intersection of the true nulls, and that happens with probability"
            " at most alpha. <bookmark mark='d'/> With Bonferroni as the local test, closed testing is Holm's "
            "procedure; with Simes's test, it is Hommel's, provided each intersection satisfies the conditions making"
            " Simes valid, such as independent null p-values or the required positive regression dependence. Holm is "
            "step-down; Hommel uses a different shortcut through the closure."
        ) as vo:
            heading=label('One valid intersection test guards every false rejection',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lattice(self):
        d = load("simul")
        p = np.asarray(d["p"])
        m = len(p)

        def rej(S, local):
            ps = np.sort(p[list(S)])
            if local == "bonferroni":
                return ps[0] <= 0.05 / len(S)
            return bool(np.any(ps <= 0.05 * np.arange(1, len(S) + 1) / len(S)))

        layers = [list(itertools.combinations(range(m), r)) for r in range(m, 0, -1)]
        boxes = {}
        g = VGroup()
        for li, layer in enumerate(layers):
            row = VGroup()
            for S in layer:
                t = label("".join(str(i + 1) for i in S), font_size=24)
                b = SurroundingRectangle(t, buff=0.12, corner_radius=0.06, color=GREY_B, stroke_width=2)
                row.add(VGroup(b, t))
                boxes[S] = row[-1]
            row.arrange(RIGHT, buff=0.35)
            g.add(row)
        g.arrange(DOWN, buff=0.45).move_to([-2.4, 0.3, 0])
        side = fit_rows(VGroup(
            label(r"$p = 0.011, \ 0.018, \ 0.024, \ 0.040$", font_size=22),
            label(r"the 15 intersections of $H_1, \ldots, H_4$", font_size=22, color=GREY_A),
            label(r"local Bonferroni: \ red = rejected; \ only $H_1$ is rejected by closure", font_size=22, color=REJC),
            label(r"local Simes: \ every intersection rejected: \ all four", font_size=22, color=UMPC),
            label(r"Bonferroni alone: \ only $H_1$ \ ($0.011 < 0.0125$)", font_size=22, color=CIC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        bon = lambda: [boxes[S][0].animate.set_fill(REJC, opacity=0.5) for S in boxes if rej(S, "bonferroni")]  # noqa: E731
        sim = lambda: [boxes[S][0].animate.set_fill(UMPC, opacity=0.5) for S in boxes if rej(S, "simes")]  # noqa: E731
        with self.voiceover(
            "<bookmark mark='a'/> An example with four p-values: point zero one one, point zero one eight, point zero"
            " two four and point zero four. <bookmark mark='b'/> Here are the fifteen intersections, from all four at"
            " the top down to the single hypotheses. <bookmark mark='c'/> With Bonferroni locally, the intersections "
            "rejected are shaded red; only the first hypothesis has every intersection above it rejected. <bookmark "
            "mark='d'/> With Simes's test locally, every intersection is rejected, because the p-values are all small"
            " together, and Hommel's procedure rejects all four. <bookmark mark='e'/> Plain Bonferroni would also "
            "stop at the first. Every local test must actually control its level under its intersection null. "
            "Bonferroni allows arbitrary dependence; the Simes version needs the stated dependence assumptions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*bon(), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(*sim(), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def beyond(self):
        rows = fit_rows(VGroup(
            label(r"the partitioning principle: \ test disjoint pieces of $\Theta$, \ each at level $\alpha$ \ (Finner \& Strassburger 2002)", font_size=24),
            label(r"it yields confidence sets for the \emph{direction} of each effect, \ not just rejections", font_size=24, color=UMPC),
            label(r"gatekeeping and graphical procedures: \ closed testing with a hierarchy \ (Bretz et al.\ 2009)", font_size=24, color=GREY_A),
            label(r"the FDR of Part 33 is a different promise: \ a proportion, \ not a probability", font_size=24, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two refinements. The partitioning principle of Helmut Finner and Klaus Strassburger tests "
            "disjoint pieces of the parameter space, each at level alpha, <bookmark mark='b'/> and so yields confidence "
            "statements about the direction of each effect, not merely rejections. <bookmark mark='c'/> And the gatekeeping "
            "and graphical procedures used in clinical trials are closed tests with a hierarchy built in. <bookmark "
            "mark='d'/> The false discovery rate of Part thirty-three is a different promise altogether: a bound on the "
            "expected proportion of errors, not on the probability of any."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
