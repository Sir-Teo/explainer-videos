from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class Impossibility(VoiceoverScene):
    def construct(self):
        self.card()
        self.fieller()
        self.shapes()
        self.table()
        self.gleser()
        self.bliss()
        self.elsewhere()
        self.board()

    def card(self):
        card = chapter_card(7, r"Impossibility: \ Fieller and Gleser--Hwang", r"When every honest interval must sometimes be infinite", lit=(1987,), part=PART)
        with self.voiceover("Chapter seven. Impossibility, from Fieller to Gleser and Hwang: when every honest interval must sometimes be infinite."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def fieller(self):
        rows = [
            cmath(r"a \sim N(\alpha, v_a)", r",", r"\ b \sim N(\beta,v_b), \ \text{jointly normal, known PD covariance};\ \beta\ne0", font_size=34),
            cmath(r"\frac{a - \rho b}{\sqrt{v_a - 2\rho c + \rho^2 v_b}}", r"\sim", r"N(0, 1) \ \text{exactly, \ for the true } \rho", font_size=32),
            cmath(r"C(a, b)", r"=", r"\{\rho : (a - \rho b)^2 \le z^2 (v_a - 2\rho c + \rho^2 v_b)\}", font_size=32),
            cmath(r"\text{a quadratic in } \rho", r":", r"\text{an interval, \ two rays, \ or the whole line}", font_size=32),
        ]
        rows[1][-1].set_color(UMPC)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"a ratio of means"), why(r"a pivot"), why(r"invert it: \ Fieller (1940, 1954)"), why(r"$b^2 - z^2 v_b$ decides")]
        with self.voiceover(
            "<bookmark mark='a'/> Many quantities are ratios: a dose that kills half the beetles, a cost per life "
            "saved, an instrumental-variable effect. Assume jointly normal numerator and denominator estimates with "
            "known positive definite covariance, and a nonzero true denominator. <bookmark mark='b'/> For the true "
            "ratio, a minus rho b is normal with mean zero and a known variance, so this standardized quantity is an "
            "exact pivot. <bookmark mark='c'/> Edgar Fieller inverted it: the confidence set is every rho for which "
            "the pivot is small, <bookmark mark='d'/> a quadratic inequality in rho. Depending on whether the "
            "denominator is clearly away from zero, the set is a bounded interval, the complement of an interval, two"
            " rays running off to infinity, or the entire real line."
        ) as vo:
            heading=label('A joint-normal pivot permits unbounded ratio sets',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def shapes(self):
        A = axes([-6, 6], [-5.5, 5.5], x_length=7.4, y_length=4.4, xlabel=r"$\rho$", ylabel=r"$(a - \rho b)^2 - z^2(v_a + \rho^2 v_b)$, \ scaled",
                 xticks=[-5, 0, 5], yticks=[-5, 0, 5], center=[-2.5, 0.2, 0])
        ax = A.ax
        r = np.linspace(-6, 6, 300)
        z2 = 1.96 ** 2
        cases = [(2.0, 4.0, UMPC), (2.0, 1.5, CIC), (0.3, 0.3, REJC)]
        curves = VGroup()
        for a, b, c in cases:
            q = (a - r * b) ** 2 - z2 * (1 + r ** 2)
            curves.add(polyline(ax, r, 5 * q / np.max(np.abs(q)), c, 4))
        zero = DashedLine(ax.c2p(-6, 0), ax.c2p(6, 0), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"$C$ = where the curve is below 0 \ ($v_a = v_b = 1$)", font_size=22),
            label(r"green: \ $b = 4$: \ an upward parabola: \ a bounded interval", font_size=22, color=UMPC),
            label(r"gold: \ $b = 1.5 < z$: \ downward: \ two rays to $\pm\infty$", font_size=22, color=CIC),
            label(r"red example: \ negative discriminant, \ all of $\mathbb R$", font_size=22, color=REJC),
            label(r"not a failure: \ the data cannot rule those values out", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Plot the quadratic: the confidence set is where it falls below zero. <bookmark "
            "mark='b'/> When the denominator estimate is large compared with its standard error, the parabola opens "
            "upward and the set is an ordinary interval. <bookmark mark='c'/> When its squared estimate is below z "
            "squared times its variance, the parabola opens downward. If the discriminant is positive, the set is "
            "everything outside an interval: arbitrarily large ratios, positive and negative, remain plausible. "
            "<bookmark mark='d'/> In the red example the joint quadratic has negative discriminant and stays below "
            "zero, giving the whole line. Two separately nonsignificant estimates do not by themselves guarantee that"
            " shape. <bookmark mark='e'/> This is not a defect of the method: a weak denominator can require "
            "arbitrarily large ratios to remain in the confidence set. In a probability-zero transition case the "
            "quadratic can reduce to a half-line."
        ) as vo:
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(Create(curves[k]), FadeIn(side[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("fieller")["ratio"]
        rows = [[r"denominator $\beta$ \ (SE 1)", r"bounded", r"two rays", r"all of $\mathbb R$", r"Fieller covers", r"delta method covers"]]
        for beta in ("4.0", "2.0", "1.0", "0.5"):
            r = d[beta]
            k = r["kinds"]
            rows.append([beta, f"{100 * k['bounded']:.0f}\\%", f"{100 * k['exclusive']:.0f}\\%", f"{100 * k['all']:.0f}\\%",
                         f"{100 * r['fieller']:.1f}\\%", f"{100 * r['delta']:.1f}\\%"])
        tab = table_rows(rows, font_size=26, col_buff=0.6, row_buff=0.3, colors=[GREY_A, None, None, None, None, None]).move_to([0, 0.8, 0])
        if tab.width > 13:
            tab.width = 13
        note_ = label(r"$\alpha = 1$, \ $\rho = 1/\beta$; \ 20,000 data sets each; \ nominal 95\%", font_size=24, color=GREY_A).move_to([0, -2.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Simulated, with a numerator of one and denominators of four, two, one, and one half, each with standard error one. <bookmark mark='b'/> With a strong denominator, Fieller's set is almost always an interval, and the delta method's estimate plus or minus 1.96 standard errors does about as well. <bookmark mark='c'/> As the denominator weakens, Fieller's set is more and more often unbounded, but its coverage stays at ninety-five percent, because it is exact. <bookmark mark='d'/> The delta method always reports a finite interval, and its coverage collapses to {100 * d['0.5']['delta']:.0f} percent."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_), FadeIn(exact_tag(r"simulated: 20,000 data sets per row")))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("d")
            self.play(FadeIn(tab[4]))
        self.clear_scene()

    def gleser(self):
        rows = [
            cmath(r"\Theta \ni (\alpha, \beta)", r":", r"\text{including } \beta \text{ near } 0, \text{ where } \rho \text{ is unidentified}", font_size=30),
            cmath(r"C \text{ with } \inf_\theta P_\theta(\rho \in C) \ge 1 - \alpha", r"\Rightarrow", r"P_{(0,0)}(C \text{ unbounded})\ge1-\alpha \ \text{at the limiting law}", font_size=28),
            cmath(r"\text{so}", r":", r"\text{valid interval-valued procedures need infinite expected length in this model}", font_size=32),
            cmath(r"\text{bounded intervals}", r":", r"\inf_\theta \text{coverage} = 0, \ \text{whatever their nominal level}", font_size=30),
        ]
        rows[2][-1].set_color(REJC)
        rows[3][-1].set_color(REJC)
        whys = [why(r"the parameter space"), why(r"Gleser \& Hwang (1987)"), why(r"Pratt's length, \ infinite"), why(r"the delta method, \ Wald")]
        with self.voiceover(
            "<bookmark mark='a'/> Leon Gleser and Gene Hwang proved in 1987 that this is unavoidable. In the normal "
            "ratio problem, with numerator and nonzero denominator allowed to approach zero together along any fixed "
            "ratio, <bookmark mark='b'/> any confidence set whose coverage is at least one minus alpha at every "
            "parameter value cannot be almost surely bounded throughout this model. At the limiting zero-mean "
            "distribution its probability of being unbounded is at least one minus alpha; continuity and common "
            "positive densities connect this limit to the model. <bookmark mark='c'/> For interval-valued procedures "
            "with uniform positive coverage, this forces infinite expected length. Unboundedness alone would not "
            "imply infinite Lebesgue measure for an arbitrary disconnected sparse set. <bookmark mark='d'/> Turned "
            "around: any procedure that always reports a bounded interval, such as the delta method or a Wald "
            "interval, has a worst-case coverage of zero, whatever level it claims."
        ) as vo:
            heading=label('Uniform validity can force unbounded intervals in ratio models',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bliss(self):
        d = load("fieller")["bliss"]
        rows = [
            cmath(r"\text{Bliss's beetles}", r":", r"\text{logit } P(\text{die}) = \beta_0 + \beta_1 \log_{10} \text{dose}", font_size=32),
            cmath(r"\widehat{\log_{10}\mathrm{LD}_{50}}", r"=", rf"-\hat\beta_0 / \hat\beta_1 = {d['ld50']:.4f}; \ \ \hat\beta_1 / \mathrm{{SE}} = {d['z_slope']:.1f}", font_size=32),
            cmath(r"\text{Fieller}", r":", rf"[{d['fieller'][0]:.4f}, \ {d['fieller'][1]:.4f}]; \ \ \text{{delta}}: [{d['delta'][0]:.4f}, \ {d['delta'][1]:.4f}]", font_size=30),
            cmath(r"\text{here}", r":", r"\text{the slope is far from 0, \ so the two agree}", font_size=32),
        ]
        rows[2][-1].set_color(UMPC)
        whys = [why(r"Part 24's LD50"), why(r"a ratio of coefficients"), why(r"asymptotic 95\% log-dose sets"), why(r"Fieller matters when $\beta_1$ is weak")]
        with self.voiceover(
            f"<bookmark mark='a'/> Real data: Bliss's beetles from Part twenty-four, the logistic dose-response curve. <bookmark mark='b'/> The base-ten logarithm of the dose that kills half the beetles is minus the intercept over the slope, a ratio, and the slope is about {d['z_slope']:.0f} standard errors from zero. <bookmark mark='c'/> The reported intervals are on the log-ten dose scale. Their endpoints agree to three decimals. Here the normal approximation and covariance are estimated from a logistic fit, so both intervals are asymptotic rather than exact. <bookmark mark='d'/> That is the general lesson: when the denominator is strong, the delta method is fine; Fieller inversion can retain unbounded sets when needed, but its validity still depends on the joint distribution and covariance calibration."
        ) as vo:
            self.play(FadeIn(museum_tag(r"Bliss (1935)")))
            heading=label('Bliss intervals concern log-dose and use fitted covariance',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def elsewhere(self):
        rows = fit_rows(VGroup(
            label(r"the same impossibility, \ elsewhere:", font_size=28, color=GREY_A),
            label(r"weak instruments: \ Wald intervals fail; \ Anderson--Rubin sets can be unbounded \ (Part 37; \ Dufour 1997)", font_size=24, color=CIC),
            label(r"cost-effectiveness ratios, \ relative potencies, \ the location of a maximum", font_size=24, color=CIC),
            label(r"the honest report: \ ``the data are consistent with any ratio beyond 7''", font_size=26, color=UMPC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same impossibility appears elsewhere. <bookmark mark='b'/> With weak "
            "instruments, Wald intervals for the causal effect fail, and the honest Anderson–Rubin sets of Part "
            "thirty-seven can be unbounded when the instrument contains little identifying information. Dufour's 1997"
            " impossibility results explain why uniformly valid bounded sets cannot generally solve "
            "weak-identification problems; there is no universal equivalence between one observed first-stage "
            "statistic and set shape. <bookmark mark='c'/> So too for cost-effectiveness ratios, relative potencies, "
            "and the location of a maximum. <bookmark mark='d'/> The honest report is sometimes an unbounded set: the"
            " data are consistent with any ratio beyond some value."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("ratio")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Coverage Board, a denominator of one half with standard error one. The delta "
                   "method's interval covers seventy-eight percent of the time: broken. <bookmark mark='b'/> Fieller's set, "
                   "unbounded more often than not, covers ninety-five percent: kept.",
                   [("a", [0]), ("b", [1])])
