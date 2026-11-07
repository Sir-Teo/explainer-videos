from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


class Weak(VoiceoverScene):
    def construct(self):
        self.card()
        self.one()
        self.spread()
        self.size()
        self.rules()
        self.ar()
        self.arset()

    def card(self):
        card = chapter_card(3, r"Weak instruments", r"When the nudge is too small to measure",
                            lit=(1995, 1997, 2022), part=PART)
        with self.voiceover("Chapter three. Weak instruments."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def one(self):
        d = load("iv")
        s = d["sample1"]
        ar = d["ar"]
        rows = fit_rows(VGroup(
            label(r"one realistic study: \ 5,000 adults from the survey, \ quarter 1 as the instrument", font_size=26),
            label(rf"first-stage $F$ = {s['F']:.1f}", font_size=26, color=IVC),
            label(rf"2SLS: \ {s['beta']:.3f}, \ 90\% CI {s['ci'][0]:.3f} to {s['ci'][1]:.3f}", font_size=26, color=TAUC),
            label(rf"OLS: \ {s['ols']:.3f}; \ the truth: \ {d['truth']:.3f}", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The full survey has two hundred thousand people. A realistic study might have five "
            "thousand. <bookmark mark='b'/> In one such sample, the first-stage F statistic, which measures how strongly the "
            "instrument predicts schooling, is " + say(s["F"], 1) + ". <bookmark mark='c'/> Two-stage least squares says "
            + say(s["beta"], 3) + ", with an interval from about zero to " + say(s["ci"][1], 2) + ". <bookmark mark='d'/> "
            "Ordinary least squares says " + say(s["ols"], 2) + ". With an instrument this weak, can the interval be trusted?"
        ) as vo:
            self.add(survey_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def spread(self):
        d = load("weak")
        e = np.asarray(d["edges"], float)
        h = np.asarray(d["h1"], float)
        A = axes([-0.3, 0.5], [0, 0.12], x_length=8.0, y_length=4.0, xlabel=r"2SLS estimate of the return to a year of school",
                 ylabel=r"share of surveys", xticks=[-0.2, 0, 0.075, 0.2, 0.4], yticks=[0, 0.05, 0.1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-1.6, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, e, h / d["reps"], color=IVC, opacity=0.6)
        truth = DashedLine(ax.c2p(d["truth"], 0), ax.c2p(d["truth"], 0.12), color=TRUEC, stroke_width=3)
        ols = DashedLine(ax.c2p(d["med_ols"], 0), ax.c2p(d["med_ols"], 0.12), color=MISSC, stroke_width=3)
        side = fit_rows(VGroup(
            label(rf"{d['reps']:,} surveys of 5,000", font_size=22),
            label(rf"median $F$: \ {d['medF1']:.1f}; \ below 10 in {100 * d['share_F_below_10']:.0f}\%", font_size=22, color=IVC),
            label(rf"middle half: \ {d['iqr1'][0]:.3f} to {d['iqr1'][1]:.3f}", font_size=22, color=TAUC),
            label(rf"gold: truth; \ red: OLS; \ tails outside view: {d['outside_view']['one']} / {d['reps']}", font_size=22, color=GREY_A),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Draw a thousand such surveys from the World. <bookmark mark='b'/> The median first-stage F "
            "is " + say(d["medF1"], 1) + ", and in " + str(round(100 * d["share_F_below_10"])) + " percent of surveys it is "
            "below ten. <bookmark mark='c'/> The estimates are centred near the truth, but their spread is enormous: the "
            "middle half runs from about one percent to twelve percent a year, and the tails reach far beyond the axes, in "
            "both directions. <bookmark mark='d'/> A weak instrument does not only make the estimate noisy. Its distribution "
            "is not normal, so the usual interval can mislead."
        ) as vo:
            self.add(survey_tag())
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars), Create(truth), Create(ols), FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def size(self):
        d = load("weak")["size"]
        mu = np.log2(np.asarray(d["mu2"], float))
        A = axes([0, 7], [0, 0.2], x_length=7.6, y_length=4.2, xlabel=r"instrument strength $\mu^2$ \ ($F \approx 1 + \mu^2$)",
                 ylabel=r"rejection rate of a 5\% test", xticks=[0, 2, 4, 6], yticks=[0, 0.05, 0.1, 0.15, 0.2],
                 xfmt=lambda v: f"{2 ** v:g}", yfmt=lambda v: f"{v:g}", center=[-1.8, 0.2, 0])
        ax = A.ax
        cols = {"0.2": Y0C, "0.5": TAUC, "0.9": MISSC}
        lines = VGroup(*[polyline(ax, mu, d["size"][k], c, 3.5) for k, c in cols.items()])
        nom = DashedLine(ax.c2p(0, 0.05), ax.c2p(7, 0.05), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"the 2SLS $t$-test, \ one instrument", font_size=22),
            label(r"blue: \ endogeneity $\rho = 0.2$", font_size=22, color=Y0C),
            label(r"gold: \ $\rho = 0.5$", font_size=22, color=TAUC),
            label(r"red: \ $\rho = 0.9$: \ 16\% at $\mu^2 = 1$", font_size=22, color=MISSC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How badly depends on two things: the instrument's strength, measured by the concentration "
            "parameter mu squared, roughly the first-stage F minus one, and how strongly the treatment is confounded. Here is "
            "the true rejection rate of the nominal five percent test of the two-stage least squares estimate, with one "
            "instrument. <bookmark mark='b'/> With mild confounding the test is conservative. <bookmark mark='c'/> With "
            "moderate confounding it is about right. <bookmark mark='d'/> With strong confounding and a weak instrument it "
            "rejects a true null three times too often, and the estimate is pulled towards ordinary least squares. The "
            "World's survey sits near the middle line, which is why its single-instrument intervals were not far wrong."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(side[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(Create(lines[k]), FadeIn(side[k + 1]))
        self.clear_scene()

    def rules(self):
        rows = fit_rows(VGroup(
            label(r"Staiger \& Stock (1997): \ worry if the first-stage $F$ is below 10", font_size=26, color=IVC),
            label(r"Stock \& Yogo (2005): \ critical values for bias and size, \ by the number of instruments", font_size=26),
            label(r"Lee, \ McCrary, \ Moreira \& Porter (2022): \ just-identified Gaussian approximation: \ 1.96 needs $F>104.7$", font_size=26, color=MISSC),
            label(r"their $tF$ procedure: \ at $F = 10$, \ reject only if $|t| > 3.43$", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Practice settled on a rule of thumb from Douglas Staiger and James Stock in 1997: "
            "worry if the first-stage F is below ten. <bookmark mark='b'/> Stock and Motohiro Yogo turned it into "
            "critical values that limit the bias or the size distortion, depending on the number of instruments. "
            "<bookmark mark='c'/> In 2022 David Lee, Justin McCrary, Marcelo Moreira and Jack Porter showed that ten "
            "is far too lenient for the usual interval: in their just-identified Gaussian weak-instrument "
            "approximation, using the usual one point nine six critical value at five percent regardless of "
            "endogeneity requires the F must exceed one hundred and four point seven. <bookmark mark='d'/> Their tF "
            "procedure adjusts the critical value to the observed F: at an F of ten, the t statistic must exceed "
            "three point four three."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ar(self):
        rows = [
            cmath(r"H_0", r":", r"\beta = b_0", font_size=32),
            cmath(r"Y - b_0 D", r"=", r"W\gamma + Z\delta + \text{error}", font_size=32),
            cmath(r"\text{under } H_0", r":", r"\delta = 0 \text{ exactly, \ however weak } Z \text{ is}", font_size=30),
            cmath(r"\text{AR set}", r"=", r"\{\, b_0 : \text{the } F\text{-test of } \delta = 0 \text{ does not reject} \,\}", font_size=30),
        ]
        rows[3][-1].set_color(BANDC)
        whys = [why(r"each candidate value in turn"), why(r"subtract the hypothesized effect"),
                why(r"exact Gaussian homoskedastic linear-IV reference"), why(r"invert the test")]
        with self.voiceover(
            "<bookmark mark='a'/> The cure is older than the problem. In 1949, Theodore Anderson and Herman Rubin "
            "proposed testing each candidate value of the effect directly. <bookmark mark='b'/> Subtract the "
            "hypothesized effect of the treatment from the outcome, and regress what is left on the instruments. "
            "<bookmark mark='c'/> If the hypothesis is true, the instruments' coefficients are exactly zero, by the "
            "exclusion restriction, whatever their strength. With a valid constant-effect linear IV model and "
            "independent homoskedastic Gaussian errors conditional on the instruments and controls, the F test has "
            "exact size regardless of instrument strength. Heteroskedastic errors need a robust AR procedure. "
            "<bookmark mark='d'/> The confidence set is every value the test does not reject."
        ) as vo:
            intro=label('Anderson-Rubin inversion requires a specified linear-IV error model',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def arset(self):
        d = load("iv")
        w = load("weak")
        ar = d["ar"]
        A = axes([-0.3, 0.5], [0, 1], x_length=7.6, y_length=3.8, xlabel=r"hypothesized return $b_0$", ylabel=r"AR $p$-value",
                 xticks=[-0.2, 0, 0.2, 0.4], yticks=[0, 0.1, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-1.8, 0.4, 0])
        ax = A.ax
        pc = polyline(ax, ar["grid"], ar["p"], IVC, 3.5)
        cut = DashedLine(ax.c2p(-0.3, 0.1), ax.c2p(0.5, 0.1), color=GREY_B, stroke_width=2)
        seg = Line(ax.c2p(ar["lo"], 0.03), ax.c2p(ar["hi"], 0.03), color=BANDC, stroke_width=8)
        k = w["ar_kinds"]
        n = sum(k.values())
        side = fit_rows(VGroup(
            label(rf"this study: \ {ar['lo']:.3f} to {ar['hi']:.3f}", font_size=22, color=BANDC),
            label(rf"across {n:,} surveys: \ an interval in {100 * k['interval'] / n:.0f}\%", font_size=22),
            label(rf"two rays in {100 * k['outside'] / n:.0f}\%; \ the whole line in {100 * k['line'] / n:.0f}\%", font_size=22, color=MISSC),
            label(r"an honest answer: \ the data cannot rule out much", font_size=22, color=TAUC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In our study of five thousand, the Anderson-Rubin p-value across candidate returns gives "
            "the set from about minus five percent to nineteen percent: wider than the two-stage interval. <bookmark "
            "mark='b'/> Across a thousand surveys, the set is an interval in three quarters of them. <bookmark mark='c'/> "
            "Otherwise it is two rays running off to infinity, or the whole real line. <bookmark mark='d'/> That is not a "
            "flaw. When the instrument barely moves the treatment, the data really cannot rule out much, and an interval that "
            "says so is telling the truth."
        ) as vo:
            self.add(survey_tag())
            self.play(FadeIn(A), Create(cut))
            vo.wait_until("a")
            self.play(Create(pc), FadeIn(seg), FadeIn(side[0]))
            for k_, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k_ + 1]))
        self.clear_scene()
