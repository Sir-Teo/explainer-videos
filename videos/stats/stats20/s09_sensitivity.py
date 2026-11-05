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
        A = axes([0, n + 1], [-1, 1.4], x_length=10.6, y_length=3.0, xlabel=r"", ylabel=r"sodium slope, \ mm Hg per g",
                 yticks=[-1, -0.5, 0, 0.5, 1], center=[0.3, 1.5, 0], font_size=18)
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(n + 1, 0), color=GREY_C, stroke_width=1.5)
        prim = next(i for i, r in enumerate(runs) if r["spec"] == {"meds": "exclude", "energy": True, "weights": True,
                                                                    "age_spline": False, "readings": "2+", "exposure": "day1"})
        bars, dots = VGroup(), VGroup()
        for i, r in enumerate(runs):
            c = SALT if i == prim else DES
            bars.add(Line(ax.c2p(i + 1, max(-1, r["est"] - 2 * r["se"])), ax.c2p(i + 1, min(1.4, r["est"] + 2 * r["se"])),
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
            "The plan promised all sixty-four analyses. Here they are: a specification curve, as Uri Simonsohn "
            "and colleagues called it. <bookmark mark='a'/> Each dot is one analysis's sodium slope, sorted from smallest to "
            "largest, with bars of two standard errors. <bookmark mark='b'/> Below, which choices it made: medicine users "
            "in or out, energy in the model or not, weights or not, a spline for age, which readings, one recall day or the "
            "mean of two. <bookmark mark='c'/> The pre-specified analysis is in gold, near the middle. <bookmark mark='d'/> The "
            "sixty-four slopes run from minus point one nine to plus point six two, and not one is distinguishable from zero. "
            "No choice among these rescues a large effect, or produces a negative one."
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
            "<bookmark mark='a'/> Which choices move the answer most? Average the slope over the analyses with and without "
            "each choice. <bookmark mark='b'/> Two stand out. Including people on blood-pressure medicine pulls the slope down, "
            "from about plus point two one to minus point zero eight. Using the mean of two recall days instead of one pushes "
            "it up, by about a tenth. <bookmark mark='c'/> Weights, the age spline, energy and the readings rule barely matter. "
            "<bookmark mark='d'/> The choices that matter are about who is in the sample and how the exposure is measured. "
            "Both point to the next two problems."
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
            label(r"most of one day's variation is that day, \ not the person", font_size=22, color=RES),
            label(r"reliability $\lambda = \mathrm{Var}(X) / \mathrm{Var}(W)$: \ about 0.32", font_size=22, color=OBS),
        ), 5.6, 0.42, [3.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now the exposure. Two thousand six hundred and fifty-nine adults in our sample had a second "
            "reliable recall, three to ten days after the first. Here is each person's day two against their day one. "
            "<bookmark mark='b'/> If one day measured usual intake well, the points would hug the diagonal. They don't: the "
            "correlation is point three two. <bookmark mark='c'/> The day-to-day swing within a person is larger than the "
            "spread between people. <bookmark mark='d'/> So most of the variation in one day's sodium belongs to that "
            "day. <bookmark mark='e'/> In Part 12's language of errors in x, the reliability, the share of the variance that is "
            "real differences between people, is about a third."
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
                why(r"a slope shrinks to a quarter"), why(r"energy explains the real part: \ what's left is noise")]
        with self.voiceover(
            "<bookmark mark='a'/> Write one day's sodium, W, as usual intake X plus that day's noise U. <bookmark mark='b'/> "
            "Part 12 showed that regressing on W instead of X shrinks the slope by the reliability lambda, here computed after "
            "allowing for the other covariates. <bookmark mark='c'/> Given age, sex and BMI, lambda is about point two four: "
            "a true slope would show up at a quarter of its size. <bookmark mark='d'/> And given energy as well, lambda is "
            "point zero six. Energy explains most of the real differences in people's sodium, since people who eat more eat "
            "more salt, and what's left in one day's sodium, once energy is fixed, is ninety-four percent noise. The "
            "pre-specified model, by adjusting for energy, made itself almost blind to sodium."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
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
            label(r"with energy too: \ $+0.60 \pm 9.2$, \ almost no information", font_size=22, color=RES),
            label(r"corrected, \ the survey agrees with zero \emph{and} with the trials", font_size=24, color=OBS),
        ), 12.4, 0.3, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Can we correct for it? Regression calibration, from Raymond Carroll and colleagues, uses the "
            "second day: since its noise is independent of the first day's, predicting day two from day one and the "
            "covariates estimates each person's usual intake. Fit the outcome model to that prediction. <bookmark mark='b'/> "
            "In gold, the plan's estimate; in grey, the same without energy. <bookmark mark='c'/> In blue, calibrated: plus "
            "point six zero, with an interval from about minus two to plus three. <bookmark mark='d'/> With energy in the model "
            "the calibrated interval is wider than this whole axis. <bookmark mark='e'/> So once measurement error is faced "
            "honestly, the survey no longer contradicts the trials. It's consistent with no effect and with the trials' effect "
            "alike: one day of diet simply can't tell them apart."
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
            label(r"64 reasonable analyses: \ all near zero", font_size=24, color=DES),
            label(r"but one day's sodium is two-thirds noise, \ and 94\% once energy is fixed", font_size=24, color=SALT),
            label(r"corrected, \ the interval covers both zero and the trials", font_size=24, color=OBS),
            label(r"a better survey: \ several recall days, \ or 24-hour urine collections", font_size=24, color=HIT),
            label(r"INTERSALT (1988): \ urine in 10,079 people, \ 52 centres", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: across sixty-four reasonable analyses, the slope stays near zero. <bookmark mark='b'/> But "
            "the exposure is mostly noise, two-thirds of it, and nearly all of it once energy is held fixed. "
            "<bookmark mark='c'/> Corrected for that, the survey can't distinguish zero from the trials' effect. "
            "<bookmark mark='d'/> A study designed for this question would measure usual intake better: many recall days, or "
            "better, collecting each person's urine for twenty-four hours, since nearly all the sodium we eat leaves that way. "
            "<bookmark mark='e'/> The INTERSALT study of 1988 did exactly that, for ten thousand people in fifty-two centres "
            "around the world, and found that pressure rose with age faster where people ate more salt."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
