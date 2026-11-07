from __future__ import annotations

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class Paired(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter two. Paired comparisons, power, and the leaderboard's winner's curse.", 2,
                            r"Paired comparisons", r"Same questions, \ correlated errors")
        self.pairing()
        self.mcnemar_()
        self.board()
        self.power()
        self.curse()
        self.multiplicity()

    def pairing(self):
        d = load("paired")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Two models answer the same questions, so their scores are not independent samples. "
            f"Hard questions are hard for both. <bookmark mark='b'/> The variance of the difference in means is the sum of "
            f"the two variances minus twice their covariance. <bookmark mark='c'/> The unpaired interval ignores the "
            f"covariance. With positively correlated errors, here a correlation of {d['corr']:.2f} between the two models' "
            f"right-or-wrong scores, it is too wide. <bookmark mark='d'/> The paired interval works with the per-question "
            f"differences directly: their standard deviation over root n. It is Part ten's paired t, and Part thirteen's "
            f"blocking, with questions as blocks.",
            [(r"\mathrm{Var}(\bar a - \bar b)", r"=", r"\frac{\sigma_a^2 + \sigma_b^2 - 2\sigma_{ab}}{n}", 40),
             (r"\text{unpaired}", r":", r"\text{drops } -2\sigma_{ab}", 40),
             (r"\text{correlation}", r":", rf"{d['corr']:.2f} \ \Rightarrow \ \text{{too wide}}", 40),
             (r"\text{paired}", r":", r"\mathrm{sd}(a_i - b_i)/\sqrt{n}", 40)],
            [r"a covariance", r"independent-samples", r"shared difficulty", r"Parts 10 and 13"],
            colors=[(1, NAIVEC), (3, HONC)])

    def mcnemar_(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> For right-or-wrong scores the paired test has a name. <bookmark mark='b'/> Classify each "
            "question: both right, both wrong, only A right, only B right. <bookmark mark='c'/> The questions both get right "
            "or both get wrong say nothing about which is better. Quinn McNemar's test, from 1947, uses only the discordant "
            "ones: under the null, each is equally likely to favour either model. <bookmark mark='d'/> So the count favouring "
            "A, out of the discordant total, is binomial with probability a half, an exact test of Part fourteen.",
            [(r"\text{four cells}", r":", r"n_{11}, \ n_{00}, \ n_{10}, \ n_{01}", 40),
             (r"\text{concordant}", r":", r"\text{no information}", 40),
             (r"H_0", r":", r"n_{10} \mid n_{10} + n_{01} \sim \mathrm{Bin}(n_{10} + n_{01}, \tfrac12)", 40),
             (r"\text{exact}", r":", r"\text{a sign test on discordant pairs}", 40)],
            [r"a 2 x 2 table", r"ties", r"McNemar (1947)", r"Part 14"],
            colors=[(2, HONC)])

    def board(self):
        b = load("board")["rows"]
        show_board(self, board_rows("unpaired interval", "paired interval"),
                   f"<bookmark mark='a'/> On the Board, two correlated models on the same thousand questions: the unpaired "
                   f"interval for their difference covers {100 * b[2]['achieved']:.1f} percent of the time, more than it "
                   f"promised: conservative, and wider than it needs to be. <bookmark mark='b'/> The paired interval covers "
                   f"{100 * b[3]['achieved']:.1f} percent: kept.", [("a", [0]), ("b", [1])])

    def power(self):
        d = load("paired")
        pw = d["power"]
        lx = np.log10([r["n"] for r in pw])
        A = axes([2.3, 4.0], [0, 1], x_length=7.2, y_length=4.3, xlabel=r"benchmark size $n$ (log scale)",
                 ylabel=r"power to detect a 2-point gap at 5\%", xticks=list(np.log10([250, 1000, 4000])),
                 xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.4, 0.2, 0])
        ax = A.ax

        def line(key, color):
            ys = [r[key] for r in pw]
            return VGroup(polyline(ax, lx, ys, color, 3.5), *[Dot(ax.c2p(a, b), radius=0.07, color=color) for a, b in zip(lx, ys)])
        u, p = line("unpaired", NAIVEC), line("paired", HONC)
        r1 = next(r for r in pw if r["n"] == 1000)
        r2 = next(r for r in pw if r["n"] == 2000)
        side = side_groups([
            [(r"86\% against 84\%, \ correlated errors", WHITE), (r"400 simulated benchmarks per $n$", GREY_A)],
            [(rf"red: \ unpaired, \ {100 * r1['unpaired']:.0f}\% at $n = 1{{,}}000$", NAIVEC)],
            [(rf"green: \ paired, \ {100 * r1['paired']:.0f}\% at $n = 1{{,}}000$", HONC), (rf"{100 * r2['paired']:.0f}\% at 2{{,}}000", HONC)],
            [(r"even paired: \ a thousand questions", GREY_A), (r"rarely settle a 2-point gap", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> Power, Part ten's other half. Two models whose true accuracies are 86 and 84 percent, a "
            f"two-point gap, with correlated errors, at several benchmark sizes. <bookmark mark='b'/> The unpaired test, in "
            f"red, detects the gap {100 * r1['unpaired']:.0f} percent of the time with a thousand questions. <bookmark "
            f"mark='c'/> The paired test, in green, detects it {100 * r1['paired']:.0f} percent of the time, and "
            f"{100 * r2['paired']:.0f} percent with two thousand. <bookmark mark='d'/> Pairing is free power. And even "
            f"paired, a thousand-question benchmark usually cannot tell a two-point difference from noise. Plan the "
            f"benchmark's size from the smallest difference worth detecting, as Part thirteen planned experiments."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(u[0]), FadeIn(VGroup(*u[1:])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(p[0]), FadeIn(VGroup(*p[1:])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def curse(self):
        d = load("multiple")
        rows = d["rows"]
        lx = np.log10([r["k"] for r in rows])
        A = axes([0, 2.05], [0, 0.032], x_length=7.2, y_length=4.3, xlabel=r"number of equally good models $k$ (log scale)",
                 ylabel=r"the winner's score minus its true accuracy", xticks=[0, 1, 2], xfmt=lambda v: f"{10 ** v:g}",
                 yticks=[0, 0.01, 0.02, 0.03], yfmt=lambda v: f"+{100 * v:.0f}" if v else "0", center=[-2.4, 0.2, 0])
        ax = A.ax
        sim = VGroup(polyline(ax, lx, [r["bias"] for r in rows], NAIVEC, 3.5),
                     *[Dot(ax.c2p(a, r["bias"]), radius=0.07, color=NAIVEC) for a, r in zip(lx, rows)])
        th = polyline(ax, lx, [r["approx"] for r in rows], WHITE, 2, 0.8)
        r20 = next(r for r in rows if r["k"] == 20)
        side = side_groups([
            [(r"$k$ models, \ all truly 85\%", WHITE), (r"one benchmark of 1{,}000", GREY_A)],
            [(rf"red: \ the top score's bias, \ simulated", NAIVEC), (rf"{100 * r20['bias']:.1f} points at $k = 20$", NAIVEC)],
            [(r"white: \ SE $\times$ E[max of $k$ normals]", WHITE)],
            [(r"the top of a leaderboard", GREY_A), (r"is biased upward", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> Now many models. Suppose k models are all exactly 85 percent accurate, and all are scored on the same thousand questions, with independent errors. <bookmark mark='b'/> The top score is biased upward: by {100 * r20['bias']:.1f} points with twenty models. <bookmark mark='c'/> A normal approximation gives the bias as the standard error times the expected maximum of k standard normals, which grows like the square root of two log k. It is Part fifty-six's winner's curse. <bookmark mark='d'/> A model at the top of a crowded leaderboard is likely to score lower on fresh questions, even if nothing about it was tuned to the benchmark."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(sim[0]), FadeIn(VGroup(*sim[1:])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(th), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def multiplicity(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Comparing many models requires a stated error criterion. <bookmark mark='b'/> Holm controls familywise false rejection for valid individual tests; BH instead controls false discovery rate under its dependence conditions and does not certify a selected best model. <bookmark mark='c'/> A confidence set for the best model can be formed from simultaneous pairwise contrast bounds, retaining every model that no other model demonstrably exceeds. Overlap of ordinary marginal intervals is only a descriptive screen and has no automatic simultaneous rank coverage. <bookmark mark='d'/> Confirm a selected winner on fresh questions or use justified selective inference. The confirmation target, question distribution and stopping rule should be fixed before looking.",
            [(r"\text{many comparisons}", r":", r"\text{Holm, \ BH, \ simultaneous intervals}", 40),
             (r"\text{simultaneous rank-1 set}", r":", r"\text{every model that might be best}", 40),
             (r"\text{confirm}", r":", r"\text{fresh questions}", 40),
             (r"\text{or}", r":", r"\text{condition on the selection}", 40)],
            [r"Part 33", r"rank sets", r"a holdout", r"Part 56"],
            colors=[(1, HONC)])
