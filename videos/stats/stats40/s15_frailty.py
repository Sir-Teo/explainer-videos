from __future__ import annotations

import numpy as np
from scipy import stats as st

from videos.stats.stats40.common import *  # noqa: F403


class Frailty(VoiceoverScene):
    def construct(self):
        self.card()
        self.vaupel()
        self.deceleration()
        self.shared()
        self.kidney()
        self.recurrent()

    def card(self):
        card = chapter_card(14, r"Frailty", r"Unmeasured differences in risk", lit=(1979,), part=PART)
        with self.voiceover("Chapter fourteen. Frailty."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def vaupel(self):
        rows = [
            cmath(r"h(t \mid Z)", r"=", r"Z\, h_0(t), \ \ Z\sim\operatorname{Gamma}(\text{shape }1/\theta,\ \text{scale }\theta)", font_size=32),
            cmath(r"S(t)", r"=", r"E\, e^{-Z H_0(t)} = (1 + \theta H_0(t))^{-1/\theta}", font_size=32),
            cmath(r"h_{\text{pop}}(t)", r"=", r"h_0(t) \big/ (1 + \theta H_0(t)) = E[Z \mid T > t]\, h_0(t)", font_size=30),
            cmath(r"\text{so}", r":", r"\text{selection lowers hazard relative to the individual baseline}", font_size=30),
        ]
        rows[2][-1].set_color(HAZC)
        whys = [why(r"Vaupel, \ Manton \& Stallard (1979)"), why(r"the Laplace transform"), why(r"the survivors' mean frailty"),
                why(r"selection, \ not ageing")]
        with self.voiceover(
            "<bookmark mark='a'/> James Vaupel, Kenneth Manton and Eric Stallard gave the idea a name in 1979: "
            "frailty, an unmeasured factor that multiplies each person's hazard. With a gamma frailty of mean one and"
            " variance theta, <bookmark mark='b'/> the population's survival is the average of individual survivals, "
            "which has a closed form. <bookmark mark='c'/> The population's hazard is the individual baseline times "
            "the mean frailty of the survivors, and that mean falls as the frail die. <bookmark mark='d'/> So "
            "population hazards bend below the baseline even when nobody's own hazard does: selection, not a change "
            "in anyone."
        ) as vo:
            heading = label('Frailty selection lowers hazard relative to the baseline', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def deceleration(self):
        d = load("frailty")
        ages = np.asarray(d["ages"], float)
        hi, hp = np.log10(np.asarray(d["h_ind"], float)), np.log10(np.asarray(d["h_pop"], float))
        A = axes([60, 100], [-2.5, 0], x_length=7.4, y_length=4.2, xlabel=r"age", ylabel=r"cardiovascular hazard \ (log scale)",
                 xticks=[60, 70, 80, 90, 100], yticks=[-2, -1, 0], yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.5, 0.2, 0])
        ax = A.ax
        c1 = polyline(ax, ages, np.clip(hi, -2.5, 0), GREY_B, 3)
        c2 = polyline(ax, ages, np.clip(hp, -2.5, 0), HAZC, 3)
        side = fit_rows(VGroup(
            label(r"the World's cardiovascular hazard, \ from 60", font_size=22),
            label(r"grey: \ an individual with $Z = 1$: \ Gompertz, \ straight", font_size=22, color=GREY_B),
            label(r"orange: \ the surviving population, \ $\theta = 0.6$", font_size=22, color=HAZC),
            label(r"mortality plateaus at extreme ages: \ partly this", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World's cardiovascular hazard from sixty. <bookmark mark='b'/> For any one "
            "person it follows Gompertz's straight line. <bookmark mark='c'/> For the surviving population, with the "
            "World's frailty variance of point six, it bends further and further below the line, as the frail are "
            "removed. <bookmark mark='d'/> The slowing of death rates at the very oldest ages, seen in human and "
            "insect populations, is consistent with this mechanism, although frailty is not the only possible "
            "explanation. And chapter ten's drifting hazard ratio was the same selection at work inside a trial."
        ) as vo:
            self.add(cohort_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def shared(self):
        rows = [
            cmath(r"h_{ij}(t)", r"=", r"Z_i\, h_0(t)\, e^{x_{ij}^\top \beta}: \ Z_i \text{ shared within cluster } i", font_size=30),
            cmath(r"L_i", r"=", r"\textstyle\prod_j (h_{ij}^*)^{\delta_{ij}}\, \tfrac{\theta^{d_i} \Gamma(1/\theta + d_i)}{\Gamma(1/\theta)} (1 + \theta \textstyle\sum_j H_{ij}^*)^{-1/\theta - d_i}", font_size=28),
            cmath(r"\theta", r":", r"\text{the dependence within a cluster \ (Kendall's } \tau = \theta / (\theta + 2))", font_size=30),
            cmath(r"\beta", r":", r"\text{conditional on frailty; distinct from marginal associations}", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"families, \ twins, \ repeated events"), why(r"$h^*_{ij}=h_0e^{x^\top\beta}$, $H^*_{ij}=\int h^*_{ij}$; integrate $Z_i$"), why(r"Clayton (1978)"),
                why(r"Part 25's random effects")]
        with self.voiceover(
            "<bookmark mark='a'/> When frailty is shared, by members of a family, by the two kidneys of a patient, by"
            " the repeated infections of one person, it makes their times dependent. <bookmark mark='b'/> With a "
            "gamma frailty, it integrates out of each cluster's likelihood in closed form. <bookmark mark='c'/> Its "
            "variance theta measures the dependence: David Clayton's model of 1978, whose Kendall's tau is theta over"
            " theta plus two. <bookmark mark='d'/> The coefficients are now conditional on the frailty, Part "
            "twenty-five's random effects for lifetimes, and can differ from population-averaged associations; there "
            "is no universal coefficient ordering under arbitrary covariates or misspecification."
        ) as vo:
            heading = label('Shared frailty models dependence among clustered lifetimes', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def kidney(self):
        d = load("frailty")
        lr = 2 * (d["ll"] - d["ll0"])
        p = 0.5 * st.chi2.sf(lr, 1)
        rows = [[r"kidney catheter infections \ (38 patients, \ 2 each)", r"female HR", r"$\hat\theta$"],
                [r"Cox, \ ignoring the pairing", f"{d['hr_female_cox']:.2f}", r"---"],
                [r"Weibull, \ no frailty", f"{d['hr_female_weibull']:.2f}", r"0"],
                [r"Weibull, \ gamma frailty", f"{d['hr_female_frailty']:.2f}", f"{d['theta']:.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.2, row_buff=0.36, colors=[GREY_A, GREY_B, SURVC, TAUC]).move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(rf"likelihood ratio for $\theta = 0$: \ {lr:.1f} \ ($p = {p:.3f}$, \ half a $\chi^2_1$: \ a boundary)", font_size=24, color=TAUC),
            label(r"sex association conditional on latent frailty; not a within-patient contrast", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Christine McGilchrist and Chris Aisbett's data: thirty-eight dialysis patients, each with "
            "two times to an infection at the catheter site. <bookmark mark='b'/> Ignoring the pairing, women's hazard of "
            "infection is about " + say(d["hr_female_cox"], 1) + " of men's, <bookmark mark='c'/> and a Weibull model "
            "agrees. <bookmark mark='d'/> With a shared gamma frailty, theta is " + say(d["theta"], 2) + ", and the female hazard ratio, now conditional on the latent patient frailty, is " + say(d["hr_female_frailty"], 2) + ". The likelihood ratio "
            "test of no frailty gives " + say(lr, 1) + "; because theta equal zero is on the boundary, the usual asymptotic reference is a half point mass at "
            "zero and half a chi-squared-one distribution; with only thirty-eight clusters this is an approximation, "
            "the boundary problem of variance components once more."
        ) as vo:
            self.add(kidney_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]), FadeIn(foot))
        self.clear_scene()

    def recurrent(self):
        rows = fit_rows(VGroup(
            label(r"recurrent events: \ infections, \ hospital admissions, \ tumour recurrences", font_size=26, color=TAUC),
            label(r"Andersen--Gill: \ one counting process per person, \ robust SEs", font_size=26),
            label(r"Prentice--Williams--Peterson: \ strata by event number; \ Wei--Lin--Weissfeld: \ marginal", font_size=26, color=GREY_A),
            label(r"or a frailty for each person: \ the dependence modelled, \ not just corrected", font_size=26, color=SURVC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Events that can happen again, infections, admissions, recurrences of a tumour, need the "
            "same care. <bookmark mark='b'/> The Andersen-Gill model treats each person's events as one counting process "
            "and corrects the standard errors with a sandwich. <bookmark mark='c'/> Other models stratify by the event's "
            "number, or model each event's time marginally. <bookmark mark='d'/> A person-level frailty models the "
            "dependence instead of merely correcting for it."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
