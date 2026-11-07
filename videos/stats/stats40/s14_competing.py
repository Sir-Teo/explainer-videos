from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


class Competing(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.cif()
        self.mgus()
        self.world()
        self.two_models()
        self.mgus_models()

    def card(self):
        card = chapter_card(13, r"Competing risks", r"When another event gets there first", lit=(1999,), part=PART)
        with self.voiceover("Chapter thirteen. Competing risks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = fit_rows(VGroup(
            label(r"MGUS: \ a harmless-looking protein in the blood, \ found in older adults", font_size=26),
            label(r"some progress to myeloma or a related cancer; \ most die of something else first", font_size=26, color=TAUC),
            label(r"a death is not a censoring: \ that patient can never progress", font_size=26, color=MISSC),
            label(r"1 $-$ KM gives net risk; causal elimination of other causes needs assumptions", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Monoclonal gammopathy of undetermined significance, MGUS, is an abnormal protein in"
            " the blood, common in older adults. <bookmark mark='b'/> A few patients progress to multiple myeloma or "
            "a related cancer; most die of something else first. <bookmark mark='c'/> A death is not a censoring: "
            "right censoring leaves later progression unknown, while death prevents it for ever. <bookmark mark='d'/>"
            " So one minus the Kaplan-Meier curve, treating deaths as censored, gives a net-risk quantity constructed"
            " from the observed cause-specific hazard. Interpreting it as a causal risk in a world where nobody dies "
            "of anything else requires extra assumptions about eliminating the competing cause."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def cif(self):
        rows = [
            cmath(r"h_k(t)", r"=", r"\lim P(t \le T < t + \delta, \text{cause } k \mid T \ge t)/\delta", font_size=30),
            cmath(r"F_k(t)", r"=", r"\textstyle\int_0^t S(u-)\, h_k(u)\, du", font_size=32),
            cmath(r"\hat F_k(t)", r"=", r"\textstyle\sum_{t_j \le t} \hat S(t_j-)\, d_{kj} / n_j", font_size=32),
            cmath(r"\textstyle\sum_k F_k(t)", r"=", r"1 - S(t)", font_size=32),
        ]
        rows[2][-1].set_color(CIFC)
        whys = [why(r"the cause-specific hazard"), why(r"the cumulative incidence"), why(r"Aalen--Johansen (1978)"), why(r"they add up")]
        with self.voiceover(
            "<bookmark mark='a'/> Each cause k has its own cause-specific hazard. <bookmark mark='b'/> The chance of "
            "failing from cause k by time t, the cumulative incidence, integrates that hazard against the chance of having "
            "survived everything until then. <bookmark mark='c'/> Its estimate, by Odd Aalen and Søren Johansen, sums "
            "the cause-k events over the risk sets, each weighted by the all-cause Kaplan-Meier just before. <bookmark "
            "mark='d'/> The incidences of all the causes add up to one minus the all-cause survival, as probabilities of "
            "a real world should."
        ) as vo:
            heading = label('Cumulative incidence accounts for every competing cause', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def _steps(self, ax, t, F, color, end):
        pts = [(0.0, 0.0)]
        prev = 0.0
        for a, b in zip(t, F):
            if a > end:
                break
            pts += [(a, prev), (a, b)]
            prev = b
        pts.append((end, prev))
        m = VMobject(stroke_color=color, stroke_width=3)
        m.set_points_as_corners([ax.c2p(a, b) for a, b in pts])
        return m

    def mgus(self):
        d = load("competing")
        t = np.asarray(d["t"], float)
        A = axes([0, 30], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"years from diagnosis", ylabel=r"cumulative probability",
                 xticks=[0, 10, 20, 30], yticks=[0, 0.25, 0.5, 0.75, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        c1 = self._steps(ax, t, np.asarray(d["cif1"], float), CIFC, 30)
        c2 = self._steps(ax, t, np.asarray(d["cif2"], float), GREY_B, 30)
        cn = self._steps(ax, t, np.asarray(d["naive1"], float), MISSC, 30)
        side = fit_rows(VGroup(
            label(rf"Mayo Clinic: \ {d['n']:,} patients, \ median age {d['median_age']:.0f}", font_size=22),
            label(rf"{d['n_prog']} progressed; \ {d['n_death']} died first", font_size=22, color=GREY_A),
            label(rf"grey: \ death without progression \ ({100 * d['at20']['cif2']:.0f}\% by 20 years)", font_size=22, color=GREY_B),
            label(rf"purple: \ progression, \ Aalen--Johansen: \ {100 * d['at20']['cif1']:.0f}\% by 20 years", font_size=22, color=CIFC),
            label(rf"red: \ 1 $-$ KM: \ {100 * d['at20']['naive1']:.0f}\% by 20, \ {100 * d['at30']['naive1']:.0f}\% by 30", font_size=22, color=MISSC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Robert Kyle's Mayo Clinic cohort: " + f"{d['n']:,}" + " patients with MGUS, with a "
            "median age of " + str(round(d["median_age"])) + ". <bookmark mark='b'/> " + str(d["n_prog"]) + " progressed; "
            + str(d["n_death"]) + " died without progressing. <bookmark mark='c'/> Death without progression climbs to "
            + str(round(100 * d["at20"]["cif2"])) + " percent by twenty years. <bookmark mark='d'/> The cumulative incidence "
            "of progression reaches " + str(round(100 * d["at20"]["cif1"])) + " percent by twenty years. <bookmark "
            "mark='e'/> One minus Kaplan-Meier says " + str(round(100 * d["at20"]["naive1"])) + " percent by twenty and "
            + str(round(100 * d["at30"]["naive1"])) + " by thirty: double, and more. This net-risk construction removes competing deaths from the risk set instead of counting them as outcomes that preclude progression."
        ) as vo:
            self.add(mgus_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(c1), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(cn), FadeIn(side[4]))
        self.clear_scene()

    def world(self):
        d = load("competing")["world"]
        grid = np.asarray(d["grid"], float)
        A = axes([0, 15], [0, 0.2], x_length=7.4, y_length=4.2, xlabel=r"years", ylabel=r"cumulative incidence",
                 xticks=[0, 5, 10, 15], yticks=[0, 0.05, 0.1, 0.15, 0.2], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        ct1 = polyline(ax, grid, np.asarray(d["true1"], float), TRUEC, 3)
        ca1 = polyline(ax, grid, np.asarray(d["aj1"], float), CIFC, 3)
        cn1 = polyline(ax, grid, np.asarray(d["naive1"], float), MISSC, 3)
        side = fit_rows(VGroup(
            label(r"the World's cohort: \ cardiovascular death", font_size=22),
            label(rf"gold: \ the truth \ ({100 * d['true1'][-1]:.1f}\% by 15 years)", font_size=22, color=TRUEC),
            label(rf"purple: \ Aalen--Johansen \ ({100 * d['aj1'][-1]:.1f}\%)", font_size=22, color=CIFC),
            label(rf"red: \ 1 $-$ KM \ ({100 * d['naive1'][-1]:.1f}\%)", font_size=22, color=MISSC),
            label(r"the bias grows with the competing hazard", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the World's cohort, where deaths from other causes compete with cardiovascular "
            "death, the truth is known. <bookmark mark='b'/> Fifteen-year cardiovascular mortality is " + say(100 * d["true1"][-1], 1)
            + " percent. <bookmark mark='c'/> Aalen-Johansen recovers it. <bookmark mark='d'/> One minus Kaplan-Meier "
            "overstates it, <bookmark mark='e'/> by less than for MGUS, because here the competing hazard is smaller; the "
            "bias grows with it."
        ) as vo:
            self.add(cohort_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ct1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ca1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cn1), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def two_models(self):
        rows = [
            cmath(r"\text{cause-specific Cox}", r":", r"h_k(t \mid x) = h_{0k}(t) e^{x^\top \beta_k}", font_size=30),
            cmath(r"\text{answers}", r":", r"\text{does } x \text{ change the rate of } k \text{ among those alive?}", font_size=30),
            cmath(r"\text{Fine--Gray}", r":", r"\tilde h_k(t \mid x) = \tilde h_{0k}(t) e^{x^\top \tilde\beta_k}, \ \ \tilde h_k = \tfrac{dF_k/dt}{1 - F_k}", font_size=28),
            cmath(r"\text{answers}", r":", r"\text{does } x \text{ change the chance of } k \text{ actually happening?}", font_size=30),
        ]
        rows[2][-1].set_color(CIFC)
        whys = [why(r"censor the other causes"), why(r"cause-specific association"), why(r"Fine \& Gray (1999)"), why(r"prognosis")]
        with self.voiceover(
            "<bookmark mark='a'/> Two regressions answer two questions. A cause-specific Cox model treats the other "
            "causes as censoring, <bookmark mark='b'/> and asks whether a covariate changes the rate of this event "
            "among people still alive: an association among those still event-free, not by itself a causal statement "
            "about mechanism. <bookmark mark='c'/> Jason Fine and Robert Gray's model of 1999 puts proportional "
            "hazards on the subdistribution, keeping those who died of other causes in the risk set with weights, "
            "<bookmark mark='d'/> and asks whether the covariate changes the chance that the event actually happens: "
            "a question about prognosis. They can disagree, and both can be right."
        ) as vo:
            heading = label('Cause-specific and subdistribution hazards answer different questions', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mgus_models(self):
        d = load("competing")
        cs, fg, cs2 = d["cs"], d["fg"], d["cs2"]
        rows = [[r"MGUS, \ per decade of age", r"HR", r"95\% CI"],
                [r"death \ (cause-specific)", f"{np.exp(cs2['beta'][1]):.2f}", f"{np.exp(cs2['beta'][1] - 1.96 * cs2['se'][1]):.2f}--{np.exp(cs2['beta'][1] + 1.96 * cs2['se'][1]):.2f}"],
                [r"progression \ (cause-specific)", f"{np.exp(cs['beta'][1]):.2f}", f"{np.exp(cs['beta'][1] - 1.96 * cs['se'][1]):.2f}--{np.exp(cs['beta'][1] + 1.96 * cs['se'][1]):.2f}"],
                [r"progression \ (Fine--Gray)", f"{np.exp(fg['beta'][1]):.2f}", f"{np.exp(fg['beta'][1] - 1.96 * fg['se'][1]):.2f}--{np.exp(fg['beta'][1] + 1.96 * fg['se'][1]):.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.2, row_buff=0.36, colors=[GREY_A, GREY_B, SURVC, CIFC]).move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"age speeds progression a little among the living, \ but older patients progress less often:", font_size=24, color=TAUC),
            label(r"they die of something else first; FG intervals use 399 patient bootstraps", font_size=24, color=TAUC),
        ), 12.4, 0.2, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the MGUS data, each decade of age at diagnosis multiplies the death rate by "
            + say(np.exp(cs2["beta"][1]), 2) + ". <bookmark mark='b'/> Its cause-specific effect on progression is "
            + say(np.exp(cs["beta"][1]), 2) + ": among the living, older patients progress at least as fast. <bookmark "
            "mark='c'/> But the Fine-Gray hazard ratio is " + say(np.exp(fg["beta"][1]), 2) + ": older patients are less likely ever to progress, because death comes first. The cause-specific "
            "coefficient describes the observed event rate; the subdistribution coefficient concerns cumulative "
            "incidence and is not an ordinary risk ratio. Neither establishes biology or causation. The second can "
            "help with what to tell a patient."
        ) as vo:
            self.add(mgus_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(foot))
        self.clear_scene()
