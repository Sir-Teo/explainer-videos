from __future__ import annotations

import numpy as np

from videos.stats.stats42.common import *  # noqa: F403


def houses(center, n=5, s=0.42, treated=None, color=PROGC):
    """A village of n x n houses; ``treated`` the indices that get the programme."""
    g = VGroup()
    treated = set(treated or [])
    for i in range(n):
        for j in range(n):
            k = i * n + j
            on = k in treated
            g.add(Square(side_length=s * 0.7, stroke_color=color if on else GREY_B, stroke_width=2,
                         fill_color=color if on else GREY_E, fill_opacity=0.85 if on else 0.4)
                  .move_to(np.array(center) + np.array([(j - (n - 1) / 2) * s, ((n - 1) / 2 - i) * s, 0])))
    return g


class TrialUnit(VoiceoverScene):
    def construct(self):
        self.card()
        self.estimand()
        self.unit()
        self.cornfield()
        self.pilot()
        self.icc()
        self.planning()

    def card(self):
        card = chapter_card(1, r"Case 1: \ what to randomize", r"Who gets the programme, \ and who decides?", lit=(1978,), part=PART)
        with self.voiceover("Chapter one. The first case: a trial to design. What should be randomized?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def estimand(self):
        rows = [
            cmath(r"Y_{ij}(z)", r":", r"\text{adult } i \text{ in town } j, \text{ a year on, with } (z = 1) \text{ or without the programme}", font_size=28),
            cmath(r"\tau", r"=", r"\tfrac{1}{J} \textstyle\sum_j \big[\bar Y_j(1) - \bar Y_j(0)\big]", font_size=34),
            cmath(r"\tau_{\text{people}}", r"=", r"\textstyle\sum_j \tfrac{N_j}{N} \big[\bar Y_j(1) - \bar Y_j(0)\big]", font_size=32),
            cmath(r"\delta", r"=", r"4 \text{ mm Hg: the smallest effect that would pay for itself}", font_size=30),
        ]
        rows[1][-1].set_color(CASE1)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"potential outcomes, \ Part 35"), why(r"the town-average effect"), why(r"or the person-average"),
                why(r"the ministry's number")]
        with self.voiceover(
            "<bookmark mark='a'/> First, the question has to become an estimand. Write Y i j of z for the pressure of"
            " adult i in town j a year from now, with the programme, z equal to one, or without it. <bookmark "
            "mark='b'/> The ministry would roll the programme out town by town, so the natural target is the "
            "town-average effect: over the island's towns, the change in a town's mean pressure. <bookmark mark='c'/>"
            " One could instead weight towns by population, which asks about the average person; with towns as "
            "unequal as the World's, the two can differ, and the protocol must say which. <bookmark mark='d'/> And "
            "the ministry's economists supply the most important number in any sample size calculation: the smallest "
            "effect worth detecting. A fall of four millimetres would pay for the health workers in strokes avoided. "
            "That is the planning threshold for this illustrative cost model, not a universal cutoff for useful "
            "effects."
        ) as vo:
            heading = label('Choose the town-average or person-average target before designing', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def unit(self):
        g = np.random.default_rng(42)
        tr = list(g.choice(25, 12, replace=False))
        v1 = houses([-4.2, 0.4, 0], treated=tr)
        v2 = houses([0.0, 0.4, 0], treated=range(25))
        v3 = houses([4.2, 0.4, 0], treated=[])
        arrows = VGroup()
        for k in tr[:6]:
            src = v1[k].get_center()
            nb = [m for m in (k - 1, k + 1, k - 5, k + 5) if 0 <= m < 25 and m not in tr]
            for m in nb[:1]:
                arrows.add(Arrow(src, v1[m].get_center(), buff=0.12, color=S.ACCENT, stroke_width=3, max_tip_length_to_length_ratio=0.35))
        cap = VGroup(
            label(r"households randomized", font_size=24, color=GREY_A).next_to(v1, DOWN, buff=0.35),
            label(r"a programme town", font_size=24, color=PROGC).next_to(v2, DOWN, buff=0.35),
            label(r"a control town", font_size=24, color=GREY_A).next_to(v3, DOWN, buff=0.35),
        )
        rows = fit_rows(VGroup(
            label(r"within a town, \ advice travels: \ the controls are contaminated, \ the contrast diluted", font_size=24, color=S.ACCENT),
            label(r"so the unit of randomization is the town: \ the programme is delivered to towns", font_size=24, color=CASE1),
        ), 12.4, 0.3, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Next, what to randomize. The cheapest-looking design randomizes households within "
            "each town: half get visits, half don't, and every town contributes both. <bookmark mark='b'/> But health"
            " workers talk to neighbours, neighbours talk to each other, and a town's shops and clinics change for "
            "everyone. Under this beneficial spillover story, controls also receive some benefit and the direct "
            "contrast is diluted. Interference need not always bias a contrast towards zero. In the language of Part "
            "thirty-five, the no-interference assumption fails inside a town. <bookmark mark='c'/> So we randomize "
            "whole towns to estimate the effect of this delivery policy, assuming negligible spillovers between "
            "towns: some with the programme <bookmark mark='d'/> and some without. That choice costs precision, as we"
            " will see, but it buys an answer to the question actually asked."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(v1), FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(v2), FadeIn(cap[1]))
            vo.wait_until("d")
            self.play(FadeIn(v3), FadeIn(cap[2]), FadeIn(rows[1]))
        self.clear_scene()

    def cornfield(self):
        hc = history_card(1978, r"Jerome Cornfield, \ \emph{Randomization by group: \ a formal analysis}",
                          r"in the \emph{American Journal of Epidemiology}, \ on community trials of heart disease prevention: "
                          r"towns, \ schools and workplaces randomized whole",
                          color=CASE1, width=11.4, font_size=23).move_to([0, 1.4, 0])
        q = VGroup(
            label(r"``Randomization by group accompanied by an analysis appropriate to", font_size=27),
            label(r"randomization by individual is an exercise in self-deception,", font_size=27),
            label(r"however, \ and should be discouraged.''", font_size=27),
        ).arrange(DOWN, buff=0.2).move_to([0, -1.5, 0])
        q[1].set_color(NAIVEC)
        with self.voiceover(
            "<bookmark mark='a'/> Randomizing towns is an old idea in heart disease prevention. In 1978 Jerome Cornfield, "
            "who had helped build the case that smoking causes lung cancer, wrote a short paper on randomizing by group, prompted by "
            "the community trials of the time. <bookmark mark='b'/> Its last sentence is the most quoted in the field. "
            "Randomization by group accompanied by an analysis appropriate to randomization by individual is an exercise in "
            "self-deception, however, and should be discouraged. We will measure exactly how much self-deception."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in q], lag_ratio=0.5), run_time=4.0)
        self.clear_scene()

    def pilot(self):
        d = load("pilot")
        means = np.asarray(d["town_means"])
        A = axes([112, 136], [0, 0.13], x_length=7.4, y_length=4.4, xlabel=r"a town's mean pressure in the pilot, \ mm Hg",
                 ylabel=r"density", xticks=[115, 120, 125, 130, 135], yticks=[0, 0.05, 0.1], center=[-2.5, 0.2, 0])
        ax = A.ax
        h, e = np.histogram(means, bins=24, range=(112, 136), density=True)
        bars = bars_at(ax, (e[:-1] + e[1:]) / 2, h, e[1] - e[0], TOWNC, opacity=0.7)
        xs = np.linspace(112, 136, 200)
        sd0 = d["sd_within"] / np.sqrt(30)
        null = curve(ax, xs, np.exp(-0.5 * ((xs - d["mean"]) / sd0) ** 2) / (sd0 * np.sqrt(2 * np.pi)), GREY_A, 3)
        sd1 = float(means.std(ddof=1))
        fit = curve(ax, xs, np.exp(-0.5 * ((xs - d["mean"]) / sd1) ** 2) / (sd1 * np.sqrt(2 * np.pi)), CASE1, 4)
        side = fit_rows(VGroup(
            label(r"200 towns \ $\times$ \ 30 adults", font_size=24),
            label(rf"SD within a town: \ {d['sd_within']:.1f} mm Hg", font_size=24, color=GREY_A),
            label(rf"if towns did not differ: \ town means SD {sd0:.2f}", font_size=24, color=GREY_A),
            label(rf"they do: \ town means SD {sd1:.2f}", font_size=24, color=CASE1),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> How much do towns differ? The ministry's pilot measured thirty adults in each of the "
            f"two hundred towns. Here are the two hundred town means. <bookmark mark='b'/> Within a town, pressures vary with "
            f"a standard deviation of about {d['sd_within']:.0f} millimetres. <bookmark mark='c'/> If towns did not differ at all, "
            f"the mean of thirty would vary with standard deviation sixteen over root thirty, about three: the grey curve. "
            f"<bookmark mark='d'/> The real town means are more spread out, with standard deviation {say(sd1, 1)}. The extra "
            f"spread is the towns' own differences: water, diet, the clinic down the road."
        ) as vo:
            self.play(FadeIn(A), FadeIn(pilot_tag()))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(null), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(fit), FadeIn(side[3]))
        self.clear_scene()

    def icc(self):
        d = load("pilot")
        lo, hi = d["icc_ci"]
        rows = [
            cmath(r"\text{MSB}", r"=", rf"m \cdot \widehat{{\text{{Var}}}}(\bar y_j) = {d['msb']:.1f}, \ \ \text{{MSW}} = {d['msw']:.1f}", font_size=32),
            cmath(r"\hat\sigma_b^2", r"=", rf"(\text{{MSB}} - \text{{MSW}}) / m = ({d['msb']:.1f} - {d['msw']:.1f}) / 30 = {d['s2b']:.2f}", font_size=32),
            cmath(r"\hat\rho", r"=", rf"\frac{{\hat\sigma_b^2}}{{\hat\sigma_b^2 + \hat\sigma_w^2}} = \frac{{{d['s2b']:.2f}}}{{{d['s2b']:.2f} + {d['msw']:.1f}}} = {d['icc']:.3f}", font_size=32),
            cmath(r"90\% \text{ CI}", r":", rf"[{lo:.3f}, \ {hi:.3f}] \ \ \text{{(resampling towns)}}", font_size=32),
        ]
        rows[2][-1].set_color(CASE1)
        whys = [why(r"one-way ANOVA, \ Part 25"), why(r"$E[\text{MSB}] = \sigma_w^2 + m \sigma_b^2$"), why(r"the intraclass correlation"),
                why(r"a bootstrap over towns")]
        with self.voiceover(
            f"<bookmark mark='a'/> The one-way analysis of variance of Part twenty-five turns that spread into a number. The "
            f"mean square between towns, thirty times the variance of the town means, is {d['msb']:.0f}; the mean square "
            f"within is {d['msw']:.0f}. <bookmark mark='b'/> The between mean square estimates the within variance plus m times "
            f"the between variance, so the between-town variance is their difference over thirty: {say(d['s2b'], 1)}. "
            f"<bookmark mark='c'/> The intraclass correlation is the towns' share of the total variance: {say(d['icc'], 3)}. Two "
            f"adults from the same town are correlated about three hundredths. <bookmark mark='d'/> Resampling whole towns "
            f"gives a ninety percent interval from {say(lo, 3)} to {say(hi, 3)}. A small number, and a poorly known one."
        ) as vo:
            heading = label('ANOVA separates within- and between-town variation', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def planning(self):
        d = load("pilot")
        s = load("size")
        rows = fit_rows(VGroup(
            label(rf"the pilot's estimate: \ $\hat\rho = {d['icc']:.3f}$, \ up to {d['icc_ci'][1]:.3f}", font_size=26, color=CASE1),
            label(r"a design must survive the bad end of what we don't know", font_size=26, color=GREY_A),
            label(r"and towns drift between the pilot and the trial, \ adding between-town variance", font_size=26, color=GREY_A),
            label(rf"planning value: \ $\rho = {s['icc']:.3f}$, \ $\sigma = {s['sigma']:.1f}$ mm Hg, \ $\delta = 4$ mm Hg", font_size=28, color=S.ACCENT),
            label(rf"the World's truth, \ revealed: \ {d['true_icc']:.3f} in the pilot year, \ {d['trial_icc']:.3f} in the trial year", font_size=24, color=EXACT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Which value should the plan use? The pilot says {say(d['icc'], 3)}, but its interval reaches "
            f"{say(d['icc_ci'][1], 3)}. <bookmark mark='b'/> A design should survive the bad end of what we don't know, because "
            f"an underpowered trial wastes everything spent on it. <bookmark mark='c'/> And a year passes between the pilot and "
            f"the trial, during which towns change in their own ways, which adds variance between towns. <bookmark mark='d'/> So "
            f"we plan with an intraclass correlation of {say(s['icc'], 3)}, a total standard deviation of sixteen and a half, "
            f"and the ministry's four millimetres. <bookmark mark='e'/> Only the World knows the truth, and it rewards the "
            f"caution: {say(d['true_icc'], 3)} in the pilot year, and {say(d['trial_icc'], 3)} in the year of the trial, almost "
            f"exactly the planning value. The pilot's estimate alone would have left the trial short of towns."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
