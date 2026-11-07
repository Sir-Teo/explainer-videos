from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


class Panel(VoiceoverScene):
    def construct(self):
        self.card()
        self.within()
        self.numbers()
        self.limits()
        self.nickell()
        self.hist()
        self.fix()

    def card(self):
        card = chapter_card(13, r"Panel data", r"What fixed effects remove, \ and what they add", lit=(1978, 1981), part=PART)
        with self.voiceover("Chapter thirteen. Panel data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def within(self):
        rows = [
            cmath(r"y_{it}", r"=", r"\beta x_{it} + \alpha_i + \varepsilon_{it}", font_size=32),
            cmath(r"\ddot y_{it}", r"=", r"y_{it} - \bar y_{i\cdot} = \beta\, \ddot x_{it} + \ddot\varepsilon_{it}", font_size=32),
            cmath(r"\hat\beta_{\text{FE}}", r"=", r"\text{OLS with a dummy for every unit} \ \text{(FWL, Part 12)}", font_size=30),
            cmath(r"\text{Mundlak (1978)}", r":", r"\text{add } \bar x_{i\cdot} \text{ as a regressor: \ the same } \hat\beta", font_size=30),
        ]
        rows[1][-1].set_color(BANDC)
        whys = [why(r"$\alpha_i$: \ anything fixed about unit $i$"), why(r"the within transformation"),
                why(r"Frisch--Waugh--Lovell"), why(r"the bridge to random effects")]
        with self.voiceover(
            "<bookmark mark='a'/> With repeated observations of the same units, a panel, every unit can carry its own"
            " intercept alpha i: a time-invariant additive contribution to the outcome. Nonadditive unit "
            "heterogeneity is not generally removed by one intercept. <bookmark mark='b'/> Subtracting each unit's "
            "own average removes it. Only changes within a unit identify the effect. <bookmark mark='c'/> By the "
            "Frisch-Waugh-Lovell theorem of Part twelve, this is exactly ordinary least squares with a dummy variable"
            " for every unit. <bookmark mark='d'/> And Yair Mundlak showed in 1978 that adding each unit's average of"
            " x as a regressor gives the same slope, which links fixed effects to the random-effects models of Part "
            "twenty-five."
        ) as vo:
            intro=label('Within-unit demeaning removes an additive fixed intercept',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def numbers(self):
        d = load("panel")
        rows = [[r"estimator", r"slope"],
                [r"pooled OLS", f"{d['pooled']:.3f}"],
                [r"within (fixed effects)", f"{d['fe']:.3f}"],
                [r"300 unit dummies", f"{d['lsdv']:.3f}"],
                [r"Mundlak: \ add $\bar x_{i\cdot}$", f"{d['mundlak']:.3f}"],
                [r"truth", f"{d['truth']:.3f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.2, row_buff=0.3, colors=[GREY_A, MISSC, BANDC, BANDC, BANDC, TRUEC]).move_to([0, 0.7, 0])
        foot = label(r"300 units, \ 8 periods; \ $x_{it}=0.8\alpha_i+\nu_{it}$, \ $\alpha_i$ enters $y$ with weight 2", font_size=22, color=GREY_A).move_to([0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A seeded panel: three hundred units, eight periods, and an x that is correlated with each "
            "unit's fixed characteristic, which also raises y. <bookmark mark='b'/> Pooled least squares, ignoring the "
            "units, says " + say(d["pooled"], 2) + ", nearly double the truth. <bookmark mark='c'/> The within estimator, "
            "three hundred dummies, and Mundlak's regression all give the same number, " + say(d["fe"], 3) + ", to the last "
            "decimal. The truth is one."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[5]), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[2:5]], lag_ratio=0.3))
        self.clear_scene()

    def limits(self):
        rows = fit_rows(VGroup(
            label(r"fixed effects remove what is fixed: \ not what changes over time", font_size=26, color=TAUC),
            label(r"they amplify measurement error: \ within-unit changes in $x$ are mostly noise", font_size=26, color=MISSC),
            label(r"they need strict exogeneity: \ today's $\varepsilon$ may not affect tomorrow's $x$", font_size=26, color=MISSC),
            label(r"and with a lagged outcome as a regressor, \ they are biased by construction", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fixed effects remove confounders that do not change. Anything that changes over time "
            "within a unit, and drives both x and y, remains. <bookmark mark='b'/> They amplify measurement error: if x "
            "barely changes within units, most of the change that remains is noise, and the slope is attenuated, Part "
            "twenty-three's errors in variables. <bookmark mark='c'/> They need strict exogeneity: the errors in any period "
            "must be unrelated to x in every period, so feedback from outcomes to later treatment breaks them. <bookmark "
            "mark='d'/> And with the lagged outcome as a regressor, they are biased by construction."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def nickell(self):
        d = load("panel")["nickell"]
        rows = [
            cmath(r"y_{it}", r"=", r"\rho\, y_{i,t-1} + \alpha_i + \varepsilon_{it}", font_size=32),
            cmath(r"\ddot y_{i,t-1}", r"=", r"y_{i,t-1} - \overline{y_{i,t-1}}, \ \text{whose average} \text{ contains } \varepsilon_{it}", font_size=30),
            cmath(r"\text{plim}\ \hat\rho_{\text{FE}} - \rho", r"\approx", r"-\dfrac{1 + \rho}{T - 1} \quad \text{(fixed } T,\ N \to \infty)", font_size=30),
            cmath(r"\rho = 0.5,\ T = 5", r":", rf"\text{{Nickell's formula gives }} {d['formula']:.3f}", font_size=30),
        ]
        rows[2][-1].set_color(MISSC)
        whys = [why(r"a dynamic panel"), why(r"the demeaned regressor and error correlate"),
                why(r"Nickell (1981)"), why(r"exact in $T$, \ not just the leading term")]
        with self.voiceover(
            "<bookmark mark='a'/> In a dynamic panel, this year's outcome depends on last year's, and on a unit effect. "
            "<bookmark mark='b'/> Demeaning subtracts each unit's average, and that average contains this year's error, so "
            "the demeaned lagged outcome is correlated with the demeaned error. <bookmark mark='c'/> Stephen Nickell showed "
            "in 1981 that the bias does not vanish as the number of units grows. It is roughly minus one plus rho, over T "
            "minus one. <bookmark mark='d'/> With rho a half and five periods, the formula predicts the fixed-effects "
            "estimate will converge to " + say(d["formula"], 2) + ", not to point five."
        ) as vo:
            intro=label('Demeaning a dynamic panel correlates regressors and errors',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hist(self):
        d = load("panel")["nickell"]
        e = np.linspace(0, 1, 41)
        hf, ha = np.asarray(d["hist_fe"], float), np.asarray(d["hist_ah"], float)
        A = axes([0, 1], [0, 0.5], x_length=7.6, y_length=4.0, xlabel=r"estimate of $\rho$ \ (truth 0.5)", ylabel=r"share",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-1.8, 0.2, 0])
        ax = A.ax
        bf = hist_bars(ax, e, hf / hf.sum(), color=MISSC, opacity=0.6)
        ba = hist_bars(ax, e, ha / ha.sum(), color=BANDC, opacity=0.5)
        truth = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, 0.5), color=TRUEC, stroke_width=3)
        side = fit_rows(VGroup(
            label(r"500 panels: \ 500 units, \ 5 periods", font_size=22),
            label(rf"red: \ fixed effects, \ mean {d['fe_mean']:.3f}", font_size=22, color=MISSC),
            label(rf"Nickell's formula: \ {d['formula']:.3f}", font_size=22, color=GREY_A),
            label(rf"green: \ Anderson--Hsiao, \ mean {d['ah_mean']:.3f} \ (SD {d['ah_sd']:.3f})", font_size=22, color=BANDC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Five hundred simulated panels of five hundred units and five periods. <bookmark mark='b'/> "
            "The fixed-effects estimates cluster tightly around " + say(d["fe_mean"], 2) + ", <bookmark mark='c'/> exactly "
            "where Nickell's formula says, " + say(d["formula"], 2) + ", and nowhere near the truth. The large sample makes "
            "the wrong answer precise. <bookmark mark='d'/> The estimator of Theodore Anderson and Cheng Hsiao, from 1981, "
            "is centred on the truth, at the price of three times the spread."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(truth), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bf), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(ba), FadeIn(side[3]))
        self.clear_scene()

    def fix(self):
        rows = [
            cmath(r"\Delta y_{it}", r"=", r"\rho\, \Delta y_{i,t-1} + \Delta\varepsilon_{it}", font_size=32),
            cmath(r"\text{instrument}", r":", r"y_{i,t-2} \ \text{(requires valid serial-error and initial-condition moments)}", font_size=30),
            cmath(r"\text{Arellano--Bond (1991)}", r":", r"\text{all earlier lags, \ by GMM}", font_size=30),
            cmath(r"\text{caution}", r":", r"\text{many weak instruments again (chapter 4)}", font_size=30),
        ]
        rows[1][-1].set_color(IVC)
        whys = [why(r"differencing removes $\alpha_i$"), why(r"an instrument from within the panel"),
                why(r"more instruments, \ more precision"), why(r"Roodman (2009): \ too many instruments")]
        with self.voiceover(
            "<bookmark mark='a'/> The fix uses an instrument. First-difference the model, which also removes the unit"
            " effect. <bookmark mark='b'/> The differenced lag is correlated with the differenced error, but with "
            "serially uncorrelated idiosyncratic errors and the required initial-condition moments, the outcome two "
            "periods back is uncorrelated with that differenced error, so it can serve as an instrument: Anderson and"
            " Hsiao. <bookmark mark='c'/> Manuel Arellano and Stephen Bond, in 1991, used all the earlier lags at "
            "once, by the generalized method of moments. <bookmark mark='d'/> And the number of instruments then "
            "grows with the number of periods, which brings back chapter four: with too many, the estimate drifts "
            "back towards the biased one."
        ) as vo:
            intro=label('Lagged instruments require valid serial-error moment conditions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
