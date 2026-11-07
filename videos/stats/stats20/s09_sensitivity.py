from __future__ import annotations

import numpy as np

from videos.stats.stats20.common import *  # noqa: F403

AXIS_NAMES = {"meds": r"BP medicine users in", "energy": r"energy adjusted", "weights": r"weighted",
              "age_spline": r"age spline", "readings": r"all readings", "exposure": r"two-day mean"}
ON = {"meds": "keep", "energy": True, "weights": True, "age_spline": True, "readings": "all", "exposure": "mean2"}


class Sensitivity(VoiceoverScene):
    def construct(self):
        self.card()
        self.curve()
        self.which()
        self.two_days()
        self.attenuation()
        self.calibration()
        self.verdict()

    def card(self):
        card = chapter_card(8, r"Sensitivity", r"What changes the answer?", part=PART)
        with self.voiceover("Chapter eight. Sensitivity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def curve(self):
        d = load("spec")
        runs = sorted(d["runs"], key=lambda r: r["est"])
        n = len(runs)
        lower = np.floor(min(r["est"] - r["critical"] * r["se"] for r in runs))
        upper = np.ceil(max(r["est"] + r["critical"] * r["se"] for r in runs))
        A = axes([0, n + 1], [lower, upper], x_length=10.6, y_length=3.0, xlabel=r"", ylabel=r"sodium slope, \ mm Hg per g",
                 yticks=list(np.arange(lower, upper + 0.1, 1)), center=[0.3, 1.5, 0], font_size=18)
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(n + 1, 0), color=GREY_C, stroke_width=1.5)
        prim = next(i for i, r in enumerate(runs) if r["spec"] == {"meds": "exclude", "energy": True, "weights": True,
                                                                    "age_spline": False, "readings": "2+", "exposure": "day1"})
        bars, dots = VGroup(), VGroup()
        for i, r in enumerate(runs):
            c = SALT if i == prim else DES
            bars.add(Line(ax.c2p(i + 1, r["est"] - r["critical"] * r["se"]), ax.c2p(i + 1, r["est"] + r["critical"] * r["se"]),
                          color=c, stroke_width=1.6, stroke_opacity=0.7))
            dots.add(Dot(ax.c2p(i + 1, r["est"]), radius=0.045 if i != prim else 0.08, color=c))
        grid = VGroup()
        names = VGroup()
        for j, a in enumerate(d["axes"]):
            y = -0.55 - 0.36 * j
            names.add(label(AXIS_NAMES[a], font_size=16, color=GREY_A).move_to([ax.c2p(0, 0)[0] - 0.15, y, 0], aligned_edge=RIGHT))
            for i, r in enumerate(runs):
                on = r["spec"][a] == ON[a]
                grid.add(Dot([ax.c2p(i + 1, 0)[0], y, 0], radius=0.045, color=SALT if i == prim and on else (WHITE if on else GREY_D)))
        foot = label(rf"all {n}: \ from {d['min']:+.2f} to {d['max']:+.2f}; \ none distinguishable from zero", font_size=22,
                     color=OBS).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The plan promised all sixty-four analyses. Here they are: a specification curve, as Uri Simonsohn and "
            "colleagues called it. <bookmark mark='a'/> Each dot is one analysis's sodium slope, sorted from smallest"
            " to largest, with design t intervals using the degrees of freedom of each fit. <bookmark mark='b'/> "
            "Below, which choices it made: medicine users in or out, energy in the model or not, weights or not, a "
            "spline for age, which readings, one recall day or the mean of two. <bookmark mark='c'/> The "
            "pre-specified analysis is in gold, near the middle. <bookmark mark='d'/> The sixty-four slopes run from "
            "minus point one eight to plus point six four, and not one is distinguishable from zero. The estimates "
            "include both signs. None of these sixty-four intervals excludes zero."
        ) as vo:
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Create(b), FadeIn(p)) for b, p in zip(bars, dots)], lag_ratio=0.03), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(names), FadeIn(grid), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(dots[prim], color=SALT, scale_factor=2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(1.0)
        self.clear_scene()

    def which(self):
        d = load("spec")
        means = {}
        for a in d["axes"]:
            on = [r["est"] for r in d["runs"] if r["spec"][a] == ON[a]]
            off = [r["est"] for r in d["runs"] if r["spec"][a] != ON[a]]
            means[a] = (float(np.mean(off)), float(np.mean(on)))
        order = sorted(d["axes"], key=lambda a: -abs(means[a][1] - means[a][0]))
        rows = VGroup(*[label(rf"{AXIS_NAMES[a]}: \ {means[a][0]:+.2f} $\to$ {means[a][1]:+.2f}", font_size=24,
                              color=SALT if k < 2 else GREY_A) for k, a in enumerate(order)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.3, 0])
        head = label(r"average slope without $\to$ with each choice", font_size=28).to_edge(UP, buff=0.6)
        foot = label(r"the two that matter: \ who is in the sample, \ and how sodium is measured", font_size=24, color=OBS).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> Which choices move the answer most? Average the slope over the analyses with and "
            "without each choice. <bookmark mark='b'/> Two stand out. Including people on blood-pressure medicine "
            "pulls the slope down, from about plus point two zero to minus point zero seven. Using the mean of two "
            "recall days instead of one pushes it up, by about a tenth. <bookmark mark='c'/> Weights, the age spline,"
            " energy and the readings rule barely matter. <bookmark mark='d'/> The choices that matter are about who "
            "is in the sample and how the exposure is measured. Both point to the next two problems."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2), FadeIn(rows[1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[2:]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def two_days(self):
        d = load("meas")
        a, b = np.asarray(d["day1"]), np.asarray(d["day2"])
        A = axes([0, 10], [0, 10], x_length=4.8, y_length=4.8, xlabel=r"sodium, \ day 1, \ g", ylabel=r"sodium, \ day 2, \ g",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 2, 4, 6, 8, 10], center=[-3.2, 0.1, 0], font_size=18)
        ax = A.ax
        m = (a < 10) & (b < 10)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.035, color=SALT, fill_opacity=0.7) for x, y in zip(a[m], b[m])])
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(10, 10), color=GREY_C, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(rf"{d['n2']:,} adults with two reliable recalls", font_size=22),
            label(rf"correlation \ $r = {d['reliability']:.2f}$", font_size=26, color=SALT),
            label(rf"SD of one day: \ {d['sd_day1']:.2f} g; \ of day-to-day change: \ {d['sd_diff']:.2f} g", font_size=22),
            label(r"independent replicate errors imply substantial within-person variation", font_size=22, color=RES),
            label(r"$r$ equals reliability only with independent equal-variance replicate errors", font_size=22, color=OBS),
        ), 5.6, 0.42, [3.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two thousand six hundred and fifty-nine adults in our analytic sample supplied two "
            "reliable recalls, usually several days apart. This unweighted scatter compares their reported sodium. "
            "<bookmark mark='b'/> The correlation is point three two. <bookmark mark='c'/> The standard deviation of "
            "a single day is one point seven six grams, and the standard deviation of the day difference divided by "
            "root two is one point four two. <bookmark mark='d'/> Under independent replicate errors, that difference"
            " measures within-person variation. <bookmark mark='e'/> Calling the correlation a reliability requires "
            "equal replicate error variances and no shared reporting error. Two days alone cannot verify those "
            "assumptions."
        ) as vo:
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.002), FadeIn(rows[0]), run_time=2.5)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def attenuation(self):
        d = load("meas")
        rows = [
            cmath(r"W", r"=", r"X + U", font_size=32),
            cmath(r"\hat\beta_W", r"\to", r"\lambda\,\beta_X,\ \ \lambda = \frac{\mathrm{Var}(X \mid Z)}{\mathrm{Var}(W \mid Z)}", font_size=30),
            cmath(r"\lambda, \ \text{given age, \ sex, \ BMI}", r"\approx", rf"{d['lam_noenergy']:.2f}", font_size=30),
            cmath(r"\lambda, \ \text{given energy too}", r"\approx", rf"{d['lam']:.2f}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"recalled day $=$ usual intake $+$ that day's noise"), why(r"Part 12: \ attenuation, \ given the covariates $Z$"),
                why(r"a slope shrinks to a quarter"), why(r"a weak calibration slope; \ noisy energy and correlated errors complicate it")]
        intro = label('Classical attenuation needs explicit measurement assumptions', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> In the classical model, a recalled day W is usual intake X plus independent "
            "mean-zero noise U. <bookmark mark='b'/> With accurately measured covariates Z and the appropriate linear"
            " mean model, the sodium coefficient is attenuated by the residual reliability lambda. <bookmark "
            "mark='c'/> Predicting the second day from the first, age, sex and BMI with the two-day dietary weights "
            "gives a calibration coefficient near point two four. <bookmark mark='d'/> Adding recall-day energy "
            "reduces it to point zero six. That is weak calibration, not proof that precisely ninety-four percent of "
            "the remaining sodium is noise: energy is noisy too, and its reporting error can correlate with sodium's."
            " The attenuation interpretation needs assumptions these data cannot establish."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def calibration(self):
        d = load("meas")
        t = load("model")["t"]
        items = [(r"day 1, \ energy-adjusted (the plan)", d["naive"], d["naive_se"], SALT),
                 (r"day 1, \ no energy", d["naive_noenergy"], d["naive_noenergy_se"], GREY_A),
                 (r"calibrated, \ no energy", d["calib_noenergy"], d["calib_noenergy_se"], DES)]
        A = axes([-2, 4], [0, 3.6], x_length=8.2, y_length=3.2, xlabel=r"mm Hg per g/day", xticks=[-2, -1, 0, 1, 2, 3, 4],
                 center=[2.4, 0.9, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 3.6), color=GREY_C, stroke_width=1.5)
        trial = Rectangle(width=ax.c2p(3, 0)[0] - ax.c2p(2, 0)[0], height=ax.c2p(0, 3.4)[1] - ax.c2p(0, 0.2)[1], stroke_width=0,
                          fill_color=HIT, fill_opacity=0.2).move_to(ax.c2p(2.5, 1.8))
        lines, labs = VGroup(), VGroup()
        for k, (txt, b, s, c) in enumerate(items):
            y = 3 - k
            lines.add(VGroup(Line(ax.c2p(max(-2, b - t * s), y), ax.c2p(min(4, b + t * s), y), color=c, stroke_width=6),
                             Dot(ax.c2p(b, y), radius=0.08, color=c)))
            lb = label(txt + rf": \ {b:+.2f} $\pm$ {t * s:.2f}", font_size=19, color=c)
            if lb.width > 4.3:
                lb.width = 4.3
            labs.add(lb.next_to(ax.c2p(-2, y), LEFT, buff=0.15))
        rows = fit_rows(VGroup(
            label(r"regression calibration: \ replace day 1 by $E[\,\text{day 2} \mid \text{day 1}, Z\,]$", font_size=22),
            label(rf"with energy too: \ ${d['calib']:+.2f} \pm {t * d['calib_se']:.1f}$, \ weak calibration", font_size=22, color=RES),
            label(r"two-stage uncertainty included; \ weak calibration limits the approximation", font_size=24, color=OBS),
        ), 12.4, 0.3, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Regression calibration replaces the first recall by its linear prediction from a "
            "second recall and the model covariates. We use the CDC's two-day dietary weights and jointly linearize "
            "both regressions, so the interval accounts for estimating the calibration equation. <bookmark mark='b'/>"
            " Gold is the primary recall-day estimate, grey the estimate without energy. <bookmark mark='c'/> Blue is"
            " calibration without energy: plus point three seven, with an approximate interval from minus one point "
            "nine to plus two point seven. <bookmark mark='d'/> With energy, the estimate is plus point six five and "
            "the delta-method margin is about eight point seven, wider than this axis. Such weak calibration makes "
            "even that approximation fragile. <bookmark mark='e'/> These exploratory corrections are imprecise and "
            "assumption-dependent. They do not establish agreement or disagreement with a particular trial; they show"
            " how much uncertainty a single recalled day leaves."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(trial))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lines[0]), FadeIn(labs[0]), Create(lines[1]), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(labs[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def verdict(self):
        rows = fit_rows(VGroup(
            label(r"64 specified alternatives: \ all compatible with zero", font_size=24, color=DES),
            label(r"two recalls: \ weak conditional calibration, \ with unverified error assumptions", font_size=24, color=SALT),
            label(r"exploratory calibration: \ broad approximate intervals, \ weak first stage", font_size=24, color=OBS),
            label(r"a better survey: \ several recall days, \ or 24-hour urine collections", font_size=24, color=HIT),
            label(r"INTERSALT (1988): \ urine in 10,079 people, \ 52 centres", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        intro = label('Replicate measurements help only under an adequate error model', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The sixty-four specified alternatives all remain compatible with zero. <bookmark "
            "mark='b'/> The two-recall correlation and the small conditional calibration slope raise serious "
            "measurement concerns. <bookmark mark='c'/> Correcting under a classical replicate model produces broad, "
            "approximate intervals; shared reporting error, noisy energy and weak calibration remain limitations. "
            "<bookmark mark='d'/> Better measurement could include more recall days or repeated twenty-four-hour "
            "urine collections, with attention to collection completeness. <bookmark mark='e'/> INTERSALT collected "
            "urine in ten thousand and seventy-nine adults across fifty-two centres. It found an ecological "
            "association between sodium and the rise of pressure with age; that cross-centre comparison alone does "
            "not establish an individual causal effect."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
