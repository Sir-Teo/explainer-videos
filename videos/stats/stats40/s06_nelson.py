from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


class NelsonAalen(VoiceoverScene):
    def construct(self):
        self.card()
        self.estimator()
        self.plot()
        self.compare()
        self.lifetable()
        self.diagnostic()

    def card(self):
        card = chapter_card(5, r"Nelson--Aalen", r"Estimate the hazard, \ not the survival", lit=(1969, 1978), part=PART)
        with self.voiceover("Chapter five. Nelson and Aalen."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def estimator(self):
        rows = [
            cmath(r"\hat H(t)", r"=", r"\textstyle\sum_{t_k \le t} d_k / n_k", font_size=34),
            cmath(r"\widehat{\text{Var}}\, \hat H(t)", r"=", r"\textstyle\sum_{t_k \le t} d_k / n_k^2", font_size=32),
            cmath(r"e^{-\hat H}", r"\ge", r"\hat S_{\text{KM}}: \ \text{since } e^{-x} \ge 1 - x", font_size=32),
            cmath(r"\text{why}", r":", r"\text{each event adds its share } 1/n_k \text{ of the risk}", font_size=30),
        ]
        rows[0][-1].set_color(HAZC)
        whys = [why(r"Nelson (1969), \ Aalen (1978)"), why(r"Poisson-like increments"), why(r"Fleming--Harrington's $S$"),
                why(r"a sum, \ not a product")]
        with self.voiceover(
            "<bookmark mark='a'/> Wayne Nelson, an engineer studying failures of electrical equipment, proposed in 1969 "
            "to estimate the cumulative hazard directly: at each event time, add the number of events divided by the "
            "number at risk. Odd Aalen gave it its theory in 1978. <bookmark mark='b'/> Its variance is a sum of d over n "
            "squared. <bookmark mark='c'/> Exponentiating minus it gives a survival estimate that is always a little above "
            "Kaplan-Meier, since e to the minus x exceeds one minus x. <bookmark mark='d'/> The idea: each event uses up a "
            "one over n k share of the risk among those exposed."
        ) as vo:
            heading = label('Nelson-Aalen sums events divided by the risk set', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def _steps(self, ax, t, H, color, end=35.0):
        pts = [(0.0, 0.0)]
        prev = 0.0
        for a, b in zip(t, H):
            pts += [(a, prev), (a, b)]
            prev = b
        pts.append((end, prev))
        m = VMobject(stroke_color=color, stroke_width=3.5)
        m.set_points_as_corners([ax.c2p(a, min(b, 4.0)) for a, b in pts])
        return m

    def plot(self):
        d = load("gehan")
        A = axes([0, 36], [0, 4], x_length=7.4, y_length=4.2, xlabel=r"weeks", ylabel=r"cumulative hazard $\hat H(t)$",
                 xticks=[0, 10, 20, 30], yticks=[0, 1, 2, 3, 4], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        p, m = d["pl_na"], d["mp_na"]
        cp = self._steps(ax, p["t"], p["H"], PLC, end=23)
        cm = self._steps(ax, m["t"], m["H"], MPC)
        side = fit_rows(VGroup(
            label(r"placebo \ (red): \ roughly a straight line", font_size=22, color=PLC),
            label(rf"slope: \ about {p['H'][-1] / 23:.2f} per week", font_size=22, color=PLC),
            label(r"6-MP \ (green): \ a slope about a fifth of it", font_size=22, color=MPC),
            label(r"a straight line = a constant hazard", font_size=22, color=HAZC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The two arms' cumulative hazards. On placebo, the steps climb along a fairly straight "
            "line, <bookmark mark='b'/> at about " + say(p["H"][-1] / 23, 2) + " per week. <bookmark mark='c'/> On 6-MP, "
            "the line is much flatter, about a fifth as steep. <bookmark mark='d'/> A straight cumulative hazard means "
            "a constant hazard, an exponential lifetime; curvature up or down shows the hazard rising or falling, far more "
            "visibly than a survival curve does."
        ) as vo:
            self.add(gehan_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(cp), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cm), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def compare(self):
        d = load("gehan")
        m = d["mp"]
        na = d["mp_na"]
        rows = [[r"6-MP, \ week", r"$n_k$", r"$d_k$", r"KM $\hat S$", r"$e^{-\hat H}$"]]
        for i in range(min(7, len(m["t"]))):
            rows.append([f"{m['t'][i]:.0f}", f"{m['n'][i]:.0f}", f"{m['d'][i]:.0f}", f"{m['surv'][i]:.3f}", f"{np.exp(-na['H'][i]):.3f}"])
        tab = table_rows(rows, font_size=26, col_buff=0.9, row_buff=0.28, colors=[GREY_A] + [None] * (len(rows) - 1)).move_to([0, 0.5, 0])
        for r in tab[1:]:
            r[3].set_color(SURVC)
            r[4].set_color(HAZC)
        foot = label(r"close while $d_k \ll n_k$; \ they part as the risk set thins", font_size=24, color=GREY_A).move_to([0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Side by side for 6-MP, the two survival estimates are close early in follow-up, "
            "<bookmark mark='b'/> and drift apart only as the number at risk gets small. For continuous lifetimes and"
            " independent censoring, both are consistent where follow-up has support; Nelson-Aalen is the more "
            "natural for the theory, and for checking models, because it estimates the hazard, which is what models "
            "are written in."
        ) as vo:
            self.add(gehan_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def diagnostic(self):
        rows = [
            cmath(r"\text{exponential}", r":", r"H(t) = \lambda t: \ \text{a line through } 0", font_size=30),
            cmath(r"\text{Weibull}", r":", r"\log H(t) = k \log t - k \log \lambda: \ \text{a line in } \log t", font_size=30),
            cmath(r"\text{proportional hazards}", r":", r"\log H_1(t) - \log H_0(t) = \beta: \ \text{parallel curves}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{plot } \log \hat H \text{ against } \log t \text{ before fitting anything}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"constant hazard"), why(r"slope = the shape $k$"), why(r"chapter 8's assumption"), why(r"a look, \ not a test")]
        with self.voiceover(
            "<bookmark mark='a'/> That makes the cumulative hazard a diagnostic. An exponential gives a straight line "
            "through the origin. <bookmark mark='b'/> A Weibull gives a straight line when log H is plotted against log "
            "t, with slope equal to its shape. <bookmark mark='c'/> And if two groups have proportional hazards, their "
            "log cumulative hazards are parallel, a constant distance beta apart, the assumption of chapter eight. "
            "<bookmark mark='d'/> So look at log H against log t before fitting anything."
        ) as vo:
            heading = label('Cumulative hazard plots help assess model shape', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lifetable(self):
        rows = [
            cmath(r"\text{intervals } [a_j, a_{j+1})", r":", r"n_j \text{ entering}, \ d_j \text{ deaths}, \ c_j \text{ censored}", font_size=30),
            cmath(r"\hat q_j", r"=", r"d_j \big/ (n_j - c_j/2)", font_size=32),
            cmath(r"\hat S(a_{j+1})", r"=", r"\textstyle\prod_{i \le j} (1 - \hat q_i)", font_size=32),
            cmath(r"\text{as intervals shrink}", r":", r"\text{the actuarial table becomes Kaplan--Meier}", font_size=30),
        ]
        rows[1][-1].set_color(HAZC)
        whys = [why(r"grouped data"), why(r"the censored count half"), why(r"Cutler \& Ederer (1958)"), why(r"the product limit")]
        with self.voiceover(
            "<bookmark mark='a'/> Before computers, survival was computed from life tables: follow-up cut into "
            "intervals, with the numbers entering, dying and censored in each. <bookmark mark='b'/> The actuarial "
            "estimate of the chance of dying in an interval approximately counts each censored person as at risk for "
            "half of it, using a uniform-within-interval censoring approximation. <bookmark mark='c'/> Multiplying "
            "the interval survivals gives Sidney Cutler and Fred Ederer's estimator, published the same year as "
            "Kaplan and Meier's. <bookmark mark='d'/> When exact event and censoring times are available, shrink "
            "intervals so distinct event and censoring times are separated; the actuarial table becomes the "
            "product-limit estimator: the limit in its name."
        ) as vo:
            heading = label('Grouped life tables approximate within-interval exposure', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
