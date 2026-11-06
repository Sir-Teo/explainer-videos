from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


def km_axes(center=(-2.5, 0.2, 0), xlen=7.4):
    return axes([0, 36], [0, 1], x_length=xlen, y_length=4.2, xlabel=r"weeks", ylabel=r"still in remission",
                xticks=[0, 10, 20, 30], yticks=[0, 0.25, 0.5, 0.75, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                center=list(center))


class KaplanMeier(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.staircase()
        self.both()
        self.redistribute()
        self.median()

    def card(self):
        card = chapter_card(3, r"Kaplan--Meier", r"A product of conditional survivals", lit=(1958,), part=PART)
        with self.voiceover("Chapter three. Kaplan and Meier."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def derive(self):
        rows = [
            cmath(r"S(t)", r"=", r"P(T > t_1)\, P(T > t_2 \mid T > t_1) \cdots", font_size=32),
            cmath(r"P(T > t_k \mid T \ge t_k)", r"\approx", r"1 - d_k / n_k", font_size=32),
            cmath(r"\hat S(t)", r"=", r"\textstyle\prod_{t_k \le t} \big(1 - d_k / n_k\big)", font_size=34),
            cmath(r"\text{censored}", r":", r"\text{leave the risk set } n_k \text{ without a step}", font_size=30),
        ]
        rows[2][-1].set_color(SURVC)
        whys = [why(r"the chain rule of probability"), why(r"$n_k$ at risk, \ $d_k$ events"), why(r"Kaplan \& Meier (1958)"),
                why(r"their information is used up to the end")]
        with self.voiceover(
            "<bookmark mark='a'/> Edward Kaplan and Paul Meier's idea of 1958: write survival past time t as a chain of "
            "conditional survivals, past each event time given survival to it. <bookmark mark='b'/> Each factor is easy "
            "to estimate: of the n k people still at risk just before t k, d k have the event. <bookmark mark='c'/> "
            "Multiply the factors one minus d over n. That is the product-limit estimator, and it is the nonparametric "
            "maximum likelihood estimate of S. <bookmark mark='d'/> A censored patient never causes a step: they simply "
            "leave the risk set, after contributing to every factor up to the time they were last seen."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def staircase(self):
        d = load("gehan")
        t, e, g = (np.asarray(d[k], float) for k in ("time", "event", "group"))
        k = g == 1
        A = km_axes()
        ax = A.ax
        K = KMStaircase(ax, t[k], e[k].astype(int), color=MPC)
        curve, ticks = K.curve(), K.ticks()
        people = K.people(-3.15, -5.8, 0.8)
        km = d["mp"]
        side = fit_rows(VGroup(
            label(r"6-MP: \ 21 patients", font_size=22, color=MPC),
            label(rf"week 6: \ $n = {int(km['n'][0])}$, \ $d = {int(km['d'][0])}$: \ $\times (1 - 3/21)$", font_size=22),
            label(rf"week 7: \ $n = {int(km['n'][1])}$ \ (one censored at 6): \ $\times (1 - 1/17)$", font_size=22),
            label(r"grey ticks: \ censored; \ no step", font_size=22, color=CENSC),
            label(rf"the curve ends at {km['surv'][-1]:.3f}, \ not at zero", font_size=22, color=TAUC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The KM staircase, built step by step for the twenty-one patients on 6-MP. Below the "
            "plot, each patient is a dot in order of their time, red for a relapse, grey for censored. <bookmark mark='b'/> "
            "At week six, three of the twenty-one relapse: the curve drops by the factor one minus three over twenty-one. "
            "<bookmark mark='c'/> One patient is censored at six, so at week seven only seventeen are at risk, and one "
            "relapse multiplies by one minus one over seventeen. <bookmark mark='d'/> The grey ticks mark censorings: no "
            "step, just a smaller risk set afterwards. <bookmark mark='e'/> The curve ends at " + say(km["surv"][-1], 3)
            + ", not at zero, because the longest times are censored."
        ) as vo:
            self.add(gehan_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(people), FadeIn(side[0]))
            vo.wait_until("b")
            d0 = K.drop(0)
            self.play(FadeIn(d0), FadeIn(side[1]))
            vo.wait_until("c")
            d1 = K.drop(1)
            self.play(FadeOut(d0), FadeIn(d1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeOut(d1), Create(curve), run_time=3)
            self.play(FadeIn(ticks), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def both(self):
        d = load("gehan")
        t, e, g = (np.asarray(d[k], float) for k in ("time", "event", "group"))
        A = km_axes()
        ax = A.ax
        K1 = KMStaircase(ax, t[g == 1], e[g == 1].astype(int), color=MPC)
        K0 = KMStaircase(ax, t[g == 0], e[g == 0].astype(int), color=PLC)
        side = fit_rows(VGroup(
            label(r"red: \ placebo; \ green: \ 6-MP", font_size=22),
            label(rf"median remission: \ {d['pl']['median']:.0f} weeks vs {d['mp']['median']:.0f}", font_size=22, color=TAUC),
            label(r"the curves separate from the start", font_size=22, color=GREY_A),
            label(r"chapter 7 asks: \ could chance do this?", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Both arms. On placebo, red, the curve falls to zero by week twenty-three. On 6-MP, "
            "green, it falls slowly and stays above a third. <bookmark mark='b'/> The median remission is "
            + str(round(d["pl"]["median"])) + " weeks on placebo and " + str(round(d["mp"]["median"])) + " on the drug. "
            "<bookmark mark='c'/> The curves separate from the first weeks. <bookmark mark='d'/> Whether chance could "
            "produce such a gap is chapter seven's question."
        ) as vo:
            self.add(gehan_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(K0.curve()), Create(K1.curve()), FadeIn(K1.ticks()), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def redistribute(self):
        d = load("gehan")
        rd = d["rd"]
        hist = np.asarray(rd["history"], float)
        order = np.asarray(rd["order"], int)
        t = np.asarray(d["time"], float)[np.asarray(d["group"]) == 1][order]
        e = np.asarray(d["event"], int)[np.asarray(d["group"]) == 1][order]
        n = len(t)
        x0, w = -5.6, 11.2
        xs = x0 + (np.arange(n) + 0.5) * w / n
        base = -1.6
        scale = min(18.0, 3.4 / float(hist.max()))

        def bars(row):
            g = VGroup()
            for i in range(n):
                h = max(row[i] * scale, 0.001)
                g.add(Rectangle(width=w / n * 0.8, height=h, stroke_width=0, fill_color=EVTC if e[i] else CENSC,
                                fill_opacity=0.85).move_to([xs[i], base + h / 2, 0]))
            return g

        labels = VGroup(*[MathTex(f"{int(v)}" + ("" if ev else "^+"), font_size=20, color=EVTC if ev else CENSC).move_to([x, base - 0.3, 0])
                          for x, v, ev in zip(xs, t, e)])
        B = bars(np.full(n, 1 / n))
        first_c = int(np.flatnonzero(e == 0)[0])
        side = fit_rows(VGroup(
            label(r"start: \ each patient holds mass 1/21", font_size=24),
            label(r"a censored patient passes its mass equally to everyone to its right", font_size=24, color=CENSC),
            label(r"the final masses on the relapses are the KM drops", font_size=24, color=TAUC),
        ), 12.4, 0.25, [0, 2.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Bradley Efron gave another way to see the estimator in 1967. Give each of the twenty-one "
            "patients, in order of time, an equal share of probability. <bookmark mark='b'/> When we reach a censored "
            "patient, we know their lifetime lies somewhere to the right, so pass their share equally to everyone later. "
            "<bookmark mark='c'/> When all the censored shares have been passed on, the mass sitting on each relapse is "
            "exactly the Kaplan-Meier drop there. Redistribute to the right, and the product-limit estimator appears; the "
            "mass left on the last censored patients is the curve's final height."
        ) as vo:
            self.add(gehan_tag())
            vo.wait_until("a")
            self.play(FadeIn(B), FadeIn(labels), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            self.play(Transform(B, bars(hist[first_c])), run_time=1.5)
            vo.wait_until("c")
            for i in np.flatnonzero(e == 0)[1:]:
                self.play(Transform(B, bars(hist[i])), run_time=0.5)
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def median(self):
        d = load("gehan")
        rows = [
            cmath(r"\hat t_{1/2}", r"=", r"\min\{t: \hat S(t) \le 1/2\}", font_size=32),
            cmath(r"\text{6-MP}", r":", rf"\hat t_{{1/2}} = {d['mp']['median']:.0f} \text{{ weeks}}, \ \ \text{{95\% CI from }} {d['mp']['median_ci'][0]:.0f} \text{{ to beyond 35}}", font_size=30),
            cmath(r"\text{placebo}", r":", rf"\hat t_{{1/2}} = {d['pl']['median']:.0f}, \ \ \text{{95\% CI }} {d['pl']['median_ci'][0]:.0f}\text{{--}}{d['pl']['median_ci'][1]:.0f}", font_size=30),
            cmath(r"\text{mean}", r":", r"\text{not estimable when the curve never reaches } 0", font_size=30),
        ]
        rows[1][-1].set_color(MPC)
        whys = [why(r"read across at one half"), why(r"Brookmeyer \& Crowley (1982)"), why(r"invert the band"),
                why(r"so: \ the restricted mean, \ chapter 10")]
        with self.voiceover(
            "<bookmark mark='a'/> The median is read off where the curve first reaches one half. <bookmark mark='b'/> On "
            "6-MP it is " + str(round(d["mp"]["median"])) + " weeks, and its confidence interval, from the times where "
            "the curve's band crosses one half, runs from " + str(round(d["mp"]["median_ci"][0])) + " weeks to beyond the end "
            "of the data. <bookmark mark='c'/> On placebo it is " + str(round(d["pl"]["median"])) + ", from "
            + str(round(d["pl"]["median_ci"][0])) + " to " + str(round(d["pl"]["median_ci"][1])) + ". <bookmark mark='d'/> "
            "The mean cannot be estimated at all when the curve stops above zero, because the tail is unknown: chapter ten's "
            "restricted mean is the fix."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
