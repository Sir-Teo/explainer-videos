from __future__ import annotations

import numpy as np

from videos.stats.stats63.common import *  # noqa: F403


class Census(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter six. The 2020 United States census, the largest use of differential privacy.", 6,
                            r"The 2020 Census", r"Privacy at the scale of a nation", lit=(2022,))
        self.why_()
        self.topdown()
        self.projection()
        self.chart()
        self.why_bias()
        self.debate()
        self.choice()

    def why_(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The Census Bureau is bound by law not to reveal any person's answers. For decades it "
            "protected them by swapping some households between blocks and keeping the details secret. <bookmark mark='b'/> "
            "Then it attacked its own 2010 publications. From the billions of published table cells, it reconstructed "
            "person-level records of block, sex, age, race and ethnicity, and linked many to commercial data, an exercise "
            "in Dinur and Nissim's reconstruction. <bookmark mark='c'/> The conclusion was that swapping could not survive "
            "modern computing. <bookmark mark='d'/> For 2020 the Bureau, led on this by its chief scientist John Abowd, "
            "adopted differential privacy for its main products.",
            [(r"\text{Title 13}", r":", r"\text{no one's answers revealed}", 40),
             (r"\text{2010 tables}", r":", r"\text{reconstructed, \ then linked}", 40),
             (r"\text{conclusion}", r":", r"\text{swapping will not survive}", 40),
             (r"\text{2020}", r":", r"\text{differential privacy}", 40)],
            [r"the law", r"the Bureau's own attack", r"Dinur \& Nissim (2003)", r"Abowd et al. (2022)"],
            colors=[(1, BADC), (3, PRIVC)])

    def topdown(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The TopDown algorithm works down the geographic hierarchy: nation, state, county, "
            "tract, block group, block. <bookmark mark='b'/> At each level it measures many tables of counts with "
            "discrete Gaussian noise, spending a share of the total budget, rho of 2.63 for the redistricting data. "
            "<bookmark mark='c'/> Some numbers, called invariants, were published exactly, including each state's total "
            "population, which apportions Congress. <bookmark mark='d'/> Then post-processing: an optimization finds "
            "nonnegative integer counts, consistent across levels and with the invariants, as close as possible to the noisy "
            "measurements. Post-processing costs no privacy.",
            [(r"\text{hierarchy}", r":", r"\text{nation} \to \text{state} \to \cdots \to \text{block}", 40),
             (r"\text{measure}", r":", r"\text{discrete Gaussian noise}, \ \rho = 2.63", 40),
             (r"\text{invariants}", r":", r"\text{state totals, \ exact}", 40),
             (r"\text{post-process}", r":", r"\text{nonnegative, \ consistent integers}", 40)],
            [r"top down", r"zCDP", r"apportionment", r"free for privacy"],
            colors=[(1, PRIVC), (3, OKC)])

    def projection(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A toy version shows what post-processing does to the statistics. <bookmark mark='b'/> "
            "Four hundred blocks in a county, with populations from a skewed distribution: many tiny blocks and a few large "
            "ones. <bookmark mark='c'/> Add rounded Gaussian noise of standard deviation four to each count. Some small "
            "blocks get negative counts. <bookmark mark='d'/> Then project: the least-squares nonnegative counts that add "
            "up to the county's exact total. The solution subtracts one constant from every count, and sets to zero those "
            "that would go negative: a water-filling.",
            [(r"\text{blocks}", r":", r"400, \ \text{skewed sizes}", 40),
             (r"\text{noise}", r":", r"\tilde c_b = c_b + \mathrm{round}(N(0, 4^2))", 40),
             (r"\text{project}", r":", r"\min \textstyle\sum (c_b - \tilde c_b)^2, \ \ c_b \ge 0, \ \sum c_b = C", 38),
             (r"\text{solution}", r":", r"c_b = \max(\tilde c_b - \lambda, 0)", 40)],
            [r"a toy county", r"the measurements", r"post-processing", r"water-filling"],
            colors=[(3, OKC)])

    def chart(self):
        d = load("census")
        rows = d["rows"]
        A = axes([-0.6, 3.6], [-0.2, 0.85], x_length=7.4, y_length=4.2, xlabel=r"",
                 ylabel=r"average error of the block count, \ 200 runs", xticks=None, yticks=[0, 0.25, 0.5, 0.75],
                 center=[-2.4, 0.3, 0])
        ax = A.ax
        zero = Line(ax.c2p(-0.6, 0), ax.c2p(3.6, 0), color=GREY_B, stroke_width=1.5)
        names = [r"0--4", r"5--19", r"20--99", r"100+"]
        raw, post = VGroup(), VGroup()
        for k, r in enumerate(rows):
            for grp, key, dx, col in ((raw, "bias_raw", -0.2, RAWC), (post, "bias_post", 0.2, PRIVC)):
                v = r[key]
                h = abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1])
                b = Rectangle(width=0.36, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
                b.move_to(ax.c2p(k + dx, 0), aligned_edge=DOWN if v >= 0 else UP)
                t = label(rf"{v:+.2f}", font_size=18, color=col).next_to(b, UP if v >= 0 else DOWN, buff=0.08)
                grp.add(VGroup(b, t))
        ticks = VGroup(*[label(rf"{nm} \ ({r['n']})", font_size=20, color=GREY_A).next_to(ax.c2p(k, -0.2), DOWN, buff=0.15)
                         for k, (nm, r) in enumerate(zip(names, rows))])
        ticks.add(label(r"true block population \ (blocks per class)", font_size=22, color=GREY_A).next_to(ticks, DOWN, buff=0.25))
        side = side_groups([
            [(r"400 blocks; \ noise sd 4", WHITE), (r"200 noisy releases", GREY_A)],
            [(r"blue: \ the noisy measurements", RAWC), (r"unbiased in every class", RAWC),
             (rf"{100 * d['neg_raw']:.1f}\% of counts negative", RAWC)],
            [(r"purple: \ after the projection", PRIVC), (rf"tiny blocks: \ {rows[0]['bias_post']:+.2f} people", PRIVC),
             (r"larger blocks: \ slightly low", PRIVC)],
            [(r"no negative counts, \ exact total", OKC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The average error of each block's count over two hundred runs, by the block's true "
            f"size. <bookmark mark='b'/> The noisy measurements, in blue, are unbiased in every size class, but "
            f"{100 * d['neg_raw']:.1f} percent of them are negative. <bookmark mark='c'/> After the projection, in purple, "
            f"the smallest blocks, with fewer than five people, are inflated by {rows[0]['bias_post']:.2f} of a person on "
            f"average, a large relative error, and the mass comes out of the larger blocks, which are slightly too small. "
            f"<bookmark mark='d'/> No count is negative and the total is exact. Post-processing cost nothing in privacy, "
            f"and it bought consistency with a systematic bias."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(ticks), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(raw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(post), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def why_bias(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Why the bias? <bookmark mark='b'/> A block of one person with noise of standard "
            "deviation four is pushed below zero about a third of the time, and nonnegativity lifts every such "
            "measurement up to zero. Truncation raises the mean. <bookmark mark='c'/> To keep the total exact, the "
            "projection takes the excess from everyone else, a little from each large block. <bookmark mark='d'/> The same "
            "mechanism, in the real census, made small places a little bigger and large places a little smaller, and "
            "added error to counts for small groups. The Bureau later published the noisy measurements themselves, which "
            "analysts can use without the post-processing bias: the redistricting file appeared in June 2023.",
            [(r"\text{a block of one}", r":", r"P(\tilde c < 0) \approx 0.35", 40),
             (r"\text{nonnegativity}", r":", r"\text{truncation raises the mean}", 40),
             (r"\text{exact total}", r":", r"\text{taken from large blocks}", 40),
             (r"\text{cure}", r":", r"\text{publish the noisy measurements}", 40)],
            [r"$\Phi(-1.5/4)$, \ with rounding", r"Part 41's truncation", r"a constant shift", r"analysable noise"],
            colors=[(1, BADC), (3, OKC)])

    def debate(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The change was fought over. <bookmark mark='b'/> Christopher Kenny and coauthors, "
            "studying the Bureau's demonstration data in 2021, argued that the noise could distort redistricting and "
            "voting-rights analyses, especially for racially mixed areas. <bookmark mark='c'/> The State of Alabama sued "
            "to stop the method in 2021; in June a three-judge federal court declined to block it, calling the challenge premature. <bookmark mark='d'/> Demographers worried "
            "about small-area estimates, and the Bureau set the final budget above that of its early demonstration data, "
            "buying accuracy with privacy. Every user of census data now works with a declared privacy-accuracy trade-off.",
            [(r"\text{redistricting}", r":", r"\text{distortion in mixed areas}", 40),
             (r"\text{Alabama}", r":", r"\text{sued, \ 2021; \ not blocked}", 40),
             (r"\text{demographers}", r":", r"\text{small-area accuracy}", 40),
             (r"\text{response}", r":", r"\text{a larger final budget}", 40)],
            [r"Kenny et al. (2021)", r"a federal court", r"small areas", r"a declared trade-off"],
            colors=[(0, BADC)])

    def choice(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Who should choose epsilon? <bookmark mark='b'/> John Abowd and Ian Schmutte argued in "
            "2019 that privacy and accuracy are both public goods, and that the budget is an economic choice: spend it until "
            "the marginal social cost of lost privacy equals the marginal social benefit of accuracy. <bookmark mark='c'/> "
            "The mathematics prices the trade-off exactly, in mean squared error per unit of rho. <bookmark mark='d'/> It "
            "does not say where to stand on the curve. That is a decision for the society whose data they are, informed by "
            "the curve, which is more than any previous disclosure method offered.",
            [(r"\text{who chooses } \varepsilon", r":", r"\text{a social decision}", 40),
             (r"\text{economics}", r":", r"\text{marginal cost} = \text{marginal benefit}", 40),
             (r"\text{statistics}", r":", r"\text{the exact trade-off curve}", 40),
             (r"\text{not decided by}", r":", r"\text{the mathematics alone}", 40)],
            [r"the open question", r"Abowd \& Schmutte (2019)", r"chapters 4--5", r"Part 45's decisions"],
            colors=[(2, OKC)])
