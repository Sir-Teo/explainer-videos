from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403

COLS = [MISSC, Y0C, TAUC]


class VAR(VoiceoverScene):
    def construct(self):
        self.card()
        self.data()
        self.model()
        self.granger()
        self.irf_()
        self.fevd()
        self.lesson()

    def card(self):
        card = chapter_card(10, r"VARs and Granger causality", r"Several series, \ each forecasting the others", lit=(1969, 1980), part=PART)
        with self.voiceover("Chapter ten. Vector autoregressions, and Granger causality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def data(self):
        d = load("var")
        t, Y = np.asarray(d["t"], float), np.asarray(d["Y"], float)
        A = axes([1959, 2010], [-10, 16], x_length=10.0, y_length=4.2, xlabel=r"year", ylabel=r"percent",
                 xticks=[1960, 1970, 1980, 1990, 2000, 2010], yticks=[-5, 0, 5, 10, 15], xfmt=lambda v: f"{v:.0f}", center=[0, 0.4, 0])
        lines = VGroup(*[series_line(A.ax, t, Y[:, k], COLS[k], 2) for k in range(3)])
        foot = label(r"red: \ inflation; \ blue: \ unemployment; \ gold: \ the 3-month Treasury-bill rate", font_size=24,
                     color=GREY_A).move_to([0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Three US quarterly series, 1959 to 2009: inflation, unemployment, and the three-month "
            "Treasury-bill rate, which tracks the Federal Reserve's policy. <bookmark mark='b'/> They move together: the "
            "inflation of the 1970s, the high interest rates of the early 1980s that ended it, the recessions that followed. "
            "Which drives which?"
        ) as vo:
            self.add(macro_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.4), FadeIn(foot), run_time=4.0)
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"Y_t", r"=", r"c + A_1 Y_{t-1} + \cdots + A_p Y_{t-p} + u_t, \quad u_t \sim (0, \Sigma)", font_size=30),
            cmath(r"\text{fit}", r":", r"\text{least squares, \ one equation at a time}", font_size=30),
            cmath(r"\text{Granger}", r":", r"x \not\to y \iff \text{lags of } x \text{ have zero coefficients in } y\text{'s equation}", font_size=28),
            cmath(r"\text{impulse response}", r":", r"\Psi_s P, \ \ \Sigma = PP^\top \ \text{(Cholesky: \ an ordering)}", font_size=28),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"every variable on every lag"), why(r"Sims (1980)"), why(r"Granger (1969)"), why(r"identification by ordering")]
        with self.voiceover(
            "<bookmark mark='a'/> A vector autoregression regresses each series on lags of all the series. <bookmark "
            "mark='b'/> Christopher Sims proposed it in 1980, in a paper called Macroeconomics and Reality, as an "
            "alternative to large models with what he called incredible restrictions. It is fitted by least squares, "
            "one equation at a time. <bookmark mark='c'/> Clive Granger's definition of 1969: x Granger-causes y if "
            "past x helps forecast y, given past y and the other included series; in a correctly specified linear "
            "VAR, an F test on x's lags in y's equation. <bookmark mark='d'/> Impulse responses trace how a shock to "
            "one variable moves all of them over time. Since the shocks are correlated, isolating one needs a "
            "decision: the Cholesky factorization assumes an ordering, in which later variables react to earlier ones"
            " within the quarter but not the reverse."
        ) as vo:
            intro=label('VAR restrictions concern prediction; causal shocks need identification',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def granger(self):
        d = load("var")
        G = d["granger"]
        keys = ["inflation -> unemployment", "inflation -> T-bill rate", "unemployment -> inflation",
                "unemployment -> T-bill rate", "T-bill rate -> inflation", "T-bill rate -> unemployment"]
        rows = [[r"does the past of \ldots", r"\ldots help forecast", r"$F$", r"$p$"]]
        cols = [GREY_A]
        for k in keys:
            a, b = k.split(" -> ")
            rows.append([a, b, f"{G[k]['F']:.2f}", f"{G[k]['p']:.3f}"])
            cols.append(BANDC if G[k]["p"] < 0.05 else GREY_B)
        tab = table_rows(rows, font_size=24, col_buff=0.8, row_buff=0.28, colors=cols).move_to([0, 0.6, 0])
        foot = label(r"VAR(4), conventional model-based F tests; green $p<0.05$ is unadjusted; persistence may affect validity",
                     font_size=22, color=GREY_A).move_to([0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A VAR with four lags, a year of quarters. <bookmark mark='b'/> Inflation helps forecast "
            "unemployment and the T-bill rate; unemployment helps forecast the T-bill rate, as a central bank reacting to the "
            "economy would; and the T-bill rate helps forecast inflation. <bookmark mark='c'/> Unemployment does not help "
            "forecast inflation here, and the rate does not significantly help forecast unemployment. <bookmark mark='d'/> "
            "Granger causality is a statement about forecasting. A variable can Granger-cause another because both respond, "
            "at different speeds, to a third, or because people act today on what they expect tomorrow."
        ) as vo:
            self.add(macro_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(tab[i]) for i in (1, 2, 4, 5)])
            vo.wait_until("c")
            self.play(*[FadeIn(tab[i]) for i in (3, 6)])
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def irf_(self):
        d = load("var")
        I, lo, hi = (np.asarray(d[k], float) for k in ("irf", "lo", "hi"))
        H = int(d["H"])
        h = np.arange(H + 1)
        panels = VGroup()
        titles = [r"inflation", r"unemployment", r"T-bill rate"]
        rng_ = [(-0.6, 1.0), (-0.3, 0.4), (-0.4, 1.2)]
        for k in range(3):
            low = min(float(lo[:, k, 2].min()), 0) - .05
            high = max(float(hi[:, k, 2].max()), 0) + .05
            A = axes([0, H], [low, high], x_length=3.6, y_length=2.8, xlabel=r"quarters", ylabel=r"",
                     xticks=[0, 10, 20], yticks=[0], center=[-4.4 + 4.4 * k, 0.4, 0])
            b = band(A.ax, h, lo[:, k, 2], hi[:, k, 2], COLS[k], 0.2)
            c = polyline(A.ax, h, I[:, k, 2], COLS[k], 3)
            z = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(H, 0), color=GREY_C, stroke_width=1.5)
            t = label(titles[k], font_size=22, color=COLS[k]).next_to(A, UP, buff=0.1)
            panels.add(VGroup(A, z, b, c, t))
        foot = fit_rows(VGroup(
            label(r"responses to a one-SD rise in the T-bill rate \ (ordering: \ inflation, \ unemployment, \ rate); \ 90\% bootstrap bands", font_size=22, color=GREY_A),
            label(r"inflation rises at first: \ the price puzzle \ (Sims 1992)", font_size=22, color=MISSC),
        ), 12.4, 0.25, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The responses to a surprise rise in the T-bill rate, interpreted as monetary "
            "tightening only under the recursive identifying assumptions, with the rate ordered last so that it can "
            "react to inflation and unemployment within the quarter. <bookmark mark='b'/> Unemployment rises, slowly,"
            " over two to three years, as textbooks say it should. <bookmark mark='c'/> But inflation rises too, at "
            "first. Sims noticed this price puzzle in 1992. The usual explanation is that the Federal Reserve raises "
            "rates when it sees inflation coming, from information the VAR does not have, so the 'shock' is partly a "
            "forecast. Adding information variables such as commodity prices has reduced the puzzle in some "
            "specifications; no such augmented fit is computed here. The identifying assumptions decide what an "
            "impulse response means."
        ) as vo:
            self.add(macro_tag())
            vo.wait_until("a")
            self.play(FadeIn(panels[2]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(FadeIn(panels[0]), FadeIn(foot[1]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"VARs: \ honest forecasting machines, \ few restrictions, \ many parameters", font_size=26, color=TAUC),
            label(r"with $k$ series and $p$ lags: \ $k^2 p$ coefficients; \ Bayesian shrinkage (the Minnesota prior)", font_size=26),
            label(r"causal claims need identification: \ orderings, \ sign restrictions, \ external instruments \ (Part 37)", font_size=26, color=MISSC),
            label(r"Sims's Nobel, \ 2011, \ shared with Thomas Sargent", font_size=24, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Vector autoregressions are honest forecasting machines with few restrictions. <bookmark "
            "mark='b'/> But their parameters multiply, the number of series squared times the number of lags, so in practice "
            "they are shrunk, Part twenty-five's idea, by priors such as Robert Litterman's Minnesota prior. <bookmark "
            "mark='c'/> Causal claims need identifying assumptions: orderings, signs of responses, or external instruments, "
            "the natural experiments of Part thirty-seven. <bookmark mark='d'/> Sims shared the 2011 Nobel prize with "
            "Thomas Sargent for empirical research on cause and effect in the macroeconomy."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def fevd(self):
        rows = fit_rows(VGroup(
            label(r"forecast-error variance decomposition: \ which shocks explain each variable's uncertainty, \ by horizon", font_size=26, color=TAUC),
            label(r"local projections \ (Jordà 2005): \ regress $y_{t+h}$ on today's shock, \ one $h$ at a time", font_size=26, color=BANDC),
            label(r"compatible identification and sufficient lag controls are needed for a common response target", font_size=26, color=GREY_A),
            label(r"both need the same thing: \ a credible shock", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two more tools. The forecast-error variance decomposition says what share of each "
            "variable's forecast uncertainty, at each horizon, comes from each identified shock. <bookmark mark='b'/>"
            " Òscar Jordà's local projections of 2005 estimate impulse responses directly, regressing the outcome h "
            "periods ahead on today's shock, one horizon at a time, without iterating a VAR. <bookmark mark='c'/> "
            "With adequate lag controls, compatible identifying assumptions and suitable regularity, the two can "
            "target the same responses asymptotically. A fixed misspecified finite VAR need not agree with local "
            "projections. <bookmark mark='d'/> Both need the same thing to mean anything causal: a credible shock."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
