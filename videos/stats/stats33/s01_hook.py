from __future__ import annotations

import numpy as np

from videos.stats.stats33.common import *  # noqa: F403


def fish_map(d, key, color):
    """The salmon's voxels: the fish in dark grey, lit voxels in ``color``."""
    mask = np.asarray(d["mask"], float)
    act = np.asarray(d[key], float) if key else np.zeros_like(mask)
    arr = 0.25 * mask + 0.75 * act
    return PhantomPanel(arr, size=3.4, lo=0, hi=1, tint=color, center=[-2.3, 0.4, 0])


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.scan()
        self.lit()
        self.stricter()
        self.corrected()
        self.arith()
        self.lesson()
        self.objectives()

    def story(self):
        tl = timeline(lit=(2009,)).to_edge(UP, buff=0.35)
        hc = history_card(2009, r"Craig Bennett, \ Abigail Baird, \ Michael Miller \& George Wolford",
                          r"A mature Atlantic salmon, \ `not alive at the time of scanning', \ is shown photographs of "
                          r"people in social situations in an MRI scanner. \ The standard analysis finds a cluster of "
                          r"`active' voxels in its brain", color=SIGC, width=11.0, font_size=23).move_to([0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(r"the salmon was dead; \ the analysis was standard", font_size=24),
            label(r"the point: \ test thousands of voxels and some will light up by chance", font_size=24, color=SIGC),
        ), 12.0, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2009 the neuroscientist Craig Bennett and his colleagues put a salmon into an "
            "MRI scanner. It was a mature Atlantic salmon, and, as their poster put it, not alive at the time of "
            "scanning. They showed it photographs of people in social situations and asked it to judge what emotion "
            "each person felt. <bookmark mark='b'/> A standard analysis found a small cluster of voxels in the "
            "salmon's brain that responded to the photographs. <bookmark mark='c'/> The salmon was not thinking. Its "
            "brain was tested at thousands of locations at once, and at thousands of locations, chance alone will "
            "light some up. The work became a widely discussed demonstration of multiple testing."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def scan(self):
        d = load("salmon")
        fm = fish_map(d, None, SIGC)
        rows = fit_rows(VGroup(
            label(rf"our own dead fish: \ {d['n_vox']:,} voxels of pure noise", font_size=22),
            label(r"15 independent noise images, \ spatially smoothed", font_size=22, color=GREY_A),
            label(r"a $t$-test at every voxel: \ is its mean zero?", font_size=22, color=SIGC),
            label(r"by construction, \ no voxel does", font_size=22, color=FALSEC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> We can illustrate the statistical problem with a toy simulation. Here is a "
            "fish-shaped brain of nine thousand one hundred and forty-one voxels, <bookmark mark='b'/> each measured "
            "in fifteen independent Gaussian noise images, smoothed in space. This is not a reconstruction of the "
            "original task design. <bookmark mark='c'/> At each voxel, a one-sample t-test asks whether its mean is "
            "zero. <bookmark mark='d'/> By construction, none does: every null hypothesis is true."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(fm), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.wait(0.5)
        self.clear_scene()

    def lit(self):
        d = load("salmon")
        f0 = fish_map(d, None, SIGC)
        f1 = fish_map(d, "active01", SIGC)
        rows = fit_rows(VGroup(
            label(r"uncorrected $p < 0.01$", font_size=24),
            label(rf"{d['n_active01']} voxels light up, \ in {d['clusters01']} clusters", font_size=24, color=SIGC),
            label(rf"at $p < 0.05$: \ {d['n_05']} voxels", font_size=24, color=SIGC),
            label(r"blobs, \ because neighbouring noise is correlated", font_size=22, color=GREY_A),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Threshold the map at p below one in a hundred, uncorrected. <bookmark mark='b'/> "
            "Seventy-eight voxels light up, in twenty-seven separate blobs. <bookmark mark='c'/> At the conventional five "
            "percent, four hundred and forty-six do. <bookmark mark='d'/> They form blobs rather than isolated dots because "
            "the noise at neighbouring voxels is correlated, which makes chance activity look like anatomy."
        ) as vo:
            self.add(seeded_tag())
            self.add(f0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeTransform(f0.image, f1.image), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def stricter(self):
        d = load("salmon")
        f1 = fish_map(d, "active", SIGC)
        rows = fit_rows(VGroup(
            label(r"Bennett's threshold: \ $p < 0.001$", font_size=24),
            label(rf"{d['n_active']} voxels survive here; \ about {d['expected']:.0f} expected", font_size=24, color=SIGC),
            label(r"the real salmon: \ a cluster of 3", font_size=24, color=SIGC),
            label(r"a stricter threshold is not a correction", font_size=24, color=FALSEC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The salmon study used a stricter threshold, p below one in a thousand, and required"
            " a cluster of at least three voxels. <bookmark mark='b'/> In our fish three voxels survive this "
            "realization, against an expectation of about nine. Correlation makes the count fluctuate. <bookmark "
            "mark='c'/> In the salmon's real scan, a cluster of three survived. <bookmark mark='d'/> A stricter "
            "per-voxel threshold reduces false positives, but it is not a correction for the number of tests: with a "
            "hundred and thirty thousand voxels in a human brain scan, p below a thousandth still lights up about a "
            "hundred and thirty by chance."
        ) as vo:
            self.add(seeded_tag())
            self.add(f1)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def corrected(self):
        d = load("salmon")
        f1 = fish_map(d, None, SIGC)
        rows = fit_rows(VGroup(
            label(r"correct for the number of tests", font_size=24),
            label(rf"Bonferroni: \ {d['bonf']} voxels", font_size=24, color=FWC),
            label(rf"false discovery rate (BH): \ {d['bh']} voxels", font_size=24, color=BHC),
            label(r"the dead fish is dead again", font_size=24, color=TRUEC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Bennett's real point came next: correct for the number of tests. <bookmark "
            "mark='b'/> With Bonferroni's correction, chapter two, no voxel survives. <bookmark mark='c'/> With a "
            "false discovery rate correction, chapter three, none either. <bookmark mark='d'/> The dead fish is dead "
            "again. The example shows why a per-voxel threshold alone cannot support a whole-map claim."
        ) as vo:
            self.add(seeded_tag())
            self.add(f1)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k]))
        self.clear_scene()

    def arith(self):
        rows = [
            cmath(r"E(\text{false positives})", r"=", r"m\alpha", font_size=34),
            cmath(r"m = 9{,}141, \ \alpha = 0.05", r":", r"457 \ \text{expected}; \ 446 \ \text{seen}", font_size=30),
            cmath(r"P(\text{at least one})", r"=", r"1 - (1 - \alpha)^m", font_size=32),
            cmath(r"m = 20", r":", r"64\%; \ \ m = 100: \ 99.4\%", font_size=32),
        ]
        rows[0][-1].set_color(SIGC)
        whys = [why(r"$m$ true nulls, \ exact uniform marginal $p$-values"), why(r"the fish"), why(r"independent tests"),
                why(r"Part 10's warning, \ multiplied")]
        with self.voiceover(
            "<bookmark mark='a'/> The arithmetic is simple. With exactly uniform null p-values, testing m true nulls "
            "at alpha gives m times alpha expected false positives, even under dependence. With super-uniform "
            "p-values this is an upper bound. <bookmark mark='b'/> For the fish, four hundred and fifty-seven "
            "expected at five percent; we saw four hundred and forty-six. <bookmark mark='c'/> The chance of at least"
            " one false positive is one minus one minus alpha to the m, for independent tests. <bookmark mark='d'/> "
            "With twenty tests that is already sixty-four percent; with a hundred, ninety-nine point four. Part 10's "
            "single test, multiplied."
        ) as vo:
            intro=label('Expected false counts and family-wise risk answer different questions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"genomics: \ 20{,}000 genes; \ imaging: \ 100{,}000 voxels; \ A/B testing: \ dozens of metrics", font_size=26),
            label(r"and quietly: \ many analyses of one data set", font_size=26, color=FALSEC),
            label(r"which discoveries are real?", font_size=26, color=SIGC),
            label(r"and what does `real' even mean for a list of thousands?", font_size=26, color=BHC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Modern science asks thousands of questions at once: twenty thousand genes, a hundred "
            "thousand voxels, dozens of metrics in every online experiment. <bookmark mark='b'/> And quietly, many analyses "
            "of a single data set, which is the same problem in disguise. <bookmark mark='c'/> When chance answers some "
            "of the questions, which answers are real? <bookmark mark='d'/> And what should we even promise about a list of "
            "thousands of discoveries? This part changes what error control means."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 33", font_size=34, color=GREY_B), label(r"Thousands of Questions", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"family-wise error: \ Bonferroni, \ Holm, \ closed testing, \ Westfall--Young",
            r"the false discovery rate: \ Benjamini--Hochberg, \ BY, \ Storey's $q$-values",
            r"empirical Bayes: \ local fdr and the empirical null; \ FDR as an average",
            r"knockoffs; \ the garden of forking paths; \ the p-hacking simulator",
            r"replication, \ publication bias, \ remedies; \ the false coverage rate",
        ], color=BHC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 10 and 25").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.multiple}; \ the p-hacking simulator").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-three: thousands of questions. <bookmark mark='b'/> We'll control the chance "
            "of any false positive, with Bonferroni, Holm and the permutation method of Westfall and Young; change the goal "
            "to the false discovery rate with Benjamini and Hochberg; estimate the proportion of nulls and the local false "
            "discovery rate with Efron's empirical Bayes; see that the false discovery rate is only an average; build "
            "knockoffs; simulate p-hacking; measure the replication crisis and publication bias; argue about remedies; and "
            "finish with intervals for selected effects."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
