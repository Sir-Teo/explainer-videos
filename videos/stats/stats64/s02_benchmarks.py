from __future__ import annotations

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class Benchmarks(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter one. Benchmarks are samples, and their questions come in clusters.", 1,
                            r"Benchmarks are samples", r"Error bars for evaluations")
        self.population()
        self.clt()
        self.clusters()
        self.chart()
        self.board()
        self.deff()
        self.practice()

    def population(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What is a benchmark estimating? <bookmark mark='b'/> Imagine a population of questions: "
            "everything the benchmark's authors might have written, by the same process, on the same topics. <bookmark "
            "mark='c'/> The model's accuracy on that population is the quantity of interest; the benchmark's thousand "
            "questions are a sample from it, Part eight's setting. <bookmark mark='d'/> There is a second source of "
            "randomness, the model's own sampling when its temperature is above zero. Evan Miller's 2024 paper on error bars "
            "for evaluations treats both, and recommends averaging several answers per question to shrink the second.",
            [(r"\text{population}", r":", r"\text{every question that could have been written}", 38),
             (r"\text{target}", r":", r"\mu = E[\text{score}(Q)]", 40),
             (r"\text{benchmark}", r":", r"Q_1, \dots, Q_n \ \text{a sample}", 40),
             (r"\text{also}", r":", r"\text{the model's sampling noise}", 40)],
            [r"a superpopulation", r"what we want", r"Part 8", r"Miller (2024)"],
            colors=[(1, HONC)])

    def clt(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> If the questions are independent draws, Part six's central limit theorem does everything. "
            "<bookmark mark='b'/> The mean score is approximately normal, with standard error the standard deviation of the "
            "scores over the square root of n. <bookmark mark='c'/> For right-or-wrong questions that is the square root of "
            "p times one minus p over n: about 1.1 points at 85 percent and a thousand questions. <bookmark mark='d'/> Report "
            "it. The interval is plus or minus 1.96 of those, and a leaderboard without it is a list of point estimates.",
            [(r"\bar s", r"\approx", r"N(\mu, \ \sigma^2 / n)", 40),
             (r"\mathrm{SE}", r"=", r"s_{\text{sd}} / \sqrt{n}", 40),
             (r"\text{binary}", r":", r"\sqrt{p(1 - p)/n} \approx 0.011", 40),
             (r"\text{report}", r":", r"\bar s \pm 1.96 \, \mathrm{SE}", 40)],
            [r"Part 6", r"the iid error bar", r"$p = 0.85, \ n = 1{,}000$", r"always"],
            colors=[(3, HONC)])

    def clusters(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> But benchmark questions are rarely independent. <bookmark mark='b'/> Reading-comprehension "
            "benchmarks ask several questions about each passage; coding benchmarks test several cases of each problem; "
            "translated benchmarks ask the same question in many languages. <bookmark mark='c'/> A model that misunderstands "
            "a passage tends to miss all its questions together. The scores are correlated within clusters. <bookmark "
            "mark='d'/> Then the iid error bar is too small, and the fix is Part twenty-three's cluster-robust standard "
            "error: sum the residuals within each cluster before squaring.",
            [(r"\text{clusters}", r":", r"\text{passages, \ problems, \ languages}", 40),
             (r"\text{within}", r":", r"\text{correlated scores}", 40),
             (r"\text{iid SE}", r":", r"\text{too small}", 40),
             (r"\mathrm{SE}_{\text{CR}}^2", r"=", r"\frac{G}{G - 1}\,\frac{1}{n^2} \sum_c \Big(\sum_{i \in c} (s_i - \bar s)\Big)^2", 40)],
            [r"the usual design", r"shared difficulty", r"over-confident", r"Part 23's CR1"],
            colors=[(2, NAIVEC), (3, HONC)])

    def chart(self):
        d = load("clustered")
        A = axes([-0.6, 1.6], [0, 0.03], x_length=5.4, y_length=4.2, xlabel=r"", ylabel=r"standard error of the mean accuracy",
                 xticks=None, yticks=[0, 0.01, 0.02, 0.03], center=[-3.2, 0.3, 0])
        ax = A.ax
        vals = [(d["se_naive"], NAIVEC, r"iid SE"), (d["se_cluster"], HONC, r"cluster-robust SE")]
        bars = VGroup()
        for k, (v, c, nm) in enumerate(vals):
            b = Rectangle(width=0.8, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to(ax.c2p(k, 0), aligned_edge=DOWN)
            bars.add(VGroup(b, label(rf"{100 * v:.2f}", font_size=22, color=c).next_to(b, UP, buff=0.1),
                            label(nm, font_size=22, color=c).next_to(ax.c2p(k, 0), DOWN, buff=0.2)))
        truth = DashedLine(ax.c2p(-0.6, d["sd_mean"]), ax.c2p(1.6, d["sd_mean"]), color=WHITE, stroke_width=2)
        side = side_groups([
            [(rf"{d['G']} passages $\times$ {d['m']} questions", WHITE), (r"each passage has its own difficulty", GREY_A)],
            [(rf"red: \ iid SE, \ {100 * d['se_naive']:.2f} points", NAIVEC), (rf"95\% coverage {100 * d['cov_naive']:.1f}\%", NAIVEC)],
            [(rf"green: \ cluster-robust, \ {100 * d['se_cluster']:.2f}", HONC), (rf"95\% coverage {100 * d['cov_cluster']:.1f}\%", HONC)],
            [(rf"white dashes: \ the true sd, \ {100 * d['sd_mean']:.2f}", WHITE), (rf"over {d['reps']:,} benchmarks".replace(",", "{,}"), WHITE)],
        ], pos=(3.4, 0.3, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> A simulated benchmark: {d['G']} passages with {d['m']} questions each, and each passage "
            f"with its own difficulty for the model. <bookmark mark='b'/> The iid standard error says "
            f"{100 * d['se_naive']:.1f} points, and its ninety-five percent interval covers the true accuracy only "
            f"{100 * d['cov_naive']:.0f} percent of the time. <bookmark mark='c'/> The cluster-robust standard error is "
            f"{100 * d['se_cluster']:.1f} points, and covers {100 * d['cov_cluster']:.1f} percent. <bookmark mark='d'/> The "
            f"true standard deviation of the score across {d['reps']:,} simulated benchmarks is {100 * d['sd_mean']:.1f} "
            f"points: the clustered error bar was right, and the iid one was too small by forty percent."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(truth), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def board(self):
        b = load("board")["rows"]
        show_board(self, board_rows("iid error bar", "cluster-robust"),
                   f"<bookmark mark='a'/> On the Board: the iid error bar on a clustered benchmark covers "
                   f"{100 * b[0]['achieved']:.1f} percent of the time: broken. <bookmark mark='b'/> The cluster-robust error "
                   f"bar covers {100 * b[1]['achieved']:.1f} percent: kept.", [("a", [0]), ("b", [1])])

    def deff(self):
        d = load("clustered")
        self.lad_voiceover(
            f"<bookmark mark='a'/> How much do clusters cost? Part eighteen's design effect answers it. <bookmark "
            f"mark='b'/> With clusters of size m and intraclass correlation rho, the variance is multiplied by one plus m "
            f"minus one times rho. <bookmark mark='c'/> Here the ratio of the variances is {d['deff']:.2f}, which implies "
            f"an intraclass correlation of {d['icc']:.2f}. <bookmark mark='d'/> So a thousand clustered questions are worth "
            f"about {1000 / d['deff']:.0f} independent ones. Ten questions per passage buys much less than ten passages.",
            [(r"\text{design effect}", r"=", r"1 + (m - 1)\rho", 40),
             (r"\text{here}", r":", rf"{d['deff']:.2f}, \ \ \rho \approx {d['icc']:.2f}", 40),
             (r"n_{\text{eff}}", r"=", rf"1{{,}}000 / {d['deff']:.2f} \approx {1000 / d['deff']:.0f}", 40),
             (r"\text{design}", r":", r"\text{more clusters, \ fewer per cluster}", 40)],
            [r"Part 18", r"Kish", r"the effective sample", r"the lesson"],
            colors=[(2, NAIVEC), (3, HONC)])

    def practice(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In practice. <bookmark mark='b'/> Report an error bar with every score, and say how it was "
            "computed. <bookmark mark='c'/> Cluster on the unit that was sampled: the passage, the problem, the source "
            "document. If questions were written by a handful of annotators, the annotator is a cluster too. <bookmark "
            "mark='d'/> Bootstrapping is rarely needed for a mean; when it is, resample clusters, not questions, or the "
            "bootstrap inherits the iid mistake, as Part sixteen warned.",
            [(r"\text{report}", r":", r"\text{every score with its SE}", 40),
             (r"\text{cluster on}", r":", r"\text{the sampled unit}", 40),
             (r"\text{annotators}", r":", r"\text{clusters too}", 40),
             (r"\text{bootstrap}", r":", r"\text{resample clusters}", 40)],
            [r"Miller (2024)", r"design-based", r"hidden clusters", r"Part 16"],
            colors=[(3, HONC)])
