from __future__ import annotations

import numpy as np

from videos.stats.stats20.common import *  # noqa: F403


class Design(VoiceoverScene):
    def construct(self):
        self.card()
        self.stages()
        self.psus()
        self.oversample()
        self.weights()
        self.means()
        self.deff()

    def card(self):
        card = chapter_card(2, r"The design and its weights", r"Who was asked, \ and whom they stand for", part=PART)
        with self.voiceover("Chapter two. The design, and its weights."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def stages(self):
        rows = [
            cmath(r"\text{stage 1}", r":", r"\text{counties (PSUs), \ in strata, \ chosen PPS}", font_size=28),
            cmath(r"\text{stage 2}", r":", r"\text{neighbourhoods within each county}", font_size=28),
            cmath(r"\text{stage 3}", r":", r"\text{households within neighbourhoods}", font_size=28),
            cmath(r"\text{stage 4}", r":", r"\text{people, \ some groups at higher rates}", font_size=28),
        ]
        rows[3][2].set_color(SALT)
        whys = [why(r"Part 18: \ clusters, \ strata, \ Hansen \& Hurwitz"), why(r"segments of a few blocks"),
                why(r"from address lists"), why(r"oversampling: \ the next picture")]
        intro = label('NHANES uses a multistage probability design', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Chapter one's population is two hundred and thirty-six million people; NHANES examines about five thousand "
            "adults every two years. How it picks them is Part 18 in action. <bookmark mark='a'/> First it chooses counties, "
            "the primary sampling units, grouped into strata and drawn with probability proportional to size, because a mobile "
            "examination centre must park somewhere. <bookmark mark='b'/> Within each county it chooses neighbourhoods, "
            "<bookmark mark='c'/> within them households, <bookmark mark='d'/> and within households people, with some groups "
            "deliberately chosen at higher rates. None of this is a simple random sample, and the analysis has to know it."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.72, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def psus(self):
        d = load("design")
        cells = VGroup()
        for h in range(d["strata"]):
            pair = VGroup(*[Circle(radius=0.17, stroke_color=DES, stroke_width=2, fill_color=DES, fill_opacity=0.35)
                            for _ in range(2)]).arrange(DOWN, buff=0.12)
            box = SurroundingRectangle(pair, buff=0.1, corner_radius=0.08, stroke_color=GREY_C, stroke_width=1.5)
            cells.add(VGroup(box, pair, MathTex(str(h + 1), font_size=18, color=GREY_B).next_to(box, DOWN, buff=0.08)))
        cells.arrange(RIGHT, buff=0.18).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(rf"{d['strata']} strata $\times$ 2 PSUs $=$ {d['psus']} ``masked variance units''", font_size=24, color=DES),
            label(r"the real counties are hidden, \ to protect who took part", font_size=22, color=GREY_A),
            label(r"degrees of freedom for SEs: \ 30 PSUs $-$ 15 strata $=$ 15", font_size=24, color=OBS),
            label(r"the public variance estimator uses 30 masked PSUs in 15 strata", font_size=22, color=RES),
        ), 12.0, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The public files describe the design in a disguised form: fifteen strata, each with two "
            "pseudo-PSUs, thirty in all. <bookmark mark='b'/> They're called masked variance units: built so that standard "
            "errors come out right, while the actual counties stay secret, since in a small county knowing the location, age "
            "and sex could identify a person. <bookmark mark='c'/> For standard errors, what counts is the number of PSUs "
            "minus the number of strata: fifteen degrees of freedom. <bookmark mark='d'/> Five thousand people, but in thirty "
            "clusters, and people in the same cluster resemble each other. That will matter in chapter seven."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cells], lag_ratio=0.08), FadeIn(rows[0]), run_time=2.5)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1], shift=RIGHT * 0.2))
        self.clear_scene()

    def oversample(self):
        d = load("design")
        groups = list(d["shares"].keys())
        A = axes([-0.6, len(groups) - 0.4], [0, 0.7], x_length=9.0, y_length=3.8, xlabel=r"", ylabel=r"share of adults 20+",
                 yticks=[0, 0.2, 0.4, 0.6], center=[-1.0, 0.6, 0], yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        w = ax.c2p(0.35, 0)[0] - ax.c2p(0, 0)[0]
        bs, bw = VGroup(), VGroup()
        for k, gname in enumerate(groups):
            for j, (key, col, grp) in enumerate((("sample", NH, bs), ("weighted", DES, bw))):
                v = d["shares"][gname][key]
                grp.add(Rectangle(width=w, height=max(0.01, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=col,
                                  fill_opacity=0.9).move_to(ax.c2p(k - 0.19 + 0.38 * j, 0), aligned_edge=DOWN))
        names = VGroup(*[label(gname, font_size=18, color=GREY_A).rotate(25 * DEGREES)
                         .move_to(ax.c2p(k, 0) + DOWN * 0.15 + RIGHT * 0.1, aligned_edge=UR) for k, gname in enumerate(groups)])
        rows = fit_rows(VGroup(
            label(r"cream: \ the sample", font_size=22, color=NH),
            label(r"blue: \ weighted, \ the population", font_size=22, color=DES),
            label(rf"Black adults: \ {100 * d['shares']['Black']['sample']:.0f}\% of the sample, \ {100 * d['shares']['Black']['weighted']:.0f}\% of adults", font_size=20),
            label(rf"Asian adults: \ {100 * d['shares']['Asian']['sample']:.0f}\% vs {100 * d['shares']['Asian']['weighted']:.0f}\%", font_size=20),
            label(rf"aged 60+: \ {100 * d['old_sample']:.0f}\% vs {100 * d['old_weighted']:.0f}\%", font_size=20),
            label(r"so that every group has enough people to study", font_size=20, color=OBS),
        ), 3.45, 0.36, [5.3, 0.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's what higher rates means. In cream, the share of each group in the sample of adults; "
            "<bookmark mark='b'/> in blue, its share of the population. <bookmark mark='c'/> Black adults are twenty-four "
            "percent of the sample but eleven percent of the population; <bookmark mark='d'/> Asian adults, fourteen percent "
            "against six; Hispanic adults are oversampled too; <bookmark mark='e'/> and so are older people, thirty-nine percent of "
            "the sample, twenty-nine of the population. <bookmark mark='f'/> It's deliberate: without oversampling there would be "
            "too few people in these groups to say anything about their health. White adults, sixty-two percent of the "
            "population, are a third of the sample."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bs], lag_ratio=0.1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bw], lag_ratio=0.1), FadeIn(rows[1]))
            for k, m_ in enumerate("cdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def weights(self):
        d = load("design")
        rows = [
            cmath(r"w_i", r"=", r"\frac{1}{P(i \text{ selected})} \times \text{adjustments}", font_size=32),
            cmath(r"\text{median weight}", r":", rf"\text{{{d['w_median']:,.0f}: \ one person stands for that many}}", font_size=28),
            cmath(r"\text{range}", r":", rf"\text{{{d['w_min']:,.0f} to {d['w_max']:,.0f}}}", font_size=30),
            cmath(r"\textstyle\sum_i w_i", r"=", rf"\text{{{d['pop'] / 1e6:.0f} million: \ the population}}", font_size=30),
        ]
        rows[0][2].set_color(DES)
        whys = [why(r"Horvitz--Thompson (Part 18), \ then nonresponse, \ post-strata"), why(r"the exam weight, \ adults 20+"),
                why(r"a ninety-fold spread"), why(r"matched to Census totals by age, \ sex, \ race")]
        intro = label('Survey weights connect sampled adults to their population', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Each person carries a weight: one over their probability of selection, as in Part 18's "
            "Horvitz–Thompson estimator, then adjusted for people who refused the interview or the exam, and post-stratified so "
            "that totals by age, sex and race match the Census. <bookmark mark='b'/> The median adult weight is about twenty-six "
            "and a half thousand: that person speaks for twenty-six thousand Americans. <bookmark mark='c'/> The range is "
            "large, from under five thousand for the most oversampled to over four hundred thousand. <bookmark mark='d'/> And "
            "the weights add up to the population, two hundred and thirty-six million adults."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def means(self):
        d = load("design")
        A = axes([120, 130], [0, 2], x_length=9.0, y_length=2.2, xlabel=r"mean systolic pressure, \ adults 20+, \ mm Hg",
                 xticks=[120, 122, 124, 126, 128, 130], center=[0, 0.8, 0])
        ax = A.ax
        u = Dot(ax.c2p(d["sbp_unweighted"], 1.4), radius=0.12, color=NH)
        wv = Dot(ax.c2p(d["sbp_weighted"], 0.6), radius=0.12, color=DES)
        wci = Line(ax.c2p(d["sbp_weighted"] - 2.13 * d["sbp_se"], 0.6), ax.c2p(d["sbp_weighted"] + 2.13 * d["sbp_se"], 0.6),
                   color=DES, stroke_width=5)
        lu = label(rf"unweighted: \ {d['sbp_unweighted']:.1f}", font_size=22, color=NH).next_to(u, UP, buff=0.15)
        lw = label(rf"weighted: \ {d['sbp_weighted']:.1f}", font_size=22, color=DES).next_to(wv, DOWN, buff=0.2)
        rows = fit_rows(VGroup(
            label(r"the sample is older and has more Black adults than the population", font_size=24),
            label(r"both groups have higher pressure on average", font_size=24, color=BP),
            label(r"so the raw mean overstates the nation's by 3.3 mm Hg", font_size=24, color=RES),
            label(r"a mean: \ always weighted; \ a regression slope: \ chapter five's choice", font_size=22, color=OBS),
        ), 12.0, 0.35, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Does weighting matter? For the mean systolic pressure of American adults, the unweighted "
            "average of the sample is a hundred and twenty-seven point one. <bookmark mark='b'/> Weighted, it is a hundred and "
            "twenty-three point nine. <bookmark mark='c'/> Mainly, the sample is older and includes more Black adults than "
            "the population, <bookmark mark='d'/> and both groups have higher blood pressure on average, <bookmark mark='e'/> so the "
            "raw mean overstates the nation's by three point three, more than six standard errors. <bookmark mark='f'/> For a "
            "national mean, weighting is not optional. For a regression slope the argument is subtler, and chapter five will "
            "make it."
        ) as vo:
            self.add(nh_tag(corner=DR))
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(u, scale=1.5), FadeIn(lu))
            vo.wait_until("b")
            self.play(FadeIn(wv, scale=1.5), Create(wci), FadeIn(lw))
            for k, m_ in enumerate("cdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def deff(self):
        d = load("design")
        rows = [
            cmath(r"\text{SE, \ design-based}", r":", rf"{d['sbp_se']:.2f}", font_size=30),
            cmath(r"\text{SE, \ as if an SRS}", r":", rf"{d['sbp_srs_se']:.2f}", font_size=30),
            cmath(r"\text{design effect}", r":", rf"({d['sbp_se']:.2f} / {d['sbp_srs_se']:.2f})^2 = {d['deff']:.1f}", font_size=30),
            cmath(r"n_{\text{eff}}", r":", rf"4{{,}}948 / {d['deff']:.1f} \approx {d['neff']:,.0f}", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"Taylor linearization over strata and PSUs"), why(r"weighted population SD $/ \sqrt n$, \ SRS reference"),
                why(r"clusters (Kish) and unequal weights"), why(r"what the sample is worth for this mean")]
        intro = label('Compare precision against a stated simple-random-sample reference', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> And the design changes the uncertainty. The design-based standard error of that "
            "mean, computed by linearization across the strata and PSUs, is point four nine. <bookmark mark='b'/> "
            "Using the weighted population variance as an equal-size simple-random-sample reference gives point two "
            "six. <bookmark mark='c'/> The ratio of variances, the design effect, is three point six: clustering, as "
            "in Part 18, plus unequal weights, which Kish showed cost precision too. <bookmark mark='d'/> For this "
            "mean, four thousand nine hundred and forty-eight examined adults are worth about thirteen hundred and "
            "sixty-five chosen at random. For this mean the naive interval is too narrow; stratification can also "
            "reduce variance for other outcomes."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()
