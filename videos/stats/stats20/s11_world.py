from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats20.common import *  # noqa: F403

METHODS = [("naive", r"one-day recall (the plan)", SALT), ("calib", r"regression calibration", DES),
           ("oracle", r"true intake, \ as if measured perfectly", TEAL)]


class OnTheWorld(VoiceoverScene):
    def construct(self):
        self.card()
        self.laws()
        self.one_survey()
        self.many()
        self.why_short()
        self.trial()
        self.board()

    def card(self):
        card = chapter_card(10, r"The same pipeline on the World", r"Where the answer is known", part=PART)
        with self.voiceover("Chapter ten. The same pipeline, on the World."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def laws(self):
        rows = [
            cmath(r"\text{pressure}", r"=", r"\text{age curve} + \text{BMI} + \text{sex} + 1.5 \times \text{sodium (g)} - 12 \times \text{medicine} + \text{noise}", font_size=24),
            cmath(r"\text{sodium}", r"\propto", r"\text{energy} \times \text{a taste factor}", font_size=28),
            cmath(r"\text{diagnosis}", r":", r"\text{pressure} \ge 140 \Rightarrow \text{told (75\%)}: \ \text{cut salt 10\%, \ 60\% medicated}", font_size=24),
            cmath(r"\text{two recalls}", r":", r"\text{that day's intake, \ noise SD 0.40 on the log scale}", font_size=26),
        ]
        rows[0][2].set_color(TRUE)
        whys = [why(r"the truth: \ 1.5 mm Hg per g, \ for every adult"), why(r"so energy and sodium go together"),
                why(r"the backwards loop of chapter nine"), why(r"correlation between days: \ 0.37, \ like NHANES")]
        intro = label('The simulation supplies a known structural sodium effect', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "The World now has a health block, built for this part, with laws we wrote down. <bookmark mark='a'/> Each "
            "adult's systolic pressure follows age, body size and sex, plus one point five millimetres for every gram of "
            "sodium they currently eat, minus twelve if they take medicine, plus personal variation. One point five is the "
            "truth, for everyone. <bookmark mark='b'/> Sodium is proportional to energy intake times a personal taste for "
            "salt. <bookmark mark='c'/> Those whose pressure reaches a hundred and forty are usually told so, and then cut "
            "their salt by a tenth, and most take medicine. <bookmark mark='d'/> And each adult has two dietary recalls, each "
            "that day's intake with noise, tuned so that the two days correlate about as they do in NHANES. The World's "
            "averages match NHANES too: three point four seven grams of sodium, a hundred and twenty-four millimetres of "
            "pressure."
        ) as vo:
            self.play(FadeIn(intro))
            self.add(simulated_tag(r"simulated: \ the World's health block"))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def one_survey(self):
        d = load("world")
        one = d["one"]
        t = 2.228  # t with 10 degrees of freedom
        A = axes([-0.5, 3], [0, 3.6], x_length=8.0, y_length=3.2, xlabel=r"sodium slope, \ mm Hg per g", xticks=[0, 0.5, 1, 1.5, 2, 2.5, 3],
                 center=[2.4, 0.8, 0])
        ax = A.ax
        truth = DashedLine(ax.c2p(1.5, 0), ax.c2p(1.5, 3.6), color=TRUE, stroke_width=3)
        tl = label(r"the truth: \ 1.5", font_size=22, color=TRUE).next_to(ax.c2p(1.5, 3.6), UP, buff=0.1)
        lines, labs = VGroup(), VGroup()
        for k, (key, txt, c) in enumerate(METHODS):
            b, s = one[key]
            y = 3 - k
            lines.add(VGroup(Line(ax.c2p(max(-0.5, b - t * s), y), ax.c2p(min(3, b + t * s), y), color=c, stroke_width=6),
                             Dot(ax.c2p(b, y), radius=0.08, color=c)))
            lb = label(txt + rf": \ {b:.2f}", font_size=19, color=c)
            if lb.width > 4.3:
                lb.width = 4.3
            labs.add(lb.next_to(ax.c2p(-0.5, y), LEFT, buff=0.15))
        foot = label(rf"one survey of the World: \ 10 regions $\times$ 2 towns $\times$ 250 adults; \ {one['n']:,} in the primary sample",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Use an illustrative NHANES-shaped design: ten regions, two PPS town draws per "
            "region, and two hundred and fifty adults in each draw, with older adults oversampled by age-stratified "
            "random sampling. The draw and within-age probabilities are exact. This is not NHANES's actual selection "
            "algorithm. Run the same analysis pipeline. <bookmark mark='b'/> In this survey the recall-day estimate "
            "is point three five. <bookmark mark='c'/> Joint regression calibration gives one point two three, with a"
            " much wider interval. <bookmark mark='d'/> Using true current intake gives one point zero zero. Even "
            "perfect sodium measurement does not automatically recover the structural effect, one point five."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ the World"))
            self.play(FadeIn(A), Create(truth), FadeIn(tl), FadeIn(foot))
            vo.wait_until("a")
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(Create(lines[k]), FadeIn(labs[k]))
        self.wait(1.0)
        self.clear_scene()

    def many(self):
        d = load("world")
        sm = d["summary"]
        A = axes([-1, 3.5], [0, 3.6], x_length=9.0, y_length=3.4, xlabel=r"sodium slope, \ 200 surveys of the World",
                 xticks=[-1, 0, 1, 1.5, 2, 3], center=[1.2, 0.8, 0])
        ax = A.ax
        truth = DashedLine(ax.c2p(1.5, 0), ax.c2p(1.5, 3.6), color=TRUE, stroke_width=3)
        g = np.random.Generator(np.random.PCG64(10))
        strips, labs = VGroup(), VGroup()
        for k, (key, txt, c) in enumerate(METHODS):
            y = 3 - k
            e = np.asarray(sm[key]["est"])
            e = e[(e >= -1) & (e <= 3.5)]
            strips.add(VGroup(*[Dot(ax.c2p(v, y + 0.5 * (g.random() - 0.5)), radius=0.035, color=c, fill_opacity=0.7) for v in e]))
            labs.add(label(rf"mean {sm[key]['mean']:.2f}; \ covers 1.5: \ {100 * sm[key]['cover']:.0f}\%", font_size=19, color=c)
                     .next_to(ax.c2p(-1, y), LEFT, buff=0.15))
        with self.voiceover(
            "<bookmark mark='a'/> Repeat for two hundred survey draws from this fixed World. <bookmark mark='b'/> The"
            " one-day analysis averages point two three, and none of its intervals contains one point five. <bookmark"
            " mark='c'/> Calibration averages point seven four and its joint design intervals cover in sixty-nine "
            "point five percent of draws. <bookmark mark='d'/> True intake gives an average of point nine six and "
            "coverage of fifty-three point five percent. These are empirical operating characteristics for this "
            "particular simulation and pipeline, not universal properties of survey analysis."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ the World"))
            self.play(FadeIn(A), Create(truth))
            vo.wait_until("a")
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(LaggedStart(*[FadeIn(x) for x in strips[k]], lag_ratio=0.004), FadeIn(labs[k]), run_time=1.5)
        self.wait(1.0)
        self.clear_scene()

    def why_short(self):
        d = load("world")["summary"]
        rows = [
            cmath(r"1.5 \to 0.96", r":", r"\text{diagnosis, \ selection and model projection}", font_size=28),
            cmath(r"0.96 \to 0.74", r":", r"\text{replicate calibration relies on an approximate error model}", font_size=28),
            cmath(r"0.74 \to 0.23", r":", r"\text{one day's noise, \ given energy}", font_size=28),
            cmath(r"\text{lesson}", r":", r"\text{replicates alone cannot identify a causal effect}", font_size=28),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"diagnosis, \ treatment selection and projection"), why(r"joint uncertainty from both regressions"),
                why(r"noisy energy and correlated within-day recall variation"), why(r"further causal design or assumptions are needed")]
        intro = label('A descriptive regression need not recover a structural effect', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "The simulation separates several problems, but these differences are not an additive causal "
            "decomposition. <bookmark mark='a'/> Even the true-intake regression is a descriptive projection, not the"
            " structural effect: diagnosis changes diet, medication exclusion selects adults, and the analysis's "
            "linear age and sex terms differ from the generating laws. <bookmark mark='b'/> Replicate calibration "
            "remains imperfect because its linear predictor and error assumptions are approximations. <bookmark "
            "mark='c'/> The simulated energy and sodium recalls share within-day reporting variation, so conditioning"
            " on noisy energy complicates classical attenuation. <bookmark mark='d'/> Better measurement can help, "
            "but cannot by itself establish causal identification. Confounding may be addressed only with further "
            "design or defensible assumptions, not by sodium replicates alone."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def trial(self):
        d = load("trial")
        A = axes([95, 155], [0, 3], x_length=8.4, y_length=3.0, xlabel=r"systolic pressure after a month, \ mm Hg",
                 xticks=[100, 110, 120, 130, 140, 150], center=[-1.4, 0.9, 0])
        ax = A.ax
        g = np.random.Generator(np.random.PCG64(11))
        lo = VGroup(*[Dot(ax.c2p(v, 2.1 + 0.6 * (g.random() - 0.5)), radius=0.04, color=HIT) for v in d["y_low"] if 95 <= v <= 155])
        hi = VGroup(*[Dot(ax.c2p(v, 0.9 + 0.6 * (g.random() - 0.5)), radius=0.04, color=SALT) for v in d["y_high"] if 95 <= v <= 155])
        ml = Line(ax.c2p(d["mean_low"], 1.7), ax.c2p(d["mean_low"], 2.5), color=HIT, stroke_width=5)
        mh = Line(ax.c2p(d["mean_high"], 0.5), ax.c2p(d["mean_high"], 1.3), color=SALT, stroke_width=5)
        rows = fit_rows(VGroup(
            label(r"400 adults, \ 30--70, \ not on medicine", font_size=22),
            label(rf"green: \ assigned {d['lo_g']:.2f} g a day; \ gold: \ {d['hi_g']:.2f} g", font_size=22),
            MathTex(rf"\text{{difference}}: {d['diff']:.1f} \pm {1.96 * d['diff_se']:.1f}\ \text{{mm Hg}}", font_size=26),
            MathTex(rf"\text{{per g}}: {d['est']:.2f} \pm {1.96 * d['se']:.2f}", font_size=28, color=TRUE),
            label(rf"2,000 such trials: \ intervals cover 1.5 in {100 * d['cover']:.1f}\%", font_size=22, color=HIT),
        ), 3.45, 0.4, [5.1, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now do what the trials did. Choose four hundred adults aged thirty to seventy, not on "
            "medicine, and assign half at random to a low-sodium diet, one point one five grams a day, and half to a high one, "
            "three point four five, for a month. <bookmark mark='b'/> Their pressures overlap enormously, but the means differ "
            "by four point four millimetres, <bookmark mark='c'/> which is one point nine three per gram, with an interval that "
            "contains the truth. <bookmark mark='d'/> Repeat the trial two thousand times: the intervals cover one point five "
            "ninety-six percent of the time. Four hundred randomized people succeed where five thousand surveyed people fail, "
            "because randomization breaks every arrow into sodium except the one we control."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a trial on the World"))
            self.play(FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in lo], lag_ratio=0.01), LaggedStart(*[FadeIn(x) for x in hi], lag_ratio=0.01),
                      FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ml), Create(mh), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=20) if r.part == 20]
        b = coverage_board(rows, lit_part=20, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Three rows for the Board, each a ninety-five percent interval for the World's "
            "sodium effect. The survey analysis as planned: zero percent, broken for this structural target. "
            "<bookmark mark='b'/> With joint regression calibration: sixty-nine point five percent, still below its "
            "nominal promise; causal and measurement assumptions remain unmet. <bookmark mark='c'/> The randomized "
            "trial: ninety-six percent, kept."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]))
            vo.wait_until("c")
            self.play(FadeIn(b.body[2]))
        self.wait(1.0)
        self.clear_scene()
